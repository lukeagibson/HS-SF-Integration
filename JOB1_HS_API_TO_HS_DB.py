#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created by: Kuntal
Date Created: 3/16/2020
#Function for SF-HS Intgegration Phase-1 - Job1
#Function to Pull recent changes and new records from HS, save to DB.
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

# --- Fetch Industry Mapping START

industry_df = pd.DataFrame()

mycursor = mydb.cursor()
mycursor.execute(
    "SELECT detailed_name, detailed_id, consolidated_name, consolidated_id, default_value FROM " + mySchema + ".industry_lookup;")
industry_fetch = mycursor.fetchall()

for d in industry_fetch:
    industry_dict = {'detailed_name': d[0], 'detailed_id': str(d[1]), 'consolidated_name': d[2],
                     'consolidated_id': str(d[3]), 'default_value': d[4]}
    industry_df = industry_df.append(industry_dict, ignore_index=True)

# --- Fetch Industry Mapping END

# --- Set Modify Date for Company from last run
mycursor = mydb.cursor()
mycursor.execute("SELECT max(timestamp) FROM " + mySchema + ".job_log WHERE job_name = 'HS_Company_Step_1' and "
                                                            "category = 'Start' and source = 'Hiresmith' and status ="
                                                            " 'Success';")

modify_date_company = str(mycursor.fetchall()[0][0]).replace(" ", "T")

# --- Insert/Update New Company Records from HireSmith to Intermediate Database ---
# all employer data records in dictionary form modified after last batch run
all_company_data_by_date = custfunc.getAllCompaniesByDate(url, authHeader,
                                                          modify_date_company)

script_company_1 = "INSERT INTO " + mySchema + ".hiresmith_employer (hs_employer_id, employer_name, alternate_names, " \
                                               "do_not_merge, sf_account_id, link_url, number_employees_name, " \
                                               "website, account_manager_name, outreach_lead_name, " \
                                               "outreach_priority_name, outreach_status, er_team_lead, ed_team_lead, " \
                                               "employer_classification, outreach_settings_current_as_of, " \
                                               "industries_name, create_date, modify_date, parent_id, " \
                                               "parent_company_name, employer_city, employer_metro_area, " \
                                               "employer_state, hash, status) "
script_company_2 = "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                   "%s, %s, %s, %s) "
script_company_3 = "ON DUPLICATE KEY UPDATE hs_employer_id = %s, employer_name = %s, alternate_names = %s, " \
                   "do_not_merge = %s, sf_account_id = %s, link_url = %s, number_employees_name = %s, website = %s, " \
                   "account_manager_name = %s, outreach_lead_name = %s, outreach_priority_name = %s, outreach_status " \
                   "= %s, er_team_lead = %s, ed_team_lead = %s, employer_classification = %s, " \
                   "outreach_settings_current_as_of = %s, industries_name = %s, create_date = %s, modify_date = %s, " \
                   "parent_id = %s, parent_company_name = %s, employer_city = %s, employer_metro_area = %s, " \
                   "employer_state = %s, hash = %s, status = %s "

hiresmith_company_url_start = "https://" + url + "12twenty.com/Companies#/Companies/"

final_dict_company = {}

mycursor.execute(
    "INSERT INTO " + mySchema + ".job_log (job_name, source, category, status) VALUES ('HS_Company_Step_1', "
                                "'Hiresmith', 'Start', 'Success');")
exclusion_dict = []

