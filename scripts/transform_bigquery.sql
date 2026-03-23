-- ============================================================================
-- CMS Hospital Quality Star Ratings Data Transformation
-- ============================================================================
-- This script transforms raw CMS Hospital Quality data into a clean format
-- suitable for Tableau visualization and analysis.
--
-- Input:  cms_data.hospital_quality_raw
-- Output: cms_data.hospital_quality_clean
-- ============================================================================

CREATE OR REPLACE TABLE `medicare-star-ratings-490720.cms_data.hospital_quality_clean` AS

WITH base_data AS (
  SELECT
    -- Hospital identifiers
    facility_id,
    facility_name,
    address,
    citytown AS city,
    state,
    zip_code,
    countyparish AS county_name,
    telephone_number AS phone_number,
    hospital_type,
    hospital_ownership,
    emergency_services,
    meets_criteria_for_birthing_friendly_designation AS birthing_friendly,

    -- Performance metrics
    CAST(hospital_overall_rating AS FLOAT64) AS overall_star_rating,

    -- Mortality measure counts
    SAFE_CAST(count_of_mort_measures_better AS INT64) AS mort_measures_better,
    SAFE_CAST(count_of_mort_measures_no_different AS INT64) AS mort_measures_same,
    SAFE_CAST(count_of_mort_measures_worse AS INT64) AS mort_measures_worse,

    -- Safety measure counts
    SAFE_CAST(count_of_safety_measures_better AS INT64) AS safety_measures_better,
    SAFE_CAST(count_of_safety_measures_no_different AS INT64) AS safety_measures_same,
    SAFE_CAST(count_of_safety_measures_worse AS INT64) AS safety_measures_worse,

    -- Readmission measure counts
    SAFE_CAST(count_of_readm_measures_better AS INT64) AS readm_measures_better,
    SAFE_CAST(count_of_readm_measures_no_different AS INT64) AS readm_measures_same,
    SAFE_CAST(count_of_readm_measures_worse AS INT64) AS readm_measures_worse,

    -- Patient experience & timely care
    SAFE_CAST(count_of_facility_pt_exp_measures AS INT64) AS pt_exp_measures_count,
    SAFE_CAST(count_of_facility_te_measures AS INT64) AS timely_care_measures_count,

    -- Metadata
    CURRENT_TIMESTAMP() AS transformed_at,
    EXTRACT(YEAR FROM CURRENT_DATE()) AS measurement_year

  FROM `medicare-star-ratings-490720.cms_data.hospital_quality_raw`
  
  WHERE 
    -- Filter for valid records
    facility_id IS NOT NULL
    AND hospital_overall_rating IS NOT NULL
    AND hospital_overall_rating != 'Not Available'
),

-- Add performance categories
categorized_data AS (
  SELECT
    *,
    
    -- Categorize star ratings
    CASE 
      WHEN overall_star_rating >= 5 THEN '5 Stars (Excellent)'
      WHEN overall_star_rating >= 4 THEN '4 Stars (Above Average)'
      WHEN overall_star_rating >= 3 THEN '3 Stars (Average)'
      WHEN overall_star_rating >= 2 THEN '2 Stars (Below Average)'
      ELSE '1 Star (Poor)'
    END AS rating_category,
    
    -- Performance tier
    CASE
      WHEN overall_star_rating >= 4.0 THEN 'High Performer'
      WHEN overall_star_rating >= 3.0 THEN 'Average Performer'
      ELSE 'Needs Improvement'
    END AS performance_tier,
    
    -- Geographic region
    CASE
      WHEN state IN ('CT', 'ME', 'MA', 'NH', 'RI', 'VT', 'NJ', 'NY', 'PA') THEN 'Northeast'
      WHEN state IN ('IL', 'IN', 'MI', 'OH', 'WI', 'IA', 'KS', 'MN', 'MO', 'NE', 'ND', 'SD') THEN 'Midwest'
      WHEN state IN ('DE', 'FL', 'GA', 'MD', 'NC', 'SC', 'VA', 'WV', 'AL', 'KY', 'MS', 'TN', 'AR', 'LA', 'OK', 'TX') THEN 'South'
      WHEN state IN ('AZ', 'CO', 'ID', 'MT', 'NV', 'NM', 'UT', 'WY', 'AK', 'CA', 'HI', 'OR', 'WA') THEN 'West'
      ELSE 'Other'
    END AS region
    
  FROM base_data
)

-- Final output
SELECT 
  *,
  -- Add row number for easy reference
  ROW_NUMBER() OVER (ORDER BY overall_star_rating DESC, facility_name) AS rank_by_rating
  
FROM categorized_data

ORDER BY overall_star_rating DESC, facility_name;

-- ============================================================================
-- Verification queries (run these after transformation)
-- ============================================================================

-- Check record counts
-- SELECT COUNT(*) as total_hospitals FROM `medicare-star-ratings-490720.cms_data.hospital_quality_clean`;

-- Rating distribution
-- SELECT 
--   rating_category,
--   COUNT(*) as hospital_count,
--   ROUND(AVG(overall_star_rating), 2) as avg_rating
-- FROM `medicare-star-ratings-490720.cms_data.hospital_quality_clean`
-- GROUP BY rating_category
-- ORDER BY avg_rating DESC;

-- Top 10 performers
-- SELECT
--   facility_name,
--   city,
--   state,
--   overall_star_rating
-- FROM `medicare-star-ratings-490720.cms_data.hospital_quality_clean`
-- ORDER BY overall_star_rating DESC
-- LIMIT 10;

-- Performance by state
-- SELECT 
--   state,
--   COUNT(*) as hospital_count,
--   ROUND(AVG(overall_star_rating), 2) as avg_rating,
--   COUNT(CASE WHEN overall_star_rating >= 4 THEN 1 END) as high_performers
-- FROM `medicare-star-ratings-490720.cms_data.hospital_quality_clean`
-- GROUP BY state
-- ORDER BY avg_rating DESC
-- LIMIT 10;

-- Performance by region
-- SELECT 
--   region,
--   COUNT(*) as hospital_count,
--   ROUND(AVG(overall_star_rating), 2) as avg_rating
-- FROM `medicare-star-ratings-490720.cms_data.hospital_quality_clean`
-- GROUP BY region
-- ORDER BY avg_rating DESC;
