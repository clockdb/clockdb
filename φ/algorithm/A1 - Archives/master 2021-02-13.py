# Libraries
from φ.models import *
from bs4 import BeautifulSoup
from io import StringIO
from datetime import date
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
import urllib
import xml.etree.ElementTree as ET

# TradingSymbol to EntityCentralIndexKeys
EntityCentralIndexKeys = {
    'AAPL':    '320193',
    'LLY':    '59478',
}

#
# scope
scopedperiods = [
    'lastyear',
    'secondlastyear',
    'thirdlastyear',
    'fourthlastyear',
    'fifthlastyear',
    'sixthlastyear',
    'seventhlastyear',
]

BeginningBalances = 'yes'
Regularize = 'yes'
GetStockPrice = 'no'

# Marketstack API
params = {
    'access_key': 'ecae621d4718099f0d660a237c429450',
}

# GLs
IncomeStatement_GLs = []
ComprehensiveIncome_GLs = []
BalanceSheet_GLs = []
StockholdersEquity_GLs = []
CashFlow_GLs = []

# arch financial statements
ARCH_FinancialStatements = {
    'ARCH_IncomeStatement',
    'ARCH_ComprehensiveIncome',
    'ARCH_BalanceSheet',
    'ARCH_ShareholdersEquity',
    'ARCH_CashFlowStatement',
}
ARCH_IncomeStatement = {}
ARCH_ComprehensiveIncome = {}
ARCH_BalanceSheet = {}
ARCH_StockholdersEquityStatement = {}
ARCH_CashFlowStatement = {}

# Regular Expressions Endings
RegularExpressionEndings = [
    'AndOther',
    'AndOtherAssets',
    'AndOtherLiabilities',
    'AndOtherNetofTax',
    'AndOthers',
    'AtDec',
    'AtEndOfYear',
    'Net',
    'NetOfTax',
    'OfAnd',
    'Of()And()',
    'OfTheYear',
    'LessAllowances',
    'NetCurrent',
    'NetNonCurrent',
    'NetOfAllowances',
    'NetOfAllowancesOf()And()',
]

# Regular Expressions
RegularExpressions = [
    '()',
    'AdjustmentFor',
    'AdjustmentRelatedTo',
    'AndAdditionalPaidInCapitalParValueSharesAuthorizedAndSharesIssuedAndOutstandingRespectively',
    'AndCashEquivalents',
    'AndOtherIncome',
    'AndRestrictedCash',
    'ArisingDuringPeriod',
    'AtCarryingValue',
    'AvailableForSale',
    'BeforeReclassificationAfterTax',
    'ChangeInEffectivePortionOf',
    'ChangeInFairValueOf',
    'ExcludingAssessedTax',
    'ExtraordinaryItemsNoncontrollingInterest',
    '(IncludesAndOfDiscontinuedOperations)',
    'NetOfTaxBenefitExpense',
    'NetOfTaxEffects',
    'NoParValueAuthorizedSharesIssuedSharesAnd',
    '(Note)',
    '(NoteAnd)',
    '(Notes)',
    '(NotesAnd)',
    'ReclassificationAfterTax',
]

# industries 
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
}

di = []

ip = []

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

#
# model corporation
try:
    try:
        Entity.objects.get(TradingSymbol='MODEL').delete()
    except:
        pass
    #
    m = Entity()
    #
    m.TradingSymbol='CLOCK'
    m.EntityRegistrantName = 'MODELS'
    m.Industry = 'DATA PROCESSING, AUDIT, BUSINESS VALUATION'
    m.EntityIncorporationStateCountryCode = 'NEW YORK'
    m.Region = 'CALIFORNIA'
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
    # Trial Balance
    #
    for scopedperiod in scopedperiods:
        try:
            TrialBalance.objects.get(TradingSymbol='MODEL', Period=scopedperiod)
        except:
            TrialBalance(TradingSymbol='MODEL', Period=scopedperiod).save()
except:
    pass

