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
import urllib.request, json
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

base_url = 'http://www.clockdb.com/'

entities_url = base_url + 'entities/'

with urllib.request.urlopen(entities_url) as url:
    data = json.loads(url.read().decode())
    entitiesData = data['entities']

start = 0

i = 0

for entity in entitiesData:
    #if (i > start - 1):
    if (i < 1):
        try:
            #ts = entity['url'].replace('./', '')
            ts = 'FLWS'
            try:
                e = Entity.objects.get(TradingSymbol=ts)
            except:
                e = Entity()
                e.TradingSymbol = ts
            if (e.db < 21):
                # Get url from Trading Symbol
                url = base_url + ts
                r = 0
                while r < 10:
                    try:
                        html = fetch(url)
                        r = 10
                    except:
                        r = r + 1
                html = fetch(url)
                # entity
                try:
                    #
                    e.db = int(html.find(id='WIP1')['value'])
                    #
                    e.Industry_db = int(html.find(id='Industrydb1')['value'])
                    e.Region_db = int(html.find(id='Regiondb1')['value'])
                    #
                    e.EntityRegistrantName = html.find(id='EntityRegistrantName1')['value']
                    e.EntityCentralIndexKey = html.find(id='CIK1')['value']
                    #
                    e.Industry = html.find(id='Industry1')['value']
                    #
                    e.Industry_SEC = html.find(id='Industry_SEC1')['value']
                    e.Industry_SEC_db = int(html.find(id='Industry_SEC_db1')['value'])
                    #
                    e.Region = html.find(id='Region1')['value']
                    #
                    e.CommonSharePriceLastYear = float(html.find(id='SharePrice1')['value'])
                    e.CommonSharePriceSecondLastYear = float(html.find(id='SharePrice2')['value'])
                    e.CommonSharePriceThirdLastYear = float(html.find(id='SharePrice3')['value'])
                    e.CommonSharePriceFourthLastYear = float(html.find(id='SharePrice4')['value'])
                    #
                    e.CommonSharesOutstandingLastYear = int(html.find(id='CommonSharesOutstanding1')['value'])
                    e.CommonSharesOutstandingSecondLastYear = int(html.find(id='CommonSharesOutstanding2')['value'])
                    e.CommonSharesOutstandingThirdLastYear = int(html.find(id='CommonSharesOutstanding3')['value'])
                    e.CommonSharesOutstandingFourthLastYear = int(html.find(id='CommonSharesOutstanding4')['value'])
                    #
                    e.accessionnumberlastyear = html.find(id='AccessionNumber1')['value']
                    e.accessionnumbersecondlastyear = html.find(id='AccessionNumber2')['value']
                    e.accessionnumberthirdlastyear = html.find(id='AccessionNumber3')['value']
                    e.accessionnumberfourthlastyear = html.find(id='AccessionNumber4')['value']
                    e.accessionnumberfifthlastyear = html.find(id='AccessionNumber5')['value']
                    e.accessionnumbersixthlastyear = html.find(id='AccessionNumber6')['value']
                    #
                    c = html.find(id='ContextDate1')['value']
                    c = c.replace('. ', '')
                    r = len(c) - 9
                    month = c[:r]
                    year = c.replace(month, '')[-4:]
                    day = c.replace(month, '').replace(year, '').replace('. ', '').replace(', ', '').replace(' ', '')
                    try:
                        if (month == 'Jan'):
                            month = 1
                        if (month == 'Feb'):
                            month = 2
                        if (month == 'Mar'):
                            month = 3
                        if (month == 'March'):
                            month = 3
                        if (month == 'April'):
                            month = 4
                        if (month == 'May'):
                            month = 5
                        if (month == 'Jun'):
                            month = 6
                        if (month == 'Jul'):
                            month = 7

                        if (month == 'July'):
                            month = 7
                        if (month == 'Aug'):
                            month = 8
                        if (month == 'Sept'):
                            month = 9
                        if (month == 'Oct'):
                            month = 10
                        if (month == 'Nov'):
                            month = 11
                        if (month == 'Dec'):
                            month = 12
                    except:
                        pass
                    c = datetime.datetime(year=int(year), month=int(month), day=int(day))
                    e.lastyear = c
                    #
                    c = html.find(id='ContextDate2')['value']
                    c = c.replace('. ', '')
                    r = len(c) - 9
                    month = c[:r]
                    year = c.replace(month, '')[-4:]
                    day = c.replace(month, '').replace(year, '').replace('. ', '').replace(', ', '').replace(' ', '')
                    try:
                        if (month == 'Jan'):
                            month = 1
                        if (month == 'Feb'):
                            month = 2
                        if (month == 'Mar'):
                            month = 3
                        if (month == 'March'):
                            month = 3
                        if (month == 'April'):
                            month = 4
                        if (month == 'May'):
                            month = 5
                        if (month == 'Jun'):
                            month = 6
                        if (month == 'Jul'):
                            month = 7
                        if (month == 'July'):
                            month = 7
                        if (month == 'Aug'):
                            month = 8
                        if (month == 'Sept'):
                            month = 9
                        if (month == 'Oct'):
                            month = 10
                        if (month == 'Nov'):
                            month = 11
                        if (month == 'Dec'):
                            month = 12
                    except:
                        pass
                    c = datetime.datetime(year=int(year), month=int(month), day=int(day))
                    e.secondlastyear = c
                    #
                    c = html.find(id='ContextDate3')['value']
                    c = c.replace('. ', '')
                    r = len(c) - 9
                    month = c[:r]
                    year = c.replace(month, '')[-4:]
                    day = c.replace(month, '').replace(year, '').replace('. ', '').replace(', ', '').replace(' ', '')
                    try:
                        if (month == 'Jan'):
                            month = 1
                        if (month == 'Feb'):
                            month = 2
                        if (month == 'Mar'):
                            month = 3
                        if (month == 'March'):
                            month = 3
                        if (month == 'April'):
                            month = 4
                        if (month == 'May'):
                            month = 5
                        if (month == 'Jun'):
                            month = 6
                        if (month == 'Jul'):
                            month = 7
                        if (month == 'July'):
                            month = 7
                        if (month == 'Aug'):
                            month = 8
                        if (month == 'Sept'):
                            month = 9
                        if (month == 'Oct'):
                            month = 10
                        if (month == 'Nov'):
                            month = 11
                        if (month == 'Dec'):
                            month = 12
                    except:
                        pass
                    c = datetime.datetime(year=int(year), month=int(month), day=int(day))
                    e.thirdlastyear = c
                    #
                    c = html.find(id='ContextDate4')['value']
                    c = c.replace('. ', '')
                    r = len(c) - 9
                    month = c[:r]
                    year = c.replace(month, '')[-4:]
                    day = c.replace(month, '').replace(year, '').replace('. ', '').replace(', ', '').replace(' ', '')
                    try:
                        if (month == 'Jan'):
                            month = 1
                        if (month == 'Feb'):
                            month = 2
                        if (month == 'Mar'):
                            month = 3
                        if (month == 'March'):
                            month = 3
                        if (month == 'April'):
                            month = 4
                        if (month == 'May'):
                            month = 5
                        if (month == 'Jun'):
                            month = 6
                        if (month == 'Jul'):
                            month = 7
                        if (month == 'July'):
                            month = 7
                        if (month == 'Aug'):
                            month = 8
                        if (month == 'Sept'):
                            month = 9
                        if (month == 'Oct'):
                            month = 10
                        if (month == 'Nov'):
                            month = 11
                        if (month == 'Dec'):
                            month = 12
                    except:
                        pass
                    c = datetime.datetime(year=int(year), month=int(month), day=int(day))
                    e.fourthlastyear = c
                    #
                    c = html.find(id='ContextDate5')['value']
                    c = c.replace('. ', '')
                    r = len(c) - 9
                    month = c[:r]
                    year = c.replace(month, '')[-4:]
                    day = c.replace(month, '').replace(year, '').replace('. ', '').replace(', ', '').replace(' ', '')
                    try:
                        if (month == 'Jan'):
                            month = 1
                        if (month == 'Feb'):
                            month = 2
                        if (month == 'Mar'):
                            month = 3
                        if (month == 'March'):
                            month = 3
                        if (month == 'April'):
                            month = 4
                        if (month == 'May'):
                            month = 5
                        if (month == 'Jun'):
                            month = 6
                        if (month == 'Jul'):
                            month = 7
                        if (month == 'July'):
                            month = 7
                        if (month == 'Aug'):
                            month = 8
                        if (month == 'Sept'):
                            month = 9
                        if (month == 'Oct'):
                            month = 10
                        if (month == 'Nov'):
                            month = 11
                        if (month == 'Dec'):
                            month = 12
                    except:
                        pass
                    c = datetime.datetime(year=int(year), month=int(month), day=int(day))
                    e.fifthlastyear = c
                    #
                    c = html.find(id='ContextDate6')['value']
                    c = c.replace('. ', '')
                    r = len(c) - 9
                    month = c[:r]
                    year = c.replace(month, '')[-4:]
                    day = c.replace(month, '').replace(year, '').replace('. ', '').replace(', ', '').replace(' ', '')
                    try:
                        if (month == 'Jan'):
                            month = 1
                        if (month == 'Feb'):
                            month = 2
                        if (month == 'Mar'):
                            month = 3
                        if (month == 'March'):
                            month = 3
                        if (month == 'April'):
                            month = 4
                        if (month == 'May'):
                            month = 5
                        if (month == 'Jun'):
                            month = 6
                        if (month == 'Jul'):
                            month = 7
                        if (month == 'July'):
                            month = 7
                        if (month == 'Aug'):
                            month = 8
                        if (month == 'Sept'):
                            month = 9
                        if (month == 'Oct'):
                            month = 10
                        if (month == 'Nov'):
                            month = 11
                        if (month == 'Dec'):
                            month = 12
                    except:
                        pass
                    c = datetime.datetime(year=int(year), month=int(month), day=int(day))
                    e.sixthlastyear = c
                    #
                    e.month_end = e.lastyear.month
                    #
                    e.amendlastyear = html.find(id='Amend1')['value']
                    e.amendsecondlastyear = html.find(id='Amend2')['value']
                    e.amendthirdlastyear = html.find(id='Amend3')['value']
                    e.amendfourthlastyear = html.find(id='Amend4')['value']
                    e.amendfifthlastyear = html.find(id='Amend5')['value']
                    e.amendsixthlastyear = html.find(id='Amend6')['value']
                    #
                    e.urlbalancesheetlastyear = html.find(id='urlbalancesheet1')['value']
                    e.urlbalancesheetsecondlastyear = html.find(id='urlbalancesheet2')['value']
                    e.urlbalancesheetthirdlastyear = html.find(id='urlbalancesheet3')['value']
                    e.urlbalancesheetfourthlastyear = html.find(id='urlbalancesheet4')['value']
                    e.urlbalancesheetfifthlastyear = html.find(id='urlbalancesheet5')['value']
                    e.urlbalancesheetsixthlastyear = html.find(id='urlbalancesheet6')['value']
                    #
                    e.urlincomestatementlastyear = html.find(id='urlincomestatement1')['value']
                    e.urlincomestatementsecondlastyear = html.find(id='urlincomestatement2')['value']
                    e.urlincomestatementthirdlastyear = html.find(id='urlincomestatement3')['value']
                    e.urlincomestatementfourthlastyear = html.find(id='urlincomestatement4')['value']
                    e.urlincomestatementfifthlastyear = html.find(id='urlincomestatement5')['value']
                    e.urlincomestatementsixthlastyear = html.find(id='urlincomestatement6')['value']
                    #
                    e.urlcomprehensiveincomelastyear = html.find(id='urlcomprehensiveincome1')['value']
                    e.urlcomprehensiveincomesecondlastyear = html.find(id='urlcomprehensiveincome2')['value']
                    e.urlcomprehensiveincomethirdlastyear = html.find(id='urlcomprehensiveincome3')['value']
                    e.urlcomprehensiveincomefourthlastyear = html.find(id='urlcomprehensiveincome4')['value']
                    e.urlcomprehensiveincomefifthlastyear = html.find(id='urlcomprehensiveincome5')['value']
                    e.urlcomprehensiveincomesixthlastyear = html.find(id='urlcomprehensiveincome6')['value']
                    #
                    e.urlshareholdersequitylastyear = html.find(id='urlshareholdersequity1')['value']
                    e.urlshareholdersequitysecondlastyear = html.find(id='urlshareholdersequity2')['value']
                    e.urlshareholdersequitythirdlastyear = html.find(id='urlshareholdersequity3')['value']
                    e.urlshareholdersequityfourthlastyear = html.find(id='urlshareholdersequity4')['value']
                    e.urlshareholdersequityfifthlastyear = html.find(id='urlshareholdersequity5')['value']
                    e.urlshareholdersequitysixthlastyear = html.find(id='urlshareholdersequity6')['value']
                    #
                    e.urlcashflowlastyear = html.find(id='urlcashflow1')['value']
                    e.urlcashflowsecondlastyear = html.find(id='urlcashflow2')['value']
                    e.urlcashflowthirdlastyear = html.find(id='urlcashflow3')['value']
                    e.urlcashflowfourthlastyear = html.find(id='urlcashflow4')['value']
                    e.urlcashflowfifthlastyear = html.find(id='urlcashflow5')['value']
                    e.urlcashflowsixthlastyear = html.find(id='urlcashflow6')['value']
                    #
                    e.save()
                except:
                    pass
                # last year
                try:
                    # last year audit
                    try:
                        try:
                            ad1 = AuditData.objects.get(TradingSymbol=ts, Period='lastyear')
                        except:
                            ad1 = AuditData(TradingSymbol=ts, Period='lastyear')
                        ad1.save()
                        #
                        #
                        # General - Audit
                        #
                        ad1.db = int(html.find(id='Status1')['value'])
                        ad1.AccessionNumber = e.accessionnumberlastyear
                        ad1.AmendmentFlag = e.amendlastyear
                        ad1.EntityRegistrantName = e.EntityRegistrantName
                        ad1.Period = 'lastyear'
                        ad1.PeriodEndDate = e.lastyear
                        ad1.TradingSymbol = ts
                        #
                        #
                        # Balance Sheets - Audit
                        #
                        ad1.CurrentAssets = int(html.find(id='PRO-1.2.21')['value'])
                        ad1.NonCurrentAssets = int(html.find(id='PRO-1.2.51')['value'])
                        ad1.CurrentLiabilities = int(html.find(id='PRO-1.2.81')['value'])
                        ad1.NonCurrentLiabilities = int(html.find(id='PRO-1.2.111')['value'])
                        ad1.ShareholdersEquity = int(html.find(id='PRO-1.2.141')['value'])
                        #ad1.LiabilitiesAndShareholdersEquity = int(html.find(id='PRO-1.1.21')['value'])
                        #
                        ad1.AnomalyCurrentAssets = int(html.find(id='PRO-1.3.11')['value'])
                        #
                        ad1.AnomalyNonCurrentAssets = int(html.find(id='PRO-1.3.21')['value'])
                        #
                        ad1.AnomalyCurrentLiabilities = int(html.find(id='PRO-1.3.31')['value'])
                        #
                        ad1.AnomalyNonCurrentLiabilities = int(html.find(id='PRO-1.3.41')['value'])
                        #
                        ad1.AnomalyShareholdersEquity = int(html.find(id='PRO-1.3.51')['value'])
                        #
                        #
                        # Income Statements - Audit
                        #
                        ad1.GrossMargin = int(html.find(id='PRO-2.1.21')['value'])
                        ad1.OperatingIncome = int(html.find(id='PRO-2.1.51')['value'])
                        ad1.IncomeBeforeTaxes = int(html.find(id='PRO-2.1.81')['value'])
                        ad1.NetIncome = int(html.find(id='PRO-2.1.111')['value'])
                        #
                        ad1.AnomalyGrossMargin = int(html.find(id='PRO-2.2.11')['value'])
                        #
                        ad1.AnomalyOperatingIncome = int(html.find(id='PRO-2.2.21')['value'])
                        #
                        ad1.AnomalyIncomeBeforeTaxes = int(html.find(id='PRO-2.2.31')['value'])
                        #
                        ad1.AnomalyNetIncome = int(html.find(id='PRO-2.2.41')['value'])
                        #
                        #
                        # Comprehensive Income - Audit
                        #
                        ad1.OtherComprehensiveIncome = int(html.find(id='PRO-3.1.21')['value'])
                        #
                        ad1.AnomalyOtherComprehensiveIncome = int(html.find(id='PRO-3.2.11')['value'])
                        #
                        #
                        # Shareholders Equity - Audit
                        #
                        #ad1.ShareholdersEquityBeginning = int(html.find(id='PRO-4.0.21')['value'])
                        #
                        ad1.AnomalyConvertibleDebt = int(html.find(id='PRO-4.2.01')['value'])
                        ad1.AnomalyCommonShares = int(html.find(id='PRO-4.2.11')['value'])
                        ad1.AnomalyRetainedEarnings = int(html.find(id='PRO-4.2.21')['value'])
                        ad1.AnomalyAccumulatedOtherComprehensiveIncome = int(html.find(id='PRO-4.2.31')['value'])
                        ad1.AnomalyTreasuryShares = int(html.find(id='PRO-4.2.41')['value'])
                        ad1.AnomalyEmployeeBenefitTrust = int(html.find(id='PRO-4.2.51')['value'])
                        ad1.AnomalyNonControllingInterests = int(html.find(id='PRO-4.2.61')['value'])
                        #
                        #
                        # Cash Flow - Audit
                        #
                        ad1.CashFlowCashExplainedDifference = int(html.find(id='PRO-5.1.31')['value'])
                        #
                        ad1.AnomalyOperatingActivities = int(html.find(id='PRO-5.2.11')['value'])
                        #
                        ad1.AnomalyInvestingActivities = int(html.find(id='PRO-5.2.21')['value'])
                        #
                        ad1.AnomalyFinancingActivities = int(html.find(id='PRO-5.2.31')['value'])
                        #
                        #
                        # Supplemental - Audit
                        #
                        ad1.TargetWorkingCapital = float(html.find(id='TargetWorkingCapital1')['value'])
                        ad1.ReinvestmentOfMaintenance = int(html.find(id='ReinvestmentOfMaintenance1')['value'])
                        ad1.NormalizedDividendPaymentToNonControllingInterests = int(html.find(id='NormalizedDividendPaymentToNonControllingInterests1')['value'])
                        ad1.NormalizedDividendPaymentToPreferredShareholders = int(html.find(id='NormalizedDividendPaymentToPreferredShareholders1')['value'])
                        ad1.TheoricalInterestRate = float(html.find(id='TheoricalInterestRate1')['value'])
                        ad1.TheoricalTaxRate = float(html.find(id='TheoricalTaxRate1')['value'])
                        ad1.CapitalizationRateFloor = float(html.find(id='CapitalizationRateFloor1')['value'])
                        #
                        ad1.save()
                    except:
                        pass
                    # last year cash flow
                    try:
                        try:
                            cf1 = CashFlow.objects.get(TradingSymbol=ts, Period='lastyear')
                        except:
                            cf1 = CashFlow(TradingSymbol=ts, Period='lastyear')
                        cf1.save()
                        #
                        # General - Cash Flow
                        #
                        cf1.AccessionNumber = e.accessionnumberlastyear
                        cf1.AmendmentFlag = e.amendlastyear
                        cf1.EntityRegistrantName = e.EntityRegistrantName
                        cf1.Period = 'lastyear'
                        cf1.PeriodEndDate = e.lastyear
                        cf1.TradingSymbol = ts
                        #
                        # Cash - Cash Flow
                        #
                        cf1.CashBeginningBalance = int(html.find(id='CashBeginningBalance1')['value'])
                        cf1.EffectOfExchangeRateOnCash = int(html.find(id='EffectOfExchangeRateOnCash1')['value'])
                        #
                        # Operating Activities - Cash Flow
                        #
                        cf1.DepreciationDepletionAndAmortization = int(html.find(id='DepreciationDepletionAndAmortization1')['value'])
                        cf1.GainRelatedToDisposalOrSale = int(html.find(id='GainRelatedToDisposalOrSale1')['value'])
                        cf1.RestructuringAndOtherSpecialCharges = int(html.find(id='RestructuringAndOtherSpecialCharges1')['value'])
                        cf1.AccruedEmployeeCompensation = int(html.find(id='AccruedEmployeeCompensation1')['value'])
                        cf1.ShareBasedCompensation = int(html.find(id='ShareBasedCompensationOperatingActivities1')['value'])
                        cf1.IncreaseDecreaseInIncomeTaxExpenseBenefit = int(html.find(id='IncreaseDecreaseInIncomeTaxExpenseBenefit1')['value'])
                        cf1.OtherNonCashIncomeExpense = int(html.find(id='OtherNonCashIncomeExpense1')['value'])
                        cf1.IncreaseDecreaseInAccountsReceivable = int(html.find(id='IncreaseDecreaseInAccountsReceivable1')['value'])
                        cf1.IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets = int(html.find(id='IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets1')['value'])
                        cf1.IncreaseDecreaseInInventories = int(html.find(id='IncreaseDecreaseInInventories1')['value'])
                        cf1.IncreaseDecreaseInOtherReceivables = int(html.find(id='IncreaseDecreaseInOtherReceivables1')['value'])
                        cf1.IncreaseDecreaseInAccountsPayableAndAccruedLiabilities = int(html.find(id='IncreaseDecreaseInAccountsPayableAndAccruedLiabilities1')['value'])
                        cf1.IncreaseDecreaseInContractWithCustomerLiability = int(html.find(id='IncreaseDecreaseInContractWithCustomerLiability1')['value'])
                        cf1.IncreaseDecreaseInRetirementBenefits = int(html.find(id='IncreaseDecreaseInRetirementBenefits1')['value'])
                        cf1.IncreaseDecreaseFinanceLeaseCurrent = int(html.find(id='IncreaseDecreaseFinanceLeaseCurrent1')['value'])
                        cf1.IncreaseDecreaseOperatingLeaseCurrent = int(html.find(id='IncreaseDecreaseOperatingLeaseCurrent1')['value'])
                        cf1.IncreaseDecreaseInFairValueOfDerivativesOperating = int(html.find(id='IncreaseDecreaseInFairValueOfDerivativesOperating1')['value'])
                        cf1.IncreaseDecreaseInOtherOperatingActivities = int(html.find(id='IncreaseDecreaseInOtherOperatingActivities1')['value'])
                        #
                        # Investing Activities - Cash Flow
                        #
                        cf1.PaymentsToAcquireInvestments = int(html.find(id='PaymentsToAcquireInvestments1')['value'])
                        cf1.ProceedsOfInvestments = int(html.find(id='ProceedsOfInvestments1')['value'])
                        cf1.PaymentsToAcquirePropertyPlantAndEquipment = int(html.find(id='PaymentsToAcquirePropertyPlantAndEquipment1')['value'])
                        cf1.ProceedsFromDisposalsOfPropertyAndEquipment = int(html.find(id='ProceedsFromDisposalsOfPropertyAndEquipment1')['value'])
                        cf1.PaymentsToAcquireBusinessesAndIntangibles = int(html.find(id='PaymentsToAcquireBusinessesAndIntangibles1')['value'])
                        cf1.ProceedsFromDisposalsOfBusinessesAndIntangibles = int(html.find(id='ProceedsFromDisposalsOfBusinessesAndIntangibles1')['value'])
                        cf1.ProceedsRelatedToInsuranceSettlement = int(html.find(id='ProceedsRelatedToInsuranceSettlement1')['value'])
                        cf1.ReveiptOfGovernmentGrants = int(html.find(id='ReveiptOfGovernmentGrants1')['value'])
                        cf1.PaymentOfLicenseFee = int(html.find(id='PaymentOfLicenseFee1')['value'])
                        cf1.InvestingActivitiesInDiscontinuedOperations = int(html.find(id='InvestingActivitiesInDiscontinuedOperations1')['value'])
                        cf1.OtherInvestingActivities = int(html.find(id='OtherInvestingActivities1')['value'])
                        #
                        # Financing Activities - Cash Flow
                        #
                        cf1.FinanceLeasePrincipalPayments = int(html.find(id='FinanceLeasePrincipalPayments1')['value'])
                        cf1.ProceedsFromIssuanceOfCommonShares = int(html.find(id='ProceedsFromIssuanceOfCommonShares1')['value'])
                        cf1.ProceedsFromSharePurchasePlanAndOptionsExercice = int(html.find(id='ProceedsFromSharePurchasePlanAndOptionsExercice1')['value'])
                        cf1.PaymentsRelatedToTaxWithholdingForShareBasedCompensation = int(html.find(id='PaymentsRelatedToTaxWithholdingForShareBasedCompensation1')['value'])
                        cf1.PaymentsForRepurchaseOfCommonShares = int(html.find(id='PaymentsForRepurchaseOfCommonShares1')['value'])
                        cf1.PaymentsOfDividends = int(html.find(id='PaymentsOfDividends1')['value'])
                        cf1.IncreaseDecreaseDeferredContingentConsideration = int(html.find(id='IncreaseDecreaseDeferredContingentConsideration1')['value'])
                        cf1.ProceedsFromIssuanceOfLongTermDebt = int(html.find(id='ProceedsFromIssuanceOfLongTermDebt1')['value'])
                        cf1.RepaymentsOfLongTermDebt = int(html.find(id='RepaymentsOfLongTermDebt1')['value'])
                        cf1.FinancingCosts = int(html.find(id='FinancingCosts1')['value'])
                        cf1.NetChangeInShortTermBorrowings = int(html.find(id='NetChangeInShortTermBorrowings1')['value'])
                        cf1.NetChangeInForwardAndHedgesClassifiedAsFinancingActivities = int(html.find(id='NetChangeInForwardAndHedgesClassifiedAsFinancingActivities1')['value'])
                        cf1.NetChangeInNonControllingInterests = int(html.find(id='NetChangeInNonControllingInterests1')['value'])
                        cf1.ProceedsFromRepaymentsOfCommercialPaper = int(html.find(id='ProceedsFromRepaymentsOfCommercialPaper1')['value'])
                        cf1.RepaymentsOfConvertible = int(html.find(id='RepaymentsOfConvertible1')['value'])
                        cf1.IssuanceOfConvertible = int(html.find(id='IssuanceOfConvertible1')['value'])
                        cf1.EquityInvesteeAdvancesRepayments = int(html.find(id='EquityInvesteeAdvancesRepayments1')['value'])
                        cf1.OtherFinancingActivities = int(html.find(id='OtherFinancingActivities1')['value'])
                        #
                        cf1.save()
                    except:
                        pass
                    # last year trial balance
                    try:
                        try:
                            tb1 = TrialBalance.objects.get(TradingSymbol=ts, Period='lastyear')
                        except:
                            tb1 = TrialBalance(TradingSymbol=ts, Period='lastyear')
                        tb1.save()
                        #
                        # General - Trial Balance
                        #
                        tb1.AccessionNumber = e.accessionnumberlastyear
                        tb1.AmendmentFlag = e.amendlastyear
                        tb1.EntityRegistrantName = e.EntityRegistrantName
                        tb1.Period = 'lastyear'
                        tb1.PeriodEndDate = e.lastyear
                        tb1.TradingSymbol = ts
                        #
                        #
                        # Current Assets - Trial Balance
                        #
                        tb1.Cash = int(html.find(id='TrialBalanceCash1')['value'])
                        tb1.ShortTermInvestments = int(html.find(id='TrialBalanceShortTermInvestments1')['value'])
                        tb1.AccountsReceivable = int(html.find(id='TrialBalanceAccountsReceivable1')['value'])
                        tb1.WorkInProgress = int(html.find(id='TrialBalanceWorkInProgress1')['value'])
                        tb1.Inventories = int(html.find(id='TrialBalanceInventories1')['value'])
                        tb1.PrepaidExpenses = int(html.find(id='TrialBalancePrepaidExpenses1')['value'])
                        tb1.NonTradeReceivables = int(html.find(id='TrialBalanceNonTradeReceivables1')['value'])
                        tb1.PrepaidTaxAssetsCurrent = int(html.find(id='TrialBalancePrepaidTaxAssetsCurrent1')['value'])
                        tb1.DeferredTaxAssetsCurrent = int(html.find(id='TrialBalanceDeferredTaxAssetsCurrent1')['value'])
                        tb1.RightOfUseAssetsCurrent = int(html.find(id='TrialBalanceRightOfUseAssetsCurrent1')['value'])
                        tb1.OtherCurrentAssets = int(html.find(id='TrialBalanceOtherCurrentAssets1')['value'])
                        tb1.DiscontinuedOperationsCurrent = int(html.find(id='TrialBalanceDiscontinuedOperationsCurrent1')['value'])
                        #
                        #
                        # Non-Current Assets - Trial Balance
                        #
                        tb1.LongTermReceivables = int(html.find(id='TrialBalanceLongTermReceivables1')['value'])
                        tb1.DeferredCharges = int(html.find(id='TrialBalanceDeferredCharges1')['value'])
                        tb1.Investments = int(html.find(id='TrialBalanceInvestments1')['value'])
                        tb1.PropertyPlantAndEquipment = int(html.find(id='TrialBalancePropertyPlantAndEquipment1')['value'])
                        tb1.OperatingLeaseRightOfUseAssets = int(html.find(id='TrialBalanceOperatingLeaseRightOfUseAssets1')['value'])
                        tb1.FinanceLeaseRightOfUseAssets = int(html.find(id='TrialBalanceFinanceLeaseRightOfUseAssets1')['value'])
                        tb1.IntangibleAssets = int(html.find(id='TrialBalanceIntangibleAssets1')['value'])
                        tb1.Goodwill = int(html.find(id='TrialBalanceGoodwill1')['value'])
                        tb1.RefundableTaxAssetsNonCurrent = int(html.find(id='TrialBalanceRefundableTaxAssetsNonCurrent1')['value'])
                        tb1.DeferredTaxAssetsNonCurrent = int(html.find(id='TrialBalanceDeferredTaxAssetsNonCurrent1')['value'])
                        tb1.DefinedBenefitPensionAndOtherSimilarPlans = int(html.find(id='TrialBalanceDefinedBenefitPensionAndOtherSimilarPlans1')['value'])
                        tb1.OtherNonCurrentAssets = int(html.find(id='TrialBalanceOtherNonCurrentAssets1')['value'])
                        tb1.DiscontinuedOperations = int(html.find(id='TrialBalanceDiscontinuedOperations1')['value'])
                        #
                        #
                        # Current Liabilities - Trial Balance
                        #
                        tb1.AccountsPayableAndAccruedLiabilities = int(html.find(id='TrialBalanceAccountsPayableAndAccruedLiabilities1')['value'])
                        tb1.EmployeeCompensationCurrent = int(html.find(id='TrialBalanceEmployeeCompensationCurrent1')['value'])
                        tb1.OperatingLeasesCurrent = int(html.find(id='TrialBalanceOperatingLeasesCurrent1')['value'])
                        tb1.FinanceLeasesCurrent = int(html.find(id='TrialBalanceFinanceLeasesCurrent1')['value'])
                        tb1.DeferredRevenueAndDepositsCurrent = int(html.find(id='TrialBalanceDeferredRevenueAndDepositsCurrent1')['value'])
                        tb1.AccruedTaxLiabilities = int(html.find(id='TrialBalanceAccruedTaxLiabilities1')['value'])
                        tb1.DeferredTaxLiabilitiesCurrent = int(html.find(id='TrialBalanceDeferredTaxLiabilitiesCurrent1')['value'])
                        tb1.CommercialPapers = int(html.find(id='TrialBalanceCommercialPapers1')['value'])
                        tb1.ShortTermBorrowings = int(html.find(id='TrialBalanceShortTermBorrowings1')['value'])
                        tb1.OtherCurrentLiabilities = int(html.find(id='TrialBalanceOtherCurrentLiabilities1')['value'])
                        tb1.DiscontinuedOperationsLiabilitiesCurrent = int(html.find(id='TrialBalanceDiscontinuedOperationsLiabilitiesCurrent1')['value'])
                        tb1.DividendsPayable = int(html.find(id='TrialBalanceDividendsPayable1')['value'])
                        tb1.ShortTermPortionOfLongTermDebt = int(html.find(id='TrialBalanceShortTermPortionOfLongTermDebt1')['value'])
                        #
                        #
                        # Non-Current Liabilities - Trial Balance
                        #
                        tb1.LongTermDebt = int(html.find(id='TrialBalanceLongTermDebt1')['value'])
                        tb1.PreferredSharesLiability = int(html.find(id='TrialBalancePreferredSharesLiability1')['value'])
                        tb1.RetirementBenefits = int(html.find(id='TrialBalanceRetirementBenefits1')['value'])
                        tb1.OperatingLeasesNonCurrent = int(html.find(id='TrialBalanceOperatingLeasesNonCurrent1')['value'])
                        tb1.FinanceLeasesNonCurrent = int(html.find(id='TrialBalanceFinanceLeasesNonCurrent1')['value'])
                        tb1.LeaseIncentiveObligation = int(html.find(id='TrialBalanceLeaseIncentiveObligation1')['value'])
                        tb1.DeferredRevenueAndDepositsNonCurrent = int(html.find(id='TrialBalanceDeferredRevenueAndDepositsNonCurrent1')['value'])
                        tb1.ContingentConsideration = int(html.find(id='TrialBalanceContingentConsideration1')['value'])
                        tb1.AccruedTaxLiabilitiesNonCurrent = int(html.find(id='TrialBalanceAccruedTaxLiabilitiesNonCurrent1')['value'])
                        tb1.DeferredTaxLiabilitiesNonCurrent = int(html.find(id='TrialBalanceDeferredTaxLiabilitiesNonCurrent1')['value'])
                        tb1.OtherNonCurrentLiabilities = int(html.find(id='TrialBalanceOtherNonCurrentLiabilities1')['value'])
                        tb1.RedeemableNonControllingInterests = int(html.find(id='TrialBalanceRedeemableNonControllingInterests1')['value'])
                        tb1.DiscontinuedOperationsLiabilitiesNonCurrent = int(html.find(id='TrialBalanceDiscontinuedOperationsLiabilitiesNonCurrent1')['value'])
                        #
                        #
                        # Shareholders Equity - Trial Balance
                        #
                        # convertible debt
                        tb1.ConvertibleDebtBeginning = int(html.find(id='TrialBalanceConvertibleDebt1')['value'])
                        #
                        # common shares
                        tb1.CommonSharesBeginning = int(html.find(id='TrialBalanceCommonShares1')['value'])
                        tb1.CommonSharesIssued = int(html.find(id='TrialBalanceCommonSharesIssued1')['value'])
                        tb1.ShareBasedCompensation = int(html.find(id='TrialBalanceShareBasedCompensation1')['value'])
                        #
                        # preferred shares
                        try:
                            tb1.PreferredSharesBeginning = int(html.find(id='TrialBalancePreferredShares1')['value'])
                        except:
                            pass
                        #
                        # retained earnings
                        tb1.RetainedEarningsBeginning = int(html.find(id='TrialBalanceRetainedEarningsAccumulatedDeficit1')['value'])
                        tb1.DividendsAndDividendEquivalentsDeclared = int(html.find(id='TrialBalanceDividendsAndDividendEquivalentsDeclared1')['value'])
                        tb1.CommonSharesRepurchasedAndRetired = int(html.find(id='TrialBalanceCommonSharesRepurchasedAndRetired1')['value'])
                        tb1.ShareBasedCompensationRetainedEarnings = int(html.find(id='TrialBalanceShareBasedCompensationRetainedEarnings1')['value'])
                        tb1.EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts = int(html.find(id='TrialBalanceEffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts1')['value'])
                        tb1.RetainedEarningsOthers = int(html.find(id='TrialBalanceRetainedEarningsOthers1')['value'])
                        #
                        # accumulated other comprehensive income
                        tb1.AccumulatedOtherComprehensiveIncomeBeginning = int(html.find(id='TrialBalanceAccumulatedOtherComprehensiveIncomeLoss1')['value'])
                        #
                        # treasury shares
                        tb1.TreasurySharesBeginning = int(html.find(id='TrialBalanceTreasuryShares1')['value'])
                        tb1.PurchaseAndSellOfTreasuryShares = int(html.find(id='TrialBalancePurchaseAndSellOfTreasuryShares1')['value'])
                        #
                        # employee benefit trust
                        tb1.EmployeeBenefitTrustBeginning = int(html.find(id='TrialBalanceEmployeeBenefitTrust1')['value'])
                        #
                        # non controlling interests
                        tb1.NonControllingInterestsBeginning = int(html.find(id='TrialBalanceNonControllingInterests1')['value'])
                        tb1.DividendsDeclaredToNonControllingInterests = int(html.find(id='TrialBalanceDividendsDeclaredToNonControllingInterests1')['value'])
                        tb1.AcquisitionOfNonControllingInterests = int(html.find(id='TrialBalanceAcquisitionOfNonControllingInterests1')['value'])
                        tb1.NonControllingInterestsOthers = int(html.find(id='TrialBalanceNonControllingInterestsOthers1')['value'])
                        #
                        #
                        # Income Statements - Trial Balance
                        #
                        tb1.Sales = int(html.find(id='TrialBalanceSales1')['value'])
                        tb1.CostOfSales = int(html.find(id='TrialBalanceCostOfSales1')['value'])
                        tb1.ResearchAndDevelopment = int(html.find(id='TrialBalanceResearchAndDevelopment1')['value'])
                        tb1.SellingGeneralAdministrativeAndMarketing = int(html.find(id='TrialBalanceSellingGeneralAdministrativeAndMarketing1')['value'])
                        tb1.ImpairmentRestructuringAndOtherSpecialCharges = int(html.find(id='TrialBalanceImpairmentRestructuringAndOtherSpecialCharges1')['value'])
                        tb1.NonOperatingIncome = int(html.find(id='TrialBalanceNonOperatingIncomeExpense1')['value'])
                        tb1.IncomeTaxExpenseBenefit = int(html.find(id='TrialBalanceIncomeTaxExpenseBenefit1')['value'])
                        tb1.EquityMethodInvesteesIncome = int(html.find(id='TrialBalanceEquityMethodInvesteesIncome1')['value'])
                        tb1.NetIncomeFromDiscontinuedOperations = int(html.find(id='TrialBalanceNetIncomeFromDiscontinuedOperations1')['value'])
                        #
                        #
                        # Other Comprehensive Income - Trial Balance
                        #
                        tb1.ChangeInForeignCurrencyTranslationAdjustment = int(html.find(id='TrialBalanceChangeInForeignCurrencyTranslationAdjustment1')['value'])
                        tb1.ChangeInUnrealizedGainsLossesOnDerivativeInstruments = int(html.find(id='TrialBalanceChangeInUnrealizedGainsLossesOnDerivativeInstruments1')['value'])
                        tb1.ChangeInUnrealizedGainsLossesOnInvestments = int(html.find(id='TrialBalanceChangeInUnrealizedGainsLossesOnInvestments1')['value'])
                        tb1.ChangeInDefinedBenefitPensionAndOtherSimilarPlans = int(html.find(id='TrialBalanceChangeInDefinedBenefitPensionAndOtherSimilarPlans1')['value'])
                        tb1.IncomeTaxOnOtherComprehensiveIncome = int(html.find(id='TrialBalanceIncomeTaxOnOtherComprehensiveIncome1')['value'])
                        #
                        tb1.save()
                    except:
                        pass
                except:
                    pass
                # second last year
                try:
                    # second last year audit
                    try:
                        try:
                            ad2 = AuditData.objects.get(TradingSymbol=ts, Period='secondlastyear')
                        except:
                            ad2 = AuditData(TradingSymbol=ts, Period='secondlastyear')
                        ad2.save()
                        #
                        # General - Audit
                        #
                        ad2.db = int(html.find(id='Status2')['value'])
                        ad2.AccessionNumber = e.accessionnumbersecondlastyear
                        ad2.AmendmentFlag = e.amendsecondlastyear
                        ad2.EntityRegistrantName = e.EntityRegistrantName
                        ad2.Period = 'secondlastyear'
                        ad2.PeriodEndDate = e.secondlastyear
                        ad2.TradingSymbol = ts
                        #
                        # Balance Sheets - Audit
                        #
                        ad2.CurrentAssets = int(html.find(id='PRO-1.2.22')['value'])
                        ad2.NonCurrentAssets = int(html.find(id='PRO-1.2.52')['value'])
                        ad2.CurrentLiabilities = int(html.find(id='PRO-1.2.82')['value'])
                        ad2.NonCurrentLiabilities = int(html.find(id='PRO-1.2.112')['value'])
                        ad2.ShareholdersEquity = int(html.find(id='PRO-1.2.142')['value'])
                        #ad2.LiabilitiesAndShareholdersEquity = int(html.find(id='PRO-1.1.22')['value'])
                        #
                        ad2.AnomalyCurrentAssets = int(html.find(id='PRO-1.3.12')['value'])
                        #
                        ad2.AnomalyNonCurrentAssets = int(html.find(id='PRO-1.3.22')['value'])
                        #
                        ad2.AnomalyCurrentLiabilities = int(html.find(id='PRO-1.3.32')['value'])
                        #
                        ad2.AnomalyNonCurrentLiabilities = int(html.find(id='PRO-1.3.42')['value'])
                        #
                        ad2.AnomalyShareholdersEquity = int(html.find(id='PRO-1.3.52')['value'])
                        #
                        #
                        # Income Statements - Audit
                        #
                        ad2.GrossMargin = int(html.find(id='PRO-2.1.22')['value'])
                        ad2.OperatingIncome = int(html.find(id='PRO-2.1.52')['value'])
                        ad2.IncomeBeforeTaxes = int(html.find(id='PRO-2.1.82')['value'])
                        ad2.NetIncome = int(html.find(id='PRO-2.1.112')['value'])
                        #
                        ad2.AnomalyGrossMargin = int(html.find(id='PRO-2.2.12')['value'])
                        #
                        ad2.AnomalyOperatingIncome = int(html.find(id='PRO-2.2.22')['value'])
                        #
                        ad2.AnomalyIncomeBeforeTaxes = int(html.find(id='PRO-2.2.32')['value'])
                        #
                        ad2.AnomalyNetIncome = int(html.find(id='PRO-2.2.42')['value'])
                        #
                        #
                        # Comprehensive Income - Audit
                        #
                        ad2.OtherComprehensiveIncome = int(html.find(id='PRO-3.1.22')['value'])
                        #
                        ad2.AnomalyOtherComprehensiveIncome = int(html.find(id='PRO-3.2.12')['value'])
                        #
                        #
                        # Shareholders Equity - Audit
                        #
                        #ad2.ShareholdersEquityBeginning = int(html.find(id='PRO-4.0.22')['value'])
                        #
                        ad2.AnomalyConvertibleDebt = int(html.find(id='PRO-4.2.02')['value'])
                        ad2.AnomalyCommonShares = int(html.find(id='PRO-4.2.12')['value'])
                        ad2.AnomalyRetainedEarnings = int(html.find(id='PRO-4.2.22')['value'])
                        ad2.AnomalyAccumulatedOtherComprehensiveIncome = int(html.find(id='PRO-4.2.32')['value'])
                        ad2.AnomalyTreasuryShares = int(html.find(id='PRO-4.2.42')['value'])
                        ad2.AnomalyEmployeeBenefitTrust = int(html.find(id='PRO-4.2.52')['value'])
                        ad2.AnomalyNonControllingInterests = int(html.find(id='PRO-4.2.62')['value'])
                        #
                        #
                        # Cash Flow - Audit
                        #
                        ad2.CashFlowCashExplainedDifference = int(html.find(id='PRO-5.1.32')['value'])
                        #
                        ad2.AnomalyOperatingActivities = int(html.find(id='PRO-5.2.12')['value'])
                        #
                        ad2.AnomalyInvestingActivities = int(html.find(id='PRO-5.2.22')['value'])
                        #
                        ad2.AnomalyFinancingActivities = int(html.find(id='PRO-5.2.32')['value'])
                        #
                        #
                        # Supplemental - Audit
                        #
                        ad2.TargetWorkingCapital = float(html.find(id='TargetWorkingCapital2')['value'])
                        ad2.ReinvestmentOfMaintenance = int(html.find(id='ReinvestmentOfMaintenance2')['value'])
                        ad2.NormalizedDividendPaymentToNonControllingInterests = int(html.find(id='NormalizedDividendPaymentToNonControllingInterests2')['value'])
                        ad2.NormalizedDividendPaymentToPreferredShareholders = int(html.find(id='NormalizedDividendPaymentToPreferredShareholders2')['value'])
                        ad2.TheoricalInterestRate = float(html.find(id='TheoricalInterestRate2')['value'])
                        ad2.TheoricalTaxRate = float(html.find(id='TheoricalTaxRate2')['value'])
                        ad2.CapitalizationRateFloor = float(html.find(id='CapitalizationRateFloor2')['value'])
                        #
                        ad2.save()
                    except:
                        pass
                    # second last year cash flow
                    try:
                        try:
                            cf2 = CashFlow.objects.get(TradingSymbol=ts, Period='secondlastyear')
                        except:
                            cf2 = CashFlow(TradingSymbol=ts, Period='secondlastyear')
                        cf2.save()
                        #
                        # General - Cash Flow
                        #
                        cf2.AccessionNumber = e.accessionnumbersecondlastyear
                        cf2.AmendmentFlag = e.amendsecondlastyear
                        cf2.EntityRegistrantName = e.EntityRegistrantName
                        cf2.Period = 'secondlastyear'
                        cf2.PeriodEndDate = e.secondlastyear
                        cf2.TradingSymbol = ts
                        #
                        # Cash - Cash Flow
                        #
                        cf2.CashBeginningBalance = int(html.find(id='CashBeginningBalance2')['value'])
                        cf2.EffectOfExchangeRateOnCash = int(html.find(id='EffectOfExchangeRateOnCash2')['value'])
                        #
                        # Operating Activities - Cash Flow
                        #
                        cf2.DepreciationDepletionAndAmortization = int(html.find(id='DepreciationDepletionAndAmortization2')['value'])
                        cf2.GainRelatedToDisposalOrSale = int(html.find(id='GainRelatedToDisposalOrSale2')['value'])
                        cf2.RestructuringAndOtherSpecialCharges = int(html.find(id='RestructuringAndOtherSpecialCharges2')['value'])
                        cf2.AccruedEmployeeCompensation = int(html.find(id='AccruedEmployeeCompensation2')['value'])
                        cf2.ShareBasedCompensation = int(html.find(id='ShareBasedCompensationOperatingActivities2')['value'])
                        cf2.IncreaseDecreaseInIncomeTaxExpenseBenefit = int(html.find(id='IncreaseDecreaseInIncomeTaxExpenseBenefit2')['value'])
                        cf2.OtherNonCashIncomeExpense = int(html.find(id='OtherNonCashIncomeExpense2')['value'])
                        cf2.IncreaseDecreaseInAccountsReceivable = int(html.find(id='IncreaseDecreaseInAccountsReceivable2')['value'])
                        cf2.IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets = int(html.find(id='IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets2')['value'])
                        cf2.IncreaseDecreaseInInventories = int(html.find(id='IncreaseDecreaseInInventories2')['value'])
                        cf2.IncreaseDecreaseInOtherReceivables = int(html.find(id='IncreaseDecreaseInOtherReceivables2')['value'])
                        cf2.IncreaseDecreaseInAccountsPayableAndAccruedLiabilities = int(html.find(id='IncreaseDecreaseInAccountsPayableAndAccruedLiabilities2')['value'])
                        cf2.IncreaseDecreaseInContractWithCustomerLiability = int(html.find(id='IncreaseDecreaseInContractWithCustomerLiability2')['value'])
                        cf2.IncreaseDecreaseInRetirementBenefits = int(html.find(id='IncreaseDecreaseInRetirementBenefits2')['value'])
                        cf2.IncreaseDecreaseFinanceLeaseCurrent = int(html.find(id='IncreaseDecreaseFinanceLeaseCurrent2')['value'])
                        cf2.IncreaseDecreaseOperatingLeaseCurrent = int(html.find(id='IncreaseDecreaseOperatingLeaseCurrent2')['value'])
                        cf2.IncreaseDecreaseInFairValueOfDerivativesOperating = int(html.find(id='IncreaseDecreaseInFairValueOfDerivativesOperating2')['value'])
                        cf2.IncreaseDecreaseInOtherOperatingActivities = int(html.find(id='IncreaseDecreaseInOtherOperatingActivities2')['value'])
                        #
                        # Investing Activities - Cash Flow
                        #
                        cf2.PaymentsToAcquireInvestments = int(html.find(id='PaymentsToAcquireInvestments2')['value'])
                        cf2.ProceedsOfInvestments = int(html.find(id='ProceedsOfInvestments2')['value'])
                        cf2.PaymentsToAcquirePropertyPlantAndEquipment = int(html.find(id='PaymentsToAcquirePropertyPlantAndEquipment2')['value'])
                        cf2.ProceedsFromDisposalsOfPropertyAndEquipment = int(html.find(id='ProceedsFromDisposalsOfPropertyAndEquipment2')['value'])
                        cf2.PaymentsToAcquireBusinessesAndIntangibles = int(html.find(id='PaymentsToAcquireBusinessesAndIntangibles2')['value'])
                        cf2.ProceedsFromDisposalsOfBusinessesAndIntangibles = int(html.find(id='ProceedsFromDisposalsOfBusinessesAndIntangibles2')['value'])
                        cf2.ProceedsRelatedToInsuranceSettlement = int(html.find(id='ProceedsRelatedToInsuranceSettlement2')['value'])
                        cf2.ReveiptOfGovernmentGrants = int(html.find(id='ReveiptOfGovernmentGrants2')['value'])
                        cf2.PaymentOfLicenseFee = int(html.find(id='PaymentOfLicenseFee2')['value'])
                        cf2.InvestingActivitiesInDiscontinuedOperations = int(html.find(id='InvestingActivitiesInDiscontinuedOperations2')['value'])
                        cf2.OtherInvestingActivities = int(html.find(id='OtherInvestingActivities2')['value'])
                        #
                        # Financing Activities - Cash Flow
                        #
                        cf2.FinanceLeasePrincipalPayments = int(html.find(id='FinanceLeasePrincipalPayments2')['value'])
                        cf2.ProceedsFromIssuanceOfCommonShares = int(html.find(id='ProceedsFromIssuanceOfCommonShares2')['value'])
                        cf2.ProceedsFromSharePurchasePlanAndOptionsExercice = int(html.find(id='ProceedsFromSharePurchasePlanAndOptionsExercice2')['value'])
                        cf2.PaymentsRelatedToTaxWithholdingForShareBasedCompensation = int(html.find(id='PaymentsRelatedToTaxWithholdingForShareBasedCompensation2')['value'])
                        cf2.PaymentsForRepurchaseOfCommonShares = int(html.find(id='PaymentsForRepurchaseOfCommonShares2')['value'])
                        cf2.PaymentsOfDividends = int(html.find(id='PaymentsOfDividends2')['value'])
                        cf2.IncreaseDecreaseDeferredContingentConsideration = int(html.find(id='IncreaseDecreaseDeferredContingentConsideration2')['value'])
                        cf2.ProceedsFromIssuanceOfLongTermDebt = int(html.find(id='ProceedsFromIssuanceOfLongTermDebt2')['value'])
                        cf2.RepaymentsOfLongTermDebt = int(html.find(id='RepaymentsOfLongTermDebt2')['value'])
                        cf2.FinancingCosts = int(html.find(id='FinancingCosts2')['value'])
                        cf2.NetChangeInShortTermBorrowings = int(html.find(id='NetChangeInShortTermBorrowings2')['value'])
                        cf2.NetChangeInForwardAndHedgesClassifiedAsFinancingActivities = int(html.find(id='NetChangeInForwardAndHedgesClassifiedAsFinancingActivities2')['value'])
                        cf2.NetChangeInNonControllingInterests = int(html.find(id='NetChangeInNonControllingInterests2')['value'])
                        cf2.ProceedsFromRepaymentsOfCommercialPaper = int(html.find(id='ProceedsFromRepaymentsOfCommercialPaper2')['value'])
                        cf2.RepaymentsOfConvertible = int(html.find(id='RepaymentsOfConvertible2')['value'])
                        cf2.IssuanceOfConvertible = int(html.find(id='IssuanceOfConvertible2')['value'])
                        cf2.EquityInvesteeAdvancesRepayments = int(html.find(id='EquityInvesteeAdvancesRepayments2')['value'])
                        cf2.OtherFinancingActivities = int(html.find(id='OtherFinancingActivities2')['value'])
                        #
                        cf2.save()
                    except:
                        pass
                    # second last year trial balance
                    try:
                        try:
                            tb2 = TrialBalance.objects.get(TradingSymbol=ts, Period='secondlastyear')
                        except:
                            tb2 = TrialBalance(TradingSymbol=ts, Period='secondlastyear')
                        tb2.save()
                        #
                        # General - Trial Balance
                        #
                        tb2.AccessionNumber = e.accessionnumbersecondlastyear
                        tb2.AmendmentFlag = e.amendsecondlastyear
                        tb2.EntityRegistrantName = e.EntityRegistrantName
                        tb2.Period = 'secondlastyear'
                        tb2.PeriodEndDate = e.secondlastyear
                        tb2.TradingSymbol = ts
                        #
                        #
                        # Current Assets - Trial Balance
                        #
                        tb2.Cash = int(html.find(id='TrialBalanceCash2')['value'])
                        tb2.ShortTermInvestments = int(html.find(id='TrialBalanceShortTermInvestments2')['value'])
                        tb2.AccountsReceivable = int(html.find(id='TrialBalanceAccountsReceivable2')['value'])
                        tb2.WorkInProgress = int(html.find(id='TrialBalanceWorkInProgress2')['value'])
                        tb2.Inventories = int(html.find(id='TrialBalanceInventories2')['value'])
                        tb2.PrepaidExpenses = int(html.find(id='TrialBalancePrepaidExpenses2')['value'])
                        tb2.NonTradeReceivables = int(html.find(id='TrialBalanceNonTradeReceivables2')['value'])
                        tb2.PrepaidTaxAssetsCurrent = int(html.find(id='TrialBalancePrepaidTaxAssetsCurrent2')['value'])
                        tb2.DeferredTaxAssetsCurrent = int(html.find(id='TrialBalanceDeferredTaxAssetsCurrent2')['value'])
                        tb2.RightOfUseAssetsCurrent = int(html.find(id='TrialBalanceRightOfUseAssetsCurrent2')['value'])
                        tb2.OtherCurrentAssets = int(html.find(id='TrialBalanceOtherCurrentAssets2')['value'])
                        tb2.DiscontinuedOperationsCurrent = int(html.find(id='TrialBalanceDiscontinuedOperationsCurrent2')['value'])
                        #
                        #
                        # Non-Current Assets - Trial Balance
                        #
                        tb2.LongTermReceivables = int(html.find(id='TrialBalanceLongTermReceivables2')['value'])
                        tb2.DeferredCharges = int(html.find(id='TrialBalanceDeferredCharges2')['value'])
                        tb2.Investments = int(html.find(id='TrialBalanceInvestments2')['value'])
                        tb2.PropertyPlantAndEquipment = int(html.find(id='TrialBalancePropertyPlantAndEquipment2')['value'])
                        tb2.OperatingLeaseRightOfUseAssets = int(html.find(id='TrialBalanceOperatingLeaseRightOfUseAssets2')['value'])
                        tb2.FinanceLeaseRightOfUseAssets = int(html.find(id='TrialBalanceFinanceLeaseRightOfUseAssets2')['value'])
                        tb2.IntangibleAssets = int(html.find(id='TrialBalanceIntangibleAssets2')['value'])
                        tb2.Goodwill = int(html.find(id='TrialBalanceGoodwill2')['value'])
                        tb2.RefundableTaxAssetsNonCurrent = int(html.find(id='TrialBalanceRefundableTaxAssetsNonCurrent2')['value'])
                        tb2.DeferredTaxAssetsNonCurrent = int(html.find(id='TrialBalanceDeferredTaxAssetsNonCurrent2')['value'])
                        tb2.DefinedBenefitPensionAndOtherSimilarPlans = int(html.find(id='TrialBalanceDefinedBenefitPensionAndOtherSimilarPlans2')['value'])
                        tb2.OtherNonCurrentAssets = int(html.find(id='TrialBalanceOtherNonCurrentAssets2')['value'])
                        tb2.DiscontinuedOperations = int(html.find(id='TrialBalanceDiscontinuedOperations2')['value'])
                        #
                        #
                        # Current Liabilities - Trial Balance
                        #
                        tb2.AccountsPayableAndAccruedLiabilities = int(html.find(id='TrialBalanceAccountsPayableAndAccruedLiabilities2')['value'])
                        tb2.EmployeeCompensationCurrent = int(html.find(id='TrialBalanceEmployeeCompensationCurrent2')['value'])
                        tb2.OperatingLeasesCurrent = int(html.find(id='TrialBalanceOperatingLeasesCurrent2')['value'])
                        tb2.FinanceLeasesCurrent = int(html.find(id='TrialBalanceFinanceLeasesCurrent2')['value'])
                        tb2.DeferredRevenueAndDepositsCurrent = int(html.find(id='TrialBalanceDeferredRevenueAndDepositsCurrent2')['value'])
                        tb2.AccruedTaxLiabilities = int(html.find(id='TrialBalanceAccruedTaxLiabilities2')['value'])
                        tb2.DeferredTaxLiabilitiesCurrent = int(html.find(id='TrialBalanceDeferredTaxLiabilitiesCurrent2')['value'])
                        tb2.CommercialPapers = int(html.find(id='TrialBalanceCommercialPapers2')['value'])
                        tb2.ShortTermBorrowings = int(html.find(id='TrialBalanceShortTermBorrowings2')['value'])
                        tb2.OtherCurrentLiabilities = int(html.find(id='TrialBalanceOtherCurrentLiabilities2')['value'])
                        tb2.DiscontinuedOperationsLiabilitiesCurrent = int(html.find(id='TrialBalanceDiscontinuedOperationsLiabilitiesCurrent2')['value'])
                        tb2.DividendsPayable = int(html.find(id='TrialBalanceDividendsPayable2')['value'])
                        tb2.ShortTermPortionOfLongTermDebt = int(html.find(id='TrialBalanceShortTermPortionOfLongTermDebt2')['value'])
                        #
                        #
                        # Non-Current Liabilities - Trial Balance
                        #
                        tb2.LongTermDebt = int(html.find(id='TrialBalanceLongTermDebt2')['value'])
                        tb2.PreferredSharesLiability = int(html.find(id='TrialBalancePreferredSharesLiability2')['value'])
                        tb2.RetirementBenefits = int(html.find(id='TrialBalanceRetirementBenefits2')['value'])
                        tb2.OperatingLeasesNonCurrent = int(html.find(id='TrialBalanceOperatingLeasesNonCurrent2')['value'])
                        tb2.FinanceLeasesNonCurrent = int(html.find(id='TrialBalanceFinanceLeasesNonCurrent2')['value'])
                        tb2.LeaseIncentiveObligation = int(html.find(id='TrialBalanceLeaseIncentiveObligation2')['value'])
                        tb2.DeferredRevenueAndDepositsNonCurrent = int(html.find(id='TrialBalanceDeferredRevenueAndDepositsNonCurrent2')['value'])
                        tb2.ContingentConsideration = int(html.find(id='TrialBalanceContingentConsideration2')['value'])
                        tb2.AccruedTaxLiabilitiesNonCurrent = int(html.find(id='TrialBalanceAccruedTaxLiabilitiesNonCurrent2')['value'])
                        tb2.DeferredTaxLiabilitiesNonCurrent = int(html.find(id='TrialBalanceDeferredTaxLiabilitiesNonCurrent2')['value'])
                        tb2.OtherNonCurrentLiabilities = int(html.find(id='TrialBalanceOtherNonCurrentLiabilities2')['value'])
                        tb2.RedeemableNonControllingInterests = int(html.find(id='TrialBalanceRedeemableNonControllingInterests2')['value'])
                        tb2.DiscontinuedOperationsLiabilitiesNonCurrent = int(html.find(id='TrialBalanceDiscontinuedOperationsLiabilitiesNonCurrent2')['value'])
                        #
                        #
                        # Shareholders Equity - Trial Balance
                        #
                        # convertible debt
                        tb2.ConvertibleDebtBeginning = int(html.find(id='TrialBalanceConvertibleDebt2')['value'])
                        #
                        # common shares
                        tb2.CommonSharesBeginning = int(html.find(id='TrialBalanceCommonShares2')['value'])
                        tb2.CommonSharesIssued = int(html.find(id='TrialBalanceCommonSharesIssued2')['value'])
                        tb2.ShareBasedCompensation = int(html.find(id='TrialBalanceShareBasedCompensation2')['value'])
                        #
                        # preferred shares
                        try:
                            tb2.PreferredSharesBeginning = int(html.find(id='TrialBalancePreferredShares2')['value'])
                        except:
                            pass
                        #
                        # retained earnings
                        tb2.RetainedEarningsBeginning = int(html.find(id='TrialBalanceRetainedEarningsAccumulatedDeficit2')['value'])
                        tb2.DividendsAndDividendEquivalentsDeclared = int(html.find(id='TrialBalanceDividendsAndDividendEquivalentsDeclared2')['value'])
                        tb2.CommonSharesRepurchasedAndRetired = int(html.find(id='TrialBalanceCommonSharesRepurchasedAndRetired2')['value'])
                        tb2.ShareBasedCompensationRetainedEarnings = int(html.find(id='TrialBalanceShareBasedCompensationRetainedEarnings2')['value'])
                        tb2.EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts = int(html.find(id='TrialBalanceEffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts2')['value'])
                        tb2.RetainedEarningsOthers = int(html.find(id='TrialBalanceRetainedEarningsOthers2')['value'])
                        #
                        # accumulated other comprehensive income
                        tb2.AccumulatedOtherComprehensiveIncomeBeginning = int(html.find(id='TrialBalanceAccumulatedOtherComprehensiveIncomeLoss2')['value'])
                        #
                        # treasury shares
                        tb2.TreasurySharesBeginning = int(html.find(id='TrialBalanceTreasuryShares2')['value'])
                        tb2.PurchaseAndSellOfTreasuryShares = int(html.find(id='TrialBalancePurchaseAndSellOfTreasuryShares2')['value'])
                        #
                        # employee benefit trust
                        tb2.EmployeeBenefitTrustBeginning = int(html.find(id='TrialBalanceEmployeeBenefitTrust2')['value'])
                        #
                        # non controlling interests
                        tb2.NonControllingInterestsBeginning = int(html.find(id='TrialBalanceNonControllingInterests2')['value'])
                        tb2.DividendsDeclaredToNonControllingInterests = int(html.find(id='TrialBalanceDividendsDeclaredToNonControllingInterests2')['value'])
                        tb2.AcquisitionOfNonControllingInterests = int(html.find(id='TrialBalanceAcquisitionOfNonControllingInterests2')['value'])
                        tb2.NonControllingInterestsOthers = int(html.find(id='TrialBalanceNonControllingInterestsOthers2')['value'])
                        #
                        #
                        # Income Statements - Trial Balance
                        #
                        tb2.Sales = int(html.find(id='TrialBalanceSales2')['value'])
                        tb2.CostOfSales = int(html.find(id='TrialBalanceCostOfSales2')['value'])
                        tb2.ResearchAndDevelopment = int(html.find(id='TrialBalanceResearchAndDevelopment2')['value'])
                        tb2.SellingGeneralAdministrativeAndMarketing = int(html.find(id='TrialBalanceSellingGeneralAdministrativeAndMarketing2')['value'])
                        tb2.ImpairmentRestructuringAndOtherSpecialCharges = int(html.find(id='TrialBalanceImpairmentRestructuringAndOtherSpecialCharges2')['value'])
                        tb2.NonOperatingIncome = int(html.find(id='TrialBalanceNonOperatingIncomeExpense2')['value'])
                        tb2.IncomeTaxExpenseBenefit = int(html.find(id='TrialBalanceIncomeTaxExpenseBenefit2')['value'])
                        tb2.EquityMethodInvesteesIncome = int(html.find(id='TrialBalanceEquityMethodInvesteesIncome2')['value'])
                        tb2.NetIncomeFromDiscontinuedOperations = int(html.find(id='TrialBalanceNetIncomeFromDiscontinuedOperations2')['value'])
                        #
                        #
                        # Other Comprehensive Income - Trial Balance
                        #
                        tb2.ChangeInForeignCurrencyTranslationAdjustment = int(html.find(id='TrialBalanceChangeInForeignCurrencyTranslationAdjustment2')['value'])
                        tb2.ChangeInUnrealizedGainsLossesOnDerivativeInstruments = int(html.find(id='TrialBalanceChangeInUnrealizedGainsLossesOnDerivativeInstruments2')['value'])
                        tb2.ChangeInUnrealizedGainsLossesOnInvestments = int(html.find(id='TrialBalanceChangeInUnrealizedGainsLossesOnInvestments2')['value'])
                        tb2.ChangeInDefinedBenefitPensionAndOtherSimilarPlans = int(html.find(id='TrialBalanceChangeInDefinedBenefitPensionAndOtherSimilarPlans2')['value'])
                        tb2.IncomeTaxOnOtherComprehensiveIncome = int(html.find(id='TrialBalanceIncomeTaxOnOtherComprehensiveIncome2')['value'])
                        #
                        tb2.save()
                    except:
                        pass
                except:
                    pass
                # third last year
                try:
                    # third last year audit
                    try:
                        try:
                            ad3 = AuditData.objects.get(TradingSymbol=ts, Period='thirdlastyear')
                        except:
                            ad3 = AuditData(TradingSymbol=ts, Period='thirdlastyear')
                        ad3.save()
                        #
                        # General - Audit
                        #
                        ad3.db = int(html.find(id='Status3')['value'])
                        ad3.AccessionNumber = e.accessionnumberthirdlastyear
                        ad3.AmendmentFlag = e.amendthirdlastyear
                        ad3.EntityRegistrantName = e.EntityRegistrantName
                        ad3.Period = 'thirdlastyear'
                        ad3.PeriodEndDate = e.thirdlastyear
                        ad3.TradingSymbol = ts
                        #
                        # Balance Sheets - Audit
                        #
                        ad3.CurrentAssets = int(html.find(id='PRO-1.2.23')['value'])
                        ad3.NonCurrentAssets = int(html.find(id='PRO-1.2.53')['value'])
                        ad3.CurrentLiabilities = int(html.find(id='PRO-1.2.83')['value'])
                        ad3.NonCurrentLiabilities = int(html.find(id='PRO-1.2.113')['value'])
                        ad3.ShareholdersEquity = int(html.find(id='PRO-1.2.143')['value'])
                        #ad3.LiabilitiesAndShareholdersEquity = int(html.find(id='PRO-1.1.23')['value'])
                        #
                        ad3.AnomalyCurrentAssets = int(html.find(id='PRO-1.3.13')['value'])
                        #
                        ad3.AnomalyNonCurrentAssets = int(html.find(id='PRO-1.3.23')['value'])
                        #
                        ad3.AnomalyCurrentLiabilities = int(html.find(id='PRO-1.3.33')['value'])
                        #
                        ad3.AnomalyNonCurrentLiabilities = int(html.find(id='PRO-1.3.43')['value'])
                        #
                        ad3.AnomalyShareholdersEquity = int(html.find(id='PRO-1.3.53')['value'])
                        #
                        #
                        # Income Statements - Audit
                        #
                        ad3.GrossMargin = int(html.find(id='PRO-2.1.23')['value'])
                        ad3.OperatingIncome = int(html.find(id='PRO-2.1.53')['value'])
                        ad3.IncomeBeforeTaxes = int(html.find(id='PRO-2.1.83')['value'])
                        ad3.NetIncome = int(html.find(id='PRO-2.1.113')['value'])
                        #
                        ad3.AnomalyGrossMargin = int(html.find(id='PRO-2.2.13')['value'])
                        #
                        ad3.AnomalyOperatingIncome = int(html.find(id='PRO-2.2.23')['value'])
                        #
                        ad3.AnomalyIncomeBeforeTaxes = int(html.find(id='PRO-2.2.33')['value'])
                        #
                        ad3.AnomalyNetIncome = int(html.find(id='PRO-2.2.43')['value'])
                        #
                        #
                        # Comprehensive Income - Audit
                        #
                        ad3.OtherComprehensiveIncome = int(html.find(id='PRO-3.1.23')['value'])
                        #
                        ad3.AnomalyOtherComprehensiveIncome = int(html.find(id='PRO-3.2.13')['value'])
                        #
                        #
                        # Shareholders Equity - Audit
                        #
                        #ad3.ShareholdersEquityBeginning = int(html.find(id='PRO-4.0.23')['value'])
                        #
                        ad3.AnomalyConvertibleDebt = int(html.find(id='PRO-4.2.03')['value'])
                        ad3.AnomalyCommonShares = int(html.find(id='PRO-4.2.13')['value'])
                        ad3.AnomalyRetainedEarnings = int(html.find(id='PRO-4.2.23')['value'])
                        ad3.AnomalyAccumulatedOtherComprehensiveIncome = int(html.find(id='PRO-4.2.33')['value'])
                        ad3.AnomalyTreasuryShares = int(html.find(id='PRO-4.2.43')['value'])
                        ad3.AnomalyEmployeeBenefitTrust = int(html.find(id='PRO-4.2.53')['value'])
                        ad3.AnomalyNonControllingInterests = int(html.find(id='PRO-4.2.63')['value'])
                        #
                        #
                        # Cash Flow - Audit
                        #
                        ad3.CashFlowCashExplainedDifference = int(html.find(id='PRO-5.1.33')['value'])
                        #
                        ad3.AnomalyOperatingActivities = int(html.find(id='PRO-5.2.13')['value'])
                        #
                        ad3.AnomalyInvestingActivities = int(html.find(id='PRO-5.2.23')['value'])
                        #
                        ad3.AnomalyFinancingActivities = int(html.find(id='PRO-5.2.33')['value'])
                        #
                        #
                        # Supplemental - Audit
                        #
                        ad3.TargetWorkingCapital = float(html.find(id='TargetWorkingCapital3')['value'])
                        ad3.ReinvestmentOfMaintenance = int(html.find(id='ReinvestmentOfMaintenance3')['value'])
                        ad3.NormalizedDividendPaymentToNonControllingInterests = int(html.find(id='NormalizedDividendPaymentToNonControllingInterests3')['value'])
                        ad3.NormalizedDividendPaymentToPreferredShareholders = int(html.find(id='NormalizedDividendPaymentToPreferredShareholders3')['value'])
                        ad3.TheoricalInterestRate = float(html.find(id='TheoricalInterestRate3')['value'])
                        ad3.TheoricalTaxRate = float(html.find(id='TheoricalTaxRate3')['value'])
                        ad3.CapitalizationRateFloor = float(html.find(id='CapitalizationRateFloor3')['value'])
                        #
                        ad3.save()
                    except:
                        pass
                    # third last year cash flow
                    try:
                        try:
                            cf3 = CashFlow.objects.get(TradingSymbol=ts, Period='thirdlastyear')
                        except:
                            cf3 = CashFlow(TradingSymbol=ts, Period='thirdlastyear')
                        cf3.save()
                        #
                        # General - Cash Flow
                        #
                        cf3.AccessionNumber = e.accessionnumberthirdlastyear
                        cf3.AmendmentFlag = e.amendthirdlastyear
                        cf3.EntityRegistrantName = e.EntityRegistrantName
                        cf3.Period = 'thirdlastyear'
                        cf3.PeriodEndDate = e.thirdlastyear
                        cf3.TradingSymbol = ts
                        #
                        # Cash - Cash Flow
                        #
                        cf3.CashBeginningBalance = int(html.find(id='CashBeginningBalance3')['value'])
                        cf3.EffectOfExchangeRateOnCash = int(html.find(id='EffectOfExchangeRateOnCash3')['value'])
                        #
                        # Operating Activities - Cash Flow
                        #
                        cf3.DepreciationDepletionAndAmortization = int(html.find(id='DepreciationDepletionAndAmortization3')['value'])
                        cf3.GainRelatedToDisposalOrSale = int(html.find(id='GainRelatedToDisposalOrSale3')['value'])
                        cf3.RestructuringAndOtherSpecialCharges = int(html.find(id='RestructuringAndOtherSpecialCharges3')['value'])
                        cf3.AccruedEmployeeCompensation = int(html.find(id='AccruedEmployeeCompensation3')['value'])
                        cf3.ShareBasedCompensation = int(html.find(id='ShareBasedCompensationOperatingActivities3')['value'])
                        cf3.IncreaseDecreaseInIncomeTaxExpenseBenefit = int(html.find(id='IncreaseDecreaseInIncomeTaxExpenseBenefit3')['value'])
                        cf3.OtherNonCashIncomeExpense = int(html.find(id='OtherNonCashIncomeExpense3')['value'])
                        cf3.IncreaseDecreaseInAccountsReceivable = int(html.find(id='IncreaseDecreaseInAccountsReceivable3')['value'])
                        cf3.IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets = int(html.find(id='IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets3')['value'])
                        cf3.IncreaseDecreaseInInventories = int(html.find(id='IncreaseDecreaseInInventories3')['value'])
                        cf3.IncreaseDecreaseInOtherReceivables = int(html.find(id='IncreaseDecreaseInOtherReceivables3')['value'])
                        cf3.IncreaseDecreaseInAccountsPayableAndAccruedLiabilities = int(html.find(id='IncreaseDecreaseInAccountsPayableAndAccruedLiabilities3')['value'])
                        cf3.IncreaseDecreaseInContractWithCustomerLiability = int(html.find(id='IncreaseDecreaseInContractWithCustomerLiability3')['value'])
                        cf3.IncreaseDecreaseInRetirementBenefits = int(html.find(id='IncreaseDecreaseInRetirementBenefits3')['value'])
                        cf3.IncreaseDecreaseFinanceLeaseCurrent = int(html.find(id='IncreaseDecreaseFinanceLeaseCurrent3')['value'])
                        cf3.IncreaseDecreaseOperatingLeaseCurrent = int(html.find(id='IncreaseDecreaseOperatingLeaseCurrent3')['value'])
                        cf3.IncreaseDecreaseInFairValueOfDerivativesOperating = int(html.find(id='IncreaseDecreaseInFairValueOfDerivativesOperating3')['value'])
                        cf3.IncreaseDecreaseInOtherOperatingActivities = int(html.find(id='IncreaseDecreaseInOtherOperatingActivities3')['value'])
                        #
                        # Investing Activities - Cash Flow
                        #
                        cf3.PaymentsToAcquireInvestments = int(html.find(id='PaymentsToAcquireInvestments3')['value'])
                        cf3.ProceedsOfInvestments = int(html.find(id='ProceedsOfInvestments3')['value'])
                        cf3.PaymentsToAcquirePropertyPlantAndEquipment = int(html.find(id='PaymentsToAcquirePropertyPlantAndEquipment3')['value'])
                        cf3.ProceedsFromDisposalsOfPropertyAndEquipment = int(html.find(id='ProceedsFromDisposalsOfPropertyAndEquipment3')['value'])
                        cf3.PaymentsToAcquireBusinessesAndIntangibles = int(html.find(id='PaymentsToAcquireBusinessesAndIntangibles3')['value'])
                        cf3.ProceedsFromDisposalsOfBusinessesAndIntangibles = int(html.find(id='ProceedsFromDisposalsOfBusinessesAndIntangibles3')['value'])
                        cf3.ProceedsRelatedToInsuranceSettlement = int(html.find(id='ProceedsRelatedToInsuranceSettlement3')['value'])
                        cf3.ReveiptOfGovernmentGrants = int(html.find(id='ReveiptOfGovernmentGrants3')['value'])
                        cf3.PaymentOfLicenseFee = int(html.find(id='PaymentOfLicenseFee3')['value'])
                        cf3.InvestingActivitiesInDiscontinuedOperations = int(html.find(id='InvestingActivitiesInDiscontinuedOperations3')['value'])
                        cf3.OtherInvestingActivities = int(html.find(id='OtherInvestingActivities3')['value'])
                        #
                        # Financing Activities - Cash Flow
                        #
                        cf3.FinanceLeasePrincipalPayments = int(html.find(id='FinanceLeasePrincipalPayments3')['value'])
                        cf3.ProceedsFromIssuanceOfCommonShares = int(html.find(id='ProceedsFromIssuanceOfCommonShares3')['value'])
                        cf3.ProceedsFromSharePurchasePlanAndOptionsExercice = int(html.find(id='ProceedsFromSharePurchasePlanAndOptionsExercice3')['value'])
                        cf3.PaymentsRelatedToTaxWithholdingForShareBasedCompensation = int(html.find(id='PaymentsRelatedToTaxWithholdingForShareBasedCompensation3')['value'])
                        cf3.PaymentsForRepurchaseOfCommonShares = int(html.find(id='PaymentsForRepurchaseOfCommonShares3')['value'])
                        cf3.PaymentsOfDividends = int(html.find(id='PaymentsOfDividends3')['value'])
                        cf3.IncreaseDecreaseDeferredContingentConsideration = int(html.find(id='IncreaseDecreaseDeferredContingentConsideration3')['value'])
                        cf3.ProceedsFromIssuanceOfLongTermDebt = int(html.find(id='ProceedsFromIssuanceOfLongTermDebt3')['value'])
                        cf3.RepaymentsOfLongTermDebt = int(html.find(id='RepaymentsOfLongTermDebt3')['value'])
                        cf3.FinancingCosts = int(html.find(id='FinancingCosts3')['value'])
                        cf3.NetChangeInShortTermBorrowings = int(html.find(id='NetChangeInShortTermBorrowings3')['value'])
                        cf3.NetChangeInForwardAndHedgesClassifiedAsFinancingActivities = int(html.find(id='NetChangeInForwardAndHedgesClassifiedAsFinancingActivities3')['value'])
                        cf3.NetChangeInNonControllingInterests = int(html.find(id='NetChangeInNonControllingInterests3')['value'])
                        cf3.ProceedsFromRepaymentsOfCommercialPaper = int(html.find(id='ProceedsFromRepaymentsOfCommercialPaper3')['value'])
                        cf3.RepaymentsOfConvertible = int(html.find(id='RepaymentsOfConvertible3')['value'])
                        cf3.IssuanceOfConvertible = int(html.find(id='IssuanceOfConvertible3')['value'])
                        cf3.EquityInvesteeAdvancesRepayments = int(html.find(id='EquityInvesteeAdvancesRepayments3')['value'])
                        cf3.OtherFinancingActivities = int(html.find(id='OtherFinancingActivities3')['value'])
                        #
                        cf3.save()
                    except:
                        pass
                    # third last year trial balance
                    try:
                        try:
                            tb3 = TrialBalance.objects.get(TradingSymbol=ts, Period='thirdlastyear')
                        except:
                            tb3 = TrialBalance(TradingSymbol=ts, Period='thirdlastyear')
                        tb3.save()
                        #
                        # General - Trial Balance
                        #
                        tb3.AccessionNumber = e.accessionnumberthirdlastyear
                        tb3.AmendmentFlag = e.amendthirdlastyear
                        tb3.EntityRegistrantName = e.EntityRegistrantName
                        tb3.Period = 'thirdlastyear'
                        tb3.PeriodEndDate = e.thirdlastyear
                        tb3.TradingSymbol = ts
                        #
                        #
                        # Current Assets - Trial Balance
                        #
                        tb3.Cash = int(html.find(id='TrialBalanceCash3')['value'])
                        tb3.ShortTermInvestments = int(html.find(id='TrialBalanceShortTermInvestments3')['value'])
                        tb3.AccountsReceivable = int(html.find(id='TrialBalanceAccountsReceivable3')['value'])
                        tb3.WorkInProgress = int(html.find(id='TrialBalanceWorkInProgress3')['value'])
                        tb3.Inventories = int(html.find(id='TrialBalanceInventories3')['value'])
                        tb3.PrepaidExpenses = int(html.find(id='TrialBalancePrepaidExpenses3')['value'])
                        tb3.NonTradeReceivables = int(html.find(id='TrialBalanceNonTradeReceivables3')['value'])
                        tb3.PrepaidTaxAssetsCurrent = int(html.find(id='TrialBalancePrepaidTaxAssetsCurrent3')['value'])
                        tb3.DeferredTaxAssetsCurrent = int(html.find(id='TrialBalanceDeferredTaxAssetsCurrent3')['value'])
                        tb3.RightOfUseAssetsCurrent = int(html.find(id='TrialBalanceRightOfUseAssetsCurrent3')['value'])
                        tb3.OtherCurrentAssets = int(html.find(id='TrialBalanceOtherCurrentAssets3')['value'])
                        tb3.DiscontinuedOperationsCurrent = int(html.find(id='TrialBalanceDiscontinuedOperationsCurrent3')['value'])
                        #
                        #
                        # Non-Current Assets - Trial Balance
                        #
                        tb3.LongTermReceivables = int(html.find(id='TrialBalanceLongTermReceivables3')['value'])
                        tb3.DeferredCharges = int(html.find(id='TrialBalanceDeferredCharges3')['value'])
                        tb3.Investments = int(html.find(id='TrialBalanceInvestments3')['value'])
                        tb3.PropertyPlantAndEquipment = int(html.find(id='TrialBalancePropertyPlantAndEquipment3')['value'])
                        tb3.OperatingLeaseRightOfUseAssets = int(html.find(id='TrialBalanceOperatingLeaseRightOfUseAssets3')['value'])
                        tb3.FinanceLeaseRightOfUseAssets = int(html.find(id='TrialBalanceFinanceLeaseRightOfUseAssets3')['value'])
                        tb3.IntangibleAssets = int(html.find(id='TrialBalanceIntangibleAssets3')['value'])
                        tb3.Goodwill = int(html.find(id='TrialBalanceGoodwill3')['value'])
                        tb3.RefundableTaxAssetsNonCurrent = int(html.find(id='TrialBalanceRefundableTaxAssetsNonCurrent3')['value'])
                        tb3.DeferredTaxAssetsNonCurrent = int(html.find(id='TrialBalanceDeferredTaxAssetsNonCurrent3')['value'])
                        tb3.DefinedBenefitPensionAndOtherSimilarPlans = int(html.find(id='TrialBalanceDefinedBenefitPensionAndOtherSimilarPlans3')['value'])
                        tb3.OtherNonCurrentAssets = int(html.find(id='TrialBalanceOtherNonCurrentAssets3')['value'])
                        tb3.DiscontinuedOperations = int(html.find(id='TrialBalanceDiscontinuedOperations3')['value'])
                        #
                        #
                        # Current Liabilities - Trial Balance
                        #
                        tb3.AccountsPayableAndAccruedLiabilities = int(html.find(id='TrialBalanceAccountsPayableAndAccruedLiabilities3')['value'])
                        tb3.EmployeeCompensationCurrent = int(html.find(id='TrialBalanceEmployeeCompensationCurrent3')['value'])
                        tb3.OperatingLeasesCurrent = int(html.find(id='TrialBalanceOperatingLeasesCurrent3')['value'])
                        tb3.FinanceLeasesCurrent = int(html.find(id='TrialBalanceFinanceLeasesCurrent3')['value'])
                        tb3.DeferredRevenueAndDepositsCurrent = int(html.find(id='TrialBalanceDeferredRevenueAndDepositsCurrent3')['value'])
                        tb3.AccruedTaxLiabilities = int(html.find(id='TrialBalanceAccruedTaxLiabilities3')['value'])
                        tb3.DeferredTaxLiabilitiesCurrent = int(html.find(id='TrialBalanceDeferredTaxLiabilitiesCurrent3')['value'])
                        tb3.CommercialPapers = int(html.find(id='TrialBalanceCommercialPapers3')['value'])
                        tb3.ShortTermBorrowings = int(html.find(id='TrialBalanceShortTermBorrowings3')['value'])
                        tb3.OtherCurrentLiabilities = int(html.find(id='TrialBalanceOtherCurrentLiabilities3')['value'])
                        tb3.DiscontinuedOperationsLiabilitiesCurrent = int(html.find(id='TrialBalanceDiscontinuedOperationsLiabilitiesCurrent3')['value'])
                        tb3.DividendsPayable = int(html.find(id='TrialBalanceDividendsPayable3')['value'])
                        tb3.ShortTermPortionOfLongTermDebt = int(html.find(id='TrialBalanceShortTermPortionOfLongTermDebt3')['value'])
                        #
                        #
                        # Non-Current Liabilities - Trial Balance
                        #
                        tb3.LongTermDebt = int(html.find(id='TrialBalanceLongTermDebt3')['value'])
                        tb3.PreferredSharesLiability = int(html.find(id='TrialBalancePreferredSharesLiability3')['value'])
                        tb3.RetirementBenefits = int(html.find(id='TrialBalanceRetirementBenefits3')['value'])
                        tb3.OperatingLeasesNonCurrent = int(html.find(id='TrialBalanceOperatingLeasesNonCurrent3')['value'])
                        tb3.FinanceLeasesNonCurrent = int(html.find(id='TrialBalanceFinanceLeasesNonCurrent3')['value'])
                        tb3.LeaseIncentiveObligation = int(html.find(id='TrialBalanceLeaseIncentiveObligation3')['value'])
                        tb3.DeferredRevenueAndDepositsNonCurrent = int(html.find(id='TrialBalanceDeferredRevenueAndDepositsNonCurrent3')['value'])
                        tb3.ContingentConsideration = int(html.find(id='TrialBalanceContingentConsideration3')['value'])
                        tb3.AccruedTaxLiabilitiesNonCurrent = int(html.find(id='TrialBalanceAccruedTaxLiabilitiesNonCurrent3')['value'])
                        tb3.DeferredTaxLiabilitiesNonCurrent = int(html.find(id='TrialBalanceDeferredTaxLiabilitiesNonCurrent3')['value'])
                        tb3.OtherNonCurrentLiabilities = int(html.find(id='TrialBalanceOtherNonCurrentLiabilities3')['value'])
                        tb3.RedeemableNonControllingInterests = int(html.find(id='TrialBalanceRedeemableNonControllingInterests3')['value'])
                        tb3.DiscontinuedOperationsLiabilitiesNonCurrent = int(html.find(id='TrialBalanceDiscontinuedOperationsLiabilitiesNonCurrent3')['value'])
                        #
                        #
                        # Shareholders Equity - Trial Balance
                        #
                        # convertible debt
                        tb3.ConvertibleDebtBeginning = int(html.find(id='TrialBalanceConvertibleDebt3')['value'])
                        #
                        # common shares
                        tb3.CommonSharesBeginning = int(html.find(id='TrialBalanceCommonShares3')['value'])
                        tb3.CommonSharesIssued = int(html.find(id='TrialBalanceCommonSharesIssued3')['value'])
                        tb3.ShareBasedCompensation = int(html.find(id='TrialBalanceShareBasedCompensation3')['value'])
                        #
                        # preferred shares
                        try:
                            tb3.PreferredSharesBeginning = int(html.find(id='TrialBalancePreferredShares3')['value'])
                        except:
                            pass
                        #
                        # retained earnings
                        tb3.RetainedEarningsBeginning = int(html.find(id='TrialBalanceRetainedEarningsAccumulatedDeficit3')['value'])
                        tb3.DividendsAndDividendEquivalentsDeclared = int(html.find(id='TrialBalanceDividendsAndDividendEquivalentsDeclared3')['value'])
                        tb3.CommonSharesRepurchasedAndRetired = int(html.find(id='TrialBalanceCommonSharesRepurchasedAndRetired3')['value'])
                        tb3.ShareBasedCompensationRetainedEarnings = int(html.find(id='TrialBalanceShareBasedCompensationRetainedEarnings3')['value'])
                        tb3.EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts = int(html.find(id='TrialBalanceEffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts3')['value'])
                        tb3.RetainedEarningsOthers = int(html.find(id='TrialBalanceRetainedEarningsOthers3')['value'])
                        #
                        # accumulated other comprehensive income
                        tb3.AccumulatedOtherComprehensiveIncomeBeginning = int(html.find(id='TrialBalanceAccumulatedOtherComprehensiveIncomeLoss3')['value'])
                        #
                        # treasury shares
                        tb3.TreasurySharesBeginning = int(html.find(id='TrialBalanceTreasuryShares3')['value'])
                        tb3.PurchaseAndSellOfTreasuryShares = int(html.find(id='TrialBalancePurchaseAndSellOfTreasuryShares3')['value'])
                        #
                        # employee benefit trust
                        tb3.EmployeeBenefitTrustBeginning = int(html.find(id='TrialBalanceEmployeeBenefitTrust3')['value'])
                        #
                        # non controlling interests
                        tb3.NonControllingInterestsBeginning = int(html.find(id='TrialBalanceNonControllingInterests3')['value'])
                        tb3.DividendsDeclaredToNonControllingInterests = int(html.find(id='TrialBalanceDividendsDeclaredToNonControllingInterests3')['value'])
                        tb3.AcquisitionOfNonControllingInterests = int(html.find(id='TrialBalanceAcquisitionOfNonControllingInterests3')['value'])
                        tb3.NonControllingInterestsOthers = int(html.find(id='TrialBalanceNonControllingInterestsOthers3')['value'])
                        #
                        #
                        # Income Statements - Trial Balance
                        #
                        tb3.Sales = int(html.find(id='TrialBalanceSales3')['value'])
                        tb3.CostOfSales = int(html.find(id='TrialBalanceCostOfSales3')['value'])
                        tb3.ResearchAndDevelopment = int(html.find(id='TrialBalanceResearchAndDevelopment3')['value'])
                        tb3.SellingGeneralAdministrativeAndMarketing = int(html.find(id='TrialBalanceSellingGeneralAdministrativeAndMarketing3')['value'])
                        tb3.ImpairmentRestructuringAndOtherSpecialCharges = int(html.find(id='TrialBalanceImpairmentRestructuringAndOtherSpecialCharges3')['value'])
                        tb3.NonOperatingIncome = int(html.find(id='TrialBalanceNonOperatingIncomeExpense3')['value'])
                        tb3.IncomeTaxExpenseBenefit = int(html.find(id='TrialBalanceIncomeTaxExpenseBenefit3')['value'])
                        tb3.EquityMethodInvesteesIncome = int(html.find(id='TrialBalanceEquityMethodInvesteesIncome3')['value'])
                        tb3.NetIncomeFromDiscontinuedOperations = int(html.find(id='TrialBalanceNetIncomeFromDiscontinuedOperations3')['value'])
                        #
                        #
                        # Other Comprehensive Income - Trial Balance
                        #
                        tb3.ChangeInForeignCurrencyTranslationAdjustment = int(html.find(id='TrialBalanceChangeInForeignCurrencyTranslationAdjustment3')['value'])
                        tb3.ChangeInUnrealizedGainsLossesOnDerivativeInstruments = int(html.find(id='TrialBalanceChangeInUnrealizedGainsLossesOnDerivativeInstruments3')['value'])
                        tb3.ChangeInUnrealizedGainsLossesOnInvestments = int(html.find(id='TrialBalanceChangeInUnrealizedGainsLossesOnInvestments3')['value'])
                        tb3.ChangeInDefinedBenefitPensionAndOtherSimilarPlans = int(html.find(id='TrialBalanceChangeInDefinedBenefitPensionAndOtherSimilarPlans3')['value'])
                        tb3.IncomeTaxOnOtherComprehensiveIncome = int(html.find(id='TrialBalanceIncomeTaxOnOtherComprehensiveIncome3')['value'])
                        #
                        tb3.save()
                    except:
                        pass
                except:
                    pass
                # fourth last year
                try:
                    # fourth last year audit
                    try:
                        #
                        try:
                            ad4 = AuditData.objects.get(TradingSymbol=ts, Period='fourthlastyear')
                        except:
                            ad4 = AuditData(TradingSymbol=ts, Period='fourthlastyear')
                        ad4.save()
                        #
                        # General - Audit
                        #
                        ad4.db = int(html.find(id='Status4')['value'])
                        ad4.AccessionNumber = e.accessionnumberfourthlastyear
                        ad4.AmendmentFlag = e.amendfourthlastyear
                        ad4.EntityRegistrantName = e.EntityRegistrantName
                        ad4.Period = 'fourthlastyear'
                        ad4.PeriodEndDate = e.fourthlastyear
                        ad4.TradingSymbol = ts
                        #
                        # Balance Sheets - Audit
                        #
                        ad4.CurrentAssets = int(html.find(id='PRO-1.2.24')['value'])
                        ad4.NonCurrentAssets = int(html.find(id='PRO-1.2.54')['value'])
                        ad4.CurrentLiabilities = int(html.find(id='PRO-1.2.84')['value'])
                        ad4.NonCurrentLiabilities = int(html.find(id='PRO-1.2.114')['value'])
                        ad4.ShareholdersEquity = int(html.find(id='PRO-1.2.144')['value'])
                        #ad4.LiabilitiesAndShareholdersEquity = int(html.find(id='PRO-1.1.24')['value'])
                        #
                        ad4.AnomalyCurrentAssets = int(html.find(id='PRO-1.3.14')['value'])
                        #
                        ad4.AnomalyNonCurrentAssets = int(html.find(id='PRO-1.3.24')['value'])
                        #
                        ad4.AnomalyCurrentLiabilities = int(html.find(id='PRO-1.3.34')['value'])
                        #
                        ad4.AnomalyNonCurrentLiabilities = int(html.find(id='PRO-1.3.44')['value'])
                        #
                        ad4.AnomalyShareholdersEquity = int(html.find(id='PRO-1.3.54')['value'])
                        #
                        #
                        # Income Statements - Audit
                        #
                        ad4.GrossMargin = int(html.find(id='PRO-2.1.24')['value'])
                        ad4.OperatingIncome = int(html.find(id='PRO-2.1.54')['value'])
                        ad4.IncomeBeforeTaxes = int(html.find(id='PRO-2.1.84')['value'])
                        ad4.NetIncome = int(html.find(id='PRO-2.1.114')['value'])
                        #
                        ad4.AnomalyGrossMargin = int(html.find(id='PRO-2.2.14')['value'])
                        #
                        ad4.AnomalyOperatingIncome = int(html.find(id='PRO-2.2.24')['value'])
                        #
                        ad4.AnomalyIncomeBeforeTaxes = int(html.find(id='PRO-2.2.34')['value'])
                        #
                        ad4.AnomalyNetIncome = int(html.find(id='PRO-2.2.44')['value'])
                        #
                        #
                        # Comprehensive Income - Audit
                        #
                        ad4.OtherComprehensiveIncome = int(html.find(id='PRO-3.1.24')['value'])
                        #
                        ad4.AnomalyOtherComprehensiveIncome = int(html.find(id='PRO-3.2.14')['value'])
                        #
                        #
                        # Shareholders Equity - Audit
                        #
                        #ad4.ShareholdersEquityBeginning = int(html.find(id='PRO-4.0.24')['value'])
                        #
                        ad4.AnomalyConvertibleDebt = int(html.find(id='PRO-4.2.04')['value'])
                        ad4.AnomalyCommonShares = int(html.find(id='PRO-4.2.14')['value'])
                        ad4.AnomalyRetainedEarnings = int(html.find(id='PRO-4.2.24')['value'])
                        ad4.AnomalyAccumulatedOtherComprehensiveIncome = int(html.find(id='PRO-4.2.34')['value'])
                        ad4.AnomalyTreasuryShares = int(html.find(id='PRO-4.2.44')['value'])
                        ad4.AnomalyEmployeeBenefitTrust = int(html.find(id='PRO-4.2.54')['value'])
                        ad4.AnomalyNonControllingInterests = int(html.find(id='PRO-4.2.64')['value'])
                        #
                        #
                        # Cash Flow - Audit
                        #
                        ad4.CashFlowCashExplainedDifference = int(html.find(id='PRO-5.1.34')['value'])
                        #
                        ad4.AnomalyOperatingActivities = int(html.find(id='PRO-5.2.14')['value'])
                        #
                        ad4.AnomalyInvestingActivities = int(html.find(id='PRO-5.2.24')['value'])
                        #
                        ad4.AnomalyFinancingActivities = int(html.find(id='PRO-5.2.34')['value'])
                        #
                        #
                        # Supplemental - Audit
                        #
                        ad4.TargetWorkingCapital = float(html.find(id='TargetWorkingCapital4')['value'])
                        ad4.ReinvestmentOfMaintenance = int(html.find(id='ReinvestmentOfMaintenance4')['value'])
                        ad4.NormalizedDividendPaymentToNonControllingInterests = int(html.find(id='NormalizedDividendPaymentToNonControllingInterests4')['value'])
                        ad4.NormalizedDividendPaymentToPreferredShareholders = int(html.find(id='NormalizedDividendPaymentToPreferredShareholders4')['value'])
                        ad4.TheoricalInterestRate = float(html.find(id='TheoricalInterestRate4')['value'])
                        ad4.TheoricalTaxRate = float(html.find(id='TheoricalTaxRate4')['value'])
                        ad4.CapitalizationRateFloor = float(html.find(id='CapitalizationRateFloor4')['value'])
                        #
                        ad4.save()
                    except:
                        pass
                    # fourth last year cash flow
                    try:
                        try:
                            cf4 = CashFlow.objects.get(TradingSymbol=ts, Period='fourthlastyear')
                        except:
                            cf4 = CashFlow(TradingSymbol=ts, Period='fourthlastyear')
                        cf4.save()
                        #
                        # General - Cash Flow
                        #
                        cf4.AccessionNumber = e.accessionnumberfourthlastyear
                        cf4.AmendmentFlag = e.amendfourthlastyear
                        cf4.EntityRegistrantName = e.EntityRegistrantName
                        cf4.Period = 'fourthlastyear'
                        cf4.PeriodEndDate = e.fourthlastyear
                        cf4.TradingSymbol = ts
                        #
                        # Cash - Cash Flow
                        #
                        cf4.CashBeginningBalance = int(html.find(id='CashBeginningBalance4')['value'])
                        cf4.EffectOfExchangeRateOnCash = int(html.find(id='EffectOfExchangeRateOnCash4')['value'])
                        #
                        # Operating Activities - Cash Flow
                        #
                        cf4.DepreciationDepletionAndAmortization = int(html.find(id='DepreciationDepletionAndAmortization4')['value'])
                        cf4.GainRelatedToDisposalOrSale = int(html.find(id='GainRelatedToDisposalOrSale4')['value'])
                        cf4.RestructuringAndOtherSpecialCharges = int(html.find(id='RestructuringAndOtherSpecialCharges4')['value'])
                        cf4.AccruedEmployeeCompensation = int(html.find(id='AccruedEmployeeCompensation4')['value'])
                        cf4.ShareBasedCompensation = int(html.find(id='ShareBasedCompensationOperatingActivities4')['value'])
                        cf4.IncreaseDecreaseInIncomeTaxExpenseBenefit = int(html.find(id='IncreaseDecreaseInIncomeTaxExpenseBenefit4')['value'])
                        cf4.OtherNonCashIncomeExpense = int(html.find(id='OtherNonCashIncomeExpense4')['value'])
                        cf4.IncreaseDecreaseInAccountsReceivable = int(html.find(id='IncreaseDecreaseInAccountsReceivable4')['value'])
                        cf4.IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets = int(html.find(id='IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets4')['value'])
                        cf4.IncreaseDecreaseInInventories = int(html.find(id='IncreaseDecreaseInInventories4')['value'])
                        cf4.IncreaseDecreaseInOtherReceivables = int(html.find(id='IncreaseDecreaseInOtherReceivables4')['value'])
                        cf4.IncreaseDecreaseInAccountsPayableAndAccruedLiabilities = int(html.find(id='IncreaseDecreaseInAccountsPayableAndAccruedLiabilities4')['value'])
                        cf4.IncreaseDecreaseInContractWithCustomerLiability = int(html.find(id='IncreaseDecreaseInContractWithCustomerLiability4')['value'])
                        cf4.IncreaseDecreaseInRetirementBenefits = int(html.find(id='IncreaseDecreaseInRetirementBenefits4')['value'])
                        cf4.IncreaseDecreaseFinanceLeaseCurrent = int(html.find(id='IncreaseDecreaseFinanceLeaseCurrent4')['value'])
                        cf4.IncreaseDecreaseOperatingLeaseCurrent = int(html.find(id='IncreaseDecreaseOperatingLeaseCurrent4')['value'])
                        cf4.IncreaseDecreaseInFairValueOfDerivativesOperating = int(html.find(id='IncreaseDecreaseInFairValueOfDerivativesOperating4')['value'])
                        cf4.IncreaseDecreaseInOtherOperatingActivities = int(html.find(id='IncreaseDecreaseInOtherOperatingActivities4')['value'])
                        #
                        # Investing Activities - Cash Flow
                        #
                        cf4.PaymentsToAcquireInvestments = int(html.find(id='PaymentsToAcquireInvestments4')['value'])
                        cf4.ProceedsOfInvestments = int(html.find(id='ProceedsOfInvestments4')['value'])
                        cf4.PaymentsToAcquirePropertyPlantAndEquipment = int(html.find(id='PaymentsToAcquirePropertyPlantAndEquipment4')['value'])
                        cf4.ProceedsFromDisposalsOfPropertyAndEquipment = int(html.find(id='ProceedsFromDisposalsOfPropertyAndEquipment4')['value'])
                        cf4.PaymentsToAcquireBusinessesAndIntangibles = int(html.find(id='PaymentsToAcquireBusinessesAndIntangibles4')['value'])
                        cf4.ProceedsFromDisposalsOfBusinessesAndIntangibles = int(html.find(id='ProceedsFromDisposalsOfBusinessesAndIntangibles4')['value'])
                        cf4.ProceedsRelatedToInsuranceSettlement = int(html.find(id='ProceedsRelatedToInsuranceSettlement4')['value'])
                        cf4.ReveiptOfGovernmentGrants = int(html.find(id='ReveiptOfGovernmentGrants4')['value'])
                        cf4.PaymentOfLicenseFee = int(html.find(id='PaymentOfLicenseFee4')['value'])
                        cf4.InvestingActivitiesInDiscontinuedOperations = int(html.find(id='InvestingActivitiesInDiscontinuedOperations4')['value'])
                        cf4.OtherInvestingActivities = int(html.find(id='OtherInvestingActivities4')['value'])
                        #
                        # Financing Activities - Cash Flow
                        #
                        cf4.FinanceLeasePrincipalPayments = int(html.find(id='FinanceLeasePrincipalPayments4')['value'])
                        cf4.ProceedsFromIssuanceOfCommonShares = int(html.find(id='ProceedsFromIssuanceOfCommonShares4')['value'])
                        cf4.ProceedsFromSharePurchasePlanAndOptionsExercice = int(html.find(id='ProceedsFromSharePurchasePlanAndOptionsExercice4')['value'])
                        cf4.PaymentsRelatedToTaxWithholdingForShareBasedCompensation = int(html.find(id='PaymentsRelatedToTaxWithholdingForShareBasedCompensation4')['value'])
                        cf4.PaymentsForRepurchaseOfCommonShares = int(html.find(id='PaymentsForRepurchaseOfCommonShares4')['value'])
                        cf4.PaymentsOfDividends = int(html.find(id='PaymentsOfDividends4')['value'])
                        cf4.IncreaseDecreaseDeferredContingentConsideration = int(html.find(id='IncreaseDecreaseDeferredContingentConsideration4')['value'])
                        cf4.ProceedsFromIssuanceOfLongTermDebt = int(html.find(id='ProceedsFromIssuanceOfLongTermDebt4')['value'])
                        cf4.RepaymentsOfLongTermDebt = int(html.find(id='RepaymentsOfLongTermDebt4')['value'])
                        cf4.FinancingCosts = int(html.find(id='FinancingCosts4')['value'])
                        cf4.NetChangeInShortTermBorrowings = int(html.find(id='NetChangeInShortTermBorrowings4')['value'])
                        cf4.NetChangeInForwardAndHedgesClassifiedAsFinancingActivities = int(html.find(id='NetChangeInForwardAndHedgesClassifiedAsFinancingActivities4')['value'])
                        cf4.NetChangeInNonControllingInterests = int(html.find(id='NetChangeInNonControllingInterests4')['value'])
                        cf4.ProceedsFromRepaymentsOfCommercialPaper = int(html.find(id='ProceedsFromRepaymentsOfCommercialPaper4')['value'])
                        cf4.RepaymentsOfConvertible = int(html.find(id='RepaymentsOfConvertible4')['value'])
                        cf4.IssuanceOfConvertible = int(html.find(id='IssuanceOfConvertible4')['value'])
                        cf4.EquityInvesteeAdvancesRepayments = int(html.find(id='EquityInvesteeAdvancesRepayments4')['value'])
                        cf4.OtherFinancingActivities = int(html.find(id='OtherFinancingActivities4')['value'])
                        #
                        cf4.save()
                    except:
                        pass
                    # fourth last year trial balance
                    try:
                        try:
                            tb4 = TrialBalance.objects.get(TradingSymbol=ts, Period='fourthlastyear')
                        except:
                            tb4 = TrialBalance(TradingSymbol=ts, Period='fourthlastyear')
                        tb4.save()
                        #
                        # General - Trial Balance
                        #
                        tb4.AccessionNumber = e.accessionnumberfourthlastyear
                        tb4.AmendmentFlag = e.amendfourthlastyear
                        tb4.EntityRegistrantName = e.EntityRegistrantName
                        tb4.Period = 'fourthlastyear'
                        tb4.PeriodEndDate = e.fourthlastyear
                        tb4.TradingSymbol = ts
                        #
                        #
                        # Current Assets - Trial Balance
                        #
                        tb4.Cash = int(html.find(id='TrialBalanceCash4')['value'])
                        tb4.ShortTermInvestments = int(html.find(id='TrialBalanceShortTermInvestments4')['value'])
                        tb4.AccountsReceivable = int(html.find(id='TrialBalanceAccountsReceivable4')['value'])
                        tb4.WorkInProgress = int(html.find(id='TrialBalanceWorkInProgress4')['value'])
                        tb4.Inventories = int(html.find(id='TrialBalanceInventories4')['value'])
                        tb4.PrepaidExpenses = int(html.find(id='TrialBalancePrepaidExpenses4')['value'])
                        tb4.NonTradeReceivables = int(html.find(id='TrialBalanceNonTradeReceivables4')['value'])
                        tb4.PrepaidTaxAssetsCurrent = int(html.find(id='TrialBalancePrepaidTaxAssetsCurrent4')['value'])
                        tb4.DeferredTaxAssetsCurrent = int(html.find(id='TrialBalanceDeferredTaxAssetsCurrent4')['value'])
                        tb4.RightOfUseAssetsCurrent = int(html.find(id='TrialBalanceRightOfUseAssetsCurrent4')['value'])
                        tb4.OtherCurrentAssets = int(html.find(id='TrialBalanceOtherCurrentAssets4')['value'])
                        tb4.DiscontinuedOperationsCurrent = int(html.find(id='TrialBalanceDiscontinuedOperationsCurrent4')['value'])
                        #
                        #
                        # Non-Current Assets - Trial Balance
                        #
                        tb4.LongTermReceivables = int(html.find(id='TrialBalanceLongTermReceivables4')['value'])
                        tb4.DeferredCharges = int(html.find(id='TrialBalanceDeferredCharges4')['value'])
                        tb4.Investments = int(html.find(id='TrialBalanceInvestments4')['value'])
                        tb4.PropertyPlantAndEquipment = int(html.find(id='TrialBalancePropertyPlantAndEquipment4')['value'])
                        tb4.OperatingLeaseRightOfUseAssets = int(html.find(id='TrialBalanceOperatingLeaseRightOfUseAssets4')['value'])
                        tb4.FinanceLeaseRightOfUseAssets = int(html.find(id='TrialBalanceFinanceLeaseRightOfUseAssets4')['value'])
                        tb4.IntangibleAssets = int(html.find(id='TrialBalanceIntangibleAssets4')['value'])
                        tb4.Goodwill = int(html.find(id='TrialBalanceGoodwill4')['value'])
                        tb4.RefundableTaxAssetsNonCurrent = int(html.find(id='TrialBalanceRefundableTaxAssetsNonCurrent4')['value'])
                        tb4.DeferredTaxAssetsNonCurrent = int(html.find(id='TrialBalanceDeferredTaxAssetsNonCurrent4')['value'])
                        tb4.DefinedBenefitPensionAndOtherSimilarPlans = int(html.find(id='TrialBalanceDefinedBenefitPensionAndOtherSimilarPlans4')['value'])
                        tb4.OtherNonCurrentAssets = int(html.find(id='TrialBalanceOtherNonCurrentAssets4')['value'])
                        tb4.DiscontinuedOperations = int(html.find(id='TrialBalanceDiscontinuedOperations4')['value'])
                        #
                        #
                        # Current Liabilities - Trial Balance
                        #
                        tb4.AccountsPayableAndAccruedLiabilities = int(html.find(id='TrialBalanceAccountsPayableAndAccruedLiabilities4')['value'])
                        tb4.EmployeeCompensationCurrent = int(html.find(id='TrialBalanceEmployeeCompensationCurrent4')['value'])
                        tb4.OperatingLeasesCurrent = int(html.find(id='TrialBalanceOperatingLeasesCurrent4')['value'])
                        tb4.FinanceLeasesCurrent = int(html.find(id='TrialBalanceFinanceLeasesCurrent4')['value'])
                        tb4.DeferredRevenueAndDepositsCurrent = int(html.find(id='TrialBalanceDeferredRevenueAndDepositsCurrent4')['value'])
                        tb4.AccruedTaxLiabilities = int(html.find(id='TrialBalanceAccruedTaxLiabilities4')['value'])
                        tb4.DeferredTaxLiabilitiesCurrent = int(html.find(id='TrialBalanceDeferredTaxLiabilitiesCurrent4')['value'])
                        tb4.CommercialPapers = int(html.find(id='TrialBalanceCommercialPapers4')['value'])
                        tb4.ShortTermBorrowings = int(html.find(id='TrialBalanceShortTermBorrowings4')['value'])
                        tb4.OtherCurrentLiabilities = int(html.find(id='TrialBalanceOtherCurrentLiabilities4')['value'])
                        tb4.DiscontinuedOperationsLiabilitiesCurrent = int(html.find(id='TrialBalanceDiscontinuedOperationsLiabilitiesCurrent4')['value'])
                        tb4.DividendsPayable = int(html.find(id='TrialBalanceDividendsPayable4')['value'])
                        tb4.ShortTermPortionOfLongTermDebt = int(html.find(id='TrialBalanceShortTermPortionOfLongTermDebt4')['value'])
                        #
                        #
                        # Non-Current Liabilities - Trial Balance
                        #
                        tb4.LongTermDebt = int(html.find(id='TrialBalanceLongTermDebt4')['value'])
                        tb4.PreferredSharesLiability = int(html.find(id='TrialBalancePreferredSharesLiability4')['value'])
                        tb4.RetirementBenefits = int(html.find(id='TrialBalanceRetirementBenefits4')['value'])
                        tb4.OperatingLeasesNonCurrent = int(html.find(id='TrialBalanceOperatingLeasesNonCurrent4')['value'])
                        tb4.FinanceLeasesNonCurrent = int(html.find(id='TrialBalanceFinanceLeasesNonCurrent4')['value'])
                        tb4.LeaseIncentiveObligation = int(html.find(id='TrialBalanceLeaseIncentiveObligation4')['value'])
                        tb4.DeferredRevenueAndDepositsNonCurrent = int(html.find(id='TrialBalanceDeferredRevenueAndDepositsNonCurrent4')['value'])
                        tb4.ContingentConsideration = int(html.find(id='TrialBalanceContingentConsideration4')['value'])
                        tb4.AccruedTaxLiabilitiesNonCurrent = int(html.find(id='TrialBalanceAccruedTaxLiabilitiesNonCurrent4')['value'])
                        tb4.DeferredTaxLiabilitiesNonCurrent = int(html.find(id='TrialBalanceDeferredTaxLiabilitiesNonCurrent4')['value'])
                        tb4.OtherNonCurrentLiabilities = int(html.find(id='TrialBalanceOtherNonCurrentLiabilities4')['value'])
                        tb4.RedeemableNonControllingInterests = int(html.find(id='TrialBalanceRedeemableNonControllingInterests4')['value'])
                        tb4.DiscontinuedOperationsLiabilitiesNonCurrent = int(html.find(id='TrialBalanceDiscontinuedOperationsLiabilitiesNonCurrent4')['value'])
                        #
                        #
                        # Shareholders Equity - Trial Balance
                        #
                        # convertible debt
                        tb4.ConvertibleDebtBeginning = int(html.find(id='TrialBalanceConvertibleDebt4')['value'])
                        #
                        # common shares
                        tb4.CommonSharesBeginning = int(html.find(id='TrialBalanceCommonShares4')['value'])
                        tb4.CommonSharesIssued = int(html.find(id='TrialBalanceCommonSharesIssued4')['value'])
                        tb4.ShareBasedCompensation = int(html.find(id='TrialBalanceShareBasedCompensation4')['value'])
                        #
                        # preferred shares
                        try:
                            tb4.PreferredSharesBeginning = int(html.find(id='TrialBalancePreferredShares4')['value'])
                        except:
                            pass
                        #
                        # retained earnings
                        tb4.RetainedEarningsBeginning = int(html.find(id='TrialBalanceRetainedEarningsAccumulatedDeficit4')['value'])
                        tb4.DividendsAndDividendEquivalentsDeclared = int(html.find(id='TrialBalanceDividendsAndDividendEquivalentsDeclared4')['value'])
                        tb4.CommonSharesRepurchasedAndRetired = int(html.find(id='TrialBalanceCommonSharesRepurchasedAndRetired4')['value'])
                        tb4.ShareBasedCompensationRetainedEarnings = int(html.find(id='TrialBalanceShareBasedCompensationRetainedEarnings4')['value'])
                        tb4.EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts = int(html.find(id='TrialBalanceEffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts4')['value'])
                        tb4.RetainedEarningsOthers = int(html.find(id='TrialBalanceRetainedEarningsOthers4')['value'])
                        #
                        # accumulated other comprehensive income
                        tb4.AccumulatedOtherComprehensiveIncomeBeginning = int(html.find(id='TrialBalanceAccumulatedOtherComprehensiveIncomeLoss4')['value'])
                        #
                        # treasury shares
                        tb4.TreasurySharesBeginning = int(html.find(id='TrialBalanceTreasuryShares4')['value'])
                        tb4.PurchaseAndSellOfTreasuryShares = int(html.find(id='TrialBalancePurchaseAndSellOfTreasuryShares4')['value'])
                        #
                        # employee benefit trust
                        tb4.EmployeeBenefitTrustBeginning = int(html.find(id='TrialBalanceEmployeeBenefitTrust4')['value'])
                        #
                        # non controlling interests
                        tb4.NonControllingInterestsBeginning = int(html.find(id='TrialBalanceNonControllingInterests4')['value'])
                        tb4.DividendsDeclaredToNonControllingInterests = int(html.find(id='TrialBalanceDividendsDeclaredToNonControllingInterests4')['value'])
                        tb4.AcquisitionOfNonControllingInterests = int(html.find(id='TrialBalanceAcquisitionOfNonControllingInterests4')['value'])
                        tb4.NonControllingInterestsOthers = int(html.find(id='TrialBalanceNonControllingInterestsOthers4')['value'])
                        #
                        #
                        # Income Statements - Trial Balance
                        #
                        tb4.Sales = int(html.find(id='TrialBalanceSales4')['value'])
                        tb4.CostOfSales = int(html.find(id='TrialBalanceCostOfSales4')['value'])
                        tb4.ResearchAndDevelopment = int(html.find(id='TrialBalanceResearchAndDevelopment4')['value'])
                        tb4.SellingGeneralAdministrativeAndMarketing = int(html.find(id='TrialBalanceSellingGeneralAdministrativeAndMarketing4')['value'])
                        tb4.ImpairmentRestructuringAndOtherSpecialCharges = int(html.find(id='TrialBalanceImpairmentRestructuringAndOtherSpecialCharges4')['value'])
                        tb4.NonOperatingIncome = int(html.find(id='TrialBalanceNonOperatingIncomeExpense4')['value'])
                        tb4.IncomeTaxExpenseBenefit = int(html.find(id='TrialBalanceIncomeTaxExpenseBenefit4')['value'])
                        tb4.EquityMethodInvesteesIncome = int(html.find(id='TrialBalanceEquityMethodInvesteesIncome4')['value'])
                        tb4.NetIncomeFromDiscontinuedOperations = int(html.find(id='TrialBalanceNetIncomeFromDiscontinuedOperations4')['value'])
                        #
                        #
                        # Other Comprehensive Income - Trial Balance
                        #
                        tb4.ChangeInForeignCurrencyTranslationAdjustment = int(html.find(id='TrialBalanceChangeInForeignCurrencyTranslationAdjustment4')['value'])
                        tb4.ChangeInUnrealizedGainsLossesOnDerivativeInstruments = int(html.find(id='TrialBalanceChangeInUnrealizedGainsLossesOnDerivativeInstruments4')['value'])
                        tb4.ChangeInUnrealizedGainsLossesOnInvestments = int(html.find(id='TrialBalanceChangeInUnrealizedGainsLossesOnInvestments4')['value'])
                        tb4.ChangeInDefinedBenefitPensionAndOtherSimilarPlans = int(html.find(id='TrialBalanceChangeInDefinedBenefitPensionAndOtherSimilarPlans4')['value'])
                        tb4.IncomeTaxOnOtherComprehensiveIncome = int(html.find(id='TrialBalanceIncomeTaxOnOtherComprehensiveIncome4')['value'])
                        #
                        tb4.save()
                    except:
                        pass
                except:
                    pass
                # fifth last year
                try:
                    # fifth last year audit
                    try:
                        try:
                            ad5 = AuditData.objects.get(TradingSymbol=ts, Period='fifthlastyear')
                        except:
                            ad5 = AuditData(TradingSymbol=ts, Period='fifthlastyear')
                        ad5.save()
                        #
                        # General - Audit
                        #
                        ad5.db = int(html.find(id='Status5')['value'])
                        ad5.AccessionNumber = e.accessionnumberfifthlastyear
                        ad5.AmendmentFlag = e.amendfifthlastyear
                        ad5.EntityRegistrantName = e.EntityRegistrantName
                        ad5.Period = 'fifthlastyear'
                        ad5.PeriodEndDate = e.fifthlastyear
                        ad5.TradingSymbol = ts
                        #
                        # Balance Sheets - Audit
                        #
                        ad5.CurrentAssets = int(html.find(id='PRO-1.2.25')['value'])
                        ad5.NonCurrentAssets = int(html.find(id='PRO-1.2.55')['value'])
                        ad5.CurrentLiabilities = int(html.find(id='PRO-1.2.85')['value'])
                        ad5.NonCurrentLiabilities = int(html.find(id='PRO-1.2.115')['value'])
                        ad5.ShareholdersEquity = int(html.find(id='PRO-1.2.145')['value'])
                        #ad5.LiabilitiesAndShareholdersEquity = int(html.find(id='PRO-1.1.25')['value'])
                        #
                        ad5.AnomalyCurrentAssets = int(html.find(id='PRO-1.3.15')['value'])
                        #
                        ad5.AnomalyNonCurrentAssets = int(html.find(id='PRO-1.3.25')['value'])
                        #
                        ad5.AnomalyCurrentLiabilities = int(html.find(id='PRO-1.3.35')['value'])
                        #
                        ad5.AnomalyNonCurrentLiabilities = int(html.find(id='PRO-1.3.45')['value'])
                        #
                        ad5.AnomalyShareholdersEquity = int(html.find(id='PRO-1.3.55')['value'])
                        #
                        #
                        # Income Statements - Audit
                        #
                        ad5.GrossMargin = int(html.find(id='PRO-2.1.25')['value'])
                        ad5.OperatingIncome = int(html.find(id='PRO-2.1.55')['value'])
                        ad5.IncomeBeforeTaxes = int(html.find(id='PRO-2.1.85')['value'])
                        ad5.NetIncome = int(html.find(id='PRO-2.1.115')['value'])
                        #
                        ad5.AnomalyGrossMargin = int(html.find(id='PRO-2.2.15')['value'])
                        #
                        ad5.AnomalyOperatingIncome = int(html.find(id='PRO-2.2.25')['value'])
                        #
                        ad5.AnomalyIncomeBeforeTaxes = int(html.find(id='PRO-2.2.35')['value'])
                        #
                        ad5.AnomalyNetIncome = int(html.find(id='PRO-2.2.45')['value'])
                        #
                        #
                        # Comprehensive Income - Audit
                        #
                        ad5.OtherComprehensiveIncome = int(html.find(id='PRO-3.1.25')['value'])
                        #
                        ad5.AnomalyOtherComprehensiveIncome = int(html.find(id='PRO-3.2.15')['value'])
                        #
                        #
                        # Shareholders Equity - Audit
                        #
                        #ad5.ShareholdersEquityBeginning = int(html.find(id='PRO-4.0.25')['value'])
                        #
                        ad5.AnomalyConvertibleDebt = int(html.find(id='PRO-4.2.05')['value'])
                        ad5.AnomalyCommonShares = int(html.find(id='PRO-4.2.15')['value'])
                        ad5.AnomalyRetainedEarnings = int(html.find(id='PRO-4.2.25')['value'])
                        ad5.AnomalyAccumulatedOtherComprehensiveIncome = int(html.find(id='PRO-4.2.35')['value'])
                        ad5.AnomalyTreasuryShares = int(html.find(id='PRO-4.2.45')['value'])
                        ad5.AnomalyEmployeeBenefitTrust = int(html.find(id='PRO-4.2.55')['value'])
                        ad5.AnomalyNonControllingInterests = int(html.find(id='PRO-4.2.65')['value'])
                        #
                        #
                        # Cash Flow - Audit
                        #
                        ad5.CashFlowCashExplainedDifference = int(html.find(id='PRO-5.1.35')['value'])
                        #
                        ad5.AnomalyOperatingActivities = int(html.find(id='PRO-5.2.15')['value'])
                        #
                        ad5.AnomalyInvestingActivities = int(html.find(id='PRO-5.2.25')['value'])
                        #
                        ad5.AnomalyFinancingActivities = int(html.find(id='PRO-5.2.35')['value'])
                        #
                        #
                        # Supplemental - Audit
                        #
                        ad5.TargetWorkingCapital = float(html.find(id='TargetWorkingCapital5')['value'])
                        ad5.ReinvestmentOfMaintenance = int(html.find(id='ReinvestmentOfMaintenance5')['value'])
                        ad5.NormalizedDividendPaymentToNonControllingInterests = int(html.find(id='NormalizedDividendPaymentToNonControllingInterests5')['value'])
                        ad5.NormalizedDividendPaymentToPreferredShareholders = int(html.find(id='NormalizedDividendPaymentToPreferredShareholders5')['value'])
                        ad5.TheoricalInterestRate = float(html.find(id='TheoricalInterestRate5')['value'])
                        ad5.TheoricalTaxRate = float(html.find(id='TheoricalTaxRate5')['value'])
                        ad5.CapitalizationRateFloor = float(html.find(id='CapitalizationRateFloor5')['value'])
                        #
                        ad5.save()
                    except:
                        pass
                    # fifth last year cash flow
                    try:
                        try:
                            cf5 = CashFlow.objects.get(TradingSymbol=ts, Period='fifthlastyear')
                        except:
                            cf5 = CashFlow(TradingSymbol=ts, Period='fifthlastyear')
                        cf5.save()
                        #
                        # General - Cash Flow
                        #
                        cf5.AccessionNumber = e.accessionnumberfifthlastyear
                        cf5.AmendmentFlag = e.amendfifthlastyear
                        cf5.EntityRegistrantName = e.EntityRegistrantName
                        cf5.Period = 'fifthlastyear'
                        cf5.PeriodEndDate = e.fifthlastyear
                        cf5.TradingSymbol = ts
                        #
                        # Cash - Cash Flow
                        #
                        cf5.CashBeginningBalance = int(html.find(id='CashBeginningBalance5')['value'])
                        cf5.EffectOfExchangeRateOnCash = int(html.find(id='EffectOfExchangeRateOnCash5')['value'])
                        #
                        # Operating Activities - Cash Flow
                        #
                        cf5.DepreciationDepletionAndAmortization = int(html.find(id='DepreciationDepletionAndAmortization5')['value'])
                        cf5.GainRelatedToDisposalOrSale = int(html.find(id='GainRelatedToDisposalOrSale5')['value'])
                        cf5.RestructuringAndOtherSpecialCharges = int(html.find(id='RestructuringAndOtherSpecialCharges5')['value'])
                        cf5.AccruedEmployeeCompensation = int(html.find(id='AccruedEmployeeCompensation5')['value'])
                        cf5.ShareBasedCompensation = int(html.find(id='ShareBasedCompensationOperatingActivities5')['value'])
                        cf5.IncreaseDecreaseInIncomeTaxExpenseBenefit = int(html.find(id='IncreaseDecreaseInIncomeTaxExpenseBenefit5')['value'])
                        cf5.OtherNonCashIncomeExpense = int(html.find(id='OtherNonCashIncomeExpense5')['value'])
                        cf5.IncreaseDecreaseInAccountsReceivable = int(html.find(id='IncreaseDecreaseInAccountsReceivable5')['value'])
                        cf5.IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets = int(html.find(id='IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets5')['value'])
                        cf5.IncreaseDecreaseInInventories = int(html.find(id='IncreaseDecreaseInInventories5')['value'])
                        cf5.IncreaseDecreaseInOtherReceivables = int(html.find(id='IncreaseDecreaseInOtherReceivables5')['value'])
                        cf5.IncreaseDecreaseInAccountsPayableAndAccruedLiabilities = int(html.find(id='IncreaseDecreaseInAccountsPayableAndAccruedLiabilities5')['value'])
                        cf5.IncreaseDecreaseInContractWithCustomerLiability = int(html.find(id='IncreaseDecreaseInContractWithCustomerLiability5')['value'])
                        cf5.IncreaseDecreaseInRetirementBenefits = int(html.find(id='IncreaseDecreaseInRetirementBenefits5')['value'])
                        cf5.IncreaseDecreaseFinanceLeaseCurrent = int(html.find(id='IncreaseDecreaseFinanceLeaseCurrent5')['value'])
                        cf5.IncreaseDecreaseOperatingLeaseCurrent = int(html.find(id='IncreaseDecreaseOperatingLeaseCurrent5')['value'])
                        cf5.IncreaseDecreaseInFairValueOfDerivativesOperating = int(html.find(id='IncreaseDecreaseInFairValueOfDerivativesOperating5')['value'])
                        cf5.IncreaseDecreaseInOtherOperatingActivities = int(html.find(id='IncreaseDecreaseInOtherOperatingActivities5')['value'])
                        #
                        # Investing Activities - Cash Flow
                        #
                        cf5.PaymentsToAcquireInvestments = int(html.find(id='PaymentsToAcquireInvestments5')['value'])
                        cf5.ProceedsOfInvestments = int(html.find(id='ProceedsOfInvestments5')['value'])
                        cf5.PaymentsToAcquirePropertyPlantAndEquipment = int(html.find(id='PaymentsToAcquirePropertyPlantAndEquipment5')['value'])
                        cf5.ProceedsFromDisposalsOfPropertyAndEquipment = int(html.find(id='ProceedsFromDisposalsOfPropertyAndEquipment5')['value'])
                        cf5.PaymentsToAcquireBusinessesAndIntangibles = int(html.find(id='PaymentsToAcquireBusinessesAndIntangibles5')['value'])
                        cf5.ProceedsFromDisposalsOfBusinessesAndIntangibles = int(html.find(id='ProceedsFromDisposalsOfBusinessesAndIntangibles5')['value'])
                        cf5.ProceedsRelatedToInsuranceSettlement = int(html.find(id='ProceedsRelatedToInsuranceSettlement5')['value'])
                        cf5.ReveiptOfGovernmentGrants = int(html.find(id='ReveiptOfGovernmentGrants5')['value'])
                        cf5.PaymentOfLicenseFee = int(html.find(id='PaymentOfLicenseFee5')['value'])
                        cf5.InvestingActivitiesInDiscontinuedOperations = int(html.find(id='InvestingActivitiesInDiscontinuedOperations5')['value'])
                        cf5.OtherInvestingActivities = int(html.find(id='OtherInvestingActivities5')['value'])
                        #
                        # Financing Activities - Cash Flow
                        #
                        cf5.FinanceLeasePrincipalPayments = int(html.find(id='FinanceLeasePrincipalPayments5')['value'])
                        cf5.ProceedsFromIssuanceOfCommonShares = int(html.find(id='ProceedsFromIssuanceOfCommonShares5')['value'])
                        cf5.ProceedsFromSharePurchasePlanAndOptionsExercice = int(html.find(id='ProceedsFromSharePurchasePlanAndOptionsExercice5')['value'])
                        cf5.PaymentsRelatedToTaxWithholdingForShareBasedCompensation = int(html.find(id='PaymentsRelatedToTaxWithholdingForShareBasedCompensation5')['value'])
                        cf5.PaymentsForRepurchaseOfCommonShares = int(html.find(id='PaymentsForRepurchaseOfCommonShares5')['value'])
                        cf5.PaymentsOfDividends = int(html.find(id='PaymentsOfDividends5')['value'])
                        cf5.IncreaseDecreaseDeferredContingentConsideration = int(html.find(id='IncreaseDecreaseDeferredContingentConsideration5')['value'])
                        cf5.ProceedsFromIssuanceOfLongTermDebt = int(html.find(id='ProceedsFromIssuanceOfLongTermDebt5')['value'])
                        cf5.RepaymentsOfLongTermDebt = int(html.find(id='RepaymentsOfLongTermDebt5')['value'])
                        cf5.FinancingCosts = int(html.find(id='FinancingCosts5')['value'])
                        cf5.NetChangeInShortTermBorrowings = int(html.find(id='NetChangeInShortTermBorrowings5')['value'])
                        cf5.NetChangeInForwardAndHedgesClassifiedAsFinancingActivities = int(html.find(id='NetChangeInForwardAndHedgesClassifiedAsFinancingActivities5')['value'])
                        cf5.NetChangeInNonControllingInterests = int(html.find(id='NetChangeInNonControllingInterests5')['value'])
                        cf5.ProceedsFromRepaymentsOfCommercialPaper = int(html.find(id='ProceedsFromRepaymentsOfCommercialPaper5')['value'])
                        cf5.RepaymentsOfConvertible = int(html.find(id='RepaymentsOfConvertible5')['value'])
                        cf5.IssuanceOfConvertible = int(html.find(id='IssuanceOfConvertible5')['value'])
                        cf5.EquityInvesteeAdvancesRepayments = int(html.find(id='EquityInvesteeAdvancesRepayments5')['value'])
                        cf5.OtherFinancingActivities = int(html.find(id='OtherFinancingActivities5')['value'])
                        #
                        cf5.save()
                    except:
                        pass
                    # fifth last year trial balance
                    try:
                        try:
                            tb5 = TrialBalance.objects.get(TradingSymbol=ts, Period='fifthlastyear')
                        except:
                            tb5 = TrialBalance(TradingSymbol=ts, Period='fifthlastyear')
                        tb5.save()
                        #
                        # General - Trial Balance
                        #
                        tb5.AccessionNumber = e.accessionnumberfifthlastyear
                        tb5.AmendmentFlag = e.amendfifthlastyear
                        tb5.EntityRegistrantName = e.EntityRegistrantName
                        tb5.Period = 'fifthlastyear'
                        tb5.PeriodEndDate = e.fifthlastyear
                        tb5.TradingSymbol = ts
                        #
                        #
                        # Current Assets - Trial Balance
                        #
                        tb5.Cash = int(html.find(id='TrialBalanceCash5')['value'])
                        tb5.ShortTermInvestments = int(html.find(id='TrialBalanceShortTermInvestments5')['value'])
                        tb5.AccountsReceivable = int(html.find(id='TrialBalanceAccountsReceivable5')['value'])
                        tb5.WorkInProgress = int(html.find(id='TrialBalanceWorkInProgress5')['value'])
                        tb5.Inventories = int(html.find(id='TrialBalanceInventories5')['value'])
                        tb5.PrepaidExpenses = int(html.find(id='TrialBalancePrepaidExpenses5')['value'])
                        tb5.NonTradeReceivables = int(html.find(id='TrialBalanceNonTradeReceivables5')['value'])
                        tb5.PrepaidTaxAssetsCurrent = int(html.find(id='TrialBalancePrepaidTaxAssetsCurrent5')['value'])
                        tb5.DeferredTaxAssetsCurrent = int(html.find(id='TrialBalanceDeferredTaxAssetsCurrent5')['value'])
                        tb5.RightOfUseAssetsCurrent = int(html.find(id='TrialBalanceRightOfUseAssetsCurrent5')['value'])
                        tb5.OtherCurrentAssets = int(html.find(id='TrialBalanceOtherCurrentAssets5')['value'])
                        tb5.DiscontinuedOperationsCurrent = int(html.find(id='TrialBalanceDiscontinuedOperationsCurrent5')['value'])
                        #
                        #
                        # Non-Current Assets - Trial Balance
                        #
                        tb5.LongTermReceivables = int(html.find(id='TrialBalanceLongTermReceivables5')['value'])
                        tb5.DeferredCharges = int(html.find(id='TrialBalanceDeferredCharges5')['value'])
                        tb5.Investments = int(html.find(id='TrialBalanceInvestments5')['value'])
                        tb5.PropertyPlantAndEquipment = int(html.find(id='TrialBalancePropertyPlantAndEquipment5')['value'])
                        tb5.OperatingLeaseRightOfUseAssets = int(html.find(id='TrialBalanceOperatingLeaseRightOfUseAssets5')['value'])
                        tb5.FinanceLeaseRightOfUseAssets = int(html.find(id='TrialBalanceFinanceLeaseRightOfUseAssets5')['value'])
                        tb5.IntangibleAssets = int(html.find(id='TrialBalanceIntangibleAssets5')['value'])
                        tb5.Goodwill = int(html.find(id='TrialBalanceGoodwill5')['value'])
                        tb5.RefundableTaxAssetsNonCurrent = int(html.find(id='TrialBalanceRefundableTaxAssetsNonCurrent5')['value'])
                        tb5.DeferredTaxAssetsNonCurrent = int(html.find(id='TrialBalanceDeferredTaxAssetsNonCurrent5')['value'])
                        tb5.DefinedBenefitPensionAndOtherSimilarPlans = int(html.find(id='TrialBalanceDefinedBenefitPensionAndOtherSimilarPlans5')['value'])
                        tb5.OtherNonCurrentAssets = int(html.find(id='TrialBalanceOtherNonCurrentAssets5')['value'])
                        tb5.DiscontinuedOperations = int(html.find(id='TrialBalanceDiscontinuedOperations5')['value'])
                        #
                        #
                        # Current Liabilities - Trial Balance
                        #
                        tb5.AccountsPayableAndAccruedLiabilities = int(html.find(id='TrialBalanceAccountsPayableAndAccruedLiabilities5')['value'])
                        tb5.EmployeeCompensationCurrent = int(html.find(id='TrialBalanceEmployeeCompensationCurrent5')['value'])
                        tb5.OperatingLeasesCurrent = int(html.find(id='TrialBalanceOperatingLeasesCurrent5')['value'])
                        tb5.FinanceLeasesCurrent = int(html.find(id='TrialBalanceFinanceLeasesCurrent5')['value'])
                        tb5.DeferredRevenueAndDepositsCurrent = int(html.find(id='TrialBalanceDeferredRevenueAndDepositsCurrent5')['value'])
                        tb5.AccruedTaxLiabilities = int(html.find(id='TrialBalanceAccruedTaxLiabilities5')['value'])
                        tb5.DeferredTaxLiabilitiesCurrent = int(html.find(id='TrialBalanceDeferredTaxLiabilitiesCurrent5')['value'])
                        tb5.CommercialPapers = int(html.find(id='TrialBalanceCommercialPapers5')['value'])
                        tb5.ShortTermBorrowings = int(html.find(id='TrialBalanceShortTermBorrowings5')['value'])
                        tb5.OtherCurrentLiabilities = int(html.find(id='TrialBalanceOtherCurrentLiabilities5')['value'])
                        tb5.DiscontinuedOperationsLiabilitiesCurrent = int(html.find(id='TrialBalanceDiscontinuedOperationsLiabilitiesCurrent5')['value'])
                        tb5.DividendsPayable = int(html.find(id='TrialBalanceDividendsPayable5')['value'])
                        tb5.ShortTermPortionOfLongTermDebt = int(html.find(id='TrialBalanceShortTermPortionOfLongTermDebt5')['value'])
                        #
                        #
                        # Non-Current Liabilities - Trial Balance
                        #
                        tb5.LongTermDebt = int(html.find(id='TrialBalanceLongTermDebt5')['value'])
                        tb5.PreferredSharesLiability = int(html.find(id='TrialBalancePreferredSharesLiability5')['value'])
                        tb5.RetirementBenefits = int(html.find(id='TrialBalanceRetirementBenefits5')['value'])
                        tb5.OperatingLeasesNonCurrent = int(html.find(id='TrialBalanceOperatingLeasesNonCurrent5')['value'])
                        tb5.FinanceLeasesNonCurrent = int(html.find(id='TrialBalanceFinanceLeasesNonCurrent5')['value'])
                        tb5.LeaseIncentiveObligation = int(html.find(id='TrialBalanceLeaseIncentiveObligation5')['value'])
                        tb5.DeferredRevenueAndDepositsNonCurrent = int(html.find(id='TrialBalanceDeferredRevenueAndDepositsNonCurrent5')['value'])
                        tb5.ContingentConsideration = int(html.find(id='TrialBalanceContingentConsideration5')['value'])
                        tb5.AccruedTaxLiabilitiesNonCurrent = int(html.find(id='TrialBalanceAccruedTaxLiabilitiesNonCurrent5')['value'])
                        tb5.DeferredTaxLiabilitiesNonCurrent = int(html.find(id='TrialBalanceDeferredTaxLiabilitiesNonCurrent5')['value'])
                        tb5.OtherNonCurrentLiabilities = int(html.find(id='TrialBalanceOtherNonCurrentLiabilities5')['value'])
                        tb5.RedeemableNonControllingInterests = int(html.find(id='TrialBalanceRedeemableNonControllingInterests5')['value'])
                        tb5.DiscontinuedOperationsLiabilitiesNonCurrent = int(html.find(id='TrialBalanceDiscontinuedOperationsLiabilitiesNonCurrent5')['value'])
                        #
                        #
                        # Shareholders Equity - Trial Balance
                        #
                        # convertible debt
                        tb5.ConvertibleDebtBeginning = int(html.find(id='TrialBalanceConvertibleDebt5')['value'])
                        #
                        # common shares
                        tb5.CommonSharesBeginning = int(html.find(id='TrialBalanceCommonShares5')['value'])
                        tb5.CommonSharesIssued = int(html.find(id='TrialBalanceCommonSharesIssued5')['value'])
                        tb5.ShareBasedCompensation = int(html.find(id='TrialBalanceShareBasedCompensation5')['value'])
                        #
                        # preferred shares
                        try:
                            tb5.PreferredSharesBeginning = int(html.find(id='TrialBalancePreferredShares5')['value'])
                        except:
                            pass
                        #
                        # retained earnings
                        tb5.RetainedEarningsBeginning = int(html.find(id='TrialBalanceRetainedEarningsAccumulatedDeficit5')['value'])
                        tb5.DividendsAndDividendEquivalentsDeclared = int(html.find(id='TrialBalanceDividendsAndDividendEquivalentsDeclared5')['value'])
                        tb5.CommonSharesRepurchasedAndRetired = int(html.find(id='TrialBalanceCommonSharesRepurchasedAndRetired5')['value'])
                        tb5.ShareBasedCompensationRetainedEarnings = int(html.find(id='TrialBalanceShareBasedCompensationRetainedEarnings5')['value'])
                        tb5.EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts = int(html.find(id='TrialBalanceEffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts5')['value'])
                        tb5.RetainedEarningsOthers = int(html.find(id='TrialBalanceRetainedEarningsOthers5')['value'])
                        #
                        # accumulated other comprehensive income
                        tb5.AccumulatedOtherComprehensiveIncomeBeginning = int(html.find(id='TrialBalanceAccumulatedOtherComprehensiveIncomeLoss5')['value'])
                        #
                        # treasury shares
                        tb5.TreasurySharesBeginning = int(html.find(id='TrialBalanceTreasuryShares5')['value'])
                        tb5.PurchaseAndSellOfTreasuryShares = int(html.find(id='TrialBalancePurchaseAndSellOfTreasuryShares5')['value'])
                        #
                        # employee benefit trust
                        tb5.EmployeeBenefitTrustBeginning = int(html.find(id='TrialBalanceEmployeeBenefitTrust5')['value'])
                        #
                        # non controlling interests
                        tb5.NonControllingInterestsBeginning = int(html.find(id='TrialBalanceNonControllingInterests5')['value'])
                        tb5.DividendsDeclaredToNonControllingInterests = int(html.find(id='TrialBalanceDividendsDeclaredToNonControllingInterests5')['value'])
                        tb5.AcquisitionOfNonControllingInterests = int(html.find(id='TrialBalanceAcquisitionOfNonControllingInterests5')['value'])
                        tb5.NonControllingInterestsOthers = int(html.find(id='TrialBalanceNonControllingInterestsOthers5')['value'])
                        #
                        #
                        # Income Statements - Trial Balance
                        #
                        tb5.Sales = int(html.find(id='TrialBalanceSales5')['value'])
                        tb5.CostOfSales = int(html.find(id='TrialBalanceCostOfSales5')['value'])
                        tb5.ResearchAndDevelopment = int(html.find(id='TrialBalanceResearchAndDevelopment5')['value'])
                        tb5.SellingGeneralAdministrativeAndMarketing = int(html.find(id='TrialBalanceSellingGeneralAdministrativeAndMarketing5')['value'])
                        tb5.ImpairmentRestructuringAndOtherSpecialCharges = int(html.find(id='TrialBalanceImpairmentRestructuringAndOtherSpecialCharges5')['value'])
                        tb5.NonOperatingIncome = int(html.find(id='TrialBalanceNonOperatingIncomeExpense5')['value'])
                        tb5.IncomeTaxExpenseBenefit = int(html.find(id='TrialBalanceIncomeTaxExpenseBenefit5')['value'])
                        tb5.EquityMethodInvesteesIncome = int(html.find(id='TrialBalanceEquityMethodInvesteesIncome5')['value'])
                        tb5.NetIncomeFromDiscontinuedOperations = int(html.find(id='TrialBalanceNetIncomeFromDiscontinuedOperations5')['value'])
                        #
                        #
                        # Other Comprehensive Income - Trial Balance
                        #
                        tb5.ChangeInForeignCurrencyTranslationAdjustment = int(html.find(id='TrialBalanceChangeInForeignCurrencyTranslationAdjustment5')['value'])
                        tb5.ChangeInUnrealizedGainsLossesOnDerivativeInstruments = int(html.find(id='TrialBalanceChangeInUnrealizedGainsLossesOnDerivativeInstruments5')['value'])
                        tb5.ChangeInUnrealizedGainsLossesOnInvestments = int(html.find(id='TrialBalanceChangeInUnrealizedGainsLossesOnInvestments5')['value'])
                        tb5.ChangeInDefinedBenefitPensionAndOtherSimilarPlans = int(html.find(id='TrialBalanceChangeInDefinedBenefitPensionAndOtherSimilarPlans5')['value'])
                        tb5.IncomeTaxOnOtherComprehensiveIncome = int(html.find(id='TrialBalanceIncomeTaxOnOtherComprehensiveIncome5')['value'])
                        #
                        tb5.save()
                    except:
                        pass
                except:
                    pass
                # sixth last year
                try:
                    # sixth last year audit
                    try:
                        try:
                            ad6 = AuditData.objects.get(TradingSymbol=ts, Period='sixthlastyear')
                        except:
                            ad6 = AuditData(TradingSymbol=ts, Period='sixthlastyear')
                        ad6.save()
                        #
                        # General - Audit
                        #
                        ad6.db = int(html.find(id='Status6')['value'])
                        ad6.AccessionNumber = e.accessionnumbersixthlastyear
                        ad6.AmendmentFlag = e.amendsixthlastyear
                        ad6.EntityRegistrantName = e.EntityRegistrantName
                        ad6.Period = 'sixthlastyear'
                        ad6.PeriodEndDate = e.sixthlastyear
                        ad6.TradingSymbol = ts
                        #
                        # Balance Sheets - Audit
                        #
                        ad6.CurrentAssets = int(html.find(id='PRO-1.2.26')['value'])
                        ad6.NonCurrentAssets = int(html.find(id='PRO-1.2.56')['value'])
                        ad6.CurrentLiabilities = int(html.find(id='PRO-1.2.86')['value'])
                        ad6.NonCurrentLiabilities = int(html.find(id='PRO-1.2.116')['value'])
                        ad6.ShareholdersEquity = int(html.find(id='PRO-1.2.146')['value'])
                        #ad6.LiabilitiesAndShareholdersEquity = int(html.find(id='PRO-1.1.26')['value'])
                        #
                        ad6.AnomalyCurrentAssets = int(html.find(id='PRO-1.3.16')['value'])
                        #
                        ad6.AnomalyNonCurrentAssets = int(html.find(id='PRO-1.3.26')['value'])
                        #
                        ad6.AnomalyCurrentLiabilities = int(html.find(id='PRO-1.3.36')['value'])
                        #
                        ad6.AnomalyNonCurrentLiabilities = int(html.find(id='PRO-1.3.46')['value'])
                        #
                        ad6.AnomalyShareholdersEquity = int(html.find(id='PRO-1.3.56')['value'])
                        #
                        #
                        # Income Statements - Audit
                        #
                        ad6.GrossMargin = int(html.find(id='PRO-2.1.26')['value'])
                        ad6.OperatingIncome = int(html.find(id='PRO-2.1.56')['value'])
                        ad6.IncomeBeforeTaxes = int(html.find(id='PRO-2.1.86')['value'])
                        ad6.NetIncome = int(html.find(id='PRO-2.1.116')['value'])
                        #
                        ad6.AnomalyGrossMargin = int(html.find(id='PRO-2.2.16')['value'])
                        #
                        ad6.AnomalyOperatingIncome = int(html.find(id='PRO-2.2.26')['value'])
                        #
                        ad6.AnomalyIncomeBeforeTaxes = int(html.find(id='PRO-2.2.36')['value'])
                        #
                        ad6.AnomalyNetIncome = int(html.find(id='PRO-2.2.46')['value'])
                        #
                        #
                        # Comprehensive Income - Audit
                        #
                        ad6.OtherComprehensiveIncome = int(html.find(id='PRO-3.1.26')['value'])
                        #
                        ad6.AnomalyOtherComprehensiveIncome = int(html.find(id='PRO-3.2.16')['value'])
                        #
                        #
                        # Shareholders Equity - Audit
                        #
                        #ad6.ShareholdersEquityBeginning = int(html.find(id='PRO-4.0.26')['value'])
                        #
                        ad6.AnomalyConvertibleDebt = int(html.find(id='PRO-4.2.06')['value'])
                        ad6.AnomalyCommonShares = int(html.find(id='PRO-4.2.16')['value'])
                        ad6.AnomalyRetainedEarnings = int(html.find(id='PRO-4.2.26')['value'])
                        ad6.AnomalyAccumulatedOtherComprehensiveIncome = int(html.find(id='PRO-4.2.36')['value'])
                        ad6.AnomalyTreasuryShares = int(html.find(id='PRO-4.2.46')['value'])
                        ad6.AnomalyEmployeeBenefitTrust = int(html.find(id='PRO-4.2.56')['value'])
                        ad6.AnomalyNonControllingInterests = int(html.find(id='PRO-4.2.66')['value'])
                        #
                        #
                        # Cash Flow - Audit
                        #
                        ad6.CashFlowCashExplainedDifference = int(html.find(id='PRO-5.1.36')['value'])
                        #
                        ad6.AnomalyOperatingActivities = int(html.find(id='PRO-5.2.16')['value'])
                        #
                        ad6.AnomalyInvestingActivities = int(html.find(id='PRO-5.2.26')['value'])
                        #
                        ad6.AnomalyFinancingActivities = int(html.find(id='PRO-5.2.36')['value'])
                        #
                        #
                        # Supplemental - Audit
                        #
                        ad6.TargetWorkingCapital = float(html.find(id='TargetWorkingCapital6')['value'])
                        ad6.ReinvestmentOfMaintenance = int(html.find(id='ReinvestmentOfMaintenance6')['value'])
                        ad6.NormalizedDividendPaymentToNonControllingInterests = int(html.find(id='NormalizedDividendPaymentToNonControllingInterests6')['value'])
                        ad6.NormalizedDividendPaymentToPreferredShareholders = int(html.find(id='NormalizedDividendPaymentToPreferredShareholders6')['value'])
                        ad6.TheoricalInterestRate = float(html.find(id='TheoricalInterestRate6')['value'])
                        ad6.TheoricalTaxRate = float(html.find(id='TheoricalTaxRate6')['value'])
                        ad6.CapitalizationRateFloor = float(html.find(id='CapitalizationRateFloor6')['value'])
                        #
                        ad6.save()
                    except:
                        pass
                    # sixth last year cash flow
                    try:
                        try:
                            cf6 = CashFlow.objects.get(TradingSymbol=ts, Period='sixthlastyear')
                        except:
                            cf6 = CashFlow(TradingSymbol=ts, Period='sixthlastyear')
                        cf6.save()
                        #
                        # General - Cash Flow
                        #
                        cf6.AccessionNumber = e.accessionnumbersixthlastyear
                        cf6.AmendmentFlag = e.amendsixthlastyear
                        cf6.EntityRegistrantName = e.EntityRegistrantName
                        cf6.Period = 'sixthlastyear'
                        cf6.PeriodEndDate = e.sixthlastyear
                        cf6.TradingSymbol = ts
                        #
                        # Cash - Cash Flow
                        #
                        cf6.CashBeginningBalance = int(html.find(id='CashBeginningBalance6')['value'])
                        cf6.EffectOfExchangeRateOnCash = int(html.find(id='EffectOfExchangeRateOnCash6')['value'])
                        #
                        # Operating Activities - Cash Flow
                        #
                        cf6.DepreciationDepletionAndAmortization = int(html.find(id='DepreciationDepletionAndAmortization6')['value'])
                        cf6.GainRelatedToDisposalOrSale = int(html.find(id='GainRelatedToDisposalOrSale6')['value'])
                        cf6.RestructuringAndOtherSpecialCharges = int(html.find(id='RestructuringAndOtherSpecialCharges6')['value'])
                        cf6.AccruedEmployeeCompensation = int(html.find(id='AccruedEmployeeCompensation6')['value'])
                        cf6.ShareBasedCompensation = int(html.find(id='ShareBasedCompensationOperatingActivities6')['value'])
                        cf6.IncreaseDecreaseInIncomeTaxExpenseBenefit = int(html.find(id='IncreaseDecreaseInIncomeTaxExpenseBenefit6')['value'])
                        cf6.OtherNonCashIncomeExpense = int(html.find(id='OtherNonCashIncomeExpense6')['value'])
                        cf6.IncreaseDecreaseInAccountsReceivable = int(html.find(id='IncreaseDecreaseInAccountsReceivable6')['value'])
                        cf6.IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets = int(html.find(id='IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets6')['value'])
                        cf6.IncreaseDecreaseInInventories = int(html.find(id='IncreaseDecreaseInInventories6')['value'])
                        cf6.IncreaseDecreaseInOtherReceivables = int(html.find(id='IncreaseDecreaseInOtherReceivables6')['value'])
                        cf6.IncreaseDecreaseInAccountsPayableAndAccruedLiabilities = int(html.find(id='IncreaseDecreaseInAccountsPayableAndAccruedLiabilities6')['value'])
                        cf6.IncreaseDecreaseInContractWithCustomerLiability = int(html.find(id='IncreaseDecreaseInContractWithCustomerLiability6')['value'])
                        cf6.IncreaseDecreaseInRetirementBenefits = int(html.find(id='IncreaseDecreaseInRetirementBenefits6')['value'])
                        cf6.IncreaseDecreaseFinanceLeaseCurrent = int(html.find(id='IncreaseDecreaseFinanceLeaseCurrent6')['value'])
                        cf6.IncreaseDecreaseOperatingLeaseCurrent = int(html.find(id='IncreaseDecreaseOperatingLeaseCurrent6')['value'])
                        cf6.IncreaseDecreaseInFairValueOfDerivativesOperating = int(html.find(id='IncreaseDecreaseInFairValueOfDerivativesOperating6')['value'])
                        cf6.IncreaseDecreaseInOtherOperatingActivities = int(html.find(id='IncreaseDecreaseInOtherOperatingActivities6')['value'])
                        #
                        # Investing Activities - Cash Flow
                        #
                        cf6.PaymentsToAcquireInvestments = int(html.find(id='PaymentsToAcquireInvestments6')['value'])
                        cf6.ProceedsOfInvestments = int(html.find(id='ProceedsOfInvestments6')['value'])
                        cf6.PaymentsToAcquirePropertyPlantAndEquipment = int(html.find(id='PaymentsToAcquirePropertyPlantAndEquipment6')['value'])
                        cf6.ProceedsFromDisposalsOfPropertyAndEquipment = int(html.find(id='ProceedsFromDisposalsOfPropertyAndEquipment6')['value'])
                        cf6.PaymentsToAcquireBusinessesAndIntangibles = int(html.find(id='PaymentsToAcquireBusinessesAndIntangibles6')['value'])
                        cf6.ProceedsFromDisposalsOfBusinessesAndIntangibles = int(html.find(id='ProceedsFromDisposalsOfBusinessesAndIntangibles6')['value'])
                        cf6.ProceedsRelatedToInsuranceSettlement = int(html.find(id='ProceedsRelatedToInsuranceSettlement6')['value'])
                        cf6.ReveiptOfGovernmentGrants = int(html.find(id='ReveiptOfGovernmentGrants6')['value'])
                        cf6.PaymentOfLicenseFee = int(html.find(id='PaymentOfLicenseFee6')['value'])
                        cf6.InvestingActivitiesInDiscontinuedOperations = int(html.find(id='InvestingActivitiesInDiscontinuedOperations6')['value'])
                        cf6.OtherInvestingActivities = int(html.find(id='OtherInvestingActivities6')['value'])
                        #
                        # Financing Activities - Cash Flow
                        #
                        cf6.FinanceLeasePrincipalPayments = int(html.find(id='FinanceLeasePrincipalPayments6')['value'])
                        cf6.ProceedsFromIssuanceOfCommonShares = int(html.find(id='ProceedsFromIssuanceOfCommonShares6')['value'])
                        cf6.ProceedsFromSharePurchasePlanAndOptionsExercice = int(html.find(id='ProceedsFromSharePurchasePlanAndOptionsExercice6')['value'])
                        cf6.PaymentsRelatedToTaxWithholdingForShareBasedCompensation = int(html.find(id='PaymentsRelatedToTaxWithholdingForShareBasedCompensation6')['value'])
                        cf6.PaymentsForRepurchaseOfCommonShares = int(html.find(id='PaymentsForRepurchaseOfCommonShares6')['value'])
                        cf6.PaymentsOfDividends = int(html.find(id='PaymentsOfDividends6')['value'])
                        cf6.IncreaseDecreaseDeferredContingentConsideration = int(html.find(id='IncreaseDecreaseDeferredContingentConsideration6')['value'])
                        cf6.ProceedsFromIssuanceOfLongTermDebt = int(html.find(id='ProceedsFromIssuanceOfLongTermDebt6')['value'])
                        cf6.RepaymentsOfLongTermDebt = int(html.find(id='RepaymentsOfLongTermDebt6')['value'])
                        cf6.FinancingCosts = int(html.find(id='FinancingCosts6')['value'])
                        cf6.NetChangeInShortTermBorrowings = int(html.find(id='NetChangeInShortTermBorrowings6')['value'])
                        cf6.NetChangeInForwardAndHedgesClassifiedAsFinancingActivities = int(html.find(id='NetChangeInForwardAndHedgesClassifiedAsFinancingActivities6')['value'])
                        cf6.NetChangeInNonControllingInterests = int(html.find(id='NetChangeInNonControllingInterests6')['value'])
                        cf6.ProceedsFromRepaymentsOfCommercialPaper = int(html.find(id='ProceedsFromRepaymentsOfCommercialPaper6')['value'])
                        cf6.RepaymentsOfConvertible = int(html.find(id='RepaymentsOfConvertible6')['value'])
                        cf6.IssuanceOfConvertible = int(html.find(id='IssuanceOfConvertible6')['value'])
                        cf6.EquityInvesteeAdvancesRepayments = int(html.find(id='EquityInvesteeAdvancesRepayments6')['value'])
                        cf6.OtherFinancingActivities = int(html.find(id='OtherFinancingActivities6')['value'])
                        #
                        cf6.save()
                    except:
                        pass
                    # sixth last year trial balance
                    try:
                        try:
                            tb6 = TrialBalance.objects.get(TradingSymbol=ts, Period='sixthlastyear')
                        except:
                            tb6 = TrialBalance(TradingSymbol=ts, Period='sixthlastyear')
                        tb6.save()
                        #
                        # General - Trial Balance
                        #
                        tb6.AccessionNumber = e.accessionnumbersixthlastyear
                        tb6.AmendmentFlag = e.amendsixthlastyear
                        tb6.EntityRegistrantName = e.EntityRegistrantName
                        tb6.Period = 'sixthlastyear'
                        tb6.PeriodEndDate = e.sixthlastyear
                        tb6.TradingSymbol = ts
                        #
                        #
                        # Current Assets - Trial Balance
                        #
                        tb6.Cash = int(html.find(id='TrialBalanceCash6')['value'])
                        tb6.ShortTermInvestments = int(html.find(id='TrialBalanceShortTermInvestments6')['value'])
                        tb6.AccountsReceivable = int(html.find(id='TrialBalanceAccountsReceivable6')['value'])
                        tb6.WorkInProgress = int(html.find(id='TrialBalanceWorkInProgress6')['value'])
                        tb6.Inventories = int(html.find(id='TrialBalanceInventories6')['value'])
                        tb6.PrepaidExpenses = int(html.find(id='TrialBalancePrepaidExpenses6')['value'])
                        tb6.NonTradeReceivables = int(html.find(id='TrialBalanceNonTradeReceivables6')['value'])
                        tb6.PrepaidTaxAssetsCurrent = int(html.find(id='TrialBalancePrepaidTaxAssetsCurrent6')['value'])
                        tb6.DeferredTaxAssetsCurrent = int(html.find(id='TrialBalanceDeferredTaxAssetsCurrent6')['value'])
                        tb6.RightOfUseAssetsCurrent = int(html.find(id='TrialBalanceRightOfUseAssetsCurrent6')['value'])
                        tb6.OtherCurrentAssets = int(html.find(id='TrialBalanceOtherCurrentAssets6')['value'])
                        tb6.DiscontinuedOperationsCurrent = int(html.find(id='TrialBalanceDiscontinuedOperationsCurrent6')['value'])
                        #
                        #
                        # Non-Current Assets - Trial Balance
                        #
                        tb6.LongTermReceivables = int(html.find(id='TrialBalanceLongTermReceivables6')['value'])
                        tb6.DeferredCharges = int(html.find(id='TrialBalanceDeferredCharges6')['value'])
                        tb6.Investments = int(html.find(id='TrialBalanceInvestments6')['value'])
                        tb6.PropertyPlantAndEquipment = int(html.find(id='TrialBalancePropertyPlantAndEquipment6')['value'])
                        tb6.OperatingLeaseRightOfUseAssets = int(html.find(id='TrialBalanceOperatingLeaseRightOfUseAssets6')['value'])
                        tb6.FinanceLeaseRightOfUseAssets = int(html.find(id='TrialBalanceFinanceLeaseRightOfUseAssets6')['value'])
                        tb6.IntangibleAssets = int(html.find(id='TrialBalanceIntangibleAssets6')['value'])
                        tb6.Goodwill = int(html.find(id='TrialBalanceGoodwill6')['value'])
                        tb6.RefundableTaxAssetsNonCurrent = int(html.find(id='TrialBalanceRefundableTaxAssetsNonCurrent6')['value'])
                        tb6.DeferredTaxAssetsNonCurrent = int(html.find(id='TrialBalanceDeferredTaxAssetsNonCurrent6')['value'])
                        tb6.DefinedBenefitPensionAndOtherSimilarPlans = int(html.find(id='TrialBalanceDefinedBenefitPensionAndOtherSimilarPlans6')['value'])
                        tb6.OtherNonCurrentAssets = int(html.find(id='TrialBalanceOtherNonCurrentAssets6')['value'])
                        tb6.DiscontinuedOperations = int(html.find(id='TrialBalanceDiscontinuedOperations6')['value'])
                        #
                        #
                        # Current Liabilities - Trial Balance
                        #
                        tb6.AccountsPayableAndAccruedLiabilities = int(html.find(id='TrialBalanceAccountsPayableAndAccruedLiabilities6')['value'])
                        tb6.EmployeeCompensationCurrent = int(html.find(id='TrialBalanceEmployeeCompensationCurrent6')['value'])
                        tb6.OperatingLeasesCurrent = int(html.find(id='TrialBalanceOperatingLeasesCurrent6')['value'])
                        tb6.FinanceLeasesCurrent = int(html.find(id='TrialBalanceFinanceLeasesCurrent6')['value'])
                        tb6.DeferredRevenueAndDepositsCurrent = int(html.find(id='TrialBalanceDeferredRevenueAndDepositsCurrent6')['value'])
                        tb6.AccruedTaxLiabilities = int(html.find(id='TrialBalanceAccruedTaxLiabilities6')['value'])
                        tb6.DeferredTaxLiabilitiesCurrent = int(html.find(id='TrialBalanceDeferredTaxLiabilitiesCurrent6')['value'])
                        tb6.CommercialPapers = int(html.find(id='TrialBalanceCommercialPapers6')['value'])
                        tb6.ShortTermBorrowings = int(html.find(id='TrialBalanceShortTermBorrowings6')['value'])
                        tb6.OtherCurrentLiabilities = int(html.find(id='TrialBalanceOtherCurrentLiabilities6')['value'])
                        tb6.DiscontinuedOperationsLiabilitiesCurrent = int(html.find(id='TrialBalanceDiscontinuedOperationsLiabilitiesCurrent6')['value'])
                        tb6.DividendsPayable = int(html.find(id='TrialBalanceDividendsPayable6')['value'])
                        tb6.ShortTermPortionOfLongTermDebt = int(html.find(id='TrialBalanceShortTermPortionOfLongTermDebt6')['value'])
                        #
                        #
                        # Non-Current Liabilities - Trial Balance
                        #
                        tb6.LongTermDebt = int(html.find(id='TrialBalanceLongTermDebt6')['value'])
                        tb6.PreferredSharesLiability = int(html.find(id='TrialBalancePreferredSharesLiability6')['value'])
                        tb6.RetirementBenefits = int(html.find(id='TrialBalanceRetirementBenefits6')['value'])
                        tb6.OperatingLeasesNonCurrent = int(html.find(id='TrialBalanceOperatingLeasesNonCurrent6')['value'])
                        tb6.FinanceLeasesNonCurrent = int(html.find(id='TrialBalanceFinanceLeasesNonCurrent6')['value'])
                        tb6.LeaseIncentiveObligation = int(html.find(id='TrialBalanceLeaseIncentiveObligation6')['value'])
                        tb6.DeferredRevenueAndDepositsNonCurrent = int(html.find(id='TrialBalanceDeferredRevenueAndDepositsNonCurrent6')['value'])
                        tb6.ContingentConsideration = int(html.find(id='TrialBalanceContingentConsideration6')['value'])
                        tb6.AccruedTaxLiabilitiesNonCurrent = int(html.find(id='TrialBalanceAccruedTaxLiabilitiesNonCurrent6')['value'])
                        tb6.DeferredTaxLiabilitiesNonCurrent = int(html.find(id='TrialBalanceDeferredTaxLiabilitiesNonCurrent6')['value'])
                        tb6.OtherNonCurrentLiabilities = int(html.find(id='TrialBalanceOtherNonCurrentLiabilities6')['value'])
                        tb6.RedeemableNonControllingInterests = int(html.find(id='TrialBalanceRedeemableNonControllingInterests6')['value'])
                        tb6.DiscontinuedOperationsLiabilitiesNonCurrent = int(html.find(id='TrialBalanceDiscontinuedOperationsLiabilitiesNonCurrent6')['value'])
                        #
                        #
                        # Shareholders Equity - Trial Balance
                        #
                        # convertible debt
                        tb6.ConvertibleDebtBeginning = int(html.find(id='TrialBalanceConvertibleDebt6')['value'])
                        #
                        # common shares
                        tb6.CommonSharesBeginning = int(html.find(id='TrialBalanceCommonShares6')['value'])
                        tb6.CommonSharesIssued = int(html.find(id='TrialBalanceCommonSharesIssued6')['value'])
                        tb6.ShareBasedCompensation = int(html.find(id='TrialBalanceShareBasedCompensation6')['value'])
                        #
                        # preferred shares
                        try:
                            tb6.PreferredSharesBeginning = int(html.find(id='TrialBalancePreferredShares6')['value'])
                        except:
                            pass
                        #
                        # retained earnings
                        tb6.RetainedEarningsBeginning = int(html.find(id='TrialBalanceRetainedEarningsAccumulatedDeficit6')['value'])
                        tb6.DividendsAndDividendEquivalentsDeclared = int(html.find(id='TrialBalanceDividendsAndDividendEquivalentsDeclared6')['value'])
                        tb6.CommonSharesRepurchasedAndRetired = int(html.find(id='TrialBalanceCommonSharesRepurchasedAndRetired6')['value'])
                        tb6.ShareBasedCompensationRetainedEarnings = int(html.find(id='TrialBalanceShareBasedCompensationRetainedEarnings6')['value'])
                        tb6.EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts = int(html.find(id='TrialBalanceEffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts6')['value'])
                        tb6.RetainedEarningsOthers = int(html.find(id='TrialBalanceRetainedEarningsOthers6')['value'])
                        #
                        # accumulated other comprehensive income
                        tb6.AccumulatedOtherComprehensiveIncomeBeginning = int(html.find(id='TrialBalanceAccumulatedOtherComprehensiveIncomeLoss6')['value'])
                        #
                        # treasury shares
                        tb6.TreasurySharesBeginning = int(html.find(id='TrialBalanceTreasuryShares6')['value'])
                        tb6.PurchaseAndSellOfTreasuryShares = int(html.find(id='TrialBalancePurchaseAndSellOfTreasuryShares6')['value'])
                        #
                        # employee benefit trust
                        tb6.EmployeeBenefitTrustBeginning = int(html.find(id='TrialBalanceEmployeeBenefitTrust6')['value'])
                        #
                        # non controlling interests
                        tb6.NonControllingInterestsBeginning = int(html.find(id='TrialBalanceNonControllingInterests6')['value'])
                        tb6.DividendsDeclaredToNonControllingInterests = int(html.find(id='TrialBalanceDividendsDeclaredToNonControllingInterests6')['value'])
                        tb6.AcquisitionOfNonControllingInterests = int(html.find(id='TrialBalanceAcquisitionOfNonControllingInterests6')['value'])
                        tb6.NonControllingInterestsOthers = int(html.find(id='TrialBalanceNonControllingInterestsOthers6')['value'])
                        #
                        #
                        # Income Statements - Trial Balance
                        #
                        tb6.Sales = int(html.find(id='TrialBalanceSales6')['value'])
                        tb6.CostOfSales = int(html.find(id='TrialBalanceCostOfSales6')['value'])
                        tb6.ResearchAndDevelopment = int(html.find(id='TrialBalanceResearchAndDevelopment6')['value'])
                        tb6.SellingGeneralAdministrativeAndMarketing = int(html.find(id='TrialBalanceSellingGeneralAdministrativeAndMarketing6')['value'])
                        tb6.ImpairmentRestructuringAndOtherSpecialCharges = int(html.find(id='TrialBalanceImpairmentRestructuringAndOtherSpecialCharges6')['value'])
                        tb6.NonOperatingIncome = int(html.find(id='TrialBalanceNonOperatingIncomeExpense6')['value'])
                        tb6.IncomeTaxExpenseBenefit = int(html.find(id='TrialBalanceIncomeTaxExpenseBenefit6')['value'])
                        tb6.EquityMethodInvesteesIncome = int(html.find(id='TrialBalanceEquityMethodInvesteesIncome6')['value'])
                        tb6.NetIncomeFromDiscontinuedOperations = int(html.find(id='TrialBalanceNetIncomeFromDiscontinuedOperations6')['value'])
                        #
                        #
                        # Other Comprehensive Income - Trial Balance
                        #
                        tb6.ChangeInForeignCurrencyTranslationAdjustment = int(html.find(id='TrialBalanceChangeInForeignCurrencyTranslationAdjustment6')['value'])
                        tb6.ChangeInUnrealizedGainsLossesOnDerivativeInstruments = int(html.find(id='TrialBalanceChangeInUnrealizedGainsLossesOnDerivativeInstruments6')['value'])
                        tb6.ChangeInUnrealizedGainsLossesOnInvestments = int(html.find(id='TrialBalanceChangeInUnrealizedGainsLossesOnInvestments6')['value'])
                        tb6.ChangeInDefinedBenefitPensionAndOtherSimilarPlans = int(html.find(id='TrialBalanceChangeInDefinedBenefitPensionAndOtherSimilarPlans6')['value'])
                        tb6.IncomeTaxOnOtherComprehensiveIncome = int(html.find(id='TrialBalanceIncomeTaxOnOtherComprehensiveIncome6')['value'])
                        #
                        tb6.save()
                    except:
                        pass
                except:
                    pass
                # stage
                try:
                    e.db = 1
                except:
                    pass
                # Time Of Update
                try:
                    now = datetime.datetime.now()
                    e.SEC_Update = now
                except:
                    pass
                print(ts)
                print(now)
                print(137*'-' + '\n')
                e.save()
        except:
            pass
    i = i + 1




