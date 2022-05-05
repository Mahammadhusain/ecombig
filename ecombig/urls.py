from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('adminpanel/', admin.site.urls),
    path('seller/', include('sellerapp.urls')),
    path('admin/', include('adminapp.urls')),
    path('customer/',include('customerapp.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
