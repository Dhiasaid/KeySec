from django.http import HttpResponse

def index(request):
    """
    View to display the index page.
    """
    return HttpResponse("dhia said api keystone for communicating between agents and the dashboard of suricata")

from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Agent
from .serializers import AgentSerializer
from rest_framework import viewsets

@api_view(['GET'])
def agent_list(request):
    agent = {"agent_id":1, "desktop_name": "asus", "ip_address": "192.168.0.1","vlan":"keystone"}
    return Response(agent)

class AgentViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing agent instances.
    """
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer