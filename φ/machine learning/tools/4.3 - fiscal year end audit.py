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

now = datetime.datetime.now()

l = 1

l = len(entities)

# counter
for count in range(0, l):
    try:
        #
        e = entities[count]
        #
        if e.Status == 'Phase4.3':
            #
            print(e)
            print(137*'-')
            #
            a = e.lastyear - e.secondlastyear
            a = a.days
            if a > 0:
                #
                a = e.secondlastyear - e.thirdlastyear
                a = a.days
                if a > 0:
                    #
                    a = e.thirdlastyear - e.fourthlastyear
                    a = a.days
                    if a > 0:
                        #
                        z = datetime.datetime(int(e.lastyear.year), int(e.lastyear.month), int(e.lastyear.day))
                        if e.fifthlastyear is None:
                            if e.sixthlastyear is None:
                                if (now - z).days < 420:
                                    e.Status = 'Phase5'
                                else:
                                    if (now - z).days > 540:
                                        e.Status = 'Inactive'
                        else:
                            a = e.fourthlastyear - e.fifthlastyear
                            a = a.days
                            if a > 0:
                                #
                                if e.sixthlastyear is None:
                                    if (now - z).days < 420:
                                        e.Status = 'Phase5'
                                    else:
                                        if (now - z).days > 540:
                                            e.Status = 'Inactive'
                                else:
                                    a = e.fifthlastyear - e.sixthlastyear
                                    a = a.days
                                    if a > 0:
                                        if (now - z).days < 420:
                                            e.Status = 'Phase5'
                                        else:
                                            if (now - z).days > 540:
                                                e.Status = 'Inactive'
            #
            # Time Of Update
            e.Update = now
            #
            e.save()
            #
    except:
        pass







