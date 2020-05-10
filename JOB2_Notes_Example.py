#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created by: Luke 
Date Created: 5/9/2020
'''

import PrivateKeys as fetchkeys
import pandas as pd
import Functions as custfunc
import requests
import DBconnection as connection

url, authHeader = fetchkeys.access_variables()  # function call to fetch the url, authHeader, api key and auth token
env_type = fetchkeys.env_select()  # function call to fetch the environment of run.

# CONNECT TO DATABASE SERVER
# DB Connection Setup
mydb, mySchema = connection.getDatabaseConnectionSandbox()
mycursor = mydb.cursor()

### START OF JOB 3

# STAGE_3

# --- Set Modify Date for Company Notes from last run
mycursor = mydb.cursor()
mycursor.execute(
    "SELECT max(timestamp) FROM " + mySchema + ".job_log WHERE job_name = 'HS_Company_Notes_Step_2' and category = 'Start' "
                                               "and source = 'Hiresmith' and status = 'Success';")
modify_date_company_notes = str(mycursor.fetchall()[0][0]).replace(" ", "T")

# Fetch Company Notes Data from Intermediate Database

if (str(modify_date_company_notes) != 'None'):

    script_company_notes_fetch = "SELECT * FROM  " + mySchema + ".salesforce_employer_notes WHERE hiresmith_employer_notes.ModifyDate >="
    mycursor.execute(script_company_notes_fetch + '\'' + modify_date_company_notes + '\'' + ';')
else:

    script_company_notes_fetch = "SELECT * FROM  " + mySchema + ".salesforce_employer_notes"
    mycursor.execute(script_company_notes_fetch + ';')

company_notes_sql_fetch = mycursor.fetchall()


# Get all records from HireSmith to check if exists

all_company_notes_data = custfunc.getAllCompanyNotes(url, authHeader)  # all employer notes data records in dictionary


# NULL RECORD CREATION BEGINS ----
# Company Notes default_df
default_df_company_notes = all_company_notes_data[
    list(all_company_notes_data.keys())[1]].copy()  # Fetching one record(dict) from all_company_notes_data_by_date

# creating company notes record(format: dictionary) as defualt_df with NULL values
for i in default_df_company_notes:
    if type(default_df_company_notes[i]) != dict:
        default_df_company_notes[i] = None
    else:
        for key in default_df_company_notes[i].keys():
            if key != 'AttributeId':
                default_df_company_notes[i][key] = None

# NULL RECORD CREATION ENDS ----


# ADD Values for Company Notes fetched from Intermediate Database to Data Dictionary Format
final_company_notes_put = {}
final_company_notes_post = {}
for x in company_notes_sql_fetch:

    if (x[0]) in all_company_notes_data:
        final_company_notes_put[x[0]] = all_company_notes_data[x[0]]
        final_company_notes_put[x[0]]['Id'] = x[0]
        final_company_notes_put[x[0]]['PrimaryEntityTypeId'] = x[1]
        final_company_notes_put[x[0]]['PrimaryEntityId'] = x[2]
        final_company_notes_put[x[0]]['AssociatedEntityType1Id'] = x[3]
        final_company_notes_put[x[0]]['AssociatedEntity1Id'] = x[4]
        final_company_notes_put[x[0]]['AssociatedEntityType2Id'] = x[5]
        final_company_notes_put[x[0]]['AssociatedEntity2Id'] = x[6]
        final_company_notes_put[x[0]]['Text'] = x[7]
        final_company_notes_put[x[0]]['Date'] = x[8]
        final_company_notes_put[x[0]]['StudentNoteTypeId'] = x[9]
        final_company_notes_put[x[0]]['StudentNoteTypeName'] = x[10]
        final_company_notes_put[x[0]]['CompanyNoteTypeId'] = x[11]
        final_company_notes_put[x[0]]['CompanyNoteTypeName'] = x[12]
        final_company_notes_put[x[0]]['OwnerId'] = x[13]
        final_company_notes_put[x[0]]['OwnerName'] = x[14]
        final_company_notes_put[x[0]]['FileId'] = x[15]
        final_company_notes_put[x[0]]['FileName'] = x[16]
        final_company_notes_put[x[0]]['VisibilityId'] = x[17]
        final_company_notes_put[x[0]]['CampaignIds'] = x[18]
        final_company_notes_put[x[0]]['ModifyDate'] = x[19]

        # format datetime values to json format
        if x[8] != None: final_company_notes_put[x[0]]['CreateDate'] = final_company_notes_put[x[0]]['CreateDate'].strftime(
            '%Y-%m-%dT%H:%M:%S.%f%z')
        if x[19] != None: final_company_notes_put[x[0]]['ModifyDate'] = final_company_notes_put[x[0]]['ModifyDate'].strftime(
            '%Y-%m-%dT%H:%M:%S.%f%z')

    else:
        final_company_notes_post[x[0]] = default_df_company_notes
        final_company_notes_post[x[0]]['Id'] = x[0]
        final_company_notes_post[x[0]]['PrimaryEntityTypeId'] = x[1]
        final_company_notes_post[x[0]]['PrimaryEntityId'] = x[2]
        final_company_notes_post[x[0]]['AssociatedEntityType1Id'] = x[3]
        final_company_notes_post[x[0]]['AssociatedEntity1Id'] = x[4]
        final_company_notes_post[x[0]]['AssociatedEntityType2Id'] = x[5]
        final_company_notes_post[x[0]]['AssociatedEntity2Id'] = x[6]
        final_company_notes_post[x[0]]['Text'] = x[7]
        final_company_notes_post[x[0]]['Date'] = x[8]
        final_company_notes_post[x[0]]['StudentNoteTypeId'] = x[9]
        final_company_notes_post[x[0]]['StudentNoteTypeName'] = x[10]
        final_company_notes_post[x[0]]['CompanyNoteTypeId'] = x[11]
        final_company_notes_post[x[0]]['CompanyNoteTypeName'] = x[12]
        final_company_notes_post[x[0]]['OwnerId'] = x[13]
        final_company_notes_post[x[0]]['OwnerName'] = x[14]
        final_company_notes_post[x[0]]['FileId'] = x[15]
        final_company_notes_post[x[0]]['FileName'] = x[16]
        final_company_notes_post[x[0]]['VisibilityId'] = x[17]
        final_company_notes_post[x[0]]['CampaignIds'] = x[18]
        final_company_notes_post[x[0]]['ModifyDate'] = x[19]

        # format datetime values to json format
        if x[8] != None: final_company_notes_post[x[0]]['CreateDate'] = final_company_notes_post[x[0]]['CreateDate'].strftime(
            '%Y-%m-%dT%H:%M:%S.%f%z')
        if x[19] != None: final_company_notes_post[x[0]]['ModifyDate'] = final_company_notes_post[x[0]]['ModifyDate'].strftime(
            '%Y-%m-%dT%H:%M:%S.%f%z')


# STAGE_4

# UPLOAD / UPDATE NEW DATA TO HIRESMITH BEGINS -------

script_company_notes_log_1 = "INSERT INTO " + mySchema + ".log_employer_note (employer_note_Id, PrimaryEntityTypeId, PrimaryEntityId, " \
                                               "AssociatedEntityType1Id, AssociatedEntity1Id, AssociatedEntityType2Id, AssociatedEntity2Id, " \
                                               "Text, Date, StudentNoteTypeId, " \
                                               "StudentNoteTypeName, CompanyNoteTypeId, CompanyNoteTypeName, OwnerId, " \
                                               "OwnerName, CreatorName, " \
                                               "FileId, FileName, VisibilityId, CampaignIds, " \
                                               "ModifyDate, hash, status, system_update) "

script_company_notes_log_2 = "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


mycursor.execute(
    "INSERT INTO  " + mySchema + ".job_log (job_name, source, category, status) VALUES ('HS_Company_Notes_Step_2',"
    " 'Hiresmith', 'Start', 'Success');")
mydb.commit()

# Update existing record
for key1_put in sorted(final_company_notes_put):
    PutDataUrl = 'https://' + url + '12twenty.com/api/v2/notes/' + str(key1_put)
    custfunc.putRequest(PutDataUrl, final_company_notes_put[key1_put], authHeader)

    # UPDATE LOG
    key1_put = int(key1_put)
    company_notes_dict_values = [key1_put, final_company_notes_put[key1_put]['PrimaryEntityTypeID'],
                        final_company_notes_put[key1_put]['PrimaryEntityID'],
                        final_company_notes_put[key1_put]['AssociatedEntityType1Id'],
                        final_company_notes_put[key1_put]['AssociatedEntity1Id'],
                        final_company_notes_put[key1_put]['AssociatedEntityType2Id'],
                        final_company_notes_put[key1_put]['AssociatedEntity2Id'],
                        final_company_notes_put[key1_put]['Text'],
                        final_company_notes_put[key1_put]['Date'],
                        final_company_notes_put[key1_put]['StudentNoteTypeId'],
                        final_company_notes_put[key1_put]['StudentNoteTypeName'],
                        final_company_notes_put[key1_put]['CompanyNoteTypeId'],
                        final_company_notes_put[key1_put]['CompanyNoteTypeName'],
                        final_company_notes_put[key1_put]['OwnerId'],
                        final_company_notes_put[key1_put]['OwnerName'],
                        final_company_notes_put[key1_put]['CreatorName'],
                        final_company_notes_put[key1_put]['FileId'],
                        final_company_notes_put[key1_put]['FileName'],
                        final_company_notes_put[key1_put]['VisibilityId'],
                        final_company_notes_put[key1_put]['CampaignIds'],
                        final_company_notes_put[key1_put]['ModifyDate'], ""]

    # SQL query to update records from HireSmith to Intermediate Database
    vals_company_notes = None
    vals_company_notes = company_notes_dict_values + ['Insert'] + ['Hiresmith']  # company_values to be updated
    mycursor.execute(script_company_notes_log_1 + script_company_notes_log_2, vals_company)
    mydb.commit()

# Upload new record
for key1_post in sorted(final_company_notes_post):
    PostDataUrl = 'https://' + url + '12twenty.com/api/v2/notes'
    r = requests.post(PostDataUrl, json=final_company_notes_post[key1_post], headers=authHeader)
    pastebin_url = r.text
    print("The pastebin URL is:%s" % pastebin_url)

    # UPDATE LOG
    key1_post = int(key1_post)

    company_notes_dict_values = [key1_post, final_company_notes_put[key1_post]['PrimaryEntityTypeID'],
                        final_company_notes_put[key1_post]['PrimaryEntityID'],
                        final_company_notes_put[key1_post]['AssociatedEntityType1Id'],
                        final_company_notes_put[key1_post]['AssociatedEntity1Id'],
                        final_company_notes_put[key1_post]['AssociatedEntityType2Id'],
                        final_company_notes_put[key1_post]['AssociatedEntity2Id'],
                        final_company_notes_put[key1_post]['Text'],
                        final_company_notes_put[key1_post]['Date'],
                        final_company_notes_put[key1_post]['StudentNoteTypeId'],
                        final_company_notes_put[key1_post]['StudentNoteTypeName'],
                        final_company_notes_put[key1_post]['CompanyNoteTypeId'],
                        final_company_notes_put[key1_post]['CompanyNoteTypeName'],
                        final_company_notes_put[key1_post]['OwnerId'],
                        final_company_notes_put[key1_post]['OwnerName'],
                        final_company_notes_put[key1_post]['CreatorName'],
                        final_company_notes_put[key1_post]['FileId'],
                        final_company_notes_put[key1_post]['FileName'],
                        final_company_notes_put[key1_post]['VisibilityId'],
                        final_company_notes_put[key1_post]['CampaignIds'],
                        final_company_notes_put[key1_post]['ModifyDate'], ""]

    # SQL query to insert records from HireSmith to Intermediate Database
    vals_company_notes = None
    vals_company_notes = company_notes_dict_values + ['Upload'] + ['Hiresmith']  # company_values to be uploaded
    mycursor.execute(script_company_notes_log_1 + script_company_notes_log_2, vals_company)
    mydb.commit()
# UPLOAD / UPDATE NEW DATA TO HIRESMITH ENDS -------

mycursor.execute(
    "INSERT INTO  " + mySchema + ".job_log (job_name, source, category, status) VALUES ('HS_Company_Step_2',"
    " 'Hiresmith', 'End', 'Success');")
mydb.commit()

### END OF JOB 2

