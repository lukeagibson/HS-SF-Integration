# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 14:55:36 2018

@author: Utkarsh
"""

import requests
import pandas as pd
import math
import sys
import datetime
#Starting of Function Definations

#function to fetch information in json format from URL. URL should be passed as a parameter  
#function defined so that we can do error handling for all the Get requests

def get_Auth_Token(urlvalue,key):
    getFinalAuthUrl = 'https://' + urlvalue + '12twenty.com/api/client/generateAuthenticationToken?Key=' + key
    print('Authentication url: ' + getFinalAuthUrl)
    authToken = ExceptionGet(getFinalAuthUrl,'')
    authToken = authToken.text
    return (authToken)

def get_Attribute_Id(attribute_seach_value,authHeader,Url):
    data_attribute = ExceptionGet(Url,authHeader)  #REST call with Authentication header
    data_attribute = data_attribute.json()
    print(attribute_seach_value)
    search_term = attribute_seach_value
    for x in data_attribute:
        if (x['Name'] == search_term):
            print(x['Id'])
            Id = x['Id']
            return(Id)
            break

def get_Attribute_Values(attribute_seach_value,authHeader,Url):
    ID = get_Attribute_Id(attribute_seach_value,authHeader,Url)
    getDataUrl = Url + '/' + str(ID)
    data_attribute_single = ExceptionGet(getDataUrl,authHeader)  #REST call with Authentication header
    data_attribute_single = data_attribute_single.json()
    return(data_attribute_single['Options'])

def ExceptionGet(urlvalue,header):
    print('URL: ' + urlvalue)
    try:
        response = requests.get(urlvalue,headers=header)
        response.raise_for_status() #raise error if there is one
        #print (response.text)
    except(requests.exceptions.ConnectionError, requests.exceptions.Timeout): #to check if the service is working or not.
        print('Service is down or the URL is incorrect. Please Check. Exiting Program.')
        sys.exit()
    except requests.exceptions.HTTPError as e: #if serevice is up but error in the response. 
        print(e.response.status_code)
        print ("Error in Response 4xx, 5xx")
        sys.exit()  #exit program if error
    else:
        print('The get call was successful')
        return(response)

#function to convert the data from python dictionary into a tabular format(dataFrame)
def CreateTabularFormat(data):
    for indx,value in enumerate(data['Items']): #looping over all the different items retured from the call
        for dicindex,dictvalue in data['Items'][indx].items(): #secondary loop for values which have an ID and String attached
            #print(dictvalue.__class__.__name__) # for debugging purposes 
            if (dictvalue.__class__.__name__ == 'dict'): #removing data that is not required.
            #print(dicindex) # for debugging purposes 
                if 'Name' in dictvalue:
                    data['Items'][indx][dicindex] = data['Items'][indx][dicindex]['Name'] #taking out the ID to just display the name for now.
                else:
                    data['Items'][indx][dicindex] = None
            elif(dictvalue.__class__.__name__ == 'list'):
                commasep=None
                for indx2,value2 in enumerate(dictvalue):
                    if 'Name' in value2:
                        commasep = data['Items'][indx][dicindex][indx2]['Name'] + ',' #taking out the ID to just display the name for now.
                data['Items'][indx][dicindex] = commasep
    return(pd.DataFrame(data['Items'])) #returning the tabular format.

#create tabular format when we have a single record returned.   
def CreateTabularFormatSingleStudent(data):
    data2 = dict(data) #creating a copy of the datta
    for dicindex,dictvalue in data.items(): #primary loop for all the data. 
        #print(dictvalue.__class__.__name__)
        if (dictvalue.__class__.__name__ == 'dict'): #for data that is retured with an ID and the corresponding display value.  
            #print(dicindex)
            if 'Name' in dictvalue:  
                data2[dicindex] = data[dicindex]['Name'] #removing the ID and just displaying the Name. 
        if (dictvalue.__class__.__name__ == 'list'):
            del data2[dicindex]
    del data2['CustomAttributeValues']
    return(pd.DataFrame(data2,index=[0])) #returning the tabular format.

#function to join the College Specific URL and the seach parameters for different parameters.
def CreateGetUrl(url,search_Query,URLRequired):
    if(URLRequired == 'Students'):
        getDataUrl = 'https://'+  url + '12twenty.com/api/v2/students' + search_Query
        return getDataUrl
    elif(URLRequired == 'Companies'):
        getDataUrl = 'https://'+  url + '12twenty.com/api/v2/companies' + search_Query
        return getDataUrl
    elif(URLRequired == 'Contacts'):
        getDataUrl = 'https://'+  url + '12twenty.com/api/v2/contacts' + search_Query
        return getDataUrl

def ParseDataInTabularFormat(data,search_Query,url,authHeader,URLRequired):
    if 'Total' and 'PageSize' in data:
        if data['Total'] == data['PageSize']:  #checking to see if we need more calls for all the data. 
            df = CreateTabularFormat(data) #converting to tabular format (dataframe) for more structured format. Similar to a structure in DB
        else:
            LoopLength = int(data['Total'])/int(data['PageSize']) #calculating the number of calls that will fetch all the data.
            LoopLength = math.ceil(LoopLength) #rounding the value to highest closest integer.
            df = CreateTabularFormat(data) #formatting the Data from the first call. 
            for i in range(2,LoopLength+1): #looping over to fetch data from different pages. 
                search_Query_WithPage = search_Query + '&PageNumber=' + str(i) #building seachparameters with the page number. 
                getDataUrl = CreateGetUrl(url,search_Query_WithPage,URLRequired) # create the URL for GET query
                data = ExceptionGet(getDataUrl,authHeader) # get Call to fetch data from 12-20
                data = data.json()
                value = CreateTabularFormat(data) #creating the tabular format from data recieved.
                df = df.append(value) #adding to data from other pages. 
    return(df)

def putRequest(getDataUrl,data,authHeader):
     putrequest = requests.put(getDataUrl, json = data, headers = authHeader)
     print("The output of put request is: " + putrequest.text)
     return(putrequest.text)


def updateStudentGroups(mappingtable,getDataUrl,authHeader,exceptionsg,putUrl,student_groups_key,LoopLength=2):
    df3 = pd.DataFrame(columns= ['FullName','Id','Old Groups','New Groups'])
    for i in range(2,LoopLength+1): #looping over to fetch data from different pages. 
        getDataUrl_loop = getDataUrl + '&PageNumber=' + str(i) #building seachparameters with the page number. 
        print (getDataUrl_loop)
        data = ExceptionGet(getDataUrl_loop,authHeader)  #REST call with Authentication header
        data = data.json()
        if 'Total' and 'PageSize' in data:                                         #check to see if the data containsembedded data. 
            print ('Testing')                                                      #checking to see if we need more calls for all the data. 
            for indx,value in enumerate(data['Items']):                            #looping over the students that we have.
                results =pd.DataFrame(columns=list(mappingtable))                  #initializing the dataframe
                print('starting for student name: ' + value['FullName'])           #logging for the student reference 
                Update_programs = False                                            #resetting the flag value
                containsExtragroup = False                                         #resetting the flag value
                #removing the expeption list of Student groups
                groupswithoutexceptions = []
                groupswithexception = []
                if isinstance(value['StudentGroups'],list) == False:#check to see if the student has any student groups assigned.
                    print('No student groups assigned to student.')
                    continue
                for ind,val in enumerate(value['StudentGroups']):   #checking to see if student contains student group which does not need to be changed.
                    #print (val['Name'])
                    if val['Name'] not in exceptionsg['Name'].unique():
                        groupswithoutexceptions.append(val)
                    else:
                        groupswithexception.append(val)
                        containsExtragroup = True
                value['StudentGroups'] = groupswithoutexceptions
                Grad_term = value['GraduationTerm']                              
                Grad_year = value['GraduationYearId']
                if(Grad_term == 'Spring'):
                    DateCompValue = datetime.datetime.now() -datetime.datetime(Grad_year,5,22)     #calculating the days to the change.
                elif(Grad_term == 'Winter'):
                    Grad_year= int(Grad_year) - 1                                  #as winter is counted as gradution in the next year we need to substract one year from the graduation date to actually get the correct graduation date. 
                    DateCompValue = datetime.datetime.now() -datetime.datetime(Grad_year,12,20)
                elif(Grad_term == 'Summer'):
                    Grad_year= int(Grad_year) - 1
                    DateCompValue = datetime.datetime.now() -datetime.datetime(Grad_year,8,22)
                list_of_programs = []
                #value['StudentGroups'] = new_groups
                temp_holder_list =[]    
                undergradmajor = None
                oldgroupsComma = ''
                for ind,val in enumerate(value['StudentGroups']):
                    #print (val['Name'])
                    oldgroupsComma = oldgroupsComma + ',' + val['Name']  #for testing and logging
                    list_of_programs.append(val['Id'])      #
                    string_split = val['Name'].split("-")    #chcek to get the undergrad major if there is one.
                    string_split = string_split[1].strip()
                    if string_split in mappingtable['Major'].unique() and value['Program']['Name'] == 'Undergrad BBA':
                        string_split = val['Name'].split(",")    #chcek to get the undergrad major if there is one.
                        string_split = string_split[1].strip()
                        undergradmajor = string_split
                        df = mappingtable[(mappingtable.Begin < DateCompValue.days) & (mappingtable.End > DateCompValue.days) & (mappingtable.Major == undergradmajor) & (mappingtable.GraduationTerm == value['GraduationTerm'])]   #fetching the student groups the student should actually be a member of. 
                        results = results.append(df)   
                    if (value['Program']['Name'] != 'Undergrad BBA'):    #if not undegrad then check the program rather than the major. 
                        print('Not a undergrad student')
                        results = mappingtable[(mappingtable.Begin < DateCompValue.days) & (mappingtable.End > DateCompValue.days) & (mappingtable.Program == value['Program']['Name']) & (mappingtable.GraduationTerm == value['GraduationTerm'])]
                    #   else:
                    #      print('Not a undergrad student')
                    #      results = mappingtable[(mappingtable.Begin < DateCompValue.days) & (mappingtable.End > DateCompValue.days) & (mappingtable.Program == value['Program']['Name']) & (mappingtable.GraduationTerm == value['GraduationTerm'])]
                new_groups = []
                new_groups_reference = []
                newgroupscommaseperated = ''
                for ind,val in results.iterrows():       #building the new student groups from the results dataframe. inculding ID and removing duplicates
                    list_of_groups = val['Student Groups'].split(",")
                    for y,z in enumerate(list_of_groups):
                        temp_dict = {}
                        temp_dict['Name'] = z.strip()
                        temp_dict['Id'] = student_groups_key[temp_dict['Name']]
                        if temp_dict['Id'] not in list_of_programs:                #check to see if the student groups have changed and if student profile needs to be updated.
                            Update_programs = True
                        if temp_dict['Id'] not in new_groups_reference:            #building list to check the student groups and whether there is a difference in it or not.
                            new_groups.append(temp_dict)
                            new_groups_reference.append(temp_dict['Id'])
                            newgroupscommaseperated =  newgroupscommaseperated + ',' + z     #for logging and testing.
                if len(new_groups) != len(value['StudentGroups']):       #for edge case senario where groups are deleted from students
                    Update_programs = True
                if len(new_groups) == 0:        #if the number of new groups for the student is zero then dont update the student.
                    Update_programs = False
                if Update_programs == True:    #actual updation
                    updated_student = value   
                    updated_student['StudentGroups'] = new_groups 
                        #for testing and logging.
                    df1 = pd.DataFrame([[updated_student['FullName'],updated_student['StudentId'],oldgroupsComma,newgroupscommaseperated]], columns= ['FullName','Id','Old Groups','New Groups'])
                    df3 = df3.append(df1)
                        #end of testing and logging.
                    if containsExtragroup == True:
                        updated_student['StudentGroups'].append(groupswithexception) 
                    putUrl_student = putUrl + '/' + str(updated_student['Id'])
                    putRequest(putUrl_student,updated_student,authHeader)
                    print ('the following student was updated: ' + updated_student['FullName'])
    return(df3)

def CreateDicofStudents(data,all_student_data):
    for indx,value in enumerate(data['Items']):
        if('StudentId' in value):
            all_student_data [value['StudentId']] = value
    return all_student_data

def CreateDicofCompanies(data,all_company_data):
    for indx,value in enumerate(data['Items']):
        if('Id' in value):
            all_company_data [value['Id']] = value
    return all_company_data

def CreateDicofContacts(data,all_company_data):
    for indx,value in enumerate(data['Items']):
        if('Id' in value):
            all_company_data [value['Id']] = value
    return all_company_data

def getLookups(url,authHeader):
    getDataUrl = 'https://'+  url + '12twenty.com/api/v2/Lookups?PageSize=500'
    data = ExceptionGet(getDataUrl,authHeader)  #REST call with Authentication header
    data = data.json()
    all_student_data = {}
    all_student_data = CreateDicofStudents(data,all_student_data)
    
    #The code below checks the nummber of pages of data that is fetched from the query and does GET calls to fetch the data from each respective page. 
    
    if 'Total' and 'PageSize' in data:
        LoopLength = int(data['Total'])/int(data['PageSize']) #calculating the number of calls that will fetch all the data.
        LoopLength = math.ceil(LoopLength) #rounding the value to highest closest integer.
        for i in range(2,LoopLength+1): #looping over to fetch data from different pages. 
            getDataUrl2 = getDataUrl + '&PageNumber=' + str(i) #building seachparameters with the page number. 
            data = ExceptionGet(getDataUrl2,authHeader) # get Call to fetch data from 12-20
            data = data.json()
            all_student_data = CreateDicofStudents(data,all_student_data)
    return(all_student_data)

def getAllStudents(url,authHeader):
    getDataUrl = 'https://'+  url + '12twenty.com/api/v2/students?PageSize=500'
    data = ExceptionGet(getDataUrl,authHeader)  #REST call with Authentication header
    data = data.json()
    all_student_data = {}
    all_student_data = CreateDicofStudents(data,all_student_data)
    
    #The code below checks the nummber of pages of data that is fetched from the query and does GET calls to fetch the data from each respective page. 
    
    if 'Total' and 'PageSize' in data:
        LoopLength = int(data['Total'])/int(data['PageSize']) #calculating the number of calls that will fetch all the data.
        LoopLength = math.ceil(LoopLength) #rounding the value to highest closest integer.
        for i in range(2,LoopLength+1): #looping over to fetch data from different pages. 
            getDataUrl2 = getDataUrl + '&PageNumber=' + str(i) #building seachparameters with the page number. 
            data = ExceptionGet(getDataUrl2,authHeader) # get Call to fetch data from 12-20
            data = data.json()
            all_student_data = CreateDicofStudents(data,all_student_data)
    return(all_student_data)
    
def getAllCompaniesByDate(url,authHeader,modify_date_input):
    getDataUrl = 'https://'+  url + '12twenty.com/Api/V2/companies?ModifyFromDate='+modify_date_input+'&PageSize=500'
    data = ExceptionGet(getDataUrl,authHeader)  #REST call with Authentication header
    data = data.json()
    all_company_data_by_date = {}
    all_company_data_by_date = CreateDicofCompanies(data,all_company_data_by_date)
    
    #The code below checks the nummber of pages of data that is fetched from the query and does GET calls to fetch the data from each respective page. 
    
    if 'Total' and 'PageSize' in data:
        LoopLength = int(data['Total'])/int(data['PageSize']) #calculating the number of calls that will fetch all the data.
        LoopLength = math.ceil(LoopLength) #rounding the value to highest closest integer.
        for i in range(2,LoopLength+1): #looping over to fetch data from different pages. 
            getDataUrl2 = getDataUrl + '&PageNumber=' + str(i) #building seachparameters with the page number. 
            data = ExceptionGet(getDataUrl2,authHeader) # get Call to fetch data from 12-20
            data = data.json()
            all_company_data_by_date = CreateDicofCompanies(data,all_company_data_by_date)
    return(all_company_data_by_date)
    
def getAllContactsByDate(url,authHeader,modify_date_input):
    getDataUrl = 'https://'+  url + '12twenty.com/Api/V2/contacts?ModifyFromDate='+modify_date_input+'&PageSize=500'
    data = ExceptionGet(getDataUrl,authHeader)  #REST call with Authentication header
    data = data.json()
    all_contact_data_by_date = {}
    all_contact_data_by_date = CreateDicofContacts(data,all_contact_data_by_date)
    
    #The code below checks the nummber of pages of data that is fetched from the query and does GET calls to fetch the data from each respective page. 
    
    if 'Total' and 'PageSize' in data:
        LoopLength = int(data['Total'])/int(data['PageSize']) #calculating the number of calls that will fetch all the data.
        LoopLength = math.ceil(LoopLength) #rounding the value to highest closest integer.
        for i in range(2,LoopLength+1): #looping over to fetch data from different pages. 
            getDataUrl2 = getDataUrl + '&PageNumber=' + str(i) #building seachparameters with the page number. 
            data = ExceptionGet(getDataUrl2,authHeader) # get Call to fetch data from 12-20
            data = data.json()
            all_contact_data_by_date = CreateDicofContacts(data,all_contact_data_by_date)
    return(all_contact_data_by_date)
    
def getAllCompanies(url,authHeader):
    getDataUrl = 'https://'+  url + '12twenty.com/Api/V2/companies?PageSize=500'
    data = ExceptionGet(getDataUrl,authHeader)  #REST call with Authentication header
    data = data.json()
    all_company_data = {}
    all_company_data = CreateDicofCompanies(data,all_company_data)
    
    #The code below checks the nummber of pages of data that is fetched from the query and does GET calls to fetch the data from each respective page. 
    
    if 'Total' and 'PageSize' in data:
        LoopLength = int(data['Total'])/int(data['PageSize']) #calculating the number of calls that will fetch all the data.
        LoopLength = math.ceil(LoopLength) #rounding the value to highest closest integer.
        for i in range(2,LoopLength+1): #looping over to fetch data from different pages. 
            getDataUrl2 = getDataUrl + '&PageNumber=' + str(i) #building seachparameters with the page number. 
            data = ExceptionGet(getDataUrl2,authHeader) # get Call to fetch data from 12-20
            data = data.json()
            all_company_data = CreateDicofCompanies(data,all_company_data)
    return(all_company_data)
    
def getAllContacts(url,authHeader):
    getDataUrl = 'https://'+  url + '12twenty.com/Api/V2/contacts?PageSize=500'
    data = ExceptionGet(getDataUrl,authHeader)  #REST call with Authentication header
    data = data.json()
    all_contact_data = {}
    all_contact_data = CreateDicofContacts(data,all_contact_data)
    
    #The code below checks the nummber of pages of data that is fetched from the query and does GET calls to fetch the data from each respective page. 
    
    if 'Total' and 'PageSize' in data:
        LoopLength = int(data['Total'])/int(data['PageSize']) #calculating the number of calls that will fetch all the data.
        LoopLength = math.ceil(LoopLength) #rounding the value to highest closest integer.
        for i in range(2,LoopLength+1): #looping over to fetch data from different pages. 
            getDataUrl2 = getDataUrl + '&PageNumber=' + str(i) #building seachparameters with the page number. 
            data = ExceptionGet(getDataUrl2,authHeader) # get Call to fetch data from 12-20
            data = data.json()
            all_contact_data = CreateDicofContacts(data,all_contact_data)
    return(all_contact_data)
    

def removeDuplicateStudentGroups(list_for_removal):
    new_list_groups = {}
    list_to_return = []
    for x,y in enumerate(list_for_removal):
        new_list_groups[y['Id']] = y['Name']
    for key,value in new_list_groups.items():
        d = {}
        d['Id'] = key
        d['Name'] = value
        list_to_return.append(d)
    return (list_to_return)



# --- Start Notes Functions ---


def getAllCompanyNotesByDate(url,authHeader,modify_date_input):
    getDataUrl = 'https://'+  url + '12twenty.com/Api/V2/Notes?EntityTypeId=2201&ModifyFromDate='+modify_date_input+'&PageSize=500'
    data = ExceptionGet(getDataUrl,authHeader)  #REST call with Authentication header
    data = data.json()
    all_botes_data_by_date = {}
    all_notes_data_by_date = CreateDicofNotes(data,all_notes_data_by_date)
    
    #The code below checks the nummber of pages of data that is fetched from the query and does GET calls to fetch the data from each respective page. 
    
    if 'Total' and 'PageSize' in data:
        LoopLength = int(data['Total'])/int(data['PageSize']) #calculating the number of calls that will fetch all the data.
        LoopLength = math.ceil(LoopLength) #rounding the value to highest closest integer.
        for i in range(2,LoopLength+1): #looping over to fetch data from different pages. 
            getDataUrl2 = getDataUrl + '&PageNumber=' + str(i) #building seachparameters with the page number. 
            data = ExceptionGet(getDataUrl2,authHeader) # get Call to fetch data from 12-20
            data = data.json()
            all_notes_data_by_date = CreateDicofNotes(data,all_notes_data_by_date)
    return(all_notes_data_by_date)

def getAllContactNotesByDate(url,authHeader,modify_date_input):
    getDataUrl = 'https://'+  url + '12twenty.com/Api/V2/Notes?EntityTypeId=2301&ModifyFromDate='+modify_date_input+'&PageSize=500'
    data = ExceptionGet(getDataUrl,authHeader)  #REST call with Authentication header
    data = data.json()
    all_notes_data_by_date = {}
    all_notes_data_by_date = CreateDicofNotes(data,all_notes_data_by_date)
    
    #The code below checks the nummber of pages of data that is fetched from the query and does GET calls to fetch the data from each respective page. 
    
    if 'Total' and 'PageSize' in data:
        LoopLength = int(data['Total'])/int(data['PageSize']) #calculating the number of calls that will fetch all the data.
        LoopLength = math.ceil(LoopLength) #rounding the value to highest closest integer.
        for i in range(2,LoopLength+1): #looping over to fetch data from different pages. 
            getDataUrl2 = getDataUrl + '&PageNumber=' + str(i) #building seachparameters with the page number. 
            data = ExceptionGet(getDataUrl2,authHeader) # get Call to fetch data from 12-20
            data = data.json()
            all_notes_data_by_date = CreateDicofNotes(data,all_notes_data_by_date)
    return(all_notes_data_by_date)

    
def getAllCompanyNotes(url,authHeader):
    getDataUrl = 'https://'+  url + '12twenty.com/Api/V2/Notes?EntityTypeId=2201&PageSize=500'
    data = ExceptionGet(getDataUrl,authHeader)  #REST call with Authentication header
    data = data.json()
    all_company_notes_data = {}
    all_company_notes_data = CreateDicofCompanyNotes(data,all_company_notes_data)
    
    #The code below checks the nummber of pages of data that is fetched from the query and does GET calls to fetch the data from each respective page. 
    
    if 'Total' and 'PageSize' in data:
        LoopLength = int(data['Total'])/int(data['PageSize']) #calculating the number of calls that will fetch all the data.
        LoopLength = math.ceil(LoopLength) #rounding the value to highest closest integer.
        for i in range(2,LoopLength+1): #looping over to fetch data from different pages. 
            getDataUrl2 = getDataUrl + '&PageNumber=' + str(i) #building seachparameters with the page number. 
            data = ExceptionGet(getDataUrl2,authHeader) # get Call to fetch data from 12-20
            data = data.json()
            all_company_notes_data = CreateDicofNotes(data,all_company_notes_data)
    return(all_company_notes_data)
    
def getAllContactNotes(url,authHeader):
    getDataUrl = 'https://'+  url + '12twenty.com/Api/V2/Notes?EntityTypeId=2301&PageSize=500'
    data = ExceptionGet(getDataUrl,authHeader)  #REST call with Authentication header
    data = data.json()
    all_contact_notes_data = {}
    all_contact_notes_data = CreateDicofContactNotes(data,all_contact_notes_data)
    
    #The code below checks the nummber of pages of data that is fetched from the query and does GET calls to fetch the data from each respective page. 
    
    if 'Total' and 'PageSize' in data:
        LoopLength = int(data['Total'])/int(data['PageSize']) #calculating the number of calls that will fetch all the data.
        LoopLength = math.ceil(LoopLength) #rounding the value to highest closest integer.
        for i in range(2,LoopLength+1): #looping over to fetch data from different pages. 
            getDataUrl2 = getDataUrl + '&PageNumber=' + str(i) #building seachparameters with the page number. 
            data = ExceptionGet(getDataUrl2,authHeader) # get Call to fetch data from 12-20
            data = data.json()
            all_contact_notes_data = CreateDicofNotes(data,all_contact_notes_data)
    return(all_contact_notes_data)


def CreateDicofNotes(data,all_notes_data):
    for indx,value in enumerate(data['Items']):
        if('Id' in value):
            all_notes_data [value['Id']] = value
    return all_notes_data

# end of function definations. 
