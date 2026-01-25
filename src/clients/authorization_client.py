import logging
from clients.api_client import ApiClient
from typing import Any, Dict
from models.token_response import TokenResponse



class AuthorizationClient:
    def __init__(self, client: ApiClient, logger: logging.Logger, api_version: str = "v1") -> None:
        self.client = client
        self.logger = logger
        self.api_version = api_version
        self._token = None

    def init(self) -> TokenResponse:
        self.logger.info("Calling init to initialize new user and get token ...")
        response = self.client.get("/init")
        result = TokenResponse(**response.json())
        self._token = result.access_token
        return result

    def echo(self, data: Dict[str, Any]) -> Dict[str, Any]:
        self.logger.info("Calling echo endpoint ...")
        response = self.client.post("/echo", data)
        return response.json()
    
    def health(self) -> Dict[str, Any]:
        self.logger.info("Calling health endpoint ...")
        response = self.client.get("/health")
        return response.json()

    def get_api_client_with_token(self) -> ApiClient:
        self.logger.info("Updating ApiClient with provided token ...")
        if self._token is None:
                self.init()
        self.client.set_auth_token(self._token)
        return self.client
    