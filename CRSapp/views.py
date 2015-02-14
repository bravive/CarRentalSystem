from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
from django.core.urlresolvers import reverse
from forms import *
from models import *
from CRSapp.models import *
# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator
# Used to send mail from within Django
from django.core.mail import send_mail
# Create your views here.
from django.http import HttpResponse, Http404, HttpResponseRedirect
from mimetypes import guess_type
from django.core import serializers
from django.db.models import Avg, Max, Min
from django.template.loader import render_to_string
import re
import datetime
import math

def db(request):
    context={}
    return render(request, 'Sign_in/db_in.html', "")

def admin_required(login_url=None):
    return user_passes_test(lambda u:u.is_staff and not u.is_superuser, login_url=login_url)
#---------------szy-------------#
def makeview(request,context):
    static_context={}
    static_context['form_cartype']=CarTypeForm()
    static_context['url_next']=''
    static_context.update(context)
    return render(request,static_context['url_next'],static_context)

@admin_required(login_url='/userlogin/')
@transaction.atomic
def addCarTpye(request):
    context={}
    context['url_next']='AdministratorUser/Inventory.html'
    form = CarTypeForm(request.POST, request.FILES)
    if not form.is_valid():
        context['form_cartype'] = form
        context['cartypes']=CarType.objects.all().order_by('cartype')
        context['allcars']=CarInventory.objects.all().order_by('-cartype');
        return makeview(request,context)
    form.save()
    context['cartypes']=CarType.objects.all().order_by('-cartype')
    context['allcars']=CarInventory.objects.all().order_by('-cartype');

    return makeview(request,context)

@admin_required(login_url='/userlogin/')
@transaction.atomic
def addCar(request):
    context={}
    context['url_next']='AdministratorUser/Inventory.html'
    context['cartypes']=CarType.objects.all().order_by('cartype')
    if request.method == 'POST' and 'cartype' in request.POST:
        cartype=get_object_or_404(CarType,cartype=request.POST['cartype'])
        if cartype is not None:
            cars=CarInventory.objects.filter(cartype__cartype=request.POST['cartype'])
            count=cars.count()
            if count==0:
                car_model=CarInventory(cartype=cartype,CIN=request.POST['cartype']+"#"+str(count),mile='0',status='Available')
            else:
                CIN_num=str(int(filter(str.isdigit,str(list(cars)[-1].CIN)))+1)
                car_model=CarInventory(cartype=cartype,CIN=request.POST['cartype']+"#"+CIN_num,mile='0',status='Available')
            car_model.save()

    context['allcars']=CarInventory.objects.all().order_by('-cartype')
    return makeview(request,context)

@admin_required(login_url='/userlogin/')
@transaction.atomic
def deleteCar(request):
    context={}
    context['url_next']='AdministratorUser/Inventory.html'

    if 'h_CIN' not in request.POST or request.POST['h_CIN']=='':
        context['errors_delete']='Fail to delete'
        response_text=render_to_string("JSON/error_delete.json",context)
        return HttpResponse(response_text, content_type="application/json")
    CIN = request.POST['h_CIN']
    car = CarInventory.objects.filter(CIN=CIN)
    if not car:
        context['errors_delete']='There is no such car in inventory.'
        response_text=render_to_string("JSON/error_delete.json",context)
        return HttpResponse(response_text, content_type="application/json")

    timesheets = CarReserveTimeSheet.objects.filter(car__CIN=CIN)
    if timesheets:
        context['errors_delete']='There is an order about this car. You cannot delete it .'
        response_text=render_to_string("JSON/error_delete.json",context)
        return HttpResponse(response_text, content_type="application/json")

    car = CarInventory.objects.get(CIN=CIN)
    car.delete()
    context['success']='Delete Successfully.'
    response_text=render_to_string("JSON/error_delete.json",context)
    return HttpResponse(response_text, content_type="application/json")


def logingen_required(login_url=None):
    return user_passes_test(lambda u:u.is_active and not u.is_staff, login_url=login_url)
@login_required(login_url='/userlogin/')
@transaction.atomic
def ajax_get_cars(request):
    context={}
    context['errors_time_select']=''
    if request.GET['from_date'] =='' or request.GET['from_time'] =='' or request.GET['to_date'] =='' or request.GET['to_time'] =='':
        context['errors_time_select']='Date and time are required.'
        response_text=render_to_string("JSON/error_time.json",context)
        return HttpResponse(response_text, content_type="application/json")
    
    if comparedate(request.GET['from_date'],request.GET['to_date'])==1 or comparedate(request.GET['from_date'],request.GET['to_date'])==0:
        context['errors_time_select']='Pick-up date should be smaller than Drop-off date.'
        response_text=render_to_string("JSON/error_time.json",context)
        return HttpResponse(response_text, content_type="application/json")
    
    #search by date
    timesheet=CarReserveTimeSheet.objects.all()
    availablecars=CarInventory.objects.all()

    for item in timesheet:
        if comparedate(request.GET['from_date'],item.todate)>0 or comparedate(request.GET['to_date'],item.fromdate)<0 :
            continue
        elif comparedate(request.GET['from_date'],item.todate)==0:
            if(comparetime(request.GET['from_time'],item.totime)!=1):
                overlap_mark=1
                unavailablecar=item.car
        elif comparedate(request.GET['to_date'],item.fromdate)==0:
            if(comparetime(request.GET['to_time'],item.fromtime)!=-1):
                overlap_mark=1
                unavailablecar=item.car
        else:
            overlap_mark=1
            unavailablecar=item.car
        if overlap_mark==1:
            availablecars=availablecars.exclude(id=unavailablecar.id)
    
    context['from_date']=request.GET['from_date']
    context['from_time']=request.GET['from_time']
    context['to_date']=request.GET['to_date']
    context['to_time']=request.GET['to_time']
    if request.GET['cartype'] == 'all':
        context["cars"]=availablecars
    else:
        context["cars"]=availablecars.filter(cartype__cartype=request.GET['cartype'])
    
    response_text=render_to_string("JSON/cars.json",context)
    return HttpResponse(response_text, content_type="application/json")

