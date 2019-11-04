from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from .views import *


app_name = "capstone"
urlpatterns = [
    url(r'^$', Home, name='home'),
    url(r'^donations$', Donation_List, name='donations'),
    url(r'^donations/form/$', Donation_Form, name='donation_form'),
    url(r'^donations/form/(?P<donation_id>[0-9]+)$', Donation_Edit_Form, name="donation_edit_form"),
    url(r'^donations/(?P<donation_id>[0-9]+)$', Donation_Details, name="donation"),

    url(r'^report/$', Report_Details, name="report"),
    url(r'^map/$', Map, name="map"),

    url(r'accounts/', include('django.contrib.auth.urls')),
    url(r'^login/$', login_user, name='login'),
    url(r'^logout/$', logout_user, name='logout'),
    url(r'^register/$', register_user, name='register'),

]