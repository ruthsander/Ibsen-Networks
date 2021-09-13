import xml.etree.ElementTree as ET
from lxml import etree
from html.entities import codepoint2name
import pprint

#  declaring all namespaces present in the xml files
ns = {'HIS': 'http://www.example.org/ns/HIS',
      'xml': 'http://www.w3.org/XML/1998/namespace',
      'tei': 'http://www.tei-c.org/ns/1.0'}

tree = etree.parse('../github/Ibsen-Networks/xml-data/Navneregister_HISe.xml')
root = tree.getroot()
persons = tree.xpath('.//tei:div[@type="person"or@type="organisation"]', namespaces=ns)  # ADD tei: IN XPATH
names = tree.xpath('//tei:item[@rend="name"]', namespaces=ns)


def person_id(a):
    #person_count = 0
    for person in a:
        attributes = person.attrib
        # print(attributes)
        if '{http://www.w3.org/XML/1998/namespace}id' in attributes:
            xmlid = attributes['{http://www.w3.org/XML/1998/namespace}id']
            print(xmlid)
        else:
            print(str('-'))

        # person_count += 1
    # CHECK THE NUMBER OF ENTRIES READ FROM THE PERSON INDEX
    # print(str('Number of letters/ids: ') + str(person_count))


# (person_id(persons))
# print(str('Number of letters: ') + str(len(persons)))

def given_names(b):
    name_count = 0
    for name in b:
        given_name = name.xpath('./tei:persName/tei:forename/text()', namespaces=ns)
        #print(given_name)

        if not given_name:
            print(str('-'))
        else:
            print(given_name[0])   # ONLY ONE ITEM IN LIST
            # print(name.find('tei:forname', namespaces=ns).text)
        name_count += 1
    # CHECK THE NUMBER OF ENTRIES READ FROM THE PERSON INDEX
    print(str('Number of names: ') + str(name_count))


# print(names.text)
print(str('Number of letters: ') + str(len(names)))
given_names(names)
# print(root)