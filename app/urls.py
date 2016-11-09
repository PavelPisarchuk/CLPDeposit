from django.conf.urls import url, include

from app.views import index
from app.views import login, logout

urlpatterns = [
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^deposit/', include([

    ])),
    url(r'^/*', index, name='index'),
]
