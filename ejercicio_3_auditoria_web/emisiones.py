import math


def calcular_emisiones_carbono(consumo_kwh, factor_emision=0.4):
    consumo = float(consumo_kwh)
    factor = float(factor_emision)
    if not math.isfinite(consumo) or not math.isfinite(factor):
        raise ValueError("El consumo y el factor deben ser números finitos.")
    if consumo < 0:
        raise ValueError("El consumo no puede ser negativo.")
    if factor < 0:
        raise ValueError("El factor de emisión no puede ser negativo.")
    return consumo * factor


def obtener_metricas_consumo(registros):
    consumo_por_planta = {}
    emisiones_por_planta = {}

    for registro in registros:
        planta = str(registro["planta"]).strip()
        if not planta:
            raise ValueError("Cada registro debe identificar una planta.")
        consumo = float(registro["consumo_kwh"])
        emisiones = calcular_emisiones_carbono(consumo)
        consumo_por_planta[planta] = consumo_por_planta.get(planta, 0.0) + consumo
        emisiones_por_planta[planta] = emisiones_por_planta.get(planta, 0.0) + emisiones

    total_emisiones = sum(emisiones_por_planta.values())
    planta_mayor_consumo = (
        max(consumo_por_planta, key=consumo_por_planta.get)
        if consumo_por_planta
        else None
    )
    consumo_maximo_kwh = (
        consumo_por_planta[planta_mayor_consumo]
        if planta_mayor_consumo is not None
        else 0.0
    )

    return {
        "total_emisiones": total_emisiones,
        "planta_mayor_consumo": planta_mayor_consumo,
        "consumo_maximo_kwh": consumo_maximo_kwh,
        "consumo_por_planta": consumo_por_planta,
        "emisiones_por_planta": emisiones_por_planta,
        "detalle_plantas": [
            {
                "planta": planta,
                "consumo_kwh": consumo,
                "emisiones": emisiones_por_planta[planta],
            }
            for planta, consumo in consumo_por_planta.items()
        ],
    }
