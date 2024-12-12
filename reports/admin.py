from django.contrib import admin
from .models import InjuryReport, Location, ReportStatus, Animal


admin.site.register(InjuryReport)
admin.site.register(Location)
admin.site.register(ReportStatus)
admin.site.register(Animal)
