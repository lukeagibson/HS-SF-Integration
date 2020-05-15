#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created by: Luke
Date Created: 5/12/2020
#Function for SF-HS Intgegration Phase-1 - Job1 - Notes
#Function to Pull recent changes and new records from HS for Notes, save to DB.
'''

import PrivateKeys as fetchkeys
import pandas as pd
import Functions as custfunc
from datetime import datetime
import DBconnection as connection

# --- JOB 1 --> Updating Employer and Contact tables

# Environment setup

# Base URL and Auth Header
url, authHeader = fetchkeys.access_variables()

# DB Connection Setup
mydb, mySchema = connection.getDatabaseConnectionSandbox()
mycursor = mydb.cursor()


# --- Start Notes Synchronization --- 


# --- Set Modify Date for Company Notes from last run
mycursor = mydb.cursor()
mycursor.execute("SELECT max(timestamp) FROM " + mySchema + ".job_log WHERE job_name = 'HS_Company_Notes_Step_1' and "
                                                            "category = 'Start' and source = 'Hiresmith' and status ="
                                                            " 'Success';")

modify_date_notes = str(mycursor.fetchall()[0][0]).replace(" ", "T")

# --- Insert/Update New Notes Records from HireSmith to Intermediate Database ---
# all notes data records in dictionary form modified after last batch run
all_company_notes_data_by_date = custfunc.getAllCompanyNotesByDate(url, authHeader,
                                                          modify_date_company)

# Need to change Scripts
script_company_notes_1 = "INSERT INTO " + mySchema + ".hiresmith_employer_notes (employer_note_Id, PrimaryEntityTypeId, PrimaryEntityId, " \
                                               "Text, Date, StudentNoteTypeId, " \
                                               "StudentNoteTypeName, CompanyNoteTypeId, CompanyNoteTypeName, OwnerId, " \
                                               "OwnerName, CreatorName, " \
                                               "FileId, FileName, VisibilityId, CampaignIds, " \
                                               "ModifyDate, status) "
script_company_notes_2 = "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
script_company_notes_3 = "ON DUPLICATE KEY UPDATE employer_note_Id = %s, PrimaryEntityTypeId = %s, PrimaryEntityId = %s, " \
                   "Text = %s, " \
                   "Date = %s, StudentNoteTypeId = %s, StudentNoteTypeName = %s, CompanyNoteTypeId " \
                   "= %s, CompanyNoteTypeName = %s, OwnerId = %s, OwnerName = %s, " \
                   "CreatorName = %s, FileId = %s, FileName = %s, VisibilityId = %s, " \
                   "CampaignIds = %s, ModifyDate = %s, status = %s"


final_dict_company_notes = {}

mycursor.execute(
    "INSERT INTO " + mySchema + ".job_log (job_name, source, category, status) VALUES ('HS_Company_Notes_Step_1', "
                                "'Hiresmith', 'Start', 'Success');")

for key in sorted(all_company_notes_data_by_date):

    print('Iteration started for key: ' + str(key))
    # Python Rest API to fetch detailed company details
    key = str(key)
    start = '12twenty.com/Api/V2/notes/'
    getDataUrl = 'https://' + url + start + key
    data = custfunc.ExceptionGet(getDataUrl, authHeader)  # REST call with Authentication header
    data = data.json()
    final_dict_company_notes[data['Id']] = data

    key = int(key)

    # Converting datetime object to string
    dateTimeObj = datetime.now()
    company_notes_dict_values = [key, final_dict_company_notes[key]['PrimaryEntityTypeID'],
                        final_dict_company_notes[key]['PrimaryEntityID'],
                        final_dict_company_notes[key]['Text'],
                        final_dict_company_notes[key]['Date'],
                        final_dict_company_notes[key]['StudentNoteTypeId'],
                        final_dict_company_notes[key]['StudentNoteTypeName'],
                        final_dict_company_notes[key]['CompanyNoteTypeId'],
                        final_dict_company_notes[key]['CompanyNoteTypeName'],
                        final_dict_company_notes[key]['OwnerId'],
                        final_dict_company_notes[key]['OwnerName'],
                        final_dict_company_notes[key]['CreatorName'],
                        final_dict_company_notes[key]['FileId'],
                        final_dict_company_notes[key]['FileName'],
                        final_dict_company_notes[key]['VisibilityId'],
                        final_dict_company_notes[key]['CampaignIds'],
                        final_dict_company_notes[key]['ModifyDate'], ""]

    # SQL query to insert/update records from HireSmith to Intermediate Database
    vals_company_notes = None
    vals_company_notes = company_notes_dict_values + ['Insert'] + company_notes_dict_values + ['Update']
    mycursor.execute(script_company_notes_1 + script_company_notes_2 + script_company_notes_3, vals_company)
    mydb.commit()
    print('Iteration ended for key: ' + str(key))



mycursor.execute("INSERT INTO " + mySchema + ".job_log (job_name, source, category, status) VALUES ("
                                             "'HS_Company_Notes_Step_1', 'Hiresmith', 'End', 'Success');")
mydb.commit()


# --- Set Modify Date for Contact Notes from last run
mycursor = mydb.cursor()
mycursor.execute("SELECT max(timestamp) FROM " + mySchema + ".job_log WHERE job_name = 'HS_Contact_Notes_Step_1' and "
                                                            "category = 'Start' and source = 'Hiresmith' and status ="
                                                            " 'Success';")

modify_date_notes = str(mycursor.fetchall()[0][0]).replace(" ", "T")

# --- Insert/Update New Notes Records from HireSmith to Intermediate Database ---
# all notes data records in dictionary form modified after last batch run
all_contact_notes_data_by_date = custfunc.getAllContactNotesByDate(url, authHeader,
                                                          modify_date_contact)


script_contact_notes_1 = "INSERT INTO " + mySchema + ".hiresmith_contact_notes (employer_note_Id, PrimaryEntityTypeId, PrimaryEntityId, " \
                                               "AssociatedEntityType1Id, AssociatedEntity1Id, " \
                                               "Text, Date, StudentNoteTypeId, " \
                                               "StudentNoteTypeName, CompanyNoteTypeId, CompanyNoteTypeName, OwnerId, " \
                                               "OwnerName, CreatorName, " \
                                               "FileId, FileName, VisibilityId, CampaignIds, " \
                                               "ModifyDate, status) "
script_contact_notes_2 = "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
script_contact_notes_3 = "ON DUPLICATE KEY UPDATE employer_note_Id = %s, PrimaryEntityTypeId = %s, PrimaryEntityId = %s, " \
                   "AssociatedEntityType1Id = %s, AssociatedEntity1Id = %s, Text = %s, " \
                   "Date = %s, StudentNoteTypeId = %s, StudentNoteTypeName = %s, CompanyNoteTypeId " \
                   "= %s, CompanyNoteTypeName = %s, OwnerId = %s, OwnerName = %s, " \
                   "CreatorName = %s, FileId = %s, FileName = %s, VisibilityId = %s, " \
                   "CampaignIds = %s, ModifyDate = %s, status = %s"


final_dict_contact_notes = {}

mycursor.execute(
    "INSERT INTO " + mySchema + ".job_log (job_name, source, category, status) VALUES ('HS_Contact_Notes_Step_1', "
                                "'Hiresmith', 'Start', 'Success');")


for key in sorted(all_contact_notes_data_by_date):

    print('Iteration started for key: ' + str(key))
    # Python Rest API to fetch detailed contact details
    key = str(key)
    start = '12twenty.com/Api/V2/notes/'
    getDataUrl = 'https://' + url + start + key
    data = custfunc.ExceptionGet(getDataUrl, authHeader)  # REST call with Authentication header
    data = data.json()
    final_dict_contact_notes[data['Id']] = data

    key = int(key)

    # Converting datetime object to string
    dateTimeObj = datetime.now()
    contact_notes_dict_values = [key, final_dict_contact_notes[key]['PrimaryEntityTypeID'],
                        final_dict_contact_notes[key]['PrimaryEntityID'],
                        final_dict_contact_notes[key]['AssociatedEntityType1Id'],
                        final_dict_contact_notes[key]['AssociatedEntity1Id'],
                        final_dict_contact_notes[key]['Text'],
                        final_dict_contact_notes[key]['Date'],
                        final_dict_contact_notes[key]['StudentNoteTypeId'],
                        final_dict_contact_notes[key]['StudentNoteTypeName'],
                        final_dict_contact_notes[key]['CompanyNoteTypeId'],
                        final_dict_contact_notes[key]['CompanyNoteTypeName'],
                        final_dict_contact_notes[key]['OwnerId'],
                        final_dict_contact_notes[key]['OwnerName'],
                        final_dict_contact_notes[key]['CreatorName'],
                        final_dict_contact_notes[key]['FileId'],
                        final_dict_contact_notes[key]['FileName'],
                        final_dict_contact_notes[key]['VisibilityId'],
                        final_dict_contact_notes[key]['CampaignIds'],
                        final_dict_contact_notes[key]['ModifyDate'], ""]

    # SQL query to insert/update records from HireSmith to Intermediate Database
    vals_contact_notes = None
    vals_contact_notes = contact_notes_dict_values + ['Insert'] + contact_notes_dict_values + ['Update']
    mycursor.execute(script_contact_notes_1 + script_contact_notes_2 + script_contact_notes_3, vals_contact)
    mydb.commit()
    print('Iteration ended for key: ' + str(key))


mycursor.execute("INSERT INTO " + mySchema + ".job_log (job_name, source, category, status) VALUES ("
                                             "'HS_Contact_Notes_Step_1', 'Hiresmith', 'End', 'Success');")
mydb.commit()



### END OF JOB 1
