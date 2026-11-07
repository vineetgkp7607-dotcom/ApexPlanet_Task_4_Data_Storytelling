import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "sales_cleaned.csv"
REPORT_PATH = BASE_DIR / "reports" / "hypothesis_testing_summary.txt"

# Load dataset
df = pd.read_csv(DATA_PATH)

print("=" * 55)
print("GENDER-WISE CUSTOMER SALES HYPOTHESIS TESTING")
print("=" * 55)

# Check required columns
required_columns = ["Customer_ID", "Gender", "Total_Sales"]

for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

# Remove missing values
df = df.dropna(subset=required_columns)

# Identify customers with consistent gender records
gender_counts = df.groupby("Customer_ID")["Gender"].nunique()

valid_customers = gender_counts[gender_counts == 1].index

excluded_customers = len(gender_counts) - len(valid_customers)

df = df[df["Customer_ID"].isin(valid_customers)]

# Calculate average sales per customer
customer_sales = (
    df.groupby(["Customer_ID", "Gender"])["Total_Sales"]
    .sum()
    .reset_index()
)

# Separate customer groups
male = customer_sales.loc[
    customer_sales["Gender"] == "Male", "Total_Sales"
].to_numpy()

female = customer_sales.loc[
    customer_sales["Gender"] == "Female", "Total_Sales"
].to_numpy()

# Check sample sizes
if len(male) < 2 or len(female) < 2:
    raise ValueError("Insufficient observations for statistical testing.")

# Descriptive statistics
male_mean = np.mean(male)
female_mean = np.mean(female)

difference = male_mean - female_mean

# Welch's Independent Two-Sample T-Test
t_stat, p_value = stats.ttest_ind(
    male,
    female,
    equal_var=False,
    alternative="two-sided"
)

# Calculate 95% Confidence Interval
male_var = np.var(male, ddof=1)
female_var = np.var(female, ddof=1)

se = np.sqrt(
    male_var / len(male) +
    female_var / len(female)
)

df_num = (
    male_var / len(male) +
    female_var / len(female)
) ** 2

df_den = (
    (male_var / len(male)) ** 2 / (len(male) - 1)
    +
    (female_var / len(female)) ** 2 / (len(female) - 1)
)

degrees_freedom = df_num / df_den

critical_value = stats.t.ppf(
    0.975,
    degrees_freedom
)

ci_lower = difference - critical_value * se
ci_upper = difference + critical_value * se

# Statistical decision
alpha = 0.05

if p_value < alpha:
    decision = "Reject the Null Hypothesis"
    conclusion = (
        "There is a statistically significant difference "
        "in average customer sales between male and female groups."
    )
else:
    decision = "Fail to Reject the Null Hypothesis"
    conclusion = (
        "There is insufficient statistical evidence of a "
        "difference in average customer sales between male and female groups."
    )

# Display results
results = f"""
HYPOTHESIS TESTING SUMMARY
=======================================

Business Question:
Do male and female customers differ in average sales?

Null Hypothesis (H0):
There is no difference in average customer sales.

Alternative Hypothesis (H1):
There is a difference in average customer sales.

Statistical Test:
Welch's Independent Two-Sample T-Test

Significance Level: {alpha}

DATA SUMMARY
---------------------------------------
Male Customers: {len(male)}
Female Customers: {len(female)}
Customers Excluded (Inconsistent Gender): {excluded_customers}

Male Average Sales: Rs. {male_mean:,.2f}
Female Average Sales: Rs. {female_mean:,.2f}

Mean Difference (Male - Female): Rs. {difference:,.2f}

STATISTICAL RESULTS
---------------------------------------
T-Statistic: {t_stat:.6f}
P-Value: {p_value:.8f}
Degrees of Freedom: {degrees_freedom:.2f}

95% Confidence Interval:
Lower Bound: Rs. {ci_lower:,.2f}
Upper Bound: Rs. {ci_upper:,.2f}

DECISION
---------------------------------------
{decision}

BUSINESS CONCLUSION
---------------------------------------
{conclusion}

Note:
This analysis identifies an association between gender
groups and average customer sales. It does not establish
that gender causes differences in spending.

=======================================
"""

print(results)

# Save report
REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

with open(REPORT_PATH, "w", encoding="utf-8") as file:
    file.write(results)

print(f"\nReport saved successfully: {REPORT_PATH}")