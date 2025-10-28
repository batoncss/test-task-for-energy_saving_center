from django.urls import path
from .views import upload_file

urlpatterns = [
    path('report/', upload_file, name='report'),
]
