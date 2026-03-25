# api/views.py
from rest_framework import viewsets, generics, permissions
from django.contrib.auth.models import User
from .models import Property, Booking
from .serializers import UserSerializer, PropertySerializer, BookingSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.filter(is_active=True)
    serializer_class = PropertySerializer
    # Anyone can view properties, only admins can edit
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Users only see their own bookings
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the logged-in user and calculate price
        property_obj = serializer.validated_data['property']
        days = (serializer.validated_data['check_out'] - serializer.validated_data['check_in']).days
        total = property_obj.price_per_night * max(days, 1)
        
        serializer.save(user=self.request.user, total_price=total)