from django.conf.urls import patterns, include, url
from CRSapp.forms import *

urlpatterns = patterns('',
    
    url(r'^userlogin/$', 'django.contrib.auth.views.login', {'template_name':'Sign_in/userlogin.html', 'authentication_form': LoginForm, 'extra_context':{'registerform':RegisterForm}}, name = 'userLogin'),
                       
    url(r'^userloginSuper/$', 'django.contrib.auth.views.login', {'template_name':'Sign_in/userloginSuper.html', 'authentication_form': LoginForm, 'extra_context':{'registerform':RegisterForm}}, name = 'userLoginSuper'),
    
    url(r'^userloginAdmin/$', 'django.contrib.auth.views.login', {'template_name':'Sign_in/userloginAdmin.html', 'authentication_form': LoginForm, 'extra_context':{'registerform':RegisterForm}}, name = 'userLoginAdmin'),
    
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name = "logout"),
    url(r'^userlogout$', 'CRSapp.views.userlogout', name = "userlogout"),
    url(r'^adminlogout$', 'CRSapp.views.adminlogout', name = "adminlogout"),
    url(r'^superlogout$', 'CRSapp.views.superlogout', name = "superlogout"),
                       
    url(r'^register$', 'CRSapp.views.register',name='register'),
    url(r'^$','CRSapp.views.index'),
                       #url(r'^index.html$', 'grumblrApp.views.index', name="grumblrApp_index"),
                       #url(r'^home.html$', 'grumblrApp.views.home',name="grumblrApp_home"),
    url(r'^home$', 'CRSapp.views.home',name='CRSapp_home'),
    url(r'^profile$', 'CRSapp.views.profile',name='CRSapp_profile'),
    url(r'^history$', 'CRSapp.views.history',name='CRSapp_history'),
    url(r'^home-admin$', 'CRSapp.views.home_admin',name='CRSapp_home_admin'),
    url(r'^inventory$', 'CRSapp.views.inventory',name='CRSapp_inventory'),
    url(r'^reservation$', 'CRSapp.views.reservation',name='CRSapp_reservation'),
    url(r'^return$', 'CRSapp.views.returncheck',name='CRSapp_return'),
    url(r'^customer$', 'CRSapp.views.customer',name='CRSapp_customer'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9_@\+\- ]+)/(?P<token>[a-z0-9\-]+)$', 'CRSapp.views.confirm_registration', name='confirm'),
                       
    url(r'^confirmAdmin-registration/(?P<username>[a-zA-Z0-9_@\+\- ]+)/(?P<token>[a-z0-9\-]+)$', 'CRSapp.views.confirmAdmin_registration', name='confirmAdmin'),
                       
    url(r'^changepass$', 'CRSapp.views.changepass', name = 'ChangePass'),
                       
    url(r'^superuser$', 'CRSapp.views.registerAdmin',name='registerAdmin'),
    
    url(r'^db$', 'CRSapp.views.db', name='db'),
    url(r'^findpass$', 'CRSapp.views.findpass',name='FindPass'),
                       
    url(r'^confirm-findpass/(?P<username>[a-zA-Z0-9_@\+\- ]+)/(?P<token>[a-z0-9\-]+)$', 'CRSapp.views.confirm_findpass', name='confirmfindpass'),
                       
    url(r'^resetPassword$', 'CRSapp.views.resetPassword',name='resetPassword'),
    url(r'^getphoto/(?P<user_id>\d+)$','CRSapp.views.getphoto', name = 'getphoto'),
    url(r'^getcarpicture/(?P<car_id>\d+)$','CRSapp.views.getcarpicture', name = 'getcarpicture'),
    url(r'^customerprofile/(?P<user_id>\d+)$','CRSapp.views.customerprofile', name = 'CustomerProfile'),
                       
    #---------------------------------#
    url(r'^add_confirm$','CRSapp.views.add_confirm', name = 'CRSapp_add_confirm'),
                       #-------------------------------#
    url(r'^get_confirmdata/(?P<orderid>\d+)$','CRSapp.views.get_confirmdata', name = 'CRSapp_get_confirmdata'),
                       #-------------------------------#
    url(r'^add_delete$','CRSapp.views.add_delete', name = 'CRSapp_add_delete'),
    url(r'^add_deletegen$','CRSapp.views.add_deletegen', name = 'CRSapp_add_deletegen'),
    url(r'^edit_car$','CRSapp.views.edit_car', name = 'CRSapp_edit_car'),
    #-----------szy---------#

    url(r'^generate_sheet$', 'CRSapp.views.generate_sheet', name = 'CRSapp_ajax_generate_sheet'),
    url(r'^add_return$', 'CRSapp.views.add_return', name = 'CRSapp_add_return'),
    url(r'^search_return_car$', 'CRSapp.views.ajax_get_return_car', name = 'CRSapp_ajax_return_car'),
    url(r'^add_reserve_general$', 'CRSapp.views.add_reserve_general', name = 'CRSapp_add_reserve_general'),
    url(r'^add_reserve$', 'CRSapp.views.add_reserve', name = 'CRSapp_add_reserve'),
    url(r'^get_all_generalUsers$', 'CRSapp.views.ajax_get_all_generalUsers', name = 'CRSapp_ajax_get_all_generalUsers'),
    url(r'^search_car_picture/(?P<cartype>\w+)$', 'CRSapp.views.get_car_picture', name = 'CRSapp_get_car_picture'),
    url(r'^search_cars$', 'CRSapp.views.ajax_get_cars', name = 'CRSapp_ajax_get_cars'),
    url(r'^add_car_type$', 'CRSapp.views.addCarTpye', name = 'CRSapp_addCarTpye'),
    url(r'^add_car$', 'CRSapp.views.addCar', name = 'CRSapp_addCar'),
    url(r'^delete_car$', 'CRSapp.views.deleteCar', name = 'CRSapp_add_delete_car'),

)