from django.contrib import admin
from django_otp.plugins.otp_totp.models import TOTPDevice
from .models import CustomUser

# Unregister the default TOTPDevice admin if already registered
try:
    admin.site.unregister(TOTPDevice)
except admin.sites.NotRegistered:
    pass

# Custom TOTP Device Admin (optional customization)
class CustomTOTPDeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'confirmed')
    list_filter = ('confirmed',)
    search_fields = ('user__username', 'name')

# Register your custom admin
admin.site.register(TOTPDevice, CustomTOTPDeviceAdmin)

# Custom User Admin
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'user_type', 'is_active')
    list_filter = ('user_type', 'is_active')
    search_fields = ('username', 'email')