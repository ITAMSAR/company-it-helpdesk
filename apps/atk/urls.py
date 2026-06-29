from django.urls import path
from . import views

app_name = 'atk'

urlpatterns = [
    # ATK Items (langsung ke list, tidak perlu dashboard)
    path('', views.ATKItemListView.as_view(), name='item_list'),
    path('requests/', views.ATKRequestListView.as_view(), name='request_list'),
    path('requests/create/', views.ATKRequestCreateView.as_view(), name='request_create'),
    path('requests/<int:pk>/', views.ATKRequestDetailView.as_view(), name='request_detail'),
    path('requests/<int:pk>/lines/<int:line_pk>/link-item/', views.link_atk_request_line, name='request_line_link_item'),
    path('requests/<int:pk>/review/', views.review_atk_request, name='request_review'),
    path('add/', views.ATKItemCreateView.as_view(), name='item_add'),
    path('<int:pk>/', views.ATKItemDetailView.as_view(), name='item_detail'),
    path('<int:pk>/edit/', views.ATKItemUpdateView.as_view(), name='item_edit'),
    path('<int:pk>/delete/', views.ATKItemDeleteView.as_view(), name='item_delete'),
    
    # ATK Categories
    path('categories/', views.ATKCategoryListView.as_view(), name='category_list'),
    path('categories/add/', views.ATKCategoryCreateView.as_view(), name='category_add'),
]
