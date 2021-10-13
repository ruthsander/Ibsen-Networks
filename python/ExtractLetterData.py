import xml.etree.ElementTree as ET
from lxml import etree
from html.entities import codepoint2name
import pprint
import re
import csv
import dateparser

#  declaring all namespaces present in the xml files
ns = {'HIS': 'http://www.example.org/ns/HIS',
      'xml': 'http://www.w3.org/XML/1998/namespace',
      'tei': 'http://www.tei-c.org/ns/1.0'}

tree = etree.parse('../github/Ibsen-Networks/xml-data/B1844-1871ht.xml')
root = tree.getroot()
letter_short_info = tree.xpath('//HIS:hisMsDesc[@type="letter"]', namespaces=ns)
letter_text = tree.xpath('.//tei:text[@rend="letter"]', namespaces=ns)

tree_info = etree.parse('../github/Ibsen-Networks/xml-data/B1844-1871_info.xml')
letter_head = tree_info.xpath('.//tei:div[@type = "letterHead"]', namespaces=ns)
#   Header = root[0]


def parse_letterinfo(letter_short_info):
    # retrieve all letter ids
    processed_letters = 0
    # info_ids = []  # not used

    letter_short_infos = {}
    for entry in letter_short_info:

        letter_info = entry.xpath('.//HIS:letterinfo[@corresp]', namespaces=ns)
        attributes_corresp = letter_info[0].attrib
        corresp = attributes_corresp['corresp']
        # info_ids.append(corresp)
        letter_short_infos[corresp] = {}

        sender = entry.xpath('.//HIS:letterinfo/tei:name[@role="sender"]/HIS:hisRef', namespaces=ns)
        nsender = len(sender)
        # print(sender)
        # print(nsender)

    # retrieve all senders
        all_senders = []
        all_sender_names = []
        for i in range(0, nsender):
            s = sender[i]
            name_string = re.sub('\n', '', s.text)
            attribites_sender = s.attrib
            sender_id = attribites_sender['target']
            edit_sender_id = re.sub('Navneregister_HISe.xml#', '', sender_id)
            all_senders.append(edit_sender_id)
            all_sender_names.append(name_string)

        if all_senders == 0:
            letter_short_infos[corresp]['sender_ids'] = str('')
            letter_short_infos[corresp]['sender_name'] = str('')
        else:
            letter_short_infos[corresp]['sender_ids'] = all_senders
            letter_short_infos[corresp]['sender_name'] = all_sender_names

    # retrieve letter recipients
        recipient = entry.xpath('.//HIS:letterinfo/tei:name[@role="recipient"]/HIS:hisRef', namespaces=ns)
        nrecioient = len(recipient)
        all_recipients= []
        all_recip_names = []
        for j in range(0, nrecioient):
            r = recipient[j]
            attribites_recipient = r.attrib
            recipient_string = re.sub('\n', '', r.text)
            clean_r_string = ' '.join(recipient_string.split())
            recipient_id = attribites_recipient['target']
            edit_recipient_id = re.sub('Navneregister_HISe.xml#', '', recipient_id)
            all_recipients.append(edit_recipient_id)
            all_recip_names.append(clean_r_string)

        if all_recipients == 0:
            letter_short_infos[corresp]['recipient_ids'] = str('')
            letter_short_infos[corresp]['recipient_name'] = str('')
        else:
            letter_short_infos[corresp]['recipient_ids'] = all_recipients
            letter_short_infos[corresp]['recipient_name'] = all_recip_names

    # retrieve dispatch date
        dispatch_dates = entry.xpath('.//HIS:letterinfo/tei:origDate', namespaces=ns)
        # print(dispatch_dates)
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



        print(corresp + str(' + ') + str(all_senders)+ str(' + ') + str(all_recipients) + str(' + ') + date + str(' + ') + edit_loc_abr + str(' + ') + loc_full)
        processed_letters +=1
    print(str('Number of letters/xmlids: ') + str(processed_letters))


# (parse_letterinfo(letter_short_info))


def parse_letter_text(letter_text):
    letter_texts = {}
    text_number = 0
    for corres in letter_text:

        # retrieve letter id
        id_text = corres.attrib['corresp']
        letter_texts[id_text]={}
        # print(id_text)

        # retrieve sending address
        send_to = corres.xpath('.//HIS:envelope/tei:address/tei:addrLine/text()', namespaces=ns)
        # addr_string = str(etree.tostring(send_to[0]))
        addr_str = []
        for x in send_to:
            addr_str.append(x)
        # print(addr_str)
        if addr_str:
            letter_texts[id_text]['recipient_addr'] = addr_str
        else:
            letter_texts[id_text]['recipient_addr'] = str('')
        # print(send_to)

        # retrieve persons mentioned in letter
        per_mentioned = corres.xpath('.//HIS:hisRef[@type="person"]', namespaces=ns)
        mentioned_per_id = []
        for per in per_mentioned:
            # if len(per)==0:
            #     mentioned_per_id.append(str(''))
            # else:
            m_p_id = per.attrib['target']
            edit_per_id = re.sub('Navneregister_HISe.xml#', '', m_p_id)
            mentioned_per_id.append(edit_per_id)
        # print(mentioned_per_id)

        if len(mentioned_per_id) == 0:
            letter_texts[id_text]['per_m_id'] = str('')
        else:
            letter_texts[id_text]['per_m_id'] = mentioned_per_id

        # retrieve places mentioned in letter
        place_mentioned = corres.xpath('.//HIS:hisRef[@type="place"]', namespaces=ns)
        mentioned_pl_id_abbr = []
        # mentioned_pl_full = []
        for pl in place_mentioned:
            # if len(pl)==0:
            #     mentioned_per_id.append(str(''))
            # else:
            m_pl_id = re.sub('Navneregister_HISe.xml#pl', '', pl.attrib['target'])
            mentioned_pl_id_abbr.append(m_pl_id)
            # use the following to extract full place names from code
            # m_pl_full = pl.text
            # cleaned_pl_full = ' '.join(m_pl_full.split())
        # print(mentioned_pl_id)

        if len(mentioned_pl_id_abbr) == 0:
            letter_texts[id_text]['place_m_id'] = str('')
        else:
            letter_texts[id_text]['place_m_id'] = mentioned_pl_id_abbr

        text_number += 1
    # print(str('Number of letters/xmlids: ') + str(text_number))
    #
    # #print(info_ids)
    pprint.pprint(letter_texts)
    # print(len(letter_texts))


# parse_letter_text(letter_text)


def parse_letter_heads(heads):
    letter_head_info = {}
    text_number = 0
    for head in heads:
        # retrieve letter id
        id_text_head = head.attrib['corresp']
        letter_head_info[id_text_head] = {}

        # add sender id
        letter_head_info[id_text_head]['sender_id'] = str('peHI')

        # retrieve recipient
        recip_head = str(head.xpath('.//tei:name/text()', namespaces=ns))
        recip_name = str(re.sub('Til ', '', re.sub(',', '', recip_head)))
        print(recip_name)
        letter_head_info[id_text_head]['recipient_name'] = recip_name

        # retrieve dispatch location
        dispatch_head = str(head.xpath('.//tei:placeName/text()', namespaces=ns))
        letter_head_info[id_text_head]['dispatch_location_name'] = dispatch_head

        # retrieve date
        date_head = str(head.xpath('.//tei:date/text()', namespaces=ns))
        letter_head_info[id_text_head]['date'] = date_head

    pprint.pprint(letter_head_info)


parse_letter_heads(letter_head)
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
