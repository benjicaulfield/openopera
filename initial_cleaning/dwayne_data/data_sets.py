import pandas as pd
import numpy as np
import datetime
import re
import string



main= pd.read_csv('MCDC.csv')
wash = pd.read_csv('Wash.csv')
second= pd.read_csv('Mapping Police Violence.csv')
#pd.Series(list)- creates a series from a list
#df.loc[row,col]= sum
#current database information
print(f"There are currently {len(main.index)} rows in the working dataset...\n")


def main_comparison():
    #filters both datasets by race for comparison
    wash.fillna(0,inplace=True)
    second.fillna(0,inplace=True)
    for row in wash.index:
        if type(wash.loc[row,"name"]) == str :
            new= wash.loc[row,'name']
            name = re.sub(r'[^\w\s]', '_', new).lower()
            wash.loc[row,'name']= name.replace(' ','_')
        # black_wash.loc[row,'name']= newff
    for row in second.index:
        if type(second.loc[row,"name"]) == str :
            new= second.loc[row,'name']
            name = re.sub(r'[^\w\s]', '_', new).lower()
            second.loc[row,'name']= name.replace(' ','_')
    #filters both datasets by race for comparison
    black_wash= wash.loc[ wash['race'] =='B']
    black_second= second.loc[second['race']=='Black']
    wcounter=0
    scounter=0
    total=0
    cmissing=0
    missing=[]
    for row in range(len(main.index)):
        #variables to track where each individiaul has been assigned
        washy=False
        secondy=False
        #attempting to get rid of non string names
        if type(main.loc[row,"Victim name"]) == str :
            #normalization of name
            cur = (main.loc[row,"Victim name"].lower())
            new = re.sub(r'[^\w\s]', '_', cur)
            name= new.replace(' ','_')
            age= main.loc[row,'Age']
            id= main.loc[row,'WaPo ID (If included in WaPo database)']
            city = main.loc[row,'City']
            #two ages that created errors
            if age == 'Unknown' or '40s':
                age=0
            #Wapo database comparison checks 
            if name in black_wash.name.values  :
                if black_wash.loc[(black_wash['name']==name),'age'].values[0]== float(age) or black_wash.loc[(black_wash['name']==name),'id'].values[0] == id:
                    wcounter+=1
                    washy=True
            #second database comparison
            if name in name in black_second.name.values :
                if black_second.loc[(black_second['name']==name),'age'].values[0] == float(age) or black_second.loc[(black_second['name']==name),'city'].values[0] == city :
                    scounter+=1
                    secondy=True
            #keeping track of which rows are assigned to both
            if washy == True and secondy == True:
                total+=1
            # rows that can not be accounted for 
            if washy == False and secondy == False:
                missing.append([name,age,city,id])
                cmissing += 1

    # print(wcounter,scounter,total)
    print(f"Roughly {(wcounter-total)/len(main.index)} of the working data set comes from Wapo alone")
    print(f"Roughly {(scounter-total)/len(main.index)} of the working data set comes from the second source alone")
    print(f"{((scounter+wcounter)-total)/len(main.index)} acounts for both sources")
    # print(missing)

# main_comparison()


def source_comparison():
   scopy= second.dropna(subset=['wapo_id'])
   wcopy= wash.dropna(subset=['id'])
   mcopy= main.dropna(subset=['WaPo ID (If included in WaPo database)'])
   black_wash= wash.loc[wash['race'] =='B']

   print(len(mcopy.index)/len(black_wash.index))
   print(f"The second source contains(roughly) {len(scopy.index)/len(wcopy.index)} of the Wapo set. ")
   
source_comparison()