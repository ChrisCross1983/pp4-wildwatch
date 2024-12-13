from django.db import models
from django.contrib.auth.models import User

from django.db import models
from django.contrib.auth.models import User

class InjuryReport(models.Model):
    # Dropdown-Choices
    SPECIES_CHOICES = [
        ('Cat', 'Cat'),
        ('Dog', 'Dog'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Unknown', 'Unknown'),
    ]

    INJURY_CONDITION_CHOICES = [
        ('Slightly Injured', 'Slightly Injured'),
        ('Seriously Injured', 'Seriously Injured'),
        ('Not Injured', 'Not Injured'),
    ]

    description = models.TextField()
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    injury_condition = models.CharField(max_length=50, choices=INJURY_CONDITION_CHOICES)
    location = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to='injury_reports/', blank=True, null=True)

    date_reported = models.DateTimeField(auto_now_add=True)
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.species} - {self.injury_condition}"


class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return self.name

class ReportStatus(models.Model):
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.status

class Animal(models.Model):
    species = models.CharField(max_length=50)
    gender = models.CharField(max_length=50, choices=[("Male", "Male"), ("Female", "Female"), ("Unknown", "Unknown")])
    features = models.TextField(blank=True, null=True)
    injury_condition = models.CharField(max_length=50)

    def __str__(self):
        return self.species
