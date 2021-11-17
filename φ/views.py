from .models import *

from django.contrib.auth import login, authenticate, logout
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from itertools import chain
from urllib.parse import urlencode

from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage

import os
import cv2
import json
import base64
import requests

from django.core import files

from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from account.models import *

from friend.utils import get_friend_request_or_false
from friend.friend_request_status import FriendRequestStatus
from friend.models import FriendList, FriendRequest

import datetime
import time
import json

from chat.models import PrivateChatRoom, RoomChatMessage
from chat.utils import find_or_create_private_chat



DEBUG = False

def analysis_view(request, user_id, entity_TradingSymbol):
	#
	context = {}
	context['debug_mode'] = settings.DEBUG
	context['debug'] = DEBUG
	context['room_id'] = "1"
	context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
	context['BASE_URL'] = settings.BASE_URL
	#
	context['entity'] = Entity.objects.get(TradingSymbol=entity_TradingSymbol)
	context['TrialBalance_lastyear'] = TrialBalance.objects.get(TradingSymbol=entity_TradingSymbol, Period="lastyear")
	context['TrialBalance_secondlastyear'] = TrialBalance.objects.get(TradingSymbol=entity_TradingSymbol, Period="secondlastyear")
	context['TrialBalance_thirdlastyear'] = TrialBalance.objects.get(TradingSymbol=entity_TradingSymbol, Period="thirdlastyear")
	context['TrialBalance_fourthlastyear'] = TrialBalance.objects.get(TradingSymbol=entity_TradingSymbol, Period="fourthlastyear")
	context['TrialBalance_fifthlastyear'] = TrialBalance.objects.get(TradingSymbol=entity_TradingSymbol, Period="fifthlastyear")
	context['TrialBalance_sixthlastyear'] = TrialBalance.objects.get(TradingSymbol=entity_TradingSymbol, Period="sixthlastyear")
	context['CashFlow_lastyear'] = CashFlow.objects.get(TradingSymbol=entity_TradingSymbol, Period="lastyear")
	context['CashFlow_secondlastyear'] = CashFlow.objects.get(TradingSymbol=entity_TradingSymbol, Period="secondlastyear")
	context['CashFlow_thirdlastyear'] = CashFlow.objects.get(TradingSymbol=entity_TradingSymbol, Period="thirdlastyear")
	context['CashFlow_fourthlastyear'] = CashFlow.objects.get(TradingSymbol=entity_TradingSymbol, Period="fourthlastyear")
	context['CashFlow_fifthlastyear'] = CashFlow.objects.get(TradingSymbol=entity_TradingSymbol, Period="fifthlastyear")
	context['CashFlow_sixthlastyear'] = CashFlow.objects.get(TradingSymbol=entity_TradingSymbol, Period="sixthlastyear")
	context['AuditData_lastyear'] = AuditData.objects.get(TradingSymbol=entity_TradingSymbol, Period="lastyear")
	context['AuditData_secondlastyear'] = AuditData.objects.get(TradingSymbol=entity_TradingSymbol, Period="secondlastyear")
	context['AuditData_thirdlastyear'] = AuditData.objects.get(TradingSymbol=entity_TradingSymbol, Period="thirdlastyear")
	context['AuditData_fourthlastyear'] = AuditData.objects.get(TradingSymbol=entity_TradingSymbol, Period="fourthlastyear")
	context['AuditData_fifthlastyear'] = AuditData.objects.get(TradingSymbol=entity_TradingSymbol, Period="fifthlastyear")
	context['AuditData_sixthlastyear'] = AuditData.objects.get(TradingSymbol=entity_TradingSymbol, Period="sixthlastyear")
	try:
		account = Account.objects.get(pk=user_id)
	except:
		return redirect('login')
	if account:
		context['id'] = account.id
		context['username'] = account.username
		context['email'] = account.email
		context['profile_image'] = account.profile_image.url
		context['hide_email'] = account.hide_email

		try:
			friend_list = FriendList.objects.get(user=account)
		except FriendList.DoesNotExist:
			friend_list = FriendList(user=account)
			friend_list.save()
		friends = friend_list.friends.all()
		context['friends'] = friends
		is_self = True
		is_friend = False
		request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
		friend_requests = None
		user = request.user
		if user.is_authenticated and user != account:
			is_self = False
			if friends.filter(pk=user.id):
				is_friend = True
			else:
				is_friend = False
				if get_friend_request_or_false(sender=account, receiver=user) != False:
					request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
					context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id
				elif get_friend_request_or_false(sender=user, receiver=account) != False:
					request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
				else:
					request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
		elif not user.is_authenticated:
			is_self = False
		else:
			try:
				friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
			except:
				pass
		context['is_self'] = is_self
		context['is_friend'] = is_friend
		context['request_sent'] = request_sent
		context['friend_requests'] = friend_requests
		#
		friends_requests = []
		FR = FriendRequest.objects.all()
		for friend_request in FR:
			if (friend_request.sender.id == user.id):
				if (friend_request.is_active == True):
					friends_requests.append(friend_request.receiver.id)
		context['friends_requests'] = friends_requests
	#
	# edit account
	if request.POST:
		form = AccountUpdateForm(request.POST, request.FILES, instance=user)
		if form.is_valid():
			form.save()
			return redirect("posts", user_id=user.id)
		else:
			form = AccountUpdateForm(request.POST, instance=user,
				initial={
					"id": account.id,
					"email": account.email, 
					"username": account.username,
					"profile_image": account.profile_image,
					"hide_email": account.hide_email,
				}
			)
			context['form'] = form
	else:
		form = AccountUpdateForm(
			initial={
					"id": account.id,
					"email": account.email, 
					"username": account.username,
					"profile_image": account.profile_image,
					"hide_email": account.hide_email,
				}
			)
		context['form'] = form
	#
	# messages
	room_id = request.GET.get("room_id")
	if room_id:
		room = PrivateChatRoom.objects.get(pk=room_id)
		context["room"] = room
	rooms1 = PrivateChatRoom.objects.filter(user1=user, is_active=True)
	rooms2 = PrivateChatRoom.objects.filter(user2=user, is_active=True)
	rooms = list(chain(rooms1, rooms2))
	m_and_f = [] 
	for room in rooms:
		if room.user1 == user:
			friend = room.user2
		else:
			friend = room.user1
		m_and_f.append({
			'message': "", 
			'friend': friend
		})
	context['m_and_f'] = m_and_f
	#
	# friends
	if user.is_authenticated:
		user_id = account.id
		if user_id:
			try:
				this_user = Account.objects.get(pk=user_id)
				context['this_user'] = this_user
			except Account.DoesNotExist:
				return HttpResponse("That user does not exist.")
			try:
				friend_list = FriendList.objects.get(user=this_user)
			except FriendList.DoesNotExist:
				return HttpResponse(f"Could not find a friends list for {this_user.username}")
			friends = []
			auth_user_friend_list = FriendList.objects.get(user=user)
			for friend in friend_list.friends.all():
				friends.append((friend, auth_user_friend_list.is_mutual_friend(friend)))
			context['friends'] = friends
	else:		
		return HttpResponse("You must be friends to view their friends list.")
	#
	# profiles
	if user.is_authenticated:
		user_id = account.id
		if user_id:
			friends = [] 
			auth_user_friend_list = FriendList.objects.get(user=user)
			for friend in friend_list.friends.all():
				friends.append((friend, auth_user_friend_list.is_mutual_friend(friend)))
			context['profileUsers'] = friends
	#
	# entities
	context['entities'] = Entity.objects.all().order_by('TradingSymbol')
	#
	return render(request, "base/clockdb.html", context)

