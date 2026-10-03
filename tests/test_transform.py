import pytest
import pandas as pd
from datetime import datetime
from include.transform import transform_crypto_data

def test_transform_crypto_data_success():
    # Mock raw API response payload
    raw_mock_data = [
        {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "current_price": "65000.50",
            "market_cap": "1200000000",
            "total_volume": "45000000",
            "high_24h": "66000.00",
            "low_24h": "64000.00",
            "price_change_percentage_24h": "2.5",
            "last_updated": "2026-06-06T12:00:00.000Z"
        }
    ]

    result = transform_crypto_data(raw_mock_data)

    assert len(result) == 1
    record = result[0]
    
    # Assert transformations applied correctly
    assert record["symbol"] == "BTC"  # Uppercase enforcement
    assert record["current_price"] == 65000.50
    assert isinstance(record["etl_transformed_at"], datetime)

def test_transform_crypto_data_missing_fields():
    # Mock data with missing numeric fields and keys
    raw_mock_data = [
        {
            "id": "unknown-coin",
            "symbol": "unk",
            "name": "Unknown",
            "current_price": None,
            "market_cap": "invalid",
        }
    ]

    result = transform_crypto_data(raw_mock_data)
    assert len(result) == 1
    record = result[0]

    # Assert fallback / default safe handling (nulls -> 0)
    assert record["current_price"] == 0.0
    assert record["market_cap"] == 0