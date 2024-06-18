from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(WarehouseLocation)
# admin.site.register(Warehouse)
# admin.site.register(Division)
admin.site.register(InventoryItems)
admin.site.register(WarehouseSection)
admin.site.register(WarehouseSubSection)
admin.site.register(WarehouseSubSubSection)
admin.site.register(InventoryDetails)
