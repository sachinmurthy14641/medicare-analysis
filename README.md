# Hospital Quality Star Ratings Analysis

A data analysis project demonstrating healthcare analytics capabilities using CMS Hospital Quality Star Ratings data. This project showcases data ingestion from public APIs, cloud-based transformation in BigQuery, and visualization for hospital quality performance analysis.

## 📊 Project Overview

This repository contains code and analysis for CMS Hospital Quality Star Ratings performance visualization. The project pulls real-world healthcare quality data from the CMS API, loads it into Google BigQuery for transformation, and creates an interactive Tableau dashboard to identify performance trends and improvement opportunities across U.S. hospitals.

**Key Technologies:**
- Python (data extraction & transformation)
- CMS Data API (healthcare data source)
- Google BigQuery (cloud data warehouse)
- Pandas (data manipulation)
- Tableau Public (visualization)

## 🎯 Business Context

CMS Hospital Quality Star Ratings are critical quality metrics that:

- Measure hospital performance across mortality, safety, readmission, patient experience, and timely care
- Help patients and families compare hospitals when making care decisions
- Drive hospital quality improvement initiatives
- Range from 1 to 5 stars (5 being highest quality)

This analysis helps identify:

- Top and bottom performing hospitals
- Geographic and regional performance variations
- Domain-specific improvement opportunities (e.g., readmissions, patient experience)
- Performance tier distribution across the U.S.

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.8 or higher
python --version

# Install required packages
pip install -r requirements.txt
```

### Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/medicare-star-ratings-analysis.git
cd medicare-star-ratings-analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up Google Cloud credentials:
```bash
# Authenticate with Google Cloud
gcloud auth application-default login
```

4. Run the data pipeline:
```bash
# Step 1: Pull data from CMS API and load into BigQuery
python scripts/pull_cms_data.py

# Step 2: Transform in BigQuery and export CSV for Tableau
python scripts/transform_and_export.py
```

1. Open the Tableau workbook:

- File located in `tableau/star_ratings_dashboard.twbx`
- Or view live dashboard: [Tableau Public Link]

## 📁 Repository Structure

```
medicare-star-ratings-analysis/
├── README.md                              # This file
├── requirements.txt                       # Python dependencies
├── scripts/
│   ├── pull_cms_data.py                  # CMS API extraction → BigQuery raw load
│   ├── transform_bigquery.sql            # BigQuery transformation SQL
│   └── transform_and_export.py           # BigQuery transform + CSV export
├── data/
│   ├── raw/                              # Raw API responses (not committed)
│   │   └── hospital_quality_raw_*.json
│   └── processed/                        # Cleaned data for Tableau
│       └── hospital_quality_clean.csv
├── tableau/
│   ├── star_ratings_dashboard.twbx       # Tableau workbook
│   └── screenshots/                      # Dashboard images
│       └── dashboard_preview.png
└── .gitignore                            # Ignore raw data files
```

## 🔧 Data Pipeline

### 1. Data Extraction (`pull_cms_data.py`)

Fetches Hospital Quality Star Ratings from the CMS Data API and loads into BigQuery:

- **Endpoint:** `https://data.cms.gov/data-api/v1/dataset/xubh-q36u/data`
- **Dataset:** CMS Hospital Quality Star Ratings
- **Fields:** Facility ID/name, location, overall star rating, national comparison metrics
- **BigQuery table:** `medicare-star-ratings.cms_data.hospital_quality_raw`
- Saves a timestamped raw JSON snapshot to `data/raw/`

### 2. Data Transformation (`transform_bigquery.sql` + `transform_and_export.py`)

Runs SQL transformation in BigQuery and exports clean data for Tableau:

- Casts and cleans raw fields
- Derives `rating_category` (e.g. "4 Stars (Above Average)") and `performance_tier`
- Adds US geographic `region` from state codes
- Ranks hospitals by overall star rating
- **BigQuery table:** `medicare-star-ratings.cms_data.hospital_quality_clean`
- Exports to `data/processed/hospital_quality_clean.csv`

### 3. Visualization (Tableau)

Interactive dashboard featuring:
- **Overall Star Rating Distribution:** Bar chart showing rating frequencies
- **Performance Heatmap:** Color-coded measure performance by contract
- **Geographic Analysis:** Map view of plan performance by state
- **Trend Analysis:** Year-over-year rating changes
- **Top/Bottom Performers:** Ranked list with drill-down capability

