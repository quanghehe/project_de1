import json
import os
import re
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import logging


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_JSON_ADOPT = os.path.join(BASE_DIR, "data", "adopt.json")
DATA_JSON_HAHROD = os.path.join(BASE_DIR, "data", "Harrods.json")
DATA_JSON_LIQUIES = os.path.join(BASE_DIR, "data", "liquides.json")

load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

env = os.getenv("ENV", "local")

if env == "docker":
    host = os.getenv("DB_HOST_DOCKER")
    port = os.getenv("DB_PORT_DOCKER")
else:
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")

DB_URI = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{host}:{port}/{os.getenv('DB_NAME')}"
engine = create_engine(DB_URI)

def extract_number(size_str):
    if size_str is None:
        return None
    match = re.match(r"(\d+(\.\d+)?)", str(size_str))
    return float(match.group(1)) if match else None

def load_json_to_db(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    existing_perfume_ids = set(pd.read_sql("SELECT id FROM perfumes", engine)['id'])
    existing_variant_keys = set(
        pd.read_sql("SELECT variant_id, perfume_id FROM variants", engine)
        .apply(lambda row: (str(row['variant_id']), str(row['perfume_id'])), axis=1)
    )

    perfumes = []
    variants = []

    for perfume in data:
        perfume_id = str(perfume.get('id'))

        if perfume_id not in existing_perfume_ids:
            perfumes.append({
                'id': perfume_id,
                'name': perfume.get('name'),
                'brand': perfume.get('brand', {}).get('name'),
                'category': perfume.get('category'),
                'gender': perfume.get('gender'),
                'url': perfume.get('url'),
            })

        for variant in perfume.get('variants', []):
            variant_id = str(variant.get('id'))
            key = (variant_id, perfume_id)

            if key not in existing_variant_keys:
                variants.append({
                    'variant_id': variant_id,
                    'perfume_id': perfume_id,
                    'price': variant.get('price'),
                    'size': extract_number(variant['size']),
                    'currency': variant.get('currency'),
                    'link': variant.get('link'),
                    'vendor': variant.get('vendor'),
                    'sku': variant.get('sku'),
                    'in_stock': variant.get('in_stock'),
                })

    if perfumes:
        pd.DataFrame(perfumes).to_sql('perfumes', engine, if_exists='append', index=False)
    if variants:
        pd.DataFrame(variants).to_sql('variants', engine, if_exists='append', index=False)

    logger.info("Loaded %s data into DB!", os.path.basename(filepath))
    
load_json_to_db(DATA_JSON_ADOPT)
load_json_to_db(DATA_JSON_HAHROD)
load_json_to_db(DATA_JSON_LIQUIES)
