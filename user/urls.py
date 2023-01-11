from django.urls import re_path

from . import views


app_name = 'user'

urlpatterns = [
    re_path(r'^signup/$', views.signup, name='signup'),
    re_path(r'^user/settings/$', views.settings, name='settings'),

]
