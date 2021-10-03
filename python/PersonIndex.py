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
root = tree.getroot()
# ADD tei: IN XPATH
persons_org = tree.xpath('.//tei:div[@xml:id and @type="person"or@type="organisation"]', namespaces=ns)
names = tree.xpath(
    '//tei:div[@xml:id and @type="person"or@type="organisation"]/tei:list/tei:item[@rend="name"]', namespaces=ns)


# desc = tree.xpath('//tei:list/tei:item[@rend="briefDescription"]', namespaces=ns) NOT USED


def person_id(a):
    # person_count = 0
    list_of_ids = ['XML-ID']
    for person in a:
        attributes = person.attrib
        # print(person)
        # print(attributes)
        if '{http://www.w3.org/XML/1998/namespace}id' in attributes:
            xmlid = attributes['{http://www.w3.org/XML/1998/namespace}id']
            # print(xmlid)
            list_of_ids.append(xmlid)
        # elif '{http://www.tei-c.org/ns/1.}corresp' in attributes:
        #     corresp = attributes['{http://www.tei-c.org/ns/1.}corresp']
        #     list_of_ids.append(corresp)
        #     # print(xmlid)
        #     # list_of_ids.append(str('-'))
        #     #print(str('-'))
        else:
            list_of_ids.append(str('-'))
            # person_count += 1
    return list_of_ids

    # CHECK THE NUMBER OF ENTRIES READ FROM THE PERSON INDEX
    # print(str('Number of letters/ids: ') + str(person_count))


# (person_id(persons_org))
# print(str('Number of letters: ') + str(len(persons_org)))

def given_names(b):
    # name_count = 0
    name_list = ['Given Name']
    for name in b:
        given_name = name.xpath('./tei:persName/tei:forename/text()', namespaces=ns)
        # print(given_name)

        if not given_name:
            name_list.append(str(''))
            # print(str('-'))
        else:
            name_list.append(' '.join(given_name[0].split()))
            # print(' '.join(given_name[0].split()))   # ONLY ONE ITEM IN LIST
            # print(name.find('tei:forname', namespaces=ns).text)
        # name_count += 1
    return name_list
    # CHECK THE NUMBER OF ENTRIES READ FROM THE PERSON INDEX
    # print(str('Number of names: ') + str(name_count))


# print(names.text)
# print(str('Number of letters: ') + str(len(names)))
# given_names(names)


def surname_names(c):
    # name_count = 0
    surname_list = ['Surname']
    for name in c:
        surname_name = name.xpath('./tei:persName/tei:surname/text()', namespaces=ns)
        # print(surname_name)

        if not surname_name:
            surname_list.append(str(''))
        else:
            surname_list.append(' '.join(surname_name[0].split()))  # ONLY ONE ITEM IN LIST
        # name_count += 1
    return surname_list
    # CHECK THE NUMBER OF ENTRIES READ FROM THE PERSON INDEX
    # print(str('Number of names: ') + str(name_count))


# surname_names(names)


def full_names(d):
    # name_count = 0
    list_full_name = ['Name']
    for name in d:
        name_name = name.xpath('./tei:persName/tei:name/text()', namespaces=ns)
        org_name = name.xpath('./tei:name/text()', namespaces=ns)
        given_name = name.xpath('./tei:persName/tei:forename/text()', namespaces=ns)
        surname_name = name.xpath('./tei:persName/tei:surname/text()', namespaces=ns)
        # print(name_name)

        if name_name and not org_name:
            list_full_name.append(' '.join(name_name[0].split()))  # ONLY ONE ITEM IN LIST
        elif org_name and not name_name:
            list_full_name.append(' '.join(org_name[0].split()))  # ONLY ONE ITEM IN LIST
        elif given_name and surname_name and not name_name and not org_name:
            list_full_name.append(str(' '.join(given_name[0].split()) + str(' ') + ' '.join(surname_name[0].split())))
        elif given_name and not surname_name and not name_name and not org_name:
            list_full_name.append(str(' '.join(given_name[0].split())))
        elif surname_name and not given_name and not name_name and not org_name:
            list_full_name.append(str(' '.join(surname_name[0].split())))
        else:
            list_full_name.append(str(''))
        # name_count += 1
    return list_full_name
    # CHECK THE NUMBER OF ENTRIES READ FROM THE PERSON INDEX
    # print(str('Number of names: ') + str(name_count))


# full_names(names)


def date_of_birth(e):
    # date_count = 0
    # person_org_count = 0
    list_birth_year = ['Year of Birth']
    for date in e:
        b_date = date.xpath('./tei:list/tei:item[@rend="date"]/tei:date/@from', namespaces=ns)
        if not b_date:
            list_birth_year.append(str(''))
        else:
            list_birth_year.append(b_date[0])
            # date_count += 1
        # person_org_count += 1
    return list_birth_year
    # print(str('Number of birth dates: ') + str(date_count))
    # print(str('Number of persons/organisations: ') + str(person_org_count))


