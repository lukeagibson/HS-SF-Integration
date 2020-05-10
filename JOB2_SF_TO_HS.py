#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created by: Kuntal 
Date Created: 3/22/2020
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

# --- Fetch Industry Mapping START

industry_df = pd.DataFrame()

mycursor.execute(
    "SELECT detailed_name, detailed_id, consolidated_name, consolidated_id, default_value FROM " + mySchema +
    ".industry_lookup;")

industry_fetch = mycursor.fetchall()

for d in industry_fetch:
    industry_dict = {'detailed_name': d[0], 'detailed_id': str(d[1]), 'consolidated_name': d[2],
                     'consolidated_id': str(d[3]), 'default_value': d[4]}
    industry_df = industry_df.append(industry_dict, ignore_index=True)

# --- Fetch Industry Mapping END

### START OF JOB 3

# STAGE_3


# --- Set Modify Date for Company from last run
mycursor = mydb.cursor()
mycursor.execute(
    "SELECT max(timestamp) FROM " + mySchema + ".job_log WHERE job_name = 'HS_Company_Step_2' and category = 'Start' "
                                               "and source = 'Hiresmith' and status = 'Success';")
modify_date_company = str(mycursor.fetchall()[0][0]).replace(" ", "T")

# Fetch Company Data from Intermediate Database

if (str(modify_date_company) != 'None'):

    script_company_fetch = "SELECT * FROM  " + mySchema + ".salesforce_employer WHERE hiresmith_employer.modify_date >="
    mycursor.execute(script_company_fetch + '\'' + modify_date_company + '\'' + ';')
else:

    script_company_fetch = "SELECT * FROM  " + mySchema + ".salesforce_employer"
    mycursor.execute(script_company_fetch + ';')

company_sql_fetch = mycursor.fetchall()

# --- Set Modify Date for Contacts from last run


mycursor.execute(
    "SELECT max(timestamp) FROM  " + mySchema + ".job_log WHERE job_name = 'HS_Contact_Step_2' and category = 'Start' "
                                                "and source = 'Hiresmith' and status = 'Success';")
modify_date_contact = str(mycursor.fetchall()[0][0]).replace(" ", "T")

# Fetch Contacts Data from Intermediate Database

if (str(modify_date_contact) != 'None'):

    script_contact_fetch = "SELECT * FROM  " + mySchema + ".salesforce_contact WHERE  hiresmith_contact.modify_date >="
    mycursor.execute(script_contact_fetch + '\'' + modify_date_contact + '\'' + ';')
else:

    script_contact_fetch = "SELECT * FROM  " + mySchema + ".salesforce_contact"
    mycursor.execute(script_contact_fetch + ';')

contacts_sql_fetch = mycursor.fetchall()




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

all_company_data = custfunc.getAllCompanies(url, authHeader)  # all employer data records in dictionary
all_contact_data = custfunc.getAllContacts(url, authHeader)  # all contacts data records in dictionary
all_company_notes_data = custfunc.getAllCompanyNotes(url, authHeader)  # all employer notes data records in dictionary

# NULL RECORD CREATION BEGINS ----

# Company default_df
default_df_company = all_company_data[
    list(all_company_data.keys())[1]].copy()  # Fetching one record(dict) from all_company_data_by_date

# creating company record(format: dictionary) as defualt_df with NULL values
for i in default_df_company:
    if type(default_df_company[i]) != dict:
        default_df_company[i] = None
    else:
        for key in default_df_company[i].keys():
            if key != 'AttributeId':
                default_df_company[i][key] = None

# Contacts default_df
default_df_contact = all_contact_data[
    list(all_contact_data.keys())[1]].copy()  # Fetching one record(dict) from all_contact_data_by_date

# creating contact record(format: dictionary) as defualt_df with NULL values
for i in default_df_contact:
    if type(default_df_contact[i]) != dict:
        default_df_contact[i] = None
    else:
        for key in default_df_contact[i].keys():
            if key != 'AttributeId':
                default_df_contact[i][key] = None

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

