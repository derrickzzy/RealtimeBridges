from django.contrib import admin
from server.models import *

# Register your models here.


# Register your models here.

class BridgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'conditions',)
    search_fields = ['name', 'number','conditions']
    list_filter = ('state', 'conditions',)

admin.site.register(Bridge,BridgeAdmin)