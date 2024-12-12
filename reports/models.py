from django.db import models
from django.contrib.auth.models import User 
class InjuryReport(models.Model):
    description = models.TextField()
    species = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    injury_condition = models.CharField(max_length=50)
    location = models.ForeignKey('Location', on_delete=models.SET_NULL, null=True, blank=True)  # ForeignKey
    report_status = models.ForeignKey('ReportStatus', on_delete=models.CASCADE, default=1)  # ForeignKey
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # ForeignKey
    animal = models.ForeignKey('Animal', on_delete=models.SET_NULL, null=True, blank=True)  # ForeignKey
    date_reported = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='injury_reports/', blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.species} - {self.injury_condition}"

class Location(models.Model):
    name = models.CharField(max_length=100)  # Beispiel: "Urban", "Rural"
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # Breite
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)  # Länge

    def __str__(self):
        return self.name

class ReportStatus(models.Model):
    status = models.CharField(max_length=50)  # Beispiel: "Open", "In Progress", "Completed"

    def __str__(self):
        return self.status

class Animal(models.Model):
    species = models.CharField(max_length=50)  # Beispiel: "Cat", "Dog"
    gender = models.CharField(max_length=50, choices=[("Male", "Male"), ("Female", "Female"), ("Unknown", "Unknown")])
    features = models.TextField(blank=True, null=True)  # Besonderheiten des Tieres
    injury_condition = models.CharField(max_length=50)  # Beispiel: "Slightly Injured"

    def __str__(self):
        return self.species
