from __future__ import annotations
from decimal import Decimal
from typing import List, Optional, Any
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field

class WalletStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    TERMINATED = "TERMINATED"

class Protocol(BaseModel):
    code: Optional[str] = None
    network: Optional[str] = None
    network_code: Optional[str] = Field(None, alias="networkCode")

class CurrencyOptions(BaseModel):
    address: Optional[str] = None
    explorer: Optional[str] = None
    transaction: Optional[str] = None
    confirmations: Optional[int] = None

class Currency(BaseModel):
    id: Optional[int] = None
    code: Optional[str] = None
    fiat: Optional[bool] = None
    icon: Optional[str] = None
    name: Optional[str] = None
    withdrawal_parameters: Optional[List[Any]] = Field(None, alias="withdrawalParameters")
    options: Optional[CurrencyOptions] = None
    withdrawal_fee: Optional[Decimal] = Field(None, alias="withdrawalFee")
    deposit_fee: Optional[Decimal] = Field(None, alias="depositFee")
    supports_deposits: Optional[bool] = Field(None, alias="supportsDeposits")
    supports_withdrawals: Optional[bool] = Field(None, alias="supportsWithdrawals")
    quantity_precision: Optional[int] = Field(None, alias="quantityPrecision")
    price_precision: Optional[int] = Field(None, alias="pricePrecision")
    protocols: Optional[List[Protocol]] = None
    
    
class Wallet(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: Optional[int] = None
    description: Optional[str] = None
    currency: Optional[Currency] = None
    status: Optional[WalletStatus] = None
    uuid: Optional[str] = None  # Common in these APIs, though not in your snippet
    lsid: Optional[str] = None

    supports_withdrawals: Optional[bool] = Field(None, alias="supportsWithdrawals")
    supports_deposits: Optional[bool] = Field(None, alias="supportsDeposits")
    supports_third_party: Optional[bool] = Field(None, alias="supportsThirdParty")
    supports_internal_bvnk_network_transfers: Optional[bool] = Field(
        None, alias="supportsInternalBvnkNetworkTransfers"
    )
    is_emoney: Optional[bool] = Field(None, alias="isEmoney")
    
    custodian_wallet: Optional[Any] = Field(None, alias="custodianWallet")
    partner: Optional[Any] = None
    supported_transfer_destinations: Optional[List[Any]] = Field(
        default_factory=list, alias="supportedTransferDestinations"
    )

    protocol: Optional[str] = None
    address: Optional[str] = None
    lookup: Optional[Any] = None

    balance: Optional[Decimal] = None
    available: Optional[Decimal] = None
    converted_available: Optional[Decimal] = Field(None, alias="convertedAvailable")
    approx_available: Optional[Decimal] = Field(None, alias="approxAvailable")
    approx_balance: Optional[Decimal] = Field(None, alias="approxBalance")
    approx_converted_available: Optional[Decimal] = Field(
        None, alias="approxConvertedAvailable"
    )

    # Fees & Alternatives
    withdrawal_fee: Optional[Decimal] = Field(None, alias="withdrawalFee")
    deposit_fee: Optional[Decimal] = Field(None, alias="depositFee")
    alternatives: Optional[List[Any]] = Field(default_factory=list)