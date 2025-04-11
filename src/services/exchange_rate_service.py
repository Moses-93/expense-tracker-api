import requests
from functools import lru_cache


class ExchangeRateService:
    """
    A service for fetching exchange rates from the National Bank of Ukraine's API.

    This service provides methods to retrieve the current exchange rate for specific currencies,
    with caching to optimize repeated requests.
    """

    API_URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"

    @lru_cache(maxsize=2)
    def _get_exchange_rate(self, currency: str) -> float:
        """
        Fetches the current exchange rate for the specified currency from the API.

        Args:
            currency (str): The currency code (e.g., "USD", "EUR") for which to fetch the exchange rate.

        Returns:
            float: The current exchange rate for the specified currency.

        Raises:
            requests.exceptions.RequestException: If the API request fails.
            KeyError: If the specified currency is not found in the API response.
        """
        response = requests.get(self.API_URL)
        response.raise_for_status()
        data = response.json()
        for item in data:
            if item["cc"] == currency:
                return item["rate"]

    def get_usd_exchange_rate(self) -> float:
        """
        Retrieves the current USD to UAH exchange rate.

        Returns:
            float: The current exchange rate from USD to UAH.
        """
        return self._get_exchange_rate("USD")

    def convert_uah_to_usd(self, amount: float) -> float:
        """
        Converts an amount from UAH to United (USD).

        Args:
            amount (float): The amount in UAH to be converted.

        Returns:
            float: The equivalent amount in USD.
        """
        return amount / self.get_usd_exchange_rate()
