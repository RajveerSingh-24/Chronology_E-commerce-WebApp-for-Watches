from django.contrib import admin
from .models import Product
from .models import Order

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'featured')
    list_filter = ('featured',)

admin.site.register(Order)