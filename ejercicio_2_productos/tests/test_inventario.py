import json
import tempfile
import unittest
from pathlib import Path

from inventario import (
    DispositivoEcologico,
    GestorInventario,
    PanelSolar,
    StockInvalidoError,
)


class TestInventario(unittest.TestCase):
    def test_stock_negativo_lanza_excepcion(self):
        producto = DispositivoEcologico("Lámpara LED", 18.5, 3)
        with self.assertRaises(StockInvalidoError):
            producto.stock = -1
        self.assertEqual(producto.stock, 3)

    def test_panel_hereda_y_personaliza_ficha(self):
        panel = PanelSolar("EcoPanel", 250, 5, 400, 20.5)
        ficha = panel.ficha_tecnica()
        self.assertIn("400 W", ficha)
        self.assertIn("20.5%", ficha)
        self.assertEqual(panel.a_diccionario()["tipo"], "PanelSolar")

    def test_guarda_catalogo_en_json(self):
        productos = [PanelSolar("EcoPanel", 250, 5, 400, 20.5)]
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "catalogo_ecotech.json"
            resultado = GestorInventario.guardar_catalogo_json(productos, ruta)
            datos = json.loads(resultado.read_text(encoding="utf-8"))
        self.assertEqual(datos[0]["nombre"], "EcoPanel")
        self.assertEqual(datos[0]["stock"], 5)

    def test_no_permite_crear_stock_negativo(self):
        with self.assertRaises(StockInvalidoError):
            DispositivoEcologico("Lámpara LED", 18.5, -1)

    def test_stock_cero_es_valido(self):
        producto = DispositivoEcologico("Lámpara LED", 18.5, 0)
        self.assertEqual(producto.stock, 0)

    def test_stock_debe_ser_entero(self):
        producto = DispositivoEcologico("Lámpara LED", 18.5, 3)
        with self.assertRaises(TypeError):
            producto.stock = 2.5


if __name__ == "__main__":
    unittest.main()
