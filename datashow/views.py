from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, StreamingHttpResponse, HttpResponse, FileResponse
from django.urls import reverse
from .forms import *
from .data_monster.explore import * #explore.py in data_monster
from .models import * #models.py
from .forms import * #forms.py


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

def documentation(request):
    return render(request, "datashow/documentation.html")

def test(request):
    return render(request, "datashow/test.html")

def explore(request):
    form = ExploreForm(request.POST)
    
    # get the unique values for the dropdowns
    tracer_types = INJECTION_TRACER.objects.values_list('Type', flat=True).distinct().order_by('Type')
    river_names = INJECTION_LOCATION.objects.values_list('Name', flat=True).distinct().order_by('Name')
    
    # set the choices for the dropdowns
    form.fields['river_name'].choices = [('', '')] + [(name, name) for name in river_names]
    form.fields['tracer_type'].choices = [('', '')] + [(tracer, tracer) for tracer in tracer_types]

    if request.method == "POST" and form.is_valid():
        # Store the search parameters in session
        request.session['river_name'] = form.cleaned_data['river_name']
        request.session['flow_rate'] = form.cleaned_data['flow_rate']
        request.session['channel_width'] = form.cleaned_data['channel_width']
        request.session['tracer_type'] = form.cleaned_data['tracer_type']
        request.session['from_date'] = form.cleaned_data['from_date']
        request.session['to_date'] = form.cleaned_data['to_date']

        return redirect('download_view')
    elif request.method == "POST":
        # Let Django handle form-specific validation errors
        return render(request, 'datashow/explore.html', {'form': form})
    return render(request, 'datashow/explore.html', {'form': form})




def download_view(request):

    download_form = DownloadForm(request.POST)
    
    if request.method == "POST":
        return download_csv(request)

    return render(request, "datashow/download.html", {'download_form': download_form})


# The download_csv view uses the Sheets class to generate the CSV.
def download_csv(request):
    sheets = Sheets()
    try:
        # Fetch parameters from session
        river_name = request.session.get('river_name', None)
        tracer_type = request.session.get('tracer_type', None)
        from_date = request.session.get('from_date', None)
        to_date = request.session.get('to_date', None)
        flow_rate = request.session.get('flow_rate', None)
        channel_width = request.session.get('channel_width', None)

        # Generate the CSV content
        csv_content = sheets.generate_csv(river_name, tracer_type, from_date, to_date, flow_rate, channel_width)
        
        # Create the response with the generated CSV
        response = HttpResponse(csv_content, content_type='text/csv')
        
        # Set the file name for the CSV
        file_name = sheets.get_file_name(river_name, from_date, to_date)
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        
        return response
    except Exception as e:
        print(f"Exception details: {e}")
        # Handle the exception and show an error message to the user
        return render(request, "datashow/error.html", {'message': "An error occurred while generating the CSV. Please try again later."})

def stream_csv_data(response):

    timeseries = TimeseriesData()
    river_name=response.session.get('river_name', None),
    tracer_type=response.session.get('tracer_type', None),
    from_date=response.session.get('from_date', None),
    to_date=response.session.get('to_date', None),
    data = timeseries.get_data(
        river_name=river_name, 
        tracer_type=tracer_type, 
        from_date=from_date, 
        to_data=to_date,
        )

    timeseries_data = data['timeseries']
    if not timeseries_data:
        raise ValueError("No data found for the specified criteria.") # Raise an exception

    def generate():
        yield 'Time,Concentration\n'  # Header
        for entry in timeseries_data:
            yield f"{entry['time']},{entry['concentration']}\n"

    return StreamingHttpResponse(generate(), content_type="text/csv")

def download_csv_pre_october_30(request):
    try:
        # Fetch parameters from session
        river_name = request.session.get('river_name', None)
        tracer_type = request.session.get('tracer_type', None)
        from_date = request.session.get('from_date', None)
        to_date = request.session.get('to_date', None)
        flow_rate = request.session.get('flow_rate', None)
        channel_width = request.session.get('channel_width', None)

        # Generate the CSV content
        csv_content = Sheets.generate_csv(river_name, tracer_type, from_date, to_date, flow_rate, channel_width)
        
        # Create the response with the generated CSV
        response = StreamingHttpResponse(csv_content, content_type='text/csv')
        
        # Set the file name for the CSV
        file_name = Sheets.get_file_name(river_name, from_date, to_date)
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        
        return response
    except Exception as e:
        # Handle the exception and show an error message to the user
        print(f"error from download_csv function: {e}")
        return render(request, "datashow/error.html", {'message': "An error occurred while generating the CSV. Please try again later."})


