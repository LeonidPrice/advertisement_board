from django.urls import path
from .views import boards
from .views import BoardDetailView
from .views import comments

urlpatterns = [
    path('boards/<int:pk>/comments/', comments),
    path('boards/<int:pk>/', BoardDetailView.as_view()),
    path('boards/', boards),
]