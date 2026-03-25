from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Hotel, Room, Booking

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', '')
        )
        return user

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class HotelSerializer(serializers.ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True)
    class Meta:
        model = Hotel
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    # This is the line your MyBookings.jsx page is looking for!
    room_details = RoomSerializer(source='room', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'room', 'room_details', 'check_in', 
            'check_out', 'total_price', 'status', 'created_at'
        ]
        read_only_fields = ('user', 'total_price')