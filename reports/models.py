from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class InjuryReport(models.Model):
    SPECIES_CHOICES = [
        ('Cat', 'Cat'),
        ('Dog', 'Dog'),
        ('Other', 'Other')
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Unknown', 'Unknown')
    ]

    INJURY_CONDITION_CHOICES = [
        ('Slightly Injured', 'Slightly Injured'),
        ('Seriously Injured', 'Seriously Injured'),
        ('Not Injured', 'Not Injured')
    ]
    
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    description = models.TextField(help_text="Provide a detailed description of the situation.")
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES, help_text="Select the species of the animal.")
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, help_text="Select the gender of the animal if known.")
    injury_condition = models.CharField(max_length=50, choices=INJURY_CONDITION_CHOICES, help_text="Describe the severity of the injury.")
    location = models.CharField(max_length=255, blank=True, null=True, help_text="Enter the nearest city or coordinates.")
    image = models.ImageField(upload_to='injury_reports/', blank=True, null=True, help_text="Upload a clear image if possible.")

    date_reported = models.DateTimeField(auto_now_add=True)
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    admin_comment = models.TextField(blank=True, null=True)
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='Pending',
    )

    def __str__(self):
        return f"{self.species} - {self.injury_condition}"

    def get_absolute_url(self):
        return reverse('reports:report_detail', args=[self.id])
    
    def approve(self):
        self.status = 'Approved'
        self.save()

    def reject(self, comment=None):
        self.status = 'Rejected'
        if comment:
            self.admin_comment = comment
        self.save()

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
