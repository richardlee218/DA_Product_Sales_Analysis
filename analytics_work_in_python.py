import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import pingouin
from statsmodels.stats.multicomp import pairwise_tukeyhsd

def iqr(column):
    return column.quantile(0.75) - column.quantile(0.25)

# Read in CSV Data file for analysis
df = pd.read_csv("product_sales.csv")

# Examine data set for Null Values and Data Type
print(df.info())

# Examine each feature for data anomaly
print(df[['week','sales_method','customer_id']].agg([np.min,np.max,np.mean,np.median,'nunique','count']))
print(df[['nb_sold','revenue','years_as_customer']].agg([np.min,np.max,np.mean,np.median,'nunique','count']))
print(df[['nb_site_visits','state']].agg([np.min,np.max,np.mean,np.median,'nunique','count']))

# 1) We learn that week have 6 distinct values. no null values.  It is a number but it can be used as an ordinal categorical variable as it presents n-weeks from launch. likely no data anomaly.
# 2) We learn that sales_method have 5 distinct values. no null values.  It is a categorical variable. It is a  which is more than the 3 methods highlighted in the brief. need to examine further.
# 3) We learn that customer_id is unique in the data set and each row represents a unique customer. no null values. 
# 4) nb_sold is a numerical variable. no null values. Likely no data anomaly.
# 5) revenue is a numerical variable. we already know there are null values. need to examine further.
# 6) no null values. years_as_customer is a numerical variable but it can be used as an ordinal categorical variable as it presents n-years as customer. Looking at the max there is a customer with value of 63 which seems incorrect since the company was founded in 1984 and 63 from this date would be 2047 which is a date in the future. need to examine further.
# 7) nb_site_visits is a numerical variable. no null values. Likely no data anomaly.
# 8) no null values. state is a categorical variable. has 50 unique values to represent 50 states. Likely no data anomaly.

print(df['week'].value_counts().sort_index())
print(df['sales_method'].value_counts().sort_index())
print(df['years_as_customer'].value_counts().sort_index())
print(df['state'].value_counts().sort_index())

# only 2 values in years_as_customer seems to be incorrect. These two customers can be excluded from the analysis. It is only 2 data points so it is not going to introduce any bias.
# string values in sales_method need to be fixed
# week seems to be free of data anomaly.
# state seems to be free of data anomaly.

# Clean Sales Method
df['sales_method_cleaned'] = df['sales_method'].replace({'Call': 'Call', 'Email': 'Email', 'Email + Call': 'Email + Call', 'em + call': 'Email + Call', 'email': 'Email'})

# Cleaned 
print(df['sales_method_cleaned'].value_counts().sort_index().reset_index(name='count'))

# Correlation Heatmap
corr_matrix = df.corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.show()

# Scatter of nb_sold and revenue
sns.scatterplot(data=df, x=df['nb_sold'], y=df['revenue'], hue=df['sales_method_cleaned'])
plt.show()


# Group by 'sales_method_cleaned' + 'nb_sold' and aggregate
result = df.groupby(['sales_method_cleaned', 'nb_sold']).agg(
    tot_rev_count = ('revenue', 'size'), # Counts all items in group, including NaN
    valid_rev_count = ('revenue', 'count'), # Counts non-NaN items
    na_rev_count = ('revenue', lambda x: x.isnull().sum()) # Counts NaN items
).reset_index()
print(result)


print( df.groupby(['sales_method_cleaned', 'nb_sold'])['revenue'].median().reset_index(name='median') )

print( df.groupby('sales_method_cleaned')['revenue_imputed'].mean().reset_index(name='mean') )


df['revenue_imputed'] = df.groupby(['sales_method_cleaned', 'nb_sold'])['revenue'].transform(lambda x: x.fillna(x.median()))

print( df[df['revenue'].isna()].groupby(['sales_method_cleaned', 'nb_sold'])['revenue_imputed'].median().reset_index(name='median') )

# Chart Area attributes
order_list = ['Email', 'Call', 'Email + Call']
hue_colors = {'Email':'grey', 'Call':'blue', 'Email + Call':'green'}

# Figure 1 = creates a bar plot of number of unique customers within each sales method
cust_count_by_method = df.groupby('sales_method_cleaned')['customer_id'].nunique().reset_index(name='customer_count')
fig1 = sns.barplot(x='sales_method_cleaned', y='customer_count', data=cust_count_by_method, hue='sales_method_cleaned', order=order_list, palette=hue_colors)
plt.xlabel("Sales Method")
plt.ylabel("Number of customers")
for i in fig1.containers:
    fig1.bar_label(i,)
