from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^edapp/', include('edapp.urls')),
    url(r'^admin/', admin.site.urls),
]