for key in sorted(all_company_data_by_date):
    print(str(key) + " : " + str(all_company_data_by_date[key]['IsAdminApproved']))
    if (all_company_data_by_date[key]['IsAdminApproved']):

        print('Iteration started for key: ' + str(key))
        # Python Rest API to fetch detailed company details
        # ApprovedList.append(key)
        key = str(key)
        start = '12twenty.com/Api/V2/companies/'
        getDataUrl = 'https://' + url + start + key
        data = custfunc.ExceptionGet(getDataUrl, authHeader)  # REST call with Authentication header
        data = data.json()
        final_dict_company[data['Id']] = data

        industry_value = None
        key = int(key)
        if (final_dict_company[key]['Industries'] == []):
            industry_value = None
        else:
            industry_value = industry_df.loc[industry_df['detailed_name'] == final_dict_company[key]['Industries'][0][
                'Name'], 'consolidated_name'].iloc[0]

        # Converting datetime object to string
        dateTimeObj = datetime.now()
        company_dict_values = [key, final_dict_company[key]['Name'],
                               final_dict_company[key]['CustomAttributeValues']['custom_attribute_10888805112355'],
                               final_dict_company[key]['CustomAttributeValues']['custom_attribute_10888805112902'],
                               final_dict_company[key]['CustomAttributeValues']['custom_attribute_10888805112498'],
                               final_dict_company[key]['CustomAttributeValues']['custom_attribute_10888805112499'],
                               final_dict_company[key]['NumberOfEmployeesName'], final_dict_company[key]['Website'],
                               final_dict_company[key]['AccountManagerName'],
                               final_dict_company[key]['OutreachLeadName'],
                               final_dict_company[key]['OutreachPriorityName'],
                               final_dict_company[key]['CustomAttributeValues']['custom_attribute_10888805112926'],
                               final_dict_company[key]['CustomAttributeValues']['custom_attribute_10888805112908'],
                               final_dict_company[key]['CustomAttributeValues']['custom_attribute_10888805112925'],
                               final_dict_company[key]['CustomAttributeValues']['custom_attribute_10888805112927'],
                               final_dict_company[key]['CustomAttributeValues']['custom_attribute_10888805112928'],
                               industry_value, final_dict_company[key]['CreateDate'],
                               final_dict_company[key]['ModifyDate'], final_dict_company[key]['ParentId'],
                               final_dict_company[key]['ParentCompanyName'], "", "", "", ""]

        # SQL query to insert/update records from HireSmith to Intermediate Database
        vals_company = None
        vals_company = company_dict_values + ['Insert'] + company_dict_values + ['Update']
        mycursor.execute(script_company_1 + script_company_2 + script_company_3, vals_company)
        mydb.commit()
        print('Iteration ended for key: ' + str(key))

    else:
        print('Exception iteration for key: ' + str(key))
        exclusion_dict.append(key)

mycursor.execute("INSERT INTO " + mySchema + ".job_log (job_name, source, category, status) VALUES ("
                                             "'HS_Company_Step_1', 'Hiresmith', 'End', 'Success');")
mydb.commit()
print("exclusion_dict: " + ''.join(exclusion_dict))
# --- Set Modify Date for Contacts from last run
mycursor = mydb.cursor()

mycursor.execute("SELECT max(timestamp) FROM " + mySchema + ".job_log WHERE job_name = 'HS_Contact_Step_1' and "
                                                            "category = 'Start' and source = 'Hiresmith' and status ="
                                                            " 'Success';")
modify_date_contact = str(mycursor.fetchall()[0][0]).replace(" ", "T")

# --- Insert/Update New Contact Records from HireSmith to Intermediate Database ---
# all contacts data records in dictionary form modified after last batch run
all_contact_data_by_date = custfunc.getAllContactsByDate(url, authHeader,
                                                         modify_date_contact)

script_contact_1 = "INSERT INTO " + mySchema + ".hiresmith_contact (hs_contact_id, first_name, last_name, link_url, " \
                                               "sf_contact_id, sf_account_id, employer_name, hs_employer_id, " \
                                               "create_date, modify_date, office_phone, cell_phone, email, " \
                                               "alternate_email, fax, is_alumni, job_title, is_primary, " \
                                               "linkedin_profile_url, prefix_name, preferred_name, outreach_lead, " \
                                               "location_address_1, location_address_2, location_zip_code, " \
                                               "location_country_name, location_city_name, " \
                                               "contact_additional_information, contact_alt_email, " \
                                               "contact_alumni_grad, contact_alumni_grad_prog_name, " \
                                               "contact_assigned_advisor_name, contact_company_history, " \
                                               "contact_has_photo, hash, status) "
script_contact_2 = "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" \
                   ",%s,%s,%s,%s,%s,%s,%s)"
