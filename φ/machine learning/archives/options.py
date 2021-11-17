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

# variables
try:
    #
    #
    entities = Entity.objects.all()
    #
    Audited = Phase.objects.get(db=21)
    #
    Capitalizations = Capitalization.objects.all().order_by('-db')
    #
    Industries = Industry.objects.all().order_by('Description')
    #
    PeriodEndDates = PeriodEndDate.objects.all().order_by('-db')
    #
    Phases = Phase.objects.all().order_by('-db')
    #
    Regions = Region.objects.all().order_by('Desctription').exclude(Len=0)
    #
    #
except:
    pass

# index options
try:
    #
    #
    for i in range(0, len(Industries)):
        i = Industries[i]
        print('<option value=' + str(i.db) + '>' + str(i.Description) + '</option>')
    #
    print('\n')
except:
    pass

