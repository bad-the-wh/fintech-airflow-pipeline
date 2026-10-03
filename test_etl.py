import logging
from include.extract import fetch_crypto_market_data
from include.transform import transform_crypto_data

# Configure logging to see what's happening
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    print("--- 1. Testing Extraction ---")
    raw_data = fetch_crypto_market_data(per_page=5)
    print(f"Fetched {len(raw_data)} coins from CoinGecko.")
    
    print("\n--- 2. Testing Transformation ---")
    transformed_data = transform_crypto_data(raw_data)
    print(f"Transformed {len(transformed_data)} records successfully.")
    
    print("\n--- Sample Transformed Record ---")
    if transformed_data:
        for key, value in transformed_data[0].items():
            print(f"  {key}: {value}")
            
    print("\nETL Logic Test Passed Successfully!")