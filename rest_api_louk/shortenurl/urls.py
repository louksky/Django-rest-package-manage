from django.urls import include, path
from django.contrib import admin
from authapp import urls as authapp_urls
from . import views
app_name = 'shortenurl'

urlpatterns = [
    path('register_package/', views.register_package, name='register_package'),
    path('record_arrival/<int:package_id>/<int:office_id>/', views.record_arrival, name='record_arrival'),
    path('document_departure/<int:package_id>/<int:office_id>/', views.document_departure, name='document_departure'),
    path('confirm_arrival/<int:package_id>/<int:office_id>/', views.confirm_arrival, name='confirm_arrival'),
]