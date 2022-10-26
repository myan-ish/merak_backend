
from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

documentaiton_apis = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

api_patterns = [
    path("user/", include("user.urls")),
    path("audit/", include("audit.urls")),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(documentaiton_apis)),
    path('api/', include(api_patterns)),
]
