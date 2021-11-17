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

try:
    entities = Entity.objects.all()
    l_entities = len(entities)
    #
    Capitalizations = Capitalization.objects.all().order_by('db')
    l_Capitalizations = len(Capitalizations)
    #
    Industries = Industry.objects.all()
    l_Industries = len(Industries)
    #
    Phases = Phase.objects.all()
    l_Phases = len(Phases)
    #
    Regions = Region.objects.all()
    l_Regions = len(Regions)
except:
    pass

for count in range(0, l_entities):
    #
    e = entities[count]
    #
    for i in range(0, l_Capitalizations):
        #
        r = Capitalizations[i]
        #
        c = e.MarketCapitalization
        #
        if c > r.dbp:
            e.Capitalization_db = r.db
    #
    e.save()
