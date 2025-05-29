# Product Sales Strategy Analysis

## Project Objective

The objective of this project is to analyze the effectiveness of three distinct sales approaches used to promote a newly launched product line at Pens and Printers. The Sales team needs insights to inform the executive team on which sales method yields the best results with consideration for both effectiveness and resource investment.

As part of this analysis, we aim to:
- Quantify customer reach across methods
- Understand revenue distribution overall and by method
- Evaluate changes in revenue over time by method
- Recommend a preferred sales strategy based on data
- Identify any contextual customer differences that could influence results

## Business Context

Pens and Printers Inc is a B2B office product retailer founded in 1984, known for building long-term relationships with large organizations. As the company adapts to modern buying behavior, it launched a new line of office stationery focused on creative tools for brainstorming. 

To support this launch, three sales approaches were tested over six weeks:
1. **Email Only** – Two campaign emails; minimal team effort.
2. **Phone Call Only** – 30-minute personalized sales calls.
3. **Email + Call** – Initial email followed by a 10-minute phone call.

Sales reps are looking for actionable insights to help guide future campaigns with minimal effort for maximum return.

## Data Overview

The dataset used in this analysis captures customer-level sales records for the new product line. Each row corresponds to a unique customer and includes:

| Column Name         | Description |
|---------------------|-------------|
| `week`              | Week number since the product launch when sale occurred |
| `sales_method`      | Sales method used (`email`, `call`, `email and call`) |
| `customer_id`       | Unique customer identifier |
| `nb_sold`           | Number of new products sold |
| `revenue`           | Revenue generated from the sale (in USD) |
| `years_as_customer` | Tenure of the customer relationship |
| `nb_site_visits`    | Website visits by customer in the last 6 months |
| `state`             | US state where the order was shipped |



## Key Business Questions

The following questions must be addressed in the analysis:

1. How many customers used each sales method?
2. What does the revenue distribution look like overall and for each method?
3. Are there time-based trends in revenue performance across the three methods?
4. Which method should be continued or prioritized based on effectiveness and resource cost?
5. Are there notable differences in customer attributes by sales method?

## Deliverables

### Written Report (for Head of Analytics)
- Data validation and cleaning summary
- Exploratory analysis with multiple charts
- Business metric definition and initial benchmark
- Final recommendations

### Presentation (for Sales Rep)
- Business goals and overview
- Summary of analysis approach
- Key findings and metric(s) to monitor
- Recommendation for sales strategy going forward

---

