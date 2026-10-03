import logging

logger = logging.getLogger(__name__)

def run_data_quality_checks(records: list):
    """
    Performs explicit data quality assertions on transformed records.
    Raises an exception to fail the Airflow task if anomalies are found.
    """
    if not records:
        raise ValueError("Data Quality Error: Dataset is completely empty!")

    for index, record in enumerate(records):
        # Check 1: Mandatory ID and Symbol presence
        if not record.get("id") or not record.get("symbol"):
            raise ValueError(f"Data Quality Error: Missing mandatory primary key at index {index}")

        # Check 2: Financial sanity check - price cannot be negative
        price = record.get("current_price", 0.0)
        if price < 0:
            raise ValueError(f"Data Quality Error: Negative price detected for coin {record.get('id')} ({price})")

    logger.info(f"Data Quality Check Passed: All {len(records)} records validated successfully.")
    return True