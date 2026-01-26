
from http import HTTPStatus
import pytest
from configuration.config_manager import Config
from services.currency_conversion_service import CurrencyConversionService
import time
from utils.quote_utils import *
from utils.wallet_utils import is_wallet_balance_valid, are_wallets_balances_equal


class TestQuoteProcessing:
    @pytest.mark.regression
    @pytest.mark.parametrize(
        "amount, currency_in, currency_out",
        [(1, "ETH", "TRX")],
    )
    def test_check_if_quote_processing_timeout_applied(
        self,
        amount,
        currency_in,
        currency_out,
        converter_service: CurrencyConversionService,
        config: Config,
    ):
        wallet_in = converter_service.get_wallet_by_currency(currency_in)
        wallet_out = converter_service.get_wallet_by_currency(currency_out)

        quote_added = converter_service.create_quote(
            currency_in=currency_in,
            currency_out=currency_out,
            amount_in=amount,
            wallet_in_id=wallet_in.id,
            wallet_out_id=wallet_out.id,
        )

        saved_quote = converter_service.get_single_quote(quote_added.uuid)
        assert is_quote_pending(saved_quote), f"Quote status is {saved_quote.quote_status}"
        
        time.sleep(config.quote_expiry_time_sec)
        saved_quote_after_timeout = converter_service.get_single_quote(quote_added.uuid)
        assert saved_quote_after_timeout.quote_status == "EXPIRED", \
            f"Quote status after timeout is {saved_quote_after_timeout.quote_status}, expected EXPIRED"
            
        assept_response = converter_service.accept_quote(quote_added.uuid)
        assert 400 <= assept_response.status_code < 500, \
            f"Expected a client error (4xx), but received {assept_response.status_code}"
            
        accepted_quote = converter_service.get_single_quote(quote_added.uuid)
        assert accepted_quote.quote_status == "EXPIRED", \
            f"Quote status after timeout is {accepted_quote.quote_status}, expected EXPIRED"
            
        updated_wallet_in = converter_service.get_wallet_by_id(wallet_in.id)
        updated_wallet_out = converter_service.get_wallet_by_id(wallet_out.id)  
        
        assert are_wallets_balances_equal(updated_wallet_in.balance,wallet_in.balance), \
            f"Wallet in balance changed when accepting an expired quote: expected {wallet_in.balance}, got {updated_wallet_in.balance}"
        assert are_wallets_balances_equal(updated_wallet_out.balance,wallet_out.balance), \
            f"Wallet out balance changed when accepting an expired quote: expected {wallet_out.balance}, got {updated_wallet_out.balance}"