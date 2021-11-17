#
# Libraries
from φ.models import *
from bs4 import BeautifulSoup
from io import StringIO
from datetime import datetime, date
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import QAbstractTableModel, Qt
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

marketdata = [
    '20',
    '19',
    '18',
    '17',
    '16',
    '15',
    '14',
    '13',
    '12',
    '11',
]

phases = [
    '20',
    '19',
    '18',
    '17',
    '16',
    '15',
    '14',
    '13',
    '12',
    '11',
]

API = {
    'access_key': 'ecae621d4718099f0d660a237c429450',
}

# variables
try:
    #
    entities = Entity.objects.all().order_by(
        '-db',
        'AnomaliesRatio1',
        'AnomaliesRatio2',
        'AnomaliesRatio3',
        'AnomaliesRatio4',
        'AnomaliesRatio5',
        'AnomaliesRatio6',
        '-lastyear',
        'TradingSymbol',
    )
    Audited = Entity.objects.all().filter(db=21)
    #
    Capitalizations = Capitalization.objects.all().order_by('db')
    #
    Industries = Industry.objects.all().order_by('Description').exclude(Len=0)
    #
    PeriodEndDates = PeriodEndDate.objects.all().order_by('-db')
    #
    Phases = Phase.objects.all().order_by('-db')
    #
    Regions = Region.objects.all().order_by('Description').exclude(Len=0)
    #
except:
    pass

# master
try:
    #
    try:
        m = Master.objects.all()[0]
    except:
        m = Master()
    #
    m.entities = len(entities)
    m.audited = len(Audited)
    m.capitalizations = len(Capitalizations)
    m.industries = len(Industries)
    m.regions = len(Regions)
    #
    m.save()
    #
    print(str(m.entities) + ' entities')
    print(str(m.audited) + ' audited')
    print(str(m.capitalizations) + ' capitalizations')
    print(str(m.industries) + ' industries')
    print(str(m.regions) + ' regions')
except:
    pass


