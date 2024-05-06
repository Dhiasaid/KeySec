from django.contrib import admin
from .models import Agent

class AgentAdmin(admin.ModelAdmin):
    list_display = ('agent_id', 'desktop_name', 'ip_address', 'vlan')
    list_filter = ('agent_id',)  # Adjusted indentation here
    search_fields = ('name', 'ip_address')

admin.site.register(Agent, AgentAdmin)
