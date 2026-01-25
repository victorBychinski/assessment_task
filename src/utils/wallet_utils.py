from decimal import Decimal, ROUND_HALF_UP

def is_wallet_balance_valid(initial_balance: Decimal, 
                     updated_balance: Decimal, 
                     amount_changed: Decimal, 
                     precision: int = 6, 
                     is_deducted: bool = True) -> bool:
    quant = Decimal("1").scaleb(-precision)

    expected = initial_balance - amount_changed if is_deducted else initial_balance + amount_changed
    expected = expected.quantize(quant, rounding=ROUND_HALF_UP)
    
    return abs(updated_balance - expected) <= quant
