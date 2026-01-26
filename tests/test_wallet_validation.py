
from http import HTTPStatus
from typing import List
import pytest
from clients.quote_client import QuoteClient
from configuration.config_manager import Config
from models.responses.wallet import Wallet
from services.currency_conversion_service import CurrencyConversionService
from utils.quote_utils import *
from utils.wallet_utils import is_wallet_balance_valid


class TestWalletValidation:
    @pytest.mark.regression
    def test_check_if_unsofficient_amount_is_handled(self, converter_service: CurrencyConversionService, quote_client: QuoteClient):
        all_wallets: List[Wallet] = converter_service.get_wallets()
        wallet_in = all_wallets[0]
        wallet_out = next(w for w in all_wallets if w.currency.code != wallet_in.currency.code)
        payload = converter_service.construct_new_quote_request(
            currency_in=wallet_in.currency.code,
            currency_out=wallet_out.currency.code,
            amount_in=wallet_in.balance + Decimal("1"),
            wallet_in_id=wallet_in.id,
            wallet_out_id=wallet_out.id,
        )
        response = quote_client.create_quote(payload)
        assert 400 <= response.status_code < 500, \
            f"Expected a client error (4xx), but received {response.status_code}"
