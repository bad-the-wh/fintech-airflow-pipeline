import logging
import os
from sqlalchemy import create_engine, text

logger = logging.getLogger(__name__)

def get_database_url() -> str:
    """
    Constructs the database connection string from environment variables 
    or falls back to our Docker Compose local data warehouse.
    """
    user = os.getenv("DW_USER", "postgres")
    password = os.getenv("DW_PASSWORD", "postgres")
    host = os.getenv("DW_HOST", "localhost")
    port = os.getenv("DW_PORT", "5432")
    dbname = os.getenv("DW_NAME", "fintech_dw")
    
    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"

def create_target_table_if_not_exists(engine):
    """
    Creates the crypto_market target table with a primary/unique constraint 
    on the coin id to allow safe UPSERT operations.
    """
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS crypto_market (
        id VARCHAR(50) PRIMARY KEY,
        symbol VARCHAR(20) NOT NULL,
        name VARCHAR(100) NOT NULL,
        current_price NUMERIC(18, 6),
        market_cap NUMERIC(20, 2),
        total_volume NUMERIC(20, 2),
        high_24h NUMERIC(18, 6),
        low_24h NUMERIC(18, 6),
        price_change_percentage_24h NUMERIC(8, 4),
        last_updated TIMESTAMP WITH TIME ZONE,
        etl_transformed_at TIMESTAMP WITH TIME ZONE
    );
    """
    with engine.begin() as connection:
        connection.execute(text(create_table_sql))
    logger.info("Ensured target table 'crypto_market' exists.")

def load_crypto_data_to_postgres(records: list):
    """
    Loads transformed records into PostgreSQL using an idempotent UPSERT query.
    """
    if not records:
        logger.warning("No records provided to load into PostgreSQL.")
        return

    engine = create_engine(get_database_url())
    create_target_table_if_not_exists(engine)

    upsert_sql = """
    INSERT INTO crypto_market (
        id, symbol, name, current_price, market_cap, 
        total_volume, high_24h, low_24h, 
        price_change_percentage_24h, last_updated, etl_transformed_at
    ) VALUES (
        :id, :symbol, :name, :current_price, :market_cap, 
        :total_volume, :high_24h, :low_24h, 
        :price_change_percentage_24h, :last_updated, :etl_transformed_at
    )
    ON CONFLICT (id) DO UPDATE SET
        current_price = EXCLUDED.current_price,
        market_cap = EXCLUDED.market_cap,
        total_volume = EXCLUDED.total_volume,
        high_24h = EXCLUDED.high_24h,
        low_24h = EXCLUDED.low_24h,
        price_change_percentage_24h = EXCLUDED.price_change_percentage_24h,
        last_updated = EXCLUDED.last_updated,
        etl_transformed_at = EXCLUDED.etl_transformed_at;
    """

    with engine.begin() as connection:
        for record in records:
            connection.execute(text(upsert_sql), record)
            
    logger.info(f"Successfully upserted {len(records)} records into PostgreSQL.")