plt.show()


# Figure 2 = creates a box plot of revenue 
fig2 = sns.boxplot( x='revenue_imputed' , data=df)
plt.xlabel("Revenue per customer ($)")
fig2.set_title('Overall spread of revenue per customer')
plt.show()

all_quantiles = df['revenue_imputed'].quantile([0.25, 0.5, 0.75]).reset_index(name='percentiles')
print(all_quantiles)


# Figure 3 = creates a box plot of revenue within each sales method
fig3 = sns.boxplot(y='sales_method_cleaned', x='revenue_imputed' , data=df, hue='sales_method_cleaned', order=order_list, palette=hue_colors)
plt.ylabel("Sales Method")
plt.xlabel("Revenue per customer ($)")
fig3.set_title('Spread of revenue per customer by sales method')
plt.show()


# Figure 4 = creates a line plot of revenue over weeks since poduct launch
fig4 = sns.lineplot(data=df, x='week', y='revenue_imputed', hue='sales_method_cleaned', palette=hue_colors, estimator=np.sum)
plt.xlabel("Weeks since product launch")
plt.ylabel("Revenue ($)")
plt.legend(title='Sales Method')
fig4.set_title('Total revenue over weeks since product launch by sales method')
plt.show()


# Figure 5 = creates a line plot of revenue over weeks since poduct launch
fig5 = sns.catplot(data=df, x='week', y='revenue_imputed', kind='box', col='sales_method_cleaned', hue='sales_method_cleaned', palette=hue_colors, estimator=np.sum)
fig5.set_axis_labels("Weeks since product launch", "Revenue per customer ($)")
fig5.set_titles("{col_name}")
fig5.fig.suptitle("Revenue per customer spread over weeks since product launch for each sales method", y=1.05)
fig5._legend.set_title("Sales Method")
plt.show()


# Perform one-way ANOVA Test between the 3 groups Revenue spread difference to see if the difference is significant
anova_test_results = pingouin.anova(data=df,
    dv="revenue_imputed",
    between="sales_method_cleaned")
print(anova_test_results)

# P value is extremely small so we have sufficient evidence to say that at least one of the means of the group is different from the others.
# Uncorrected pairwise p-values

# Perform Tukey's HSD test
tukey_results = pairwise_tukeyhsd( endog=df['revenue_imputed'], groups=df['sales_method_cleaned'], alpha=0.05 )
print(tukey_results)

# Statistically significant difference between the means of all groups.

q1 = np.percentile(df['revenue_imputed'][df['sales_method_cleaned'] == 'Email + Call'], 25)
q3 = np.percentile(df['revenue_imputed'][df['sales_method_cleaned'] == 'Email + Call'], 75)
results_median = np.median(df['revenue_imputed'][df['sales_method_cleaned'] == 'Email + Call'])
iqr = q3 - q1 
upper_bound = q3 + 1.5 * iqr
lower_bound = q1 - 1.5 * iqr
results_mean = np.mean(df['revenue_imputed'][df['sales_method_cleaned'] == 'Email + Call'])

results_mean = df.groupby('sales_method_cleaned')['revenue_imputed'].mean().reset_index()
print(results_mean)

print( 'Median: '+ str(results_median) )
print( '25th Percentile: '+ str(q1) )
print( '75th Percentile: '+ str(q3) )
print( 'Upper Bound Threshold: '+ str(upper_bound) )
print( 'Lower Bound Threshold: '+ str(lower_bound) )

week6_emailncall_median = np.median(df['revenue_imputed'][(df['sales_method_cleaned'] == 'Email + Call') & (df['week'] == 6)])
print(week6_emailncall_median)


# Figure 6 = creates a bar plot of total revenue within each sales method
tot_rev_by_method = df.groupby('sales_method_cleaned')['revenue_imputed'].sum().reset_index()
fig6 = sns.barplot(x='sales_method_cleaned', y='revenue_imputed' , data=tot_rev_by_method, hue='sales_method_cleaned', order=order_list, palette=hue_colors)
plt.xlabel("Sales Method")
plt.ylabel("Revenue ($)")
fig6.set_title('Total revenue for each sales method')
for i in fig6.containers:
    fig6.bar_label(i,)
plt.show()


