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


## Main ###

## product category = sport_leisure
q1 = f"""SELECT freight_value FROM dataset 
WHERE product_category = "sports_leisure" """

n1 = pysqldf(q1)
#print(n1, "\n")

## product category = watches_gifts
q2 = f"""SELECT product_category, freight_value FROM dataset 
WHERE product_category = "watches_gifts" """

n2 = pysqldf(q2)
#print(n2, "\n")

##### Intervals #####

## Sport leisure
SportsIntevrval = st.norm.interval(0.95, np.mean(n1["freight_value"]), st.sem(n1["freight_value"]))
print("\nIntervalo de confianza 95% para Sports leisure freight_value")
print(SportsIntevrval, "\n")

## Watches gifts
WatchesIntevrval = st.norm.interval(0.95, np.mean(n2["freight_value"]), st.sem(n2["freight_value"]))
print("\nIntervalo de confianza 95% para Watches gifts freight_value")
print(WatchesIntevrval, "\n")

## Calculo Ancho intervalos y porcentajes

### Sports Leisure
Sfin = SportsIntevrval[1]
Sinicio = SportsIntevrval[0]
Sancho = Sfin - Sinicio
print("\nAncho Sports leisure = ", Sancho)

### Watches gifts
Wfin = WatchesIntevrval[1]
Winicio = WatchesIntevrval[0]
Wancho = Wfin - Winicio
print("\nAncho Watches gift = ", Wancho)

Percentage = (Sancho*100)/Wancho

print("\npercentage = ", Percentage, "% \n")