@admin_required(login_url='/userlogin/')
@transaction.atomic
def ajax_get_all_generalUsers(request):
    context={}
    context["allGeneralUsers"]=User.objects.filter(is_staff=False)
    response_text = serializers.serialize("json", context["allGeneralUsers"])
    return HttpResponse(response_text, content_type="application/json")


def comparedate(date1, date2):
    str1=date1.split('/')
    str2=date2.split('/')
    if int(str1[2])>int(str2[2]):
        return 1
    elif int(str1[2])<int(str2[2]):
        return -1
    else:
        if int(str1[0])>int(str2[0]):
            return 1
        elif int(str1[0])<int(str2[0]):
            return -1
        else:
            if int(str1[1])>int(str2[1]):
                #date1>date2
                return 1
            elif int(str1[1])<int(str2[1]):
                #date1<date2
                return -1
            else:
                #==
                return 0

def comparetime(time1, time2):
    str1=re.split(':',time1)
    str2=re.split(':',time2)
    if int(str1[0])>int(str2[0]):
        return 1
    elif int(str1[0])<int(str2[0]):
        return -1
    else:
        return 0

def checkIfTodayCarAvalable(car):
    nowdate=datetime.date.today().strftime("%m/%d/%Y")
    TheCarSheets = CarReserveTimeSheet.objects.filter(car=car)
    if not TheCarSheets:
        return True#avaliable
    for carsheet in TheCarSheets:
        if comparedate(nowdate,carsheet.fromdate)<0 or comparedate(nowdate,carsheet.todate)>0 or comparedate(nowdate,carsheet.todate)==0:
            continue
        else:
            return False
    return True




#@login_required(login_url='/userlogin/')
@transaction.atomic
def get_car_picture(request,cartype):
    cartype = get_object_or_404(CarType, cartype=cartype)
    if not cartype.picture:
        raise Http404
    content_type = guess_type(cartype.picture.name)
    return HttpResponse(cartype.picture, content_type=content_type)
    
@admin_required(login_url='/userlogin/')
@transaction.atomic
def add_reserve(request):
    context={}
    overlap_mark=0
    
    #if 'oldmiles' not in request.POST or request.POST['oldmiles'] == '':
    #    context['error_mile_required']='Old Mile Field is required'
    #    response_text=render_to_string("JSON/error_mile.json",context)
    #    return HttpResponse(response_text, content_type="application/json")

    CIN = request.POST['h_CIN']
    FROM_DATE = request.POST['h_fromdate']
    FROM_TIME = request.POST['h_fromtime']
    TO_DATE = request.POST['h_todate']
    TO_TIME = request.POST['h_totime']
    G_USERNAME = request.POST['generalusername']
    #TOTAL_FEE = request.POST['h_totalfee']

    car=get_object_or_404(CarInventory,CIN=CIN)
    user=get_object_or_404(User,username=G_USERNAME)

    TheCarSheets = CarReserveTimeSheet.objects.filter(car__CIN = CIN)
    TheUserHistory = UserReserveHistory.objects.filter(user__username = G_USERNAME)

    if TheUserHistory:
        lastid = TheUserHistory.aggregate(Max('id'))
        item=get_object_or_404(UserReserveHistory,id=lastid['id__max'])
        if item.status_deleted == False and item.status_returned == False:
            context['reserve']='You have reserved a car. You cannot reserve another!'
            response_text=render_to_string("JSON/error_mile.json",context)
            return HttpResponse(response_text, content_type="application/json")

    if not TheCarSheets:
        TIMESHEET=CarReserveTimeSheet(car=car,fromdate=FROM_DATE,fromtime=FROM_TIME,todate=TO_DATE,totime=TO_TIME)
        TIMESHEET.save()
        USERHISTORY=UserReserveHistory(user=user,status_reserved=True,CIN=CIN,fromdate=FROM_DATE,fromtime=FROM_TIME,todate=TO_DATE,totime=TO_TIME)
        USERHISTORY.save()
        context['success']='Reserve Successful!'
        response_text=render_to_string("JSON/error_mile.json",context)
        return HttpResponse(response_text, content_type="application/json")
    else:
        for carsheet in TheCarSheets:
            #newfrom>oldto || newto>oldfrom
            if comparedate(FROM_DATE,carsheet.todate)>0 or comparedate(TO_DATE,carsheet.fromdate)<0 :
                continue
            #newfrom=oldto
            elif comparedate(FROM_DATE,carsheet.todate)==0:
                if(comparetime(FROM_TIME,carsheet.totime)!=1):
                    overlap_mark=1
                    break
            #newto=oldfrom
            elif comparedate(TO_DATE,carsheet.fromdate)==0:
                if(comparetime(TO_TIME,carsheet.fromtime)!=-1):
                    overlap_mark=1
                    break
            else:
                overlap_mark=1
                break
        if overlap_mark==0:
            TIMESHEET=CarReserveTimeSheet(car=car,fromdate=FROM_DATE,fromtime=FROM_TIME,todate=TO_DATE,totime=TO_TIME)
            TIMESHEET.save()
            USERHISTORY=UserReserveHistory(user=user,status_reserved=True,CIN=CIN,fromdate=FROM_DATE,fromtime=FROM_TIME,todate=TO_DATE,totime=TO_TIME)
            USERHISTORY.save()
            context['success']='Reserve Successful!'
            response_text=render_to_string("JSON/error_mile.json",context)
            return HttpResponse(response_text, content_type="application/json")
        else:
            context['error_overlap']='Fail: You cannot reserve the car within the selected time.Please select again!'
            response_text=render_to_string("JSON/error_mile.json",context)
            return HttpResponse(response_text, content_type="application/json")
