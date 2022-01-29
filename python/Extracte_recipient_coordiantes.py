import re
import csv
import sys
import openpyxl
import pandas as pd


colnames = ['Letter_ID','Sender_ID','Sender_Name','Recipient_ID','Recipient_Name','Date',
            'Dispatch_Location','Dispatch_Location_Abbr','GeoName_ID','toponymName','Country',
            'Latitude','Longitude','Recipient_Adress','Recipient_Location','Recipient_Location_Abbr',
            'Recipient_Addr_Latitude','Recipient_Addr_Longitude','Mentioned_Person_ID',
            'Mentioned_Persons','Mentioned_Org_ID','Mentioned_Org','Mentioned_Works_IDs',
            'Mention_Works_Title','Text_ID','Mention_Works_Genre','Collective_Vesions_ID',
            'Mentioned_Places','Mentioned_Places_Abbr']
work_file = pd.read_csv('Compiled_Letter_Data.csv', names=colnames, na_filter=False)

recip_place = work_file.Recipient_Location.tolist()
# recip_country = work_file.Country.tolist()
recip_lat = work_file.Recipient_Addr_Latitude.tolist()
recip_long = work_file.Recipient_Addr_Longitude.tolist()

with open('All_Recipient_Coordinates.csv', 'w', ) as work_csv:
    wr = csv.writer(work_csv, delimiter=',')

    rows = zip(recip_place,recip_lat,recip_long)
    # rows = list(dict.fromkeys(rows))
    for row in rows:
        wr.writerow(row)
