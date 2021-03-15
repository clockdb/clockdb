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

###############################################################################################################
# function

# BeautifulSoup parser
def fetch(url):
    thepage = urllib.request.urlopen(url)
    soupdata = BeautifulSoup(thepage,"html.parser")
    return soupdata

# Append values if key already exists
def append_value(dict_obj, key, value):
    # Check if key exist in dict or not
    if key in dict_obj:
        if not isinstance(dict_obj[key], list):
            dict_obj[key] = [dict_obj[key]]
        dict_obj[key].append(value)
    else:
        dict_obj[key] = value

###############################################################################################################

# Marketstack API
params = {
  'access_key': 'ecae621d4718099f0d660a237c429450',
}

# STRUCTURE DATA 
# https://www.sec.gov/structureddata

# MASTER
# https://xbrl.sec.gov/dei/2020/dei-doc-2020-01-31.xml

# US-GAAP
# https://xbrl.fasb.org/us-gaap/

# Others
# https://www.sec.gov/data.json
# https://www.sec.gov/Archives/edgar/cik-lookup-data.txt
# https://www.sec.gov/files/company_TradingSymbols.json

# currency codes 
# https://xbrl.sec.gov/currency/

# exchanges 
# https://xbrl.sec.gov/exch/2020/exch-doc-2020-01-31.xml
Exchanges = {
    'VDRK' : 'TSX VENTURE EXCHANGE - DRK',
}

# industries 
# https://xbrl.sec.gov/sic/
Industries = {
    '100': 'AGRICULTURAL PRODUCTION-CROPS',
    '200': 'AGRICULTURAL PROD-LIVESTOCK & ANIMAL SPECIALTIES',
    '700': 'AGRICULTURAL SERVICES',
    '800': 'FORESTRY',
    '900': 'FISHING, HUNTING AND TRAPPING',
    '1000': 'METAL MINING',
    '1040': 'GOLD AND SILVER ORES',
    '1090': 'MISCELLANEOUS METAL ORES',
    '1220': 'BITUMINOUS COAL & LIGNITE MINING',
    '1221': 'BITUMINOUS COAL & LIGNITE SURFACE MINING',
    '1311': 'CRUDE PETROLEUM & NATURAL GAS',
    '1381': 'DRILLING OIL & GAS WELLS',
    '1382': 'OIL & GAS FIELD EXPLORATION SERVICES',
    '1389': 'OIL & GAS FIELD SERVICES, NEC',
    '1400': 'MINING & QUARRYING OF NONMETALLIC MINERALS (NO FUELS)',
    '1520': 'GENERAL BLDG CONTRACTORS - RESIDENTIAL BLDGS',
    '1531': 'OPERATIVE BUILDERS',
    '1540': 'GENERAL BLDG CONTRACTORS - NONRESIDENTIAL BLDGS',
    '1600': 'HEAVY CONSTRUCTION OTHER THAN BLDG CONST - CONTRACTORS',
    '1623': 'WATER, SEWER, PIPELINE, COMM & POWER LINE CONSTRUCTION',
    '1700': 'CONSTRUCTION - SPECIAL TRADE CONTRACTORS',
    '1731': 'ELECTRICAL WORK',
    '2000': 'FOOD AND KINDRED PRODUCTS',
    '2011': 'MEAT PACKING PLANTS',
    '2013': 'SAUSAGES & OTHER PREPARED MEAT PRODUCTS',
    '2015': 'POULTRY SLAUGHTERING AND PROCESSING',
    '2020': 'DAIRY PRODUCTS',
    '2024': 'ICE CREAM & FROZEN DESSERTS',
    '2030': 'CANNED, FROZEN & PRESERVD FRUIT, VEG & FOOD SPECIALTIES',
    '2033': 'CANNED, FRUITS, VEG, PRESERVES, JAMS & JELLIES',
    '2040': 'GRAIN MILL PRODUCTS',
    '2050': 'BAKERY PRODUCTS',
    '2052': 'COOKIES & CRACKERS',
    '2060': 'SUGAR & CONFECTIONERY PRODUCTS',
    '2070': 'FATS & OILS',
    '2080': 'BEVERAGES',
    '2082': 'MALT BEVERAGES',
    '2086': 'BOTTLED & CANNED SOFT DRINKS & CARBONATED WATERS',
    '2090': 'MISCELLANEOUS FOOD PREPARATIONS & KINDRED PRODUCTS',
    '2092': 'PREPARED FRESH OR FROZEN FISH & SEAFOODS',
    '2100': 'TOBACCO PRODUCTS',
    '2111': 'CIGARETTES',
    '2200': 'TEXTILE MILL PRODUCTS',
    '2211': 'BROADWOVEN FABRIC MILLS, COTTON',
    '2221': 'BROADWOVEN FABRIC MILLS, MAN MADE FIBER & SILK',
    '2250': 'KNITTING MILLS',
    '2253': 'KNIT OUTERWEAR MILLS',
    '2273': 'CARPETS & RUGS',
    '2300': 'APPAREL & OTHER FINISHD PRODS OF FABRICS & SIMILAR MATL',
    '2320': 'MENS & BOYS FURNISHGS, WORK CLOTHG, & ALLIED GARMENTS',
    '2330': 'WOMENS, MISSES, AND JUNIORS OUTERWEAR',
    '2340': 'WOMENS, MISSES, CHILDRENS & INFANTS UNDERGARMENTS',
    '2390': 'MISCELLANEOUS FABRICATED TEXTILE PRODUCTS',
    '2400': 'LUMBER & WOOD PRODUCTS (NO FURNITURE)',
    '2421': 'SAWMILLS & PLANTING MILLS, GENERAL',
    '2430': 'MILLWOOD, VENEER, PLYWOOD, & STRUCTURAL WOOD MEMBERS',
    '2451': 'MOBILE HOMES',
    '2452': 'PREFABRICATED WOOD BLDGS & COMPONENTS',
    '2510': 'HOUSEHOLD FURNITURE',
    '2511': 'WOOD HOUSEHOLD FURNITURE, (NO UPHOLSTERED)',
    '2520': 'OFFICE FURNITURE',
    '2522': 'OFFICE FURNITURE (NO WOOD)',
    '2531': 'PUBLIC BLDG & RELATED FURNITURE',
    '2540': 'PARTITIONS, SHELVG, LOCKERS, & OFFICE & STORE FIXTURES',
    '2590': 'MISCELLANEOUS FURNITURE & FIXTURES',
    '2600': 'PAPERS & ALLIED PRODUCTS',
    '2611': 'PULP MILLS',
    '2621': 'PAPER MILLS',
    '2631': 'PAPERBOARD MILLS',
    '2650': 'PAPERBOARD CONTAINERS & BOXES',
    '2670': 'CONVERTED PAPER & PAPERBOARD PRODS (NO CONTANERS/BOXES)',
    '2673': 'PLASTICS, FOIL & COATED PAPER BAGS',
    '2711': 'NEWSPAPERS: PUBLISHING OR PUBLISHING & PRINTING',
    '2721': 'PERIODICALS: PUBLISHING OR PUBLISHING & PRINTING',
    '2731': 'BOOKS: PUBLISHING OR PUBLISHING & PRINTING',
    '2732': 'BOOK PRINTING',
    '2741': 'MISCELLANEOUS PUBLISHING',
    '2750': 'COMMERCIAL PRINTING',
    '2761': 'MANIFOLD BUSINESS FORMS',
    '2771': 'GREETING CARDS',
    '2780': 'BLANKBOOKS, LOOSELEAF BINDERS & BOOKBINDG & RELATD WORK',
    '2790': 'SERVICE INDUSTRIES FOR THE PRINTING TRADE',
    '2800': 'CHEMICALS & ALLIED PRODUCTS',
    '2810': 'INDUSTRIAL INORGANIC CHEMICALS',
    '2820': 'PLASTIC MATERIAL, SYNTH RESIN/RUBBER, CELLULOS (NO GLASS)',
    '2821': 'PLASTIC MATERIALS, SYNTH RESINS & NONVULCAN ELASTOMERS',
    '2833': 'MEDICINAL CHEMICALS & BOTANICAL PRODUCTS',
    '2834': 'PHARMACEUTICAL PREPARATIONS',
    '2835': 'IN VITRO & IN VIVO DIAGNOSTIC SUBSTANCES',
    '2836': 'BIOLOGICAL PRODUCTS, (NO DISGNOSTIC SUBSTANCES)',
    '2840': 'SOAP, DETERGENTS, CLEANG PREPARATIONS, PERFUMES, COSMETICS',
    '2842': 'SPECIALTY CLEANING, POLISHING AND SANITATION PREPARATIONS',
    '2844': 'PERFUMES, COSMETICS & OTHER TOILET PREPARATIONS',
    '2851': 'PAINTS, VARNISHES, LACQUERS, ENAMELS & ALLIED PRODS',
    '2860': 'INDUSTRIAL ORGANIC CHEMICALS',
    '2870': 'AGRICULTURAL CHEMICALS',
    '2890': 'MISCELLANEOUS CHEMICAL PRODUCTS',
    '2891': 'ADHESIVES & SEALANTS',
    '2911': 'PETROLEUM REFINING',
    '2950': 'ASPHALT PAVING & ROOFING MATERIALS',
    '2990': 'MISCELLANEOUS PRODUCTS OF PETROLEUM & COAL',
    '3011': 'TIRES & INNER TUBES',
    '3021': 'RUBBER & PLASTICS FOOTWEAR',
    '3050': 'GASKETS, PACKG & SEALG DEVICES & RUBBER & PLASTICS HOSE',
    '3060': 'FABRICATED RUBBER PRODUCTS, NEC',
    '3080': 'MISCELLANEOUS PLASTICS PRODUCTS',
    '3081': 'UNSUPPORTED PLASTICS FILM & SHEET',
    '3086': 'PLASTICS FOAM PRODUCTS',
    '3089': 'PLASTICS PRODUCTS, NEC',
    '3100': 'LEATHER & LEATHER PRODUCTS',
    '3140': 'FOOTWEAR, (NO RUBBER)',
    '3211': 'FLAT GLASS',
    '3220': 'GLASS & GLASSWARE, PRESSED OR BLOWN',
    '3221': 'GLASS CONTAINERS',
    '3231': 'GLASS PRODUCTS, MADE OF PURCHASED GLASS',
    '3241': 'CEMENT, HYDRAULIC',
    '3250': 'STRUCTURAL CLAY PRODUCTS',
    '3260': 'POTTERY & RELATED PRODUCTS',
    '3270': 'CONCRETE, GYPSUM & PLASTER PRODUCTS',
    '3272': 'CONCRETE PRODUCTS, EXCEPT BLOCK & BRICK',
    '3281': 'CUT STONE & STONE PRODUCTS',
    '3290': 'ABRASIVE, ASBESTOS & MISC NONMETALLIC MINERAL PRODS',
    '3310': 'STEEL WORKS, BLAST FURNACES & ROLLING & FINISHING MILLS',
    '3312': 'STEEL WORKS, BLAST FURNACES & ROLLING MILLS (COKE OVENS)',
    '3317': 'STEEL PIPE & TUBES',
    '3320': 'IRON & STEEL FOUNDRIES',
    '3330': 'PRIMARY SMELTING & REFINING OF NONFERROUS METALS',
    '3334': 'PRIMARY PRODUCTION OF ALUMINUM',
    '3341': 'SECONDARY SMELTING & REFINING OF NONFERROUS METALS',
    '3350': 'ROLLING DRAWING & EXTRUDING OF NONFERROUS METALS',
    '3357': 'DRAWING & INSULATING OF NONFERROUS WIRE',
    '3360': 'NONFERROUS FOUNDRIES (CASTINGS)',
    '3390': 'MISCELLANEOUS PRIMARY METAL PRODUCTS',
    '3411': 'METAL CANS',
    '3412': 'METAL SHIPPING BARRELS, DRUMS, KEGS & PAILS',
    '3420': 'CUTLERY, HANDTOOLS & GENERAL HARDWARE',
    '3430': 'HEATING EQUIP, EXCEPT ELEC & WARM AIR; & PLUMBING FIXTURES',
    '3433': 'HEATING EQUIPMENT, EXCEPT ELECTRIC & WARM AIR FURNACES',
    '3440': 'FABRICATED STRUCTURAL METAL PRODUCTS',
    '3442': 'METAL DOORS, SASH, FRAMES, MOLDINGS & TRIM',
    '3443': 'FABRICATED PLATE WORK (BOILER SHOPS)',
    '3444': 'SHEET METAL WORK',
    '3448': 'PREFABRICATED METAL BUILDINGS & COMPONENTS',
    '3451': 'SCREW MACHINE PRODUCTS',
    '3452': 'BOLTS, NUTS, SCREWS, RIVETS & WASHERS',
    '3460': 'METAL FORGINGS & STAMPINGS',
    '3470': 'COATING, ENGRAVING & ALLIED SERVICES',
    '3480': 'ORDNANCE & ACCESSORIES, (NO VEHICLES/GUIDED MISSILES)',
    '3490': 'MISCELLANEOUS FABRICATED METAL PRODUCTS',
    '3510': 'ENGINES & TURBINES',
    '3523': 'FARM MACHINERY & EQUIPMENT',
    '3524': 'LAWN & GARDEN TRACTORS & HOME LAWN & GARDENS EQUIP',
    '3530': 'CONSTRUCTION, MINING & MATERIALS HANDLING MACHINERY & EQUIP',
    '3531': 'CONSTRUCTION MACHINERY & EQUIP',
    '3532': 'MINING MACHINERY & EQUIP (NO OIL & GAS FIELD MACH & EQUIP)',
    '3533': 'OIL & GAS FIELD MACHINERY & EQUIPMENT',
    '3537': 'INDUSTRIAL TRUCKS, TRACTORS, TRAILORS & STACKERS',
    '3540': 'METALWORKG MACHINERY & EQUIPMENT',
    '3541': 'MACHINE TOOLS, METAL CUTTING TYPES',
    '3550': 'SPECIAL INDUSTRY MACHINERY (NO METALWORKING MACHINERY)',
    '3555': 'PRINTING TRADES MACHINERY & EQUIPMENT',
    '3559': 'SPECIAL INDUSTRY MACHINERY, NEC',
    '3560': 'GENERAL INDUSTRIAL MACHINERY & EQUIPMENT',
    '3561': 'PUMPS & PUMPING EQUIPMENT',
    '3562': 'BALL & ROLLER BEARINGS',
    '3564': 'INDUSTRIAL & COMMERCIAL FANS & BLOWERS & AIR PURIFING EQUIP',
    '3567': 'INDUSTRIAL PROCESS FURNACES & OVENS',
    '3569': 'GENERAL INDUSTRIAL MACHINERY & EQUIPMENT, NEC',
    '3570': 'COMPUTER & OFFICE EQUIPMENT',
    '3571': 'ELECTRONIC COMPUTERS',
    '3572': 'COMPUTER STORAGE DEVICES',
    '3575': 'COMPUTER TERMINALS',
    '3576': 'COMPUTER COMMUNICATIONS EQUIPMENT',
    '3577': 'COMPUTER PERIPHERAL EQUIPMENT, NEC',
    '3578': 'CALCULATING & ACCOUNTING MACHINES (NO ELECTRONIC COMPUTERS)',
    '3579': 'OFFICE MACHINES, NEC',
    '3580': 'REFRIGERATION & SERVICE INDUSTRY MACHINERY',
    '3585': 'AIR-COND & WARM AIR HEATG EQUIP & COMM & INDL REFRIG EQUIP',
    '3590': 'MISC INDUSTRIAL & COMMERCIAL MACHINERY & EQUIPMENT',
    '3600': 'ELECTRONIC & OTHER ELECTRICAL EQUIPMENT (NO COMPUTER EQUIP)',
    '3612': 'POWER, DISTRIBUTION & SPECIALTY TRANSFORMERS',
    '3613': 'SWITCHGEAR & SWITCHBOARD APPARATUS',
    '3620': 'ELECTRICAL INDUSTRIAL APPARATUS',
    '3621': 'MOTORS & GENERATORS',
    '3630': 'HOUSEHOLD APPLIANCES',
    '3634': 'ELECTRIC HOUSEWARES & FANS',
    '3640': 'ELECTRIC LIGHTING & WIRING EQUIPMENT',
    '3651': 'HOUSEHOLD AUDIO & VIDEO EQUIPMENT',
    '3652': 'PHONOGRAPH RECORDS & PRERECORDED AUDIO TAPES & DISKS',
    '3661': 'TELEPHONE & TELEGRAPH APPARATUS',
    '3663': 'RADIO & TV BROADCASTING & COMMUNICATIONS EQUIPMENT',
    '3669': 'COMMUNICATIONS EQUIPMENT, NEC',
    '3670': 'ELECTRONIC COMPONENTS & ACCESSORIES',
    '3672': 'PRINTED CIRCUIT BOARDS',
    '3674': 'SEMICONDUCTORS & RELATED DEVICES',
    '3677': 'ELECTRONIC COILS, TRANSFORMERS & OTHER INDUCTORS',
    '3678': 'ELECTRONIC CONNECTORS',
    '3679': 'ELECTRONIC COMPONENTS, NEC',
    '3690': 'MISCELLANEOUS ELECTRICAL MACHINERY, EQUIPMENT & SUPPLIES',
    '3695': 'MAGNETIC & OPTICAL RECORDING MEDIA',
    '3711': 'MOTOR VEHICLES & PASSENGER CAR BODIES',
    '3713': 'TRUCK & BUS BODIES',
    '3714': 'MOTOR VEHICLE PARTS & ACCESSORIES',
    '3715': 'TRUCK TRAILERS',
    '3716': 'MOTOR HOMES',
    '3720': 'AIRCRAFT & PARTS',
    '3721': 'AIRCRAFT',
    '3724': 'AIRCRAFT ENGINES & ENGINE PARTS',
    '3728': 'AIRCRAFT PARTS & AUXILIARY EQUIPMENT, NEC',
    '3730': 'SHIP & BOAT BUILDING & REPAIRING',
    '3743': 'RAILROAD EQUIPMENT',
    '3751': 'MOTORCYCLES, BICYCLES & PARTS',
    '3760': 'GUIDED MISSILES & SPACE VEHICLES & PARTS',
    '3790': 'MISCELLANEOUS TRANSPORTATION EQUIPMENT',
    '3812': 'SEARCH, DETECTION, NAVAGATION, GUIDANCE, AERONAUTICAL SYS',
    '3821': 'LABORATORY APPARATUS & FURNITURE',
    '3822': 'AUTO CONTROLS FOR REGULATING RESIDENTIAL & COMML ENVIRONMENTS',
    '3823': 'INDUSTRIAL INSTRUMENTS FOR MEASUREMENT, DISPLAY, AND CONTROL',
    '3824': 'TOTALIZING FLUID METERS & COUNTING DEVICES',
    '3825': 'INSTRUMENTS FOR MEAS & TESTING OF ELECTRICITY & ELEC SIGNALS',
    '3826': 'LABORATORY ANALYTICAL INSTRUMENTS',
    '3827': 'OPTICAL INSTRUMENTS & LENSES',
    '3829': 'MEASURING & CONTROLLING DEVICES, NEC',
    '3841': 'SURGICAL & MEDICAL INSTRUMENTS & APPARATUS',
    '3842': 'ORTHOPEDIC, PROSTHETIC & SURGICAL APPLIANCES & SUPPLIES',
    '3843': 'DENTAL EQUIPMENT & SUPPLIES',
    '3844': 'X-RAY APPARATUS & TUBES & RELATED IRRADIATION APPARATUS',
    '3845': 'ELECTROMEDICAL & ELECTROTHERAPEUTIC APPARATUS',
    '3851': 'OPHTHALMIC GOODS',
    '3861': 'PHOTOGRAPHIC EQUIPMENT & SUPPLIES',
    '3873': 'WATCHES, CLOCKS, CLOCKWORK OPERATED DEVICES/PARTS',
    '3910': 'JEWELRY, SILVERWARE & PLATED WARE',
    '3911': 'JEWELRY, PRECIOUS METAL',
    '3931': 'MUSICAL INSTRUMENTS',
    '3942': 'DOLLS & STUFFED TOYS',
    '3944': 'GAMES, TOYS & CHILDRENS VEHICLES (NO DOLLS & BICYCLES)',
    '3949': 'SPORTING & ATHLETIC GOODS, NEC',
    '3950': 'PENS, PENCILS & OTHER ARTISTS MATERIALS',
    '3960': 'COSTUME JEWELRY & NOVELTIES',
    '3990': 'MISCELLANEOUS MANUFACTURING INDUSTRIES',
    '4011': 'RAILROADS, LINE-HAUL OPERATING',
    '4013': 'RAILROAD SWITCHING & TERMINAL ESTABLISHMENTS',
    '4100': 'LOCAL & SUBURBAN TRANSIT & INTERURBAN HWY PASSENGER TRANS',
    '4210': 'TRUCKING & COURIER SERVICES (NO AIR)',
    '4213': 'TRUCKING (NO LOCAL)',
    '4220': 'PUBLIC WAREHOUSING & STORAGE',
    '4231': 'TERMINAL MAINTENANCE FACILITIES FOR MOTOR FREIGHT TRANSPORT',
    '4400': 'WATER TRANSPORTATION',
    '4412': 'DEEP SEA FOREIGN TRANSPORTATION OF FREIGHT',
    '4512': 'AIR TRANSPORTATION, SCHEDULED',
    '4513': 'AIR COURIER SERVICES',
    '4522': 'AIR TRANSPORTATION, NONSCHEDULED',
    '4581': 'AIRPORTS, FLYING FIELDS & AIRPORT TERMINAL SERVICES',
    '4610': 'PIPE LINES (NO NATURAL GAS)',
    '4700': 'TRANSPORTATION SERVICES',
    '4731': 'ARRANGEMENT OF TRANSPORTATION OF FREIGHT & CARGO',
    '4812': 'RADIOTELEPHONE COMMUNICATIONS',
    '4813': 'TELEPHONE COMMUNICATIONS (NO RADIOTELEPHONE)',
    '4822': 'TELEGRAPH & OTHER MESSAGE COMMUNICATIONS',
    '4832': 'RADIO BROADCASTING STATIONS',
    '4833': 'TELEVISION BROADCASTING STATIONS',
    '4841': 'CABLE & OTHER PAY TELEVISION SERVICES',
    '4899': 'COMMUNICATIONS SERVICES, NEC',
    '4900': 'ELECTRIC, GAS & SANITARY SERVICES',
    '4911': 'ELECTRIC SERVICES',
    '4922': 'NATURAL GAS TRANSMISSION',
    '4923': 'NATURAL GAS TRANSMISISON & DISTRIBUTION',
    '4924': 'NATURAL GAS DISTRIBUTION',
    '4931': 'ELECTRIC & OTHER SERVICES COMBINED',
    '4932': 'GAS & OTHER SERVICES COMBINED',
    '4941': 'WATER SUPPLY',
    '4950': 'SANITARY SERVICES',
    '4953': 'REFUSE SYSTEMS',
    '4955': 'HAZARDOUS WASTE MANAGEMENT',
    '4961': 'STEAM & AIR-CONDITIONING SUPPLY',
    '4991': 'COGENERATION SERVICES & SMALL POWER PRODUCERS',
    '5000': 'WHOLESALE-DURABLE GOODS',
    '5010': 'WHOLESALE-MOTOR VEHICLES & MOTOR VEHICLE PARTS & SUPPLIES',
    '5013': 'WHOLESALE-MOTOR VEHICLE SUPPLIES & NEW PARTS',
    '5020': 'WHOLESALE-FURNITURE & HOME FURNISHINGS',
    '5030': 'WHOLESALE-LUMBER & OTHER CONSTRUCTION MATERIALS',
    '5031': 'WHOLESALE-LUMBER, PLYWOOD, MILLWORK & WOOD PANELS',
    '5040': 'WHOLESALE-PROFESSIONAL & COMMERCIAL EQUIPMENT & SUPPLIES',
    '5045': 'WHOLESALE-COMPUTERS & PERIPHERAL EQUIPMENT & SOFTWARE',
    '5047': 'WHOLESALE-MEDICAL, DENTAL & HOSPITAL EQUIPMENT & SUPPLIES',
    '5050': 'WHOLESALE-METALS & MINERALS (NO PETROLEUM)',
    '5051': 'WHOLESALE-METALS SERVICE CENTERS & OFFICES',
    '5063': 'WHOLESALE-ELECTRICAL APPARATUS & EQUIPMENT, WIRING SUPPLIES',
    '5064': 'WHOLESALE-ELECTRICAL APPLIANCES, TV & RADIO SETS',
    '5065': 'WHOLESALE-ELECTRONIC PARTS & EQUIPMENT, NEC',
    '5070': 'WHOLESALE-HARDWARE & PLUMBING & HEATING EQUIPMENT & SUPPLIES',
    '5072': 'WHOLESALE-HARDWARE',
    '5080': 'WHOLESALE-MACHINERY, EQUIPMENT & SUPPLIES',
    '5082': 'WHOLESALE-CONSTRUCTION & MINING (NO PETRO) MACHINERY & EQUIP',
    '5084': 'WHOLESALE-INDUSTRIAL MACHINERY & EQUIPMENT',
    '5090': 'WHOLESALE-MISC DURABLE GOODS',
    '5094': 'WHOLESALE-JEWELRY, WATCHES, PRECIOUS STONES & METALS',
    '5099': 'WHOLESALE-DURABLE GOODS, NEC',
    '5110': 'WHOLESALE-PAPER & PAPER PRODUCTS',
    '5122': 'WHOLESALE-DRUGS, PROPRIETARIES & DRUGGISTS SUNDRIES',
    '5130': 'WHOLESALE-APPAREL, PIECE GOODS & NOTIONS',
    '5140': 'WHOLESALE-GROCERIES & RELATED PRODUCTS',
    '5141': 'WHOLESALE-GROCERIES, GENERAL LINE',
    '5150': 'WHOLESALE-FARM PRODUCT RAW MATERIALS',
    '5160': 'WHOLESALE-CHEMICALS & ALLIED PRODUCTS',
    '5171': 'WHOLESALE-PETROLEUM BULK STATIONS & TERMINALS',
    '5172': 'WHOLESALE-PETROLEUM & PETROLEUM PRODUCTS (NO BULK STATIONS)',
    '5180': 'WHOLESALE-BEER, WINE & DISTILLED ALCOHOLIC BEVERAGES',
    '5190': 'WHOLESALE-MISCELLANEOUS NONDURABLE GOODS',
    '5200': 'RETAIL-BUILDING MATERIALS, HARDWARE, GARDEN SUPPLY',
    '5211': 'RETAIL-LUMBER & OTHER BUILDING MATERIALS DEALERS',
    '5271': 'RETAIL-MOBILE HOME DEALERS',
    '5311': 'RETAIL-DEPARTMENT STORES',
    '5331': 'RETAIL-VARIETY STORES',
    '5399': 'RETAIL-MISC GENERAL MERCHANDISE STORES',
    '5400': 'RETAIL-FOOD STORES',
    '5411': 'RETAIL-GROCERY STORES',
    '5412': 'RETAIL-CONVENIENCE STORES',
    '5500': 'RETAIL-AUTO DEALERS & GASOLINE STATIONS',
    '5531': 'RETAIL-AUTO & HOME SUPPLY STORES',
    '5600': 'RETAIL-APPAREL & ACCESSORY STORES',
    '5621': 'RETAIL-WOMENS CLOTHING STORES',
    '5651': 'RETAIL-FAMILY CLOTHING STORES',
    '5661': 'RETAIL-SHOE STORES',
    '5700': 'RETAIL-HOME FURNITURE, FURNISHINGS & EQUIPMENT STORES',
    '5712': 'RETAIL-FURNITURE STORES',
    '5731': 'RETAIL-RADIO, TV & CONSUMER ELECTRONICS STORES',
    '5734': 'RETAIL-COMPUTER & COMPUTER SOFTWARE STORES',
    '5735': 'RETAIL-RECORD & PRERECORDED TAPE STORES',
    '5810': 'RETAIL-EATING & DRINKING PLACES',
    '5812': 'RETAIL-EATING PLACES',
    '5900': 'RETAIL-MISCELLANEOUS RETAIL',
    '5912': 'RETAIL-DRUG STORES AND PROPRIETARY STORES',
    '5940': 'RETAIL-MISCELLANEOUS SHOPPING GOODS STORES',
    '5944': 'RETAIL-JEWELRY STORES',
    '5945': 'RETAIL-HOBBY, TOY & GAME SHOPS',
    '5960': 'RETAIL-NONSTORE RETAILERS',
    '5961': 'RETAIL-CATALOG & MAIL-ORDER HOUSES',
    '5990': 'RETAIL-RETAIL STORES, NEC',
    '6021': 'NATIONAL COMMERCIAL BANKS',
    '6022': 'STATE COMMERCIAL BANKS',
    '6029': 'COMMERCIAL BANKS, NEC',
    '6035': 'SAVINGS INSTITUTION, FEDERALLY CHARTERED',
    '6036': 'SAVINGS INSTITUTIONS, NOT FEDERALLY CHARTERED',
    '6099': 'FUNCTIONS RELATED TO DEPOSITORY BANKING, NEC',
    '6111': 'FEDERAL & FEDERALLY-SPONSORED CREDIT AGENCIES',
    '6141': 'PERSONAL CREDIT INSTITUTIONS',
    '6153': 'SHORT-TERM BUSINESS CREDIT INSTITUTIONS',
    '6159': 'MISCELLANEOUS BUSINESS CREDIT INSTITUTION',
    '6162': 'MORTGAGE BANKERS & LOAN CORRESPONDENTS',
    '6163': 'LOAN BROKERS',
    '6172': 'FINANCE LESSORS',
    '6189': 'ASSET-BACKED SECURITIES',
    '6199': 'FINANCE SERVICES',
    '6200': 'SECURITY & COMMODITY BROKERS, DEALERS, EXCHANGES & SERVICES',
    '6211': 'SECURITY BROKERS, DEALERS & FLOTATION COMPANIES',
    '6221': 'COMMODITY CONTRACTS BROKERS & DEALERS',
    '6282': 'INVESTMENT ADVICE',
    '6311': 'LIFE INSURANCE',
    '6321': 'ACCIDENT & HEALTH INSURANCE',
    '6324': 'HOSPITAL & MEDICAL SERVICE PLANS',
    '6331': 'FIRE, MARINE & CASUALTY INSURANCE',
    '6351': 'SURETY INSURANCE',
    '6361': 'TITLE INSURANCE',
    '6399': 'INSURANCE CARRIERS, NEC',
    '6411': 'INSURANCE AGENTS, BROKERS & SERVICE',
    '6500': 'REAL ESTATE',
    '6510': 'REAL ESTATE OPERATORS (NO DEVELOPERS) & LESSORS',
    '6512': 'OPERATORS OF NONRESIDENTIAL BUILDINGS',
    '6513': 'OPERATORS OF APARTMENT BUILDINGS',
    '6519': 'LESSORS OF REAL PROPERTY, NEC',
    '6531': 'REAL ESTATE AGENTS & MANAGERS (FOR OTHERS)',
    '6532': 'REAL ESTATE DEALERS (FOR THEIR OWN ACCOUNT)',
    '6552': 'LAND SUBDIVIDERS & DEVELOPERS (NO CEMETERIES)',
    '6770': 'BLANK CHECKS',
    '6792': 'OIL ROYALTY TRADERS',
    '6794': 'PATENT OWNERS & LESSORS',
    '6795': 'MINERAL ROYALTY TRADERS',
    '6798': 'REAL ESTATE INVESTMENT TRUSTS',
    '6799': 'INVESTORS, NEC',
    '7000': 'HOTELS, ROOMING HOUSES, CAMPS & OTHER LODGING PLACES',
    '7011': 'HOTELS & MOTELS',
    '7200': 'SERVICES-PERSONAL SERVICES',
    '7310': 'SERVICES-ADVERTISING',
    '7311': 'SERVICES-ADVERTISING AGENCIES',
    '7320': 'SERVICES-CONSUMER CREDIT REPORTING, COLLECTION AGENCIES',
    '7330': 'SERVICES-MAILING, REPRODUCTION, COMMERCIAL ART & PHOTOGRAPHY',
    '7331': 'SERVICES-DIRECT MAIL ADVERTISING SERVICES',
    '7340': 'SERVICES-TO DWELLINGS & OTHER BUILDINGS',
    '7350': 'SERVICES-MISCELLANEOUS EQUIPMENT RENTAL & LEASING',
    '7359': 'SERVICES-EQUIPMENT RENTAL & LEASING, NEC',
    '7361': 'SERVICES-EMPLOYMENT AGENCIES',
    '7363': 'SERVICES-HELP SUPPLY SERVICES',
    '7370': 'SERVICES-COMPUTER PROGRAMMING, DATA PROCESSING, ETC.',
    '7371': 'SERVICES-COMPUTER PROGRAMMING SERVICES',
    '7372': 'SERVICES-PREPACKAGED SOFTWARE',
    '7373': 'SERVICES-COMPUTER INTEGRATED SYSTEMS DESIGN',
    '7374': 'SERVICES-COMPUTER PROCESSING & DATA PREPARATION',
    '7377': 'SERVICES-COMPUTER RENTAL & LEASING',
    '7380': 'SERVICES-MISCELLANEOUS BUSINESS SERVICES',
    '7381': 'SERVICES-DETECTIVE, GUARD & ARMORED CAR SERVICES',
    '7384': 'SERVICES-PHOTOFINISHING LABORATORIES',
    '7385': 'SERVICES-TELEPHONE INTERCONNECT SYSTEMS',
    '7389': 'SERVICES-BUSINESS SERVICES, NEC',
    '7500': 'SERVICES-AUTOMOTIVE REPAIR, SERVICES & PARKING',
    '7510': 'SERVICES-AUTO RENTAL & LEASING (NO DRIVERS)',
    '7600': 'SERVICES-MISCELLANEOUS REPAIR SERVICES',
    '7812': 'SERVICES-MOTION PICTURE & VIDEO TAPE PRODUCTION',
    '7819': 'SERVICES-ALLIED TO MOTION PICTURE PRODUCTION',
    '7822': 'SERVICES-MOTION PICTURE & VIDEO TAPE DISTRIBUTION',
    '7829': 'SERVICES-ALLIED TO MOTION PICTURE DISTRIBUTION',
    '7830': 'SERVICES-MOTION PICTURE THEATERS',
    '7841': 'SERVICES-VIDEO TAPE RENTAL',
    '7900': 'SERVICES-AMUSEMENT & RECREATION SERVICES',
    '7948': 'SERVICES-RACING, INCLUDING TRACK OPERATION',
    '7990': 'SERVICES-MISCELLANEOUS AMUSEMENT & RECREATION',
    '7997': 'SERVICES-MEMBERSHIP SPORTS & RECREATION CLUBS',
    '8000': 'SERVICES-HEALTH SERVICES',
    '8011': 'SERVICES-OFFICES & CLINICS OF DOCTORS OF MEDICINE',
    '8050': 'SERVICES-NURSING & PERSONAL CARE FACILITIES',
    '8051': 'SERVICES-SKILLED NURSING CARE FACILITIES',
    '8060': 'SERVICES-HOSPITALS',
    '8062': 'SERVICES-GENERAL MEDICAL & SURGICAL HOSPITALS, NEC',
    '8071': 'SERVICES-MEDICAL LABORATORIES',
    '8082': 'SERVICES-HOME HEALTH CARE SERVICES',
    '8090': 'SERVICES-MISC HEALTH & ALLIED SERVICES, NEC',
    '8093': 'SERVICES-SPECIALTY OUTPATIENT FACILITIES, NEC',
    '8111': 'SERVICES-LEGAL SERVICES',
    '8200': 'SERVICES-EDUCATIONAL SERVICES',
    '8300': 'SERVICES-SOCIAL SERVICES',
    '8351': 'SERVICES-CHILD DAY CARE SERVICES',
    '8600': 'SERVICES-MEMBERSHIP ORGANIZATIONS',
    '8700': 'SERVICES-ENGINEERING, ACCOUNTING, RESEARCH, MANAGEMENT',
    '8711': 'SERVICES-ENGINEERING SERVICES',
    '8731': 'SERVICES-COMMERCIAL PHYSICAL & BIOLOGICAL RESEARCH',
    '8734': 'SERVICES-TESTING LABORATORIES',
    '8741': 'SERVICES-MANAGEMENT SERVICES',
    '8742': 'SERVICES-MANAGEMENT CONSULTING SERVICES',
    '8744': 'SERVICES-FACILITIES SUPPORT MANAGEMENT SERVICES',
    '8880': 'AMERICAN DEPOSITARY RECEIPTS',
    '8888': 'FOREIGN GOVERNMENTS',
    '8900': 'SERVICES-SERVICES, NEC',
    '9721': 'INTERNATIONAL AFFAIRS',
    '9995': 'NON-OPERATING ESTABLISHMENTS',
}

