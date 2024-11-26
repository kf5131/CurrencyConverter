import requests
from typing import Optional
import os
from dotenv import load_dotenv

class CurrencyConverter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://v6.exchangerate-api.com/v6"

    def get_exchange_rate(self, from_currency: str, to_currency: str) -> Optional[float]:
        """Get the exchange rate between two currencies."""
        try:
            url = f"{self.base_url}/{self.api_key}/pair/{from_currency}/{to_currency}"
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            data = response.json()
            return data.get("conversion_rate")
        except requests.RequestException as e:
            print(f"Error fetching exchange rate: {e}")
            return None

    def convert_currency(self, amount: float, from_currency: str, to_currency: str) -> Optional[float]:
        """Convert an amount from one currency to another."""
        if amount < 0:
            raise ValueError("Amount cannot be negative")

        rate = self.get_exchange_rate(from_currency, to_currency)
        if rate is None:
            return None
            
        return round(amount * rate, 2)

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment variables
    API_KEY = os.getenv('EXCHANGE_RATE_API_KEY')
    if not API_KEY:
        raise ValueError("API key not found. Please check your .env file.")
    
    converter = CurrencyConverter(API_KEY)
    
    try:
        # Example usage
        amount = float(input("Enter amount to convert: "))
        from_currency = input("Enter source currency code (e.g., USD): ").upper()
        to_currency = input("Enter target currency code (e.g., EUR): ").upper()
        
        result = converter.convert_currency(amount, from_currency, to_currency)
        
        if result is not None:
            print(f"{amount} {from_currency} = {result} {to_currency}")
        else:
            print("Conversion failed. Please check your inputs and try again.")
            
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
