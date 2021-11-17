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
        if e.Status == 'Phase5':
            #
            print(137*'-' + '\n')
            print(e.EntityRegistrantName + ' (' + e.TradingSymbol + ') \n')
            #
            # last filings
            try:
                #
                # URL
                URL = r"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="
                URL = URL + str(e.EntityCentralIndexKey) 
                URL = URL + "&type=10-k&dateb=&owner=exclude&count=40&search_text="
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
                        while '[Amend]' not in c:
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
                # date of report
                try:
                    amended = {}
                    for acc in accessionnumbers:
                        #
                        b = r"https://www.sec.gov/Archives/edgar/data/"
                        b = b + e.EntityCentralIndexKey + '/'
                        b = b + acc.replace('-','') + '/'
                        b = b + acc + '-index.htm'
                        #
                        g = 0
                        while g < 10:
                            try:
                                b = fetch(b)
                                g = 10
                            except:
                                g = g + 1
                        #
                        b = b.find_all('div', class_="info")[3].text
                        #
                        d = datetime.datetime.strptime(b, '%Y-%m-%d')
                        #
                        append_value(amended, acc, d)
                except:
                    pass
                #
                #
                print(amended)
                #
                # variables
                try:
                    a = ''
                    b = ''
                    c = ''
                    d = ''
                    ee = ''
                    f = ''
                except:
                    pass
                #
                # amend
                for key, value in amended.items():
                    #
                    s = e.lastyear
                    s = datetime.datetime(s.year, s.month, s.day)
                    if s == value:
                        if a == '':
                            a = 'Amend'
                            e.accessionnumberlastyear = key
                            e.amendlastyear = a
                    #
                    s = e.secondlastyear
                    s = datetime.datetime(s.year, s.month, s.day)
                    if s == value:
                        if b == '':
                            b = 'Amend'
                            e.accessionnumbersecondlastyear = key
                            e.amendsecondlastyear = b
                    #
                    s = e.thirdlastyear
                    s = datetime.datetime(s.year, s.month, s.day)
                    if s == value:
                        if c == '':
                            c = 'Amend'
                            e.accessionnumberthirdlastyear = key
                            e.amendthirdlastyear = c
                    #
                    s = e.fourthlastyear
                    s = datetime.datetime(s.year, s.month, s.day)
                    if s == value:
                        if d == '':
                            d = 'Amend'
                            e.accessionnumberfourthlastyear = key
                            e.amendfourthlastyear = d
                    #
                    try:
                        s = e.fifthlastyear
                        s = datetime.datetime(s.year, s.month, s.day)
                        if s == value:
                            if ee == '':
                                ee = 'Amend'
                                e.accessionnumberfifthlastyear = key
                                e.amendfifthlastyear = ee
                    except:
                        pass
                    #
                    try:
                        s = e.sixthlastyear
                        s = datetime.datetime(s.year, s.month, s.day)
                        if s == value:
                            if f == '':
                                f = 'Amend'
                                e.accessionnumbersixthlastyear = key
                                e.amendsixthlastyear = f
                    except:
                        pass
                #
                # phase
                if e.accessionnumberlastyear != '':
                    if e.accessionnumbersecondlastyear != '':
                        if e.accessionnumberthirdlastyear != '':
                            if e.accessionnumberfourthlastyear != '':
                                e.Status = 'Phase6.1'
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



