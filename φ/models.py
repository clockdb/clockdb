
from django.db import models   


class Auditor(models.Model):
    #
    Name = models.CharField(max_length=93)
    Number = models.CharField(max_length=93)
    URL = models.CharField(max_length=93)
    #
    def __str__(self):
        return f"{self.Name}"

class Entity(models.Model):
    #
    EntityRegistrantName = models.CharField(max_length=93)
    TradingSymbol = models.CharField(max_length=7, null=False, unique=True)
    EntityCentralIndexKey = models.CharField(max_length=10)
    Industry = models.CharField(max_length=61)
    EntityIncorporationStateCountryCode = models.CharField(max_length=44)
    Region = models.CharField(max_length=44)
    CurrentFiscalYearEndDate = models.CharField(max_length=13, default=0)
    SecurityExchangeName = models.CharField(max_length=55, default=0)
    Regulator = models.CharField(max_length=3)
    Update = models.CharField(max_length=13, default=0)
    Clockφ = models.IntegerField(default=0)
    ClockφChange = models.IntegerField(default=0)
    Bridgeφ = models.CharField(max_length=100, default=0)
    Status = models.CharField(max_length=100, default=0)
    StockPrice = models.IntegerField(default=0)
    Anomalies = models.CharField(max_length=100, default=0)
    #
    lastquarter = models.CharField(max_length=13, default=0)
    secondlastquarter = models.CharField(max_length=13, default=0)
    thirdlastquarter = models.CharField(max_length=13, default=0)
    fourthlastquarter = models.CharField(max_length=13, default=0)
    #
    lastyear = models.CharField(max_length=13, default=0)
    secondlastyear = models.CharField(max_length=13, default=0)
    thirdlastyear = models.CharField(max_length=13, default=0)
    fourthlastyear = models.CharField(max_length=13, default=0)
    fifthlastyear = models.CharField(max_length=13, default=0)
    sixthlastyear = models.CharField(max_length=13, default=0)
    seventhlastyear = models.CharField(max_length=13, default=0)
    eighthlastyear = models.CharField(max_length=13, default=0)
    #
    def __str__(self):
        return f"{self.TradingSymbol}"


