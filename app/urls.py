from django.conf.urls import url, include

from app.views import index
from app.views import login, logout
import app.views_deposit as deposit
import app.views_client as client

urlpatterns = [
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^client/', include([
        url(r'^list/', client.list, name='client_list'),
        url(r'^new/', client.new, name='client_new'),
        url(r'^info/', client.info, name='client_info'),
        url(r'^edit/', client.edit, name='client_edit'),
    ])),
    url(r'^deposit/', include([
        url(r'^list/', deposit.list, name='deposit_list'),
        url(r'^open/', deposit.open, name='deposit_open'),
        url(r'^refill/', deposit.refill, name='deposit_refill'),
        url(r'^transfer/', deposit.transfer, name='deposit_transfer'),
        url(r'^close/', deposit.close, name='deposit_close'),
        url(r'^extract/', deposit.extract, name='deposit_extract'),
        url(r'^history/', deposit.history, name='deposit_history')
    ])),
    url(r'', index, name='index'),
]
