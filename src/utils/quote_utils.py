from models.responses.quote import Quote
from decimal import Decimal, ROUND_HALF_UP

def is_fee_applied_on_amount_out_correct_value_valid(
    quote: Quote,
    fee_rate: float,
    *,
    precision: int = 6,
) -> bool:
    """
    Validate if the fee applied on amount_out is correct.
    Args:
        quote (Quote): A quote object.
        fee_rate (float): The fee rate applied on the quote.
        precision (int): The decimal precision for comparison.
    Returns:
        bool: True if the fee applied on amount_out is correct, False otherwise.
    """
    if fee_rate is None:
        return False

    if quote.fees is None:
        return False

    if quote.fees.percentage is None or quote.fees.value is None:
        return False

    expected_out = quote.amount_in * (Decimal(1) - Decimal(fee_rate)) * quote.price
    
    # TODO: Add configuration for rounding mode.
    quant = Decimal("1").scaleb(-precision)
    expected_out = expected_out.quantize(quant, rounding=ROUND_HALF_UP)

    return abs(quote.amount_out - expected_out) <= quant


def is_quote_pending(quote: Quote) -> bool:
    """
    Check if the quote status is PENDING.
    
    Args:
        quote (Quote): A quote object.
    Returns:
        bool: True if the quote status is PENDING, False otherwise.
    """
    return quote.quote_status == "PENDING"


def is_quote_fee_as_expected(quote: Quote, expected_fee: float) -> bool:
    """
    Check if the quote fee matches the expected fee.
    
    Args:
        quote (Quote): A quote object.
        expected_fee (float): The expected fee percentage.
    Returns:
        bool: True if the quote fee matches the expected fee, False otherwise.
    """
    return quote.fee == expected_fee


def are_quote_currencies_valid(quote: Quote, currency_in: str, currency_out: str) -> bool:
    """
    Check if the quote currencies match the expected input and output currencies.
    
    Args:
        quote (Quote): A quote object.
        currency_in (str): Expected input currency.
        currency_out (str): Expected output currency.
    Returns:
        bool: True if the quote currencies match, False otherwise.
    """
    return quote.from_currency == currency_in and quote.to_currency == currency_out