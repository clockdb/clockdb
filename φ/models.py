from django.db import models, migrations
from django.db.models.fields import BigIntegerField, BigIntegerField

class Entity(models.Model):
    #
    db = models.IntegerField(default=0)
    Industry_db = models.IntegerField(default=0)
    Industry_SEC_db = models.IntegerField(default=0)
    Region_db = models.IntegerField(default=0)
    #
    EntityRegistrantName = models.CharField(max_length=93)
    EntityCentralIndexKey = models.CharField(max_length=10)
    #
    Industry = models.CharField(max_length=61, default='')
    #
    Industry_SEC = models.CharField(max_length=61)
    #
    Region = models.CharField(max_length=44)
    #
    SecurityExchangeName = models.CharField(max_length=55, default=0)
    TradingSymbol = models.CharField(max_length=7, null=False, unique=True)
    #
    SECurl = models.CharField(max_length=66, default=0)    
    URL = models.CharField(max_length=99, default='')
    #
    SEC_Update = models.DateField(null=True)
    SEC_UpdateDateAndTime = models.DateTimeField(null=True)
    #
    SecuritiesUpdate = models.DateTimeField(null=True)
    #
    OpinionφLastYear = models.CharField(max_length=55, null=True)
    OpinionφSecondLastYear = models.CharField(max_length=55, null=True)
    OpinionφThirdLastYear = models.CharField(max_length=55, null=True)
    OpinionφFourthLastYear = models.CharField(max_length=55, null=True)
    #
    ClockφLastYear = models.FloatField(default=0, null=True)
    ClockφSecondLastYear = models.FloatField(default=0, null=True)
    ClockφThirdLastYear = models.FloatField(default=0, null=True)
    ClockφFourthLastYear = models.FloatField(default=0, null=True)
    #
    BridgeφLastYear = models.CharField(max_length=128, default=0)
    BridgeφSecondLastYear = models.CharField(max_length=128, default=0)
    BridgeφThirdLastYear = models.CharField(max_length=128, default=0)
    BridgeφFourthLastYear = models.CharField(max_length=128, default=0)
    #
    Anomalies = models.CharField(max_length=128, default=0)
    #
    AnomaliesRatio1 = models.FloatField(default=9999)
    AnomaliesRatio2 = models.FloatField(default=9999)
    AnomaliesRatio3 = models.FloatField(default=9999)
    AnomaliesRatio4 = models.FloatField(default=9999)
    AnomaliesRatio5 = models.FloatField(default=9999)
    AnomaliesRatio6 = models.FloatField(default=9999)
    #
    NumberOfYearsAudited = models.IntegerField(default=0)
    #
    CommonSharesIntrinsicValueLastYear = models.BigIntegerField(default=0, null=True)
    CommonSharesIntrinsicValueSecondLastYear = models.BigIntegerField(default=0, null=True)
    CommonSharesIntrinsicValueThirdLastYear = models.BigIntegerField(default=0, null=True)
    CommonSharesIntrinsicValueFourthLastYear = models.BigIntegerField(default=0, null=True)
    #
    MarketCapitalizationLastYear = models.BigIntegerField(default=0, null=True)
    MarketCapitalizationSecondLastYear = models.BigIntegerField(default=0, null=True)
    MarketCapitalizationThirdLastYear = models.BigIntegerField(default=0, null=True)
    MarketCapitalizationFourthLastYear = models.BigIntegerField(default=0, null=True)
    #
    CommonShareIntrinsicValueLastYear = models.FloatField(default=0, null=True)
    CommonShareIntrinsicValueSecondLastYear = models.FloatField(default=0, null=True)
    CommonShareIntrinsicValueThirdLastYear = models.FloatField(default=0, null=True)
    CommonShareIntrinsicValueFourthLastYear = models.FloatField(default=0, null=True)
    #
    CommonSharePriceLastYear = models.FloatField(default=0, null=True)
    CommonSharePriceSecondLastYear = models.FloatField(default=0, null=True)
    CommonSharePriceThirdLastYear = models.FloatField(default=0, null=True)
    CommonSharePriceFourthLastYear = models.FloatField(default=0, null=True)
    #
    CommonSharesOutstandingLastYear = models.BigIntegerField(default=0, null=True)
    CommonSharesOutstandingSecondLastYear = models.BigIntegerField(default=0, null=True)
    CommonSharesOutstandingThirdLastYear = models.BigIntegerField(default=0, null=True)
    CommonSharesOutstandingFourthLastYear = models.BigIntegerField(default=0, null=True)
    #
    accessionnumberlastyear = models.CharField(max_length=20, default='')
    accessionnumbersecondlastyear = models.CharField(max_length=20, default='')
    accessionnumberthirdlastyear = models.CharField(max_length=20, default='')
    accessionnumberfourthlastyear = models.CharField(max_length=20, default='')
    accessionnumberfifthlastyear = models.CharField(max_length=20, default='')
    accessionnumbersixthlastyear =  models.CharField(max_length=20, default='')
    #
    month_end = models.IntegerField(default=0)
    #
    lastyear = models.DateField(null=True)
    secondlastyear = models.DateField(null=True)
    thirdlastyear = models.DateField(null=True)
    fourthlastyear = models.DateField(null=True)
    fifthlastyear = models.DateField(null=True)
    sixthlastyear = models.DateField(null=True)
    #
    amendlastyear =  models.CharField(max_length=5, default='')
    amendsecondlastyear =  models.CharField(max_length=5, default='')
    amendthirdlastyear =  models.CharField(max_length=5, default='')
    amendfourthlastyear =  models.CharField(max_length=5, default='')
    amendfifthlastyear =  models.CharField(max_length=5, default='')
    amendsixthlastyear =  models.CharField(max_length=5, default='')
    #
    urlbalancesheetlastyear =  models.CharField(max_length=170, default='')
    urlbalancesheetsecondlastyear =  models.CharField(max_length=170, default='')
    urlbalancesheetthirdlastyear =  models.CharField(max_length=170, default='')
    urlbalancesheetfourthlastyear =  models.CharField(max_length=170, default='')
    urlbalancesheetfifthlastyear =  models.CharField(max_length=170, default='')
    urlbalancesheetsixthlastyear =  models.CharField(max_length=170, default='')
    #
    urlincomestatementlastyear =  models.CharField(max_length=170, default='')
    urlincomestatementsecondlastyear =  models.CharField(max_length=170, default='')
    urlincomestatementthirdlastyear =  models.CharField(max_length=170, default='')
    urlincomestatementfourthlastyear =  models.CharField(max_length=170, default='')
    urlincomestatementfifthlastyear =  models.CharField(max_length=170, default='')
    urlincomestatementsixthlastyear =  models.CharField(max_length=170, default='')
    #
    urlcomprehensiveincomelastyear =  models.CharField(max_length=170, default='')
    urlcomprehensiveincomesecondlastyear =  models.CharField(max_length=170, default='')
    urlcomprehensiveincomethirdlastyear =  models.CharField(max_length=170, default='')
    urlcomprehensiveincomefourthlastyear =  models.CharField(max_length=170, default='')
    urlcomprehensiveincomefifthlastyear =  models.CharField(max_length=170, default='')
    urlcomprehensiveincomesixthlastyear =  models.CharField(max_length=170, default='')
    #
    urlshareholdersequitylastyear =  models.CharField(max_length=170, default='')
    urlshareholdersequitysecondlastyear =  models.CharField(max_length=170, default='')
    urlshareholdersequitythirdlastyear =  models.CharField(max_length=170, default='')
    urlshareholdersequityfourthlastyear =  models.CharField(max_length=170, default='')
    urlshareholdersequityfifthlastyear =  models.CharField(max_length=170, default='')
    urlshareholdersequitysixthlastyear =  models.CharField(max_length=170, default='')
    #
    urlcashflowlastyear =  models.CharField(max_length=170, default='')
    urlcashflowsecondlastyear =  models.CharField(max_length=170, default='')
    urlcashflowthirdlastyear =  models.CharField(max_length=170, default='')
    urlcashflowfourthlastyear =  models.CharField(max_length=170, default='')
    urlcashflowfifthlastyear =  models.CharField(max_length=170, default='')
    urlcashflowsixthlastyear =  models.CharField(max_length=170, default='')
    #
    urlsauditlastyear = models.IntegerField(default=0)
    urlsauditsecondlastyear = models.IntegerField(default=0)
    urlsauditthirdlastyear = models.IntegerField(default=0)
    urlsauditfourthlastyear = models.IntegerField(default=0)
    urlsauditfifthlastyear = models.IntegerField(default=0)
    urlsauditsixthlastyear = models.IntegerField(default=0)
    #
    def __str__(self):
        return f"{self.TradingSymbol}"

