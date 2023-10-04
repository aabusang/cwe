from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.db.models import Q
from datetime import datetime
import math
import re
from django.urls import reverse
import numpy as np

from .models import *
from .forms import *

# import hydroshare


def index(request):    

    if request.method == 'POST':
        return redirect('datashow-river')
    else:
        names = INJECTION_LOCATION.objects.distinct('Name')
        context = {"data": names}
        return render(request, "datashow/index.html", context)


def about(request):
    return render(request, "datashow/about.html")
def login(request):
    return render(request, "datashow/login.html")

def river(request, river_name):
    return render(request, "datashow/river.html")

def upload(request):
    return render(request, "datashow/upload.html") 

def test(request):
    return render(request, "datashow/test.html")

def get_timeseries_form_data(request):
    if request.method == "POST":
        form = timeseriesForm(request.POST)
        if form.is_valid():
            river_name = form.cleaned_data["river_name"]
            tracer_type = form.cleaned_data["tracer_type"]
            geo_feature = form.cleaned_data["geo_feature"]
            feature_range = form.cleaned_data["feature_range"]
            flow_rate = form.cleaned_data["flow_rate"]
            
            return {
                'river_name': river_name,
                'tracer_type': tracer_type,
                'geo_feature': geo_feature,
                'feature_range': feature_range,
                'flow_rate': flow_rate,
            }
    else:
        form = timeseriesForm()
    return render(request, "datashow/explore.html", {"form": form})
# class FormData:

