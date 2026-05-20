"""
Loads OList CSV files into PostgreSQL database.
Run after docker compose up and the containers are healthy. 
"""

import os
import time
import logging
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine
from dotenv import load_dotenv
from olist_analytics.handler.cursor import Connection

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/load_data.log"),
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

DATA_DIR = 'data/raw'

# Map CSV filename to table name and load order
# Load order matters -- parent tables before child tables 
TABLES = [
    ("olist_customers_dataset.csv", "olist_customers"),
    ("olist_products_dataset.csv", "olist_products"),
    ("product_category_name_translation.csv", "olist_product_category_name_translation"),
    ("olist_sellers_dataset.csv", "olist_sellers"),
    ("olist_orders_dataset.csv", "olist_orders"),
    ("olist_order_items_dataset.csv", "olist_order_items"),
    ("olist_order_payments_dataset.csv", "olist_order_payments"),
    ("olist_order_reviews_dataset.csv", "olist_order_reviews"),
    ("olist_geolocation_dataset.csv", "olist_geolocation")
]

# Columns to parse as timestamps
TIMESTAMP_COLS = {
    "olist_orders": [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ],
    "olist_order_items": ["shipping_limit_date"],
    "olist_order_reviews": [
        "review_creation_date",
        "review_answer_timestamp",
    ]
}

def wait_for_db(engine: Engine, entries: int = 5, delay: int = 3) -> None:
    """
    Wait for PostgreSQL to be ready before loading data.
    
    :param engine: SQLAlchemy engine instance
    :type engine: Engine
    :param entries: Number of retry attempts
    :type entries: int
    :param delay: Delay in seconds between retries
    :type delay: int
    """
    for attempt in range(entries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database is ready.")
            return
        except Exception as e:
            logger.warning(f"Database not ready (attempt {attempt + 1}/{entries}): {repr(e)}")
            time.sleep(delay)
    raise RuntimeError("Database is not ready after multiple attempts.")

def load_table(engine: Engine, csv_path: str, table_name: str) -> int:
    """
    Load a single CSV file into a PostgreSQL table.
    
    :param engine: SQLAlchemy engine instance
    :type engine: Engine
    :param csv_path: Path to the CSV file
    :type csv_path: str
    :param table_name: Name of the target database table
    :type table_name: str
    :returns: Number of rows loaded
    :rtype: int
    """
    logger.info(f"Loading {csv_path} into {table_name}...")
    
    parse_dates = TIMESTAMP_COLS.get(table_name, [])
    
    df = pd.read_csv(
        csv_path,
        parse_dates=parse_dates if parse_dates else False,
        low_memory=False
    )
    
    # Clean columns names -- strip whitespace to avoid issues with SQLAlchemy and PostgreSQL
    df.columns = df.columns.str.strip()

    df.to_sql(
        table_name, 
        con=engine, 
        if_exists='append',
        index=False,
        chunksize=500
    )
    
    logger.info(f"{len(df):,} rows loaded.")
    return len(df)


def main():
    engine = Connection().get_engine()
    wait_for_db(engine)

    total_rows = 0
    for csv_file, table_name in TABLES:
        csv_path = os.path.join(DATA_DIR, csv_file)

        if not os.path.exists(csv_path):
            logger.warning(f"{csv_path} not found -- skipping.")
            continue

        rows = load_table(engine, csv_path, table_name)
        total_rows += rows

    logger.info(f"Done. {total_rows:,} total rows loaded across {len(TABLES)} tables.")


if __name__ == "__main__":
    main()