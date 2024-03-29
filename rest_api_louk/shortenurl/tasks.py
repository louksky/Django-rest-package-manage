from celery import shared_task
from django.db import connection, IntegrityError
from .models import Package, PostOffice
import string
import random

def generate_tracking_number():
    """Generate a random tracking number."""
    characters = string.ascii_uppercase + string.digits
    tracking_number = ''.join(random.choice(characters) for _ in range(10))
    return tracking_number

@shared_task
def register_package_task(package_data):
    """
    Celery task to register a new package.
    """
    try:
        print('------------------------------------------------------')
        while True:
            tracking_number = generate_tracking_number()
            with connection.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO shortenurl_package (destination_address, destination_zip_code, recipient_name, tracking_number, package_type)
                    VALUES (%s, %s, %s, %s, %s)
                """, [
                    package_data['destination_address'],
                    package_data['destination_zip_code'],
                    package_data['recipient_name'],
                    tracking_number,
                    package_data['package_type']
                ])
            return "Package registered successfully"
    except Exception as e:
        return f"An error occurred: {str(e)}"

@shared_task
def record_arrival_task(package_id, office_id):
    """
    Celery task to record the arrival of a package at an intermediate post office.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE shortenurl_package
                SET intermediate_office_id = %s, status = %s
                WHERE id = %s
            """, [office_id, 'Arrived at Intermediate Post Office', package_id])
            row_count = cursor.rowcount
        if row_count == 1:
            return f"Arrival recorded for package {package_id}"
        else:
            return f"Failed to record arrival for package {package_id}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

@shared_task
def document_departure_task(package_id, office_id):
    """
    Celery task to document the departure of a package from an intermediate post office.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE shortenurl_package
                SET origin_office_id = %s, status = %s
                WHERE id = %s
            """, [office_id, 'Departed from Intermediate Post Office', package_id])
            row_count = cursor.rowcount
        if row_count == 1:
            return f"Departure documented for package {package_id}"
        else:
            return f"Failed to document departure for package {package_id}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

@shared_task
def confirm_arrival_task(package_id, office_id):
    """
    Celery task to confirm the arrival of a package at the destination post office.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE shortenurl_package
                SET destination_office_id = %s, status = %s
                WHERE id = %s
            """, [office_id, 'Arrived at Destination Post Office', package_id])
            row_count = cursor.rowcount
        if row_count == 1:
            return f"Arrival confirmed for package {package_id}"
        else:
            return f"Failed to confirm arrival for package {package_id}"
    except Exception as e:
        return f"An error occurred: {str(e)}"