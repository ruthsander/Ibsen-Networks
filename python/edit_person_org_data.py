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

#  declaring all namespaces present in the xml files
ns = {'HIS': 'http://www.example.org/ns/HIS',
      'xml': 'http://www.w3.org/XML/1998/namespace',
      'tei': 'http://www.tei-c.org/ns/1.0'}

tree = etree.parse('../github/Ibsen-Networks/xml-data/Navneregister_HISe.xml')
regest_entries = tree.xpath('//tei:div[@xml:id and @type="person" or @type="organisation"]', namespaces=ns)


def count_letters_to_person(reg_entries):
    n_letters_received = {'XML_ID': 'Letters_Received'}
    mentions_list = {'XML_ID': 'Times_Mentioned'}
    for entry in reg_entries:
        xml_id = entry.attrib['{http://www.w3.org/XML/1998/namespace}id']
        received = entry.xpath('.//tei:div/tei:list[@type="recipient_letter"]/tei:item', namespaces=ns)
        mentions = entry.xpath('.//tei:div/tei:list[@type="mentioned_letter"]/tei:item', namespaces=ns)

        n_letters_received[xml_id] = (len(received))
        mentions_list[xml_id] = (len(mentions))

    return n_letters_received, mentions_list





# print(n_letter_received)
# print(n_mentions)


def edit_person_org_csv():
    colnames = ['XML_ID', 'Wikidata_ID', 'Viaf_ID', 'NHRP_ID', 'Given_Name', 'Surname', 'Name', 'Year_of_Birth',
                'Year_of_Death', 'Lifespan', 'Country_of_citizenship', 'Occupation', 'Instance', 'Gender',
                'Brief_Description']
    prof_col = ['Norsk','English']
    work_file = pd.read_csv('final_pers_org_details.csv', names=colnames, na_filter=False)
    prof_file = pd.read_csv('occupations_list.csv',names=prof_col, na_filter=False)

    xmlID = work_file.XML_ID.tolist()
    wikidataID = work_file.Wikidata_ID.tolist()
    viafID = work_file.Viaf_ID.tolist()
    nhrpID = work_file.NHRP_ID.tolist()
    givenName = work_file.Given_Name.tolist()
    surname = work_file.Surname.tolist()
    name = work_file.Name.tolist()
    yearBirth = work_file.Year_of_Birth.tolist()
    yearDeath = work_file.Year_of_Death.tolist()
    lifespan = work_file.Lifespan.tolist()
    citizenship = work_file.Country_of_citizenship.tolist()
    occupation = work_file.Occupation.tolist()
    instance = work_file.Instance.tolist()
    gender = work_file.Gender.tolist()
    description = work_file.Brief_Description.tolist()
    occup_norsk = prof_file.Norsk.tolist()
    occup_eng = prof_file.English.tolist()

    instance_label = []
    for label in instance:
        if label not in instance_label:
            if label == str(''):
                continue
            else:
                instance_label.append(label)
    #pprint.pprint(instance_label)

    prof_label = []
    for prof in occupation:
        if prof not in prof_label:
            if prof == str(''):
                continue
            else:
                prof_label.append(prof)
    #pprint.pprint(prof_label)

    dict_instance_label = {'bank': 'bank',
                           'stiftet': 'foundation',
                           'embetskontor': 'civil service office',
                           'forening': 'society',
                           'studentforening': 'student society',
                           'studentforeningsstyre': 'student society board',
                           'bokhandel': 'bookshop',
                           'forlag': 'publisher',
                           'bokhandel og forlag': 'bookshop, publisher',
                           'organisasjon': 'organization',
                           'universitetsstyre': 'university board',
                           'litterært selskap': 'literary society',
                           'teater': 'theatre',
                           'interesseorganisasjon': 'interest group',
                           #'interesseorganisasjon og teateragentur': 'interest group, theatre agency',
                           'bedriftsstyre': 'company board',
                           'byrett': 'court',
                           'departement': 'ministry',
                           'fotograf': 'photographer',
                           'hotell': 'hotel',
                           'komit': 'commitee',
                           'statsoverhode': 'head of state',
                           #'teater, opera og ballett': 'theatre, opera, ballet',
                           'ballett':'ballet',
                           'arbeidersamfunn': 'writers’ organization',
                           'etat': 'budgetary',
                           'tidsskrift': 'magazine',
                           'forretningsfører': 'society head',
                           'hoffembete': '',
                           'bedrift': 'company',
                           'lokaladministrativ enhet': 'local administrative unit',
                           'fetevareforretning': ''}

    titles = {'fyrst':'Prince',
              'prins':'Prince',
              'dronning':'Queen',
              'keiser': 'Emperor',
              'prinsesse': 'Princess',
              'greve': 'Count',
              'sultan': 'Sultan',
              'emir': 'Commander/Prince',
              'grevinne':'Countess',
              'kong':'King'}

    gender_indicators = [
        'hustru',
        'mor',
        'datter',
        'prinsesse',
        'dronning',
        'inne']

    nationality = {
        'norsk':'Norway',
        'dansk':'Denmark',
        'svensk':'Sweden',
        'tysk':'Germany',
        'østerriksk': 'Austria',
        'sveitsisk':'Switzerland',
        'engelsk':'England',
        'italiensk':'Italy',
        'spansk':'Spain',
        'fransk':'France',
        'gresk':'Greece',
        'polsk':'Poland',
        'amerikansk':'United States of America',
        'russisk':'Russia',
        'tsjekkisk':'Czechoslovakia',
        'britisk': 'United Kingdom of Great Britain and Ireland'
    }

    dict_occup = {}
    for line in range(1, 229):
        norsk = occup_norsk[line]
        eng = occup_eng[line]
        dict_occup[norsk] = eng


    new_inst_list = ['Instance']
    new_occup_list = ['Occupation']
    new_gender_list = ['Gender']
    new_nationality_list = ['Country_of_citizenship']
    for i in range(1, 1704):
        inst = instance[i]
        desc = description[i]
        professions = occupation[i]
        gen = gender[i]
        citi_ship = citizenship[i]
        xmlid = xmlID[i]

        # add missing instnaces
        if inst == str(''):
            key_list = []
            for key in dict_instance_label:
                if key in desc:
                    key_list.append(dict_instance_label[key])
            if 'org' in xmlid:
                key_list.append('organization')
                #print(dict_instance_label[key])
            #print(key_list)
            # if len(key_list) == 0:
            #     new_inst_list.append(str(''))
            # # elif len(key_list) == 1:
            # #     new_inst_list.append(key_list[0])
            # else:
            new_inst_list.append(key_list)
        else:
            inst_list = []
            if inst == 'human':
                inst_list.append(inst)
                for title in titles:
                    if title in desc:
                        inst_list.append(titles[title])
                    else:
                        continue

            elif 'org' in xmlid:
                inst_list.append('organization')
                inst_list.append(inst)

            #pprint.pprint(inst_list)
            if 'Princess' in inst_list:
                inst_list.remove('Prince')

            new_inst_list.append(inst_list)

        # add missing occupations
        temp_occup_list = []
        if professions != str(''):
            temp_occup_list.append(professions)

        if 'human' not in new_inst_list[i]:
            temp_occup_list.append('organization')
        else:
            for k in dict_occup:
                if k in desc:
                    if dict_occup[k] in temp_occup_list:
                        continue
                    else:
                        temp_occup_list.append(dict_occup[k])

            if 'literary historian' in temp_occup_list:
                for items in temp_occup_list:
                    if items == 'literarian':
                        temp_occup_list.remove(items)
                    if items == 'historian':
                        temp_occup_list.remove(items)

            if 'housewife' in temp_occup_list:

                for item in temp_occup_list:
                    if item != 'housewife':
                        temp_occup_list.remove(item)
                    else:
                        continue
                if len(temp_occup_list) >= 1:
                    for item in temp_occup_list:
                        if item != 'housewife':
                            temp_occup_list.remove(item)

        new_occup_list.append(temp_occup_list)

        # add missing genders
        new_occup = new_occup_list[i]
        if gen != str(''):
            new_gender_list.append(gen)
        else:
            if 'organization'in new_occup:
                new_gender_list.append(str(''))
            else:
                if any(indicator in desc for indicator in gender_indicators):
                    new_gender_list.append('female')
                else:
                    new_gender_list.append('male')

        # add missing citizenship information
        if citi_ship == str(''):
            nat_list = []
            if 'hustru' in desc:
                nat_list.append(str(''))
            else:
                for k in nationality:
                    if k in desc:
                        nat_list.append(nationality[k])
            new_nationality_list.append(nat_list)
        else:
            new_nationality_list.append(citi_ship)
            #print(nat_list)


    for x in range(len(new_nationality_list)):
        new_input = re.sub('\[', '', re.sub('\]', '', re.sub('\'', '',str(new_nationality_list[x]))))
        new_nationality_list[x]=new_input

    #pprint.pprint(new_nationality_list)
    #print(len(new_nationality_list))
    #pprint.pprint(new_nationality_list)
    #print(len(new_nationality_list))

    return new_inst_list,new_gender_list,new_nationality_list, new_occup_list


