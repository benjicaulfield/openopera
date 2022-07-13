import pandas as pd
import numpy as np

from collections import Counter

def normalize():
    mpv = standardize_mpv(pd.read_csv('datasets/mpv.csv'))
    wapo = standardize_wapo(pd.read_csv('datasets/wapo.csv'))
    mpv.to_csv('normal_mpv.csv')
    wapo.to_csv('normal_wapo.csv')
    

def standardize_wapo(wapo):
    rename_dict = {'id': 'ID',
                   'name': 'Victim\'s name',
                   'date': 'Incident Date (MM/DD/YYYY)',
                   'manner_of_death': 'Cause of death',
                   'armed': 'Unarmed/Did Not Have an Actual Weapon',
                   'age': 'Age',
                   'gender': 'Gender',
                   'city': 'City',
                   'state': 'State',
                   'signs_of_mental_illness': 'Symptoms of mental illness',
                   'threat_level': 'Alleged Threat Level (Source: WaPo)',
                   'flee': 'Fleeing (Source: WaPo)',
                   'body_camera': 'Body Camera (Source: WaPo)',
                   'latitude': 'Latitude',
                   'longitude': 'Longitude'}

    wapo = wapo[wapo['race'] == 'B']
    keys = [key for key in rename_dict.keys()]
    wapo = wapo[keys]
    wapo = wapo.rename(columns=rename_dict)
    wapo = wapo.fillna(0)
    wapo['Age'] = wapo['Age'].astype(int)
    wapo['Gender'] = wapo['Gender'].replace(['M', 'F'], ['Male', 'Female'])
    wapo['Incident Date (MM/DD/YYYY)'] = pd.to_datetime(wapo['Incident Date (MM/DD/YYYY)'])
    return wapo
    
def standardize_mpv(mpv):
    rename_dict = {'name': 'Victim\'s name',
                   'age': 'Age',
                   'gender': 'Gender', 
                   'date': 'Incident Date (MM/DD/YYYY)',
                   'street_address': 'Incident Location/Address',
                   'city': 'City',
                   'state': 'State',
                   'zip': 'Zip Code',
                   'county': 'County',
                   'agency_responsible': 'Agency responsible for death',
                   'cause_of_death': 'Cause of death',
                   'circumstances': 'A brief description of the circumstances surrounding the death',
                   'disposition_official': 'Official disposition of death (justified or other)',
                   'officer_charged': 'Criminal Charges?',
                   'news_urls': 'Link to news article or photo of official document',
                   'signs_of_mental_illness': 'Symptoms of mental illness?',
                   'allegedly_armed': 'Unarmed/Did Not Have an Actual Weapon',
                   'wapo_armed': 'Alleged Weapon (Source: WaPo and Review of Cases Not Included in WaPo Database)',
                   'wapo_threat_level': 'Alleged Threat Level (Source: WaPo)',
                   'wapo_flee': 'Fleeing (Source: WaPo)',
                   'wapo_body_camera': 'Body Camera (Source: WaPo)',
                   'wapo_id': 'WaPo ID (If included in WaPo database)',
                   'off_duty_killing': 'Off-Duty Killing',
                   'latitude': 'Latitude',
                   'longitude': 'Longitude'}
    
    mpv = mpv[mpv['race'] == 'Black']
    keys = [key for key in rename_dict.keys()]
    mpv = mpv[keys]
    mpv = mpv.rename(columns=rename_dict)
    mpv = mpv.fillna(0)
    mpv['Age'] = mpv['Age'].astype(int)
    mpv['Incident Date (MM/DD/YYYY)'] = pd.to_datetime(mpv['Incident Date (MM/DD/YYYY)'])
    return mpv

normalize()






                   

