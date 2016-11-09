from django.conf.urls import url

from app.views import Index

urlpatterns = [
    url(r'^index/', Index, name='IndexURL'),
]
