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
import json
import os
import pandas as pd
import pathlib
import requests
import urllib
import xml.etree.ElementTree as ET


##############################################################################################################    

# OUTPUT DIRECTORY
try:
    output_directory = './φ/algorithm/layout/'
    # Delete the content of the download file
    files = glob.glob('A:/arch/φ/algorithm/output/*')
    for f in files:
        os.remove(f)
except:
    print('---Could not define and clear output directory.')

# LAYOUT
entities_list = Entity.objects.all().order_by('EntityRegistrantName')
with open(output_directory + 'layout.txt', 'a') as layout:
    for count in range(0, len(entities_list)):
        layout.write("{ name: '" + entities_list[count].EntityRegistrantName.replace("'", "`") + " (" + entities_list[count].TradingSymbol + ")' , url: './" + entities_list[count].TradingSymbol + "'},")
        layout.write('\n')

###############################################################################################################

