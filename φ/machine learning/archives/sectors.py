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

entities = Entity.objects.all().order_by('db').filter(Industry_db=22)

############################################

db = 0

ll = 1
ll = len(entities)

for count in range(0, ll):
    #
    #
    e = entities[count]
    #
    #
    if ll == 1:
        e = Entity.objects.get(TradingSymbol='BW')
    #
    #
    i = e.Industry_SEC
    #
    #
    aaa = 'Art, Sports & Culture'
    try:
        #
        aa = [
            'Amusement & Recreation',
            'Art & Photography',
            'Artist',
            ' Book ',
            ' Books ',
            'Dolls & Stuffed Toys',
            'Jewelry',
            'Clockwork',
            'Newspapers',
            'Membership Organizations',
            'Motion Picture',
            'Musical',
            'Photofinishing Laborator',
            'Picture Theatres',
            'Publishing',
            'Phonograph',
            'Precious Metal',
            'Printing',
            'Racing',
            'Sporting',
            'Sports & Recreation',
            'Toys',
            'Video Tape Rental',

        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 3
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Aeronautical'
    try:
        #
        aa = [
            'Aeronautic',
            'Boat',
            'Ship',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 1
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Automobile & Motor Vehicules'
    try:
        #
        aa = [
            'Automobile',
            'Automotiv',
            'Bicycles',
            'Bus ',
            'Mobile Homes',
            'Motor Homes',
            'Motorcycles',
            'Motor Vehic',
            'Truck ',
            'Vehicule',
        ]
        bb = [
            'Games',
        ]
        for a in aa:
            #
            if a in i:
                #
                a = 0
                #
                for b in bb:
                    #
                    if b in i:
                        #
                        a = 1
                #
                if a == 0:
                    #
                    try:
                        ii = Industry.objects.get(Description=aaa)
                    except:
                        ii = Industry()
                        ii.Description = aaa
                        ii.Sector_db = 1
                        db = db + 1
                        ii.db = db
                        ii.save()
                    #
                    e.Industry_db = ii.db
                    #
                    e.Industry = aaa
                    #
                    print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Energy'
    try:
        #
        aa = [
            'Coal',
            'Crude',
            'Drilling',
            'Gas',
            'Energy',
            'Gas Other Services',
            'Gaz ',
            'Heating Equipment, Except Electric & Warm Air Furnaces',
            'Natural Gas',
            'Oil & Gas',
            'Oil & Gas Field',
            'Oil Royalty Traders',
            'Petroleum Refining',
            'Power Producers',
            'Power, Distribution',
            'Products Of Petroleum',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 1
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Computer & Semiconductors'
    try:
        #
        aa = [
            'Computer & Office Equipment',
            'Computer Communications Equipment',
            'Computer Storage Device',
            'Computer Peripheral Equipment',
            'Computer Terminals',
            'Electronic',
            'Printed Circuit Boards',
            'Office Machines',
            'Semiconductors',
            'Computer Integrated Systems Design',
            'Computer Processing',
            'Computer Programming',
            'Computer Rental & Leasing',
            'Storage Devices',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 1
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Information Technology'
    try:
        #
        aa = [
            'Calculating & Accounting',
            'Computer Processing',
            'Computer Programming',
            'Data Processing',
            'Information Technology',
            'Services-Computer',
            'Software',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 1
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Telecommunication'
    try:
        #
        aa = [
            'Broadcasting Stations',
            'Communications',
            'Household Audio & Video Equipment',
            'Magnetic & Optical Recording Media',
            'Radio',
            'Telephone',
            'Television',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 1
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Breweries & Bottlers'
    try:
        #
        aa = [
            'Brewer',
            'Bottle',
            'Malt Beverages',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 1
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Furniture & Fixtures'
    try:
        #
        aa = [
            'Furniture',
            'Fixtures',
        ]
        for a in aa:
            #
            #
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 1
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Electric'
    try:
        #
        aa = [
            'Electric',
            'Switchgear & Switchboard',
        ]
        bb = [
            'Except Electric',
        ]
        for a in aa:
            #
            if a in i:
                #
                a = 0
                #
                for b in bb:
                    #
                    if b in i:
                        #
                        a = 1
                #
                if a == 0:
                    try:
                        ii = Industry.objects.get(Description=aaa)
                    except:
                        ii = Industry()
                        ii.Description = aaa
                        ii.Sector_db = 1
                        db = db + 1
                        ii.db = db
                        ii.save()
                    #
                    e.Industry_db = ii.db
                    #
                    e.Industry = aaa
                    #
                    print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Chemical Engineering'
    try:
        #
        aa = [
            'Abrasive',
            'Adhesives',
            'Asphalt',
            'Cement',
            'Chemical',
            'Cleaning Preparations',
            'Concrete',
            'Cosmetics',
            'Detergent',
            'Glass',
            'Paints',
            'Perfumes',
            'Plastic',
            'Pottery',
            'Rubber',
            'Sanitation Preparations',
            'Sealants',
            'Soap',
            'Tires',
            'Tubes',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 1
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Aerospacial'
    try:
        #
        aa = [
            'Aircraft',
            'Aerospac',
            'Space',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 1
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Textile & Leather'
    try:
        #
        aa = [
            'Carpets',
            'Cotton',
            'Fabrics',
            'Fiber',
            'Footwear',
            'Garments',
            'Knit',
            'Leather',
            'Outerwear',
            'Textile',
            'Undergarments',
            'Work Clothg',
        ]
        bb = [
            'Rubber & Plastics',
        ]
        for a in aa:
            #
            if a in i:
                #
                a = 0
                #
                for b in bb:
                    #
                    if b in i:
                        #
                        a = 1
                #
                if a == 0:
                    #
                    try:
                        ii = Industry.objects.get(Description=aaa)
                    except:
                        ii = Industry()
                        ii.Description = aaa
                        ii.Sector_db = 1
                        db = db + 1
                        ii.db = db
                        ii.save()
                    #
                    e.Industry_db = ii.db
                    #
                    e.Industry = aaa
                    #
                    print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Tobacco Products'
    try:
        #
        aa = [
            'Tobacco',
            'Cigarettes',
        ]
        for a in aa:
            #
            #
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 1
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Wood Products'
    try:
        #
        aa = [
            'Binders',
            'Blankbooks',
            'Bookbindg',
            'Paperboard',
            'Greeting Cards',
            'Lumber',
            'Millwood',
            ' Paper',
            'Paper Mills',
            'Planting Mills',
            'Plywood',
            'Pulp Mills',
            'Sawmills',
            'Wood Products',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 1
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Finance, Legal, Management & Consulting'
    try:
        #
        aa = [
            'Advice',
            'Business',
            'Services-Personal',
            'Consulting',
            'Employment Agencies',
            'Finance',
            'Management',
            'Manifold Business Forms',
            'Services-Legal',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 2
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Building & Infrastructures'
    try:
        #
        aa = [
            'Buildings',
            'Construction',
            'Contractors',
            'Door',
            'Establishment',
            'Frames',
            'Non Residential',
            'Operative Builders',
            'Plumbing',
            'Prefabricated Wood Bldgs',
            'Paving',
            'Public Utilities',
            'Refuse System',
            'Residential',
            'Roofing',
            'Sanitary Services',
            'Structural Clay',
            'Utilities',
            'Waste Management',
            'Water Trans',
            'Social Services',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 1
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Engineering & Laboratory'
    try:
        #
        aa = [
            'Auto Controls',
            'Engineering',
            'Laborator',
            'Measuring & Controlling Devices',
            'Optical',
            'Photographic Equipment',
            'Repair Services',
        ]
        for a in aa:
            #
            #
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 1
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Banking'
    try:
        #
        aa = [
            'Bank',
            'Credit Institution',
            'Investors',
            'Mortgage',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 2
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    aaa = 'Brokers, Investors, Savings Institutions'
    try:
        #
        aa = [
            'Asset-Backed Securities',
            'Brokers',
            'Investors',
            'Savings Institution',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 2
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    aaa = 'Credit & Collection Agencies'
    try:
        #
        aa = [
            'Collection Agencies',
            'Credit Agencies',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 2
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    aaa = 'Blank Checks'
    try:
        #
        aa = [
            'Blank Checks',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 2
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Marketing & Advertising'
    try:
        #
        aa = [
            'Advertis',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 2
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Patent Owners & Lessors'
    try:
        #
        aa = [
            'Patent Owners & Lessors',
            'Rental & Leasing',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 2
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Real Estate'
    try:
        #
        aa = [
            'Dwellings',
            'Hotel',
            'Land Subdividers',
            'Operators Of Nonresidential Buildings',
            'Operators Of Apartment Buildings',
            'Real Estate',
            'Real Property',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 2
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Transportation, Routing & Courier'
    try:
        #
        aa = [
            'Air Transport',
            'Airport',
            'Courier',
            'Flying Fields',
            'Pipe Lines (No Natural Gax)',
            'Shipping',
            'Transport ',
            'Trucking',

        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 2
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Industrial, Machinery & Equipment'
    try:
        #
        aa = [
            'Air-Cond',
            'Air Purifing Equip',
            'Comml Environments',
            'Bearings',
            'Commercial Machinery',
            'Commercial Printing',
            'Engines',
            'Fans & Blowers',
            'Fluid Meters',
            'Gaskets',
            'Packg',
            'Hydraulic',
            'Industrial',
            'Industrial',
            'Industrial',
            'Instruments For Meas',
            'Gardens Equip',
            'Garden Tractors',
            'Household Appliances',
            'Housewares & Fans',
            'Machinery',
            'Manufacturing',
            'Motors',
            'Pumps',
            'Refrigeration',
            'Special Industry',
            'Switchgear',
            'Transportation Equipment',
            'Truck ',
            'Turbines',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 1
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Metal Manufacturing'
    try:
        #
        aa = [
            'Aluminum',
            'Boiler Shops',
            'Bolts',
            'Coating, Engraving',
            'Cutlery',
            'Ferrous',
            'Finishing Mills',
            'Forging',
            'Foundries',
            'Iron',
            'Metal',
            'Nonferrous Wire',
            'Refining of Metals',
            'Refining of Nonferrous Metals',
            'Rivets',
            'Rolling',
            'Screw',
            'Smelting',
            'Steel',
            'Services-Services',
        ]
        bb = [
            'Mining',
            'Building',
        ]
        for a in aa:
            #
            if a in i:
                #
                a = 0
                #
                for b in bb:
                    #
                    if b in i:
                        #
                        a = 1
                #
                if a == 0:
                    #
                    try:
                        ii = Industry.objects.get(Description=aaa)
                    except:
                        ii = Industry()
                        ii.Description = aaa
                        ii.Sector_db = 1
                        db = db + 1
                        ii.db = db
                        ii.save()
                    #
                    e.Industry_db = ii.db
                    #
                    e.Industry = aaa
                    #
                    print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Educational'
    try:
        #
        aa = [
            'Education',
            'Services-Child Day Care Services',
            'Universit',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 3
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Government'
    try:
        #
        aa = [
            'American Depositary Receipts',
            'Government',
            'International Affairs',

        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 3
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Insurance'
    try:
        #
        aa = [
            'Insurance',

        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 2
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Pharmaceutical'
    try:
        #
        aa = [
            'Pharmaceutical',
            'Biological Research',

        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 3
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Military, Marine & Surety'
    try:
        #
        aa = [
            'Detective, Guard',
            'Ordnance',
            'Missiles',
        ]
        for a in aa:
            #
            #
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 3
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Agriculture & Forestry'
    try:
        #
        aa = [
            'Agricultur',
            'Forestr',
            'Unsupported Plastics Film & Sheet',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 0
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Fishing & Hunting'
    try:
        #
        aa = [
            'Fishing',
            'Hunting',
            'Traping',

        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 0
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Mining & Quarrying'
    try:
        #
        aa = [
            'Gold',
            'Metal',
            'Mineral',
            'Mining',
            'Quarrying',
            'Silver',
            'Stone',
        ]
        bb = [
            'Construction',
            'Cutting',
            'Doors',
            'Fabricated',
            'Forging',
        ]
        for a in aa:
            #
            if a in i:
                #
                a = 0
                #
                for b in bb:
                    #
                    if b in i:
                        #
                        a = 1
                #
                if a == 0:
                    #
                    try:
                        ii = Industry.objects.get(Description=aaa)
                    except:
                        ii = Industry()
                        ii.Description = aaa
                        ii.Sector_db = 0
                        db = db + 1
                        ii.db = db
                        ii.save()
                    #
                    e.Industry_db = ii.db
                    #
                    e.Industry = aaa
                    #
                    print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Food'
    try:
        #
        aa = [
            'Bakery',
            'Beverage',
            'Biological',
            'Carbonated Waters',
            'Confectionery',
            'Cookies',
            'Dairy',
            'Eating Places',
            'Fats & Oils',
            'Food',
            'Frozen Fish',
            'Fruits',
            'Grain',
            'Ice Cream',
            'Meat',
            'Metal Cans',
            'Prepared Fresh Or Frozen',
            'Prepared Fresh',
            'Prepared Frozen',
            'Retail-Eating',
            'Sausages',
            'Seafoods',
            'Slaughtering',
            'Soft Drinks',
            'Water Supply',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 1
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Health Care'
    try:
        #
        aa = [
            'Dental',
            'Health',
            'Hospitals',
            'In Vitro',
            'Medical',
            'medical',
            'Medicin',
            'Nursing',
            'Ophthalmic',
            'Orthopedic',
            'Outpatient',
            'Personal Care',
            'Services-Help',
            'Services-Social Services',
            'Surgical',
            'X-Ray Apparatus & Tubes & Related Irradiation Apparatus',

        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 3
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Railroads'
    try:
        #
        aa = [
            'Passenger Trans',
            'Railroad',
        ]
        for a in aa:
            #
            if a in i:
                #
                try:
                    ii = Industry.objects.get(Description=aaa)
                except:
                    ii = Industry()
                    ii.Description = aaa
                    ii.Sector_db = 1
                    db = db + 1
                    ii.db = db
                    ii.save()
                #
                e.Industry_db = ii.db
                #
                e.Industry = aaa
                #
                print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Wholesale, Distribution & Storage'
    try:
        #
        aa = [
            'Wholesale',
        ]
        bb = [
            'Clothing',
            'Shoe Store',
            'Sporting & Athletic',
            'Retail-',
            'Storage Devices',
            'Natural Gas',
            'Power',
            'Motion Picture',
        ]
        for a in aa:
            #
            if a in i:
                #
                a = 0
                #
                for b in bb:
                    #
                    if b in i:
                        #
                        a = 1
                #
                if a == 0:
                    #
                    try:
                        ii = Industry.objects.get(Description=aaa)
                    except:
                        ii = Industry()
                        ii.Description = aaa
                        ii.Sector_db = 2
                        db = db + 1
                        ii.db = db
                        ii.save()
                    #
                    e.Industry_db = ii.db
                    #
                    e.Industry = aaa
                    #
                    print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    aaa = 'Retail'
    try:
        #
        aa = [
            'Clothing',
            'Shoe Store',
            'Sporting & Athletic',
            'Retail-',
        ]
        bb = [
            'Distribution',
            'Natural Gas',
            'Power',
            'Motion Picture',
            'Power',
            'Storage',
            'Warehousing',
            'Wholesale',
        ]
        for a in aa:
            #
            if a in i:
                #
                a = 0
                #
                for b in bb:
                    #
                    if b in i:
                        #
                        a = 1
                #
                if a == 0:
                    #
                    try:
                        ii = Industry.objects.get(Description=aaa)
                    except:
                        ii = Industry()
                        ii.Description = aaa
                        ii.Sector_db = 2
                        db = db + 1
                        ii.db = db
                        ii.save()
                    #
                    e.Industry_db = ii.db
                    #
                    e.Industry = aaa
                    #
                    print(e.TradingSymbol + ': ' + e.Industry + ' (' + e.Industry_SEC + ')')
        #
        e.save()
    except:
        pass
    #
    #
    print(e)
    print(e.Industry)
    print(e.Industry_db)
    print('\n')




