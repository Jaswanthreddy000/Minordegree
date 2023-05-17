from django import forms
from .models import BTMMarksDistribution

class MarksDistributionForm(forms.ModelForm):
    class Meta:
        model = BTMMarksDistribution
        fields = ['Regulation', 'DistributionNames', 'Distribution', 'PromoteThreshold']
    threshold = forms.IntegerField()

class RollNumberForm(forms.Form):
    roll_number = forms.CharField(label='Enter your roll number', max_length=10)