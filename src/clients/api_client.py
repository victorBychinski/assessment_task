import logging
from typing import Any, Optional, Dict
from urllib.parse import urljoin
import httpx



class ApiClient:
    def __init__(self, base_url: str, logger: logging.Logger, auth_token: str = None) -> None:
        self.base_url = base_url
        self._auth_token = auth_token
        self.logger = logger
        self.client = httpx.Client(headers=self.get_headers())

    def __enter__(self) -> "ApiClient":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.client.close()

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> httpx.Response:
        self.logger.info(f"Making GET request to {endpoint} with params {params}...")
        url = urljoin(self.base_url, endpoint)
        return self.client.get(url, params=params)

    def post(self, endpoint: str, data: Optional[str | Dict[str, Any]] = None) -> httpx.Response:
        self.logger.info(f"Making POST request to {endpoint} with data {data}...")
        url = urljoin(self.base_url, endpoint)
        if isinstance(data, str):
            return self.client.post(url, data=data)
        return self.client.post(url, json=data)
     
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None) -> httpx.Response:
        self.logger.info(f"Making PUT request to {endpoint} with data {data}...")
        url = urljoin(self.base_url, endpoint)
        return self.client.put(url, json=data)

    def set_auth_token(self, token: str) -> None:
        self._auth_token = token
        self.client.close()
        self.client = httpx.Client(headers=self.get_headers())

    def get_headers(self) -> Dict[str, str]:
        # TODO: Refactor to avoid code duplication, add support for additional headers/tokens
        if self._auth_token is None:
            return {
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
        return {
            "Authorization": f"Bearer {self._auth_token}",
            "Content-Type": "application/json"
        }
        
    def clone(self) -> ApiClient:
        return ApiClient(
            base_url=self.base_url,
            logger=self.logger,
            auth_token=self._auth_token
    )