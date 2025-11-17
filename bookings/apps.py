from django.apps import AppConfig
import os

class BookingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bookings'
    
    def ready(self):
        # connect signal when app is ready
        from django.db.models.signals import post_migrate
        from . import signals  # ensure module import
        post_migrate.connect(signals.create_admin_user, sender=self)