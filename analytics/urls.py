from django.urls import path
from . import views

urlpatterns = [
    path('analytics-summary/', views.analytics_summary, name='analytics_summary'),
    path('track/', views.track_visit, name='track-visit'),
]