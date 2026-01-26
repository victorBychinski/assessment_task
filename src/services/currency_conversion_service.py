
from pydantic import BaseModel
from models.requests.quote_request import QuoteRequest
from clients.quote_client import QuoteClient
from clients.wallet_client import WalletClient
from decimal import Decimal
import logging
from typing import List, Any, Type, TypeVar
import httpx
from utils.types_util import validate_list
from models.responses.quote import Quote
from models.responses.wallet import Wallet

T = TypeVar("T", bound=BaseModel)

class CurrencyConversionService:
    def __init__(self, quote_client: QuoteClient, wallet_client: WalletClient, logger: logging.Logger) -> None:
        self.quote_client = quote_client
        self.wallet_client = wallet_client
        self.logger = logger
        
    def create_quote(self, currency_in:str, currency_out:str, amount_in: Decimal, wallet_in_id: int= None, wallet_out_id: int = None) -> Quote:
        if not wallet_in_id or not wallet_out_id:
            self.logger.info("Fetching wallets to detect IDs...")
            all_wallets_response = self.wallet_client.get_all_wallets(offset=0, max_count=100)
            all_wallets = all_wallets_response.json()
            
            if not wallet_in_id:
                wallet = self.__find_wallet_by_currency(all_wallets, currency_in)
                if wallet:
                    wallet_in_id = wallet.id
            if not wallet_out_id:
                wallet = self.__find_wallet_by_currency(all_wallets, currency_out)
                if wallet:
                    wallet_out_id = wallet.id
        payload = self.constract_new_quote_request(currency_in, currency_out, amount_in, wallet_in_id, wallet_out_id)
        
        response = self.quote_client.create_quote(payload)
        response.raise_for_status()
        return Quote.model_validate(response.json())
    
    def accept_quote(self, quote_uid: str) -> httpx.Response:
        return self.quote_client.accept_quote(quote_uid)
    
    def get_single_quote(self, quote_uid: str) -> Quote:
        response = self.quote_client.get_specific_quote(quote_uid)
        return self._parse_single(response, Quote)

    def get_quotes(self) -> List[Quote]:
        response = self.quote_client.get_quote()
        response.raise_for_status()
        return self._parse_list(response, Quote)

    def get_wallets(self, offset: int=0, max_count: int=100) -> List[Wallet]:
        return self.__get_all_wallets(offset, max_count)

    def get_wallet_by_id(self, wallet_id: int) -> Wallet:
        response = self.wallet_client.get_single_wallet(wallet_id)
        return self._parse_single(response, Wallet)

    def get_wallet_by_currency(self, currency: str) -> Wallet:
        all_wallets = self.__get_all_wallets()
        return self.__find_wallet_by_currency(all_wallets, currency)

    def get_wallet_balance_by_currency(self, currency: str) -> Decimal:
        all_wallets = self.__get_all_wallets()
        wallet = self.__find_wallet_by_currency(all_wallets, currency)
        return wallet.balance

    def get_current_wallet_balance(self, wallet_id: str) -> Any:
        wallet = self.get_wallet_by_id(wallet_id)
        return wallet.balance
    
    def get_quote_fee(self, quote_uid: str) -> Any:
        response = self.get_single_quote(quote_uid)
        quote = Quote(response.json())
        return quote.fee
    
    def _parse_single(self, response, model: Type[T]) -> T:
        response.raise_for_status()
        return model.model_validate(response.json())

    def _parse_list(self, response, model: Type[T]) -> List[T]:
        response.raise_for_status()
        return validate_list(model, response.json())
    
    def __get_all_wallets(self, offset: int = 0, max_count: int = 100) -> List[dict]:
        all_wallets_response = self.wallet_client.get_all_wallets(offset=offset, max_count=max_count)
        return self._parse_list(all_wallets_response, Wallet)
    
    def __find_wallet_by_currency(self, wallets: List[Wallet], currency: str) -> Wallet:
        
        wallet = next(
            (
                w
                for w in wallets
                if w.currency.code.lower() == currency.lower()
            ),
            None
        )

        if wallet is None:
            self.logger.error(f"No wallet found for currency: {currency}")
            available = [w.get("currency", {}).get("code") for w in wallets]
            
            # TODO: Custom exception for better error handling
            raise ValueError(f"No wallet found for {currency}. Available: {available}")
            
        return wallet
    


    def constract_new_quote_request( self,
    currency_in: str,
    currency_out: str,
    amount_in: Decimal,
    wallet_in_id: int,
    wallet_out_id: int,):
        self.logger.info("Constructing new quote request ...")
        quote_request = QuoteRequest(
            from_currency=currency_in,
            to_currency=currency_out,
            amount_in=amount_in,
            from_wallet=wallet_in_id,
            to_wallet=wallet_out_id
        )
        return quote_request.model_dump_json(by_alias=True, exclude_none=True)
        