import pytest
import logging
from clients.authorization_client import AuthorizationClient
from http import HTTPStatus
from models.responses.quote import Quote
from models.token_response import TokenResponse
from services.currency_conversion_service import CurrencyConversionService
from utils.quote_utils import *
from utils.wallet_utils import is_wallet_balance_valid


class TestE2EConversionTest:
    @pytest.mark.e2e
    @pytest.mark.parametrize(
        "amount, currency_in, currency_out",
        [(1, "ETH", "TRX"), (420, "TRX", "USDT"), (987, "TRX", "ETH")],
    )
    def test_check_if_currency_conversion_works_and_fee_applied(
        self,
        amount,
        currency_in,
        currency_out,
        converter_service: CurrencyConversionService,
        service_fee: float,
        precision: int,
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
        assert is_quote_fee_as_expected(quote_added, service_fee), f"Expected fee: {service_fee}, but got: {quote_added.fee}"
        assert are_quote_currencies_valid(quote_added, currency_in, currency_out), \
            "Quote currencies do not match the requested currencies"

        saved_quote = converter_service.get_single_quote(quote_added.uuid)

        assert is_fee_applied_on_amount_out_correct_value_valid(saved_quote, service_fee, precision=precision), \
            "Fee applied on amount_out is not correct"

        assert is_quote_pending(saved_quote), f"Quote status is {saved_quote.quote_status}"

        wallet_in_intermediate_state = converter_service.get_wallet_by_id(wallet_in.id)
        wallet_out_intermediate_state = converter_service.get_wallet_by_id(wallet_out.id)

        assert wallet_in_intermediate_state.balance == wallet_in.balance, \
            "Wallet in balance changed before quote acceptance"
        assert wallet_out_intermediate_state.balance == wallet_out.balance, \
            "Wallet out balance changed before quote acceptance"
        

        accept_quote_response = converter_service.accept_quote(quote_added.uuid)
        assert (accept_quote_response.status_code == HTTPStatus.OK), \
            f"Accept quote failed with status code: {accept_quote_response.status_code}"

        assepted_quote = converter_service.get_single_quote(quote_added.uuid)

        assert is_fee_applied_on_amount_out_correct_value_valid(assepted_quote, service_fee, precision=precision), \
            "Fee applied on amount_out is not correct"

        updated_wallet_in = converter_service.get_wallet_by_id(wallet_in.id)
        updated_wallet_out = converter_service.get_wallet_by_id(wallet_out.id)

        assert is_wallet_balance_valid
        (
            wallet_in.balance,
            updated_wallet_in.balance,
            quote_added.amount_in,
            precision,
        ), "Wallet in balance is not correct after quote acceptance"

        assert is_wallet_balance_valid
        (
            wallet_out.balance,
            updated_wallet_out.balance,
            quote_added.amount_out,
            precision,
            False,
        ), "Wallet out balance is not correct after quote acceptance"