# ADD Values for Company fetched from Intermediate Database to Data Dictionary Format
final_company_put = {}
final_company_post = {}
for x in company_sql_fetch:

    if (x[0]) in all_company_data:
        final_company_put[x[0]] = all_company_data[x[0]]
        final_company_put[x[0]]['Id'] = x[0]
        final_company_put[x[0]]['Name'] = x[1]
        final_company_put[x[0]]['CustomAttributeValues']['custom_attribute_10888805112355'] = x[2]
        final_company_put[x[0]]['CustomAttributeValues']['custom_attribute_10888805112902'] = x[3]
        final_company_put[x[0]]['CustomAttributeValues']['custom_attribute_10888805112498'] = x[4]
        final_company_put[x[0]]['CustomAttributeValues']['custom_attribute_10888805112499'] = x[5]
        final_company_put[x[0]]['NumberOfEmployeesName'] = x[6]
        final_company_put[x[0]]['Website'] = x[7]
        final_company_put[x[0]]['AccountManagerName'] = x[8]
        final_company_put[x[0]]['OutreachLeadName'] = x[9]
        final_company_put[x[0]]['OutreachPriorityName'] = x[10]
        final_company_put[x[0]]['CustomAttributeValues']['custom_attribute_10888805112926'] = x[11]
        final_company_put[x[0]]['CustomAttributeValues']['custom_attribute_10888805112908'] = x[12]
        final_company_put[x[0]]['CustomAttributeValues']['custom_attribute_10888805112925'] = x[13]
        final_company_put[x[0]]['CustomAttributeValues']['custom_attribute_10888805112927'] = x[14]
        final_company_put[x[0]]['CustomAttributeValues']['custom_attribute_10888805112928'] = x[15]

        if (x[16] != None):
            detailed_industry_value = industry_df.loc[(industry_df['consolidated_name'] == x[16]) & (
                        industry_df['default_value'] == 'Yes'), 'detailed_name'].iloc[0]
            detailed_industry_id = industry_df.loc[(industry_df['consolidated_name'] == x[16]) & (
                        industry_df['default_value'] == 'Yes'), 'detailed_id'].iloc[0]
            if final_company_put[x[0]]['Industries'] == []:  # no existing industry, we use default industry
                final_company_put[x[0]]['Industries'][0]['Name'] = detailed_industry_value
                final_company_put[x[0]]['Industries'][0]['Id'] = detailed_industry_id
            elif (x[16] != industry_df.loc[industry_df['detailed_name'] == final_company_put[x[0]]['Industries'][0][
                'Name'], 'consolidated_name'].iloc[
                0]):  # existing industry but first value is not the default industry, we prepend the default industry
                final_company_put[x[0]]['Industries'].insert(0, {'Name': detailed_industry_value,
                                                                 'Id': detailed_industry_id})

        final_company_put[x[0]]['CreateDate'] = x[17]
        final_company_put[x[0]]['ModifyDate'] = x[18]
        final_company_put[x[0]]['ParentId'] = x[19]
        final_company_put[x[0]]['ParentCompanyName'] = x[20]

        # format datetime values to json format
        if x[17] != None: final_company_put[x[0]]['CreateDate'] = final_company_put[x[0]]['CreateDate'].strftime(
            '%Y-%m-%dT%H:%M:%S.%f%z')
        if x[18] != None: final_company_put[x[0]]['ModifyDate'] = final_company_put[x[0]]['ModifyDate'].strftime(
            '%Y-%m-%dT%H:%M:%S.%f%z')

    else:
        final_company_post[x[0]] = default_df_company
        final_company_post[x[0]]['Id'] = x[0]
        final_company_post[x[0]]['Name'] = x[1]
        final_company_post[x[0]]['CustomAttributeValues']['custom_attribute_10888805112355'] = x[2]
        final_company_post[x[0]]['CustomAttributeValues']['custom_attribute_10888805112902'] = x[3]
        final_company_post[x[0]]['CustomAttributeValues']['custom_attribute_10888805112498'] = x[4]
        final_company_post[x[0]]['CustomAttributeValues']['custom_attribute_10888805112499'] = x[5]
        final_company_post[x[0]]['NumberOfEmployeesName'] = x[6]
        final_company_post[x[0]]['Website'] = x[7]
        final_company_post[x[0]]['AccountManagerName'] = x[8]
        final_company_post[x[0]]['OutreachLeadName'] = x[9]
        final_company_post[x[0]]['OutreachPriorityName'] = x[10]
        final_company_post[x[0]]['CustomAttributeValues']['custom_attribute_10888805112926'] = x[11]
        final_company_post[x[0]]['CustomAttributeValues']['custom_attribute_10888805112908'] = x[12]
        final_company_post[x[0]]['CustomAttributeValues']['custom_attribute_10888805112925'] = x[13]
        final_company_post[x[0]]['CustomAttributeValues']['custom_attribute_10888805112927'] = x[14]
        final_company_post[x[0]]['CustomAttributeValues']['custom_attribute_10888805112928'] = x[15]

        if x[16] != None:
            detailed_industry_value = industry_df.loc[(industry_df['consolidated_name'] == x[16]) & (
                    industry_df['default_value'] == 'Yes'), 'detailed_name'].iloc[0]
            detailed_industry_id = industry_df.loc[(industry_df['consolidated_name'] == x[16]) & (
                    industry_df['default_value'] == 'Yes'), 'detailed_id'].iloc[0]
            if final_company_post[x[0]]['Industries'] == []:  # no existing industry, we use default industry
                final_company_post[x[0]]['Industries'][0]['Name'] = detailed_industry_value
                final_company_post[x[0]]['Industries'][0]['Id'] = detailed_industry_id
            elif (x[16] != industry_df.loc[industry_df['detailed_name'] == final_company_post[x[0]]['Industries'][0][
                'Name'], 'consolidated_name'].iloc[
                0]):  # existing industry but first value is not the default industry, we prepend the default industry
                final_company_post[x[0]]['Industries'].insert(0, {'Name': detailed_industry_value,
                                                                  'Id': detailed_industry_id})

        final_company_post[x[0]]['CreateDate'] = x[17]
        final_company_post[x[0]]['ModifyDate'] = x[18]
        final_company_post[x[0]]['ParentId'] = x[19]
        final_company_post[x[0]]['ParentCompanyName'] = x[20]

        # format datetime values to json format
        if x[17] != None: final_company_post[x[0]]['CreateDate'] = final_company_post[x[0]]['CreateDate'].strftime(
            '%Y-%m-%dT%H:%M:%S.%f%z')
        if x[18] != None: final_company_post[x[0]]['ModifyDate'] = final_company_post[x[0]]['ModifyDate'].strftime(
            '%Y-%m-%dT%H:%M:%S.%f%z')

