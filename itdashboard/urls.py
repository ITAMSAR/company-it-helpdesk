from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from apps.users.views import DashboardView
from apps.users.logout_view import logout_view
from apps.inventory.qr_views import item_detail_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DashboardView.as_view(), name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', logout_view, name='logout'),
    path('users/', include('apps.users.urls')),
    path('inventory/', include('apps.inventory.urls')),
    path('tickets/', include('apps.tickets.urls')),
    path('reminder/', include('apps.reminder.urls')),
    
    # QR Code public route - accessible from mobile (handle slashes in inventory code)
    path('item/<path:code>/', item_detail_view, name='item_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
