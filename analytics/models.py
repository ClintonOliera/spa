from django.db import models

# Create your models here.
class Visit(models.Model):
    ip_address = models.CharField(max_length=50)
    path = models.CharField(max_length=255)
    referrer = models.CharField(max_length=512, null=True, blank=True)
    user_agent = models.CharField(max_length=1000, null=True, blank=True)
    browser = models.CharField(max_length=50, null=True, blank=True)
    os = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.ip_address} visited {self.path}"
