from django.db.models import Q
from datetime import datetime
import math, re, os, csv, zipfile
import numpy as np
from datashow.models import *
from django.http import StreamingHttpResponse
from io import StringIO
from itertools import zip_longest






class TimeseriesData:
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

    def by_river_name(self, river_name, get_names=False, get_timeseries=False):
        print(f"Getting data for {river_name}")
        injection_location = INJECTION_LOCATION.objects.filter(Name=river_name)
        if injection_location:
            tracer_nos = [il.TracerNo for il in injection_location]
        else:
            # print("No data found for " + river_name)
            return None
        if tracer_nos:
            self.tracer_nums.extend([tn.TracerNo for tn in tracer_nos])
        return [tn.TracerNo for tn in tracer_nos]
   

    def by_channel_width(self, channel_width):
        st_geo = ST_GEOMORPHOLOGY.objects.filter(Channel_width=channel_width)
        if st_geo:
            geo_nos = [sg.GeoNo for sg in st_geo]
            injection_location = INJECTION_LOCATION.objects.filter(GeoNo__in=geo_nos)
            tracer_nos = [il.TracerNo for il in injection_location]
        else:
            print("No data found for channel width")
            return None
        if tracer_nos:
            self.tracer_nums.extend([tn.TracerNo for tn in tracer_nos])
        return [tn.TracerNo for tn in tracer_nos]       



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

    def get_data(self, **kwargs):
        # Default parameters set to None
        params = {
            'river_name': None, 
            'stream_order': None,
            'channel_width': None,
            'from_date': None, 
            'to_date': None, 
            'tracer_type': None,
            'flow_rate': None,
        }

        # Update default parameters with provided arguments
        params.update(kwargs)

        # get all the functions tracer numbers here, remove duplicates, then call the filtered_data function
        self.by_river_name(params['river_name'], False, False)
        self.by_tracer_type(params['tracer_type'])
        # self.by_channel_width(params['channel_width'])
        # self.by_flow_rate(params['flow_rate'])
        # self.by_date_range(params['from_date'], params['to_date'])

        tracer_no_set = set(self.tracer_nums)
            
        return {'timeseries': self.filtered_data(tracer_no_set)}
    



class ExploreData:

    def __init__(self):
        self.timseries_data = TimeseriesData()

    def get_data(self, **kwargs):
        # Default parameters set to None
        params = {
            'river_name': None, 
            'stream_order': None,
            'channel_width': None,
            'from_date': None, 
            'to_date': None, 
            'tracer_type': None,
            'flow_rate': None,
        }
        
        # Update default parameters with provided arguments
        params.update(kwargs)

        data = self.timseries_data.get_data(**params)

    # def stream_csv_data(response):
    #     # Sample data
    #     data  = TimeseriesData().get_data(river_name="Shane")

    #     timeseries_data = data['timeseries']

    #     # Create a generator for the CSV rows
    #     def generate():
    #         yield 'Time,Concentration\n'  # Header
    #         for entry in timeseries_data:
    #             yield f"{entry['time']},{entry['concentration']}\n"

    #     return StreamingHttpResponse(generate(), content_type="text/csv")

    # def download_csv(request):
    #     response = StreamingHttpResponse(stream_csv_data(request), content_type='text/csv')
    #     response['Content-Disposition'] = 'attachment; filename="timeseries_data.csv"'
    #     return response

    # def get_csv(self, river_name):

    #     if river_name:
    #         print("Yes there is a river")
    #         injection_locations = INJECTION_LOCATION.objects.filter(Name=river_name)
    
            # for inj_loc in injection_locations:
                # Fetch related data using the foreign key relationships
                # hydro_data = ST_HYDROLOGY.objects.get(pk=inj_loc.HydroNo_id)
                # This will return a list of Flow_rate values for all ST_HYDROLOGY objects
                # flow_rates = ST_HYDROLOGY.objects.all().values_list('Flow_rate', flat=True)

                # print(hydro_data)
                # for hydro in hydro_data:
                #     print(hydro)
                # char_data = ST_CHARACTERISTICS.objects.get(pk=inj_loc.CharNo_id)
                # geo_data = ST_GEOMORPHOLOGY.objects.get(pk=inj_loc.GeoNo_id)
                # tracer_data = INJECTION_TRACER.objects.get(pk=inj_loc.TracerNo_id)
                # ws_data = WS_CHARACTERISTICS.objects.get(pk=inj_loc.WSNo_id)
                
                # If there are other models that have a foreign key relationship with INJECTION_LOCATION, 
                # you can fetch their data similarly.
                # downstream_data = DOWNSTREAM.objects.filter(ILNo=inj_loc)



