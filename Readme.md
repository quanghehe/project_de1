ETL project using Airflow + DBT + Docker.

- `dags/`: Airflow DAGs
- `extract_load/`, `load_data/`: Scripts extract & load
- `transform/`: DBT models
- `docker-compose.yml`: Build docker 

## Set up
- Adjust the .env files to match your local environment
    + extract_load/.env
    + .env
    
cp .env.example .env you can use this file like example for .env

## Run 
docker-compose down

docker-compose build

docker-compose up -d

##
