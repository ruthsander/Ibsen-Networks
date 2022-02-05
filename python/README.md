{\rtf1\ansi\ansicpg1252\cocoartf2636
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\fswiss\fcharset0 Helvetica-Bold;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
{\*\listtable{\list\listtemplateid1\listhybrid{\listlevel\levelnfc0\levelnfcn0\leveljc0\leveljcn0\levelfollow0\levelstartat1\levelspace360\levelindent0{\*\levelmarker \{decimal\}.}{\leveltext\leveltemplateid1\'02\'00.;}{\levelnumbers\'01;}\fi-360\li720\lin720 }{\listname ;}\listid1}
{\list\listtemplateid2\listhybrid{\listlevel\levelnfc0\levelnfcn0\leveljc0\leveljcn0\levelfollow0\levelstartat1\levelspace360\levelindent0{\*\levelmarker \{decimal\}.}{\leveltext\leveltemplateid101\'02\'00.;}{\levelnumbers\'01;}\fi-360\li720\lin720 }{\listname ;}\listid2}}
{\*\listoverridetable{\listoverride\listid1\listoverridecount0\ls1}{\listoverride\listid2\listoverridecount0\ls2}}
\paperw11900\paperh16840\margl1440\margr1440\vieww14700\viewh10840\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # Ibsen-Networks\
\
**python**\
\
This folder contains all the python files written and used during the project. \
\
The files stored in this folder are:\
\
	\'95	PersonIndex.py\
	\'95	edit_person_org_data.py\
\
	\'95	ExtractLetterData.py\
	\'95	combine-letter-info.py\
	\'95	edit_letter_data.py\
	\'95	Text_search_works.py\
\
	\'95	Extract_professions_chart.py\
	\'95	Extract_sender_coordinates.py\
	\'95	Extracte_recipient_coordiantes.py\
\
\
**Implementation**
\f1\b \

\f0\b0 \
These scripts were run in an anaconda environment and have to be executed in a specific order.\
\
Extracting information on the senders and recipients:\
This done by \
\pard\tx220\tx720\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\li720\fi-720\pardirnatural\partightenfactor0
\ls1\ilvl0\cf0 {\listtext	1.	}running first half of PersonIndex.py on the person register xml file to compile a csv with Wikidata ids for each person/organisation (in this case practice_person_info.csv)\
{\listtext	2.	}manually confirming and/or correcting the collected Wikidata ids and save the changes.\
{\listtext	3.	}run the rest of the PersonIndex.py script on the edited csv file for the previous step.\
{\listtext	4.	}run edit_person_org_data.py on the resulting csv file to clean and compile the final data.\
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0
\cf0 \
Extracting letter data:\
This is done by running ExtractLetterData.py, combine-letter-info.py, edit_letter_data.py, Text_search_works.py. Follow these steps\
\pard\tx220\tx720\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\li720\fi-720\pardirnatural\partightenfactor0
\ls2\ilvl0\cf0 {\listtext	1.	}run ExtractLetterData.py on each xml file grouping containing letter data (all files for years 1844-1871, 1871-1879 etc.). The output is a csv file for each grouping.\
{\listtext	2.	}run combine-letter-info.py on all four created csv files from the previous step to create one large csv file for all letters.\
{\listtext	3.	}manually confirm the dates have been extracted correctly and correct if necessary. There are about 30 entries with incomplete dates (only year or year and month) which were incorrectly completed by the script with the date of execution. \
{\listtext	4.	}run edit_letter_data.py on the csv from the previous step.\
{\listtext	5.	}run Text_search_works.py using the previously complied csv file and the excel file Works_ids_and_text_NME.xlsx\
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0
\cf0 \
\
**General information**\
\
The project is funded by Teksthub, University of Oslo. \
\
Project runtime: 2021-beginning of 2022\
\
Participants: Ruth Sander and the Centre for Ibsen Studies, University of Oslo\
\
The dataset consists of Henrik Ibsens\'92s correspondences, held by the Centre for Ibsen Studies. \
The contents of the letters is written in Norwegian and the files are encoded in TEI. \
\
**Sharing and access information**\
\
All files, data, and scripts are open access under the CC by NC40 license. \
\
**Contact**\
\
Inquires about the project and the data can be posted in this repository or by contacting the project Henrik Ibsens Skrifter: https://www.ibsen.uio.no}