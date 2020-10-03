from os import name
from django.contrib import admin
from django.db.models.query_utils import PathInfo
from django.urls import path
from .views import registerview, loginview, homeview, logoutview, updateview, listview, deleteview, dataview, statsview



urlpatterns = [
        path('', loginview, name='login'),
        path('register/', registerview, name='register'),
        path('login/', loginview, name='login'),
        path('home/', homeview, name='home'),
        path('logout/', logoutview, name='logout'),
        path('update/<int:pk>', updateview, name='update'),
        path('list/', listview, name='list'),
        path('delete/', deleteview, name='delete'),
        path('data/', dataview, name='data'),
        path('stats/', statsview, name='stats'),
        
]