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

tree = etree.parse('../github/Ibsen-Networks/xml-data/B1890-1905ht.xml')
root = tree.getroot()
letter_short_info = tree.xpath('//HIS:hisMsDesc[@type="letter"]', namespaces=ns)
letter_text = tree.xpath('.//tei:text[@rend="letter"]', namespaces=ns)

tree_info = etree.parse('../github/Ibsen-Networks/xml-data/B1890-1905_info.xml')
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
            # date = str(attributes_dates['when'])
            letter_short_infos[corresp]['send_date'] = str(attributes_dates['when'])

        elif 'notBefore' in attributes_dates and 'notAfter' in attributes_dates:
            # date = str(attributes_dates['notBefore'] + str(' - ') + attributes_dates['notAfter'])
            letter_short_infos[corresp]['send_date'] = str(attributes_dates['notBefore'] + str(' - ') + attributes_dates['notAfter'])
        else:
            date = str('unknown')
            letter_short_infos[corresp]['send_date'] = str('unknown')

    # retrieve dispatch locations
        dispatch_location = entry.xpath('.//HIS:letterinfo/tei:origPlace/HIS:hisRef', namespaces=ns)
        if len(dispatch_location) == 0:
            letter_short_infos[corresp]['dispatch_loc_abbr'] = str('')
            letter_short_infos[corresp]['dispatch_loc_full'] = str('')
        else:
            attributes_loc = dispatch_location[0].attrib
            edit_loc_abr = re.sub('Navneregister_HISe.xml#pl', '', attributes_loc['target'])
            loc_full = dispatch_location[0].text
            letter_short_infos[corresp]['dispatch_loc_abbr'] = edit_loc_abr
            letter_short_infos[corresp]['dispatch_loc_full'] = loc_full

        #print(corresp + str(' + ') + str(all_senders)+ str(' + ') + str(all_recipients) + str(' + ') + date + str(' + ') + edit_loc_abr + str(' + ') + loc_full)
        #processed_letters +=1
        #pprint.pprint(letter_short_infos)
    #return corresp, all_senders
    #print(str('Number of letters/xmlids: ') + str(processed_letters))
    return letter_short_infos

# parse_letterinfo(letter_short_info)

def parse_letter_text(letter_text):
    letter_texts = {}
    text_number = 0

    # create list of places
    # places_list = []
    # point = tree.xpath('.//HIS:hisRef[@type="place"]/text()', namespaces=ns)
    # #places_list.append(point)
    # comp_loc = list(dict.fromkeys(point))
    # pprint.pprint(comp_loc)

    for corres in letter_text:

        # retrieve letter id
        id_text = corres.attrib['corresp']
        letter_texts[id_text] = {}
        # print(id_text)

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
        place_mentioned_text = corres.xpath('.//HIS:hisRef[@type="place"]/text()', namespaces=ns)
        mentioned_pl_id_abbr = []
        mentioned_pl_full = []

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

        for pl_full in place_mentioned_text:
            cleaned_pl_full = ' '.join(pl_full.split())
            mentioned_pl_full.append(cleaned_pl_full)
            # print(cleaned_pl_full)

        if len(mentioned_pl_id_abbr) == 0:
            letter_texts[id_text]['place_m_id'] = str('')
        else:
            letter_texts[id_text]['place_m_id'] = mentioned_pl_id_abbr

        if len(mentioned_pl_full) == 0:
            letter_texts[id_text]['place_m_name'] = str('')
        else:
            letter_texts[id_text]['place_m_name'] = mentioned_pl_full

        # retrieve organisations mentioned in the letter
        org_mentioned = corres.xpath('.//HIS:hisRef[@type="org"]', namespaces=ns)
        mentioned_org_id = []
        for org in org_mentioned:
            m_o_id = org.attrib['target']
            edit_org_id = re.sub('Navneregister_HISe.xml#', '', m_o_id)
            mentioned_org_id.append(edit_org_id)
        # print(mentioned_per_id)

        if len(mentioned_org_id) == 0:
            letter_texts[id_text]['org_m_id'] = str('')
        else:
            letter_texts[id_text]['org_m_id'] = mentioned_org_id

        # retrieve sending address
        send_to = corres.xpath('.//HIS:envelope/tei:address/tei:addrLine/text()', namespaces=ns)
        # addr_string = str(etree.tostring(send_to[0]))
        addr_str = []
        for x in send_to:
            addr_str.append(x)
        # print(addr_str)
        # create list of locations for comparison

        if addr_str:
            letter_texts[id_text]['recipient_addr'] = addr_str
        else:
            letter_texts[id_text]['recipient_addr'] = str('')
        # print(send_to)

        text_number += 1

    # print(str('Number of letters/xmlids: ') + str(text_number))
    #
    # #print(info_ids)
    # pprint.pprint(letter_texts)
    # print(len(letter_texts))
    return letter_texts


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
        #print(recip_name)
        letter_head_info[id_text_head]['recipient_name'] = recip_name

        # retrieve dispatch location
        dispatch_head = str(head.xpath('.//tei:placeName/text()', namespaces=ns))
        letter_head_info[id_text_head]['dispatch_location_name'] = dispatch_head

        # retrieve date
        date_head = str(head.xpath('.//tei:date/text()', namespaces=ns))
        try:
            cleaned_date = dateparser.parse(re.sub('\[', '', re.sub(']', '', re.sub('\'', '', date_head)))).strftime("%Y-%m-%d")
            letter_head_info[id_text_head]['date'] = cleaned_date
        except AttributeError:
            cleaned_date = (re.sub('\[', '', re.sub(']', '', re.sub('\'', '', date_head))))
            letter_head_info[id_text_head]['date'] = cleaned_date

    # pprint.pprint(letter_head_info)
    return letter_head_info