# For all Entity,
for EntityCentralIndexKey in EntityCentralIndexKeys:
    #
    # TradingSymbol
    TradingSymbol = EntityCentralIndexKey
    #
    # entity
    try:
        print(137*'-' + '\n')
        #
        try:
            e = Entity.objects.get(TradingSymbol=TradingSymbol)
            #
            print(e.EntityRegistrantName + ' (' + e.TradingSymbol + ') retreived from φ.')
        except:
            e = Entity()
            e.TradingSymbol = TradingSymbol
            e.EntityCentralIndexKey = EntityCentralIndexKeys[TradingSymbol]
            e.save()
            #
            print('New Entity for TradingSymbol ' + TradingSymbol + ' created in φ.')
            #
            print(137*'-' + '\n')
    except:
        pass
    #
    # data
    for scopedperiod in scopedperiods:
        #
        #
        # models, filings, entity information, documents, etc.
        try:
            # dictionaries
            try:
                IncomeStatement = {}
                ComprehensiveIncomeStatement = {}
                BalanceSheet = {}
                StockholdersEquityStatement = {}
                CashFlowStatement = {}
            except:
                pass
            #
            # period
            try:
                print(scopedperiod)
                print(137*'-')
            except:
                print('---Could not print name, symbol or period.')
            #
            # trial balance
            try:
                # Deletes Trial Balance
                try:
                    tb = TrialBalance.objects.get(TradingSymbol=TradingSymbol, Period=scopedperiod)
                    print('Trial Balance from ' + tb.Period + ' deleted from the φ.')
                    tb.delete()
                except:
                    pass
                # Creates Trial Balance
                try:
                    tb = TrialBalance(TradingSymbol=TradingSymbol, Period=scopedperiod)
                    tb.save()
                    print('Trial Balance for ' + scopedperiod + ' created.')
                except:
                    pass
            except:
                pass
            #
            # cash flow
            try:
                # Deletes Cash Flow Statements
                try:
                    cf = CashFlow.objects.get(TradingSymbol=TradingSymbol, Period=scopedperiod)
                    print('Cash Flow from ' + cf.Period + ' deleted from the φ.')
                    cf.delete()
                except:
                    pass
                # Creates ARCH Cash Flow Statements
                try:
                    cf = CashFlow(TradingSymbol=TradingSymbol, Period=scopedperiod)
                    cf.save()
                    print('Cash Flow for ' + scopedperiod + ' created.')
                except:
                    pass
            except:
                pass
            #
            # audit
            try:
                # Deletes Audit
                try:
                    a = AuditData.objects.get(TradingSymbol=TradingSymbol, Period=scopedperiod)
                    print('Audit from ' + cf.Period + ' deleted from the φ.')
                    a.delete()
                except:
                    pass
                # Creates Audit
                try:
                    a = AuditData(TradingSymbol=TradingSymbol, Period=scopedperiod)
                    a.save()
                    print('Audit for ' + scopedperiod + ' created.')
                except:
                    pass
            except:
                pass
            #
            # last filings
            try:
                filings_list_base_url = r"https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="
                EntityCentralIndexKey = EntityCentralIndexKeys[TradingSymbol]
                print(137*'-')
                print('CIK: ' + str(EntityCentralIndexKey))
                if scopedperiod in Quarters:
                    report = '10-Q'
                    if scopedperiod == 'lastquarter':
                        periodurl = ''
                else:
                    report = '10-K'
                    if scopedperiod == 'lastyear':
                        periodurl = ''
                print('Report type:' + report)
                try:
                    prior = periodurl
                    filings_list_base_url = filings_list_base_url + EntityCentralIndexKey + '&type=' + report + '&dateb='
                    filings_url = filings_list_base_url + prior + '&owner=exclude&count=40&search_text='
                    print(filings_url)
                except:
                    filings_url = filings_list_base_url + '&owner=exclude&count=40&search_text='
                    print(filings_url)
                filings_list_html = fetch(filings_url)
                #
                e.save()
            except:
                pass
            #
            # accession number - (to be updated re amend)
            try:
                i = 0
                accessionnumber = filings_list_html.find_all('td', class_='small')[i].text
                #
                # Accession Number Replacements
                rep1 = 'Transition reports [Rule 13a-10 or 15d-10]Acc-no: '
                rep2 = 'Annual report [Section 13 and 15(d), not S-K Item 405]Acc-no: '
                rep3 = 'Quarterly report [Sections 13 or 15(d)]Acc-no: '
                #
                while accessionnumber == '[Amend]':
                    i = i + 1
                    accessionnumber = filings_list_html.find_all('td', class_='small')[i].text
                    print(accessionnumber)
                #
                accessionnumber = accessionnumber.replace(rep1,'').replace(rep2,'').replace(rep3,'')[:20]
                #
                print('Accession number ' + accessionnumber)
                print(137*'-')
            except:
                print("---Could not retreive accession number.")
            #
            # entity information
            try:
                company_info_div = filings_list_html.find_all('div', class_='companyInfo')[0]
                #
                e.EntityRegistrantName = company_info_div.find_all('span', class_='companyName')[0].text.split(' CIK')[0].upper()
                print(e.EntityRegistrantName)
                #
                e.Industry = Industries[company_info_div.find_all('a')[1].text]
                print(e.Industry)
                #
                e.Region = Regions[company_info_div.find_all('a')[2].text]
                print(e.Region)
                #
                e.EntityIncorporationStateCountryCode = Regions[company_info_div.find_all('strong')[0].text]
                print(e.EntityIncorporationStateCountryCode)
                #
                print(137*'-')
            except:
                pass
            #
            # documents
            try:
                #
                # Retreives documents URL 
                try:
                    filing_documents_base_url = r"https://www.sec.gov/Archives/edgar/data/"
                    filing_documents_url = filing_documents_base_url + EntityCentralIndexKey + '/' + accessionnumber.replace('-','') + '/' + accessionnumber + '-index.htm'
                    tb.Link = filing_documents_url
                except:
                    print('---Could not retreive document`s url.')
                #
                # Retreives html code from filing documents url
                try:
                    filing_documents_html = fetch(filing_documents_url)
                except:
                    print('---Could not retreive filing html.')
                #
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
                    print('DOCS URL: ' + filing_documents_url)
                #
                except:
                    print('---Could not retreive filing report date.')
                #
                # saves period of report
                try:
                    tb.PeriodOfReport = period
                    print('Period Of Report: ' + tb.PeriodOfReport)
                    tb.FilingDate = filing_documents_html.find_all('div', class_="info")[0].text
                    print('Filing Date: ' + tb.FilingDate)
                except:
                    print('---Could not establish Period Of Report And / Or Filing Date')
                #
                # Retreive filing documents tables
                try:
                    XBRL_taxonomy = filing_documents_html.find_all('table', class_="tableFile")[1].findAll('a')
                except:
                    print('---Could not retreive filing documents tables')
                #
                # Creates xml base url for calculation, definition and label 
                try:
                    xml_base_url = filing_documents_base_url + EntityCentralIndexKey + '/' + accessionnumber.replace('-','') + '/'
                except:
                    print('---Could not define xml_base_url')
                #
                # Defines downloads directory
                try:
                    downloads_directory = './φ/algorithm/downloads/'
                except:
                    print('---Could not define downloads directory.')
                #
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
                #
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
                #
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
                #
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
                #
                # Define downloads directory for SEC files
                try:
                    SEC_directory = pathlib.Path.cwd().joinpath('./φ/algorithm/downloads')
                except:
                    print('---Could not define path to downloads.')
                #
                # Resolve path to files
                try:
                    file_htm = SEC_directory.joinpath(filing_document).resolve()
                    file_cal = SEC_directory.joinpath(calculation_document).resolve()
                    file_def = SEC_directory.joinpath(definition_document).resolve()
                    file_lab = SEC_directory.joinpath(label_document).resolve()
                except:
                    print('Could not resolve directory.')
                #
                # Define the different storage components
                try:
                    storage_list = []
                    storage_values = {}
                    storage_gaap = {}
                except:
                    print('---Could not define storage components')
                #
                # Creates tuple
                try:
                    FilingTuple = collections.namedtuple('FilingTuple',['file_path','namespace_element','namespace_label'])
                except:
                    print('---Could not create tuples')
                #
                # Initialize list of named tuples to be parsed
                try:
                    files_list = [
                        FilingTuple(file_cal, r'{http://www.xbrl.org/2003/linkbase}calculationLink', 'calculation'),
                        FilingTuple(file_def, r'{http://www.xbrl.org/2003/linkbase}definitionLink', 'definition'),
                        FilingTuple(file_lab, r'{http://www.xbrl.org/2003/linkbase}labelLink', 'label'),
                    ]
                except:
                    print('---Could not initialize list of named tuples to be parsed')
                #
                # Defines categories of labels to be excluded
                try:
                    avoids = ['linkbase','roleRef']
                    parse = ['label','labelLink','labelArc','loc','definitionLink','definitionArc','calculationArc']
                except:
                    print('---Could not define labels to be excluded')
                #
                # Creates empty sets
                try:
                    lab_list = set()
                    cal_list = set()
                except:
                    print('---Could not create empty sets.')
            except:
                pass
            #
            # Trees
            try:
                print(137*'-')
                f = open(file_htm, "r")
                content = f.read()                
                #
                # Method after 2018
                if content[:5] == '<?xml':
                    MethodAfter2018Applies = 'yes'
                    try:
                        # files
                        for file in files_list:
                            tree = ET.parse(file.file_path)
                            elements = tree.findall(file.namespace_element)
                            for element in elements:
                                for child_element in element.iter():
                                    element_split_label = child_element.tag.split('}')
                                    namespace = element_split_label[0]
                                    label = element_split_label[1]
                                    if label in parse:
                                        element_type_label = file.namespace_label + '_' + label
                                        dict_storage = {}
                                        dict_storage['item_type'] = element_type_label
                                        cal_keys = child_element.keys()
                                        for key in cal_keys:
                                            if '}' in key:
                                                new_key = key.split('}')[1]
                                                dict_storage[new_key] = child_element.attrib[key]
                                            else:
                                                dict_storage[key] = child_element.attrib[key]
                                        if element_type_label == 'label_label':
                                            key_store = dict_storage['label']
                                            master_key = key_store.replace('lab_', '')
                                            label_split = master_key.split('_')
                                            gaap_id = label_split[0] + ":" + label_split[1]
                                            storage_values[master_key] = {}
                                            storage_values[master_key]['label_id'] = key_store
                                            storage_values[master_key]['location_id'] = key_store.replace('lab_','loc_')
                                            storage_values[master_key]['us_gaap_id'] = gaap_id
                                            storage_values[master_key]['us_gaap_value'] = None
                                            storage_values[master_key][element_type_label] = dict_storage
                                            storage_gaap[gaap_id] = {}
                                            storage_gaap[gaap_id]['id'] = gaap_id
                                            storage_gaap[gaap_id]['master_id'] = master_key
                                        storage_list.append([file.namespace_label, dict_storage])
                        #
                        # Tree Data
                        try:
                            #
                            # Qualitative
                            try:
                                tree = ET.parse(file_htm)
                                for element in tree.iter():
                                    if 'nonNumeric' in element.tag:
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
                                            print(SEC_component + ': ' + value)
                                        elif SEC_component == 'AmendmentFlag':
                                            tb.AmendmentFlag = value
                                            print(SEC_component + ': ' + value)
                                        elif SEC_component == 'DocumentFiscalPeriodFocus':
                                            tb.DocumentFiscalPeriodFocus = value
                                            print(SEC_component + ': ' + value)
                                        elif SEC_component == 'DocumentFiscalYearFocus':
                                            tb.DocumentFiscalYearFocus = value
                                            print(SEC_component + ': ' + value)
                                        elif SEC_component == 'DocumentPeriodEndDate':
                                            tb.DocumentPeriodEndDate = value
                                            print(SEC_component + ': ' + value)
                                        elif SEC_component == 'EntityIncorporationStateCountryCode':
                                            tb.EntityIncorporationStateCountryCode = value
                                            print(SEC_component + ': ' + value)
                                        elif SEC_component == 'Region':
                                            tb.Region = value
                                            print(SEC_component + ': ' + value)
                                        elif SEC_component == 'CurrentFiscalYearEndDate':
                                            tb.CurrentFiscalYearEndDate = value
                                            print(SEC_component + ': ' + value)
                                        elif SEC_component == 'SecurityExchangeName':
                                            if tb.SecurityExchangeName is None:
                                                tb.SecurityExchangeName = value
                                                print(SEC_component + ': ' + value)
                                        else:
                                            pass
                                # Save
                                tb.save()
                                print(137 * '-')
                            #
                            except:
                                pass
                        #
                        except:
                            pass
                    except:
                        pass
                #
                # Method After 2018
                else:
                    MethodAfter2018Applies = 'no'
                #
                print(137*'-')
                #
                # Documents general method
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
                    #
                    # list of reports in filing summary
                    reports = soup.find('myreports')
                    #
                    # reports
                    master_reports = []
                    statements_url = []
                    statements_set = {}
                    for report in reports.find_all('report')[:-1]:
                        report_dict = {}
                        report_dict['name_short'] = report.shortname.text
                        report_dict['name_long'] = report.longname.text
                        report_dict['position'] = report.position.text
                        report_dict['category'] = report.menucategory.text
                        report_dict['url'] = base_url + report.htmlfilename.text
                        t = report_dict['url']
                        d = report_dict['name_short'].upper()
                        d = re.sub(r"[^A-Z' ]", "", d)
                        q = [
                            'CONDENSED',
                            'CONSOLIDATED',
                            'STATEMENT',
                        ]
                        b = [
                            'DETAIL',
                            'PARENTHETICAL',
                            'POLICIES',
                            'SCHEDULE',
                            'SEGMENT',
                            'TABLE',
                            'UNAUDITED',
                        ]
                        s = 'a'
                        for p in q:
                            if s == 'a':
                                if p in d:
                                    i = 0
                                    l = 'e'
                                    s = 'a'
                                    for h in b:
                                        if s == 'a':
                                            while i < len(b):
                                                if b[i] in d:
                                                    l = 'u'
                                                i = i + 1
                                            if l == 'e':
                                                if 'EQUITY' in d:
                                                    append_value(ARCH_StockholdersEquityStatement, d,  t)
                                                if 'SHEET' in d:
                                                    append_value(ARCH_BalanceSheet, d,  t)
                                                if 'COMPREHENSIVE' in d:
                                                    append_value(ARCH_ComprehensiveIncome, d,  t)
                                                if 'INCOME' in d:
                                                    append_value(ARCH_IncomeStatement, d,  t)
                                                if 'OPERATION' in d:
                                                    append_value(ARCH_IncomeStatement, d,  t)
                                                if 'CASH' in d:
                                                    append_value(ARCH_CashFlowStatement, d,  t)
                                                append_value(statements_set, d,  t)
                                                statements_url.append(t)
                                                s = 'z'
                    #
                    #
                    pprint.pprint(statements_set)
                    #
                    #
                    # Statements data
                    statements_data = []
                    dad = 0
                    #
                    for financial_statement in statements_set:
                        #
                        statement = statements_set[financial_statement]
                        #
                        print(137*'-')
                        print(financial_statement)
                        print(137*'-')
                        #
                        statement_data = {}
                        statement_data['headers'] = []
                        statement_data['sections'] = []
                        statement_data['data'] = []
                        content = requests.get(statement).content
                        report_soup = BeautifulSoup(content, 'html')
                        #
                        m = report_soup.table.find_all('tr')
                        #
                        for index, row in enumerate(m):
                            #
                            try:
                                cols = row.find_all('td')
                                #
                                if (len(row.find_all('th')) == 0 and len(row.find_all('strong')) == 0):
                                    #
                                    t = [ele.text.strip() for ele in cols]
                                    #
                                    GL_SEC = t[0]
                                    #
                                    GL = re.sub(r"[^a-zA-Z()]", "", GL_SEC.title())
                                    #
                                    for y in RegularExpressions:
                                        GL = GL.replace(y,'')
                                    #
                                    for y in RegularExpressionEndings:
                                        l = len(GL) - len(y)
                                        if GL[l:] == y :
                                            GL = GL.split(y)[0]
                                    #
                                    # dad
                                    try:
                                        if dad == 0:
                                            try:
                                                qb = statement_data['headers'][0][0]
                                                if qb[-11:].upper() == 'IN MILLIONS':
                                                    dad = 1000000
                                                elif qb[-12:].upper() == 'IN THOUSANDS':
                                                    dad = 1000
                                                else:
                                                    dad = 1
                                            except:
                                                pass
                                    except:
                                        print('---Could not establish scale.')
                                    #
                                    #
                                    # value - stockholders equity statement
                                    if financial_statement in ARCH_StockholdersEquityStatement:
                                        value = 0
                                        o = 1
                                        while o < len(t):
                                            try:
                                                g = t[o]
                                                if g == '':
                                                    g = 0
                                                w = 1
                                                if '(' in g:
                                                    w = -1
                                                g = re.sub(r"[^.0123456789]", "", str(g))
                                                g = float(g)
                                                g = int(g * w * dad)
                                                value = value + g
                                            except:
                                                pass
                                            o = o + 1
                                        #
                                        # Arching
                                        try:
                                            append_value(StockholdersEquityStatement, GL, value)
                                            StockholdersEquity_GLs.append(GL)
                                            print('Stockholders Equity, ' + GL + ': ' + str(value))
                                        except:
                                            print('---Could not arch' + GL)
                                    #
                                    # value - other cases
                                    else:
                                        try:
                                            z = len(m[5].find_all('td'))
                                            x = m[5].find_all('td')[1].text
                                            if z == 5:
                                                if x == '' :
                                                    g = t[2]
                                                else:
                                                    g = t[1]
                                            else:
                                                g = t[1]
                                            if g == '':
                                                g = 0
                                            w = 1
                                            if '(' in g:
                                                w = -1
                                            g = re.sub(r"[^.0123456789]", "", str(g))
                                            g = float(g)
                                            value = int(g * w * dad)
                                            #
                                            # Arching
                                            try:
                                                if financial_statement in ARCH_IncomeStatement:
                                                    append_value(IncomeStatement, GL, value)
                                                    IncomeStatement_GLs.append(GL)
                                                    print('Income Statement, ' + GL + ': ' + str(value))
                                                #
                                                elif financial_statement in ARCH_ComprehensiveIncome:
                                                    append_value(ComprehensiveIncomeStatement, GL, value)
                                                    ComprehensiveIncome_GLs.append(GL)
                                                    print('Comprehensive Income, ' + GL + ': ' + str(value))
                                                #
                                                elif financial_statement in ARCH_BalanceSheet:
                                                    append_value(BalanceSheet, GL, value)
                                                    BalanceSheet_GLs.append(GL)
                                                    print('Balance Sheet, ' + GL + ': ' + str(value))
                                                #
                                                elif financial_statement in ARCH_CashFlowStatement:
                                                    append_value(CashFlowStatement, GL, value)
                                                    CashFlow_GLs.append(GL)
                                                    print('Cashflow, ' + GL + ': ' + str(value))
                                                #
                                                else:
                                                    print('---' + GL + ' Unallocated')
                                            except:
                                                print('---Could not arch' + GL)
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
                                    print('---Could not distinguish headers from section and regular rows.')
                            #
                            except:
                                print('---Could not append ARCH_GL')
                        #
                        statements_data.append(statement_data)
                    #
                    print(137*'-')
                    #
                    # Define documents period end date
                    if MethodAfter2018Applies == 'no':
                        try:
                            DPED = statements_data[0]['headers'][1][0].replace('Jan.', 'January').replace('Feb.', 'February').replace('Mar.', 'March')
                            DPED = DPED.replace('Apr.', 'April').replace('Jun.', 'June').replace('Jul.', 'July').replace('Aug.', 'August')
                            DPED = DPED.replace('Sep.', 'September').replace('Oct.', 'October').replace('Nov.', 'November').replace('Dec.', 'December')
                            #
                            tb.DocumentPeriodEndDate = DPED
                        except:
                            print('---Could not establish document period end date.')
                    try:
                        print('Document period End Date: ' + str(tb.DocumentPeriodEndDate))
                    except:
                        print('---Could not establish period end date')
                    #
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
                        print(137*'-')
                    except:
                        print('---Could Not Define Entity`s Period End Dates')
                except:
                    print('---Could not extract data from urls.')
            #
            except:
                print('---Could not extract tree.')
        except:
            pass
        #
        #
        # financial statements
        try:
            print('\n' * 3)
            #
            # balance sheet
            print('balance sheet')
            print(137*'-' + '\n')
            #
            #
            # current assets
            try:
                #
                print('current assets')
                print(137*'-')
                #
                #
                # total current assets
                try:
                    TotalCurrentAssets = []
                    r = 0
                    for key, value in BalanceSheet.items():
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
                            'Inventor',
                            'Investments',
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
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'TotalCurrentAssets')
                                        CurrentAssetsRank = r
                        r = r + 1
                    a.CurrentAssets = sum(TotalCurrentAssets)
                except:
                    pass
                #
                print('\n')
                #
                # cash
                try:
                    Cash = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r < CurrentAssetsRank:
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
                                            Cash.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'Cash')
                        r = r + 1
                    tb.Cash = sum(Cash)
                except:
                    pass
                #
                # short term investment
                try:
                    ShortTermInvestments = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r < CurrentAssetsRank:
                            d = key
                            q = [
                                'Investment',
                                'Securities',
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
                                            ShortTermInvestments.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'ShortTermInvestments')
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
                        if r < CurrentAssetsRank:
                            d = key
                            q = [
                                'Receivable',
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
                                            AccountsReceivable.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'AccountsReceivable')
                        r = r + 1
                    tb.AccountsReceivable = sum(AccountsReceivable)
                except:
                    pass
                #
                # inventories
                try:
                    Inventories = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r < CurrentAssetsRank:
                            d = key
                            q = [
                                'Inventor',
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'Inventories')
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
                        if r < CurrentAssetsRank:
                            d = key
                            q = [
                                'Prepaid',
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
                                            PrepaidExpenses.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'PrepaidExpenses')
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
                        if r < CurrentAssetsRank:
                            d = key
                            q = [
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'NonTradeReceivables')
                        r = r + 1
                    tb.NonTradeReceivables = sum(NonTradeReceivables)
                except:
                    pass
                #
                # deferred tax assets current
                try:
                    DeferredTaxAssetsCurrent = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r < CurrentAssetsRank:
                            d = key
                            q = [
                                'DeferredTax',
                                'DeferredIncome',
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
                                            DeferredTaxAssetsCurrent.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'DeferredTaxAssetsCurrent')
                        r = r + 1
                    tb.DeferredTaxAssetsCurrent = sum(DeferredTaxAssetsCurrent)
                except:
                    pass
                #
                # other current assets
                try:
                    OtherCurrentAssets = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r < CurrentAssetsRank:
                            d = key
                            q = [
                                'Other',
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
                                            OtherCurrentAssets.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'OtherCurrentAssets')
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
                        if r < CurrentAssetsRank:
                            d = key
                            q = [
                                'Discontinued',
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'DiscontinuedOperationsCurrent')
                        r = r + 1
                    tb.DiscontinuedOperationsCurrent = sum(DiscontinuedOperationsCurrent)
                except:
                    pass
                #
                print('\n' * 3)
                #
            except:
                pass
            #
            # non-current assets
            try:
                #
                print('non-current assets')
                print(137*'-')
                #
                # total non current assets
                try:
                    TotalNonCurrentAssets = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r > CurrentAssetsRank:
                            d = key
                            q = [
                                'NonCurrentAsset',
                            ]
                            b = [
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'TotalNonCurrentAssets')
                        r = r + 1
                    a.NonCurrentAssets = sum(TotalNonCurrentAssets)
                except:
                    pass
                #
                print('\n')
                #
                # investments
                try:
                    Investments = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r > CurrentAssetsRank:
                            d = key
                            q = [
                                'Investment',
                                'MarketableSecurities',
                            ]
                            b = [
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'Investments')
                        r = r + 1
                    tb.Investments = sum(Investments)
                except:
                    pass
                #
                # property plant and equipments
                try:
                    PropertyPlantAndEquipment = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r > CurrentAssetsRank:
                            d = key
                            q = [
                                'Property',
                            ]
                            b = [
                                'UnderCapitalLease',
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
                                            PropertyPlantAndEquipment.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'PropertyPlantAndEquipment')
                        r = r + 1
                    tb.PropertyPlantAndEquipment = sum(PropertyPlantAndEquipment)
                except:
                    pass
                #
                # operating lease right of use assets
                try:
                    OperatingLeaseRightOfUseAssets = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r > CurrentAssetsRank:
                            d = key
                            q = [
                                'OperatingLease',
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
                                            OperatingLeaseRightOfUseAssets.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'OperatingLeaseRightOfUseAssets')
                        r = r + 1
                    tb.OperatingLeaseRightOfUseAssets = sum(OperatingLeaseRightOfUseAssets)
                except:
                    pass
                #
                # finance lease right of use assets
                try:
                    FinanceLeaseRightOfUseAssets = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r > CurrentAssetsRank:
                            d = key
                            q = [
                                'FinanceLease',
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
                                            FinanceLeaseRightOfUseAssets.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'FinanceLeaseRightOfUseAssets')
                        r = r + 1
                    tb.FinanceLeaseRightOfUseAssets = sum(FinanceLeaseRightOfUseAssets)
                except:
                    pass
                #
                # property under capital lease and financing obligations
                try:
                    PropertyUnderCapitalLeaseAndFinancingObligations = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r > CurrentAssetsRank:
                            d = key
                            q = [
                                'PropertyUnderCapitalLease',
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
                                            PropertyUnderCapitalLeaseAndFinancingObligations.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'PropertyUnderCapitalLeaseAndFinancingObligations')
                        r = r + 1
                    tb.PropertyUnderCapitalLeaseAndFinancingObligations = sum(PropertyUnderCapitalLeaseAndFinancingObligations)
                except:
                    pass
                #
                # intangible assets
                try:
                    IntangibleAssets = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r > CurrentAssetsRank:
                            d = key
                            q = [
                                'Intangible',
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'IntangibleAssets')
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'Goodwill')
                        r = r + 1
                    tb.Goodwill = sum(Goodwill)
                except:
                    pass
                #
                # deferred tax assets non current
                try:
                    DeferredTaxAssetsNonCurrent = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r > CurrentAssetsRank:
                            d = key
                            q = [
                                'DeferredTaxAssets',
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'DeferredTaxAssetsNonCurrent')
                        r = r + 1
                    tb.DeferredTaxAssetsNonCurrent = sum(DeferredTaxAssetsNonCurrent)
                except:
                    pass
                #
                # other non-current assets
                try:
                    OtherNonCurrentAssets = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r > CurrentAssetsRank:
                            d = key
                            q = [
                                'OtherAssetsNoncurrent',
                                'OtherLongTermAsset',
                                'OtherNonCurrentAsset',
                                'OtherNoncurrentAsset',
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
                                            OtherNonCurrentAssets.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'OtherNonCurrentAssets')
                        r = r + 1
                    tb.OtherNonCurrentAssets = sum(OtherNonCurrentAssets)
                except:
                    pass
                #
                print('\n' * 3)
                #
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
                            'Liabilit',
                            'Operating',
                            'Other'
                            'Property',
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
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'TotalAssets')
                    r = r + 1
                a.Assets = sum(TotalAssets)
                #
                # total asset not null
                try:
                    if a.NonCurrentAssets == 0:
                        a.NonCurrentAssets = a.Assets - a.CurrentAssets
                except:
                    pass
                #
                print(137*'-')
                print('\n' * 3)
            except:
                pass
            #
            # current liabilities
            try:
                print('current liabilities')
                print(137*'-')
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'CurrentLiabilities')
                                            CurrentLiabilitiesRank = r
                        r = r + 1
                    a.CurrentLiabilities = -sum(CurrentLiabilities)
                except:
                    pass
                #
                print('\n')
                #
                # accounts payable and accrued liabilities
                try:
                    AccountsPayableAndAccruedLiabilities = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r < CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'Accrued',
                                'Payable',
                                'SalesRebatesAndDiscounts',
                            ]
                            b = [
                                'Deferred',
                                'Employee',
                                'Tax',
                                'Dividend',
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
                                            AccountsPayableAndAccruedLiabilities.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'AccountsPayableAndAccruedLiabilities')
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
                        if r < CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'EmployeeCompensation',
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
                                            EmployeeCompensationCurrent.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'EmployeeCompensationCurrent')
                        r = r + 1
                    tb.EmployeeCompensationCurrent = -sum(EmployeeCompensationCurrent)
                except:
                    pass
                #
                # operating leases current
                try:
                    OperatingLeasesCurrent = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r < CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'OperatingLeaseLiabilit',
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'OperatingLeasesCurrent')
                        r = r + 1
                    tb.OperatingLeasesCurrent = -sum(OperatingLeasesCurrent)
                except:
                    pass
                #
                # finance leases current
                try:
                    FinanceLeasesCurrent = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r < CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'FinanceLeaseObligation',
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'FinanceLeasesCurrent')
                        r = r + 1
                    tb.FinanceLeasesCurrent = -sum(FinanceLeasesCurrent)
                except:
                    pass
                #
                # capital lease and financing obligations current
                try:
                    CapitalLeaseAndFinancingObligationsCurrent = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r < CurrentLiabilitiesRank:
                            d = key
                            q = [
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
                                            CapitalLeaseAndFinancingObligationsCurrent.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'CapitalLeaseAndFinancingObligationsCurrent')
                        r = r + 1
                    tb.CapitalLeaseAndFinancingObligationsCurrent = -sum(CapitalLeaseAndFinancingObligationsCurrent)
                except:
                    pass
                #
                # deferred revenue and deposits current
                try:
                    DeferredRevenueAndDepositsCurrent = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r < CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'ContractWithCustomerLiabilit',
                                'DeferredRevenue',
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'DeferredRevenueAndDepositsCurrent')
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
                        if r < CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'IncomeTaxes',
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'AccruedTaxLiabilities')
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
                        if r < CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'DeferredIncomeTax',
                                'DeferredTax'
                            ]
                            b = [
                                'Accrued',
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'DeferredTaxLiabilitiesCurrent')
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'CommercialPapers')
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
                        if r < CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'ShortTermBorrowings',
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'ShortTermBorrowings')
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
                        if r < CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'OtherCurrentLiabilit',
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'OtherCurrentLiabilities')
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
                        if r < CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'CurrentLiabilitiesOfDiscontinuedOperation',
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'DiscontinuedOperationsLiabilitiesCurrent')
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'DividendsPayable')
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
                        if r < CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'TermDebt',
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'ShortTermPortionOfLongTermDebt')
                        r = r + 1
                    tb.ShortTermPortionOfLongTermDebt = -sum(ShortTermPortionOfLongTermDebt)
                except:
                    pass
                #
                print('\n' * 3)
                #
            except:
                pass
            #
            # non-current liabilities
            try:
                #
                print('non-current liabilities')
                print(137*'-')
                #
                # total non-current liabilities
                try:
                    TotalNonCurrentLiabilities = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r > CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'LiabilitiesNoncurrent',
                                'NonCurrentLiabilities',
                                'TotalOtherLiabilities',
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
                                            TotalNonCurrentLiabilities.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'TotalNonCurrentLiabilities')
                        r = r + 1
                    a.NonCurrentLiabilities = -sum(TotalNonCurrentLiabilities)
                except:
                    pass
                #
                print('\n')
                #
                # long-term debt
                try:
                    LongTermDebt = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r > CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'TermDebt',
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
                                            LongTermDebt.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'LongTermDebt')
                        r = r + 1
                    tb.LongTermDebt = -sum(LongTermDebt)
                except:
                    pass
                #
                # retirement benefits
                try:
                    RetirementBenefits = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r > CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'AccruedRetirementBenefits',
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'RetirementBenefits')
                        r = r + 1
                    tb.RetirementBenefits = -sum(RetirementBenefits)
                except:
                    pass
                #
                # operating leases non-current
                try:
                    OperatingLeasesNonCurrent = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r > CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'OperatingLeaseObligation',
                                'OperatingLeaseLiabilit',
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
                                            OperatingLeasesNonCurrent.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'OperatingLeasesNonCurrent')
                        r = r + 1
                    tb.OperatingLeasesNonCurrent = -sum(OperatingLeasesNonCurrent)
                except:
                    pass
                #
                # finance leases non-current
                try:
                    FinanceLeasesNonCurrent = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r > CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'FinanceLeaseObligation',
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
                                            FinanceLeasesNonCurrent.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'FinanceLeasesNonCurrent')
                        r = r + 1
                    tb.FinanceLeasesNonCurrent = -sum(FinanceLeasesNonCurrent)
                except:
                    pass
                #
                # capital leases and financing obligations non-current
                try:
                    CapitalLeaseAndFinancingObligationsNonCurrent = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r > CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'CapitalLease',
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
                                            CapitalLeaseAndFinancingObligationsNonCurrent.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'CapitalLeaseAndFinancingObligationsNonCurrent')
                        r = r + 1
                    tb.CapitalLeaseAndFinancingObligationsNonCurrent = -sum(CapitalLeaseAndFinancingObligationsNonCurrent)
                except:
                    pass
                #
                # deferred revenue and deposits non-current
                try:
                    DeferredRevenueAndDepositsNonCurrent = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r > CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'DeferredRevenue',
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'DeferredRevenueAndDepositsNonCurrent')
                        r = r + 1
                    tb.DeferredRevenueAndDepositsNonCurrent = -sum(DeferredRevenueAndDepositsNonCurrent)
                except:
                    pass
                #
                # Accrued Tax Liabilities Non Current
                try:
                    AccruedTaxLiabilitiesNonCurrent = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r > CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'IncomeTaxesPayable',
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
                                            AccruedTaxLiabilitiesNonCurrent.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'AccruedTaxLiabilitiesNonCurrent')
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
                            d = key
                            q = [
                                'DeferredIncomeTax',
                                'DeferredTaxLiabilit',
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'DeferredTaxLiabilitiesNonCurrent')
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
                            d = key
                            q = [
                                'OtherLiabilitiesNoncurrent',
                                'OtherLiabilitiesNonCurrent',
                                'OtherNonCurrentLiabilit',
                                'OtherNoncurrentLiabilit',
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'OtherNonCurrentLiabilities')
                        r = r + 1
                    tb.OtherNonCurrentLiabilities = -sum(OtherNonCurrentLiabilities)
                except:
                    pass
                #
                # discontinued operation non current liabilities
                try:
                    DiscontinuedOperationsLiabilitiesNonCurrent = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r > CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'NoncurrentLiabilitiesOfDiscontinuedOperations',
                                'NonCurrentLiabilitiesOfDiscontinuedOperations',
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'DiscontinuedOperationsLiabilitiesNonCurrent')
                        r = r + 1
                    tb.DiscontinuedOperationsLiabilitiesNonCurrent = -sum(DiscontinuedOperationsLiabilitiesNonCurrent)
                except:
                    pass
                #
                print('\n' * 3)
                #
            except:
                pass
            #
            # total liabilities
            try:
                print(137*'-')
                TotalLiabilities = []
                r = 0
                for key, value in BalanceSheet.items():
                    if r > CurrentLiabilitiesRank:
                        d = key
                        q = [
                            'Liabilit',
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
                                        TotalLiabilities.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'TotalLiabilities')
                        r = r + 1
                a.Liabilities = -sum(TotalLiabilities)
                #
                print(137*'-' + '\n' * 3)
            except:
                pass
            #
            # shareholders' equity
            try:
                print('shareholders equity')
                print(137*'-')
                #
                # common shares
                try:
                    CommonShares = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r > CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'AdditionalPaidInCapital',
                                'CommonStock',
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
                                            if value != None:
                                                ARCHvalue = BalanceSheet[key]
                                                BalanceSheet[key] = None
                                            else:
                                                ARCHvalue = 0
                                        if ARCHvalue != 0:
                                            CommonShares.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'CommonShares')
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
                        if r > CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'RetainedEarning',
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
                                            RetainedEarnings.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'RetainedEarnings')
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
                        if r > CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'AccumulatedOtherComprehensive',
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'AccumulatedOtherComprehensiveIncome')
                        r = r + 1
                    a.AccumulatedOtherComprehensiveIncome = -sum(AccumulatedOtherComprehensiveIncome)
                except:
                    pass
                #
                # employee benefit trust
                try:
                    EmployeeBenefitTrust = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r > CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'EmployeeBenefitTrust',
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'EmployeeBenefitTrust')
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
                        if r > CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'NoncontrollingInterests',
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
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'NonControllingInterests')
                        r = r + 1
                    a.NonControllingInterests = -sum(NonControllingInterests)
                except:
                    pass
                #
                # stockholders equity
                try:
                    StockholdersEquity = []
                    r = 0
                    for key, value in BalanceSheet.items():
                        if r > CurrentLiabilitiesRank:
                            d = key
                            q = [
                                'TotalEquity',
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
                                            StockholdersEquity.append(ARCHvalue)
                                            print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'StockholdersEquity')
                        r = r + 1
                    a.StockholdersEquity = -sum(StockholdersEquity)
                except:
                    pass
                #
                print('\n' * 3)
                #
            except:
                pass
            #
            print(137*'-')
            #
            # total liabilities and stockholders' equity
            try:
                LiabilitiesAndStockholdersEquity = []
                r = 0
                for key, value in BalanceSheet.items():
                    if r > CurrentLiabilitiesRank:
                        d = key
                        q = [
                            'LiabilitiesAndStockholder',
                            'LiabilitiesAndEquity',
                            'LiabilitiesAndShareholder',
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
                                        LiabilitiesAndStockholdersEquity.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'LiabilitiesAndStockholdersEquity')
                        r = r + 1
                a.LiabilitiesAndStockholdersEquity = -sum(LiabilitiesAndStockholdersEquity)
            except:
                pass
            #
            print(137*'-' + '\n' * 3)
            #
            #
            # income statement
            print('income statement')
            print(137*'-')
            #
            # sales
            try:
                Sales = []
                r = 0
                for key, value in IncomeStatement.items():
                    d = key
                    q = [
                        'Membership',
                        'NetSales',
                        'Revenue',
                        'RevenueFromContractWithCustomer',
                        'SalesofMachineryEnergyTransportation',
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
                                    Sales.append(ARCHvalue)
                                    print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'Sales')
                        r = r + 1
                tb.Sales = -sum(Sales)
            except:
                pass
            #
            # cost of sales
            try:
                CostOfSales = []
                r = 0
                for key, value in IncomeStatement.items():
                    d = key
                    q = [
                        'CostOfGoods',
                        'CostOfRevenue',
                        'CostOfSales',
                    ]
                    b = [
                        'DiscontinuedOperation',
                        'CostOfSalesOperatingExpensesAndOtherNet',
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
                                    CostOfSales.append(ARCHvalue)
                                    print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'CostOfSales')
                        r = r + 1
                tb.CostOfSales = sum(CostOfSales)
            except:
                pass
            #
            # gross margin
            try:
                GrossMargin = []
                r = 0
                for key, value in IncomeStatement.items():
                    d = key
                    q = [
                        'GrossMargin',
                        'GrossProfit',
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
                                    print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'GrossMargin')
                        r = r + 1
                a.GrossMargin = -sum(GrossMargin)
            except:
                pass
            #
            # research and development
            try:
                ResearchAndDevelopment = []
                r = 0
                for key, value in IncomeStatement.items():
                    d = key
                    q = [
                        'ResearchAndDevelopment',
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
                                    print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'ResearchAndDevelopment')
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
                    d = key
                    q = [
                        'GeneralAndAdministrative',
                        'OtherOperatingExpenses',
                        'OtherOperatingIncomeExpenses',
                        'SellingAndAdministrative',
                        'SellingAndMarketing',
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
                                        ARCHvalue = IncomeStatement[key]
                                        IncomeStatement[key] = None
                                    else:
                                        ARCHvalue = 0
                                if ARCHvalue != 0:
                                    SellingGeneralAdministrativeAndMarketing.append(ARCHvalue)
                                    print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'SellingGeneralAdministrativeAndMarketing')
                        r = r + 1
                tb.SellingGeneralAdministrativeAndMarketing = sum(SellingGeneralAdministrativeAndMarketing)
            except:
                pass
            #
            # total operating expense
            try:
                OperatingExpenses = []
                r = 0
                for key, value in IncomeStatement.items():
                    d = key
                    q = [
                        'CostsAndExpenses',
                        'OperatingExpenses',
                        'TotalOperatingCosts',
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
                                    OperatingExpenses.append(ARCHvalue)
                                    print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'OperatingExpenses')
                        r = r + 1
                a.OperatingExpenses = sum(OperatingExpenses)
            except:
                pass
            #
            # total operating income
            try:
                OperatingIncome = []
                r = 0
                for key, value in IncomeStatement.items():
                    d = key
                    q = [
                        'OperatingIncome',
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
                                        ARCHvalue = IncomeStatement[key]
                                        IncomeStatement[key] = None
                                    else:
                                        ARCHvalue = 0
                                if ARCHvalue != 0:
                                    OperatingIncome.append(ARCHvalue)
                                    print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'OperatingIncome')
                        r = r + 1
                a.OperatingIncome = -sum(OperatingIncome)
            except:
                pass
            #
            # Asset Impairment, restructuring, and other special charges
            try:
                ImpairmentRestructuringAndOtherSpecialCharges = []
                r = 0
                for key, value in IncomeStatement.items():
                    d = key
                    q = [
                        'AssetImpairmentRestructuringAndOtherSpecialCharges',
                        'GoodwillImpairmentCharge',
                        'LossOnExtinguishmentOfDebt',
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
                                        ARCHvalue = IncomeStatement[key]
                                        IncomeStatement[key] = None
                                    else:
                                        ARCHvalue = 0
                                if ARCHvalue != 0:
                                    ImpairmentRestructuringAndOtherSpecialCharges.append(ARCHvalue)
                                    print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'ImpairmentRestructuringAndOtherSpecialCharges')
                        r = r + 1
                tb.ImpairmentRestructuringAndOtherSpecialCharges = sum(ImpairmentRestructuringAndOtherSpecialCharges)
            except:
                pass
            #
            # non-operating income (expense)
            try:
                NonOperatingIncome = []
                r = 0
                for key, value in IncomeStatement.items():
                    d = key
                    q = [
                        'OtherNetIncomeExpense',
                    ]
                    b = [
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
                                    NonOperatingIncome.append(ARCHvalue)
                                    print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'NonOperatingIncome')
                        r = r + 1
                tb.NonOperatingIncome = -sum(NonOperatingIncome)
            except:
                pass
            #
            # income before taxes
            try:
                IncomeBeforeTaxes = []
                r = 0
                for key, value in IncomeStatement.items():
                    d = key
                    q = [
                        'IncomeBeforeIncomeTax',
                        'IncomeBeforeProvisionForIncomeTax',
                        'IncomeLossFromContinuingOperationsBeforeIncomeTax',
                        'ProfitBeforeTax',
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
                                    print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'IncomeBeforeTaxes')
                        r = r + 1
                a.IncomeBeforeTaxes = -sum(IncomeBeforeTaxes)
            except:
                pass
            #
            # income tax expense benefit
            try:
                IncomeTaxExpenseBenefit = []
                r = 0
                for key, value in IncomeStatement.items():
                    d = key
                    q = [
                        'IncomeTaxes',
                        'IncomeTaxExpenseBenefit',
                        'ProvisionBenefitForIncomeTaxes',
                        'ProvisionForIncomeTaxes',
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
                                        ARCHvalue = IncomeStatement[key]
                                        IncomeStatement[key] = None
                                    else:
                                        ARCHvalue = 0
                                if ARCHvalue != 0:
                                    IncomeTaxExpenseBenefit.append(ARCHvalue)
                                    print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'IncomeTaxExpenseBenefit')
                        r = r + 1
                tb.IncomeTaxExpenseBenefit = sum(IncomeTaxExpenseBenefit)
            except:
                pass
            #
            # net Income From Discontinued Operations
            try:
                NetIncomeFromDiscontinuedOperations = []
                r = 0
                for key, value in IncomeStatement.items():
                    d = key
                    q = [
                        'LossFromDiscontinuedOperation',
                        'IncomeFromDiscontinuedOperation',
                        'Income(Loss)FromDiscontinuedOperation',
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
                                    print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'NetIncomeFromDiscontinuedOperations')
                        r = r + 1
                tb.NetIncomeFromDiscontinuedOperations = -sum(NetIncomeFromDiscontinuedOperations)
            except:
                pass
            #
            # net income
            try:
                NetIncome = []
                r = 0
                for key, value in IncomeStatement.items():
                    d = key
                    q = [
                        'Loss',
                        'NetIncome',
                    ]
                    b = [
                        'ContinuingOperations',
                        'CostOfGoods',
                        'CostOfOperations',
                        'CostOfRevenue',
                        'CostOfSales',
                        'DiscontinuedOperation',
                        'Gain',
                        'Other',
                        'PerShare',
                        'Research',
                        'Revenue',
                        'Sales',
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
                                    print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'NetIncome')
                        r = r + 1
                a.NetIncome = -sum(NetIncome)
            except:
                pass
            #
            print('\n' * 3)
            #
            #
            # comprehensive income
            print('other comprehensive income')
            print(137*'-')
            #
            try:
                #
                # foreign currency translation
                try:
                    ChangeInForeignCurrencyTranslationAdjustment = []
                    r = 0
                    for key, value in ComprehensiveIncomeStatement.items():
                        d = key
                        q = [
                            'ForeignCurrencyTransaction',
                            'CurrencyTranslation',
                            'ForeignCurrencyTranslation',
                        ]
                        b = [
                            'ContinuingOperations',
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
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'ChangeInForeignCurrencyTranslationAdjustment')
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
                        d = key
                        q = [
                            'CashFlowHedge',
                            'Derivatives',
                            'NetGains(Losses)RealizedAndIncludedInNetIncome',
                            'NetInvestmentHedges',
                        ]
                        b = [
                            'ContinuingOperations',
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
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'ChangeInUnrealizedGainsLossesOnDerivativeInstruments')
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
                        d = key
                        q = [
                            'ChangeInNetUnrealizedGains(Losses)OnSecurities',
                            'ChangeInNetUnrealizedGainsAndLossesOnSecurities',
                            'MarketableDebtSecurities',
                            'MarketableSecurities',
                            'NetGains(Losses)RealizedAndIncludedInNetIncome',
                            'SecuritiesAdjustment',
                            'UnrealizedGainOnSecurities',
                            'UnrealizedHoldingGain(Loss)OnSecurities',
                        ]
                        b = [
                            'ContinuingOperations',
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
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'ChangeInUnrealizedGainsLossesOnInvestments')
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
                        d = key
                        q = [
                            'ChangeInDefinedBenefitPensionAndRetireeHealthBenefitPlans',
                        ]
                        b = [
                            'ContinuingOperations',
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
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'ChangeInDefinedBenefitPensionAndOtherSimilarPlans')
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
                        d = key
                        q = [
                            'Benefit(Provision)ForIncomeTaxesRelatedToOtherComprehensiveIncome',
                        ]
                        b = [
                            'ChangeIn',
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
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'IncomeTaxOnOtherComprehensiveIncome')
                        r = r + 1
                    tb.IncomeTaxOnOtherComprehensiveIncome = -sum(IncomeTaxOnOtherComprehensiveIncome)
                except:
                    pass
                #
                # comprehensive income
                try:
                    ComprehensiveIncome = []
                    r = 0
                    for key, value in ComprehensiveIncomeStatement.items():
                        d = key
                        q = [
                            'ComprehensiveIncome',
                        ]
                        b = [
                            'ContinuingOperations',
                            'NetOtherComprehensiveIncome',
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
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'ComprehensiveIncome')
                        r = r + 1
                    #
                    a.ComprehensiveIncome = -sum(ComprehensiveIncome)
                    #
                    a.OtherComprehensiveIncome = a.ComprehensiveIncome - a.NetIncome
                except:
                    pass
            except:
                pass
            #
            print('\n' * 3)
            #
            # stockholders equity
            print("stockholders equity")
            print(137*'-')
            #
            try:
                #
                # common stock issued
                try:
                    CommonStockIssued = []
                    r = 0
                    for key, value in ComprehensiveIncomeStatement.items():
                        d = key
                        q = [
                            'CommonStockIssued',
                            'IssuanceOfStockUnderEmployeeStockPlan',
                            'PurchaseOfTreasurySharesValue',
                            'StockIssuedDuringPeriodValue',
                        ]
                        b = [
                            'Retirement',
                            'Repurchase',
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
                                    try:
                                        i = len(value) - 1
                                        while StockholdersEquityStatement[key][i] == None:
                                            i = i - 1
                                        ARCHvalue = StockholdersEquityStatement[key][i]
                                        StockholdersEquityStatement[key][i] = None
                                    except:
                                        if StockholdersEquityStatement[key] != None:
                                            ARCHvalue = StockholdersEquityStatement[key]
                                            StockholdersEquityStatement[key] = None
                                        else:
                                            ARCHvalue = 0
                                    if ARCHvalue != 0:
                                        CommonStockIssued.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'CommonStockIssued')
                        r = r + 1
                    tb.CommonStockIssued = -sum(CommonStockIssued)
                except:
                    pass
                #
                # share based compensation and other stockholders equity components
                try:
                    ShareBasedCompensation = []
                    r = 0
                    for key, value in StockholdersEquityStatement.items():
                        d = key
                        q = [
                            'ShareBasedCompensation',
                        ]
                        b = [
                            'Retirement',
                            'Repurchase',
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
                                    try:
                                        i = len(value) - 1
                                        while StockholdersEquityStatement[key][i] == None:
                                            i = i - 1
                                        ARCHvalue = StockholdersEquityStatement[key][i]
                                        StockholdersEquityStatement[key][i] = None
                                    except:
                                        if StockholdersEquityStatement[key] != None:
                                            ARCHvalue = StockholdersEquityStatement[key]
                                            StockholdersEquityStatement[key] = None
                                        else:
                                            ARCHvalue = 0
                                    if ARCHvalue != 0:
                                        ShareBasedCompensation.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'ShareBasedCompensation')
                    tb.ShareBasedCompensation = -sum(ShareBasedCompensation)
                except:
                    pass
                #
                # dividends and dividend equivalents declared
                try:
                    DividendsAndDividendEquivalentsDeclared = []
                    r = 0
                    for key, value in StockholdersEquityStatement.items():
                        d = key
                        q = [
                            'Dividends',
                        ]
                        b = [
                            'Retirement',
                            'Repurchase',
                            'NoncontrollingInterest',
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
                                    try:
                                        i = len(value) - 1
                                        while StockholdersEquityStatement[key][i] == None:
                                            i = i - 1
                                        ARCHvalue = StockholdersEquityStatement[key][i]
                                        StockholdersEquityStatement[key][i] = None
                                    except:
                                        if StockholdersEquityStatement[key] != None:
                                            ARCHvalue = StockholdersEquityStatement[key]
                                            StockholdersEquityStatement[key] = None
                                        else:
                                            ARCHvalue = 0
                                    if ARCHvalue != 0:
                                        DividendsAndDividendEquivalentsDeclared.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'DividendsAndDividendEquivalentsDeclared')
                        r = r + 1
                    tb.DividendsAndDividendEquivalentsDeclared = -sum(DividendsAndDividendEquivalentsDeclared)
                except:
                    pass
                #
                #
                # dividends and dividend equivalents declared to non controlling interests
                try:
                    DividendsDeclaredToNonControllingInterests = []
                    r = 0
                    for key, value in StockholdersEquityStatement.items():
                        d = key
                        q = [
                            'DividendsAndDividendEquivalentsDeclaredToNoncontrollingInterest',
                        ]
                        b = [
                            'Retirement',
                            'Repurchase',
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
                                    try:
                                        i = len(value) - 1
                                        while StockholdersEquityStatement[key][i] == None:
                                            i = i - 1
                                        ARCHvalue = StockholdersEquityStatement[key][i]
                                        StockholdersEquityStatement[key][i] = None
                                    except:
                                        if StockholdersEquityStatement[key] != None:
                                            ARCHvalue = StockholdersEquityStatement[key]
                                            StockholdersEquityStatement[key] = None
                                        else:
                                            ARCHvalue = 0
                                    if ARCHvalue != 0:
                                        DividendsDeclaredToNonControllingInterests.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'DividendsDeclaredToNonControllingInterests')
                        r = r + 1
                    tb.DividendsDeclaredToNonControllingInterests = -sum(DividendsDeclaredToNonControllingInterests)
                except:
                    pass
                #
                # common stock repurchased and retired
                try:
                    CommonStockRepurchasedAndRetired = []
                    r = 0
                    for key, value in StockholdersEquityStatement.items():
                        d = key
                        q = [
                            'AcquisitionOfCommonStockInExchangeOffer',
                            'CommonStockRepurchased',
                            'PurchaseOfCompanyStock',
                            'PurchaseOfTreasuryShares',
                            'RepurchasesOfCommonStock',
                            'RepurchaseOfCommonStock',
                            'StockRepurchased',
                            'RetirementOfTreasurySharesValue',
                        ]
                        b = [
                            'Dividend',
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
                                    try:
                                        i = len(value) - 1
                                        while StockholdersEquityStatement[key][i] == None:
                                            i = i - 1
                                        ARCHvalue = StockholdersEquityStatement[key][i]
                                        StockholdersEquityStatement[key][i] = None
                                    except:
                                        if StockholdersEquityStatement[key] != None:
                                            ARCHvalue = StockholdersEquityStatement[key]
                                            StockholdersEquityStatement[key] = None
                                        else:
                                            ARCHvalue = 0
                                    if ARCHvalue != 0:
                                        CommonStockRepurchasedAndRetired.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'CommonStockRepurchasedAndRetired')
                        r = r + 1
                    tb.CommonStockRepurchasedAndRetired = -sum(CommonStockRepurchasedAndRetired)
                except:
                    pass
                #
                # effect of adoption of new accounting pronouncement or tax cuts
                try:
                    EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts = []
                    r = 0
                    for key, value in StockholdersEquityStatement.items():
                        d = key
                        q = [
                            'AdoptionOfNewAccountingStandardsNetOfIncomeTaxes',
                            'CumulativeEffectOfChangeInAccountingPrinciple',
                            'ReclassificationOfStrandedTaxEffectsAndAdoptionOfNewAccountingStandards',
                            'ReclassificationOfStrandedTaxEffectsProvisional',
                        ]
                        b = [
                            'Dividend',
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
                                    try:
                                        i = len(value) - 1
                                        while StockholdersEquityStatement[key][i] == None:
                                            i = i - 1
                                        ARCHvalue = StockholdersEquityStatement[key][i]
                                        StockholdersEquityStatement[key][i] = None
                                    except:
                                        if StockholdersEquityStatement[key] != None:
                                            ARCHvalue = StockholdersEquityStatement[key]
                                            StockholdersEquityStatement[key] = None
                                        else:
                                            ARCHvalue = 0
                                    if ARCHvalue != 0:
                                        EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts')
                        r = r + 1
                    tb.EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts = sum(EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts)
                except:
                    pass
                #
                print('\n' * 3)
                #
            except:
                pass
            #
            print('cash flow')
            #
            # cash beginning balance
            print(137*'-')
            try:
                CashBeginningBalance = []
                r = 0
                for key, value in CashFlowStatement.items():
                    d = key
                    q = [
                        'CashBeginning',
                        'CashAtBeginning',
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
                                    CashBeginningBalance.append(ARCHvalue)
                                    print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'CashBeginningBalance')
                    r = r + 1
                cf.CashBeginningBalance = sum(CashBeginningBalance)
            except:
                pass
            print('\n' * 3)
            #
            # effect of exchange rate on cash
            try:
                EffectOfExchangeRateOnCash = []
                r = 0
                for key, value in CashFlowStatement.items():
                    d = key
                    q = [
                        'EffectOfExchange',
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
                                    print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'EffectOfExchangeRateOnCash')
                    r = r + 1
                cf.EffectOfExchangeRateOnCash = sum(EffectOfExchangeRateOnCash)
            except:
                pass
            print('\n' * 3)
            #
            # operating activities
            try:
                print('operating activities')
                print(137*'-')
                #
                # depreciation depletion and amortization
                try:
                    DepreciationDepletionAndAmortization = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'DepreciationAndAmortization',
                            'DepreciationDepletionAndAmortization',
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
                                        DepreciationDepletionAndAmortization.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'DepreciationDepletionAndAmortization')
                        r = r + 1
                    cf.DepreciationDepletionAndAmortization = sum(DepreciationDepletionAndAmortization)
                except:
                    pass
                #
                # Gain Related To Disposal Or Sale
                try:
                    GainRelatedToDisposalOrSale = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'GainRelatedToDisposalOrSale',
                        ]
                        b = [
                            'Acquire',
                            'Acquisition',
                            'Decrease',
                            'DiscontinuedOperation',
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
                                        GainRelatedToDisposalOrSale.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'GainRelatedToDisposalOrSale')
                        r = r + 1
                    cf.GainRelatedToDisposalOrSale = sum(GainRelatedToDisposalOrSale)
                except:
                    pass
                #
                # share based compensation
                try:
                    ShareBasedCompensation = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'ShareBasedCompensation',
                            'StockBasedCompensation',
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
                                        ShareBasedCompensation.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'ShareBasedCompensation')
                        r = r + 1
                    cf.ShareBasedCompensation = sum(ShareBasedCompensation)
                except:
                    pass
                #
                # deferred income tax expense (benefit)
                try:
                    DeferredIncomeTaxExpenseBenefit = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'DeferredIncomeTax',
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
                                        DeferredIncomeTaxExpenseBenefit.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'DeferredIncomeTaxExpenseBenefit')
                        r = r + 1
                    cf.DeferredIncomeTaxExpenseBenefit = sum(DeferredIncomeTaxExpenseBenefit)
                except:
                    pass
                #
                # other non cash income expense
                try:
                    OtherNonCashIncomeExpense = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'OtherNoncashIncomeExpense',
                        ]
                        b = [
                            'Amortization',
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
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'OtherNonCashIncomeExpense')
                        r = r + 1
                    cf.OtherNonCashIncomeExpense = -sum(OtherNonCashIncomeExpense)
                except:
                    pass
                #
                # increase (decrease) in accounts receivable
                try:
                    IncreaseDecreaseInAccountsReceivable = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'Receivable',
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
                                        IncreaseDecreaseInAccountsReceivable.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'IncreaseDecreaseInAccountsReceivable')
                        r = r + 1
                    cf.IncreaseDecreaseInAccountsReceivable = sum(IncreaseDecreaseInAccountsReceivable)
                except:
                    pass
                #
                # increase (decrease) in inventories
                try:
                    IncreaseDecreaseInInventories = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'Inventories',
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
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'IncreaseDecreaseInInventories')
                        r = r + 1
                    cf.IncreaseDecreaseInInventories = -sum(IncreaseDecreaseInInventories)
                except:
                    pass
                #
                # increase (decrease) in other receivables and prepaid expenses
                try:
                    IncreaseDecreaseInOtherReceivables = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'OtherReceivables',
                            'VendorNonTradeReceivables',
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
                                        IncreaseDecreaseInOtherReceivables.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'IncreaseDecreaseInOtherReceivables')
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
                        d = key
                        q = [
                            'AccountPayable',
                            'AccountsPayable',
                            'AccruedLiabilit',
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
                                        IncreaseDecreaseInAccountsPayableAndAccruedLiabilities.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'IncreaseDecreaseInAccountsPayableAndAccruedLiabilities')
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
                        d = key
                        q = [
                            'ContractWithCustomerLiability',
                            'DeferredRevenue',
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
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'IncreaseDecreaseInContractWithCustomerLiability')
                        r = r + 1
                    cf.IncreaseDecreaseInContractWithCustomerLiability = sum(IncreaseDecreaseInContractWithCustomerLiability)
                except:
                    pass
                #
                # increase (decrease) in other operating activities
                try:
                    IncreaseDecreaseInOtherOperatingActivities = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'AccountsPayableAndOtherLiabiltiesIncrease(Decrease)',
                            'OtherCurrentAndNonCurrentAssets',
                            'OtherCurrentAndNonCurrentLiabilities',
                            'OtherNoncurrentLiabilities',
                            'OtherOperatingAssets',
                            'OtherOperatingLiabilities',
                            'OtherAssets(Increase)Decrease',
                            'NetProceedsFrom(PaymentsFor)TerminationsOfInterestRateSwaps',
                            'OtherNonCashOperatingActivities',
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
                                        IncreaseDecreaseInOtherOperatingActivities.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'IncreaseDecreaseInOtherOperatingActivities')
                        r = r + 1
                    cf.IncreaseDecreaseInOtherOperatingActivities = sum(IncreaseDecreaseInOtherOperatingActivities)
                except:
                    pass
                #
                # total operating activities
                try:
                    OperatingActivities = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'OperatingActivities',
                        ]
                        b = [
                            'InvestingActivities',
                            'FinancingActivities',
                            'OtherNonCashOperatingActivities',
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
                                        OperatingActivities.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'OperatingActivities')
                        r = r + 1
                    a.OperatingActivities = sum(OperatingActivities)
                    print('\n' * 3)
                except:
                    pass
            except:
                pass
            #
            # investing activities
            try:
                print('investing activities')
                print(137*'-')
                #
                # Payments To Acquire Investment
                try:
                    PaymentsToAcquireInvestments = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'Investments',
                            'MarketableSecurities',
                            'OtherInvestments',
                            'SecuritiesDebt',
                            'ShortTermInvestments',
                        ]
                        b = [
                            'Proceeds',
                            'Disposal',
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
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'PaymentsToAcquireInvestments')
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
                        d = key
                        q = [
                            'ProceedsFromMaturitiesOfMarketableSecurities',
                            'ProceedsFromMaturitiesPrepaymentsAndCallsOfSecurities',
                            'ProceedsFromNonMarketableSecurities',
                            'ProceedsFromSaleAndMaturityOfOtherInvestments',
                            'ProceedsFromSaleOfAvailableForSaleSecuritiesDebt',
                            'ProceedsFromSalesAndMaturitiesOfShortTermInvestments',
                            'ProceedsFromSalesOfMarketableSecurities',
                            'ProceedsFromSalesOfNoncurrentInvestments',
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
                                        ProceedsOfInvestments.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'ProceedsOfInvestments')
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
                        d = key
                        q = [
                            'PropertyPlantAndEquipment',
                            'PropertyAndEquipment',
                        ]
                        b = [
                            'Proceed',
                            'Disposal',
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
                                        PaymentsToAcquirePropertyPlantAndEquipment.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'PaymentsToAcquirePropertyPlantAndEquipment')
                        r = r + 1
                    cf.PaymentsToAcquirePropertyPlantAndEquipment = sum(PaymentsToAcquirePropertyPlantAndEquipment)
                except:
                    pass
                #
                # Proceeds From Disposal of Property Plant And Equipment
                try:
                    ProceedsFromDisposalsOfPropertyAndEquipment = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'PropertyPlantAndEquipment',
                            'PropertyAndEquipment',
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
                                        ProceedsFromDisposalsOfPropertyAndEquipment.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'ProceedsFromDisposalsOfPropertyAndEquipment')
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
                        d = key
                        q = [
                            'Intangible',
                            'StrategicInvestments',
                            'BusinessAcquisitions'
                            'AcquireBusinesses',
                            'CashPaidForAcquisitions',
                            'ResearchAndDevelopment',
                        ]
                        b = [
                            'Proceed',
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
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'PaymentsToAcquireBusinessesAndIntangibles')
                        r = r + 1
                    cf.PaymentsToAcquireBusinessesAndIntangibles = sum(PaymentsToAcquireBusinessesAndIntangibles)
                except:
                    pass
                #
                # Total Investing Activities
                try:
                    InvestingActivities = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'InvestingActivities',
                        ]
                        b = [
                            'Financing',
                            'Operating',
                            'Other',
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
                                        InvestingActivities.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'InvestingActivities')
                        r = r + 1
                    a.InvestingActivities = sum(InvestingActivities)
                except:
                    pass
                #
                print('\n' * 3)
                #
            except:
                pass
            #
            # financing activities
            try:

                print('financing activities')
                print(137*'-')
                #
                # Finance Lease Principal Payments
                try:
                    FinanceLeasePrincipalPayments = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'FinanceLeasePrincipalPayments',
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
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'FinanceLeasePrincipalPayments')
                        r = r + 1
                    cf.FinanceLeasePrincipalPayments = sum(FinanceLeasePrincipalPayments)
                except:
                    pass        
                #
                # Proceeds From Issuance Of Common Stock
                try:
                    ProceedsFromIssuanceOfCommonStock = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'ProceedsFromIssuanceOfCommonStock',
                        ]
                        b = [
                            'Purchase',
                            'Payment',
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
                                        ProceedsFromIssuanceOfCommonStock.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'ProceedsFromIssuanceOfCommonStock')
                        r = r + 1
                    cf.ProceedsFromIssuanceOfCommonStock = sum(ProceedsFromIssuanceOfCommonStock)
                except:
                    pass
                #
                # Payments Related To Tax Withholding For Share Based Compensation
                try:
                    PaymentsRelatedToTaxWithholdingForShareBasedCompensation = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'PaymentsRelatedToTaxWithholdingForShareBasedCompensation',
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
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'PaymentsRelatedToTaxWithholdingForShareBasedCompensation')
                        r = r + 1
                    cf.PaymentsRelatedToTaxWithholdingForShareBasedCompensation = -sum(PaymentsRelatedToTaxWithholdingForShareBasedCompensation)
                except:
                    pass
                #
                # Payments Of Dividends
                try:
                    PaymentsOfDividends = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'DividendsAndDividendEquivalentsPaid',
                            'DividendsPaid',
                            'PaymentsForDividendsAndDividendEquivalents',
                            'PaymentsOfDividends',
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
                                        PaymentsOfDividends.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'PaymentsOfDividends')
                        r = r + 1
                    cf.PaymentsOfDividends = sum(PaymentsOfDividends)
                except:
                    pass
                #
                # Payments For Repurchase Of Common Stock
                try:
                    PaymentsForRepurchaseOfCommonStock = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'PaymentsForRepurchaseOfCommonStock',
                            'RepurchaseOfCommonStock',
                            'RepurchasesOfCommonStock',
                            'PurchasesOfCommonStock',
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
                                        PaymentsForRepurchaseOfCommonStock.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'PaymentsForRepurchaseOfCommonStock')
                        r = r + 1
                    cf.PaymentsForRepurchaseOfCommonStock = -sum(PaymentsForRepurchaseOfCommonStock)
                except:
                    pass
                #
                # Payments For Taxes Related To Net Share Settlement Of Equity Award
                try:
                    PaymentsForTaxesRelatedToNetShareSettlementOfEquityAward = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'ExcessTaxBenefitsFromEquityAwards',
                            'PaymentsForTaxesRelatedToNetShareSettlementOfEquityAward',
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
                                        PaymentsForTaxesRelatedToNetShareSettlementOfEquityAward.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'PaymentsForTaxesRelatedToNetShareSettlementOfEquityAward')
                        r = r + 1
                    cf.PaymentsForTaxesRelatedToNetShareSettlementOfEquityAward = sum(PaymentsForTaxesRelatedToNetShareSettlementOfEquityAward)
                except:
                    pass
                #
                # Proceeds From Issuance Of Long Term Debt
                try:
                    ProceedsFromIssuanceOfLongTermDebt = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'ProceedsFromIssuanceOfLongTermDebt',
                            'ProceedsFromIssuanceOfTermDebt',
                        ]
                        b = [
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
                                        ProceedsFromIssuanceOfLongTermDebt.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'ProceedsFromIssuanceOfLongTermDebt')
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
                        d = key
                        q = [
                            'RepaymentsOfLongTermDebt',
                            'RepaymentsOfTermDebt',
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
                                        RepaymentsOfLongTermDebt.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'RepaymentsOfLongTermDebt')
                        r = r + 1
                    cf.RepaymentsOfLongTermDebt = sum(RepaymentsOfLongTermDebt)
                except:
                    pass
                #
                # Proceeds From Repayments Of Commercial Paper
                try:
                    ProceedsFromRepaymentsOfCommercialPaper = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'CommercialPaper',
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
                                        ProceedsFromRepaymentsOfCommercialPaper.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'ProceedsFromRepaymentsOfCommercialPaper')
                        r = r + 1
                    cf.ProceedsFromRepaymentsOfCommercialPaper = sum(ProceedsFromRepaymentsOfCommercialPaper)
                except:
                    pass
                #
                # Other Financing Activities
                try:
                    OtherFinancingActivities = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'ProceedsFromPaymentsForOtherFinancingActivities',
                            'NetChangeInShortTermBorrowings',
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
                                        OtherFinancingActivities.append(ARCHvalue)
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'OtherFinancingActivities')
                        r = r + 1
                    cf.OtherFinancingActivities = sum(OtherFinancingActivities)
                except:
                    pass
                #
                # Total Financing Activities
                try:
                    FinancingActivities = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'FinancingActivities',
                        ]
                        b = [
                            'OperatingActivities',
                            'InvestingActivities',
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
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'FinancingActivities')
                        r = r + 1
                    a.FinancingActivities = sum(FinancingActivities)
                    #
                    print('\n' * 3)
                except:
                    pass
                #
                # supplemental cash flow disclosure
                print('supplemental cash flow disclosure')
                print(137*'-' + '\n' * 3)
                #
                # Cash paid for taxes
                try:
                    CashPaidForTaxes = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'CashPaidForIncomeTaxes',
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
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'CashPaidForTaxes')
                        r = r + 1
                    cf.CashPaidForTaxes = sum(CashPaidForTaxes)
                except:
                    pass 
                #
                # Cash paid for in interest
                try:
                    CashPaidForInterest = []
                    r = 0
                    for key, value in CashFlowStatement.items():
                        d = key
                        q = [
                            'Interest',
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
                                        print(key + ': ' + str(ARCHvalue) + ' allocated to ' + 'CashPaidForInterest')
                        r = r + 1
                    cf.CashPaidForInterest = sum(CashPaidForInterest)
                    #
                    print(137*'-' + '\n')
                    #
                except:
                    pass 
                #
                # save
                try:
                    try:
                        tb.save()
                        #
                        print("Trial Balance Saved.")
                    except:
                        pass
                    try:
                        cf.save()
                        #
                        print("Cash Flow Saved.")
                    except:
                        pass
                    try:
                        a.save()
                        #
                        print("Audit Saved.")
                        print(137 * '-' + '\n' * 3)
                    except:
                        pass
                except:
                    pass
            except:
                pass
        except:
            pass
        #
        #
        # number of shares outstanding
        try:
            #
            OutstandingSharesURL = 'https://www.sec.gov/Archives/edgar/data/' + EntityCentralIndexKey + '/' + accessionnumber.replace('-','') + '/' 'R1.htm'
            content = requests.get(OutstandingSharesURL).content
            soup = BeautifulSoup(content, 'html')
            q = soup.find_all('tr')
            p = 0
            while p < len(q) - 1:
                try:
                    d = q[p].find_all('a')[0].text
                    if 'Outstanding' in d:
                        h = p
                except:
                    pass
                p = p + 1
            #
            b = int(q[h].find_all('td', class_='nump')[0].text.replace(',',''))
            #
            # dad
            d = soup.find_all('tr')[0].text
            if 'SHARES IN THOUSANDS' in d.upper():
                dad = 1000
            else:
                dad = 1
            a.EntityCommonStockSharesOutstanding = b * dad
            #
            a.save()
            #
            print('number of shares outstanding: ' + str(a.EntityCommonStockSharesOutstanding))
            print(137*'-' + '\n' * 3)
        except:
            pass
        #
        #
        # stock price
        try:
            if GetStockPrice == 'yes':
                #
                if scopedperiod == 'lastyear':
                    #
                    try:
                        #
                        d = requests.get('https://api.marketstack.com/v1/tickers/' + TradingSymbol + '/eod', params)
                        #
                        p = d.json()['data']['name']
                        q = d.json()['data']['symbol']
                        b = d.json()['data']['eod'][0]['date']
                        d = d.json()['data']['eod'][0]['close']
                        #
                        a.StockPrice = d
                        a.save()
                    except:
                        print('--Could not establish current Stock Price.')
                #
                else:
                    try:
                        q = 0
                        p = ''
                        while q < 9:
                            while p == '':
                                try:
                                    d = datetime.datetime.strptime(tb.FilingDate, '%Y-%m-%d')
                                    d = d - datetime.timedelta(days=q)
                                    d = str(d)[:10]
                                    b = requests.get('https://api.marketstack.com/v1/tickers/' + TradingSymbol + '/eod/' + d, params)
                                    d = b.json()['close']
                                    p = 'h'
                                except:
                                    pass
                            q = q + 1
                        if p == 'h':
                            a.StockPrice = d
                            a.save()
                    except:
                        print('---Could not establish Stock Price.')
                #
                print('stock price: ' + str(a.StockPrice))
                #
                print(137*'-' + '\n' * 3)
        #
        except:
            pass
        #
        #
        # save
        try:
            #
            tb.save()
            cf.save()
            a.save()
            e.save()
            #
            print(str(e.EntityRegistrantName) + ' (' + str(e.TradingSymbol) + '), ' + str(tb.DocumentPeriodEndDate) + ' (' + str(tb.Period) + ') SEC Data Arched.' + '\n' * 3)
            #
        except:
            print('---Could not save.')
    #
    #
    # Delete the content of the download file
    try:
        files = glob.glob('A:/arch/φ/algorithm/downloads/*')
        for f in files:
            os.remove(f)
        #
        print(137*'-' + '\n')
    except:
        pass
    #
    #
    # stockholders equity beginning balances
    #
    if BeginningBalances == 'yes':
        #
        for scopedperiod in scopedperiods:
            #
            try:
                #
                # Model Current Year Beginning Balance
                tb = TrialBalance.objects.get(TradingSymbol=TradingSymbol, Period=scopedperiod)
                a = AuditData.objects.get(TradingSymbol=TradingSymbol, Period=scopedperiod)
                #
                chronology = {
                    'lastyear': 'secondlastyear',
                    'secondlastyear': 'thirdlastyear',
                    'thirdlastyear': 'fourthlastyear',
                    'fourthlastyear': 'fifthlastyear',
                    'fifthlastyear': 'sixthlastyear',
                    'sixthlastyear': 'seventhlastyear',
                }
                #
                prioryear = chronology[scopedperiod]
                #
                # Model Prior Year Beginning Balance
                try:
                    backwards = 'yes'
                    prioryeartb = TrialBalance.objects.get(TradingSymbol=TradingSymbol, Period=prioryear)
                    prioryeara = AuditData.objects.get(TradingSymbol=TradingSymbol, Period=prioryear)
                    if prioryeara.RetainedEarnings != 0:
                        backwards = ''
                        print('Beginning Balances for ' + scopedperiod + ' from ' + prioryear + " ending balance")
                except:
                    pass
                #
                print(137*'-')
                #
                #
                # Common Shares - Beginning Balance
                if backwards == '':
                    tb.CommonSharesBeginning = prioryeara.CommonShares
                    print('Common Shares Beginning Balance: ' + str(tb.CommonSharesBeginning))
                else:
                    c = a.CommonShares
                    c = c - tb.CommonStockIssued
                    c = c - tb.ShareBasedCompensation
                    tb.CommonSharesBeginning = c
                    print('Common Shares Beginning Balance: ' + str(tb.CommonSharesBeginning))
                #
                #
                # Retained Earnings - Beginning Balance
                if backwards == '':
                    tb.RetainedEarningsBeginning = prioryeara.RetainedEarnings
                    print('Retained Earnings Beginning Balance: ' + str(tb.RetainedEarningsBeginning))
                else:
                    c = a.RetainedEarnings
                    c = c - tb.DividendsAndDividendEquivalentsDeclared
                    c = c - tb.CommonStockRepurchasedAndRetired
                    c = c - tb.EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts
                    c = c - a.NetIncome
                    tb.RetainedEarningsBeginning = c
                    print('Retained Earnings Beginning Balance: ' + str(tb.RetainedEarningsBeginning))
                #
                #
                # Accumulated Other Comprehensive Income - Beginning Balance
                if backwards == '':
                    tb.AccumulatedOtherComprehensiveIncomeBeginning = prioryeara.AccumulatedOtherComprehensiveIncome
                    print('Accumulated Other Comprehensive Income (Loss) Beginning Balance: ' + str(tb.AccumulatedOtherComprehensiveIncomeBeginning))
                else:
                    c = a.AccumulatedOtherComprehensiveIncome
                    c = c - tb.ChangeInForeignCurrencyTranslationAdjustment
                    c = c - tb.ChangeInUnrealizedGainsLossesOnDerivativeInstruments
                    c = c - tb.ChangeInUnrealizedGainsLossesOnInvestments
                    tb.AccumulatedOtherComprehensiveIncomeBeginning = c
                    print('Accumulated Other Comprehensive Income (Loss) Beginning Balance: ' + str(tb.AccumulatedOtherComprehensiveIncomeBeginning))
                #
                #
                # Employee Benefit Trust - Beginning Balance
                if backwards == '':
                    tb.EmployeeBenefitTrustBeginning = prioryeara.EmployeeBenefitTrust
                    print('Employee Benefit Trust Beginning Balance: ' + str(tb.EmployeeBenefitTrustBeginning))
                else:
                    c = a.EmployeeBenefitTrust
                    tb.EmployeeBenefitTrustBeginning = c
                    print('Employee Benefit Trust Beginning Balance: ' + str(tb.EmployeeBenefitTrustBeginning))
                #
                #
                # Non Controling Interest - Beginning Balance
                if backwards == '':
                    c = prioryeara.NonControllingInterests
                    c = c - tb.DividendsDeclaredToNonControllingInterests
                    c = c - tb.NonControllingInterestsOthers
                    tb.NonControllingInterestsBeginning = c
                    print('Non-Controling Interests Beginning Balance: ' + str(tb.NonControllingInterestsBeginning))
                else:
                    tb.NonControllingInterestsBeginning = a.NonControllingInterests
                    print('Non-Controlling Interests Beginning Balance: ' + str(tb.NonControllingInterestsBeginning))
            #
            except:
                print('---Could not establish beginning balances.')
            #
            tb.save()
            #
            print(137 * '-')
            print('\n' * 3)
    #
    #
    # anomalies & corrections
    if Regularize == 'yes':
        #
        for scopedperiod in scopedperiods:
            # 
            #
            print('anomalies and regularizations for ' + scopedperiod)
            #
            tb = TrialBalance.objects.get(TradingSymbol=TradingSymbol, Period=scopedperiod)
            a = AuditData.objects.get(TradingSymbol=TradingSymbol, Period=scopedperiod)
            #
            print(137*'-' + '\n')
            #
            try:
                #
                #
                # current assets
                try:
                    print('Cash: ' + str(tb.Cash) + ' $')
                    print('Short Term Investments: ' + str(tb.ShortTermInvestments) + ' $')
                    print('Accounts Receivable: ' + str(tb.AccountsReceivable) + ' $')
                    print('Inventories: ' + str(tb.Inventories) + ' $')
                    print('Prepaid Expenses: ' + str(tb.PrepaidExpenses) + ' $')
                    print('Non Trade Receivables: ' + str(tb.NonTradeReceivables) + ' $')
                    print('Deferred Tax Assets Current: ' + str(tb.DeferredTaxAssetsCurrent) + ' $')
                    print('Other Current Assets: ' + str(tb.OtherCurrentAssets) + ' $')
                    print('Discontinued Operations: ' + str(tb.DiscontinuedOperations) + ' $')
                    print(' == Total Current Assets: ' + str(a.CurrentAssets) + ' $')
                    #
                    print(137*'-')
                except:
                    pass
                try:
                    Anomaly = 0
                    Components = [
                        tb.Cash,
                        tb.ShortTermInvestments,
                        tb.AccountsReceivable,
                        tb.Inventories,
                        tb.PrepaidExpenses,
                        tb.NonTradeReceivables,
                        tb.DeferredTaxAssetsCurrent,
                        tb.OtherCurrentAssets,
                        tb.DiscontinuedOperationsCurrent,
                    ]
                    Total = a.CurrentAssets
                    #
                    Components = sum(Components)
                    print('Components: ' + str(Components))
                    print('Total: ' + str(Total))
                    Anomaly = Components - Total
                    print('Anomaly: ' + str(Anomaly))
                    #
                    tb.OtherCurrentAssets = tb.OtherCurrentAssets - Anomaly
                    a.AnomalyCurrentAssets = Anomaly
                    #
                    if Anomaly != 0:
                        print(137*'-')
                        #
                        print('Other Current Assets ' + str(tb.OtherCurrentAssets))
                    #
                    tb.save()
                    a.save()
                    #
                    print(137*'-' + '\n')
                    #
                except:
                    print('---Could Not Examinate Current Assets.')
                #
                #
                # non-current assets
                try:
                    #
                    # non current assets
                    print('Investments: ' + str(tb.Investments) + ' $')
                    print('Property Plant And Equipment: ' + str(tb.PropertyPlantAndEquipment) + ' $')
                    print('Operating Lease Right Of Use Asset: ' + str(tb.OperatingLeaseRightOfUseAssets) + ' $')
                    print('Finance Lease Right Of Use Asset: ' + str(tb.FinanceLeaseRightOfUseAssets) + ' $')
                    print('Intangible Assets: ' + str(tb.IntangibleAssets) + ' $')
                    print('Goodwill: ' + str(tb.Goodwill) + ' $')
                    print('Deferred Tax Assets Non Current: ' + str(tb.DeferredTaxAssetsNonCurrent) + ' $')
                    print('Other Non Current Assets: ' + str(tb.OtherNonCurrentAssets) + ' $')
                    print(' == Total Non Current Assets: ' + str(a.NonCurrentAssets) + ' $')
                    #
                    print(137*'-')
                except:
                    pass
                try:
                    Anomaly = 0
                    Components = [
                        tb.Investments,
                        tb.PropertyPlantAndEquipment,
                        tb.OperatingLeaseRightOfUseAssets,
                        tb.FinanceLeaseRightOfUseAssets,
                        tb.IntangibleAssets,
                        tb.Goodwill,
                        tb.DeferredTaxAssetsNonCurrent,
                        tb.OtherNonCurrentAssets,
                        tb.DiscontinuedOperations,
                    ]
                    Total = a.NonCurrentAssets
                    #
                    Components = sum(Components)
                    print('Components: ' + str(Components))
                    print('Total: ' + str(Total))
                    Anomaly = Components - Total
                    print('Anomaly: ' + str(Anomaly))
                    #
                    tb.OtherNonCurrentAssets = tb.OtherNonCurrentAssets - Anomaly
                    a.AnomalyNonCurrentAssets = Anomaly
                    #
                    if Anomaly != 0:
                        print(137*'-')
                        #
                        print('Other Non Current Assets: ' + str(tb.OtherNonCurrentAssets))
                    #
                    tb.save()
                    a.save()
                    #
                    print(137*'-' + '\n')
                    #
                except:
                    print('---Could Not Examinate Non-Current Assets .')
                #
                #
                # assets
                print(' === Total Assets: ' + str(a.Assets) + ' $')
                print(137*'-')
                print('\n' * 3)
                #
                #
                # current liabilities
                try:
                    print('Accounts Payable And Accrued Liabilities: ' + str(tb.AccountsPayableAndAccruedLiabilities) + ' $')
                    print('Employee Compensation: ' + str(tb.EmployeeCompensationCurrent) + ' $')
                    print('Operating Leases Current: ' + str(tb.OperatingLeasesCurrent) + ' $')
                    print('Finance Leases Current: ' + str(tb.FinanceLeasesCurrent) + ' $')
                    print('Capital Lease And Financing Obligations Current: ' + str(tb.CapitalLeaseAndFinancingObligationsCurrent) + ' $')
                    print('Deferred Revenue And Deposits Current: ' + str(tb.DeferredRevenueAndDepositsCurrent) + ' $')
                    print('Accrued Tax Liabilities: ' + str(tb.AccruedTaxLiabilities) + ' $')
                    print('Deferred Tax Liabilities Current: ' + str(tb.DeferredTaxLiabilitiesCurrent) + ' $')
                    print('Commercial Papers: ' + str(tb.CommercialPapers) + ' $')
                    print('Other Current Liabilities: ' + str(tb.OtherCurrentLiabilities) + ' $')
                    print('Discontinued Operations Liabilities Current: ' + str(tb.DiscontinuedOperationsLiabilitiesCurrent) + ' $')
                    print('Dividends Payable: ' + str(tb.DividendsPayable) + ' $')
                    print('Short Term Borrowings: ' + str(tb.ShortTermBorrowings) + ' $')
                    print('Short Term Portion Of Long Term Debt: ' + str(tb.ShortTermPortionOfLongTermDebt) + ' $')
                    print(' == Total Current Liabilities: ' + str(a.CurrentLiabilities) + ' $')
                    #
                    print(137*'-')
                except:
                    pass
                try:
                    Anomaly = 0
                    Components = [
                        tb.AccountsPayableAndAccruedLiabilities,
                        tb.EmployeeCompensationCurrent,
                        tb.OperatingLeasesCurrent,
                        tb.FinanceLeasesCurrent,
                        tb.CapitalLeaseAndFinancingObligationsCurrent,
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
                    a.AnomalyCurrentLiabilities = Anomaly
                    #
                    Components = sum(Components)
                    print('Components: ' + str(Components))
                    print('Total: ' + str(Total))
                    Anomaly = Components - Total
                    print('Anomaly: ' + str(Anomaly))
                    #
                    tb.OtherCurrentLiabilities = tb.OtherCurrentLiabilities - Anomaly
                    #
                    if Anomaly != 0:
                        print(137*'-')
                        #
                        print('Other Current Liabilities: ' + str(tb.OtherCurrentLiabilities))
                    #
                    tb.save()
                    a.save()
                    #
                    print(137*'-' + '\n')
                    #
                except:
                    print('---Could Not Examinate Current Liabilities.')
                #
                #
                # non-current liabilities
                try:
                    print('Long Term Debt: ' + str(tb.LongTermDebt) + ' $')
                    print('Retirement Benefits: ' + str(tb.RetirementBenefits) + ' $')
                    print('Operating Leases Non-Current: ' + str(tb.OperatingLeasesNonCurrent) + ' $')
                    print('Finance Leases Non-Current: ' + str(tb.FinanceLeasesNonCurrent) + ' $')
                    print('Capital Lease And Financing Obligations Non Current: ' + str(tb.CapitalLeaseAndFinancingObligationsNonCurrent) + ' $')
                    print('Deferred Revenue and Deposits Non Current: ' + str(tb.DeferredRevenueAndDepositsNonCurrent) + ' $')
                    print('Accrued Tax Liabilities Non Current: ' + str(tb.AccruedTaxLiabilitiesNonCurrent) + ' $')
                    print('Deferred Tax Liabilities Non Current: ' + str(tb.DeferredTaxLiabilitiesNonCurrent) + ' $')
                    print('Other Non Current Liabilities: ' + str(tb.OtherNonCurrentLiabilities) + ' $')
                    print('Discontinued Operations Liabilities Non Current: ' + str(tb.DiscontinuedOperationsLiabilitiesNonCurrent) + ' $')
                    print(' == Total Non Current Liabilities: ' + str(a.NonCurrentLiabilities) + ' $')
                    print(137*'-')
                except:
                    pass
                try:
                    Anomaly = 0
                    Components = [
                        tb.LongTermDebt,
                        tb.RetirementBenefits,
                        tb.OperatingLeasesNonCurrent,
                        tb.FinanceLeasesNonCurrent,
                        tb.CapitalLeaseAndFinancingObligationsNonCurrent,
                        tb.DeferredRevenueAndDepositsNonCurrent,
                        tb.AccruedTaxLiabilitiesNonCurrent,
                        tb.DeferredTaxLiabilitiesNonCurrent,
                        tb.OtherNonCurrentLiabilities,
                        tb.DiscontinuedOperationsLiabilitiesNonCurrent,
                    ]
                    if a.NonCurrentLiabilities == 0:
                        if a.Liabilities == 0:
                            a.Liabilities = a.LiabilitiesAndStockholdersEquity - a.StockholdersEquity
                        a.NonCurrentLiabilities = a.Liabilities - a.CurrentLiabilities
                    #
                    Total = a.NonCurrentLiabilities
                    #
                    Components = sum(Components)
                    print('Components: ' + str(Components))
                    print('Total: ' + str(Total))
                    Anomaly = Components - Total
                    print('Anomaly: ' + str(Anomaly))
                    #
                    tb.OtherNonCurrentLiabilities = tb.OtherNonCurrentLiabilities - Anomaly   
                    a.AnomalyNonCurrentLiabilities = Anomaly         
                    if Anomaly != 0:
                        print(137*'-')
                        #
                        print('Other Non-Current Liabilities: ' + str(tb.OtherNonCurrentLiabilities))
                    #
                    tb.save()
                    a.save()
                    #
                    print(137*'-' + '\n')
                    #
                except:
                    print('---Could Not Examinate Non-Current Liabilities.')
                #
                #
                # liabilities
                print(' === Total Liabilities: ' + str(a.Liabilities) + ' $')
                print(137*'-')
                print('\n' * 3)
                #
                #
                # gross margin
                try:
                    print('Sales: ' + str(tb.Sales) + ' $')
                    print('Cost Of Sales: ' + str(tb.CostOfSales) + ' $')
                    print(' = Gross Margin: ' + str(a.GrossMargin) + ' $')
                    print(137*'-')
                except:
                    pass
                try:
                    Anomaly = 0
                    Components = [
                        tb.Sales,
                        tb.CostOfSales,
                    ]
                    if a.GrossMargin == 0:
                        a.GrossMargin = sum(Components)
                        print(' = Gross Margin: ' + str(a.GrossMargin) + ' $, based on components')
                    #
                    Total = a.GrossMargin
                    #
                    Components = sum(Components)
                    print('Components: ' + str(Components))
                    print('Total: ' + str(Total))
                    Anomaly = Components - Total
                    print('Anomaly: ' + str(Anomaly))
                    #
                    if tb.Sales == 0:
                        tb.Sales = Anomaly
                    elif tb.CostOfSales == 0:
                        tb.CostOfSales = Anomaly
                    else:
                        if Anomaly > 0:
                            tb.Sales = tb.Sales - Anomaly
                        else:
                            tb.CostOfSales = tb.CostOfSales - Anomaly
                    #
                    a.AnomalyGrossMargin = Anomaly
                    #
                    tb.save()
                    a.save()
                    #
                    print(137*'-' + '\n')
                    #
                except:
                    print('---Could Not Examinate Gross Margin.')
                #
                #
                # operating expenses
                try:
                    print('Research And Development: ' + str(tb.ResearchAndDevelopment) + ' $')
                    print('Selling General Administrative And Marketing: ' + str(tb.SellingGeneralAdministrativeAndMarketing) + ' $')
                    print(' = Operating Expenses: ' + str(a.OperatingExpenses) + ' $')
                    #
                    print(137*'-')
                except:
                    pass
                try:
                    Anomaly = 0
                    Components = [
                        tb.ResearchAndDevelopment,
                        tb.SellingGeneralAdministrativeAndMarketing,
                    ]
                    if a.OperatingExpenses == 0:
                        #
                        if a.OperatingIncome == 0:
                            a.OperatingIncome = a.GrossMargin + sum(Components)
                            print(' = Operating Income: ' + str(a.OperatingIncome) + ' $, based on components')
                        #
                        a.OperatingExpenses = a.OperatingIncome - a.GrossMargin
                        print(' = Operating Expense: ' + str(a.OperatingExpenses) + ' $, based on difference in operating income and gross margin.')
                    #
                    Total = a.OperatingExpenses
                    #
                    Components = sum(Components)
                    print('Components: ' + str(Components))
                    print('Total: ' + str(Total))
                    Anomaly = Components - Total
                    print('Anomaly: ' + str(Anomaly))
                    #
                    tb.SellingGeneralAdministrativeAndMarketing = tb.SellingGeneralAdministrativeAndMarketing - Anomaly
                    a.AnomalyOperatingExpenses = Anomaly
                    #
                    if Anomaly != 0:
                        #
                        print(137*'-')
                        #
                        print('Selling, Administrative And Marketing: ' + str(tb.SellingGeneralAdministrativeAndMarketing))
                    #
                    tb.save()
                    a.save()
                    #
                    print(137*'-' + '\n')
                    #
                except:
                    print('---Could Not Examinate Operating Expenses.')
                #
                #
                # operating income
                try:
                    print(' = Operating Income: ' + str(a.OperatingIncome) + ' $')
                    print(137*'-')
                except:
                    pass
                try:
                    Anomaly = 0
                    Components = [
                        a.GrossMargin,
                        a.OperatingExpenses,
                    ]
                    Total = a.OperatingIncome
                    #
                    Components = sum(Components)
                    print('Components: ' + str(Components))
                    print('Total: ' + str(Total))
                    Anomaly = Components - Total
                    print('Anomaly: ' + str(Anomaly))
                    #
                    a.AnomalyOperatingIncome = Anomaly
                    #
                    tb.save()
                    a.save()
                    #
                    print(137*'-' + '\n')
                    #
                except:
                    print('---Could Not Examinate Operating Income.')
                #
                #
                # income before taxes
                try:
                    print('Non Operating Expense (Income): ' + str(tb.NonOperatingIncome) + ' $')
                    print('Impairment Restructuring And Other Special Charges: ' + str(tb.ImpairmentRestructuringAndOtherSpecialCharges) + ' $')
                    print(' = Income Before Taxes: ' + str(a.IncomeBeforeTaxes) + ' $')
                    #
                    print(137*'-')
                except:
                    pass
                try:
                    Anomaly = 0
                    Components = [
                        a.OperatingIncome,
                        tb.ImpairmentRestructuringAndOtherSpecialCharges,
                        tb.NonOperatingIncome,
                    ]
                    Total = a.IncomeBeforeTaxes
                    #
                    Components = sum(Components)
                    print('Components: ' + str(Components))
                    print('Total: ' + str(Total))
                    Anomaly = Components - Total
                    print('Anomaly: ' + str(Anomaly))
                    #
                    tb.NonOperatingIncome = tb.NonOperatingIncome - Anomaly
                    a.AnomalyNonOperatingIncome = Anomaly
                    #
                    if Anomaly != 0:
                        #
                        print(137*'-')
                        #
                        print('Non Operating Income: ' + str(tb.NonOperatingIncome))
                    #
                    print(137*'-' + '\n')
                    #
                except:
                    print('---Could Not Examinate Income Before Taxes.')
                #
                #
                # net income
                try:
                    print('Income Tax Expense Benefit: ' + str(tb.IncomeTaxExpenseBenefit) + ' $')
                    print('Net Income From Discontinued Operations: ' + str(tb.NetIncomeFromDiscontinuedOperations) + ' $')
                    print(' == Net Income: ' + str(a.NetIncome) + ' $')
                    #
                    print(137*'-')
                except:
                    pass
                try:
                    Anomaly = 0
                    Components = [
                        a.IncomeBeforeTaxes,
                        tb.IncomeTaxExpenseBenefit,
                        tb.NetIncomeFromDiscontinuedOperations,
                    ]
                    Total = a.NetIncome
                    #
                    Components = sum(Components)
                    print('Components: ' + str(Components))
                    print('Total: ' + str(Total))
                    Anomaly = Components - Total
                    print('Anomaly: ' + str(Anomaly))
                    #
                    a.AnomalyNetIncome = Anomaly
                    #
                    tb.save()
                    a.save()
                    #
                    print(137*'-' + '\n')
                    #
                except:
                    print('---Could Not Examinate Net Income.')
                #
                #
                # other comprehensive income
                try:
                    print('Change In Foreign Currency Translation Adjustment Net Of Taxes: ' + str(tb.ChangeInForeignCurrencyTranslationAdjustment) + ' $')
                    print('Change In Unrealized Gains (Losses) On Derivative Instruments, Net Of Taxes: ' + str(tb.ChangeInUnrealizedGainsLossesOnDerivativeInstruments) + ' $')
                    print('Change In Unrealized Gains (Losses) On Investment, Net Of Taxes: ' + str(tb.ChangeInUnrealizedGainsLossesOnInvestments) + ' $')
                    print('Change In Defined Benefit Pension And Other Similar Plans: ' + str(tb.ChangeInDefinedBenefitPensionAndOtherSimilarPlans) + ' $')
                    print('Income Tax On Other Comprehensive Income: ' + str(tb.IncomeTaxOnOtherComprehensiveIncome) + ' $')
                    #
                    print(' = Other Comprehensive Income: ' + str(a.OtherComprehensiveIncome) + ' $')
                    #
                    print('Net Income: ' + str(a.NetIncome) + ' $')
                    print('Comprehensive Income: ' + str(a.ComprehensiveIncome) + ' $')
                    #
                    print(137*'-')
                except:
                    pass
                try:
                    Anomaly = 0
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
                    print('Components: ' + str(Components))
                    print('Total: ' + str(Total))
                    Anomaly = Components - Total
                    print('Anomaly: ' + str(Anomaly))
                    #
                    tb.ChangeInUnrealizedGainsLossesOnInvestments = tb.ChangeInUnrealizedGainsLossesOnInvestments - Anomaly
                    a.AnomalyOtherComprehensiveIncome = Anomaly
                    #
                    if Anomaly != 0:
                        #
                        print(137*'-')
                        #
                        print('Change In Unrealized Gains (Losses) On Investments, Net Of Taxes: ' + str(tb.ChangeInUnrealizedGainsLossesOnInvestments))
                    #
                    tb.save()
                    a.save()
                    #
                    print(137*'-' + '\n')
                    #
                except:
                    print('---Could Not Examinate Other Comprehensive Income.')
                #
                #
                # common shares
                try:
                    print('Common Shares Beginning Balance: ' + str(tb.CommonSharesBeginning) + ' $')
                    print('Common Stock Issued: ' + str(tb.CommonStockIssued) + ' $')
                    print('Share Based Compensation: ' + str(tb.ShareBasedCompensation) + ' $')
                    print(137*'-')
                except:
                    pass
                try:
                    Anomaly = 0
                    Components = [
                        tb.CommonSharesBeginning,
                        tb.CommonStockIssued,
                        tb.ShareBasedCompensation,
                    ]
                    #
                    Total = a.CommonShares
                    #
                    Components = sum(Components)
                    print('Components: ' + str(Components))
                    print('Total: ' + str(Total))
                    Anomaly = Components - Total
                    print('Anomaly: ' + str(Anomaly))
                    #
                    tb.ShareBasedCompensation = tb.ShareBasedCompensation - Anomaly
                    #
                    a.AnomalyCommonShares = Anomaly
                    #
                    if Anomaly != 0:
                        #
                        print(137*'-')
                        #
                        print('Share Based Compensation: ' + str(tb.ShareBasedCompensation))
                    #
                    tb.save()
                    a.save()
                    #
                    print(137*'-' + '\n')
                    #
                except:
                    print('---Could Not Examinate Common Shares.')
                #
                #
                # accumulated other comprehensive income
                try:
                    print('Accumulated Other Comprehensive Income Beginning Balance: ' + str(tb.AccumulatedOtherComprehensiveIncomeBeginning) + ' $')
                    print('Change In Foreign Currency Translation Adjustment Net Of Taxes: ' + str(tb.ChangeInForeignCurrencyTranslationAdjustment) + ' $')
                    print('Change In Unrealized Gains (Losses) On Derivative Instruments, Net Of Taxes: ' + str(tb.ChangeInUnrealizedGainsLossesOnDerivativeInstruments) + ' $')
                    print('Change In Unrealized Gains (Losses) On Investment, Net Of Taxes: ' + str(tb.ChangeInUnrealizedGainsLossesOnInvestments) + ' $')
                    print('Change In Defined Benefit Pension And Other Similar Plans: ' + str(tb.ChangeInDefinedBenefitPensionAndOtherSimilarPlans) + ' $')
                    print('Income Tax On Other Comprehensive Income: ' + str(tb.IncomeTaxOnOtherComprehensiveIncome) + ' $')
                    print(' = Other Comprehensive Income: ' + str(a.OtherComprehensiveIncome) + ' $')
                    print('Accumulated Other Comprehensive Income Ending Balance: ' + str(a.AccumulatedOtherComprehensiveIncome) + ' $')
                    print(137*'-')
                except:
                    pass
                try:
                    Anomaly = 0
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
                    print('Components: ' + str(Components))
                    print('Total: ' + str(Total))
                    Anomaly = Components - Total
                    print('Anomaly: ' + str(Anomaly))
                    #
                    tb.ChangeInUnrealizedGainsLossesOnInvestments = tb.ChangeInUnrealizedGainsLossesOnInvestments - Anomaly
                    #
                    a.OtherComprehensiveIncome = a.OtherComprehensiveIncome - Anomaly
                    #
                    a.AnomalyOtherComprehensiveIncome = a.AnomalyOtherComprehensiveIncome + Anomaly
                    #
                    if Anomaly != 0:
                        #
                        print(137*'-')
                        #
                        print('Change In Unrealized Gains (Losses) On Investments, Net Of Taxes: ' + str(tb.ChangeInUnrealizedGainsLossesOnInvestments))
                    #
                    tb.save()
                    a.save()
                    #
                    print(137*'-' + '\n')
                except:
                    print('---Could Not Examinate Accumulated Other Compregensive Income (Loss).')
                #
                # 
                # retained earnings
                try:
                    print('Retained Earnings Beginning Balance: ' + str(tb.RetainedEarningsBeginning) + ' $')
                    print('Dividends And Dividend Equivalents Declared: ' + str(tb.DividendsAndDividendEquivalentsDeclared) + ' $')
                    print('Common Stock Repurchased And Retired: ' + str(tb.CommonStockRepurchasedAndRetired) + ' $')
                    print('Effect Of Adoption Of New Accounting Pronouncement Or Tax Cuts: ' + str(tb.EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts) + ' $')
                    print('Retained Earnings, Others: ' + str(tb.RetainedEarningsOthers) + ' $')
                    print('Net Income: ' + str(a.NetIncome) + ' $')
                    print('Retained Earnings Ending Balance: ' + str(a.RetainedEarnings) + ' $')
                    print(137*'-')
                except:
                    pass
                try:
                    Anomaly = 0
                    Components = [
                        tb.RetainedEarningsBeginning,
                        tb.DividendsAndDividendEquivalentsDeclared,
                        tb.CommonStockRepurchasedAndRetired,
                        tb.EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts,
                        tb.RetainedEarningsOthers,
                        a.NetIncome,
                    ]
                    #
                    Total = a.RetainedEarnings
                    #
                    Components = sum(Components)
                    print('Components: ' + str(Components))
                    print('Total: ' + str(Total))
                    Anomaly = Components - Total
                    print('Anomaly: ' + str(Anomaly))
                    #
                    tb.RetainedEarningsOthers = -Anomaly
                    #
                    a.AnomalyRetainedEarnings = Anomaly
                    #
                    if Anomaly != 0:
                        #
                        print(137*'-')
                        #
                        print('Other Adjustment Affecting Retained Earnings: ' + str(tb.RetainedEarningsOthers))
                    #
                    tb.save()
                    a.save()
                    #
                    print(137*'-' + '\n')
                    #
                except:
                    print('---Could Not Examinate Retained Earnings.')
                #
                # 
                # non controlling interests
                try:
                    print('Non Controlling Interests Beginning Balance: ' + str(tb.NonControllingInterestsBeginning) + ' $')
                    print('Dividends Declared To Non Controlling Interests: ' + str(tb.DividendsDeclaredToNonControllingInterests) + ' $')
                    print('Non Controlling Interests Others: ' + str(tb.NonControllingInterestsOthers) + ' $')
                    
                    print('Non Controlling Interests Ending Balance: ' + str(a.NonControllingInterests) + ' $')
                    print(137*'-')
                except:
                    pass
                try:
                    Anomaly = 0
                    Components = [
                        tb.NonControllingInterestsBeginning,
                        tb.DividendsDeclaredToNonControllingInterests,
                        tb.NonControllingInterestsOthers,
                    ]
                    #
                    Total = a.NonControllingInterests
                    #
                    Components = sum(Components)
                    print('Components: ' + str(Components))
                    print('Total: ' + str(Total))
                    Anomaly = Components - Total
                    print('Anomaly: ' + str(Anomaly))
                    #
                    tb.NonControllingInterestsOthers = -Anomaly
                    #
                    a.AnomalyNonControllingInterests = Anomaly
                    #
                    if Anomaly != 0:
                        #
                        print(137*'-')
                        #
                        print('Non Controlling Interests Others: ' + str(tb.NonControllingInterestsOthers))
                    #
                    tb.save()
                    a.save()
                    #
                    print(137*'-' + '\n')
                    #
                except:
                    print('---Could Not Examinate Non Controlling Interests.')
                #
                #
                # shareholders equity
                try:
                    print('Common Shares - Ending Balance: ' + str(a.CommonShares) + ' $')
                    print('Accumulated Other Comprehensive Income - Ending Balance: ' + str(a.AccumulatedOtherComprehensiveIncome) + ' $')
                    print('Retained Earnings - Ending Balance: ' + str(a.RetainedEarnings) + ' $')
                    print('Employee Benefit Trust - Ending Balance: ' + str(a.EmployeeBenefitTrust) + ' $')
                    print('Non Controlling Interests - Ending Balance: ' + str(a.RetainedEarnings) + ' $')
                    print(' == Stockholders Equity: ' + str(a.StockholdersEquity) + ' $')
                    print(137*'-')
                except:
                    pass
                try:
                    Anomaly = 0
                    Components = [
                        a.CommonShares,
                        a.AccumulatedOtherComprehensiveIncome,
                        a.RetainedEarnings,
                        a.EmployeeBenefitTrust,
                        a.NonControllingInterests,
                    ]
                    Total = a.StockholdersEquity
                    #
                    Components = sum(Components)
                    print('Components: ' + str(Components))
                    print('Total: ' + str(Total))
                    Anomaly = Components - Total
                    print('Anomaly: ' + str(Anomaly))
                    #
                    a.AnomalyStockholdersEquity = Anomaly
                    #
                    tb.save()
                    a.save()
                    #
                    print(137*'-' + '\n')
                    #
                except:
                    print('---Could Not Examinate Shareholders Equity.')
                #
                #
                # save
                try:
                    tb.save()
                except:
                    print('---Could not save Trial Balance.')
            except:
                print('---Could not examinate Trial Balance.')
            #
            # 
            # cash flow 
            try:
                cf = CashFlow.objects.get(TradingSymbol=TradingSymbol, Period=scopedperiod)
                #
                #
                # operating activities
                try:
                    print('Net Income: ' + str(-a.NetIncome) + ' $')
                    print('Depreciation Depletion And Amortization: ' + str(cf.DepreciationDepletionAndAmortization) + ' $')
                    print('Gain Related To Disposal Or Sale: ' + str(cf.GainRelatedToDisposalOrSale) + ' $')
                    print('Share Based Compensation Operating Activities: ' + str(cf.ShareBasedCompensation) + ' $')
                    print('Deferred Income Tax Expense (Benefit): ' + str(cf.DeferredIncomeTaxExpenseBenefit) + ' $')
                    print('Other Non Cash Income Expense: ' + str(cf.OtherNonCashIncomeExpense) + ' $')
                    print('Increase (Decrease) In Accounts Receivable: ' + str(cf.IncreaseDecreaseInAccountsReceivable) + ' $')
                    print('Increase (Decrease) In Inventories: ' + str(cf.IncreaseDecreaseInInventories) + ' $')
                    print('Increase (Decrease) In Other Receivables: ' + str(cf.IncreaseDecreaseInOtherReceivables) + ' $')
                    print('Increase (Decrease) In Accounts Payable: ' + str(cf.IncreaseDecreaseInAccountsPayableAndAccruedLiabilities) + ' $')
                    print('Increase (Decrease) In Contract With Customer Liability: ' + str(cf.IncreaseDecreaseInContractWithCustomerLiability) + ' $')
                    print('Increase (Decrease) In Other Operating Activities: ' + str(cf.IncreaseDecreaseInOtherOperatingActivities) + ' $')
                    print(' == Operating Activities: ' + str(a.OperatingActivities) + ' $')
                    print(137*'-')
                except:
                    pass
                try:
                    Anomaly = 0
                    Components = [
                        -a.NetIncome,
                        cf.DepreciationDepletionAndAmortization,
                        cf.GainRelatedToDisposalOrSale,
                        cf.ShareBasedCompensation,
                        cf.DeferredIncomeTaxExpenseBenefit,
                        cf.OtherNonCashIncomeExpense,
                        cf.IncreaseDecreaseInAccountsReceivable, 
                        cf.IncreaseDecreaseInInventories,
                        cf.IncreaseDecreaseInOtherReceivables,
                        cf.IncreaseDecreaseInAccountsPayableAndAccruedLiabilities,
                        cf.IncreaseDecreaseInContractWithCustomerLiability,
                        cf.IncreaseDecreaseInOtherOperatingActivities,
                    ]
                    Total = a.OperatingActivities
                    #
                    Components = sum(Components)
                    print('Components: ' + str(Components))
                    print('Total: ' + str(Total))
                    Anomaly = Components - Total
                    print('Anomaly: ' + str(Anomaly))
                    #
                    cf.IncreaseDecreaseInOtherOperatingActivities = cf.IncreaseDecreaseInOtherOperatingActivities - Anomaly
                    #
                    if Anomaly != 0:
                        #
                        print(137*'-')
                        #
                        print('Increase (Decrease) In Other Operating Activities: ' + str(cf.IncreaseDecreaseInOtherOperatingActivities))
                    #
                    a.AnomalyOperatingActivities = Anomaly
                    #
                    cf.save()
                    a.save()
                    #
                    print(137*'-' + '\n')
                    #
                except:
                    print('---Could Not Examinate Operating Activities.') 
                #
                #
                # investing activities
                try:
                    print('Payments To Acquire Property Plant And Equipment: ' + str(cf.PaymentsToAcquirePropertyPlantAndEquipment) + ' $')
                    print('Payments To Acquire Investment: ' + str(cf.PaymentsToAcquireInvestments) + ' $')
                    print('Proceeds Of Investment: ' + str(cf.ProceedsOfInvestments) + ' $')
                    print('Payments To Acquire Businesses and Intangibles, Net Of Cash Acquired: ' + str(cf.PaymentsToAcquireBusinessesAndIntangibles) + ' $')
                    print('Other Investing Activities: ' + str(cf.OtherInvestingActivities) + ' $')
                    print(' == Investing Activities: ' + str(a.InvestingActivities) + ' $')
                    print(137*'-')
                except:
                    pass
                try:
                    Anomaly = 0
                    Components = [
                        cf.PaymentsToAcquirePropertyPlantAndEquipment,
                        cf.PaymentsToAcquireInvestments,
                        cf.ProceedsOfInvestments,
                        cf.PaymentsToAcquireBusinessesAndIntangibles,
                        cf.OtherInvestingActivities,
                    ]
                    Total = a.InvestingActivities
                    #
                    Components = sum(Components)
                    print('Components: ' + str(Components))
                    print('Total: ' + str(Total))
                    Anomaly = Components - Total
                    print('Anomaly: ' + str(Anomaly))
                    #
                    cf.OtherInvestingActivities = cf.OtherInvestingActivities - Anomaly
                    #
                    a.AnomalyInvestingActivities = Anomaly
                    #
                    if Anomaly != 0:
                        #
                        print(137*'-')
                        #
                        print('Other Investing Activities: ' + str(cf.OtherInvestingActivities))
                    #
                    cf.save()
                    a.save()
                    #
                    print(137*'-' + '\n')
                    #
                except:
                    print('---Could Not Examinate Investing Activities.') 
                #
                #
                # financing activities
                try:
                    print('Finance Lease Principal Payments: ' + str(cf.FinanceLeasePrincipalPayments) + ' $')
                    print('Proceeds From Issuance Of Common Stock: ' + str(cf.ProceedsFromIssuanceOfCommonStock) + ' $')
                    print('Payments Related To Tax Withholding For Share Based Compensation: ' + str(cf.PaymentsRelatedToTaxWithholdingForShareBasedCompensation) + ' $')
                    print('Payments Of Dividends: ' + str(cf.PaymentsOfDividends) + ' $')
                    print('Payments For Repurchase Of Common Stock: ' + str(cf.PaymentsForRepurchaseOfCommonStock) + ' $')
                    print('Payments For Taxes Related To Net Share Settlement Of Equity Award: ' + str(cf.PaymentsForTaxesRelatedToNetShareSettlementOfEquityAward) + ' $')
                    print('Proceeds From Issuance Of Long Term Debt: ' + str(cf.ProceedsFromIssuanceOfLongTermDebt) + ' $')
                    print('Repayments Of Long Term Debt: ' + str(cf.RepaymentsOfLongTermDebt) + ' $')
                    print('Proceeds From Repayments Of Commercial Paper: ' + str(cf.ProceedsFromRepaymentsOfCommercialPaper) + ' $')
                    print('Other Financing Activities: ' + str(cf.OtherFinancingActivities) + ' $')
                    print(' == Financing Activities: ' + str(a.FinancingActivities) + ' $')
                    print(137*'-')
                except:
                    pass
                try:
                    Anomaly = 0
                    Components = [
                        cf.FinanceLeasePrincipalPayments,
                        cf.ProceedsFromIssuanceOfCommonStock,
                        cf.PaymentsRelatedToTaxWithholdingForShareBasedCompensation,
                        cf.PaymentsOfDividends,
                        cf.PaymentsForRepurchaseOfCommonStock,
                        cf.PaymentsForTaxesRelatedToNetShareSettlementOfEquityAward,
                        cf.ProceedsFromIssuanceOfLongTermDebt,
                        cf.RepaymentsOfLongTermDebt,
                        cf.ProceedsFromRepaymentsOfCommercialPaper,
                        cf.OtherFinancingActivities,
                    ]
                    Total = a.FinancingActivities
                    #
                    Components = sum(Components)
                    print('Components: ' + str(Components))
                    print('Total: ' + str(Total))
                    Anomaly = Components - Total
                    print('Anomaly: ' + str(Anomaly))
                    #
                    cf.OtherFinancingActivities = cf.OtherFinancingActivities - Anomaly
                    #
                    a.AnomalyFinancingActivities = Anomaly
                    #
                    if Anomaly != 0:
                        #
                        print(137*'-')
                        #
                        print('Other Financing Activities: ' + str(cf.OtherFinancingActivities))
                    #
                    cf.save()
                    a.save()
                    #
                    print(137*'-' + '\n')
                    #
                except:
                    print('---Could Not Examinate Financing Activities.') 
                #
                #
                # supplemental information
                try:
                    # cash beginning balance
                    print('=== Cash Beginning Balance: ' + str(cf.CashBeginningBalance) + ' $')
                    print(137*'-' + '\n')
                    #
                    # cash paid for interest and taxes
                    print('=== Cash Paid For Taxes: ' + str(cf.CashPaidForTaxes) + ' $')
                    print('=== Cash Paid For Interest: ' + str(cf.CashPaidForInterest) + ' $')
                    print(137*'-' + '\n' * 3)
                    #
                    cf.save()
                    a.save()
                    #
                except:
                    pass
                #
                #
                # anomalies
                print('classification anomalies')
                print(137*'-' + '\n')
                #
                #
                # Balance Sheets - Audit
                #
                print('current assets: ' + str(a.AnomalyCurrentAssets))
                print('non current assets: ' + str(a.AnomalyNonCurrentAssets))
                print('assets: ' + str(a.AnomalyAssets))
                print('current liabilities: ' + str(a.AnomalyCurrentLiabilities))
                print('non current liabilities: ' + str(a.AnomalyNonCurrentLiabilities))
                print('liabilities: ' + str(a.AnomalyLiabilities))
                print('stockholders equity: ' + str(a.AnomalyStockholdersEquity))
                print('liabilities and stockholders equity: ' + str(a.AnomalyLiabilitiesAndStockholdersEquity) + '\n')
                #
                #
                # Income Statements - Audit
                #
                print('gross margin: ' + str(a.AnomalyGrossMargin))
                print('operating expenses: ' + str(a.AnomalyOperatingExpenses))
                print('operating income ' + str(a.AnomalyOperatingIncome))
                print('income before taxes: ' + str(a.AnomalyIncomeBeforeTaxes))
                print('net income: ' + str(a.AnomalyNetIncome) + '\n')
                #
                #
                # Comprehensive Income - Audit
                #
                print('other comprehensinve income: ' + str(a.AnomalyOtherComprehensiveIncome))
                print('comprehensive income: ' + str(a.AnomalyComprehensiveIncome) + '\n')
                #
                #
                # Stockholders Equity - Audit
                #
                print('common shares: ' + str(a.AnomalyCommonShares))
                print('retained earnings: ' + str(a.AnomalyRetainedEarnings))
                print('accumulated other comprehensive income: ' + str(a.AnomalyAccumulatedOtherComprehensiveIncome))
                print('employee benefit trust: ' + str(a.AnomalyEmployeeBenefitTrust))
                print('non controlling interests: ' + str(a.AnomalyNonControllingInterests) + '\n')
                #
                #
                # Cash Flow - Audit
                print('operating activities: ' + str(a.AnomalyOperatingActivities))
                print('investing activities: ' + str(a.AnomalyInvestingActivities))
                print('financing activities: ' + str(a.AnomalyFinancingActivities))
            #
            except:
                pass
            #
            print('\n' * 3)
        #
        print(137 * '-')
        print('\n' * 3)
    #
    #
    # save entity and update date time
    try:
        # Time Of Update
        today = date.today()
        date_text = today.strftime("%B %d, %Y")
        e.Update = date_text
        print("Update: ", str(e.Update))
    except:
        print('---Could not save time of update.')
    #
    # save
    try:
        e.save()
        print('Entity ' + TradingSymbol + ' Saved.')
    except:
        print('---Could not save entity.')

