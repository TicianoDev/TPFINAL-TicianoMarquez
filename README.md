# 🌱 EcoTech Solutions

![EcoTech Solutions: sensores, productos y auditoría web](assets/ecotech-banner.gif)

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.x-092E20?style=flat-square&logo=django&logoColor=white)
![IDE](https://img.shields.io/badge/IDE-PyCharm%20Professional-21A179?style=flat-square)
![Pruebas](https://img.shields.io/badge/Tests-26%20OK-238636?style=flat-square)

Proyecto académico de Python y Django con tres ejercicios independientes: procesamiento de sensores, gestión de productos y un panel web de sustentabilidad.

**Desarrollado y probado en PyCharm Professional.** También se puede ejecutar desde una terminal, sin depender del IDE.

---

## 📂 Estructura

```text
ecotech-solutions/
├── README.md
├── .gitignore
├── assets/
│   └── ecotech-banner.gif
├── ejercicio_1_sensores/
│   ├── sensores.py
│   └── tests/test_sensores.py
├── ejercicio_2_productos/
│   ├── inventario.py
│   ├── catalogo_ecotech.json
│   └── tests/test_inventario.py
└── ejercicio_3_auditoria_web/
    ├── manage.py
    ├── emisiones.py
    ├── tests.py
    ├── requirements.txt
    ├── configuracion/
    └── sustentabilidad/
        ├── views.py
        ├── urls.py
        └── templates/sustentabilidad/panel.html
```

Cada ejercicio puede abrirse como un proyecto separado en PyCharm. `assets` solo contiene la animación del README.

## 🛠️ Requisitos y preparación

- Python **3.10 o superior**.
- PyCharm Professional o cualquier editor con terminal.
- Django para el ejercicio 3. Los dos primeros usan solo la biblioteca estándar.

Abre la carpeta del repositorio en PyCharm y configura un entorno virtual. También puedes crearlo desde la raíz:

```bash
python -m venv .venv
```

Actívalo según tu sistema:

| Sistema | Comando |
| --- | --- |
| Windows — PowerShell | `.\.venv\Scripts\Activate.ps1` |
| Windows — CMD | `.venv\Scripts\activate.bat` |
| Linux / macOS | `source .venv/bin/activate` |

Si tu sistema usa `python3`, reemplaza `python` por `python3` al crear el entorno.

---

## 🌡️ Ejercicio 1 · Sensores

Normaliza lecturas térmicas y genera un reporte de temperaturas.

- Limpieza de espacios en los identificadores.
- Conversión de temperaturas a `float`, con ejemplos como `24.5C` y `27,2 °C`.
- Ubicación predeterminada cuando no se informa.
- Validación de lecturas inválidas.
- Promedio global y sensores que superan el umbral.

Desde la raíz del repositorio:

```bash
cd ejercicio_1_sensores
python sensores.py
python -m unittest discover -s tests -v
cd ..
```

**Resultado del ejemplo:**

```text
Reporte de sensores EcoTech Solutions
Sensores procesados: 3
Temperatura promedio: 27.57 °C
Sensores sobre el umbral: SENSOR-002
```

## 📦 Ejercicio 2 · Productos e inventario

Implementa un catálogo con programación orientada a objetos y persistencia en JSON.

- Clase base `DispositivoEcologico` y clase derivada `PanelSolar`.
- Stock encapsulado mediante una propiedad.
- Excepción `StockInvalidoError` para impedir valores negativos.
- Herencia y polimorfismo en las fichas técnicas.
- Exportación con `GestorInventario` a `catalogo_ecotech.json`.

Desde la raíz del repositorio:

```bash
cd ejercicio_2_productos
python inventario.py
python -m unittest discover -s tests -v
cd ..
```

El programa demuestra la captura de un stock negativo y guarda los productos válidos. Cada ejecución actualiza el JSON de ejemplo.

## 🌍 Ejercicio 3 · Auditoría y panel Django

Calcula las emisiones de carbono del consumo eléctrico y muestra las métricas en una aplicación Django.

- `calcular_emisiones_carbono`, con factor predeterminado de **0,4 kg CO₂/kWh**.
- Clase `TestCalculoEmisiones`, basada en `unittest.TestCase`.
- Cálculo de emisiones totales y consumo acumulado por planta.
- Vista basada en función: `vista_panel_sustentabilidad`.
- Plantilla `sustentabilidad/panel.html`.
- Registros simulados en `sustentabilidad/views.py`.

Desde la raíz, con el entorno virtual activo:

```bash
cd ejercicio_3_auditoria_web
python -m pip install -r requirements.txt
python manage.py check
python manage.py test -v 2
python manage.py runserver
```

Abre **http://127.0.0.1:8000/sustentabilidad/**.

Detén el servidor con **Ctrl + C**. Para este panel no hace falta cargar usuarios ni ejecutar migraciones.

---

## 🧪 Pruebas automatizadas

Se incluyen **26 pruebas**, todas aprobadas durante la verificación local del proyecto:

| Ejercicio | Pruebas | Comprobaciones |
| --- | ---: | --- |
| Sensores | 8 | Limpieza, decimales, validaciones, alertas, promedio y lista vacía |
| Productos | 6 | Stock válido e inválido, herencia, ficha técnica y exportación JSON |
| Auditoría y web | 12 | Cálculos, excepciones, agregación, URL, contexto y plantilla |
| **Total** | **26** | **Todas aprobadas** |

Las pruebas utilizan **`unittest`** y las herramientas de testing de Django. La verificación del proyecto se realizó con **Django 5.2.18**.

> El indicador de pruebas resume la comprobación local. No representa una ejecución automática de GitHub Actions.

## ✅ Decisiones de implementación

- La lógica de cálculo está separada de la vista Django.
- La limpieza devuelve un diccionario nuevo y no modifica el original.
- Una temperatura igual al umbral no genera alerta: debe superarlo.
- Una lista vacía de sensores devuelve `([], 0.0)`.
- Si falla una actualización de stock, se conserva su valor anterior.
- La planta de mayor consumo se determina sumando todos sus registros. En un empate, se conserva la primera del historial.
- Un historial vacío devuelve emisiones cero y ninguna planta ganadora.
- El catálogo JSON se guarda con codificación UTF-8.
- `.gitignore` excluye entornos virtuales, cachés, archivos del IDE y secretos locales.

## 🔒 Alcance

Proyecto orientado a una entrega académica y a pruebas locales. El factor de emisión es de ejemplo, no una certificación ambiental.

Django utiliza una clave de desarrollo y `DEBUG=True`. La configuración requiere ajustes de seguridad antes de un despliegue en producción.
