"""
Pull Hospital Quality Star Ratings data from CMS API and load into BigQuery.

This script:
1. Fetches Hospital Quality data from CMS Data API
2. Saves raw JSON locally for reference
3. Loads data into BigQuery raw table
"""

import requests
import json
import pandas as pd
from google.cloud import bigquery
from datetime import datetime
import os

# Configuration
PROJECT_ID = "medicare-star-ratings-490720"  # Update if your project ID is different
DATASET_ID = "cms_data"
TABLE_ID = "hospital_quality_raw"

# CMS Provider Data API endpoint for Hospital Quality Star Ratings
# Dataset: Hospital General Information (xubh-q36u)
CMS_API_URL = "https://data.cms.gov/provider-data/api/1/datastore/query/xubh-q36u/0"
PAGE_SIZE = 1000

def fetch_cms_data():
    """Fetch all Hospital Quality Star Ratings records from CMS API with pagination."""
    print("Fetching data from CMS API...")

    all_records = []
    offset = 0

    try:
        while True:
            response = requests.get(CMS_API_URL, params={"limit": PAGE_SIZE, "offset": offset})
            response.raise_for_status()

            payload = response.json()
            records = payload.get("results", [])
            all_records.extend(records)

            total = payload.get("count", 0)
            offset += len(records)

            print(f"  Fetched {offset}/{total} records...")

            if offset >= total or not records:
                break

        print(f"OK: Successfully fetched {len(all_records)} records from CMS API")
        return all_records

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Error fetching data from CMS API: {e}")
        raise

def save_raw_json(data):
    """Save raw API response as JSON for reference."""
    print("Saving raw JSON data locally...")
    
    # Create data/raw directory if it doesn't exist
    os.makedirs("data/raw", exist_ok=True)
    
    # Save with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"data/raw/hospital_quality_raw_{timestamp}.json"
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"OK: Raw data saved to: {filepath}")
    return filepath

def load_to_bigquery(data):
    """Load data into BigQuery raw table."""
    print(f"Loading data to BigQuery: {PROJECT_ID}.{DATASET_ID}.{TABLE_ID}")

    # Convert to DataFrame
    df = pd.DataFrame(data)

    print(f"   Data shape: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"   Columns: {', '.join(df.columns[:5])}..." if len(df.columns) > 5 else f"   Columns: {', '.join(df.columns)}")

    # Initialize BigQuery client
    client = bigquery.Client(project=PROJECT_ID)

    # Create dataset if it doesn't exist
    dataset_ref = bigquery.Dataset(f"{PROJECT_ID}.{DATASET_ID}")
    dataset_ref.location = "US"
    client.create_dataset(dataset_ref, exists_ok=True)
    print(f"   Dataset {DATASET_ID} ready")
    
    # Define table reference
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    
    # Configure load job
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,  # Overwrite existing data
        autodetect=True,  # Auto-detect schema
    )
    
    # Load data to BigQuery
    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    
    # Wait for job to complete
    job.result()
    
    # Get table info
    table = client.get_table(table_ref)
    print(f"OK: Successfully loaded {table.num_rows} rows to BigQuery table: {table_ref}")
    
    return table_ref

def main():
    """Main execution function."""
    print("=" * 60)
    print("CMS Star Ratings Data Pipeline - Step 1: Data Ingestion")
    print("=" * 60)
    print()
    
    try:
        # Step 1: Fetch data from CMS API
        data = fetch_cms_data()
        print()
        
        # Step 2: Save raw JSON locally
        json_filepath = save_raw_json(data)
        print()
        
        # Step 3: Load to BigQuery
        table_ref = load_to_bigquery(data)
        print()
        
        print("=" * 60)
        print("DATA INGESTION COMPLETE!")
        print("=" * 60)
        print()
        print(f"Raw JSON saved: {json_filepath}")
        print(f"BigQuery table: {table_ref}")
        print()
        print("Next steps:")
        print("1. Run: python scripts/transform_in_bigquery.py")
        print("2. Or open BigQuery console to view data")
        print()
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"ERROR: {e}")
        print("=" * 60)
        raise

if __name__ == "__main__":
    main()
