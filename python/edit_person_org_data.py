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


n_letter_received, n_mentions = count_letters_to_person(regest_entries)
print(n_letter_received)
print(n_mentions)


# Add missing organisation types
def edit_person_org_csv():
    colnames = ['XML_ID','Wikidata_ID','Viaf_ID','NHRP_ID','Given_Name','Surname','Name','Year_of_Birth','Year_of_Death','Lifespan','Country_of_citizenship','Occupation','Instance','Gender','Brief_Description']
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
    citizenship = work_file.Country_of_citizenship.tolist()
    occupation = work_file.Occupation.tolist()
    instance = work_file.Instance.tolist()
    gender = work_file.Gender.tolist()
    description = work_file.Brief_Description.tolist()


# edit_person_org_csv()