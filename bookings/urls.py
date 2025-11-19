from django.urls import path
from bookings import views
from bookings.views import CustomTokenView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # --- Auth ---
    path('register/', views.register_user, name='register'),
    path('token/', CustomTokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', CustomTokenView.as_view(), name='login'),

    # --- Bookings ---
    path('bookings/', views.booking_list, name='bookings'),
    path('admin/bookings/', views.admin_bookings, name='admin_bookings'),
    path('admin/bookings/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),

    # --- Contact ---
    path('contact/', views.contact_messages, name='contact_messages'),
    path('admin/messages/', views.admin_messages, name='admin_messages'),

    # --- Stats & User ---
    path('booking-stats/', views.booking_stats, name='booking_stats'),
    path('user/', views.get_user, name='get_user'),
]