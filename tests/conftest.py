from decimal import Decimal
import pytest
import logging
from clients.api_client import ApiClient
from clients.quote_client import QuoteClient
from clients.wallet_client import WalletClient
from clients.authorization_client import AuthorizationClient
from configuration.config_manager import Config
from services.currency_conversion_service import CurrencyConversionService


def pytest_addoption(parser):
    parser.addoption("--base-url", action="store", default=None, help="Base URL for the API")
    parser.addoption("--fee", action="store", default=None, help="Service fee percentage (e.g. 0.01)")
    parser.addoption( "--precision", action="store", default=None, help="Decimal precision for amounts")
    
@pytest.fixture(scope="session")
def config(request) -> Config:
    overrides = {
        "base_url": request.config.getoption("--base-url"),
        "fee": request.config.getoption("--fee"),
        "precision": request.config.getoption("--precision"),
    }
    return Config(overrides=overrides)


@pytest.fixture(scope="session")
def base_url(request, config) -> str:
    """
    Provides the base URL from configuration.
    
    Returns:
        str: Base URL for API requests
    """
    return config.base_url


@pytest.fixture(scope="session")
def service_fee(config) -> float:
    """
    Get the service fee percentage from configuration and provide it as a float.
    
    Returns:
        float: Service fee percentage
    """
    return config.service_fee / 100

@pytest.fixture(scope="session")
def precision(config) -> int:
    """
    Get the decimal precision from configuration.
    
    Returns:
        int: Decimal precision
    """
    return config.decimal_precision



@pytest.fixture(scope="session")
def logger() -> logging.Logger:
    """
    Session-scoped fixture that provides a configured logger.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    return __setup_logging()


@pytest.fixture(scope="class")
def api_client(config, logger) -> ApiClient:
    """
    Provides the API client.
    
    Returns:
        api_client: API client instance
    """
    return ApiClient(base_url=config.base_url, logger=logger)

@pytest.fixture(scope="class")
def authorization_client(api_client, logger) -> AuthorizationClient:
    """
    Provides the Authorization client.
    
    Returns:
        authorization_client: Authorization client instance
    """
    
    return AuthorizationClient(client=api_client, logger=logger)

@pytest.fixture(scope="class")
def authorized_api_client(authorization_client) -> ApiClient:
    return authorization_client.get_api_client_with_token()

@pytest.fixture(scope="class")
def quote_client(authorized_api_client, config, logger) -> QuoteClient:
    """
    Provides the Quote client.
    
    Returns:
        quote_client: Quote client instance
    """
    return QuoteClient(client=authorized_api_client, logger=logger, api_version=config.api_version)

@pytest.fixture(scope="class")
def wallet_client(authorized_api_client, config, logger) -> WalletClient:
    """
    Provides the Wallet client.
    
    Returns:
        wallet_client: Wallet client instance
    """
    return WalletClient(client=authorized_api_client, logger=logger, api_version=config.api_version)

@pytest.fixture(scope="class")
def converter_service(quote_client, wallet_client, logger) -> CurrencyConversionService:
    """
    Provides the Currency Conversion Service.
    
    Returns:
        converter_service: Currency Conversion Service instance
    """
    
    return CurrencyConversionService(quote_client=quote_client, wallet_client=wallet_client, logger=logger)

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
    logger = logging.getLogger(__name__)
    logger.info("Logger initialized.")
    return logger