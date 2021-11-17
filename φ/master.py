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

def append_value(dict_obj, key, value):
    # Check if key exist in dict or not
    if key in dict_obj:
        dict_obj[key] = value
    else:
        dict_obj[key] = value

API = {
    'access_key': 'ecae621d4718099f0d660a237c429450',
}

# Machine Learning
try:
    CurrentAssetsGL = []
    NonCurrentAssetsGL = []
    CurrentLiabilitiesGL = []
    NonCurrentLiabilitiesGL = []
    ShareholdersEquityBalanceGL = []
    GrossMarginGL = []
    OperatingExpensesGL = []
    OperatingIncomeGL = []
    IncomeBeforeTaxesGL = []
    NetIncomeGL = []
    OtherComprehensiveIncomeGL = []
    ShareholdersEquityGL = []
    OperatingActivitiesGL = []
    InvestingActivitiesGL = []
    FinancingActivitiesGL = []
except:
    pass

RegularExpressions = [
    'AndAdditional',
    'AtJanuary',
    'AuthorizedShares',
    'AndJanuary',
    'AndOutstanding',
    'AndPaidInCapital',
    'AndAdditionalPaidInCapital',
    'ParValue',
    'SharesAuthorized',
    'SharesIssued'
    'Respectively',
    'OfParValue',
    'OutstandingAt',
    'AtDecember',
    'AndDecember',
    'SharesAnd',
    'AndIssued',
    'OfAt',
    'MarchAnd',
    'AtMarch',
    'IssuedShare',
    'AndMarch',
    'InAndIssued',
    'SharesInAndIn',
    'OutstandingShares',
    'InAndIn',
    'InAndNone',
    'IssuedAndOutstanding',
    'PerShare',
    'AtSeptember',
    'AndSeptember',
    'NetOfAccumulatedAmortization',
    'AsOfDecember',
    '()',
]

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

auditcompleted = [
    21,
]

marketdata = [
]

phases = [
    21,
    20,
    19,
    18,
    17,
    16,
    15,
    14,
    13,
    12,
    11,
    10,
    9,
    8,
    7,
    6,
    5,
    4,
    3,
    2,
    1,
]

ll = len(entities)
ll = 1

