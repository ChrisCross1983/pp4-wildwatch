from django.contrib import admin
from .models import InjuryReport, Location, ReportStatus, Animal

admin.site.register(Location)
admin.site.register(ReportStatus)
admin.site.register(Animal)

@admin.register(InjuryReport)
class InjuryReportAdmin(admin.ModelAdmin):
    list_display = ('species', 'location', 'injury_condition', 'status', 'date_reported', 'reported_by')
    list_filter = ('status', 'species', 'injury_condition')
    search_fields = ('species', 'description', 'location')
    actions = ['approve_reports', 'reject_reports']

    def approve_reports(self, request, queryset):
        queryset.update(status='Approved')
        self.message_user(request, f"{queryset.count()} reports approved.")

    def reject_reports(self, request, queryset):
        queryset.update(status='Rejected')
        self.message_user(request, f"{queryset.count()} reports rejected.")