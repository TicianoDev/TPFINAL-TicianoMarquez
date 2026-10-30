from django.urls import include, path


urlpatterns = [
    path("sustentabilidad/", include("sustentabilidad.urls")),
]
