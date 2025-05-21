from django import forms
from .models import UserHealth, MedicalCondition

class UserHealthForm(forms.ModelForm):
    """Form for updating user health profile"""
    
    conditions = forms.ModelMultipleChoiceField(
        queryset=MedicalCondition.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    class Meta:
        model = UserHealth
        fields = ['age', 'height', 'weight', 'conditions']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'height': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        labels = {
            'height': 'Height (cm)',
            'weight': 'Weight (kg)',
        }
        help_texts = {
            'age': 'Your age in years',
            'height': 'Your height in centimeters',
            'weight': 'Your weight in kilograms',
            'conditions': 'Select any medical conditions you have',
        }