class AuditData(models.Model):
    #
    # General - Audit
    #
    db = models.IntegerField(default=0)
    AccessionNumber = models.CharField(max_length=20, default='')
    AmendmentFlag = models.CharField(max_length=5, default=0)
    EntityRegistrantName = models.CharField(max_length=93)
    Period = models.CharField(max_length=27, default=0)
    PeriodEndDate = models.DateField(null=True)
    TradingSymbol = models.CharField(max_length=13, default=0)
    #
    # Balance Sheets - Audit
    #
    CurrentAssets = models.BigIntegerField(default=0)
    NonCurrentAssets = models.BigIntegerField(default=0)
    Assets = models.BigIntegerField(default=0)
    CurrentLiabilities = models.BigIntegerField(default=0)
    NonCurrentLiabilities = models.BigIntegerField(default=0)
    Liabilities = models.BigIntegerField(default=0)
    ShareholdersEquity = models.BigIntegerField(default=0)
    LiabilitiesAndShareholdersEquity = models.BigIntegerField(default=0)
    #
    CurrentAssetsGL_i = models.CharField(max_length=180, default='')
    CurrentAssetsGL_ii = models.CharField(max_length=180, default='')
    CurrentAssetsGL_iii = models.CharField(max_length=180, default='')
    AnomalyCurrentAssets = models.BigIntegerField(default=0)
    AnomalyCurrentAssetsSEC = models.BigIntegerField(default=0)
    #
    NonCurrentAssetsGL_i = models.CharField(max_length=180, default='')
    NonCurrentAssetsGL_ii = models.CharField(max_length=180, default='')
    NonCurrentAssetsGL_iii = models.CharField(max_length=180, default='')
    AnomalyNonCurrentAssets = models.BigIntegerField(default=0)
    AnomalyNonCurrentAssetsSEC = models.BigIntegerField(default=0)
    #
    AnomalyAssets = models.BigIntegerField(default=0)
    #
    CurrentLiabilitiesGL_i = models.CharField(max_length=180, default='')
    CurrentLiabilitiesGL_ii = models.CharField(max_length=180, default='')
    CurrentLiabilitiesGL_iii = models.CharField(max_length=180, default='')
    AnomalyCurrentLiabilities = models.BigIntegerField(default=0)
    AnomalyCurrentLiabilitiesSEC = models.BigIntegerField(default=0)
    #
    NonCurrentLiabilitiesGL_i = models.CharField(max_length=180, default='')
    NonCurrentLiabilitiesGL_ii = models.CharField(max_length=180, default='')
    NonCurrentLiabilitiesGL_iii = models.CharField(max_length=180, default='')
    AnomalyNonCurrentLiabilities = models.BigIntegerField(default=0)
    AnomalyNonCurrentLiabilitiesSEC = models.BigIntegerField(default=0)
    #
    AnomalyLiabilities = models.BigIntegerField(default=0)
    AnomalyShareholdersEquity = models.BigIntegerField(default=0)
    #
    ShareholdersEquityBalanceGL_i = models.CharField(max_length=180, default='')
    ShareholdersEquityBalanceGL_ii = models.CharField(max_length=180, default='')
    ShareholdersEquityBalanceGL_iii = models.CharField(max_length=180, default='')
    AnomalyShareholdersEquitySEC = models.BigIntegerField(default=0)
    AnomalyLiabilitiesAndShareholdersEquity = models.BigIntegerField(default=0)
    #
    #
    # Income Statements - Audit
    #
    Sales = models.BigIntegerField(default=0)
    CostOfSales = models.BigIntegerField(default=0)
    GrossMargin = models.BigIntegerField(default=0)
    OperatingExpenses = models.BigIntegerField(default=0)
    OperatingIncome = models.BigIntegerField(default=0)
    IncomeBeforeTaxes = models.BigIntegerField(default=0)
    NetIncome = models.BigIntegerField(default=0)
    NetIncomeAttributableToNonControllingInterest = models.BigIntegerField(default=0)
    #
    GrossMarginGL_i = models.CharField(max_length=180, default='')
    GrossMarginGL_ii = models.CharField(max_length=180, default='')
    GrossMarginGL_iii = models.CharField(max_length=180, default='')
    #
    AnomalyGrossMargin = models.BigIntegerField(default=0)
    #
    OperatingExpensesGL_i = models.CharField(max_length=180, default='')
    OperatingExpensesGL_ii = models.CharField(max_length=180, default='')
    OperatingExpensesGL_iii = models.CharField(max_length=180, default='')
    #
    AnomalyOperatingExpenses = models.BigIntegerField(default=0)
    #
    OperatingIncomeGL_i = models.CharField(max_length=180, default='')
    OperatingIncomeGL_ii = models.CharField(max_length=180, default='')
    OperatingIncomeGL_iii = models.CharField(max_length=180, default='')
    #
    AnomalyOperatingIncome = models.BigIntegerField(default=0)
    #
    IncomeBeforeTaxesGL_i = models.CharField(max_length=180, default='')
    IncomeBeforeTaxesGL_ii = models.CharField(max_length=180, default='')
    IncomeBeforeTaxesGL_iii = models.CharField(max_length=180, default='')
    #
    AnomalyIncomeBeforeTaxes = models.BigIntegerField(default=0)
    #
    NetIncomeGL_i = models.CharField(max_length=180, default='')
    NetIncomeGL_ii = models.CharField(max_length=180, default='')
    NetIncomeGL_iii = models.CharField(max_length=180, default='')
    #
    AnomalyNetIncome = models.BigIntegerField(default=0)
    #
    #
    # Comprehensive Income - Audit
    #
    OtherComprehensiveIncome = models.BigIntegerField(default=0)
    ComprehensiveIncome = models.BigIntegerField(default=0)
    #
    OtherComprehensiveIncomeGL_i = models.CharField(max_length=180, default='')
    OtherComprehensiveIncomeGL_ii = models.CharField(max_length=180, default='')
    OtherComprehensiveIncomeGL_iii = models.CharField(max_length=180, default='')
    AnomalyOtherComprehensiveIncome = models.BigIntegerField(default=0)
    AnomalyComprehensiveIncome = models.BigIntegerField(default=0)
    #
    #
    # Shareholders Equity - Audit
    #
    ShareholdersEquityBeginning = models.BigIntegerField(default=0)
    #
    ConvertibleDebt = models.BigIntegerField(default=0)
    CommonShares = models.BigIntegerField(default=0)
    PreferredShares = models.BigIntegerField(default=0)
    RetainedEarnings = models.BigIntegerField(default=0)
    AccumulatedOtherComprehensiveIncome = models.BigIntegerField(default=0)
    TreasuryShares = models.BigIntegerField(default=0)
    EmployeeBenefitTrust = models.BigIntegerField(default=0)
    NonControllingInterests = models.BigIntegerField(default=0)
    #
    AnomalyConvertibleDebt = models.BigIntegerField(default=0)
    #
    AnomalyCommonShares = models.BigIntegerField(default=0)
    #
    AnomalyPreferredShares = models.BigIntegerField(default=0)
    #
    AnomalyRetainedEarnings = models.BigIntegerField(default=0)
    #
    AnomalyAccumulatedOtherComprehensiveIncome = models.BigIntegerField(default=0)
    #
    AnomalyTreasuryShares = models.BigIntegerField(default=0)
    #
    AnomalyEmployeeBenefitTrust = models.BigIntegerField(default=0)
    #
    AnomalyNonControllingInterests = models.BigIntegerField(default=0)
    #
    ShareholdersEquityGL_i = models.CharField(max_length=180, default='')
    ShareholdersEquityGL_ii = models.CharField(max_length=180, default='')
    ShareholdersEquityGL_iii = models.CharField(max_length=180, default='')
    #
    #
    # Cash Flow - Audit
    #
    OperatingActivities = models.BigIntegerField(default=0)
    InvestingActivities = models.BigIntegerField(default=0)
    FinancingActivities = models.BigIntegerField(default=0)
    IncreaseDecreaseInCash = models.BigIntegerField(default=0)
    #
    CashFlowCashExplainedDifference = models.BigIntegerField(default=0)
    #
    OperatingActivitiesGL_i = models.CharField(max_length=180, default='')
    OperatingActivitiesGL_ii = models.CharField(max_length=180, default='')
    OperatingActivitiesGL_iii = models.CharField(max_length=180, default='')
    AnomalyOperatingActivities = models.BigIntegerField(default=0)
    AnomalyOperatingActivitiesSEC = models.BigIntegerField(default=0)
    #
    InvestingActivitiesGL_i = models.CharField(max_length=180, default='')
    InvestingActivitiesGL_ii = models.CharField(max_length=180, default='')
    InvestingActivitiesGL_iii = models.CharField(max_length=180, default='')
    AnomalyInvestingActivities = models.BigIntegerField(default=0)
    AnomalyInvestingActivitiesSEC = models.BigIntegerField(default=0)
    #
    FinancingActivitiesGL_i = models.CharField(max_length=180, default='')
    FinancingActivitiesGL_ii = models.CharField(max_length=180, default='')
    FinancingActivitiesGL_iii = models.CharField(max_length=180, default='')
    AnomalyFinancingActivities = models.BigIntegerField(default=0)
    AnomalyFinancingActivitiesSEC = models.BigIntegerField(default=0)
    #
    #
    # Supplemental - Audit
    #
    TargetWorkingCapital = models.FloatField(default=1.2)
    ReinvestmentOfMaintenance = models.BigIntegerField(default=0)
    NormalizedDividendPaymentToNonControllingInterests = models.BigIntegerField(default=0)
    NormalizedDividendPaymentToPreferredShareholders = models.BigIntegerField(default=0)
    TheoricalInterestRate = models.FloatField(default=0.035)
    TheoricalTaxRate = models.FloatField(default=0.25)
    CapitalizationRateFloor = models.FloatField(default=0.021)
    #
    #
    def __str__(self):
        return f"{self.TradingSymbol}:{self.Period}"