class AuditData(models.Model):
    #
    # General - Audit
    #
    EntityRegistrantName = models.CharField(max_length=93)
    TradingSymbol = models.CharField(max_length=13, default=0)
    AmendmentFlag = models.CharField(max_length=5, default=0)
    CurrentFiscalYearEndDate = models.CharField(max_length=7, default=0)
    DocumentFiscalPeriodFocus = models.CharField(max_length=2, default=0)
    DocumentFiscalYearFocus = models.CharField(max_length=4, default=0)
    DocumentPeriodEndDate = models.CharField(max_length=13, default=0)
    Period = models.CharField(max_length=13, default=0)
    #
    # Balance Sheets - Audit
    #
    CurrentAssets = models.IntegerField(default=0)
    NonCurrentAssets = models.IntegerField(default=0)
    Assets = models.IntegerField(default=0)
    CurrentLiabilities = models.IntegerField(default=0)
    NonCurrentLiabilities = models.IntegerField(default=0)
    Liabilities = models.IntegerField(default=0)
    StockholdersEquity = models.IntegerField(default=0)
    LiabilitiesAndStockholdersEquity = models.IntegerField(default=0)
    #
    AnomalyCurrentAssets = models.IntegerField(default=0)
    AnomalyCurrentAssetsSEC = models.IntegerField(default=0)
    AnomalyNonCurrentAssets = models.IntegerField(default=0)
    AnomalyNonCurrentAssetsSEC = models.IntegerField(default=0)
    AnomalyAssets = models.IntegerField(default=0)
    AnomalyCurrentLiabilities = models.IntegerField(default=0)
    AnomalyCurrentLiabilitiesSEC = models.IntegerField(default=0)
    AnomalyNonCurrentLiabilities = models.IntegerField(default=0)
    AnomalyNonCurrentLiabilitiesSEC = models.IntegerField(default=0)
    AnomalyLiabilities = models.IntegerField(default=0)
    AnomalyStockholdersEquity = models.IntegerField(default=0)
    AnomalyStockholdersEquitySEC = models.IntegerField(default=0)
    AnomalyLiabilitiesAndStockholdersEquity = models.IntegerField(default=0)
    #
    #
    # Income Statements - Audit
    #
    Sales = models.IntegerField(default=0)
    CostOfSales = models.IntegerField(default=0)
    GrossMargin = models.IntegerField(default=0)
    OperatingExpenses = models.IntegerField(default=0)
    OperatingIncome = models.IntegerField(default=0)
    IncomeBeforeTaxes = models.IntegerField(default=0)
    NetIncome = models.IntegerField(default=0)
    NetIncomeAttributableToNonControllingInterest = models.IntegerField(default=0)
    #
    AnomalyGrossMargin = models.IntegerField(default=0)
    AnomalyOperatingExpenses = models.IntegerField(default=0)
    AnomalyOperatingIncome = models.IntegerField(default=0)
    AnomalyIncomeBeforeTaxes = models.IntegerField(default=0)
    AnomalyNetIncome = models.IntegerField(default=0)
    #
    #
    # Comprehensive Income - Audit
    #
    OtherComprehensiveIncome = models.IntegerField(default=0)
    ComprehensiveIncome = models.IntegerField(default=0)
    #
    AnomalyOtherComprehensiveIncome = models.IntegerField(default=0)
    AnomalyComprehensiveIncome = models.IntegerField(default=0)
    #
    #
    # Stockholders Equity - Audit
    #
    StockholdersEquityBeginning = models.IntegerField(default=0)
    #
    CommonShares = models.IntegerField(default=0)
    RetainedEarnings = models.IntegerField(default=0)
    AccumulatedOtherComprehensiveIncome = models.IntegerField(default=0)
    TreasuryShares = models.IntegerField(default=0)
    EmployeeBenefitTrust = models.IntegerField(default=0)
    NonControllingInterests = models.IntegerField(default=0)
    #
    AnomalyCommonShares = models.IntegerField(default=0)
    AnomalyRetainedEarnings = models.IntegerField(default=0)
    AnomalyAccumulatedOtherComprehensiveIncome = models.IntegerField(default=0)
    AnomalyTreasuryShares = models.IntegerField(default=0)
    AnomalyEmployeeBenefitTrust = models.IntegerField(default=0)
    AnomalyNonControllingInterests = models.IntegerField(default=0)
    #
    #
    # Cash Flow - Audit
    #
    OperatingActivities = models.IntegerField(default=0)
    InvestingActivities = models.IntegerField(default=0)
    FinancingActivities = models.IntegerField(default=0)
    #
    AnomalyOperatingActivities = models.IntegerField(default=0)
    AnomalyOperatingActivitiesSEC = models.IntegerField(default=0)
    AnomalyInvestingActivities = models.IntegerField(default=0)
    AnomalyInvestingActivitiesSEC = models.IntegerField(default=0)
    AnomalyFinancingActivities = models.IntegerField(default=0)
    AnomalyFinancingActivitiesSEC = models.IntegerField(default=0)
    #
    #
    # Supplemental - Audit
    #
    MarketCapitalization = models.IntegerField(default=0)
    EntityCommonStockSharesOutstanding = models.IntegerField(default=0)
    StockPrice = models.FloatField(default=0)
    #
    NormalizedTheoricalInterestCharge = models.IntegerField(default=0)
    TheoricalTaxRate = models.FloatField(default=0)
    TheoricalOperatingIncomeAttributableToNonControllingInterests = models.FloatField(default=0) 
    #
    #
    def __str__(self):
        return f"{self.TradingSymbol}:{self.Period}"


