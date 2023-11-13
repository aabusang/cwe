from django import forms
from .models import INJECTION_TRACER, INJECTION_LOCATION
from django.shortcuts import render, redirect
import re


class DownloadForm(forms.Form):
    timeseries_data = forms.CharField(label="Timeseries Data", required=False)
    dummy1 = forms.CharField(label="Dummy 1", required=False)
    dummy2 = forms.CharField(label="Dummy 2", required=False)
    dummy3 = forms.CharField(label="Dummy 3", required=False)

    def clean(self):
        cleaned_data = super().clean()

        if not any(cleaned_data.values()):
            raise ValidationError("Please select at least one item before submitting.")

        return cleaned_data

def explore_form(request):
    tracer_types = INJECTION_TRACER.objects.values_list('Type', flat=True).distinct()
    river_names = INJECTION_LOCATION.objects.values_list('Name', flat=True).distinct()

    form = ExploreForm()
    form.fields['river_name'].choices = [('', '')] + [(name, name) for name in river_names]
    form.fields['tracer_type'].choices = [('', '')] + [(tracer, tracer) for tracer in tracer_types]

    return render(request, 'datashow/forms/explore_form.html', {'form': form})

class ExploreForm(forms.Form):
    # River Name Dropdown
    RIVER_CHOICES = [
        ('', ''),  # Default empty choice
    ]
    river_name = forms.ChoiceField(
        choices=RIVER_CHOICES, 
        required=False, 
        label="River Name",
        help_text="This is the name given in the study literature."
        )

    # Channel Width Range
    channel_width = forms.CharField(
        required=False, 
        label="Channel Width (units))",
        widget=forms.TextInput(attrs={'placeholder': '10 or 10-23.9'}),
        help_text="Width of the channel measured at the survey site measured in feet."
    )

    # Flow Rate Range
    flow_rate = forms.CharField(
        required=False, 
        label="Flow Rate (ft)",
        widget=forms.TextInput(attrs={'placeholder': '10 or 10-23.9'}),
        help_text="Volumetric flow of water traveling through survey site measured in ft<sup>3</sup>/s",
    )

    # Tracer Type Dropdown
    TRACER_CHOICES = [
        ('', ''),  # Default empty choice
    ]
    tracer_type = forms.ChoiceField(
        choices=TRACER_CHOICES, 
        required=False, 
        label="Tracer Type",
        help_text="Type of chemical tracer used in the injection."
        )

    # Date Range
    from_date = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="The date is the recorded value at the time of injection."
        )
    to_date = forms.DateField(
        required=False, 
        widget=forms.DateInput(attrs={'type': 'date'}), 
        help_text="The date is the recorded value at the time of injection."
        )

    def clean(self):
        cleaned_data = super().clean()

        # Check if at least one field is filled out
        if not any(cleaned_data.values()):
            raise forms.ValidationError("At least one field must be filled out.")

        # Validate flow_rate and channel_width
        for field in ['flow_rate', 'channel_width']:
            value = cleaned_data.get(field)
            if value:
                # Check if the value matches the pattern for a single number or a range
                pattern = re.compile(r'^(\d+(\.\d+)?)(-(\d+(\.\d+)?))?$')
                match = pattern.match(value)
                if not match:
                    self.add_error(field, f"{field.replace('_', ' ').capitalize()} must be a number or a range of numbers (e.g., '10' or '10-23.9').")
                elif match.group(3):  # if range is provided
                    lower_value = float(match.group(1))
                    upper_value = float(match.group(4))
                    if lower_value >= upper_value:
                        self.add_error(field, f"In {field.replace('_', ' ').capitalize()}, the lower number must be less than the higher number.")
         # Convert date fields to string format
        for date_field in ['from_date', 'to_date']:
            date_value = cleaned_data.get(date_field)
            if date_value:
                cleaned_data[date_field] = date_value.isoformat()

        return cleaned_data