# date_of_birth(persons_org)


def date_of_death(f):
    # date_count = 0
    # person_org_count = 0
    list_death_year = ['Year of Death']
    for date in f:
        d_date = date.xpath('./tei:list/tei:item[@rend="date"]/tei:date/@to', namespaces=ns)
        if not d_date:
            list_death_year.append(str(''))
        else:
            list_death_year.append(d_date[0])
            # date_count += 1
        # person_org_count += 1
    return list_death_year
    # print(str('Number of death dates: ') + str(date_count))
    # print(str('Number of persons/organisations: ') + str(person_org_count))


# date_of_death(persons_org)


def lifespan(g):
    # date_count = 0
    # person_org_count = 0
    list_life = ['Lifespan']
    for date in g:
        b_date = date.xpath('./tei:list/tei:item[@rend="date"]/tei:date/@from', namespaces=ns)
        d_date = date.xpath('./tei:list/tei:item[@rend="date"]/tei:date/@to', namespaces=ns)

        if b_date and not d_date:
            list_life.append(b_date[0] + str('-'))  # ONLY ONE ITEM IN LIST
            # date_count += 1
        elif d_date and not b_date:
            list_life.append(str('-') + d_date[0])  # ONLY ONE ITEM IN LIST
            # date_count += 1
        elif b_date and d_date:
            list_life.append(b_date[0] + str('-') + d_date[0])
            # date_count += 1
        else:
            list_life.append(str(''))
    #     person_org_count += 1
    return list_life
    # CHECK THE NUMBER OF ENTRIES READ FROM THE PERSON INDEX
    # print(str('Number of dates: ') + str(date_count))
    # print(str('Number of persons/organisations: ') + str(person_org_count))


# lifespan(persons_org)


def person_org_desc(h):
    desc_count = 0
    person_org_count = 0
    list_desc = ['Brief Description']
    for pers_org in h:
        description = pers_org.xpath('./tei:list/tei:item[@rend="briefDescription"]/text()', namespaces=ns)
        description_full = (pers_org.xpath('./tei:list/tei:item[@rend="briefDescription"]', namespaces=ns))
        child = pers_org.xpath('./tei:list/tei:item[@rend="briefDescription"]/HIS:hisRef', namespaces=ns)

        if not description_full:
            list_desc.append(str(''))
            # desc_count +=1
        elif not child and len(description_full) == 1:
            list_desc.append(' '.join(description[0].split()))
            desc_count += 1
        else:

            def multiple_replace(replace, string):
                # CREATES REGULAR EXPRESSION FOR DICTIONARY KEYS
                regex = re.compile("(%s)" % "|".join(map(re.escape, replace.keys())))

                # LOOK UP MATCHING VALUE IN DICTIONARY
                return regex.sub(lambda mo: replace_string[mo.string[mo.start():mo.end()]], string)

            if __name__ == "__main__":
                if len(description_full) == 1:
                    text = str(etree.tostring(description_full[0]))
                    remove_tags = re.sub('<[^>]+>', '', text)
                    cleaned_str = ' '.join(remove_tags.split())
                replace_string = {
                    '\'': '',
                    'b': '',
                    r'\n': '',
                    '&#229;': 'å',
                    '&#246;': 'ö',
                    '&#248;': 'ø',
                    '&#252;': 'ü',
                    '&amp;': '&'

                }

                list_desc.append(multiple_replace(replace_string, cleaned_str))
            desc_count += 1

        person_org_count += 1
    return list_desc
    # print(str('Number of descriptions: ') + str(desc_count))
    # print(str('Number of persons/organisations: ') + str(person_org_count))


# person_org_desc(persons_org)

# XML_tree = etree.fromstring(XML_content)
# text = XML_tree.xpath('string(//text[@title="book"]/div/div/p)')


def get_wikidata_ids(target):
    ntarget = len(target)
    list_wikidata_ids = ['Wikidata ID']
    for i in range(1, ntarget):
        entry = target[i]
        remove_bracket_right = entry.replace('[', '')
        remove_bracket_left = remove_bracket_right.replace(']', '')
        search_name = remove_bracket_left

        try:
            def getItems(site, itemtitle):
                params = {'action': 'wbsearchentities', 'format': 'json', 'language': 'en', 'type': 'item',
                          'search': itemtitle}
                request = api.Request(site=site, **params)
                return request.submit()

            # Login to wikidata
            site = pywikibot.Site("wikidata", "wikidata")
            repo = site.data_repository()
            # token = repo.token(pywikibot.Page(repo, 'Main Page'), 'edit')
            wikidataEntries = getItems(site, search_name)
            # Print the different Wikidata entries to the screen
            # prettyPrint(wikidataEntries)

            search_result = wikidataEntries.get('search')
            wiki_id = search_result[0].get('id')
            # print(wiki_id)
            list_wikidata_ids.append(str(wiki_id))
            time.sleep(1)
        except IndexError:
            # print(str(''))
            list_wikidata_ids.append(str(''))
            time.sleep(1)
    return list_wikidata_ids


