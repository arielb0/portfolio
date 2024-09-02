from django.contrib import admin
from .models import Currency, Category, Ad, Report

# Register your models here.

admin.site.register([Currency, Category, Ad, Report])
