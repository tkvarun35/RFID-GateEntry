from django.urls import path

from .import views

urlpatterns=[
    path('',views.index,name='index'),
    path('connect',views.connect,name='index'),
    path('getData',views.getDeviceData,name='index'),
    path('getRTLog',views.getRTlog,name='index'),
    path('search',views.searchDevice,name='index'),
    path('getDeviceParam',views.getDeviceParam,name='index'),
    path('setDeviceParam',views.setDeviceParam,name='index'),
    path('restart',views.restart,name='index'),
    path('addUser',views.addUser,name='index'),
    path('deleteUser',views.deleteUser,name='index'),










]