# ADD Values for Contacts fetched from Intermediate Database to Data Dictionary Format

final_contacts_put = {}
final_contacts_post = {}
for y in contacts_sql_fetch:


    mycursor.execute(
        "SELECT * FROM  " + mySchema + ".hiresmith_contact WHERE  hiresmith_contact.modify_date >= '2019-10-01';")

    if (y[0]) in all_contact_data[0]:
        final_contacts_put[y[0]] = all_contact_data[y[0]]
        final_contacts_put[y[0]]['Id'] = y[0]
        final_contacts_put[y[0]]['FirstName'] = y[1]
        final_contacts_put[y[0]]['LastName'] = y[2]
        final_contacts_put[y[0]]['CustomAttributeValues']['custom_attribute_10888805112356'] = y[3]
        final_contacts_put[y[0]]['CustomAttributeValues']['custom_attribute_10888805112357'] = y[4]
        final_contacts_put[y[0]]['CompanyName'] = y[6]
        final_contacts_put[y[0]]['CompanyId'] = y[7]
        final_contacts_put[y[0]]['CreateDate'] = y[8]
        final_contacts_put[y[0]]['ModifyDate'] = y[9]
        final_contacts_put[y[0]]['OfficePhone'] = y[10]
        final_contacts_put[y[0]]['CellPhone'] = y[11]
        final_contacts_put[y[0]]['EmailAddress'] = y[12]
        final_contacts_put[y[0]]['AlternateEmailAddress'] = y[13]
        final_contacts_put[y[0]]['Fax'] = y[14]
        final_contacts_put[y[0]]['IsAlumni'] = y[15]
        final_contacts_put[y[0]]['JobTitle'] = y[16]
        final_contacts_put[y[0]]['IsPrimary'] = y[17]
        final_contacts_put[y[0]]['LinkedInProfileUrl'] = y[18]
        final_contacts_put[y[0]]['PrefixName'] = y[19]
        final_contacts_put[y[0]]['PreferredName'] = y[20]
        final_contacts_put[y[0]]['OutreachLead'] = y[21]
        if y[22] != None:
            final_contacts_put[y[0]]['Location']['AddressLine1'] = y[22]
            final_contacts_put[y[0]]['Location']['AddressLine2'] = y[23]
            final_contacts_put[y[0]]['Location']['ZipCode'] = y[24]
            final_contacts_put[y[0]]['Location']['CountryName'] = y[25]
            final_contacts_put[y[0]]['Location']['CityName'] = y[26]

        final_contacts_put[y[0]]['AdditionalInformation'] = y[27]
        final_contacts_put[y[0]]['AlternateEmailAddress'] = y[28]
        final_contacts_put[y[0]]['AlumniGraduationYear'] = y[29]
        final_contacts_put[y[0]]['AlumniGraduationProgramName'] = y[30]
        final_contacts_put[y[0]]['AssignedAdvisorName'] = y[31]
        final_contacts_put[y[0]]['CompanyHistory'] = y[32]
        final_contacts_put[y[0]]['HasPhoto'] = y[33]

        # format datetime values to json format
        if y[8] != None: final_contacts_put[y[0]]['CreateDate'] = final_contacts_put[y[0]]['CreateDate'].strftime(
            '%Y-%m-%dT%H:%M:%S.%f%z')
        if y[9] != None: final_contacts_put[y[0]]['ModifyDate'] = final_contacts_put[y[0]]['ModifyDate'].strftime(
            '%Y-%m-%dT%H:%M:%S.%f%z')

    else:
        final_contacts_post[y[0]] = default_df_contact
        final_contacts_post[y[0]]['Id'] = y[0]
        final_contacts_post[y[0]]['FirstName'] = y[1]
        final_contacts_post[y[0]]['LastName'] = y[2]
        final_contacts_post[y[0]]['CustomAttributeValues']['custom_attribute_10888805112356'] = y[3]
        final_contacts_post[y[0]]['CustomAttributeValues']['custom_attribute_10888805112357'] = y[4]
        final_contacts_post[y[0]]['CompanyName'] = y[6]
        final_contacts_post[y[0]]['CompanyId'] = y[7]
        final_contacts_post[y[0]]['CreateDate'] = y[8]
        final_contacts_post[y[0]]['ModifyDate'] = y[9]
        final_contacts_post[y[0]]['OfficePhone'] = y[10]
        final_contacts_post[y[0]]['CellPhone'] = y[11]
        final_contacts_post[y[0]]['EmailAddress'] = y[12]
        final_contacts_post[y[0]]['AlternateEmailAddress'] = y[13]
        final_contacts_post[y[0]]['Fax'] = y[14]
        final_contacts_post[y[0]]['IsAlumni'] = y[15]
        final_contacts_post[y[0]]['JobTitle'] = y[16]
        final_contacts_post[y[0]]['IsPrimary'] = y[17]
        final_contacts_post[y[0]]['LinkedInProfileUrl'] = y[18]
        final_contacts_post[y[0]]['PrefixName'] = y[19]
        final_contacts_post[y[0]]['PreferredName'] = y[20]
        final_contacts_post[y[0]]['OutreachLead'] = y[21]
        if y[22] != None:
            final_contacts_post[y[0]]['Location']['AddressLine1'] = y[22]
            final_contacts_post[y[0]]['Location']['AddressLine2'] = y[23]
            final_contacts_post[y[0]]['Location']['ZipCode'] = y[24]
            final_contacts_post[y[0]]['Location']['CountryName'] = y[25]
            final_contacts_post[y[0]]['Location']['CityName'] = y[26]

        final_contacts_post[y[0]]['AdditionalInformation'] = y[27]
        final_contacts_post[y[0]]['AlternateEmailAddress'] = y[28]
        final_contacts_post[y[0]]['AlumniGraduationYear'] = y[29]
        final_contacts_post[y[0]]['AlumniGraduationProgramName'] = y[30]
        final_contacts_post[y[0]]['AssignedAdvisorName'] = y[31]
        final_contacts_post[y[0]]['CompanyHistory'] = y[32]
        final_contacts_post[y[0]]['HasPhoto'] = y[33]

        # format datetime values to json format
        if y[8] != None: final_contacts_post[y[0]]['CreateDate'] = final_contacts_post[y[0]]['CreateDate'].strftime(
            '%Y-%m-%dT%H:%M:%S.%f%z')
        if y[9] != None: final_contacts_post[y[0]]['ModifyDate'] = final_contacts_post[y[0]]['ModifyDate'].strftime(
            '%Y-%m-%dT%H:%M:%S.%f%z')

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

