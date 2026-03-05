from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('emails/', views.EmployeeEmailListView.as_view(), name='email_list'),
    path('emails/add/', views.EmployeeEmailCreateView.as_view(), name='email_add'),
    path('emails/<int:pk>/edit/', views.EmployeeEmailUpdateView.as_view(), name='email_edit'),
    path('emails/<int:pk>/delete/', views.EmployeeEmailDeleteView.as_view(), name='email_delete'),
    path('verify-password/', views.verify_admin_password, name='verify_password'),
    path('emails/export/', views.export_emails_excel, name='export_emails'),
]
