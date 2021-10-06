import xml.etree.ElementTree as ET
from lxml import etree
from html.entities import codepoint2name
import pprint
import re
import csv

#  declaring all namespaces present in the xml files
ns = {'HIS': 'http://www.example.org/ns/HIS',
      'xml': 'http://www.w3.org/XML/1998/namespace',
      'tei': 'http://www.tei-c.org/ns/1.0'}

tree = etree.parse('../github/Ibsen-Networks/xml-data/B1844-1871ht.xml')
root = tree.getroot()
letter_short_info = tree.xpath('//HIS:hisMsDesc[@type="letter"]', namespaces=ns)
letter_text = tree.xpath('.//tei:text[@rend="letter"]', namespaces=ns)

#   Header = root[0]

# retrieve all letter ids
processed_letters = 0
info_ids = []
for entry in letter_short_info:

    letter_info = entry.xpath('.//HIS:letterinfo[@corresp]', namespaces=ns)
    attributes_corresp = letter_info[0].attrib
    corresp = attributes_corresp['corresp']
    info_ids.append(corresp)

    sender = entry.xpath('.//HIS:letterinfo/tei:name[@role="sender"]/HIS:hisRef', namespaces=ns)
    nsender = len(sender)
    # print(sender)
    # print(nsender)

# retrieve all senders
    all_senders = []
    for i in range(0, nsender):
        s = sender[i]
        attribites_sender = s.attrib
        sender_id = attribites_sender['target']
        edit_sender_id = re.sub('Navneregister_HISe.xml#', '', sender_id)
        all_senders.append(edit_sender_id)

# retrieve letter recipients
    recipient = entry.xpath('.//HIS:letterinfo/tei:name[@role="recipient"]/HIS:hisRef', namespaces=ns)
    nrecioient = len(recipient)
    all_recipients= []
    for j in range(0, nrecioient):
        r = recipient[j]
        attribites_recipient = r.attrib
        recipient_id = attribites_recipient['target']
        edit_recipient_id = re.sub('Navneregister_HISe.xml#', '', recipient_id)
        all_recipients.append(edit_recipient_id)

# retrieve dispatch date
    dispatch_dates = entry.xpath('.//HIS:letterinfo/tei:origDate', namespaces=ns)
    #print(dispatch_dates)
    attributes_dates = dispatch_dates[0].attrib
    # print(attributes_dates)
    if 'when' in attributes_dates:
        date = str(attributes_dates['when'])
    elif 'notBefore' in attributes_dates and 'notAfter' in attributes_dates:
        date = str(attributes_dates['notBefore'] + str(' - ') + attributes_dates['notAfter'])
    else:
        date = str('unknown')

# retrieve dispatch locations
    dispatch_location = entry.xpath('.//HIS:letterinfo/tei:origPlace/HIS:hisRef', namespaces=ns)
    attributes_loc = dispatch_location[0].attrib
    edit_loc_abr = re.sub('Navneregister_HISe.xml#pl', '', attributes_loc['target'])
    loc_full = dispatch_location[0].text



    #print(corresp + str(' + ') + str(all_senders)+ str(' + ') + str(all_recipients) + str(' + ') + date + str(' + ') + edit_loc_abr + str(' + ') + loc_full)
    processed_letters +=1
#print(str('Number of letters/xmlids: ') + str(processed_letters))

letter_texts = {}
text_number = 0
for corres in letter_text:
    # retrieve sending address
    text_corresp = corres.attrib
    corresp_text_id = text_corresp['corresp']
    #print(text_corresp)

    send_to = corres.xpath('.//HIS:envelope/tei:address', namespaces=ns)
    print(send_to)
    letter_texts[corresp_text_id] = {}

    text_number +=1
#print(str('Number of letters/xmlids: ') + str(text_number))

#print(info_ids)
#print(letter_texts)


# xmlns = root.get('xmlns')
# print(sorted(root.keys()))
# print(xmlns)
#
# xmlid = r.get('xml:id', namespaces={'xml': 'http://www.tei-c.org/ns/1.0'})
# pprint.pprint(xmlid)
#
#
# print(root.tag)
#
# pprint.pprint(r)
# print(str('Number of letters: ')+str(len(r)))

