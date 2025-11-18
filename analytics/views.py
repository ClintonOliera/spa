from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.db.models import Count
from .models import Visit

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def analytics_summary(request):
    total_visits = Visit.objects.count()
    unique_visitors = Visit.objects.values("ip_address").distinct().count()

    top_pages = list(
        Visit.objects.values("path")
        .annotate(count=Count("path"))
        .order_by("-count")[:10]
    )

    top_browsers = list(
        Visit.objects.values("browser")
        .annotate(count=Count("browser"))
        .order_by("-count")[:5]
    )

    return Response({
        "total_visits": total_visits,
        "unique_visitors": unique_visitors,
        "top_pages": top_pages,
        "top_browsers": top_browsers,
    })
