from clients.api_client import ApiClient
from typing import Any, Dict
import logging
import httpx

class WalletClient:
    def __init__(self, client: ApiClient, logger: logging.Logger, api_version: str = "v1") -> None:
        self.api_client = client
        self.logger = logger
        self.api_version = api_version

    def get_all_wallets(self, offset: int, max_count: int) -> httpx.Response:
        self.logger.info("Fetching all wallets ...")
        params = {"offset": offset, "max_count": max_count}
        return self.api_client.get("/api/wallet", params=params)

    def get_single_wallet(self, wallet_id: int) -> httpx.Response:
        self.logger.info(f"Fetching wallet with ID: {wallet_id} ...")
        return self.api_client.get(f"/api/wallet/{wallet_id}")