script_contact_3 = "ON DUPLICATE KEY UPDATE hs_contact_id = %s, first_name = %s, last_name = %s, link_url = %s, " \
                   "sf_contact_id = %s, sf_account_id = %s, employer_name = %s, hs_employer_id = %s, create_date = " \
                   "%s, modify_date = %s, office_phone = %s, cell_phone = %s, email = %s, alternate_email = %s, " \
                   "fax = %s, is_alumni = %s, job_title = %s, is_primary = %s, linkedin_profile_url = %s, prefix_name " \
                   "= %s, preferred_name = %s, outreach_lead = %s, location_address_1 = %s, location_address_2 = %s, " \
                   "location_zip_code = %s, location_country_name = %s, location_city_name = %s, " \
                   "contact_additional_information = %s, contact_alt_email = %s, contact_alumni_grad = %s, " \
                   "contact_alumni_grad_prog_name = %s, contact_assigned_advisor_name = %s, contact_company_history = " \
                   "%s, contact_has_photo = %s, hash = %s, status = %s; "

mycursor.execute(
    "INSERT INTO " + mySchema + ".job_log (job_name, source, category, status) VALUES ('HS_Contact_Step_1', "
                                "'Hiresmith', 'Start', 'Success');")

hiresmith_contact_url_start = "https://" + url + "12twenty.com/Companies#/Contacts/"
final_dict_contacts = {}
ApprovedContacts = []
ApprovedList = []
all_company_data_by_date = custfunc.getAllCompaniesByDate(url, authHeader,
                                                          '')

for key in all_company_data_by_date:
    if all_company_data_by_date[key]['IsAdminApproved']:
        ApprovedList.append(key)

for key in sorted(all_contact_data_by_date):
    if all_contact_data_by_date[key]['IsAdminApproved']:
        if all_contact_data_by_date[key]['CompanyId'] in ApprovedList:
            ApprovedContacts.append(key)


for key in ApprovedContacts:
    # Python Rest API to fetch detailed contact details
    key = str(key)
    start = '12twenty.com/Api/V2/contacts/'
    getDataUrl = 'https://' + url + start + key
    data = custfunc.ExceptionGet(getDataUrl, authHeader)  # REST call with Authentication header
    data = data.json()
    final_dict_contacts[data['Id']] = data
    # SQL query to insert/update records from HireSmith to Intermediate Database
    key = int(key)
    contact_dict_values = [key, final_dict_contacts[key]['FirstName'], final_dict_contacts[key]['LastName'],
                           final_dict_contacts[key]['CustomAttributeValues']['custom_attribute_10888805112356'],
                           final_dict_contacts[key]['CustomAttributeValues']['custom_attribute_10888805112357'],
                           final_dict_contacts[key]['CustomAttributeValues']['custom_attribute_10888805112357'],
                           final_dict_contacts[key]['CompanyName'], final_dict_contacts[key]['CompanyId'],
                           final_dict_contacts[key]['CreateDate'], final_dict_contacts[key]['ModifyDate'],
                           final_dict_contacts[key]['OfficePhone'], final_dict_contacts[key]['CellPhone'],
                           final_dict_contacts[key]['EmailAddress'],
                           final_dict_contacts[key]['AlternateEmailAddress'], final_dict_contacts[key]['Fax'],
                           final_dict_contacts[key]['IsAlumni'], final_dict_contacts[key]['JobTitle'],
                           final_dict_contacts[key]['IsPrimary'], final_dict_contacts[key]['LinkedInProfileUrl'],
                           final_dict_contacts[key]['PrefixName'], final_dict_contacts[key]['PreferredName'], "",
                           final_dict_contacts[key]['Location']['AddressLine1'],
                           final_dict_contacts[key]['Location']['AddressLine2'],
                           final_dict_contacts[key]['Location']['ZipCode'],
                           final_dict_contacts[key]['Location']['CountryName'],
                           final_dict_contacts[key]['Location']['CityName'],
                           final_dict_contacts[key]['AdditionalInformation'],
                           final_dict_contacts[key]['AlternateEmailAddress'],
                           final_dict_contacts[key]['AlumniGraduationYear'],
                           final_dict_contacts[key]['AlumniGraduationProgramName'],
                           final_dict_contacts[key]['AssignedAdvisorName'],
                           # ''.join(final_dict_contacts[key]['CompanyHistory']),
                           str(final_dict_contacts[key]['CompanyHistory']),
                           final_dict_contacts[key]['HasPhoto'], ""]
    vals_contact = None
    vals_contact = contact_dict_values + ['Insert'] + contact_dict_values + ['Update']
    mycursor.execute(script_contact_1 + script_contact_2 + script_contact_3, vals_contact)
    mydb.commit()

