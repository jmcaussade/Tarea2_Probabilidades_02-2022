## LINKs códigos:
            ##Link Collab: https://colab.research.google.com/drive/1SF3p2nz389SQnAgoKO5os2ZjlexW_O16?authuser=2#scrollTo=seR4-BXXb1f_
## Parte del código extraido de google collab

## Loading the required libraries:
import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
import scipy.stats as st
import math
#import warnings
#warnings.filterwarnings('ignore')

from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())

## Functions ##
def MeanDiff(array1, array2): ## array[mean, var, tamaño muestra]
    z = 1.96
    sub = array1[0] - array2[0]
    sum = (array1[1]/array1[2] + array2[1]/array2[2])
    Sroot = math.sqrt(sum)
    timesZ = z*Sroot
    resultleft = sub - timesZ
    resultright = sub + timesZ
    IC = "( ", resultleft, " ,", resultright, " )"
    return IC




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

## SELECTING DATA

# SP
q1 = f"""SELECT seller_state, freight_value FROM dataset
WHERE seller_state = "SP" 
"""
n1 = pysqldf(q1)

SPMean= n1["freight_value"].mean()
SPVar= n1["freight_value"].var()
print("SPMean:", SPMean)

SampleSP = n1["freight_value"].sample(frac= .20)
SPSampleMean = np.mean(SampleSP)
print("SP Sample Mean: ", SPSampleMean)

#RJ
q2 = f"""SELECT seller_state, freight_value FROM dataset
WHERE seller_state = "RJ" 
"""
n2 = pysqldf(q2)


RJMean= n2["freight_value"].mean()
RJVar= n2["freight_value"].var()
print("RJMean:", RJMean)

SampleRJ = n2["freight_value"].sample(frac= .20)
RJSampleMean = np.mean(SampleRJ)
print("RJ Sample Mean: ", RJSampleMean)

# MG
q3 = f"""SELECT seller_state, freight_value FROM dataset
WHERE seller_state = "MG" 
"""
n3 = pysqldf(q3)

MGMean= n3["freight_value"].mean()
MGVar= n3["freight_value"].var()
print("MGMean:", MGMean)

SampleMG = n3["freight_value"].sample(frac= .20)
MGSampleMean = np.mean(SampleMG)
print("MG Sample Mean: ", MGSampleMean)


## Part 1 Intervals ####

IntervalSP = st.norm.interval(0.95, SPSampleMean, st.sem(SampleSP))
print("IntervalSP", IntervalSP)

IntervalRJ= st.norm.interval(0.95, RJSampleMean, st.sem(SampleRJ))
print("IntervalRJ", IntervalRJ)

IntervalMG= st.norm.interval(0.95, MGSampleMean, st.sem(SampleMG))
print("IntervalMG", IntervalMG)

##### PART 2 Mean difference #####



