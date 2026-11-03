# 💱 Conversor de Divisas (cotización en vivo)

Programa de consola que convierte un monto en **pesos argentinos (ARS)** a
**dólar oficial** y **dólar blue**, usando la cotización actual obtenida de la
API pública [DolarApi](https://dolarapi.com/v1/dolares).

La conversión usa el precio de **venta** (el precio al que se compran dólares
con pesos):

```text
total_usd = monto_ars / venta
```

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
├── main.py            ← punto de entrada
├── cotizaciones.py    ← consulta a la API y cálculos
└── vista.py           ← entrada del usuario y tabla por consola
```

## ⚙️ Instalación

Requiere **Python 3.10 o superior**.

```bash
# 1. Clonar el repositorio y entrar a la carpeta
git clone <URL_DEL_REPOSITORIO>
cd conversor_divisas

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

Ejemplo de salida:

```text
💱 Conversor de Divisas — Cotización en vivo

Ingresá un monto en pesos (ARS): 100000

Conversión de $ 100.000,00:

╭─────────┬────────────┬────────────┬────────────────────╮
│ Dólar   │     Compra │      Venta │   Total convertido │
├─────────┼────────────┼────────────┼────────────────────┤
│ Oficial │ $ 1.520,00 │ $ 1.570,00 │          US$ 63,69 │
├─────────┼────────────┼────────────┼────────────────────┤
│ Blue    │ $ 1.550,00 │ $ 1.570,00 │          US$ 63,69 │
╰─────────┴────────────┴────────────┴────────────────────╯
```

*(los valores cambian según la cotización del día)*

## 🛡️ Manejo de errores

El programa contempla con `try / except`:

- Monto no numérico, negativo o cero (lo vuelve a pedir).
- Sin conexión a internet o API que no responde.
- Tiempo de espera agotado.
- Errores HTTP de la API (404, 500, etc.).
- Respuesta que no es un JSON válido o con datos faltantes.
- Cancelación con `Ctrl + C`.

## 👥 Integrantes

- Nombre Apellido
- Nombre Apellido
- Nombre Apellido
