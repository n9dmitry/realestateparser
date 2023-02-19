from django.contrib import admin
from .models import Advertisement, Source

class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['url', 'title', 'price', 'phone', 'appartment_square', 'appartment_floor', 'floors_count', 'marketing_source', 'date']

admin.site.register(Advertisement, AdvertisementAdmin)


admin.site.register(Source)
