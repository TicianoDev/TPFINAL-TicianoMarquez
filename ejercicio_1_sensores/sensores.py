import math
import re


_NUMERO = re.compile(r"\s*([-+]?(?:\d+(?:[.,]\d*)?|[.,]\d+)(?:[eE][-+]?\d+)?)\s*[°º]?\s*[a-zA-Z]*\s*")


def limpiar_registro_sensor(registro_crudo):
    if not isinstance(registro_crudo, dict):
        raise TypeError("El registro del sensor debe ser un diccionario.")

    sensor_id = str(registro_crudo.get("sensor_id") or "").strip()
    if not sensor_id:
        raise ValueError("El registro debe incluir un sensor_id.")

    temperatura_raw = registro_crudo.get("temperatura")
    if isinstance(temperatura_raw, bool) or temperatura_raw is None:
        raise ValueError("La temperatura debe contener un valor numérico.")

    if isinstance(temperatura_raw, (int, float)):
        temperatura = float(temperatura_raw)
    else:
        coincidencia = _NUMERO.fullmatch(str(temperatura_raw))
        if not coincidencia:
            raise ValueError(f"Temperatura no válida: {temperatura_raw!r}")
        temperatura = float(coincidencia.group(1).replace(",", "."))

    if not math.isfinite(temperatura):
        raise ValueError("La temperatura debe ser un número finito.")

    ubicacion = str(registro_crudo.get("ubicacion") or "").strip()
    if not ubicacion:
        ubicacion = "Ubicación no especificada"

    return {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "ubicacion": ubicacion,
    }


def generar_resumen_sensores(lista_sensores_limpios, umbral_temperatura):
    umbral = float(umbral_temperatura)
    if not math.isfinite(umbral):
        raise ValueError("El umbral debe ser un número finito.")

    sensores = list(lista_sensores_limpios)

    lista_sensores_alerta = []
    for sensor in sensores:
        if float(sensor["temperatura"]) > umbral:
            lista_sensores_alerta.append(sensor["sensor_id"])

    total_temp = 0
    for s in sensores:
        total_temp += float(s["temperatura"])

    if len(sensores) > 0:
        promedio_temperatura = total_temp / len(sensores)
    else:
        promedio_temperatura = 0.0

    return lista_sensores_alerta, promedio_temperatura


def main():
    registros_raw = [
        {"sensor_id": " SENSOR-001 ", "temperatura": "24.5C", "ubicacion": "Planta Norte"},
        {"sensor_id": "SENSOR-002", "temperatura": "31 °C", "ubicacion": "Planta Sur"},
        {"sensor_id": "SENSOR-003", "temperatura": "27,2C"},
    ]

    sensores_limpios = []
    for registro in registros_raw:
        sensores_limpios.append(limpiar_registro_sensor(registro))

    alertas, promedio = generar_resumen_sensores(sensores_limpios, 30)

    print("Reporte de sensores EcoTech Solutions")
    print(f"Sensores procesados: {len(sensores_limpios)}")
    print(f"Temperatura promedio: {promedio:.2f} °C")

    if len(alertas) > 0:
        print(f"Sensores sobre el umbral: {', '.join(alertas)}")
    else:
        print("Sensores sobre el umbral: ninguno")


if __name__ == "__main__":
    main()