# regions 
# https://xbrl.sec.gov/country/
# https://xbrl.sec.gov/stpr/
Regions = {
    'AL': 'ALABAMA',
    'AK': 'ALASKA',
    'AZ': 'ARIZONA',
    'AR': 'ARKANSAS',
    'CA': 'CALIFORNIA',
    'CO': 'COLORADO',
    'CT': 'CONNECTICUT',
    'DE': 'DELAWARE',
    'DC': 'DISTRICT OF COLUMBIA',
    'FL': 'FLORIDA',
    'GA': 'GEORGIA',
    'HI': 'HAWAII',
    'ID': 'IDAHO',
    'IL': 'ILLINOIS',
    'IN': 'INDIANA',
    'IA': 'IOWA',
    'KS': 'KANSAS',
    'KY': 'KENTUCKY',
    'LA': 'LOUISIANA',
    'ME': 'MAINE',
    'MD': 'MARYLAND',
    'MA': 'MASSACHUSETTS',
    'MI': 'MICHIGAN',
    'MN': 'MINNESOTA',
    'MS': 'MISSISSIPPI',
    'MO': 'MISSOURI',
    'MT': 'MONTANA',
    'NE': 'NEBRASKA',
    'NV': 'NEVADA',
    'NH': 'NEW HAMPSHIRE',
    'NJ': 'NEW JERSEY',
    'NM': 'NEW MEXICO',
    'NY': 'NEW YORK',
    'NC': 'NORTH CAROLINA',
    'ND': 'NORTH DAKOTA',
    'OH': 'OHIO',
    'OK': 'OKLAHOMA',
    'OR': 'OREGON',
    'PA': 'PENNSYLVANIA',
    'RI': 'RHODE ISLAND',
    'SC': 'SOUTH CAROLINA',
    'SD': 'SOUTH DAKOTA',
    'TN': 'TENNESSEE',
    'TX': 'TEXAS',
    'X1': 'UNITED STATES',
    'UT': 'UTAH',
    'VT': 'VERMONT',
    'VA': 'VIRGINIA',
    'WA': 'WASHINGTON',
    'WV': 'WEST VIRGINIA',
    'WI': 'WISCONSIN',
    'WY': 'WYOMING',
    'A0': 'ALBERTA, CANADA',
    'A1': 'BRITISH COLUMBIA, CANADA',
    'A2': 'MANITOBA, CANADA',
    'A3': 'NEW BRUNSWICK, CANADA',
    'A4': 'NEWFOUNDLAND, CANADA',
    'A5': 'NOVA SCOTIA, CANADA',
    'A6': 'ONTARIO, CANADA',
    'A7': 'PRINCE EDWARD ISLAND, CANADA',
    'A8': 'QUEBEC, CANADA',
    'A9': 'SASKATCHEWAN, CANADA',
    'B0': 'YUKON, CANADA',
    'Z4': 'CANADA (Federal Level)',
    'B2': 'AFGHANISTAN',
    'Y6': 'ALAND ISLANDS',
    'B3': 'ALBANIA',
    'B4': 'ALGERIA',
    'B5': 'AMERICAN SAMOA',
    'B6': 'ANDORRA',
    'B7': 'ANGOLA',
    '1A': 'ANGUILLA',
    'B8': 'ANTARCTICA',
    'B9': 'ANTIGUA AND BARBUDA',
    'C1': 'ARGENTINA',
    '1B': 'ARMENIA',
    '1C': 'ARUBA',
    'C3': 'AUSTRALIA',
    'C4': 'AUSTRIA',
    '1D': 'AZERBAIJAN',
    'C5': 'BAHAMAS',
    'C6': 'BAHRAIN',
    'C7': 'BANGLADESH',
    'C8': 'BARBADOS',
    '1F': 'BELARUS',
    'C9': 'BELGIUM',
    'D1': 'BELIZE',
    'G6': 'BENIN',
    'D0': 'BERMUDA',
    'D2': 'BHUTAN',
    'D3': 'BOLIVIA',
    '1E': 'BOSNIA AND HERZEGOVINA',
    'B1': 'BOTSWANA',
    'D4': 'BOUVET ISLAND',
    'D5': 'BRAZIL',
    'D6': 'BRITISH INDIAN OCEAN TERRITORY',
    'D9': 'BRUNEI DARUSSALAM',
    'E0': 'BULGARIA',
    'X2': 'BURKINA FASO',
    'E2': 'BURUNDI',
    'E3': 'CAMBODIA',
    'E4': 'CAMEROON',
    'Z4': 'CANADA (Federal Level)',
    'E8': 'CAPE VERDE',
    'E9': 'CAYMAN ISLANDS',
    'F0': 'CENTRAL AFRICAN REPUBLIC',
    'F2': 'CHAD',
    'F3': 'CHILE',
    'F4': 'CHINA',
    'F6': 'CHRISTMAS ISLAND',
    'F7': 'COCOS (KEELING) ISLANDS',
    'F8': 'COLOMBIA',
    'F9': 'COMOROS',
    'G0': 'CONGO',
    'Y3': 'CONGO, THE DEMOCRATIC REPUBLIC OF THE',
    'G1': 'COOK ISLANDS',
    'G2': 'COSTA RICA',
    'L7': 'COTE DIVOIRE',
    '1M': 'CROATIA',
    'G3': 'CUBA',
    'G4': 'CYPRUS',
    '2N': 'CZECH REPUBLIC',
    'G7': 'DENMARK',
    '1G': 'DJIBOUTI',
    'G9': 'DOMINICA',
    'G8': 'DOMINICAN REPUBLIC',
    'H1': 'ECUADOR',
    'H2': 'EGYPT',
    'H3': 'EL SALVADOR',
    'H4': 'EQUATORIAL GUINEA',
    '1J': 'ERITREA',
    '1H': 'ESTONIA',
    'H5': 'ETHIOPIA',
    'H7': 'FALKLAND ISLANDS (MALVINAS)',
    'H6': 'FAROE ISLANDS',
    'H8': 'FIJI',
    'H9': 'FINLAND',
    'I0': 'FRANCE',
    'I3': 'FRENCH GUIANA',
    'I4': 'FRENCH POLYNESIA',
    '2C': 'FRENCH SOUTHERN TERRITORIES',
    'I5': 'GABON',
    'I6': 'GAMBIA',
    '2Q': 'GEORGIA',
    '2M': 'GERMANY',
    'J0': 'GHANA',
    'J1': 'GIBRALTAR',
    'J3': 'GREECE',
    'J4': 'GREENLAND',
    'J5': 'GRENADA',
    'J6': 'GUADELOUPE',
    'GU': 'GUAM',
    'J8': 'GUATEMALA',
    'Y7': 'GUERNSEY',
    'J9': 'GUINEA',
    'S0': 'GUINEA-BISSAU',
    'K0': 'GUYANA',
    'K1': 'HAITI',
    'K4': 'HEARD ISLAND AND MCDONALD ISLANDS',
    'X4': 'HOLY SEE (VATICAN CITY STATE)',
    'K2': 'HONDURAS',
    'K3': 'HONG KONG',
    'K5': 'HUNGARY',
    'K6': 'ICELAND',
    'K7': 'INDIA',
    'K8': 'INDONESIA',
    'K9': 'IRAN, ISLAMIC REPUBLIC OF',
    'L0': 'IRAQ',
    'L2': 'IRELAND',
    'Y8': 'ISLE OF MAN',
    'L3': 'ISRAEL',
    'L6': 'ITALY',
    'L8': 'JAMAICA',
    'M0': 'JAPAN',
    'Y9': 'JERSEY',
    'M2': 'JORDAN',
    '1P': 'KAZAKSTAN',
    'M3': 'KENYA',
    'J2': 'KIRIBATI',
    'M4': 'KOREA, DEMOCRATIC PEOPLES REPUBLIC OF',
    'M5': 'KOREA, REPUBLIC OF',
    'M6': 'KUWAIT',
    '1N': 'KYRGYZSTAN',
    'M7': 'LAO PEOPLES DEMOCRATIC REPUBLIC',
    '1R': 'LATVIA',
    'M8': 'LEBANON',
    'M9': 'LESOTHO',
    'N0': 'LIBERIA',
    'N1': 'LIBYAN ARAB JAMAHIRIYA',
    'N2': 'LIECHTENSTEIN',
    '1Q': 'LITHUANIA',
    'N4': 'LUXEMBOURG',
    'N5': 'MACAU',
    '1U': 'MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF',
    'N6': 'MADAGASCAR',
    'N7': 'MALAWI',
    'N8': 'MALAYSIA',
    'N9': 'MALDIVES',
    'O0': 'MALI',
    'O1': 'MALTA',
    '1T': 'MARSHALL ISLANDS',
    'O2': 'MARTINIQUE',
    'O3': 'MAURITANIA',
    'O4': 'MAURITIUS',
    '2P': 'MAYOTTE',
    'O5': 'MEXICO',
    '1K': 'MICRONESIA, FEDERATED STATES OF',
    '1S': 'MOLDOVA, REPUBLIC OF',
    'O9': 'MONACO',
    'P0': 'MONGOLIA',
    'Z5': 'MONTENEGRO',
    'P1': 'MONTSERRAT',
    'P2': 'MOROCCO',
    'P3': 'MOZAMBIQUE',
    'E1': 'MYANMAR',
    'T6': 'NAMIBIA',
    'P5': 'NAURU',
    'P6': 'NEPAL',
    'P7': 'NETHERLANDS',
    'P8': 'NETHERLANDS ANTILLES',
    '1W': 'NEW CALEDONIA',
    'Q2': 'NEW ZEALAND',
    'Q3': 'NICARAGUA',
    'Q4': 'NIGER',
    'Q5': 'NIGERIA',
    'Q6': 'NIUE',
    'Q7': 'NORFOLK ISLAND',
    '1V': 'NORTHERN MARIANA ISLANDS',
    'Q8': 'NORWAY',
    'P4': 'OMAN',
    'R0': 'PAKISTAN',
    '1Y': 'PALAU',
    '1X': 'PALESTINIAN TERRITORY, OCCUPIED',
    'R1': 'PANAMA',
    'R2': 'PAPUA NEW GUINEA',
    'R4': 'PARAGUAY',
    'R5': 'PERU',
    'R6': 'PHILIPPINES',
    'R8': 'PITCAIRN',
    'R9': 'POLAND',
    'S1': 'PORTUGAL',
    'PR': 'PUERTO RICO',
    'S3': 'QATAR',
    'S4': 'REUNION',
    'S5': 'ROMANIA',
    '1Z': 'RUSSIAN FEDERATION',
    'S6': 'RWANDA',
    'Z0': 'SAINT BARTHELEMY',
    'U8': 'SAINT HELENA',
    'U7': 'SAINT KITTS AND NEVIS',
    'U9': 'SAINT LUCIA',
    'Z1': 'SAINT MARTIN',
    'V0': 'SAINT PIERRE AND MIQUELON',
    'V1': 'SAINT VINCENT AND THE GRENADINES',
    'Y0': 'SAMOA',
    'S8': 'SAN MARINO',
    'S9': 'SAO TOME AND PRINCIPE',
    'T0': 'SAUDI ARABIA',
    'T1': 'SENEGAL',
    'Z2': 'SERBIA',
    'T2': 'SEYCHELLES',
    'T8': 'SIERRA LEONE',
    'U0': 'SINGAPORE',
    '2B': 'SLOVAKIA',
    '2A': 'SLOVENIA',
    'D7': 'SOLOMON ISLANDS',
    'U1': 'SOMALIA',
    'T3': 'SOUTH AFRICA',
    '1L': 'SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS',
    'U3': 'SPAIN',
    'F1': 'SRI LANKA',
    'V2': 'SUDAN',
    'V3': 'SURINAME',
    'L9': 'SVALBARD AND JAN MAYEN',
    'V6': 'SWAZILAND',
    'V7': 'SWEDEN',
    'V8': 'SWITZERLAND',
    'V9': 'SYRIAN ARAB REPUBLIC',
    'F5': 'TAIWAN, PROVINCE OF CHINA',
    '2D': 'TAJIKISTAN',
    'W0': 'TANZANIA, UNITED REPUBLIC OF',
    'W1': 'THAILAND',
    'Z3': 'TIMOR-LESTE',
    'W2': 'TOGO',
    'W3': 'TOKELAU',
    'W4': 'TONGA',
    'W5': 'TRINIDAD AND TOBAGO',
    'W6': 'TUNISIA',
    'W8': 'TURKEY',
    '2E': 'TURKMENISTAN',
    'W7': 'TURKS AND CAICOS ISLANDS',
    '2G': 'TUVALU',
    'W9': 'UGANDA',
    '2H': 'UKRAINE',
    'C0': 'UNITED ARAB EMIRATES',
    'X0': 'UNITED KINGDOM',
    '2J': 'UNITED STATES MINOR OUTLYING ISLANDS',
    'X3': 'URUGUAY',
    '2K': 'UZBEKISTAN',
    '2L': 'VANUATU',
    'X5': 'VENEZUELA',
    'Q1': 'VIET NAM',
    'D8': 'VIRGIN ISLANDS, BRITISH',
    'VI': 'VIRGIN ISLANDS, U.S.',
    'X8': 'WALLIS AND FUTUNA',
    'U5': 'WESTERN SAHARA',
    'T7': 'YEMEN',
    'Y4': 'ZAMBIA',
    'Y5': 'ZIMBABWE',
    'XX': 'UNKNOWN',
}

