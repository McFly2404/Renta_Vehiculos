from django.contrib import admin
from django.urls import path, include
from reservas.views import (
    ApiDocsView,
    IntegracionesView,
    LandingView,
    LoginView,
    RegistroView,
)

urlpatterns = [
    # HTML pages
    path("",          LandingView.as_view(),  name="landing"),
    path("registro/", RegistroView.as_view(), name="registro"),
    path("login/",    LoginView.as_view(),    name="login"),
    path("docs/",     ApiDocsView.as_view(),  name="api-docs"),
    path("integraciones/", IntegracionesView.as_view(), name="integraciones"),
    # Admin
    path("admin/",    admin.site.urls),
    path("i18n/",     include("django.conf.urls.i18n")),
    # API REST
    path("api/",      include("usuarios.urls")),
    path("api/",      include("reservas.urls")),
    path("api/",      include("pagos.urls")),
    path("api/",      include("integraciones.urls")),
]
