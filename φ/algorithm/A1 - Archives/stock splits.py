# Libraries
from φ.models import *
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import date
from io import StringIO
from urllib.request import urlopen
import collections
import csv
import glob
import html5lib
import os
import pandas as pd
import pathlib
import requests
import urllib
import xml.etree.ElementTree as ET
# historical
# URL
# TradingSymbol and entity PROTOTYPE ONLY ############################################################################################################### 
TradingSymbol = 'AAPL'
e = Entity.objects.get(TradingSymbol=TradingSymbol)
############################################################################################################### 
historicalurlfile = 'https://query1.finance.yahoo.com/v7/finance/download/' + TradingSymbol + '?period1=345427200&period2=9999999999&interval=1d&events=split&includeAdjustedClose=true'
response = requests.get(historicalurlfile)
historicalsplits = TradingSymbol + '_splits'
# Range
stockpricedates = [
    e.secondlastyear,
    e.thirdlastyear,
    e.fourthlastyear,
]
# Loop
for stockpricedate in stockpricedates:
    # Date String to be converted
    month = stockpricedate.split(',')[0]
    # Month numeric value
    if month[:7] == 'January':
        month = 1
    elif month[:2] == 'February':
        month = 2
    elif month[:5] == 'March':
        month = 3
    elif month[:5] == 'April':
        month = 4
    elif month[:6] == 'May':
        month = 5
    elif month[:4] == 'June':
        month = 6
    elif month[:4] == 'July':
        month = 7
    elif month[:6] == 'August':
        month = 8
    elif month[:9] == 'September':
        month = 9
    elif month[:7] == 'October':
        month = 10
    elif month[:8] == 'November':
        month = 11
    elif month[:8] == 'December':
        month = 12
    # day numeric value
    day = int(stockpricedate.split(',')[0][-2:])
    # year numeric value
    year = int(stockpricedate.split(',')[1].replace(' ', ''))
    if stockpricedate == stockpricedates[0]:
        datecolumn1 = date(year, month, day)
    if stockpricedate == stockpricedates[1]:
        datecolumn2 = date(year, month, day)
    if stockpricedate == stockpricedates[2]:
        datecolumn3 = date(year, month, day)
    if stockpricedate == stockpricedates[3]:
        datecolumn4 = date(year, month, day)
    if stockpricedate == stockpricedates[4]:
        datecolumn5 = date(year, month, day)

# Downloading and saving CSV file
with open('./φ/algorithm/stockssplits/' + historicalsplits + '.csv', 'w') as f:
    writer = csv.writer(f)
    for line in response.iter_lines():
        data = line.decode('utf-8').split(',')
        writer.writerow(data)

# path to csv file
path = './φ/algorithm/stockssplits/' +  historicalsplits + '.csv'
file = open(path, newline='')
reader = csv.reader(file)

# header
header = next(reader)

# Print
i = 1
ii = 1
iii = 1
iv = 1
v = 1
vi = 1

for row in reader:
    try:
        # Row date
        checkdate = datetime.strptime(row[0], '%Y-%m-%d')
        checkdate = date(checkdate.year, checkdate.month, checkdate.day)
        # Delta
        delta1 = checkdate - datecolumn1
        delta2 = checkdate - datecolumn2
        delta3 = checkdate - datecolumn3
        delta4 = checkdate - datecolumn4
        delta5 = checkdate - datecolumn5
        # Is it New Year?
        if delta1.days > 0:
            a = int(row[1].split(':')[0])/int(row[1].split(':')[1])
            i = i * a
        else:
            pass
        if delta2.days > 0:
            a = int(row[1].split(':')[0])/int(row[1].split(':')[1])
            ii = ii * a
        else:
            pass
        if delta3.days > 0:
            a = int(row[1].split(':')[0])/int(row[1].split(':')[1])
            iii = iii * a
        else:
            pass
        if delta4.days > 0:
            a = int(row[1].split(':')[0])/int(row[1].split(':')[1])
            iv = iv * a
        else:
            pass
        if delta5.days > 0:
            a = int(row[1].split(':')[0])/int(row[1].split(':')[1])
            v = v * a
        else:
            pass
    except:
        pass

print(i)
print(ii)
print(iii)
print(iv)
print(v)