@logingen_required(login_url='/userlogin/')
@transaction.atomic
def add_reserve_general(request):
    context={}
    overlap_mark=0

    #if 'oldmiles' not in request.POST or request.POST['oldmiles'] == '':
    #    context['error_mile_required']='Old Mile Field is required'
    #    response_text=render_to_string("JSON/error_mile.json",context)
    #    return HttpResponse(response_text, content_type="application/json")
    if 'h_CIN' not in request.POST:
        print(1)
    CIN = request.POST['h_CIN']
    print(0)
    FROM_DATE = request.POST['h_fromdate']
    FROM_TIME = request.POST['h_fromtime']
    TO_DATE = request.POST['h_todate']
    TO_TIME = request.POST['h_totime']

    G_USERNAME = request.user.username
    #TOTAL_FEE = request.POST['h_totalfee']

    car=get_object_or_404(CarInventory,CIN=CIN)
    user=get_object_or_404(User,username=G_USERNAME)

    TheCarSheets = CarReserveTimeSheet.objects.filter(car__CIN = CIN)
    TheUserHistory = UserReserveHistory.objects.filter(user__username = G_USERNAME)

    if TheUserHistory:
        lastid = TheUserHistory.aggregate(Max('id'))
        item=get_object_or_404(UserReserveHistory,id=lastid['id__max'])
        if item.status_deleted == False and item.status_returned == False:
            context['reserve']='You have reserved a car. You cannot reserve another!'
            response_text=render_to_string("JSON/error_mile.json",context)
            return HttpResponse(response_text, content_type="application/json")

    if not TheCarSheets:
        TIMESHEET=CarReserveTimeSheet(car=car,fromdate=FROM_DATE,fromtime=FROM_TIME,todate=TO_DATE,totime=TO_TIME)
        TIMESHEET.save()
        USERHISTORY=UserReserveHistory(user=user,status_reserved=True,CIN=CIN,fromdate=FROM_DATE,fromtime=FROM_TIME,todate=TO_DATE,totime=TO_TIME)
        USERHISTORY.save()
        context['success']='Reserve Successful!'
        response_text=render_to_string("JSON/error_mile.json",context)
        return HttpResponse(response_text, content_type="application/json")
    else:
        for carsheet in TheCarSheets:
            #newfrom>oldto || newto>oldfrom
            if comparedate(FROM_DATE,carsheet.todate)>0 or comparedate(TO_DATE,carsheet.fromdate)<0 :
                continue
            #newfrom=oldto
            elif comparedate(FROM_DATE,carsheet.todate)==0:
                if(comparetime(FROM_TIME,carsheet.totime)!=1):
                    overlap_mark=1
                    break
            #newto=oldfrom
            elif comparedate(TO_DATE,carsheet.fromdate)==0:
                if(comparetime(TO_TIME,carsheet.fromtime)!=-1):
                    overlap_mark=1
                    break
            else:
                overlap_mark=1
                break
        if overlap_mark==0:
            TIMESHEET=CarReserveTimeSheet(car=car,fromdate=FROM_DATE,fromtime=FROM_TIME,todate=TO_DATE,totime=TO_TIME)
            TIMESHEET.save()
            USERHISTORY=UserReserveHistory(user=user,status_reserved=True,CIN=CIN,fromdate=FROM_DATE,fromtime=FROM_TIME,todate=TO_DATE,totime=TO_TIME)
            USERHISTORY.save()
            context['success']='Reserve Successful!'
            response_text=render_to_string("JSON/error_mile.json",context)
            return HttpResponse(response_text, content_type="application/json")
        else:
            context['error_overlap']='Fail: You cannot reserve the car within the selected time.Please select again!'
            response_text=render_to_string("JSON/error_mile.json",context)
            return HttpResponse(response_text, content_type="application/json")