def fiscal_year_end_view(request, db, start, end):
    e = Entity.objects.all().filter(PeriodEndDate_db=db)
    data = []
    end = min(len(e), int(end))
    for i in range(int(start), end):
        json = {
            "EntityRegistrantName1": e[i].EntityRegistrantName,
            "TradingSymbol1": e[i].TradingSymbol,
            "ContextDate1": e[i].lastyear,
        }
        data.append(json)    
    time.sleep(1)
    return JsonResponse({
        "entities": data
    })

def home_screen_view(request):
	user = request.user
	context = {}
	context['debug_mode'] = settings.DEBUG
	context['debug'] = DEBUG
	context['room_id'] = "1"
	if user.is_authenticated: 
		return redirect("posts", user_id=user.id)
	return redirect("login")

def phase_view(request, db, start, end):
    e = Entity.objects.all().filter(db=db)
    data = []
    end = min(len(e), int(end))
    for i in range(int(start), end):
        json = {
            "EntityRegistrantName1": e[i].EntityRegistrantName,
            "TradingSymbol1": e[i].TradingSymbol,
            "CIK1": e[i].EntityCentralIndexKey,
            "db1": e[i].db,
            "Industry_SEC1": e[i].Industry_SEC,
            "Industry_SEC_db1": e[i].Industry_SEC_db,
            "Industry1": e[i].Industry,
            "Industrydb1": e[i].Industry_db,
            "Region1": e[i].Region,
            "Regiondb1": e[i].Region_db,
            "ContextDate1": e[i].lastyear,
            "ContextDate2": e[i].secondlastyear,
            "ContextDate3": e[i].thirdlastyear,
            "ContextDate4": e[i].fourthlastyear,
            "ContextDate5": e[i].fifthlastyear,
            "ContextDate6": e[i].sixthlastyear,
            "Amend1": e[i].amendlastyear,
            "Amend2": e[i].amendlastyear,
            "Amend3": e[i].amendlastyear,
            "Amend4": e[i].amendlastyear,
            "Amend5": e[i].amendlastyear,
            "Amend6": e[i].amendlastyear,
            "AccessionNumber1": e[i].accessionnumberlastyear,
            "AccessionNumber2": e[i].accessionnumbersecondlastyear,
            "AccessionNumber3": e[i].accessionnumberthirdlastyear,
            "AccessionNumber4": e[i].accessionnumberfourthlastyear,
            "AccessionNumber5": e[i].accessionnumberfifthlastyear,
            "AccessionNumber6": e[i].accessionnumbersixthlastyear,
            "urlbalancesheet1": e[i].urlbalancesheetlastyear,
            "urlbalancesheet2": e[i].urlbalancesheetsecondlastyear,
            "urlbalancesheet3": e[i].urlbalancesheetthirdlastyear,
            "urlbalancesheet4": e[i].urlbalancesheetfourthlastyear,
            "urlbalancesheet5": e[i].urlbalancesheetfifthlastyear,
            "urlbalancesheet6": e[i].urlbalancesheetsixthlastyear,
            "urlincomestatement1": e[i].urlincomestatementlastyear,
            "urlincomestatement2": e[i].urlincomestatementsecondlastyear,
            "urlincomestatement3": e[i].urlincomestatementthirdlastyear,
            "urlincomestatement4": e[i].urlincomestatementfourthlastyear,
            "urlincomestatement5": e[i].urlincomestatementfifthlastyear,
            "urlincomestatement6": e[i].urlincomestatementsixthlastyear,
            "urlcomprehensiveincome1": e[i].urlcomprehensiveincomelastyear,           
            "urlcomprehensiveincome2": e[i].urlcomprehensiveincomesecondlastyear,           
            "urlcomprehensiveincome3": e[i].urlcomprehensiveincomethirdlastyear,           
            "urlcomprehensiveincome4": e[i].urlcomprehensiveincomefourthlastyear,           
            "urlcomprehensiveincome5": e[i].urlcomprehensiveincomefifthlastyear,           
            "urlcomprehensiveincome6": e[i].urlcomprehensiveincomesixthlastyear,
            "urlshareholdersequity1": e[i].urlshareholdersequitylastyear,
            "urlshareholdersequity2": e[i].urlshareholdersequitysecondlastyear,
            "urlshareholdersequity3": e[i].urlshareholdersequitythirdlastyear,
            "urlshareholdersequity4": e[i].urlshareholdersequityfourthlastyear,
            "urlshareholdersequity5": e[i].urlshareholdersequityfifthlastyear,
            "urlshareholdersequity6": e[i].urlshareholdersequitysixthlastyear,
            "urlcashflow1": e[i].urlcashflowlastyear,
            "urlcashflow2": e[i].urlcashflowsecondlastyear,
            "urlcashflow3": e[i].urlcashflowthirdlastyear,
            "urlcashflow4": e[i].urlcashflowfourthlastyear,
            "urlcashflow5": e[i].urlcashflowfifthlastyear,
            "urlcashflow6": e[i].urlcashflowsixthlastyear,
        }
        data.append(json)    
    time.sleep(1)
    return JsonResponse({
        "entities": data
    })

