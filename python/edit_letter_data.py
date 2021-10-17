import xml.etree.ElementTree as ET
from lxml import etree
from html.entities import codepoint2name
import pprint
import re
import csv
from pywikibot.data import api
import pywikibot
import requests
from pywikibot import pagegenerators as pg
import pandas as pd
from csv import writer
from csv import reader
import time
import numpy as np
import sys


def edit_letter_info_csv():
    colnames = ['Letter_ID','Sender_ID','Sender_Name','Recipient_ID','Recipient_Name','Date','Dispatch_Location','Dispatch_Location_Abbr','Mentioned_Person_ID','Mentioned_Person','Mentioned_Org_ID','Mentioned_Org','Mentioned_Places_Abbr','Mentioned_Places','Recipient_Adress']
    person_org_col = ['XML_ID', 'Wikidata_ID', 'Viaf_ID', 'NHRP_ID', 'Given_Name', 'Surname', 'Name', 'Year_of_Birth',
                'Year_of_Death', 'Lifespan', 'Country_of_citizenship', 'Occupation', 'Instance', 'Gender',
                'Brief_Description']
    work_file = pd.read_csv('letter_information_1844-1871.csv', names=colnames, na_filter=False)
    pers_org_file = pd.read_csv('final_pers_org_details.csv',names=person_org_col, na_filter=False)

    letter_id = work_file.Letter_ID.tolist()
    s_id = work_file.Sender_ID.tolist()
    s_name = work_file.Sender_Name.tolist()
    recip_id = work_file.Recipient_ID.tolist()
    recip_name = work_file.Recipient_Name.tolist()
    date = work_file.Date.tolist()
    disp_location = work_file.Dispatch_Location.tolist()
    disp_loc_abbr = work_file.Dispatch_Location_Abbr.tolist()
    ment_per_id = work_file.Mentioned_Person_ID.tolist()
    ment_pers = work_file.Mentioned_Person.tolist()
    ment_org_abbr = work_file.Mentioned_Org_ID.tolist()
    ment_org = work_file.Mentioned_Org.tolist()
    ment_pla_abbr = work_file.Mentioned_Places_Abbr.tolist()
    ment_place = work_file.Mentioned_Places.tolist()
    recip_addr = work_file.Recipient_Adress.tolist()

    register_name = pers_org_file.Name.tolist()
    register_id = pers_org_file.XML_ID.tolist()

    #pprint.pprint(s_id)
    # print(len(sender_id))

    new_sender_names = ['Sender_Name']

    for i in range(1,334):
        sender_name = ' '.join(s_name[i].split())
        sender_id = s_id[i]
        if sender_name == 'IBSEN, HENRIK':
            sender_name = 'HENRIK IBSEN'
        new_sender_names.append(sender_name)

    #print(new_sender_names[163])


edit_letter_info_csv()