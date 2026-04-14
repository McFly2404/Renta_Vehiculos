"""Vistas de páginas HTML. Solo sirven templates — sin lógica de negocio."""
from django.views.generic import TemplateView


class LandingView(TemplateView):
    template_name = "index.html"

class RegistroView(TemplateView):
    template_name = "registro.html"

class LoginView(TemplateView):
    template_name = "login.html"

class ApiDocsView(TemplateView):
    template_name = "api_docs.html"
