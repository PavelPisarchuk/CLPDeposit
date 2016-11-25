from django.conf.urls import url, include

from app.views import index
from app.views import login, logout
import app.views_deposit as deposit
import app.views_client as client
import app.views_admin as admin
import app.views_contract as contract

urlpatterns = [
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^admin/', include([
        url(r'^new/', admin.new, name='new'),
        url(r'^list/', admin.list, name='list'),
        url(r'^info/', admin.info, name='info'),
        url(r'^edit/', admin.edit, name='edit'),
    ], namespace='employee')),
    url(r'^client/', include([
        url(r'^list/', client.list, name='list'),
        url(r'^new/', client.new, name='new'),
        url(r'^info/', client.info, name='info'),
        url(r'^edit/', client.edit, name='edit'),
    ], namespace='client')),
    url(r'^deposit/', include([
        url(r'^list/(?P<deposit_id>[0-9]+)/', deposit.list, name='listToArch'),
        url(r'^list/', deposit.list, name='list'),
        url(r'^new/', deposit.new, name='new'),
        url(r'^edit/(?P<deposit_id>[0-9]+)/', deposit.edit, name='edit'),
        url(r'^currency/', deposit.currency, name='currency'),


        url(r'^refill/', deposit.refill, name='refill'),
        url(r'^transfer/', deposit.transfer, name='transfer'),
        url(r'^close/', deposit.close, name='close'),
        url(r'^extract/', deposit.extract, name='extract'),
        url(r'^history/', deposit.history, name='history')
    ], namespace='deposit')),
    url(r'^contract/', include([
        url(r'^all/', contract.all, name='all'),
        url(r'^new/(?P<deposit_id>[0-9]+)', contract.new, name='new'),
        url(r'^list/', contract.list, name='list'),
        url(r'^info/(?P<deposit_id>[0-9]+)', contract.info, name='info'),
    ], namespace='contract')),
    url(r'', index, name='index'),
]
