from django.urls import path

from api_service import views

urlpatterns = [
    path('datasets/', views.datasets_view),
    path('datasets/<int:pk>/', views.DatasetDetailView.as_view()),
    path('datasets/<int:pk>/<slug:export_type>/', views.export_data),
]