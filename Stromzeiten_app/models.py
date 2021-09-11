from django.db import models
from django.utils import timezone
from django.conf import settings


# Create your models here.

class Generation(models.Model):
    id = models.IntegerField(primary_key=True)
    Biomass = models.IntegerField()
    Fossil_Brown_coal_Lignite = models.IntegerField()
    Fossil_Gas = models.IntegerField()
    Fossil_Hard_coal = models.IntegerField()
    Fossil_Oil = models.IntegerField()
    Geothermal = models.IntegerField()
    Hydro_Pumped_Storage = models.IntegerField()
    Hydro_Run_of_river_and_poundage = models.IntegerField()
    Hydro_Water_Reservoir = models.IntegerField()
    Nuclear = models.IntegerField()
    Other = models.IntegerField()
    Other_renewable = models.IntegerField()
    Solar = models.IntegerField()
    Waste = models.IntegerField()
    Wind_Offshore = models.IntegerField()
    Wind_Onshore = models.IntegerField()
    Date = models.CharField(max_length=100)
    Total_Non_Renewables = models.IntegerField()
    Total_Renewables = models.IntegerField()
    Total = models.IntegerField()
    Renewables_procentaqe = models.IntegerField()

class Stromzeiten_table(models.Model):
    id = models.IntegerField(primary_key=True)
    Solar = models.IntegerField()
    Wind_Offshore = models.IntegerField()
    Wind_Onshore = models.IntegerField()
    Total = models.IntegerField()
    Renewable_Load_ratio = models.IntegerField()
    Quality_ratio = models.IntegerField()
    Date = models.DateTimeField()

class Beste_table(models.Model):
    id = models.IntegerField(primary_key=True)
    Date_start = models.DateTimeField()
    Date_end = models.DateTimeField()

class Gute_table(models.Model):
    id = models.IntegerField(primary_key=True)
    Date_start = models.DateTimeField()
    Date_end = models.DateTimeField()

class Schlechte_table(models.Model):
    id = models.IntegerField(primary_key=True)
    Date_start = models.DateTimeField()
    Date_end = models.DateTimeField()


class Stromzeiten_table_forecast(models.Model):
    id = models.IntegerField(primary_key=True)
    Solar = models.IntegerField()
    Wind_Offshore = models.IntegerField()
    Wind_Onshore = models.IntegerField()
    Total = models.IntegerField()
    Renewable_Load_ratio = models.IntegerField()
    Quality_ratio = models.IntegerField()
    Date = models.DateTimeField()

class Beste_table_forecast(models.Model):
    id = models.IntegerField(primary_key=True)
    Date_start = models.DateTimeField()
    Date_end = models.DateTimeField()

class Gute_table_forecast(models.Model):
    id = models.IntegerField(primary_key=True)
    Date_start = models.DateTimeField()
    Date_end = models.DateTimeField()

class Schlechte_table_forecast(models.Model):
    id = models.IntegerField(primary_key=True)
    Date_start = models.DateTimeField()
    Date_end = models.DateTimeField()