@admin_required(login_url='/userlogin/')
@transaction.atomic
def ajax_get_return_car(request):
    context={}
    context['ReserveHistory']=''
    context['User_email']=''
    if 'carCIN' not in request.GET or request.GET['carCIN'] == '':
        context['error_CIN_required']='Car CIN is required'
        response_text=render_to_string("JSON/error_return.json",context)
        return HttpResponse(response_text, content_type="application/json")
    if ('username' not in request.GET or request.GET['username'] == '') and \
            ('email' not in request.GET or request.GET['email'] == '') :
        context['error_username_email_required']='Either Username or email is required'
        response_text=render_to_string("JSON/error_return.json",context)
        return HttpResponse(response_text, content_type="application/json")
    CIN=request.GET['carCIN']
    Username=request.GET['username']
    Email=request.GET['email']

    if Email=='':
        history = UserReserveHistory.objects.filter(CIN=CIN,user__username=Username,status_confirmed=True,status_returned=False)
        if not history:
            context['error_match']='There is no such match in system.'
            response_text=render_to_string("JSON/error_return.json",context)
            return HttpResponse(response_text, content_type="application/json")
        #SUCCESS RETURN INFOR.
        user=User.objects.get(username=Username)
        context['ReserveHistory']=history
        context['User_email']=user.email
        response_text=render_to_string("JSON/error_return.json",context)
        return HttpResponse(response_text, content_type="application/json")
    elif Username=='':
        user=get_object_or_404(User, email=Email)
        #history = UserReserveHistory.objects.filter(CIN=CIN,user=user,status_confirmed=True)
        history = UserReserveHistory.objects.filter(CIN=CIN,user=user,status_confirmed=True,status_returned=False)
        if not history:
            context['error_match']='There is no such match in system.'
            response_text=render_to_string("JSON/error_return.json",context)
            return HttpResponse(response_text, content_type="application/json")
        #SUCCESS RETURN INFOR.
        context['ReserveHistory']=history
        context['User_email']=user.email
        response_text=render_to_string("JSON/error_return.json",context)
        return HttpResponse(response_text, content_type="application/json")
    else:
        user=User.objects.filter(username=Username, email=Email)
        if not user:
            context['error_match']='Username and Email do not match'
            response_text=render_to_string("JSON/error_return.json",context)
            return HttpResponse(response_text, content_type="application/json")
        user=User.objects.get(username=Username, email=Email)
        history = UserReserveHistory.objects.filter(CIN=CIN,user=user,status_confirmed=True,status_returned=False)
        if not history:
            context['error_match']='There is no such match in system.'
            response_text=render_to_string("JSON/error_return.json",context)
            return HttpResponse(response_text, content_type="application/json")
        #SUCCESS RETURN INFOR.
        context['ReserveHistory']=history
        context['User_email']=user.email#object
        response_text=render_to_string("JSON/error_return.json",context)
        return HttpResponse(response_text, content_type="application/json")

@admin_required(login_url='/userlogin/')
@transaction.atomic
def add_return(request):
    context={}
    if 'h_CIN' not in request.POST or request.POST['h_CIN']=='' or \
        'h_email' not in request.POST or request.POST['h_email']=='' \
        'h_fromdate' not in request.POST or request.POST['h_fromdate']==''\
        'h_todate' not in request.POST or request.POST['h_todate']=='':
        context['return_error']='Failing to return, Please retry.'
        response_text=render_to_string("JSON/error_return.json",context)
        return HttpResponse(response_text, content_type="application/json")

    CIN=request.POST['h_CIN']
    email=request.POST['h_email']
    fromdate=request.POST['h_fromdate']
    todate=request.POST['h_todate']
    mile_final=request.POST['h_mile_final']
    user=get_object_or_404(User, email=email)
    history = UserReserveHistory.objects.filter(CIN=CIN,user=user,status_confirmed=True,status_returned=False)
    if not history:
        context['return_error']='Failing to return, Please retry.'
        response_text=render_to_string("JSON/error_return.json",context)
        return HttpResponse(response_text, content_type="application/json")

    #SUCCESS RETURN INFOR.
    # 1. Inventory
    car=get_object_or_404(CarInventory,CIN=CIN)
    car.status="Avaliable"
    car.save(update_fields=['status'])
    car.mile=mile_final
    car.save(update_fields=['mile'])
    # 2. TimeSheet
    timesheet=CarReserveTimeSheet.objects.get(car=car,fromdate=fromdate,todate=todate)
    timesheet.delete()
    print("here1")
    # 3. ReserveHistory
    history=UserReserveHistory.objects.get(CIN=CIN,user=user,status_confirmed=True,status_returned=False)
    history.status_returned=True
    history.save(update_fields=['status_returned'])

    context['return_success']="Return Successfully."
    response_text=render_to_string("JSON/error_return.json",context)
    return HttpResponse(response_text, content_type="application/json")


@admin_required(login_url='/userlogin/')
@transaction.atomic
def generate_sheet(request):
    context={}
    # A number is required in mile field
    if 'final_mile' not in request.GET or request.GET['final_mile'] == '' or isNum(request.GET['final_mile'])== False:
        context['error_mile_match']='Please enter a valid nubmer in mile field!'
        response_text=render_to_string("JSON/error_return.json",context)
        return HttpResponse(response_text, content_type="application/json")
    # Other information must be in the sheet
    if 'car_CIN' not in request.GET or request.GET['car_CIN'] == '' or \
        'customer_name' not in request.GET or request.GET['customer_name'] == '' or \
        'customer_email' not in request.GET or request.GET['customer_email'] == '' or \
        'customer_fromdate' not in request.GET or request.GET['customer_fromdate'] == '' or \
        'customer_fromtime' not in request.GET or request.GET['customer_fromtime'] == '' or \
        'customer_todate' not in request.GET or request.GET['customer_todate'] == '' or \
        'customer_totime' not in request.GET or request.GET['customer_totime'] == '':
        #print(request.GET['car_CIN'])
        context['error_sheet']='The sheet content is not integral!'
        response_text=render_to_string("JSON/error_return.json",context)
        return HttpResponse(response_text, content_type="application/json")

    CIN = request.GET['car_CIN']
    final_mile = request.GET['final_mile']
    email = request.GET['customer_email']
    fromdate = request.GET['customer_fromdate']
    fromtime = request.GET['customer_fromtime']
    todate = request.GET['customer_todate']
    totime = request.GET['customer_totime']

    car_last_mile = CarInventory.objects.get(CIN=CIN).mile
    car_fee = CarType.objects.get(cartype=CarInventory.objects.get(CIN=CIN).cartype).rentalfee
    # check mile is correct > old mile value
    if float(final_mile) < float(car_last_mile):
        context['error_mile_match']='When ruturn, MILE should be Greater than original!'
        response_text=render_to_string("JSON/error_return.json",context)
        return HttpResponse(response_text, content_type="application/json")
    context["CIN"] = CIN
    context["car_fee"]=car_fee
    context["email"] = email
    context["mile_final"]= float(final_mile)
    context["mile_diff"]= float(final_mile)-float(car_last_mile)
    context["fromdate"]=fromdate
    context["fromtime"]=fromtime
    context["todate"]=todate
    context["totime"]=totime
    response_text=render_to_string("JSON/error_return.json",context)
    return HttpResponse(response_text, content_type="application/json")

