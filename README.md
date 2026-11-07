# ApexPlanet Task 4: Data Storytelling & Statistical Validation

## Project Overview
This project presents business insights from a sales dataset and uses statistical hypothesis testing to validate a business question.

## Project Structure
- `data/` - Cleaned sales dataset
- `python_scripts/` - Hypothesis testing Python script
- `reports/` - Business story and hypothesis testing reports
- `presentation/` - Final PowerPoint presentation

## Key Findings
- Total recorded revenue: ₹139.40 million.
- Electronics was the highest-revenue category.
- March had the highest monthly sales (₹13.06 million).
- September had the lowest monthly sales (₹9.18 million).
- Customer segmentation identified 38 Champions and 10 At Risk customers.
- Hypothesis testing found insufficient statistical evidence of a difference in average recorded customer sales between male and female groups.

## Statistical Method
Welch's Independent Two-Sample T-Test  
Significance Level: 0.05  
Confidence Level: 95%

## Data Limitations
Some Order_ID values are reused across different customers and records. Reported order counts and AOV require validation. 34 customers with inconsistent gender records were excluded from the hypothesis test.
