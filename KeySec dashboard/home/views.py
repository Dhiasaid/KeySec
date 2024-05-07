from django.shortcuts import render, redirect
from admin_datta.forms import RegistrationForm, LoginForm, UserPasswordChangeForm, UserPasswordResetForm, UserSetPasswordForm
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordResetConfirmView, PasswordResetView
from django.views.generic import CreateView
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from elasticsearch import Elasticsearch

from rest_framework.views import APIView

from .models import *

def index(request):

  context = {
    'segment'  : 'index',
    #'products' : Product.objects.all()
  }
  return render(request, "pages/index.html", context)

def tables(request):
  context = {
    'segment': 'tables'
  }
  return render(request, "pages/dynamic-tables.html", context)

class ElasticsearchQueryView(APIView):
    def get(self, request, format=None):
        # Connect to Elasticsearch
        es = Elasticsearch(['localhost:9200'])

        # Extract query parameters from request
        query = request.query_params.get('query', '')
        index_name = request.query_params.get('index', 'your_default_index')

        # Query Elasticsearch
        try:
            response = es.search(index=index_name, body={'query': {'match': {'content': query}}})
            hits = response['hits']['hits']
            # Process hits as needed
            return Response(hits)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
