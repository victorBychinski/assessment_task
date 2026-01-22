

import pytest

from clients.authorization_client import AuthorizationClient
from models.token_response import TokenResponse


class TestAuthorizationClient:
    
    @pytest.mark.auth
    def test_login_valid_credentials(self, authorization_client:AuthorizationClient):
        token_response = authorization_client.init()
        
        assert isinstance(token_response, TokenResponse)
        assert token_response.access_token is not None
        assert token_response.token_type == "bearer"
        assert token_response.expiry > 0