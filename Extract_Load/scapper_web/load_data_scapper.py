import json
import os
import re
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import logging

DATA_JSON_ADOPT = "Extract_Load/data/adopt.json"
DATA_JSON_HAHORD = "Extract_Load/data/Harrods.json"


load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DB_URI = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DB_URI)

def extract_number(size_str):
    if size_str is None:
        return None
    match = re.match(r"(\d+(\.\d+)?)", str(size_str))
    return float(match.group(1)) if match else None

def load_json_to_db(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    perfumes = []
    variants = []

    for perfume in data:
        perfume_id = perfume.get('id')
        perfumes.append({
            'id': perfume_id,
            'name': perfume.get('name'),
            'brand': perfume.get('brand', {}).get('name'),
            'category': perfume.get('category'),
            'gender': perfume.get('gender'),
            'url': perfume.get('url'),
        })

        for variant in perfume.get('variants', []):
            variants.append({
                'variant_id': variant.get('id'),
                'perfume_id': perfume_id,
                'price': variant.get('price'),
                'size': extract_number(variant['size']),
                'currency': variant.get('currency'),
                'link': variant.get('link'),
                'vendor': variant.get('vendor'),
                'sku': variant.get('sku'),
                'in_stock': variant.get('in_stock'),
            })
            
    pd.DataFrame(perfumes).to_sql('perfumes', engine, if_exists='append', index=False)
    pd.DataFrame(variants).to_sql('variants', engine, if_exists='append', index=False)


    logger.info("Loaded %s data into DB!", os.path.basename(filepath))
load_json_to_db(DATA_JSON_ADOPT)
load_json_to_db(DATA_JSON_HAHORD)
