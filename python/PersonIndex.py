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

### This script is the first step in collecting relevant information from the person-register xml ###

#  declaring all namespaces present in the xml files
ns = {'HIS': 'http://www.example.org/ns/HIS',
      'xml': 'http://www.w3.org/XML/1998/namespace',
      'tei': 'http://www.tei-c.org/ns/1.0'}

# declare root and xpath to specific elements
tree = etree.parse('../github/Ibsen-Networks/xml-data/Navneregister_HISe.xml')
root = tree.getroot()
# ADD tei: IN XPATH
persons_org = tree.xpath('.//tei:div[@xml:id and @type="person"or@type="organisation"]', namespaces=ns)
names = tree.xpath(
    '//tei:div[@xml:id and @type="person"or@type="organisation"]/tei:list/tei:item[@rend="name"]', namespaces=ns)


# desc = tree.xpath('//tei:list/tei:item[@rend="briefDescription"]', namespaces=ns) NOT USED

# collect the xml-id of each person/organization
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

# collect the given name of each person. If no name is found an empty string in added
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

# collect the surname name of each person. If no name is found an empty string in added
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

# collect the full name of each person. If no name is found an empty string in added
# the names of organisations are retrieved from a different element
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

# retrieve birth date per person. If no date is found an empty string is added
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

# retrieve death date per person. If no date is found an empty string is added
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

# the birth and death dates are combined to create the lifespan
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

# retrieve the person's /organization's short description. If the element <tei:item[@rend="briefDescription"]>
# has a child node then then entire element is retrieved as a string and cleaned
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

# retrieve wikidata ids base on the person/organization name
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


# collect previously collected information and compile it into a csv.
# !!! this csv, specifically the wiki_ids, have to be corrected manually. Any changes are
# saved under 'practice_person_info_edited.csv' !!!
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

# using the edited cvs 'practice_person_info_edited.csv' further information is queried from Wikidata
def retrieve_further_data():
    colnames = ['XML-ID', 'Wikidata_ID', 'Given_Name', 'Surname', 'Name', 'Year_of_Birth', 'Year_of_Death', 'Lifespan',
                'Brief_Description']
    data_csv = pd.read_csv('practice_person_info_edited.csv', names=colnames, na_filter=False)
    q_ids = data_csv.Wikidata_ID.tolist()
    # q_ids.fillna('', inplace=True)
    # print(q_ids)
    # print(len(q_ids))

    # the data being quiried from wikidata
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

    # the queries are performed in groups of 300-400 to prevent the script from ending unexpectedly
    # the ranges used are: (1, 300), (301, 600), (601, 900), (901, 1300), (1301-1703)
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

            # compile all queried data into dictionaries
            for item in data['results']['bindings']:
                # try:
                #   item['item']['value']
                #   details_Qid.append(item['item']['value'])
                # except KeyError:
                #     details_Qid.append(str(''))

                try:
                    # item['item']['value']
                    details_instance.append(item['instanceLabel']['value'])
                except KeyError:
                    details_instance.append(str(''))

                try:
                    # item['genderLabel']['value']
                    details_gender.append(item['genderLabel']['value'])
                except KeyError:
                    details_gender.append(str(''))

                try:
                    # item['viaf']['value']
                    details_viaf.append(item['viaf']['value'])
                except KeyError:
                    details_viaf.append(str(''))

                try:
                    # item['nhrpId']['value']
                    details_nhrp.append(item['nhrpId']['value'])
                except KeyError:
                    details_nhrp.append(str(''))

                try:
                    # item['nationalityLabel']['value']
                    details_nat.append(item['nationalityLabel']['value'])
                except KeyError:
                    details_nat.append(str(''))

                try:
                    # item['nationalityLabel']['value']
                    details_occup.append(item['occupationLabel']['value'])
                except KeyError:
                    details_occup.append(str(''))

                # pprint.pprint(data['results']['bindings'])
                time.sleep(2)

        except ValueError:
            print(str('Error at') + str(index))
            break
    return details_instance, details_gender, details_viaf, details_nhrp, details_nat, details_occup


# retrieve_further_data()
details_instance, details_gender, details_viaf, details_nhrp, details_nat, details_occup = retrieve_further_data()


# create intermediate csv files containing the collected data from wikidate for each range group
def intermediate_csv(list_details_instance, list_details_gender, list_details_viaf, list_details_nhrp, list_details_nat,
                     list_details_occup):
    # match the name of the csv according to the range group being processed in the previous function
    with open('person_info_new_data_1-300.csv', 'w', ) as work_csv:
        wr = csv.writer(work_csv, delimiter=',')
        rows = zip(list_details_instance, list_details_gender, list_details_viaf, list_details_nhrp, list_details_nat,
                   list_details_occup)
        for row in rows:
            wr.writerow(row)


intermediate_csv(details_instance, details_gender, details_viaf, details_nhrp, details_nat, details_occup)


