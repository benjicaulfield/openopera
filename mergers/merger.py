
import pandas as pd
import numpy as np
import editdistance

stn= pd.read_csv('stn.csv')
mpv= pd.read_csv('normal_mpv.csv')
wapo= pd.read_csv('normal_wapo.csv')
final_compiled= pd.read_csv('source_merger.csv')
compiled= pd.DataFrame()
# for col in stn.columns.tolist():
#     compiled[col]=''

#helper functnios
def find_match(num):
    key= [mpv.loc[num,"Victim's name"],mpv.loc[num,'WaPo ID (If included in WaPo database)']]
    
    #find idex with matching wapo id 
    idx=wapo.index[wapo['ID']== int(key[1])]
   
    #returns the row with the matching index
    return wapo.loc[idx]

def update_row(match,row):
    global wapo
   
    #creating a key for current row and identifying its matching row
    key=mpv.loc[row,'WaPo ID (If included in WaPo database)']
    idx=wapo.index[wapo['ID']== int(key)]
   
    #looping through each column name that exists in wapo if it differs, assign the mpv value to wapo
    for cell in mpv.columns.tolist():
        if cell != 'Unnamed: 0':
            if cell in wapo.columns.tolist():
                if mpv.loc[row,cell] != wapo.loc[idx.values[0],cell]:
                    mpv.loc[row,cell]=wapo.loc[idx.values[0],cell]
    #dropping any row that is assigned 
    wapo =wapo.drop(idx.values[0])
    return mpv.loc[row],wapo
        
#formating problem with name
rename={"Victim's name":'name'}
final_compiled=final_compiled.rename(columns=rename)
issues={}
stn_priority=['Biographical Information','Bio URL',
'Photo URL',
'A brief description of the circumstances surrounding the death',
'Official disposition of death (justified or other)',
'Criminal Charges?',
'Unarmed/Did Not Have an Actual Weapon',
'Alleged Weapon (Source: WaPo and Review of Cases Not Included in WaPo Database)',
'Alleged Threat Level (Source: WaPo)',
'Fleeing (Source: WaPo)']

def flag_check(num):
    global issues
    global final_compiled
    #creating a key for each row
    key= [stn.loc[num,"Victim's name"],stn.loc[num,"Age"],stn.loc[num,"Incident Date (MM/DD/YYYY)"]]
    # Victim key index values
    # 0- Name
    # 1-Age
    # 2- Dates
    # 3- City

    #if key exits in (compiled), find a matching idex in compiled based on date
    if key[0] in final_compiled.name.values:
        # print(final_compiled.loc[(final_compiled["name"]== key[0]) ,'Age'].values[0] , key[1])
        if str(final_compiled.loc[(final_compiled["name"]== key[0]) ,'Age'].values[0]) == key[1]:
            idx=final_compiled.index[final_compiled["name"]==key[0]]
    
            match= final_compiled.loc[idx]

            # stn row does not com
            if stn.loc[num].equals(match) != True:
                for cell in stn.columns.tolist():  

                    if cell != 'Unnamed: 40' and cell != 'Unnamed: 41' and cell != "Victim's name" and cell != 'Incident Date (MM/DD/YYYY)':
                        st= stn.loc[num,cell] 
                        comp= final_compiled.loc[idx.values[0],cell]


                        if pd.isna(final_compiled.loc[idx.values[0],cell]) == True:
                            final_compiled.loc[idx.values[0],cell]=stn.loc[num,cell]

                
                        else:
                            #priority to wapo in threat lvl,
                            # nan in stn but not compiled
                            #added information(brief description of circumstances priority over compiled)
                            # if != or comp exists within st
                            #'Unarmed/Did Not Have an Actual Weapon'- prioirty to stn
                            #'Alleged Threat Level (Source: WaPo)' priority to stn
                            #'Official disposition of death (justified or other)'
                            #Fleeing(Source:Wapo)
                            #Criminal Charges
                            #'Alleged Weapon (Source: WaPo and Review of Cases Not Included in WaPo Database)'
                            if cell in stn_priority:
                                final_compiled.loc[idx.values[0],cell]=stn.loc[num,cell]
                            else:
                                if editdistance.eval(str(stn.loc[num,cell]), str(final_compiled.loc[idx.values[0],cell])) > 5 and pd.isna(stn.loc[num,cell]) != True and str(final_compiled.loc[idx.values[0],cell]) not in str(stn.loc[num,cell]) :
                                    issues[num]=(f"Row {num} has a confliction with its match {idx.values[0]}")
                        
    else:
        final_compiled.loc[len(compiled.index)]= stn.loc[num]




def source_merger():
    global wapo
    global compiled
    for row in mpv.index:
        if mpv.loc[row,'WaPo ID (If included in WaPo database)'] != 0:
            match=find_match(row)
            if match.empty is not True:
                final,wapo=update_row(match,row)
                compiled.loc[len(compiled.index)]= final
        else:
            compiled.loc[len(compiled.index)]= mpv.loc[row]
    for row in wapo.index: 
        compiled.loc[len(compiled.index)]= wapo.loc[row]
    compiled.to_csv('source_merger.csv')

def stn_merger():
    for row in stn.index:
       flag_check(row)
    final_compiled.to_csv('merged.csv')

       
    print(len(issues))
# source_merger()
stn_merger()
    



