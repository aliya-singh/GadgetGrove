# 🛒 GadgetGrove: Miniature Customer Analytics Pipeline

**Vspark Greenfield Training - Stretch Assignment**

GadgetGrove is a miniature data engineering ecosystem that demonstrates how to bridge the gap between operational data (SQL/NoSQL) and analytical insights. This project automates the extraction of sales and sentiment data, transforms it into a clean Star Schema, and serves it through an interactive Streamlit dashboard.

---

## 🏗️ Project Structure
* `app.py`: The main entry point. A 3-stage interactive Streamlit dashboard.
* `etl_pipeline.py`: Core logic for merging SQL/NoSQL data and loading the Star Schema.
* `database_manager.py`: Handles SQLite schema creation and synthetic data generation.
* `nosql_manager.py`: Simulates a MongoDB document store using JSON-based persistence.
* `setup_sql.sql`: Raw SQL script for relational database schema initialization.
* `Dockerfile`: Configuration for containerized deployment.

---

## 🛠️ Local Setup Instructions

### 1. Prerequisites
Ensure you have **Python 3.9+** installed on your machine.

### 2. Clone and Environment Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd gadgetgrove-pipeline

# Create a virtual environment
python -m venv .venv

# Activate the environment
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

3. Running the Application
Launch the Streamlit interface:

streamlit run app.py

🚀 Pipeline Workflow
Once the app is running, use the Sidebar to navigate through the lifecycle:

Stage 1: Data Setup: Click the initialization buttons. This creates gadgetgrove.db (SQL) and mongo_reviews.json (NoSQL) with synthetic records.

Stage 2: Run ETL: Execute the pipeline. This joins the two data sources, cleans missing values, and populates the Fact and Dimension tables.

Stage 3: Analytics Dashboard: View business intelligence charts, including revenue sunbursts, satisfaction heatmaps, and top-performing products.

🐳 Docker Deployment
To run the application in an isolated container:

# Build the image
docker build -t gadgetgrove-app .

# Run the container
docker run -p 8501:8501 gadgetgrove-app
Access the dashboard at http://localhost:8501.

📊 Data Warehousing Logic
This project transitions data from an OLTP (Online Transactional Processing) model to an OLAP (Online Analytical Processing) model using a Star Schema:

dim_product_report: A dimension table for descriptive product data (Category, Name).

fact_sales_reviews: A central fact table containing metrics (Quantity, Total Price, Satisfaction Rating) and keys for rapid analysis.

🚀 Deployed Streamlit application
https://gadgetgrove.streamlit.app/