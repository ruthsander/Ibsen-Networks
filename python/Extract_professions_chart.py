import re
import csv
import sys
import openpyxl
import pandas as pd


colnames = ['XML_ID','Wikidata_ID','Viaf_ID','NHRP_ID','Given_Name','Surname','Name',
            'Year_of_Birth','Year_of_Death','Lifespan','Instance','Gender',
            'Country_of_citizenship','Occupation','Letters_Received','Times_Mentioned',
            'Brief_Description','Spouses_Name','Spouses_ID']
work_file = pd.read_csv('Person_Register_Info.csv', names=colnames, na_filter=False)

professions = work_file.Occupation.tolist()
name = work_file.Name.tolist()
id = work_file.XML_ID.tolist()


expand_id = []
expand_name = []
expand_prof = []

occupation = []
occup_frequency = []

for a,b,c in zip(id, name, professions):
    if a == '' and b == '' and c == '':
        continue
    else:
        prof_tokens = c.split(', ')
        for token in prof_tokens:
            # print(token)
            expand_id.append(a)
            expand_name.append(b)
            expand_prof.append(token)

for o in expand_prof:
    if o not in occupation:
        occupation.append(o)
        occup_frequency.append(1)
    else:
        index = occupation.index(o)
        occup_frequency[index] = occup_frequency[index]+1


with open('Occupation_freq.csv', 'w', ) as work_csv:
    wr = csv.writer(work_csv, delimiter=',')

    rows = zip(occupation, occup_frequency)
    # rows = list(dict.fromkeys(rows))
    for row in rows:
        wr.writerow(row)
