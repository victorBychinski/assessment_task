from clients.api_client import ApiClient
from typing import Any, Dict
import logging
import httpx

class QuoteClient:
    
    def __init__(self, client: ApiClient, logger: logging.Logger, api_version: str = "v1") -> None:
        self.client = client
        self.logger = logger
        self.api_version = api_version
        self.resource = "quote"
        
    def get_quote(self) -> httpx.Response:
        self.logger.info("Fetching quote ...")
        return self.client.get(f"/api/{self.api_version}/{self.resource}")

    def get_specific_quote(self, quote_uid: str) -> httpx.Response:
        self.logger.info(f"Fetching quote with UID: {quote_uid} ...")
        return self.client.get(f"/api/{self.api_version}/{self.resource}/{quote_uid}")

    def create_quote(self, data: str | Dict[str, Any]) -> httpx.Response:
        self.logger.info("Creating new quote ...")
        return self.client.post(f"/api/{self.api_version}/{self.resource}", data)
    
    def accept_quote(self, quote_uid: str) -> httpx.Response:
        self.logger.info(f"Accepting quote with ID: {quote_uid} ...")
        return self.client.put(f"/api/{self.api_version}/{self.resource}/accept/{quote_uid}")
    
    