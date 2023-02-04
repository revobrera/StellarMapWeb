from django.contrib import admin

from .models import (ManagementCronHealth, StellarCreatorAccountLineage,
                     UserInquirySearchHistory)


# Register your models here.
@admin.register(UserInquirySearchHistory)
class RequestDemoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in
    UserInquirySearchHistory._meta.get_fields()]

@admin.register(StellarCreatorAccountLineage)
class RequestDemoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in
    StellarCreatorAccountLineage._meta.get_fields()]

@admin.register(ManagementCronHealth)
class RequestDemoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in
    ManagementCronHealth._meta.get_fields()]