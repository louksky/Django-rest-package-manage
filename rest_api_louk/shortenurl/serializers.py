from rest_framework import serializers
from .models import PostOffice, Package

class PostOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostOffice
        fields = ['id', 'name', 'address', 'zip_code']

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = ['id', 'destination_address', 'destination_zip_code', 'recipient_name', 'tracking_number', 'package_type', 'origin_office', 'intermediate_office', 'destination_office', 'status', 'history']
