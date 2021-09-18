import xml.etree.ElementTree as ET
from lxml import etree
from html.entities import codepoint2name
import pprint
import re

#  declaring all namespaces present in the xml files
ns = {'HIS': 'http://www.example.org/ns/HIS',
      'xml': 'http://www.w3.org/XML/1998/namespace',
      'tei': 'http://www.tei-c.org/ns/1.0'}

tree = etree.parse('../github/Ibsen-Networks/xml-data/Navneregister_HISe.xml')
root = tree.getroot()
persons_org = tree.xpath('.//tei:div[@type="person"or@type="organisation"]', namespaces=ns)  # ADD tei: IN XPATH
names = tree.xpath('//tei:item[@rend="name"]', namespaces=ns)
desc = tree.xpath('//tei:list/tei:item[@rend="briefDescription"]', namespaces=ns)


def person_id(a):
    person_count = 0
    for person in a:
        attributes = person.attrib
        # print(person)
        # print(attributes)
        if '{http://www.w3.org/XML/1998/namespace}id' in attributes:
            xmlid = attributes['{http://www.w3.org/XML/1998/namespace}id']
            print(xmlid)
        else:
            print(str('-'))

        person_count += 1
    # CHECK THE NUMBER OF ENTRIES READ FROM THE PERSON INDEX
    print(str('Number of letters/ids: ') + str(person_count))


# (person_id(persons_org))
# print(str('Number of letters: ') + str(len(persons_org)))

def given_names(b):
    name_count = 0
    for name in b:
        given_name = name.xpath('./tei:persName/tei:forename/text()', namespaces=ns)
        # print(given_name)

        if not given_name:
            print(str('-'))
        else:
            print(' '.join(given_name[0].split()))   # ONLY ONE ITEM IN LIST
            # print(name.find('tei:forname', namespaces=ns).text)
        name_count += 1
    # CHECK THE NUMBER OF ENTRIES READ FROM THE PERSON INDEX
    # print(str('Number of names: ') + str(name_count))


# print(names.text)
# print(str('Number of letters: ') + str(len(names)))
# given_names(names)


def surname_names(c):
    name_count = 0
    for name in c:
        surname_name = name.xpath('./tei:persName/tei:surname/text()', namespaces=ns)
        # print(surname_name)

        if not surname_name:
            print(str('-'))
        else:
            print(' '.join(surname_name[0].split()))   # ONLY ONE ITEM IN LIST
        name_count += 1
    # CHECK THE NUMBER OF ENTRIES READ FROM THE PERSON INDEX
    # print(str('Number of names: ') + str(name_count))


# surname_names(names)


def full_names(d):
    name_count = 0
    for name in d:
        name_name = name.xpath('./tei:persName/tei:name/text()', namespaces=ns)
        org_name = name.xpath('./tei:name/text()', namespaces=ns)
        given_name = name.xpath('./tei:persName/tei:forename/text()', namespaces=ns)
        surname_name = name.xpath('./tei:persName/tei:surname/text()', namespaces=ns)
        # print(name_name)

        if name_name and not org_name:
            print(' '.join(name_name[0].split()))  # ONLY ONE ITEM IN LIST
        elif org_name and not name_name:
            print(' '.join(org_name[0].split()))   # ONLY ONE ITEM IN LIST
        elif given_name and surname_name and not name_name and not org_name:
            print(str(' '.join(given_name[0].split()) + str(' ') + ' '.join(surname_name[0].split())))
        elif given_name and not surname_name and not name_name and not org_name:
            print(str(' '.join(given_name[0].split())))
        elif surname_name and not given_name and not name_name and not org_name:
            print(str(' '.join(surname_name[0].split())))
        else:
            print(str('-'))
        name_count += 1
    # CHECK THE NUMBER OF ENTRIES READ FROM THE PERSON INDEX
    # print(str('Number of names: ') + str(name_count))


# full_names(names)


def date_of_birth(e):
    date_count = 0
    person_org_count = 0
    for date in e:
        b_date = date.xpath('./tei:list/tei:item[@rend="date"]/tei:date/@from', namespaces=ns)
        if not b_date:
            print(str('-'))
        else:
            print(b_date[0])
            date_count += 1
        person_org_count += 1
    print(str('Number of birth dates: ') + str(date_count))
    print(str('Number of persons/organisations: ') + str(person_org_count))


# date_of_birth(persons_org)


def date_of_death(f):
    date_count = 0
    person_org_count = 0
    for date in f:
        d_date = date.xpath('./tei:list/tei:item[@rend="date"]/tei:date/@to', namespaces=ns)
        if not d_date:
            print(str('-'))
        else:
            print(d_date[0])
            date_count += 1
        person_org_count += 1
    print(str('Number of death dates: ') + str(date_count))
    print(str('Number of persons/organisations: ') + str(person_org_count))


# date_of_death(persons_org)


def lifespan(g):
    date_count = 0
    person_org_count = 0
    for date in g:
        b_date = date.xpath('./tei:list/tei:item[@rend="date"]/tei:date/@from', namespaces=ns)
        d_date = date.xpath('./tei:list/tei:item[@rend="date"]/tei:date/@to', namespaces=ns)

        if b_date and not d_date:
            print(b_date[0] + str('-'))  # ONLY ONE ITEM IN LIST
            date_count += 1
        elif d_date and not b_date:
            print(str('-') + d_date[0])  # ONLY ONE ITEM IN LIST
            date_count += 1
        elif b_date and d_date:
            print(b_date[0] + str('-') + d_date[0])
            date_count += 1
        else:
            print(str('-'))
        person_org_count += 1
    # CHECK THE NUMBER OF ENTRIES READ FROM THE PERSON INDEX
    print(str('Number of dates: ') + str(date_count))
    print(str('Number of persons/organisations: ') + str(person_org_count))


# lifespan(persons_org)


def person_org_desc(h):
    desc_count = 0
    person_org_count = 0
    for pers_org in h:
        description = pers_org.xpath('./tei:list/tei:item[@rend="briefDescription"]/text()', namespaces=ns)
        description_full = (pers_org.xpath('./tei:list/tei:item[@rend="briefDescription"]', namespaces=ns))
        child = pers_org.xpath('./tei:list/tei:item[@rend="briefDescription"]/HIS:hisRef', namespaces=ns)

        if not description_full:
            print(str('-'))
            # desc_count +=1
        elif not child and len(description_full) == 1:
            print(' '.join(description[0].split()))
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

                print(multiple_replace(replace_string, cleaned_str))
            desc_count += 1

        person_org_count += 1
    print(str('Number of descriptions: ') + str(desc_count))
    print(str('Number of persons/organisations: ') + str(person_org_count))


person_org_desc(persons_org)

# XML_tree = etree.fromstring(XML_content)
# text = XML_tree.xpath('string(//text[@title="book"]/div/div/p)')
