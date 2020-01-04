from django.urls import path

from api_service import views

urlpatterns = [
    path('datasets/', views.datasets_view),
]