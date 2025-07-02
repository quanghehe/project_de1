import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import logging

load_dotenv()

print("PG_PORT:", os.getenv("PG_PORT"))
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

mysql_engine = create_engine(
    f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DB')}"
)

pg_engine = create_engine(
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

df = pd.read_sql("SELECT * FROM perfume", mysql_engine)

df.to_sql("raw_mysql_products", pg_engine, if_exists="replace", index=False)

logger.info("Loaded data into PostgreSQL!")
