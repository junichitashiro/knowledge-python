from django.contrib import admin
from django.urls import path, include

from sampleapp.views import top

urlpatterns = [
    path('', top, name='top'),
    path('sampleapp/', include('sampleapp.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]
