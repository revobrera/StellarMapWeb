from django.contrib import admin
from .models import StellarAccountInquiryHistory, StellarAccountLineage

# Register your models here.
@admin.register(StellarAccountInquiryHistory)
class RequestDemoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in
    StellarAccountInquiryHistory._meta.get_fields()]

@admin.register(StellarAccountLineage)
class RequestDemoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in
    StellarAccountLineage._meta.get_fields()]