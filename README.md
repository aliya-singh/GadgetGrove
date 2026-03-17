# GadgetGrove Analytics - Dockerized

This is a dockerized version of the GadgetGrove customer analytics pipeline.

## Prerequisites

- Docker and Docker Compose installed

## Quick Start

1. Clone or ensure the project files are in a directory.

2. Build and run the services:
   ```bash
   docker-compose up --build
   ```

3. Open your browser and go to `http://localhost:8501`

## Services

- **app**: Streamlit web application
- **mongo**: MongoDB database for reviews

## Data Persistence

- SQLite database (`gadgetgrove.db`) and JSON reviews (`mongo_reviews.json`) are mounted as volumes to persist data between runs.

## Architecture

The application consists of:
- **Streamlit App**: Web interface for data setup, ETL, and analytics dashboard
- **SQLite**: Relational database for orders, customers, products
- **MongoDB**: NoSQL database for customer reviews
- **ETL Pipeline**: Merges data into a star schema for analytics

## Usage

1. **Data Setup**: Initialize SQL and NoSQL data
2. **Run ETL**: Transform and load data into analytics schema
3. **Analytics Dashboard**: View insights, charts, and metrics

## Stopping

```bash
docker-compose down
```

## Volumes

- `mongo_data`: MongoDB data
- Host-mounted: `gadgetgrove.db` and `mongo_reviews.json`
