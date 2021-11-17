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
 
#
# scope
scopedperiods = [
    'lastyear',
    'secondlastyear',
    'thirdlastyear',
    'fourthlastyear',
    'fifthlastyear',
    'sixthlastyear',
]

entities = Entity.objects.all().order_by('EntityRegistrantName')

l = 1

l = len(entities)

# counter
for count in range(0, l):
    #
    e = entities[count]
    #
    if e.Status == 'Phase3':
        #
        ts = e.TradingSymbol
        #
        print(137*'-' + '\n' + e.EntityRegistrantName + ' (' + ts + ') \n')
        #
        # data gathering
        for scopedperiod in scopedperiods:
            #
            d = scopedperiod
            #
            # trial balance
            try:
                tb = TrialBalance.objects.get(TradingSymbol=ts, Period=d)
            except:
                try:
                    tb = TrialBalance(TradingSymbol=ts, Period=d)
                    tb.save()
                except:
                    pass
            #
            # cash flow
            try:
                cf = CashFlow.objects.get(TradingSymbol=ts, Period=d)
            except:
                try:
                    cf = CashFlow(TradingSymbol=ts, Period=d)
                    cf.save()
                except:
                    pass
            #
            # audit
            try:
                a = AuditData.objects.get(TradingSymbol=ts, Period=d)
            except:
                try:
                    a = AuditData(TradingSymbol=ts, Period=d)
                    a.save()
                except:
                    pass
        #
        # status
        e.Status = 'Phase4.1'
        #
        # Time Of Update
        try:
            now = datetime.datetime.now()
            e.Update = now
        except:
            pass
        #
        e.save()



