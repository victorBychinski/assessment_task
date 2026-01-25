from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Union


class QuoteRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    from_currency: str = Field(None, alias="from", min_length=3)
    to_currency: str = Field(None, alias="to", min_length=3)

    from_wallet: int = Field(None, alias="fromWallet", gt=0)
    to_wallet: int = Field(None, alias="toWallet", gt=0)

    amount_in: Decimal = Field(Decimal(0), alias="amountIn")
    amount_out: Decimal = Field(Decimal(0), alias="amountOut")

    use_maximum: bool = Field(True, alias="useMaximum")
    use_minimum: bool = Field(False, alias="useMinimum")

    reference: Optional[str] = Field("test", alias="reference")
    pay_in_method: Optional[str] = Field("wallet", alias="payInMethod")
    pay_out_method: Optional[str] = Field("wallet", alias="payOutMethod")

