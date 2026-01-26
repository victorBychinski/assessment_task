import logging
from typing import Any, Optional, Dict
from urllib.parse import urljoin
import httpx



class ApiClient:
    DEFAULT_TIMEOUT_SEC = 5.0
    def __init__(self, base_url: str, logger: logging.Logger, auth_token: str = None) -> None:
        self.base_url = base_url
        self._auth_token = auth_token
        self.logger = logger
        self.client = httpx.Client(headers=self.get_headers())
        
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, timeout: float = DEFAULT_TIMEOUT_SEC) -> httpx.Response:
        self.logger.info(f"Making GET request to {endpoint} with params {params}...")
        if params:
            self.logger.debug(f"GET {endpoint} params: {params}")
        url = urljoin(self.base_url, endpoint)
        response = self.client.get(url, params=params, timeout=timeout)
        self.logger.debug(f"GET {endpoint} response status: {response.status_code}, body: {response.text[:500]}")
        return response

    def post(self, endpoint: str, data: Optional[str | Dict[str, Any]] = None, timeout: float = DEFAULT_TIMEOUT_SEC) -> httpx.Response:
        self.logger.info(f"Making POST request to {endpoint}...")
        self.logger.debug(f"POST {endpoint} request body: {data}")
        url = urljoin(self.base_url, endpoint)
        if isinstance(data, str):
            response = self.client.post(url, data=data, timeout=timeout)
        else:
            response = self.client.post(url, json=data, timeout=timeout)
        self.logger.debug(f"POST {endpoint} response status: {response.status_code}, body: {response.text[:500]}")
        return response

    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None, timeout: float = DEFAULT_TIMEOUT_SEC) -> httpx.Response:
        self.logger.info(f"Making PUT request to {endpoint}...")
        self.logger.debug(f"PUT {endpoint} request body: {data}")
        url = urljoin(self.base_url, endpoint)
        response = self.client.put(url, json=data, timeout=timeout)
        self.logger.debug(f"PUT {endpoint} response status: {response.status_code}, body: {response.text[:500]}")
        return response

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