class CashFlow(models.Model):
    #
    # General - Cash Flow
    #
    EntityRegistrantName = models.CharField(max_length=93)
    TradingSymbol = models.CharField(max_length=13, default=0)
    AmendmentFlag = models.CharField(max_length=5, default=0)
    CurrentFiscalYearEndDate = models.CharField(max_length=7, default=0)
    DocumentFiscalPeriodFocus = models.CharField(max_length=2, default=0)
    DocumentFiscalYearFocus = models.CharField(max_length=4, default=0)
    DocumentPeriodEndDate = models.CharField(max_length=13, default=0)
    Period = models.CharField(max_length=13, default=0)
    #
    # Cash - Cash Flow
    #
    CashBeginningBalance = models.IntegerField(default=0)
    EffectOfExchangeRateOnCash = models.IntegerField(default=0)
    #
    # Operating Activities - Cash Flow
    #
    DepreciationDepletionAndAmortization = models.IntegerField(default=0)
    GainRelatedToDisposalOrSale = models.IntegerField(default=0)
    RestructuringAndOtherSpecialCharges = models.IntegerField(default=0)
    AccruedEmployeeCompensation = models.IntegerField(default=0)
    ShareBasedCompensation = models.IntegerField(default=0)
    IncreaseDecreaseInIncomeTaxExpenseBenefit = models.IntegerField(default=0)
    OtherNonCashIncomeExpense = models.IntegerField(default=0)
    IncreaseDecreaseInAccountsReceivable = models.IntegerField(default=0)
    IncreaseDecreaseInInventories = models.IntegerField(default=0)
    IncreaseDecreaseInPrepaidDeferredExpenseAndOtherAssets = models.IntegerField(default=0)
    IncreaseDecreaseInOtherReceivables = models.IntegerField(default=0)
    IncreaseDecreaseInAccountsPayableAndAccruedLiabilities = models.IntegerField(default=0)
    IncreaseDecreaseInContractWithCustomerLiability = models.IntegerField(default=0)
    IncreaseDecreaseOperatingLeaseCurrent = models.IntegerField(default=0)
    IncreaseDecreaseInOtherOperatingActivities = models.IntegerField(default=0)
    #
    # Investing Activities - Cash Flow
    #
    PaymentsToAcquireInvestments = models.IntegerField(default=0)
    ProceedsOfInvestments = models.IntegerField(default=0)
    PaymentsToAcquirePropertyPlantAndEquipment = models.IntegerField(default=0)
    ProceedsFromDisposalsOfPropertyAndEquipment = models.IntegerField(default=0)
    PaymentsToAcquireBusinessesAndIntangibles = models.IntegerField(default=0)
    ProceedsFromDisposalsOfBusinessesAndIntangibles = models.IntegerField(default=0)
    ReveiptOfGovernmentGrants = models.IntegerField(default=0)
    OtherInvestingActivities = models.IntegerField(default=0)
    #
    # Financing Activities - Cash Flow
    #
    FinanceLeasePrincipalPayments = models.IntegerField(default=0)
    ProceedsFromIssuanceOfCommonStock = models.IntegerField(default=0)
    ProceedsFromStockOptionExercices = models.IntegerField(default=0)
    PaymentsRelatedToTaxWithholdingForShareBasedCompensation = models.IntegerField(default=0)
    PaymentsForRepurchaseOfCommonStock = models.IntegerField(default=0)
    PaymentsOfDividends = models.IntegerField(default=0)
    PaymentsForTaxesRelatedToNetShareSettlementOfEquityAward = models.IntegerField(default=0)
    ProceedsFromIssuanceOfLongTermDebt = models.IntegerField(default=0)
    RepaymentsOfLongTermDebt = models.IntegerField(default=0)
    NetChangeInShortTermBorrowings = models.IntegerField(default=0)
    ProceedsFromRepaymentsOfCommercialPaper = models.IntegerField(default=0)
    RepaymentsOfConvertible = models.IntegerField(default=0)
    IssuanceOfConvertible = models.IntegerField(default=0)
    OtherFinancingActivities = models.IntegerField(default=0)
    #
    # Supplemental - Cash Flow
    #
    CashPaidForTaxes = models.IntegerField(default=0)
    CashPaidForInterest = models.IntegerField(default=0)
    #
    #
    def __str__(self):
        return f"{self.TradingSymbol}:{self.Period}"