def isNum(value):
    try:
        int(float(value))
    except TypeError:
        return False
    except ValueError:
        return False
    except Exception, e:
        return False
    else:
        return True

#--------------------------------#
@admin_required(login_url='/userlogin/')
@transaction.atomic
def get_confirmdata(request, orderid):
    context={}
    order=UserReserveHistory.objects.get(id=orderid)
    cin=order.CIN
    car=CarInventory.objects.get(CIN=cin)
    context["car"]=car
    response_text=render_to_string("JSON/carconfirm.json",context)
    return HttpResponse(response_text, content_type="application/json")

@admin_required(login_url='/userlogin/')
@transaction.atomic
def add_confirm(request):
    context={}
    if 'oldmiles' not in request.POST or request.POST['oldmiles'] == '':
        context['error_mile_required']='Old Mile Field is required'
        response_text=render_to_string("JSON/error_mile.json",context)
        return HttpResponse(response_text, content_type="application/json")

    CIN = request.POST['h_CIN']
    FROM_DATE = request.POST['h_fromdate']
    FROM_TIME = request.POST['h_fromtime']
    TO_DATE = request.POST['h_todate']
    TO_TIME = request.POST['h_totime']
    username = request.POST['h_user']
    print(CIN)
    car=get_object_or_404(CarInventory,CIN=CIN)

    if (isNum(request.POST['oldmiles'])==False):
        context['error_mile_required']='Old Mile error!'
        response_text=render_to_string("JSON/error_mile.json",context)
        return HttpResponse(response_text, content_type="application/json")
    
    if (float(request.POST['oldmiles'])<float(car.mile)):
        print(car.mile)
        print(request.POST['oldmiles'])
        context['error_mile_required']='Old Mile error!'
        response_text=render_to_string("JSON/error_mile.json",context)
        return HttpResponse(response_text, content_type="application/json")

    TheUserHistory = UserReserveHistory.objects.get(CIN = CIN,user__username = username,fromdate = FROM_DATE,fromtime = FROM_TIME,todate = TO_DATE,totime = TO_TIME)
    print(TheUserHistory)

    if(TheUserHistory.status_confirmed==True):
        context['success']='Already Confirmed!'
        response_text=render_to_string("JSON/error_mile.json",context)
        return HttpResponse(response_text, content_type="application/json")

    else:
        TheUserHistory.status_confirmed=True
        TheUserHistory.save()
        
        car.mile=request.POST['oldmiles']
        car.save()
        
        context['success']='Confirm Successful!'
        response_text=render_to_string("JSON/error_mile.json",context)
        return HttpResponse(response_text, content_type="application/json")

@admin_required(login_url='/userlogin/')
@transaction.atomic
def add_delete(request):
    context={}
    
    CIN = request.POST['h_CIN']
    FROM_DATE = request.POST['h_fromdate']
    FROM_TIME = request.POST['h_fromtime']
    TO_DATE = request.POST['h_todate']
    TO_TIME = request.POST['h_totime']
    username = request.POST['h_user']
    print(CIN)
    car=get_object_or_404(CarInventory,CIN=CIN)
    
    TheUserHistory = UserReserveHistory.objects.get(CIN = CIN,user__username = username,fromdate = FROM_DATE,fromtime = FROM_TIME,todate = TO_DATE,totime = TO_TIME)
    print(TheUserHistory)

    if(TheUserHistory.status_confirmed==True):
        context['error_conflict']='This reservation has been confirmed! You cannot delete it!'
        response_text=render_to_string("JSON/error_mile.json",context)
        return HttpResponse(response_text, content_type="application/json")

    if(TheUserHistory.status_returned==True):
        context['error_conflict']='This car has been returned! You cannot delete!'
        response_text=render_to_string("JSON/error_mile.json",context)
        return HttpResponse(response_text, content_type="application/json")


    if(TheUserHistory.status_deleted==True):
        context['success']='Already Delete!'
        response_text=render_to_string("JSON/error_mile.json",context)
        return HttpResponse(response_text, content_type="application/json")
    else:
        TheUserHistory.status_deleted=True
        TheUserHistory.save()
        
        TheTimeSheet = CarReserveTimeSheet.objects.get(car=car,fromdate = FROM_DATE,fromtime = FROM_TIME,todate = TO_DATE,totime = TO_TIME)
        TheTimeSheet.delete()
        
        context['success']='Delete Successful!'
        response_text=render_to_string("JSON/error_mile.json",context)
        return HttpResponse(response_text, content_type="application/json")

