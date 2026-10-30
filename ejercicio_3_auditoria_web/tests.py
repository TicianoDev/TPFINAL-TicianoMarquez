import unittest

from django.test import RequestFactory, SimpleTestCase

from emisiones import calcular_emisiones_carbono, obtener_metricas_consumo
from sustentabilidad.views import vista_panel_sustentabilidad


class TestCalculoEmisiones(unittest.TestCase):
    def test_calculo_nominal(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(100), 40.0)

    def test_factor_personalizado(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(50, 0.2), 10.0)

    def test_consumo_cero(self):
        self.assertEqual(calcular_emisiones_carbono(0), 0.0)

    def test_consumo_decimal(self):
        self.assertAlmostEqual(calcular_emisiones_carbono(12.75), 5.1)

    def test_factor_cero(self):
        self.assertEqual(calcular_emisiones_carbono(100, 0), 0.0)

    def test_consumo_negativo_lanza_value_error(self):
        with self.assertRaises(ValueError):
            calcular_emisiones_carbono(-1)


class TestMetricasConsumo(unittest.TestCase):
    def test_agrega_consumos_por_planta(self):
        registros = [
            {"planta": "Norte", "consumo_kwh": 100},
            {"planta": "Sur", "consumo_kwh": 300},
            {"planta": "Norte", "consumo_kwh": 50},
        ]
        metricas = obtener_metricas_consumo(registros)
        self.assertAlmostEqual(metricas["total_emisiones"], 180.0)
        self.assertEqual(metricas["planta_mayor_consumo"], "Sur")
        self.assertEqual(metricas["consumo_por_planta"]["Norte"], 150.0)

    def test_mayor_consumo_se_calcula_por_acumulado(self):
        registros = [
            {"planta": "Norte", "consumo_kwh": 200},
            {"planta": "Sur", "consumo_kwh": 300},
            {"planta": "Norte", "consumo_kwh": 200},
        ]
        metricas = obtener_metricas_consumo(registros)
        self.assertEqual(metricas["planta_mayor_consumo"], "Norte")
        self.assertEqual(metricas["consumo_maximo_kwh"], 400)

    def test_historial_vacio(self):
        metricas = obtener_metricas_consumo([])
        self.assertEqual(metricas["total_emisiones"], 0)
        self.assertIsNone(metricas["planta_mayor_consumo"])
        self.assertEqual(metricas["detalle_plantas"], [])

    def test_historial_con_consumo_negativo(self):
        with self.assertRaises(ValueError):
            obtener_metricas_consumo([{"planta": "Norte", "consumo_kwh": -1}])


class TestVistaPanel(SimpleTestCase):
    def test_vista_renderiza_metricas(self):
        request = RequestFactory().get("/sustentabilidad/")
        respuesta = vista_panel_sustentabilidad(request)
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Panel de sustentabilidad")
        self.assertContains(respuesta, "Planta Sur")

    def test_url_y_plantilla_del_panel(self):
        respuesta = self.client.get("/sustentabilidad/")
        self.assertEqual(respuesta.status_code, 200)
        self.assertTemplateUsed(respuesta, "sustentabilidad/panel.html")
        self.assertAlmostEqual(respuesta.context["total_emisiones"], 2548.0)
        self.assertEqual(respuesta.context["planta_mayor_consumo"], "Planta Sur")