script_company_log_1 = "INSERT INTO  " + mySchema + ".log_employer (hs_employer_id, employer_name, alternate_names," \
                                                    " do_not_merge, sf_account_id, link_url, number_employees_name, " \
                                                    "website, account_manager_name, outreach_lead_name, " \
                                                    "outreach_priority_name, outreach_status, er_team_lead," \
                                                    " ed_team_lead, employer_classification, " \
                                                    "outreach_settings_current_as_of, industries_name, create_date," \
                                                    " modify_date, parent_id, parent_company_name, employer_city," \
                                                    " employer_metro_area, employer_state, hash, status," \
                                                    " system_updated)"
script_company_log_2 = "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                       "%s, %s, %s, %s, %s, %s, %s)"


script_contact_log_1 = "INSERT INTO  " + mySchema + ".log_contact (hs_contact_id, first_name, last_name, link_url, " \
                                                    "sf_contact_id, sf_account_id, employer_name, hs_employer_id," \
                                                    " create_date, modify_date, office_phone, cell_phone, email," \
                                                    " alternate_email, fax, is_alumni, job_title, is_primary," \
                                                    " linkedin_profile_url, prefix_name, preferred_name, " \
                                                    "outreach_lead, location_address_1, location_address_2," \
                                                    " location_zip_code, location_country_name, location_city_name," \
                                                    " contact_additional_information, contact_alt_email," \
                                                    " contact_alumni_grad, contact_alumni_grad_prog_name, " \
                                                    "contact_assigned_advisor_name, contact_company_history," \
                                                    " contact_has_photo, hash, status, system_updated)"
