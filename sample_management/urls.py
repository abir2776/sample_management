from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

schema_view = get_schema_view(
    openapi.Info(
        title="swift_web_ai API",
        default_version="main",
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Swagger
    re_path(
        r"^docs/swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=10),
        name="schema-json",
    ),
    re_path(
        r"^docs/swagger$",
        schema_view.with_ui("swagger", cache_timeout=10),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^docs/redoc$",
        schema_view.with_ui("redoc", cache_timeout=10),
        name="schema-redoc",
    ),
    # JWT Token
    path(
        "api/v1/token",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "api/v1/token/refresh",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "api/v1/token/verify",
        TokenVerifyView.as_view(),
        name="token_verify",
    ),
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("organizations.rest.urls.register")),
    path("api/v1/organizations/", include("organizations.rest.urls")),
    path("api/v1/sample_manager/", include("sample_manager.rest.urls")),
    path("api/v1/users/", include("core.rest.urls")),
    path("api/v1/me", include("core.rest.urls.me")),
    path("api/v1/core/logs/", include("core.rest.urls.activitylog")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