fig7 = sns.catplot(data=df, x='state', kind='count', col='sales_method_cleaned', hue='sales_method_cleaned', palette=hue_colors)
fig7.set_axis_labels("State", "Number of customers")
fig7.set_titles("{col_name}")
fig7.fig.suptitle("Number of customers per state for each sales method", y=1.05)
fig7._legend.set_title("Sales Method")
fig7.set_xticklabels(rotation=90)
plt.show()


fig8 = sns.catplot(data=df, x='state', kind='count')
fig8.set_axis_labels("State", "Number of customers")
fig8.set_titles("{col_name}")
fig8.fig.suptitle("Number of customers per state for each sales method", y=1.05)
fig8.set_xticklabels(rotation=90,fontsize=8)
plt.show()



sales_method_site_visits = df.groupby('sales_method_cleaned')['nb_site_visits'].median().reset_index(name='median')
print(sales_method_site_visits)

sales_method_years_as_customer = df[df['years_as_customer']<40].groupby('sales_method_cleaned')['years_as_customer'].median().reset_index(name='median')
print(sales_method_years_as_customer)


# Figure 9 = creates a box plot of Spread of site visits
fig9 = sns.boxplot( x='nb_site_visits' , data=df)
plt.xlabel("Site Visits")
fig9.set_title('Spread of site visits')
plt.show()


# Figure 10 = creates a box plot of spread of Years as customer
fig10 = sns.boxplot( x='years_as_customer' , data=df[df['years_as_customer']<40])
plt.xlabel("Years as customer")
fig10.set_title('Spread of years as customer')
plt.show()




cust_count_by_method = df.groupby('sales_method_cleaned')['customer_id'].nunique().reset_index(name='count')
tot_sold_by_method = df.groupby('sales_method_cleaned')['nb_sold'].sum().reset_index()
tot_rev_by_method = df.groupby('sales_method_cleaned')['revenue_imputed'].sum().reset_index()
tot_visit_by_method = df.groupby('sales_method_cleaned')['nb_site_visits'].sum().reset_index()

stats_by_method = cust_count_by_method.merge(tot_sold_by_method, on='sales_method_cleaned').merge(tot_rev_by_method, on='sales_method_cleaned').merge(tot_visit_by_method, on='sales_method_cleaned')
stats_by_method['nb_sold_per_cust'] = stats_by_method['nb_sold']/stats_by_method['count']
stats_by_method['rev_per_cust'] = stats_by_method['revenue_imputed']/stats_by_method['count']
stats_by_method['avg_rev_per_unit_sold'] = stats_by_method['revenue_imputed']/stats_by_method['nb_sold']
stats_by_method['avg_sold_per_visit'] = stats_by_method['nb_sold']/stats_by_method['nb_site_visits']
stats_by_method['avg_rev_per_visit'] = stats_by_method['revenue_imputed']/stats_by_method['nb_site_visits']


# Figure 2 = creates a bar plot of total new products sold within each sales method

fig2 = sns.barplot(x='sales_method_cleaned', y='avg_sold_per_visit' , data=stats_by_method, hue='sales_method_cleaned', order=order_list, palette=hue_colors)
plt.xlabel("Sales Method")
plt.ylabel("Average new products sold per site visit")
for i in fig2.containers:
    fig2.bar_label(i,)
plt.show()


# Figure 2 = creates a bar plot of total new products sold within each sales method

fig2 = sns.barplot(x='sales_method_cleaned', y='avg_rev_per_visit' , data=stats_by_method, hue='sales_method_cleaned', order=order_list, palette=hue_colors)
plt.xlabel("Sales Method")
plt.ylabel("Average revenue per site visit")
for i in fig2.containers:
    fig2.bar_label(i,)
plt.show()


# Figure 2 = creates a bar plot of total new products sold within each sales method

fig2 = sns.barplot(x='sales_method_cleaned', y='avg_rev_per_unit_sold' , data=stats_by_method, hue='sales_method_cleaned', order=order_list, palette=hue_colors)
plt.xlabel("Sales Method")
plt.ylabel("Average revenue per new products sold")
for i in fig2.containers:
    fig2.bar_label(i,)
plt.show()



# Figure 4 = creates a line plot of customer over weeks since product launch
cust_count_per_week_by_method = df.groupby(['sales_method_cleaned','week'])['customer_id'].nunique().reset_index(name='count')
fig4 = sns.lineplot(data=cust_count_per_week_by_method, x='week', y='count', hue='sales_method_cleaned', palette=hue_colors)
plt.xlabel("Weeks since product launch")
plt.ylabel("Number of Customers")
plt.legend(title='Sales Method')
fig4.set_title('Total number of customers over weeks since product launch by sales method')
plt.show()