@admin_required(login_url='/userlogin/')
@transaction.atomic
def edit_car(request):
    context={}
    carid=request.POST['ed_carid']
    print(carid)
    car=get_object_or_404(CarInventory,id=carid)
    print(car)

    if(request.POST['miles']=='' or request.POST['fee']==''):
        context['error_mile_required']='Please enter new value!'
        response_text=render_to_string("JSON/edit_car.json",context)
        return HttpResponse(response_text, content_type="application/json")
    print("here")
    if isNum(request.POST['miles'])==False or isNum(request.POST['fee'])==False :
        print("here2")
        context['error_mile_required']='Input should be a valid number!'
        response_text=render_to_string("JSON/edit_car.json",context)
        return HttpResponse(response_text, content_type="application/json")
    if(float(request.POST['miles'])<float(car.mile)):
        context['error_mile_required']='New mile is smaller than old one!'
        response_text=render_to_string("JSON/edit_car.json",context)
        return HttpResponse(response_text, content_type="application/json")

    if request.POST['miles']:
        car.mile=request.POST['miles']
        car.save()
    if request.POST['fee']:
        cartype=CarType.objects.get(cartype=car.cartype)
        cartype.rentalfee=request.POST['fee']
        cartype.save()

    context['success']='Edit success!'
    context['mile']=car.mile
    context['fee']=cartype.rentalfee
    response_text=render_to_string("JSON/edit_car.json",context)
    return HttpResponse(response_text, content_type="application/json")
@logingen_required(login_url='/userlogin/')
@transaction.atomic
def add_deletegen(request):
    context={}
    
    CIN = request.POST['g_CIN']
    FROM_DATE = request.POST['g_fromdate']
    FROM_TIME = request.POST['g_fromtime']
    TO_DATE = request.POST['g_todate']
    TO_TIME = request.POST['g_totime']
    username = request.POST['g_user']
    print(CIN)
    car=get_object_or_404(CarInventory,CIN=CIN)
    
    TheUserHistory = UserReserveHistory.objects.get(CIN = CIN,user__username = username,fromdate = FROM_DATE,fromtime = FROM_TIME,todate = TO_DATE,totime = TO_TIME)
    print(TheUserHistory)

    if(TheUserHistory.status_confirmed==True):
        context['error_conflict']='This reservation has been confirmed! You cannot delete it!'
        response_text=render_to_string("JSON/error_mile.json",context)
        return HttpResponse(response_text, content_type="application/json")

    if(TheUserHistory.status_returned==True):
        context['error_conflict']='This car has been returned! You cannot delete!'
        response_text=render_to_string("JSON/error_mile.json",context)
        return HttpResponse(response_text, content_type="application/json")

    if(TheUserHistory.status_deleted==True):
        context['success']='Already Delete!'
        response_text=render_to_string("JSON/error_mile.json",context)
        return HttpResponse(response_text, content_type="application/json")
    else:
        TheUserHistory.status_deleted=True
        TheUserHistory.save()
        
        TheTimeSheet = CarReserveTimeSheet.objects.get(car=car,fromdate = FROM_DATE,fromtime = FROM_TIME,todate = TO_DATE,totime = TO_TIME)
        TheTimeSheet.delete()
        
        context['success']='Delete Successful!'
        response_text=render_to_string("JSON/error_mile.json",context)
        return HttpResponse(response_text, content_type="application/json")

#----------------------------------------------------------------------------------------------#


@logingen_required(login_url='/userlogin/')
def index(request):
    context={}
    if request.method == 'POST':
        print request.POST.get('cartype')
        requiretype = request.POST.get('cartype')
        if requiretype == 'all':
            cars=CarInventory.objects.all()
            context['cars'] = cars
            context['url_next']='GeneralUser/Home.html'
            context['cartypes']=CarType.objects.all().order_by('cartype');
            return makeview(request,context)
        else:
            requirecartype = CarType.objects.get(cartype = requiretype)
            cars=CarInventory.objects.filter(cartype = requirecartype)
            context['cars'] = cars
            context['url_next']='GeneralUser/Home.html'
            context['cartypes']=CarType.objects.all().order_by('cartype');
            return makeview(request,context)
    else:
        cars=CarInventory.objects.all()
        context['cars'] = cars
        context['url_next']='GeneralUser/Home.html'
        context['cartypes']=CarType.objects.all().order_by('cartype');
        return makeview(request,context)
#return render(request,'AdministratorUser/Home_admin.html',{})

def superuser_required(login_url=None):
    return user_passes_test(lambda u:u.is_superuser, login_url=login_url)

@superuser_required(login_url='/userloginSuper/')
def registerAdmin(request):
    context = {}
    if request.method == 'GET':
        registerform = RegisterForm()
        context = {'registerform':registerform}
        return render(request, 'Sign_in/registerAdmin.html', context)
    
    registerform = RegisterForm(request.POST)
    if not registerform.is_valid():
        context = {'registerform':registerform}
        return render(request, 'Sign_in/registerAdmin.html', context)

    new_user = User.objects.create_user(username = registerform.cleaned_data['username'],
                                        password = registerform.cleaned_data['password1'],
                                        email = registerform.cleaned_data['email'])

    # Mark the user as inactive to prevent login before email confirmation.
    new_user.is_staff = True
    new_user.is_active = False
    new_user.save()
    
    # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(new_user)
    
    email_body = """
    Welcome to the CRS.  Please click the link below to
    verify your email address and complete the registration of your account:
        
    http://%s%s
    """ % (request.get_host(),
           reverse('confirmAdmin', args=(new_user.username, token)))
            
    send_mail(subject="Verify your email address",
          message= email_body,
          from_email="crswelcome@gmail.com",
          recipient_list=[new_user.email])
               
    context['email'] = registerform.cleaned_data['email']
    return render(request, 'Sign_in/needs-confirmation.html', context)

@transaction.atomic
def confirmAdmin_registration(request, username, token):
    user = get_object_or_404(User, username=username)
    
    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404
    
    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'Sign_in/confirmedAdmin.html', {})

def userlogout(request):
    logout(request);
    return HttpResponseRedirect('home')

def adminlogout(request):
    logout(request);
    return HttpResponseRedirect('home-admin')

def superlogout(request):
    logout(request);
    return HttpResponseRedirect('superuser')