class TimeSeries:
    tracer_nums = []
    # takes a list of tracer numbers and returns a list of dicts of time and concentration data
    # TODO: fix timeseries filter to get more than one conc_timeseries object
    def filtered_data(self, tracer_nos):
        data = []
        # TODO: fix timeseries filter to get more than one conc_timeseries object
        timeseries = CONC_TIMESERIES.objects.filter(TracerNo__in=tracer_nos)
        for ts in timeseries:
            # print(ts.Sheet_name)
            if not (ts.Time and ts.Obs_conc):
                continue
            data.extend(self.clean_tc(ts.Time, ts.Obs_conc))
        return data
    # # Cleans the time and concentration data and return dict of time and concentration
    # # time and concentration are lists of strings each representing float values
    # # returns a list of dicts of time and concentration data
    def clean_tc(self, time, concentration):
        data = []

        pattern = r"^[,.?]+|[,.?]+$"

        for t, c in zip(time, concentration):
            t = re.sub(pattern, "", t)
            c = re.sub(pattern, "", c)
            try:
                t, c = float(t), float(c)
            except ValueError:
                continue
            if not (math.isnan(t) or math.isnan(c)):
                data.append({
                    'time': t,
                    'concentration': c,
                })
        return data

    # get date century from date string
    def get_century(self, date):
        year = int(date[-2:])  # Extract the last two digits as the year

        if year >= 0 and year <= 99:
            if year >= 0 and year <= 20:
                century = 2000 + year
            else:
                century = 1900 + year
        else:
            raise ValueError("Invalid year")

        return century
    #TODO: finish this function when I have a map and or lat and long data
    def by_injection(self, data):

        injection, river, latitude, longitude = data['injection_name'], data['river_name'], data['lat'], data['lng']
        results = []

        # injection_location = INJECTION_LOCATION.objects.filter(Name=river, Latitude=latitude, Longitude=longitude)
        river = data['river_name']
        injection_location = INJECTION_LOCATION.objects.filter(Name=river)
        for il in injection_location:
            timeseries = CONC_TIMESERIES.objects.filter(TracerNo=il.TracerNo)
            for ts in timeseries:
                if not (ts.Time and ts.Obs_conc):
                    continue
                results.extend(self.clean_tc(ts.Time, ts.Obs_conc))
        return results

    def by_river_name(self, river_name):
        injection_location = INJECTION_LOCATION.objects.filter(Name=river_name)
        if injection_location:
            tracer_nos = [il.TracerNo for il in injection_location]
        else:
            print("No data found for " + river_name)
            return None
        if tracer_nos:
            self.tracer_nums.extend([tn.TracerNo for tn in tracer_nos])
        return [tn.TracerNo for tn in tracer_nos]
   
    def by_stream_order(self, stream_order):
        
        return 
   
    def by_channel_width(self, channel_width):
        
        return
    # TODO: fix this function
    # PROBLEMS: values are in tuples, not just numbers which is what I expected
    # BEWARE: Bed_material is a string, not a number
    def by_geo_feature(self, feature='Bed Slope', range=(0, 0)):
        gf_map = {
            'Bed Mat Thickness': 'Bed_mat_thickness',
            'Bed Slope': 'Bed_slope',
            'Channel Width': 'Channel_width',
            'Chanel Depth': 'Channel_Depth',
            'Mannings n': 'Mannings_n',
        }
        field_name = gf_map[feature]
        #dictionary unpacking to filter out nan values, cuz exclude and filter don't take dynamic field names
        st_geo = ST_GEOMORPHOLOGY.objects.exclude(**{f'{field_name}__in': [np.nan]})
        geo_nos = st_geo.values_list('GeoNo', flat=True).filter(**{f'{field_name}__range': range})
        injection_location = INJECTION_LOCATION.objects.filter(GeoNo__in=geo_nos)
        tracer_nos_objs = [il.TracerNo for il in injection_location]
        tracer_nos = [tn.TracerNo for tn in tracer_nos_objs]
        self.tracer_nums.extend(tracer_nos)    
        return tracer_nos
        
    def by_date_range(self, from_date, to_date):
        data, filtered_sheets = [], []
        
        parsed_from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        parsed_to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
        from_date_str = datetime.strftime(parsed_from_date, "%m-%d-%y")
        to_date_str = datetime.strftime(parsed_to_date, "%m-%d-%y")
        
        sheet_names = CONC_TIMESERIES.objects.values_list('Sheet_name', flat=True)
        for sheet_name in sheet_names:
            match = re.search(r'\d{1,2}-\d{1,2}-\d{2,4}', sheet_name)
            if not match:
                continue
            try:
                sheet_date = datetime.strptime(match.group(), '%m-%d-%y').date()
            except ValueError:
                try:
                    sheet_date = datetime.strptime(match.group(), '%m-%d-%Y').date()
                except ValueError:
                    print("Invalid date format", match.group())
                    
            if sheet_date >= parsed_from_date and sheet_date <= parsed_to_date:
                # date_sheet_tuples.append((match.group(), sheet_name))
                filtered_sheets.append(sheet_name)

        timeseries = CONC_TIMESERIES.objects.all()
        tracer_nos = []
        for ts in timeseries:
            if ts.Sheet_name in filtered_sheets:
                tracer_nos.append(ts.TracerNo)
        self.tracer_nums.extend([tn for tn in tracer_nos])
        return [tn.TracerNo for tn in tracer_nos]
    
    def by_tracer_type(self, tracer_type):
        injection_tracer = INJECTION_TRACER.objects.filter(Type=tracer_type)
        tracer_nos = [it.TracerNo for it in injection_tracer]
        
        self.tracer_nums.extend([tn for tn in tracer_nos])
        return [tn for tn in tracer_nos]
    
    def by_flow_rate(self, flow_rate=41):
        hydro_nos = ST_HYDROLOGY.objects.values_list('Flow_rate', flat=True).filter(Flow_rate=flow_rate)
        injectin_location = INJECTION_LOCATION.objects.filter(HydroNo__in=hydro_nos)
        tracer_nos = [il.TracerNo for il in injectin_location]
        
        self.tracer_nums.extend([tn.TracerNo for tn in tracer_nos])
        return [tn.TracerNo for tn in tracer_nos]
    def get_whole_sheets(tracer_nos):
        pass
    def get_data(self, params = {
        'river': 'Shane', 
        'stream_order': 0,
        'channel_width': 0,
        'from_date': '1969-05-27', 
        'to_date': '1970-01-01', 
        'tracer_type': 'Rhodamine BA',
        'geo_feature': {'feature': 'Bed Slope', 'range': (0, 1)},
        'flow_rate': '41',
        }):
        # get all the functions tracer numbers here, remove duplicates, then call the filtered_data function
        # gf = params['geo_feature']
        self.by_river_name(params['river'])
        # self.by_stream_order(params['stream_order'])
        # self.by_channel_width(params['channel_width'])
        self.by_tracer_type(params['tracer_type'])
        self.by_flow_rate(params['flow_rate'])
        
        tracer_no_set = set(self.tracer_nums)
        # user tracer_no_set to get rivers, sheets data is coming from
        rivers = INJECTION_LOCATION.objects.values_list('Name', flat=True).filter(TracerNo__in=tracer_no_set).distinct()
        sheets = CONC_TIMESERIES.objects.values_list('Sheet_name', flat=True).filter(TracerNo__in=tracer_no_set).distinct()
        # print(rivers)
        # print(len(sheets))
            
        return {'timeseries': self.filtered_data(tracer_no_set), 'rivers': rivers, 'sheets': sheets}
    
        