n_letter_received, n_mentions = count_letters_to_person(regest_entries)
#print(n_letter_received)
new_i_list, new_g_list,new_n_list,new_occup_list = edit_person_org_csv()

def combile_to_csv(instance, gender,citizenship,occupation,n_letter_received, n_mentions):
    colnames = ['XML_ID', 'Wikidata_ID', 'Viaf_ID', 'NHRP_ID', 'Given_Name', 'Surname', 'Name', 'Year_of_Birth',
                'Year_of_Death', 'Lifespan', 'Country_of_citizenship', 'Occupation', 'Instance', 'Gender',
                'Brief_Description']
    work_file = pd.read_csv('final_pers_org_details.csv', names=colnames, na_filter=False)

    xmlID = work_file.XML_ID.tolist()
    wikidataID = work_file.Wikidata_ID.tolist()
    viafID = work_file.Viaf_ID.tolist()
    nhrpID = work_file.NHRP_ID.tolist()
    givenName = work_file.Given_Name.tolist()
    surname = work_file.Surname.tolist()
    name = work_file.Name.tolist()
    yearBirth = work_file.Year_of_Birth.tolist()
    yearDeath = work_file.Year_of_Death.tolist()
    lifespan = work_file.Lifespan.tolist()
    description = work_file.Brief_Description.tolist()
    n_l_received = []
    n_mention = []

    for key in n_letter_received:
        n_l_received.append(n_letter_received[key])

    for keys in n_mentions:
        n_mention.append(n_mentions[keys])

    rows = zip(xmlID,wikidataID,viafID,nhrpID,givenName,surname,name,yearBirth,yearDeath,lifespan,instance, gender,citizenship,occupation,n_l_received, n_mention,description)
    with open('Person_Register_Info.csv', 'w', ) as work_csv:
        wr = csv.writer(work_csv, delimiter=',')

        for row in rows:
            wr.writerow(row)


combile_to_csv(new_i_list, new_g_list,new_n_list,new_occup_list, n_letter_received, n_mentions)