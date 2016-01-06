"""
This dummy urlconf is here (along with its associated view) to allow Django
checks to pass when developing / testing management commands.

If/when additional Django apps are added to this project which implement
actual views/urls, this dummy url can be disposed of.
"""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
