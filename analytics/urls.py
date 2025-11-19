from django.urls import path
from . import views

urlpatterns = [
    path('api/analytics/summary/', views.analytics_summary, name='analytics_summary'),
    path('api/track/', views.track_visit, name='track-visit'),
]