script_contact_log_2 = "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                       "%s,%s,%s,%s,%s,%s,%s,%s,%s)"

script_company_notes_log_1 = "INSERT INTO " + mySchema + ".log_employer_note (employer_note_Id, PrimaryEntityTypeId, PrimaryEntityId, " \
                                               "AssociatedEntityType1Id, AssociatedEntity1Id, AssociatedEntityType2Id, AssociatedEntity2Id, " \
                                               "Text, Date, StudentNoteTypeId, " \
                                               "StudentNoteTypeName, CompanyNoteTypeId, CompanyNoteTypeName, OwnerId, " \
                                               "OwnerName, CreatorName, " \
                                               "FileId, FileName, VisibilityId, CampaignIds, " \
                                               "ModifyDate, hash, status, system_update) "

script_company_notes_log_2 = "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"


mycursor.execute(
    "INSERT INTO  " + mySchema + ".job_log (job_name, source, category, status) VALUES ('HS_Company_Step_2',"
    " 'Hiresmith', 'Start', 'Success');")
mydb.commit()

# Update existing record
for key1_put in sorted(final_company_put):
    PutDataUrl = 'https://' + url + '12twenty.com/api/v2/companies/' + str(key1_put)
    custfunc.putRequest(PutDataUrl, final_company_put[key1_put], authHeader)

    # UPDATE LOG
    key1_put = int(key1_put)
    if final_company_put[key1_put]['Industries'] == []:
        industry_value = None
    else:
        industry_value = industry_df.loc[industry_df['detailed_name'] == final_company_put[key1_put]['Industries'][0][
            'Name'], 'consolidated_name'].iloc[0]

    company_dict_values = [key1_put, final_company_put[key1_put]['Name'],
                           final_company_put[key1_put]['CustomAttributeValues']['custom_attribute_10888805112355'],
                           final_company_put[key1_put]['CustomAttributeValues']['custom_attribute_10888805112902'],
                           final_company_put[key1_put]['CustomAttributeValues']['custom_attribute_10888805112498'],
                           final_company_put[key1_put]['CustomAttributeValues']['custom_attribute_10888805112499'],
                           final_company_put[key1_put]['NumberOfEmployeesName'], final_company_put[key1_put]['Website'],
                           final_company_put[key1_put]['AccountManagerName'],
                           final_company_put[key1_put]['OutreachLeadName'],
                           final_company_put[key1_put]['OutreachPriorityName'],
                           final_company_put[key1_put]['CustomAttributeValues']['custom_attribute_10888805112926'],
                           final_company_put[key1_put]['CustomAttributeValues']['custom_attribute_10888805112908'],
                           final_company_put[key1_put]['CustomAttributeValues']['custom_attribute_10888805112925'],
                           final_company_put[key1_put]['CustomAttributeValues']['custom_attribute_10888805112927'],
                           final_company_put[key1_put]['CustomAttributeValues']['custom_attribute_10888805112928'],
                           industry_value, final_company_put[key1_put]['CreateDate'],
                           final_company_put[key1_put]['ModifyDate'], final_company_put[key1_put]['ParentId'],
                           final_company_put[key1_put]['ParentCompanyName'], "", "", "", ""]

    # SQL query to update records from HireSmith to Intermediate Database
    vals_company = None
    vals_company = company_dict_values + ['Insert'] + ['Hiresmith']  # company_values to be updated
    mycursor.execute(script_company_log_1 + script_company_log_2, vals_company)
    mydb.commit()

