from __future__ import annotations
from decimal import Decimal
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict

class MethodDisplay(BaseModel):
    id: Optional[int] = None
    display: Optional[str] = None

class PayInMethod(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    settlement_currency: Optional[str] = Field(None, alias="settlementCurrency")
    requested_currency: Optional[str] = Field(None, alias="requestedCurrency")
    estimated_exchange_rate: Optional[Decimal] = Field(None, alias="estimatedExchangeRate")
    account_methods: Optional[List[MethodDisplay]] = Field(default_factory=list, alias="accountMethods")

class PayOutMethod(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    currency: Optional[str] = None
    account_methods: Optional[List[MethodDisplay]] = Field(default_factory=list, alias="accountMethods")

class PayInLeg(BaseModel):
    id: Optional[int] = None
    amount: Optional[Decimal] = None
    date_created: Optional[int] = Field(None, alias="dateCreated")
    reference: Optional[str] = None
    currency: Optional[str] = None

class PayInInstruction(BaseModel):
    action: Optional[str] = None
    form: Optional[dict] = None
    redirect_url: Optional[str] = Field(None, alias="redirectUrl")
    display_parameters: Optional[dict] = Field(None, alias="displayParameters")

class FeeDetail(BaseModel):
    service: Optional[Decimal] = None
    processing: Optional[Decimal] = None

class Fees(BaseModel):
    percentage: Optional[FeeDetail] = None
    value: Optional[FeeDetail] = None

class Quote(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: Optional[int] = None
    from_currency: Optional[str] = Field(None, alias="from")
    to_currency: Optional[str] = Field(None, alias="to")
    amount_in: Optional[Decimal] = Field(None, alias="amountIn")
    amount_due: Optional[Decimal] = Field(None, alias="amountDue")
    amount_out: Optional[Decimal] = Field(None, alias="amountOut")
    price: Optional[Decimal] = None

    quote_status: Optional[str] = Field(None, alias="quoteStatus")
    payment_status: Optional[str] = Field(None, alias="paymentStatus")
    type: Optional[str] = None
    
    acceptance_expiry_date: Optional[int] = Field(None, alias="acceptanceExpiryDate")
    acceptance_date: Optional[int] = Field(None, alias="acceptanceDate")
    payment_expiry_date: Optional[int] = Field(None, alias="paymentExpiryDate")
    payment_receipt_date: Optional[int] = Field(None, alias="paymentReceiptDate")
    date_created: Optional[int] = Field(None, alias="dateCreated")
    last_updated: Optional[int] = Field(None, alias="lastUpdated")
    
    pay_in_legs: Optional[List[PayInLeg]] = Field(default_factory=list, alias="payInLegs")
    pay_in_method: Optional[PayInMethod]= Field(None, alias="payInMethod")
    pay_out_method: Optional[PayOutMethod] = Field(None, alias="payOutMethod")

    uuid: Optional[str] = None
    pay_out_instruction: Optional[dict] = Field(None, alias="payOutInstruction")
    pay_in_instruction: Optional[PayInInstruction] = Field(None, alias="payInInstruction")

    use_pay_in_method: Optional[MethodDisplay] = Field(None, alias="usePayInMethod")
    use_pay_out_method: Optional[MethodDisplay] = Field(None, alias="usePayOutMethod")
    
    fee: Optional[float] = None
    processing_fee: Optional[Decimal] = Field(None, alias="processingFee")
    net_price: Optional[Decimal] = Field(None, alias="netPrice")
    gross_price: Optional[Decimal] = Field(None, alias="grossPrice")
    amount_in_gross: Optional[Decimal] = Field(None, alias="amountInGross")
    amount_in_net: Optional[Decimal] = Field(None, alias="amountInNet")
    
    fees: Optional[Fees] = None