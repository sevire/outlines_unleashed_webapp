from django import forms
from django.forms import Select

from ou_app.data_drivers.dropdown_driver import dropdown_select_list
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
        widgets = {
            'transformation': Select(choices=dropdown_select_list)
        }