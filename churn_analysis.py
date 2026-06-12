import pandas as pd
import numpy as np
import duckdb

df=pd.read_csv("Bank.csv")

print(df.isnull().sum())
print("\n")
df=df.drop_duplicates()

print("First few rows:")
print(df.head())
print("\n")

print("Columns:")
print(df.columns)
print("\n")

print("Dataset info:")
print(df.info())
print("\n")

print("Churn distribution:")
print(df["churn"].value_counts())
print("\n")

churn_rate=df["churn"].mean()*100
print("Overall churn rate:",round(churn_rate,2),"%")
print("\n")

df["age_group"]=np.where(
    df["age"]<30,"Young",
    np.where(df["age"]<50,"Middle","Senior")
)

df["balance_cat"]=np.where(
    df["balance"]==0,"Zero Balance",
    np.where(df["balance"]<100000,"Medium Balance","High Balance")
)


df["credit_category"]=np.select(
    [
    df["credit_score"]<500,
    df["credit_score"]<650,
    df["credit_score"]<750,
    df["credit_score"]>=750
    ],
    ["Poor","Average","Good","Excellent"],
    default="Unkown"
    )

print(df[["age","age_group","balance","balance_cat","credit_category"]].head())
print("\n")

print("Average balance by churn:")
print(df.groupby("churn")["balance"].mean())
print("\n")

print("Average credit score:")
print(np.mean(df["credit_score"]))
print("\n")

print("Average credit score by churn:")
print(df.groupby("churn")["credit_score"].mean())
print("\n")

print("Average salary by churn")
print(df.groupby("churn")["estimated_salary"].mean())
print("\n")


print("Percentiles: <25,50,75>")
print(np.percentile(df["balance"],[25,50,75]))
print("\n")

def sqldf(query):
    return duckdb.sql(query).df()

q1="""select country, count(*) total_customers,
sum(churn) churned_customers,
round(sum(churn)*100.0/count(*),2) churn_rate
from df group by country
order by churn_rate desc
"""
print("churn rate by country:")
result=sqldf(q1)
print(result)
print("\n")

q2="""select age_group, count(*) total,
sum(churn) churned,
round(sum(churn)*100.0/count(*),2) churn_rate
from df group by age_group
order by churn_rate desc
"""
print("churn rate by age group:")
result=sqldf(q2)
print(result)
print("\n")

q3="""select products_number, count(*) total_customers,
sum(churn) churned_customers,
round(sum(churn)*100.0/count(*),2) churn_rate
from df group by products_number
order by products_number
"""
print("product vs churn rate")
result=sqldf(q3)
print(result)
print("\n")

q4="""select customer_id, country, age, balance
from df order by balance desc
limit 10
"""
print("Customers with highest bank balance (or) High value customers:")
result=sqldf(q4)
print(result)
print("\n")

q5="""select country, age_group, count(*) as total_customers,
sum(churn) as churned_customers, 
round(sum(churn)*100.0/count(*),2) as churn_rate,
rank() over(order by round(sum(churn)*100.0/count(*),2)desc) as risk_rank
from df group by country, age_group
order by churn_rate desc 
"""
print("Churn rate with respect to country and age group")
result=sqldf(q5)
print(result)
print("\n")

q6="""select active_member,count(*) total_customers,
sum(churn) churned, round(sum(churn)*100.0/count(*),2) churn_rate
from df group by active_member order by churn_rate desc
"""
print("Rate of non-active vs active members churned:")
result=sqldf(q6)
print(result)
print("\n")

q7="""select credit_category,
count(*) customers, sum(churn) churned,
round(sum(churn)*100.0/count(*),2) churn_rate
from df group by credit_category
order by churn_rate desc
"""
print("Churn rate of each credit category")
result=sqldf(q7)
print(result)
print("\n")

q8="""select count(*) as total_customers,
sum(churn) as churned,
round(sum(churn)*100.0/count(*),2) as churn_rate
from df where credit_score<(select avg(credit_score)from df)"""
print("Churn rate of customers with lesser than average credit score:")
result=sqldf(q8)
print(result)
print("\n")

