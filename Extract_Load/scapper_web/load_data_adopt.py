import json
import os
from sqlalchemy import create_engine, Table, MetaData
from dotenv import load_dotenv
import pandas as pd
import logging

#Load bien moi trg tu .env
load_dotenv()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DB_URI = f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(DB_URI)

#Load JSON
with open('Extract/data/adopt.json','r',encoding='utf-8') as f:
    data = json.load(f)
    
    perfumes = []
    variants = []
    
    for perfume in data:
        perfumes.append({
            'id': perfume['id'],
            'name': perfume['name'],
            'brand': perfume['brand']['name'],
            'category': perfume['category'],
            'gender': perfume['gender'],
            'url': perfume['url']
        })
        
        for variant in perfume['variants']:
            variants.append({
                'variant_id': variant['id'],
                'perfume_id': perfume['id'],
                'price': variant['price'],
                'size': variant['size'],
                'currency': variant['currency'],
                'link': variant['link'],
                'vendor': variant['vendor'],
                'sku': variant['sku'],
                'in_stock': variant['in_stock']
            })

# Đưa vào DB
pd.DataFrame(perfumes).to_sql('perfumes', engine, if_exists='replace', index=False)
pd.DataFrame(variants).to_sql('variants', engine, if_exists='replace', index=False)

logger.info("Loaded data into PostgreSQL!")
