from django.urls import path
from . import views
from . import qr_views

app_name = 'inventory'

urlpatterns = [
    # Equipment URLs
    path('', views.EquipmentListView.as_view(), name='equipment_list'),
    path('add/', views.EquipmentCreateView.as_view(), name='equipment_add'),
    path('<int:pk>/edit/', views.EquipmentUpdateView.as_view(), name='equipment_edit'),
    path('<int:pk>/delete/', views.EquipmentDeleteView.as_view(), name='equipment_delete'),
    path('export/', views.export_equipment_excel, name='export_equipment'),
    
    # QR Code Generation (login required)
    path('qr/<int:equipment_id>/', qr_views.generate_qr_code, name='generate_qr'),
    
    # Category URLs
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category_add'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
    
    # AJAX URLs
    path('api/subcategories/', views.get_subcategories, name='get_subcategories'),
    
    # Test mobile access
    path('test-mobile/', qr_views.test_mobile_access, name='test_mobile'),
]