mycursor.execute("INSERT INTO " + mySchema + ".job_log (job_name, source, category, status) VALUES ("
                                             "'HS_Contact_Step_1', 'Hiresmith', 'End', 'Success');")
mydb.commit()







# --- Set Modify Date for Company Notes from last run
mycursor = mydb.cursor()
mycursor.execute("SELECT max(timestamp) FROM " + mySchema + ".job_log WHERE job_name = 'HS_Company_Step_1' and "
                                                            "category = 'Start' and source = 'Hiresmith' and status ="
                                                            " 'Success';")

modify_date_notes = str(mycursor.fetchall()[0][0]).replace(" ", "T")

# --- Insert/Update New Notes Records from HireSmith to Intermediate Database ---
# all notes data records in dictionary form modified after last batch run
all_company_notes_data_by_date = custfunc.getAllCompanyNotesByDate(url, authHeader,
                                                          modify_date_company)

# Need to change Scripts
script_company_notes_1 = "INSERT INTO " + mySchema + ".hiresmith_employer_note (employer_note_Id, PrimaryEntityTypeId, PrimaryEntityId, " \
                                               "AssociatedEntityType1Id, AssociatedEntity1Id, AssociatedEntityType2Id, AssociatedEntity2Id, " \
                                               "Text, Date, StudentNoteTypeId, " \
                                               "StudentNoteTypeName, CompanyNoteTypeId, CompanyNoteTypeName, OwnerId, " \
                                               "OwnerName, CreatorName, " \
                                               "FileId, FileName, VisibilityId, CampaignIds, " \
                                               "ModifyDate) "
script_company_notes_2 = "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
script_company_notes_3 = "ON DUPLICATE KEY UPDATE employer_note_Id = %s, PrimaryEntityTypeId = %s, PrimaryEntityId = %s, " \
                   "AssociatedEntityType1Id = %s, AssociatedEntity1Id = %s, AssociatedEntityType2Id = %s, AssociatedEntity2Id = %s, Text = %s, " \
                   "Date = %s, StudentNoteTypeId = %s, StudentNoteTypeName = %s, CompanyNoteTypeId " \
                   "= %s, CompanyNoteTypeName = %s, OwnerId = %s, OwnerName = %s, " \
                   "CreatorName = %s, FileId = %s, FileName = %s, VisibilityId = %s, " \
                   "CampaignIds = %s, ModifyDate = %s"


final_dict_company_notes = {}

mycursor.execute(
    "INSERT INTO " + mySchema + ".job_log (job_name, source, category, status) VALUES ('HS_Company_Notes_Step_1', "
                                "'Hiresmith', 'Start', 'Success');")
# exclusion_dict = []

for key in sorted(all_company_notes_data_by_date):
#    print(str(key) + " : " + str(all_company_notes_data_by_date[key]['IsAdminApproved']))
#    if (all_company_data_by_date[key]['IsAdminApproved']):

    print('Iteration started for key: ' + str(key))
    # Python Rest API to fetch detailed company details
    # ApprovedList.append(key)
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
                        final_dict_company_notes[key]['AssociatedEntityType1Id'],
                        final_dict_company_notes[key]['AssociatedEntity1Id'],
                        final_dict_company_notes[key]['AssociatedEntityType2Id'],
                        final_dict_company_notes[key]['AssociatedEntity2Id'],
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
                        final_dict_company_notes[key]['ModifyDate']]

    # SQL query to insert/update records from HireSmith to Intermediate Database
    vals_company_notes = None
    vals_company_notes = company_notes_dict_values + ['Insert'] + company_notes_dict_values + ['Update']
    mycursor.execute(script_company_notes_1 + script_company_notes_2 + script_company_notes_3, vals_company)
    mydb.commit()
    print('Iteration ended for key: ' + str(key))

#    else:
#        print('Exception iteration for key: ' + str(key))
#        exclusion_dict.append(key)

mycursor.execute("INSERT INTO " + mySchema + ".job_log (job_name, source, category, status) VALUES ("
                                             "'HS_Company_Notes_Step_1', 'Hiresmith', 'End', 'Success');")
mydb.commit()


### END OF JOB 1
