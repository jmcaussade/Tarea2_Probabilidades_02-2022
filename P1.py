## LINKs códigos:
            ##Link Collab: https://colab.research.google.com/drive/1SF3p2nz389SQnAgoKO5os2ZjlexW_O16?authuser=2#scrollTo=seR4-BXXb1f_
## Parte del código extraido de google collab

## Loading the required libraries:
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import scipy.stats as st
#import warnings
#warnings.filterwarnings('ignore')

from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())

## Reading the data:
order_items = pd.read_csv('olist_order_items_dataset.csv', on_bad_lines='skip')  ## Unclassified orders dataset
seller=pd.read_csv('olist_sellers_dataset.csv', on_bad_lines='skip') ## Seller information
translation=pd.read_csv('product_category_name_translation.csv', on_bad_lines='skip')
product = pd.read_csv('olist_products_dataset.csv', on_bad_lines='skip')  ## Product translation to english

# Generate data at product-item level:
order_item_products = pd.merge(order_items,product, how='left', on='product_id')
orders_item_products_english = pd.merge(order_item_products,translation, how='left', on='product_category_name')
orders = pd.merge(orders_item_products_english,seller, how='left', on='seller_id')

# Select only the columns we are going to use:
selected_columns = orders[['order_id','product_id', 'product_category_name_english','seller_id', 'seller_city','seller_state','price','freight_value']]

# Aggregate data: Count orders to get the quantity of sold items:
order_products = selected_columns.groupby(['product_id','seller_state','seller_city','product_category_name_english']).aggregate({'order_id':'count','price':'mean','freight_value':'mean'}).rename(columns={'order_id':'quantity'}).reset_index() #.sort_values(by='quantity',ascending=False).reset_index()

# Multiply 'price' and 'quantity' to get the Gross Monetary Value (GMV):
order_products['GMV'] = order_products['price']*order_products['quantity'] 
dataset = order_products
#### Fin extraccion Google Collab ###

## Renaming column
dataset.rename(columns ={"product_category_name_english" : "product_category"}, inplace = True)

############## FUNCTIONS ###############

def STD(dataframe):
    size = dataframe["quantity"].sum()
    mean = dataframe["GMV"].sum()/size
    SquareSum = 0
    i = 0
    while i<dataframe.shape[0]:
        SquareSum+= (dataframe["GMV"][i] - mean)**2
        i+=1
    Division = SquareSum/size
    std = Division**(1/2)
    #print(size)
    #print(mean)
    #print(SquareSum)
    #print(std)
    list = [mean, std]
    return list

############## END FUNCTIONS ###########

q1 = f"""SELECT product_category, SUM(quantity) as sum_quantity, SUM(GMV) as sum_GMV FROM dataset 
GROUP BY product_category
ORDER BY sum_GMV DESC 
LIMIT 1 """
n1 = pysqldf(q1)
#print(n1, "\n")

category = n1["product_category"][0]
q2 = f"""SELECT product_category, quantity, price, GMV FROM dataset WHERE product_category = "{category}" 
ORDER BY price DESC"""
n2 = pysqldf(q2)
#print(n2, "\n")



###  SAMPLE N = 25 #####
Sample25 = n2["GMV"].sample(n = 25)
#print(Sample25)
Interval25t = st.t.interval(0.95, (len(Sample25) - 1),np.mean(Sample25), st.sem(Sample25))
print("\nIntervalo confianza n = 25")
print(Interval25t)

###  SAMPLE N = 100 #####
Sample100 = n2["GMV"].sample(n = 100)
#print(Sample100)
Interval100 = st.norm.interval(0.95, np.mean(Sample100), st.sem(Sample100))
print("\nIntervalo confianza n = 100")
print(Interval100)


###  SAMPLE N = 1000 #####
Sample1000 = n2["GMV"].sample(n = 1000)
#print(Sample100)
Interval1000 = st.norm.interval(0.95, np.mean(Sample1000), st.sem(Sample1000))
print("\nIntervalo confianza n = 1000")
print(Interval1000, "\n")









