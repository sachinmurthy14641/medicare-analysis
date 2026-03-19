# Medicare Star Ratings Analysis

A data analysis project demonstrating healthcare analytics capabilities using CMS Medicare Advantage and Part D Star Ratings data. This project showcases data ingestion from public APIs, data transformation, and visualization for quality measure performance analysis.

## 📊 Project Overview

This repository contains code and analysis for Medicare Star Ratings performance visualization. The project pulls real-world healthcare quality data from the CMS API, processes it for analysis, and creates an interactive Tableau dashboard to identify performance trends and improvement opportunities.

**Key Technologies:**
- Python (data extraction & transformation)
- CMS Data API (healthcare data source)
- Pandas (data manipulation)
- Tableau Public (visualization)

## 🎯 Business Context

Medicare Star Ratings are critical quality metrics that:
- Measure health plan performance on clinical quality and patient experience
- Impact plan reimbursement and bonus payments
- Guide beneficiary plan selection decisions
- Range from 1 to 5 stars (5 being highest quality)

This analysis helps identify:
- Top and bottom performing plans
- Geographic performance variations
- Measure-specific improvement opportunities
- Year-over-year performance trends

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

3. Run the data pipeline:
```bash
# Pull data from CMS API
python scripts/pull_cms_data.py

# Clean and transform data
python scripts/clean_data.py
```

4. Open the Tableau workbook:
- File located in `tableau/star_ratings_dashboard.twbx`
- Or view live dashboard: [Tableau Public Link]

## 📁 Repository Structure

```
medicare-star-ratings-analysis/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── scripts/
│   ├── pull_cms_data.py              # CMS API data extraction
│   └── clean_data.py                 # Data cleaning & transformation
├── data/
│   ├── raw/                          # Raw API responses (not committed)
│   │   └── star_ratings_raw.json
│   └── processed/                    # Cleaned data for Tableau
│       └── star_ratings_clean.csv
├── tableau/
│   ├── star_ratings_dashboard.twbx   # Tableau workbook
│   └── screenshots/                  # Dashboard images
│       └── dashboard_preview.png
└── .gitignore                        # Ignore raw data files
```

## 🔧 Data Pipeline

### 1. Data Extraction (`pull_cms_data.py`)

Pulls Medicare Star Ratings data from CMS Data API:
- **Endpoint:** CMS Medicare Part C & D Star Ratings dataset
- **Coverage:** Multiple contract years (2020-2024)
- **Records:** ~500+ Medicare Advantage contracts
- **Fields:** Contract ID, organization name, ratings, measure scores

### 2. Data Transformation (`clean_data.py`)

Processes raw API data for analysis:
- Standardizes column names
- Handles missing values
- Calculates derived metrics
- Filters for active contracts
- Exports clean CSV for Tableau

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
- **Dataset ID:** Medicare Part C & D Star Ratings
- **Update Frequency:** Annual (October release)
- **Rate Limits:** None for public endpoints

### Data Schema

**Key Fields:**
- `contract_id`: Unique plan identifier (e.g., H1234)
- `org_name`: Parent organization name
- `overall_rating`: Star rating (1-5)
- `plan_type`: MA-PD, MA-only, PDP
- `state`: Primary state of operation
- `measure_scores`: Individual HEDIS/HOS/CAHPS measure results

### Dependencies

```txt
requests>=2.31.0
pandas>=2.0.0
numpy>=1.24.0
python-dotenv>=1.0.0
```

## 📊 Sample Visualizations

### Overall Star Rating Distribution
![Star Rating Distribution](tableau/screenshots/rating_distribution.png)

### Performance Heatmap by Measure
![Performance Heatmap](tableau/screenshots/heatmap.png)

## 🎓 Healthcare Analytics Skills Demonstrated

This project showcases:

- ✅ **Healthcare Domain Knowledge:** Understanding of CMS Star Ratings, HEDIS measures, Medicare Advantage
- ✅ **API Integration:** Programmatic data extraction from public healthcare APIs
- ✅ **Data Engineering:** ETL pipeline design, data cleaning, transformation
- ✅ **SQL/Python Proficiency:** Data manipulation, aggregation, quality validation
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

*Last Updated: March 18, 2026*
