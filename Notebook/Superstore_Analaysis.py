import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



# Check if missingness correlates with another column
# df.groupby('segment')['discount'].apply(lambda x: x.isnull().mean())

# df['discount'] = df.groupby('segment')['discount'].transform(
#     lambda x: x.fillna(x.median())
# )


pd.set_option('display.max_columns',None)
pd.set_option('display.width',None)
pd.set_option('display.max_colwidth',None)

df1 = pd.read_csv("E:\Projects\Portfolio_Projects\Python\Superstore sales analytics\Superstore_cleaned_dt.csv")

# print(df1.tail(20))

# print(df1.info())

df1['order_date'] = pd.to_datetime(df1['order_date'])
df1['ship_date'] = pd.to_datetime(df1['ship_date'])


##1. What is the total sales, profit, and order count for the entire dataset?
# print(f' Total_sales {df1['sales'].sum().round(2)}')
# print(f' Total Profit {df1['profit'].sum().round(2)}')
# print(f'Total Orders {df1['order_id'].nunique()}')
# print("Profit margin",round(np.divide(df1['profit'].sum(),df1['sales'].sum()) * 100,2))

##2. how does each year perform based on sales and profit?

## to show in tables
sales_profit_year = df1.groupby('year').agg({'sales':'sum','profit':'sum'})
# print(sales_profit_year)

## to show in chart
# sns.lineplot(data= df1, x= 'year', y= 'sales',estimator= 'sum',errorbar= None, markers= 'o',label= "Sales")
# sns.lineplot(data= df1, x= 'year', y= 'profit',estimator= 'sum',errorbar= None, markers= 'o',label= "Profit")
# plt.title('Sales&Profit_trend_overtime')
# plt.xticks(rotation= 45)

# plt.ylabel("Amount")
# plt.tight_layout()
# plt.show()

##3. which market generates highest revenue
## to show in tables
market_revenue = df1.groupby(['market'],as_index= False)['sales'].sum().sort_values(by= 'sales',ascending=False)
# print(market_revenue)

## to show in chart
# plt.figure(figsize= (7,5))
# plt.xticks(rotation= 45)

# ax = sns.barplot(data= market_revenue,x= 'market',y= 'sales',palette='muted')
# for bars in ax.containers:
#     ax.bar_label(bars,fmt='{:,.0f}', padding=3)

# plt.title('Market wise revenue')
# plt.tight_layout()
# plt.show()

##4 product category wise quantity,revenue , and profit

# to show in table
category_revenue = df1.groupby('category').agg({'quantity':'sum','sales':'sum','profit':'sum'})
# print(category_revenue)

## to show in charts
# plt.figure(figsize=(6, 4))         
# sns.set_style('darkgrid')            

# ax = sns.barplot(data=category_revenue, x='category', y='sales', palette='deep')

# for bars in ax.containers:
#     ax.bar_label(bars,fmt='{:,.0f}', padding=3)

# plt.title('Revenue per Product Category')
# plt.tight_layout()
# plt.show()

##5. How does shipping time(shipping_date - order_date) vary by mode?
df1['ship_date'].dropna()
df1['shipping_time'] = (df1['ship_date']- df1['order_date']).dt.days

# print(shipping_time_days)
average_delays_mode = df1.groupby(['ship_mode'],as_index= False)['shipping_time'].mean().sort_values(by= 'shipping_time')
# print(average_delays_mode)

ship_cost_aveg_delay_By_mode = df1.groupby(['ship_mode'],as_index= False).agg({'shipping_time':'mean','shipping_cost':'sum'})
# print(ship_cost_aveg_delay_By_mode)


##6. which customer segment is most profitable?

## to show in table
customer_segment_profit = df1.groupby(['segment'],as_index= False)['profit'].sum().sort_values(by= 'profit',ascending=False)
# print(customer_segment_profit)

## to show in charts
# plt.figure(figsize=(5, 4))        
# sns.set_style('darkgrid')           

