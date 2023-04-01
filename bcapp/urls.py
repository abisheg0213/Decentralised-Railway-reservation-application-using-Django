from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.display,name="display"),
    path('dis',views.d1,name="inner_page"),
    path('bookt',views.booktic,name="booktic"),
    path('cancelt',views.cantic,name="cantic"),
    path('ticdet',views.ticket_details,name="ticdetails"),
     path('tcavail',views.avreq,name="tic_Avail")
]   