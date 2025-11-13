from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'service_type', 'booking_date', 'status']
    list_filter = ['service_type', 'status']
    search_fields = ['user__username', 'service_type']
