#
# Libraries
from φ.models import *
from bs4 import BeautifulSoup
from io import StringIO
from datetime import datetime, date
from django.contrib.auth.models import User
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
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

entities = Entity.objects.all().order_by(
    '-db',
    '-NumberOfYearsAudited',
    '-AnomaliesRatio1',
    '-AnomaliesRatio2',
    '-AnomaliesRatio3',
    '-AnomaliesRatio4',
    '-AnomaliesRatio5',
    '-AnomaliesRatio6',
    '-lastyear',
    'TradingSymbol',
)

ll = 1
ll = len(entities)

driver = webdriver.Firefox(executable_path=r'C:\\Program Files\\geckodriver.exe')

base_url = 'http://127.0.0.1:8000/'

driver.get(base_url)

try:
    link = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, "email"))
    )
    email = driver.find_element_by_id("inputEmail")
    password = driver.find_element_by_id("inputPassword")
    login = driver.find_element_by_id("Login")
    email.send_keys('clockdb@gmail.com')
    password.send_keys('Astromind101$')
    login.click()
except:
    pass

time.sleep(10)

# master
try:
    #
    # entities
    for count in range(0, ll):
        #
        e = entities[count]
        #
        if ll == 1:
            e = Entity.objects.get(TradingSymbol='FNMFO')
        #
        #
        # entity
        print('\n' + 137 * '-' + '\n' + e.EntityRegistrantName + ' (' + e.TradingSymbol + ')' + ', ' + str(round(count/ll * 1000) / 10) + '%\n')
        print('\n' + 'Phase ' + str(e.db) + ', number of year audited: ' + str(e.NumberOfYearsAudited) + '\n' + 137 * '-' + '\n')
        #
        # web application
        try:
            #
            url = base_url + '67/WorkingPaper/' + e.TradingSymbol + '/Opinion/'
            driver.get(url)
            #
            # anomalies ratio
            try:
                bb = [
                    'AnomaliesRatio1',
                    'AnomaliesRatio2',
                    'AnomaliesRatio3',
                    'AnomaliesRatio4',
                    'AnomaliesRatio5',
                    'AnomaliesRatio6',
                ]
                dd = [
                    '%',
                    ',',
                ]
                qq = [
                    '∞',
                    'NaN',
                ]
                #
                cc = []
                #
                for b in bb:
                    c = driver.find_element_by_id(b).get_attribute('value')
                    for d in dd:
                        try:
                            c = c.replace(d,'')
                        except:
                            pass
                    for q in qq:
                        try:
                            c = c.replace(q,'999999')
                        except:
                            pass
                    c = int(c)
                    c = c / 100
                    cc.append(c)
                #
                pprint.pprint(cc)
                #
                ea = 0
                i = 0
                lt = 0
                #
                for c in cc:
                    #
                    # last year
                    if i == 0:
                        e.AnomaliesRatio1 = c
                        a = AuditData.objects.get(TradingSymbol=e.TradingSymbol, Period='lastyear')
                    #
                    # second last year
                    if i == 1:
                        e.AnomaliesRatio2 = c
                        a = AuditData.objects.get(TradingSymbol=e.TradingSymbol, Period='secondlastyear')
                    #
                    # third last year
                    if i == 2:
                        e.AnomaliesRatio3 = c
                        a = AuditData.objects.get(TradingSymbol=e.TradingSymbol, Period='thirdlastyear')
                    #
                    # fourth last year
                    if i == 3:
                        e.AnomaliesRatio4 = c
                        a = AuditData.objects.get(TradingSymbol=e.TradingSymbol, Period='fourthlastyear')
                    #
                    # fifth last year
                    if i == 4:
                        e.AnomaliesRatio5 = c
                        a = AuditData.objects.get(TradingSymbol=e.TradingSymbol, Period='fifthlastyear')
                    #
                    # sixth last year
                    if i == 5:
                        e.AnomaliesRatio6 = c
                        a = AuditData.objects.get(TradingSymbol=e.TradingSymbol, Period='sixthlastyear')
                    #
                    #
                    a.db = 0
                    if c < 1:
                        if a.Sales != 0:
                            if a.NetIncome != 0:
                                if a.Assets != 0:
                                    a.db = 20
                                    lt = lt + 1
                        if a.AmendmentFlag == 'Amend':
                            if a.Sales == 0:
                                if a.NetIncome == 0:
                                    if a.Assets == 0:
                                        lt = lt + 1
                                        ea = ea + 1
                        a.save()
                    #
                    i = i + 1
                #
            except:
                pass
            #
            # clock, intrinsic value, market capitalization, bridge and opinion to db.
            try:
                #
                aa = [
                    'Bridgeφ1',
                    'Bridgeφ2',
                    'Bridgeφ3',
                    'Bridgeφ4',
                    'Opinionφ1',
                    'Opinionφ2',
                    'Opinionφ3',
                    'Opinionφ4',
                    'Clockφ1',
                    'Clockφ2',
                    'Clockφ3',
                    'Clockφ4',
                    'IntrinsicValues1',
                    'IntrinsicValues2',
                    'IntrinsicValues3',
                    'IntrinsicValues4',
                    'IntrinsicValueOfACommonShares1',
                    'IntrinsicValueOfACommonShares2',
                    'IntrinsicValueOfACommonShares3',
                    'IntrinsicValueOfACommonShares4',
                    'MarketCapitalization1',
                    'MarketCapitalization2',
                    'MarketCapitalization3',
                    'MarketCapitalization4',
                    'SharePrice1',
                    'SharePrice2',
                    'SharePrice3',
                    'SharePrice4',
                    'CommonSharesOutstanding1',
                    'CommonSharesOutstanding2',
                    'CommonSharesOutstanding3',
                    'CommonSharesOutstanding4',
                ]
                #
                dd = [
                    ',',
                ]
                qq = [
                    '∞',
                    'NaN',
                ]
                i = 0
                for a in aa:
                    g = driver.find_element_by_id(a)
                    c = g.get_attribute('innerHTML')
                    if c == '':
                        c = g.get_attribute('value')
                    w = ''
                    if i > 7:
                        #
                        for d in dd:
                            try:
                                c = c.replace(d,'')
                            except:
                                pass
                        #
                        for q in qq:
                            try:
                                if q in c:
                                    c = None
                            except:
                                pass
                        #
                        try:
                            if '%' in c:
                                c = float(int(c.replace('%','')))
                        except:
                            pass
                        #
                        try:
                            c = float(c)
                        except:
                            pass
                    #
                    if a == aa[0]:
                        e.BridgeφLastYear = c
                    if a == aa[1]:
                        e.BridgeφSecondLastYear = c
                    if a == aa[2]:
                        e.BridgeφThirdLastYear = c
                    if a == aa[3]:
                        e.BridgeφFourthLastYear = c
                    #
                    if a == aa[4]:
                        e.OpinionφLastYear = c
                    if a == aa[5]:
                        e.OpinionφSecondLastYear = c
                    if a == aa[6]:
                        e.OpinionφThirdLastYear = c
                    if a == aa[7]:
                        e.OpinionφFourthLastYear = c
                    #
                    if a == aa[8]:
                        e.ClockφLastYear = c
                    if a == aa[9]:
                        e.ClockφSecondLastYear = c
                    if a == aa[10]:
                        e.ClockφThirdLastYear = c
                    if a == aa[11]:
                        e.ClockφFourthLastYear = c
                    #
                    if a == aa[12]:
                        e.CommonSharesIntrinsicValueLastYear = c
                    if a == aa[13]:
                        e.CommonSharesIntrinsicValueSecondLastYear = c
                    if a == aa[14]:
                        e.CommonSharesIntrinsicValueThirdLastYear = c
                    if a == aa[15]:
                        e.CommonSharesIntrinsicValueFourthLastYear = c
                    #
                    if a == aa[16]:
                        e.CommonShareIntrinsicValueLastYear = c
                    if a == aa[17]:
                        e.CommonShareIntrinsicValueSecondLastYear = c
                    if a == aa[18]:
                        e.CommonShareIntrinsicValueThirdLastYear = c
                    if a == aa[19]:
                        e.CommonShareIntrinsicValueFourthLastYear = c
                    #
                    if a == aa[20]:
                        e.MarketCapitalizationLastYear = c
                    if a == aa[21]:
                        e.MarketCapitalizationSecondLastYear = c
                    if a == aa[22]:
                        e.MarketCapitalizationThirdLastYear = c
                    if a == aa[23]:
                        e.MarketCapitalizationFourthLastYear = c
                    #
                    if a == aa[24]:
                        e.CommonSharePriceLastYear = c
                    if a == aa[25]:
                        e.CommonSharePriceSecondLastYear = c
                    if a == aa[26]:
                        e.CommonSharePriceThirdLastYear = c
                    if a == aa[27]:
                        e.CommonSharePriceFourthLastYear = c
                    #
                    if a == aa[28]:
                        e.CommonSharesOutstandingLastYear = c
                    if a == aa[29]:
                        e.CommonSharesOutstandingSecondLastYear = c
                    if a == aa[30]:
                        e.CommonSharesOutstandingThirdLastYear = c
                    if a == aa[31]:
                        e.CommonSharesOutstandingFourthLastYear = c
                    #
                    i = i + 1
            except:
                pass
        except:
            pass
        #
        # save entity
        try:
            e.save()
            print('\n' + 137 * '-' + '\n' + e.EntityRegistrantName + ' (' + e.TradingSymbol + ')' + ', ' + str(round(count/ll * 1000) / 10) + '%\n')
            print('\n' + e.db + ', ' + str(e.NumberOfYearsAudited) + '\n' + 137 * '-' + '\n')
        except:
            pass
except:
    pass