def back_end_test():
    print("___________________________Testing backend___________________________")
    # timeseries = TimeSeries()
    # print(timeseries.get_data()['sheets'])
    # print(len(set(timeseries.tracer_nums)))
    print("___________________________Done testing___________________________")
back_end_test()










def explore(request): 
    # timeseries = TimeSeries()
    
    rivers = INJECTION_LOCATION.objects.values_list('Name', flat=True).distinct()
    sheets = CONC_TIMESERIES.objects.values_list('Sheet_name', flat=True).distinct()
    tracers = INJECTION_TRACER.objects.values_list('Type', flat=True).distinct()
    features = ['Bed Material', 'Bed Mat Thickness', 'Bed Slope', 'Channel Width',
                'Channel Depth', 'Cx Area', 'Mannings n']
    orders = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    if request.method == 'POST':
        # form = timeseriesForm(request.POST) #
        if form.is_valid():
            river_name = form.cleaned_data['river_name']
            stream_order = form.cleaned_data['stream_order']
            # channel_width = form.channel_width['channel_width']
            tracer_type = form.cleaned_data['tracer_type']
            flow_rate = form.cleaned_data['flow_rate']
        # ts = timeseries.get_data(
        #         {
        #             'river': river_name,
        #             'stream_order': stream_order,
        #             # 'channel_width': channel_width,
        #             'tracer_type': tracer_type,
        #             'flow_rate': flow_rate, #flow_rate.split(',')[0],
        #             })
        context = {
            'form': form,
            'current_river': river_name,
            'tracers': sorted(tracers),
            'features': sorted(features),
            # 'timeseries': ts['timeseries'],
            # 'ss_rivers':  sorted(ts['rivers']),
            # 'ss_sheets':  sorted(ts['sheets']),
        }
    else:
        form = timeseriesForm()
        # ts = timeseries.get_data(
        #         {
        #             'river': 'Shane',
        #             'stream_order': 0,
        #             'channel_width': 0,
        #             'tracer_type': 'Rhodamine BA',
        #             'flow_rate': 41,
        #         })
        context = {
            'form': form,
            'orders': orders,
            'rivers': sorted(rivers), 
            'sheets': sorted(sheets),
            'tracers': sorted(tracers),
            # 'features': sorted(features),
            #timeseries below is for testing when method is get
            # 'timeseries': ts['timeseries'],
            # 'ss_rivers':  sorted(ts['rivers']),
            # 'ss_sheets':  sorted(ts['sheets']),
        }
    return render(request, 'datashow/explore.html', context)



# # not found page to deal with the case when the data is not found
def not_found(request, error_message):
    return render(request, 'datashow/not_found.html', {'error_message': error_message})