# compile the data collected in the previous functions and write a new csv file
# this function should remain commented out until all intermediate csv file have been written.
# the functions 'intermediate_csv', 'retrieve_further_data' and 'write_csv' are not necessary for this step
def final_csv(ids, names_given, last_name, names_full, year_of_birth, year_of_death, lifespans, descriptions):
    colnames = ['Instance', 'Gender', 'Viaf_Id', 'NHRP_ID', 'Country_of_citizenship', 'Occupation']
    data_csv_p1 = pd.read_csv('person_info_new_data_1-300.csv', names=colnames, na_filter=False)
    data_csv_p2 = pd.read_csv('person_info_new_data_301-600.csv', names=colnames, na_filter=False)
    data_csv_p3 = pd.read_csv('person_info_new_data_601-900.csv', names=colnames, na_filter=False)
    data_csv_p4 = pd.read_csv('person_info_new_data_901-1300.csv', names=colnames, na_filter=False)
    data_csv_p5 = pd.read_csv('person_info_new_data_1301-1703.csv', names=colnames, na_filter=False)

    instance_1 = data_csv_p1.Instance.tolist()
    instance_2 = data_csv_p2.Instance.tolist()
    instance_3 = data_csv_p3.Instance.tolist()
    instance_4 = data_csv_p4.Instance.tolist()
    instance_5 = data_csv_p5.Instance.tolist()

    gender_1 = data_csv_p1.Gender.tolist()
    gender_2 = data_csv_p2.Gender.tolist()
    gender_3 = data_csv_p3.Gender.tolist()
    gender_4 = data_csv_p4.Gender.tolist()
    gender_5 = data_csv_p5.Gender.tolist()

    viaf_1 = data_csv_p1.Viaf_Id.tolist()
    viaf_2 = data_csv_p2.Viaf_Id.tolist()
    viaf_3 = data_csv_p3.Viaf_Id.tolist()
    viaf_4 = data_csv_p4.Viaf_Id.tolist()
    viaf_5 = data_csv_p5.Viaf_Id.tolist()

    nhrp_1 = data_csv_p1.NHRP_ID.tolist()
    nhrp_2 = data_csv_p2.NHRP_ID.tolist()
    nhrp_3 = data_csv_p3.NHRP_ID.tolist()
    nhrp_4 = data_csv_p4.NHRP_ID.tolist()
    nhrp_5 = data_csv_p5.NHRP_ID.tolist()

    country_1 = data_csv_p1.Country_of_citizenship.tolist()
    country_2 = data_csv_p2.Country_of_citizenship.tolist()
    country_3 = data_csv_p3.Country_of_citizenship.tolist()
    country_4 = data_csv_p4.Country_of_citizenship.tolist()
    country_5 = data_csv_p5.Country_of_citizenship.tolist()

    occupation_1 = data_csv_p1.Occupation.tolist()
    occupation_2 = data_csv_p2.Occupation.tolist()
    occupation_3 = data_csv_p3.Occupation.tolist()
    occupation_4 = data_csv_p4.Occupation.tolist()
    occupation_5 = data_csv_p5.Occupation.tolist()

    # print(len(nhrp_5))
    instance_list = ['Instance']
    gender_list = ['Gender']
    viaf_list = ['Viaf ID']
    nhrp_list = ['NHRP ID']
    country_list = ['Country of coitizenship']
    occupation_list = ['Occupation']

    for index in range(1, 300):
        instance_list.append(instance_1[index])
        gender_list.append(gender_1[index])
        viaf_list.append(viaf_1[index])
        nhrp_list.append(nhrp_1[index])
        country_list.append(country_1[index])
        occupation_list.append(occupation_1[index])
        # return instance_list

    for index in range(1, 301):
        instance_list.append(instance_2[index])
        gender_list.append(gender_2[index])
        viaf_list.append(viaf_2[index])
        nhrp_list.append(nhrp_2[index])
        country_list.append(country_2[index])
        occupation_list.append(occupation_2[index])
        # return instance_list

    for index in range(1, 301):
        instance_list.append(instance_3[index])
        gender_list.append(gender_3[index])
        viaf_list.append(viaf_3[index])
        nhrp_list.append(nhrp_3[index])
        country_list.append(country_3[index])
        occupation_list.append(occupation_3[index])
        # return instance_list

    for index in range(1, 401):
        instance_list.append(instance_4[index])
        gender_list.append(gender_4[index])
        viaf_list.append(viaf_4[index])
        nhrp_list.append(nhrp_4[index])
        country_list.append(country_4[index])
        occupation_list.append(occupation_4[index])
        # return instance_list

    for index in range(1, 405):
        instance_list.append(instance_5[index])
        gender_list.append(gender_5[index])
        viaf_list.append(viaf_5[index])
        nhrp_list.append(nhrp_5[index])
        country_list.append(country_5[index])
        occupation_list.append(occupation_5[index])
        # return instance_list

    for i in range(1, 1704):
        instances = instance_list[i]
        xml_ids = ids[i]
        if instances == str(''):
            if xml_ids.startswith('pe'):
                instance_list[i] = str('human')
            else:
                continue

    # print(instance_list)
    # print(len(instance_list))
    # print(gender_list)
    # print(len(gender_list))
    # print(viaf_list)
    # print(len(viaf_list))
    # print(nhrp_list)
    # print(len(nhrp_list))
    # print(occupation_list)
    # print(len(occupation_list))

    colnames2 = ['XML-ID', 'Wikidata_ID', 'Given_Name', 'Surname', 'Name', 'Year_of_Birth', 'Year_of_Death', 'Lifespan',
                 'Brief_Description']
    data_csv = pd.read_csv('practice_person_info_edited.csv', names=colnames2, na_filter=False)
    q_ids = data_csv.Wikidata_ID.tolist()

    rows = zip(ids, q_ids, viaf_list, nhrp_list, names_given, last_name, names_full, year_of_birth, year_of_death,
               lifespans, country_list, occupation_list, instance_list, gender_list, descriptions)
    with open('final_pers_org_details.csv', 'w', ) as work_csv:
        wr = csv.writer(work_csv, delimiter=',')

        for row in rows:
            wr.writerow(row)

# final_csv(id_list, given_name_list, surnames_list, names_list, birth_year_list, death_year_list, lifespan_list, descriptions_list)
