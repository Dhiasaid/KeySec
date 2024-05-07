from django.urls import path
from django.contrib.auth import views as auth_views
from .views import ElasticsearchQueryView

from . import views

urlpatterns = [
  path(''       , views.index,  name='index'),
  path('tables/', views.tables, name='tables'),
   path('elasticsearch-query/', ElasticsearchQueryView.as_view(), name='elasticsearch-query'),
]
