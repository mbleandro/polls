from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('pollsApp.urls')),
    path('admin/', admin.site.urls),
]