Quarters = {
    'lastquarter',
    'secondlastquarter',
    'thirdlastquarter',
    'fourthlastquarter',
    'fifthlastquarter',
    'sixthlastquarter',
    'seventhlastquarter',
    'eighthlastquarter',
}

# Replacements variables
rep1 = 'Transition reports [Rule 13a-10 or 15d-10]Acc-no: '
rep2 = 'Annual report [Section 13 and 15(d), not S-K Item 405]Acc-no: '
rep3 = 'Quarterly report [Sections 13 or 15(d)]Acc-no: '

ARCH_IncomeStatement = {
    "CONSOLIDATED STATEMENTS OF INCOME",
    "CONSOLIDATED STATEMENTS OF OPERATIONS",
}

ARCH_ComprehensiveIncome = {
    "CONSOLIDATED STATEMENTS OF COMPREHENSIVE INCOME",
}

ARCH_BalanceSheet = {
    "CONSOLIDATED BALANCE SHEETS",
}

ARCH_StockholdersEquity = {
    "CONSOLIDATED STATEMENTS OF SHAREHOLDERS' EQUITY",
}

ARCH_CashFlowStatement = {
    "CONSOLIDATED STATEMENTS OF CASH FLOWS",
}

ARCH_FinancialStatements = {
    'ARCH_IncomeStatement',
    'ARCH_ComprehensiveIncome',
    'ARCH_BalanceSheet',
    'ARCH_ShareholdersEquity',
    'ARCH_CashFlowStatement',
}

IncomeStatement_GLs = []

ComprehensiveIncome_GLs = []

BalanceSheet_GLs = []

StockholdersEquity_GLs = []

CashFlow_GLs = []

# EntityCentralIndexKeys
# https://www.sec.gov/include/TradingSymbol.txt
EntityCentralIndexKeys = {
    'AAPL':    '320193',
    'CAT':    '18230',
    'WMT':    '104169',
}

# TradingSymbols
TradingSymbols = [
    'AAPL',
    #'CAT',
    #'WMT',
]

###############################################################################################################