class CashFlow(models.Model):
    #
    # General - Cash Flow
    #
    AccessionNumber = models.CharField(max_length=20, default='')
    AmendmentFlag = models.CharField(max_length=5, default=0)
    EntityRegistrantName = models.CharField(max_length=93)
    Period = models.CharField(max_length=27, default=0)
    PeriodEndDate = models.DateField(null=True)
    TradingSymbol = models.CharField(max_length=13, default=0)
    #
    # Cash - Cash Flow
    #
    CashBeginningBalance = models.BigIntegerField(default=0)
    EffectOfExchangeRateOnCash = models.BigIntegerField(default=0)
    #
    # Operating Activities - Cash Flow
    #
    DepreciationDepletionAndAmortization = models.BigIntegerField(default=0)
    GainRelatedToDisposalOrSale = models.BigIntegerField(default=0)
    RestructuringAndOtherSpecialCharges = models.BigIntegerField(default=0)
    AccruedEmployeeCompensation = models.BigIntegerField(default=0)
    ShareBasedCompensation = models.BigIntegerField(default=0)
    IncreaseDecreaseInIncomeTaxExpenseBenefit = models.BigIntegerField(default=0)
    OtherNonCashIncomeExpense = models.BigIntegerField(default=0)
    IncreaseDecreaseInAccountsReceivable = models.BigIntegerField(default=0)
    IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets = models.BigIntegerField(default=0)
    IncreaseDecreaseInInventories = models.BigIntegerField(default=0)
    IncreaseDecreaseInOtherReceivables = models.BigIntegerField(default=0)
    IncreaseDecreaseInAccountsPayableAndAccruedLiabilities = models.BigIntegerField(default=0)
    IncreaseDecreaseInContractWithCustomerLiability = models.BigIntegerField(default=0)
    IncreaseDecreaseInRetirementBenefits = models.BigIntegerField(default=0)
    IncreaseDecreaseFinanceLeaseCurrent = models.BigIntegerField(default=0)
    IncreaseDecreaseOperatingLeaseCurrent = models.BigIntegerField(default=0)
    IncreaseDecreaseInFairValueOfDerivativesOperating = models.BigIntegerField(default=0)
    IncreaseDecreaseInOtherOperatingActivities = models.BigIntegerField(default=0)
    #
    # Investing Activities - Cash Flow
    #
    PaymentsToAcquireInvestments = models.BigIntegerField(default=0)
    ProceedsOfInvestments = models.BigIntegerField(default=0)
    PaymentsToAcquirePropertyPlantAndEquipment = models.BigIntegerField(default=0)
    ProceedsFromDisposalsOfPropertyAndEquipment = models.BigIntegerField(default=0)
    PaymentsToAcquireBusinessesAndIntangibles = models.BigIntegerField(default=0)
    ProceedsFromDisposalsOfBusinessesAndIntangibles = models.BigIntegerField(default=0)
    ProceedsRelatedToInsuranceSettlement = models.BigIntegerField(default=0)
    ReveiptOfGovernmentGrants = models.BigIntegerField(default=0)
    PaymentOfLicenseFee = models.BigIntegerField(default=0)
    InvestingActivitiesInDiscontinuedOperations = models.BigIntegerField(default=0)
    OtherInvestingActivities = models.BigIntegerField(default=0)
    #
    # Financing Activities - Cash Flow
    #
    FinanceLeasePrincipalPayments = models.BigIntegerField(default=0)
    ProceedsFromIssuanceOfCommonShares = models.BigIntegerField(default=0)
    ProceedsFromSharePurchasePlanAndOptionsExercice = models.BigIntegerField(default=0)
    PaymentsRelatedToTaxWithholdingForShareBasedCompensation = models.BigIntegerField(default=0)
    PaymentsForRepurchaseOfCommonShares = models.BigIntegerField(default=0)
    PaymentsOfDividends = models.BigIntegerField(default=0)
    IncreaseDecreaseDeferredContingentConsideration = models.BigIntegerField(default=0)
    ProceedsFromIssuanceOfLongTermDebt = models.BigIntegerField(default=0)
    RepaymentsOfLongTermDebt = models.BigIntegerField(default=0)
    FinancingCosts = models.BigIntegerField(default=0)
    NetChangeInShortTermBorrowings = models.BigIntegerField(default=0)
    NetChangeInForwardAndHedgesClassifiedAsFinancingActivities = models.BigIntegerField(default=0)
    NetChangeInNonControllingInterests = models.BigIntegerField(default=0)
    ProceedsFromRepaymentsOfCommercialPaper = models.BigIntegerField(default=0)
    RepaymentsOfConvertible = models.BigIntegerField(default=0)
    IssuanceOfConvertible = models.BigIntegerField(default=0)
    EquityInvesteeAdvancesRepayments = models.BigIntegerField(default=0)
    OtherFinancingActivities = models.BigIntegerField(default=0)
    #
    # Supplemental - Cash Flow
    #
    CashPaidForTaxes = models.BigIntegerField(default=0)
    CashPaidForInterest = models.BigIntegerField(default=0)
    #
    #
    def __str__(self):
        return f"{self.TradingSymbol}:{self.Period}"

