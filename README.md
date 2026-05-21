# Olist E-Commerce Analytics

![GitHub last commit](https://img.shields.io/github/last-commit/chrisandrews1012/olist-analytics)
![Python Version](https://img.shields.io/badge/python-3.11-blue)
![Stack](https://img.shields.io/badge/stack-PostgreSQL%20%7C%20SQLAlchemy%20%7C%20pandas%20%7C%20Jupyter-blue)

SQL analytics project built on the [Olist Brazilian E-Commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce), 100,000 real orders from a Brazilian marketplace between 2016 and 2018.

## Problem Statement

Raw transactional data across 8 CSVs spanning customers, orders, products, sellers, payments, reviews, and geolocation. The goal is to load it into a structured PostgreSQL database and use it as a foundation for SQL practice and analysis.

## Approach

A Python load script ingests the CSVs into Postgres in dependency order, respecting foreign key constraints. The schema is defined as plain SQL and runs automatically on container startup. Two notebooks sit on top: one for structured SQL practice building from basic queries up to window functions and CTEs, one for analysis.

## Results

## How to Run

```bash
git clone https://github.com/chrisandrews1012/olist-analytics.git
cd olist-analytics
uv sync
cp .env.template .env
```

Fill in `.env` (example values):

```
POSTGRES_USER=olist
POSTGRES_PASSWORD=olist
POSTGRES_DB=olist
POSTGRES_PORT=5432
DB_HOST=localhost
```

Download the dataset from [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) and unzip into `data/raw/`.

```bash
docker compose up -d
uv run python scripts/load_data.py
```

## File Structure

```
olist-analytics/
├── docker-compose.yml
├── pyproject.toml
├── scripts/
│   └── load_data.py
├── schema/
│   └── create_tables.sql
├── src/
│   └── olist_analytics/
│       └── handler/
│           └── cursor.py
├── notebooks/
│   ├── sql_practice.ipynb
│   └── olist_analysis.ipynb
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── external/
├── reports/
│   └── figures/
├── references/
└── tests/
```

## License

This project is licensed under the [MIT License](LICENSE).
