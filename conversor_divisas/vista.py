"""Módulo encargado de la interacción con el usuario por consola."""

from datetime import datetime

from tabulate import tabulate

OPCIONES_MENU: dict[str, str] = {
    "1": "Convertir pesos (ARS) a dólares (USD)",
    "2": "Convertir dólares (USD) a pesos (ARS)",
    "3": "Actualizar cotizaciones",
    "0": "Salir",
}


def pedir_opcion() -> str:
    """Muestra el menú y pide una opción hasta que sea válida.

    Returns:
        La clave de la opción elegida (ej: "1").
    """
    print("\n¿Qué querés hacer?")
    for clave, descripcion in OPCIONES_MENU.items():
        print(f"  {clave}. {descripcion}")

    while True:
        opcion = input("Opción: ").strip()
        if opcion in OPCIONES_MENU:
            return opcion
        print("⚠️  Opción inválida. Elegí uno de los números del menú.")


def pedir_monto(moneda: str) -> float:
    """Pide al usuario un monto hasta que ingrese uno válido.

    Acepta coma o punto como separador decimal.

    Args:
        moneda: Texto de la moneda a mostrar en el pedido (ej: "ARS").

    Returns:
        Monto positivo ingresado por el usuario.
    """
    while True:
        texto = input(f"Ingresá un monto en {moneda}: ").strip()
        try:
            monto = float(texto.replace(",", "."))
        except ValueError:
            print("⚠️  Eso no es un número válido. Probá de nuevo.\n")
            continue

        if monto <= 0:
            print("⚠️  El monto debe ser mayor a cero.\n")
            continue
        return monto


def formatear_numero(valor: float) -> str:
    """Formatea un número al estilo argentino (ej: 1.234,56).

    Args:
        valor: Número a formatear.

    Returns:
        Texto con punto de miles y coma decimal.
    """
    texto = f"{valor:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def formatear_pesos(valor: float | None) -> str:
    """Formatea un número como pesos (ej: $ 1.234,56).

    Args:
        valor: Número a formatear, o None si no hay dato.

    Returns:
        Texto con el formato de moneda, o "-" si no hay dato.
    """
    return "-" if valor is None else f"$ {formatear_numero(valor)}"


def formatear_dolares(valor: float | None) -> str:
    """Formatea un número como dólares (ej: US$ 1.234,56).

    Args:
        valor: Número a formatear, o None si no hay dato.

    Returns:
        Texto con el formato de moneda, o "-" si no hay dato.
    """
    return "-" if valor is None else f"US$ {formatear_numero(valor)}"


def formatear_fecha(fecha: datetime | None) -> str:
    """Formatea la fecha de actualización (ej: 03/11 15:00).

    Args:
        fecha: Fecha a formatear, o None si no hay dato.

    Returns:
        Texto con día, mes y hora, o "-" si no hay dato.
    """
    return "-" if fecha is None else fecha.strftime("%d/%m %H:%M")


def mostrar_tabla(resultados: list[dict], monto: float,
                  a_dolares: bool) -> None:
    """Imprime los resultados de la conversión en una tabla.

    Args:
        resultados: Cotizaciones con la clave "total" ya calculada.
        monto: Monto original ingresado por el usuario.
        a_dolares: True si se convirtió ARS → USD, False si USD → ARS.
    """
    if a_dolares:
        titulo = f"{formatear_pesos(monto)} en dólares (precio de venta)"
        formatear_total = formatear_dolares
    else:
        titulo = f"{formatear_dolares(monto)} en pesos (precio de compra)"
        formatear_total = formatear_pesos

    filas = [
        [
            fila["nombre"],
            formatear_pesos(fila["compra"]),
            formatear_pesos(fila["venta"]),
            formatear_total(fila["total"]),
            formatear_fecha(fila["fecha"]),
        ]
        for fila in resultados
    ]
    encabezados = ["Dólar", "Compra", "Venta", "Total", "Actualizado"]

    print(f"\n{titulo}:\n")
    print(tabulate(filas, headers=encabezados, tablefmt="rounded_outline",
                   colalign=("left", "right", "right", "right", "center")))


def mostrar_mensaje(mensaje: str) -> None:
    """Muestra un mensaje informativo.

    Args:
        mensaje: Texto a mostrar.
    """
    print(f"\n✅ {mensaje}")


def mostrar_error(mensaje: str) -> None:
    """Muestra un mensaje de error de forma uniforme.

    Args:
        mensaje: Texto del error a mostrar.
    """
    print(f"\n❌ {mensaje}")
