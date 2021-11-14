from django.contrib import admin
from .models import Cryptocurrency, AssetHistory, OrderHistory


admin.site.register(Cryptocurrency)
admin.site.register(AssetHistory)
admin.site.register(OrderHistory)