# Upload new record
for key1_post in sorted(final_company_post):
    PostDataUrl = 'https://' + url + '12twenty.com/api/v2/companies'
    r = requests.post(PostDataUrl, json=final_company_post[key1_post], headers=authHeader)
    pastebin_url = r.text
    print("The pastebin URL is:%s" % pastebin_url)

    # UPDATE LOG
    key1_post = int(key1_post)
    if (final_company_post[key1_post]['Industries'] == []):
        industry_value = None
    else:
        industry_value = industry_df.loc[industry_df['detailed_name'] == final_company_post[key1_post]['Industries'][0][
            'Name'], 'consolidated_name'].iloc[0]

    company_dict_values = [key1_post, final_company_post[key1_post]['Name'],
                           final_company_post[key1_post]['CustomAttributeValues']['custom_attribute_10888805112355'],
                           final_company_post[key1_post]['CustomAttributeValues']['custom_attribute_10888805112902'],
                           final_company_post[key1_post]['CustomAttributeValues']['custom_attribute_10888805112498'],
                           final_company_post[key1_post]['CustomAttributeValues']['custom_attribute_10888805112499'],
                           final_company_post[key1_post]['NumberOfEmployeesName'],
                           final_company_post[key1_post]['Website'],
                           final_company_post[key1_post]['AccountManagerName'],
                           final_company_post[key1_post]['OutreachLeadName'],
                           final_company_post[key1_post]['OutreachPriorityName'],
                           final_company_post[key1_post]['CustomAttributeValues']['custom_attribute_10888805112926'],
                           final_company_post[key1_post]['CustomAttributeValues']['custom_attribute_10888805112908'],
                           final_company_post[key1_post]['CustomAttributeValues']['custom_attribute_10888805112925'],
                           final_company_post[key1_post]['CustomAttributeValues']['custom_attribute_10888805112927'],
                           final_company_post[key1_post]['CustomAttributeValues']['custom_attribute_10888805112928'],
                           industry_value, final_company_post[key1_post]['CreateDate'],
                           final_company_post[key1_post]['ModifyDate'], final_company_post[key1_post]['ParentId'],
                           final_company_post[key1_post]['ParentCompanyName'], "", "", "", ""]

    # SQL query to insert records from HireSmith to Intermediate Database
    vals_company = None
    vals_company = company_dict_values + ['Upload'] + ['Hiresmith']  # company_values to be uploaded
    mycursor.execute(script_company_log_1 + script_company_log_2, vals_company)
    mydb.commit()