def posts_screen_view(request, user_id):
	context = {}
	context['BASE_URL'] = settings.BASE_URL
	context['debug_mode'] = settings.DEBUG
	context['debug'] = DEBUG
	context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
    # profile
	try:
		account = Account.objects.get(pk=user_id)
	except:
		return redirect('login')
	if account:
		context['id'] = account.id
		context['username'] = account.username
		context['email'] = account.email
		context['profile_image'] = account.profile_image.url
		context['hide_email'] = account.hide_email
		try:
			friend_list = FriendList.objects.get(user=account)
		except FriendList.DoesNotExist:
			friend_list = FriendList(user=account)
			friend_list.save()
		friends = friend_list.friends.all()
		context['friends'] = friends
		#
		# friends requests
		is_self = True
		is_friend = False
		request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
		friend_requests = None
		user = request.user
		if user.is_authenticated and user != account:
			is_self = False
			if friends.filter(pk=user.id):
				is_friend = True
			else:
				is_friend = False
				if get_friend_request_or_false(sender=account, receiver=user) != False:
					request_sent = FriendRequestStatus.THEM_SENT_TO_YOU.value
					context['pending_friend_request_id'] = get_friend_request_or_false(sender=account, receiver=user).id
				elif get_friend_request_or_false(sender=user, receiver=account) != False:
					request_sent = FriendRequestStatus.YOU_SENT_TO_THEM.value
				else:
					request_sent = FriendRequestStatus.NO_REQUEST_SENT.value
		elif not user.is_authenticated:
			is_self = False
		else:
			try:
				friend_requests = FriendRequest.objects.filter(receiver=user, is_active=True)
			except:
				pass
		context['is_self'] = is_self
		context['is_friend'] = is_friend
		context['request_sent'] = request_sent
		#
		friends_requests = []
		FR = FriendRequest.objects.all()
		for friend_request in FR:
			if (friend_request.sender.id == user.id):
				if (friend_request.is_active == True):
					friends_requests.append(friend_request.receiver.id)
		context['friends_requests'] = friends_requests
    #
	# edit_profile
	if request.POST:
		form = AccountUpdateForm(request.POST, request.FILES, instance=user)
		if form.is_valid():
			form.save()
			return redirect("posts", user_id=user.id)
		else:
			form = AccountUpdateForm(request.POST, instance=user,
				initial={
					"id": account.id,
					"email": account.email, 
					"username": account.username,
					"profile_image": account.profile_image,
					"hide_email": account.hide_email,
				}
			)
			context['form'] = form
	else:
		form = AccountUpdateForm(
			initial={
					"id": account.id,
					"email": account.email, 
					"username": account.username,
					"profile_image": account.profile_image,
					"hide_email": account.hide_email,
				}
			)
		context['form'] = form
    #
	# chat
	room_id = request.GET.get("room_id")
	if room_id:
		room = PrivateChatRoom.objects.get(pk=room_id)
		context["room"] = room
	rooms1 = PrivateChatRoom.objects.filter(user1=user, is_active=True)
	rooms2 = PrivateChatRoom.objects.filter(user2=user, is_active=True)
	rooms = list(chain(rooms1, rooms2))
	m_and_f = [] 
	for room in rooms:
		# Figure out which user is the "other user" (aka friend)
		if room.user1 == user:
			friend = room.user2
		else:
			friend = room.user1
		m_and_f.append({
			'message': "", # blank msg for now (since we have no messages)
			'friend': friend
		})
	context['m_and_f'] = m_and_f
	#
	# friends
	if user.is_authenticated:
		user_id = account.id
		if user_id:
			try:
				this_user = Account.objects.get(pk=user_id)
				context['this_user'] = this_user
			except Account.DoesNotExist:
				return HttpResponse("That user does not exist.")
			try:
				friend_list = FriendList.objects.get(user=this_user)
			except FriendList.DoesNotExist:
				return HttpResponse(f"Could not find a friends list for {this_user.username}")
			friends = []
			auth_user_friend_list = FriendList.objects.get(user=user)
			for friend in friend_list.friends.all():
				friends.append((friend, auth_user_friend_list.is_mutual_friend(friend)))
			context['friends'] = friends
	#
	# profiles
	if user.is_authenticated:
		user_id = account.id
		if user_id:
			friends = []
			auth_user_friend_list = FriendList.objects.get(user=user)
			for friend in friend_list.friends.all():
				friends.append((friend, auth_user_friend_list.is_mutual_friend(friend)))
			context['profileUsers'] = friends
	#
	# entities
	context['entities'] = Entity.objects.all().order_by('TradingSymbol')
	#
	return render(request, "base/clockdb.html", context)