class Sheets:

    @staticmethod
    def generate_csv(river_name=None, tracer_type=None, from_date=None, to_date=None, flow_rate=None, channel_width=None):
        # Ensure at least one parameter is provided
        if not any([river_name, tracer_type, from_date, to_date, flow_rate, channel_width]):
            print("Sheets Class: user didn't provide any parameters")
            raise ValueError("At least one search parameter must be provided.")
        
        # Fetch relevant timeseries data based on the search criteria
        time_series_data = Sheets.get_timeseries_data(river_name, tracer_type, from_date, to_date, flow_rate, channel_width)

        # Transpose time_series_data to align it horizontally
        transposed_data = list(zip_longest(*[Sheets.extract_time_series(entry) for entry in time_series_data], fillvalue=['']*4))
        # Function to clean and split the data
        def clean_and_split(data_str):
            cleaned_data = data_str.strip("[]")  # Remove the brackets
            return cleaned_data.split(',')  # Split the string into a list
        # Function to safely get an element from a list or return an empty string if index is out of range
        def safe_get(lst, idx):
            return lst[idx] if idx < len(lst) else ''

        # Check if any time series data exists, if not, return an empty string
        if not time_series_data:
            return ""

        def clean_and_split(data_str):
            # Remove brackets and quotes, then split by comma
            return data_str.strip("[]'").split(',')

        # Function to extend lists to a common length
        def extend_lists_to_common_length(lists):
            max_length = max(len(lst) for lst in lists)
            for lst in lists:
                lst.extend([''] * (max_length - len(lst)))

        # Function to clean, split the data, and pad it to a uniform length
        def clean_split_and_pad(data_str, max_length):
            cleaned_data = data_str.strip("[]'").split(',')
            return cleaned_data + [''] * (max_length - len(cleaned_data))
        
        # Write data to CSV
        output = StringIO()
        writer = csv.writer(output)

        writer.writerow(['Parameter', 'Units', 'Values', 'Additional Ref'])
        writer.writerow(['River Surveyed', '', river_name if river_name else '', ''])
        writer.writerow(['Channel Width', 'ft', channel_width if channel_width else '', ''])

        if river_name:
            injection_location = INJECTION_LOCATION.objects.filter(Name=river_name).first()
            if injection_location:
                hydro_data = ST_HYDROLOGY.objects.get(pk=injection_location.HydroNo_id)
                char_data = ST_CHARACTERISTICS.objects.get(pk=injection_location.CharNo_id)
                geo_data = ST_GEOMORPHOLOGY.objects.get(pk=injection_location.GeoNo_id)
                
                writer.writerow(['Flow Rate', 'm3/s', hydro_data.Flow_rate if hydro_data else '', ''])
                writer.writerow(['Channel Depth', 'm', geo_data.Channel_Depth if geo_data else '', ''])
                writer.writerow(['Bed Slope', '', geo_data.Bed_slope if geo_data else '', ''])
                writer.writerow(['Vegetation', '', char_data.Vegetation if char_data else '', ''])
                writer.writerow(['Temperature', '°C', char_data.Temperature if char_data else '', ''])
                writer.writerow(['pH', '', char_data.Ph if char_data else '', ''])
                writer.writerow(['Dissolved Solids', 'mg/L', char_data.DissSol if char_data else '', ''])
                writer.writerow(['Tracer Type', '', tracer_type if tracer_type else '', ''])




        # Determine the maximum length of any time series
        max_series_length = max(len(entry.Time.strip("[]'").split(',')) for entry in time_series_data)

        # Organize the data for each entry
        all_series_data = []
        for entry in time_series_data:
            time_list = clean_split_and_pad(entry.Time, max_series_length)
            obs_conc_list = clean_split_and_pad(entry.Obs_conc, max_series_length)
            conserv_conc_list = clean_split_and_pad(entry.Conserv_conc, max_series_length)
            disch_adj_conc_list = clean_split_and_pad(entry.Disch_adj_conc, max_series_length)

            # Combine the data for this series and add to the overall list
            combined_data = list(zip(time_list, obs_conc_list, conserv_conc_list, disch_adj_conc_list))
            all_series_data.append(combined_data)

        # Write headers for each time series
        headers = ['Time since injection', 'Observed concentration', 'Conservative concentration', 'Discharge adjusted concentration']
        full_header_row = []
        for _ in range(len(time_series_data)):
            full_header_row.extend(headers + [' '])
        writer.writerow(full_header_row)

        # Write the data to CSV, handling each row across all series
        for i in range(max_series_length):
            row = []
            for series_data in all_series_data:
                row.extend(series_data[i] if i < len(series_data) else [''] * len(headers))
                row.append('')  # Gap column
            writer.writerow(row)
            
            
            
        output.seek(0)
        return output.getvalue()


    @staticmethod
    def extract_time_series(entry):
        # Extract the relevant fields from each entry and return as a list
        return [entry.Time, entry.Obs_conc, entry.Conserv_conc, entry.Disch_adj_conc]
    
    @staticmethod
    def get_timeseries_data(river_name=None, tracer_type=None, from_date=None, to_date=None, flow_rate=None, channel_width=None):
        """
        Retrieve the CONC_TIMESERIES data based on the provided search criteria.
        """
        # Initial query for CONC_TIMESERIES
        query = CONC_TIMESERIES.objects.all()
        
        # If river_name is provided, filter based on related INJECTION_LOCATION
        if river_name:
            injection_location_ids = INJECTION_LOCATION.objects.filter(Name=river_name).values_list('TracerNo', flat=True)
            query = query.filter(TracerNo__in=injection_location_ids)
        
        # If tracer_type is provided, filter based on related INJECTION_TRACER
        if tracer_type:
            tracer_ids = INJECTION_TRACER.objects.filter(Type=tracer_type).values_list('TracerNo', flat=True)
            query = query.filter(TracerNo__in=tracer_ids)
        
        # If flow_rate is provided, filter based on related ST_HYDROLOGY
        if flow_rate:
            hydro_ids = handle_range_filtering(ST_HYDROLOGY.objects.all(), 'Flow_rate', flow_rate).values_list('HydroNo', flat=True)
            injection_location_ids = INJECTION_LOCATION.objects.filter(HydroNo__in=hydro_ids).values_list('TracerNo', flat=True)
            query = query.filter(TracerNo__in=injection_location_ids)
        
        # If channel_width is provided, filter based on related ST_GEOMORPHOLOGY
        if channel_width:
            geo_ids = handle_range_filtering(ST_GEOMORPHOLOGY.objects.all(), 'Channel_width', channel_width).values_list('GeoNo', flat=True)
            injection_location_ids = INJECTION_LOCATION.objects.filter(GeoNo__in=geo_ids).values_list('TracerNo', flat=True)
            query = query.filter(TracerNo__in=injection_location_ids)

        # If dates are provided, filter based on those dates
        if from_date and to_date:
            query = query.filter(Date__range=(from_date, to_date))
        elif from_date:
            query = query.filter(Date__gte=from_date)
        elif to_date:
            query = query.filter(Date__lte=to_date)
        
        return list(query)
        
    @staticmethod
    def handle_range_filtering(queryset, field_name, value):
        """
        Filters the given queryset based on the field_name and the value.
        The value can be either a single number or a range (e.g., "10-20").
        """
        if "-" in value:  # Value is a range
            min_value, max_value = map(float, value.split('-'))
            queryset = queryset.filter(**{f"{field_name}__gte": min_value, f"{field_name}__lte": max_value})
        else:  # Value is a single number
            queryset = queryset.filter(**{field_name: float(value)})
        
        return queryset


    @staticmethod
    def get_file_name_old(river_name, from_date, to_date):
        # Use today's date if both from_date and to_date are None
        if not from_date and not to_date:
            date_str = datetime.today().strftime('%B-%d-%Y')
        else:
            date_str = from_date.strftime('%B-%d-%Y') if from_date else to_date.strftime('%B-%d-%Y')
        return f"{river_name} {date_str}.csv" if river_name else f"{date_str}.csv"

    @staticmethod
    def get_file_name(river_name, from_date, to_date):
        # Use today's date if both from_date and to_date are None
        if not from_date and not to_date:
            date_str = datetime.today().strftime('%B-%d-%Y')
        else:
            date_str = from_date if from_date else to_date
        return f"{river_name} {date_str}.csv" if river_name else f"{date_str}.csv"
    @staticmethod
    def generate_zip(river_names, from_date, to_date):
        # Create a zip file
        zip_filename = "/mnt/data/exported_data.zip"
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for river in river_names:
                csv_data = Sheets.generate_csv(river_name=river, from_date=from_date, to_date=to_date)
                file_name = Sheets.get_file_name(river, from_date, to_date)
                # Add the CSV data to the zip file
                zipf.writestr(file_name, csv_data)
        return zip_filename




class ExploreForm(): 
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
