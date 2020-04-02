#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 11 12:53:06 2019

@author: Rishi Jain GA-OCS

#Sandbox Environment Specific

# Python file to return url, api key and auth token
"""


import requests
import Functions as custfunc
import pandas as pd
import math
import sys
import datetime


def access_variables():
    url = 'smith-maryland.admin.sandbox-' #Specific url for Smith school.
    api_key = 'Lep5LeXZ4LpyBEzx' #key value which we should have before hand.
    authToken = custfunc.get_Auth_Token(url,api_key) #Generating authentication token and header to access data
    authHeader = { 'Authorization': 'Bearer ' + authToken }
    return url, authHeader

def env_select():
    env_type = 'Sandbox'
    return env_type


# end of function definations. 
