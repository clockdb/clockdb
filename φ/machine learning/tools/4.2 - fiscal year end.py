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

# BeautifulSoup parser
def fetch(url):
    thepage = urllib.request.urlopen(url)
    soupdata = BeautifulSoup(thepage,"html.parser")
    return soupdata

# loop
entities = Entity.objects.all().order_by('TradingSymbol')

print(137*'-')

l = 1

l = len(entities)

# counter
for count in range(0, l):
    #
    # retreives entity from db
    try:
        #
        e = entities[count]
        #
        if e.Status == 'Phase4.2':
            #
            print(str(e) + '\n' + 137*'-')
            #
            # accession numbers and periods dictionnairies
            try:
                accs = [
                    e.accessionnumberlastyear,
                    e.accessionnumbersecondlastyear,
                    e.accessionnumberthirdlastyear,
                    e.accessionnumberfourthlastyear,
                    e.accessionnumberfifthlastyear,
                    e.accessionnumbersixthlastyear,
                    e.accessionnumberseventhlastyear,
                ]
            except:
                pass
            #
            # retreives periods from accession numbers
            for acc in accs:
                try:
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
                    # saves data
                    try:
                        if acc == accs[0]:
                            e.lastyear = d
                        if acc == accs[1]:
                            e.secondlastyear = d
                        if acc == accs[2]:
                            e.thirdlastyear = d
                        if acc == accs[3]:
                            e.fourthlastyear = d
                        if acc == accs[4]:
                            e.fifthlastyear = d
                        if acc == accs[5]:
                            e.sixthlastyear = d
                        if acc == accs[6]:
                            e.seventhlastyear = d
                    except:
                        pass
                except:
                    pass
            #
            # Time Of Update
            try:
                now = datetime.datetime.now()
                e.Update = now
            except:
                pass
            #
            # update status
            if e.lastyear != None:
                if e.secondlastyear != None:
                    if e.thirdlastyear != None:
                        if e.fourthlastyear != None:
                            e.Status = 'Phase4.3'
            #
            # save entity
            e.save()
    except:
        pass

