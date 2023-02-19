from django.contrib import admin
from .models import Advertisement, Source
from django.utils.html import format_html


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['print_url_shortly', 'title', 'price', 'print_phone_as_link', 'appartment_square', 'appartment_floor', 'floors_count', 'marketing_source', 'date']

    def print_url_shortly(self, object):
        return object.url[20:][:30]

    def print_phone_as_link(self, obj):
        return format_html(f'<a href="{obj.phone}">{obj.phone}</a>')


admin.site.register(Advertisement, AdvertisementAdmin)


admin.site.register(Source)
