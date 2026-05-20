import os
import logging
from sqlalchemy import create_engine, URL
from sqlalchemy.engine import Engine
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class Connection:
    def __init__(self):
        try:
            self.engine = create_engine(URL.create(
                drivername="postgresql+psycopg2",
                host=os.getenv("DB_HOST"),
                database=os.getenv("POSTGRES_DB"),
                port=os.getenv("POSTGRES_PORT"),
                username=os.getenv("POSTGRES_USER"),
                password=os.getenv("POSTGRES_PASSWORD"),
            ))
        except Exception as e:
            logger.error(f"Error creating DB connection engine: {repr(e)}")
            raise

    def get_engine(self) -> Engine:
        return self.engine
