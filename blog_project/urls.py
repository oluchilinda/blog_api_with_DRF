"""blog_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.account.views import confirm_email
from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_auth.views import PasswordResetConfirmView
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

from rest_framework import permissions
from drf_yasg.views import get_schema_view as scheme
from drf_yasg import openapi


from rest_framework_swagger.views import get_swagger_view

from blog_api import views

API_TITLE = "Blog API"  #
API_DESCRIPTION = "A Web API for creating and editing blog posts."

coreapi_schema_view = get_schema_view(title=API_TITLE)

swagger_schema_view = get_swagger_view(title=API_TITLE)


schema_view = scheme(
    openapi.Info(
        title="Snippets API",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("blog_api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("api/v1/rest-auth/", include("rest_auth.urls")),
    path("api/v1/rest-auth/registration/", include("rest_auth.registration.urls")),
    url(
        r"^api/v1/accounts-rest/registration/account-confirm-email/(?P<key>.+)/$",
        confirm_email,
        name="account_confirm_email",
    ),
    url(
        r"^api/v1/registration/complete/$", views.success_view, name="account_confirm_complete"
    ),
    url(
        r"^api/v1/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    path('docs/', include_docs_urls(title=API_TITLE,description=API_DESCRIPTION)),
    path("schema/", coreapi_schema_view),
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]
