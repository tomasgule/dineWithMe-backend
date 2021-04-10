from django.contrib import admin
from .models import DinnerEvent

# Register your models here.
@admin.register(DinnerEvent)
class DinnerEventeAdmin(admin.ModelAdmin):
    list_display = ("header", "host", "description", "dateTime")