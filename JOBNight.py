#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created by: Luke, Punit
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
import requests
import sys


# Environment setup

# Base URL and Auth Header
url, authHeader = fetchkeys.access_variables()

# DB Connection Setup
mydb, mySchema = connection.getDatabaseConnectionDev()

# --- Set Modify Date for Company from last run
mycursor = mydb.cursor()
mycursor.execute(
    "INSERT INTO  " + mySchema + ".job_log (job_name, source, category, status) VALUES ('HS_Night_Recruit',"
    " 'Hiresmith', 'Start', 'Success');")
mydb.commit()


mycursor.execute("SELECT max(timestamp) FROM " + mySchema + ".job_log WHERE job_name = 'HS_Night_Recruit' and "
                                                            "category = 'Start' and source = 'Hiresmith' and status ="
                                                            " 'Success';")

modify_date_event = str(mycursor.fetchall()[0][0]).replace(" ", "T")

recruiting_event_data_by_date = custfunc.getAllRecruitingEvents(url, authHeader) #, modify_date_event)

for key in sorted(recruiting_event_data_by_date):
    print('Iteration started for key: ' + str(key))
    key = str(key)
    start = '12twenty.com/Api/V2/Events/'
    getDataUrl = 'https://' + url + start + key
    data = custfunc.ExceptionGet(getDataUrl, authHeader)  # REST call with Authentication header
    data = data.json()
    companyid = str(data['CompanyId'])
    #print(data['StartDate'])
    startdate = datetime.strptime(data['StartDate'],'%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d')
    #print(startdate)
    mycursor.execute("UPDATE " + mySchema + ".hiresmith_employer SET LastRecruitingEventDate = " + startdate + " WHERE hs_employer_id = " + companyid)

mydb.commit()
mycursor.execute(
    "INSERT INTO  " + mySchema + ".job_log (job_name, source, category, status) VALUES ('HS_Night_Recruit',"
    " 'Hiresmith', 'End', 'Success');")
mydb.commit()

mycursor.execute(
    "INSERT INTO  " + mySchema + ".job_log (job_name, source, category, status) VALUES ('HS_Night_Last_Job_Date',"
    " 'Hiresmith', 'Start', 'Success');")
mydb.commit()
modify_date_input = str(mycursor.fetchall()[0][0]).replace(" ", "T")

# Get All Jobs
mycursor.execute("SELECT max(timestamp) FROM " + mySchema + ".job_log WHERE job_name = 'HS_Night_Last_Job_Date' and "
                                                            "category = 'End' and source = 'Hiresmith' and status ="
                                                            " 'Success';")
jobs = custfunc.getAllJobPostingsByDate(url,authHeader,modify_date_input)

companies = [] # All Company IDs
for k,v in jobs.items():
    companies.append(v['CompanyId'])

uniqueCompanyList = [] # All Unique Company IDs
for company in companies:
    if company not in uniqueCompanyList:
        uniqueCompanyList.append(company)

# Find Last OCI Date and Last Job Modification Date and Update DB
for companyId in uniqueCompanyList:
    OCIdates = []
    JobPostings = []
    for key, job in jobs.items():
        if (job['CompanyId'] == companyId and job['OciId'] != 0 and job['InterviewDates'] != []):
            for date in job['InterviewDates']:
                OCIdates.append([job['OciId'], date])
        if(job['CompanyId'] == companyId and job['OciId'] == 0):
            JobPostings.append([job['Id'], job["ModifyDate"]])
    if (OCIdates != []):
        LastOCI = max(OCIdates, key=lambda x: x[1])
        LastOCIDate = datetime.strptime(LastOCI[1],'%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d')
        mycursor.execute("UPDATE "+mySchema+".hiresmith_employer SET LastOCIDate = " + LastOCIDate + "WHERE hs_employer_id = " + companyId)
    if (JobPostings != []):
        LastJobPosting = max(JobPostings, key=lambda x: x[1])
        LastModifiedDate = datetime.strptime(LastJobPosting[1],'%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d')
        mycursor.execute("UPDATE "+mySchema+".hiresmith_employer SET LastJobPostingDATe = " + LastModifiedDate + "WHERE hs_employer_id = " + companyId)
    
mydb.commit()

mycursor.execute(
    "INSERT INTO  " + mySchema + ".job_log (job_name, source, category, status) VALUES ('HS_Night_Last_Job_Date',"
    " 'Hiresmith', 'End', 'Success');")
mydb.commit()
