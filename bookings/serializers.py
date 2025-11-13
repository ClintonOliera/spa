from datetime import datetime
from rest_framework import serializers
from .models import Booking, ContactMessage
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class BookingSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = Booking
        fields = ['id', 'user', 'username', 'service_type', 'booking_date', 'message', 'status']
        read_only_fields = ['user']  # prevents needing to pass user in POST

    def get_username(self, obj):
        return obj.user.username if obj.user else 'N/A'

    def validate_booking_date(self, value):
        # Ensure datetime is timezone-aware
        if isinstance(value, datetime) and timezone.is_naive(value):
            value = timezone.make_aware(value)
        return value
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = '__all__'

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # ✅ Add custom claims to the JWT
        token['username'] = user.username
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser

        return token