from django.db import models

class InjuryReport(models.Model):
    description = models.TextField()  # Beschreibung
    species = models.CharField(max_length=100)  # Freitexteingabe für Spezies
    gender = models.CharField(max_length=100, default='Unknown')  # Freitexteingabe für Geschlecht, mit Default
    injury_condition = models.CharField(max_length=100)  # Freitexteingabe für Verletzung
    location = models.CharField(max_length=255, blank=True, null=True)  # Ort (optional)
    image = models.ImageField(upload_to='injury_reports/', blank=True, null=True)  # Bild (optional)

    def __str__(self):
        return f"{self.species} - {self.injury_condition}"
