from django.shortcuts import render
from .models import *
from datetime import datetime, timedelta
from django.db.models import When, Case

now = datetime.now()

data_set = Stromzeiten_table.objects.all()



def home(request):




    context = {
        'data_forecast': Stromzeiten_table_forecast.objects.all(),
        'data1_forecast': Beste_table_forecast.objects.all(),
        'data2_forecast': Gute_table_forecast.objects.all(),
        'data3_forecast': Schlechte_table_forecast.objects.all(),
        'data': Stromzeiten_table.objects.all(),
        'data1': Beste_table.objects.all(),
        'data2': Gute_table.objects.all(),
        'data3': Schlechte_table.objects.all(),
        'data4': Stromzeiten_table.objects.filter(Date__gt=datetime.now()-timedelta(minutes=15))

    }
    return render(request, 'Stromzeiten_app/home.html', context)

def homeNew(request):

    context = {
        'data_forecast': Stromzeiten_table_forecast.objects.all(),
        'data1_forecast': Beste_table_forecast.objects.all(),
        'data2_forecast': Gute_table_forecast.objects.all(),
        'data3_forecast': Schlechte_table_forecast.objects.all(),
        'data': Stromzeiten_table.objects.all(),
        'data1': Beste_table.objects.all(),
        'data2': Gute_table.objects.all(),
        'data3': Schlechte_table.objects.all(),
        'data4': Stromzeiten_table.objects.filter(Date__gt=datetime.now()-timedelta(minutes=15))

    }
    return render(request, 'Stromzeiten_app/home-new.html', context)


def about(request):
    return render(request, 'Stromzeiten_app/about.html', {'title': 'About'})


def chart(request):
    context = {
        'data': Stromzeiten_table.objects.order_by('Date')
    }
    return render(request, 'Stromzeiten_app/chart.html', context)


