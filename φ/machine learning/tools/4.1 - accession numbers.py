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

# Accession Number Replacements
rep = [
    'Transition reports [Rule 13a-10 or 15d-10]Acc-no: ',
    'Annual report [Section 13 and 15(d), not S-K Item 405]Acc-no: ',
    'Annual report [Sections 13 and 15(d), not S-K Item 405]Acc-no: ',
    'Annual report [Section 13 and 15(d), S-K Item 405] ',
    'Annual report [Sections 13 and 15(d), S-K Item 405] ',
    'Quarterly report [Sections 13 or 15(d)]Acc-no: ',
    '[Cover]',
    '[Amend] ',
]

# BeautifulSoup parser
def fetch(url):
    thepage = urllib.request.urlopen(url)
    soupdata = BeautifulSoup(thepage,"html.parser")
    return soupdata

# Append values if key already exists
def append_value(dict_obj, key, value):
    # Check if key exist in dict or not
    if key in dict_obj:
        dict_obj[key] = value
    else:
        dict_obj[key] = value

# loop
entities = Entity.objects.all().order_by('TradingSymbol')

l = 1

l = len(entities)

# counter
for count in range(0, l):
    #
    e = entities[count]
    #
    # retreives entity from db
    try:
        #
        if e.Status == 'Phase4.1':
            #
            print(137*'-' + '\n')
            print(e.EntityRegistrantName + ' (' + e.TradingSymbol + ') \n')
            #
            # deletes dates and accession numbers entries
            try:
                e.lastyear = None
                e.accessionnumberlastyear = ''
                e.secondlastyear = None
                e.accessionnumbersecondlastyear = ''
                e.thirdlastyear = None
                e.accessionnumberthirdlastyear = ''
                e.fourthlastyear = None
                e.accessionnumberfourthlastyear = ''
                e.fifthlastyear = None
                e.accessionnumberfifthlastyear = ''
                e.sixthlastyear = None
                e.accessionnumbersixthlastyear = ''
                e.seventhlastyear = None
                e.accessionnumberseventhlastyear = ''
            except:
                pass
            #
            # last filings
            try:
                #
                # URL
                URL = r"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="
                URL = URL + str(e.EntityCentralIndexKey) 
                URL = URL + "&type=10-k&dateb=&owner=exclude&count=40&search_text="
                #
                print(URL)
                #
                # html
                r = 0
                while r < 10:
                    try:
                        html = fetch(URL)
                        r = 10
                    except:
                        r = r + 1
                #
                # retreives accession numbers
                try:
                    accessionnumbers = []
                    #
                    u = html.find_all('td', class_='small')
                    #
                    i = 0
                    #
                    while i < len(u) - 1:
                        #
                        c = u[i].text
                        #
                        while '[Amend]' in c:
                            i = i + 1
                            c = u[i].text
                        #
                        for r in rep:
                            c = c.replace(r,'')
                        #
                        c = c[:20]
                        #
                        accessionnumber = c
                        #
                        if accessionnumber != None:
                            accessionnumbers.append(accessionnumber)
                        #
                        i = i + 1
                except:
                    pass
                #
                print(accessionnumbers)
                #
                # save data 
                try:
                    #
                    t = 0
                    s = len(accessionnumbers)
                    #
                    while t < s:
                        #
                        c = None
                        c = accessionnumbers[t]
                        #
                        if t == 0:
                            e.accessionnumberlastyear = c
                        if t == 1:
                            e.accessionnumbersecondlastyear = c
                        if t == 2:
                            e.accessionnumberthirdlastyear = c
                        if t == 3:
                            e.accessionnumberfourthlastyear = c
                        if t == 4:
                            e.accessionnumberfifthlastyear = c
                        if t == 5:
                            e.accessionnumbersixthlastyear = c
                        if t == 6:
                            e.accessionnumberseventhlastyear = c
                        #
                        t = t + 1
                except:
                    pass
                #
                # Phase
                if e.accessionnumberlastyear != '':
                    if e.accessionnumbersecondlastyear != '':
                        if e.accessionnumberthirdlastyear != '':
                            if e.accessionnumberfourthlastyear != '':
                                e.Status = 'Phase4.2'
                #
                # Time Of Update
                try:
                    now = datetime.datetime.now()
                    e.Update = now
                except:
                    pass
                #
                # save entity
                e.save()
                #
            except:
                pass
    except:
        pass



