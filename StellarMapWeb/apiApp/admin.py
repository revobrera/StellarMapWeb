from django.contrib import admin

from .models import (ManagementCronHealth, ManagementCronHealthHistory,
                     StellarAccountInquiryHistory, StellarAccountLineage,
                     StellarCreatorAccountLineage, UserInquirySearchHistory)


# Register your models here.
@admin.register(StellarAccountInquiryHistory)
class RequestDemoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in
    StellarAccountInquiryHistory._meta.get_fields()]

@admin.register(StellarAccountLineage)
class RequestDemoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in
    StellarAccountLineage._meta.get_fields()]

@admin.register(ManagementCronHealthHistory)
class RequestDemoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in
    ManagementCronHealthHistory._meta.get_fields()]

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