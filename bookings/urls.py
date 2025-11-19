from django.urls import path
from bookings import views
from bookings.views import CustomTokenView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # --- Auth ---
    path('api/register/', views.register_user, name='register'),
    path('api/token/', CustomTokenView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/login/', CustomTokenView.as_view(), name='login'),

    # --- Bookings ---
    path('api/bookings/', views.booking_list, name='bookings'),
    path('api/admin/bookings/', views.admin_bookings, name='admin_bookings'),
    path('api/admin/bookings/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),

    # --- Contact ---
    path('api/contact/', views.contact_messages, name='contact_messages'),
    path('api/admin/messages/', views.admin_messages, name='admin_messages'),

    # --- Stats & User ---
    path('api/booking-stats/', views.booking_stats, name='booking_stats'),
    path('api/user/', views.get_user, name='get_user'),
]