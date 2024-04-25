from django.contrib import admin
from .models import Order, Summary, Sum

class SummaryAdmin(admin.ModelAdmin):
    list_display = ('date_order', 'name', 'amount', 'sum', 'average')
    list_filter = ['name']
    ordering = ['date_order', 'amount', 'sum', 'average']

class SumAdmin(admin.ModelAdmin):
    list_display = ('date_order', 'sum')

admin.site.register(Order)
admin.site.register(Summary, SummaryAdmin)
admin.site.register(Sum, SumAdmin)