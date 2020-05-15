#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created by: Luke
Date Created: 5/12/2020
#Function for SF-HS Intgegration Phase-2 - Job-N
#Function to Pull Specific Fields from HS, save to DB.
'''

import PrivateKeys as fetchkeys
import pandas as pd
import Functions as custfunc
from datetime import datetime
import DBconnection as connection
import time


# Environment setup

# Base URL and Auth Header
url, authHeader = fetchkeys.access_variables()

# DB Connection Setup
#mydb, mySchema = connection.getDatabaseConnectionDev()
#mycursor = mydb.cursor()

# --- Set Modify Date for Company from last run
#mycursor = mydb.cursor()
#mycursor.execute(
#    "INSERT INTO  " + mySchema + ".job_log (job_name, source, category, status) VALUES ('HS_Contact_Step_2',"
#    " 'Hiresmith', 'Start', 'Success');")
#mydb.commit()
#mycursor.execute("SELECT max(timestamp) FROM " + mySchema + ".job_log WHERE job_name = 'HS_Night_1' and "
#                                                            "category = 'Start' and source = 'Hiresmith' and status ="
#                                                            " 'Success';")

#modify_date_event = str(mycursor.fetchall()[0][0]).replace(" ", "T")

company_notes_data = custfunc.getAllCompanyNotes(url, authHeader) #, modify_date_event)

for key in sorted(company_notes_data):
    print('Iteration started for key: ' + str(key))
    key = str(key)
    start = '12twenty.com/Api/V2/notes/'
    getDataUrl = 'https://' + url + start + key
    data = custfunc.ExceptionGet(getDataUrl, authHeader)  # REST call with Authentication header
    data = data.json()
    print(data)
#    mycursor.execute("UPDATE " + mySchema + ".hiresmith_employer SET LastRecruitingEventDate = " + startdate + " WHERE hs_employer_id = " + companyid)

#mydb.commit()
#mycursor.execute(
#    "INSERT INTO  " + mySchema + ".job_log (job_name, source, category, status) VALUES ('HS_Contact_Step_2',"
#    " 'Hiresmith', 'End', 'Success');")
#mydb.commit()