for TradingSymbol in TradingSymbols:
    # Retreive or create object
    try:
        e = Entity.objects.get(TradingSymbol=TradingSymbol)
        print(137*'-')
        print(e.EntityRegistrantName + ' (' + e.TradingSymbol + ') retreived from φ.')
        print(137*'-')
    except:
        e = Entity()
        e.TradingSymbol = TradingSymbol
        e.EntityCentralIndexKey = EntityCentralIndexKeys[TradingSymbol]
        e.save()
        print(137*'-')
        print('New Entity for TradingSymbol ' + TradingSymbol + ' created in φ.')
        print(137*'-')
    ###########################################################################################################
    # Scoped
    ###########################################################################################################
    scopedperiods = [
        'lastquarter',
        'secondlastquarter',
        'thirdlastquarter',
        'lastyear',
        'secondlastyear',
        'thirdlastyear',
        'fourthlastyear',
        'fifthlastyear',
        'sixthlastyear',
        'seventhlastyear',
    ]
    for scopedperiod in scopedperiods:
        IncomeStatement = {}
        ComprehensiveIncome = {}
        BalanceSheet = {}
        StockholdersEquity = {}
        CashFlowStatement = {}
        #################################################################################################################################################
        try:
            print(137*'-')
            print('Arching ' + e.EntityRegistrantName + ' (' + e.TradingSymbol + '), ' + scopedperiod)
        except:
            print('---Could not print name, symbol or period.')
        #################################################################################################################################################
        # Deletes ARCH Trial Balance
        try:
            tb = TrialBalance.objects.get(TradingSymbol=TradingSymbol, Period=scopedperiod).delete()
            print(tb.TradingSymbol + ", " + tb.Period + " existing ARCH trial balance deleted from the φ.")
            tb.delete()
        except:
            pass
        # Creates ARCH Trial Balance
        try:
            tb = TrialBalance(TradingSymbol=TradingSymbol, Period=scopedperiod)
            tb.save()
            print(tb.TradingSymbol + ", " + scopedperiod.capitalize() + "'s ARCH trial balance created.")
        except:
            pass
        #################################################################################################################################################
        # Deletes ARCH Cash Flow Statements
        try:
            cf = CashFlow.objects.get(TradingSymbol=TradingSymbol, Period=scopedperiod).delete()
            print(cf.TradingSymbol + ", " + cf.Period + " existing ARCH cash flow statement deleted from the φ.")
            cf.delete()
        except:
            pass
        # Creates ARCH Cash Flow Statements
        try:
            cf = CashFlow(TradingSymbol=TradingSymbol, Period=scopedperiod)
            cf.save()
            print(cf.TradingSymbol + ", " + scopedperiod.capitalize() + "'s ARCH cash flow statement created.")
        except:
            pass
        #################################################################################################################################################
        # Deletes ARCH Data Audit Procedures
        try:
            a = AuditData.objects.get(TradingSymbol=TradingSymbol, Period=scopedperiod).delete()
            print(a.TradingSymbol + ", " + a.Period + " existing ARCH Audit procedure deleted from the φ.")
            a.delete()
        except:
            pass
        # Creates ARCH Audit Procedures
        try:
            a = AuditData(TradingSymbol=TradingSymbol, Period=scopedperiod)
            a.save()
            print(a.TradingSymbol + ", " + scopedperiod.capitalize() + "'s ARCH Audit procedure created.")
        except:
            pass
        #################################################################################################################################################
        # Retreive Entity's Information and last report's accession number
        try:
            filings_list_base_url = r"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="
            EntityCentralIndexKey = EntityCentralIndexKeys[TradingSymbol]
            print(EntityCentralIndexKey)
            if scopedperiod in Quarters:
                report = '10-Q'
                print(report)
                if scopedperiod == 'lastquarter':
                    periodurl = ''
            else:
                report = '10-K'
                print(report)
                if scopedperiod == 'lastyear':
                    periodurl = ''
            try:
                prior = periodurl
                filings_list_base_url = filings_list_base_url + EntityCentralIndexKey + '&type=' + report + '&dateb='
                print(filings_list_base_url)
                filings_url = filings_list_base_url + prior + '&owner=exclude&count=40&search_text='
                print(filings_url)
            except:
                filings_url = filings_list_base_url + '&owner=exclude&count=40&search_text='
                print(filings_url)
            filings_list_html = fetch(filings_url)
            # Company Info
            company_info_div = filings_list_html.find_all('div', class_='companyInfo')[0]
            e.EntityRegistrantName = company_info_div.find_all('span', class_='companyName')[0].text.split(' CIK')[0].upper()
            print(e.EntityRegistrantName)
            e.Industry = Industries[company_info_div.find_all('a')[1].text]
            print(e.Industry)
            e.Region = Regions[company_info_div.find_all('a')[2].text]
            print(e.Region)
            e.EntityIncorporationStateCountryCode = Regions[company_info_div.find_all('strong')[0].text]
            print(e.EntityIncorporationStateCountryCode)
            #################################################################################################################################################            
            e.save()
            print('Entity information saved.')
            #################################################################################################################################################
            # Amend (Update)
            #################################################################################################################################################
            # Accession Number
            i = 0
            # Make sure the document is an original
            accessionnumber = filings_list_html.find_all('td', class_='small')[i].text
            print(accessionnumber)
            while accessionnumber == '[Amend]':
                i = i + 1
                accessionnumber = filings_list_html.find_all('td', class_='small')[i].text
                print(accessionnumber)
            accessionnumber = accessionnumber.replace(rep1,'').replace(rep2,'').replace(rep3,'')[:20]
            print('Processing filing ' + accessionnumber + ' (' + report + ')')
        except:
            print("---Could not retreive accession number.")
        # Retreives documents URL 
        try:
            filing_documents_base_url = r"https://www.sec.gov/Archives/edgar/data/"
            filing_documents_url = filing_documents_base_url + EntityCentralIndexKey + '/' + accessionnumber.replace('-','') + '/' + accessionnumber + '-index.htm'
            tb.Link = filing_documents_url
            print('Documents URL: ' + filing_documents_url)
        except:
            print('---Could not retreive document`s url.')
        # Retreives html code from filing documents url
        try:
            filing_documents_html = fetch(filing_documents_url)
        except:
            print('---Could not retreive filing html.')
        # Retreive filing period of report
        try:
            period = filing_documents_html.find_all('div', class_="info")[3].text
            periodurl = period.replace('-','')
            if scopedperiod == 'lastquarter':
                periodlastquarter = period
                print('Last Quarter: ' + period)
            elif scopedperiod == 'lastyear':
                periodlastyear = period
                print('Last Year: ' + period)
            else:
                pass
        except:
            print('---Could not retreive filing report date.')
        # Retreive filing documents tables
        try:
            XBRL_taxonomy = filing_documents_html.find_all('table', class_="tableFile")[1].findAll('a')
        except:
            print('---Could not retreive filing documents tables')
        # Creates xml base url for calculation, definition and label 
        try:
            xml_base_url = filing_documents_base_url + EntityCentralIndexKey + '/' + accessionnumber.replace('-','') + '/'
        except:
            print('---Could not define xml_base_url')
        # Defines downloads directory
        try:
            downloads_directory = './φ/algorithm/downloads/'
        except:
            print('---Could not define downloads directory.')
        # Retreives filing document
        try:
            filing_document = filing_documents_html.find_all('td')[2].text
            filing_document = filing_document.split(' ')[0]
            print('Filing document: ' + filing_document)
            filing_url = xml_base_url + filing_document
            print('Filing url: ' + filing_url)
            r = requests.get(filing_url)
            with open(downloads_directory + '/' + filing_document, 'wb') as f:
                f.write(r.content)
                print('Filing saved.')
        except:
            print("---Could not retreive filing document")
        # Retreives calculation document
        try:
            calculation_document = XBRL_taxonomy[1].text
            print('Calculation document: ' + calculation_document)
            xml_cal = xml_base_url + calculation_document
            print('xml calculation url: ' + xml_cal)
            r = requests.get(xml_cal)
            with open(downloads_directory + '/' + calculation_document, 'wb') as f:
                f.write(r.content)
                print('xml_cal saved.')
        except:
            print('---Could not retreive calculation linkbase document')
        # Retreives definition document
        try:
            definition_document = XBRL_taxonomy[2].text
            print('Definition document: ' + definition_document)
            xml_def = xml_base_url + definition_document
            print('xml definition url: ' + xml_def)
            r = requests.get(xml_def)
            with open(downloads_directory + '/' + definition_document, 'wb') as f:
                f.write(r.content)
                print('xml_def saved.')
        except:
            print('---Could not retreive definition linkbase document')
        # Retreives label document
        try:
            label_document = XBRL_taxonomy[3].text
            print('Label document: ' + label_document)
            xml_lab = xml_base_url + label_document
            print('xml label url: ' + xml_lab)
            r = requests.get(xml_lab)
            with open(downloads_directory + '/' + label_document, 'wb') as f:
                f.write(r.content)
                print('xml_lab saved.')
        except:
            print('---Could not retreive label linkbase document')
        # Define downloads directory for SEC files
        try:
            SEC_directory = pathlib.Path.cwd().joinpath('./φ/algorithm/downloads')
        except:
            print('---Could not define path to downloads.')
        # Resolve path to files
        try:
            file_htm = SEC_directory.joinpath(filing_document).resolve()
            file_cal = SEC_directory.joinpath(calculation_document).resolve()
            file_def = SEC_directory.joinpath(definition_document).resolve()
            file_lab = SEC_directory.joinpath(label_document).resolve()
        except:
            print('Could not resolve directory.')
        # Define the different storage components
        try:
            storage_list = []
            storage_values = {}
            storage_gaap = {}
        except:
            print('---Could not define storage components')
        # Creates tuple
        try:
            FilingTuple = collections.namedtuple('FilingTuple',['file_path','namespace_element','namespace_label'])
        except:
            print('---Could not create tuples')
        # Initialize list of named tuples to be parsed
        try:
            files_list = [
                FilingTuple(file_cal, r'{http://www.xbrl.org/2003/linkbase}calculationLink', 'calculation'),
                FilingTuple(file_def, r'{http://www.xbrl.org/2003/linkbase}definitionLink', 'definition'),
                FilingTuple(file_lab, r'{http://www.xbrl.org/2003/linkbase}labelLink', 'label'),
            ]
        except:
            print('---Could not initialize list of named tuples to be parsed')
        # Defines categories of labels to be excluded
        try:
            avoids = ['linkbase','roleRef']
            parse = ['label','labelLink','labelArc','loc','definitionLink','definitionArc','calculationArc']
        except:
            print('---Could not define labels to be excluded')
        # Creates empty sets
        try:
            lab_list = set()
            cal_list = set()
        except:
            print('---Could not create empty sets.')
        # ARCHING METHODS
        try:
            f = open(file_htm, "r")
            content = f.read()
            if content[:5] == '<?xml':
                MethodAfter2018Applies = 'yes'
                # Method after 2018
                print(137*'-')
                print('Method after 2018 applies.')
                print(137*'-')
                try:
                    # Creates xml dictionary
                    for file in files_list:
                        tree = ET.parse(file.file_path)
                        elements = tree.findall(file.namespace_element)
                        # Loop through each element
                        for element in elements:
                            for child_element in element.iter():
                                element_split_label = child_element.tag.split('}')
                                namespace = element_split_label[0]
                                label = element_split_label[1]
                                # Establishs if it's a label we need
                                if label in parse:
                                    element_type_label = file.namespace_label + '_' + label
                                    dict_storage = {}
                                    dict_storage['item_type'] = element_type_label
                                    cal_keys = child_element.keys()
                                    # for each attributes
                                    for key in cal_keys:
                                        if '}' in key:
                                            new_key = key.split('}')[1]
                                            dict_storage[new_key] = child_element.attrib[key]
                                        else:
                                            dict_storage[key] = child_element.attrib[key]
                                    # Organizing information
                                    if element_type_label == 'label_label':
                                        key_store = dict_storage['label']
                                        master_key = key_store.replace('lab_', '')
                                        label_split = master_key.split('_')
                                        gaap_id = label_split[0] + ":" + label_split[1]
                                        # Adds the master key to the first countainer
                                        storage_values[master_key] = {}
                                        storage_values[master_key]['label_id'] = key_store
                                        storage_values[master_key]['location_id'] = key_store.replace('lab_','loc_')
                                        storage_values[master_key]['us_gaap_id'] = gaap_id
                                        storage_values[master_key]['us_gaap_value'] = None
                                        storage_values[master_key][element_type_label] = dict_storage
                                        # Adds the gaap metrics to another dictionnary
                                        storage_gaap[gaap_id] = {}
                                        storage_gaap[gaap_id]['id'] = gaap_id
                                        storage_gaap[gaap_id]['master_id'] = master_key
                                    # Add to dictionnary
                                    storage_list.append([file.namespace_label, dict_storage])
                    # Tree
                    try:
                        # Qualitative
                        tree = ET.parse(file_htm)
                        for element in tree.iter():
                            if 'nonNumeric' in element.tag:
                                # Grab the attribute name and the master ID
                                attr_name = element.attrib['name']
                                gaap_id = storage_gaap[attr_name]['master_id']
                                storage_gaap[attr_name]['context_ref'] = element.attrib['contextRef']
                                SEC_context = storage_gaap[attr_name]['context_ref']
                                storage_gaap[attr_name]['context_id'] = element.attrib['id']
                                storage_gaap[attr_name]['continued_at'] = element.attrib.get('continued_at', 'null')
                                storage_gaap[attr_name]['escape'] = element.attrib.get('escape', 'null')
                                storage_gaap[attr_name]['format'] = element.attrib.get('format', 'null')
                                storage_gaap[attr_name]['value'] = element.text.strip() if element.text else 'null'
                                value = storage_gaap[attr_name]['value']
                                SEC_component = str(attr_name.split(":")[1])
                                if SEC_component == 'EntityRegistrantName':
                                    tb.EntityRegistrantName = value
                                    print(SEC_component)
                                    print(value)
                                elif SEC_component == 'AmendmentFlag':
                                    tb.AmendmentFlag = value
                                    print(SEC_component)
                                    print(value)
                                elif SEC_component == 'DocumentFiscalPeriodFocus':
                                    tb.DocumentFiscalPeriodFocus = value
                                    print(SEC_component)
                                    print(value)
                                elif SEC_component == 'DocumentFiscalYearFocus':
                                    tb.DocumentFiscalYearFocus = value
                                    print(SEC_component)
                                    print(value)
                                elif SEC_component == 'DocumentPeriodEndDate':
                                    tb.DocumentPeriodEndDate = value
                                    print(SEC_component)
                                elif SEC_component == 'Industry':
                                    tb.Industry = value
                                elif SEC_component == 'EntityIncorporationStateCountryCode':
                                    tb.EntityIncorporationStateCountryCode = value
                                elif SEC_component == 'Region':
                                    tb.Region = value
                                elif SEC_component == 'CurrentFiscalYearEndDate':
                                    tb.CurrentFiscalYearEndDate = value
                                elif SEC_component == 'SecurityExchangeName':
                                    tb.SecurityExchangeName = value
                        # Quantitative
                        tree = ET.parse(file_htm)
                        for element in tree.iter():
                            if 'nonFraction' in element.tag:
                                try:
                                    attr_name = element.attrib['name']
                                    gaap_id = storage_gaap[attr_name]['master_id']
                                    storage_values[gaap_id]['us_gaap_value'] = storage_gaap[attr_name]
                                    account = storage_values[gaap_id]['us_gaap_value']
                                    storage_gaap[attr_name]['context_ref'] = element.attrib['contextRef']
                                    storage_gaap[attr_name]['fraction_id'] = element.attrib['id']
                                    storage_gaap[attr_name]['unit_ref'] = element.attrib.get('unitRef', 'null')
                                    storage_gaap[attr_name]['decimals'] = element.attrib.get('decimals', 'null')
                                    storage_gaap[attr_name]['scale'] = element.attrib.get('scale', 'null')
                                    storage_gaap[attr_name]['sign'] = element.attrib.get('sign', 'null')
                                    storage_gaap[attr_name]['format'] = element.attrib.get('format', 'null')
                                    storage_gaap[attr_name]['value'] = element.text.strip() if element.text else 'null'
                                    source = str(attr_name.split(":")[1])
                                    if storage_gaap[attr_name]['sign'] == '-':
                                        sign = -1
                                    else:
                                        sign = 1
                                    # Dad
                                    try:
                                        dad = 10**int(account.get('scale'))
                                    except:
                                        dad = 1
                                    # Type
                                    try:
                                        SECvalue = int(float(account.get('value').replace(",","")) * dad * sign)
                                    except:
                                        pass
                                except:
                                    pass
                        tb.save()
                    except:
                        print('---Could not arch elements.')
                except:
                    print('---Could not complete method 1 sequence')
            # Method 2 (before 2019)
            else:
                MethodAfter2018Applies = 'no'
                print('Method after 2018 does not apply.')
            print(137*'-')
            print('General Method.')
            print(137*'-')
            # Documents
            try:
                base_url = r"https://www.sec.gov"
                index_url = xml_base_url + 'index.json'
                content = requests.get(index_url).json()
                for file in content['directory']['item']:
                    if file['name'] == 'FilingSummary.xml':
                        xml_summary = base_url + content['directory']['name'] + '/' + file['name']
            except:
                print('---Could not define directory url.')
            try:
                base_url = xml_summary.replace('FilingSummary.xml', '')
                content = requests.get(xml_summary).content
                soup = BeautifulSoup(content, 'lxml')
                reports = soup.find('myreports')
                # Master list of reports
                master_reports = []
                for report in reports.find_all('report')[:-1]:
                    report_dict = {}
                    report_dict['name_short'] = report.shortname.text
                    report_dict['name_long'] = report.longname.text
                    report_dict['position'] = report.position.text
                    report_dict['category'] = report.menucategory.text
                    report_dict['url'] = base_url + report.htmlfilename.text
                    master_reports.append(report_dict)
                # Statements urls
                statements_url = []
                statements_set = {}
                for report_dict in master_reports:
                    report_list = {
                        "CONSOLIDATED STATEMENTS OF INCOME",
                        "CONSOLIDATED STATEMENTS OF OPERATIONS",
                        "CONSOLIDATED STATEMENTS OF COMPREHENSIVE INCOME",
                        "CONSOLIDATED BALANCE SHEETS",
                        "CONSOLIDATED STATEMENTS OF SHAREHOLDERS' EQUITY",
                        "CONSOLIDATED STATEMENTS OF CASH FLOWS",
                    }
                    if report_dict['name_short'].upper() in report_list:
                        financial_url = report_dict['url']
                        financial_set = report_dict['name_short'],
                        append_value(statements_set, financial_set,  financial_url)
                        statements_url.append(financial_url)
                print(statements_set)
                # Statements data
                i = 0
                statements_data = []
                for financial_set in statements_set:
                    financial_statement = financial_set[0]
                    statement = statements_set[financial_set]
                    print(statement)
                    statement_data = {}
                    statement_data['headers'] = []
                    statement_data['sections'] = []
                    statement_data['data'] = []
                    content = requests.get(statement).content
                    report_soup = BeautifulSoup(content, 'html')
                    for index, row in enumerate(report_soup.table.find_all('tr')):
                        cols = row.find_all('td')
                        if (len(row.find_all('th')) == 0 and len(row.find_all('strong')) == 0):
                            reg_row = [ele.text.strip() for ele in cols]
                            account = reg_row[0]
                            value = reg_row[1]
                            if financial_statement in ARCH_StockholdersEquity:
                                value = 0
                                i = 2
                                while i <= (len(reg_row) - 1):
                                    column_value = reg_row[i].replace('$','').replace(' ','').replace(',','').replace('(','-').replace(')','')
                                    if column_value == '':
                                        column_value = 0
                                    value = value + int(column_value)
                                    i = i + 1
                            ARCH_GL = [
                                financial_statement,
                                account,
                                value,
                            ]
                            print(ARCH_GL)
                            statement_data['data'].append(ARCH_GL)
                        elif (len(row.find_all('th')) == 0 and len(row.find_all('strong')) != 0):
                            sec_row = cols[0].text.strip()
                            statement_data['sections'].append(sec_row)
                        elif len(row.find_all('th')) != 0:
                            hed_row = [ele.text.strip() for ele in row.find_all('th')]
                            statement_data['headers'].append(hed_row)
                        else:
                            print('---Could not distinguish headers from section and regular rows.')
                    statements_data.append(statement_data)
                    i = i + 1
                print(137*'-')
                # Define documents period end date
                if MethodAfter2018Applies == 'no':
                    print('Period End Date From General Method')
                    DPED = statements_data[0]['headers'][1][0].replace('Jan.', 'January').replace('Feb.', 'February').replace('Mar.', 'March')
                    DPED = DPED.replace('Apr.', 'April').replace('Jun.', 'June').replace('Jul.', 'July').replace('Aug.', 'August')
                    DPED = DPED.replace('Sep.', 'September').replace('Oct.', 'October').replace('Nov.', 'November').replace('Dec.', 'December')
                    tb.DocumentPeriodEndDate = DPED
                print('Document Period End Date: ' + str(tb.DocumentPeriodEndDate))
                # Define entity period end date
                try:
                    if scopedperiod == 'lastquarter':
                        e.lastquarter =  tb.DocumentPeriodEndDate
                    elif scopedperiod == 'secondlastquarter':
                        e.secondlastquarter =  tb.DocumentPeriodEndDate
                    elif scopedperiod == 'thirdlastquarter':
                        e.thirdlastquarter =  tb.DocumentPeriodEndDate
                    elif scopedperiod == 'fourthlastquarter':
                        e.fourthlastquarter =  tb.DocumentPeriodEndDate
                    elif scopedperiod == 'lastyear':
                        e.lastyear =  tb.DocumentPeriodEndDate
                    elif scopedperiod == 'secondlastyear':
                        e.secondlastyear =  tb.DocumentPeriodEndDate
                    elif scopedperiod == 'thirdlastyear':
                        e.thirdlastyear =  tb.DocumentPeriodEndDate
                    elif scopedperiod == 'fourthlastyear':
                        e.fourthlastyear =  tb.DocumentPeriodEndDate
                    elif scopedperiod == 'fifthlastyear':
                        e.fifthlastyear =  tb.DocumentPeriodEndDate
                    elif scopedperiod == 'sixthlastyear':
                        e.sixthlastyear =  tb.DocumentPeriodEndDate
                    elif scopedperiod == 'seventhlastyear':
                        e.seventhlastyear =  tb.DocumentPeriodEndDate
                    else:
                        pass
                except:
                    print('---Could Not Define Entity`s Period End Dates')
                # dad
                if statement_data['headers'][0][0][-11:].upper() == 'IN MILLIONS':
                    dad = 1000000
                elif statement_data['headers'][0][0][-12:].upper() == 'IN THOUSANDS':
                    dad = 1000
                else:
                    dad = 1
                # Line Header
                i = 0
                while len(statements_data) > i:
                    j = 0
                    while len(statements_data[i]['data']) > j:
                        try:
                            financial_statement = statements_data[i]['data'][j][0]
                            source = statements_data[i]['data'][j][1].title()
                            source = source.replace(',','').replace('.','').replace('’','').replace("'","").replace('/','')
                            source = source.replace('0','').replace('1','').replace('2','').replace('3','').replace('4','')
                            source = source.replace('5','').replace('6','').replace('7','').replace('8','').replace('9','')
                            source = source.replace(' ','').replace('-','').replace('_','').replace('(','').replace(')','').replace('$','')
                            GL = source.replace('[','').replace(']','').replace(':','').replace(';','')
                            value = statements_data[i]['data'][j][2]
                            try:
                                value = value.replace(',','').replace(' ','').replace('$','')
                                if value[0] == '(':
                                    value = value.replace('(','').replace(')','')
                                    value = -int(value)
                                else:
                                    value = int(value)
                            except:
                                value = int(value)
                            value = value * dad
                            if financial_statement in ARCH_IncomeStatement:
                                append_value(IncomeStatement, GL, value)
                                IncomeStatement_GLs.append(GL)
                            elif financial_statement in ARCH_ComprehensiveIncome:
                                append_value(ComprehensiveIncome, GL, value)
                                ComprehensiveIncome_GLs.append(GL)
                            elif financial_statement in ARCH_BalanceSheet:
                                append_value(BalanceSheet, GL, value)
                                BalanceSheet_GLs.append(GL)
                            elif financial_statement in ARCH_StockholdersEquity:
                                append_value(StockholdersEquity, GL, value)
                                StockholdersEquity_GLs.append(GL)
                            elif financial_statement in ARCH_CashFlowStatement:
                                append_value(CashFlowStatement, GL, value)
                                CashFlow_GLs.append(GL)
                            else:
                                pass
                        except:
                            print('---Could not ARCH ' + GL + ' from ' + financial_statement)
                        j = j + 1
                    i = i + 1
            except:
                print('---Could not complete general sequence')
        except:
            print('---Could not establish which method to use')
        print(137*'-')
        print('Income Statement')
        print(IncomeStatement)
        print(137*'-')
        print('Comprehensive Income')
        print(ComprehensiveIncome)
        print(137*'-')
        print('Balance Sheet')
        print(BalanceSheet)
        print(137*'-')
        print('Stockholders Equity')
        print(StockholdersEquity)
        print(137*'-')
        print('Cash Flow Statement')
        print(CashFlowStatement)
        print(137*'-')
        # Save
        try:
            tb.save()
            e.save()
            print(e.EntityRegistrantName + ' (' + e.TradingSymbol + '), ' + tb.DocumentPeriodEndDate + ' (' + tb.Period + ') SEC Data Saved.')
        except:
            print('---Could not save.')
        # Delete the content of the download file
        files = glob.glob('A:/arch/φ/algorithm/downloads/*')
        for f in files:
            os.remove(f)
        print('A:/arch/φ/algorithm/downloads/ repository cleared.')
        ############################################################################################################################################################################################################################ 
        # (Update basis of 1000)
        ############################################################################################################################################################################################################################ 
        # Number of Shares Outstanding
        try:
            OutstandingSharesURL = 'https://www.sec.gov/Archives/edgar/data/' + EntityCentralIndexKey + '/' + accessionnumber.replace('-','') + '/' 'R1.htm'
            PublicFloatAndOutstandingShares = fetch(OutstandingSharesURL).find_all('td', class_="nump")
            tb.EntityCommonStockSharesOutstanding = 1000 * max(int(float(PublicFloatAndOutstandingShares[0].text.replace(',', '').replace('$', ''))), int(float(PublicFloatAndOutstandingShares[1].text.replace(',', '').replace('$', ''))))
            tb.save()
            print(str(tb.EntityCommonStockSharesOutstanding) + " Common Shares Outstanding.")
        except:
            pass
        ###############################################################################################################
        # STOCK PRICE
        ###############################################################################################################
        print(137*'-')
        print('STOCK PRICE')
        print(137*'-')
        ###############################################################################################################
        print('Update')
        # FINANCIAL STATEMENTS
        ###############################################################################################################
        # BALANCE SHEETS
        ###############################################################################################################
        print(137*'-')
        print('BALANCE SHEETS')
        print(137*'-')
        ###############################################################################################################
        # CURRENT ASSETS
        ###############################################################################################################
        print(137*'-')
        print('CURRENT ASSETS')
        print(137*'-')
        ###############################################################################################################
        CurrentAssetsDict = []
        # Cash
        try:
            Cash = []
            for key,value in BalanceSheet.items():
                if key == 'CashAndCashEquivalentsAtCarryingValue':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Cash And Cash Equivalents At Carrying Value: ' + str(ARCHvalue))
                    Cash.append(ARCHvalue)
                elif key == 'CashAndCashEquivalents':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Cash And Cash Equivalents: ' + str(ARCHvalue))
                    Cash.append(ARCHvalue)
                else:
                    pass
            tb.Cash = sum(Cash)
            CurrentAssetsDict.append(tb.Cash)
            print()
            print('Cash: ' + str(tb.Cash) + ' $')
            print(15*"-")
        except:
            pass
        # Short Term Investment
        try:
            ShortTermInvestments = []
            for key,value in BalanceSheet.items():
                if key == 'MarketableSecuritiesCurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Securities Current: ' + str(ARCHvalue))
                    ShortTermInvestments.append(ARCHvalue)
                elif key == 'MarketableSecurities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Marketable Securities: ' + str(ARCHvalue))
                    ShortTermInvestments.append(ARCHvalue)
                elif key == 'ShortTermMarketableSecurities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Short Term Marketable Securities: ' + str(ARCHvalue))
                    ShortTermInvestments.append(ARCHvalue)
                elif key == 'AvailableForSaleSecuritiesDebtSecuritiesCurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Available For Sale Securities Debt Securities Current: ' + str(ARCHvalue))
                    ShortTermInvestments.append(ARCHvalue)
                else:
                    pass
            tb.ShortTermInvestments = sum(ShortTermInvestments)
            CurrentAssetsDict.append(tb.ShortTermInvestments)
            print()
            print('Short Term Investment: ' + str(tb.ShortTermInvestments) + ' $')
            print(15*"-")
        except:
            pass
        # Account Receivable
        try:
            AccountsReceivable = []
            for key,value in BalanceSheet.items():
                if key == 'AccountsReceivableNetCurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Accounts Receivable Net Current: ' + str(ARCHvalue))
                    AccountsReceivable.append(ARCHvalue)
                elif key == 'AccountsReceivableNet':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Accounts ReceivableNet: ' + str(ARCHvalue))
                    AccountsReceivable.append(ARCHvalue)
                elif key == 'AccountsReceivableLessAllowancesOfAndRespectively':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Accounts Receivable Less Allowances Of And Respectively: ' + str(ARCHvalue))
                    AccountsReceivable.append(ARCHvalue)
                else:
                    pass
            tb.AccountsReceivable = sum(AccountsReceivable)
            CurrentAssetsDict.append(tb.AccountsReceivable)
            print()
            print('Accounts Receivable: ' + str(tb.AccountsReceivable) + ' $')
            print(15*"-")
        except:
            pass
        # Inventories
        try:
            Inventories = []
            for key,value in BalanceSheet.items():
                if key == 'InventoryNet':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Inventory Net: ' + str(ARCHvalue))
                    Inventories.append(ARCHvalue)
                elif key == 'Inventories':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Inventories: ' + str(ARCHvalue))
                    Inventories.append(ARCHvalue)
                else:
                    pass
            tb.Inventories = sum(Inventories)
            CurrentAssetsDict.append(tb.Inventories)
            print()
            print('Inventories: ' + str(tb.Inventories) + ' $')
            print(15*"-")
        except:
            pass
        # Prepaid Expenses
        try:
            PrepaidExpenses = []
            for key,value in BalanceSheet.items():
                if key == 'PrepaidExpenseAndOtherAssetsCurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Prepaid Expense And Other Assets Current: ' + str(ARCHvalue))
                    PrepaidExpenses.append(ARCHvalue)
                else:
                    pass
            tb.PrepaidExpenses = sum(PrepaidExpenses)
            CurrentAssetsDict.append(tb.PrepaidExpenses)
            print()
            print('Prepaid Expenses: ' + str(tb.PrepaidExpenses) + ' $')
            print(15*"-")
        except:
            pass
        # Non-Trade Receivables
        try:
            NonTradeReceivables = []
            for key,value in BalanceSheet.items():
                if key == 'NontradeReceivablesCurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Non trade Receivables Current: ' + str(ARCHvalue))
                    NonTradeReceivables.append(ARCHvalue)
                elif key == 'VendorNonTradeReceivables':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Vendor Non Trade Receivables: ' + str(ARCHvalue))
                    NonTradeReceivables.append(ARCHvalue)
                else:
                    pass
            tb.NonTradeReceivables = sum(NonTradeReceivables)
            CurrentAssetsDict.append(tb.NonTradeReceivables)
            print()
            print('Non Trade Receivables: ' + str(tb.NonTradeReceivables) + ' $')
            print(15*"-")
        except:
            pass
        # Deferred Tax Assets
        try:
            DeferredTaxAssets = []
            for key,value in BalanceSheet.items():
                if key == 'DeferredTaxAssets':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Deferred Tax Assets: ' + str(ARCHvalue))
                    DeferredTaxAssets.append(ARCHvalue)
                else:
                    pass
            tb.DeferredTaxAssets = sum(DeferredTaxAssets)
            CurrentAssetsDict.append(tb.DeferredTaxAssets)
            print()
            print('Deferred Tax Assets: ' + str(tb.DeferredTaxAssets) + ' $')
            print(15*"-")
        except:
            pass
        # Other Current Assets
        try:
            OtherCurrentAssets = []
            for key,value in BalanceSheet.items():
                if key == 'OtherAssetsCurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Other Assets Current: ' + str(ARCHvalue))
                    OtherCurrentAssets.append(ARCHvalue)
                elif key == 'OtherCurrentAssets':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Other Current Assets: ' + str(ARCHvalue))
                    OtherCurrentAssets.append(ARCHvalue)
                else:
                    pass
            tb.OtherCurrentAssets = sum(OtherCurrentAssets)
            CurrentAssetsDict.append(tb.OtherCurrentAssets)
            print()
            print('Other Current Assets: ' + str(tb.OtherCurrentAssets) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Total Current Assets
        try:
            TotalCurrentAssets = []
            for key,value in BalanceSheet.items():
                if key == 'AssetsCurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Assets Current: ' + str(ARCHvalue))
                    TotalCurrentAssets.append(ARCHvalue)
                elif key == 'TotalCurrentAssets':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Total Current Assets: ' + str(ARCHvalue))
                    TotalCurrentAssets.append(ARCHvalue)
                else:
                    pass
            a.CurrentAssets = sum(TotalCurrentAssets)
            print()
            print('Total Current Assets: ' + str(a.CurrentAssets) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # NON-CURRENT ASSETS
        ###############################################################################################################
        print(137*'-')
        print('NON-CURRENT ASSETS')
        print(137*'-')
        NonCurrentAssetsDict = []
        # Investments
        try:
            Investments = []
            for key,value in BalanceSheet.items():
                if key == 'MarketableSecuritiesNoncurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Marketable Securities Non current: ' + str(ARCHvalue))
                    Investments.append(ARCHvalue)
                elif key == 'LongTermMarketableSecurities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Long Term Marketable Securities: ' + str(ARCHvalue))
                    Investments.append(ARCHvalue)
                elif key == 'MarketableSecurities':
                    try:
                        ARCHvalue = value[1]
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Marketable Securities: ' + str(ARCHvalue))
                    Investments.append(ARCHvalue)
                else:
                    pass
            tb.Investments = sum(Investments)
            NonCurrentAssetsDict.append(tb.Investments)
            print()
            print('Investments: ' + str(tb.Investments) + ' $')
            print(15*"-")
        except:
            pass
        # Property Plant And Equipments
        try:
            PropertyPlantAndEquipment = []
            for key,value in BalanceSheet.items():
                if key == 'PropertyPlantAndEquipmentNet':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Property Plant And Equipment Net: ' + str(ARCHvalue))
                    PropertyPlantAndEquipment.append(ARCHvalue)
                elif key == 'PropertyPlantAndEquipmentAndFinanceLeaseRightofUseAssetAfterAccumulatedDepreciationAndAmortization':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Property Plant And Equipment And Finance Lease Right of Use Asset After Accumulated Depreciation And Amortization: ' + str(ARCHvalue))
                    PropertyPlantAndEquipment.append(ARCHvalue)
                else:
                    pass
            tb.PropertyPlantAndEquipment = sum(PropertyPlantAndEquipment)
            NonCurrentAssetsDict.append(tb.PropertyPlantAndEquipment)
            print()
            print('Property Plant And Equipment: ' + str(tb.PropertyPlantAndEquipment) + ' $')
            print(15*"-")
        except:
            pass
        # Right Of Use Assets
        try:
            RightOfUseAssets = []
            for key,value in BalanceSheet.items():
                if key == 'OperatingLeaseRightOfUseAsset':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Operating Lease Right Of Use Asset: ' + str(ARCHvalue))
                    RightOfUseAssets.append(ARCHvalue)
                else:
                    pass
            tb.RightOfUseAssets = sum(RightOfUseAssets)
            NonCurrentAssetsDict.append(tb.RightOfUseAssets)
            print()
            print('Right Of Use Asset: ' + str(tb.RightOfUseAssets) + ' $')
            print(15*"-")
        except:
            pass
        # Intangible Assets
        try:
            IntangibleAssets = []
            for key,value in BalanceSheet.items():
                if key == 'IntangibleAssetsNetExcludingGoodwill':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Intangible Assets Net Excluding Goodwill: ' + str(ARCHvalue))
                    IntangibleAssets.append(ARCHvalue)
                else:
                    pass
            tb.IntangibleAssets = sum(IntangibleAssets)
            NonCurrentAssetsDict.append(tb.IntangibleAssets)
            print()
            print('Intangible Assets: ' + str(tb.IntangibleAssets) + ' $')
            print(15*"-")
        except:
            pass
        # Goodwill
        try:
            Goodwill = []
            for key,value in BalanceSheet.items():
                if key == 'Goodwill':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Goodwill: ' + str(ARCHvalue))
                    Goodwill.append(ARCHvalue)
                else:
                    pass
            tb.Goodwill = sum(Goodwill)
            NonCurrentAssetsDict.append(tb.Goodwill)
            print()
            print('Goodwill: ' + str(tb.Goodwill) + ' $')
            print(15*"-")
        except:
            pass
        # Other Non-Current Assets
        try:
            OtherNonCurrentAssets = []
            for key,value in BalanceSheet.items():
                if key == 'OtherAssetsNoncurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Other Assets Non current: ' + str(ARCHvalue))
                    OtherNonCurrentAssets.append(ARCHvalue)
                elif key == 'OtherNonCurrentAssets':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Other Non Current Assets: ' + str(ARCHvalue))
                    OtherNonCurrentAssets.append(ARCHvalue)
                else:
                    pass
            tb.OtherNonCurrentAssets = sum(OtherNonCurrentAssets)
            NonCurrentAssetsDict.append(tb.OtherNonCurrentAssets)
            print()
            print('Other Non Current Assets: ' + str(tb.OtherNonCurrentAssets) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Total Non Current Assets
        try:
            TotalNonCurrentAssets = []
            for key,value in BalanceSheet.items():
                if key == 'AssetsNoncurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Assets Non current: ' + str(ARCHvalue))
                    TotalNonCurrentAssets.append(ARCHvalue)
                elif key == 'TotalNonCurrentAssets':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Total Non Current Assets: ' + str(ARCHvalue))
                    TotalNonCurrentAssets.append(ARCHvalue)
                else:
                    pass
            a.NonCurrentAssets = sum(TotalNonCurrentAssets)
            print()
            print('Total Non Current Assets: ' + str(a.NonCurrentAssets) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Total Assets
        try:
            TotalAssets = []
            for key,value in BalanceSheet.items():
                if key == 'Assets':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Assets: ' + str(ARCHvalue))
                    TotalAssets.append(ARCHvalue)
                elif key == 'TotalAssets':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Total Assets: ' + str(ARCHvalue))
                    TotalAssets.append(ARCHvalue)
                else:
                    pass
            a.Assets = sum(TotalAssets)
            print()
            print('Total Assets: ' + str(a.Assets) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        try:
            if a.NonCurrentAssets == 0:
                a.NonCurrentAssets = a.Assets - a.CurrentAssets
        except:
            pass
        ###############################################################################################################
        # LIABILITIES
        ###############################################################################################################
        print(137*'-')
        print('LIABILITIES')
        print(137*'-')
        # CURRENT LIABILITIES
        ###############################################################################################################
        print(137*'-')
        print('CURRENT LIABILITIES')
        print(137*'-')
        CurrentLiabilitiesDict = []
        # Accounts Payable And Accrued Liabilities
        try:
            AccountsPayableAndAccruedLiabilities = []
            for key,value in BalanceSheet.items():
                if key == 'AccountsPayableCurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Accounts Payable Current: ' + str(ARCHvalue))
                    AccountsPayableAndAccruedLiabilities.append(ARCHvalue)
                elif key == 'AccountsPayable':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Accounts Payable: ' + str(ARCHvalue))
                    AccountsPayableAndAccruedLiabilities.append(ARCHvalue)
                elif key == 'AccruedExpenses':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Current Liabilities Accrued Expenses: ' + str(ARCHvalue))
                    AccountsPayableAndAccruedLiabilities.append(ARCHvalue)
                elif key == 'AccruedLiabilitiesCurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Accrued Liabilities Current: ' + str(ARCHvalue))
                    AccountsPayableAndAccruedLiabilities.append(ARCHvalue)
                else:
                    pass
            tb.AccountsPayableAndAccruedLiabilities = -sum(AccountsPayableAndAccruedLiabilities)
            CurrentLiabilitiesDict.append(tb.AccountsPayableAndAccruedLiabilities)
            print()
            print('Accounts Payable And Accrued Liabilities: ' + str(tb.AccountsPayableAndAccruedLiabilities) + ' $')
            print(15*"-")
        except:
            pass
        # Operating Leases Current
        try:
            OperatingLeasesCurrent = []
            for key,value in BalanceSheet.items():
                if key == 'OperatingLeaseLiabilityCurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Operating Lease Liability Current: ' + str(ARCHvalue))
                    OperatingLeasesCurrent.append(ARCHvalue)
                else:
                    pass
            tb.OperatingLeasesCurrent = -sum(OperatingLeasesCurrent)
            CurrentLiabilitiesDict.append(tb.OperatingLeasesCurrent)
            print()
            print('Operating Leases Current: ' + str(tb.OperatingLeasesCurrent) + ' $')
            print(15*"-")
        except:
            pass
        # Deferred Revenue And Deposits Current
        try:
            DeferredRevenueAndDepositsCurrent = []
            for key,value in BalanceSheet.items():
                if key == 'ContractWithCustomerLiabilityCurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Contract With Customer Liability Current: ' + str(ARCHvalue))
                    DeferredRevenueAndDepositsCurrent.append(ARCHvalue)
                elif key == 'DeferredRevenue':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Deferred Revenue: ' + str(ARCHvalue))
                    DeferredRevenueAndDepositsCurrent.append(ARCHvalue)
                else:
                    pass
            tb.DeferredRevenueAndDepositsCurrent = -sum(DeferredRevenueAndDepositsCurrent)
            CurrentLiabilitiesDict.append(tb.DeferredRevenueAndDepositsCurrent)
            print()
            print('Deferred Revenue And Deposits Current: ' + str(tb.DeferredRevenueAndDepositsCurrent) + ' $')
            print(15*"-")
        except:
            pass
        # Other Short Term Borrowings And Current Liabilities
        try:
            OtherShortTermBorrowingsAndCurrentLiabilities = []
            for key,value in BalanceSheet.items():
                if key == 'OtherLiabilitiesCurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Other Liabilities Current: ' + str(ARCHvalue))
                    OtherShortTermBorrowingsAndCurrentLiabilities.append(ARCHvalue)
                elif key == 'OtherCurrentLiabilities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Other Current Liabilities: ' + str(ARCHvalue))
                    OtherShortTermBorrowingsAndCurrentLiabilities.append(ARCHvalue)
                elif key == 'CommercialPaper':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Commercial Paper: ' + str(ARCHvalue))
                    OtherShortTermBorrowingsAndCurrentLiabilities.append(ARCHvalue)
                elif key == 'AccountsPayableTradeCurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Accounts Payable Trade Current: ' + str(ARCHvalue))
                    OtherShortTermBorrowingsAndCurrentLiabilities.append(ARCHvalue)
                else:
                    pass
            tb.OtherShortTermBorrowingsAndCurrentLiabilities = -sum(OtherShortTermBorrowingsAndCurrentLiabilities)
            CurrentLiabilitiesDict.append(tb.OtherShortTermBorrowingsAndCurrentLiabilities)
            print()
            print('Other Short Term Borrowings And Current Liabilities: ' + str(tb.OtherShortTermBorrowingsAndCurrentLiabilities) + ' $')
            print(15*"-")
        except:
            pass
        # Short Term Portion Of Long Term Debt
        try:
            ShortTermPortionOfLongTermDebt = []
            for key,value in BalanceSheet.items():
                if key == 'LongTermDebtCurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Long Term Debt Current: ' + str(ARCHvalue))
                    ShortTermPortionOfLongTermDebt.append(ARCHvalue)
                elif key == 'CurrentPortionOfLongTermDebt':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Current Portion Of Long Term Debt: ' + str(ARCHvalue))
                    ShortTermPortionOfLongTermDebt.append(value)
                if key == 'TermDebt':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Term Debt: ' + str(ARCHvalue))
                    ShortTermPortionOfLongTermDebt.append(ARCHvalue)
                else:
                    pass
            tb.ShortTermPortionOfLongTermDebt = -sum(ShortTermPortionOfLongTermDebt)
            CurrentLiabilitiesDict.append(tb.ShortTermPortionOfLongTermDebt)
            print()
            print('Short Term Portion Of Long Term Debt: ' + str(tb.ShortTermPortionOfLongTermDebt) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Total Current Liabilities
        try:
            TotalCurrentLiabilities = []
            for key,value in BalanceSheet.items():
                if key == 'LiabilitiesCurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Liabilities Current: ' + str(ARCHvalue))
                    TotalCurrentLiabilities.append(ARCHvalue)
                elif key == 'TotalCurrentLiabilities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Total Current Liabilities: ' + str(ARCHvalue))
                    TotalCurrentLiabilities.append(ARCHvalue)
                else:
                    pass
            a.CurrentLiabilities = -sum(TotalCurrentLiabilities)
            print()
            print('Total Current Liabilities: ' + str(tb.TotalCurrentLiabilities) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Anomaly Current Liabilities
        try:
            Anomaly = a.CurrentLiabilities - sum(CurrentLiabilitiesDict)
        except:
            pass
        ###############################################################################################################
        # NON-CURRENT LIABILITIES
        ###############################################################################################################
        print(137*'-')
        print('NON-CURRENT LIABILITIES')
        print(137*'-')
        NonCurrentLiabilitiesDict = []
        # Long-Term Debt
        try:
            LongTermDebt = []
            for key,value in BalanceSheet.items():
                if key == 'LongTermDebtNoncurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Long Term Debt Non current: ' + str(ARCHvalue))
                    LongTermDebt.append(ARCHvalue)
                elif key == 'LongTermDebt':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Long Term Debt: ' + str(ARCHvalue))
                    LongTermDebt.append(ARCHvalue)
                if key == 'TermDebt':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Term Debt: ' + str(ARCHvalue))
                    LongTermDebt.append(ARCHvalue)
                else:
                    pass
            tb.LongTermDebt = -sum(LongTermDebt)
            NonCurrentLiabilitiesDict.append(tb.LongTermDebt)
            print()
            print('Long Term Debt: ' + str(tb.LongTermDebt) + ' $')
            print(15*"-")
        except:
            pass
        # Operating Leases Non-Current
        try:
            OperatingLeasesNonCurrent = []
            for key,value in BalanceSheet.items():
                if key == 'OperatingLeaseLiabilityNoncurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Operating Lease Liability Non current: ' + str(ARCHvalue))
                    OperatingLeasesNonCurrent.append(ARCHvalue)
                else:
                    pass
            tb.OperatingLeasesNonCurrent = -sum(OperatingLeasesNonCurrent)
            NonCurrentLiabilitiesDict.append(tb.OperatingLeasesNonCurrent)
            print()
            print('Operating Leases Non-Current: ' + str(tb.OperatingLeasesNonCurrent) + ' $')
            print(15*"-")
        except:
            pass
        # Deferred Revenue and Deposits Non-Current
        try:
            DeferredRevenueAndDepositsNonCurrent = []
            for key,value in BalanceSheet.items():
                if key == 'DeferredRevenue':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Deferred Revenue: ' + str(ARCHvalue))
                    DeferredRevenueAndDepositsNonCurrent.append(ARCHvalue)
                elif key == 'DeferredRevenueNonCurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Deferred Revenue Non Current: ' + str(ARCHvalue))
                    DeferredRevenueAndDepositsNonCurrent.append(ARCHvalue)
                else:
                    pass
            tb.DeferredRevenueAndDepositsNonCurrent = -sum(DeferredRevenueAndDepositsNonCurrent)
            NonCurrentLiabilitiesDict.append(tb.DeferredRevenueAndDepositsNonCurrent)
            print()
            print('Deferred Revenue and DepositsNonCurrent: ' + str(tb.DeferredRevenueAndDepositsNonCurrent) + ' $')
            print(15*"-")
        except:
            pass
        # Other Non-Current Liabilities
        try:
            OtherNonCurrentLiabilities = []
            for key,value in BalanceSheet.items():
                if key == 'OtherLiabilitiesNoncurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Other Liabilities Non current: ' + str(ARCHvalue))
                    OtherNonCurrentLiabilities.append(ARCHvalue)
                elif key == 'OtherNonCurrentLiabilities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Other Non Current Liabilities: ' + str(ARCHvalue))
                    OtherNonCurrentLiabilities.append(ARCHvalue)
                else:
                    pass
            tb.OtherNonCurrentLiabilities = -sum(OtherNonCurrentLiabilities)
            NonCurrentLiabilitiesDict.append(tb.OtherNonCurrentLiabilities)
            print()
            print('Other Non Current Liabilities: ' + str(tb.OtherNonCurrentLiabilities) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Total Non Current Liabilities
        try:
            TotalNonCurrentLiabilities = []
            for key,value in BalanceSheet.items():
                if key == 'LiabilitiesNoncurrent':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Liabilities Non current: ' + str(ARCHvalue))
                    TotalNonCurrentLiabilities.append(ARCHvalue)
                elif key == 'TotalNonCurrentLiabilities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Total Non Current Liabilities: ' + str(ARCHvalue))
                    TotalNonCurrentLiabilities.append(ARCHvalue)
                else:
                    pass
            a.NonCurrentLiabilities = -sum(TotalNonCurrentLiabilities)
            print()
            print('Total Non Current Liabilities: ' + str(a.NonCurrentLiabilities) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Total Liabilities
        try:
            TotalLiabilities = []
            for key,value in BalanceSheet.items():
                if key == 'Liabilities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Liabilities: ' + str(ARCHvalue))
                    TotalLiabilities.append(ARCHvalue)
                elif key == 'TotalLiabilities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Total Liabilities: ' + str(ARCHvalue))
                    TotalLiabilities.append(ARCHvalue)
                else:
                    pass
            a.Liabilities = -sum(TotalLiabilities)
            print()
            print('Total Liabilities: ' + str(tb.Liabilities) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        try:
            if a.NonCurrentLiabilities == 0:
                a.NonCurrentLiabilities = a.Liabilities - a.CurrentLiabilities
        except:
            pass
        ###############################################################################################################
        # EQUITY
        ###############################################################################################################
        print(137*'-')
        print('EQUITY')
        print(137*'-')
        StockholdersEquityDict = []   
        # Common Shares
        try:
            CommonShares = []
            for key,value in BalanceSheet.items():
                if key == 'CommonStocksIncludingAdditionalPaidInCapital':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Common Stocks Including Additional Paid In Capital: ' + str(ARCHvalue))
                    CommonShares.append(ARCHvalue)
                if key == 'CommonStockAndAdditionalPaidInCapitalParValueSharesAuthorizedAndSharesIssuedAndOutstandingRespectively':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Common Stock And Additional Paid In Capital Par Value Shares Authorized And Shares Issued And Outstanding Respectively: ' + str(ARCHvalue))
                    CommonShares.append(ARCHvalue)
                elif key == 'AdditionalPaidInCapital':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Additional Paid In Capital: ' + str(ARCHvalue))
                    CommonShares.append(ARCHvalue)
                else:
                    pass
            tb.CommonShares = -sum(CommonShares)
            BalanceSheetDict.append(tb.CommonShares)
            print()
            print('Common Shares: ' + str(tb.CommonShares) + ' $')
            print(15*"-")
        except:
            pass
        # Accumulated Other Comprehensive Income (Loss)
        try:
            AccumulatedOtherComprehensiveIncomeLoss = []
            for key,value in BalanceSheet.items():
                if key == 'AccumulatedOtherComprehensiveIncomeLossNetOfTax':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Accumulated Other Comprehensive Income Loss Net Of Tax: ' + str(ARCHvalue))
                    AccumulatedOtherComprehensiveIncomeLoss.append(ARCHvalue)
                elif key == 'AccumulatedOtherComprehensiveIncomeLoss':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Accumulated Other Comprehensive Income Loss: ' + str(ARCHvalue))
                    AccumulatedOtherComprehensiveIncomeLoss.append(ARCHvalue)
                else:
                    pass
            tb.AccumulatedOtherComprehensiveIncomeLoss = -sum(AccumulatedOtherComprehensiveIncomeLoss)
            BalanceSheetDict.append(tb.AccumulatedOtherComprehensiveIncomeLoss)
            print()
            print('Accumulated Other Comprehensive Income (Loss): ' + str(tb.AccumulatedOtherComprehensiveIncomeLoss) + ' $')
            print(15*"-")
        except:
            pass
        # Retained Earnings (Accumulated Deficit)
        try:
            RetainedEarningsAccumulatedDeficit = []
            for key,value in BalanceSheet.items():
                if key == 'RetainedEarningsAccumulatedDeficit':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Retained Earnings Accumulated Deficit: ' + str(ARCHvalue))
                    RetainedEarningsAccumulatedDeficit.append(ARCHvalue)
                if key == 'RetainedEarnings':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Retained Earnings: ' + str(ARCHvalue))
                    RetainedEarningsAccumulatedDeficit.append(ARCHvalue)
                else:
                    pass
            tb.RetainedEarningsAccumulatedDeficit = -sum(RetainedEarningsAccumulatedDeficit)
            BalanceSheetDict.append(tb.RetainedEarningsAccumulatedDeficit)
            print()
            print('Retained Earnings Accumulated Deficit: ' + str(tb.RetainedEarningsAccumulatedDeficit) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Stockholders Equity
        try:
            StockholdersEquityD = []
            for key,value in BalanceSheet.items():
                if key == 'StockholdersEquity':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Stockholders Equity: ' + str(ARCHvalue))
                    StockholdersEquityD.append(ARCHvalue)
                elif key == 'TotalShareholdersEquity':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Total Shareholders Equity: ' + str(ARCHvalue))
                    StockholdersEquityD.append(ARCHvalue)
                else:
                    pass
            a.StockholdersEquity = -sum(StockholdersEquityD)
            print()
            print('Stockholders Equity: ' + str(a.StockholdersEquity) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Total Stockholders Equity And Liabilities
        try:
            LiabilitiesAndStockholdersEquity = []
            for key,value in BalanceSheet.items():
                if key == 'LiabilitiesAndStockholdersEquity':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Liabilities And Stockholders Equity: ' + str(ARCHvalue))
                    LiabilitiesAndStockholdersEquity.append(ARCHvalue)
                elif key == 'TotalLiabilitiesAndShareholdersEquity':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        BalanceSheet[key] = None
                    print('Total Liabilities And Shareholders Equity: ' + str(ARCHvalue))
                    LiabilitiesAndStockholdersEquity.append(ARCHvalue)
                else:
                    pass
            a.LiabilitiesAndStockholdersEquity = sum(LiabilitiesAndStockholdersEquity)
            print()
            print('Total Liabilities And Stockholders Equity: ' + str(a.LiabilitiesAndStockholdersEquity) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # INCOME STATEMENTS
        print(137*'-')
        print('INCOME STATEMENTS')
        print(137*'-')
        ###############################################################################################################
        OperatingIncomeDict = []
        # Sales
        try:
            Sales = []
            for key,value in IncomeStatement.items():
                if key == 'RevenueFromContractWithCustomerExcludingAssessedTax':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Revenue From Contract With Customer Excluding Assessed Tax: ' + str(ARCHvalue))
                    Sales.append(ARCHvalue)
                elif key == 'NetSales':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Net Sales: ' + str(ARCHvalue))
                    Sales.append(ARCHvalue)
                else:
                    pass
            tb.Sales = -sum(Sales)
            OperatingIncomeDict.append(tb.Sales)
            print()
            print('Sales: ' + str(tb.Sales) + ' $')
            print(15*"-")
        except:
            pass
        # Cost Of Sales
        try:
            CostOfSales = []
            for key,value in IncomeStatement.items():
                if key == 'CostOfGoodsAndServicesSold':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Cost Of Goods And Services Sold: ' + str(ARCHvalue))
                    CostOfSales.append(ARCHvalue)
                elif key == 'CostOfSales':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Cost Of Sales: ' + str(ARCHvalue))
                    CostOfSales.append(ARCHvalue)
                elif key == 'CostOfRevenue':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Cost Of Revenue: ' + str(ARCHvalue))
                    CostOfSales.append(ARCHvalue)
                else:
                    pass
            tb.CostOfSales = sum(CostOfSales)
            OperatingIncomeDict.append(tb.CostOfSales)
            print()
            print('Cost Of Sales: ' + str(tb.CostOfSales) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        GrossMarginDict = [
            tb.Sales,
            tb.CostOfSales,
        ]
        # Gross Margin
        try:
            GrossMargin = []
            for key,value in IncomeStatement.items():
                if key == 'GrossProfit':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Gross Profit: ' + str(ARCHvalue))
                    GrossMargin.append(ARCHvalue)
                elif key == 'GrossMargin':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Gross Margin: ' + str(ARCHvalue))
                    GrossMargin.append(ARCHvalue)
                else:
                    pass
            a.GrossMargin = sum(GrossMargin)
            print()
            print('Gross Margin: ' + str(a.GrossMargin) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Anomaly Non Current Liabilities
        try:
            Anomaly = a.GrossMargin - sum(GrossMarginDict)
        except:
            pass
        ###############################################################################################################
        OperatingExpensesDict = []
        # Research And Development
        try:
            ResearchAndDevelopment = []
            for key,value in IncomeStatement.items():
                if key == 'ResearchAndDevelopmentExpense':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Research And Development Expense: ' + str(ARCHvalue))
                    ResearchAndDevelopment.append(ARCHvalue)
                elif key == 'ResearchAndDevelopment':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Research And Development: ' + str(ARCHvalue))
                    ResearchAndDevelopment.append(ARCHvalue)
                else:
                    pass
            tb.ResearchAndDevelopment = sum(ResearchAndDevelopment)
            OperatingExpensesDict.append(tb.ResearchAndDevelopment)
            print()
            print('Research And Development: ' + str(tb.ResearchAndDevelopment) + ' $')
            print(15*"-")
        except:
            pass
        # Selling General, Administrative And Marketing
        try:
            SellingGeneralAdministrativeAndMarketing = []
            for key,value in IncomeStatement.items():
                if key == 'SellingGeneralAndAdministrativeExpense':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Selling General And Administrative Expense: ' + str(ARCHvalue))
                    SellingGeneralAdministrativeAndMarketing.append(ARCHvalue)
                elif key == 'SellingGeneralAndAdministrative':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Selling General And Administrative: ' + str(ARCHvalue))
                    SellingGeneralAdministrativeAndMarketing.append(ARCHvalue)
                elif key == 'SellingAndMarketingExpense':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Selling And Marketing Expense: ' + str(ARCHvalue))
                    SellingGeneralAdministrativeAndMarketing.append(ARCHvalue)
                elif key == 'GeneralAndAdministrativeExpense':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('General And Administrative Expense: ' + str(ARCHvalue))
                    SellingGeneralAdministrativeAndMarketing.append(ARCHvalue)
                else:
                    pass
            tb.SellingGeneralAdministrativeAndMarketing = sum(SellingGeneralAdministrativeAndMarketing)
            OperatingExpensesDict.append(tb.SellingGeneralAdministrativeAndMarketing)
            print()
            print('Selling General Administrative And Marketing: ' + str(tb.SellingGeneralAdministrativeAndMarketing) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Total Operating Expenses
        try:
            OperatingExpenses = []
            for key,value in IncomeStatement.items():
                if key == 'OperatingExpenses':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Operating Expenses: ' + str(ARCHvalue))
                    OperatingExpenses.append(ARCHvalue)
                elif key == 'TotalOperatingExpenses':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Total Operating Expenses: ' + str(ARCHvalue))
                    OperatingExpenses.append(ARCHvalue)
                elif key == 'CostsAndExpenses':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Costs And Expenses: ' + str(ARCHvalue))
                    OperatingExpenses.append(ARCHvalue)
                else:
                    pass
            a.OperatingExpenses = -sum(OperatingExpenses)
            print()
            print('Operating Expenses: ' + str(a.OperatingExpenses) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Operating Income (Loss)
        try:
            a.OperatingIncome = (a.GrossMargin + a.OperatingExpenses)
            print('Operating Income: ' + str(a.OperatingIncome) + ' $')
        except:
            pass
        ###############################################################################################################
        try:
            IncomeBeforeTaxesDict = [
                a.OperatingIncome,
            ]
        except:
            pass
        # NonOperatingIncomeExpense
        try:
            NonOperatingIncomeExpense = []
            for key,value in IncomeStatement.items():
                if key == 'NonoperatingIncomeExpense':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Non operating Income Expense: ' + str(ARCHvalue))
                    NonOperatingIncomeExpense.append(ARCHvalue)
                elif key == 'OtherIncomeExpenseNet':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Other Income Expense Net: ' + str(ARCHvalue))
                    NonOperatingIncomeExpense.append(ARCHvalue)
                else:
                    pass
            tb.NonOperatingIncomeExpense = -sum(NonOperatingIncomeExpense)
            print()
            print('Non Operating Income (Expense): ' + str(tb.NonOperatingIncomeExpense) + ' $')
            print(15*"-")
        except:
            pass
        # Interest Expense ##################################################### Classification Anomaly #####################################################
        try:
            InterestExpense = []
            for key,value in IncomeStatement.items():
                if key == 'InterestExpense':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Interest Expense: ' + str(ARCHvalue))
                    InterestExpense.append(ARCHvalue)
                elif key == 'CashPaidForInterest':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Cash Paid For Interest: ' + str(ARCHvalue))
                    InterestExpense.append(ARCHvalue)
                else:
                    pass
            tb.InterestExpense = sum(InterestExpense)
            tb.NonOperatingIncomeExpense = tb.NonOperatingIncomeExpense - tb.InterestExpense
            IncomeBeforeTaxesDict.append(tb.InterestExpense)
            IncomeBeforeTaxesDict.append(tb.NonOperatingIncomeExpense)
            print()
            print('Interest Expense: ' + str(tb.InterestExpense) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Income Before Taxes
        try:
            IncomeBeforeTaxes = []
            for key,value in IncomeStatement.items():
                if key == 'IncomeLossFromContinuingOperationsBeforeIncomeTaxesExtraordinaryItemsNoncontrollingInterest':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Income Loss From Continuing Operations Before Income Taxes Extraordinary Items Non controlling Interest: ' + str(ARCHvalue))
                    IncomeBeforeTaxes.append(ARCHvalue)
                elif key == 'IncomeBeforeProvisionForIncomeTaxes':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Income Before Provision For Income Taxes: ' + str(ARCHvalue))
                    IncomeBeforeTaxes.append(ARCHvalue)
                else:
                    pass
            a.IncomeBeforeTaxes = sum(IncomeBeforeTaxes)
            print()
            print('Income Before Taxes: ' + str(a.IncomeBeforeTaxes) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        try:
            NetIncomeDict = [
                a.IncomeBeforeTaxes,
            ]
        except:
            pass
        # Income Tax Expense (Benefit)
        try:
            IncomeTaxExpenseBenefit = []
            for key,value in IncomeStatement.items():
                if key == 'IncomeTaxExpenseBenefit':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Income Tax Expense Benefit: ' + str(ARCHvalue))
                    IncomeTaxExpenseBenefit.append(ARCHvalue)
                elif key == 'ProvisionForIncomeTaxes':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Provision For Income Taxes: ' + str(ARCHvalue))
                    IncomeTaxExpenseBenefit.append(ARCHvalue)
                else:
                    pass
            tb.IncomeTaxExpenseBenefit = sum(IncomeTaxExpenseBenefit)
            NetIncomeDict.append(tb.IncomeTaxExpenseBenefit)
            print()
            print('IncomeTaxExpenseBenefit: ' + str(tb.IncomeTaxExpenseBenefit) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Net Income
        try:
            NetIncome = []
            for key,value in IncomeStatement.items():
                if key == 'NetIncomeLoss':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Net Income Loss: ' + str(ARCHvalue))
                    NetIncome.append(ARCHvalue)
                elif key == 'NetIncome':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        IncomeStatement[key] = None
                    print('Net Income: ' + str(ARCHvalue))
                    NetIncome.append(ARCHvalue)
                else:
                    pass
            a.NetIncome = sum(NetIncome)
            print()
            print('Net Income: ' + str(a.NetIncome) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # COMPREHENSIVE INCOME
        print(137*'-')
        print('COMPREHENSIVE INCOME')
        print(137*'-')
        ###############################################################################################################
        try:
            ComprehensiveIncomeDict = [
                a.NetIncome,
            ]
        except:
            pass
        # Change In Foreign Currency Translation Adjustment Net Of Taxes
        try:
            ChangeInForeignCurrencyTranslationAdjustmentNetOfTaxes = []
            for key,value in ComprehensiveIncome.items():
                if key == 'ForeignCurrencyTransactionAndTranslationAdjustmentNetOfTax':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Foreign Currency Transaction And Translation Adjustment Net Of Tax: ' + str(ARCHvalue))
                    ChangeInForeignCurrencyTranslationAdjustmentNetOfTaxes.append(ARCHvalue)
                elif key == 'ChangeInForeignCurrencyTranslationNetOfTax':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Change In Foreign Currency Translation, Net Of Tax: ' + str(ARCHvalue))
                    ChangeInForeignCurrencyTranslationAdjustmentNetOfTaxes.append(ARCHvalue)
                elif key == 'ChangeInForeignCurrencyTranslationNetOfTaxEffectsOfAndRespectively':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Loss Change In Foreign Currency Translation Net Of Tax Effects Of And Respectively: ' + str(ARCHvalue))
                    ChangeInForeignCurrencyTranslationAdjustmentNetOfTaxes.append(ARCHvalue)
                else:
                    pass
            tb.ChangeInForeignCurrencyTranslationAdjustmentNetOfTaxes = -sum(ChangeInForeignCurrencyTranslationAdjustmentNetOfTaxes)
            ComprehensiveIncomeDict.append(tb.ChangeInForeignCurrencyTranslationAdjustmentNetOfTaxes)
            print()
            print('Change In Foreign Currency Translation Adjustment Net Of Taxes: ' + str(tb.ChangeInForeignCurrencyTranslationAdjustmentNetOfTaxes) + ' $')
            print(15*"-")
        except:
            pass
        # Change In Unrealized Gains (Losses) On Derivative Instruments Net Of Taxes
        try:
            ChangeInUnrealizedGainsLossesOnDerivativeInstrumentsNetOfTaxes = []
            for key,value in ComprehensiveIncome.items():
                if key == 'DerivativeInstrumentGainLossbeforeReclassificationafterTax':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Derivative Instrument Gain Loss before Reclassification after Tax: ' + str(ARCHvalue))
                    ChangeInUnrealizedGainsLossesOnDerivativeInstrumentsNetOfTaxes.append(ARCHvalue)
                elif key == 'UnrealizedGainLossOnDerivativesArisingDuringPeriodNetOfTax':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Unrealized Gain Loss On Derivatives Arising During Period Net Of Tax: ' + str(ARCHvalue))
                    ChangeInUnrealizedGainsLossesOnDerivativeInstrumentsNetOfTaxes.append(ARCHvalue)
                elif key == 'CashFlowHedgeGainLossReclassificationAfterTax':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Cash Flow Hedge Gain Loss Reclassification After Tax: ' + str(ARCHvalue))
                    ChangeInUnrealizedGainsLossesOnDerivativeInstrumentsNetOfTaxes.append(-value)
                elif key == 'ReclassificationAdjustmentFromAOCIOnDerivativesNetOfTax':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Reclassification Adjustment From AOCI On Derivatives Net Of Tax: ' + str(ARCHvalue))
                    ChangeInUnrealizedGainsLossesOnDerivativeInstrumentsNetOfTaxes.append(-value)
                elif key == 'ChangeInFairValueOfDerivativesNetOfTaxBenefitExpenseOfAndRespectively':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Change In Fair Value Of Derivatives Net Of Tax Benefit Expense Of And Respectively: ' + str(ARCHvalue))
                    ChangeInUnrealizedGainsLossesOnDerivativeInstrumentsNetOfTaxes.append(ARCHvalue)
                elif key == 'AdjustmentForNetGainsLossesRealizedAndIncludedInNetIncomeNetOfTaxExpenseBenefitOfAndRespectively':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Adjustment For Net Gains Losses Realized And Included In Net Income Net Of Tax Expense Benefit Of And Respectively: ' + str(ARCHvalue))
                    ChangeInUnrealizedGainsLossesOnDerivativeInstrumentsNetOfTaxes.append(ARCHvalue)
                elif key == 'ChangeInFairValueOfDerivatives':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Change In Fair Value Of Derivatives: ' + str(ARCHvalue))
                    ChangeInUnrealizedGainsLossesOnDerivativeInstrumentsNetOfTaxes.append(ARCHvalue)
                elif key == 'AdjustmentForNetGainsLossesRealizedAndIncludedInNetIncome':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Adjustment For Net Gains (Losses) Realized And Included In Net Income: ' + str(ARCHvalue))
                    ChangeInUnrealizedGainsLossesOnDerivativeInstrumentsNetOfTaxes.append(ARCHvalue)
                elif key == 'ChangeInFairValueOfDerivativesNetOfTaxBenefitExpenseOfAndRespectively':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Change In Fair Value Of Derivatives Net Of Tax Benefit Expense Of And Respectively: ' + str(ARCHvalue))
                    ChangeInUnrealizedGainsLossesOnDerivativeInstrumentsNetOfTaxes.append(ARCHvalue)
                elif key == 'AdjustmentForNetGainsLossesRealizedAndIncludedInNetIncomeNetOfTaxExpenseBenefitOfAndRespectively':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Adjustment For Net Gains Losses Realized And Included In Net Income, Net Of Tax Expense Benefit Of And Respectively: ' + str(ARCHvalue))
                    ChangeInUnrealizedGainsLossesOnDerivativeInstrumentsNetOfTaxes.append(ARCHvalue)
                else:
                    pass
            tb.ChangeInUnrealizedGainsLossesOnDerivativeInstrumentsNetOfTaxes = -sum(ChangeInUnrealizedGainsLossesOnDerivativeInstrumentsNetOfTaxes)
            ComprehensiveIncomeDict.append(tb.ChangeInUnrealizedGainsLossesOnDerivativeInstrumentsNetOfTaxes)
            print()
            print('Change In Unrealized Gains (Losses) On Derivative Instruments, Net Of Taxes: ' + str(tb.ChangeInUnrealizedGainsLossesOnDerivativeInstrumentsNetOfTaxes) + ' $')
            print(15*"-")
        except:
            pass
        # Change In Unrealized Gains (Losses) On Investment, Net Of Taxes
        try:
            ChangeInUnrealizedGainsLossesOnInvestmentsNetOfTaxes = []
            for key,value in ComprehensiveIncome.items():
                if key == 'UnrealizedHoldingGainLossOnSecuritiesArisingDuringPeriodNetOfTax':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Unrealized Holding Gain Loss On Securities Arising During Period Net Of Tax: ' + str(ARCHvalue))
                    ChangeInUnrealizedGainsLossesOnInvestmentsNetOfTaxes.append(ARCHvalue)
                elif key == 'LossReclassificationAdjustmentFromAOCIForSaleOfSecuritiesNetOfTax':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Reclassification Adjustment From AOCI For Sale Of Securities Net Of Tax: ' + str(ARCHvalue))
                    ChangeInUnrealizedGainsLossesOnInvestmentsNetOfTaxes.append(ARCHvalue)
                elif key == 'ChangeInFairValueOfMarketableSecuritiesNetOfTaxBenefitExpenseOfAndRespectively':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Change In Fair Value Of Marketable Securities NetOfTaxBenefitExpenseOfAndRespectively: ' + str(ARCHvalue))
                    ChangeInUnrealizedGainsLossesOnInvestmentsNetOfTaxes.append(ARCHvalue)
                elif key == 'AdjustmentForNetGainsLossesRealizedAndIncludedInNetIncomeNetOfTaxExpenseBenefitOfAndRespectively':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Adjustment For Net Gains Losses Realized And Included In Net Income Net Of Tax Expense Benefit Of And Respectively: ' + str(ARCHvalue))
                    ChangeInUnrealizedGainsLossesOnInvestmentsNetOfTaxes.append(ARCHvalue)
                elif key == 'AvailableForSaleSecuritiesAdjustmentAndOtherNetofTax':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Available For Sale Securities Adjustment And Other Net of Tax: ' + str(ARCHvalue))
                    ChangeInUnrealizedGainsLossesOnInvestmentsNetOfTaxes.append(ARCHvalue)
                elif key == 'ChangeInFairValueOfMarketableDebtSecurities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Change In Fair Value Of Marketable Debt Securities: ' + str(ARCHvalue))
                    ChangeInUnrealizedGainsLossesOnInvestmentsNetOfTaxes.append(ARCHvalue)
                elif key == 'AdjustmentForNetGainsLossesRealizedAndIncludedInNetIncome':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Adjustment For Net Gains Losses Realized And Included In Net Income: ' + str(ARCHvalue))
                    ChangeInUnrealizedGainsLossesOnInvestmentsNetOfTaxes.append(ARCHvalue)
                elif key == 'ChangeInFairValueOfMarketableSecurities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Change In Fair Value Of Marketable Securities: ' + str(ARCHvalue))
                    ChangeInUnrealizedGainsLossesOnInvestmentsNetOfTaxes.append(ARCHvalue)
                else:
                    pass 
            tb.ChangeInUnrealizedGainsLossesOnInvestmentsNetOfTaxes = -sum(ChangeInUnrealizedGainsLossesOnInvestmentsNetOfTaxes)
            ComprehensiveIncomeDict.append(tb.ChangeInUnrealizedGainsLossesOnInvestmentsNetOfTaxes)
            print()
            print('Change In Unrealized Gains (Losses) On Investment, Net Of Taxes: ' + str(tb.ChangeInUnrealizedGainsLossesOnInvestmentsNetOfTaxes) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Comprehensive Income
        try:
            ComprehensiveIncomeD = []
            for key,value in ComprehensiveIncome.items():
                if key == 'ComprehensiveIncomeNetOfTax':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Comprehensive Income Net Of Tax: ' + str(ARCHvalue))
                    ComprehensiveIncomeD.append(ARCHvalue)
                elif key == 'ChangeInUnrealizedGainsLossesOnMarketableSecuritiesTotalComprehensiveIncome':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        ComprehensiveIncome[key] = None
                    print('Change In Unrealized Gains Losses On Marketable Securities Total Comprehensive Income: ' + str(ARCHvalue))
                    ComprehensiveIncomeD.append(ARCHvalue)
                else:
                    pass
            a.ComprehensiveIncome = sum(ComprehensiveIncomeDict)
            print()
            print('Comprehensive Income: ' + str(a.ComprehensiveIncome) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Anomaly Non Current Liabilities
        try:
            Anomaly = a.ComprehensiveIncome - sum(ComprehensiveIncomeDict)
        except:
            pass
        ###############################################################################################################
        # STOCKHOLDERS EQUITY
        print(137*'-')
        print("STOCKHOLDERS' EQUITY")
        print(137*'-')
        ###############################################################################################################
        StockholdersEquityDict = []
        # Common Stock Issued
        try:
            CommonStockIssued = []
            for key,value in StockholdersEquity.items():
                if key == 'StockIssuedDuringPeriodValueNewIssues':
                    try:
                        i = len(value) - 1
                        while value[i] == None:
                            i = i - 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        StockholdersEquity[key] = None
                    print('Stock Issued During Period Value New Issues: ' + str(ARCHvalue))
                    CommonStockIssued.append(ARCHvalue)
                elif key == 'CommonStockIssuedNetOfSharesWithheldForEmployeeTaxes':
                    try:
                        i = len(value) - 1
                        while value[i] == None:
                            i = i - 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        StockholdersEquity[key] = None
                    print('Common Stock Issued Net Of Shares Withheld For Employee Taxes: ' + str(ARCHvalue))
                    CommonStockIssued.append(ARCHvalue)
                elif key == 'StockIssuedDuringPeriodValueStockOptionsExercised':
                    try:
                        i = len(value) - 1
                        while value[i] == None:
                            i = i - 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        StockholdersEquity[key] = None
                    print('Stock Issued During Period Value Stock Options Exercised: ' + str(ARCHvalue))
                    CommonStockIssued.append(ARCHvalue)
                elif key == 'CommonStockIssued':
                    try:
                        i = len(value) - 1
                        while value[i] == None:
                            i = i - 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        StockholdersEquity[key] = None
                    print('Common Stock Issued: ' + str(ARCHvalue))
                    CommonStockIssued.append(ARCHvalue)
                else:
                    pass
            tb.CommonStockIssued = -sum(CommonStockIssued)
            StockholdersEquityDict.append(tb.CommonStockIssued)
            print()
            print('Common Stock Issued: ' + str(tb.CommonStockIssued) + ' $')
            print(15*"-")
        except:
            pass
        # Share Based Compensation and Other Stockholders Equity Components
        try:
            ShareBasedCompensation = []
            for key,value in StockholdersEquity.items():
                if key == 'AdjustmentsRelatedToTaxWithholdingForShareBasedCompensation':
                    try:
                        i = len(value) - 1
                        while value[i] == None:
                            i = i - 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        StockholdersEquity[key] = None
                    print('Adjustments Related To Tax Withholding For Share Based Compensation: ' + str(ARCHvalue))
                    ShareBasedCompensation.append(ARCHvalue)
                elif key == 'AdjustmentsToAdditionalPaidInCapitalSharebasedCompensationRequisiteServicePeriodRecognitionValue':
                    try:
                        i = len(value) - 1
                        while value[i] == None:
                            i = i - 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        StockholdersEquity[key] = None
                    print('Adjustments To Additional Paid In Capital Share based Compensation Requisite Service Period Recognition Value: ' + str(ARCHvalue))
                    ShareBasedCompensation.append(ARCHvalue)
                elif key == 'IncreaseDecreaseInStockholdersEquityRollForwardShareBasedCompensation':
                    try:
                        i = len(value) - 1
                        while value[i] == None:
                            i = i - 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        StockholdersEquity[key] = None
                    print('Increase Decrease In Stockholders Equity RollForward Share Based Compensation: ' + str(ARCHvalue))
                    ShareBasedCompensation.append(ARCHvalue)
                elif key == 'IncreaseDecreaseInStockholdersEquityRollForwardCommonStockIssuedNetOfSharesWithheldForEmployeeTaxes':
                    try:
                        i = len(value) - 1
                        while value[i] == None:
                            i = i - 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        StockholdersEquity[key] = None
                    print('Increase Decrease In Stockholders Equity RollForward Common Stock Issued Net Of Shares Withheld For Employee Taxes: ' + str(ARCHvalue))
                    ShareBasedCompensation.append(ARCHvalue)
                elif key == 'ShareholdersEquityShareBasedCompensation':
                    try:
                        i = len(value) - 1
                        while value[i] == None:
                            i = i - 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        StockholdersEquity[key] = None
                    print('Shareholders Equity Share Based Compensation: ' + str(ARCHvalue))
                    ShareBasedCompensation.append(ARCHvalue)
                elif key == 'StockIssuedDuringPeriodValueRestrictedStockUnitBeforeTaxSettlement':
                    try:
                        i = len(value) - 1
                        while value[i] == None:
                            i = i - 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        StockholdersEquity[key] = None
                    print('Stock Issued During Period Value Restricted Stock Unit Before Tax Settlement: ' + str(ARCHvalue))
                    ShareBasedCompensation.append(ARCHvalue)
                elif key == 'ShareBasedCompensation':
                    try:
                        i = len(value) - 1
                        while value[i] == None:
                            i = i - 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        StockholdersEquity[key] = None
                    print('Share Based Compensation: ' + str(ARCHvalue))
                    ShareBasedCompensation.append(ARCHvalue)
                elif key == 'CommonStockWithheldRelatedToNetShareSettlementOfEquityAwards':
                    try:
                        i = len(value) - 1
                        while value[i] == None:
                            i = i - 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        StockholdersEquity[key] = None
                    print('Common Stock Withheld Related To Net Share Settlement Of Equity Awards: ' + str(ARCHvalue))
                    ShareBasedCompensation.append(ARCHvalue)
                else:
                    pass
            tb.ShareBasedCompensation = -sum(ShareBasedCompensation)
            StockholdersEquityDict.append(tb.ShareBasedCompensation)
            print()
            print('Share Based Compensation: ' + str(tb.ShareBasedCompensation) + ' $')
            print(15*"-")
        except:
            pass
        # Dividends And Dividend Equivalents Declared
        try:
            DividendsAndDividendEquivalentsDeclared = []
            for key,value in StockholdersEquity.items():
                if key == 'Dividends':
                    try:
                        i = len(value) - 1
                        while value[i] == None:
                            i = i - 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        StockholdersEquity[key] = None
                    print('Dividends: ' + str(ARCHvalue))
                    DividendsAndDividendEquivalentsDeclared.append(ARCHvalue)
                elif key == 'DividendsAndDividendEquivalentsDeclared':
                    try:
                        i = len(value) - 1
                        print(value[i])
                        while value[i] == None:
                            i = i - 1
                        print(137*'-')
                        print(value[i])
                        print(137*'-')
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        StockholdersEquity[key] = None
                    print('Dividends And Dividend Equivalents Declared: ' + str(ARCHvalue))
                    DividendsAndDividendEquivalentsDeclared.append(ARCHvalue)
                else:
                    pass
            tb.DividendsAndDividendEquivalentsDeclared = -sum(DividendsAndDividendEquivalentsDeclared)
            StockholdersEquityDict.append(tb.DividendsAndDividendEquivalentsDeclared)
            print()
            print('Dividends And Dividend Equivalents Declared: ' + str(tb.DividendsAndDividendEquivalentsDeclared) + ' $')
            print(15*"-")
        except:
            pass
        # Common Stock Repurchased And Retired
        try:
            CommonStockRepurchasedAndRetired = []
            for key,value in StockholdersEquity.items():
                if key == 'StockRepurchasedAndRetiredDuringPeriodValue':
                    try:
                        i = len(value) - 1
                        while value[i] == None:
                            i = i - 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        StockholdersEquity[key] = None
                    print('Stock Repurchased And Retired During Period Value: ' + str(ARCHvalue))
                    CommonStockRepurchasedAndRetired.append(ARCHvalue)
                elif key == 'RepurchasesOfCommonStock':
                    try:
                        i = len(value) - 1
                        while value[i] == None:
                            i = i - 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        StockholdersEquity[key] = None
                    print('Repurchases Of Common Stock: ' + str(ARCHvalue))
                    CommonStockRepurchasedAndRetired.append(ARCHvalue)
                elif key == 'RepurchaseOfCommonStock':
                    try:
                        i = len(value) - 1
                        while value[i] == None:
                            i = i - 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        StockholdersEquity[key] = None
                    print('Repurchase Of Common Stock: ' + str(ARCHvalue))
                    CommonStockRepurchasedAndRetired.append(ARCHvalue)
                elif key == 'StockRepurchasedDuringPeriodValue':
                    try:
                        i = len(value) - 1
                        while value[i] == None:
                            i = i - 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        StockholdersEquity[key] = None
                    print('Stock Repurchased During Period Value: ' + str(ARCHvalue))
                    CommonStockRepurchasedAndRetired.append(ARCHvalue)
                elif key == 'CommonStockRepurchased':
                    try:
                        i = len(value) - 1
                        while value[i] == None:
                            i = i - 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        StockholdersEquity[key] = None
                    print('Common Stock Repurchased: ' + str(ARCHvalue))
                    CommonStockRepurchasedAndRetired.append(ARCHvalue)
                else:
                    pass
            tb.CommonStockRepurchasedAndRetired = -sum(CommonStockRepurchasedAndRetired)
            StockholdersEquityDict.append(tb.CommonStockRepurchasedAndRetired)
            print()
            print('Common Stock Repurchased And Retired: ' + str(tb.CommonStockRepurchasedAndRetired) + ' $')
            print(15*"-")
        except:
            pass
        # Effect Of Adoption Of New Accounting Pronouncement Or Tax Cuts
        try:
            EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts = []
            for key,value in StockholdersEquity.items():
                if key == 'CumulativeEffectOfChangeInAccountingPrinciple':
                    try:
                        i = len(value) - 1
                        while value[i] == None:
                            i = i - 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        StockholdersEquity[key] = None
                    print('Cumulative Effect Of Change In Accounting Principle: ' + str(ARCHvalue))
                    EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts.append(ARCHvalue)
                else:
                    pass
            tb.EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts = sum(EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts)
            StockholdersEquityDict.append(tb.EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts)
            print()
            print('Effect Of Adoption Of New Accounting Pronouncement Or Tax Cuts: ' + str(tb.EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts) + ' $')
            print(15*"-")
        except:
            pass
        # Other Comprehensive Income (Loss)
        try:
            a.StockholdersEquityOtherComprehensiveIncome = (a.ComprehensiveIncome - a.NetIncome)
            StockholdersEquityDict.append(a.StockholdersEquityOtherComprehensiveIncome)
            print()
            print('Other Comprehensive Income (Loss): ' + str(a.StockholdersEquityOtherComprehensiveIncome) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Anomaly Stockholders Equity
        try:
            Anomaly = tb.OtherAdjustmentToStockholdersEquity - sum(StockholdersEquityDict)
            tb.OtherAdjustmentToStockholdersEquity = Anomaly
        except:
            pass
        ###############################################################################################################
        # CASH FLOW
        print(137*'-')
        print('CASH FLOW')
        print(137*'-')
        ###############################################################################################################
        # OPERATING ACTIVITIES        
        ###############################################################################################################
        print(137*'-')
        print('OPERATING ACTIVITIES')
        print(137*'-')
        # Cash Ending Balance
        try:
            CashBeginningBalance = []
            for key,value in CashFlowStatement.items():
                if key == 'CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Cash Cash Equivalents Restricted Cash And Restricted Cash Equivalents: ' + str(ARCHvalue))
                    CashBeginningBalance.append(ARCHvalue)
                elif key == 'CashAndCashEquivalentsBeginningOfTheYear':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Cash And Cash Equivalents Beginning Of The Year: ' + str(ARCHvalue))
                    CashBeginningBalance.append(ARCHvalue)
                elif key == 'CashAndCashEquivalentsBeginningOfTheYear':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Cash And Cash Equivalents Beginning Of The Year: ' + str(ARCHvalue))
                    CashBeginningBalance.append(ARCHvalue)
                elif key == 'CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Cash Cash Equivalents Restricted Cash And Restricted Cash Equivalents: ' + str(ARCHvalue))
                    CashBeginningBalance.append(ARCHvalue)
                else:
                    pass
            cf.CashBeginningBalance = sum(CashBeginningBalance)
            print()
            print('Cash Ending Balance: ' + str(cf.CashBeginningBalance) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Anomaly
        ###############################################################################################################
        OperatingActivitiesDict = [
            a.NetIncome,
        ]
        # Depreciation Depletion And Amortization
        try:
            DepreciationDepletionAndAmortization = []
            for key,value in CashFlowStatement.items():
                if key == 'DepreciationDepletionAndAmortization':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Depreciation Depletion And Amortization: ' + str(ARCHvalue))
                    DepreciationDepletionAndAmortization.append(ARCHvalue)
                elif key == 'DepreciationAndAmortization':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Depreciation And Amortization: ' + str(ARCHvalue))
                    DepreciationDepletionAndAmortization.append(ARCHvalue)
                else:
                    pass
            cf.DepreciationDepletionAndAmortization = sum(DepreciationDepletionAndAmortization)
            OperatingActivitiesDict.append(cf.DepreciationDepletionAndAmortization)
            print()
            print('Depreciation Depletion And Amortization: ' + str(cf.DepreciationDepletionAndAmortization) + ' $')
            print(15*"-")
        except:
            pass
        # Share Based Compensation
        try:
            ShareBasedCompensation = []
            for key,value in CashFlowStatement.items():
                if key == 'ShareBasedCompensation':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Share Based Compensation: ' + str(ARCHvalue))
                    ShareBasedCompensation.append(ARCHvalue)
                if key == 'ShareBasedCompensationExpense':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Share Based Compensation Expense: ' + str(ARCHvalue))
                    ShareBasedCompensation.append(ARCHvalue)
                else:
                    pass
            cf.ShareBasedCompensation = sum(ShareBasedCompensation)
            OperatingActivitiesDict.append(cf.ShareBasedCompensation)
            print()
            print('Share Based Compensation Operating Activities: ' + str(cf.ShareBasedCompensationOperatingActivities) + ' $')
            print(15*"-")
        except:
            pass
        # Deferred Income Tax Expense (Benefit)
        try:
            DeferredIncomeTaxExpenseBenefit = []
            for key,value in CashFlowStatement.items():
                if key == 'DeferredIncomeTaxExpenseBenefit':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Deferred Income Tax Expense Benefit: ' + str(ARCHvalue))
                    DeferredIncomeTaxExpenseBenefit.append(ARCHvalue)
                    DeferredIncomeTaxExpenseBenefit.append(ARCHvalue)
                if key == 'DeferredIncomeTaxExpense':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Deferred Income Tax Expense: ' + str(ARCHvalue))
                    DeferredIncomeTaxExpenseBenefit.append(ARCHvalue)
                if key == 'DeferredIncomeTaxBenefit':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Deferred Income Tax Benefit: ' + str(ARCHvalue))
                    DeferredIncomeTaxExpenseBenefit.append(ARCHvalue)
                else:
                    pass
            cf.DeferredIncomeTaxExpenseBenefit = sum(DeferredIncomeTaxExpenseBenefit)
            OperatingActivitiesDict.append(cf.DeferredIncomeTaxExpenseBenefit)
            print()
            print('Deferred Income Tax Expense (Benefit): ' + str(cf.DeferredIncomeTaxExpenseBenefit) + ' $')
            print(15*"-")
        except:
            pass
        # Other Non Cash Income Expense
        try:
            OtherNonCashIncomeExpense = []
            for key,value in CashFlowStatement.items():
                if key == 'OtherNoncashIncomeExpense':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Other Non cash Income Expense: ' + str(ARCHvalue))
                    OtherNonCashIncomeExpense.append(ARCHvalue)
                else:
                    pass
            cf.OtherNonCashIncomeExpense = -sum(OtherNonCashIncomeExpense)
            OperatingActivitiesDict.append(cf.OtherNonCashIncomeExpense)
            print()
            print('Other Non Cash Income Expense: ' + str(cf.OtherNonCashIncomeExpense) + ' $')
            print(15*"-")
        except:
            pass
        # Increase (Decrease) In Accounts Receivable
        try:
            IncreaseDecreaseInAccountsReceivable = []
            for key,value in CashFlowStatement.items():
                if key == 'IncreaseDecreaseInAccountsReceivable':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Increase Decrease In Accounts Receivable: ' + str(ARCHvalue))
                    IncreaseDecreaseInAccountsReceivable.append(ARCHvalue)
                if key == 'AccountsReceivableNet':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Changes In Operating Assets And Liabilities Accounts ReceivableNet: ' + str(ARCHvalue))
                    IncreaseDecreaseInAccountsReceivable.append(ARCHvalue)
                else:
                    pass
            cf.IncreaseDecreaseInAccountsReceivable = sum(IncreaseDecreaseInAccountsReceivable)
            OperatingActivitiesDict.append(cf.IncreaseDecreaseInAccountsReceivable)
            print()
            print('Increase (Decrease) In Accounts Receivable: ' + str(cf.IncreaseDecreaseInAccountsReceivable) + ' $')
            print(15*"-")
        except:
            pass
        # Increase (Decrease) In Inventories
        try:
            IncreaseDecreaseInInventories = []
            for key,value in CashFlowStatement.items():
                if key == 'IncreaseDecreaseInInventories':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Increase Decrease In Inventories: ' + str(ARCHvalue))
                    IncreaseDecreaseInInventories.append(ARCHvalue)
                if key == 'Inventories':
                    ARCHvalue = -value
                    print('Changes In Operating Assets And Liabilities Inventories: ' + str(ARCHvalue))
                    IncreaseDecreaseInInventories.append(ARCHvalue)
                else:
                    pass
            cf.IncreaseDecreaseInInventories = -sum(IncreaseDecreaseInInventories)
            OperatingActivitiesDict.append(cf.IncreaseDecreaseInInventories)
            print()
            print('Increase (Decrease) In Inventories: ' + str(cf.IncreaseDecreaseInInventories) + ' $')
            print(15*"-")
        except:
            pass
        # Increase (Decrease) In Other Receivables And Prepaid Expenses
        try:
            IncreaseDecreaseInOtherReceivables = []
            for key,value in CashFlowStatement.items():
                if key == 'IncreaseDecreaseInOtherReceivables':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Increase Decrease In Other Receivables: ' + str(ARCHvalue))
                    IncreaseDecreaseInOtherReceivables.append(ARCHvalue)
                if key == 'VendorNonTradeReceivables':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Vendor Non Trade Receivables: ' + str(ARCHvalue))
                    IncreaseDecreaseInOtherReceivables.append(ARCHvalue)
                if key == 'IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Increase Decrease In Prepaid Deferred Expense And Other Assets: ' + str(ARCHvalue))
                    IncreaseDecreaseInOtherReceivables.append(ARCHvalue)
                if key == 'IncreaseDecreaseInOtherAccountsPayable':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Increase Decrease In Other Accounts Payable: ' + str(ARCHvalue))
                    IncreaseDecreaseInOtherReceivables.append(ARCHvalue)
                else:
                    pass
            cf.IncreaseDecreaseInOtherReceivables = sum(IncreaseDecreaseInOtherReceivables)
            OperatingActivitiesDict.append(cf.IncreaseDecreaseInOtherReceivables)
            print()
            print('Increase (Decrease) In Other Receivables: ' + str(cf.IncreaseDecreaseInOtherReceivables) + ' $')
            print(15*"-")
        except:
            pass
        # Increase (Decrease) In Accounts Payable and Accrued Liabilities
        try:
            IncreaseDecreaseInAccountsPayableAndAccruedLiabilities = []
            for key,value in CashFlowStatement.items():
                if key == 'IncreaseDecreaseInAccountsPayable':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Increase Decrease In Accounts Payable: ' + str(ARCHvalue))
                    IncreaseDecreaseInAccountsPayableAndAccruedLiabilities.append(ARCHvalue)
                if key == 'AccountsPayable':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Accounts Payable: ' + str(ARCHvalue))
                    IncreaseDecreaseInAccountsPayableAndAccruedLiabilities.append(ARCHvalue)
                if key == 'IncreaseDecreaseInAccountsPayableTrade':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Increase Decrease In Accounts Payable Trade: ' + str(ARCHvalue))
                    IncreaseDecreaseInAccountsPayableAndAccruedLiabilities.append(ARCHvalue)
                if key == 'IncreaseDecreaseInAccruedLiabilities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Increase Decrease In Accrued Liabilities: ' + str(ARCHvalue))
                    IncreaseDecreaseInAccountsPayableAndAccruedLiabilities.append(ARCHvalue)
                else:
                    pass
            cf.IncreaseDecreaseInAccountsPayableAndAccruedLiabilities = sum(IncreaseDecreaseInAccountsPayableAndAccruedLiabilities)
            OperatingActivitiesDict.append(cf.IncreaseDecreaseInAccountsPayableAndAccruedLiabilities)
            print()
            print('Increase (Decrease) In Accounts Payable: ' + str(cf.IncreaseDecreaseInAccountsPayableAndAccruedLiabilities) + ' $')
            print(15*"-")
        except:
            pass
        # Increase (Decrease) In Contract With Customer Liability
        try:
            IncreaseDecreaseInContractWithCustomerLiability = []
            for key,value in CashFlowStatement.items():
                if key == 'IncreaseDecreaseInContractWithCustomerLiability':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Increase Decrease In Contract With Customer Liability: ' + str(ARCHvalue))
                    IncreaseDecreaseInContractWithCustomerLiability.append(ARCHvalue)
                if key == 'DeferredRevenue':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Deferred Revenue: ' + str(ARCHvalue))
                    IncreaseDecreaseInContractWithCustomerLiability.append(ARCHvalue)
                else:
                    pass
            cf.IncreaseDecreaseInContractWithCustomerLiability = sum(IncreaseDecreaseInContractWithCustomerLiability)
            OperatingActivitiesDict.append(cf.IncreaseDecreaseInContractWithCustomerLiability)
            print()
            print('Increase (Decrease) In Contract With Customer Liability: ' + str(cf.IncreaseDecreaseInContractWithCustomerLiability) + ' $')
            print(15*"-")
        except:
            pass
        # Increase (Decrease) In Other Operating Activities
        try:
            IncreaseDecreaseInOtherOperatingActivities = []
            for key,value in CashFlowStatement.items():
                if key == 'IncreaseDecreaseInOtherOperatingAssets':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Increase Decrease In Other Operating Assets: ' + str(ARCHvalue))
                    IncreaseDecreaseInOtherOperatingActivities.append(ARCHvalue)
                if key == 'OtherCurrentAndNonCurrentAssets':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Other Current And Non Current Assets: ' + str(ARCHvalue))
                    IncreaseDecreaseInOtherOperatingActivities.append(ARCHvalue)
                if key == 'IncreaseDecreaseInOtherOperatingLiabilities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Increase Decrease In Other Operating Liabilities: ' + str(ARCHvalue))
                    IncreaseDecreaseInOtherOperatingActivities.append(ARCHvalue)
                if key == 'OtherCurrentAndNonCurrentLiabilities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Other Current And Non Current Liabilities: ' + str(ARCHvalue))
                    IncreaseDecreaseInOtherOperatingActivities.append(ARCHvalue)
                if key == 'IncreaseDecreaseInOtherNoncurrentLiabilities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Increase Decrease In Other Non current Liabilities: ' + str(ARCHvalue))
                    IncreaseDecreaseInOtherOperatingActivities.append(ARCHvalue)
                if key == 'OtherCurrentAndNonCurrentAssets':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Other Current And Non Current Assets: ' + str(ARCHvalue))
                    IncreaseDecreaseInOtherOperatingActivities.append(ARCHvalue)
                if key == 'OtherCurrentAndNonCurrentLiabilities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Other Current And Non Current Liabilities: ' + str(ARCHvalue))
                    IncreaseDecreaseInOtherOperatingActivities.append(ARCHvalue)
                else:
                    pass
            cf.IncreaseDecreaseInOtherOperatingActivities = sum(IncreaseDecreaseInOtherOperatingActivities)
            OperatingActivitiesDict.append(cf.IncreaseDecreaseInOtherOperatingActivities)
            print()
            print('Increase (Decrease) In Other Operating Activities: ' + str(cf.IncreaseDecreaseInOtherOperatingActivities) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Total Operating Activities
        try:
            OperatingActivities = []
            for key,value in CashFlowStatement.items():
                if key == 'NetCashProvidedByUsedInOperatingActivities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Net Cash Provided By Used In Operating Activities: ' + str(ARCHvalue))
                    OperatingActivities.append(ARCHvalue)
                if key == 'CashGeneratedByOperatingActivities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Cash Generated By Operating Activities: ' + str(ARCHvalue))
                    OperatingActivities.append(ARCHvalue)
                else:
                    pass
            a.OperatingActivities = sum(OperatingActivities)
            print()
            print('Operating Activities: ' + str(a.OperatingActivities) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Anomaly Operating Activities
        try:
            Anomaly = a.OperatingActivities - sum(OperatingActivitiesDict)
            cf.IncreaseDecreaseInOtherOperatingActivities = cf.IncreaseDecreaseInOtherOperatingActivities + Anomaly
        except:
            pass
        ###############################################################################################################
        # INVESTING ACTIVITIES 
        ###############################################################################################################
        print(137*'-')
        print('INVESTING ACTIVITIES')
        print(137*'-')
        InvestingActivitiesDict = []
        # Payments To Acquire Investment
        try:
            PaymentsToAcquireInvestments = []
            for key,value in CashFlowStatement.items():
                if key == 'PaymentsToAcquireAvailableForSaleSecuritiesDebt':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Payments To Acquire Available For Sale Securities Debt: ' + str(ARCHvalue))
                    PaymentsToAcquireInvestments.append(ARCHvalue)
                if key == 'PaymentsToAcquireOtherInvestments':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Payments To Acquire Other Investments: ' + str(ARCHvalue))
                    PaymentsToAcquireInvestments.append(ARCHvalue)
                if key == 'PaymentsForProceedsFromOtherInvestingActivities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Payments For Proceeds From Other Investing Activities: ' + str(ARCHvalue))
                    PaymentsToAcquireInvestments.append(ARCHvalue)
                if key == 'PurchasesOfMarketableSecurities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Purchases Of Marketable Securities: ' + str(ARCHvalue))
                    PaymentsToAcquireInvestments.append(ARCHvalue)
                if key == 'PurchasesOfNonMarketableSecurities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Purchases Of Non Marketable Securities: ' + str(ARCHvalue))
                    PaymentsToAcquireInvestments.append(ARCHvalue)
                if key == 'PaymentsToAcquireMarketableSecurities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Payments To Acquire Marketable Securities: ' + str(ARCHvalue))
                    PaymentsToAcquireInvestments.append(ARCHvalue)
                else:
                    pass
            cf.PaymentsToAcquireInvestments = sum(PaymentsToAcquireInvestments)
            InvestingActivitiesDict.append(cf.PaymentsToAcquireInvestments)
            print()
            print('Payments To Acquire Investment: ' + str(cf.PaymentsToAcquireInvestments) + ' $')
            print(15*"-")
        except:
            pass
        # Proceeds Of Investment
        try:
            ProceedsOfInvestments = []
            for key,value in CashFlowStatement.items():
                if key == 'ProceedsFromMaturitiesPrepaymentsAndCallsOfAvailableForSaleSecurities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Proceeds From Maturities Prepayments And Calls Of Available For Sale Securities: ' + str(ARCHvalue))
                    ProceedsOfInvestments.append(ARCHvalue)
                elif key == 'ProceedsFromSaleOfAvailableForSaleSecuritiesDebt':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Proceeds From Sale Of Available For Sale Securities Debt: ' + str(ARCHvalue))
                    ProceedsOfInvestments.append(ARCHvalue)
                elif key == 'ProceedsFromSaleAndMaturityOfOtherInvestments':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Proceeds From Sale And Maturity Of Other Investments: ' + str(ARCHvalue))
                    ProceedsOfInvestments.append(ARCHvalue)
                elif key == 'ProceedsFromMaturitiesOfMarketableSecurities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Proceeds From Maturities Of Marketable Securities: ' + str(ARCHvalue))
                    ProceedsOfInvestments.append(ARCHvalue)
                elif key == 'ProceedsFromSalesOfMarketableSecurities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Proceeds From Sales Of Marketable Securities: ' + str(ARCHvalue))
                    ProceedsOfInvestments.append(ARCHvalue)
                elif key == 'ProceedsFromNonMarketableSecurities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Proceeds From Non Marketable Securities: ' + str(ARCHvalue))
                    ProceedsOfInvestments.append(ARCHvalue)
                else:
                    pass
            cf.ProceedsOfInvestments = sum(ProceedsOfInvestments)
            InvestingActivitiesDict.append(cf.ProceedsOfInvestments)
            print()
            print('Proceeds Of Investment: ' + str(cf.ProceedsOfInvestments) + ' $')
            print(15*"-")
        except:
            pass
        # Payments To Acquire Property Plant And Equipment
        try:
            PaymentsToAcquirePropertyPlantAndEquipment = []
            for key,value in CashFlowStatement.items():
                if key == 'PaymentsToAcquirePropertyPlantAndEquipment':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Payments To Acquire Property Plant And Equipment: ' + str(ARCHvalue))
                    PaymentsToAcquirePropertyPlantAndEquipment.append(-value)
                if key == 'PaymentsForAcquisitionOfPropertyPlantAndEquipment':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Payments For Acquisition Of Property Plant And Equipment: ' + str(ARCHvalue))
                    PaymentsToAcquirePropertyPlantAndEquipment.append(ARCHvalue)
                else:
                    pass
            cf.PaymentsToAcquirePropertyPlantAndEquipment = sum(PaymentsToAcquirePropertyPlantAndEquipment)
            InvestingActivitiesDict.append(cf.PaymentsToAcquirePropertyPlantAndEquipment)
            print()
            print('Payments To Acquire Property Plant And Equipment: ' + str(cf.PaymentsToAcquirePropertyPlantAndEquipment) + ' $')
            print(15*"-")
        except:
            pass
        # Payments To Acquire Businesses and Intangibles Net Of Cash Acquired
        try:
            PaymentsToAcquireBusinessesAndIntangibles = []
            for key,value in CashFlowStatement.items():
                if key == 'PaymentsToAcquireBusinessesNetOfCashAcquired':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Payments To Acquire Businesses Net Of Cash Acquired: ' + str(ARCHvalue))
                    PaymentsToAcquireBusinessesAndIntangibles.append(ARCHvalue)
                if key == 'PaymentsMadeInConnectionWithBusinessAcquisitionsNet':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Payments Made In Connection With Business Acquisitions Net: ' + str(ARCHvalue))
                    PaymentsToAcquireBusinessesAndIntangibles.append(ARCHvalue)
                if key == 'PaymentsForAcquisitionOfIntangibleAssets':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Payments For Acquisition Of Intangible Assets: ' + str(ARCHvalue))
                    PaymentsToAcquireBusinessesAndIntangibles.append(ARCHvalue)
                if key == 'PaymentsForStrategicInvestmentsNet':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Payments For Strategic Investments Net: ' + str(ARCHvalue))
                    PaymentsToAcquireBusinessesAndIntangibles.append(ARCHvalue)
                if key == 'PaymentsForStrategicInvestments':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Payments For Strategic Investments: ' + str(ARCHvalue))
                    PaymentsToAcquireBusinessesAndIntangibles.append(ARCHvalue)
                if key == 'PaymentsToAcquireBusinessesNetOfCashAcquiredAndPurchasesOfIntangibleAndOtherAssets':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Payments To Acquire Businesses Net Of Cash Acquired And Purchases Of Intangible And Other Assets: ' + str(ARCHvalue))
                    PaymentsToAcquireBusinessesAndIntangibles.append(ARCHvalue)
                else:
                    pass
            cf.PaymentsToAcquireBusinessesAndIntangibles = sum(PaymentsToAcquireBusinessesAndIntangibles)
            InvestingActivitiesDict.append(cf.PaymentsToAcquireBusinessesAndIntangibles)
            print()
            print('Payments To Acquire Businesses and Intangibles, Net Of Cash Acquired: ' + str(cf.PaymentsToAcquireBusinessesAndIntangibles) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Total Investing Activities
        try:
            InvestingActivities = []
            for key,value in CashFlowStatement.items():
                if key == 'NetCashProvidedByUsedInInvestingActivities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Net Cash Provided By Used In Investing Activities: ' + str(ARCHvalue))
                    InvestingActivities.append(ARCHvalue)
                if key == 'CashGeneratedByUsedInInvestingActivities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Cash Generated By Used In Investing Activities: ' + str(ARCHvalue))
                    InvestingActivities.append(ARCHvalue)
                if key == 'CashUsedInInvestingActivities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Cash Used In Investing Activities: ' + str(ARCHvalue))
                    InvestingActivities.append(ARCHvalue)
                else:
                    pass
            a.InvestingActivities = sum(InvestingActivities)
            print()
            print('Investing Activities: ' + str(a.InvestingActivities) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Anomaly Investing Activities
        try:
            Anomaly = a.InvestingActivities - sum(InvestingActivitiesDict)
            cf.OtherInvestingActivities = Anomaly
        except:
            pass
        ###############################################################################################################
        # FINANCING ACTIVITIES
        print(137*'-')
        print('FINANCING ACTIVITIES')
        print(137*'-')
        ###############################################################################################################
        FinancingActivitiesDict = []
        # Finance Lease Principal Payments
        try:
            FinanceLeasePrincipalPayments = []
            for key,value in CashFlowStatement.items():
                if key == 'FinanceLeasePrincipalPayments':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Finance Lease Principal Payments: ' + str(ARCHvalue))
                    FinanceLeasePrincipalPayments.append(ARCHvalue)
                else:
                    pass
            cf.FinanceLeasePrincipalPayments = sum(FinanceLeasePrincipalPayments)
            FinancingActivitiesDict.append(cf.FinanceLeasePrincipalPayments)
            print()
            print('Proceeds From Issuance Of Common Stock: ' + str(cf.FinanceLeasePrincipalPayments) + ' $')
            print(15*"-")
        except:
            pass        
        # Proceeds From Issuance Of Common Stock
        try:
            ProceedsFromIssuanceOfCommonStock = []
            for key,value in CashFlowStatement.items():
                if key == 'ProceedsFromIssuanceOfCommonStock':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Proceeds From Issuance Of Common Stock: ' + str(ARCHvalue))
                    ProceedsFromIssuanceOfCommonStock.append(ARCHvalue)
                else:
                    pass
            cf.ProceedsFromIssuanceOfCommonStock = sum(ProceedsFromIssuanceOfCommonStock)
            FinancingActivitiesDict.append(cf.ProceedsFromIssuanceOfCommonStock)
            print()
            print('Proceeds From Issuance Of Common Stock: ' + str(cf.ProceedsFromIssuanceOfCommonStock) + ' $')
            print(15*"-")
        except:
            pass
        # Payments Related To Tax Withholding For Share Based Compensation
        try:
            PaymentsRelatedToTaxWithholdingForShareBasedCompensation = []
            for key,value in CashFlowStatement.items():
                if key == 'PaymentsRelatedToTaxWithholdingForShareBasedCompensation':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Payments Related To Tax Withholding For Share Based Compensation: ' + str(ARCHvalue))
                    PaymentsRelatedToTaxWithholdingForShareBasedCompensation.append(ARCHvalue)
                else:
                    pass
            cf.PaymentsRelatedToTaxWithholdingForShareBasedCompensation = -sum(PaymentsRelatedToTaxWithholdingForShareBasedCompensation)
            FinancingActivitiesDict.append(cf.PaymentsRelatedToTaxWithholdingForShareBasedCompensation)
            print()
            print('Payments Related To Tax Withholding For Share Based Compensation: ' + str(cf.PaymentsRelatedToTaxWithholdingForShareBasedCompensation) + ' $')
            print(15*"-")
        except:
            pass
        # Payments Of Dividends
        try:
            PaymentsOfDividends = []
            for key,value in CashFlowStatement.items():
                if key == 'PaymentsOfDividends':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Payments Of Dividends: ' + str(ARCHvalue))
                    PaymentsOfDividends.append(ARCHvalue)
                if key == 'PaymentsForDividendsAndDividendEquivalents':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Payments For Dividends And Dividend Equivalents: ' + str(ARCHvalue))
                    PaymentsOfDividends.append(ARCHvalue)
                else:
                    pass
            cf.PaymentsOfDividends = sum(PaymentsOfDividends)
            FinancingActivitiesDict.append(cf.PaymentsOfDividends)
            print()
            print('Payments Of Dividends: ' + str(cf.PaymentsOfDividends) + ' $')
            print(15*"-")
        except:
            pass
        # Payments For Repurchase Of Common Stock
        try:
            PaymentsForRepurchaseOfCommonStock = []
            for key,value in CashFlowStatement.items():
                if key == 'PaymentsForRepurchaseOfCommonStock':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Payments For Repurchase Of Common Stock: ' + str(ARCHvalue))
                    PaymentsForRepurchaseOfCommonStock.append(ARCHvalue)
                if key == 'RepurchasesOfCommonStock':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Repurchases Of Common Stock: ' + str(ARCHvalue))
                    PaymentsForRepurchaseOfCommonStock.append(-value)
                else:
                    pass
            cf.PaymentsForRepurchaseOfCommonStock = -sum(PaymentsForRepurchaseOfCommonStock)
            FinancingActivitiesDict.append(cf.PaymentsForRepurchaseOfCommonStock)
            print()
            print('Payments For Repurchase Of Common Stock: ' + str(cf.PaymentsForRepurchaseOfCommonStock) + ' $')
            print(15*"-")
        except:
            pass
        # Payments For Taxes Related To Net Share Settlement Of Equity Award
        try:
            PaymentsForTaxesRelatedToNetShareSettlementOfEquityAward = []
            for key,value in CashFlowStatement.items():
                if key == 'PaymentsForTaxesRelatedToNetShareSettlementOfEquityAward':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Payments For Taxes Related To Net Share Settlement Of Equity Award: ' + str(ARCHvalue))
                    PaymentsForTaxesRelatedToNetShareSettlementOfEquityAward.append(ARCHvalue)
                if key == 'PaymentsForTaxesRelatedToNetShareSettlementOfEquityAwards':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Payments For Taxes Related To Net Share Settlement Of Equity Awards: ' + str(ARCHvalue))
                    PaymentsForTaxesRelatedToNetShareSettlementOfEquityAward.append(ARCHvalue)
                if key == 'ExcessTaxBenefitsFromEquityAwards':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Excess Tax Benefits From Equity Awards: ' + str(ARCHvalue))
                    PaymentsForTaxesRelatedToNetShareSettlementOfEquityAward.append(ARCHvalue)
                else:
                    pass
            cf.PaymentsForTaxesRelatedToNetShareSettlementOfEquityAward = sum(PaymentsForTaxesRelatedToNetShareSettlementOfEquityAward)
            FinancingActivitiesDict.append(cf.PaymentsForTaxesRelatedToNetShareSettlementOfEquityAward)
            print()
            print('Payments For Taxes Related To Net Share Settlement Of Equity Award: ' + str(cf.PaymentsForTaxesRelatedToNetShareSettlementOfEquityAward) + ' $')
            print(15*"-")
        except:
            pass
        # Proceeds From Issuance Of Long Term Debt
        try:
            ProceedsFromIssuanceOfLongTermDebt = []
            for key,value in CashFlowStatement.items():
                if key == 'ProceedsFromIssuanceOfLongTermDebt':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Proceeds From Issuance Of Long Term Debt: ' + str(ARCHvalue))
                    ProceedsFromIssuanceOfLongTermDebt.append(ARCHvalue)
                if key == 'ProceedsFromIssuanceOfTermDebtNet':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Proceeds From Issuance Of Term Debt Net: ' + str(ARCHvalue))
                    ProceedsFromIssuanceOfLongTermDebt.append(ARCHvalue)
                else:
                    pass
            cf.ProceedsFromIssuanceOfLongTermDebt = sum(ProceedsFromIssuanceOfLongTermDebt)
            FinancingActivitiesDict.append(cf.ProceedsFromIssuanceOfLongTermDebt)
            print()
            print('Proceeds From Issuance Of Long Term Debt: ' + str(cf.ProceedsFromIssuanceOfLongTermDebt) + ' $')
            print(15*"-")
        except:
            pass
        # Repayments Of Long Term Debt
        try:
            RepaymentsOfLongTermDebt = []
            for key,value in CashFlowStatement.items():
                if key == 'RepaymentsOfLongTermDebt':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Repayments Of Long Term Debt: ' + str(ARCHvalue))
                    RepaymentsOfLongTermDebt.append(ARCHvalue)
                if key == 'RepaymentsOfTermDebt':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Repayments Of Term Debt: ' + str(ARCHvalue))
                    RepaymentsOfLongTermDebt.append(ARCHvalue)
                else:
                    pass
            cf.RepaymentsOfLongTermDebt = sum(RepaymentsOfLongTermDebt)
            FinancingActivitiesDict.append(cf.RepaymentsOfLongTermDebt)
            print()
            print('Repayments Of Long Term Debt: ' + str(cf.RepaymentsOfLongTermDebt) + ' $')
            print(15*"-")
        except:
            pass
        # Proceeds From Repayments Of Commercial Paper
        try:
            ProceedsFromRepaymentsOfCommercialPaper = []
            for key,value in CashFlowStatement.items():
                if key == 'ProceedsFromRepaymentsOfCommercialPaper':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Proceeds From Repayments Of Commercial Paper: ' + str(ARCHvalue))
                    ProceedsFromRepaymentsOfCommercialPaper.append(ARCHvalue)
                if key == 'ChangeInCommercialPaperNet':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Change In Commercial Paper Net: ' + str(ARCHvalue))
                    ProceedsFromRepaymentsOfCommercialPaper.append(ARCHvalue)
                if key == 'ChangeInCommercialPaperNet':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Change In Commercial Paper Net: ' + str(ARCHvalue))
                    ProceedsFromRepaymentsOfCommercialPaper.append(ARCHvalue)
                if key == 'RepaymentsOfCommercialPaperNet':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Repayments Of Commercial Paper Net: ' + str(ARCHvalue))
                    ProceedsFromRepaymentsOfCommercialPaper.append(ARCHvalue)
                else:
                    pass
            cf.ProceedsFromRepaymentsOfCommercialPaper = sum(ProceedsFromRepaymentsOfCommercialPaper)
            FinancingActivitiesDict.append(cf.ProceedsFromRepaymentsOfCommercialPaper)
            print()
            print('Proceeds From Repayments Of Commercial Paper: ' + str(cf.ProceedsFromRepaymentsOfCommercialPaper) + ' $')
            print(15*"-")
        except:
            pass
        # Other Financing Activities
        try:
            OtherFinancingActivities = []
            for key,value in CashFlowStatement.items():
                if key == 'ProceedsFromPaymentsForOtherFinancingActivities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Proceeds From Payments For Other Financing Activities: ' + str(ARCHvalue))
                    OtherFinancingActivities.append(ARCHvalue)
                if key == 'ProceedsFromRepaymentsOfBankOverdrafts':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Proceeds From Repayments Of Bank Overdrafts: ' + str(ARCHvalue))
                    OtherFinancingActivities.append(ARCHvalue)
                else:
                    pass
            cf.OtherFinancingActivities = sum(OtherFinancingActivities)
            FinancingActivitiesDict.append(cf.OtherFinancingActivities)
            print()
            print('Other Financing Activities: ' + str(cf.OtherFinancingActivities) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Total Financing Activities
        try:
            FinancingActivities = []
            for key,value in CashFlowStatement.items():
                if key == 'NetCashProvidedByUsedInFinancingActivities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Net Cash Provided By Used In Financing Activities: ' + str(ARCHvalue))
                    FinancingActivities.append(ARCHvalue)
                if key == 'CashUsedInFinancingActivities':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Cash Used In Financing Activities: ' + str(ARCHvalue))
                    FinancingActivities.append(ARCHvalue)
                else:
                    pass
            a.FinancingActivities = sum(FinancingActivities)
            print()
            print('Financing Activities: ' + str(a.FinancingActivities) + ' $')
            print(15*"-")
        except:
            pass
        ###############################################################################################################
        # Anomaly Financing Activities
        try:
            Anomaly = a.FinancingActivities - sum(FinancingActivitiesDict)
            cf.OtherFinancingActivities = cf.OtherFinancingActivities + Anomaly
        except:
            pass
        ###############################################################################################################
        # SUPPLEMENTAL CASH FLOW DISCLOSURE
        print(137*'-')
        print('SUPPLEMENTAL CASH FLOW DISCLOSURE')
        print(137*'-')
        ###############################################################################################################
        # Cash paid for in interest
        try:
            CashPaidForInterest = []
            for key,value in CashFlowStatement.items():
                if key == 'CashPaidForInterest':
                    try:
                        i = 0
                        while value[i] == None:
                            i = i + 1
                        ARCHvalue = value[i]
                        value[i] = None
                    except:
                        ARCHvalue = value
                        CashFlowStatement[key] = None
                    print('Cash Paid For Interest: ' + str(ARCHvalue))
                    CashPaidForInterest.append(ARCHvalue)
                else:
                    pass
            cf.CashPaidForInterest = sum(CashPaidForInterest)
            print()
            print('Cash Paid For Interest: ' + str(cf.CashPaidForInterest) + ' $')
            print(15*"-")
        except:
            pass 
        ###############################################################################################################
        print(137*'-')
        try:
            tb.save()
            print(TradingSymbol + " Trial Balance Saved.")
        except:
            pass
        try:
            cf.save()
            print(TradingSymbol + " Cash Flow Saved.")
        except:
            pass
        try:
            a.save()
            print(TradingSymbol + " Audit Saved.")
        except:
            pass
        print(137*'-')
    ###############################################################################################################
    # STOCKHOLDERS EQUITY BEGINNING BALANCES
    ###############################################################################################################
    for scopedperiod in scopedperiods:
        print('Beginning Balance ' + scopedperiod)
        try:
            dates = {
                'lastyear': 'secondlastyear',
                'secondlastyear': 'thirdlastyear',
                'thirdlastyear': 'fourthlastyear',
                'fourthlastyear': 'fifthlastyear',
                'fifthlastyear': 'sixthlastyear',
                'sixthlastyear': 'seventhlastyear',
                'lastquarter': 'secondlastquarter',
                'secondlastquarter': 'thirdlastquarter',
                'thirdlastquarter': 'fourthlastquarter',
            }
            prioryeartb = dates[scopedperiod]
            print('Ending Balance from ' + prioryeartb + "'s trial balance.")
            tb = TrialBalance.objects.get(TradingSymbol=TradingSymbol, Period=scopedperiod)
            a = AuditData.objects.get(TradingSymbol=TradingSymbol, Period=scopedperiod)
            prioryeartb = TrialBalance.objects.get(TradingSymbol=TradingSymbol, Period=prioryeartb)
            tb.StockholdersEquityBeginning = prioryeartb.StockholdersEquity
            print('Stockholders Equity Beginning Balance: ' + str(tb.StockholdersEquityBeginning))
            print('Prior Year Stockholders Equity: ' + str(prioryeartb.StockholdersEquity))
            tb.CommonSharesBeginning = prioryeartb.CommonShares
            print('Common Shares Beginning Balance: ' + str(tb.CommonSharesBeginning))
            print('Prior Year Common Shares: ' + str(prioryeartb.CommonShares))
            tb.AccumulatedOtherComprehensiveIncomeBeginning = prioryeartb.AccumulatedOtherComprehensiveIncomeLoss
            print('Accumulated Other Comprehensive Income (Loss) Beginning Balance: ' + str(tb.AccumulatedOtherComprehensiveIncomeBeginning))
            tb.RetainedEarningsBeginning = prioryeartb.RetainedEarningsAccumulatedDeficit
            print('Retained Earnings Beginning Balance: ' + str(tb.RetainedEarningsBeginning))
            StockholdersEquityVariation = tb.StockholdersEquity - tb.StockholdersEquityBeginning
            #
            ComponentsVariation = {
                tb.CommonStockIssued,
                tb.ShareBasedCompensation,
                tb.DividendsAndDividendEquivalentsDeclared,
                tb.CommonStockRepurchasedAndRetired,
                tb.EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts,
                tb.OtherAdjustmentToStockholdersEquity,
                a.OtherComprehensiveIncome,
                a.NetIncome,
            }
            Anomaly = StockholdersEquityVariation - sum(ComponentsVariation)
            print('Anomaly: ' + str(Anomaly))
            #
            tb.save()
        except:
            print('---Could not establish beggining balances.')
    ############################################################################################################### 
    # Save Entity
    ###############################################################################################################
    # Time Of Update
    try:
        now = datetime.now()
        year = now.strftime("%Y")
        month = now.strftime("%m")
        day = now.strftime("%d")
        time = now.strftime("%H:%M:%S")
        date = now.strftime("%d/%m/%Y")
        date_text = now.strftime("%B %d, %Y")
        e.Update = date_text
        print("Update: ", e.Update)
    except:
        pass
    try:
        e.save()
        print(137*'-')
        print('Entity ' + TradingSymbol + ' Saved.')
        print(137*'-')
    except:
        print(137*'-')
        print('---Could not save entity.')
        print(137*'-')

