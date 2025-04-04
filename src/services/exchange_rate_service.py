import requests
from functools import lru_cache


class ExchangeRateService:
    API_URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"

    @classmethod
    @lru_cache(maxsize=1)
    def get_usd_exchange_rate(cls) -> float:
        """
        Fetches the current USD to UAH exchange rate from the API.
        Returns:
            float: The current exchange rate.
        """
        response = requests.get(cls.API_URL)
        response.raise_for_status()
        data = response.json()
        for item in data:
            if item["cc"] == "USD":
                return item["rate"]
