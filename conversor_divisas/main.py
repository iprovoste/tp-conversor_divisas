"""Punto de entrada del Conversor de Divisas (ARS ⇄ USD y otras monedas)."""

from cotizaciones import (
    ErrorCotizacion,
    buscar_moneda,
    calcular_conversiones,
    cargar_todo,
)
from historial import (
    ARCHIVO_CSV,
    ARCHIVO_TXT,
    ErrorHistorial,
    guardar_conversion,
    leer_historial,
)
from vista import (
    formatear_moneda,
    mostrar_advertencia,
    mostrar_error,
    mostrar_historial,
    mostrar_mensaje,
    mostrar_tabla,
    pedir_moneda,
    pedir_monto,
    pedir_opcion,
)


def convertir(
    cotizaciones: list[dict],
    monto: float,
    desde_pesos: bool,
    titulo: str,
    mostrar_brecha: bool = False,
) -> None:
    """Hace la conversión, muestra la tabla y la guarda en el historial.

    Si no se puede guardar el historial, avisa pero no corta el programa.

    Args:
        cotizaciones: Cotizaciones a usar en la conversión.
        monto: Monto ingresado por el usuario.
        desde_pesos: True para ARS → moneda, False para moneda → ARS.
        titulo: Texto a mostrar arriba de la tabla.
        mostrar_brecha: True para agregar la columna de brecha.
    """
    resultados = calcular_conversiones(cotizaciones, monto, desde_pesos)
    mostrar_tabla(resultados, titulo, desde_pesos, mostrar_brecha)
    try:
        guardar_conversion(resultados, monto, desde_pesos)
    except ErrorHistorial as error:
        mostrar_advertencia(str(error))


def atender_opcion(opcion: str, datos: dict[str, list[dict]]) -> None:
    """Ejecuta la opción de conversión o de historial elegida.

    Args:
        opcion: Clave de la opción del menú ("1" a "5").
        datos: Diccionario con las listas "dolares" y "monedas".

    Raises:
        ErrorCotizacion: Si la moneda elegida no tiene cotización.
    """
    if opcion == "1":
        monto = pedir_monto("pesos (ARS)")
        titulo = f"{formatear_moneda(monto, 'ARS')} en dólares (venta)"
        convertir(datos["dolares"], monto, True, titulo, mostrar_brecha=True)
    elif opcion == "2":
        monto = pedir_monto("dólares (USD)")
        titulo = f"{formatear_moneda(monto, 'USD')} en pesos (compra)"
        convertir(datos["dolares"], monto, False, titulo, mostrar_brecha=True)
    elif opcion == "3":
        monto = pedir_monto("pesos (ARS)")
        titulo = f"{formatear_moneda(monto, 'ARS')} en otras monedas (venta)"
        convertir(datos["monedas"], monto, True, titulo)
    elif opcion == "4":
        codigo = pedir_moneda(datos["monedas"])
        moneda = buscar_moneda(datos["monedas"], codigo)
        monto = pedir_monto(f"{moneda['nombre']} ({codigo})")
        titulo = f"{formatear_moneda(monto, codigo)} en pesos (compra)"
        convertir([moneda], monto, False, titulo)
    elif opcion == "5":
        try:
            mostrar_historial(leer_historial())
            print(f"\nHistorial completo en: {ARCHIVO_CSV.name} "
                  f"y {ARCHIVO_TXT.name}")
        except ErrorHistorial as error:
            mostrar_error(str(error))


def main() -> None:
    """Coordina el programa: carga cotizaciones y atiende el menú."""
    print("💱 Conversor de Divisas — Cotización en vivo")
    try:
        datos = cargar_todo()
        mostrar_mensaje(
            f"Se cargaron {len(datos['dolares'])} tipos de dólar y "
            f"{len(datos['monedas'])} monedas."
        )

        while True:
            opcion = pedir_opcion()
            if opcion == "0":
                print("\n¡Hasta luego!")
                break
            if opcion == "6":
                try:
                    datos = cargar_todo()
                    mostrar_mensaje("Cotizaciones actualizadas.")
                except ErrorCotizacion as error:
                    mostrar_error(f"{error} Se siguen usando las anteriores.")
                continue
            try:
                atender_opcion(opcion, datos)
            except ErrorCotizacion as error:
                mostrar_error(str(error))
    except ErrorCotizacion as error:
        mostrar_error(str(error))
    except (KeyboardInterrupt, EOFError):
        print("\n\nPrograma cancelado por el usuario.")


if __name__ == "__main__":
    main()