# ax = sns.barplot(data=customer_segment_profit, x='segment', y='profit', palette='deep')

# for bars in ax.containers:
#     ax.bar_label(bars,fmt='{:,.0f}', padding=3)

# plt.title('Total Profit by Customer Segment')
# plt.tight_layout()
# plt.show()

##7. who are the top 10 customers by sales?

# to show in tables 
customer_revenue = df1.groupby(['customer_name'],as_index=False)['sales'].sum().sort_values(by= 'sales',ascending=False).head(10)
# print(customer_revenue)

## to show in charts
# plt.figure(figsize=(14, 3))         
# sns.set_style('darkgrid')            

# ax = sns.barplot(data=customer_revenue, x='customer_name', y='sales', palette='deep')

# for bars in ax.containers:
#     ax.bar_label(bars,fmt='{:,.0f}', padding=3)

# plt.title('Top 10 customers by revenue')
# plt.tight_layout()
# plt.show()

##8. what is average order value per segment?

segment_avg_order = df1.groupby(['segment'],as_index=False)['sales'].mean().sort_values(by= 'sales',ascending=False)
# print(segment_avg_order)

## to show in charts
# plt.figure(figsize=(5, 4))          
# sns.set_style('darkgrid')            

# ax = sns.barplot(data=segment_avg_order, x='segment', y='sales', palette='deep')

# for bars in ax.containers:
#     ax.bar_label(bars,fmt='{:,.0f}', padding=3)

# plt.title('Average order value by Segment')
# plt.tight_layout()
# plt.show()

##9. what are the top 10 and bottom 10 selling products?
best_products = df1.groupby(['product_name'],as_index=False)['sales'].sum().sort_values(by= 'sales',ascending=False).head(10)
worst_products = df1.groupby(['product_name'],as_index=False)['sales'].sum().sort_values(by= 'sales',ascending=False).tail(10)

# print(best_products)
# print(worst_products)

## to show in charts
# plt.figure(figsize=(8, 5))         
# sns.set_style('darkgrid')            
# plt.xticks(rotation= 90)

# ax = sns.barplot(data=best_products, x='product_name', y='sales', palette='deep',hue= 'product_name',legend=False)

# for bars in ax.containers:
#     ax.bar_label(bars,fmt='{:,.0f}', padding=3)

# plt.title('Top 10 products by revenue')
# plt.tight_layout()
# plt.show()

##10. which country sold most orders and generated highest revenues?

country_orders = df1.groupby(['country'],as_index=False)['order_id'].count().sort_values(by= 'order_id',ascending=False).head(10)
country_revenue = df1.groupby(['country'],as_index=False)['sales'].sum().sort_values(by= 'sales',ascending=False).head(10)
# print(country_orders)
# print(country_revenue)

## top 10 countries by no of orders

# plt.figure(figsize=(10, 4))          
# sns.set_style('darkgrid')            

# ax = sns.barplot(data=country_orders, x='country', y='order_id', palette='deep',hue= 'country',legend= False)

# for bars in ax.containers:
#     ax.bar_label(bars,fmt='{:,.0f}', padding=3)
# plt.ylabel('Total orders')
# plt.title('Top 10 country by no of orders')
# plt.tight_layout()
# plt.show()

#..................................
## top 10 countries by revenue

# plt.figure(figsize=(10, 4))          
# sns.set_style('darkgrid')            

# ax = sns.barplot(data=country_revenue, x='country', y='sales', palette='deep',hue= 'country',legend= False)

# for bars in ax.containers:
#     ax.bar_label(bars,fmt='{:,.0f}', padding=3)
# plt.ylabel('Total Revenue')
# plt.title('Top 10 country by revenue')
# plt.tight_layout()
# plt.show()


##12. what is optimal discount range that maximizes profit, not just sales?
discount_range_profit = df1.groupby(pd.cut(df1['discount'], bins=[0,0.1,0.2,0.3,0.4,0.5,1]))['profit'].mean()
# print(discount_range_profit)
 
