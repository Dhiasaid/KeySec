from django.urls import re_path
from django.views.decorators.csrf import csrf_exempt
from .views import ElasticsearchQueryView

from api.views import *
from . import views


urlpatterns = [

	re_path("product/((?P<pk>\d+)/)?", csrf_exempt(ProductView.as_view())),
     path('elasticsearch-query/', ElasticsearchQueryView.as_view(), name='elasticsearch-query'),

]