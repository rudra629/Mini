from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, HotelViewSet, RoomViewSet, BookingViewSet

router = DefaultRouter()
# Registering the new endpoints
router.register(r'hotels', HotelViewSet, basename='hotel')
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    # Auth endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # App endpoints (includes /api/hotels/ and /api/rooms/)
    path('', include(router.urls)),
]