mycursor.execute(
    "INSERT INTO  " + mySchema + ".job_log (job_name, source, category, status) VALUES ('HS_Company_Step_2',"
    " 'Hiresmith', 'End', 'Success');")
mycursor.execute(
    "INSERT INTO  " + mySchema + ".job_log (job_name, source, category, status) VALUES ('HS_Contact_Step_2',"
    " 'Hiresmith', 'Start', 'Success');")
mydb.commit()

# Update existing record
for key2_put in sorted(final_contacts_put):
    PutDataUrl = 'https://' + url + '12twenty.com/api/v2/contacts/' + str(key2_put)
    custfunc.putRequest(PutDataUrl, final_contacts_put[key2_put], authHeader)

    # UPDATE LOG
    key2_put = int(key2_put)

    contact_dict_values = [key2_put, final_contacts_put[key2_put]['FirstName'],
                           final_contacts_put[key2_put]['LastName'],
                           final_contacts_put[key2_put]['CustomAttributeValues']['custom_attribute_10888805112356'],
                           final_contacts_put[key2_put]['CustomAttributeValues']['custom_attribute_10888805112357'],
                           final_contacts_put[key2_put]['CustomAttributeValues']['custom_attribute_10888805112357'],
                           final_contacts_put[key2_put]['CompanyName'], final_contacts_put[key2_put]['CompanyId'],
                           final_contacts_put[key2_put]['CreateDate'], final_contacts_put[key2_put]['ModifyDate'],
                           final_contacts_put[key2_put]['OfficePhone'], final_contacts_put[key2_put]['CellPhone'],
                           final_contacts_put[key2_put]['EmailAddress'],
                           final_contacts_put[key2_put]['AlternateEmailAddress'], final_contacts_put[key2_put]['Fax'],
                           final_contacts_put[key2_put]['IsAlumni'], final_contacts_put[key2_put]['JobTitle'],
                           final_contacts_put[key2_put]['IsPrimary'],
                           final_contacts_put[key2_put]['LinkedInProfileUrl'],
                           final_contacts_put[key2_put]['PrefixName'], final_contacts_put[key2_put]['PreferredName'],
                           "",
                           final_contacts_put[key2_put]['Location']['AddressLine1'],
                           final_contacts_put[key2_put]['Location']['AddressLine2'],
                           final_contacts_put[key2_put]['Location']['ZipCode'],
                           final_contacts_put[key2_put]['Location']['CountryName'],
                           final_contacts_put[key2_put]['Location']['CityName'],
                           final_contacts_put[key2_put]['AdditionalInformation'],
                           final_contacts_put[key2_put]['AlternateEmailAddress'],
                           final_contacts_put[key2_put]['AlumniGraduationYear'],
                           final_contacts_put[key2_put]['AlumniGraduationProgramName'],
                           final_contacts_put[key2_put]['AssignedAdvisorName'],
                           ''.join(final_contacts_put[key2_put]['CompanyHistory']),
                           final_contacts_put[key2_put]['HasPhoto'], ""]

    vals_contact = None
    vals_contact = contact_dict_values + ['Insert'] + ['Hiresmith']  # contact_values to be updated
    mycursor.execute(script_contact_log_1 + script_contact_log_2, vals_contact)
    mydb.commit()

