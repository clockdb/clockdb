#
# Libraries
from φ.models import *
from bs4 import BeautifulSoup
from io import StringIO
from datetime import datetime, date
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.request import urlopen
import collections
import csv
import datetime
import glob
import html5lib
import json
import os
import pandas as pd
import pathlib
import pprint
import re
import requests
import time
import urllib
import xml.etree.ElementTree as ET

# loop
entities = Entity.objects.all().order_by('TradingSymbol')

l = 1

l = len(entities)

phases = [
    'Phase6.2',
]

for count in range(0, l):
    #
    e = entities[count]
    #
    if e.Status in phases:
        #
        print(str(e) + '\n' + 137*'-')
        #
        # urls
        try:
            urls1 = [
                e.urlbalancesheetlastyear,
                e.urlincomestatementlastyear,
                e.urlcomprehensiveincomelastyear,
                e.urlstockholdersequitylastyear,
                e.urlcashflowlastyear,
            ]
            urls2 = [
                e.urlbalancesheetsecondlastyear,
                e.urlincomestatementsecondlastyear,
                e.urlcomprehensiveincomesecondlastyear,
                e.urlstockholdersequitysecondlastyear,
                e.urlcashflowsecondlastyear,
            ]
            urls3 = [
                e.urlbalancesheetthirdlastyear,
                e.urlincomestatementthirdlastyear,
                e.urlcomprehensiveincomethirdlastyear,
                e.urlstockholdersequitythirdlastyear,
                e.urlcashflowthirdlastyear,
            ]
            urls4 = [
                e.urlbalancesheetfourthlastyear,
                e.urlincomestatementfourthlastyear,
                e.urlcomprehensiveincomefourthlastyear,
                e.urlstockholdersequityfourthlastyear,
                e.urlcashflowfourthlastyear,
            ]
            urls5 = [
                e.urlbalancesheetfifthlastyear,
                e.urlincomestatementfifthlastyear,
                e.urlcomprehensiveincomefifthlastyear,
                e.urlstockholdersequityfifthlastyear,
                e.urlcashflowfifthlastyear,
            ]
            urls6 = [
                e.urlbalancesheetsixthlastyear,
                e.urlincomestatementsixthlastyear,
                e.urlcomprehensiveincomesixthlastyear,
                e.urlstockholdersequitysixthlastyear,
                e.urlcashflowsixthlastyear,
            ]
        except:
            pass
        #
        # counter
        try: 
            #
            # last year
            u = 0
            e.urlsauditlastyear = 0
            for urls in urls1:
                if urls != '':
                    u = u + 1
                    e.urlsauditlastyear = u
            #
            # second last year
            u = 0
            e.urlsauditsecondlastyear = 0
            for urls in urls2:
                if urls != '':
                    u = u + 1
                    e.urlsauditsecondlastyear = u
            #
            # third last year
            u = 0
            e.urlsauditthirdlastyear = 0
            for urls in urls3:
                if urls != '':
                    u = u + 1
                    e.urlsauditthirdlastyear = u
            #
            # fourth last year
            u = 0
            e.urlsauditfourthlastyear = 0
            for urls in urls4:
                if urls != '':
                    u = u + 1
                    e.urlsauditfourthlastyear = u
            #
            # fifth last year
            u = 0
            e.urlsauditfifthlastyear = 0
            for urls in urls5:
                if urls != '':
                    u = u + 1
                    e.urlsauditfifthlastyear = u
            #
            # sixth last year
            u = 0
            e.urlsauditsixthlastyear = 0
            for urls in urls6:
                if urls != '':
                    u = u + 1
                    e.urlsauditsixthlastyear = u
        except:
            pass
        #
        # status
        if e.Status == 'Phase6.2':
            e.Status = 'Phase6.1'
            a = 'Phase6.3'
            if e.urlsauditlastyear > 3:
                if e.urlsauditsecondlastyear > 3:
                    if e.urlsauditthirdlastyear > 3:
                        if e.urlsauditfourthlastyear > 3:
                            if e.fifthlastyear != None:
                                if e.urlsauditfifthlastyear > 3:
                                    if e.sixthlastyear != None:
                                        if e.urlsauditsixthlastyear > 3:
                                            e.Status = a
                                    else:
                                        e.Status = a
                            else:
                                e.Status = a
        #
        # Time Of Update
        try:
            now = datetime.datetime.now()
            e.Update = now
        except:
            pass
        #
        # save
        e.save()


