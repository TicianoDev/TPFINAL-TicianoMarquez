import json
import math
from pathlib import Path


class StockInvalidoError(ValueError):
    pass


class DispositivoEcologico:
    def __init__(self, nombre, precio, stock):
        self.nombre = str(nombre).strip()
        if not self.nombre:
            raise ValueError("El nombre del dispositivo no puede estar vacío.")
        self.precio = float(precio)
        if not math.isfinite(self.precio) or self.precio < 0:
            raise ValueError("El precio debe ser finito y no negativo.")
        self.stock = stock

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise TypeError("El stock debe ser un número entero.")
        if valor < 0:
            raise StockInvalidoError("El stock no puede ser negativo.")
        self._stock = valor

    def ficha_tecnica(self):
        return f"{self.nombre} | Precio: ${self.precio:.2f} | Stock: {self.stock}"

    def a_diccionario(self):
        return {
            "tipo": self.__class__.__name__,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock": self.stock,
        }


class PanelSolar(DispositivoEcologico):
    def __init__(self, nombre, precio, stock, potencia_w, eficiencia):
        super().__init__(nombre, precio, stock)
        self.potencia_w = float(potencia_w)
        self.eficiencia = float(eficiencia)
        if not math.isfinite(self.potencia_w) or self.potencia_w <= 0:
            raise ValueError("La potencia debe ser mayor que cero.")
        if not 0 < self.eficiencia <= 100:
            raise ValueError("La eficiencia debe estar entre 0 y 100.")

    def ficha_tecnica(self):
        return (
            f"Panel solar {self.nombre} | {self.potencia_w:g} W | "
            f"Eficiencia: {self.eficiencia:.1f}% | "
            f"Precio: ${self.precio:.2f} | Stock: {self.stock}"
        )

    def a_diccionario(self):
        datos = super().a_diccionario()
        datos.update({
            "potencia_w": self.potencia_w,
            "eficiencia": self.eficiencia,
        })
        return datos


class GestorInventario:
    @staticmethod
    def guardar_catalogo_json(lista_dispositivos, ruta_archivo):
        ruta = Path(ruta_archivo)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        catalogo = [dispositivo.a_diccionario() for dispositivo in lista_dispositivos]
        ruta.write_text(
            json.dumps(catalogo, ensure_ascii=False, indent=2, allow_nan=False),
            encoding="utf-8",
        )
        return ruta


def main():
    panel = PanelSolar("EcoPanel 450", 289.90, 12, 450, 21.5)
    otro_panel = PanelSolar("EcoPanel 380", 239.50, 8, 380, 19.8)

    try:
        panel.stock = -3
    except StockInvalidoError as error:
        print(f"No se pudo actualizar el stock: {error}")

    dispositivos = [panel, otro_panel]
    for dispositivo in dispositivos:
        print(dispositivo.ficha_tecnica())

    ruta = GestorInventario.guardar_catalogo_json(
        dispositivos,
        Path(__file__).with_name("catalogo_ecotech.json"),
    )
    print(f"Catálogo guardado en: {ruta}")


if __name__ == "__main__":
    main()
