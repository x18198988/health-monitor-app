from django.db import models
from django.contrib.auth.models import User

class HealthData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    steps = models.PositiveIntegerField()
    sleep_hours = models.FloatField()
    calories = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.date}"
