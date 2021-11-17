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

entities = Entity.objects.all().order_by(
    'TradingSymbol', 
    'EntityRegistrantName'
)

ll = 1
ll = len(entities)

#
# clear layout file
try:
    f = glob.glob('A:/clock/φ/algorithm/layout/layout.txt')
    if f != []:
        os.remove(f)
except:
    pass

with open('./φ/algorithm/layout/' + 'layout.txt', 'w') as layout:

    # entities
    for count in range(0, ll):
        #
        e = entities[count]
        #
        if ll == 1:
            e = Entity.objects.get(TradingSymbol='AAPL')
        #
        phases = [
            'Phase Audited',
            'Phase Prepared',
            'Phase 8',
            'Phase 7.8',
            'Phase 7.7',
            'Phase 7.6',
            'Phase 7.5',
            'Phase 7.4',
            'Phase 7.3',
            'Phase 7.2',
            'Phase 7.1',
        ]
        #
        # layout
        if e.Status in phases:
            #
            # entity
            print('\n' + 137 * '-' + '\n' + str(e) + ', ' + str(round(count/ll * 1000) / 10) + '%\n' + 137 * '-' + '\n')
            #
            layout.write("{ name: '" + e.EntityRegistrantName.replace("'", "`") + " (" + e.TradingSymbol + ")' , url: './" + e.TradingSymbol + "'}, \n")



