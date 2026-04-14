from django.contrib import admin
from django.urls import path, include
from reservas.views import LandingView, RegistroView, LoginView, ApiDocsView

urlpatterns = [
    # Páginas HTML
    path("",          LandingView.as_view(),  name="landing"),
    path("registro/", RegistroView.as_view(), name="registro"),
    path("login/",    LoginView.as_view(),    name="login"),
    path("docs/",     ApiDocsView.as_view(),  name="api-docs"),
    # Admin
    path("admin/",    admin.site.urls),
    # API REST
    path("api/",      include("usuarios.urls")),
    path("api/",      include("reservas.urls")),
    path("api/",      include("pagos.urls")),
]
