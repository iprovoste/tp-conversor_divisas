"""Módulo encargado de la interacción con el usuario por consola."""

from tabulate import tabulate


def pedir_monto() -> float:
    """Pide al usuario un monto en pesos hasta que ingrese uno válido.

    Acepta coma o punto como separador decimal.

    Returns:
        Monto positivo ingresado por el usuario.
    """
    while True:
        texto = input("Ingresá un monto en pesos (ARS): ").strip()
        try:
            monto = float(texto.replace(",", "."))
        except ValueError:
            print("⚠️  Eso no es un número válido. Probá de nuevo.\n")
            continue

        if monto <= 0:
            print("⚠️  El monto debe ser mayor a cero.\n")
            continue
        return monto


def formatear_pesos(valor: float) -> str:
    """Formatea un número como pesos argentinos (ej: $ 1.234,56).

    Args:
        valor: Número a formatear.

    Returns:
        Texto con el formato de moneda argentina.
    """
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"$ {texto}"


def formatear_dolares(valor: float) -> str:
    """Formatea un número como dólares (ej: US$ 1.234,56).

    Args:
        valor: Número a formatear.

    Returns:
        Texto con el formato de moneda en dólares.
    """
    return "US" + formatear_pesos(valor)


def mostrar_tabla(resultados: list[dict], monto_ars: float) -> None:
    """Imprime los resultados de la conversión en una tabla.

    Args:
        resultados: Lista con nombre, compra, venta y total_usd.
        monto_ars: Monto original en pesos, para mostrarlo como título.
    """
    filas = [
        [
            fila["nombre"],
            formatear_pesos(fila["compra"]),
            formatear_pesos(fila["venta"]),
            formatear_dolares(fila["total_usd"]),
        ]
        for fila in resultados
    ]
    encabezados = ["Dólar", "Compra", "Venta", "Total convertido"]

    print(f"\nConversión de {formatear_pesos(monto_ars)}:\n")
    print(tabulate(filas, headers=encabezados, tablefmt="rounded_grid",
                   colalign=("left", "right", "right", "right")))


def mostrar_error(mensaje: str) -> None:
    """Muestra un mensaje de error de forma uniforme.

    Args:
        mensaje: Texto del error a mostrar.
    """
    print(f"\n❌ {mensaje}")
