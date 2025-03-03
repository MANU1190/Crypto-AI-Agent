import requests
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CryptoTool:
    def __init__(self):
        self.base_url = "https://api.coingecko.com/api/v3"
        self.cache = {} # Simple caching for prices
        self.last_call = 0 # For rate limiting
        self.rate_limit = 1 # 1 second between calls
        self.valid_fiat_currencies = {"usd", "eur", "inr", "gbp"} # Supported fiat currencies
        self.valid_coins = None # Will be populated dynamically

    def _fetch_valid_coins(self):
        """Fetch a list of all valid cryptocurrencies from CoinGecko."""
        if self.valid_coins is not None:
            return self.valid_coins
        try:
            url = f"{self.base_url}/coins/list"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            coins = {coin["id"].lower() for coin in response.json()}
            self.valid_coins = coins
            return coins
        except requests.RequestException as e:
            logging.error(f"Error fetching valid coins: {str(e)}")
            return f"Error fetching valid coins: {str(e)}"

    def is_valid_coin(self, coin):
        """Check if a coin is valid by querying CoinGecko dynamically."""
        if isinstance(self.valid_coins, str) and "Error" in self.valid_coins:
            return False # Fallback if CoinGecko list can't be fetched
        coins = self._fetch_valid_coins()
        if isinstance(coins, str): # Handle error case
            return False
        return coin.lower() in coins

    def get_price(self, coin="bitcoin", currency="usd"):
        """Fetch current price of a cryptocurrency."""
        # Normalize inputs to lowercase
        coin = coin.lower()
        currency = currency.lower()
        # Check cache first
        cache_key = f"{coin}_{currency}"
        if cache_key in self.cache and (time.time() - self.cache[cache_key]["timestamp"] < 60):
            return self.cache[cache_key]["price"]
        # Rate limiting
        if time.time() - self.last_call < self.rate_limit:
            time.sleep(self.rate_limit - (time.time() - self.last_call))
        # Validate coin dynamically
        if not self.is_valid_coin(coin):
            return f"Error: '{coin}' is not a recognized cryptocurrency. Please use a valid cryptocurrency (e.g., Bitcoin, Ethereum, Dogecoin)."
        # Validate currency
        if currency not in self.valid_fiat_currencies:
            return f"Error: '{currency}' is not a supported fiat currency for pricing. Please use valid currencies like USD, EUR, or INR."
        try:
            url = f"{self.base_url}/simple/price?ids={coin}&vs_currencies={currency}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            price = data.get(coin, {}).get(currency)
            if price is None:
                raise ValueError("Invalid cryptocurrency or currency")
            # Update cache
            self.cache[cache_key] = {"price": price, "timestamp": time.time()}
            self.last_call = time.time()
            return price
        except requests.RequestException as e:
            logging.error(f"Error fetching price: {str(e)}")
            return f"Error fetching price: {str(e)}"
        except ValueError as e:
            logging.error(f"Value error: {str(e)}")
            return f"Value error: {str(e)}"
        except Exception as e:
            logging.exception("An unexpected error occurred")  # Logs the full traceback
            return f"Sorry, I couldn’t process your request: {str(e)}"
