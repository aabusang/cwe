from django.db import models


class ST_HYDROLOGY(models.Model):
    HydroNo = models.AutoField(primary_key=True)
    Flow_rate = models.FloatField()
    Flow_velocity = models.FloatField()
    Shear_velocity = models.FloatField(null=True)
    
    class Meta:
        db_table = 'ST_HYDROLOGY'


class ST_CHARACTERISTICS(models.Model):
    CharNo = models.AutoField(primary_key=True)
    Ph = models.FloatField()
    DissSol = models.FloatField()
    Vegetation = models.CharField(max_length=255)
    Temperature = models.FloatField()
    class Meta:
        db_table = 'ST_CHARACTERISTICS'

class ST_GEOMORPHOLOGY(models.Model):
    GeoNo = models.AutoField(primary_key=True)
    Bed_slope = models.FloatField()
    Channel_width = models.FloatField()
    Channel_Depth = models.FloatField()
    Cx_area = models.FloatField()
    Bed_material = models.CharField(max_length=255)
    Bed_mat_thickness = models.FloatField()
    Mannings_n = models.FloatField()
    class Meta:
        db_table = 'ST_GEOMORPHOLOGY'


class WS_CHARACTERISTICS(models.Model):
    WsNo = models.AutoField(primary_key=True)
    Drainage_area = models.FloatField(null=True)
    class Meta:
        db_table = 'WS_CHARACTERISTICS'

class INJECTION_TRACER(models.Model):
    TracerNo = models.AutoField(primary_key=True)
    Mass = models.FloatField(null=True)
    Concentration = models.FloatField(null=True)
    BG_conc = models.FloatField(null=True)
    Inj_duration = models.FloatField(null=True)
    Type = models.CharField(max_length=80)
    Start_time = models.FloatField(null=True)
    End_time = models.FloatField(null=True)
    Date = models.DateField(null=True)
    Note = models.CharField(max_length=255, null=True)
    Monitor_method = models.CharField(max_length=255)
    class Meta:
        db_table = 'INJECTION_TRACER'

class INJECTION_LOCATION(models.Model):
    ILNo = models.AutoField(primary_key=True)
    Inj_latitude = models.FloatField(null=True)
    Inj_longitude = models.FloatField(null=True)
    Name = models.CharField(max_length=255)
    Inj_order = models.IntegerField(null=True)
    HydroNo = models.ForeignKey(ST_HYDROLOGY, on_delete=models.CASCADE)
    CharNo = models.ForeignKey(ST_CHARACTERISTICS, on_delete=models.CASCADE)
    GeoNo = models.ForeignKey(ST_GEOMORPHOLOGY, on_delete=models.CASCADE)
    TracerNo = models.ForeignKey(INJECTION_TRACER, on_delete=models.CASCADE)
    WSNo = models.ForeignKey(WS_CHARACTERISTICS, on_delete=models.CASCADE)
    class Meta:
        db_table = 'INJECTION_LOCATION'


class CONC_TIMESERIES(models.Model):
    TSNo = models.AutoField(primary_key=True)
    Sheet_name = models.CharField(max_length=100)  
    Date = models.CharField(max_length=15, blank=True, null=True)
    Time = models.TextField(blank=True, null=True)
    Obs_conc = models.TextField(blank=True, null=True)
    Conserv_conc = models.TextField(blank=True, null=True)
    Disch_adj_conc = models.TextField(blank=True, null=True)
    TracerNo = models.ForeignKey(INJECTION_TRACER, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'CONC_TIMESERIES'

class SAMPLING_LOCATION(models.Model):
    SLNo = models.AutoField(primary_key=True)
    S_latitude = models.FloatField(null=True)
    S_longitude = models.FloatField(null=True)
    S_order = models.IntegerField(null=True)    
    HydroNo = models.ForeignKey(ST_HYDROLOGY, on_delete=models.CASCADE)
    CharNo = models.ForeignKey(ST_CHARACTERISTICS, on_delete=models.CASCADE)
    GeoNo = models.ForeignKey(ST_GEOMORPHOLOGY, on_delete=models.CASCADE)
    Sheet_name = models.CharField(max_length=80)
    class Meta:
        db_table = 'SAMPLING_LOCATION'

class DOWNSTREAM(models.Model):
    DNo = models.AutoField(primary_key=True)
    Distance_down = models.FloatField(null=True)
    SLNo = models.ForeignKey(SAMPLING_LOCATION, on_delete=models.CASCADE)
    ILNo = models.ForeignKey(INJECTION_LOCATION, on_delete=models.CASCADE)
    class Meta:
        db_table = 'DOWNSTREAM'

class SAMPLE(models.Model):
    SNo = models.AutoField(primary_key=True)
    Sheet_name = models.CharField(max_length=80)
    TracerNo = models.ForeignKey(INJECTION_TRACER, on_delete=models.CASCADE)
    SLNo = models.ForeignKey(SAMPLING_LOCATION, on_delete=models.CASCADE)
    class Meta:
        db_table = 'SAMPLE'
    
    
    
