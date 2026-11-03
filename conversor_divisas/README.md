# 💱 Conversor de Divisas (cotización en vivo)

Programa de consola que convierte montos entre **pesos argentinos (ARS)**,
**dólares (USD)** y otras monedas usando las cotizaciones del día, obtenidas
de la API pública [DolarApi](https://dolarapi.com).

## ✨ Funcionalidades

- **Menú interactivo**: se pueden hacer varias conversiones sin volver a
  ejecutar el programa.
- **Conversión en los dos sentidos**:
  - **ARS → moneda** con el precio de **venta** (al que se compra la moneda
    con pesos): `total = monto_ars / venta`
  - **Moneda → ARS** con el precio de **compra** (el que pagan cuando vendés
    la moneda): `total_ars = monto * compra`
- **Todos los tipos de dólar** que informa la API: Oficial, Blue, Bolsa (MEP),
  Contado con liquidación, Mayorista, Cripto y Tarjeta.
- **Brecha cambiaria**: porcentaje de diferencia del precio de venta de cada
  dólar contra el oficial: `brecha = (venta / venta_oficial - 1) * 100`
- **Otras monedas**: Euro (EUR), Real brasileño (BRL), Peso chileno (CLP) y
  Peso uruguayo (UYU).
- **Historial de conversiones**: cada conversión se guarda en dos archivos
  junto al programa, y se puede consultar desde el menú:
  - `historial.csv`: una fila por resultado, para abrir con Excel.
  - `historial.txt`: un bloque legible por conversión.
- **Fecha y hora de actualización** de cada cotización, en la hora local.
- Opción para **actualizar las cotizaciones** sin salir del programa.

## 📋 Menú

| Opción | Qué hace |
|:------:|----------|
| 1 | Pesos (ARS) → dólares, con todos los tipos y la brecha |
| 2 | Dólares → pesos (ARS), con todos los tipos y la brecha |
| 3 | Pesos (ARS) → todas las otras monedas |
| 4 | Una moneda a elección (USD, EUR, BRL, CLP, UYU) → pesos (ARS) |
| 5 | Ver las últimas 20 líneas del historial |
| 6 | Actualizar cotizaciones |
| 0 | Salir |

## 📦 Librerías de terceros

| Librería   | Para qué se usa                               |
|------------|-----------------------------------------------|
| `requests` | Hacer la petición HTTP a la API.              |
| `tabulate` | Mostrar los resultados en una tabla prolija.  |

## 🗂️ Estructura

```text
conversor_divisas/
├── .gitignore         ← ignora .venv/, __pycache__/ y el historial
├── README.md          ← este archivo
├── requirements.txt   ← dependencias congeladas
├── main.py            ← punto de entrada y menú principal
├── cotizaciones.py    ← consulta a la API, limpieza de datos y cálculos
├── historial.py       ← guarda y lee el historial (CSV y TXT)
└── vista.py           ← menú, entrada del usuario y tablas por consola
```

Los archivos `historial.csv` e `historial.txt` se crean solos con la primera
conversión y no se suben a Git.

## ⚙️ Instalación

Requiere **Python 3.10 o superior**.

```bash
# 1. Clonar el repositorio y entrar a la carpeta del proyecto
git clone https://github.com/iprovoste/tp-conversor_divisas.git
cd tp-conversor_divisas/conversor_divisas

# 2. Crear el entorno virtual
python -m venv .venv

# 3. Activarlo
source .venv/bin/activate      # Linux / Mac
.venv\Scripts\activate         # Windows

# 4. Instalar las dependencias
pip install -r requirements.txt
```

> ⚠️ En Windows/PowerShell, si no deja activar el entorno:
> `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

## ▶️ Ejecución

```bash
python main.py
```

Ejemplo de uso:

```text
💱 Conversor de Divisas — Cotización en vivo

✅ Se cargaron 7 tipos de dólar y 5 monedas.

¿Qué querés hacer?
  1. Pesos (ARS) → dólares (todos los tipos)
  2. Dólares → pesos (ARS) (todos los tipos)
  3. Pesos (ARS) → otras monedas
  4. Otra moneda → pesos (ARS)
  5. Ver historial de conversiones
  6. Actualizar cotizaciones
  0. Salir
Opción: 1
Ingresá un monto en pesos (ARS): 100000

$ 100.000,00 en dólares (venta):

╭─────────────────────────┬────────────┬────────────┬──────────┬───────────┬───────────────╮
│ Cotización              │     Compra │      Venta │   Brecha │     Total │  Actualizado  │
├─────────────────────────┼────────────┼────────────┼──────────┼───────────┼───────────────┤
│ Oficial                 │ $ 1.520,00 │ $ 1.570,00 │  +0,00 % │ US$ 63,69 │  03/11 15:00  │
│ Blue                    │ $ 1.550,00 │ $ 1.570,00 │  +0,00 % │ US$ 63,69 │  03/11 17:57  │
│ Bolsa                   │ $ 1.575,30 │ $ 1.581,10 │  +0,71 % │ US$ 63,25 │  03/11 17:57  │
│ Contado con liquidación │ $ 1.667,20 │ $ 1.668,80 │  +6,29 % │ US$ 59,92 │  03/11 17:57  │
│ Mayorista               │ $ 1.542,00 │ $ 1.551,00 │  -1,21 % │ US$ 64,47 │  03/11 12:46  │
│ Cripto                  │ $ 1.654,13 │ $ 1.659,45 │  +5,70 % │ US$ 60,26 │  03/11 17:57  │
│ Tarjeta                 │ $ 1.976,00 │ $ 2.041,00 │ +30,00 % │ US$ 49,00 │  03/11 15:00  │
╰─────────────────────────┴────────────┴────────────┴──────────┴───────────┴───────────────╯
```

Ejemplo de `historial.txt`:

```text
[2026-11-03 20:08:33] 100,00 EUR → ARS
    Euro: 172.503,54 ARS (precio 1.725,04)
```

*(los valores cambian según la cotización del día)*

## 🛡️ Manejo de errores

El programa contempla con `try / except`:

- Opción de menú o código de moneda inválido (lo vuelve a pedir).
- Monto no numérico, negativo o cero (lo vuelve a pedir).
- Error al escribir el historial (por ejemplo, el CSV abierto en Excel):
  se avisa y el programa sigue funcionando.
- Historial dañado o ilegible al consultarlo.
- Sin conexión a internet o API que no responde.
- Tiempo de espera agotado.
- Errores HTTP de la API (404, 500, etc.).
- Respuesta que no es un JSON válido, o cotizaciones con datos faltantes o
  no numéricos (se descartan o se muestran como `-`).
- Falla al actualizar: se avisa y se siguen usando las cotizaciones anteriores.
- Cancelación con `Ctrl + C`.

## 👥 Integrantes

- Oscar Israel Provoste Sanchez