##############################################################################################################    

# OUTPUT DIRECTORY
try:
    output_directory = './φ/algorithm/GL/'
    # Delete the content of the download file
    files = glob.glob('A:/arch/φ/algorithm/GL/*')
    for f in files:
        os.remove(f)
except:
    print('---Could not define and clear output directory.')

# GL (Dictionary)
#with open(output_directory + 'GL.txt', 'a') as GL_file:
#    for GL_Dictionary_item in GL_Dictionary:
#        GL_file.write(GL_Dictionary_item)
#        GL_file.write('\n')

###############################################################################################################
# Model
#
try:
    try:
        Entity.objects.get(TradingSymbol='CLOCK').delete()
    except:
        pass

    m = Entity()
    #
    m.TradingSymbol='CLOCK'
    m.EntityRegistrantName = 'MODEL'
    m.Industry = 'DATA PROCESSING'
    m.EntityIncorporationStateCountryCode = 'CALIFORNIA'
    m.Region = 'NEW YORK'
    m.CurrentFiscalYearEndDate = '12-31'
    m.SecurityExchangeName = 'Security Exchange Name'
    m.Regulator = 'Regulator'
    #
    m.lastquarter = 'September 31, 2020'
    m.secondlastquarter = 'June 31, 2020'
    m.thirdlastquarter = 'March 31, 2020'
    #
    m.lastyear = 'December 31, 2020'
    m.secondlastyear = 'December 31, 2019'
    m.thirdlastyear = 'December 31, 2018'
    m.fourthlastyear = 'December 31, 2017'
    m.fifthlastyear = 'December 31, 2016'
    m.sixthlastyear = 'December 31, 2015'
    m.seventhlastyear = 'December 31, 2014'
    m.save()
    #
    # ARCH Trial Balance
    #
    for scopedperiod in scopedperiods:
        try:
            TrialBalance.objects.get(TradingSymbol='CLOCK', Period=scopedperiod)
        except:
            TrialBalance(TradingSymbol='CLOCK', Period=scopedperiod).save()
except:
    pass

#print(137*'-')
#print(IncomeStatement_GLs)
#print(IncomeStatement)
#print(137*'-')
#print(ComprehensiveIncome_GLs)
#print(ComprehensiveIncome)
#print(137*'-')
#print(BalanceSheet_GLs)
#print(BalanceSheet)
#print(137*'-')
#print(StockholdersEquity_GLs)
#print(StockholdersEquity)
#print(137*'-')
#print(CashFlow_GLs)
#print(CashFlow)
#print(137*'-')