def origina___download_csv(request):
    try:
        response = StreamingHttpResponse(stream_csv_data(request), content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="timeseries_data.csv"'
        return response
    except Exception as e:
 # Log the detailed error for internal use
        print(f"Error from download_csv function: {e}")
        
        # Show a generic error message to the user
        user_friendly_message = "An error occurred while processing your request. Please try again."
        return render(request, "datashow/error.html", {'message': str(e)})



def explore_form(request):
    if request.method == "GET":
        print("GETTING")
    
    else:
        print("Insider explore form but not getting")


def explore_results(request):
    tracer_types = INJECTION_TRACER.objects.values_list('Type', flat=True).distinct()
    river_names = INJECTION_LOCATION.objects.values_list('Name', flat=True).distinct()

    if request.method == "POST":
        print("\n POSTING \n")
        # form = ExploreForm(request.POST)
        # form.fields['river_name'].choices = [('', '')] + [(name, name) for name in river_names]
        # form.fields['tracer_type'].choices = [('', '')] + [(tracer, tracer) for tracer in tracer_types]

        # if form.is_valid():
        #     river_name = form.cleaned_data['river_name']
        #     tracer_type = form.cleaned_data['tracer_type']
        #     flow_rate = form.cleaned_data['flow_rate']
        #     channel_width = form.cleaned_data['channel_width']
        #     from_date = form.cleaned_data['from_date']
        #     to_date = form.cleaned_data['to_date']

        #     explore_data = ExploreData()
            # data = explore_data.get_data(
        #         {
        #             'river': river_name,
        #             'tracer_type': tracer_type,
        #             'flow_rate': flow_rate,
        #             'channel_width': channel_width,
        #             'from_date': from_date,
        #             'to_date': to_date,
        #         })

            # return render(request, 'datashow/explore_results.html', {'form': form, 'data': data})
        return render(request, 'datashow/explore_results.html', {'data': ['a','b','c']})


def explore_old(request): 
    # timeseries = TimeSeries()
    
    rivers = INJECTION_LOCATION.objects.values_list('Name', flat=True).distinct()
    sheets = CONC_TIMESERIES.objects.values_list('Sheet_name', flat=True).distinct()
    tracers = INJECTION_TRACER.objects.values_list('Type', flat=True).distinct()
    features = ['Bed Material', 'Bed Mat Thickness', 'Bed Slope', 'Channel Width',
                'Channel Depth', 'Cx Area', 'Mannings n']
    orders = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    if request.method == 'POST':
        # form = timeseriesForm(request.POST) #
        # if form.is_valid():
        #     river_name = form.cleaned_data['river_name']
        #     stream_order = form.cleaned_data['stream_order']
            # channel_width = form.channel_width['channel_width']
            # tracer_type = form.cleaned_data['tracer_type']
            # flow_rate = form.cleaned_data['flow_rate']
        # ts = timeseries.get_data(
        #         {
        #             'river': river_name,
        #             'stream_order': stream_order,
        #             # 'channel_width': channel_width,
        #             'tracer_type': tracer_type,
        #             'flow_rate': flow_rate, #flow_rate.split(',')[0],
        #             })
        context = {
            # 'form': form,
            'current_river': rivers[0],
            'tracers': sorted(tracers),
            'features': sorted(features),
            # 'timeseries': ts['timeseries'],
            # 'ss_rivers':  sorted(ts['rivers']),
            # 'ss_sheets':  sorted(ts['sheets']),
        }
    else:
        # form = timeseriesForm()
        # ts = timeseries.get_data(
        #         {
        #             'river': 'Shane',
        #             'stream_order': 0,
        #             'channel_width': 0,
        #             'tracer_type': 'Rhodamine BA',
        #             'flow_rate': 41,
        #         })
        context = {
            # 'form': form,
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