# master
try:
    #
    # entities
    for count in range(0, ll):
        #
        e = entities[count]
        #
        if ll == 1:
            e = Entity.objects.get(TradingSymbol='FB')
        #
        if e.db in phases:
            #
            # entity
            print('\n' + 137 * '-' + '\n' + e.EntityRegistrantName + ' (' + e.TradingSymbol + ')' + ', ' + str(round(count/ll * 1000) / 10) + '%\n')
            print('\n' + 'Phase ' + str(e.db) + ', number of year audited: ' + str(e.NumberOfYearsAudited) + '\n' + 137 * '-' + '\n')
            #
            # dates and accession numbers
            try:
                periodenddates = [
                    e.lastyear,
                    e.secondlastyear,
                    e.thirdlastyear,
                    e.fourthlastyear,
                    e.fifthlastyear,
                    e.sixthlastyear,
                ]
                accs = [
                    e.accessionnumberlastyear,
                    e.accessionnumbersecondlastyear,
                    e.accessionnumberthirdlastyear,
                    e.accessionnumberfourthlastyear,
                    e.accessionnumberfifthlastyear,
                    e.accessionnumbersixthlastyear,
                ]
            except:
                pass
            #
            # financial statements
            try:
                #
                periodenddates.sort(reverse=True)
                #
                for periodenddate in periodenddates:
                    #
                    if periodenddate != None:
                        #
                        a = AuditData.objects.get(TradingSymbol=e.TradingSymbol, PeriodEndDate=periodenddate)
                        #
                        if a.db not in auditcompleted:
                            #
                            a.db = 0
                            #
                            # period end dates to accession numbers
                            try:
                                if periodenddate == periodenddates[0]:
                                    acc = accs[0]
                                    amend = e.amendlastyear
                                    period = 'last year'
                                #
                                if periodenddate == periodenddates[1]:
                                    acc = accs[1]
                                    amend = e.amendsecondlastyear
                                    period = 'second last year'
                                #
                                if periodenddate == periodenddates[2]:
                                    acc = accs[2]
                                    amend = e.amendthirdlastyear
                                    period = 'third last year'
                                #
                                if periodenddate == periodenddates[3]:
                                    acc = accs[3]
                                    amend = e.amendfourthlastyear
                                    period = 'fourth last year'
                                #
                                if periodenddate == periodenddates[4]:
                                    acc = accs[4]
                                    amend = e.amendfifthlastyear
                                    period = 'fifth last year'
                                #
                                if periodenddate == periodenddates[5]:
                                    acc = accs[5]
                                    amend = e.amendsixthlastyear
                                    period = 'sixth last year'
                                #
                                print(str(periodenddate) + ' (' + period + ') \n')
                                print(acc + '\n')
                                #
                            except:
                                pass
                            #
                            # statements directories
                            try:
                                mine = 'A:/venv/src/φ/mine/'
                                #
                                accn = acc.replace('-','')
                                #
                                BS = mine + accn + '-bs.html'
                                IS = mine + accn + '-is.html'
                                CI = mine + accn + '-ci.html'
                                SE = mine + accn +  '-se.html'
                                CF = mine + accn + '-cf.html'
                                #
                                statements = {
                                    BS: 'Balance Sheet',
                                    IS: 'Income Statement',
                                    CI: 'Comprehensive Income Statement',
                                    SE: 'Shareholders Equity Statement',
                                    CF: 'Cashflow Statement',
                                }
                                #
                                pprint.pprint(statements)
                            except:
                                pass
                            #
                            # statements dictionaries
                            try:
                                BalanceSheet = {}
                                IncomeStatement = {}
                                ComprehensiveIncomeStatement = {}
                                ShareholdersEquityStatement = {}
                                CashFlowStatement = {}
                            except:
                                pass
                            #
                            # statements data
                            for statement in statements:
                                try:
                                    #
                                    # variables
                                    try:
                                        dad = None
                                        statement_data = {}
                                        statement_data['headers'] = []
                                        statement_data['sections'] = []
                                        statement_data['data'] = []
                                    except:
                                        pass
                                    #
                                    # html
                                    m = None
                                    try:
                                        with open(statement, 'r') as f:
                                            m = f.read()
                                        #
                                        m = BeautifulSoup(m, 'html')
                                        #
                                        m = m.table.find_all('tr')
                                        #
                                    except:
                                        pass
                                    #
                                    # loop (rows)
                                    for index, row in enumerate(m):
                                        try:
                                            cols = row.find_all('td')
                                            #
                                            if (len(row.find_all('th')) == 0 and len(row.find_all('strong')) == 0):
                                                #
                                                t = [ele.text.strip() for ele in cols]
                                                #
                                                GL_SEC = t[0].lower().title()
                                                #
                                                GL = re.sub(r"[^a-zA-Z()]", "", GL_SEC)
                                                #
                                                if statement == SE:
                                                    #
                                                    ss = []
                                                    i = 1
                                                    #
                                                    for s in statement_data['headers'][0]:
                                                        #
                                                        f = s.lower().title()
                                                        #
                                                        f = re.sub(r"[^a-zA-Z()]", "", f)
                                                        #
                                                        for y in RegularExpressions:
                                                            f = f.replace(y,'')
                                                        #
                                                        ss.append(f)
                                                        #
                                                        i = i + 1
                                                    #
                                                    try:
                                                        GL_row1 = ''
                                                        GL_row2 = ''
                                                        GL_row3 = ''
                                                        GL_row4 = ''
                                                        GL_row5 = ''
                                                        GL_row6 = ''
                                                        GL_row7 = ''
                                                        GL_row8 = ''
                                                        GL_row9 = ''
                                                        #
                                                        GL_row1 = GL + ss[1]
                                                        GL_row2 = GL + ss[2]
                                                        GL_row3 = GL + ss[3]
                                                        GL_row4 = GL + ss[4]
                                                        GL_row5 = GL + ss[5]
                                                        GL_row6 = GL + ss[6]
                                                        GL_row7 = GL + ss[7]
                                                        GL_row8 = GL + ss[8]
                                                        GL_row9 = GL + ss[9]
                                                    except:
                                                        pass
                                                else:
                                                    for y in RegularExpressions:
                                                        GL = GL.replace(y,'')
                                                #
                                                # statement, currency, scale
                                                try:
                                                    #
                                                    #
                                                    f = [
                                                        ' SHARES IN MILLIONS',
                                                        ' SHARES IN THOUSANDS',
                                                        'UNLESS OTHERWISE SPECIFIED',
                                                        'EXCEPT SHARE DATA',
                                                        ', ',
                                                        ',',
                                                    ]
                                                    # dad
                                                    qd = statement_data['headers']
                                                    qb = qd[0][0].upper()
                                                    #
                                                    if dad is None:
                                                        #
                                                        for g in f:
                                                            qb = qb.replace(g, '')
                                                        #
                                                        print('\n' + 137 * '-' + '\n')
                                                        print(qb)
                                                        print(137 * '-' + '\n')
                                                        #
                                                        if qb[-11:] == 'IN MILLIONS':
                                                            #
                                                            dad = 1000000
                                                        #
                                                        elif qb[-12:] == 'IN THOUSANDS':
                                                            #
                                                            dad = 1000
                                                        #
                                                        else:
                                                            #
                                                            dad = 1
                                                except:
                                                    pass
                                                #
                                                # value
                                                try:
                                                    #
                                                    z = len(m[5].find_all('td'))
                                                    #
                                                    x = m[5].find_all('td')[1].text
                                                    #
                                                    if statement == SE:
                                                        #
                                                        try:
                                                            try:
                                                                value_row1 = 0
                                                                l = t[1]
                                                                if l == '':
                                                                    l = 0
                                                                w = 1
                                                                if '(' in l:
                                                                    w = -1
                                                                #
                                                                l = re.sub(r"[^.0123456789]", "", str(l))
                                                                l = float(l)
                                                                value_row1 = l * dad * w
                                                            except:
                                                                pass
                                                            try:
                                                                value_row2 = 0
                                                                l = t[2]
                                                                if l == '':
                                                                    l = 0
                                                                w = 1
                                                                if '(' in l:
                                                                    w = -1
                                                                #
                                                                l = re.sub(r"[^.0123456789]", "", str(l))
                                                                l = float(l)
                                                                value_row2 = l * dad * w
                                                            except:
                                                                pass
                                                            try:
                                                                value_row3 = 0
                                                                l = t[3]
                                                                if l == '':
                                                                    l = 0
                                                                w = 1
                                                                if '(' in l:
                                                                    w = -1
                                                                #
                                                                l = re.sub(r"[^.0123456789]", "", str(l))
                                                                l = float(l)
                                                                value_row3 = l * dad * w
                                                            except:
                                                                pass
                                                            try:
                                                                value_row4 = 0
                                                                l = t[4]
                                                                if l == '':
                                                                    l = 0
                                                                w = 1
                                                                if '(' in l:
                                                                    w = -1
                                                                #
                                                                l = re.sub(r"[^.0123456789]", "", str(l))
                                                                l = float(l)
                                                                value_row4 = l * dad * w
                                                            except:
                                                                pass
                                                            try:
                                                                value_row5 = 0
                                                                l = t[5]
                                                                if l == '':
                                                                    l = 0
                                                                w = 1
                                                                if '(' in l:
                                                                    w = -1
                                                                #
                                                                l = re.sub(r"[^.0123456789]", "", str(l))
                                                                l = float(l)
                                                                value_row4 = l * dad * w
                                                            except:
                                                                pass
                                                            try:
                                                                value_row6 = 0
                                                                l = t[6]
                                                                if l == '':
                                                                    l = 0
                                                                w = 1
                                                                if '(' in l:
                                                                    w = -1
                                                                #
                                                                l = re.sub(r"[^.0123456789]", "", str(l))
                                                                l = float(l)
                                                                value_row6 = l * dad * w
                                                            except:
                                                                pass
                                                            try:
                                                                value_row7 = 0
                                                                l = t[7]
                                                                if l == '':
                                                                    l = 0
                                                                w = 1
                                                                if '(' in l:
                                                                    w = -1
                                                                #
                                                                l = re.sub(r"[^.0123456789]", "", str(l))
                                                                l = float(l)
                                                                value_row7 = l * dad * w
                                                            except:
                                                                pass
                                                            try:
                                                                value_row8 = 0
                                                                l = t[8]
                                                                if l == '':
                                                                    l = 0
                                                                w = 1
                                                                if '(' in l:
                                                                    w = -1
                                                                #
                                                                l = re.sub(r"[^.0123456789]", "", str(l))
                                                                l = float(l)
                                                                value_row8 = l * dad * w
                                                            except:
                                                                pass
                                                            try:
                                                                value_row9 = 0
                                                                l = t[9]
                                                                if l == '':
                                                                    l = 0
                                                                w = 1
                                                                if '(' in l:
                                                                    w = -1
                                                                #
                                                                l = re.sub(r"[^.0123456789]", "", str(l))
                                                                l = float(l)
                                                                value_row9 = l * dad * w
                                                            except:
                                                                pass
                                                        except:
                                                            pass
                                                    #
                                                    else:
                                                        if z > 10:
                                                            g = (z - 3)
                                                            g = t[g]
                                                        #
                                                        elif z > 3:
                                                            if x == '' :
                                                                g = t[2]
                                                            else:
                                                                g = t[1]
                                                        else:
                                                            g = t[1]
                                                        #
                                                        if g == '':
                                                            g = 0
                                                        #
                                                        w = 1
                                                        if '(' in g:
                                                            w = -1
                                                        #
                                                        g = re.sub(r"[^.0123456789]", "", str(g))
                                                        g = float(g)
                                                        #
                                                        value = int(g * w * dad)
                                                    #
                                                    # Arching
                                                    try:
                                                        #
                                                        if statement == BS:
                                                            append_value(BalanceSheet, GL, value)
                                                            print('Balance Sheet, ' + GL + ': ' + str('{:,}'.format(value)))
                                                        #
                                                        if statement == IS:
                                                            append_value(IncomeStatement, GL, value)
                                                            print('Income Statement, ' + GL + ': ' + str('{:,}'.format(value)))
                                                        #
                                                        if statement == CI:
                                                            append_value(ComprehensiveIncomeStatement, GL, value)
                                                            print('Comprehensive Income, ' + GL + ': ' + str('{:,}'.format(value)))
                                                        #
                                                        if statement == SE:
                                                            try:
                                                                append_value(ShareholdersEquityStatement, GL_row1, value_row1)
                                                                append_value(ShareholdersEquityStatement, GL_row2, value_row2)
                                                                append_value(ShareholdersEquityStatement, GL_row3, value_row3)
                                                                append_value(ShareholdersEquityStatement, GL_row4, value_row4)
                                                                append_value(ShareholdersEquityStatement, GL_row5, value_row5)
                                                                append_value(ShareholdersEquityStatement, GL_row6, value_row6)
                                                                append_value(ShareholdersEquityStatement, GL_row7, value_row7)
                                                                append_value(ShareholdersEquityStatement, GL_row8, value_row8)
                                                                append_value(ShareholdersEquityStatement, GL_row9, value_row9)
                                                            except:
                                                                pass
                                                            try:
                                                                print('Shareholders Equity, ' + GL_row1 + ': ' + str('{:,}'.format(value_row1)))
                                                                print('Shareholders Equity, ' + GL_row2 + ': ' + str('{:,}'.format(value_row2)))
                                                                print('Shareholders Equity, ' + GL_row3 + ': ' + str('{:,}'.format(value_row3)))
                                                                print('Shareholders Equity, ' + GL_row4 + ': ' + str('{:,}'.format(value_row4)))
                                                                print('Shareholders Equity, ' + GL_row5 + ': ' + str('{:,}'.format(value_row5)))
                                                                print('Shareholders Equity, ' + GL_row6 + ': ' + str('{:,}'.format(value_row6)))
                                                                print('Shareholders Equity, ' + GL_row7 + ': ' + str('{:,}'.format(value_row7)))
                                                                print('Shareholders Equity, ' + GL_row8 + ': ' + str('{:,}'.format(value_row8)))
                                                                print('Shareholders Equity, ' + GL_row9 + ': ' + str('{:,}'.format(value_row9)))
                                                            except:
                                                                pass
                                                        #
                                                        if statement == CF:
                                                            append_value(CashFlowStatement, GL, value)
                                                            print('Cashflow, ' + GL + ': ' + str('{:,}'.format(value)))
                                                        #
                                                        else:
                                                            pass
                                                    except:
                                                        pass
                                                except:
                                                    pass
                                            #
                                            elif (len(row.find_all('th')) == 0 and len(row.find_all('strong')) != 0):
                                                #
                                                sec_row = cols[0].text.strip()
                                                #
                                                statement_data['sections'].append(sec_row)
                                            #
                                            elif len(row.find_all('th')) != 0:
                                                #
                                                hed_row = [ele.text.strip() for ele in row.find_all('th')]
                                                #
                                                statement_data['headers'].append(hed_row)
                                            #
                                            else:
                                                pass
                                        except:
                                            pass
                                except:
                                    pass
                            #
                            # define trial balances, cash flow and audit objects
                            try:
                                periodref = period.replace(' ','')
                                #
                                tb = TrialBalance.objects.get(TradingSymbol=e.TradingSymbol, Period=periodref)
                                cf = CashFlow.objects.get(TradingSymbol=e.TradingSymbol, Period=periodref)
                                a = AuditData.objects.get(TradingSymbol=e.TradingSymbol, Period=periodref)
                            except:
                                pass
                            #
                            # context (tb, cf, a)
                            try:
                                #
                                tb.PeriodEndDate = periodenddate
                                cf.PeriodEndDate = periodenddate
                                a.PeriodEndDate = periodenddate
                                #
                                tb.AccessionNumber = acc
                                cf.AccessionNumber = acc
                                a.AccessionNumber = acc
                                #
                                tb.AmendmentFlag = amend
                                cf.AmendmentFlag = amend
                                a.AmendmentFlag = amend
                                #
                                c = r"https://www.sec.gov/Archives/edgar/data/"
                                c = c + e.EntityCentralIndexKey + '/' 
                                c = c + tb.AccessionNumber.replace('-','') + '/' 
                                c = c + tb.AccessionNumber + '-index.htm'
                                tb.Link = c
                            except:
                                pass
                            #
                            # write to fs
                            try:
                                #
                                # balance sheet
                                try:
                                    print('\n' + 137 * '-')
                                    print(e.EntityRegistrantName)
                                    print('balance sheet')
                                    print(periodenddate)
                                    print(137 * '-' + '\n')
                                    #
                                    # totals
                                    try:
                                        #
                                        # cash
                                        try:
                                            Cash = []
                                            r = 0
                                            CashRank = None
                                            for key, value in BalanceSheet.items():
                                                if r < 5:
                                                    d = key
                                                    q = [
                                                        'Cash',
                                                    ]
                                                    b = [
                                                        'AssetsCurrent',
                                                        'CurrentAssets',
                                                        'DeferredTax',
                                                        'DeferredIncome',
                                                        'DiscontinuedOperations',
                                                        'Inventor',
                                                        'LongTerm',
                                                        'Prepaid',
                                                        'Receivable',
                                                        'Securities',
                                                        'Total',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while BalanceSheet[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = BalanceSheet[key][i]
                                                                    BalanceSheet[key][i] = None
                                                                except:
                                                                    if BalanceSheet[key] != None:
                                                                        ARCHvalue = BalanceSheet[key]
                                                                        BalanceSheet[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    Cash.append(ARCHvalue)
                                                                    if CashRank is None:
                                                                        CashRank = r
                                                r = r + 1
                                            tb.Cash = sum(Cash)
                                        except:
                                            pass
                                        #
                                        # total current assets
                                        try:
                                            TotalCurrentAssets = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CashRank:
                                                    d = key
                                                    q = [
                                                        'AssetsCurrent',
                                                        'CurrentAssets',
                                                    ]
                                                    b = [
                                                        'Cash',
                                                        'DeferredTax',
                                                        'DeferredIncome',
                                                        'DiscontinuedOperations',
                                                        'Financ',
                                                        'Intangible',
                                                        'Inventor',
                                                        'Investments',
                                                        'LongTerm',
                                                        'NonCurrent',
                                                        'Noncurrent',
                                                        'Miscellaneous',
                                                        'Other',
                                                        'Prepaid',
                                                        'Receivable',
                                                        'Securities',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while BalanceSheet[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = BalanceSheet[key][i]
                                                                    BalanceSheet[key][i] = None
                                                                except:
                                                                    if BalanceSheet[key] != None:
                                                                        ARCHvalue = BalanceSheet[key]
                                                                        BalanceSheet[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    TotalCurrentAssets.append(ARCHvalue)
                                                                    CurrentAssetsRank = r
                                                                
                                                r = r + 1
                                            a.CurrentAssets = sum(TotalCurrentAssets)
                                        except:
                                            pass
                                        #                   
                                        # total non current assets
                                        try:
                                            TotalNonCurrentAssets = []
                                            NonCurrentAssetsRank = None
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentAssetsRank:
                                                    d = key
                                                    q = [
                                                        'NonCurrentAsset',
                                                        'NoncurrentAsset',
                                                    ]
                                                    b = [
                                                        'IntangibleAssets',
                                                        'OtherNonCurrentAsset',
                                                        'OtherNoncurrentAsset',
                                                        'ShortTerm',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while BalanceSheet[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = BalanceSheet[key][i]
                                                                    BalanceSheet[key][i] = None
                                                                except:
                                                                    if BalanceSheet[key] != None:
                                                                        ARCHvalue = BalanceSheet[key]
                                                                        BalanceSheet[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    TotalNonCurrentAssets.append(ARCHvalue)
                                                                    NonCurrentAssetsRank = r
                                                r = r + 1
                                            a.NonCurrentAssets = sum(TotalNonCurrentAssets)
                                        except:
                                            pass
                                        #
                                        # total assets
                                        try:
                                            TotalAssets = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentAssetsRank:
                                                    d = key
                                                    q = [
                                                        'Assets',
                                                    ]
                                                    b = [
                                                        'Deferred',
                                                        'Goodwill',
                                                        'Intangible',
                                                        'Investment',
                                                        'Lease',
                                                        'Liabilit',
                                                        'Operating',
                                                        'Other',
                                                        'Miscellaneous',
                                                        'Property',
                                                        'Right',
                                                        'Tax',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while BalanceSheet[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = BalanceSheet[key][i]
                                                                    BalanceSheet[key][i] = None
                                                                except:
                                                                    if BalanceSheet[key] != None:
                                                                        ARCHvalue = BalanceSheet[key]
                                                                        BalanceSheet[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    TotalAssets.append(ARCHvalue)
                                                                    AssetsRank = r
                                                r = r + 1
                                            a.Assets = sum(TotalAssets)
                                            #
                                            # total asset not null
                                            try:
                                                if a.NonCurrentAssets == 0:
                                                    a.NonCurrentAssets = a.Assets - a.CurrentAssets
                                            except:
                                                pass
                                        except:
                                            pass
                                        #
                                        # total current liabilities
                                        try:
                                            CurrentLiabilities = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentAssetsRank:
                                                    d = key
                                                    q = [
                                                        'LiabilitiesCurrent',
                                                        'CurrentLiabilities',
                                                    ]
                                                    b = [
                                                        'Asset',
                                                        'LongTerm',
                                                        'Noncurrent',
                                                        'NonCurrent',
                                                        'OperatingLease',
                                                        'OtherCurrentLiabilit',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while BalanceSheet[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = BalanceSheet[key][i]
                                                                    BalanceSheet[key][i] = None
                                                                except:
                                                                    if BalanceSheet[key] != None:
                                                                        ARCHvalue = BalanceSheet[key]
                                                                        BalanceSheet[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    CurrentLiabilities.append(ARCHvalue)
                                                                    CurrentLiabilitiesRank = r
                                                r = r + 1
                                            a.CurrentLiabilities = -sum(CurrentLiabilities)
                                        except:
                                            pass
                                        #
                                        # total non-current liabilities
                                        try:
                                            TotalNonCurrentLiabilities = []
                                            NonCurrentLiabilitiesRank = None
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                d = key
                                                q = [
                                                    'LiabilitiesNoncurrent',
                                                    'LongTermLiabilit',
                                                    'NonCurrentLiabilit',
                                                    'NoncurrentLiabilit',
                                                    'TotalLongTermLiabilit',
                                                    'TotalOtherLiabilit',
                                                ]
                                                b = [
                                                    'Asset',
                                                    'OtherLongTermLiabilit',
                                                    'OtherNonCurrentLiabilit',
                                                    'OtherNoncurrentLiabilit',
                                                ]
                                                for l in q:
                                                    if l in d:
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = 0
                                                                while BalanceSheet[key][i] == None:
                                                                    i = i + 1
                                                                ARCHvalue = BalanceSheet[key][i]
                                                                BalanceSheet[key][i] = None
                                                            except:
                                                                if BalanceSheet[key] != None:
                                                                    ARCHvalue = BalanceSheet[key]
                                                                    BalanceSheet[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                TotalNonCurrentLiabilities.append(ARCHvalue)
                                                                NonCurrentLiabilitiesRank = r
                                                r = r + 1
                                            a.NonCurrentLiabilities = -sum(TotalNonCurrentLiabilities)
                                            if NonCurrentLiabilitiesRank is None:
                                                a.NonCurrentLiabilities = None
                                        except:
                                            pass
                                        #
                                        # total liabilities
                                        try:
                                            TotalLiabilities = []
                                            LiabilitiesRank = None
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                d = key
                                                q = [
                                                    'Liabilit',
                                                ]
                                                b = [
                                                    'Asset',
                                                    'Accrued',
                                                    'Businesses',
                                                    'Contract',
                                                    'Current',
                                                    'Equity',
                                                    'Lease',
                                                    'HeldForSale',
                                                    'LongTermLiabilit',
                                                    'NonCurrent',
                                                    'Noncurrent',
                                                    'Other',
                                                    'Miscellaneous',
                                                    'Payroll',
                                                    'Shareholder',
                                                    'Stockholder',
                                                    'Tax',
                                                    'Warrant',
                                                ]
                                                s = 'a'
                                                for l in q:
                                                    if s == 'a':
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while BalanceSheet[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = BalanceSheet[key][i]
                                                                    BalanceSheet[key][i] = None
                                                                except:
                                                                    if BalanceSheet[key] != None:
                                                                        ARCHvalue = BalanceSheet[key]
                                                                        BalanceSheet[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    TotalLiabilities.append(ARCHvalue)
                                                                    LiabilitiesRank = r
                                                                    s = 'z'
                                                    r = r + 1
                                            a.Liabilities = -sum(TotalLiabilities)
                                            if LiabilitiesRank is None:
                                                a.Liabilities = None
                                            else:
                                                pass
                                        except:
                                            pass
                                        #
                                        # total liabilities and shareholders' equity
                                        try:
                                            LiabilitiesAndShareholdersEquity = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                d = key
                                                q = [
                                                    'LiabilitiesAndStockholder',
                                                    'LiabilitiesAndEquity',
                                                    'LiabilitiesAndShareholders',
                                                    'LiabilitiesTemporaryEquity',
                                                ]
                                                b = [
                                                    'Asset',
                                                ]
                                                for l in q:
                                                    if l in d:
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = 0
                                                                while BalanceSheet[key][i] == None:
                                                                    i = i + 1
                                                                ARCHvalue = BalanceSheet[key][i]
                                                                BalanceSheet[key][i] = None
                                                            except:
                                                                if BalanceSheet[key] != None:
                                                                    ARCHvalue = BalanceSheet[key]
                                                                    BalanceSheet[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                LiabilitiesAndShareholdersEquity.append(ARCHvalue)
                                                                LiabilitiesAndShareholdersEquityRank = r
                                                r = r + 1
                                            a.LiabilitiesAndShareholdersEquity = -sum(LiabilitiesAndShareholdersEquity)
                                        except:
                                            pass
                                        #
                                        # debugging
                                        try:
                                            if a.Liabilities is None:
                                                #
                                                if a.NonCurrentLiabilities is None:
                                                    #
                                                    # shareholders equity
                                                    try:
                                                        ShareholdersEquity = []
                                                        r = 0
                                                        for key, value in BalanceSheet.items():
                                                            d = key
                                                            q = [
                                                                'TotalEquity',
                                                                'TotalShareholdersEquity',
                                                                'TotalStockholdersEquity',
                                                            ]
                                                            b = [
                                                                'Asset',
                                                                'Liabilit',
                                                                'Obligation',
                                                            ]
                                                            for l in q:
                                                                if l in d:
                                                                    h = 'p'
                                                                    for p in b:
                                                                        u = 0
                                                                        while u < len(b):
                                                                            if p in d:
                                                                                h = ''
                                                                            u = u + 1
                                                                    if h == 'p':
                                                                        try:
                                                                            i = 0
                                                                            while BalanceSheet[key][i] == None:
                                                                                i = i + 1
                                                                            ARCHvalue = BalanceSheet[key][i]
                                                                            BalanceSheet[key][i] = None
                                                                        except:
                                                                            if BalanceSheet[key] != None:
                                                                                ARCHvalue = BalanceSheet[key]
                                                                                BalanceSheet[key] = None
                                                                            else:
                                                                                ARCHvalue = 0
                                                                        if ARCHvalue != 0:
                                                                            ShareholdersEquity.append(ARCHvalue)
                                                            r = r + 1
                                                        a.ShareholdersEquity = -sum(ShareholdersEquity)
                                                    except:
                                                        pass
                                                    #
                                                    # liabilities
                                                    a.Liabilities = a.LiabilitiesAndShareholdersEquity - a.ShareholdersEquity
                                                    #
                                                    # non current liabilities
                                                    a.NonCurrentLiabilities = a.Liabilities - a.CurrentLiabilities
                                                    #
                                                else:
                                                    #
                                                    # non current liabilities
                                                    a.Liabilities = a.CurrentLiabilities + a.NonCurrentLiabilities
                                                    a.ShareholdersEquity = a.LiabilitiesAndShareholdersEquity - a.Liabilities
                                                #
                                                # liabilities rank & method
                                                LiabilitiesRank = LiabilitiesAndShareholdersEquityRank - 4
                                                NonCurrentLiabilitiesRankMethod = 'bridge'
                                                print('Non Current Liabilities Method: Bridge')
                                                #
                                            else:
                                                #
                                                # shareholders equity
                                                try:
                                                    #
                                                    a.ShareholdersEquity = a.LiabilitiesAndShareholdersEquity - a.Liabilities
                                                    #
                                                    if a.NonCurrentLiabilities is None:
                                                        a.NonCurrentLiabilities = a.Liabilities - a.CurrentLiabilities
                                                    #
                                                    a.AnomalyNonCurrentLiabilitiesSEC = 0
                                                    if NonCurrentLiabilitiesRank + 1 == LiabilitiesRank:
                                                        if NonCurrentLiabilitiesRank - 1 == CurrentLiabilitiesRank:
                                                            a.AnomalyNonCurrentLiabilitiesSEC = -a.NonCurrentLiabilities
                                                except:
                                                    pass
                                        except:
                                            pass
                                        #
                                        # dataframe balance sheet
                                        try:
                                            #
                                            df = pd.DataFrame({
                                                #
                                                '..': 
                                                    #
                                                    ['a.CurrentAssets',
                                                    'a.NonCurrentAssets',
                                                    'a.Assets',
                                                    'a.CurrentLiabilities',
                                                    'a.NonCurrentLiabilities',
                                                    'a.Liabilities',
                                                    'a.LiabilitiesAndShareholdersEquity'],
                                                #
                                                '.':
                                                    #
                                                    ['{:,}'.format(a.CurrentAssets),
                                                    '{:,}'.format(a.NonCurrentAssets),
                                                    '{:,}'.format(a.Assets),
                                                    '{:,}'.format(a.CurrentLiabilities),
                                                    '{:,}'.format(a.NonCurrentLiabilities),
                                                    '{:,}'.format(a.Liabilities),
                                                    '{:,}'.format(a.LiabilitiesAndShareholdersEquity)],
                                                #
                                                'rank':
                                                    #
                                                    [CurrentAssetsRank,
                                                    NonCurrentAssetsRank,
                                                    AssetsRank,
                                                    CurrentLiabilitiesRank,
                                                    NonCurrentLiabilitiesRank,
                                                    LiabilitiesRank,
                                                    LiabilitiesAndShareholdersEquityRank],
                                            })
                                            print(df)
                                            print('\n' + 137 * '-' + '\n')
                                            #
                                            tb.save()
                                            a.save()
                                        except:
                                            pass
                                        #
                                        # anomalies attributable to the SEC
                                        try:
                                            #
                                            print('anomalies attributable to the SEC')
                                            print(137 * '-' + '\n')
                                            #
                                            # current assets
                                            try:
                                                r = 0
                                                CAA = 0
                                                f = [
                                                    'TotalCash',
                                                    'TotalFinancialAssets',
                                                ]
                                                for key, value in BalanceSheet.items():
                                                    if r > CashRank - 1:
                                                        if r < CurrentAssetsRank:
                                                            d = key
                                                            b = ''
                                                            for g in f:
                                                                if g in d:
                                                                    b = 'p'
                                                            if b == '':
                                                                CAA = CAA + value
                                                    r = r + 1
                                                a.AnomalyCurrentAssetsSEC = CAA - a.CurrentAssets
                                                #
                                                # dataframe 
                                                try:
                                                    #
                                                    df = pd.DataFrame({
                                                        #
                                                        'current assets': 
                                                            #
                                                            ['Total',
                                                            'Components',
                                                            'Anomaly SEC'],
                                                        #
                                                        '.':
                                                            #
                                                            ['{:,}'.format(a.CurrentAssets),
                                                            '{:,}'.format(CAA),
                                                            '{:,}'.format(a.AnomalyCurrentAssetsSEC)],
                                                    })
                                                    print(df)
                                                    print(137 * '-' + '\n')
                                                except:
                                                    pass
                                            except:
                                                pass
                                            #
                                            # non current assets
                                            try:
                                                r = 0
                                                NCAA = 0
                                                ppepass = 0
                                                for key, value in BalanceSheet.items():
                                                    d = key
                                                    if r > CurrentAssetsRank:
                                                        if r < AssetsRank:
                                                            if ppepass == 0:
                                                                skip = ''
                                                                h = [
                                                                    'Land',
                                                                    'BuildingsAndLeasehold',
                                                                    'BuildingsAndImprovement',
                                                                    'ConstructionInProgress',
                                                                    'EquipmentAndFixtures',
                                                                    'LeaseholdCostsAndImprovments',
                                                                    'FixturesAndEquipment',
                                                                    'TotalOtherAssets',
                                                                ]
                                                                k = [
                                                                    'AccumulatedA',
                                                                    'AccumulatedD',
                                                                ]
                                                                for l in h:
                                                                    if l in d:
                                                                        skip = 'skip'
                                                                for m in k:
                                                                    if m in d:
                                                                        value = -abs(value)
                                                                        ppepass = 1
                                                                if skip == '':
                                                                    if value != None:
                                                                        NCAA = NCAA + value
                                                            else:
                                                                ppepass = 0
                                                    r = r + 1
                                                a.AnomalyNonCurrentAssetsSEC = NCAA - a.NonCurrentAssets
                                                #
                                                # dataframe
                                                try:
                                                    #
                                                    df = pd.DataFrame({
                                                        #
                                                        'non current assets': 
                                                            #
                                                            ['Total',
                                                            'Components',
                                                            'SEC Anomaly'],
                                                        #
                                                        '.':
                                                            #
                                                            ['{:,}'.format(a.NonCurrentAssets),
                                                            '{:,}'.format(NCAA),
                                                            '{:,}'.format(a.AnomalyNonCurrentAssetsSEC)],
                                                    })
                                                    print(df)
                                                except:
                                                    pass
                                                #
                                                print(137 * '-' + '\n')
                                            except:
                                                pass
                                            #
                                            # current liabilities
                                            try:
                                                r = 0
                                                CLA = 0
                                                for key, value in BalanceSheet.items():
                                                    d = key
                                                    if r > AssetsRank:
                                                        if r < CurrentLiabilitiesRank:
                                                            CLA = CLA - value
                                                    r = r + 1
                                                a.AnomalyCurrentLiabilitiesSEC = CLA - a.CurrentLiabilities
                                                #
                                                # dataframe
                                                try:
                                                    #
                                                    df = pd.DataFrame({
                                                        #
                                                        'current liabilities': 
                                                            #
                                                            ['Total',
                                                            'Components',
                                                            'SEC Anomaly'],
                                                        #
                                                        '.':
                                                            #
                                                            ['{:,}'.format(a.CurrentLiabilities),
                                                            '{:,}'.format(CLA),
                                                            '{:,}'.format(a.AnomalyCurrentLiabilitiesSEC)],
                                                    })
                                                    print(df)
                                                except:
                                                    pass
                                                #
                                                print(137 * '-' + '\n')
                                            except:
                                                pass
                                            #
                                            # non current liabilities
                                            try:
                                                if NonCurrentLiabilitiesRankMethod != 'bridge':
                                                    #
                                                    print('bridge ncl method')
                                                    #
                                                    LiabilitiesRank = min(LiabilitiesRank , LiabilitiesAndShareholdersEquityRank)
                                                    #
                                                    r = 0
                                                    NCLA = 0
                                                    k = [
                                                        'FaceValueOfLongTermDebtIncludingObligationsUnderCapitalLeasesAndFinancingObligations',
                                                        'AdjustmentToReflectFairValueInterestRateHedges',
                                                    ]
                                                    for key, value in BalanceSheet.items():
                                                        d = key
                                                        if r > CurrentLiabilitiesRank:
                                                            if r < LiabilitiesRank:
                                                                t = ''
                                                                for m in k:
                                                                    if m in d:
                                                                        t = 'n'
                                                                if t == '':
                                                                    NCLA = NCLA - value
                                                                    print(d)
                                                                    print('{:,}'.format(value))
                                                        r = r + 1
                                                    a.AnomalyNonCurrentLiabilitiesSEC = NCLA - (a.Liabilities - a.CurrentLiabilities)
                                                    #
                                                    # dataframe
                                                    try:
                                                        #
                                                        df = pd.DataFrame({
                                                        #
                                                        'non current liabilities': 
                                                            #
                                                            ['Total',
                                                            'Components',
                                                            'SEC Anomaly'],
                                                        #
                                                        '.':
                                                            #
                                                            ['{:,}'.format(a.NonCurrentLiabilities),
                                                            '{:,}'.format(NCLA),
                                                            '{:,}'.format(a.AnomalyNonCurrentLiabilitiesSEC)],
                                                        })
                                                        print(df)
                                                    except:
                                                        pass
                                                    #
                                                    print(137 * '-' + '\n')
                                                else:
                                                    pass
                                            except:
                                                pass
                                        except:
                                            pass
                                    except:
                                        pass
                                    #
                                    # current assets components
                                    try:
                                        #
                                        print(e.EntityRegistrantName)
                                        print('current assets')
                                        print(periodenddate)
                                        print(137 * '-' + '\n')
                                        #
                                        # short term investment
                                        try:
                                            ShortTermInvestments = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CashRank:
                                                    if r < CurrentAssetsRank:
                                                        d = key
                                                        q = [
                                                            'Investment',
                                                            'Securities',
                                                            'Trading',
                                                        ]
                                                        b = [
                                                            'AssetsCurrent',
                                                            'Cash',
                                                            'CurrentAssets',
                                                            'DeferredTax',
                                                            'DeferredIncome',
                                                            'DiscontinuedOperations',
                                                            'Inventor',
                                                            'Prepaid',
                                                            'Receivable',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        ShortTermInvestments.append(ARCHvalue)
                                                r = r + 1
                                            tb.ShortTermInvestments = sum(ShortTermInvestments)
                                        except:
                                            pass
                                        #
                                        # account receivable
                                        try:
                                            AccountsReceivable = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CashRank:
                                                    if r < CurrentAssetsRank:
                                                        d = key
                                                        q = [
                                                            'Receivable',
                                                            'LessAllowances',
                                                        ]
                                                        b = [
                                                            'Cash',
                                                            'DeferredTax',
                                                            'DeferredIncome',
                                                            'DiscontinuedOperations',
                                                            'Inventor',
                                                            'Investments',
                                                            'Prepaid',
                                                            'Securities',
                                                            'UnbilledReceivable',
                                                            'WorkInProgress',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        AccountsReceivable.append(ARCHvalue)
                                                r = r + 1
                                            tb.AccountsReceivable = sum(AccountsReceivable)
                                        except:
                                            pass
                                        #
                                        # work in progress
                                        try:
                                            WorkInProgress = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CashRank:
                                                    if r < CurrentAssetsRank:
                                                        d = key
                                                        q = [
                                                            'UnbilledReceivable',
                                                            'WorkInProgress',
                                                        ]
                                                        b = [
                                                            'AssetsCurrent',
                                                            'Cash',
                                                            'CurrentAssets',
                                                            'DeferredTax',
                                                            'DeferredIncome',
                                                            'DiscontinuedOperations',
                                                            'Inventor',
                                                            'Investments',
                                                            'Prepaid',
                                                            'Securities',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        WorkInProgress.append(ARCHvalue)
                                                r = r + 1
                                            tb.WorkInProgress = sum(WorkInProgress)
                                        except:
                                            pass
                                        #
                                        # inventories
                                        try:
                                            Inventories = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CashRank:
                                                    if r < CurrentAssetsRank:
                                                        d = key
                                                        q = [
                                                            'Inventor',
                                                            'Reserve',
                                                            'CarPooling',
                                                            'VehiclePooling',
                                                        ]
                                                        b = [
                                                            'AssetsCurrent',
                                                            'Cash',
                                                            'CurrentAssets',
                                                            'DeferredTax',
                                                            'DeferredIncome',
                                                            'DiscontinuedOperations',
                                                            'Investments',
                                                            'Prepaid',
                                                            'Receivable',
                                                            'Securities',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        Inventories.append(ARCHvalue)
                                                r = r + 1
                                            tb.Inventories = sum(Inventories)
                                        except:
                                            pass
                                        #
                                        # prepaid expenses
                                        try:
                                            PrepaidExpenses = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CashRank:
                                                    if r < CurrentAssetsRank:
                                                        d = key
                                                        q = [
                                                            'Prepaid',
                                                            'Deposit',
                                                            'ContractAsset',
                                                        ]
                                                        b = [
                                                            'Cash',
                                                            'DeferredTax',
                                                            'DeferredIncome',
                                                            'DiscontinuedOperations',
                                                            'Inventor',
                                                            'Investments',
                                                            'Receivable',
                                                            'Securities',
                                                            'Tax',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        PrepaidExpenses.append(ARCHvalue)
                                                r = r + 1
                                            tb.PrepaidExpenses = sum(PrepaidExpenses)
                                        except:
                                            pass
                                        #
                                        # non-trade receivables
                                        try:
                                            NonTradeReceivables = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CashRank:
                                                    if r < CurrentAssetsRank:
                                                        d = key
                                                        q = [
                                                            'LoansReceivable',
                                                            'NonTradeReceivable',
                                                            'OtherReceivable',
                                                        ]
                                                        b = [
                                                            'AssetsCurrent',
                                                            'Cash',
                                                            'CurrentAssets',
                                                            'DeferredTax',
                                                            'DeferredIncome',   
                                                            'DiscontinuedOperations',
                                                            'Inventor',
                                                            'Investments',
                                                            'Prepaid',
                                                            'Securities',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        NonTradeReceivables.append(ARCHvalue)
                                                r = r + 1
                                            tb.NonTradeReceivables = sum(NonTradeReceivables)
                                        except:
                                            pass
                                        #
                                        # prepaid tax assets current
                                        try:
                                            PrepaidTaxAssetsCurrent = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CashRank:
                                                    if r < CurrentAssetsRank:
                                                        d = key
                                                        q = [
                                                            'PrepaidTax',
                                                            'PrepaidIncomeTax',
                                                            'TaxesRefundable',
                                                            'RefundableIncomeTax',
                                                            'RefundableTax',
                                                        ]
                                                        b = [
                                                            'Cash',
                                                            'DiscontinuedOperations',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        PrepaidTaxAssetsCurrent.append(ARCHvalue)
                                                r = r + 1
                                            tb.PrepaidTaxAssetsCurrent = sum(PrepaidTaxAssetsCurrent)
                                        except:
                                            pass
                                        #
                                        # deferred tax assets current
                                        try:
                                            DeferredTaxAssetsCurrent = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CashRank:
                                                    if r < CurrentAssetsRank:
                                                        d = key
                                                        q = [
                                                            'DeferredIncomeTax',
                                                            'DeferredTax',
                                                            'DeferredIncome',
                                                        ]
                                                        b = [
                                                            'Cash',
                                                            'DiscontinuedOperations',
                                                            'Inventor',
                                                            'Investments',
                                                            'Prepaid',
                                                            'Receivable',
                                                            'Securities',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        DeferredTaxAssetsCurrent.append(ARCHvalue)
                                                r = r + 1
                                            tb.DeferredTaxAssetsCurrent = sum(DeferredTaxAssetsCurrent)
                                        except:
                                            pass
                                        #
                                        # right of use assets current
                                        try:
                                            RightOfUseAssetsCurrent = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CashRank:
                                                    if r < CurrentAssetsRank:
                                                        d = key
                                                        q = [
                                                            'RightOfUse',
                                                        ]
                                                        b = [
                                                            'AssetsCurrent',
                                                            'Cash',
                                                            'CurrentAssets', 
                                                            'DiscontinuedOperations',
                                                            'Inventor',
                                                            'Investments',
                                                            'Prepaid',
                                                            'Receivable',
                                                            'Securities',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        RightOfUseAssetsCurrent.append(ARCHvalue)
                                                r = r + 1
                                            tb.RightOfUseAssetsCurrent = sum(RightOfUseAssetsCurrent)
                                        except:
                                            pass
                                        #
                                        # other current assets
                                        try:
                                            OtherCurrentAssets = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CashRank:
                                                    if r < CurrentAssetsRank:
                                                        d = key
                                                        q = [
                                                            'Other',
                                                            'Miscellaneous',
                                                        ]
                                                        b = [
                                                            'Cash',
                                                            'DeferredTax',
                                                            'DeferredIncome',
                                                            'DiscontinuedOperations',
                                                            'Inventor',
                                                            'Investments',
                                                            'Prepaid',
                                                            'Receivable',
                                                            'Securities',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        OtherCurrentAssets.append(ARCHvalue)
                                                r = r + 1
                                            tb.OtherCurrentAssets = sum(OtherCurrentAssets)
                                        except:
                                            pass
                                        #
                                        # discontinued operations current
                                        try:
                                            DiscontinuedOperationsCurrent = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CashRank:
                                                    if r < CurrentAssetsRank:
                                                        d = key
                                                        q = [
                                                            'Discontinued',
                                                            'AssetsHeldForSale',
                                                            'BusinessesHeldForSale',
                                                        ]
                                                        b = [
                                                            'AssetsCurrent',
                                                            'Cash',
                                                            'CurrentAssets', 
                                                            'DeferredTax',
                                                            'DeferredIncome',
                                                            'DiscontinuedOperations',
                                                            'Inventor',
                                                            'Investments',
                                                            'Prepaid',
                                                            'Receivable',
                                                            'Securities',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        DiscontinuedOperationsCurrent.append(ARCHvalue)
                                                r = r + 1
                                            tb.DiscontinuedOperationsCurrent = sum(DiscontinuedOperationsCurrent)
                                        except:
                                            pass
                                        #
                                        # ML
                                        try:
                                            w = None
                                            a.CurrentAssetsGL_i = ''
                                            m = None 
                                            a.CurrentAssetsGL_ii = ''
                                            t = None
                                            a.CurrentAssetsGL_iii = ''
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CashRank:
                                                    if r < CurrentAssetsRank:
                                                        d = key
                                                        b = [
                                                            'Total',
                                                        ]
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = 0
                                                                while BalanceSheet[key][i] == None:
                                                                    i = i + 1
                                                                ARCHvalue = BalanceSheet[key][i]
                                                                BalanceSheet[key][i] = None
                                                            except:
                                                                if BalanceSheet[key] != None:
                                                                    ARCHvalue = BalanceSheet[key]
                                                                    BalanceSheet[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                try:
                                                                    #
                                                                    if w is None:
                                                                        a.CurrentAssetsGL_i = d
                                                                        w = ''
                                                                    #
                                                                    elif m is None:
                                                                        a.CurrentAssetsGL_ii = d
                                                                        m = ''
                                                                    #
                                                                    elif t is None:
                                                                        a.CurrentAssetsGL_iii = d
                                                                        t = ''
                                                                    else:
                                                                        pass
                                                                    #
                                                                    if d not in CurrentAssetsGL:
                                                                        CurrentAssetsGL.append(d)
                                                                    #
                                                                except:
                                                                    pass
                                                r = r + 1
                                        except:
                                            pass
                                        #
                                        # dataframe                        
                                        try:
                                            df = pd.DataFrame({
                                                #
                                                '..': 
                                                    #
                                                    ['tb.Cash',
                                                    'tb.ShortTermInvestments',
                                                    'tb.AccountsReceivable',
                                                    'tb.WorkInProgress',
                                                    'tb.Inventories',
                                                    'tb.PrepaidExpenses',
                                                    'tb.NonTradeReceivables',
                                                    'tb.DeferredTaxAssetsCurrent',
                                                    'tb.PrepaidTaxAssetsCurrent',
                                                    'tb.RightOfUseAssetsCurrent',
                                                    'tb.OtherCurrentAssets',
                                                    'tb.DiscontinuedOperationsCurrent'],
                                                #
                                                '.':
                                                    #
                                                    ['{:,}'.format(tb.Cash),
                                                    '{:,}'.format(tb.ShortTermInvestments),
                                                    '{:,}'.format(tb.AccountsReceivable),
                                                    '{:,}'.format(tb.WorkInProgress),
                                                    '{:,}'.format(tb.Inventories),
                                                    '{:,}'.format(tb.PrepaidExpenses),
                                                    '{:,}'.format(tb.NonTradeReceivables),
                                                    '{:,}'.format(tb.DeferredTaxAssetsCurrent),
                                                    '{:,}'.format(tb.PrepaidTaxAssetsCurrent),
                                                    '{:,}'.format(tb.RightOfUseAssetsCurrent),
                                                    '{:,}'.format(tb.OtherCurrentAssets),
                                                    '{:,}'.format(tb.DiscontinuedOperationsCurrent)],
                                            })
                                            print(df)
                                            print(137 * '-' + '\n')
                                        except:
                                            pass
                                    except:
                                        pass
                                    #
                                    # non-current assets components
                                    try:
                                        #
                                        print(e.EntityRegistrantName)
                                        print('non-current assets')
                                        print(periodenddate)
                                        print(137 * '-' + '\n')
                                        #
                                        # long term receivables
                                        try:
                                            LongTermReceivables = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentAssetsRank:
                                                    if r < AssetsRank:
                                                        d = key
                                                        q = [
                                                            'Receivable',
                                                        ]
                                                        b = [
                                                            'Intangible',
                                                            'ShortTerm',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        LongTermReceivables.append(ARCHvalue)
                                                r = r + 1
                                            tb.LongTermReceivables = sum(LongTermReceivables)
                                        except:
                                            pass
                                        #
                                        # deferred charges
                                        try:
                                            DeferredCharges = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentAssetsRank:
                                                    if r < AssetsRank:
                                                        d = key
                                                        q = [
                                                            'DeferredCharges',
                                                            'DeferredCost',
                                                        ]
                                                        b = [
                                                            'ShortTerm',
                                                            'Tax',
                                                            'Income',
                                                            'Intangible',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        DeferredCharges.append(ARCHvalue)
                                                r = r + 1
                                            tb.DeferredCharges = sum(DeferredCharges)
                                        except:
                                            pass
                                        #
                                        # investments
                                        try:
                                            Investments = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentAssetsRank:
                                                    if r < AssetsRank:
                                                        d = key
                                                        q = [
                                                            'Investment',
                                                            'Securities',
                                                        ]
                                                        b = [
                                                            'Intangible',
                                                            'ShortTerm',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        Investments.append(ARCHvalue)
                                                r = r + 1
                                            tb.Investments = sum(Investments)
                                        except:
                                            pass
                                        #
                                        # property plant and equipments
                                        try:
                                            PropertyPlantAndEquipment = []
                                            r = 0
                                            ppe = ''
                                            ppepass = ''
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentAssetsRank:
                                                    if r < AssetsRank:
                                                        d = key
                                                        x = ''
                                                        q = [
                                                            'Property',
                                                            'AccumulatedA',
                                                            'AccumulatedD',
                                                        ]
                                                        b = [
                                                            'Intangible',
                                                            'UnderCapitalLease',
                                                        ]
                                                        m = [
                                                            'AccumulatedA',
                                                            'AccumulatedD',
                                                        ]
                                                        k = [
                                                            'Property',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                for j in k:
                                                                    for y in m:
                                                                        if y in d:
                                                                            x = 'p'
                                                                if x == '' :
                                                                    if j in d:
                                                                        if ppe == 'once':
                                                                            ppe = 'twice'
                                                                            ppepass = 'no'
                                                                        elif ppe == '':
                                                                            ppe = 'once'
                                                                if ppe == 'once':
                                                                    ppepass = ''
                                                                if h == 'p':
                                                                    if ppepass == '':
                                                                        try:
                                                                            i = 0
                                                                            while BalanceSheet[key][i] == None:
                                                                                i = i + 1
                                                                            ARCHvalue = BalanceSheet[key][i]
                                                                            BalanceSheet[key][i] = None
                                                                        except:
                                                                            if BalanceSheet[key] != None:
                                                                                ARCHvalue = BalanceSheet[key]
                                                                                BalanceSheet[key] = None
                                                                            else:
                                                                                ARCHvalue = 0
                                                                        for n in m:
                                                                            if n in d:
                                                                                ARCHvalue = -abs(ARCHvalue) 
                                                                        if ARCHvalue != 0:
                                                                            PropertyPlantAndEquipment.append(ARCHvalue)
                                                r = r + 1
                                            tb.PropertyPlantAndEquipment = sum(PropertyPlantAndEquipment)
                                        except:
                                            pass
                                        #
                                        # finance lease right of use assets
                                        try:
                                            FinanceLeaseRightOfUseAssets = []
                                            r = 0
                                            ppe = ''
                                            ppepass = ''
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentAssetsRank:
                                                    if r < AssetsRank:
                                                        d = key
                                                        q = [
                                                            'CapitalLease',
                                                            'FinanceLease',
                                                            'FinancingLease',
                                                        ]
                                                        b = [
                                                            'Due',
                                                            'Intangible',
                                                            'Liabilit',
                                                        ]
                                                        m = [
                                                            'AccumulatedA',
                                                            'AccumulatedD',
                                                        ]
                                                        k = [
                                                            'CapitalLease',
                                                            'FinanceLease',
                                                            'FinancingLease',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                for j in k:
                                                                    for y in m:
                                                                        if y in d:
                                                                            x = 'p'
                                                                if x == '' :
                                                                    if j in d:
                                                                        if ppe == 'once':
                                                                            ppe = 'twice'
                                                                            ppepass = 'no'
                                                                        elif ppe == '':
                                                                            ppe = 'once'
                                                                if ppe == 'once':
                                                                    ppepass = ''
                                                                if h == 'p':
                                                                    if ppepass == '':
                                                                        try:
                                                                            i = 0
                                                                            while BalanceSheet[key][i] == None:
                                                                                i = i + 1
                                                                            ARCHvalue = BalanceSheet[key][i]
                                                                            BalanceSheet[key][i] = None
                                                                        except:
                                                                            if BalanceSheet[key] != None:
                                                                                ARCHvalue = BalanceSheet[key]
                                                                                BalanceSheet[key] = None
                                                                            else:
                                                                                ARCHvalue = 0
                                                                        if ARCHvalue != 0:
                                                                            FinanceLeaseRightOfUseAssets.append(ARCHvalue)
                                                r = r + 1
                                            tb.FinanceLeaseRightOfUseAssets = sum(FinanceLeaseRightOfUseAssets)
                                        except:
                                            pass
                                        #
                                        # operating lease right of use assets
                                        try:
                                            OperatingLeaseRightOfUseAssets = []
                                            r = 0
                                            ppe = ''
                                            ppepass = ''
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentAssetsRank:
                                                    if r < AssetsRank:
                                                        d = key
                                                        x = ''
                                                        q = [
                                                            'AccumulatedA',
                                                            'AccumulatedD',
                                                            'OperatingLease',
                                                            'OperatingRight',
                                                            'RightOfUse',
                                                        ]
                                                        b = [
                                                            'Liabilit',
                                                            'Intangible',
                                                            'Due',
                                                            'Obligations',
                                                            'Buildings',
                                                        ]
                                                        m = [
                                                            'AccumulatedA',
                                                            'AccumulatedD',
                                                        ]
                                                        k = [
                                                            'OperatingLease',
                                                            'OperatingRight',
                                                            'RightOfUse',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                for j in k:
                                                                    for y in m:
                                                                        if y in d:
                                                                            x = 'p'
                                                                if x == '' :
                                                                    if j in d:
                                                                        if ppe == 'once':
                                                                            ppe = 'twice'
                                                                            ppepass = 'no'
                                                                        elif ppe == '':
                                                                            ppe = 'once'
                                                                if ppe == 'once':
                                                                    ppepass = ''
                                                                if h == 'p':
                                                                    if ppepass == '':
                                                                        try:
                                                                            i = 0
                                                                            while BalanceSheet[key][i] == None:
                                                                                i = i + 1
                                                                            ARCHvalue = BalanceSheet[key][i]
                                                                            BalanceSheet[key][i] = None
                                                                        except:
                                                                            if BalanceSheet[key] != None:
                                                                                ARCHvalue = BalanceSheet[key]
                                                                                BalanceSheet[key] = None
                                                                            else:
                                                                                ARCHvalue = 0
                                                                        if ARCHvalue != 0:
                                                                            OperatingLeaseRightOfUseAssets.append(ARCHvalue)
                                                r = r + 1
                                            tb.OperatingLeaseRightOfUseAssets = sum(OperatingLeaseRightOfUseAssets)
                                        except:
                                            pass
                                        #
                                        # intangible assets
                                        try:
                                            IntangibleAssets = []
                                            r = 0
                                            x = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentAssetsRank:
                                                    if r < AssetsRank:
                                                        d = key
                                                        print(d)
                                                        print(value)
                                                        q = [
                                                            'EquipmentAtCustomers',
                                                            'FranchiseRight',
                                                            'Intangible',
                                                            'Software',
                                                            'Trademarks',
                                                            'Research',
                                                        ]
                                                        b = [
                                                            'Liabilit',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        IntangibleAssets.append(ARCHvalue)
                                                                        print(d)
                                                                        print('{:,}'.format(value))
                                                r = r + 1
                                            tb.IntangibleAssets = sum(IntangibleAssets)
                                        except:
                                            pass
                                        #
                                        # goodwill
                                        try:
                                            Goodwill = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentAssetsRank:
                                                    if r < AssetsRank:
                                                        d = key
                                                        q = [
                                                            'Goodwill',
                                                        ]
                                                        b = [
                                                            'Liabilit',
                                                            'Intangible',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        Goodwill.append(ARCHvalue)
                                                r = r + 1
                                            tb.Goodwill = sum(Goodwill)
                                        except:
                                            pass
                                        #
                                        # refundable tax assets non current
                                        try:
                                            RefundableTaxAssetsNonCurrent = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentAssetsRank:
                                                    if r < AssetsRank:
                                                        d = key
                                                        q = [
                                                            'TaxesRefundable',
                                                            'RefundableIncomeTax',
                                                            'RefundableTax',
                                                        ]
                                                        b = [
                                                            'Deferred',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        RefundableTaxAssetsNonCurrent.append(ARCHvalue)
                                                r = r + 1
                                            tb.RefundableTaxAssetsNonCurrent = sum(RefundableTaxAssetsNonCurrent)
                                        except:
                                            pass
                                        #
                                        # deferred tax assets non current
                                        try:
                                            DeferredTaxAssetsNonCurrent = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentAssetsRank:
                                                    if r < AssetsRank:
                                                        d = key
                                                        q = [
                                                            'DeferredTax',
                                                            'DeferredIncome',
                                                        ]
                                                        b = [
                                                            'Liabilit',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        DeferredTaxAssetsNonCurrent.append(ARCHvalue)
                                                r = r + 1
                                            tb.DeferredTaxAssetsNonCurrent = sum(DeferredTaxAssetsNonCurrent)
                                        except:
                                            pass
                                        #
                                        # Defined Benefit Pension And Other Similar Plans
                                        try:
                                            DefinedBenefitPensionAndOtherSimilarPlans = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentAssetsRank:
                                                    if r < AssetsRank:
                                                        d = key
                                                        q = [
                                                            'DefinedBenefit',
                                                            'Pension',
                                                        ]
                                                        b = [
                                                            'Liability',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        DefinedBenefitPensionAndOtherSimilarPlans.append(ARCHvalue)
                                                r = r + 1
                                            tb.DefinedBenefitPensionAndOtherSimilarPlans = sum(DefinedBenefitPensionAndOtherSimilarPlans)
                                        except:
                                            pass
                                        #
                                        # other non-current assets
                                        try:
                                            OtherNonCurrentAssets = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentAssetsRank:
                                                    if r < AssetsRank:
                                                        d = key
                                                        q = [
                                                            'RestrictedCash',
                                                            'Miscellaneous',
                                                            'Other',
                                                            'Sundry',
                                                        ]
                                                        b = [
                                                            'Liabilit',
                                                            'Total',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        OtherNonCurrentAssets.append(ARCHvalue)
                                                r = r + 1
                                            tb.OtherNonCurrentAssets = sum(OtherNonCurrentAssets)
                                        except:
                                            pass
                                        #
                                        # ML
                                        try:
                                            w = None
                                            a.NonCurrentAssetsGL_i = ''
                                            m = None
                                            a.NonCurrentAssetsGL_ii = ''
                                            t = None
                                            a.NonCurrentAssetsGL_iii = ''
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentAssetsRank:
                                                    if r < AssetsRank:
                                                        d = key
                                                        b = [
                                                            'Total',
                                                        ]
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = 0
                                                                while BalanceSheet[key][i] == None:
                                                                    i = i + 1
                                                                ARCHvalue = BalanceSheet[key][i]
                                                                BalanceSheet[key][i] = None
                                                            except:
                                                                if BalanceSheet[key] != None:
                                                                    ARCHvalue = BalanceSheet[key]
                                                                    BalanceSheet[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                try:
                                                                    #
                                                                    if w is None:
                                                                        a.NonCurrentAssetsGL_i = d
                                                                        w = ''
                                                                    #
                                                                    elif m is None:
                                                                        a.NonCurrentAssetsGL_ii = d
                                                                        m = ''
                                                                    #
                                                                    elif t is None:
                                                                        a.NonCurrentAssetsGL_iii = d
                                                                        t = ''
                                                                    else:
                                                                        pass
                                                                    #
                                                                    if d not in NonCurrentAssetsGL:
                                                                        NonCurrentAssetsGL.append(d)
                                                                    #
                                                                except:
                                                                    pass
                                                r = r + 1
                                        except:
                                            pass
                                        #
                                        # dataframe                        
                                        try:
                                            df = pd.DataFrame({
                                                #
                                                '..': 
                                                    #
                                                    ['tb.LongTermReceivables',
                                                    'tb.DeferredCharges',
                                                    'tb.Investments',
                                                    'tb.PropertyPlantAndEquipment',
                                                    'tb.OperatingLeaseRightOfUseAssets',
                                                    'tb.FinanceLeaseRightOfUseAssets',
                                                    'tb.IntangibleAssets',
                                                    'tb.Goodwill',
                                                    'tb.RefundableTaxAssetsNonCurrent',
                                                    'tb.DeferredTaxAssetsNonCurrent',
                                                    'tb.DefinedBenefitPensionAndOtherSimilarPlans',
                                                    'tb.OtherNonCurrentAssets'],
                                                #
                                                '.':
                                                    #
                                                    ['{:,}'.format(tb.LongTermReceivables),
                                                    '{:,}'.format(tb.DeferredCharges),
                                                    '{:,}'.format(tb.Investments),
                                                    '{:,}'.format(tb.PropertyPlantAndEquipment),
                                                    '{:,}'.format(tb.OperatingLeaseRightOfUseAssets),
                                                    '{:,}'.format(tb.FinanceLeaseRightOfUseAssets),
                                                    '{:,}'.format(tb.IntangibleAssets),
                                                    '{:,}'.format(tb.Goodwill),
                                                    '{:,}'.format(tb.RefundableTaxAssetsNonCurrent),
                                                    '{:,}'.format(tb.DeferredTaxAssetsNonCurrent),
                                                    '{:,}'.format(tb.DefinedBenefitPensionAndOtherSimilarPlans),
                                                    '{:,}'.format(tb.OtherNonCurrentAssets)],
                                            })
                                            print(df)
                                            print(137 * '-' + '\n')
                                        except:
                                            pass
                                    except:
                                        pass
                                    #                   
                                    # current liabilities components
                                    try:
                                        print(e.EntityRegistrantName)
                                        print('current liabilities')
                                        print(periodenddate)
                                        print(137 * '-' + '\n')
                                        #
                                        # accounts payable and accrued liabilities
                                        try:
                                            AccountsPayableAndAccruedLiabilities = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > AssetsRank:
                                                    if r < CurrentLiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'Accrued',
                                                            'Payable',
                                                            'SalesRebates',
                                                            'Discounts',
                                                        ]
                                                        b = [
                                                            'Benefit',
                                                            'Deferred',
                                                            'Employee',
                                                            'Tax',
                                                            'Dividend',
                                                            'LongTerm',
                                                            'NonCurrent',
                                                            'Noncurrent',
                                                            'Compensation',
                                                            'Payroll',
                                                            'Salaries',
                                                            'Wages',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        AccountsPayableAndAccruedLiabilities.append(ARCHvalue)
                                                r = r + 1
                                            tb.AccountsPayableAndAccruedLiabilities = -sum(AccountsPayableAndAccruedLiabilities)
                                        except:
                                            pass
                                        #
                                        # employee compensation current
                                        try:
                                            EmployeeCompensationCurrent = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > AssetsRank:
                                                    if r < CurrentLiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'AccruedBenefits',
                                                            'BonusAndBenefits',
                                                            'Compensation',
                                                            'Payroll',
                                                            'Salaries',
                                                            'Wages',
                                                        ]
                                                        b = [
                                                            'Equity',
                                                            'LongTerm',
                                                            'NonCurrent',
                                                            'Noncurrent',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        EmployeeCompensationCurrent.append(ARCHvalue)
                                                r = r + 1
                                            tb.EmployeeCompensationCurrent = -sum(EmployeeCompensationCurrent)
                                        except:
                                            pass
                                        #
                                        # finance leases current
                                        try:
                                            FinanceLeasesCurrent = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > AssetsRank:
                                                    if r < CurrentLiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'FinanceLease',
                                                            'FinancingLease',
                                                            'FinancingObligation',
                                                            'CapitalLease',
                                                        ]
                                                        b = [
                                                            'LongTerm',
                                                            'NonCurrent',
                                                            'Noncurrent',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        FinanceLeasesCurrent.append(ARCHvalue)
                                                r = r + 1
                                            tb.FinanceLeasesCurrent = -sum(FinanceLeasesCurrent)
                                        except:
                                            pass
                                        #
                                        # operating leases current
                                        try:
                                            OperatingLeasesCurrent = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > AssetsRank:
                                                    if r < CurrentLiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'LeaseLiabilit',
                                                            'LeaseObligation',
                                                            'OperatingLease',
                                                        ]
                                                        b = [
                                                            'LongTerm',
                                                            'NonCurrent',
                                                            'Noncurrent',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        OperatingLeasesCurrent.append(ARCHvalue)
                                                r = r + 1
                                            tb.OperatingLeasesCurrent = -sum(OperatingLeasesCurrent)
                                        except:
                                            pass
                                        #
                                        # deferred revenue and deposits current
                                        try:
                                            DeferredRevenueAndDepositsCurrent = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > AssetsRank:
                                                    if r < CurrentLiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'ContractWithCustomer',
                                                            'ContractLiabilit',
                                                            'CustomerAdvancePayment',
                                                            'DeferredIncome',
                                                            'DeferredRevenue',
                                                            'Deposit',
                                                            'Guarantee',
                                                        ]
                                                        b = [
                                                            'LongTerm',
                                                            'NonCurrent',
                                                            'Noncurrent',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        DeferredRevenueAndDepositsCurrent.append(ARCHvalue)
                                                r = r + 1
                                            tb.DeferredRevenueAndDepositsCurrent = -sum(DeferredRevenueAndDepositsCurrent)
                                        except:
                                            pass
                                        #
                                        # accrued tax liabilities
                                        try:
                                            AccruedTaxLiabilities = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > AssetsRank:
                                                    if r < CurrentLiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'Tax',
                                                        ]
                                                        b = [
                                                            'Deferred',
                                                            'LongTerm',
                                                            'NonCurrent',
                                                            'Noncurrent',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        AccruedTaxLiabilities.append(ARCHvalue)
                                                r = r + 1
                                            tb.AccruedTaxLiabilities = -sum(AccruedTaxLiabilities)
                                        except:
                                            pass
                                        #
                                        # deferred tax liabilities
                                        try:
                                            DeferredTaxLiabilitiesCurrent = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > AssetsRank:
                                                    if r < CurrentLiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'Deferred',
                                                        ]
                                                        b = [
                                                            'Accrued',
                                                            'Charges',
                                                            'Expense',
                                                            'LongTerm',
                                                            'NonCurrent',
                                                            'Noncurrent',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        DeferredTaxLiabilitiesCurrent.append(ARCHvalue)
                                                r = r + 1
                                            tb.DeferredTaxLiabilitiesCurrent = -sum(DeferredTaxLiabilitiesCurrent)
                                        except:
                                            pass
                                        #
                                        # commercial papers
                                        try:
                                            CommercialPapers = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > AssetsRank:
                                                    if r < CurrentLiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'CommercialPaper',
                                                        ]
                                                        b = [
                                                            'Accrued',
                                                            'Deferred',
                                                            'LongTerm',
                                                            'NonCurrent',
                                                            'Noncurrent',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        CommercialPapers.append(ARCHvalue)
                                                r = r + 1
                                            tb.CommercialPapers = -sum(CommercialPapers)
                                        except:
                                            pass
                                        #
                                        # short term borrowings
                                        try:
                                            ShortTermBorrowings = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > AssetsRank:
                                                    if r < CurrentLiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'BankIndebtedness',
                                                            'Borrowings',
                                                            'LineOfCredit',
                                                            'LinesOfCredit',
                                                            'ShortTermBorrowing',
                                                            'Revolver',
                                                            'Revolving',
                                                        ]
                                                        b = [
                                                            'Accrued',
                                                            'Deferred',
                                                            'LongTerm',
                                                            'NonCurrent',
                                                            'Noncurrent',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        ShortTermBorrowings.append(ARCHvalue)
                                                r = r + 1
                                            tb.ShortTermBorrowings = -sum(ShortTermBorrowings)
                                        except:
                                            pass
                                        #
                                        # other current liabilities
                                        try:
                                            OtherCurrentLiabilities = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > AssetsRank:
                                                    if r < CurrentLiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'OtherCurrentLiabilit',
                                                            'SelfInsuranceReserves',
                                                        ]
                                                        b = [
                                                            'LongTerm',
                                                            'NonCurrent',
                                                            'Noncurrent',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        OtherCurrentLiabilities.append(ARCHvalue)
                                                r = r + 1
                                            tb.OtherCurrentLiabilities = -sum(OtherCurrentLiabilities)
                                        except:
                                            pass
                                        #
                                        # discontinued operations
                                        try:
                                            DiscontinuedOperationsLiabilitiesCurrent = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > AssetsRank:
                                                    if r < CurrentLiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'DiscontinuedOperation',
                                                            'HeldForSale',
                                                        ]
                                                        b = [
                                                            'LongTerm',
                                                            'NonCurrent',
                                                            'Noncurrent',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        DiscontinuedOperationsLiabilitiesCurrent.append(ARCHvalue)
                                                r = r + 1
                                            tb.DiscontinuedOperationsLiabilitiesCurrent = -sum(DiscontinuedOperationsLiabilitiesCurrent)
                                        except:
                                            pass
                                        #
                                        # dividend payable
                                        try:
                                            DividendsPayable = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > AssetsRank:
                                                    if r < CurrentLiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'DividendsPayable',
                                                            'DividendPayable',
                                                        ]
                                                        b = [
                                                            'LongTerm',
                                                            'NonCurrent',
                                                            'Noncurrent',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        DividendsPayable.append(ARCHvalue)
                                                r = r + 1
                                            tb.DividendsPayable = -sum(DividendsPayable)
                                        except:
                                            pass
                                        #
                                        # short term portion of long term debt
                                        try:
                                            ShortTermPortionOfLongTermDebt = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > AssetsRank:
                                                    if r < CurrentLiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'Debt',
                                                            'CorporateBorrowings',
                                                            'Loan',
                                                        ]
                                                        b = [
                                                            'Asset',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        ShortTermPortionOfLongTermDebt.append(ARCHvalue)
                                                r = r + 1
                                            tb.ShortTermPortionOfLongTermDebt = -sum(ShortTermPortionOfLongTermDebt)
                                        except:
                                            pass
                                        #
                                        # ML
                                        try:
                                            w = None
                                            a.CurrentLiabilitiesGL_i = ''
                                            m = None
                                            a.CurrentLiabilitiesGL_ii = ''
                                            t = None
                                            a.CurrentLiabilitiesGL_iii = ''
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > AssetsRank:
                                                    if r < CurrentLiabilitiesRank:
                                                        d = key
                                                        b = [
                                                            'Total',
                                                        ]
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = 0
                                                                while BalanceSheet[key][i] == None:
                                                                    i = i + 1
                                                                ARCHvalue = BalanceSheet[key][i]
                                                                BalanceSheet[key][i] = None
                                                            except:
                                                                if BalanceSheet[key] != None:
                                                                    ARCHvalue = BalanceSheet[key]
                                                                    BalanceSheet[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                try:
                                                                    #
                                                                    if w is None:
                                                                        a.CurrentLiabilitiesGL_i = d
                                                                        w = ''
                                                                    #
                                                                    elif m is None:
                                                                        a.CurrentLiabilitiesGL_ii = d
                                                                        m = ''
                                                                    #
                                                                    elif t is None:
                                                                        a.CurrentLiabilitiesGL_iii = d
                                                                        t = ''
                                                                    else:
                                                                        pass
                                                                    #
                                                                    if d not in CurrentLiabilitiesGL:
                                                                        CurrentLiabilitiesGL.append(d)
                                                                    #
                                                                except:
                                                                    pass
                                                r = r + 1
                                        except:
                                            pass
                                        #
                                        # dataframe                        
                                        try:
                                            df = pd.DataFrame({
                                                #
                                                '..': 
                                                    #
                                                    ['tb.AccountsPayableAndAccruedLiabilities',
                                                    'tb.EmployeeCompensationCurrent',
                                                    'tb.OperatingLeasesCurrent',
                                                    'tb.FinanceLeasesCurrent',
                                                    'tb.AccruedTaxLiabilities',
                                                    'tb.DeferredTaxLiabilitiesCurrent',
                                                    'tb.DeferredRevenueAndDepositsCurrent',
                                                    'tb.CommercialPapers',
                                                    'tb.ShortTermBorrowings',
                                                    'tb.OtherCurrentLiabilities',
                                                    'tb.DiscontinuedOperationsLiabilitiesCurrent',
                                                    'tb.DividendsPayable',
                                                    'tb.ShortTermPortionOfLongTermDebt'],
                                                #
                                                '.':
                                                    #
                                                    ['{:,}'.format(tb.AccountsPayableAndAccruedLiabilities),
                                                    '{:,}'.format(tb.EmployeeCompensationCurrent),
                                                    '{:,}'.format(tb.OperatingLeasesCurrent),
                                                    '{:,}'.format(tb.FinanceLeasesCurrent),
                                                    '{:,}'.format(tb.AccruedTaxLiabilities),
                                                    '{:,}'.format(tb.DeferredTaxLiabilitiesCurrent),
                                                    '{:,}'.format(tb.DeferredRevenueAndDepositsCurrent),
                                                    '{:,}'.format(tb.CommercialPapers),
                                                    '{:,}'.format(tb.ShortTermBorrowings),
                                                    '{:,}'.format(tb.OtherCurrentLiabilities),
                                                    '{:,}'.format(tb.DiscontinuedOperationsLiabilitiesCurrent),
                                                    '{:,}'.format(tb.DividendsPayable),
                                                    '{:,}'.format(tb.ShortTermPortionOfLongTermDebt)],
                                            })
                                            print(df)
                                            print(137 * '-' + '\n')
                                        except:
                                            pass
                                    except:
                                        pass
                                    #                   
                                    # non-current liabilities components
                                    try:
                                        #
                                        print(e.EntityRegistrantName)
                                        print('non-current liabilities')
                                        print(periodenddate)
                                        print(137 * '-' + '\n')
                                        #
                                        # long-term debt
                                        try:
                                            LongTermDebt = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentLiabilitiesRank:
                                                    if r < LiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'Debt',
                                                            'CorporateBorrowings',
                                                            'Loan',
                                                            'NotePayable',
                                                            'NotesPayable',
                                                        ]
                                                        b = [
                                                            'Asset',
                                                            'Short',
                                                            'FaceValueOfLongTermDebtIncludingObligationsUnderCapitalLeasesAndFinancingObligations',
                                                            'AdjustmentToReflectFairValueInterestRateHedges',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        LongTermDebt.append(ARCHvalue)
                                                r = r + 1
                                            tb.LongTermDebt = -sum(LongTermDebt)
                                        except:
                                            pass
                                        #
                                        # preferred shares
                                        try:
                                            PreferredSharesLiability = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentLiabilitiesRank:
                                                    if r < LiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'PreferredShare',
                                                            'PreferredStock',
                                                        ]
                                                        b = [
                                                            'Asset',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        PreferredSharesLiability.append(ARCHvalue)
                                                r = r + 1
                                            tb.PreferredSharesLiability = -sum(PreferredSharesLiability)
                                        except:
                                            pass
                                        #
                                        # retirement benefits
                                        try:
                                            RetirementBenefits = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentLiabilitiesRank:
                                                    if r < LiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'Pension',
                                                            'PostretirementBenefit',
                                                            'RetirementBenefit',
                                                        ]
                                                        b = [
                                                            'Asset',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        RetirementBenefits.append(ARCHvalue)
                                                r = r + 1
                                            tb.RetirementBenefits = -sum(RetirementBenefits)
                                        except:
                                            pass
                                        #
                                        # finance leases non-current
                                        try:
                                            FinanceLeasesNonCurrent = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentLiabilitiesRank:
                                                    if r < LiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'FinanceLease',
                                                            'CapitalLease',
                                                            'FinancingLease',
                                                            'FinancingObligation',
                                                            'Rent',
                                                        ]
                                                        b = [
                                                            'Asset',
                                                            'Debt',
                                                            'Right',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        FinanceLeasesNonCurrent.append(ARCHvalue)
                                                r = r + 1
                                            tb.FinanceLeasesNonCurrent = -sum(FinanceLeasesNonCurrent)
                                        except:
                                            pass
                                        #
                                        # operating leases non-current
                                        try:
                                            OperatingLeasesNonCurrent = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentLiabilitiesRank:
                                                    if r < LiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'Lease',
                                                            'Rent',
                                                        ]
                                                        b = [
                                                            'Asset',
                                                            'Buildings',
                                                            'Debt',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        OperatingLeasesNonCurrent.append(ARCHvalue)
                                                r = r + 1
                                            tb.OperatingLeasesNonCurrent = -sum(OperatingLeasesNonCurrent)
                                        except:
                                            pass
                                        #
                                        # lease incentive obligation
                                        try:
                                            LeaseIncentiveObligation = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentLiabilitiesRank:
                                                    if r < LiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'LeaseIncentive',
                                                        ]
                                                        b = [
                                                            'Asset',
                                                            'Debt',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        LeaseIncentiveObligation.append(ARCHvalue)
                                                r = r + 1
                                            tb.LeaseIncentiveObligation = -sum(LeaseIncentiveObligation)
                                        except:
                                            pass
                                        #
                                        # deferred revenue and deposits non-current
                                        try:
                                            DeferredRevenueAndDepositsNonCurrent = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentLiabilitiesRank:
                                                    if r < LiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'DeferredRevenue',
                                                            'ContractLiabilities',
                                                            'Guarantee',
                                                            'Warrant',
                                                        ]
                                                        b = [
                                                            'Asset',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        DeferredRevenueAndDepositsNonCurrent.append(ARCHvalue)
                                                r = r + 1
                                            tb.DeferredRevenueAndDepositsNonCurrent = -sum(DeferredRevenueAndDepositsNonCurrent)
                                        except:
                                            pass
                                        #
                                        # contingent consideration
                                        try:
                                            ContingentConsideration = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentLiabilitiesRank:
                                                    if r < LiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'Contingent',
                                                        ]
                                                        b = [
                                                            'Asset',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        ContingentConsideration.append(ARCHvalue)
                                                r = r + 1
                                            tb.ContingentConsideration = -sum(ContingentConsideration)
                                        except:
                                            pass
                                        #
                                        # Accrued Tax Liabilities Non Current
                                        try:
                                            AccruedTaxLiabilitiesNonCurrent = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentLiabilitiesRank:
                                                    if r < LiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'IncomeTaxes',
                                                            'LongTermIncomeTaxes',
                                                            'Tax',
                                                        ]
                                                        b = [
                                                            'Deferred',
                                                            'LongTerm',
                                                            'Warrant',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        AccruedTaxLiabilitiesNonCurrent.append(ARCHvalue)
                                                r = r + 1
                                            tb.AccruedTaxLiabilitiesNonCurrent = -sum(AccruedTaxLiabilitiesNonCurrent)
                                        except:
                                            pass
                                        #
                                        # deferred Tax Liabilities Non Current
                                        try:
                                            DeferredTaxLiabilitiesNonCurrent = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentLiabilitiesRank:
                                                    if r < LiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'DeferredIncomeTax',
                                                            'DeferredTax',
                                                            'TransitionTaxLiability',
                                                        ]
                                                        b = [
                                                            'Asset',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        DeferredTaxLiabilitiesNonCurrent.append(ARCHvalue)
                                                r = r + 1
                                            tb.DeferredTaxLiabilitiesNonCurrent = -sum(DeferredTaxLiabilitiesNonCurrent)
                                        except:
                                            pass
                                        #
                                        # other non-current liabilities
                                        try:
                                            OtherNonCurrentLiabilities = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentLiabilitiesRank:
                                                    if r < LiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'ExhibitorServices',
                                                            'OtherLongTermLiabilit',
                                                            'OtherNonCurrentLiabilit',
                                                            'OtherNoncurrentLiabilit',
                                                            'OtherLiabilities',
                                                        ]
                                                        b = [
                                                            'Asset',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        OtherNonCurrentLiabilities.append(ARCHvalue)
                                                r = r + 1
                                            tb.OtherNonCurrentLiabilities = -sum(OtherNonCurrentLiabilities)
                                        except:
                                            pass
                                        #
                                        # redeemable non controlling interests
                                        try:
                                            RedeemableNonControllingInterests = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentLiabilitiesRank:
                                                    if r < LiabilitiesRank:
                                                        d = key
                                                        print(d)
                                                        q = [
                                                            'NoncontrollingInterest',
                                                            'NonControllingInterest',
                                                        ]
                                                        b = [
                                                            'Asset',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        RedeemableNonControllingInterests.append(ARCHvalue)
                                                r = r + 1
                                            tb.RedeemableNonControllingInterests = -sum(RedeemableNonControllingInterests)
                                        except:
                                            pass
                                        #
                                        # discontinued operation non current liabilities
                                        try:
                                            DiscontinuedOperationsLiabilitiesNonCurrent = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentLiabilitiesRank:
                                                    if r < LiabilitiesRank:
                                                        d = key
                                                        q = [
                                                            'DiscontinuedOperations',
                                                            'HeldForSale',
                                                        ]
                                                        b = [
                                                            'Asset',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        DiscontinuedOperationsLiabilitiesNonCurrent.append(ARCHvalue)
                                                r = r + 1
                                            tb.DiscontinuedOperationsLiabilitiesNonCurrent = -sum(DiscontinuedOperationsLiabilitiesNonCurrent)
                                        except:
                                            pass
                                        #
                                        # ML
                                        try:
                                            w = None
                                            a.NonCurrentLiabilitiesGL_i = ''
                                            m = None
                                            a.NonCurrentLiabilitiesGL_ii = ''
                                            t = None
                                            a.NonCurrentLiabilitiesGL_iii = ''
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > CurrentLiabilitiesRank:
                                                    if r < LiabilitiesRank:
                                                        d = key
                                                        b = [
                                                            'Total',
                                                        ]
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = 0
                                                                while BalanceSheet[key][i] == None:
                                                                    i = i + 1
                                                                ARCHvalue = BalanceSheet[key][i]
                                                                BalanceSheet[key][i] = None
                                                            except:
                                                                if BalanceSheet[key] != None:
                                                                    ARCHvalue = BalanceSheet[key]
                                                                    BalanceSheet[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                try:
                                                                    #
                                                                    if w is None:
                                                                        a.NonCurrentLiabilitiesGL_i = d
                                                                        w = ''
                                                                    #
                                                                    elif m is None:
                                                                        a.NonCurrentLiabilitiesGL_ii = d
                                                                        m = ''
                                                                    #
                                                                    elif t is None:
                                                                        a.NonCurrentLiabilitiesGL_iii = d
                                                                        t = ''
                                                                    else:
                                                                        pass
                                                                    #
                                                                    if d not in NonCurrentLiabilitiesGL:
                                                                        NonCurrentLiabilitiesGL.append(d)
                                                                    #
                                                                except:
                                                                    pass
                                                r = r + 1
                                        except:
                                            pass
                                        #
                                        # dataframe
                                        try:
                                            df = pd.DataFrame({
                                                #
                                                '..': 
                                                    #
                                                    ['tb.LongTermDebt',
                                                    'tb.PreferredSharesLiability',
                                                    'tb.RetirementBenefits',
                                                    'tb.OperatingLeasesNonCurrent',
                                                    'tb.LeaseIncentiveObligation',
                                                    'tb.FinanceLeasesNonCurrent',
                                                    'tb.DeferredRevenueAndDepositsNonCurrent',
                                                    'tb.ContingentConsideration',
                                                    'tb.AccruedTaxLiabilitiesNonCurrent',
                                                    'tb.DeferredTaxLiabilitiesNonCurrent',
                                                    'tb.OtherNonCurrentLiabilities',
                                                    'tb.RedeemableNonControllingInterests',
                                                    'tb.DiscontinuedOperationsLiabilitiesNonCurrent'],
                                                #
                                                '.':
                                                    #
                                                    ['{:,}'.format(tb.LongTermDebt),
                                                    '{:,}'.format(tb.PreferredSharesLiability),
                                                    '{:,}'.format(tb.RetirementBenefits),
                                                    '{:,}'.format(tb.OperatingLeasesNonCurrent),
                                                    '{:,}'.format(tb.LeaseIncentiveObligation),
                                                    '{:,}'.format(tb.FinanceLeasesNonCurrent),
                                                    '{:,}'.format(tb.DeferredRevenueAndDepositsNonCurrent),
                                                    '{:,}'.format(tb.ContingentConsideration),
                                                    '{:,}'.format(tb.AccruedTaxLiabilitiesNonCurrent),
                                                    '{:,}'.format(tb.DeferredTaxLiabilitiesNonCurrent),
                                                    '{:,}'.format(tb.OtherNonCurrentLiabilities),
                                                    '{:,}'.format(tb.RedeemableNonControllingInterests),
                                                    '{:,}'.format(tb.DiscontinuedOperationsLiabilitiesNonCurrent)],
                                            })
                                            print(df)
                                            print(137 * '-' + '\n')
                                        except:
                                            pass
                                    except:
                                        pass
                                    #                   
                                    # shareholders' equity components
                                    try:
                                        print(e.EntityRegistrantName)
                                        print('shareholders equity - balance sheets')
                                        print(periodenddate)
                                        print(137 * '-' + '\n')
                                        #
                                        # convertible debt
                                        try:
                                            ConvertibleDebt = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > LiabilitiesRank:
                                                    d = key
                                                    q = [
                                                        'ConvertibleDebt',
                                                    ]
                                                    b = [
                                                        'AdditionalCapital',
                                                        'AdditionalPaidInCapital',
                                                        'CapitalInExcessOfParValue',
                                                        'CapitalSurplus',
                                                        'CommonShares',
                                                        'CommonStock',
                                                        'OrdinaryShares',
                                                        'Surplus',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while BalanceSheet[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = BalanceSheet[key][i]
                                                                    BalanceSheet[key][i] = None
                                                                except:
                                                                    if value != None:
                                                                        ARCHvalue = BalanceSheet[key]
                                                                        BalanceSheet[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    ConvertibleDebt.append(ARCHvalue)
                                                r = r + 1
                                            a.ConvertibleDebt = -sum(ConvertibleDebt)
                                        except:
                                            pass
                                        #
                                        # common shares
                                        try:
                                            CommonShares = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > LiabilitiesRank:
                                                    d = key
                                                    q = [
                                                        'AdditionalCapital',
                                                        'AdditionalPaidInCapital',
                                                        'CapitalInExcessOfParValue',
                                                        'CapitalSurplus',
                                                        'CommonShares',
                                                        'CommonStock',
                                                        'OrdinaryShares',
                                                        'Surplus',
                                                    ]
                                                    b = [
                                                        'Asset',
                                                        'Dividend',
                                                        'Liabilit',
                                                        'Obligation',
                                                        'Treasury',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while BalanceSheet[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = BalanceSheet[key][i]
                                                                    BalanceSheet[key][i] = None
                                                                except:
                                                                    if value != None:
                                                                        ARCHvalue = BalanceSheet[key]
                                                                        BalanceSheet[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    CommonShares.append(ARCHvalue)
                                                r = r + 1
                                            a.CommonShares = -sum(CommonShares)
                                        except:
                                            pass
                                        #
                                        # retained earnings
                                        try:
                                            RetainedEarnings = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > LiabilitiesRank:
                                                    if r < LiabilitiesAndShareholdersEquityRank:
                                                        d = key
                                                        q = [
                                                            'Earning',
                                                            'AccumulatedDeficit',
                                                            'RetainedDeficit',
                                                        ]
                                                        b = [
                                                            'Asset',
                                                            'Liabilit',
                                                            'Obligation',
                                                            'Treasury',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        RetainedEarnings.append(ARCHvalue)
                                                r = r + 1
                                            a.RetainedEarnings = -sum(RetainedEarnings)
                                        except:
                                            pass
                                        #
                                        # accumulated other comprehensive income
                                        try:
                                            AccumulatedOtherComprehensiveIncome = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > LiabilitiesRank:
                                                    if r < LiabilitiesAndShareholdersEquityRank:
                                                        d = key
                                                        q = [
                                                            'AccumulatedOtherComprehensive',
                                                            'Accumulatedothercomprehensiveincome',
                                                        ]
                                                        b = [
                                                            'Asset',
                                                            'Liabilit',
                                                            'Obligation',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        AccumulatedOtherComprehensiveIncome.append(ARCHvalue)
                                                r = r + 1
                                            a.AccumulatedOtherComprehensiveIncome = -sum(AccumulatedOtherComprehensiveIncome)
                                        except:
                                            pass
                                        #
                                        # treasury shares
                                        try:
                                            TreasuryShares = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > LiabilitiesRank:
                                                    if r < LiabilitiesAndShareholdersEquityRank:
                                                        d = key
                                                        q = [
                                                            'Treasury',
                                                        ]
                                                        b = [
                                                            'Asset',
                                                            'Employee',
                                                            'Liabilit',
                                                            'NonControlling',
                                                            'Noncontrolling',
                                                            'Obligation',
                                                            'RetainedEarnings',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        TreasuryShares.append(ARCHvalue)
                                                r = r + 1
                                            a.TreasuryShares = -sum(TreasuryShares)
                                        except:
                                            pass
                                        #
                                        # employee benefit trust
                                        try:
                                            EmployeeBenefitTrust = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > LiabilitiesRank:
                                                    if r < LiabilitiesAndShareholdersEquityRank:
                                                        d = key
                                                        q = [
                                                            'EmployeeBenefit',
                                                            'Trust',
                                                        ]
                                                        b = [
                                                            'Asset',
                                                            'Liabilit',
                                                            'Obligation',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        EmployeeBenefitTrust.append(ARCHvalue)
                                                r = r + 1
                                            a.EmployeeBenefitTrust = -sum(EmployeeBenefitTrust)
                                        except:
                                            pass
                                        #
                                        # non controlling interests
                                        try:
                                            NonControllingInterests = []
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > LiabilitiesRank:
                                                    if r < LiabilitiesAndShareholdersEquityRank:
                                                        d = key
                                                        print(d)
                                                        q = [
                                                            'NoncontrollingInterest',
                                                            'NonControllingInterest',
                                                        ]
                                                        b = [
                                                            'Asset',
                                                            'Liabilit',
                                                            'Obligation',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while BalanceSheet[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = BalanceSheet[key][i]
                                                                        BalanceSheet[key][i] = None
                                                                    except:
                                                                        if BalanceSheet[key] != None:
                                                                            ARCHvalue = BalanceSheet[key]
                                                                            BalanceSheet[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        NonControllingInterests.append(ARCHvalue)
                                                r = r + 1
                                            a.NonControllingInterests = -sum(NonControllingInterests)
                                        except:
                                            pass
                                        #
                                        # ML
                                        try:
                                            w = None
                                            a.ShareholdersEquityGL_i = ''
                                            m = None
                                            a.ShareholdersEquityGL_ii = ''
                                            t = None
                                            a.ShareholdersEquityGL_iii = ''
                                            r = 0
                                            for key, value in BalanceSheet.items():
                                                if r > LiabilitiesRank:
                                                    if r < LiabilitiesAndShareholdersEquityRank:
                                                        d = key
                                                        b = [
                                                            'Total',
                                                            'Beginning',
                                                            'Ending',
                                                            'BalancesAt',
                                                        ]
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = 0
                                                                while BalanceSheet[key][i] == None:
                                                                    i = i + 1
                                                                ARCHvalue = BalanceSheet[key][i]
                                                                BalanceSheet[key][i] = None
                                                            except:
                                                                if BalanceSheet[key] != None:
                                                                    ARCHvalue = BalanceSheet[key]
                                                                    BalanceSheet[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                try:
                                                                    #
                                                                    if w is None:
                                                                        a.ShareholdersEquityGL_i = d
                                                                        w = ''
                                                                    #
                                                                    elif m is None:
                                                                        a.ShareholdersEquityGL_ii = d
                                                                        m = ''
                                                                    #
                                                                    elif t is None:
                                                                        a.ShareholdersEquityGL_iii = d
                                                                        t = ''
                                                                    else:
                                                                        pass
                                                                    #
                                                                    if d not in ShareholdersEquityGL:
                                                                        ShareholdersEquityGL.append(d)
                                                                    #
                                                                except:
                                                                    pass
                                                r = r + 1
                                        except:
                                            pass
                                        #
                                        # dataframe
                                        try:
                                            df = pd.DataFrame({
                                                #
                                                '..': 
                                                    #
                                                    ['a.ConvertibleDebt',
                                                    'a.CommonShares',
                                                    'a.RetainedEarnings',
                                                    'a.AccumulatedOtherComprehensiveIncome',
                                                    'a.TreasuryShares',
                                                    'a.EmployeeBenefitTrust',
                                                    'a.NonControllingInterests'],
                                                #
                                                '.':
                                                    #
                                                    ['{:,}'.format(a.ConvertibleDebt),
                                                    '{:,}'.format(a.CommonShares),
                                                    '{:,}'.format(a.RetainedEarnings),
                                                    '{:,}'.format(a.AccumulatedOtherComprehensiveIncome),
                                                    '{:,}'.format(a.TreasuryShares),
                                                    '{:,}'.format(a.EmployeeBenefitTrust),
                                                    '{:,}'.format(a.NonControllingInterests)],
                                            })
                                            print(df)
                                            print(137 * '-' + '\n')
                                        except:
                                            pass
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # income statement
                                try:
                                    print(e.EntityRegistrantName)
                                    print('income statement')
                                    print(periodenddate)
                                    print(137 * '-' + '\n')
                                    #
                                    # net income
                                    try:
                                        NetIncome = []
                                        NetIncomeRank = None
                                        r = 0
                                        s = 'a'
                                        for key, value in IncomeStatement.items():
                                            d = key
                                            q = [
                                                'Loss',
                                                'NetIncome',
                                                'NetEarning',
                                            ]
                                            b = [
                                                'Before',
                                                'Benefit',
                                                'ContinuingOp',
                                                'Cost',
                                                'CreditLosses',
                                                'DiscontinuedOp',
                                                'Disposal',
                                                'Equity',
                                                'Extinguishment',
                                                'ForeignCurrency',
                                                'FromOperations',
                                                'Gain',
                                                'NonConsolidated',
                                                'Marketable',
                                                'Miscellaneous',
                                                'Opera',
                                                'Other',
                                                'PerShare',
                                                'Provisions',
                                                'Research',
                                                'Revenue',
                                                'Sale',
                                                'Securities',
                                                'Tax',
                                                'Unrealized',
                                            ]
                                            for l in q:
                                                if s == 'a':
                                                    if l in d:
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = 0
                                                                while IncomeStatement[key][i] == None:
                                                                    i = i + 1
                                                                ARCHvalue = IncomeStatement[key][i]
                                                                IncomeStatement[key][i] = None
                                                            except:
                                                                if IncomeStatement[key] != None:
                                                                    ARCHvalue = IncomeStatement[key]
                                                                    IncomeStatement[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                NetIncome.append(ARCHvalue)
                                                                s = 'z'
                                                                NetIncomeRank = r
                                                                print(d)
                                                                print('{:,}'.format(value))
                                            r = r + 1
                                        a.NetIncome = -sum(NetIncome)
                                    except:
                                        pass
                                    #
                                    # gross margin
                                    try:
                                        GrossMargin = []
                                        GrossMarginRank = 10
                                        r = 0
                                        for key, value in IncomeStatement.items():
                                            if r < NetIncomeRank:
                                                d = key
                                                q = [
                                                    'Gross',
                                                ]
                                                b = [
                                                    'DiscontinuedOperation',
                                                ]
                                                for l in q:
                                                    if l in d:
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = 0
                                                                while IncomeStatement[key][i] == None:
                                                                    i = i + 1
                                                                ARCHvalue = value[i]
                                                                IncomeStatement[key][i] = None
                                                            except:
                                                                if IncomeStatement[key] != None:
                                                                    ARCHvalue = IncomeStatement[key]
                                                                    IncomeStatement[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                GrossMargin.append(ARCHvalue)
                                                                GrossMarginRank = r
                                            r = r + 1
                                        a.GrossMargin = -abs(sum(GrossMargin))
                                    except:
                                        pass
                                    #
                                    # total sales
                                    try:
                                        Sales = []
                                        SalesRank = None
                                        r = 0
                                        for key, value in IncomeStatement.items():
                                            if r < NetIncomeRank:
                                                if r < GrossMarginRank:
                                                        d = key
                                                        q = [
                                                            'TotalNetRevenue',
                                                            'TotalRevenue',
                                                            'TotalSales',
                                                        ]
                                                        b = [
                                                            'Cost',
                                                            'MarketingAndSales',
                                                        ]
                                                        s = 'a'
                                                        for l in q:
                                                            if s == 'a':
                                                                if l in d:
                                                                    h = 'p'
                                                                    for p in b:
                                                                        u = 0
                                                                        while u < len(b):
                                                                            if p in d:
                                                                                h = ''
                                                                            u = u + 1
                                                                    if h == 'p':
                                                                        try:
                                                                            i = 0
                                                                            while IncomeStatement[key][i] == None:
                                                                                i = i + 1
                                                                            ARCHvalue = IncomeStatement[key][i]
                                                                            IncomeStatement[key][i] = None
                                                                        except:
                                                                            if IncomeStatement[key] != None:
                                                                                ARCHvalue = IncomeStatement[key]
                                                                                IncomeStatement[key] = None
                                                                            else:
                                                                                ARCHvalue = 0
                                                                        if ARCHvalue != 0:
                                                                            Sales.append(ARCHvalue)
                                                                            s = 'z'
                                            r = r + 1
                                        a.Sales = -sum(Sales)
                                    except:
                                        pass
                                    #
                                    # total cost of sales
                                    try:
                                        CostOfSales = []
                                        r = 0
                                        CostOfSalesRank = None
                                        for key, value in IncomeStatement.items():
                                            if r < NetIncomeRank:
                                                if r < GrossMarginRank:
                                                    d = key
                                                    q = [
                                                        'Amortization',
                                                        'CostOfSales',
                                                        'CostOfRevenues',
                                                        'Depreciation',
                                                        'FilmExhibitionCost',
                                                        'FoodAndBeverageCost',
                                                        'InformationTechnology',
                                                        'Merchandise',
                                                        'Occupancy',
                                                        'Payroll',
                                                        'Personel',
                                                        'Product',
                                                        'Rent',
                                                        'Services',
                                                        'TotalCost',
                                                        'TotalNetCost',
                                                    ]
                                                    b = [
                                                        'Administrative',
                                                        'ResearchAndDevelopment',
                                                        'CostsOfSoftware',
                                                        'CostAndExpenses',
                                                        'CostsAndExpenses',
                                                        'CostsExpensesAndOther',
                                                        'CostOfProduct',
                                                        'CostOfSales',
                                                        'CostOfService',
                                                        'Funded',
                                                        'Income',
                                                        'Interest',
                                                        'OperatingExpenses',
                                                        'Marketing',
                                                        'MergerAcquisition',
                                                        'ProductSale',
                                                        'Restructuring',
                                                        'SalesAndOtherExpenses',
                                                        'TotalRevenue',
                                                    ]
                                                    s = 'a'
                                                    for l in q:
                                                        if s == 'a':
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while IncomeStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = IncomeStatement[key][i]
                                                                        IncomeStatement[key][i] = None
                                                                    except:
                                                                        if IncomeStatement[key] != None:
                                                                            ARCHvalue = IncomeStatement[key]
                                                                            IncomeStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        CostOfSales.append(abs(ARCHvalue))
                                                                        CostOfSalesRank = r
                                                                        s = 'z'
                                                                        print(d)
                                                                        print('{:,}'.format(value))
                                            r = r + 1
                                        a.CostOfSales = sum(CostOfSales)
                                    except:
                                        pass  
                                    #
                                    # total operating income
                                    try:
                                        OperatingIncome = []
                                        OperatingIncomeRank = None
                                        r = 0
                                        for key, value in IncomeStatement.items():
                                            if r < NetIncomeRank:
                                                d = key
                                                q = [
                                                    'EarningsFromOperations',
                                                    'IncomeFromOperations',
                                                    'LossFromOperations',
                                                    '(Loss)FromOperations',
                                                    '(Losses)FromOperations',
                                                    'OperatingEarnings',
                                                    'OperatingIncome',
                                                    'OperatingProfit',
                                                    'OperatingLoss',
                                                    'Operating(Loss)',
                                                ]
                                                b = [
                                                    'DiscontinuedOperation',
                                                    'OtherOperating',
                                                    'Research',
                                                ]
                                                for l in q:
                                                    if l in d:
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = 0
                                                                while IncomeStatement[key][i] == None:
                                                                    i = i + 1
                                                                ARCHvalue = IncomeStatement[key][i]
                                                                IncomeStatement[key][i] = None
                                                            except:
                                                                if IncomeStatement[key] != None:
                                                                    ARCHvalue = IncomeStatement[key]
                                                                    IncomeStatement[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                OperatingIncome.append(ARCHvalue)
                                                                OperatingIncomeRank = r
                                            r = r + 1
                                        a.OperatingIncome = -sum(OperatingIncome)
                                    except:
                                        pass
                                    #
                                    # Operating income rank based on net income rank
                                    try:
                                        if OperatingIncomeRank is None:
                                            TempOperatingIncomeRank = NetIncomeRank - 7
                                            OperatingIncomeRank = TempOperatingIncomeRank
                                    except:
                                        print('Could not attribute Operating Income Rank to Net Income Rank')
                                    #
                                    # income before taxes
                                    try:
                                        IncomeBeforeTaxes = []
                                        IncomeBeforeTaxesRank = None
                                        r = 0
                                        for key, value in IncomeStatement.items():
                                            if r < NetIncomeRank:
                                                if r > OperatingIncomeRank:
                                                    d = key
                                                    q = [
                                                        'BeforeIncomeTax',
                                                        'BeforeProvisionForIncome',
                                                        'BeforeProvisionFor(BenefitFrom)IncomeTax',
                                                        'BeforeTax',
                                                    ]
                                                    b = [
                                                        'DiscontinuedOperation',
                                                        'Research',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while IncomeStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = IncomeStatement[key][i]
                                                                    IncomeStatement[key][i] = None
                                                                except:
                                                                    if IncomeStatement[key] != None:
                                                                        ARCHvalue = value
                                                                        IncomeStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    IncomeBeforeTaxes.append(ARCHvalue)
                                                                    IncomeBeforeTaxesRank = r
                                                                    print(d)
                                                                    print('{:,}'.format(value))
                                            r = r + 1
                                        a.IncomeBeforeTaxes = -sum(IncomeBeforeTaxes)
                                    except:
                                        pass
                                    #
                                    # Operating income rank based on income before taxes
                                    try:
                                        if OperatingIncomeRank == TempOperatingIncomeRank:
                                            OperatingIncomeRank = IncomeBeforeTaxesRank
                                    except:
                                        pass
                                    #
                                    # net Income From Discontinued Operations
                                    try:
                                        NetIncomeFromDiscontinuedOperations = []
                                        r = 0
                                        NetIncomeFromDiscontinuedOperationsRank = None
                                        for key, value in IncomeStatement.items():
                                            if r < NetIncomeRank:
                                                d = key
                                                q = [
                                                    'DiscontinuedOperation',
                                                ]
                                                b = [
                                                    'Research',
                                                    'PerShare',
                                                ]
                                                for l in q:
                                                    if l in d:
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = 0
                                                                while IncomeStatement[key][i] == None:
                                                                    i = i + 1
                                                                ARCHvalue = IncomeStatement[key][i]
                                                                IncomeStatement[key][i] = None
                                                            except:
                                                                if IncomeStatement[key] != None:
                                                                    ARCHvalue = IncomeStatement[key]
                                                                    IncomeStatement[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                NetIncomeFromDiscontinuedOperations.append(ARCHvalue)
                                                                NetIncomeFromDiscontinuedOperationsRank = r
                                            r = r + 1
                                        tb.NetIncomeFromDiscontinuedOperations = -sum(NetIncomeFromDiscontinuedOperations)
                                    except:
                                        pass
                                    #
                                    # sales components
                                    try:
                                        Sales = []
                                        r = 0
                                        TotalRevenueRank = 10
                                        for key, value in IncomeStatement.items():
                                            if r < NetIncomeRank:
                                                if r < GrossMarginRank:
                                                        d = key
                                                        q = [
                                                            'Admissions',
                                                            'Advertising',
                                                            'AgencyRevenue',
                                                            'AutomotiveRevenue',
                                                            'BiocatalystResearchAndDevelopment',
                                                            'Financing',
                                                            'Funded',
                                                            'Food',
                                                            'Membership',
                                                            'MerchantRevenue',
                                                            'NetSales',
                                                            'Product',
                                                            'ResearchAndDevelopmentRevenue',
                                                            'RentalIncome',
                                                            'Revenue',
                                                            'Sales',
                                                            'Services',
                                                            'Theatre',
                                                        ]
                                                        b = [
                                                            'Cost',
                                                            'DiscontinuedOperation',
                                                            'ExciseTaxes',
                                                            'MarketingAndSales',
                                                        ]
                                                        c = [
                                                            'TotalRevenue',
                                                            'TotalNetRevenue',
                                                        ]
                                                        s = 'a'
                                                        for l in q:
                                                            if s == 'a':
                                                                if l in d:
                                                                    h = 'p'
                                                                    for p in b:
                                                                        u = 0
                                                                        while u < len(b):
                                                                            if p in d:
                                                                                h = ''
                                                                            for f in c:
                                                                                if f in d:
                                                                                    TotalRevenueRank = r
                                                                            u = u + 1
                                                                    if r < TotalRevenueRank:
                                                                        if h == 'p':
                                                                            try:
                                                                                i = 0
                                                                                while IncomeStatement[key][i] == None:
                                                                                    i = i + 1
                                                                                ARCHvalue = IncomeStatement[key][i]
                                                                                IncomeStatement[key][i] = None
                                                                            except:
                                                                                if IncomeStatement[key] != None:
                                                                                    ARCHvalue = IncomeStatement[key]
                                                                                    IncomeStatement[key] = None
                                                                                else:
                                                                                    ARCHvalue = 0
                                                                            if ARCHvalue != 0:
                                                                                Sales.append(ARCHvalue)
                                                                                s = 'z'
                                            r = r + 1
                                        tb.Sales = -sum(Sales)
                                    except:
                                        pass
                                    #
                                    # debugging sales
                                    try:
                                        if tb.Sales == 0:
                                            tb.Sales = a.Sales
                                        #
                                        if a.Sales == 0:
                                            a.Sales = tb.Sales
                                    except:
                                        pass
                                    #
                                    # cost of sales components
                                    try:
                                        CostOfSales = []
                                        r = 0
                                        TotalCostRank = 10
                                        for key, value in IncomeStatement.items():
                                            if r < NetIncomeRank:
                                                if r < GrossMarginRank:
                                                    d = key
                                                    q = [
                                                        'Cost',
                                                        'Merchandise',
                                                        'Payroll',
                                                        'Personnel',
                                                        'Product',
                                                        'Rent',
                                                        'Sales',
                                                        'Services',
                                                    ]
                                                    b = [
                                                        'BiocatalystProductSales',
                                                        'BiocatalystResearchAndDevelopment',
                                                        'CostAndExpenses',
                                                        'CostsAndExpenses',
                                                        'CostsExpensesAndOther',
                                                        'CostOfSalesOperatingExpensesAndOther',
                                                        'Funded',
                                                        'OtherCosts',
                                                        'MarketingAndSales',
                                                        'Merger',
                                                        'ProductSale',
                                                        'Restructuring',
                                                        'SalesAndOtherExpenses',
                                                        'TotalOperatingExpenses',
                                                        'TotalRevenue',
                                                    ]
                                                    c = [
                                                        'TotalCost',
                                                        'TotalNetCost',
                                                    ]
                                                    s = 'a'
                                                    for l in q:
                                                        if s == 'a':
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        for f in c:
                                                                            if f in d:
                                                                                TotalCostRank = r
                                                                                s = 'z'
                                                                        u = u + 1
                                                                if s == 'a':
                                                                    if r < TotalCostRank:
                                                                        if h == 'p':
                                                                            try:
                                                                                i = 0
                                                                                while IncomeStatement[key][i] == None:
                                                                                    i = i + 1
                                                                                ARCHvalue = IncomeStatement[key][i]
                                                                                IncomeStatement[key][i] = None
                                                                            except:
                                                                                if IncomeStatement[key] != None:
                                                                                    ARCHvalue = IncomeStatement[key]
                                                                                    IncomeStatement[key] = None
                                                                                else:
                                                                                    ARCHvalue = 0
                                                                            if ARCHvalue != 0:
                                                                                if r < TotalCostRank:
                                                                                    CostOfSales.append(ARCHvalue)
                                                                                    s = 'z'
                                                                                    print(d)
                                                                                    print('{:,}'.format(value))
                                            r = r + 1
                                        tb.CostOfSales = sum(CostOfSales)
                                    except:
                                        pass
                                    #
                                    # research and development
                                    try:
                                        ResearchAndDevelopment = []
                                        r = 0
                                        for key, value in IncomeStatement.items():
                                            if r < NetIncomeRank:
                                                if r < OperatingIncomeRank:
                                                    d = key
                                                    q = [
                                                        'Development',
                                                        'Engineering',
                                                        'Research',
                                                    ]
                                                    b = [
                                                        'DiscontinuedOperation',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while IncomeStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = IncomeStatement[key][i]
                                                                    IncomeStatement[key][i] = None
                                                                except:
                                                                    if IncomeStatement[key] != None:
                                                                        ARCHvalue = IncomeStatement[key]
                                                                        IncomeStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    ResearchAndDevelopment.append(ARCHvalue)
                                            r = r + 1
                                        tb.ResearchAndDevelopment = sum(ResearchAndDevelopment)
                                    except:
                                        pass
                                    #
                                    # selling general, administrative and marketing
                                    try:
                                        SellingGeneralAdministrativeAndMarketing = []
                                        r = 0
                                        for key, value in IncomeStatement.items():
                                            if r < NetIncomeRank:
                                                if r < OperatingIncomeRank:
                                                    d = key
                                                    q = [
                                                        'Acquisition',
                                                        'Administrative',
                                                        'AssociateIncentives',
                                                        'Amortization',
                                                        'Depreciation',
                                                        'Depletion',
                                                        'FinanceLease',
                                                        'InformationTechnology',
                                                        'MarketingAndSales',
                                                        'OperatingExpenses',
                                                        'ExpensesOperating',
                                                        'OperatingIncomeExpenses',
                                                        'Personnel',
                                                        'Marketing',
                                                        'SalesAndOtherExpense',
                                                    ]
                                                    b = [
                                                        'CostOfSales',
                                                        'CostsExpensesAndOther',
                                                        'DiscontinuedOperation',
                                                        'Interest',
                                                        'Impairment',
                                                        'LegalSettlement',
                                                        'Merger',
                                                        'NonOperating',
                                                        'OtherIncome',
                                                        'Other(Expense)',
                                                        'OtherNetIncome',
                                                        'OtherNetExpense',
                                                        'OtherNet(Income)',
                                                        'OtherNet(Expense)',
                                                        'Research',
                                                        'Restructuring',
                                                        'SpecialCharges',
                                                        'Total',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                if '(Income)' in d:
                                                                    y = -1
                                                                else:
                                                                    y = 1
                                                                try:
                                                                    i = 0
                                                                    while IncomeStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = abs(IncomeStatement[key][i]) * y
                                                                    IncomeStatement[key][i] = None
                                                                except:
                                                                    if IncomeStatement[key] != None:
                                                                        ARCHvalue = abs(IncomeStatement[key]) * y
                                                                        IncomeStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    SellingGeneralAdministrativeAndMarketing.append(ARCHvalue)
                                            r = r + 1
                                        tb.SellingGeneralAdministrativeAndMarketing = sum(SellingGeneralAdministrativeAndMarketing)
                                        #
                                        OperatingIncomeMethod = ''
                                        if a.OperatingIncome == 0:
                                            c = tb.Sales
                                            c = c + tb.CostOfSales
                                            c = c + tb.ResearchAndDevelopment
                                            c = c + tb.SellingGeneralAdministrativeAndMarketing
                                            a.OperatingIncome = c
                                            OperatingIncomeMethod = 'bridge'
                                    except:
                                        pass
                                    #
                                    # debugging gross margin
                                    if tb.CostOfSales == 0:
                                        if a.CostOfSales == 0:
                                            if a.GrossMargin == 0:
                                                #
                                                c = a.OperatingIncome
                                                c = c - tb.SellingGeneralAdministrativeAndMarketing
                                                c = c - tb.ResearchAndDevelopment
                                                a.GrossMargin = c
                                            # 
                                            c = a.GrossMargin - a.Sales
                                            a.CostOfSales = c
                                        #
                                        tb.CostOfSales = a.CostOfSales
                                    #
                                    # Asset Impairment, restructuring, and other special charges
                                    try:
                                        ImpairmentRestructuringAndOtherSpecialCharges = []
                                        ImpairmentRestructuringAndOtherSpecialChargesRank = None
                                        r = 0
                                        for key, value in IncomeStatement.items():
                                            if r < NetIncomeRank:
                                                if r > GrossMarginRank:
                                                    d = key
                                                    q = [
                                                        'Arbitration',
                                                        'Contingency',
                                                        'Disposal',
                                                        'ChangeInEstimates',
                                                        'ExtinguishmentOfDebt',
                                                        'GainOnSale',
                                                        '(Gain)OnSale',
                                                        'GainOnDisposal',
                                                        '(Gain)OnDisposal',
                                                        'Impairment',
                                                        'Litigation',
                                                        'LossOnSale',
                                                        '(Loss)OnSale',
                                                        'LossOnDisposal',
                                                        '(Loss)OnDisposal',
                                                        'Merger',
                                                        'Proceed',
                                                        'Restructuring',
                                                        'SaleOfAsset',
                                                        'SalesOfAsset',
                                                        'Special',
                                                        'Settlement',
                                                        'WriteOff',
                                                    ]
                                                    b = [
                                                        'DiscontinuedOperation',
                                                        'Investment',
                                                        'Research',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while IncomeStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = IncomeStatement[key][i]
                                                                    IncomeStatement[key][i] = None
                                                                except:
                                                                    if IncomeStatement[key] != None:
                                                                        ARCHvalue = IncomeStatement[key]
                                                                        IncomeStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    ImpairmentRestructuringAndOtherSpecialCharges.append(ARCHvalue)
                                                                    ImpairmentRestructuringAndOtherSpecialChargesRank = r
                                                                    print(d)
                                                                    print('{:,}'.format(value))
                                            r = r + 1
                                        tb.ImpairmentRestructuringAndOtherSpecialCharges = sum(ImpairmentRestructuringAndOtherSpecialCharges)
                                        #
                                        if ImpairmentRestructuringAndOtherSpecialChargesRank != None:
                                            if ImpairmentRestructuringAndOtherSpecialChargesRank < OperatingIncomeRank:
                                                if OperatingIncomeMethod == '':
                                                    c = a.OperatingIncome
                                                    c = c - tb.ImpairmentRestructuringAndOtherSpecialCharges
                                                    a.OperatingIncome = c
                                    except:
                                        pass
                                    #
                                    # non-operating income (expense)
                                    try:
                                        NonOperatingIncome = []
                                        r = 0
                                        for key, value in IncomeStatement.items():
                                            if r < NetIncomeRank:
                                                if r > GrossMarginRank:
                                                    d = key
                                                    q = [
                                                        'Borrowing',
                                                        'Debt',
                                                        'Exhibitor',
                                                        'Finance',
                                                        'Currency',
                                                        'Interest',
                                                        'Investment',
                                                        'Marketable',
                                                        'Securit',
                                                        'NonOperating',
                                                        'OtherIncome',
                                                        'OtherExpense',
                                                        'OtherNet(Income)',
                                                        'OtherNet(Expense)',
                                                        'OtherNetIncome',
                                                        'OtherNetExpense',
                                                    ]
                                                    b = [
                                                        'Contingency',
                                                        'Disposal',
                                                        'GainOnSale',
                                                        '(Gain)OnSale',
                                                        'GainOnDisposal',
                                                        '(Gain)OnDisposal',
                                                        'Impairment',
                                                        'ExtinguishmentOfDebt',
                                                        'Settlement',
                                                        'Merger',
                                                        'Restructuring',
                                                        'Special',
                                                        'WriteOff',
                                                        'LossOnSale',
                                                        '(Loss)OnSale',
                                                        'LossOnDisposal',
                                                        '(Loss)OnDisposal',
                                                        'Proceed',
                                                    ]
                                                    g = [
                                                        '(Income)',
                                                        '(Earnings)',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                y = 1
                                                                for f in g:
                                                                    if f in d:
                                                                        y = -1
                                                                try:
                                                                    i = 0
                                                                    while IncomeStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = abs(IncomeStatement[key][i]) * y
                                                                    IncomeStatement[key][i] = None
                                                                except:
                                                                    if IncomeStatement[key] != None:
                                                                        ARCHvalue = abs(IncomeStatement[key]) * y
                                                                        IncomeStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    NonOperatingIncome.append(ARCHvalue)
                                            r = r + 1
                                        tb.NonOperatingIncome = -sum(NonOperatingIncome)
                                    except:
                                        pass
                                    #
                                    # income tax expense benefit
                                    try:
                                        IncomeTaxExpenseBenefit = []
                                        r = 0
                                        for key, value in IncomeStatement.items():
                                            if r < NetIncomeRank:
                                                if r > IncomeBeforeTaxesRank:
                                                    d = key
                                                    q = [
                                                        'IncomeTax',
                                                        'ProvisionForTaxes',
                                                        'TaxItem',
                                                        'TaxReform',
                                                    ]
                                                    b = [
                                                        'DiscontinuedOperation',
                                                        'IncomeBefore',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while IncomeStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = IncomeStatement[key]
                                                                    IncomeStatement[key][i] = None
                                                                except:
                                                                    if IncomeStatement[key] != None:
                                                                        ARCHvalue = IncomeStatement[key]
                                                                        IncomeStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    if (a.NetIncome - tb.NetIncomeFromDiscontinuedOperations) > a.IncomeBeforeTaxes:
                                                                        y = 1
                                                                    else:
                                                                        y = -1
                                                                    ARCHvalue = abs(ARCHvalue) * y
                                                                    IncomeTaxExpenseBenefit.append(ARCHvalue)
                                            r = r + 1
                                        tb.IncomeTaxExpenseBenefit = sum(IncomeTaxExpenseBenefit)
                                    except:
                                        pass
                                    #
                                    # equity method investee's income
                                    try:
                                        EquityMethodInvesteesIncome = []
                                        r = 0
                                        for key, value in IncomeStatement.items():
                                            if r > IncomeBeforeTaxesRank :
                                                d = key
                                                q = [
                                                    'EquityInLossesOfInvestee',
                                                    'EquityIncome(loss)',
                                                    'EquityIn(Earnings)',
                                                    'EquityInNetIncome',
                                                    'EquityLoss',
                                                    'EquityMethodInvesteesIncome',
                                                ]
                                                b = [
                                                    'CostOfGoods',
                                                    'CostOfOperations',
                                                    'CostOfRevenue',
                                                    'CostOfSales',
                                                    'DiscontinuedOperation',
                                                    'Other',
                                                    'Miscellaneous',
                                                    'Research',
                                                    'Revenue',
                                                    'Sales',
                                                ]
                                                g = [
                                                    'Loss',
                                                ]
                                                s = 'a'
                                                for l in q:
                                                    if s == 'a':
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            y = 1
                                                            for gg in g:
                                                                if gg in d:
                                                                    y = -1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while IncomeStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = IncomeStatement[key][i]
                                                                    IncomeStatement[key][i] = None
                                                                except:
                                                                    if IncomeStatement[key] != None:
                                                                        ARCHvalue = IncomeStatement[key]
                                                                        IncomeStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    EquityMethodInvesteesIncome.append(ARCHvalue)
                                                                    s = 'z'
                                            r = r + 1
                                        tb.EquityMethodInvesteesIncome = -abs(sum(EquityMethodInvesteesIncome)) * y
                                    except:
                                        pass
                                    #
                                    # net income Non Controlling Interests
                                    try:
                                        NetIncomeAttributableToNonControllingInterest = []
                                        r = 0
                                        for key, value in IncomeStatement.items():
                                            d = key
                                            q = [
                                                'NetIncomeAttributableToMinorityInterest',
                                                'NetIncomeAttributableToNonControllingInterest',
                                                'NetIncomeAttributableToNoncontrollingInterest',
                                            ]
                                            b = [
                                                'CostOfGoods',
                                                'CostOfOperations',
                                                'CostOfRevenue',
                                                'CostOfSales',
                                                'DiscontinuedOperation',
                                                'Gain',
                                                'Other',
                                                'Miscellaneous',
                                                'PerShare',
                                                'Research',
                                                'Revenue',
                                                'Sales',
                                                'Tax',
                                            ]
                                            s = 'a'
                                            for l in q:
                                                if s == 'a':
                                                    if l in d:
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = 0
                                                                while IncomeStatement[key][i] == None:
                                                                    i = i + 1
                                                                ARCHvalue = IncomeStatement[key][i]
                                                                IncomeStatement[key][i] = None
                                                            except:
                                                                if IncomeStatement[key] != None:
                                                                    ARCHvalue = IncomeStatement[key]
                                                                    IncomeStatement[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                NetIncomeAttributableToNonControllingInterest.append(ARCHvalue)
                                                                s = 'z'
                                            r = r + 1
                                        a.NetIncomeAttributableToNonControllingInterest = -abs(sum(NetIncomeAttributableToNonControllingInterest))
                                    except:
                                        pass
                                    #
                                    # ML
                                    try:
                                        w = None
                                        a.NetIncomeGL_i = ''
                                        m = None
                                        a.NetIncomeGL_ii = ''
                                        t = None
                                        a.NetIncomeGL_iii = ''
                                        r = 0
                                        for key, value in IncomeStatement.items():
                                            if r < NetIncomeRank:
                                                d = key
                                                b = [
                                                    'Total',
                                                ]
                                                h = 'p'
                                                for p in b:
                                                    u = 0
                                                    while u < len(b):
                                                        if p in d:
                                                            h = ''
                                                        u = u + 1
                                                if h == 'p':
                                                    try:
                                                        i = 0
                                                        while IncomeStatement[key][i] == None:
                                                            i = i + 1
                                                        ARCHvalue = IncomeStatement[key][i]
                                                        IncomeStatement[key][i] = None
                                                    except:
                                                        if IncomeStatement[key] != None:
                                                            ARCHvalue = IncomeStatement[key]
                                                            IncomeStatement[key] = None
                                                        else:
                                                            ARCHvalue = 0
                                                    if ARCHvalue != 0:
                                                        try:
                                                            #
                                                            if w is None:
                                                                a.NetIncomeGL_i = d
                                                                w = ''
                                                            #
                                                            elif m is None:
                                                                a.NetIncomeGL_ii = d
                                                                m = ''
                                                            #
                                                            elif t is None:
                                                                a.NetIncomeGL_iii = d
                                                                t = ''
                                                            else:
                                                                pass
                                                            #
                                                            if d not in NetIncomeGL:
                                                                NetIncomeGL.append(d)
                                                            #
                                                        except:
                                                            pass
                                            r = r + 1
                                    except:
                                        pass
                                    #
                                    # dataframe components
                                    try:
                                        #
                                        df = pd.DataFrame({
                                            #
                                            '..': 
                                                [
                                                'a.Sales',
                                                'tb.Sales',
                                                'a.CostOfSales',
                                                'tb.CostOfSales',
                                                'a.GrossMargin',
                                                'tb.ResearchAndDevelopment',
                                                'tb.SellingGeneralAdministrativeAndMarketing',
                                                'a.OperatingIncome',
                                                'tb.ImpairmentRestructuringAndOtherSpecialCharges',
                                                'tb.NonOperatingIncome',
                                                'a.IncomeBeforeTaxes',
                                                'tb.IncomeTaxExpenseBenefit',
                                                'tb.EquityMethodInvesteesIncome',
                                                'tb.NetIncomeFromDiscontinuedOperations',
                                                'a.NetIncomeAttributableToNonControllingInterest',
                                                'a.NetIncome',
                                                ],
                                            #
                                            '.':
                                                [
                                                '{:,}'.format(a.Sales),
                                                '{:,}'.format(tb.Sales),
                                                '{:,}'.format(a.CostOfSales),
                                                '{:,}'.format(tb.CostOfSales),
                                                '{:,}'.format(a.GrossMargin),
                                                '{:,}'.format(tb.ResearchAndDevelopment),
                                                '{:,}'.format(tb.SellingGeneralAdministrativeAndMarketing),
                                                '{:,}'.format(a.OperatingIncome),
                                                '{:,}'.format(tb.ImpairmentRestructuringAndOtherSpecialCharges),
                                                '{:,}'.format(tb.NonOperatingIncome),
                                                '{:,}'.format(a.IncomeBeforeTaxes),
                                                '{:,}'.format(tb.IncomeTaxExpenseBenefit),
                                                '{:,}'.format(tb.EquityMethodInvesteesIncome),
                                                '{:,}'.format(tb.NetIncomeFromDiscontinuedOperations),
                                                '{:,}'.format(a.NetIncomeAttributableToNonControllingInterest),
                                                '{:,}'.format(a.NetIncome),
                                                ],
                                        })
                                        print(df)
                                        print(137 * '-' + '\n')
                                        #
                                        tb.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # comprehensive income
                                try:
                                    #
                                    print(e.EntityRegistrantName)
                                    print('comprehensive income')
                                    print(periodenddate)
                                    print(137 * '-' + '\n')
                                    #
                                    if ComprehensiveIncomeStatement == {}:
                                        ComprehensiveIncomeStatement = IncomeStatement
                                    #
                                    # other comprehensive income
                                    try:
                                        #
                                        ComprehensiveIncome = []
                                        r = 0
                                        for key, value in ComprehensiveIncomeStatement.items():
                                            d = key
                                            q = [
                                                'ComprehensiveIncome',
                                            ]
                                            b = [
                                                'Accumulated',
                                                'ContinuingOperations',
                                                'OtherComprehensiveIncome',
                                                'TotalChangeIn',
                                            ]
                                            for l in q:
                                                if l in d:
                                                    h = 'p'
                                                    for p in b:
                                                        u = 0
                                                        while u < len(b):
                                                            if p in d:
                                                                h = ''
                                                            u = u + 1
                                                    if h == 'p':
                                                        try:
                                                            i = 0
                                                            while ComprehensiveIncomeStatement[key][i] == None:
                                                                i = i + 1
                                                            ARCHvalue = ComprehensiveIncomeStatement[key][i]
                                                            ComprehensiveIncomeStatement[key][i] = None
                                                        except:
                                                            if ComprehensiveIncomeStatement[key] != None:
                                                                ARCHvalue = ComprehensiveIncomeStatement[key]
                                                                ComprehensiveIncomeStatement[key] = None
                                                            else:
                                                                ARCHvalue = 0
                                                        if ARCHvalue != 0:
                                                            ComprehensiveIncome.append(ARCHvalue)
                                                            ComprehensiveIncomeRank = r
                                            r = r + 1
                                        #
                                        a.ComprehensiveIncome = -sum(ComprehensiveIncome)
                                        #
                                        a.OtherComprehensiveIncome = a.ComprehensiveIncome - a.NetIncome
                                        #
                                    except:
                                        pass
                                    #
                                    # foreign currency translation
                                    try:
                                        ChangeInForeignCurrencyTranslationAdjustment = []
                                        r = 0
                                        for key, value in ComprehensiveIncomeStatement.items():
                                            if r < ComprehensiveIncomeRank:
                                                d = key
                                                q = [
                                                    'CurrencyTransaction',
                                                    'Translation',
                                                ]
                                                b = [
                                                    'ContinuingOperations',
                                                    'TotalChangeIn',
                                                ]
                                                for l in q:
                                                    if l in d:
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = 0
                                                                while ComprehensiveIncomeStatement[key][i] == None:
                                                                    i = i + 1
                                                                ARCHvalue = ComprehensiveIncomeStatement[key][i]
                                                                ComprehensiveIncomeStatement[key][i] = None
                                                            except:
                                                                if ComprehensiveIncomeStatement[key] != None:
                                                                    ARCHvalue = ComprehensiveIncomeStatement[key]
                                                                    ComprehensiveIncomeStatement[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                ChangeInForeignCurrencyTranslationAdjustment.append(ARCHvalue)
                                            r = r + 1
                                        tb.ChangeInForeignCurrencyTranslationAdjustment = -sum(ChangeInForeignCurrencyTranslationAdjustment)
                                    except:
                                        pass
                                    #
                                    # unrealized gains (losses) on derivative instruments
                                    try:
                                        ChangeInUnrealizedGainsLossesOnDerivativeInstruments = []
                                        r = 0
                                        for key, value in ComprehensiveIncomeStatement.items():
                                            if r < ComprehensiveIncomeRank:
                                                d = key
                                                q = [
                                                    'Hedge',
                                                    'Derivatives',
                                                    'RealizedAndIncludedInNetIncome',
                                                ]
                                                b = [
                                                    'ContinuingOperations',
                                                    'TotalChangeIn',
                                                ]
                                                for l in q:
                                                    if l in d:
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = 0
                                                                while ComprehensiveIncomeStatement[key][i] == None:
                                                                    i = i + 1
                                                                ARCHvalue = ComprehensiveIncomeStatement[key][i]
                                                                ComprehensiveIncomeStatement[key][i] = None
                                                            except:
                                                                if ComprehensiveIncomeStatement[key] != None:
                                                                    ARCHvalue = ComprehensiveIncomeStatement[key]
                                                                    ComprehensiveIncomeStatement[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                ChangeInUnrealizedGainsLossesOnDerivativeInstruments.append(ARCHvalue)
                                            r = r + 1
                                        tb.ChangeInUnrealizedGainsLossesOnDerivativeInstruments = -sum(ChangeInUnrealizedGainsLossesOnDerivativeInstruments)
                                    except:
                                        pass
                                    #
                                    # unrealized gains (losses) on investment
                                    try:
                                        ChangeInUnrealizedGainsLossesOnInvestments = []
                                        r = 0
                                        for key, value in ComprehensiveIncomeStatement.items():
                                            if r < ComprehensiveIncomeRank:
                                                d = key
                                                q = [
                                                    '(Losses)OnSecurit',
                                                    'LossesOnSecurit',
                                                    '(Loss)OnSecurit',
                                                    'LossOnSecurit',
                                                    '(Gains)OnSecurit',
                                                    '(Gain)OnSecurit',
                                                    'GainsOnSecurit',
                                                    'GainOnSecurit',
                                                    'GainOnAvailableForSale',
                                                    'GainsOnAvailableForSale',
                                                    '(Gain)OnAvailableForSale',
                                                    '(Gains)OnAvailableForSale',
                                                    'LossOnAvailableForSale',
                                                    'LossesOnAvailableForSale',
                                                    '(Loss)OnAvailableForSale',
                                                    '(Losses)OnAvailableForSale',
                                                    'MarketableDebt',
                                                    'MarketableSecurit',
                                                    'LossesOnInvestment',
                                                    'LossOnInvestment',
                                                    '(Losses)OnInvestment',
                                                    '(Loss)OnInvestment',
                                                    '(Gains)OnInvestment',
                                                    '(Gain)OnInvestment',
                                                    'GainsOnInvestment',
                                                    'GainOnInvestment',
                                                    'SecuritiesAdjustment',
                                                ]
                                                b = [
                                                    'ContinuingOperations',
                                                    'TotalChangeIn',
                                                ]
                                                for l in q:
                                                    if l in d:
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = 0
                                                                while ComprehensiveIncomeStatement[key][i] == None:
                                                                    i = i + 1
                                                                ARCHvalue = ComprehensiveIncomeStatement[key][i]
                                                                ComprehensiveIncomeStatement[key][i] = None
                                                            except:
                                                                if ComprehensiveIncomeStatement[key] != None:
                                                                    ARCHvalue = ComprehensiveIncomeStatement[key]
                                                                    ComprehensiveIncomeStatement[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                ChangeInUnrealizedGainsLossesOnInvestments.append(ARCHvalue)
                                            r = r + 1
                                        tb.ChangeInUnrealizedGainsLossesOnInvestments = -sum(ChangeInUnrealizedGainsLossesOnInvestments)
                                    except:
                                        pass
                                    #
                                    # defined benefit pension and other similar plans
                                    try:
                                        ChangeInDefinedBenefitPensionAndOtherSimilarPlans = []
                                        r = 0
                                        for key, value in ComprehensiveIncomeStatement.items():
                                            if r < ComprehensiveIncomeRank:
                                                d = key
                                                q = [
                                                    'Pension',
                                                    'DefinedBenefit',
                                                ]
                                                b = [
                                                    'Currency',
                                                    'Derivatives',
                                                    'Investments',
                                                    'TotalChangeIn',
                                                ]
                                                for l in q:
                                                    if l in d:
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = 0
                                                                while ComprehensiveIncomeStatement[key][i] == None:
                                                                    i = i + 1
                                                                ARCHvalue = ComprehensiveIncomeStatement[key][i]
                                                                ComprehensiveIncomeStatement[key][i] = None
                                                            except:
                                                                if ComprehensiveIncomeStatement[key] != None:
                                                                    ARCHvalue = ComprehensiveIncomeStatement[key]
                                                                    ComprehensiveIncomeStatement[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                ChangeInDefinedBenefitPensionAndOtherSimilarPlans.append(ARCHvalue)
                                            r = r + 1
                                        tb.ChangeInDefinedBenefitPensionAndOtherSimilarPlans = -sum(ChangeInDefinedBenefitPensionAndOtherSimilarPlans)
                                    except:
                                        pass
                                    #
                                    # income tax on other comprehensive income
                                    try:
                                        IncomeTaxOnOtherComprehensiveIncome = []
                                        r = 0
                                        for key, value in ComprehensiveIncomeStatement.items():
                                            if r < ComprehensiveIncomeRank:
                                                d = key
                                                q = [
                                                    'BenefitForIncomeTax',
                                                    '(Benefit)ForIncomeTax',
                                                    'ProvisionForIncomeTax',
                                                    '(Provision)ForIncomeTax',
                                                    'IncomeTaxes',
                                                    'TaxBenefit',
                                                ]
                                                b = [
                                                    'BeforeIncomeTaxe',
                                                    'TotalChangeIn',
                                                ]
                                                for l in q:
                                                    if l in d:
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = 0
                                                                while ComprehensiveIncomeStatement[key][i] == None:
                                                                    i = i + 1
                                                                ARCHvalue = ComprehensiveIncomeStatement[key][i]
                                                                ComprehensiveIncomeStatement[key][i] = None
                                                            except:
                                                                if ComprehensiveIncomeStatement[key] != None:
                                                                    ARCHvalue = ComprehensiveIncomeStatement[key]
                                                                    ComprehensiveIncomeStatement[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                IncomeTaxOnOtherComprehensiveIncome.append(ARCHvalue)
                                            r = r + 1
                                        tb.IncomeTaxOnOtherComprehensiveIncome = -sum(IncomeTaxOnOtherComprehensiveIncome)
                                    except:
                                        pass
                                    #
                                    # ML
                                    try:
                                        w = None
                                        a.OtherComprehensiveIncomeGL_i = ''
                                        #
                                        m = None
                                        a.OtherComprehensiveIncomeGL_ii = ''
                                        #
                                        t = None
                                        a.OtherComprehensiveIncomeGL_iii = ''
                                        r = 0
                                        for key, value in ComprehensiveIncomeStatement.items():
                                            if r < ComprehensiveIncomeRank:
                                                d = key
                                                b = [
                                                    'TotalChangeIn',
                                                    'TotalOtherComprehensive',
                                                ]
                                                if d != 'NetIncome':
                                                    h = 'p'
                                                    for p in b:
                                                        u = 0
                                                        while u < len(b):
                                                            if p in d:
                                                                h = ''
                                                            u = u + 1
                                                    if h == 'p':
                                                        try:
                                                            i = 0
                                                            while ComprehensiveIncomeStatement[key][i] == None:
                                                                i = i + 1
                                                            ARCHvalue = ComprehensiveIncomeStatement[key][i]
                                                            ComprehensiveIncomeStatement[key][i] = None
                                                        except:
                                                            if ComprehensiveIncomeStatement[key] != None:
                                                                ARCHvalue = ComprehensiveIncomeStatement[key]
                                                                ComprehensiveIncomeStatement[key] = None
                                                            else:
                                                                ARCHvalue = 0
                                                        if ARCHvalue != 0:
                                                            try:
                                                                #
                                                                if w is None:
                                                                    a.OtherComprehensiveIncomeGL_i = d
                                                                    w = ''
                                                                #
                                                                elif m is None:
                                                                    a.OtherComprehensiveIncomeGL_ii = d
                                                                    m = ''
                                                                #
                                                                elif t is None:
                                                                    a.OtherComprehensiveIncomeGL_iii = d
                                                                    t = ''
                                                                else:
                                                                    pass
                                                                #
                                                                if d not in OtherComprehensiveIncomeGL:
                                                                    OtherComprehensiveIncomeGL.append(d)
                                                                #
                                                            except:
                                                                pass
                                            r = r + 1
                                    except:
                                        pass
                                    #
                                    # dataframe
                                    try:
                                        #
                                        df = pd.DataFrame({
                                            #
                                            '..': 
                                                [
                                                'tb.ChangeInForeignCurrencyTranslationAdjustment',
                                                'tb.ChangeInUnrealizedGainsLossesOnDerivativeInstruments',
                                                'tb.ChangeInUnrealizedGainsLossesOnInvestments',
                                                'tb.ChangeInDefinedBenefitPensionAndOtherSimilarPlans',
                                                'tb.IncomeTaxOnOtherComprehensiveIncome',
                                                'a.OtherComprehensiveIncome',
                                                ],
                                            #
                                            '.':
                                                [
                                                '{:,}'.format(tb.ChangeInForeignCurrencyTranslationAdjustment),
                                                '{:,}'.format(tb.ChangeInUnrealizedGainsLossesOnDerivativeInstruments),
                                                '{:,}'.format(tb.ChangeInUnrealizedGainsLossesOnInvestments),
                                                '{:,}'.format(tb.ChangeInDefinedBenefitPensionAndOtherSimilarPlans),
                                                '{:,}'.format(tb.IncomeTaxOnOtherComprehensiveIncome),
                                                '{:,}'.format(a.OtherComprehensiveIncome),
                                                ],
                                        })
                                        print(df)
                                        print('\n' + 137 * '-' + '\n')
                                        #
                                        tb.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # shareholders equity statement
                                try:
                                    #
                                    print(e.EntityRegistrantName)
                                    print('shareholders equity')
                                    print(periodenddate)
                                    print(137 * '-' + '\n')
                                    #
                                    # Rank
                                    try:
                                        r = 0
                                        t = 0
                                        for key, value in ShareholdersEquityStatement.items():
                                            d = key
                                            q = [
                                                'EndingBalances',
                                            ]
                                            b = [
                                                'InShares',
                                            ]
                                            for l in q:
                                                if l in d:
                                                    h = 'p'
                                                    for p in b:
                                                        u = 0
                                                        while u < len(b):
                                                            if p in d:
                                                                h = ''
                                                            u = u + 1
                                                    if h == 'p':
                                                        if value != 0:
                                                            t = t + 1
                                                            print(d)
                                                            print(value)
                                                            print(t)
                                            r = r + 1
                                        ShareholdersEquityRank = t / z - 1
                                        print('Shareholders Equity Rank: ' + str(ShareholdersEquityRank))
                                    except:
                                        pass
                                    #
                                    # common stock issued
                                    try:
                                        CommonSharesIssued = []
                                        r = 0
                                        for key, value in ShareholdersEquityStatement.items():
                                            if r > ShareholdersEquityRank:
                                                d = key
                                                q = [
                                                    'CommonStockIssu',
                                                    'CommonStockOfferings',
                                                    'IssuedCommon',
                                                    'IssuanceOfCommon',
                                                ]
                                                b = [
                                                    'Debt',
                                                    'Retirement',
                                                    'Repurchase',
                                                    'InShares',
                                                    'Total',
                                                    'Beginning',
                                                    'Ending',
                                                ]
                                                for l in q:
                                                    if l in d:
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = len(value) - 1
                                                                while ShareholdersEquityStatement[key][i] == None:
                                                                    i = i - 1
                                                                ARCHvalue = ShareholdersEquityStatement[key][i]
                                                                ShareholdersEquityStatement[key][i] = None
                                                            except:
                                                                if ShareholdersEquityStatement[key] != None:
                                                                    ARCHvalue = ShareholdersEquityStatement[key]
                                                                    ShareholdersEquityStatement[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                CommonSharesIssued.append(ARCHvalue)
                                                                print(d)
                                                                print('{:,}'.format(value))
                                            r = r + 1
                                        tb.CommonSharesIssued = -sum(CommonSharesIssued)
                                    except:
                                        pass
                                    #
                                    # share based compensation (Common Shares Component)
                                    try:
                                        ShareBasedCompensation = []
                                        r = 0
                                        for key, value in ShareholdersEquityStatement.items():
                                            if r > ShareholdersEquityRank:
                                                d = key
                                                q = [
                                                    'EquityAward',
                                                    'EquityBasedCompensation',
                                                    'EquityBasedArrangements',
                                                    'EquityBasedPaymentArrangements',
                                                    'ShareBasedCompensation',
                                                    'StockBasedCompendation',
                                                    'SharesWithheldRelatedToNetShareSettlement',
                                                    'StockWithheldRelatedToNetShareSettlement',
                                                ]
                                                b = [
                                                    'RetainedEarnings',
                                                    'Retirement',
                                                    'Repurchase',
                                                    'InShares',
                                                    'Total',
                                                    'Beginning',
                                                    'Ending',
                                                ]
                                                for l in q:
                                                    if l in d:
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = len(value) - 1
                                                                while ShareholdersEquityStatement[key][i] == None:
                                                                    i = i - 1
                                                                ARCHvalue = ShareholdersEquityStatement[key][i]
                                                                ShareholdersEquityStatement[key][i] = None
                                                            except:
                                                                if ShareholdersEquityStatement[key] != None:
                                                                    ARCHvalue = ShareholdersEquityStatement[key]
                                                                    ShareholdersEquityStatement[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                ShareBasedCompensation.append(ARCHvalue)
                                                                print(d)
                                                                print('{:,}'.format(value))
                                            r = r + 1
                                        tb.ShareBasedCompensation = -sum(ShareBasedCompensation)
                                    except:
                                        pass
                                    #
                                    # share based compensation (Retained Earnings Component)
                                    try:
                                        ShareBasedCompensationRetainedEarnings = []
                                        r = 0
                                        for key, value in ShareholdersEquityStatement.items():
                                            if r > ShareholdersEquityRank:
                                                d = key
                                                q = [
                                                    'EquityBasedCompensation',
                                                    'EquityBasedArrangements',
                                                    'EquityBasedPaymentArrangements',
                                                    'ShareBasedCompensation',
                                                    'StockBasedCompendation',
                                                    'SharesWithheldRelatedToNetShareSettlement',
                                                    'StockWithheldRelatedToNetShareSettlement',
                                                ]
                                                b = [
                                                    'Retirement',
                                                    'Repurchase',
                                                    'InShares',
                                                    'Total',
                                                    'Beginning',
                                                    'Ending',
                                                ]
                                                for l in q:
                                                    if l in d:
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = len(value) - 1
                                                                while ShareholdersEquityStatement[key][i] == None:
                                                                    i = i - 1
                                                                ARCHvalue = ShareholdersEquityStatement[key][i]
                                                                ShareholdersEquityStatement[key][i] = None
                                                            except:
                                                                if ShareholdersEquityStatement[key] != None:
                                                                    ARCHvalue = ShareholdersEquityStatement[key]
                                                                    ShareholdersEquityStatement[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                ShareBasedCompensationRetainedEarnings.append(ARCHvalue)
                                                                print(d)
                                                                print('{:,}'.format(value))
                                            r = r + 1
                                        tb.ShareBasedCompensationRetainedEarnings = -sum(ShareBasedCompensationRetainedEarnings)
                                    except:
                                        pass
                                    #
                                    # dividends and dividend equivalents declared
                                    try:
                                        DividendsAndDividendEquivalentsDeclared = []
                                        r = 0
                                        for key, value in ShareholdersEquityStatement.items():
                                            if r > ShareholdersEquityRank:
                                                d = key
                                                q = [
                                                    'Dividends',
                                                ]
                                                b = [
                                                    'Retirement',
                                                    'Repurchase',
                                                    'NoncontrollingInterest',
                                                    'InShares',
                                                    'Total',
                                                    'Beginning',
                                                    'Ending',
                                                ]
                                                for l in q:
                                                    if l in d:
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = len(value) - 1
                                                                while ShareholdersEquityStatement[key][i] == None:
                                                                    i = i - 1
                                                                ARCHvalue = ShareholdersEquityStatement[key][i]
                                                                ShareholdersEquityStatement[key][i] = None
                                                            except:
                                                                if ShareholdersEquityStatement[key] != None:
                                                                    ARCHvalue = ShareholdersEquityStatement[key]
                                                                    ShareholdersEquityStatement[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                ARCHvalue = -abs(ARCHvalue)
                                                                DividendsAndDividendEquivalentsDeclared.append(ARCHvalue)
                                                                print(d)
                                                                print('{:,}'.format(value))
                                            r = r + 1
                                        tb.DividendsAndDividendEquivalentsDeclared = -sum(DividendsAndDividendEquivalentsDeclared)
                                    except:
                                        pass
                                    #
                                    # dividends and dividend equivalents declared to non controlling interests
                                    try:
                                        DividendsDeclaredToNonControllingInterests = []
                                        r = 0
                                        for key, value in ShareholdersEquityStatement.items():
                                            if r > ShareholdersEquityRank:
                                                d = key
                                                q = [
                                                    'DividendEquivalentsDeclaredToNoncontrollingInterest',
                                                    'DividendEquivalentsDeclaredToNonControllingInterest',
                                                    'DividendDeclaredToNoncontrollingInterest',
                                                    'DividendDeclaredToNonControllingInterest',
                                                ]
                                                b = [
                                                    'Acquisition',
                                                    'Retirement',
                                                    'Repurchase',
                                                    'InShares',
                                                    'Total',
                                                    'Beginning',
                                                    'Ending',
                                                ]
                                                for l in q:
                                                    if l in d:
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = len(value) - 1
                                                                while ShareholdersEquityStatement[key][i] == None:
                                                                    i = i - 1
                                                                ARCHvalue = ShareholdersEquityStatement[key][i]
                                                                ShareholdersEquityStatement[key][i] = None
                                                            except:
                                                                if ShareholdersEquityStatement[key] != None:
                                                                    ARCHvalue = ShareholdersEquityStatement[key]
                                                                    ShareholdersEquityStatement[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                DividendsDeclaredToNonControllingInterests.append(ARCHvalue)
                                                                print(d)
                                                                print('{:,}'.format(value))
                                            r = r + 1
                                        tb.DividendsDeclaredToNonControllingInterests = -sum(DividendsDeclaredToNonControllingInterests)
                                    except:
                                        pass
                                    #
                                    # acquisition of non controlling interests
                                    try:
                                        AcquisitionOfNonControllingInterests = []
                                        r = 0
                                        for key, value in ShareholdersEquityStatement.items():
                                            if r > ShareholdersEquityRank:
                                                d = key
                                                q = [
                                                    'AcquisitionOfNonControllingInterests',
                                                    'AcquisitionOfNoncontrollingInterests',
                                                    'RepaymentOfNonControllingInterests',
                                                    'RepaymentOfNoncontrollingInterests',
                                                    'DistributionsToNoncontrollingInterests',
                                                    'DistributionsToNonControllingInterests',
                                                ]
                                                b = [
                                                    'Dividend',
                                                    'InShares',
                                                    'Total',
                                                    'Beginning',
                                                    'Ending',
                                                ]
                                                for l in q:
                                                    if l in d:
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = len(value) - 1
                                                                while ShareholdersEquityStatement[key][i] == None:
                                                                    i = i - 1
                                                                ARCHvalue = ShareholdersEquityStatement[key][i]
                                                                ShareholdersEquityStatement[key][i] = None
                                                            except:
                                                                if ShareholdersEquityStatement[key] != None:
                                                                    ARCHvalue = ShareholdersEquityStatement[key]
                                                                    ShareholdersEquityStatement[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                AcquisitionOfNonControllingInterests.append(ARCHvalue)
                                                                print(d)
                                                                print('{:,}'.format(value))
                                            r = r + 1
                                        tb.AcquisitionOfNonControllingInterests = -sum(AcquisitionOfNonControllingInterests)
                                    except:
                                        pass
                                    #
                                    # common stock repurchased and retired
                                    try:
                                        CommonSharesRepurchasedAndRetired = []
                                        r = 0
                                        for key, value in ShareholdersEquityStatement.items():
                                            if r > ShareholdersEquityRank:
                                                d = key
                                                q = [
                                                    'AcquisitionOfCommon',
                                                    'CommonStockRepurchased',
                                                    'PurchaseOfCompanyShare',
                                                    'PurchaseOfCompanyStock',
                                                    'PurchaseOfTreasuryShare',
                                                    'RepurchasesOfCommonStock',
                                                    'RepurchaseOfCommonStock',
                                                    'RetirementOfTreasuryShares',
                                                    'ShareRepurchases',
                                                    'StockRepurchased',
                                                ]
                                                b = [
                                                    'Dividend',
                                                    'InShares',
                                                    'Total',
                                                    'Beginning',
                                                    'Ending',
                                                ]
                                                for l in q:
                                                    if l in d:
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = len(value) - 1
                                                                while ShareholdersEquityStatement[key][i] == None:
                                                                    i = i - 1
                                                                ARCHvalue = ShareholdersEquityStatement[key][i]
                                                                ShareholdersEquityStatement[key][i] = None
                                                            except:
                                                                if ShareholdersEquityStatement[key] != None:
                                                                    ARCHvalue = ShareholdersEquityStatement[key]
                                                                    ShareholdersEquityStatement[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                CommonSharesRepurchasedAndRetired.append(ARCHvalue)
                                                                print(d)
                                                                print('{:,}'.format(value))
                                            r = r + 1
                                        tb.CommonSharesRepurchasedAndRetired = -sum(CommonSharesRepurchasedAndRetired)
                                    except:
                                        pass
                                    #
                                    # effect of adoption of new accounting pronouncement or tax cuts
                                    try:
                                        EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts = []
                                        r = 0
                                        for key, value in ShareholdersEquityStatement.items():
                                            if r > ShareholdersEquityRank:
                                                d = key
                                                q = [
                                                    'AdoptionOfNewAccountingStandards',
                                                    'ChangeInAccountingPrinciple',
                                                    'ReclassificationOfStrandedTaxEffects',
                                                    'CumulativeEffectAdjustment',
                                                    'CumulativeOfChangeInAccounting',
                                                ]
                                                b = [
                                                    'Distribution',
                                                    'Dividend',
                                                    'InShares',
                                                    'Total',
                                                    'Beginning',
                                                    'Ending',
                                                ]
                                                for l in q:
                                                    if l in d:
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = len(value) - 1
                                                                while ShareholdersEquityStatement[key][i] == None:
                                                                    i = i - 1
                                                                ARCHvalue = ShareholdersEquityStatement[key][i]
                                                                ShareholdersEquityStatement[key][i] = None
                                                            except:
                                                                if ShareholdersEquityStatement[key] != None:
                                                                    ARCHvalue = ShareholdersEquityStatement[key]
                                                                    ShareholdersEquityStatement[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts.append(ARCHvalue)
                                                                print(d)
                                                                print('{:,}'.format(value))
                                            r = r + 1
                                        tb.EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts = sum(EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts)
                                    except:
                                        pass
                                    #
                                    # ML
                                    try:
                                        w = None
                                        a.ShareholdersEquityGL_i = ''
                                        #
                                        m = None
                                        a.ShareholdersEquityGL_ii = ''
                                        #
                                        t = None
                                        a.ShareholdersEquityGL_iii = ''
                                        r = 0
                                        for key, value in ShareholdersEquityStatement.items():
                                            if r > ShareholdersEquityRank:
                                                d = key
                                                b = [
                                                    'BalancesAt'
                                                    'Beginning',
                                                    'Ending',
                                                    'InShares',
                                                    'NetIncome',
                                                    'OtherComprehensiveIncome',
                                                    'Total',
                                                ]
                                                h = 'p'
                                                for p in b:
                                                    u = 0
                                                    while u < len(b):
                                                        if p in d:
                                                            h = ''
                                                        u = u + 1
                                                if h == 'p':
                                                    try:
                                                        i = 0
                                                        while ShareholdersEquityStatement[key][i] == None:
                                                            i = i + 1
                                                        ARCHvalue = ShareholdersEquityStatement[key][i]
                                                        ShareholdersEquityStatement[key][i] = None
                                                    except:
                                                        if ShareholdersEquityStatement[key] != None:
                                                            ARCHvalue = ShareholdersEquityStatement[key]
                                                            ShareholdersEquityStatement[key] = None
                                                        else:
                                                            ARCHvalue = 0
                                                    if ARCHvalue != 0:
                                                        try:
                                                            #
                                                            if w is None:
                                                                a.ShareholdersEquityGL_i = d
                                                                w = ''
                                                            #
                                                            elif m is None:
                                                                a.ShareholdersEquityGL_ii = d
                                                                m = ''
                                                            #
                                                            elif t is None:
                                                                a.ShareholdersEquityGL_iii = d
                                                                t = ''
                                                            else:
                                                                pass
                                                            #
                                                            if d not in ShareholdersEquityGL:
                                                                ShareholdersEquityGL.append(d)
                                                            #
                                                        except:
                                                            pass
                                            r = r + 1
                                    except:
                                        pass
                                    # dataframe
                                    try:
                                        #
                                        df = pd.DataFrame({
                                            #
                                            '..': 
                                                [
                                                'tb.CommonSharesIssued',
                                                'tb.ShareBasedCompensation',
                                                'tb.ShareBasedCompensationRetainedEarnings',
                                                'tb.DividendsAndDividendEquivalentsDeclared',
                                                'tb.DividendsDeclaredToNonControllingInterests',
                                                'tb.AcquisitionOfNonControllingInterests',
                                                'tb.CommonSharesRepurchasedAndRetired',
                                                'tb.EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts',
                                                ],
                                            #
                                            '.':
                                                [
                                                '{:,}'.format(tb.CommonSharesIssued),
                                                '{:,}'.format(tb.ShareBasedCompensation),
                                                '{:,}'.format(tb.ShareBasedCompensationRetainedEarnings),
                                                '{:,}'.format(tb.DividendsAndDividendEquivalentsDeclared),
                                                '{:,}'.format(tb.DividendsDeclaredToNonControllingInterests),
                                                '{:,}'.format(tb.AcquisitionOfNonControllingInterests),
                                                '{:,}'.format(tb.CommonSharesRepurchasedAndRetired),
                                                '{:,}'.format(tb.EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts),
                                                ],
                                        })
                                        print(df)
                                        print('\n' + 137 * '-')
                                        #
                                        tb.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # cash flow
                                try:
                                    #
                                    print(e.EntityRegistrantName)
                                    print('cash flow')
                                    print(periodenddate)
                                    print(137 * '-' + '\n')
                                    #
                                    # effect of exchange rate on cash
                                    try:
                                        EffectOfExchangeRateOnCash = []
                                        r = 0
                                        for key, value in CashFlowStatement.items():
                                            d = key
                                            q = [
                                                'ExchangeRate',
                                            ]
                                            b = [
                                                'Acquire',
                                                'Acquisition',
                                                'Decrease',
                                                'Disposal',
                                                'DiscontinuedOperation',
                                                'Ending',
                                                'Financing',
                                                'Hedge',
                                                'Increase',
                                                'Investment',
                                                'Investing',
                                                'Operating',
                                                'Payment',
                                                'Proceeds',
                                                'Purchase',
                                                'Selling',
                                            ]
                                            for l in q:
                                                if l in d:
                                                    h = 'p'
                                                    for p in b:
                                                        u = 0
                                                        while u < len(b):
                                                            if p in d:
                                                                h = ''
                                                            u = u + 1
                                                    if h == 'p':
                                                        try:
                                                            i = 0
                                                            while CashFlowStatement[key][i] == None:
                                                                i = i + 1
                                                            ARCHvalue = CashFlowStatement[key][i]
                                                            CashFlowStatement[key][i] = None
                                                        except:
                                                            if CashFlowStatement[key] != None:
                                                                ARCHvalue = CashFlowStatement[key]
                                                                CashFlowStatement[key] = None
                                                            else:
                                                                ARCHvalue = 0
                                                        if ARCHvalue != 0:
                                                            EffectOfExchangeRateOnCash.append(ARCHvalue)
                                            r = r + 1
                                        cf.EffectOfExchangeRateOnCash = sum(EffectOfExchangeRateOnCash)
                                    except:
                                        pass
                                    #
                                    # total operating activities
                                    try:
                                        OperatingActivities = []
                                        OperatingActivitiesRank = 5
                                        r = 0
                                        for key, value in CashFlowStatement.items():
                                            d = key
                                            q = [
                                                'OperatingActivities',
                                                'CashProvidedByOperation',
                                                'CashProvidedFromOperation',
                                                'CashProvidedFrom(UsedFor)Operations',
                                                'Cash(UsedFor)ProvidedFromOperations',
                                            ]
                                            b = [
                                                'Acquisition',
                                                'Acquire',
                                                'ContinuingOperation',
                                                'DiscontinuedOperations',
                                                'InterestPaid',
                                                'InvestingActivities',
                                                'FinancingActivities',
                                                'OtherNonCashOperatingActivities',
                                                'Other',
                                                'Miscellaneous',
                                                'NetIncome',
                                                'NetLoss',
                                                'Net(Loss)',
                                                'Payment',
                                                'Purchase',
                                            ]
                                            for l in q:
                                                if l in d:
                                                    h = 'p'
                                                    for p in b:
                                                        u = 0
                                                        while u < len(b):
                                                            if p in d:
                                                                h = ''
                                                            u = u + 1
                                                    if h == 'p':
                                                        try:
                                                            i = 0
                                                            while CashFlowStatement[key][i] == None:
                                                                i = i + 1
                                                            ARCHvalue = CashFlowStatement[key][i]
                                                            CashFlowStatement[key][i] = None
                                                        except:
                                                            if CashFlowStatement[key] != None:
                                                                ARCHvalue = CashFlowStatement[key]
                                                                CashFlowStatement[key] = None
                                                            else:
                                                                ARCHvalue = 0
                                                        if ARCHvalue != 0:
                                                            OperatingActivities.append(ARCHvalue)
                                                            OperatingActivitiesRank = r
                                            r = r + 1
                                        a.OperatingActivities = sum(OperatingActivities)
                                    except:
                                        pass
                                    #
                                    # Total Investing Activities
                                    try:
                                        InvestingActivities = []
                                        InvestingActivitiesRank = None
                                        r = 0
                                        for key, value in CashFlowStatement.items():
                                            d = key
                                            q = [
                                                'InvestingActivities',
                                            ]
                                            b = [
                                                'ContinuingOperations',
                                                'DiscontinuedOperations',
                                                'Financing',
                                                'Operating',
                                                'Other',
                                                'Miscellaneous',
                                            ]
                                            s = 'a'
                                            for l in q:
                                                if l in d:
                                                    h = 'p'
                                                    for p in b:
                                                        u = 0
                                                        while u < len(b):
                                                            if p in d:
                                                                h = ''
                                                            u = u + 1
                                                    if h == 'p':
                                                        try:
                                                            i = 0
                                                            while CashFlowStatement[key][i] == None:
                                                                i = i + 1
                                                            ARCHvalue = CashFlowStatement[key][i]
                                                            CashFlowStatement[key][i] = None
                                                        except:
                                                            if CashFlowStatement[key] != None:
                                                                ARCHvalue = CashFlowStatement[key]
                                                                CashFlowStatement[key] = None
                                                            else:
                                                                ARCHvalue = 0
                                                        if ARCHvalue != 0:
                                                            if s == 'a':
                                                                InvestingActivities.append(ARCHvalue)
                                                                InvestingActivitiesRank = r
                                                                s = 'z'
                                            r = r + 1
                                        a.InvestingActivities = sum(InvestingActivities)
                                    except:
                                        pass
                                    #
                                    # Total Financing Activities
                                    try:
                                        FinancingActivities = []
                                        FinancingActivitiesRank = None
                                        r = 0
                                        for key, value in CashFlowStatement.items():
                                            d = key
                                            q = [
                                                'FinancingActivities',
                                            ]
                                            b = [
                                                'ContinuingOperation',
                                                'DiscontinuedOperation',
                                                'InvestingActivities',
                                                'OperatingActivities',
                                                'OtherFinancingActivities',
                                            ]
                                            for l in q:
                                                if l in d:
                                                    h = 'p'
                                                    for p in b:
                                                        u = 0
                                                        while u < len(b):
                                                            if p in d:
                                                                h = ''
                                                            u = u + 1
                                                    if h == 'p':
                                                        try:
                                                            i = 0
                                                            while CashFlowStatement[key][i] == None:
                                                                i = i + 1
                                                            ARCHvalue = CashFlowStatement[key][i]
                                                            CashFlowStatement[key][i] = None
                                                        except:
                                                            if CashFlowStatement[key] != None:
                                                                ARCHvalue = CashFlowStatement[key]
                                                                CashFlowStatement[key] = None
                                                            else:
                                                                ARCHvalue = 0
                                                        if ARCHvalue != 0:
                                                            FinancingActivities.append(ARCHvalue)
                                                            FinancingActivitiesRank = r
                                            r = r + 1
                                        a.FinancingActivities = sum(FinancingActivities)
                                    except:
                                        pass
                                    #
                                    # increase decrease in cash
                                    try:
                                        c = a.OperatingActivities
                                        c = c + a.InvestingActivities
                                        c = c + a.FinancingActivities
                                        c = c + cf.EffectOfExchangeRateOnCash
                                        a.IncreaseDecreaseInCash = c
                                    except:
                                        pass
                                    #
                                    # cash beginning balance backwards
                                    try:
                                        CashEndingBalance = []
                                        r = 0
                                        s = 'a'
                                        for key, value in CashFlowStatement.items():
                                            if r > FinancingActivitiesRank:
                                                d = key
                                                q = [
                                                    'Cash',
                                                    'Balance',
                                                ]
                                                b = [
                                                    'Acquire',
                                                    'Acquisition',
                                                    'Beginning',
                                                    'ChangeIn',
                                                    'Decrease',
                                                    'Disposal',
                                                    'Distributed',
                                                    'Dividends',
                                                    'Effect',
                                                    'Exchange',
                                                    'Financing',
                                                    'Flows'
                                                    'From',
                                                    'Hedge',
                                                    'Impairment',
                                                    'Increase',
                                                    'Investing',
                                                    'Net',
                                                    'NonCash',
                                                    'Operating',
                                                    'Paid',
                                                    'Payment',
                                                    'Proceeds',
                                                    'Provided',
                                                    'Purchase',
                                                    'Received',
                                                    'Restructuring',
                                                    'Sale',
                                                    'Selling',
                                                ]
                                                for l in q:
                                                    if s == 'a':
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while CashFlowStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = CashFlowStatement[key][i]
                                                                    CashFlowStatement[key][i] = None
                                                                except:
                                                                    if CashFlowStatement[key] != None:
                                                                        ARCHvalue = CashFlowStatement[key]
                                                                        CashFlowStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    CashEndingBalance.append(ARCHvalue)
                                                                    s = 'z'
                                            r = r + 1
                                        c = sum(CashEndingBalance)
                                        if c == 0:
                                            c = tb.Cash
                                        c = c - a.IncreaseDecreaseInCash
                                        cf.CashBeginningBalance = c
                                        #
                                        c = cf.CashBeginningBalance
                                        c = c + a.IncreaseDecreaseInCash
                                        c = c - tb.Cash
                                        a.CashFlowCashExplainedDifference = c
                                    except:
                                        pass
                                    #
                                    # supplemental cash flow disclosure
                                    try:
                                        #
                                        # Cash paid for in interest
                                        try:
                                            CashPaidForInterest = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > FinancingActivitiesRank:
                                                    d = key
                                                    q = [
                                                        'CashPaidForInterest',
                                                    ]
                                                    b = [
                                                        'Deferred',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while CashFlowStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = CashFlowStatement[key][i]
                                                                    CashFlowStatement[key][i] = None
                                                                except:
                                                                    if CashFlowStatement[key] != None:
                                                                        ARCHvalue = CashFlowStatement[key]
                                                                        CashFlowStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    CashPaidForInterest.append(ARCHvalue)
                                                r = r + 1
                                            cf.CashPaidForInterest = sum(CashPaidForInterest)
                                        except:
                                            pass
                                        #
                                        # Cash paid for taxes
                                        try:
                                            CashPaidForTaxes = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > FinancingActivitiesRank:
                                                    d = key
                                                    q = [
                                                        'CashPaidForIncomeTax',
                                                        'CashPaidForTax',
                                                        'IncomeTaxesPaid',
                                                    ]
                                                    b = [
                                                        'Deferred',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while CashFlowStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = CashFlowStatement[key][i]
                                                                    CashFlowStatement[key][i] = None
                                                                except:
                                                                    if CashFlowStatement[key] != None:
                                                                        ARCHvalue = CashFlowStatement[key]
                                                                        CashFlowStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    CashPaidForTaxes.append(ARCHvalue)
                                                r = r + 1
                                            cf.CashPaidForTaxes = sum(CashPaidForTaxes)
                                        except:
                                            pass
                                    except:
                                        pass
                                    #
                                    # dataframe
                                    try:
                                        #
                                        df = pd.DataFrame({
                                            #
                                            '..': 
                                                [
                                                'a.IncreaseDecreaseInCash',
                                                'cf.CashPaidForInterest',
                                                'cf.CashPaidForTaxes',
                                                ],
                                            #
                                            '.':
                                                [
                                                '{:,}'.format(a.IncreaseDecreaseInCash),
                                                '{:,}'.format(cf.CashPaidForInterest),
                                                '{:,}'.format(cf.CashPaidForTaxes),
                                                ],
                                        })
                                        print(df)
                                        print('\n' + 137 * '-' + '\n')
                                        #
                                        tb.save()
                                        a.save()
                                    except:
                                        pass
                                    #
                                    # anomalies attributable to the SEC
                                    try:
                                        #
                                        print(e.EntityRegistrantName)
                                        print('anomalies attributable to the SEC')
                                        print(periodenddate)
                                        print(137 * '-' + '\n')
                                        #
                                        # Operating Activities
                                        try:
                                            r = 0
                                            OA = 0
                                            f = [
                                                'Beginning',
                                                'CashAcquiredFromAcquisition',
                                                'CashAndCashEquivalents',
                                                'CashProvidedBy',
                                                'CashUsedFor',
                                                'IncomeFromContinuingOperation',
                                                'NetCashProvided',
                                                'NetChangeInOper',
                                                'NetEarning',
                                                'NetIncome',
                                                'NetLoss',
                                                'Net(Loss)',
                                                'Total',
                                            ]
                                            t = [
                                                'OperatingActivitiesDiscontinuedOperations',
                                            ]
                                            for key, value in CashFlowStatement.items():
                                                skip = ''
                                                d = key
                                                if r < OperatingActivitiesRank:
                                                    for g in f:
                                                        if g in d:
                                                            skip = 'skip'
                                                            for y in t:
                                                                if y in d:
                                                                    skip = ''
                                                    if skip == '':
                                                        if value != None:
                                                            print(d)
                                                            print('{:,}'.format(value))
                                                            OA = OA + value
                                                r = r + 1
                                            #
                                            c = OA
                                            c = c - a.OperatingActivities
                                            c = c - a.NetIncome
                                            a.AnomalyOperatingActivitiesSEC = c
                                            #
                                            # dataframe
                                            try:
                                                #
                                                df = pd.DataFrame({
                                                    #
                                                    'operating activities': 
                                                        [
                                                        'Total',
                                                        'Components',
                                                        'SEC Anomaly',
                                                        ],
                                                    #
                                                    '.':
                                                        [
                                                        '{:,}'.format(a.OperatingActivities + a.NetIncome),
                                                        '{:,}'.format(OA),
                                                        '{:,}'.format(a.AnomalyOperatingActivitiesSEC),
                                                        ],
                                                })
                                                print('\n')
                                                print(df)
                                                print('\n' + 137 * '-')
                                                #
                                                cf.save()
                                                a.save()
                                            except:
                                                pass
                                        except:
                                            pass
                                        #
                                        # Investing Activities
                                        try:
                                            #
                                            r = 0
                                            IA = 0
                                            f = [
                                                'Beginning',
                                                'CashAndCashEquivalents',
                                                'NetChange',
                                                'CashProvidedBy',
                                                'CashUsedFor',
                                                'Total',
                                            ]
                                            t = [
                                                'InvestingActivitiesDiscontinuedOperations',
                                            ]
                                            for key, value in CashFlowStatement.items():
                                                skip = ''
                                                d = key
                                                if r > OperatingActivitiesRank:
                                                    if r < InvestingActivitiesRank:
                                                        for g in f:
                                                            if g in d:
                                                                skip = 'skip'
                                                                for y in t:
                                                                    if y in d:
                                                                        skip = ''
                                                        if skip == '':
                                                            if value != None:
                                                                print(d)
                                                                print('{:,}'.format(value))
                                                                IA = IA + value
                                                r = r + 1
                                            #
                                            c = IA
                                            c = c - a.InvestingActivities
                                            a.AnomalyInvestingActivitiesSEC = c
                                            #
                                            # dataframe
                                            try:
                                                #
                                                df = pd.DataFrame({
                                                    #
                                                    'investing activities': 
                                                        [
                                                        'Total',
                                                        'Components',
                                                        'SEC Anomaly',
                                                        ],
                                                    #
                                                    '.':
                                                        [
                                                        '{:,}'.format(a.InvestingActivities),
                                                        '{:,}'.format(IA),
                                                        '{:,}'.format(a.AnomalyInvestingActivitiesSEC),
                                                        ],
                                                })
                                                print('\n')
                                                print(df)
                                                print('\n' + 137 * '-')
                                                #
                                                cf.save()
                                                a.save()
                                            except:
                                                pass
                                        except:
                                            pass
                                        #
                                        # Financing Activities
                                        try:
                                            r = 0
                                            FA = 0
                                            skip = ''
                                            f = [
                                                'CashProvidedBy',
                                                'CashUsedFor',
                                                'ContinuingOperations',
                                                'NetCashProvided',
                                                'NetChangeInFinancing',
                                                'Net(Loss)'
                                                'NetLoss'
                                                'Total',
                                            ]
                                            t = [
                                                'FinancingActivitiesDiscontinuedOperations',
                                            ]
                                            h = [
                                                'Payment',
                                                'Purchase',
                                                'Repayment',
                                                'Repurchase',
                                            ]
                                            i = [
                                                '(Paymen',
                                                '(Purchas',
                                                '(Repaymen',
                                                '(Repurchas',
                                            ]
                                            x = [
                                                'PurchasePlan',
                                                'PaymentArrangement',
                                                'NetOfShareRepurchasesForWithholdingTaxes',
                                            ]
                                            for key, value in CashFlowStatement.items():
                                                skip = ''
                                                d = key
                                                for w in x:
                                                    d = d.replace(w,'')
                                                if r > InvestingActivitiesRank:
                                                    if r < FinancingActivitiesRank:
                                                        if value != None:
                                                            for g in f:
                                                                if g in d:
                                                                    skip = 'skip'
                                                                    for y in t:
                                                                        if y in d:
                                                                            skip = ''
                                                            if skip == '':
                                                                for k in h:
                                                                    if k in d:
                                                                        y = 'y'
                                                                        for t in i:
                                                                            if t in d:
                                                                                y = 'n'
                                                                        if y == 'y':
                                                                            value = -abs(value)
                                                                if value != None:
                                                                    print(d)
                                                                    print('{:,}'.format(value))
                                                                    FA = FA + value
                                                r = r + 1
                                            #
                                            c = FA
                                            c = c - a.FinancingActivities
                                            a.AnomalyFinancingActivitiesSEC = c
                                            #
                                            # dataframe
                                            try:
                                                #
                                                df = pd.DataFrame({
                                                    #
                                                    'financing activities': 
                                                        [
                                                        'Total',
                                                        'Components',
                                                        'SEC Anomaly',
                                                        ],
                                                    #
                                                    '.':
                                                        [
                                                        '{:,}'.format(a.FinancingActivities),
                                                        '{:,}'.format(FA),
                                                        '{:,}'.format(a.AnomalyFinancingActivitiesSEC),
                                                        ],
                                                })
                                                print('\n')
                                                print(df)
                                                print('\n' + 137 * '-' + '\n')
                                                #
                                                cf.save()
                                                a.save()
                                            except:
                                                pass
                                        except:
                                            pass
                                    except:
                                        pass
                                    #
                                    # operating activities components
                                    try:
                                        print(e.EntityRegistrantName)
                                        print('operating activities')
                                        print(periodenddate)
                                        print(137 * '-' + '\n')
                                        #
                                        # depreciation depletion and amortization
                                        try:
                                            DepreciationDepletionAndAmortization = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r < OperatingActivitiesRank:
                                                    d = key
                                                    q = [
                                                        'Depreciation',
                                                        'Amortization',
                                                    ]
                                                    b = [
                                                        'Acquire',
                                                        'Acquisition',
                                                        'Debt',
                                                        'Decrease',
                                                        'Disposal',
                                                        'DiscontinuedOperation',
                                                        'Ending',
                                                        'Financing',
                                                        'Hedge',
                                                        'Increase',
                                                        'Impairment',
                                                        'Investment',
                                                        'Investing',
                                                        'Payment',
                                                        'Premium',
                                                        'Proceeds',
                                                        'Purchase',
                                                        'Selling',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while CashFlowStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = CashFlowStatement[key][i]
                                                                    CashFlowStatement[key][i] = None
                                                                except:
                                                                    if CashFlowStatement[key] != None:
                                                                        ARCHvalue = CashFlowStatement[key]
                                                                        CashFlowStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    DepreciationDepletionAndAmortization.append(ARCHvalue)
                                                r = r + 1
                                            cf.DepreciationDepletionAndAmortization = sum(DepreciationDepletionAndAmortization)
                                        except:
                                            pass
                                        #
                                        # Gain (Loss) Related To Disposal Or Sale
                                        try:
                                            GainRelatedToDisposalOrSale = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r < OperatingActivitiesRank:
                                                    d = key
                                                    q = [
                                                        'InvestmentGain',
                                                        'LossesOnDisposal',
                                                        '(Losses)OnDisposal',
                                                        'LossOnDisposal',
                                                        '(Loss)OnDisposal',
                                                        'Loss(Gain)',
                                                        'LossOnDebtConversion',
                                                        '(Loss)OnDebtConversion',
                                                        'LossesOnDebtConversion',
                                                        '(Losses)OnDebtConversion',
                                                        'GainOnDebtConversion',
                                                        'GainsOnDebtConversion',
                                                        '(Gain)OnDebtConversion',
                                                        '(Gains)OnDebtConversion',
                                                        'LossOnDisposal',
                                                        'GainRelatedTo',
                                                        'Gain(Loss',
                                                        'GainOnDisposal',
                                                        '(Gain)OnDisposal',
                                                        'GainsOnDisposal',
                                                        '(Gains)OnDisposal',
                                                        'GainOnDisposition',
                                                        'GainOnDivestiture',
                                                        'GainOnInsurance',
                                                        'GainOnSale',
                                                        'GainRelatedToDisposition',
                                                        'GainsRelatedToDisposition',
                                                        '(Gain)RelatedToDisposition',
                                                        '(Gains)RelatedToDisposition',
                                                        '(Gain)Loss',
                                                        '(Gain)AndLoss',
                                                        '(Gains)AndLoss',
                                                        '(Gains)Loss',
                                                        '(Gains)Loss',
                                                        '(Gains)AndLoss',
                                                        'MarketableEquitySecurit',
                                                        'MarketableSecurit',
                                                        'InvestmentLoss',
                                                        'DispositionOfAssets',
                                                        'SaleOfAssets',
                                                        'SalesOfAssets',
                                                        'SaleOfBuilding',
                                                        'SalesOfBuilding',
                                                        'SaleOfBusiness',
                                                        'SalesOfBusiness',
                                                    ]
                                                    b = [
                                                        'Acquire',
                                                        'Acquisition',
                                                        'Decrease',
                                                        'Ending',
                                                        'Financing',
                                                        'Hedge',
                                                        'Increase',
                                                        'Payment',
                                                        'Purchase',
                                                    ]
                                                    k = [
                                                        'Gain(Loss)',
                                                        'Gain(Losses)',
                                                        'Gains(Losses)',
                                                        'Gains(Loss)',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while CashFlowStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = CashFlowStatement[key][i]
                                                                    CashFlowStatement[key][i] = None
                                                                except:
                                                                    if CashFlowStatement[key] != None:
                                                                        ARCHvalue = CashFlowStatement[key]
                                                                        CashFlowStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    for m in k:
                                                                        if m in d:
                                                                            tempARCHvalue = -abs(ARCHvalue)
                                                                            if ARCHvalue != tempARCHvalue:
                                                                                c = a.AnomalyOperatingActivitiesSEC
                                                                                c = c + tempARCHvalue
                                                                                c = c - ARCHvalue
                                                                                a.AnomalyOperatingActivitiesSEC = c 
                                                                                ARCHvalue = tempARCHvalue
                                                                    GainRelatedToDisposalOrSale.append(ARCHvalue)
                                                r = r + 1
                                            cf.GainRelatedToDisposalOrSale = sum(GainRelatedToDisposalOrSale)
                                        except:
                                            pass
                                        #
                                        # Restructuring And Other Special Charges
                                        try:
                                            RestructuringAndOtherSpecialCharges = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r < OperatingActivitiesRank:
                                                    d = key
                                                    q = [
                                                        'BadDebt',
                                                        'Settlement',
                                                        'DebtDiscount',
                                                        'Depletion',
                                                        'DiscontinuedOperation',
                                                        'Impairment',
                                                        'LossOnExtinguishmentOfDebt',
                                                        'LossesOnExtinguishmentOfDebt',
                                                        '(Loss)OnExtinguishmentOfDebt',
                                                        '(Losses)OnExtinguishmentOfDebt',
                                                        'GainOnExtinguishmentOfDebt',
                                                        'GainsOnExtinguishmentOfDebt',
                                                        '(Gain)OnExtinguishmentOfDebt',
                                                        '(Gains)OnExtinguishmentOfDebt',
                                                        'Refinancing',
                                                        'Restructuring',
                                                        'Special',
                                                    ]
                                                    b = [
                                                        'Acquire',
                                                        'Acquisition',
                                                        'Decrease',
                                                        'Ending',
                                                        'Financing',
                                                        'Hedge',
                                                        'Increase',
                                                        'Payment',
                                                        'Purchase',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while CashFlowStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = CashFlowStatement[key][i]
                                                                    CashFlowStatement[key][i] = None
                                                                except:
                                                                    if CashFlowStatement[key] != None:
                                                                        ARCHvalue = CashFlowStatement[key]
                                                                        CashFlowStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    RestructuringAndOtherSpecialCharges.append(ARCHvalue)
                                                r = r + 1
                                            cf.RestructuringAndOtherSpecialCharges = sum(RestructuringAndOtherSpecialCharges)
                                        except:
                                            pass
                                        #
                                        # Accrued Employee Compensation
                                        try:
                                            AccruedEmployeeCompensation = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r < OperatingActivitiesRank:
                                                    d = key
                                                    q = [
                                                        'AccruedBenefits',
                                                        'Compensation',
                                                    ]
                                                    b = [
                                                        'Acquire',
                                                        'Acquisition',
                                                        'Decrease',
                                                        'Disposal',
                                                        'DiscontinuedOperation',
                                                        'Ending',
                                                        'Equity',
                                                        'Financing',
                                                        'Hedge',
                                                        'Increase',
                                                        'Investment',
                                                        'Investing',
                                                        'Operating',
                                                        'Payment',
                                                        'Proceeds',
                                                        'Purchase',
                                                        'Selling',
                                                        'ShareBasedCompensation',
                                                        'StockBasedCompensation',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while CashFlowStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = CashFlowStatement[key][i]
                                                                    CashFlowStatement[key][i] = None
                                                                except:
                                                                    if CashFlowStatement[key] != None:
                                                                        ARCHvalue = CashFlowStatement[key]
                                                                        CashFlowStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    AccruedEmployeeCompensation.append(ARCHvalue)
                                                r = r + 1
                                            cf.AccruedEmployeeCompensation = sum(AccruedEmployeeCompensation)
                                        except:
                                            pass                
                                        #
                                        # share based compensation
                                        try:
                                            ShareBasedCompensation = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r < OperatingActivitiesRank:
                                                    d = key
                                                    q = [
                                                        'EquityBasedCompensation',
                                                        'EquityBasedEmployeeCompensation',
                                                        'EquityBasedPayment',
                                                        'EquityBasedEmployeePayment',
                                                        'ShareBasedCompensation',
                                                        'ShareBasedEmployeeCompensation',
                                                        'StockBasedCompensation',
                                                        'StockBasedEmployeeCompensation',
                                                    ]
                                                    b = [
                                                        'Acquire',
                                                        'Acquisition',
                                                        'Decrease',
                                                        'Disposal',
                                                        'DiscontinuedOperation',
                                                        'Employee',
                                                        'Ending',
                                                        'Financing',
                                                        'Hedge',
                                                        'Increase',
                                                        'Investment',
                                                        'Investing',
                                                        'Operating',
                                                        'Proceeds',
                                                        'Purchase',
                                                        'Selling',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while CashFlowStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = CashFlowStatement[key][i]
                                                                    CashFlowStatement[key][i] = None
                                                                except:
                                                                    if CashFlowStatement[key] != None:
                                                                        ARCHvalue = CashFlowStatement[key]
                                                                        CashFlowStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    ShareBasedCompensation.append(ARCHvalue)
                                                r = r + 1
                                            cf.ShareBasedCompensation = sum(ShareBasedCompensation)
                                        except:
                                            pass
                                        #
                                        # increase decrease in income tax expense (benefit)
                                        try:
                                            IncreaseDecreaseInIncomeTaxExpenseBenefit = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r < OperatingActivitiesRank:
                                                    d = key
                                                    q = [
                                                        'IncomeTax',
                                                        'DeferredTax',
                                                        'DeferredBenefitForIncomeTax',
                                                        'DeferredBenefitsForIncomeTax',
                                                        'DeferredBenefitForTax',
                                                        'DeferredBenefitsForTax',
                                                        'CurrentTax',
                                                        'TaxProvision',
                                                        'Deferredincometax',
                                                        'TaxAct',
                                                        'TaxBenefit',
                                                        'TaxPayable',
                                                    ]
                                                    b = [
                                                        'Purchase',
                                                        'Acquisition',
                                                        'Acquire',
                                                        'CashPaidFor',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while CashFlowStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = CashFlowStatement[key][i]
                                                                    CashFlowStatement[key][i] = None
                                                                except:
                                                                    if CashFlowStatement[key] != None:
                                                                        ARCHvalue = CashFlowStatement[key]
                                                                        CashFlowStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    IncreaseDecreaseInIncomeTaxExpenseBenefit.append(ARCHvalue)
                                                r = r + 1
                                            cf.IncreaseDecreaseInIncomeTaxExpenseBenefit = sum(IncreaseDecreaseInIncomeTaxExpenseBenefit)
                                        except:
                                            pass
                                        #
                                        # other non cash income expense
                                        try:
                                            OtherNonCashIncomeExpense = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r < OperatingActivitiesRank:
                                                    d = key
                                                    q = [
                                                        'Amortization(Accretion)',
                                                        'AmortizationAccretion',
                                                        'DebtIssuanceCost',
                                                        'ForeignCurrency',
                                                        'LandlordContribution',
                                                        'NoncashIncomeExpense',
                                                        'NonCashInterest',
                                                        'NonCashRent',
                                                    ]
                                                    b = [
                                                        'Payment',
                                                        'Purchase',
                                                        'Acquisition',
                                                        'Acquire',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while CashFlowStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = CashFlowStatement[key][i]
                                                                    CashFlowStatement[key][i] = None
                                                                except:
                                                                    if CashFlowStatement[key] != None:
                                                                        ARCHvalue = CashFlowStatement[key]
                                                                        CashFlowStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    OtherNonCashIncomeExpense.append(ARCHvalue)
                                                r = r + 1
                                            cf.OtherNonCashIncomeExpense = sum(OtherNonCashIncomeExpense)
                                        except:
                                            pass
                                        #
                                        # increase (decrease) in accounts receivable
                                        try:
                                            IncreaseDecreaseInAccountsReceivable = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r < OperatingActivitiesRank:
                                                    d = key
                                                    q = [
                                                        'CreditLossesAndChargebacks',
                                                        'DoubtfulAccounts',
                                                        'Receivable',
                                                        'UncollectibleProvision',
                                                    ]
                                                    b = [
                                                        'NonTrade',
                                                        'Payment',
                                                        'Purchase',
                                                        'Acquisition',
                                                        'Acquire',
                                                        'RepurchaseAgreements',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while CashFlowStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = CashFlowStatement[key][i]
                                                                    CashFlowStatement[key][i] = None
                                                                except:
                                                                    if CashFlowStatement[key] != None:
                                                                        ARCHvalue = CashFlowStatement[key]
                                                                        CashFlowStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    IncreaseDecreaseInAccountsReceivable.append(ARCHvalue)
                                                r = r + 1
                                            cf.IncreaseDecreaseInAccountsReceivable = sum(IncreaseDecreaseInAccountsReceivable)
                                        except:
                                            pass
                                        #
                                        # increase (decrease) in prepaid expenses
                                        try:
                                            IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r < OperatingActivitiesRank:
                                                    d = key
                                                    q = [
                                                        'DeferredExpense',
                                                        'DeferredRent',
                                                        'Deposits',
                                                        'Prepaid',
                                                    ]
                                                    b = [
                                                        'Acquire',
                                                        'Acquisition',
                                                        'Income',
                                                        'NonTrade',
                                                        'Payment',
                                                        'Purchase',
                                                        'Tax',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while CashFlowStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = CashFlowStatement[key][i]
                                                                    CashFlowStatement[key][i] = None
                                                                except:
                                                                    if CashFlowStatement[key] != None:
                                                                        ARCHvalue = CashFlowStatement[key]
                                                                        CashFlowStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets.append(ARCHvalue)
                                                r = r + 1
                                            cf.IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets = sum(IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets)
                                        except:
                                            pass
                                        #
                                        # increase (decrease) in inventories
                                        try:
                                            IncreaseDecreaseInInventories = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r < OperatingActivitiesRank:
                                                    d = key
                                                    q = [
                                                        'Inventor',
                                                        'Fifo',
                                                        'Lifo',
                                                    ]
                                                    b = [
                                                        'NonTrade',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while CashFlowStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = CashFlowStatement[key][i]
                                                                    CashFlowStatement[key][i] = None
                                                                except:
                                                                    if CashFlowStatement[key] != None:
                                                                        ARCHvalue = CashFlowStatement[key]
                                                                        CashFlowStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    IncreaseDecreaseInInventories.append(ARCHvalue)
                                                r = r + 1
                                            cf.IncreaseDecreaseInInventories = sum(IncreaseDecreaseInInventories)
                                        except:
                                            pass
                                        #
                                        # increase (decrease) in other receivables and prepaid expenses
                                        try:
                                            IncreaseDecreaseInOtherReceivables = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r < OperatingActivitiesRank:
                                                    d = key
                                                    q = [
                                                        'OtherReceivables',
                                                        'NonTrade',
                                                    ]
                                                    b = [
                                                        'Payment',
                                                        'Purchase',
                                                        'Acquisition',
                                                        'Acquire',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while CashFlowStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = CashFlowStatement[key][i]
                                                                    CashFlowStatement[key][i] = None
                                                                except:
                                                                    if CashFlowStatement[key] != None:
                                                                        ARCHvalue = CashFlowStatement[key]
                                                                        CashFlowStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    IncreaseDecreaseInOtherReceivables.append(ARCHvalue)
                                                r = r + 1
                                            cf.IncreaseDecreaseInOtherReceivables = sum(IncreaseDecreaseInOtherReceivables)
                                        except:
                                            pass
                                        #
                                        # increase (decrease) in accounts payable and accrued liabilities
                                        try:
                                            IncreaseDecreaseInAccountsPayableAndAccruedLiabilities = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r < OperatingActivitiesRank:
                                                    d = key
                                                    q = [
                                                        'AccountPayable',
                                                        'AccountsPayable',
                                                        'AccruedLiabilit',
                                                        'AccruedExpense',
                                                    ]
                                                    b = [
                                                        'Acquire',
                                                        'Acquisition',
                                                        'NonTrade',
                                                        'Payment',
                                                        'PropertyAndEquipmentInAccountsPayable',
                                                        'Purchase',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while CashFlowStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = CashFlowStatement[key][i]
                                                                    CashFlowStatement[key][i] = None
                                                                except:
                                                                    if CashFlowStatement[key] != None:
                                                                        ARCHvalue = CashFlowStatement[key]
                                                                        CashFlowStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    IncreaseDecreaseInAccountsPayableAndAccruedLiabilities.append(ARCHvalue)
                                                r = r + 1
                                            cf.IncreaseDecreaseInAccountsPayableAndAccruedLiabilities = sum(IncreaseDecreaseInAccountsPayableAndAccruedLiabilities)
                                        except:
                                            pass
                                        #
                                        # increase (decrease) in contract with customer liability
                                        try:
                                            IncreaseDecreaseInContractWithCustomerLiability = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r < OperatingActivitiesRank:
                                                    d = key
                                                    q = [
                                                        'ContractWithCustomer',
                                                        'DeferredRevenue',
                                                        'CustomerDeposits',
                                                    ]
                                                    b = [
                                                        'NonTrade',
                                                        'Payment',
                                                        'Purchase',
                                                        'Acquisition',
                                                        'Acquire',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while CashFlowStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = CashFlowStatement[key][i]
                                                                    CashFlowStatement[key][i] = None
                                                                except:
                                                                    if CashFlowStatement[key] != None:
                                                                        ARCHvalue = CashFlowStatement[key]
                                                                        CashFlowStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    IncreaseDecreaseInContractWithCustomerLiability.append(ARCHvalue)
                                                r = r + 1
                                            cf.IncreaseDecreaseInContractWithCustomerLiability = sum(IncreaseDecreaseInContractWithCustomerLiability)
                                        except:
                                            pass
                                        #
                                        # increase (decrease) in retirement and post-retirement benefits
                                        try:
                                            IncreaseDecreaseInRetirementBenefits = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r < OperatingActivitiesRank:
                                                    d = key
                                                    q = [
                                                        'BenefitCost',
                                                        'BenefitsCost',
                                                        'Pension',
                                                        'Retirement',
                                                    ]
                                                    b = [
                                                        'NonTrade',
                                                        'Payment',
                                                        'Purchase',
                                                        'Acquisition',
                                                        'Acquire',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while CashFlowStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = CashFlowStatement[key][i]
                                                                    CashFlowStatement[key][i] = None
                                                                except:
                                                                    if CashFlowStatement[key] != None:
                                                                        ARCHvalue = CashFlowStatement[key]
                                                                        CashFlowStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    IncreaseDecreaseInRetirementBenefits.append(ARCHvalue)
                                                r = r + 1
                                            cf.IncreaseDecreaseInRetirementBenefits = sum(IncreaseDecreaseInRetirementBenefits)
                                        except:
                                            pass
                                        #
                                        # increase (decrease) in finance lease current
                                        try:
                                            IncreaseDecreaseFinanceLeaseCurrent = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r < OperatingActivitiesRank:
                                                    d = key
                                                    q = [
                                                        'CapitalLease',
                                                        'FinanceLease',
                                                        'FinancingLease',
                                                        'FinancingObligation',
                                                    ]
                                                    b = [
                                                        'Acquisition',
                                                        'Acquire',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while CashFlowStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = CashFlowStatement[key][i]
                                                                    CashFlowStatement[key][i] = None
                                                                except:
                                                                    if CashFlowStatement[key] != None:
                                                                        ARCHvalue = CashFlowStatement[key]
                                                                        CashFlowStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    IncreaseDecreaseFinanceLeaseCurrent.append(ARCHvalue)
                                                r = r + 1
                                            cf.IncreaseDecreaseFinanceLeaseCurrent = sum(IncreaseDecreaseFinanceLeaseCurrent)
                                        except:
                                            pass
                                        #
                                        # increase (decrease) in operating lease current
                                        try:
                                            IncreaseDecreaseOperatingLeaseCurrent = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r < OperatingActivitiesRank:
                                                    d = key
                                                    q = [
                                                        'OperatingLease',
                                                        'LeaseLiabilit',
                                                    ]
                                                    b = [
                                                        'Acquisition',
                                                        'Acquire',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while CashFlowStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = CashFlowStatement[key][i]
                                                                    CashFlowStatement[key][i] = None
                                                                except:
                                                                    if CashFlowStatement[key] != None:
                                                                        ARCHvalue = CashFlowStatement[key]
                                                                        CashFlowStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    IncreaseDecreaseOperatingLeaseCurrent.append(ARCHvalue)
                                                r = r + 1
                                            cf.IncreaseDecreaseOperatingLeaseCurrent = sum(IncreaseDecreaseOperatingLeaseCurrent)
                                        except:
                                            pass
                                        #
                                        # increase (decrease) in fair value of derivaties
                                        try:
                                            IncreaseDecreaseInFairValueOfDerivativesOperating = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r < OperatingActivitiesRank:
                                                    d = key
                                                    q = [
                                                        'Derivative',
                                                        'Swap',
                                                    ]
                                                    b = [
                                                        'Acquisition',
                                                        'Acquire',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while CashFlowStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = CashFlowStatement[key][i]
                                                                    CashFlowStatement[key][i] = None
                                                                except:
                                                                    if CashFlowStatement[key] != None:
                                                                        ARCHvalue = CashFlowStatement[key]
                                                                        CashFlowStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    IncreaseDecreaseInFairValueOfDerivativesOperating.append(ARCHvalue)
                                                r = r + 1
                                            cf.IncreaseDecreaseInFairValueOfDerivativesOperating = sum(IncreaseDecreaseInFairValueOfDerivativesOperating)
                                        except:
                                            pass
                                        #
                                        # increase (decrease) in other operating activities
                                        try:
                                            IncreaseDecreaseInOtherOperatingActivities = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r < OperatingActivitiesRank:
                                                    d = key
                                                    q = [
                                                        'CurrentAssetsAndCurrentLiabilit',
                                                        'Other',
                                                        'Miscellaneous',
                                                    ]
                                                    b = [
                                                        'NetChangeInOperatingAssetsAndLiabilities',
                                                        'NonTrade',
                                                        'Payment',
                                                        'Acquisition',
                                                        'Investing',
                                                        'Financing',
                                                        'PropertyAndEquipment',
                                                    ]
                                                    for l in q:
                                                        if l in d:
                                                            h = 'p'
                                                            for p in b:
                                                                u = 0
                                                                while u < len(b):
                                                                    if p in d:
                                                                        h = ''
                                                                    u = u + 1
                                                            if h == 'p':
                                                                try:
                                                                    i = 0
                                                                    while CashFlowStatement[key][i] == None:
                                                                        i = i + 1
                                                                    ARCHvalue = CashFlowStatement[key][i]
                                                                    CashFlowStatement[key][i] = None
                                                                except:
                                                                    if CashFlowStatement[key] != None:
                                                                        ARCHvalue = CashFlowStatement[key]
                                                                        CashFlowStatement[key] = None
                                                                    else:
                                                                        ARCHvalue = 0
                                                                if ARCHvalue != 0:
                                                                    IncreaseDecreaseInOtherOperatingActivities.append(ARCHvalue)
                                                r = r + 1
                                            c = sum(IncreaseDecreaseInOtherOperatingActivities)
                                            c = c - a.AnomalyOperatingActivitiesSEC
                                            cf.IncreaseDecreaseInOtherOperatingActivities = c
                                        except:
                                            pass
                                        #
                                        # ML
                                        try:
                                            w = None
                                            a.OperatingActivitiesGL_i = ''
                                            m = None
                                            a.OperatingActivitiesGL_ii = ''
                                            t = None
                                            a.OperatingActivitiesGL_iii = ''
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r < OperatingActivitiesRank:
                                                    d = key
                                                    b = [
                                                        'Total',
                                                    ]
                                                    h = 'p'
                                                    for p in b:
                                                        u = 0
                                                        while u < len(b):
                                                            if p in d:
                                                                h = ''
                                                            u = u + 1
                                                    if h == 'p':
                                                        try:
                                                            i = 0
                                                            while CashFlowStatement[key][i] == None:
                                                                i = i + 1
                                                            ARCHvalue = CashFlowStatement[key][i]
                                                            CashFlowStatement[key][i] = None
                                                        except:
                                                            if CashFlowStatement[key] != None:
                                                                ARCHvalue = CashFlowStatement[key]
                                                                CashFlowStatement[key] = None
                                                            else:
                                                                ARCHvalue = 0
                                                        if ARCHvalue != 0:
                                                            try:
                                                                #
                                                                if w is None:
                                                                    a.OperatingActivitiesGL_i = d
                                                                    w = ''
                                                                #
                                                                elif m is None:
                                                                    a.OperatingActivitiesGL_ii = d
                                                                    m = ''
                                                                #
                                                                elif t is None:
                                                                    a.OperatingActivitiesGL_iii = d
                                                                    t = ''
                                                                else:
                                                                    pass
                                                                #
                                                                if d not in OperatingActivitiesGL:
                                                                    OperatingActivitiesGL.append(d)
                                                            #
                                                            except:
                                                                pass
                                                r = r + 1
                                        except:
                                            pass
                                        #
                                        # dataframe
                                        try:
                                            #
                                            df = pd.DataFrame({
                                                #
                                                '..': 
                                                    [
                                                    'cf.DepreciationDepletionAndAmortization',
                                                    'cf.GainRelatedToDisposalOrSale',
                                                    'cf.ShareBasedCompensation',
                                                    'cf.RestructuringAndOtherSpecialCharges',
                                                    'cf.AccruedEmployeeCompensation',
                                                    'cf.IncreaseDecreaseInIncomeTaxExpenseBenefit',
                                                    'cf.OtherNonCashIncomeExpense',
                                                    'cf.IncreaseDecreaseInAccountsReceivable',
                                                    'cf.IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets',
                                                    'cf.IncreaseDecreaseInInventories',
                                                    'cf.IncreaseDecreaseInOtherReceivables',
                                                    'cf.IncreaseDecreaseInAccountsPayableAndAccruedLiabilities',
                                                    'cf.IncreaseDecreaseInContractWithCustomerLiability',
                                                    'cf.IncreaseDecreaseInRetirementBenefits',
                                                    'cf.IncreaseDecreaseFinanceLeaseCurrent',
                                                    'cf.IncreaseDecreaseOperatingLeaseCurrent',
                                                    'cf.IncreaseDecreaseInFairValueOfDerivativesOperating',
                                                    'cf.IncreaseDecreaseInOtherOperatingActivities',
                                                    ],
                                                #
                                                '.':
                                                    [
                                                    '{:,}'.format(cf.DepreciationDepletionAndAmortization),
                                                    '{:,}'.format(cf.GainRelatedToDisposalOrSale),
                                                    '{:,}'.format(cf.ShareBasedCompensation),
                                                    '{:,}'.format(cf.RestructuringAndOtherSpecialCharges),
                                                    '{:,}'.format(cf.AccruedEmployeeCompensation),
                                                    '{:,}'.format(cf.IncreaseDecreaseInIncomeTaxExpenseBenefit),
                                                    '{:,}'.format(cf.OtherNonCashIncomeExpense),
                                                    '{:,}'.format(cf.IncreaseDecreaseInAccountsReceivable),
                                                    '{:,}'.format(cf.IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets),
                                                    '{:,}'.format(cf.IncreaseDecreaseInInventories),
                                                    '{:,}'.format(cf.IncreaseDecreaseInOtherReceivables),
                                                    '{:,}'.format(cf.IncreaseDecreaseInAccountsPayableAndAccruedLiabilities),
                                                    '{:,}'.format(cf.IncreaseDecreaseInContractWithCustomerLiability),
                                                    '{:,}'.format(cf.IncreaseDecreaseInRetirementBenefits),
                                                    '{:,}'.format(cf.IncreaseDecreaseFinanceLeaseCurrent),
                                                    '{:,}'.format(cf.IncreaseDecreaseOperatingLeaseCurrent),
                                                    '{:,}'.format(cf.IncreaseDecreaseInFairValueOfDerivativesOperating),
                                                    '{:,}'.format(cf.IncreaseDecreaseInOtherOperatingActivities),
                                                    ],
                                            })
                                            print(df)
                                            print('\n' + 137 * '-' + '\n')
                                            #
                                            tb.save()
                                            a.save()
                                        except:
                                            pass
                                    except:
                                        pass
                                    #
                                    # investing activities components
                                    try:
                                        print(e.EntityRegistrantName)
                                        print('investing activities')
                                        print(periodenddate)
                                        print(137 * '-' + '\n')
                                        #
                                        # Payments To Acquire Investment
                                        try:
                                            PaymentsToAcquireInvestments = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > OperatingActivitiesRank:
                                                    if r < InvestingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'Acquisition',
                                                            'ConvertibleNote',
                                                            'Investment',
                                                            'Maturitie',
                                                            'NoteReceivable',
                                                            'NotesReceivable',
                                                            'Securit',
                                                            'TradingAsset',
                                                        ]
                                                        b = [
                                                            'Begin',
                                                            'CashAnd',
                                                            'Disposal',
                                                            'Disposition',
                                                            'End',
                                                            'Gain(Loss)',
                                                            'Maturities',
                                                            'Proceeds',
                                                            'SaleOf',
                                                            'SalesOf',
                                                            'Sell',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        PaymentsToAcquireInvestments.append(ARCHvalue)
                                                r = r + 1
                                            cf.PaymentsToAcquireInvestments = sum(PaymentsToAcquireInvestments)
                                        except:
                                            pass
                                        #
                                        # Proceeds Of Investment
                                        try:
                                            ProceedsOfInvestments = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > OperatingActivitiesRank:
                                                    if r < InvestingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'ConvertibleNote',
                                                            'FinancialInstrument',
                                                            'Investment',
                                                            'Securit',
                                                            'TradingAsset',
                                                            'Maturities',
                                                            'NotesReceivable',
                                                            'DispositionOfLongTermAsset',
                                                            'SaleLeaseBack',
                                                            'SaleOfMajorityOwnedSubs',
                                                            'SettlementOfNetInvestment',
                                                            'PromissoryNote',
                                                            'ReturnOfCapital',
                                                        ]
                                                        b = [
                                                            'Addition',
                                                            'Begin',
                                                            'CashAnd',
                                                            'End',
                                                            'Payment',
                                                            'Purchase',
                                                            'Acquisition',
                                                            'Acquire',
                                                            'PropertyAndEquipment',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        ProceedsOfInvestments.append(ARCHvalue)
                                                r = r + 1
                                            cf.ProceedsOfInvestments = sum(ProceedsOfInvestments)
                                        except:
                                            pass
                                        #
                                        # Payments To Acquire Property Plant And Equipment
                                        try:
                                            PaymentsToAcquirePropertyPlantAndEquipment = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > OperatingActivitiesRank:
                                                    if r < InvestingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'Equipment',
                                                            'Property',
                                                            'CapitalExpenditures',
                                                            'DeferredTurnaroundAndCatalystCosts',
                                                            'PurchasesOfSolarEnergySystems',
                                                        ]
                                                        b = [
                                                            'Proceed',
                                                            'Disposal',
                                                            'Selling',
                                                            'Sold',
                                                            'AccountsPayable',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        PaymentsToAcquirePropertyPlantAndEquipment.append(ARCHvalue)
                                                r = r + 1
                                            cf.PaymentsToAcquirePropertyPlantAndEquipment = -abs(sum(PaymentsToAcquirePropertyPlantAndEquipment))
                                        except:
                                            pass
                                        #
                                        # Proceeds From Disposal of Property Plant And Equipment
                                        try:
                                            ProceedsFromDisposalsOfPropertyAndEquipment = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > OperatingActivitiesRank:
                                                    if r < InvestingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'Property',
                                                            'DisposalOfAsset',
                                                            'SaleOfBuilding',
                                                        ]
                                                        b = [
                                                            'Payment',
                                                            'Purchase',
                                                            'Acquisition',
                                                            'Acquire',
                                                            'Addition',
                                                            'PropertyAndEquipmentInAccountsPayable',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        ProceedsFromDisposalsOfPropertyAndEquipment.append(ARCHvalue)
                                                r = r + 1
                                            cf.ProceedsFromDisposalsOfPropertyAndEquipment = sum(ProceedsFromDisposalsOfPropertyAndEquipment)
                                        except:
                                            pass
                                        #
                                        # Payments To Acquire Businesses and Intangibles Net Of Cash Acquired
                                        try:
                                            PaymentsToAcquireBusinessesAndIntangibles = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > OperatingActivitiesRank:
                                                    if r < InvestingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'AcquireBusiness',
                                                            'AcquiredBusiness',
                                                            'AcquisitionOfBusiness',
                                                            'AcquisitionOfValero',
                                                            'AcquisitionOfUndividedInterest',
                                                            'AcquisitionsNetOfCashAcquired',
                                                            'BusinessAcquisitions',
                                                            'BusinessCombinations',
                                                            'CashPaidForAcquisitions',
                                                            'Intangible',
                                                            'PeruAcquisition',
                                                            'Mergers',
                                                            'PurchasesOfAffAsset',
                                                            'PurchasesOfRestaurant',
                                                            'PurchasesOfStores',
                                                            'Software',
                                                            'StrategicInvestments',
                                                            'PendingAcquisition',
                                                        ]
                                                        b = [
                                                            'Proceed',
                                                            'Disposal',
                                                            'Sell',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        PaymentsToAcquireBusinessesAndIntangibles.append(ARCHvalue)
                                                r = r + 1
                                            cf.PaymentsToAcquireBusinessesAndIntangibles = sum(PaymentsToAcquireBusinessesAndIntangibles)
                                        except:
                                            pass
                                        #
                                        # Proceeds From Disposals Of Businesses and Intangibles
                                        try:
                                            ProceedsFromDisposalsOfBusinessesAndIntangibles = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > OperatingActivitiesRank:
                                                    if r < InvestingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'Divestiture',
                                                            'SaleOfMonster',
                                                            'TransferOfDistributionRights',
                                                            'DisposalOfCertainOperations',
                                                            'ReverseRepurchaseAgreement',
                                                            'SaleOfAsset',
                                                            'SalesOfAsset',
                                                            'SaleOfBusiness',
                                                            'SalesOfBusiness',
                                                            'SaleOfSubsidiary',
                                                            'SalesOfSubsidiary',
                                                            'SalesOfRestaurantBusiness',
                                                        ]
                                                        b = [
                                                            'Acquisition',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        ProceedsFromDisposalsOfBusinessesAndIntangibles.append(ARCHvalue)
                                                r = r + 1
                                            cf.ProceedsFromDisposalsOfBusinessesAndIntangibles = sum(ProceedsFromDisposalsOfBusinessesAndIntangibles)
                                        except:
                                            pass
                                        #
                                        # Proceeds related to insurance settlement
                                        try:
                                            ProceedsRelatedToInsuranceSettlement = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > OperatingActivitiesRank:
                                                    if r < InvestingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'Insurance',
                                                        ]
                                                        b = [
                                                            'Acquisition',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        ProceedsRelatedToInsuranceSettlement.append(ARCHvalue)
                                                r = r + 1
                                            cf.ProceedsRelatedToInsuranceSettlement = sum(ProceedsRelatedToInsuranceSettlement)
                                        except:
                                            pass
                                        #
                                        # Reveipt Of Government Grands
                                        try:
                                            ReveiptOfGovernmentGrants = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > OperatingActivitiesRank:
                                                    if r < InvestingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'Grants',
                                                            'Subsidies',
                                                        ]
                                                        b = [
                                                            'Acquisition',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        ReveiptOfGovernmentGrants.append(ARCHvalue)
                                                r = r + 1
                                            cf.ReveiptOfGovernmentGrants = sum(ReveiptOfGovernmentGrants)
                                        except:
                                            pass
                                        #
                                        # Loan Repayment (Advances) From Equity Investee
                                        try:
                                            EquityInvesteeAdvancesRepayments = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > OperatingActivitiesRank:
                                                    if r < InvestingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'AdvancesToEquityInvestee',
                                                            'LoanAdvancesToEquityInvestee',
                                                            'LoanRepaymentFromEquityInvestee',
                                                        ]
                                                        b = [
                                                            'Proceeds',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        EquityInvesteeAdvancesRepayments.append(ARCHvalue)
                                                r = r + 1
                                            cf.EquityInvesteeAdvancesRepayments = sum(EquityInvesteeAdvancesRepayments)
                                        except:
                                            pass
                                        #
                                        # License Payment
                                        try:
                                            PaymentOfLicenseFee = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > OperatingActivitiesRank:
                                                    if r < InvestingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'PaymentOfLicenseFee',
                                                            'PaymentForLicenseFee',
                                                        ]
                                                        b = [
                                                            'Acquisition',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        PaymentOfLicenseFee.append(ARCHvalue)
                                                r = r + 1
                                            cf.PaymentOfLicenseFee = sum(PaymentOfLicenseFee)
                                        except:
                                            pass
                                        #
                                        # Investing Activities In Discontinued Operating
                                        try:
                                            InvestingActivitiesInDiscontinuedOperations = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > OperatingActivitiesRank:
                                                    if r < InvestingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'DiscontinuedOperation',
                                                        ]
                                                        b = [
                                                            'Acquisition',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        InvestingActivitiesInDiscontinuedOperations.append(ARCHvalue)
                                                r = r + 1
                                            cf.InvestingActivitiesInDiscontinuedOperations = sum(InvestingActivitiesInDiscontinuedOperations)
                                        except:
                                            pass
                                        #
                                        # Other Investing Activities
                                        try:
                                            OtherInvestingActivities = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > OperatingActivitiesRank:
                                                    if r < InvestingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'Other',
                                                            'NetTransferOfCash',
                                                            'RestrictedCash',
                                                        ]
                                                        b = [
                                                            'AccountsPayable',
                                                            'Financing',
                                                            'Proceeds',
                                                            'Repayments',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        OtherInvestingActivities.append(ARCHvalue)
                                                r = r + 1
                                            cf.OtherInvestingActivities = sum(OtherInvestingActivities)
                                            
                                            c = sum(OtherInvestingActivities)
                                            c = c - a.AnomalyInvestingActivitiesSEC
                                            cf.OtherInvestingActivities = c
                                        except:
                                            pass
                                        #
                                        # ML
                                        try:
                                            w = None
                                            a.InvestingActivitiesGL_i = ''
                                            m = None
                                            a.InvestingActivitiesGL_ii = ''
                                            t = None
                                            a.InvestingActivitiesGL_iii = ''
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > OperatingActivitiesRank:
                                                    if r < InvestingActivitiesRank:
                                                        d = key
                                                        b = [
                                                            'Total',
                                                        ]
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = 0
                                                                while CashFlowStatement[key][i] == None:
                                                                    i = i + 1
                                                                ARCHvalue = CashFlowStatement[key][i]
                                                                CashFlowStatement[key][i] = None
                                                            except:
                                                                if CashFlowStatement[key] != None:
                                                                    ARCHvalue = CashFlowStatement[key]
                                                                    CashFlowStatement[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                try:
                                                                    #
                                                                    if w is None:
                                                                        a.InvestingActivitiesGL_i = d
                                                                        w = ''
                                                                    #
                                                                    elif m is None:
                                                                        a.InvestingActivitiesGL_ii = d
                                                                        m = ''
                                                                    #
                                                                    elif t is None:
                                                                        a.InvestingActivitiesGL_iii = d
                                                                        t = ''
                                                                    else:
                                                                        pass
                                                                    #
                                                                    if d not in InvestingActivitiesGL:
                                                                        InvestingActivitiesGL.append(d)
                                                                    #
                                                                except:
                                                                    pass
                                                r = r + 1
                                        except:
                                            pass
                                        #
                                        # dataframe
                                        try:
                                            #
                                            df = pd.DataFrame({
                                                #
                                                '..': 
                                                    [
                                                    'cf.PaymentsToAcquireInvestments',
                                                    'cf.ProceedsOfInvestments',
                                                    'cf.PaymentsToAcquirePropertyPlantAndEquipment',
                                                    'cf.ProceedsFromDisposalsOfPropertyAndEquipment',
                                                    'cf.PaymentsToAcquireBusinessesAndIntangibles',
                                                    'cf.ProceedsFromDisposalsOfBusinessesAndIntangibles',
                                                    'cf.ProceedsRelatedToInsuranceSettlement',
                                                    'cf.ReveiptOfGovernmentGrants',
                                                    'cf.EquityInvesteeAdvancesRepayments',
                                                    'cf.OtherInvestingActivities',
                                                    'cf.InvestingActivitiesInDiscontinuedOperations',
                                                    ],
                                                #
                                                '.':
                                                    [
                                                    '{:,}'.format(cf.PaymentsToAcquireInvestments),
                                                    '{:,}'.format(cf.ProceedsOfInvestments),
                                                    '{:,}'.format(cf.PaymentsToAcquirePropertyPlantAndEquipment),
                                                    '{:,}'.format(cf.ProceedsFromDisposalsOfPropertyAndEquipment),
                                                    '{:,}'.format(cf.PaymentsToAcquireBusinessesAndIntangibles),
                                                    '{:,}'.format(cf.ProceedsFromDisposalsOfBusinessesAndIntangibles),
                                                    '{:,}'.format(cf.ProceedsRelatedToInsuranceSettlement),
                                                    '{:,}'.format(cf.ReveiptOfGovernmentGrants),
                                                    '{:,}'.format(cf.EquityInvesteeAdvancesRepayments),
                                                    '{:,}'.format(cf.OtherInvestingActivities),
                                                    '{:,}'.format(cf.InvestingActivitiesInDiscontinuedOperations),
                                                    ],
                                            })
                                            print(df)
                                            print('\n' + 137 * '-' + '\n')
                                            #
                                            cf.save()
                                            a.save()
                                            #
                                        except:
                                            pass
                                    except:
                                        pass
                                    #
                                    # financing activities components
                                    try:
                                        print(e.EntityRegistrantName)
                                        print('financing activities')
                                        print(periodenddate)
                                        print(137 * '-' + '\n')
                                        #
                                        # Finance Lease Principal Payments
                                        try:
                                            FinanceLeasePrincipalPayments = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > InvestingActivitiesRank:
                                                    if r < FinancingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'CapitalLease',
                                                            'FinanceLease',
                                                            'FinancingLease',
                                                            'FinancingObligation',
                                                            'PrincipalPaymentsOnCapitalLease',
                                                            'PrincipalPaymentsUnderCapital',
                                                            'CollateralizedLease',
                                                        ]
                                                        b = [
                                                            'Operating',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        FinanceLeasePrincipalPayments.append(ARCHvalue)
                                                                        print(d)
                                                                        print('{:,}'.format(value))
                                                r = r + 1
                                            cf.FinanceLeasePrincipalPayments = sum(FinanceLeasePrincipalPayments)
                                        except:
                                            pass        
                                        #
                                        # Payments For Repurchase Of Common Stock
                                        try:
                                            PaymentsForRepurchaseOfCommonShares = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > InvestingActivitiesRank:
                                                    if r < FinancingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'CommonSharesRepurchase',
                                                            'CommonSharesRepurchases',
                                                            'CommonStockRepurchase',
                                                            'CommonStockRepurchases',
                                                            'CompanyStockRepurchase',
                                                            'CompanyStockRepurchases',
                                                            'CompanySharesRepurchase',
                                                            'CompanySharesRepurchases',
                                                            'StockForTreasuryRepurchase',
                                                            'StockForTreasuryRepurchases',
                                                            #
                                                            'CommonSharesRepurchased',
                                                            'CommonStockRepurchased',
                                                            'CompanyStockRepurchased',
                                                            'CompanySharesRepurchased',
                                                            'StockForTreasuryRepurchased',
                                                            #     
                                                            'PurchasesOfClassACommonStock',
                                                            'PurchasesOfClassACommonShares',
                                                            'PurchasesOfClassBCommonStock',
                                                            'PurchasesOfClassBCommonShares',
                                                            'PurchaseOfCommonShares',
                                                            'PurchasesOfCommonShares',
                                                            'PurchaseOfCommonStock',
                                                            'PurchasesOfCommonStock',
                                                            'PurchaseOfCompanyStock',
                                                            'PurchasesOfCompanyStock',
                                                            'PurchaseOfCompanyShares',
                                                            'PurchasesOfCompanyShares',
                                                            'PurchaseOfStockForTreasury',
                                                            'PurchasesOfStockForTreasury',
                                                            'PurchaseOfTreasuryStock',
                                                            'PurchasesOfTreasuryStock',
                                                            'PurchaseOfTreasuryShare',
                                                            'PurchasesOfTreasuryShare',
                                                            #
                                                            'ReacquiredClassACommonStock',
                                                            'ReacquiredClassACommonShares',
                                                            'ReacquiredClassBCommonStock',
                                                            'ReacquiredClassBCommonShares',
                                                            'ReacquiredCommonShares',
                                                            'ReacquiredCommonStock',
                                                            'ReacquiredCompanyStock',
                                                            'ReacquiredCompanyShares',
                                                            'ReacquiredShares',
                                                            'ReacquiredStockForTreasury',
                                                            'ReacquiredTreasuryShare',
                                                            #
                                                            'RepurchasesOfClassACommonStock',
                                                            'RepurchasesOfClassACommonShares',
                                                            'RepurchasesOfClassBCommonStock',
                                                            'RepurchasesOfClassBCommonShares',
                                                            'RepurchaseOfCommonShares',
                                                            'RepurchasesOfCommonShares',
                                                            'RepurchaseOfCommonStock',
                                                            'RepurchasesOfCommonStock',
                                                            'RepurchaseOfCompanyStock',
                                                            'RepurchasesOfCompanyStock',
                                                            'RepurchaseOfCompanyShares',
                                                            'RepurchasesOfCompanyShares',
                                                            'RepurchaseOfStockForTreasury',
                                                            'RepurchasesOfStockForTreasury',
                                                            #
                                                            'RetirementOfClassBCommonStock',
                                                            'RetirementOfClassBCommonShares',
                                                            'RetirementOfCommonStock',
                                                            'RetirementOfCommonShare',
                                                            #
                                                            'StockRepurchase',
                                                            #
                                                            'TreasuryStockPurchases',
                                                            'TreasuryStockRepurchases',
                                                            'TreasuryStockRepurchased',
                                                        ]
                                                        b = [
                                                            'Proceeds',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        PaymentsForRepurchaseOfCommonShares.append(ARCHvalue)
                                                r = r + 1
                                            cf.PaymentsForRepurchaseOfCommonShares = sum(PaymentsForRepurchaseOfCommonShares)
                                        except:
                                            pass
                                        #
                                        # Proceeds From Issuance Of Common Stock
                                        try:
                                            ProceedsFromIssuanceOfCommonShares = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > InvestingActivitiesRank:
                                                    if r < FinancingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'IssuanceOfCommon',
                                                            'IssuancesOfCommon',
                                                            'IssuanceOfStock',
                                                            'IssuancesOfStock',
                                                            'NetProceedsFromEquityOffering',
                                                            'OfferingCost',
                                                            'ProceedsCommonStockOffering',
                                                            'ProceedsFromCommonStockOffering',
                                                            'ProceedsFromIssuance',
                                                            'PublicOffering',
                                                            'SalesOfCommonStock',
                                                            'SaleOfTreasuryStock',
                                                            'SettlementAgreement',
                                                            'RedemptionOfCommonStock',
                                                        ]
                                                        b = [
                                                            'Debt',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        ProceedsFromIssuanceOfCommonShares.append(ARCHvalue)
                                                r = r + 1
                                            cf.ProceedsFromIssuanceOfCommonShares = sum(ProceedsFromIssuanceOfCommonShares)
                                        except:
                                            pass
                                        #
                                        # Tax Related To Share Based Compensation
                                        try:
                                            PaymentsRelatedToTaxWithholdingForShareBasedCompensation = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > InvestingActivitiesRank:
                                                    if r < FinancingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'ShareRepurchasedToSatisfyTax',
                                                            'ShareRepurchasesToSatisfyTax',
                                                            'ShareBasedTaxWithholdings',
                                                            'StockBasedTaxWithholdings',
                                                            'BenefitForShare',
                                                            'BenefitForStock',
                                                            'BenefitFromShare',
                                                            'BenefitFromStock',
                                                            'BenefitsForShare',
                                                            'BenefitsForStock',
                                                            'BenefitsFromEquity',
                                                            'BenefitFromExercise',
                                                            'BenefitsFromEquity',
                                                            'BenefitsFromShare',
                                                            'BenefitsFromStock',
                                                            'BenefitsFromStock',
                                                            'BenefitsOnStock',
                                                            'TaxesRelatedToNetShareSettlement',
                                                            'TaxesRemittedOnShare',
                                                            'TaxesOnStockBasedCompensation',
                                                            'PaidRelatedToNetShareSettlement',
                                                            'WithheldAndRemittedOnShare',
                                                            'WithheldAndRemittedOnStock',
                                                            'WithholdingsOnEquity',
                                                            'WithholdingOnEquity',
                                                            'WithholdingOnStockBased',
                                                            'WithholdingsOnStockBased',
                                                            'WithholdingsForEquity',
                                                            'WithholdingForEquity',
                                                            'WithholdingForShareBased',
                                                            'WithholdingForNetShareSettledEquityAwards',
                                                            'WithholdingsOnShareBased',
                                                            'PaidForRestrictedUnitWithholdings',
                                                            'PaidUponTheVestingOfEquity',
                                                            'PaidUponTheVestingOfRestrictedStockUnits',
                                                            'TaxesRelatedToNetShare',
                                                            'TaxRelatedToNetShare',
                                                            'TaxesRelatedToNetStock',
                                                            'TaxRelatedToNetStock',
                                                        ]
                                                        b = [
                                                            'Proceeds',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        PaymentsRelatedToTaxWithholdingForShareBasedCompensation.append(ARCHvalue)
                                                r = r + 1
                                            cf.PaymentsRelatedToTaxWithholdingForShareBasedCompensation = sum(PaymentsRelatedToTaxWithholdingForShareBasedCompensation)
                                        except:
                                            pass
                                        #
                                        # Proceeds from stock option exercices
                                        try:
                                            ProceedsFromSharePurchasePlanAndOptionsExercice = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > InvestingActivitiesRank:
                                                    if r < FinancingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'ExerciseOfEquityAward',
                                                            'ShareBasedAward',
                                                            'StockBasedAward',
                                                            'ShareBasedCompensation',
                                                            'StockBasedCompensation',
                                                            'StockOption',
                                                            'StockPurchasePlan',
                                                            'SharePurchasePlan',
                                                            'ProceedsFromEmployeeStockPurchasePlan',
                                                        ]
                                                        b = [
                                                            'TaxBenefit',
                                                            'TaxWithh',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        ProceedsFromSharePurchasePlanAndOptionsExercice.append(ARCHvalue)
                                                r = r + 1
                                            cf.ProceedsFromSharePurchasePlanAndOptionsExercice = sum(ProceedsFromSharePurchasePlanAndOptionsExercice)
                                        except:
                                            pass
                                        #
                                        # Payments Of Dividends
                                        try:
                                            PaymentsOfDividends = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > InvestingActivitiesRank:
                                                    if r < FinancingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'Dividend',
                                                        ]
                                                        b = [
                                                            'Proceeds',
                                                            'NonControllingInterest',
                                                            'NoncontrollingInterest',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        ARCHvalue = -abs(ARCHvalue)
                                                                        PaymentsOfDividends.append(ARCHvalue)
                                                r = r + 1
                                            cf.PaymentsOfDividends = sum(PaymentsOfDividends)
                                        except:
                                            pass
                                        #
                                        # Payment Of Deferred Contingent Consideration
                                        try:
                                            IncreaseDecreaseDeferredContingentConsideration = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > InvestingActivitiesRank:
                                                    if r < FinancingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'ContingentAcquisition',
                                                            'ContingentConsideration',
                                                            'HoldbackPaymentRelatedToAcquisition',
                                                            'HoldbackPaymentRelatedToPriorAcquisition',
                                                        ]
                                                        b = [
                                                            'Proceeds',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        IncreaseDecreaseDeferredContingentConsideration.append(ARCHvalue)
                                                r = r + 1
                                            cf.IncreaseDecreaseDeferredContingentConsideration = sum(IncreaseDecreaseDeferredContingentConsideration)
                                        except:
                                            pass
                                        #
                                        # Proceeds From Issuance Of Long Term Debt
                                        try:
                                            ProceedsFromIssuanceOfLongTermDebt = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > InvestingActivitiesRank:
                                                    if r < FinancingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'CreditAgreement',
                                                            'Debt',
                                                            'Loan',
                                                            'Note',
                                                        ]
                                                        b = [
                                                            'Convertible',
                                                            'DebtIssuanceCost',
                                                            'Payment',
                                                            'Purchase',
                                                            'Repayment',
                                                            'Repurchase',
                                                            'Revolv',
                                                            'ShortTerm',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        ProceedsFromIssuanceOfLongTermDebt.append(ARCHvalue)
                                                r = r + 1
                                            cf.ProceedsFromIssuanceOfLongTermDebt = sum(ProceedsFromIssuanceOfLongTermDebt)
                                        except:
                                            pass
                                        #
                                        # Repayments Of Long Term Debt
                                        try:
                                            RepaymentsOfLongTermDebt = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > InvestingActivitiesRank:
                                                    if r < FinancingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'CreditAgreement',
                                                            'Debt',
                                                            'FinancingRepayments',
                                                            'Loan',
                                                            'Note',
                                                        ]
                                                        b = [
                                                            'Issuance',
                                                            'Lease',
                                                            'Proceeds',
                                                            'Revolv',
                                                            'ShortTerm',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        if 'Repayment' in d:
                                                                            ARCHvalue = -abs(ARCHvalue)
                                                                        RepaymentsOfLongTermDebt.append(ARCHvalue)
                                                r = r + 1
                                            cf.RepaymentsOfLongTermDebt = sum(RepaymentsOfLongTermDebt)
                                        except:
                                            pass
                                        #
                                        # Financing Costs And Securization
                                        try:
                                            FinancingCosts = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > InvestingActivitiesRank:
                                                    if r < FinancingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'CostIncurred',
                                                            'CostsIncurred',
                                                            'DebtIssuanceCost',
                                                            'DeferredFinancingCosts',
                                                            'FinancingIssuance',
                                                            'FinanceFees',
                                                            'FinancingCost',
                                                            'ReceivablesSecuritization',
                                                            'RecoveryOfShortSwingProfit',
                                                        ]
                                                        b = [
                                                            'Lease',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        if 'Repayment' in d:
                                                                            ARCHvalue = -abs(ARCHvalue)
                                                                        FinancingCosts.append(ARCHvalue)
                                                                        print(d)
                                                                        print('{:,}'.format(value))
                                                r = r + 1
                                            cf.FinancingCosts = sum(FinancingCosts)
                                        except:
                                            pass
                                        #
                                        # Proceeds From Repayments Of Commercial Paper
                                        try:
                                            ProceedsFromRepaymentsOfCommercialPaper = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > InvestingActivitiesRank:
                                                    if r < FinancingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'CommercialPaper',
                                                        ]
                                                        b = [
                                                            'Acquisition',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        ProceedsFromRepaymentsOfCommercialPaper.append(ARCHvalue)
                                                r = r + 1
                                            cf.ProceedsFromRepaymentsOfCommercialPaper = sum(ProceedsFromRepaymentsOfCommercialPaper)
                                        except:
                                            pass
                                        #
                                        # Repayments Of Convertible
                                        try:
                                            RepaymentsOfConvertible = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > InvestingActivitiesRank:
                                                    if r < FinancingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'Convertible',
                                                            'DiscontinuedConvertible',
                                                        ]
                                                        b = [
                                                            'Issuance',
                                                            'Proceeds',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        RepaymentsOfConvertible.append(ARCHvalue)
                                                r = r + 1
                                            cf.RepaymentsOfConvertible = sum(RepaymentsOfConvertible)
                                        except:
                                            pass
                                        #
                                        # Issuance Of Convertible
                                        try:
                                            IssuanceOfConvertible = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > InvestingActivitiesRank:
                                                    if r < FinancingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'Convertible',
                                                        ]
                                                        b = [
                                                            'Repayment',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        IssuanceOfConvertible.append(ARCHvalue)
                                                r = r + 1
                                            cf.IssuanceOfConvertible = sum(IssuanceOfConvertible)
                                        except:
                                            pass
                                        #
                                        # Net Change In Short Term Borrowings
                                        try:
                                            NetChangeInShortTermBorrowings = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > InvestingActivitiesRank:
                                                    if r < FinancingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'CreditFacility',
                                                            'LineOfCredit',
                                                            'LinesOfCredit',
                                                            'ShortTermBorrowing',
                                                            'ShortTermDebt',
                                                            'Revolv',
                                                        ]
                                                        b = [
                                                            'CommercialPaper',
                                                        ]
                                                        g = [
                                                            '(Payment)',
                                                            '(Repayment)',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        for t in g:
                                                                            if t in d:
                                                                                if ARCHvalue < 1:
                                                                                    ARCHvalue = -abs(ARCHvalue)
                                                                        NetChangeInShortTermBorrowings.append(ARCHvalue)
                                                r = r + 1
                                            cf.NetChangeInShortTermBorrowings = sum(NetChangeInShortTermBorrowings)
                                        except:
                                            pass
                                        #
                                        # Net Change In Forward And Hedges Classified As Financing Activities
                                        try:
                                            NetChangeInForwardAndHedgesClassifiedAsFinancingActivities = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > InvestingActivitiesRank:
                                                    if r < FinancingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'Forward',
                                                            'Hedg',
                                                        ]
                                                        b = [
                                                            'Invest',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        NetChangeInForwardAndHedgesClassifiedAsFinancingActivities.append(ARCHvalue)
                                                r = r + 1
                                            cf.NetChangeInForwardAndHedgesClassifiedAsFinancingActivities = sum(NetChangeInForwardAndHedgesClassifiedAsFinancingActivities)
                                        except:
                                            pass
                                        #
                                        # Net Change In Non Controlling Interests
                                        try:
                                            NetChangeInNonControllingInterests = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > InvestingActivitiesRank:
                                                    if r < FinancingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'NonControllingInterest',
                                                            'NoncontrollingInterest',
                                                        ]
                                                        b = [
                                                            'CommercialPaper',
                                                        ]
                                                        g = [
                                                            '(Payment)',
                                                            '(Repayment)',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        for t in g:
                                                                            if t in d:
                                                                                if ARCHvalue < 1:
                                                                                    ARCHvalue = -abs(ARCHvalue)
                                                                        NetChangeInNonControllingInterests.append(ARCHvalue)
                                                r = r + 1
                                            cf.NetChangeInNonControllingInterests = sum(NetChangeInNonControllingInterests)
                                        except:
                                            pass
                                        #
                                        # Other Financing Activities
                                        try:
                                            OtherFinancingActivities = []
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > InvestingActivitiesRank:
                                                    if r < FinancingActivitiesRank:
                                                        d = key
                                                        q = [
                                                            'Miscellaneous',
                                                            'Other',
                                                        ]
                                                        b = [
                                                            'AccountsPayable',
                                                        ]
                                                        for l in q:
                                                            if l in d:
                                                                h = 'p'
                                                                for p in b:
                                                                    u = 0
                                                                    while u < len(b):
                                                                        if p in d:
                                                                            h = ''
                                                                        u = u + 1
                                                                if h == 'p':
                                                                    try:
                                                                        i = 0
                                                                        while CashFlowStatement[key][i] == None:
                                                                            i = i + 1
                                                                        ARCHvalue = CashFlowStatement[key][i]
                                                                        CashFlowStatement[key][i] = None
                                                                    except:
                                                                        if CashFlowStatement[key] != None:
                                                                            ARCHvalue = CashFlowStatement[key]
                                                                            CashFlowStatement[key] = None
                                                                        else:
                                                                            ARCHvalue = 0
                                                                    if ARCHvalue != 0:
                                                                        OtherFinancingActivities.append(ARCHvalue)
                                                r = r + 1
                                            c = sum(OtherFinancingActivities)
                                            c = c - a.AnomalyFinancingActivitiesSEC
                                            cf.OtherFinancingActivities = c
                                        except:
                                            pass
                                        #
                                        # ML
                                        try:
                                            w = None
                                            a.FinancingActivitiesGL_i = ''
                                            m = None
                                            a.FinancingActivitiesGL_ii = ''
                                            t = None
                                            a.FinancingActivitiesGL_iii = ''
                                            r = 0
                                            for key, value in CashFlowStatement.items():
                                                if r > InvestingActivitiesRank:
                                                    if r < FinancingActivitiesRank:
                                                        d = key
                                                        b = [
                                                            'Total',
                                                        ]
                                                        h = 'p'
                                                        for p in b:
                                                            u = 0
                                                            while u < len(b):
                                                                if p in d:
                                                                    h = ''
                                                                u = u + 1
                                                        if h == 'p':
                                                            try:
                                                                i = 0
                                                                while CashFlowStatement[key][i] == None:
                                                                    i = i + 1
                                                                ARCHvalue = CashFlowStatement[key][i]
                                                                CashFlowStatement[key][i] = None
                                                            except:
                                                                if CashFlowStatement[key] != None:
                                                                    ARCHvalue = CashFlowStatement[key]
                                                                    CashFlowStatement[key] = None
                                                                else:
                                                                    ARCHvalue = 0
                                                            if ARCHvalue != 0:
                                                                try:
                                                                    #
                                                                    if w is None:
                                                                        a.FinancingActivitiesGL_i = d
                                                                        w = ''
                                                                    #
                                                                    elif m is None:
                                                                        a.FinancingActivitiesGL_ii = d
                                                                        m = ''
                                                                    #
                                                                    elif t is None:
                                                                        a.FinancingActivitiesGL_iii = d
                                                                        t = ''
                                                                    else:
                                                                        pass
                                                                    #
                                                                    if d not in FinancingActivitiesGL:
                                                                        FinancingActivitiesGL.append(d)
                                                                    #
                                                                except:
                                                                    pass
                                                r = r + 1
                                        except:
                                            pass
                                        #
                                        # dataframe
                                        try:
                                            #
                                            df = pd.DataFrame({
                                                #
                                                '..': 
                                                    [
                                                    'cf.FinanceLeasePrincipalPayments',
                                                    'cf.PaymentsForRepurchaseOfCommonShares',
                                                    'cf.ProceedsFromIssuanceOfCommonShares',
                                                    'cf.PaymentsRelatedToTaxWithholdingForShareBasedCompensation',
                                                    'cf.PaymentsOfDividends',
                                                    'cf.IncreaseDecreaseDeferredContingentConsideration',
                                                    'cf.ProceedsFromIssuanceOfLongTermDebt',
                                                    'cf.RepaymentsOfLongTermDebt',
                                                    'cf.FinancingCosts',
                                                    'cf.ProceedsFromRepaymentsOfCommercialPaper',
                                                    'cf.RepaymentsOfConvertible',
                                                    'cf.IssuanceOfConvertible',
                                                    'cf.NetChangeInShortTermBorrowings',
                                                    'cf.NetChangeInForwardAndHedgesClassifiedAsFinancingActivities',
                                                    'cf.NetChangeInNonControllingInterests',
                                                    'cf.ProceedsFromSharePurchasePlanAndOptionsExercice',
                                                    'cf.OtherFinancingActivities',
                                                    ],
                                                #
                                                '.':
                                                    [
                                                    '{:,}'.format(cf.FinanceLeasePrincipalPayments),
                                                    '{:,}'.format(cf.PaymentsForRepurchaseOfCommonShares),
                                                    '{:,}'.format(cf.ProceedsFromIssuanceOfCommonShares),
                                                    '{:,}'.format(cf.PaymentsRelatedToTaxWithholdingForShareBasedCompensation),
                                                    '{:,}'.format(cf.PaymentsOfDividends),
                                                    '{:,}'.format(cf.IncreaseDecreaseDeferredContingentConsideration),
                                                    '{:,}'.format(cf.ProceedsFromIssuanceOfLongTermDebt),
                                                    '{:,}'.format(cf.RepaymentsOfLongTermDebt),
                                                    '{:,}'.format(cf.FinancingCosts),
                                                    '{:,}'.format(cf.ProceedsFromRepaymentsOfCommercialPaper),
                                                    '{:,}'.format(cf.RepaymentsOfConvertible),
                                                    '{:,}'.format(cf.IssuanceOfConvertible),
                                                    '{:,}'.format(cf.NetChangeInShortTermBorrowings),
                                                    '{:,}'.format(cf.NetChangeInForwardAndHedgesClassifiedAsFinancingActivities),
                                                    '{:,}'.format(cf.NetChangeInNonControllingInterests),
                                                    '{:,}'.format(cf.ProceedsFromSharePurchasePlanAndOptionsExercice),
                                                    '{:,}'.format(cf.OtherFinancingActivities),
                                                    ],
                                            })
                                            print(df)
                                            print('\n' + 137 * '-' + '\n')
                                            #
                                            cf.save()
                                            a.save()
                                        except:
                                            pass
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # save
                                a.save()
                                cf.save()
                                tb.save()
                            except:
                                pass
            except:
                pass
            #
            # beginning balances
            try:
                #
                periodenddates.sort(reverse=True)
                #
                for periodenddate in periodenddates:
                    #
                    if periodenddate != None:
                        #
                        a = AuditData.objects.get(TradingSymbol=e.TradingSymbol, PeriodEndDate=periodenddate)
                        #
                        if a.db not in auditcompleted:
                            #
                            print(137 * '-' + '\n')
                            print(e.EntityRegistrantName)
                            print('beginning balances')
                            print(periodenddate)
                            print(137 * '-' + '\n')
                            #
                            # math
                            try:
                                #
                                # Model Current Year Beginning Balance
                                tb = TrialBalance.objects.get(TradingSymbol=e.TradingSymbol, PeriodEndDate=periodenddate)
                                a = AuditData.objects.get(TradingSymbol=e.TradingSymbol, PeriodEndDate=periodenddate)
                                #
                                chronology = {
                                    e.lastyear: e.secondlastyear,
                                    e.secondlastyear: e.thirdlastyear,
                                    e.thirdlastyear: e.fourthlastyear,
                                    e.fourthlastyear: e.fifthlastyear,
                                    e.fifthlastyear: e.sixthlastyear,
                                    e.sixthlastyear: e.seventhlastyear,
                                }
                                #
                                prioryear = chronology[periodenddate]
                                #
                                # Model Prior Year Beginning Balance
                                try:
                                    backwards = 'yes'
                                    prioryeartb = TrialBalance.objects.get(TradingSymbol=e.TradingSymbol, PeriodEndDate=prioryear)
                                    prioryeara = AuditData.objects.get(TradingSymbol=e.TradingSymbol, PeriodEndDate=prioryear)
                                    if prioryeara.RetainedEarnings != 0:
                                        backwards = ''
                                except:
                                    pass
                                #
                                # Convertible Debt - Beginning Balance
                                if backwards == '':
                                    tb.ConvertibleDebtBeginning = prioryeara.ConvertibleDebt
                                else:
                                    c = a.ConvertibleDebt
                                    tb.ConvertibleDebtBeginning = c
                                #
                                # Common Shares - Beginning Balance
                                if backwards == '':
                                    tb.CommonSharesBeginning = prioryeara.CommonShares
                                else:
                                    c = a.CommonShares
                                    c = c - tb.CommonSharesIssued
                                    c = c - tb.ShareBasedCompensation
                                    tb.CommonSharesBeginning = c
                                #
                                # Retained Earnings - Beginning Balance
                                if backwards == '':
                                    tb.RetainedEarningsBeginning = prioryeara.RetainedEarnings
                                else:
                                    c = a.RetainedEarnings
                                    c = c - tb.DividendsAndDividendEquivalentsDeclared
                                    c = c - tb.CommonSharesRepurchasedAndRetired
                                    c = c - tb.ShareBasedCompensationRetainedEarnings
                                    c = c - tb.EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts
                                    c = c - a.NetIncome
                                    tb.RetainedEarningsBeginning = c
                                #
                                # Accumulated Other Comprehensive Income - Beginning Balance
                                if backwards == '':
                                    tb.AccumulatedOtherComprehensiveIncomeBeginning = prioryeara.AccumulatedOtherComprehensiveIncome
                                else:
                                    c = a.AccumulatedOtherComprehensiveIncome
                                    c = c - tb.ChangeInForeignCurrencyTranslationAdjustment
                                    c = c - tb.ChangeInUnrealizedGainsLossesOnDerivativeInstruments
                                    c = c - tb.ChangeInUnrealizedGainsLossesOnInvestments
                                    tb.AccumulatedOtherComprehensiveIncomeBeginning = c
                                #
                                # Treasury Stocks - Beginning Balance
                                if backwards == '':
                                    tb.TreasurySharesBeginning = prioryeara.TreasuryShares
                                else:
                                    c = a.TreasuryShares
                                    tb.TreasurySharesBeginning = c
                                #
                                # Employee Benefit Trust - Beginning Balance
                                if backwards == '':
                                    tb.EmployeeBenefitTrustBeginning = prioryeara.EmployeeBenefitTrust
                                else:
                                    c = a.EmployeeBenefitTrust
                                    tb.EmployeeBenefitTrustBeginning = c
                                #
                                # Non Controling Interest - Beginning Balance
                                if backwards == '':
                                    c = prioryeara.NonControllingInterests
                                    c = c - tb.DividendsDeclaredToNonControllingInterests
                                    c = c - tb.AcquisitionOfNonControllingInterests
                                    c = c - tb.NonControllingInterestsOthers
                                    tb.NonControllingInterestsBeginning = c
                                else:
                                    tb.NonControllingInterestsBeginning = a.NonControllingInterests
                            except:
                                pass
                            #
                            # dataframe
                            try:
                                #
                                df = pd.DataFrame({
                                    #
                                    periodenddate:
                                        [
                                        'tb.CommonSharesBeginning',
                                        'tb.RetainedEarningsBeginning',
                                        'tb.AccumulatedOtherComprehensiveIncomeBeginning',
                                        'tb.TreasurySharesBeginning',
                                        'tb.EmployeeBenefitTrustBeginning',
                                        'tb.NonControllingInterestsBeginning',
                                        ],
                                    #
                                    '.':
                                        [
                                        '{:,}'.format(tb.CommonSharesBeginning),
                                        '{:,}'.format(tb.RetainedEarningsBeginning),
                                        '{:,}'.format(tb.AccumulatedOtherComprehensiveIncomeBeginning),
                                        '{:,}'.format(tb.TreasurySharesBeginning),
                                        '{:,}'.format(tb.EmployeeBenefitTrustBeginning),
                                        '{:,}'.format(tb.NonControllingInterestsBeginning),
                                        ],
                                })
                                print(df)
                                print('\n' + 137 * '-' + '\n')
                                #
                                tb.save()
                                a.save()
                            except:
                                pass
            except:
                pass
            #
            # regularizations
            try:
                #
                periodenddates.sort(reverse=True)
                #
                for periodenddate in periodenddates:
                    #
                    if periodenddate != None:
                        #
                        a = AuditData.objects.get(TradingSymbol=e.TradingSymbol, PeriodEndDate=periodenddate)
                        #
                        if a.db not in auditcompleted:
                            # 
                            tb = TrialBalance.objects.get(TradingSymbol=e.TradingSymbol, PeriodEndDate=periodenddate)
                            #
                            print(e.EntityRegistrantName)
                            print('Regularizations')
                            print(tb.PeriodEndDate)
                            print(137 * '-' + '\n')
                            #
                            # bs, is, ci & se
                            try:
                                #
                                # current assets
                                try:
                                    #
                                    Anomaly = 0
                                    #
                                    Components = [
                                        tb.Cash,
                                        tb.ShortTermInvestments,
                                        tb.AccountsReceivable,
                                        tb.WorkInProgress,
                                        tb.Inventories,
                                        tb.PrepaidExpenses,
                                        tb.NonTradeReceivables,
                                        tb.PrepaidTaxAssetsCurrent,
                                        tb.DeferredTaxAssetsCurrent,
                                        tb.RightOfUseAssetsCurrent,
                                        tb.OtherCurrentAssets,
                                        tb.DiscontinuedOperationsCurrent,
                                    ]
                                    Total = a.CurrentAssets
                                    #
                                    Components = sum(Components)
                                    #
                                    Anomaly = Components - Total
                                    #
                                    tb.OtherCurrentAssets = tb.OtherCurrentAssets - Anomaly
                                    #
                                    a.AnomalyCurrentAssets = (Anomaly - a.AnomalyCurrentAssetsSEC)
                                    #
                                    # dataframe                        
                                    try:
                                        df = pd.DataFrame({
                                            #
                                            'anomaly current assets': 
                                                #
                                                [
                                                'Components',
                                                'Total',
                                                'Anomaly',
                                                'a.AnomalyCurrentAssetsSEC',
                                                'tb.OtherCurrentAssets',
                                                ],
                                            #
                                            '.':
                                                #
                                                [
                                                '{:,}'.format(Components),
                                                '{:,}'.format(Total),
                                                '{:,}'.format(Anomaly),
                                                '{:,}'.format(a.AnomalyCurrentAssetsSEC),
                                                '{:,}'.format(tb.OtherCurrentAssets),
                                                ],
                                        })
                                        print(df)
                                        print(137 * '-' + '\n')
                                        #
                                        tb.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # non-current assets
                                try:
                                    #
                                    Anomaly = 0
                                    #
                                    Components = [
                                        tb.LongTermReceivables,
                                        tb.DeferredCharges,
                                        tb.Investments,
                                        tb.PropertyPlantAndEquipment,
                                        tb.OperatingLeaseRightOfUseAssets,
                                        tb.FinanceLeaseRightOfUseAssets,
                                        tb.IntangibleAssets,
                                        tb.Goodwill,
                                        tb.RefundableTaxAssetsNonCurrent,
                                        tb.DeferredTaxAssetsNonCurrent,
                                        tb.DefinedBenefitPensionAndOtherSimilarPlans,
                                        tb.OtherNonCurrentAssets,
                                        tb.DiscontinuedOperations,
                                    ]
                                    Total = a.NonCurrentAssets
                                    #
                                    Components = sum(Components)
                                    Anomaly = Components - Total
                                    #
                                    tb.OtherNonCurrentAssets = tb.OtherNonCurrentAssets - Anomaly
                                    #
                                    a.AnomalyNonCurrentAssets = (Anomaly - a.AnomalyNonCurrentAssetsSEC)
                                    #
                                    #
                                    # dataframe
                                    try:
                                        df = pd.DataFrame({
                                            #
                                            'anomaly non current assets': 
                                                #
                                                [
                                                'Components',
                                                'Total',
                                                'Anomaly',
                                                'a.AnomalyNonCurrentAssetsSEC',
                                                'tb.OtherNonCurrentAssets',
                                                ],
                                            #
                                            '.':
                                                #
                                                [
                                                '{:,}'.format(Components),
                                                '{:,}'.format(Total),
                                                '{:,}'.format(Anomaly),
                                                '{:,}'.format(a.AnomalyNonCurrentAssetsSEC),
                                                '{:,}'.format(tb.OtherNonCurrentAssets),
                                                ],
                                        })
                                        print(df)
                                        print(137 * '-' + '\n')
                                        #
                                        tb.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # current liabilities
                                try:
                                    #
                                    Anomaly = 0
                                    #
                                    Components = [
                                        tb.AccountsPayableAndAccruedLiabilities,
                                        tb.EmployeeCompensationCurrent,
                                        tb.OperatingLeasesCurrent,
                                        tb.FinanceLeasesCurrent,
                                        tb.DeferredRevenueAndDepositsCurrent,
                                        tb.AccruedTaxLiabilities,
                                        tb.DeferredTaxLiabilitiesCurrent,
                                        tb.CommercialPapers,
                                        tb.OtherCurrentLiabilities,
                                        tb.DiscontinuedOperationsLiabilitiesCurrent,
                                        tb.DividendsPayable,
                                        tb.ShortTermBorrowings,
                                        tb.ShortTermPortionOfLongTermDebt,
                                    ]
                                    Total = a.CurrentLiabilities
                                    #
                                    Components = sum(Components)
                                    #
                                    Anomaly = Components - Total
                                    #
                                    tb.OtherCurrentLiabilities = tb.OtherCurrentLiabilities - Anomaly
                                    #
                                    a.AnomalyCurrentLiabilities = (a.AnomalyCurrentLiabilitiesSEC - Anomaly)
                                    #
                                    # dataframe
                                    try:
                                        df = pd.DataFrame({
                                            #
                                            'anomaly current liabilities': 
                                                #
                                                [
                                                'Components',
                                                'Total',
                                                'Anomaly',
                                                'a.AnomalyCurrentLiabilitiesSEC',
                                                'tb.OtherCurrentLiabilities',
                                                ],
                                            #
                                            '.':
                                                #
                                                [
                                                '{:,}'.format(Components),
                                                '{:,}'.format(Total),
                                                '{:,}'.format(Anomaly),
                                                '{:,}'.format(a.AnomalyCurrentLiabilitiesSEC),
                                                '{:,}'.format(tb.OtherCurrentLiabilities),
                                                ],
                                        })
                                        print(df)
                                        print(137 * '-' + '\n')
                                        #
                                        tb.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # non-current liabilities
                                try:
                                    #
                                    Anomaly = 0
                                    #
                                    Components = [
                                        tb.LongTermDebt,
                                        tb.PreferredSharesLiability,
                                        tb.RetirementBenefits,
                                        tb.OperatingLeasesNonCurrent,
                                        tb.LeaseIncentiveObligation,
                                        tb.FinanceLeasesNonCurrent,
                                        tb.DeferredRevenueAndDepositsNonCurrent,
                                        tb.ContingentConsideration,
                                        tb.AccruedTaxLiabilitiesNonCurrent,
                                        tb.DeferredTaxLiabilitiesNonCurrent,
                                        tb.OtherNonCurrentLiabilities,
                                        tb.RedeemableNonControllingInterests,
                                        tb.DiscontinuedOperationsLiabilitiesNonCurrent,
                                    ]
                                    if a.NonCurrentLiabilities == 0:
                                        if a.Liabilities == 0:
                                            a.Liabilities = a.LiabilitiesAndShareholdersEquity - a.ShareholdersEquity
                                        a.NonCurrentLiabilities = a.Liabilities - a.CurrentLiabilities
                                    #
                                    Total = a.NonCurrentLiabilities
                                    #
                                    Components = sum(Components)
                                    #
                                    Anomaly = Components - Total
                                    #
                                    tb.OtherNonCurrentLiabilities = tb.OtherNonCurrentLiabilities - Anomaly  
                                    #
                                    a.AnomalyNonCurrentLiabilities = (a.AnomalyNonCurrentLiabilitiesSEC - Anomaly) 
                                    #
                                    # dataframe
                                    try:
                                        df = pd.DataFrame({
                                            #
                                            'anomaly non current liabilities': 
                                                #
                                                [
                                                'Components',
                                                'Total',
                                                'Anomaly',
                                                'a.AnomalyNonCurrentLiabilitiesSEC',
                                                'tb.OtherNonCurrentLiabilities',
                                                ],
                                            #
                                            '.':
                                                #
                                                [
                                                '{:,}'.format(Components),
                                                '{:,}'.format(Total),
                                                '{:,}'.format(Anomaly),
                                                '{:,}'.format(a.AnomalyNonCurrentLiabilitiesSEC),
                                                '{:,}'.format(tb.OtherNonCurrentLiabilities),
                                                ],
                                        })
                                        print(df)
                                        print(137 * '-' + '\n')
                                        #
                                        tb.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # gross margin
                                try:
                                    #
                                    Anomaly = 0
                                    #
                                    Components = [
                                        tb.Sales,
                                        tb.CostOfSales,
                                    ]
                                    if a.GrossMargin == 0:
                                        a.GrossMargin = sum(Components)
                                    #
                                    Total = a.GrossMargin
                                    #
                                    Components = sum(Components)
                                    #
                                    Anomaly = Components - Total
                                    #
                                    if tb.Sales == 0:
                                        tb.Sales = -Anomaly
                                    #
                                    elif tb.CostOfSales == 0:
                                        tb.CostOfSales = -Anomaly
                                    #
                                    else:
                                        if Anomaly > 0:
                                            tb.Sales = tb.Sales - Anomaly
                                        else:
                                            tb.CostOfSales = tb.CostOfSales - Anomaly
                                    #
                                    a.AnomalyGrossMargin = Anomaly
                                    #
                                    # dataframe
                                    try:
                                        df = pd.DataFrame({
                                            #
                                            'anomaly gross margin': 
                                                #
                                                [
                                                'Components',
                                                'Total',
                                                'Anomaly',
                                                'a.AnomalyGrossMargin',
                                                ],
                                            #
                                            '.':
                                                #
                                                [
                                                '{:,}'.format(Components),
                                                '{:,}'.format(Total),
                                                '{:,}'.format(Anomaly),
                                                '{:,}'.format(a.AnomalyGrossMargin),
                                                ],
                                        })
                                        print(df)
                                        print(137 * '-' + '\n')
                                        #
                                        tb.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # operating expenses
                                try:
                                    #
                                    Anomaly = 0
                                    #
                                    Components = [
                                        tb.ResearchAndDevelopment,
                                        tb.SellingGeneralAdministrativeAndMarketing,
                                    ]
                                    #
                                    if a.OperatingIncome == 0:
                                        a.OperatingIncome = a.GrossMargin + sum(Components)
                                    #
                                    a.OperatingExpenses = a.OperatingIncome - a.GrossMargin
                                    #
                                    Total = a.OperatingExpenses
                                    #
                                    Components = sum(Components)
                                    #
                                    Anomaly = Components - Total
                                    #
                                    tb.SellingGeneralAdministrativeAndMarketing = tb.SellingGeneralAdministrativeAndMarketing - Anomaly
                                    #
                                    a.AnomalyOperatingExpenses = Anomaly
                                    #
                                    # dataframe
                                    try:
                                        df = pd.DataFrame({
                                            #
                                            'anomaly selling, administrative and marketing': 
                                                #
                                                [
                                                'Components',
                                                'Total',
                                                'Anomaly',
                                                'a.AnomalyOperatingExpenses',
                                                'tb.SellingGeneralAdministrativeAndMarketing',
                                                ],
                                            #
                                            '.':
                                                #
                                                [
                                                '{:,}'.format(Components),
                                                '{:,}'.format(Total),
                                                '{:,}'.format(Anomaly),
                                                '{:,}'.format(a.AnomalyOperatingExpenses),
                                                '{:,}'.format(tb.SellingGeneralAdministrativeAndMarketing),
                                                ],
                                        })
                                        print(df)
                                        print(137 * '-' + '\n')
                                        #
                                        tb.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # operating income
                                try:
                                    Anomaly = 0
                                    Components = [
                                        a.GrossMargin,
                                        a.OperatingExpenses,
                                    ]
                                    Total = a.OperatingIncome
                                    #
                                    Components = sum(Components)
                                    #
                                    Anomaly = Components - Total
                                    #
                                    a.AnomalyOperatingIncome = Anomaly
                                    #
                                    # dataframe
                                    try:
                                        df = pd.DataFrame({
                                            #
                                            'operating income': 
                                                #
                                                [
                                                'Components',
                                                'Total',
                                                'Anomaly',
                                                'a.AnomalyOperatingIncome',
                                                ],
                                            #
                                            '.':
                                                #
                                                [
                                                '{:,}'.format(Components),
                                                '{:,}'.format(Total),
                                                '{:,}'.format(Anomaly),
                                                '{:,}'.format(a.AnomalyOperatingIncome),
                                                ],
                                        })
                                        print(df)
                                        print(137 * '-' + '\n')
                                        #
                                        tb.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # income before taxes
                                try:
                                    #
                                    Anomaly = 0
                                    #
                                    Components = [
                                        a.OperatingIncome,
                                        tb.ImpairmentRestructuringAndOtherSpecialCharges,
                                        tb.NonOperatingIncome,
                                    ]
                                    Total = a.IncomeBeforeTaxes
                                    #
                                    Components = sum(Components)
                                    #
                                    Anomaly = Components - Total
                                    #
                                    tb.NonOperatingIncome = tb.NonOperatingIncome - Anomaly
                                    #
                                    a.AnomalyNonOperatingIncome = Anomaly
                                    #
                                    # dataframe
                                    try:
                                        df = pd.DataFrame({
                                            #
                                            'income before taxes': 
                                                #
                                                [
                                                'Components',
                                                'Total',
                                                'Anomaly',
                                                'a.AnomalyNonOperatingIncome',
                                                'tb.NonOperatingIncome',
                                                ],
                                            #
                                            '.':
                                                #
                                                [
                                                '{:,}'.format(Components),
                                                '{:,}'.format(Total),
                                                '{:,}'.format(Anomaly),
                                                '{:,}'.format(a.AnomalyNonOperatingIncome),
                                                '{:,}'.format(tb.NonOperatingIncome),
                                                ],
                                        })
                                        print(df)
                                        print(137 * '-' + '\n')
                                        #
                                        tb.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # net income
                                try:
                                    #
                                    Anomaly = 0
                                    #
                                    Components = [
                                        a.IncomeBeforeTaxes,
                                        tb.IncomeTaxExpenseBenefit,
                                        tb.EquityMethodInvesteesIncome,
                                        tb.NetIncomeFromDiscontinuedOperations,
                                    ]
                                    Total = a.NetIncome
                                    #
                                    Components = sum(Components)
                                    #
                                    Anomaly = Components - Total
                                    #
                                    a.AnomalyNetIncome = Anomaly
                                    #
                                    # dataframe
                                    try:
                                        df = pd.DataFrame({
                                            #
                                            'net income': 
                                                #
                                                [
                                                'Components',
                                                'Total',
                                                'Anomaly',
                                                'a.AnomalyNetIncome',
                                                ],
                                            #
                                            '.':
                                                #
                                                [
                                                '{:,}'.format(Components),
                                                '{:,}'.format(Total),
                                                '{:,}'.format(Anomaly),
                                                '{:,}'.format(a.AnomalyNetIncome),
                                                ],
                                        })
                                        print(df)
                                        print(137 * '-' + '\n')
                                        #
                                        tb.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # other comprehensive income
                                try:
                                    #
                                    Anomaly = 0
                                    #
                                    Components = [
                                        tb.ChangeInForeignCurrencyTranslationAdjustment,
                                        tb.ChangeInUnrealizedGainsLossesOnDerivativeInstruments,
                                        tb.ChangeInUnrealizedGainsLossesOnInvestments,
                                        tb.ChangeInDefinedBenefitPensionAndOtherSimilarPlans,
                                        tb.IncomeTaxOnOtherComprehensiveIncome,
                                    ]
                                    #
                                    Total = a.OtherComprehensiveIncome
                                    #
                                    Components = sum(Components)
                                    #
                                    Anomaly = Components - Total
                                    #
                                    c = tb.ChangeInUnrealizedGainsLossesOnInvestments
                                    c = c - Anomaly
                                    tb.ChangeInUnrealizedGainsLossesOnInvestments = c
                                    #
                                    a.AnomalyOtherComprehensiveIncome = Anomaly
                                    #
                                    # dataframe
                                    try:
                                        df = pd.DataFrame({
                                            #
                                            'other comprehensive income': 
                                                #
                                                [
                                                'Components',
                                                'Total',
                                                'Anomaly',
                                                'a.AnomalyOtherComprehensiveIncome',
                                                'tb.ChangeInUnrealizedGainsLossesOnInvestments',
                                                ],
                                            #
                                            '.':
                                                #
                                                [
                                                '{:,}'.format(Components),
                                                '{:,}'.format(Total),
                                                '{:,}'.format(Anomaly),
                                                '{:,}'.format(a.AnomalyOtherComprehensiveIncome),
                                                '{:,}'.format(tb.ChangeInUnrealizedGainsLossesOnInvestments),
                                                ],
                                        })
                                        print(df)
                                        print(137 * '-' + '\n')
                                        #
                                        tb.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # convertible debt
                                try:
                                    #
                                    Anomaly = 0
                                    #
                                    Components = [
                                        tb.ConvertibleDebtBeginning,
                                    ]
                                    #
                                    Total = a.ConvertibleDebt
                                    #
                                    Components = sum(Components)
                                    #
                                    Anomaly = Components - Total
                                    #
                                    a.AnomalyConvertibleDebt = Anomaly
                                    #
                                    # dataframe
                                    try:
                                        df = pd.DataFrame({
                                            #
                                            'convertible debt': 
                                                #
                                                [
                                                'Components',
                                                'Total',
                                                'Anomaly',
                                                'a.AnomalyCommonShares',
                                                ],
                                            #
                                            '.':
                                                #
                                                [
                                                '{:,}'.format(Components),
                                                '{:,}'.format(Total),
                                                '{:,}'.format(Anomaly),
                                                '{:,}'.format(a.AnomalyConvertibleDebt),
                                                ],
                                        })
                                        print(df)
                                        print(137 * '-' + '\n')
                                        #
                                        tb.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # common shares
                                try:
                                    #
                                    Anomaly = 0
                                    #
                                    Components = [
                                        tb.CommonSharesBeginning,
                                        tb.CommonSharesIssued,
                                        tb.ShareBasedCompensation,
                                    ]
                                    #
                                    Total = a.CommonShares
                                    #
                                    Components = sum(Components)
                                    #
                                    Anomaly = Components - Total
                                    #
                                    tb.ShareBasedCompensation = tb.ShareBasedCompensation - Anomaly
                                    #
                                    a.AnomalyCommonShares = Anomaly
                                    #
                                    # dataframe
                                    try:
                                        df = pd.DataFrame({
                                            #
                                            'common shares': 
                                                #
                                                [
                                                'Components',
                                                'Total',
                                                'Anomaly',
                                                'a.AnomalyCommonShares',
                                                'tb.ShareBasedCompensation',
                                                ],
                                            #
                                            '.':
                                                #
                                                [
                                                '{:,}'.format(Components),
                                                '{:,}'.format(Total),
                                                '{:,}'.format(Anomaly),
                                                '{:,}'.format(a.AnomalyCommonShares),
                                                '{:,}'.format(tb.ShareBasedCompensation),
                                                ],
                                        })
                                        print(df)
                                        print(137 * '-' + '\n')
                                        #
                                        tb.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # accumulated other comprehensive income
                                try:
                                    #
                                    Anomaly = 0
                                    #
                                    Components = [
                                        tb.AccumulatedOtherComprehensiveIncomeBeginning,
                                        tb.ChangeInForeignCurrencyTranslationAdjustment,
                                        tb.ChangeInUnrealizedGainsLossesOnDerivativeInstruments,
                                        tb.ChangeInUnrealizedGainsLossesOnInvestments,
                                        tb.ChangeInDefinedBenefitPensionAndOtherSimilarPlans,
                                        tb.IncomeTaxOnOtherComprehensiveIncome,
                                    ]
                                    #
                                    Total = a.AccumulatedOtherComprehensiveIncome
                                    #
                                    Components = sum(Components)
                                    #
                                    Anomaly = Components - Total
                                    #
                                    c = tb.ChangeInUnrealizedGainsLossesOnInvestments
                                    c = c - Anomaly
                                    tb.ChangeInUnrealizedGainsLossesOnInvestments = c
                                    #
                                    c = a.OtherComprehensiveIncome
                                    c = c - Anomaly
                                    a.OtherComprehensiveIncome = c
                                    #
                                    c = Anomaly
                                    a.AnomalyAccumulatedOtherComprehensiveIncome = c
                                    #
                                    # dataframe
                                    try:
                                        df = pd.DataFrame({
                                            #
                                            'accumulated other comprehensive income': 
                                                #
                                                [
                                                'Components',
                                                'Total',
                                                'Anomaly',
                                                'a.AnomalyOtherComprehensiveIncome',
                                                'tb.ChangeInUnrealizedGainsLossesOnInvestments',
                                                ],
                                            #
                                            '.':
                                                #
                                                [
                                                '{:,}'.format(Components),
                                                '{:,}'.format(Total),
                                                '{:,}'.format(Anomaly),
                                                '{:,}'.format(a.AnomalyOtherComprehensiveIncome),
                                                '{:,}'.format(tb.ChangeInUnrealizedGainsLossesOnInvestments),
                                                ],
                                        })
                                        print(df)
                                        print(137 * '-' + '\n')
                                        #
                                        tb.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # retained earnings
                                try:
                                    Anomaly = 0
                                    Components = [
                                        tb.RetainedEarningsBeginning,
                                        tb.DividendsAndDividendEquivalentsDeclared,
                                        tb.CommonSharesRepurchasedAndRetired,
                                        tb.ShareBasedCompensationRetainedEarnings,
                                        tb.EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts,
                                        a.NetIncome,
                                    ]
                                    #
                                    Total = a.RetainedEarnings
                                    #
                                    Components = sum(Components)
                                    #
                                    Anomaly = Components - Total
                                    #
                                    tb.RetainedEarningsOthers = -Anomaly
                                    #
                                    a.AnomalyRetainedEarnings = Anomaly
                                    #
                                    # dataframe
                                    try:
                                        df = pd.DataFrame({
                                            #
                                            'retained earnings': 
                                                #
                                                [
                                                'Components',
                                                'Total',
                                                'Anomaly',
                                                'a.AnomalyRetainedEarnings',
                                                'tb.RetainedEarningsOthers',
                                                ],
                                            #
                                            '.':
                                                #
                                                [
                                                '{:,}'.format(Components),
                                                '{:,}'.format(Total),
                                                '{:,}'.format(Anomaly),
                                                '{:,}'.format(a.AnomalyRetainedEarnings),
                                                '{:,}'.format(tb.RetainedEarningsOthers),
                                                ],
                                        })
                                        print(df)
                                        print(137 * '-' + '\n')
                                        #
                                        tb.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # treasury shares
                                try:
                                    #
                                    Anomaly = 0
                                    #
                                    Components = [
                                        tb.TreasurySharesBeginning,
                                        tb.PurchaseAndSellOfTreasuryShares,
                                    ]
                                    #
                                    Total = a.TreasuryShares
                                    #
                                    Components = sum(Components)
                                    #
                                    Anomaly = Components - Total
                                    #
                                    c = tb.PurchaseAndSellOfTreasuryShares
                                    c = c - Anomaly
                                    tb.PurchaseAndSellOfTreasuryShares = c
                                    #
                                    a.AnomalyTreasuryShares = Anomaly
                                    #
                                    # dataframe
                                    try:
                                        df = pd.DataFrame({
                                            #
                                            'treasury shares': 
                                                #
                                                [
                                                'Components',
                                                'Total',
                                                'Anomaly',
                                                'a.AnomalyTreasuryShares',
                                                'tb.PurchaseAndSellOfTreasuryShares',
                                                ],
                                            #
                                            '.':
                                                #
                                                [
                                                '{:,}'.format(Components),
                                                '{:,}'.format(Total),
                                                '{:,}'.format(Anomaly),
                                                '{:,}'.format(a.AnomalyTreasuryShares),
                                                '{:,}'.format(tb.PurchaseAndSellOfTreasuryShares),
                                                ],
                                        })
                                        print(df)
                                        print(137 * '-' + '\n')
                                        #
                                        tb.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # non controlling interests
                                try:
                                    #
                                    Anomaly = 0
                                    #
                                    Components = [
                                        tb.NonControllingInterestsBeginning,
                                        tb.DividendsDeclaredToNonControllingInterests,
                                        tb.AcquisitionOfNonControllingInterests,
                                        tb.NonControllingInterestsOthers,
                                    ]
                                    #
                                    Total = a.NonControllingInterests
                                    #
                                    Components = sum(Components)
                                    #
                                    Anomaly = Components - Total
                                    #
                                    tb.NonControllingInterestsOthers = -Anomaly
                                    #
                                    a.AnomalyNonControllingInterests = Anomaly
                                    #
                                    # dataframe
                                    try:
                                        df = pd.DataFrame({
                                            #
                                            'non controlling interests': 
                                                #
                                                [
                                                'Components',
                                                'Total',
                                                'Anomaly',
                                                'a.AnomalyNonControllingInterests',
                                                'tb.NonControllingInterestsOthers',
                                                ],
                                            #
                                            '.':
                                                #
                                                [
                                                '{:,}'.format(Components),
                                                '{:,}'.format(Total),
                                                '{:,}'.format(Anomaly),
                                                '{:,}'.format(a.AnomalyNonControllingInterests),
                                                '{:,}'.format(tb.NonControllingInterestsOthers),
                                                ],
                                        })
                                        print(df)
                                        print(137 * '-' + '\n')
                                        #
                                        tb.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # shareholders equity
                                try:
                                    #
                                    Anomaly = 0
                                    #
                                    Components = [
                                        a.ConvertibleDebt,
                                        a.CommonShares,
                                        a.AccumulatedOtherComprehensiveIncome,
                                        a.RetainedEarnings,
                                        a.TreasuryShares,
                                        a.EmployeeBenefitTrust,
                                        a.NonControllingInterests,
                                    ]
                                    Total = a.ShareholdersEquity
                                    #
                                    Components = sum(Components)
                                    #
                                    Anomaly = Components - Total
                                    #
                                    a.AnomalyShareholdersEquity = Anomaly
                                    #
                                    # dataframe
                                    try:
                                        df = pd.DataFrame({
                                            #
                                            'shareholders equity': 
                                                #
                                                [
                                                'Components',
                                                'Total',
                                                'Anomaly',
                                                'a.AnomalyShareholdersEquity',
                                                ],
                                            #
                                            '.':
                                                #
                                                [
                                                '{:,}'.format(Components),
                                                '{:,}'.format(Total),
                                                '{:,}'.format(Anomaly),
                                                '{:,}'.format(a.AnomalyShareholdersEquity),
                                                ],
                                        })
                                        print(df)
                                        print(137 * '-' + '\n')
                                        #
                                        tb.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                            except:
                                pass
                            #
                            # cf 
                            try:
                                #
                                cf = CashFlow.objects.get(TradingSymbol=e.TradingSymbol, PeriodEndDate=periodenddate)
                                #
                                # operating activities
                                try:
                                    Anomaly = 0
                                    Components = [
                                        -a.NetIncome,
                                        cf.DepreciationDepletionAndAmortization,
                                        cf.GainRelatedToDisposalOrSale,
                                        cf.RestructuringAndOtherSpecialCharges,
                                        cf.AccruedEmployeeCompensation,
                                        cf.ShareBasedCompensation,
                                        cf.IncreaseDecreaseInIncomeTaxExpenseBenefit,
                                        cf.OtherNonCashIncomeExpense,
                                        cf.IncreaseDecreaseInAccountsReceivable, 
                                        cf.IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets,
                                        cf.IncreaseDecreaseInInventories,
                                        cf.IncreaseDecreaseInOtherReceivables,
                                        cf.IncreaseDecreaseInAccountsPayableAndAccruedLiabilities,
                                        cf.IncreaseDecreaseInContractWithCustomerLiability,
                                        cf.IncreaseDecreaseInRetirementBenefits,
                                        cf.IncreaseDecreaseFinanceLeaseCurrent,
                                        cf.IncreaseDecreaseOperatingLeaseCurrent,
                                        cf.IncreaseDecreaseInFairValueOfDerivativesOperating,
                                        cf.IncreaseDecreaseInOtherOperatingActivities,
                                    ]
                                    Total = a.OperatingActivities
                                    #
                                    Components = sum(Components)
                                    #
                                    Anomaly = Components - Total
                                    #
                                    c = cf.IncreaseDecreaseInOtherOperatingActivities
                                    c = c - Anomaly
                                    cf.IncreaseDecreaseInOtherOperatingActivities = c
                                    #
                                    #
                                    # dataframe
                                    try:
                                        df = pd.DataFrame({
                                            #
                                            'operating activities': 
                                                #
                                                [
                                                'Components',
                                                'Total',
                                                'Anomaly',
                                                'a.AnomalyOperatingActivitiesSEC',
                                                'cf.IncreaseDecreaseInOtherOperatingActivities',
                                                ],
                                            #
                                            '.':
                                                #
                                                [
                                                '{:,}'.format(Components),
                                                '{:,}'.format(Total),
                                                '{:,}'.format(Anomaly),
                                                '{:,}'.format(a.AnomalyOperatingActivitiesSEC),
                                                '{:,}'.format(cf.IncreaseDecreaseInOtherOperatingActivities),
                                                ],
                                        })
                                        print(df)
                                        print(137 * '-' + '\n')
                                        #
                                        cf.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # investing activities
                                try:
                                    #
                                    Anomaly = 0
                                    #
                                    Components = [
                                        cf.PaymentsToAcquirePropertyPlantAndEquipment,
                                        cf.ProceedsFromDisposalsOfPropertyAndEquipment,
                                        cf.PaymentsToAcquireInvestments,
                                        cf.ProceedsOfInvestments,
                                        cf.PaymentsToAcquireBusinessesAndIntangibles,
                                        cf.ProceedsFromDisposalsOfBusinessesAndIntangibles,
                                        cf.ProceedsRelatedToInsuranceSettlement,
                                        cf.ReveiptOfGovernmentGrants,
                                        cf.EquityInvesteeAdvancesRepayments,
                                        cf.PaymentOfLicenseFee,
                                        cf.InvestingActivitiesInDiscontinuedOperations,
                                        cf.OtherInvestingActivities,
                                    ]
                                    Total = a.InvestingActivities
                                    #
                                    Components = sum(Components)
                                    #
                                    Anomaly = Components - Total
                                    #
                                    c = cf.OtherInvestingActivities
                                    c = c - Anomaly
                                    cf.OtherInvestingActivities = c
                                    #
                                    c = Anomaly
                                    a.AnomalyInvestingActivities = c
                                    #
                                    # dataframe
                                    try:
                                        df = pd.DataFrame({
                                            #
                                            'investing activities': 
                                                #
                                                [
                                                'Components',
                                                'Total',
                                                'Anomaly',
                                                'a.AnomalyInvestingActivities',
                                                'a.AnomalyInvestingActivitiesSEC',
                                                'cf.OtherInvestingActivities',
                                                ],
                                            #
                                            '.':
                                                #
                                                [
                                                '{:,}'.format(Components),
                                                '{:,}'.format(Total),
                                                '{:,}'.format(Anomaly),
                                                '{:,}'.format(a.AnomalyInvestingActivities),
                                                '{:,}'.format(a.AnomalyInvestingActivitiesSEC),
                                                '{:,}'.format(cf.OtherInvestingActivities),
                                                ],
                                        })
                                        print(df)
                                        print(137 * '-' + '\n')
                                        #
                                        cf.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                                #
                                # financing activities
                                try:
                                    #
                                    Anomaly = 0
                                    #
                                    Components = [
                                        cf.FinanceLeasePrincipalPayments,
                                        cf.ProceedsFromIssuanceOfCommonShares,
                                        cf.ProceedsFromSharePurchasePlanAndOptionsExercice,
                                        cf.PaymentsRelatedToTaxWithholdingForShareBasedCompensation,
                                        cf.PaymentsOfDividends,
                                        cf.PaymentsForRepurchaseOfCommonShares,
                                        cf.IncreaseDecreaseDeferredContingentConsideration,
                                        cf.ProceedsFromIssuanceOfLongTermDebt,
                                        cf.RepaymentsOfLongTermDebt,
                                        cf.FinancingCosts,
                                        cf.NetChangeInShortTermBorrowings,
                                        cf.NetChangeInForwardAndHedgesClassifiedAsFinancingActivities,
                                        cf.NetChangeInNonControllingInterests,
                                        cf.ProceedsFromRepaymentsOfCommercialPaper,
                                        cf.RepaymentsOfConvertible,
                                        cf.IssuanceOfConvertible,
                                        cf.OtherFinancingActivities,
                                    ]
                                    Total = a.FinancingActivities
                                    #
                                    Components = sum(Components)
                                    #
                                    Anomaly = Components - Total
                                    #
                                    c = cf.OtherFinancingActivities
                                    c = c - Anomaly
                                    cf.OtherFinancingActivities = c
                                    #
                                    c = Anomaly
                                    a.AnomalyFinancingActivities = c
                                    #
                                    # dataframe
                                    try:
                                        df = pd.DataFrame({
                                            #
                                            'financing activities': 
                                                #
                                                [
                                                'Components',
                                                'Total',
                                                'Anomaly',
                                                'a.AnomalyFinancingActivities',
                                                'a.AnomalyFinancingActivitiesSEC',
                                                'cf.OtherFinancingActivities',
                                                ],
                                            #
                                            '.':
                                                #
                                                [
                                                '{:,}'.format(Components),
                                                '{:,}'.format(Total),
                                                '{:,}'.format(Anomaly),
                                                '{:,}'.format(a.AnomalyFinancingActivities),
                                                '{:,}'.format(a.AnomalyFinancingActivitiesSEC),
                                                '{:,}'.format(cf.OtherFinancingActivities),
                                                ],
                                        })
                                        print(df)
                                        print(137 * '-' + '\n')
                                        #
                                        cf.save()
                                        a.save()
                                    except:
                                        pass
                                except:
                                    pass
                            except:
                                pass
            except:
                pass
            #            
            # additional information
            try:
                #
                periodenddates.sort(reverse=True)
                #
                print(periodenddates)
                #
                for periodenddate in periodenddates:
                    #
                    if periodenddate != None:
                        #
                        a = AuditData.objects.get(TradingSymbol=e.TradingSymbol, PeriodEndDate=periodenddate)
                        #
                        if a.db not in marketdata:
                            # 
                            print(e.EntityRegistrantName)
                            print('additional information')
                            print(tb.PeriodEndDate)
                            print(137 * '-' + '\n')
                            #
                            tb = TrialBalance.objects.get(TradingSymbol=e.TradingSymbol, PeriodEndDate=periodenddate)
                            cf = CashFlow.objects.get(TradingSymbol=e.TradingSymbol, PeriodEndDate=periodenddate)
                            a = AuditData.objects.get(TradingSymbol=e.TradingSymbol, PeriodEndDate=periodenddate)
                            #
                            # additional informations
                            try:
                                #
                                # Target Working Capital
                                try:
                                    z = 1.2
                                    a.TargetWorkingCapital = z
                                except:
                                    pass
                                #
                                # Reinvestment Of Maintenance
                                try:
                                    z = -cf.PaymentsToAcquirePropertyPlantAndEquipment
                                    a.ReinvestmentOfMaintenance = z
                                except:
                                    pass
                                #
                                # Theorical Annual Interest Charge
                                try:
                                    z = 0.035
                                    a.TheoricalInterestRate = z
                                except:
                                    pass
                                #
                                # Normalized Dividend Payment To Non Controlling Interests
                                try:
                                    z = tb.DividendsDeclaredToNonControllingInterests
                                    a.NormalizedDividendPaymentToNonControllingInterests = z
                                except:
                                    pass
                                #
                                # Normalized Dividend Payment To Preferred Shareholders
                                try:
                                    a.NormalizedDividendPaymentToPreferredShareholders = 0
                                except:
                                    pass
                                #
                                # Theorical Tax Rate
                                try:
                                    z = tb.IncomeTaxExpenseBenefit
                                    z = z / -a.IncomeBeforeTaxes
                                    z = min(0.35, z)
                                    z = max(0.15, z)
                                    a.TheoricalTaxRate = z
                                except:
                                    pass
                                #
                                a.save()
                                #
                                # dataframe
                                try:
                                    df = pd.DataFrame({
                                        #
                                        'additional information': 
                                            #
                                            [
                                            'a.NormalizedTheoricalInterestCharge',
                                            'a.ReinvestmentOfMaintenance',
                                            'a.NormalizedDividendPaymentToNonControllingInterests',
                                            'a.NormalizedDividendPaymentToPreferredShareholders',
                                            'a.TheoricalTaxRate',
                                            'a.TargetWorkingCapital',
                                            ],
                                        #
                                        '.':
                                            #
                                            [
                                            '{:,}'.format(a.NormalizedTheoricalInterestCharge),
                                            '{:,}'.format(a.ReinvestmentOfMaintenance),
                                            '{:,}'.format(a.NormalizedDividendPaymentToNonControllingInterests),
                                            '{:,}'.format(a.NormalizedDividendPaymentToPreferredShareholders),
                                            '{:,}'.format(a.TheoricalTaxRate),
                                            '{:,}'.format(a.TargetWorkingCapital),
                                            ],
                                    })
                                    print(df)
                                    print(137 * '-' + '\n')
                                    #
                                    a.save()
                                except:
                                    pass
                            except:
                                pass
            except:
                pass
            #
            # outstanding shares
            try:
                #
                periodenddates.sort(reverse=True)
                #
                for periodenddate in periodenddates:
                    #
                    if periodenddate != None:
                        #
                        if e.db in marketdata:
                            #
                            try:
                                #
                                a = AuditData.objects.get(TradingSymbol=e.TradingSymbol, PeriodEndDate=periodenddate)
                                #
                                acc = a.AccessionNumber
                                #
                                OutstandingShares = []
                                #
                                c = 'https://www.sec.gov/Archives/edgar/data/'
                                try:
                                    c = c + e.EntityCentralIndexKey
                                    c = c + '/' + acc.replace('-','')
                                    c = c + '/' 'R1.htm'
                                    #
                                    a.URLoustandingshares = c
                                    #
                                    r = 0
                                    while r < 10:
                                        try:
                                            c = requests.get(c).content
                                            r = 10
                                        except:
                                            r = r + 1
                                            time.sleep(1)
                                    #
                                    r = 0
                                    while r < 10:
                                        try:
                                            c = BeautifulSoup(c, 'html')
                                            r = 10
                                        except:
                                            r = r + 1
                                            time.sleep(1)
                                    #
                                    r = 0
                                    while r < 10:
                                        try:
                                            q = c.find_all('tr')
                                            r = 10
                                        except:
                                            r = r + 1
                                            time.sleep(1)
                                except:
                                    pass
                                #
                                p = 0
                                while p < len(q) - 1:
                                    try:
                                        d = q[p].find_all('a')[0].text
                                        if 'OUTSTANDING' in d.upper():
                                            OutstandingShares.append(p)
                                    except:
                                        pass
                                    p = p + 1
                                    #
                                b = 0
                                for h in OutstandingShares:
                                    #
                                    b = b + int(q[h].find_all('td', class_='nump')[0].text.replace(',',''))
                                #
                                # dad
                                d = c.find_all('tr')[0].text
                                q = [
                                    b,
                                    d,
                                ]
                                #
                                dad = 0
                                for p in q:
                                    if 'SHARES IN MILLIONS' in d.upper():
                                        dad = 1000000
                                    elif 'SHARES IN THOUSANDS' in d.upper():
                                        dad = 1000
                                    else:
                                        dad = 1
                                #
                                c = b * dad
                                a.CommonSharesOutstanding = c
                                #
                                if a.PeriodEndDate == periodenddates[0]:
                                    e.CommonSharesOutstandingLastYear = c
                                if a.PeriodEndDate == periodenddates[1]:
                                    e.CommonSharesOutstandingSecondLastYear = c
                                if a.PeriodEndDate == periodenddates[2]:
                                    e.CommonSharesOutstandingThirdLastYear = c
                                if a.PeriodEndDate == periodenddates[3]:
                                    e.CommonSharesOutstandingFourthLastYear = c
                                #
                                a.save()
                                e.save()
                                #
                                print(e.EntityRegistrantName)
                                print('shares outstanding')
                                print(a.PeriodEndDate)
                                print(137*'-' + '\n')
                                print(str('{:,}'.format(a.CommonSharesOutstanding)))
                                print('\n' + 137*'-' + '\n')
                            except:
                                pass
            except:
                pass               
            #
            # filing dates
            try:
                #
                periodenddates.sort(reverse=True)
                #
                for periodenddate in periodenddates:
                    #
                    if periodenddate != None:
                        #
                        if e.db in marketdata:
                            #
                            a = AuditData.objects.get(TradingSymbol=e.TradingSymbol, PeriodEndDate=periodenddate)
                            #
                            acc = a.AccessionNumber
                            #
                            try:
                                c = 0
                                q = 0
                                p = ''
                                while q < 9:
                                    if p == '':
                                        try:
                                            d = periodenddate
                                            d = d - datetime.timedelta(days=q)
                                            b = 'https://api.marketstack.com/v1/tickers/' + e.TradingSymbol + '/eod/' + str(d)
                                            b = requests.get(b, API)
                                            c = b.json()['close']
                                            if c != 0:
                                                p = 'h'
                                        except:
                                            time.sleep(1)
                                    else:
                                        pass
                                    q = q + 1
                                if p == 'h':
                                    a.CommonSharePrice = c
                                    #
                                    if a.PeriodEndDate == periodenddates[0]:
                                        e.CommonSharePriceLastYear = c
                                    if a.PeriodEndDate == periodenddates[1]:
                                        e.CommonSharePriceSecondLastYear = c
                                    if a.PeriodEndDate == periodenddates[2]:
                                        e.CommonSharePriceThirdLastYear = c
                                    if a.PeriodEndDate == periodenddates[3]:
                                        e.CommonSharePriceFourthLastYear = c
                            except:
                                pass
                            #
                            # market capitalization
                            try:
                                c = c * a.CommonSharesOutstanding
                                a.MarketCapitalization = c
                                #
                                if a.PeriodEndDate == periodenddates[0]:
                                    e.MarketCapitalizationLastYear = c
                                if a.PeriodEndDate == periodenddates[1]:
                                    e.MarketCapitalizationSecondLastYear = c
                                if a.PeriodEndDate == periodenddates[2]:
                                    e.MarketCapitalizationThirdLastYear = c
                                if a.PeriodEndDate == periodenddates[3]:
                                    e.MarketCapitalizationFourthLastYear = c
                            except:
                                pass
                            #
                            a.save()
                            #
                            print(e.EntityRegistrantName)
                            print('stock price')
                            print(a.PeriodEndDate)
                            print(137*'-' + '\n')
                            print(str('{:,}'.format(a.CommonSharePrice)))
                            print(str('{:,}'.format(a.MarketCapitalization)))
                            print(137*'-' + '\n')
            except:
                pass
            #
            # current stock price
            try:
                #
                d = requests.get('https://api.marketstack.com/v1/tickers/' + e.TradingSymbol + '/eod', API)
                p = d.json()['data']['name']
                q = d.json()['data']['symbol']
                b = d.json()['data']['eod'][0]['date']
                c = d.json()['data']['eod'][0]['close']
                #
                e.CommonSharePriceLastYear = float(c)
                e.SecuritiesUpdate = datetime.datetime.today()
                e.save()
                #
                # market capitalization
                try:
                    #
                    u = e.CommonSharesOutstandingLastYear
                    c = u * c
                    e.MarketCapitalization = c
                    #
                    print(e.EntityRegistrantName)
                    print('current stock price & market capitalization')
                    print(137*'-' + '\n')
                    print(str('{:,}'.format(e.CommonSharePriceLastYear)))
                    print(str('{:,}'.format(e.MarketCapitalizationLastYear)))
                    print(137*'-' + '\n')
                    #
                except:
                    pass
            except:
                pass
            #
            # web application
            try:
                #
                driver = webdriver.Firefox(executable_path=r'C:\\Program Files\\geckodriver.exe')
                #
                url = 'http://127.0.0.1:8000/'
                #
                driver.get(url)
                #
                try:
                    link = WebDriverWait(driver, 13).until(
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
                #
                url = 'http://127.0.0.1:8000/67/WorkingPaper/' + e.TradingSymbol + '/'
                #
                driver.get(url)
                #
                try:
                    link = WebDriverWait(driver, 13).until(
                        EC.presence_of_element_located((By.NAME, "Opinion"))
                    )
                except:
                    pass
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
                        'Bridgeφ1',
                        'Bridgeφ2',
                        'Bridgeφ3',
                        'Bridgeφ4',
                        'Opinionφ1',
                        'Opinionφ2',
                        'Opinionφ3',
                        'Opinionφ4',
                    ]
                    #
                    dd = [
                        ',',
                    ]
                    qq = [
                        '∞',
                        'NaN',
                    ]
                    #
                    i = 0
                    #
                    print('---')
                    #
                    for a in aa:
                        #
                        print(a)
                        #
                        g = driver.find_element_by_id(a)
                        #
                        print(g)
                        #
                        c = g.get_attribute('innerHTML')
                        #
                        print(c)
                        #
                        if c == '':
                            c = g.get_attribute('value')
                        #
                        print(c)
                        w = ''
                        if i < 12:
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
                        print(c)
                        #
                        if a == aa[0]:
                            e.ClockφLastYear = c
                        if a == aa[1]:
                            e.ClockφSecondLastYear = c
                        if a == aa[2]:
                            e.ClockφThirdLastYear = c
                        if a == aa[3]:
                            e.ClockφFourthLastYear = c
                        if a == aa[4]:
                            e.CommonSharesIntrinsicValueLastYear = c
                        if a == aa[5]:
                            e.CommonSharesIntrinsicValueSecondLastYear = c
                        if a == aa[6]:
                            e.CommonSharesIntrinsicValueThirdLastYear = c
                        if a == aa[7]:
                            e.CommonSharesIntrinsicValueFourthLastYear = c
                        if a == aa[8]:
                            e.CommonShareIntrinsicValueLastYear = c
                        if a == aa[9]:
                            e.CommonShareIntrinsicValueSecondLastYear = c
                        if a == aa[10]:
                            e.CommonShareIntrinsicValueThirdLastYear = c
                        if a == aa[11]:
                            e.CommonShareIntrinsicValueFourthLastYear = c
                        if a == aa[12]:
                            e.BridgeφLastYear = c
                        if a == aa[13]:
                            e.BridgeφSecondLastYear = c
                        if a == aa[14]:
                            e.BridgeφThirdLastYear = c
                        if a == aa[15]:
                            e.BridgeφFourthLastYear = c
                        if a == aa[16]:
                            e.OpinionφLastYear = c
                        if a == aa[17]:
                            e.OpinionφSecondLastYear = c
                        if a == aa[18]:
                            e.OpinionφThirdLastYear = c
                        if a == aa[19]:
                            e.OpinionφFourthLastYear = c
                        #
                        i = i + 1
                except:
                    pass
            except:
                pass
            #
            # driver quit
            try:
                driver.quit()
            except:
                pass
            #
            # db
            try:
                e.db = 12 + lt
                if e.db > 17:
                    if e.CommonSharePriceLastYear != 0:
                        k = 0
                        periodenddatesb = [
                            e.lastyear,
                            e.secondlastyear,
                            e.thirdlastyear,
                            e.fourthlastyear,
                        ]
                        for periodenddate in periodenddatesb:
                            a = AuditData.objects.get(TradingSymbol=e.TradingSymbol, PeriodEndDate=periodenddate)
                            if a.CommonSharePrice != 0:
                                k = k + 1
                        if k > 3:
                            e.db = 20
                        else:
                            e.db = 19
                #
                e.NumberOfYearsAudited = lt - ea
                #
                if e.NumberOfYearsAudited == 0:
                    e.db = 12
            except:
                pass
            #
            # time of update
            try:
                e.SEC_Update = datetime.datetime.today()
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
    #
    # machine learning
    try:
        #
        # clear
        try:
            f = glob.glob('A:/clock/φ/machine learning/ml.txt')
            if f != []:
                os.remove(f)
        except:
            pass
        #
        c = './φ/machine learning/'
        #
        # current assets
        CurrentAssetsGL.sort()
        with open(c + 'CurrentAssetsGL.txt', 'w') as ml:
            for g in CurrentAssetsGL:
                ml.write(g + " \n")
        #
        # non current assets
        NonCurrentAssetsGL.sort()
        with open(c + 'NonCurrentAssetsGL.txt', 'w') as ml:
            for g in NonCurrentAssetsGL:
                ml.write(g + " \n")
        #
        # current liabilities
        CurrentLiabilitiesGL.sort()
        with open(c + 'CurrentLiabilitiesGL.txt', 'w') as ml:
            for g in CurrentLiabilitiesGL:
                ml.write(g + " \n")
        #
        # non current liabilities
        NonCurrentLiabilitiesGL.sort()
        with open(c + 'NonCurrentLiabilitiesGL.txt', 'w') as ml:
            for g in NonCurrentLiabilitiesGL:
                ml.write(g + " \n")
        #
        # non current liabilities
        ShareholdersEquityBalanceGL.sort()
        with open(c + 'ShareholdersEquityBalanceGL.txt', 'w') as ml:
            for g in ShareholdersEquityBalanceGL:
                ml.write(g + " \n")
        #
        # gross margin
        GrossMarginGL.sort()
        with open(c + 'GrossMarginGL.txt', 'w') as ml:
            for g in GrossMarginGL:
                ml.write(g + " \n")
        #
        # operating expenses
        OperatingExpensesGL.sort()
        with open(c + 'OperatingExpensesGL.txt', 'w') as ml:
            for g in OperatingExpensesGL:
                ml.write(g + " \n")
        #
        # operating income
        OperatingIncomeGL.sort()
        with open(c + 'OperatingIncomeGL.txt', 'w') as ml:
            for g in OperatingIncomeGL:
                ml.write(g + " \n")
        #
        # income before taxes
        IncomeBeforeTaxesGL.sort()
        with open(c + 'IncomeBeforeTaxesGL.txt', 'w') as ml:
            for g in IncomeBeforeTaxesGL:
                ml.write(g + " \n")
        #
        # net income
        NetIncomeGL.sort()
        with open(c + 'NetIncomeGL.txt', 'w') as ml:
            for g in NetIncomeGL:
                ml.write(g + " \n")
        #
        # other comprehensive income
        OtherComprehensiveIncomeGL.sort()
        with open(c + 'OtherComprehensiveIncomeGL.txt', 'w') as ml:
            for g in OtherComprehensiveIncomeGL:
                ml.write(g + " \n")
        #
        # shareholders equity
        ShareholdersEquityGL.sort()
        with open(c + 'ShareholdersEquityGL.txt', 'w') as ml:
            for g in ShareholdersEquityGL:
                ml.write(g + " \n")
        #
        # operating activities
        OperatingActivitiesGL.sort()
        with open(c + 'OperatingActivitiesGL.txt', 'w') as ml:
            for g in OperatingActivitiesGL:
                ml.write(g + " \n")
        #
        # investing activities
        InvestingActivitiesGL.sort()
        with open(c + 'InvestingActivitiesGL.txt', 'w') as ml:
            for g in InvestingActivitiesGL:
                ml.write(g + " \n")
        #
        # financing activities
        FinancingActivitiesGL.sort()
        with open(c + 'FinancingActivitiesGL.txt', 'w') as ml:
            for g in FinancingActivitiesGL:
                ml.write(g + " \n")
    except:
        pass
    #
    # db stats
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
except:
    pass


