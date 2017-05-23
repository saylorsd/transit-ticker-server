from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from . import models

class TickerAdmin(admin.ModelAdmin):
    readonly_fields = ('status','last_message')

admin.site.register(models.TickerStation, TickerAdmin)
admin.site.register(models.Prediction)

