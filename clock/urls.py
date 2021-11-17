"""ChatServerPlayground URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from φ.views import *
from account.views import *
from friend.views import *
from chat.views import *

urlpatterns = [
    #
	path('', home_screen_view, name='home'),
	path('Home', home_screen_view, name='home'),
	path('admin/', admin.site.urls),
    path("entities/<str:search>/<str:start>/<str:end>/", entities_view, name="entities"),
    path("posts/<str:industry_db>/<str:industry_SEC_db>/<str:year_end>/<str:db>/<str:region_db>/<str:order_db>/<str:sort_db>/<str:start>/<str:end>/", posts_view, name="posts"),
    path('login/', login_view, name="login"),
    path('logout/', logout_view, name="logout"),
    path('register/', register_view, name="register"),
    #
    path('friend_remove/', remove_friend, name='remove-friend'),
    path('friend_request/', send_friend_request, name='friend-request'),
    path('friend_request_cancel/', cancel_friend_request, name='friend-request-cancel'),
    path('friend_request_accept/<friend_request_id>/', accept_friend_request, name='friend-request-accept'),
    path('friend_request_decline/<friend_request_id>/', decline_friend_request, name='friend-request-decline'),
	path('create_or_return_private_chat/', create_or_return_private_chat, name='create-or-return-private-chat'),
    #
    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='profile/password_reset/password_change_done.html'), 
        name='password_change_done'),

    path('<str:user_id>/change_password/',
        auth_views.PasswordChangeView.as_view(template_name='profile/password_reset/change_password.html'), 
        name='change_password'),

    path('password_reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='profile/password_reset/password_reset_done.html'),
        name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    path('password_reset/',
        auth_views.PasswordResetView.as_view(template_name='profile/password_reset/password_reset.html'),
        name='password_reset'),
    
    path('reset/done/',
        auth_views.PasswordResetCompleteView.as_view(template_name='profile/password_reset/password_reset_complete.html'),
        name='password_reset_complete'),
    #    
    path('<str:user_id>/', posts_screen_view, name='posts'),
    #
    path("<str:user_id>/Home/", posts_screen_view, name="posts"),
    #
    path("<str:user_id>/profile/", posts_screen_view, name="profile"),
    path("<str:user_id>/edit/", posts_screen_view, name="edit"),
	path('<user_id>/edit/cropImage/', crop_image, name="crop_image"),
    #
	path('<str:user_id>/Entities/', posts_screen_view, name="entities"),
	path('<str:user_id>/Network/', posts_screen_view, name="network"),
    path("<str:user_id>/messages/", posts_screen_view, name="messages"),
    path("<str:user_id>/friend_requests/", posts_screen_view, name="friend-requests"),
    #
    path("<str:user_id>/about/", posts_screen_view, name="about"),
    path('<str:user_id>/AdvancedSearch/', posts_screen_view, name='AdvancedSearch'),
    path("<str:user_id>/commands/", posts_screen_view, name="commands"),
    path("<str:user_id>/disclaimer/", posts_screen_view, name="disclaimer"),
    path("<str:user_id>/display/", posts_screen_view, name="display"),
    path('<str:user_id>/database/', posts_screen_view, name="database"),
    path("<str:user_id>/documentation/", posts_screen_view, name="documentation"),
    path('<str:user_id>/fiscalYearEnd/', posts_screen_view, name="fiscalYearEnd"),
    path('<str:user_id>/fiscalYearEnd/<str:db>/<str:start>/<str:end>/', fiscal_year_end_view, name="fiscalYearEndJson"),
    path('<str:user_id>/fiscalYearEnds/', posts_screen_view, name="fiscalYearEnds"),
    path("<str:user_id>/phase/", posts_screen_view, name="phase"),
    path("<str:user_id>/phase/<str:db>/<str:start>/<str:end>/", phase_view, name="phaseJson"),
    path('<str:user_id>/phases/', posts_screen_view, name="phases"),
    path('<str:user_id>/Posts/', posts_screen_view, name="Posts"),
    path('<str:user_id>/settings/', posts_screen_view, name="settings"),
    #
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/", analysis_view, name="analysis"),
    #
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/Home/", analysis_view, name="analysis"),
    #
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/profile/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/edit_profile/", analysis_view, name="analysis"),
	path('<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/edit_profile/cropImage/', crop_image, name="crop_image"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/Entities/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/Network/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/messages/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/friend_requests/", analysis_view, name="analysis"),
    #
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/About/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/Arch/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/Bridge/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/Clock/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/Summary/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/Graph/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/Documentation/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/Commands/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/Context/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/AnnualCashFlow/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/AnnualBalanceSheets/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/AnnualIncomeStatements/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/AnnualComprehensiveIncome/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/AnnualShareholdersEquity/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/AnnualTrialBalances/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/Mission/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/MaterialityThreshold/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/Procedures/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/ProcedureAnnualCashFlow/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/ProcedureAnnualBalanceSheets/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/ProcedureAnnualIncomeStatements/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/ProcedureAnnualComprehensiveIncome/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/ProcedureAnnualShareholdersEquity/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/Anomalies/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/Summary/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/FinancialRatios/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/AdditionalInformation/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/CapitalizedCashFlow/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/CapitalizedIncome/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/IntrinsicValues/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/CapitalizationRates/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/Opinion/", analysis_view, name="analysis"),
    #
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/Files/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/ReferenceMap/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/Open/", analysis_view, name="analysis"),
    #
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/Settings/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/Rollover/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/Open/", analysis_view, name="analysis"),
    #
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/disclaimer/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/documentation/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/about/", analysis_view, name="analysis"),
    path("<str:user_id>/WorkingPaper/<str:entity_TradingSymbol>/commands/", analysis_view, name="analysis"),
    #
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



