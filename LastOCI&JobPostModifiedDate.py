#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created by: Punit & Stephen 
Date Created: 4/7/2020
'''

import PrivateKeys as fetchkeys
import pandas as pd
import Functions as custfunc
import requests
import DBconnection as connection
import sys
from datetime import datetime
import time

url, authHeader = fetchkeys.access_variables()  # function call to fetch the url, authHeader, api key and auth token
env_type = fetchkeys.env_select()  # function call to fetch the environment of run.

# CONNECT TO DATABASE SERVER
# DB Connection Setup
mydb, mySchema = connection.getDatabaseConnectionSandbox()
mycursor = mydb.cursor()

mycursor.execute("SELECT max(timestamp) FROM " + mySchema + ".job_log WHERE job_name = 'HS_Last_OCI_Job_Date' and "
                                                            "category = 'End' and source = 'Hiresmith' and status ="
                                                            " 'Success';")
modify_date_input = str(mycursor.fetchall()[0][0]).replace(" ", "T")

# Get All Jobs
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
    "INSERT INTO " + mySchema + ".job_log (job_name, source, category, status) VALUES ('HS_Last_OCI_Job_Date', 'Hiresmith', 'End', 'Success');"
)
mydb.commit()