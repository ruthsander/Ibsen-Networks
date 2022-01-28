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

disp_city = work_file.toponymName.tolist()
disp_country = work_file.Country.tolist()
disp_lat = work_file.Latitude.tolist()
disp_long = work_file.Longitude.tolist()

# disp_city = list(dict.fromkeys(disp_city))
# disp_country = list(dict.fromkeys(disp_country))
# disp_lat = list(dict.fromkeys(disp_lat))
# disp_long = list(dict.fromkeys(disp_long))

for a,b,c,d in zip(disp_city,disp_country,disp_lat,disp_long):
    if a == '' and b == '' and c == '' and d == '':
        disp_city.remove(a)
        disp_country.remove(b)
        disp_lat.remove(c)
        disp_long.remove(d)
    else:
        continue


# print(len(disp_city))
# print(disp_city)
# for n in range(1,2410):
#     city = disp_city[n]
#     country = disp_country[n]
#     lat = disp_lat[n]
#     long = disp_long[n]

    # if city == '' and country == '' and lat == '' and long == '':
    #     disp_city.remove(city)
    #     disp_country.remove(country)
    #     disp_lat.remove(lat)
    #     disp_long.remove(long)

with open('All_Sender_Coordinates.csv', 'w', ) as work_csv:
    wr = csv.writer(work_csv, delimiter=',')

    rows = zip(disp_city,disp_country,disp_lat,disp_long)
    # rows = list(dict.fromkeys(rows))
    for row in rows:
        wr.writerow(row)
