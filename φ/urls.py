from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views


app_name = "φ"


urlpatterns = [
    
    path("", views.index, name="index"),

    path("db/", views.db, name="db"),

    path("qp/", views.qp, name="qp"),

    path("disclaimer/", views.disclaimer, name="disclaimer"),

    path("entities/", views.entities, name="entities"),
    
    path("documentation/", views.documentation, name="documentation"),

    path("menu/", views.menu, name="menu"),

    path("<str:entity_TradingSymbol>/", views.analysis, name="analysis"),
    #
    path("<str:entity_TradingSymbol>/Arch", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/Bridge", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/Clock", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/Graph", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/Opinion", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/AnnualCashFlow", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/AnnualBalanceSheets", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/AnnualIncomeStatements", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/AnnualComprehensiveIncome", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/AnnualStockholdersEquity", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/AnnualTrialBalances", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/Mission", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/MaterialityThreshold", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/ProcedureAnnualCashFlow", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/ProcedureAnnualBalanceSheets", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/ProcedureAnnualIncomeStatements", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/ProcedureAnnualComprehensiveIncome", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/ProcedureAnnualStockholdersEquity", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/AuditDetailed", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/AuditSummary", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/AnnualFinancialRatios", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/AdditionnalInformation", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/CapitalizedCashFlow", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/CapitalizedIncome", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/IntrinsicValues", views.analysis, name="analysis"),
    path("<str:entity_TradingSymbol>/CapitalizationRate", views.analysis, name="analysis"),
]

urlpatterns += staticfiles_urlpatterns()