def write_csv(ids, wiki_id, names_given, last_name, names_full, year_of_birth, year_of_death, lifespans, descriptions):
    # print(ids)
    rows = zip(ids, wiki_id, names_given, last_name, names_full, year_of_birth, year_of_death, lifespans, descriptions)
    with open('practice_person_info.csv', 'w', ) as new_csv:
        wr = csv.writer(new_csv, delimiter=',')

        for row in rows:
            wr.writerow(row)


id_list = (person_id(persons_org))
given_name_list = (given_names(names))
surnames_list = (surname_names(names))
names_list = full_names(names)
birth_year_list = (date_of_birth(persons_org))
death_year_list = (date_of_death(persons_org))
lifespan_list = (lifespan(persons_org))
descriptions_list = (person_org_desc(persons_org))


# w_ids = (get_wikidata_ids(names_list))
# write_csv(id_list, w_ids, given_name_list, surnames_list, names_list, birth_year_list, death_year_list, lifespan_list, descriptions_list)


def retrieve_further_data():
    colnames = ['XML-ID', 'Wikidata_ID', 'Given_Name', 'Surname', 'Name', 'Year_of_Birth', 'Year_of_Death', 'Lifespan',
                'Brief_Description']
    data_csv = pd.read_csv('practice_person_info_edited.csv', names=colnames, na_filter=False)
    q_ids = data_csv.Wikidata_ID.tolist()
    # q_ids.fillna('', inplace=True)
    # print(q_ids)
    # print(len(q_ids))

    # details_Qid = ['Wiki ID']
    details_instance = ['Instance']
    details_gender = ['Gender']
    details_viaf = ['Viaf_Id']
    details_nhrp = ['NHRP_ID']
    details_nat = ['Country_of_citizenship']
    details_occup = ['Occupation']

    # q_is_list =[]
    # entry = (wiki_ids['Wikidata ID'])
    # q_is_list.append(entry)
    #
    # for row in wiki_ids:
    #     print(row)

    for index in range(1, 300):
        try:
            search_id = q_ids[index]
            # print(search_id)
            # for search_id in q_ids:
            # print(search_id)
            # q_is_list.append(value)

            # details = []
            # if search_id == str(''):
            #     #print(str('next'))
            #     # details_Qid.append(str(''))
            #     details_instance.append(str(''))
            #     details_gender.append(str(''))
            #     details_viaf.append(str(''))
            #     details_nhrp.append(str(''))
            #     details_nat.append(str(''))
            #     details_occup.append(str(''))
            #
            # else:
            print(search_id)
            # with open('sparql.rq', 'r') as query_file:
            query = '''PREFIX wikibase: <http://wikiba.se/ontology#>
                PREFIX wd: <http://www.wikidata.org/entity/>
                PREFIX wdt: <http://www.wikidata.org/prop/direct/>
                PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

                SELECT ?item ?instanceLabel ?genderLabel ?viaf ?nhrpId ?nationalityLabel ?occupationLabel WHERE {
                VALUES ?item {wd:Q36661}
                OPTIONAL {?item wdt:P1477 ?itemLabel.}
                OPTIONAL {?item wdt:P31 ?instance.}
                OPTIONAL {?item wdt:P21 ?gender.}
                OPTIONAL {?item wdt:P214 ?viaf.}
                OPTIONAL {?item wdt:P4574 ?nhrpId.}
                OPTIONAL {?item wdt:P27 ?nationality.}
                OPTIONAL {?item wdt:P106 ?occupation.}
                SERVICE wikibase:label {bd:serviceParam wikibase:language "en" .}}
                LIMIT 1'''

            change_values = re.sub('Q36661', search_id, query)

            url = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql'
            data = requests.get(url, params={'query': change_values, 'format': 'json'}).json()

                #for item in data['results']['bindings']:
                    # if item['itemLabel'] == True and item['genderLabel']== True and item['viaf']== True and item['nhrpId']== True and item['nationalityLabel']== True:
                    #     details.append({
                    #         'Name': item['itemLabel']['value'],
                    #         'Gender': item['genderLabel']['value'],
                    #         'VIAF': item['viaf']['value'],
                    #         'nhrpId': item['nhrpId']['value'],
                    #         'nationality': item['nationalityLabel']['value']
                    #     })
                    # else:
                    #     skip
                pprint.pprint(data['results']['bindings'])
                time.sleep(1)


add_further_data()