def posts_view(request, industry_db, industry_SEC_db, year_end, db, region_db, order_db, sort_db, start, end):
    #
    e = Entity.objects.all()
    #
    a = '-db'
    b = '-NumberOfYearsAudited'
    c = 'AnomaliesRatio1'
    d = 'AnomaliesRatio2'
    ee = 'AnomaliesRatio3'
    f = 'AnomaliesRatio4'
    g = 'AnomaliesRatio5'
    h = 'AnomaliesRatio6'
    #
    if sort_db == 'any':
        e = e.order_by(a, b, c, d, ee, f, g, h)
    else:
        sort = sort_db
        if order_db != 'any':
            if order_db != '+':
                sort = order_db + sort
        e = e.order_by(sort, a, b, c, d, ee, f, g, h)
    #
    if industry_db != 'any':
        e = e.filter(Industry_db=industry_db)
    #
    if industry_SEC_db != 'any':
        e = e.filter(Industry_SEC_db=industry_SEC_db)
    #
    if year_end != 'any':
        e = e.filter(year_end=year_end)
    #
    if db != 'any':
        e = e.filter(db=db)
    #
    if region_db != 'any':
        e = e.filter(Region_db=region_db)
    #
    start = int(start) - 1
    #
    end = int(end)
    if end > len(e):
        end = len(e)
    #
    data = []
    #
    for i in range(start, end):
        json = {
            "entity": e[i].EntityRegistrantName,
            "tradingSymbol": e[i].TradingSymbol,
            "industry_db": e[i].Industry_db,
            "industry": e[i].Industry,
            "industry_sec_db": e[i].Industry_SEC_db,
            "industry_sec": e[i].Industry_SEC,
            "db": e[i].db,
            "region_db": e[i].Region_db,
            "region": e[i].Region,
            #
            "lastyear": e[i].lastyear,
            "secondlastyear": e[i].secondlastyear,
            "thirdlastyear": e[i].thirdlastyear,
            "fourthlastyear": e[i].fourthlastyear,
            "amendlastyear": e[i].amendlastyear,
            "amendsecondlastyear": e[i].amendsecondlastyear,
            "amendthirdlastyear": e[i].amendthirdlastyear,
            "amendfourthlastyear": e[i].amendfourthlastyear,
            #
            "SecuritiesUpdate": e[i].SecuritiesUpdate,
            #
            "OpinionφLastYear": e[i].OpinionφLastYear,
            "OpinionφSecondLastYear": e[i].OpinionφSecondLastYear,
            "OpinionφThirdLastYear": e[i].OpinionφThirdLastYear,
            "OpinionφFourthLastYear": e[i].OpinionφFourthLastYear,
            #
            "ClockφLastYear": e[i].ClockφLastYear,
            "ClockφSecondLastYear": e[i].ClockφSecondLastYear,
            "ClockφThirdLastYear": e[i].ClockφThirdLastYear,
            "ClockφFourthLastYear": e[i].ClockφFourthLastYear,
            #
            "BridgeφLastYear": e[i].BridgeφLastYear,
            "BridgeφSecondLastYear": e[i].BridgeφSecondLastYear,
            "BridgeφThirdLastYear": e[i].BridgeφThirdLastYear,
            "BridgeφFourthLastYear": e[i].BridgeφFourthLastYear,
            #
            "CommonSharesIntrinsicValueLastYear": e[i].CommonSharesIntrinsicValueLastYear,
            "CommonSharesIntrinsicValueSecondLastYear": e[i].CommonSharesIntrinsicValueSecondLastYear,
            "CommonSharesIntrinsicValueThirdLastYear": e[i].CommonSharesIntrinsicValueThirdLastYear,
            "CommonSharesIntrinsicValueFourthLastYear": e[i].CommonSharesIntrinsicValueFourthLastYear,
            #
            "MarketCapitalizationLastYear": e[i].MarketCapitalizationLastYear,
            "MarketCapitalizationSecondLastYear": e[i].MarketCapitalizationSecondLastYear,
            "MarketCapitalizationThirdLastYear": e[i].MarketCapitalizationThirdLastYear,
            "MarketCapitalizationFourthLastYear": e[i].MarketCapitalizationFourthLastYear,
            #
            "CommonShareIntrinsicValueLastYear": e[i].CommonShareIntrinsicValueLastYear,
            "CommonShareIntrinsicValueSecondLastYear": e[i].CommonShareIntrinsicValueSecondLastYear,
            "CommonShareIntrinsicValueThirdLastYear": e[i].CommonShareIntrinsicValueThirdLastYear,
            "CommonShareIntrinsicValueFourthLastYear": e[i].CommonShareIntrinsicValueFourthLastYear,
            #
            "CommonSharePriceLastYear": e[i].CommonSharePriceLastYear,
            "CommonSharePriceSecondLastYear": e[i].CommonSharePriceSecondLastYear,
            "CommonSharePriceThirdLastYear": e[i].CommonSharePriceThirdLastYear,
            "CommonSharePriceFourthLastYear": e[i].CommonSharePriceFourthLastYear,
            #
            "CommonSharesOutstandingLastYear": e[i].CommonSharesOutstandingLastYear,
            "CommonSharesOutstandingSecondLastYear": e[i].CommonSharesOutstandingSecondLastYear,
            "CommonSharesOutstandingThirdLastYear": e[i].CommonSharesOutstandingThirdLastYear,
            "CommonSharesOutstandingFourthLastYear": e[i].CommonSharesOutstandingFourthLastYear,
        }
        data.append(json)

    time.sleep(1)

    return JsonResponse({
        "posts": data,
		"len": len(e)
    })

