# Ibsen-Networks

**python**

This folder contains all the python files written and used during the project. 

The files stored in this folder are:

	•	PersonIndex.py
	•	edit_person_org_data.py

	•	ExtractLetterData.py
	•	combine-letter-info.py
	•	edit_letter_data.py
	•	Text_search_works.py

	•	Extract_professions_chart.py
	•	Extract_sender_coordinates.py
	•	Extracte_recipient_coordiantes.py


**Implementation**

These scripts were run in an anaconda environment and have to be executed in a specific order.

Extracting information on the senders and recipients:
This done by 

	1.	running first half of PersonIndex.py on the person register xml file to compile a csv with Wikidata ids for each person/organisation (in this case practice_person_info.csv)
	
	2.	manually confirming and/or correcting the collected Wikidata ids and save the changes.
	
	3.	run the rest of the PersonIndex.py script on the edited csv file for the previous step.
	
	4.	run edit_person_org_data.py on the resulting csv file to clean and compile the final data.

Extracting letter data:
This is done by running ExtractLetterData.py, combine-letter-info.py, edit_letter_data.py, Text_search_works.py. Follow these steps

	1.	run ExtractLetterData.py on each xml file grouping containing letter data (all files for years 1844-1871, 1871-1879 etc.). The output is a csv file for each grouping.
	
	2.	run combine-letter-info.py on all four created csv files from the previous step to create one large csv file for all letters.
	
	3.	manually confirm the dates have been extracted correctly and correct if necessary. There are about 30 entries with incomplete dates (only year or year and month) which were incorrectly completed by the script with the date of execution. 
	
	4.	run edit_letter_data.py on the csv from the previous step.
	
	5.	run Text_search_works.py using the previously complied csv file and the excel file Works_ids_and_text_NME.xlsx


**General information**

The project is funded by Teksthub, University of Oslo. 

Project runtime: 2021-beginning of 2022

Participants: Ruth Sander and the Centre for Ibsen Studies, University of Oslo

The dataset consists of Henrik Ibsens’s correspondences, held by the Centre for Ibsen Studies. 
The contents of the letters is written in Norwegian and the files are encoded in TEI. 

**Sharing and access information**

All files, data, and scripts are open access under the CC by NC40 license. 

**Contact**

Inquires about the project and the data can be posted in this repository or by contacting the project Henrik Ibsens Skrifter: https://www.ibsen.uio.no
