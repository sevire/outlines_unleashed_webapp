from django import forms
from ou_app.models import TransformationInstance

UNLEASH_CHOICES = [
    ('risk_management', 'Risk Management'),
    ('ppt_skeleton', 'Basic Powerpoint Presentation')
]


class TransformationForm(forms.ModelForm):
    class Meta:
        model = TransformationInstance
        fields = [
            'file',
            'transformation'
        ]