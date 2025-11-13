from rest_framework import permissions, status
from .models import Booking, ContactMessage
from .serializers import BookingSerializer, ContactMessageSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Count
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)

    user = User.objects.create_user(username=username, password=password, email=email)
    refresh = RefreshToken.for_user(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'message': ' successfully registered'
    })
@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticated])
def booking_list(request):
    if request.method == 'GET':
        bookings = Booking.objects.filter(user=request.user).order_by('created_at')
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

# --- Contact Messages ---
@api_view(['GET', 'POST'])
def contact_messages(request):
    if request.method == 'POST':
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Message received!'}, status=201)
        return Response(serializer.errors, status=400)

    elif request.method == 'GET':
        messages = ContactMessage.objects.all().order_by('-created_at')
        serializer = ContactMessageSerializer(messages, many=True)
        return Response(serializer.data)
    


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = request.user
    return Response({
        "username": user.username,
        "email": user.email,
        "is_staff": user.is_staff,
        "is_superuser": user.is_superuser
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsAdminUser])
def booking_stats(request):
    approved = Booking.objects.filter(status='Confirmed').count()
    pending = Booking.objects.filter(status='Pending').count()
    cancelled = Booking.objects.filter(status='Cancelled').count()
    total_bookings = Booking.objects.count()
    services_summary = Booking.objects.values('service_type').annotate(total=Count('id'))

    return Response({
        'total_bookings': total_bookings,
        'approved': approved,
        'pending': pending,
        'cancelled': cancelled,
        'services_summary': list(services_summary)
    })

# ---- Admin Bookings ----
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_bookings(request):
    bookings = Booking.objects.all().order_by('-created_at')
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([permissions.IsAuthenticated, IsAdminUser])
def update_booking_status(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=404)

    status = request.data.get('status')
    if status in ['Pending', 'Confirmed', 'Cancelled']:
        booking.status = status
        booking.save()
        return Response({'success': True, 'status': booking.status})
    return Response({'error': 'Invalid status'}, status=400)

# ---- Contact Messages ----
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsAdminUser])
def admin_messages(request):
    messages = ContactMessage.objects.all().order_by('-created_at')
    serializer = ContactMessageSerializer(messages, many=True)
    return Response(serializer.data)


class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer