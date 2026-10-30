from django.shortcuts import render

from emisiones import obtener_metricas_consumo


REGISTROS_DEMO = [
    {"planta": "Planta Norte", "consumo_kwh": 1250},
    {"planta": "Planta Sur", "consumo_kwh": 1820},
    {"planta": "Planta Este", "consumo_kwh": 970},
    {"planta": "Planta Norte", "consumo_kwh": 900},
    {"planta": "Planta Sur", "consumo_kwh": 650},
    {"planta": "Planta Este", "consumo_kwh": 780},
]


def vista_panel_sustentabilidad(request):
    contexto = obtener_metricas_consumo(REGISTROS_DEMO)
    return render(request, "sustentabilidad/panel.html", contexto)
