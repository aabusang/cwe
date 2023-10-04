from django import forms


class timeseriesForm(forms.Form):

    river_name = forms.CharField(label="Injection (River Name)", required=False)
    stream_order = forms.FloatField(label="Stream Order", required=False)
    channel_width = forms.CharField(label="Channel Width", required=False)
    tracer_type = forms.CharField(label="Tracer Type", required=False)
    flow_rate = forms.FloatField(label="Discharge(cfs)", required=False)
    
    # geo_feature = forms.ChoiceField(label="Geo Feature", required=False)
    # feature_range = forms.CharField(label="Feature Range", max_length=255, required=False)
    # from_date = forms.DateField(label="From Date", required=False, 
    #                             widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    # to_data = forms.DateField(label="To Date", required=False, 
    #                           widget=forms.DateInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    