dict_letter_info = (parse_letterinfo(letter_short_info))
dict_letter_text = parse_letter_text(letter_text)
dict_letter_head = parse_letter_heads(letter_head)

def compile_letter_info(dict_info, dict_text, dict_head):
    list_info_per_letter = [['Letter_ID','Sender_ID','Sender_Name','Recipient_ID', 'Recipient_Name', 'Date', 'Dispatch_Location', 'Dispatch_Location_Abbr', 'Mentioned_Person_ID', 'Mentioned_Person', 'Mentioned_Org_ID', 'Mentioned_Org', 'Mentioned_Places_Abbr', 'Mentioned_Places', 'Recipient_Adress']]

    for key in dict_info.keys():
        individual_letter_list =[]
        # append letter id
        individual_letter_list.append(key)
        # get sender id
        sender_string = str(dict_info[key]['sender_ids'])
        individual_letter_list.append(str(re.sub('\[\'', '',(re.sub('\'\]', '', sender_string)))))
        # get sender name
        sender_n_string = re.sub('\[\'', '',(re.sub('\'\]', '', str((dict_info[key]['sender_name'])))))
        individual_letter_list.append(sender_n_string)
        # get recipient id
        recipient_string = str(dict_info[key]['recipient_ids'])
        individual_letter_list.append(str(re.sub('\[\'', '', (re.sub('\'\]', '', recipient_string)))))
        # get recipient name
        recip_n_string = str(dict_info[key]['recipient_name'])
        individual_letter_list.append(re.sub('\[\'', '',(re.sub('\'\]', '', str(recip_n_string)))))
        # get send date
        individual_letter_list.append(str(dict_info[key]['send_date']))
        # get dispatch location name
        individual_letter_list.append(str(dict_info[key]['dispatch_loc_full']))
        # get dispatch location abbreviation
        individual_letter_list.append(str(dict_info[key]['dispatch_loc_abbr']))
        # get ids of persons mentioned
        if len(dict_text[key]['per_m_id'])==0:
            individual_letter_list.append(str(''))
        elif len(dict_text[key]['per_m_id'])==1:
            individual_letter_list.append(str(re.sub('\[', '',re.sub('\]', '', (re.sub('\'', '', str(dict_text[key]['per_m_id'])))))))
        else:
            individual_letter_list.append(str(re.sub('\[', '\'',(re.sub('\]', '\'', (re.sub('\'', '', str(dict_text[key]['per_m_id']))))))))
        # append name of persons mentioned
        individual_letter_list.append(str(''))
        # get ids of organisations mentioned
        if len(dict_text[key]['org_m_id']) == 0:
            individual_letter_list.append(str(''))
        elif len(dict_text[key]['org_m_id']) == 1:
            individual_letter_list.append(
                str(re.sub('\[', '', re.sub('\]', '', (re.sub('\'', '', str(dict_text[key]['org_m_id'])))))))
        else:
            individual_letter_list.append(
                str(re.sub('\[', '\'', (re.sub('\]', '\'', (re.sub('\'', '', str(dict_text[key]['org_m_id']))))))))
        # append name of organisations mentioned
        individual_letter_list.append(str(''))
        # get mentoned places'ids
        if len(dict_text[key]['place_m_id'])==0:
            individual_letter_list.append(str(''))
        elif len(dict_text[key]['place_m_id'])==1:
            individual_letter_list.append(str(re.sub('\[', '',re.sub('\]', '', (re.sub('\'', '', str(dict_text[key]['place_m_id'])))))))
        else:
            individual_letter_list.append(str(re.sub('\[', '\'',(re.sub('\]', '\'', (re.sub('\'', '', str(dict_text[key]['place_m_id']))))))))
        # get mentioned places' names
        if len(dict_text[key]['place_m_name'])==0:
            individual_letter_list.append(str(''))
        elif len(dict_text[key]['place_m_name'])==1:
            individual_letter_list.append(str(re.sub('\[', '',re.sub('\]', '', (re.sub('\'', '', str(dict_text[key]['place_m_name'])))))))
        else:
            individual_letter_list.append(str(re.sub('\[', '\'',(re.sub('\]', '\'', (re.sub('\'', '', str(dict_text[key]['place_m_name']))))))))
        # get address of recipient
        if len(dict_text[key]['recipient_addr'])==0:
            individual_letter_list.append(str(''))
        else:
            #len(dict_text[key]['recipient_addr'])==1:
            individual_letter_list.append(str(re.sub('\[', '\'',re.sub('\]', '\'', (re.sub('\'', '', str(dict_text[key]['recipient_addr'])))))))
        list_info_per_letter.append(individual_letter_list)

    for keys in dict_head.keys():
        if keys in dict_info:
            continue
        else:
            solo_letter_list = []
            # append letter id
            solo_letter_list.append(keys)
            # get sender id
            sender_str = str(dict_head[keys]['sender_id'])
            solo_letter_list.append(str(re.sub('\'', '', (re.sub('\'', '', sender_str)))))
            # append sender name
            solo_letter_list.append('HENRIK IBSEN')
            # get recipient id
            solo_letter_list.append(str(''))
            # get recipient name
            recip_name = str(dict_head[keys]['recipient_name'])
            solo_letter_list.append(re.sub('\[\'', '', (re.sub('\'\]', '', recip_name))))
            # get send date
            solo_letter_list.append(str(dict_head[keys]['date']))
            # get dispatch location name
            solo_letter_list.append(re.sub('\[\'', '', (re.sub('\'\]', '',(str(dict_head[keys]['dispatch_location_name']))))))
            # get dispatch location abbreviation
            solo_letter_list.append(str(''))
            # get ids of persons mentioned
            if len(dict_text[keys]['per_m_id']) == 0:
                solo_letter_list.append(str(''))
            elif len(dict_text[keys]['per_m_id']) == 1:
                solo_letter_list.append(str(re.sub('\[', '', re.sub('\]', '', (re.sub('\'', '', str(dict_text[keys]['per_m_id'])))))))
            else:
                solo_letter_list.append(str(re.sub('\[', '\'', (re.sub('\]', '\'', (re.sub('\'', '', str(dict_text[keys]['per_m_id']))))))))
            # append name of persons mentioned
            solo_letter_list.append(str(''))
            # get ids of organisations mentioned
            if len(dict_text[keys]['org_m_id']) == 0:
                solo_letter_list.append(str(''))
            elif len(dict_text[keys]['org_m_id']) == 1:
                solo_letter_list.append(
                    str(re.sub('\[', '', re.sub('\]', '', (re.sub('\'', '', str(dict_text[key]['org_m_id'])))))))
            else:
                solo_letter_list.append(
                    str(re.sub('\[', '\'', (re.sub('\]', '\'', (re.sub('\'', '', str(dict_text[key]['org_m_id']))))))))
            # append name of organisations mentioned
            solo_letter_list.append(str(''))
            # get mentoned places'ids
            if len(dict_text[keys]['place_m_id']) == 0:
                solo_letter_list.append(str(''))
            elif len(dict_text[keys]['place_m_id']) == 1:
                solo_letter_list.append(str(re.sub('\[', '', re.sub('\]', '', (re.sub('\'', '', str(dict_text[keys]['place_m_id'])))))))
            else:
                solo_letter_list.append(str(re.sub('\[', '\'', (re.sub('\]', '\'', (re.sub('\'', '', str(dict_text[keys]['place_m_id']))))))))
            # get mentioned places' names
            if len(dict_text[keys]['place_m_name']) == 0:
                solo_letter_list.append(str(''))
            elif len(dict_text[keys]['place_m_name']) == 1:
                solo_letter_list.append(str(re.sub('\[', '', re.sub('\]', '', (re.sub('\'', '', str(dict_text[keys]['place_m_name'])))))))
            else:
                solo_letter_list.append(str(re.sub('\[', '\'', (re.sub('\]', '\'', (re.sub('\'', '', str(dict_text[keys]['place_m_name']))))))))
            # get address of recipient
            if len(dict_text[keys]['recipient_addr']) == 0:
                solo_letter_list.append(str(''))
            else:
                # len(dict_text[key]['recipient_addr'])==1:
                solo_letter_list.append(
                    str(re.sub('\[', '\'', re.sub('\]', '\'', (re.sub('\'', '', str(dict_text[keys]['recipient_addr'])))))))
            list_info_per_letter.append(solo_letter_list)

    return list_info_per_letter
    #pprint.pprint(list_info_per_letter)
    #print(len(list_info_per_letter))
    # letter_id_info = dict_info.keys()
    # print(letter_id_info)
    # for entries in dict_info:
    #     letter_id = entries.key
    #     print(letter_id)

def create_csv_letters(info_list):

    with open('letter_information_1890-1905.csv', 'w', ) as work_csv:
        wr = csv.writer(work_csv, delimiter=',')

        for list in info_list:
            #print(list)
            # rows = zip(list)
            #     for element in list:
            wr.writerow(list)


compiled_list = compile_letter_info(dict_letter_info, dict_letter_text, dict_letter_head)
create_csv_letters(compiled_list)
# pprint.pprint(dict_letter_head)
# pprint.pprint(dict_letter_info)
# pprint.pprint(dict_letter_text)
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
