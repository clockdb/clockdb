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


#
# db
try:
    # variables
    try:
        entities = Entity.objects.all()
        Audited = Entity.objects.all().filter(db=21)
        Prepared = Entity.objects.all().filter(db=20)
        MarketAndSecuritiesPhase = Entity.objects.all().filter(db=19)
        SixYearAudited = Entity.objects.all().filter(db=18)
        FiveYearAudited = Entity.objects.all().filter(db=17)
        FourYearAudited = Entity.objects.all().filter(db=16)
        ThreeYearAudited = Entity.objects.all().filter(db=15)
        TwoYearAudited = Entity.objects.all().filter(db=14)
        OneYearAudited = Entity.objects.all().filter(db=13)
        #
        Capitalizations = Capitalization.objects.all().order_by('db')
        #
        Industries = Industry.objects.all().order_by('Description')
        #
        Intrinsics = Intrinsic.objects.all().order_by('db')
        #
        PeriodEndDates = PeriodEndDate.objects.all().order_by('-db')
        #
        Phases = Phase.objects.all().order_by('-db')
        #
        Regions = Region.objects.all().order_by('Description')
        #
    except:
        pass
    #
    # phases
    for i in range(0, len(Phases)):
        try:
            r = Phases[i]
            r.Len = len(Entity.objects.all().filter(db=r.db))
            r.save()
        except:
            pass
    #
    # progress
    try:
        progress = [
            len(Audited),
            len(Prepared),
            len(MarketAndSecuritiesPhase),
            len(SixYearAudited),
            len(FiveYearAudited) * 5/6,
            len(FourYearAudited) * 4/6,
            len(ThreeYearAudited) * 3/6,
            len(TwoYearAudited) * 2/6,
            len(OneYearAudited) * 1/6,
        ]
        eq = sum(progress)
        progress = round(eq / len(entities) * 1000) / 10
        #
        onboarded = [
            len(Audited),
            len(Prepared),
            len(MarketAndSecuritiesPhase),
            len(SixYearAudited),
            len(FiveYearAudited),
            len(FourYearAudited),
            len(ThreeYearAudited),
            len(TwoYearAudited),
            len(OneYearAudited),
        ]
    except:
        pass
    #
    # master
    try:
        #
        m = Master.objects.all()[0]
        #
        m.entities = len(entities)
        m.audited = len(Audited)
        m.onboarded = sum(onboarded)
        m.eq = eq
        m.progress = progress
        #
        m.save()
    except:
        pass
except:
    pass




