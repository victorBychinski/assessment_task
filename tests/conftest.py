import pytest
import logging
from clients.api_client import ApiClient
from clients.authorization_client import AuthorizationClient
from configuration.config_manager import Config


@pytest.fixture(scope="session")
def config() -> Config:
    """
    Session-scoped fixture that provides the Config object.
    
    Returns:
        Config: Configuration manager object
    """
    return Config()


@pytest.fixture(scope="session")
def base_url(config) -> str:
    """
    Provides the base URL from configuration.
    
    Returns:
        str: Base URL for API requests
    """
    return config.base_url


@pytest.fixture(scope="session")
def service_fee(config) -> float:
    """
    Provides the service fee from configuration.
    
    Returns:
        float: Service fee percentage
    """
    return config.service_fee



@pytest.fixture(scope="session")
def logger() -> logging.Logger:
    """
    Session-scoped fixture that provides a configured logger.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    return __setup_logging()


@pytest.fixture(scope="session")
def api_client(config, logger) -> ApiClient:
    """
    Provides the API client.
    
    Returns:
        api_client: API client instance
    """
    return ApiClient(base_url=config.base_url, logger=logger)

@pytest.fixture(scope="session")
def authorization_client(api_client, logger) -> AuthorizationClient:
    """
    Provides the Authorization client.
    
    Returns:
        authorization_client: Authorization client instance
    """
    
    return AuthorizationClient(client=api_client, logger=logger)
      
      
def __setup_logging() -> logging.Logger:
    """
    Sets up logger with appropriate format and level.
    """
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_level = logging.INFO
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("tests.log")
        ]
    )
    
    return logging.getLogger(__name__)



