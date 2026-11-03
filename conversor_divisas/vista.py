"""Módulo encargado de la interacción con el usuario por consola."""

from datetime import datetime

from tabulate import tabulate

OPCIONES_MENU: dict[str, str] = {
    "1": "Pesos (ARS) → dólares (todos los tipos)",
    "2": "Dólares → pesos (ARS) (todos los tipos)",
    "3": "Pesos (ARS) → otras monedas",
    "4": "Otra moneda → pesos (ARS)",
    "5": "Ver historial de conversiones",
    "6": "Actualizar cotizaciones",
    "0": "Salir",
}
SIMBOLOS: dict[str, str] = {
    "ARS": "$",
    "USD": "US$",
    "EUR": "€",
    "BRL": "R$",
    "CLP": "CLP$",
    "UYU": "$U",
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


def pedir_moneda(monedas: list[dict]) -> str:
    """Muestra las monedas disponibles y pide un código válido.

    Args:
        monedas: Cotizaciones normalizadas de las monedas.

    Returns:
        Código ISO de la moneda elegida, en mayúsculas (ej: "EUR").
    """
    codigos = [moneda["moneda"] for moneda in monedas]
    print("\nMonedas disponibles:")
    for moneda in monedas:
        print(f"  {moneda['moneda']} → {moneda['nombre']}")

    while True:
        codigo = input("Código de la moneda: ").strip().upper()
        if codigo in codigos:
            return codigo
        print(f"⚠️  Código inválido. Opciones: {', '.join(codigos)}.")


def formatear_numero(valor: float) -> str:
    """Formatea un número al estilo argentino (ej: 1.234,56).

    Args:
        valor: Número a formatear.

    Returns:
        Texto con punto de miles y coma decimal.
    """
    texto = f"{valor:,.2f}"
    return texto.replace(",", "X").replace(".", ",").replace("X", ".")


def formatear_moneda(valor: float | None, codigo: str) -> str:
    """Formatea un número con el símbolo de su moneda (ej: € 1.234,56).

    Args:
        valor: Número a formatear, o None si no hay dato.
        codigo: Código ISO de la moneda (ej: "EUR").

    Returns:
        Texto con el formato de moneda, o "-" si no hay dato.
    """
    if valor is None:
        return "-"
    return f"{SIMBOLOS.get(codigo, codigo)} {formatear_numero(valor)}"


def formatear_porcentaje(valor: float | None) -> str:
    """Formatea un porcentaje con signo (ej: +6,30 %).

    Args:
        valor: Porcentaje a formatear, o None si no hay dato.

    Returns:
        Texto con signo y símbolo de porcentaje, o "-" si no hay dato.
    """
    if valor is None:
        return "-"
    signo = "+" if valor >= 0 else "-"
    return f"{signo}{formatear_numero(abs(valor))} %"


def formatear_fecha(fecha: datetime | None) -> str:
    """Formatea la fecha de actualización (ej: 03/11 15:00).

    Args:
        fecha: Fecha a formatear, o None si no hay dato.

    Returns:
        Texto con día, mes y hora, o "-" si no hay dato.
    """
    return "-" if fecha is None else fecha.strftime("%d/%m %H:%M")


def mostrar_tabla(
    resultados: list[dict],
    titulo: str,
    desde_pesos: bool,
    mostrar_brecha: bool = False,
) -> None:
    """Imprime los resultados de una conversión en una tabla.

    Args:
        resultados: Cotizaciones con la clave "total" ya calculada.
        titulo: Texto a mostrar arriba de la tabla.
        desde_pesos: True si se convirtió ARS → moneda (el total va en la
            moneda de cada fila), False si moneda → ARS (total en pesos).
        mostrar_brecha: True para agregar la columna de brecha contra el
            dólar oficial.
    """
    encabezados = ["Cotización", "Compra", "Venta"]
    alineacion = ["left", "right", "right"]
    if mostrar_brecha:
        encabezados.append("Brecha")
        alineacion.append("right")
    encabezados += ["Total", "Actualizado"]
    alineacion += ["right", "center"]

    filas = []
    for fila in resultados:
        moneda_total = fila["moneda"] if desde_pesos else "ARS"
        datos = [
            fila["nombre"],
            formatear_moneda(fila["compra"], "ARS"),
            formatear_moneda(fila["venta"], "ARS"),
        ]
        if mostrar_brecha:
            datos.append(formatear_porcentaje(fila.get("brecha")))
        datos += [
            formatear_moneda(fila["total"], moneda_total),
            formatear_fecha(fila["fecha"]),
        ]
        filas.append(datos)

    print(f"\n{titulo}:\n")
    print(tabulate(filas, headers=encabezados, tablefmt="rounded_outline",
                   colalign=alineacion))


def formatear_valor_guardado(texto: str, codigo: str) -> str:
    """Formatea un monto leído del historial (que viene como texto).

    Args:
        texto: Valor tal como está en el archivo.
        codigo: Código ISO de la moneda del valor.

    Returns:
        El valor formateado, "-" si está vacío o el texto original si no
        es un número.
    """
    if not texto:
        return "-"
    try:
        return formatear_moneda(float(texto), codigo)
    except ValueError:
        return texto


def mostrar_historial(registros: list[dict]) -> None:
    """Imprime las últimas conversiones guardadas en una tabla.

    Args:
        registros: Filas leídas del historial CSV.
    """
    if not registros:
        print("\nTodavía no hay conversiones en el historial.")
        return

    filas = [
        [
            registro.get("fecha", "-"),
            formatear_valor_guardado(registro.get("monto", ""),
                                     registro.get("origen", "")),
            registro.get("cotizacion", "-"),
            formatear_valor_guardado(registro.get("resultado", ""),
                                     registro.get("destino", "")),
        ]
        for registro in registros
    ]
    encabezados = ["Fecha", "Monto", "Cotización", "Resultado"]

    print(f"\nÚltimas {len(registros)} líneas del historial:\n")
    print(tabulate(filas, headers=encabezados, tablefmt="rounded_outline",
                   colalign=("left", "right", "left", "right")))


def mostrar_mensaje(mensaje: str) -> None:
    """Muestra un mensaje informativo.

    Args:
        mensaje: Texto a mostrar.
    """
    print(f"\n✅ {mensaje}")


def mostrar_advertencia(mensaje: str) -> None:
    """Muestra una advertencia que no detiene el programa.

    Args:
        mensaje: Texto a mostrar.
    """
    print(f"\n⚠️  {mensaje}")


def mostrar_error(mensaje: str) -> None:
    """Muestra un mensaje de error de forma uniforme.

    Args:
        mensaje: Texto del error a mostrar.
    """
    print(f"\n❌ {mensaje}")
