from rest_framework import viewsets, generics, permissions
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Hotel, Room, Booking
from .serializers import UserSerializer, HotelSerializer, RoomSerializer, BookingSerializer
from .models import Hotel, Room, Booking, ServiceReservation
from .serializers import UserSerializer, HotelSerializer, RoomSerializer, BookingSerializer, ServiceReservationSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.filter(is_active=True)
    serializer_class = HotelSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.filter(is_active=True)
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users only see their own bookings, newest first
        return Booking.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        room_obj = serializer.validated_data['room']
        check_in = serializer.validated_data['check_in']
        check_out = serializer.validated_data['check_out']

        # 1. THE CONFLICT CHECK
        # We look for overlapping dates for this specific room
        # Logic: (Existing Check-in < New Check-out) AND (Existing Check-out > New Check-in)
        overlapping_bookings = Booking.objects.filter(
            room=room_obj,
            status__in=['PENDING', 'CONFIRMED']
        ).filter(
            Q(check_in__lt=check_out) & Q(check_out__gt=check_in)
        )

        if overlapping_bookings.exists():
            raise ValidationError({
                "detail": "This room is already booked for the selected dates. Please try different dates."
            })

        # 2. Calculate price (if no conflict found)
        delta = check_out - check_in
        days = max(delta.days, 1)
        
        total = room_obj.price_per_night * days
        
        serializer.save(user=self.request.user, total_price=total)

class ServiceReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ServiceReservation.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)