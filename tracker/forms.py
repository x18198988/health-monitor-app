from django import forms
from .models import HealthData

class HealthDataForm(forms.ModelForm):
    class Meta:
        model = HealthData
        fields = ['date', 'steps', 'sleep_hours', 'calories']
