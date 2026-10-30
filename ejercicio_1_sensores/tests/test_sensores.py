import unittest

from sensores import generar_resumen_sensores, limpiar_registro_sensor


class TestSensores(unittest.TestCase):

    def test_limpia_espacios_unidades_y_ubicacion_ausente(self):
        resultado = limpiar_registro_sensor({
            "sensor_id": " SENSOR-001 ",
            "temperatura": "24.5C",
            "ubicacion": "  ",
        })
        self.assertEqual(resultado["sensor_id"], "SENSOR-001")
        self.assertEqual(resultado["temperatura"], 24.5)
        self.assertEqual(resultado["ubicacion"], "Ubicación no especificada")

    def test_acepta_decimal_con_coma(self):
        # European format decimal check
        resultado = limpiar_registro_sensor({
            "sensor_id": "SENSOR-002",
            "temperatura": "27,2 °C",
            "ubicacion": "Planta Sur",
        })
        self.assertEqual(resultado["temperatura"], 27.2)

    def test_rechaza_temperatura_invalida(self):
        # Should fail when passing text instead of numbers
        with self.assertRaises(ValueError):
            limpiar_registro_sensor({"sensor_id": "S-1", "temperatura": "frío"})

    def test_resumen_devuelve_alertas_y_promedio(self):
        sensores = [
            {"sensor_id": "S-1", "temperatura": 20.0},
            {"sensor_id": "S-2", "temperatura": 32.0},
            {"sensor_id": "S-3", "temperatura": 28.0},
        ]
        alertas, promedio = generar_resumen_sensores(sensores, 30)

        self.assertEqual(alertas, ["S-2"])
        self.assertEqual(promedio, 80 / 3)

    def test_no_modifica_el_registro_original(self):
        registro = {"sensor_id": " S-1 ", "temperatura": "20C"}
        copia = dict(registro)  # Using dict() instead of .copy() just cuz
        limpiar_registro_sensor(registro)
        self.assertEqual(registro, copia)

    def test_rechaza_identificador_ausente(self):
        with self.assertRaises(ValueError):
            limpiar_registro_sensor({"sensor_id": None, "temperatura": 20})

    def test_igual_al_umbral_no_genera_alerta(self):
        sensores = [{"sensor_id": "S-1", "temperatura": 30.0}]
        res_alertas, res_promedio = generar_resumen_sensores(sensores, 30)

        self.assertEqual(res_alertas, [])
        self.assertEqual(res_promedio, 30.0)

    def test_resumen_vacio(self):
        vacio_alertas, vacio_promedio = generar_resumen_sensores([], 30)
        self.assertEqual(vacio_alertas, [])
        self.assertEqual(vacio_promedio, 0.0)


if __name__ == "__main__":
    unittest.main()