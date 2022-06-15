import imp
from django.urls import path
from .views import *

app_name = 'main'

urlpatterns = [
    path('accounts/logout/', BLogoutView.as_view(), name='logout'),
    path('account/profile/delete/', DeleteUserView.as_view(), name='profile_delete'),
    path('accounts/password/change/', BPasswordChangeView.as_view(), name='password_change'),
    path('account/profile/change/', ChangeUserInfoView.as_view(), name='profile_change'),
    path('account/profile/change/<int:pk>/', profile_board_change, name='profile_board_change'),
    path('account/profile/delete/<int:pk>/', profile_board_delete, name='profile_board_delete'),
    path('account/profile/add/', profile_board_add, name='profile_board_add'),
    path('accouts/profile/<int:pk>/', profile_board_detail, name='profile_board_detail'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/register/activate/<str:sign>/', user_activate, name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/login/', BLoginView.as_view(), name='login'),
    path('<int:rubric_pk>/<int:pk>/', detail, name='detail'),
    path('<int:pk>/', by_rubric, name='by_rubric'),
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
]

