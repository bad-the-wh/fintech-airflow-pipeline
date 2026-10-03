import logging
from datetime import datetime, timezone
import pandas as pd

logger = logging.getLogger(__name__)

def transform_crypto_data(raw_data: list) -> list:
    """
    Cleans, normalizes, and type-casts raw cryptocurrency market data.
    Returns a list of dictionaries ready for database loading.
    """
    if not raw_data:
        logger.warning("Received empty raw data payload for transformation.")
        return []

    df = pd.DataFrame(raw_data)
    
    # Define the target schema columns for our fintech warehouse
    target_columns = [
        "id", "symbol", "name", "current_price", 
        "market_cap", "total_volume", "high_24h", 
        "low_24h", "price_change_percentage_24h", "last_updated"
    ]
    
    # Filter for columns that actually exist in the response
    existing_cols = [col for col in target_columns if col in df.columns]
    df = df[existing_cols]

    # Enforce strict data types and handle missing/null values safely
    numeric_columns = [
        "current_price",
        "market_cap",
        "total_volume",
        "high_24h",
        "low_24h",
        "price_change_percentage_24h",
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
        else:
            df[col] = 0.0

    # Standardize string fields (e.g., uppercase ticker symbols)
    df["symbol"] = df["symbol"].astype(str).str.upper()
    df["name"] = df["name"].astype(str)
    df["id"] = df["id"].astype(str)

   # Parse timestamps or fallback to current UTC time
    if "last_updated" in df.columns:
        df["last_updated"] = pd.to_datetime(df["last_updated"], errors="coerce")
        df["last_updated"] = df["last_updated"].fillna(pd.Timestamp.now(timezone.utc))
    else:
        df["last_updated"] = pd.Timestamp.now(timezone.utc)

    # Inject corporate auditing metadata
    df["etl_transformed_at"] = pd.Timestamp.now(timezone.utc)

    # Convert both timestamps to ISO format strings for JSON/XCom serialization
    df["last_updated"] = df["last_updated"].astype(str)
    df["etl_transformed_at"] = df["etl_transformed_at"].astype(str)

    logger.info(f"Successfully transformed {len(df)} records into clean schema.")
    
    # Convert back to a list of dicts for Airflow XCom or database insertion
    return df.to_dict(orient="records")