#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created by: Kuntal 
Date Created: 3/8/2020
'''

import mysql.connector

def getDatabaseConnectionSandbox():
    mydb = mysql.connector.connect(
        host="192.168.15.25",
        port="3306",
        database="hiresmith_etl_sandbox",
        user="hiresmith_etl",
        passwd="s*2FZ8&hin%ISyte"
    )

    return mydb, "hiresmith_etl_sandbox"


def getDatabaseConnectionDev():
    mydb = mysql.connector.connect(
        host="127.0.0.1",
        port="3306",
        database="hiresmith_test_db",
        user="root",
        passwd=""
    )

    return mydb, "hiresmith_test_db"

def getDatabaseConnectionProd():
    mydb = mysql.connector.connect(
        host="",
        port="",
        database="",
        user="",
        passwd=""
    )

    return mydb, "hiresmith_etl_sandbox"
