import imp
from django.urls import path
from .views import *

app_name = 'main'
urlpatterns = [
    path('accounts/logout/', BLogoutView.as_view(), name='logout'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/login/', BLoginView.as_view(), name='login'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]