class TrialBalance(models.Model):
    #
    #
    # General - Trial Balance
    #
    AccessionNumber = models.CharField(max_length=20, default='')
    AmendmentFlag = models.CharField(max_length=5, default=0)
    EntityRegistrantName = models.CharField(max_length=93)
    Link = models.CharField(max_length=360, default=0)
    Period = models.CharField(max_length=27, default=0)
    PeriodEndDate = models.DateField(null=True)
    PeriodOfReport = models.CharField(max_length=13, default=0)
    TradingSymbol = models.CharField(max_length=13, default=0)
    #
    #
    # Current Assets - Trial Balance
    #
    Cash = models.BigIntegerField(default=0)
    ShortTermInvestments = models.BigIntegerField(default=0)
    AccountsReceivable = models.BigIntegerField(default=0)
    WorkInProgress = models.BigIntegerField(default=0)
    Inventories = models.BigIntegerField(default=0)
    PrepaidExpenses = models.BigIntegerField(default=0)
    NonTradeReceivables = models.BigIntegerField(default=0)
    PrepaidTaxAssetsCurrent = models.BigIntegerField(default=0)
    DeferredTaxAssetsCurrent = models.BigIntegerField(default=0)
    RightOfUseAssetsCurrent = models.BigIntegerField(default=0)
    OtherCurrentAssets = models.BigIntegerField(default=0)
    DiscontinuedOperationsCurrent = models.BigIntegerField(default=0)
    #
    #
    # Non-Current Assets - Trial Balance
    #
    LongTermReceivables = models.BigIntegerField(default=0)
    DeferredCharges = models.BigIntegerField(default=0)
    Investments = models.BigIntegerField(default=0)
    PropertyPlantAndEquipment = models.BigIntegerField(default=0)
    OperatingLeaseRightOfUseAssets = models.BigIntegerField(default=0)
    FinanceLeaseRightOfUseAssets = models.BigIntegerField(default=0)
    IntangibleAssets = models.BigIntegerField(default=0)
    Goodwill = models.BigIntegerField(default=0)
    RefundableTaxAssetsNonCurrent = models.BigIntegerField(default=0)
    DeferredTaxAssetsNonCurrent = models.BigIntegerField(default=0)
    DefinedBenefitPensionAndOtherSimilarPlans = models.BigIntegerField(default=0)
    OtherNonCurrentAssets = models.BigIntegerField(default=0)
    DiscontinuedOperations = models.BigIntegerField(default=0)
    #
    #
    # Current Liabilities - Trial Balance
    #
    AccountsPayableAndAccruedLiabilities = models.BigIntegerField(default=0)
    EmployeeCompensationCurrent = models.BigIntegerField(default=0)
    OperatingLeasesCurrent = models.BigIntegerField(default=0)
    FinanceLeasesCurrent = models.BigIntegerField(default=0)
    DeferredRevenueAndDepositsCurrent = models.BigIntegerField(default=0)
    AccruedTaxLiabilities = models.BigIntegerField(default=0)
    DeferredTaxLiabilitiesCurrent = models.BigIntegerField(default=0)
    CommercialPapers = models.BigIntegerField(default=0)
    ShortTermBorrowings = models.BigIntegerField(default=0)
    OtherCurrentLiabilities = models.BigIntegerField(default=0)
    DiscontinuedOperationsLiabilitiesCurrent = models.BigIntegerField(default=0)
    DividendsPayable = models.BigIntegerField(default=0)
    ShortTermPortionOfLongTermDebt = models.BigIntegerField(default=0)
    #
    #
    # Non-Current Liabilities - Trial Balance
    #
    LongTermDebt = models.BigIntegerField(default=0)
    PreferredSharesLiability = models.BigIntegerField(default=0)
    RetirementBenefits = models.BigIntegerField(default=0)
    OperatingLeasesNonCurrent = models.BigIntegerField(default=0)
    FinanceLeasesNonCurrent = models.BigIntegerField(default=0)
    LeaseIncentiveObligation = models.BigIntegerField(default=0)
    DeferredRevenueAndDepositsNonCurrent = models.BigIntegerField(default=0)
    ContingentConsideration = models.BigIntegerField(default=0)
    AccruedTaxLiabilitiesNonCurrent = models.BigIntegerField(default=0)
    DeferredTaxLiabilitiesNonCurrent = models.BigIntegerField(default=0)
    OtherNonCurrentLiabilities = models.BigIntegerField(default=0)
    RedeemableNonControllingInterests = models.BigIntegerField(default=0)
    DiscontinuedOperationsLiabilitiesNonCurrent = models.BigIntegerField(default=0)
    #
    #
    # Shareholders Equity - Trial Balance
    #
    # convertible debt
    ConvertibleDebtBeginning = models.BigIntegerField(default=0)
    #
    # common shares
    CommonSharesBeginning = models.BigIntegerField(default=0)
    CommonSharesIssued = models.BigIntegerField(default=0)
    ShareBasedCompensation = models.BigIntegerField(default=0)
    #
    # preferred shares
    PreferredSharesBeginning = models.BigIntegerField(default=0)
    #
    # retained earnings
    RetainedEarningsBeginning = models.BigIntegerField(default=0)
    DividendsAndDividendEquivalentsDeclared = models.BigIntegerField(default=0)
    CommonSharesRepurchasedAndRetired = models.BigIntegerField(default=0)
    ShareBasedCompensationRetainedEarnings = models.BigIntegerField(default=0)
    EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts = models.BigIntegerField(default=0)
    RetainedEarningsOthers = models.BigIntegerField(default=0)
    #
    # accumulated other comprehensive income
    AccumulatedOtherComprehensiveIncomeBeginning = models.BigIntegerField(default=0)
    #
    # treasury shares
    TreasurySharesBeginning = models.BigIntegerField(default=0)
    PurchaseAndSellOfTreasuryShares = models.BigIntegerField(default=0)
    #
    # employee benefit trust
    EmployeeBenefitTrustBeginning = models.BigIntegerField(default=0)
    #
    # non controlling interests
    NonControllingInterestsBeginning = models.BigIntegerField(default=0)
    DividendsDeclaredToNonControllingInterests = models.BigIntegerField(default=0)
    AcquisitionOfNonControllingInterests = models.BigIntegerField(default=0)
    NonControllingInterestsOthers = models.BigIntegerField(default=0)
    #
    #
    # Income Statements - Trial Balance
    #
    Sales = models.BigIntegerField(default=0)
    CostOfSales = models.BigIntegerField(default=0)
    ResearchAndDevelopment = models.BigIntegerField(default=0)
    SellingGeneralAdministrativeAndMarketing = models.BigIntegerField(default=0)
    ImpairmentRestructuringAndOtherSpecialCharges = models.BigIntegerField(default=0)
    NonOperatingIncome = models.BigIntegerField(default=0)
    IncomeTaxExpenseBenefit = models.BigIntegerField(default=0)
    EquityMethodInvesteesIncome = models.BigIntegerField(default=0)
    NetIncomeFromDiscontinuedOperations = models.BigIntegerField(default=0)
    #
    #
    # Other Comprehensive Income - Trial Balance
    #
    ChangeInForeignCurrencyTranslationAdjustment = models.BigIntegerField(default=0)
    ChangeInUnrealizedGainsLossesOnDerivativeInstruments = models.BigIntegerField(default=0)
    ChangeInUnrealizedGainsLossesOnInvestments = models.BigIntegerField(default=0)
    ChangeInDefinedBenefitPensionAndOtherSimilarPlans = models.BigIntegerField(default=0)
    IncomeTaxOnOtherComprehensiveIncome = models.BigIntegerField(default=0)
    #
    #
    def __str__(self):
        return f"{self.TradingSymbol}:{self.Period}"
