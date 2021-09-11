from django.contrib import admin
from .models import Generation, Stromzeiten_table

admin.site.register(Generation)
admin.site.register(Stromzeiten_table)
# Register your models here.