from django.test import TestCase
from unittest.mock import patch
from .models import Package, PostOffice
from .tasks import register_package_task, record_arrival_task, document_departure_task, confirm_arrival_task

class CeleryTasksTestCase(TestCase):
    def setUp(self):
        self.post_office = PostOffice.objects.create(name="Test Office", address="Test Address", zip_code="12345")

    @patch('your_app.tasks.Package.objects.create')
    def test_register_package_task(self, mock_create):
        package_data = {
            "destination_address": "Test Destination",
            "destination_zip_code": "54321",
            "recipient_name": "Test Recipient",
            "tracking_number": "TEST123",
            "type": "Package"
        }
        register_package_task(package_data)
        mock_create.assert_called_once_with(**package_data)

    def test_record_arrival_task(self):
        package = Package.objects.create(
            destination_address="Test Destination",
            destination_zip_code="54321",
            recipient_name="Test Recipient",
            tracking_number="TEST123",
            type="Package"
        )
        record_arrival_task(package.id, self.post_office.id)
        updated_package = Package.objects.get(pk=package.id)
        self.assertEqual(updated_package.status, "Arrived at Intermediate Post Office")
        self.assertEqual(updated_package.intermediate_office, self.post_office)

    def test_document_departure_task(self):
        package = Package.objects.create(
            destination_address="Test Destination",
            destination_zip_code="54321",
            recipient_name="Test Recipient",
            tracking_number="TEST123",
            type="Package"
        )
        package.intermediate_office = self.post_office
        package.save()
        document_departure_task(package.id, self.post_office.id)
        updated_package = Package.objects.get(pk=package.id)
        self.assertEqual(updated_package.status, "Departed from Intermediate Post Office")
        self.assertEqual(updated_package.origin_office, self.post_office)

    def test_confirm_arrival_task(self):
        package = Package.objects.create(
            destination_address="Test Destination",
            destination_zip_code="54321",
            recipient_name="Test Recipient",
            tracking_number="TEST123",
            type="Package"
        )
        package.intermediate_office = self.post_office
        package.save()
        confirm_arrival_task(package.id, self.post_office.id)
        updated_package = Package.objects.get(pk=package.id)
        self.assertEqual(updated_package.status, "Arrived at Destination Post Office")
        self.assertEqual(updated_package.destination_office, self.post_office)