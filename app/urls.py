from django.conf.urls import url, include

from app.views import index
from app.views import login, logout
import app.views_deposit as deposit

urlpatterns = [
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^deposit/', include([
        url(r'^list/', deposit.list, name='list'),
        url(r'^open/', deposit.open, name='open'),
        url(r'^refill/', deposit.refill, name='refill'),
        url(r'^transfer/', deposit.transfer, name='transfer'),
        url(r'^close/', deposit.close, name='close'),
        url(r'^extract/', deposit.extract, name='extract'),
        url(r'^history/', deposit.history, name='history')
    ])),
    url(r'', index, name='index'),
]
