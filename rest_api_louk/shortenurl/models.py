from django.db import models
from django.conf import settings
from django.db.models import JSONField
# Create your models here.

class PostOffice(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=20)

class Package(models.Model):
    TYPE_CHOICES = (
        ('Letter', 'Letter'),
        ('Package', 'Package'),
    )
    destination_address = models.CharField(max_length=200)
    destination_zip_code = models.CharField(max_length=20)
    recipient_name = models.CharField(max_length=100)
    tracking_number = models.CharField(max_length=50, unique=True)
    package_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    origin_office = models.ForeignKey(PostOffice, related_name='origin_packages', on_delete=models.CASCADE, null=True)
    intermediate_office = models.ForeignKey(PostOffice, related_name='intermediate_packages', on_delete=models.SET_NULL, null=True)
    destination_office = models.ForeignKey(PostOffice, related_name='destination_packages', on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=100, default='Registered', null=True)
    history = JSONField(default=list, null=True)

    def update_status_with_history(self, new_status):
        """
        Update status and tracking history.
        """
        current_datetime = timezone.now()
        previous_status = self.status
        self.status = new_status
        self.history.append({
            'datetime': current_datetime.isoformat(),
            'previous_status': previous_status,
            'new_status': new_status
        })
        self.save()

    def get_tracking_history_as_str(self):
        """
        Return tracking history as a string.
        """
        history_str = ""
        for entry in self.history:
            history_str += f"Date/Time: {entry['datetime']}, Previous Status: {entry['previous_status']}, New Status: {entry['new_status']}\n"
        return history_str