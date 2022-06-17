from django.urls import path
from .views import boards
from .views import BoardDetailView

urlpatterns = [
    path('boards/<int:pk>/', BoardDetailView.as_view()),
    path('boards/', boards),
]