from django.conf.urls import url, include

from app.views import index
from app.views import login, logout
import app.views_deposit as deposit
import app.views_client as client
import app.views_admin as admin

urlpatterns = [
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^admin/', include([
        url(r'^deposit_configurator/', admin.DepositConfigurator, name='depositConfigurator'),
        url(r'^newCurrency/', admin.NewCurrency, name='newCurrency'),
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
        url(r'^list/', deposit.list, name='list'),
        url(r'^open/', deposit.open, name='open'),
        url(r'^refill/', deposit.refill, name='refill'),
        url(r'^transfer/', deposit.transfer, name='transfer'),
        url(r'^close/', deposit.close, name='close'),
        url(r'^extract/', deposit.extract, name='extract'),
        url(r'^history/', deposit.history, name='history')
    ], namespace='deposit')),
    url(r'', index, name='index'),
]