## 📈 Key Insights

From the analysis, we can identify:

1. **Performance Distribution**
   - Majority of plans achieve 3.5-4.5 star ratings
   - Small percentage achieve 5-star status
   - Geographic clustering of high performers

2. **Measure Patterns**
   - Clinical quality measures show higher performance than patient experience
   - Diabetes care measures (HbA1c testing) consistently strong
   - Medication adherence measures show room for improvement

3. **Improvement Opportunities**
   - Focus areas for 3-3.5 star plans to reach 4+ stars
   - Specific measures driving overall rating down
   - Best practice sharing from 5-star plans

## 🛠️ Technical Details

### API Documentation

- **Source:** [CMS Data API](https://data.cms.gov/api-docs)
- **Dataset:** Hospital Quality Star Ratings (`xubh-q36u`)
- **Update Frequency:** Annual
- **Rate Limits:** None for public endpoints

### Data Schema

**Key Fields:**

- `facility_id`: Unique hospital identifier
- `facility_name`: Hospital name
- `city`, `state`, `zip_code`, `county_name`: Location fields
- `hospital_type`, `hospital_ownership`: Facility characteristics
- `overall_star_rating`: Star rating (1–5)
- `mortality_comparison`, `safety_comparison`, `readmission_comparison`, `patient_experience_comparison`, `timely_care_comparison`: National comparison metrics
- `rating_category`: Derived label (e.g., "4 Stars (Above Average)")
- `performance_tier`: High Performer / Average Performer / Needs Improvement
- `region`: US geographic region derived from state

### Dependencies

```txt
requests>=2.31.0
pandas>=2.0.0
numpy>=1.24.0
python-dotenv>=1.0.0
google-cloud-bigquery>=3.11.0
db-dtypes>=1.1.1
```

## 📊 Sample Visualizations

### Overall Star Rating Distribution
![Star Rating Distribution](tableau/screenshots/rating_distribution.png)

### Performance Heatmap by Measure
![Performance Heatmap](tableau/screenshots/heatmap.png)

## 🎓 Healthcare Analytics Skills Demonstrated

This project showcases:

- ✅ **Healthcare Domain Knowledge:** Understanding of CMS Star Ratings and hospital quality metrics
- ✅ **API Integration:** Programmatic data extraction from public healthcare APIs
- ✅ **Cloud Data Engineering:** End-to-end ETL pipeline with Google BigQuery
- ✅ **SQL Proficiency:** BigQuery transformation with CTEs, CASE logic, window functions
- ✅ **Python Proficiency:** Data ingestion, BigQuery client, pandas export
- ✅ **Data Visualization:** Tableau dashboard design for healthcare stakeholders
- ✅ **Documentation:** Clear README, code comments, reproducible analysis

## 🔮 Future Enhancements

Potential extensions to this analysis:

- [ ] Add year-over-year trend analysis with statistical significance testing
- [ ] Incorporate plan enrollment data to identify high-impact improvement areas
- [ ] Build predictive model for rating changes based on measure trends
- [ ] Add competitive benchmarking against regional peers
- [ ] Automate monthly dashboard refresh via GitHub Actions
- [ ] Integrate with additional CMS datasets (enrollment, complaints, appeals)

## 📝 Use Cases

This analysis is relevant for:

- **Health Plans:** Identify performance gaps and improvement priorities
- **Healthcare Consultants:** Benchmark client performance against market
- **Regulators:** Monitor market-wide quality trends
- **Researchers:** Analyze factors driving quality performance
- **Data Analysts:** Reference implementation for healthcare data pipelines

## 📧 Contact

**Sachin C. Murthy**
- Email: sachinmurthy14941@gmail.com
- LinkedIn: [linkedin.com/in/sachin-murthy](https://linkedin.com/in/sachin-murthy)
- Portfolio: [www.sachinmurthy.com](https://www.sachinmurthy.com)

## 📄 License

This project uses publicly available CMS data. All code is available under the MIT License.

## 🙏 Acknowledgments

- **Data Source:** Centers for Medicare & Medicaid Services (CMS)
- **API Documentation:** [data.cms.gov](https://data.cms.gov)
- **Inspiration:** Real-world healthcare analytics challenges in Medicare Advantage quality improvement

---

**Built with:** 🐍 Python • 📊 Tableau • 💾 CMS Data API • ❤️ Healthcare Analytics

*Last Updated: March 19, 2026*
