"""
Transform Star Ratings data in BigQuery and export for Tableau.

This script:
1. Runs SQL transformations in BigQuery
2. Exports clean data to CSV for Tableau visualization
"""

from google.cloud import bigquery
import pandas as pd
import os
from datetime import datetime

# Configuration
PROJECT_ID = "medicare-star-ratings"  # Update if your project ID is different
DATASET_ID = "cms_data"
RAW_TABLE = "hospital_quality_raw"
CLEAN_TABLE = "hospital_quality_clean"

def run_transformation():
    """Execute SQL transformation in BigQuery."""
    print("🔄 Running BigQuery transformation...")
    
    # Initialize BigQuery client
    client = bigquery.Client(project=PROJECT_ID)
    
    # Read SQL file
    sql_file = "scripts/transform_bigquery.sql"
    
    if not os.path.exists(sql_file):
        print(f"⚠️  SQL file not found: {sql_file}")
        print("   Using inline transformation query instead...")
        
        # Inline transformation if SQL file doesn't exist
        query = f"""
        CREATE OR REPLACE TABLE `{PROJECT_ID}.{DATASET_ID}.{CLEAN_TABLE}` AS
        SELECT
          -- Hospital identifiers
          facility_id,
          facility_name,
          
          -- Performance metrics
          CAST(hospital_overall_rating AS FLOAT64) AS overall_star_rating,
          
          -- Geographic info
          state,
          city,
          zip_code,
          
          -- Categorize ratings
          CASE 
            WHEN CAST(hospital_overall_rating AS FLOAT64) >= 5 THEN '5 Stars'
            WHEN CAST(hospital_overall_rating AS FLOAT64) >= 4 THEN '4 Stars'
            WHEN CAST(hospital_overall_rating AS FLOAT64) >= 3 THEN '3 Stars'
            WHEN CAST(hospital_overall_rating AS FLOAT64) >= 2 THEN '2 Stars'
            ELSE '1 Star'
          END AS rating_category,
          
          -- Metadata
          CURRENT_TIMESTAMP() AS transformed_at
          
        FROM `{PROJECT_ID}.{DATASET_ID}.{RAW_TABLE}`
        WHERE facility_id IS NOT NULL
          AND hospital_overall_rating IS NOT NULL
        """
    else:
        # Read SQL from file
        with open(sql_file, 'r') as f:
            query = f.read()
    
    # Execute query
    query_job = client.query(query)
    query_job.result()  # Wait for completion
    
    # Get row count
    result = client.query(f"SELECT COUNT(*) as count FROM `{PROJECT_ID}.{DATASET_ID}.{CLEAN_TABLE}`")
    row_count = list(result)[0]['count']
    
    print(f"✅ Transformation complete: {row_count} rows in clean table")
    
    return row_count

def export_to_csv():
    """Export clean BigQuery table to CSV for Tableau."""
    print("📤 Exporting data to CSV for Tableau...")
    
    # Initialize BigQuery client
    client = bigquery.Client(project=PROJECT_ID)
    
    # Query clean table
    query = f"""
    SELECT *
    FROM `{PROJECT_ID}.{DATASET_ID}.{CLEAN_TABLE}`
    ORDER BY overall_star_rating DESC
    """
    
    # Execute query and load to DataFrame
    df = client.query(query).to_dataframe()
    
    print(f"   Retrieved {len(df)} rows with {len(df.columns)} columns")
    
    # Create output directory
    os.makedirs("data/processed", exist_ok=True)
    
    # Export to CSV
    output_file = "data/processed/hospital_quality_clean.csv"
    df.to_csv(output_file, index=False)
    
    print(f"✅ Data exported to: {output_file}")
    print(f"   File size: {os.path.getsize(output_file) / 1024:.2f} KB")
    
    # Show preview
    print("\n📊 Data preview (first 5 rows):")
    print(df.head().to_string())
    
    return output_file

def show_summary_stats():
    """Show summary statistics from BigQuery."""
    print("\n📈 Summary Statistics:")
    print("=" * 60)
    
    client = bigquery.Client(project=PROJECT_ID)
    
    # Rating distribution
    query = f"""
    SELECT 
      rating_category,
      COUNT(*) as contract_count,
      ROUND(AVG(overall_star_rating), 2) as avg_rating
    FROM `{PROJECT_ID}.{DATASET_ID}.{CLEAN_TABLE}`
    GROUP BY rating_category
    ORDER BY avg_rating DESC
    """
    
    df = client.query(query).to_dataframe()
    print("\n⭐ Rating Distribution:")
    print(df.to_string(index=False))
    
    # Top performers
    query = f"""
    SELECT 
      facility_name,
      facility_id,
      city,
      state,
      overall_star_rating
    FROM `{PROJECT_ID}.{DATASET_ID}.{CLEAN_TABLE}`
    ORDER BY overall_star_rating DESC
    LIMIT 5
    """
    
    df = client.query(query).to_dataframe()
    print("\n🏆 Top 5 Performers:")
    print(df.to_string(index=False))
    
    print("\n" + "=" * 60)

def main():
    """Main execution function."""
    print("=" * 60)
    print("CMS Star Ratings - Step 2: Transform & Export")
    print("=" * 60)
    print()
    
    try:
        # Step 1: Run transformation
        row_count = run_transformation()
        print()
        
        # Step 2: Export to CSV
        csv_file = export_to_csv()
        print()
        
        # Step 3: Show summary stats
        show_summary_stats()
        print()
        
        print("=" * 60)
        print("✅ TRANSFORMATION & EXPORT COMPLETE!")
        print("=" * 60)
        print()
        print(f"📊 BigQuery table: {PROJECT_ID}.{DATASET_ID}.{CLEAN_TABLE}")
        print(f"📁 CSV for Tableau: {csv_file}")
        print()
        print("Next steps:")
        print("1. Open Tableau Public")
        print("2. Connect to data/processed/hospital_quality_clean.csv")
        print("3. Build dashboard!")
        print()
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"❌ ERROR: {e}")
        print("=" * 60)
        import traceback
        traceback.print_exc()
        raise

if __name__ == "__main__":
    main()
