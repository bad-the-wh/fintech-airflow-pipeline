import logging
import requests
from requests.exceptions import RequestException

logger = logging.getLogger(__name__)

def fetch_crypto_market_data(vs_currency: str = "usd", per_page: int = 20, page: int = 1) -> list:
    """
    Fetches top cryptocurrency market data from the public CoinGecko API.
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": page,
        "sparkline": "false"
    }
    
    headers = {
        "accept": "application/json"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        logger.info(f"Successfully fetched {len(data)} records from CoinGecko API.")
        return data
    except RequestException as e:
        logger.error(f"API request failed: {e}")
        raise