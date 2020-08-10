from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    # url(r'^test/$', views.TestView.as_view(), name='login'),
    url(r'^images/$', views.ImageCodeView.as_view()),
    url(r'sms_codes/(?P<mobile>1[3-9]\d{9})/$', views.SMSCodeView.as_view()),

]
