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
import urllib.request, json
import os
import pandas as pd
import pathlib
import pprint
import re
import requests
import time
import urllib
import xml.etree.ElementTree as ET

# BeautifulSoup parser
def fetch(url):
    thepage = urllib.request.urlopen(url)
    soupdata = BeautifulSoup(thepage,"html.parser")
    return soupdata

base_url = 'http://www.clockdb.com/'

entities_url = base_url + 'entities/'

with urllib.request.urlopen(entities_url) as url:
    data = json.loads(url.read().decode())
    entitiesData = data['entities']

start = 0

i = 0

for entity in entitiesData:
    if (i > start - 1):
    #if (i < 1):
        try:
            ts = entity['url'].replace('./', '')
            #ts = 'FB'
            try:
                e = Entity.objects.get(TradingSymbol=ts)
            except:
                e = Entity()
                e.TradingSymbol = ts
            if (e.db < 21):
                # Get url from Trading Symbol
                url = base_url + ts
                r = 0
                while r < 10:
                    try:
                        html = fetch(url)
                        r = 10
                    except:
                        r = r + 1
                html = fetch(url)
                # entity
                try:
                    #
                    c = html.find(id='SharePriceAsOf1')['value']
                    c = c.replace(c.split(' ')[3],'')
                    c = c.replace(',  p.m.','')
                    c = c.replace(',  a.m.','')
                    month = re.sub(r"[^a-zA-Z()]", "", c)
                    year = c.replace(month, '')[-4:]
                    day = c.replace(month, '').replace(year, '').replace('. ', '').replace(', ', '').replace(' ', '')
                    try:
                        if (month == 'Jan'):
                            month = 1
                        if (month == 'Feb'):
                            month = 2
                        if (month == 'Mar'):
                            month = 3
                        if (month == 'March'):
                            month = 3
                        if (month == 'April'):
                            month = 4
                        if (month == 'May'):
                            month = 5
                        if (month == 'Jun'):
                            month = 6
                        if (month == 'June'):
                            month = 6
                        if (month == 'Jul'):
                            month = 7
                        if (month == 'July'):
                            month = 7
                        if (month == 'Aug'):
                            month = 8
                        if (month == 'Sept'):
                            month = 9
                        if (month == 'Oct'):
                            month = 10
                        if (month == 'Nov'):
                            month = 11
                        if (month == 'Dec'):
                            month = 12
                    except:
                        pass
                    c = datetime.datetime(year=int(year), month=int(month), day=int(day))
                    e.SecuritiesUpdate = c
                    #
                    e.save()
                except:
                    pass
                # stage
                try:
                    e.db = 1
                except:
                    pass
                # Time Of Update
                try:
                    now = datetime.datetime.now()
                    e.SEC_Update = now
                except:
                    pass
                print(ts)
                print(now)
                print(137*'-' + '\n')
                e.save()
        except:
            pass
    i = i + 1




