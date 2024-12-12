# reports/models.py
from django.db import models
from django.contrib.auth.models import User

class Species(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Gender(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class InjuryCondition(models.Model):
    condition_name = models.CharField(max_length=50)

    def __str__(self):
        return self.condition_name


class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class ReportStatus(models.Model):
    status_name = models.CharField(max_length=50)

    def __str__(self):
        return self.status_name


class Animal(models.Model):
    species = models.ForeignKey(Species, on_delete=models.CASCADE)
    gender = models.ForeignKey(Gender, on_delete=models.SET_NULL, null=True)
    features = models.TextField()
    injury_condition = models.ForeignKey(InjuryCondition, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.species.name} ({self.injury_condition.condition_name})"


class InjuryReport(models.Model):
    description = models.TextField()
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    report_status = models.ForeignKey(ReportStatus, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    date_reported = models.DateField(auto_now_add=True)
    comments = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='reports_images/', blank=True, null=True)

    def __str__(self):
        return f"Report by {self.reported_by.username} on {self.date_reported}"
