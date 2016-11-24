from django.conf.urls import url, include

from app.views import index, rates
from app.views import login, logout, password
import app.views_deposit as deposit
import app.views_client as client
import app.views_admin as admin
import app.views_errors as errors
import app.views_messages as messages

urlpatterns = [
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^rates/', rates, name='rates'),
    url(r'^password/', password, name='password'),
    url(r'^message/', include([
        url(r'^send/(?P<pk>[0-9]+)/$', messages.send_message, name='send'),
        url(r'^updatemsg/', messages.updatemsg, name='updatemsg'),
        url(r'^messages/', messages.messages, name='messages'),
        url(r'^readmsg/(?P<pk>[0-9]+)/$', messages.readmessage, name='readmsg'),
    ], namespace='message')),
    url(r'^employee/', include([
        url(r'^new/', admin.new, name='new'),
        url(r'^list/', admin.list, name='list'),
        url(r'^info/', admin.info, name='info'),
        url(r'^edit/', admin.edit, name='edit'),
        url(r'^edituser/(?P<pk>[0-9]+)/$', admin.edit_user, name='uedit'),
        url(r'^edituser/', admin.edit_user, name='uedit'),
    ], namespace='employee')),
    url(r'^client/', include([
        url(r'^list/', client.list, name='list'),
        url(r'^new/', client.new, name='new'),
        url(r'^info/', client.info, name='info'),
        url(r'^edit/', client.edit, name='edit'),
        url(r'^search/', client.search, name='search'),
        url(r'^search/(?P<first_name>\w+)/(?P<last_name>\w+)/(?P<passport_id>\w+/$)', client.search, name='search'),
    ], namespace='client')),
    url(r'^deposit/', include([
        url(r'^list/', deposit.list, name='list'),
        url(r'^open/', deposit.open, name='open'),
        url(r'^refill/', deposit.refill, name='refill'),
        url(r'^transfer/', deposit.transfer, name='transfer'),
        url(r'^close/', deposit.close, name='close'),
        url(r'^extract/', deposit.extract, name='extract'),
        url(r'^history/', deposit.history, name='history')
    ], namespace='deposit')),
    url(r'errors/',include([
        url('r^permission/',errors.permission_error,name='error')
    ],namespace='errors')),
    url(r'', index, name='index'),
]
