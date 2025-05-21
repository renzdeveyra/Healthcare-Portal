from django.db import models
from accounts.models import CustomUser

class MedicalCondition(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Treatment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    conditions = models.ManyToManyField(MedicalCondition, related_name='treatments')
    effectiveness_score = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class UserHealth(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='health_profile')
    age = models.PositiveIntegerField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True, help_text="Height in cm")
    weight = models.FloatField(null=True, blank=True, help_text="Weight in kg")
    conditions = models.ManyToManyField(MedicalCondition, blank=True, related_name='users')

    def __str__(self):
        return f"{self.user.username}'s Health Profile"

class Recommendation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recommendations')
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    condition = models.ForeignKey(MedicalCondition, on_delete=models.CASCADE)
    score = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-score', '-created_at']

    def __str__(self):
        return f"Recommendation for {self.user.username}: {self.treatment.name}"
