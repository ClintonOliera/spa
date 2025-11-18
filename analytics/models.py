from django.db import models

# Create your models here.
class Visit(models.Model):
    ip_address = models.GenericIPAddressField()
    path = models.CharField(max_length=255)
    browser = models.CharField(max_length=100)
    os = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
