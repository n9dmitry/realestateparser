
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('go/', include('parserAvitoCian.urls'), name='go'),
    path('login/', include('users.urls')),
]