class TrialBalance(models.Model):
    #
    #
    # General - Trial Balance
    #
    EntityRegistrantName = models.CharField(max_length=93)
    TradingSymbol = models.CharField(max_length=13, default=0)
    AmendmentFlag = models.CharField(max_length=5, default=0)
    CurrentFiscalYearEndDate = models.CharField(max_length=7, default=0)
    DocumentFiscalPeriodFocus = models.CharField(max_length=2, default=0)
    DocumentFiscalYearFocus = models.CharField(max_length=4, default=0)
    DocumentPeriodEndDate = models.CharField(max_length=13, default=0)
    PeriodOfReport = models.CharField(max_length=13, default=0)
    NumberOfDays = models.IntegerField(default=0)
    FilingDate = models.CharField(max_length=13, default=0)
    Period = models.CharField(max_length=13, default=0)
    Link = models.CharField(max_length=360, default=0)
    #
    #
    # Current Assets - Trial Balance
    #
    Cash = models.IntegerField(default=0)
    ShortTermInvestments = models.IntegerField(default=0)
    AccountsReceivable = models.IntegerField(default=0)
    Inventories = models.IntegerField(default=0)
    PrepaidExpenses = models.IntegerField(default=0)
    NonTradeReceivables = models.IntegerField(default=0)
    DeferredTaxAssetsCurrent = models.IntegerField(default=0)
    OtherCurrentAssets = models.IntegerField(default=0)
    DiscontinuedOperationsCurrent = models.IntegerField(default=0)
    #
    #
    # Non-Current Assets - Trial Balance
    #
    LongTermReceivables = models.IntegerField(default=0)
    DeferredCharges = models.IntegerField(default=0)
    Investments = models.IntegerField(default=0)
    PropertyPlantAndEquipment = models.IntegerField(default=0)
    OperatingLeaseRightOfUseAssets = models.IntegerField(default=0)
    FinanceLeaseRightOfUseAssets = models.IntegerField(default=0)
    IntangibleAssets = models.IntegerField(default=0)
    Goodwill = models.IntegerField(default=0)
    DeferredTaxAssetsNonCurrent = models.IntegerField(default=0)
    DefinedBenefitPensionAndOtherSimilarPlans = models.IntegerField(default=0)
    OtherNonCurrentAssets = models.IntegerField(default=0)
    DiscontinuedOperations = models.IntegerField(default=0)
    #
    #
    # Current Liabilities - Trial Balance
    #
    AccountsPayableAndAccruedLiabilities = models.IntegerField(default=0)
    EmployeeCompensationCurrent = models.IntegerField(default=0)
    OperatingLeasesCurrent = models.IntegerField(default=0)
    FinanceLeasesCurrent = models.IntegerField(default=0)
    CapitalLeaseAndFinancingObligationsCurrent = models.IntegerField(default=0)
    DeferredRevenueAndDepositsCurrent = models.IntegerField(default=0)
    AccruedTaxLiabilities = models.IntegerField(default=0)
    DeferredTaxLiabilitiesCurrent = models.IntegerField(default=0)
    CommercialPapers = models.IntegerField(default=0)
    ShortTermBorrowings = models.IntegerField(default=0)
    OtherCurrentLiabilities = models.IntegerField(default=0)
    DiscontinuedOperationsLiabilitiesCurrent = models.IntegerField(default=0)
    DividendsPayable = models.IntegerField(default=0)
    ShortTermPortionOfLongTermDebt = models.IntegerField(default=0)
    #
    #
    # Non-Current Liabilities - Trial Balance
    #
    LongTermDebt = models.IntegerField(default=0)
    RetirementBenefits = models.IntegerField(default=0)
    OperatingLeasesNonCurrent = models.IntegerField(default=0)
    FinanceLeasesNonCurrent = models.IntegerField(default=0)
    CapitalLeaseAndFinancingObligationsNonCurrent = models.IntegerField(default=0)
    DeferredRevenueAndDepositsNonCurrent = models.IntegerField(default=0)
    AccruedTaxLiabilitiesNonCurrent = models.IntegerField(default=0)
    DeferredTaxLiabilitiesNonCurrent = models.IntegerField(default=0)
    OtherNonCurrentLiabilities = models.IntegerField(default=0)
    DiscontinuedOperationsLiabilitiesNonCurrent = models.IntegerField(default=0)
    #
    #
    # Stockholders Equity - Trial Balance
    #
    # common shares
    CommonSharesBeginning = models.IntegerField(default=0)
    CommonStockIssued = models.IntegerField(default=0)
    ShareBasedCompensation = models.IntegerField(default=0)
    #
    # retained earnings
    RetainedEarningsBeginning = models.IntegerField(default=0)
    DividendsAndDividendEquivalentsDeclared = models.IntegerField(default=0)
    CommonStockRepurchasedAndRetired = models.IntegerField(default=0)
    EffectOfAdoptionOfNewAccountingPronouncementOrTaxCuts = models.IntegerField(default=0)
    RetainedEarningsOthers = models.IntegerField(default=0)
    #
    # accumulated other comprehensive income
    AccumulatedOtherComprehensiveIncomeBeginning = models.IntegerField(default=0)
    #
    # treasury shares
    TreasurySharesBeginning = models.IntegerField(default=0)
    PurchaseAndSellOfTreasuryShares = models.IntegerField(default=0)
    #
    # employee benefit trust
    EmployeeBenefitTrustBeginning = models.IntegerField(default=0)
    #
    # non controlling interests
    NonControllingInterestsBeginning = models.IntegerField(default=0)
    DividendsDeclaredToNonControllingInterests = models.IntegerField(default=0)
    NonControllingInterestsOthers = models.IntegerField(default=0)
    #
    #
    # Income Statements - Trial Balance
    #
    Sales = models.IntegerField(default=0)
    CostOfSales = models.IntegerField(default=0)
    ResearchAndDevelopment = models.IntegerField(default=0)
    SellingGeneralAdministrativeAndMarketing = models.IntegerField(default=0)
    ImpairmentRestructuringAndOtherSpecialCharges = models.IntegerField(default=0)
    NonOperatingIncome = models.IntegerField(default=0)
    IncomeTaxExpenseBenefit = models.IntegerField(default=0)
    NetIncomeFromDiscontinuedOperations = models.IntegerField(default=0)
    #
    #
    # Other Comprehensive Income - Trial Balance
    #
    ChangeInForeignCurrencyTranslationAdjustment = models.IntegerField(default=0)
    ChangeInUnrealizedGainsLossesOnDerivativeInstruments = models.IntegerField(default=0)
    ChangeInUnrealizedGainsLossesOnInvestments = models.IntegerField(default=0)
    ChangeInDefinedBenefitPensionAndOtherSimilarPlans = models.IntegerField(default=0)
    IncomeTaxOnOtherComprehensiveIncome = models.IntegerField(default=0)
    #
    #
    def __str__(self):
        return f"{self.TradingSymbol}:{self.Period}"


