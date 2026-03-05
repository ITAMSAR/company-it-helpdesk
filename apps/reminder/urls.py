from django.urls import path
from . import views

app_name = 'reminder'

urlpatterns = [
    path('', views.reminder_view, name='reminder'),
    path('log/<int:pk>/delete/', views.delete_log, name='delete_log'),
    path('export/', views.export_logs_excel, name='export_logs'),
]
