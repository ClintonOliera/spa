from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.db.models import Count
from .models import Visit
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import requests
from django.conf import settings
# Public track endpoint (called from frontend on page load)
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def track_visit(request):
    """
    Accepts JSON: { page, referrer (optional) }
    Will capture IP from headers and user-agent automatically.
    """
    try:
        data = request.data if isinstance(request.data, dict) else {}
        path = data.get('page', request.data.get('path') or request.META.get('PATH_INFO', '/'))
        referrer = data.get('referrer') or request.META.get('HTTP_REFERER', '')
        ua_string = data.get('userAgent') or request.META.get('HTTP_USER_AGENT', '')
        ip = (request.META.get('HTTP_X_FORWARDED_FOR') or request.META.get('REMOTE_ADDR') or '').split(',')[0].strip()

        # best-effort UA parse (if user-agents installed)
        browser = None
        os = None
        try:
            from user_agents import parse
            ua = parse(ua_string or "")
            browser = ua.browser.family
            os = ua.os.family
        except Exception:
            pass

        # Optional: geolocation by IP (disabled by default)
        country = None
        city = None
        if getattr(settings, "ANALYTICS_LOOKUP_IP", False) and ip:
            try:
                # small, free service; beware rate limits in production. Replace if needed.
                r = requests.get(f"https://ipapi.co/{ip}/json/", timeout=3)
                if r.ok:
                    j = r.json()
                    country = j.get('country_name')
                    city = j.get('city')
            except Exception:
                pass

        Visit.objects.create(
            ip_address=ip or '0.0.0.0',
            path=path[:255],
            referrer=referrer[:512] if referrer else '',
            user_agent=ua_string[:1000] if ua_string else '',
            browser=browser,
            os=os,
            country=country,
            city=city,
            created_at=timezone.now()
        )
        return Response({"status": "ok"})
    except Exception as e:
        return Response({"status": "error", "detail": str(e)}, status=500)


# Admin-only analytics summary for your admin.html JS
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def analytics_summary(request):
    total_visits = Visit.objects.count()
    unique_visitors = Visit.objects.values("ip_address").distinct().count()

    top_pages = list(
        Visit.objects.values("path")
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    top_countries = list(
        Visit.objects.values("country")
        .annotate(count=Count('id'))
        .order_by('-count')[:10]
    )

    recent = list(
        Visit.objects.order_by('-created_at')[:20]
        .values('ip_address', 'path', 'country', 'city', 'browser', 'os', 'created_at')
    )

    return Response({
        "total_visits": total_visits,
        "unique_visitors": unique_visitors,
        "top_pages": top_pages,
        "top_countries": top_countries,
        "recent": recent,
    })
