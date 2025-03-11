from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
from cloudinary.models import CloudinaryField

class InjuryReport(models.Model):

    PUBLICATION_STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]
    
    STATUS_CHOICES = [
        ("Open", "Open"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    publication_status = models.CharField(
        max_length=10,
        choices=PUBLICATION_STATUS_CHOICES,
        default="Pending",
    )

    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default="Open",
    )
    
    title = models.CharField(
        max_length=255,
        help_text="Provide a specific title for the report (e.g., 'Cat injured on left paw').",
        blank=False
    )

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
    
    description = models.TextField(help_text="Provide a detailed description of the situation.")
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES, help_text="Select the species of the animal.")
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, help_text="Select the gender of the animal if known.")
    injury_condition = models.CharField(max_length=50, choices=INJURY_CONDITION_CHOICES, help_text="Describe the severity of the injury.")
    location = models.CharField(max_length=255, blank=True, null=True, help_text="Enter the nearest city or coordinates.")
    image = CloudinaryField('image', blank=True, null=True, default='placeholder_report_qe8gab.jpg', help_text="Upload a clear image if possible.")
    date_reported = models.DateTimeField(auto_now_add=True)
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    helper = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name='helper', help_text="User who is taking care of this report.",)
    helpers = models.ManyToManyField(User, related_name='helped_reports', blank=True)
    admin_comment = models.TextField(blank=True, null=True)
    edit_history = models.TextField(blank=True, null=True, help_text="Track changes made to the report.")

    def __str__(self):
        return f"{self.species} - {self.injury_condition}"

    def get_absolute_url(self):
        return reverse('reports:report_detail', args=[self.id])
    
    def approve(self):
        self.publication_status = 'Approved'
        self.save()

    def reject(self, comment=None, admin_user=None):
        self.publication_status = 'Rejected'
        if comment:
            self.admin_comment = comment
            if admin_user:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                history_entry = f"{timestamp} - {admin_user.username}: Report rejected with comment: '{comment}'\n"
                self.edit_history = (self.edit_history or "") + history_entry
            self.save()
        
    def add_to_history(self, user, change_description, updated_fields=None):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        history_entry = f"{timestamp} - {user.username}: {change_description}"
        
        if updated_fields:
            changes = "\n".join([f"  Field '{field}' changed from '{old}' to '{new}'"
                                 for field, (old, new) in updated_fields.items()])
            history_entry += f"\n{changes}"

        if self.edit_history and history_entry.strip() in self.edit_history:
            return
        
        self.edit_history = (self.edit_history or "") + history_entry + "\n"
        self.save()

    def set_status(self, new_status, user=None):
        self.status = new_status
        if user and new_status == 'In Progress':
            self.helper = user
        self.save()

    def save(self, *args, **kwargs):
        if self.helper and self.helper not in self.helpers.all():
            self.helpers.add(self.helper)
        super().save(*args, **kwargs)

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
