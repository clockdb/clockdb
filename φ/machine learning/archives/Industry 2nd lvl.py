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

def append_value(dict_obj, key, value):
    # Check if key exist in dict or not
    if key in dict_obj:
        dict_obj[key] = value
    else:
        dict_obj[key] = value

entities = Entity.objects.all().order_by('Industry_SEC')

Industries_match = {}

Industries_names = {}

Industries_sub = {}

priorvalue = 0

for count in range(0, len(entities)):
    #
    e = entities[count]
    #
    i = e.Industry_SEC_db
    #
    u = e.Industry_db
    #
    d = e.Industry
    #
    c = e.Industry_SEC
    #
    if i not in Industries_match:
        #
        append_value(Industries_match, i, u)
        #
        append_value(Industries_names, u, d)
        #
        append_value(Industries_sub, c, i)
        #

n = 0

while n < 100:
    #
    for i in Industries_match:
        #
        value = Industries_match[i]
        #
        if value == n:
            #
            for u in Industries_names:
                #
                if u == n :
                    #
                    v = Industries_names[u]
                    #
                    if value != priorvalue:
                        print("                        </select>")
                        print("                    </form>")
                        print("                </td>")
                        print("            </tr>")
                        #
                        c = '            <tr id=' + str(value) + 'row style="display:none;" class="industry">'
                        print(c)
                        #
                        print("                <td colspan='2'></td>")
                        print("                <td colspan='4'>")
                        print("                    <form>")
                        c = '                        <select id=' + str(value) + ' name=' + '"' + str(v) + '"' + '>'
                        print(c)
                        #
                        print("                            <option value=any selected></option>")
                    #
                    for g in Industries_sub:
                        #
                        m = Industries_sub[g]
                        #
                        try:
                            #
                            if m == i:
                                #
                                print('                            <option value=' + str(i) + '>' + str(g) + '</option>')    
                        except:
                            pass
                    #
                    priorvalue = value
    #
    n = n + 1