def logouts(request):
    logout(request);
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def findpass(request):
    context = {}
    if request.method == 'GET':
        findpassform = FindPass();
        context = {'findpassform':findpassform}
        return render(request, 'Sign_in/forgetpass.html', context)

    findpassform = FindPass(request.POST)
    context = {'findpassform':findpassform}
    if not findpassform.is_valid():
        return render(request, 'Sign_in/forgetpass.html', context)

    forgetuser = User.objects.get(username = findpassform.cleaned_data['username'])
    email_corr = forgetuser.email
    email_input = findpassform.cleaned_data['email']

    if email_corr == email_input:
        # forgetuser.backend = 'django.contrib.auth.backends.ModelBackend'
        #login(request, forgetuser)

        # Generate a one-time use token and an email message body
        token = default_token_generator.make_token(forgetuser)
    
        email_body = """
            Please click the link below to reset your password:
        http://%s%s
        """ % (request.get_host(),
               reverse('confirmfindpass', args=(forgetuser.username, token)))
            
        send_mail(subject="Reset your password",
              message= email_body,
              from_email="crswelcome@gmail.com",
              recipient_list=[email_corr])
               
        context['email'] = email_corr
        return render(request, 'Sign_in/needs-confirmation-password.html', context)
    context['errorinfo'] = "The username and the email is not match"
    return render(request, 'Sign_in/forgetpass.html', context)

@transaction.atomic
def confirm_findpass(request, username, token):

    context = {}
    user = get_object_or_404(User, username=username)
    
    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    resetpassform = ResetPass()
    context['resetpassform'] = resetpassform
    return render(request, 'Sign_in/reset_password.html', context)

@login_required(login_url='/userlogin/')
def resetPassword(request):
    context = {}
    resetpassform = ResetPass(request.POST)
    if not resetpassform.is_valid():
        context['resetpassform'] = resetpassform
        return render(request, 'Sign_in/reset_password.html', context)

    user = request.user
    newpass = request.POST.get('password1')
    user.set_password(newpass)
    user.save()
    context = {}
    loginform = LoginForm();
    registerform = RegisterForm()
    context = {'form':loginform, 'registerform':registerform}
    return render(request, 'Sign_in/userlogin.html', context)

def register(request):
    context = {}
    loginform = LoginForm();
    if request.method == 'GET':
        registerform = RegisterForm()
        context = {'form':loginform, 'registerform':registerform}
        return render(request, 'Sign_in/userlogin.html', context)
    
    registerform = RegisterForm(request.POST)
    if not registerform.is_valid():
        context = {'form':loginform, 'registerform':registerform}
        return render(request, 'Sign_in/userlogin.html', context)

    new_user = User.objects.create_user(username = registerform.cleaned_data['username'],
                                        password = registerform.cleaned_data['password1'],
                                        email = registerform.cleaned_data['email'])

    # Mark the user as inactive to prevent login before email confirmation.
    #new_user.is_active = False
    new_user.save()
    
    # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(new_user)
    
    email_body = """
    Welcome to the grumblr.  Please click the link below to
    verify your email address and complete the registration of your account:
        
    http://%s%s
    """ % (request.get_host(),
           reverse('confirm', args=(new_user.username, token)))
            
    send_mail(subject="Verify your email address",
          message= email_body,
          from_email="crswelcome@gmail.com",
          recipient_list=[new_user.email])
               
    context['email'] = registerform.cleaned_data['email']
    return render(request, 'Sign_in/needs-confirmation.html', context)

@transaction.atomic
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)
    
    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404
    
    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()
    return render(request, 'Sign_in/confirmed.html', {})

@logingen_required(login_url='/userlogin/')
def home(request):
    context={}
    if request.method == 'POST':
        print request.POST.get('cartype')
        requiretype = request.POST.get('cartype')
        if requiretype == 'all':
            cars=CarInventory.objects.all()
            count = cars.count()
            print count
            firstid = cars.aggregate(Min('id'))
            
            print firstid['id__min']
            context['firstid'] = firstid['id__min']
            context['cars'] = cars
            context['url_next']='GeneralUser/Home.html'
            context['cartypes']=CarType.objects.all().order_by('cartype');
            return makeview(request,context)
        else:
            requirecartype = CarType.objects.get(cartype = requiretype)
            cars=CarInventory.objects.filter(cartype = requirecartype)
            count = cars.count()
            print count
            firstid = cars.aggregate(Min('id'))
            context['firstid'] = firstid['id__min']
            context['cars'] = cars
            context['url_next']='GeneralUser/Home.html'
            context['cartypes']=CarType.objects.all().order_by('cartype');
            return makeview(request,context)
    else:
        cars=CarInventory.objects.all()
        count = cars.count()
        firstid = cars.aggregate(Min('id'))
        context['firstid'] = firstid['id__min']
        context['cars'] = cars
        context['url_next']='GeneralUser/Home.html'
        context['cartypes']=CarType.objects.all().order_by('cartype');
        return makeview(request,context)

@logingen_required(login_url='/userlogin/')
def profile(request):
    context = {}
    changeform=ChangePass()
    profileform=Profiles()
    print request.user
    try:
        profilecur = Profile.objects.get(owner=request.user)
    except:
        profilecur = Profile.objects.create(owner=request.user)

    profileform = Profiles(instance=profilecur)

    if request.method == 'GET':
        context['profilecur'] = profilecur
        context['profileform'] = profileform
        context['id'] = request.user.id
        context['currentuser'] = request.user
        context['changeform']=changeform
        return render(request, 'GeneralUser/Profile.html', context)
    
    profileform = Profiles(request.POST, request.FILES, instance=profilecur)
    if not profileform.is_valid():
        context['profilecur'] = profilecur
        context['id'] = request.user.id
        context['currentuser'] = request.user
        context['profileform'] = profileform
        context['changeform']=changeform
        return render(request, 'GeneralUser/Profile.html', context)

    profileform.save()
    context['profileform'] = profileform
    context['id'] = request.user.id
    context['currentuser'] = request.user
    context['changeform']=changeform
    context['profilecur']=Profile.objects.get(owner=request.user)
    
    return render(request,'GeneralUser/Profile.html',context)

