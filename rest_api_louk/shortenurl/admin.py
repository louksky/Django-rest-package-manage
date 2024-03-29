from django.contrib import admin
from .models import PostOffice, Package

@admin.register(PostOffice)
class PostOfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'zip_code')
    search_fields = ['name', 'address', 'zip_code']
    list_filter = ('zip_code',)
    class Meta:
        verbose_name = "Post Office"
        verbose_name_plural = "Post Offices"

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('tracking_number', 'destination_address', 'destination_zip_code', 'recipient_name', 'package_type', 'origin_office', 'intermediate_office', 'destination_office', 'status')
    search_fields = ['tracking_number', 'destination_address', 'recipient_name']
    list_filter = ('package_type', 'status', 'origin_office', 'intermediate_office', 'destination_office')
    class Meta:
        verbose_name = "Package"
        verbose_name_plural = "Packages"