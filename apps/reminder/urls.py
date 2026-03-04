from django.urls import path
from . import views

app_name = 'reminder'

urlpatterns = [
    path('', views.reminder_view, name='reminder'),
]