@login_required
def getphoto(request, user_id):
    profilecur = get_object_or_404(Profile, owner=User.objects.get(id=user_id))
    if not profilecur.picture:
        raise Http404
    content_type = guess_type(profilecur.picture.name)
    return HttpResponse(profilecur.picture, content_type=content_type)

@login_required
def getcarpicture(request, car_id):
    carcur = get_object_or_404(CarInventory, id=car_id)
    if not carcur.cartype.picture:
        raise Http404
    content_type = guess_type(carcur.cartype.picture.name)
    return HttpResponse(carcur.cartype.picture, content_type=content_type)

@logingen_required(login_url='/userlogin/')
def history(request):
    context={}
    try:
        profilecur = Profile.objects.get(owner=request.user)
    except:
        profilecur = Profile.objects.create(owner=request.user)

    context['id'] = request.user.id
    context['currentuser'] = request.user
    context['profilecur'] = profilecur
    context['historys']=UserReserveHistory.objects.filter(user__id=request.user.id)
    return render(request,'GeneralUser/History.html',context)


@admin_required(login_url='/userloginAdmin/')
def home_admin(request):
    context={}
    if request.method == 'POST':
        print request.POST.get('cartype')
        requiretype = request.POST.get('cartype')
        if requiretype == 'all':
            cars=CarInventory.objects.all()
            context['cars'] = cars
            context['url_next']='AdministratorUser/Home_admin.html'
            context['cartypes']=CarType.objects.all().order_by('cartype')
            return makeview(request,context)
        else:
            requirecartype = CarType.objects.get(cartype = requiretype)
            cars=CarInventory.objects.filter(cartype = requirecartype)
            context['cars'] = cars
            context['url_next']='AdministratorUser/Home_admin.html'
            context['cartypes']=CarType.objects.all().order_by('cartype')
            return makeview(request,context)
    else:
        cars=CarInventory.objects.all()
        context['cars'] = cars
        context['url_next']='AdministratorUser/Home_admin.html'
        context['cartypes']=CarType.objects.all().order_by('cartype')
        return makeview(request,context)

@admin_required(login_url='/userlogin/')
def inventory(request):
    context={}
    context['cartypes']=CarType.objects.all().order_by('cartype')
    tempcars=CarInventory.objects.all()
    for tempcar in tempcars:
        tempcar_object=get_object_or_404(CarInventory,CIN=tempcar.CIN)
        #only check reservetimesheet
        if(checkIfTodayCarAvalable(tempcar_object)==False):
            tempcar_object.status="Unavaliable"
            tempcar_object.save(update_fields=['status'])
        else:
            tempcar_object.status="Avaliable"
            tempcar_object.save(update_fields=['status'])
    context['allcars']=CarInventory.objects.all().order_by('-cartype')
    context['url_next']='AdministratorUser/Inventory.html'
    return makeview(request,context)

@admin_required(login_url='/userloginAdmin/')
def reservation(request):
    context={}
    nowdate=datetime.date.today().strftime("%m/%d/%Y")
    context['today_orders'] = UserReserveHistory.objects.filter(fromdate=nowdate,status_reserved=True)
    context['future_orders'] = UserReserveHistory.objects.filter(fromdate__gt=nowdate,status_reserved=True)
    print(context['future_orders'])
    return render(request,'AdministratorUser/Reservation.html',context)

@admin_required(login_url='/userloginAdmin/')
def returncheck(request):
    context={}
    context["allGeneralUsers"]=User.objects.filter(is_staff=False).order_by('username')
    context['allCars']=CarInventory.objects.all().order_by('-cartype')
    return render(request,'AdministratorUser/Return.html',context)

@admin_required(login_url='/userloginAdmin/')
def customer(request):
    context={}
    context={'profilecur':[], 'currentcustomer':[]}
    context['customer']=User.objects.filter(is_staff=False)
    return render(request,'AdministratorUser/Customer.html',context)

@admin_required(login_url='/userloginAdmin/')
def customerprofile(request, user_id):
    context={}
    #context['id'] = request.user.id
    #context['currentuser'] = request.user
    #user_id = 1
    userview = get_object_or_404(User,id = user_id)
    #userview = User.objects.get(id = user_id)
    try:
        profilecur = Profile.objects.get(owner = userview)
    except:
        context = {'profilecur': []}
    else:
        profilecur = Profile.objects.get(owner = userview)
        #profileform = Profiles(instance=profilecur)
        context = {'profilecur':profilecur}
#context['id'] = request.user.id
    context['currentcustomer'] = userview
    context['historys']=UserReserveHistory.objects.filter(user__id=user_id)
#   context['viewid'] = user_id
#   context['viewname'] = userview.username
#context={'profilecur':[]}
    context['customer']=User.objects.filter(is_staff=False)
    return render(request,'AdministratorUser/Customer.html',context)


@logingen_required(login_url='/userlogin/')
def changepass(request):
    username = request.user.username
    oldpass = request.POST.get('Old_Password')
    user = authenticate(username=username,password=oldpass)
    if user is not None and user.is_active:
        newpass = request.POST.get('New_Password')
        user.set_password(newpass)
        user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



