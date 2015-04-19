# -*-coding:utf8-*-

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from views import *

urlpatterns = patterns('mgr.views',
                       url(r'^index[/]?$', login_required(PatientView.as_view()), name='list_patient'),
                       url(r'^btypes[/]?$', login_required(BtypeView.as_view()), name='list_btype'),
#                        url(r'^bcates[/]?$', login_required(BcateView.as_view()), name='list_bcate'),
                       url(r'^bcates[/]?$', login_required(BcateView.as_view()), name='list_bcate'),
                       url(r'^histories/(?P<uid>\d+)[/]?$', login_required(BHistoryView.as_view()), name='list_history'),
                       
                       url(r'^addbcate[/]?/',login_required(BcateCreate.as_view()),name='add_bcate'),
                       url(r'^addbtype[/]?/',login_required(BtypeCreate.as_view()),name='add_btype'),
                       url(r'^addpatient[/]?/',login_required(PatientCreate.as_view()),name='add_patient'),
                       url(r'^addhis/(?P<uid>\d+)[/]?$',login_required(BHistoryCreate.as_view()),name='add_bhistory'),
                       
                       url(r'^modhis/(?P<pk>\d+)[/]?$',login_required(BHistoryUpdate.as_view()),name='mod_bhistory'),
                       url(r'^modpatient/(?P<pk>\d+)[/]?$',login_required(PatientUpdate.as_view()),name='mod_patient'),
                       url(r'^modbtype/(?P<pk>\d+)[/]?$',login_required(BtypeUpdate.as_view()),name='mod_btype'),
                       url(r'^modbcate/(?P<pk>\d+)[/]?$',login_required(BcateUpdate.as_view()),name='mod_bcate'),
                       )
