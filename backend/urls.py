"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from bookings import views
from analytics.views import analytics_summary, track_visit
from bookings.views import CustomTokenView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('admin/', admin.site.urls),

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
    path('api/analytics/summary/', analytics_summary, name='analytics_summary'),
    path('api/track/', views.track_visit, name='track-visit'),
]

