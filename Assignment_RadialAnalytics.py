
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np


# In[285]:

patienClaims = 'patienClaims.csv'
claimUtilization = 'claimUtilization.csv'
sourceFile = 'data.csv'


# In[286]:

def driverFile1():
    #Read CSV File
    df_1 = pd.read_csv(sourceFile)
    print("====================")
    print("Question 1 Starts") 
    print("====================") 
    print("Source data.csv File read")
    print("====================") 
    #Renaming columns for ease of use
    df_1.rename(columns={'State Code from Claim (SSA)': 'State','Gender Code from Claim': 'Gender','LDS Age Category': 'Age'},
                inplace=True)
    #Create dataFrame consisting of State, Age and Gender as we need only these columns for our analysis
    df_data = pd.DataFrame(df_1,columns=['State','Age','Gender'])
    #Working on Gender column first: Male and Female Counts
    df_gender = df_data.copy()
    df_gender['count'] = 1
    df_g = df_gender.pivot_table('count', index='State', columns='Gender', aggfunc='sum').fillna(0).reset_index()
    df_g.rename(columns={1: 'Male',2: 'Female'}, inplace=True)
    #Working on Age Column now, creating separate dataframe to handle the analysis
    df_age = pd.DataFrame(df_data,columns=['State','Age'])
    df_age['count'] = 1
    df_a = df_age.pivot_table('count', index='State', columns='Age', aggfunc='sum').fillna(0).reset_index()
    df_a.rename(columns={0:'Unknown', 1: 'Ages<65',2: 'Age65',3:'Age74',4:'Age79',5:'Age80',6:'Age84'}, inplace=True)
    df_a['Ages 65-74'] = df_a['Age65'] +df_a['Age74'] 
    df_a['Ages 75+'] = df_a['Age79'] +df_a['Age80'] + df_a['Age84']
    df_a.drop(df_a.columns[[2,3,4,5,6]], axis=1, inplace=True)
    #Create CSV File
    merged_inner = pd.merge(left=df_g,right=df_a, left_on='State', right_on='State')
    merged_inner.to_csv(patienClaims,index=False)
    print("====================")
    print("Output File created patienClaims.csv")
    print("====================")
    print("Question 1 Finished")
    
    


# In[280]:

def driverFile2():
    print("====================")
    print("Question 2 Starts")
    print("====================")
    print("Source data.csv File read")
    #Read CSV File
    df_1 = pd.read_csv(sourceFile)
    #Renaming columns for ease of use
    df_1.rename(columns={'Claim Utilization Day Count': 'Utilization_Range'}, inplace=True)
    #Create dataFrame consisting of Utilization_Range column only
    df_util = pd.DataFrame(df_1,columns=['Utilization_Range'])
    #print(df_util.head())
    #Calculate Count
    df_util['Counts'] = 1
    df_u = df_util.pivot_table('Counts', index='Utilization_Range', aggfunc='sum').fillna(0).reset_index()    
    df_test = pd.DataFrame(df_u,columns=['Utilization_Range','Counts'])
    #print(df_test.head())
    #Started dividing the column values in to ranges 6-10,11-30 $ >30
    df_test.loc[(df_test['Utilization_Range'] > 5) & (df_test['Utilization_Range'] <11), 'Utilization_Range'] = 6
    df_test.loc[(df_test['Utilization_Range'] > 10) & (df_test['Utilization_Range'] <31), 'Utilization_Range'] = 11
    df_test.loc[df_test['Utilization_Range'] > 30, 'Utilization_Range'] = 31
    #Convert to STring datatype as we cannot use '-' since out current datatype is int
    df_test.Utilization_Range = df_test.Utilization_Range.astype(str)
    #print(df_test.dtypes)
    #Create the ranges
    df_test.loc[(df_test['Utilization_Range'] == '6' ),'Utilization_Range'] = '6-10'
    df_test.loc[(df_test['Utilization_Range'] == '11' ),'Utilization_Range'] = '11-30'
    df_test.loc[(df_test['Utilization_Range'] == '31' ),'Utilization_Range'] = '>30'
    #print(df_test)
    #Perform groupby on the column 
    df = pd.DataFrame(df_test.groupby(['Utilization_Range'],sort=False).agg({'Counts': 'sum'}).reset_index())
    #print(df.head())
    #Calculate percentage
    fullcount = df['Counts'].sum()
    #print(fullcount)
    df['Percentages'] = np.round((100 * (df['Counts']/fullcount)),decimals=2)
    #Formatting the col
    df['Percentages'] = df['Percentages'].apply( lambda x : str(x) + '%')
    df['Counts'] = df.apply(lambda x: "{:,}".format(x['Counts']), axis=1)
    #print(df.head()) 
    #Create CSV File
    df.to_csv(claimUtilization,index=False)
    print("====================")
    print("Output File created claimUtilization.csv")
    print("====================")
    print("Question 2 Finished")

# In[287]:

driverFile1()


# In[282]:

driverFile2()

