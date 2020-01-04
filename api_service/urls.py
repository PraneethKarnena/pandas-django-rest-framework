from django.urls import path

from api_service import views

urlpatterns = [
    path('datasets/', views.DatasetListView.as_view()),
]