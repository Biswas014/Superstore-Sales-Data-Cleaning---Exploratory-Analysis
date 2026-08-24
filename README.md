# Superstore Sales Data Cleaning & Exploratory Analysis
A Python-based exploratory data analysis project focused on cleaning and analyzing a simulated raw Superstore sales dataset. The project examines sales, profitability, customer, product, shipping and geographical performance to identify business patterns and potential areas for improvement.

## Dataset
The dataset contains approximately 52,000 Superstore sales records covering 2011–2014, including order details, customer information, product purchases and shipping information.

Original Data Source: [Kaggle](https://www.kaggle.com/datasets/thuandao/superstore-sales-analytics)

The original dataset was structured for analysis. For this project, realistic data-quality issues were introduced to simulate a raw operational dataset and provide an opportunity to apply data-cleaning techniques.

## Tech Stack	
•	Python — Data cleaning, transformation, exploratory analysis and exporting

•	Pandas — Data exploration, cleaning and aggregation

•	NumPy — Numerical operations

•	Matplotlib & Seaborn — Data visualization

•	VS Code — Development environment

## Highlights
### Business Problem
The business cannot reliably evaluate sales and profitability because the raw dataset contains inconsistent formats, missing values, duplicate records and other data-quality issues. Reliable analysis therefore requires the data to be assessed, cleaned and standardized before examining business performance.

### Objectives
The analysis aims to answer questions such as:
•	How have revenue and profit changed year over year?
•	Which customers generated the highest revenue?
•	How does shipping time vary across shipping modes?
•	How do shipping costs vary across shipping modes?
•	Is there a discount range associated with lower profitability?
•	Which products generated the highest and lowest revenue?
•	Which countries contributed the most orders and revenue?

### Analytical Approach
1. Data Cleaning & Transformation
•	Removed unnecessary columns and duplicate records.
•	Standardized text, date, percentage and accounting formats.
•	Developed reusable functions to identify missing-value patterns and format inconsistencies.
•	Investigated whether missing values followed identifiable patterns before handling them.
•	Exported the cleaned dataset for downstream analysis.
2. Exploratory Data Analysis
•	Aggregated sales, profit, orders, customers, products, shipping and geographical data using Pandas.
•	Compared revenue and profit across years.
•	Examined customer and product performance.
•	Analyzed shipping time and shipping cost across shipping modes.
•	Investigated the relationship between discount levels and profitability.

### Key Findings
•	Total sales were $8.68M, with approximately $1.48M in total profit and a 17.05% profit margin.

•	Revenue and profit increased year over year, with 2014 generating approximately $2.95M in revenue and $505K in profit.

•	Standard Class recorded the highest average shipping time among the analyzed shipping modes.

•	Standard Class also incurred the highest shipping cost, providing an opportunity to examine the relationship between shipping cost and delivery performance.

•	Eldon File Cart generated the highest revenue among the analyzed products, while Newell 310 was among the lowest-performing products.

•	Discounts between 0% and 20% did not show an obvious negative profitability pattern in the analyzed data.

•	The United States contributed the largest share of orders among the countries analyzed, accounting for approximately 37% with 1.4M revenue out of total revenue.

### Business Implications & Recommendations
•	Shipping efficiency: Standard Class showed both higher average shipping time and higher shipping cost. The business could review carrier, fulfillment and shipping-route performance to determine whether the highest cost is justified by the service level.

•	Product performance: Products with low revenue may warrant further investigation into demand, pricing, availability or product positioning.

•	Discount strategy: The observed profitability pattern suggests that discounts up to 20% did not create an obvious negative effect in this dataset. Further analysis could examine profitability by product category and customer segment before changing discount policies.

•	Geographical performance: The strong contribution from the United States suggests that customer and product performance within this market could be examined further to identify opportunities for growth.

## Data Quality & Limitations
•	1042 records contained missing customer names. When customer-level revenue was grouped using the customer-name field, records with missing names generated 174.3K which is the highest among all the customers. Because the customer identity could not be established from the name field alone, this result was not treated as a valid customer-performance insight.

•	The project dataset was intentionally modified to introduce data-quality issues; therefore, some cleaning decisions are specific to this simulated scenario.

## Project Outcome
The project transformed a simulated raw sales dataset into a cleaner, structured dataset and used exploratory analysis to identify trends in profitability, customers, products, shipping and geographical performance. The analysis demonstrates how data preparation and exploratory analysis can support business-oriented decision making.

