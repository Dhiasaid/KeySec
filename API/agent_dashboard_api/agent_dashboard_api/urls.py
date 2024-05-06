# project_name/urls.py

from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from agent_api import views
from rest_framework import routers
from django.contrib import admin

# Define the router for registering viewsets
router = routers.DefaultRouter()
router.register(r'agents', views.AgentViewSet)
router.register(r'posts', views.AgentViewSet, basename='post')  # Assuming you have a PostViewSet

# Define schema view for API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation for our project",
        contact=openapi.Contact(email="dhiasaid337@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

# Define URL patterns
urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', views.index, name='index'),
    path('api/', include(router.urls)),  # Include API endpoints under /api/ prefix
]
