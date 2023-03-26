
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('adds/', include('parserAvitoCian.urls'), name='adds'),
    path('login/', include('users.urls')),
]