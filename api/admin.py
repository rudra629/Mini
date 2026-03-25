# api/admin.py
from django.contrib import admin
from .models import Property, Booking

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'price_per_night', 'is_active')
    search_fields = ('title', 'location')
    list_filter = ('is_active',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'property', 'check_in', 'check_out', 'status')
    list_filter = ('status', 'check_in')
    search_fields = ('user__username', 'property__title')
    list_editable = ('status',)