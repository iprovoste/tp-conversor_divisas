# 💱 Conversor de Divisas (cotización en vivo)

Programa de consola que convierte montos entre **pesos argentinos (ARS)** y
**dólares (USD)** usando las cotizaciones del día, obtenidas de la API
pública [DolarApi](https://dolarapi.com/v1/dolares).

## ✨ Funcionalidades

- **Menú interactivo**: se pueden hacer varias conversiones sin volver a
  ejecutar el programa.
- **Conversión en los dos sentidos**:
  - **ARS → USD** con el precio de **venta** (al que se compran dólares con
    pesos): `total_usd = monto_ars / venta`
  - **USD → ARS** con el precio de **compra** (el que pagan cuando vendés
    dólares): `total_ars = monto_usd * compra`
- **Todos los tipos de dólar** que informa la API: Oficial, Blue, Bolsa (MEP),
  Contado con liquidación, Mayorista, Cripto y Tarjeta.
- **Fecha y hora de actualización** de cada cotización, en la hora local.
- Opción para **actualizar las cotizaciones** sin salir del programa.

## 📦 Librerías de terceros

| Librería   | Para qué se usa                               |
|------------|-----------------------------------------------|
| `requests` | Hacer la petición HTTP a la API.              |
| `tabulate` | Mostrar los resultados en una tabla prolija.  |

## 🗂️ Estructura

```text
conversor_divisas/
├── .gitignore         ← ignora .venv/ y __pycache__/
├── README.md          ← este archivo
├── requirements.txt   ← dependencias congeladas
├── main.py            ← punto de entrada y menú principal
├── cotizaciones.py    ← consulta a la API, limpieza de datos y cálculos
└── vista.py           ← menú, entrada del usuario y tablas por consola
```

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

✅ Se cargaron 7 cotizaciones.

¿Qué querés hacer?
  1. Convertir pesos (ARS) a dólares (USD)
  2. Convertir dólares (USD) a pesos (ARS)
  3. Actualizar cotizaciones
  0. Salir
Opción: 1
Ingresá un monto en pesos (ARS): 100000

$ 100.000,00 en dólares (precio de venta):

╭─────────────────────────┬────────────┬────────────┬───────────┬───────────────╮
│ Dólar                   │     Compra │      Venta │     Total │  Actualizado  │
├─────────────────────────┼────────────┼────────────┼───────────┼───────────────┤
│ Oficial                 │ $ 1.520,00 │ $ 1.570,00 │ US$ 63,69 │  03/11 15:00  │
│ Blue                    │ $ 1.550,00 │ $ 1.570,00 │ US$ 63,69 │  03/11 17:57  │
│ Bolsa                   │ $ 1.575,30 │ $ 1.581,10 │ US$ 63,25 │  03/11 17:57  │
│ Contado con liquidación │ $ 1.667,20 │ $ 1.668,80 │ US$ 59,92 │  03/11 17:57  │
│ Mayorista               │ $ 1.542,00 │ $ 1.551,00 │ US$ 64,47 │  03/11 12:46  │
│ Cripto                  │ $ 1.654,13 │ $ 1.659,45 │ US$ 60,26 │  03/11 17:57  │
│ Tarjeta                 │ $ 1.976,00 │ $ 2.041,00 │ US$ 49,00 │  03/11 15:00  │
╰─────────────────────────┴────────────┴────────────┴───────────┴───────────────╯
```

*(los valores cambian según la cotización del día)*

## 🛡️ Manejo de errores

El programa contempla con `try / except`:

- Opción de menú inválida (la vuelve a pedir).
- Monto no numérico, negativo o cero (lo vuelve a pedir).
- Sin conexión a internet o API que no responde.
- Tiempo de espera agotado.
- Errores HTTP de la API (404, 500, etc.).
- Respuesta que no es un JSON válido, o cotizaciones con datos faltantes o
  no numéricos (se descartan o se muestran como `-`).
- Falla al actualizar: se avisa y se siguen usando las cotizaciones anteriores.
- Cancelación con `Ctrl + C`.

## 👥 Integrantes

- Oscar Israel Provoste Sanchez