# Upload new record
for key2_post in sorted(final_contacts_post):
    PostDataUrl = 'https://' + url + '12twenty.com/api/v2/contacts'
    r = requests.post(PostDataUrl, json=final_contacts_post[key2_post], headers=authHeader)
    pastebin_url = r.text
    print("The pastebin URL is:%s" % pastebin_url)

    # UPDATE LOG
    key2_post = int(key2_post)

    contact_dict_values = [key2_post, final_contacts_post[key2_post]['FirstName'],
                           final_contacts_post[key2_post]['LastName'],
                           final_contacts_post[key2_post]['CustomAttributeValues']['custom_attribute_10888805112356'],
                           final_contacts_post[key2_post]['CustomAttributeValues']['custom_attribute_10888805112357'],
                           final_contacts_post[key2_post]['CustomAttributeValues']['custom_attribute_10888805112357'],
                           final_contacts_post[key2_post]['CompanyName'], final_contacts_post[key2_post]['CompanyId'],
                           final_contacts_post[key2_post]['CreateDate'], final_contacts_post[key2_post]['ModifyDate'],
                           final_contacts_post[key2_post]['OfficePhone'], final_contacts_post[key2_post]['CellPhone'],
                           final_contacts_post[key2_post]['EmailAddress'],
                           final_contacts_post[key2_post]['AlternateEmailAddress'],
                           final_contacts_post[key2_post]['Fax'],
                           final_contacts_post[key2_post]['IsAlumni'], final_contacts_post[key2_post]['JobTitle'],
                           final_contacts_post[key2_post]['IsPrimary'],
                           final_contacts_post[key2_post]['LinkedInProfileUrl'],
                           final_contacts_post[key2_post]['PrefixName'],
                           final_contacts_post[key2_post]['PreferredName'], "",
                           final_contacts_post[key2_post]['Location']['AddressLine1'],
                           final_contacts_post[key2_post]['Location']['AddressLine2'],
                           final_contacts_post[key2_post]['Location']['ZipCode'],
                           final_contacts_post[key2_post]['Location']['CountryName'],
                           final_contacts_post[key2_post]['Location']['CityName'],
                           final_contacts_post[key2_post]['AdditionalInformation'],
                           final_contacts_post[key2_post]['AlternateEmailAddress'],
                           final_contacts_post[key2_post]['AlumniGraduationYear'],
                           final_contacts_post[key2_post]['AlumniGraduationProgramName'],
                           final_contacts_post[key2_post]['AssignedAdvisorName'],
                           ''.join(final_contacts_post[key2_post]['CompanyHistory']),
                           final_contacts_post[key2_post]['HasPhoto'], ""]
    vals_contact = None
    vals_contact = contact_dict_values + ['Upload'] + ['Hiresmith']  # contact_values to be updated
    mycursor.execute(script_contact_log_1 + script_contact_log_2, vals_contact)
    mydb.commit()

mycursor.execute(
    "INSERT INTO  " + mySchema + ".job_log (job_name, source, category, status) VALUES ('HS_Contact_Step_2', "
                                 "'Hiresmith', 'End', 'Success');")
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