def entities_view(request, search, start, end):
	e = Entity.objects.all().order_by('TradingSymbol')
	entities = []
	for i in range(0, len(e)):
		b = 0
		search = search.lower()
		if (search in e[i].EntityRegistrantName.lower()):
				b = 1
		if (search in e[i].TradingSymbol.lower()):
				b = 1
		if (search in e[i].Industry.lower()):
				b = 1
		if (search in e[i].Industry_SEC.lower()):
				b = 1
		if (search in e[i].Region.lower()):
				b = 1
		if (b == 1):
			Json = {
				"EntityRegistrantName": e[i].EntityRegistrantName,
				"TradingSymbol": e[i].TradingSymbol,
				"Industry": e[i].Industry,
				"Industry_SEC": e[i].Industry_SEC,
				"Region": e[i].Region,
			}
			entities.append(Json)
	data = []
	start = int(start) - 1
	end = min(len(entities), int(end))
	for u in range(int(start), end):
		Json = {
            "EntityRegistrantName": entities[u]['EntityRegistrantName'],
            "TradingSymbol": entities[u]['TradingSymbol'],
            "Industry": entities[u]['Industry'],
            "Industry_SEC": entities[u]['Industry_SEC'],
            "Region": entities[u]['Region'],
		}
		data.append(Json)
	time.sleep(1)
	return JsonResponse({
		"entities": data,
		"len": len(entities)
	})
