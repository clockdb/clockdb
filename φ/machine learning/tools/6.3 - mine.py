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
entities = Entity.objects.all().order_by('-lastyear', 'TradingSymbol')

#l = 1
l = len(entities)

phases = [
    'Phase6.3',
]

driver = webdriver.Chrome('C:\\Program Files (x86)\\chromedriver.exe')

# counter
for count in range(0, l):
    #
    # retreives entity from db
    try:
        #
        #e = Entity.objects.get(TradingSymbol='A')
        e = entities[count]
        #
        if e.Status in phases:
            #
            # entity
            print('\n' + str(e) + '\n' + 137*'-' + '\n')
            #
            # urls
            urls = [
                e.urlbalancesheetlastyear,
                e.urlbalancesheetsecondlastyear,
                e.urlbalancesheetthirdlastyear,
                e.urlbalancesheetfourthlastyear,
                e.urlbalancesheetfifthlastyear,
                e.urlbalancesheetsixthlastyear,
                #
                e.urlincomestatementlastyear,
                e.urlincomestatementsecondlastyear,
                e.urlincomestatementthirdlastyear,
                e.urlincomestatementfourthlastyear,
                e.urlincomestatementfifthlastyear,
                e.urlincomestatementsixthlastyear,
                #
                e.urlcomprehensiveincomelastyear,
                e.urlcomprehensiveincomesecondlastyear,
                e.urlcomprehensiveincomethirdlastyear,
                e.urlcomprehensiveincomefourthlastyear,
                e.urlcomprehensiveincomefifthlastyear,
                e.urlcomprehensiveincomesixthlastyear,
                #
                e.urlstockholdersequitylastyear,
                e.urlstockholdersequitysecondlastyear,
                e.urlstockholdersequitythirdlastyear,
                e.urlstockholdersequityfourthlastyear,
                e.urlstockholdersequityfifthlastyear,
                e.urlstockholdersequitysixthlastyear,
                #
                e.urlcashflowlastyear,
                e.urlcashflowsecondlastyear,
                e.urlcashflowthirdlastyear,
                e.urlcashflowfourthlastyear,
                e.urlcashflowfifthlastyear,
                e.urlcashflowsixthlastyear,
            ]
            #
            # url loop
            u = 0
            for url in urls:
                try:
                    #
                    driver.get(url)
                    #
                    filename = url[-25:][:18]
                    #
                    if u < 6 :
                        statement = 'bs'
                    elif u < 12:
                        statement = 'is'
                    elif u < 18:
                        statement = 'ci'
                    elif u < 24:
                        statement = 'se'
                    elif u < 30:
                        statement = 'cf'
                    else:
                        pass
                    #
                    path = 'mine/' + filename + '-' + statement + '.html'
                    #
                    print(path)
                    #
                    with open(path, 'w+') as f:
                        f.write(driver.page_source)
                        f.close()
                    #
                    time.sleep(1)
                    #
                except:
                    pass
                #
                u = u + 1
            #
            # Status
            if e.Status == 'Phase6.3':
                e.Status = 'Phase7'
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
            #
            print(137*'-')
    except:
        pass



