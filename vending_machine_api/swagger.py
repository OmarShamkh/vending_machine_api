from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Vending Machine API",
        default_version='v1',
        description="API documentation for the Vending Machine",
    ),
    public=True,
)
