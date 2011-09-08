'''
Created on Aug 11, 2011

@author: mmornati
'''

from webui.puppetclasses.models import PuppetClass
from django.contrib import admin
from guardian.admin import GuardedModelAdmin
    

class PuppetClassAdmin(GuardedModelAdmin):
    fieldsets = [
        ("General",   {'fields': ['name']}),
        ("Details",   {'fields': ['description', 'icon', 'enabled', 'parent']}),         
    ]
    list_display = ('name', 'description')
    search_fields = ['name']
    
admin.site.register(PuppetClass, PuppetClassAdmin)
