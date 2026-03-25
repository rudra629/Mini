from django.contrib import admin
from .models import Hotel, Room, Booking

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'star_rating', 'is_active')
    search_fields = ('name', 'location')
    list_filter = ('is_active', 'star_rating')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'title', 'price_per_night', 'capacity', 'is_active')
    search_fields = ('title', 'hotel__name')
    list_filter = ('is_active', 'capacity')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'room', 'check_in', 'check_out', 'status')
    list_filter = ('status', 'check_in')
    search_fields = ('user__username', 'room__title', 'room__hotel__name')
    list_editable = ('status',)