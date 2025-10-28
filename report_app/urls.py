from django.urls import path
from .views import upload_report_view

urlpatterns = [
    path('report/', upload_report_view, name='report'),
]
