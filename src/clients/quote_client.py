from clients.api_client import ApiClient
from typing import Any, Dict
import logging

class QuoteClient:
    
    def __init__(self, client: ApiClient, logger: logging.Logger, api_version: str = "v1") -> None:
        self.client = client
        self.logger = logger
        self.api_version = api_version
        self.resource = "quote"
        
    def get_quote(self) -> Dict[str, Any]:
        self.logger.info("Fetching quote ...")
        response = self.client.get(f"/api/{self.api_version}/{self.resource}")
        return response
    
    def get_specific_quote(self, quote_id: str) -> Dict[str, Any]:
        self.logger.info(f"Fetching quote with ID: {quote_id} ...")
        response = self.client.get(f"/api/{self.api_version}/{self.resource}/{quote_id}")
        return response
    
    def create_quote(self, data: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info("Creating new quote ...")
        response = self.client.post(f"/api/{self.api_version}/{self.resource}", data)
        return response
    
    def accept_quote(self, quote_id: str) -> Dict[str, Any]:
        self.logger.info(f"Accepting quote with ID: {quote_id} ...")
        response = self.client.put(f"/api/{self.api_version}/{self.resource}/accept/{quote_id}")
        return response
    
    