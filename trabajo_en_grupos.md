# 👥 Unidad 11 — Trabajo en grupos (3 sesiones)

La clase se divide en **3 grupos**, uno por sala/sesión. Cada grupo elige **una** de estas dos opciones:

| Opción | Qué hacen |
|--------|-----------|
| **A. Ejercicio avanzado asignado** | Resuelven el ejercicio que le toca al grupo (tabla de abajo). |
| **B. Mini proyecto propio** | Inventan un mini proyecto que use **librerías de terceros**. |

Las dos opciones tienen los **mismos requisitos de entrega** (ver más abajo).

---

## 🅰️ Opción A — Ejercicio asignado por grupo

| Grupo | Ejercicio | Librerías | Enunciado |
|-------|-----------|-----------|-----------|
| **Grupo 1** | Conversor de Divisas (cotización en vivo) | `requests`, `tabulate` | [`avanzados/ejercicio_1.py`](avanzados/ejercicio_1.py) |
| **Grupo 2** | Generador de Códigos QR | `qrcode`, `pillow` | [`avanzados/ejercicio_2.py`](avanzados/ejercicio_2.py) |
| **Grupo 3** | Extractor de Titulares (web scraping) | `requests`, `beautifulsoup4` | [`avanzados/ejercicio_3.py`](avanzados/ejercicio_3.py) |

> 💡 Como modelo de referencia tienen el **Ejercicio 5 resuelto** en [`avanzados/ejercicio_5_generador_datos/`](avanzados/ejercicio_5_generador_datos/) (`faker` + `rich`). Miren cómo está dividido en módulos.

---

## 🅱️ Opción B — Mini proyecto propio

El grupo propone su propio programa de consola. Condiciones:

- Usa **al menos 2 librerías de terceros** instaladas con `pip`.
- Tiene **al menos 1 módulo propio** además de `main.py` (ej: `logica.py`, `vista.py`).
- Antes de arrancar, **se lo cuentan al profesor** en 2 o 3 líneas (qué hace y qué librerías usa).

Ideas para inspirarse:

| Idea | Librerías sugeridas |
|------|---------------------|
| Clima de una ciudad por consola | `requests`, `rich` |
| Estadísticas de un CSV con gráfico | `pandas`, `matplotlib` |
| Simulador de datos con análisis | `numpy`, `faker` |
| Lista de tareas con tabla de colores | `rich`, `tabulate` |
| Generador de contraseñas seguras + QR | `qrcode`, `pillow` |
| Juego de preguntas con API pública | `requests`, `colorama` |

> 🔎 Las librerías se buscan en [PyPI](https://pypi.org). Siempre lean la documentación oficial antes de usarlas.

---

## ✅ Requisitos de entrega (A y B)

- [ ] Carpeta propia del proyecto (ej: `conversor_divisas/`).
- [ ] Entorno virtual creado (`.venv/`) — **no se entrega ni se sube a Git**.
- [ ] `requirements.txt` generado con `pip freeze`.
- [ ] `README.md` que explique qué hace, cómo instalarlo y cómo ejecutarlo.
- [ ] `.gitignore` con `.venv/` y `__pycache__/`.
- [ ] Manejo de errores con `try / except` (entradas inválidas, sin conexión, archivos, etc.).
- [ ] Docstrings en todas las funciones (PEP 257).
- [ ] Anotación de tipos en parámetros y retornos.
- [ ] Código que respete PEP 8 (nombres en `snake_case`, 4 espacios, imports arriba).
- [ ] Proyecto subido a un **repositorio PÚBLICO en GitHub** (si es privado no se puede corregir).
- [ ] En el `README.md`, una sección **Integrantes** con nombre y apellido de todos los que participaron.

> ⚠️ **Importante:** este trabajo cuenta para la **nota de concepto**, que se aplica **solamente al segundo parcial** y puede **subir o bajar** esa nota. Solo se tiene en cuenta a quienes figuren en la sección **Integrantes** del `README.md`. Si tu nombre no está, no se te computa.

### 🙋 Si no estuviste en la clase

Quienes no estuvieron presentes también tienen que hacer el trabajo: pueden **armar su propio grupo de hasta 5 personas**, elegir la Opción A o la B y cumplir los mismos requisitos y la misma fecha de entrega.

### 📤 Cómo y cuándo se entrega

- Se entrega el **link al repositorio público** junto con los **nombres de los integrantes** del grupo.
- Si no llegan a terminarlo en la clase de hoy, lo completan durante la semana.
- 📅 **Fecha límite: domingo 01 de noviembre.**
- 📅 **Segunda Fecha límite: domingo 08 de noviembre.**
- 

---

## 📝 Memo resumen (teoría Unidad 11)

### 1. Entorno virtual (`venv`)

**¿Qué es?** Una "caja" aislada con su propio Python y sus propias librerías, una por proyecto.

**¿Por qué?** Si el proyecto A necesita `requests==2.25` y el B `requests==2.31`, sin entorno virtual chocan. Con `venv` cada uno tiene lo suyo y no se ensucia el Python del sistema.

```bash
# Crear (dentro de la carpeta del proyecto)
python -m venv .venv

# Activar
source .venv/bin/activate      # Linux / Mac
.venv\Scripts\activate         # Windows

# Se ve (.venv) al inicio de la terminal → está activo

# Desactivar
deactivate
```

> ⚠️ **Windows / PowerShell:** si no deja activar el entorno:
> `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`

### 2. Instalar librerías de terceros (`pip`)

`pip` es el gestor de paquetes de Python: descarga librerías desde [PyPI](https://pypi.org).

```bash
pip install requests              # instalar
pip install --upgrade requests    # actualizar
pip uninstall requests            # desinstalar
pip show requests                 # ver versión e info
pip list                          # ver todo lo instalado
```

**Congelar y reinstalar dependencias:**

```bash
pip freeze > requirements.txt     # guardar lo instalado (con versiones)
pip install -r requirements.txt   # reinstalar todo en otra máquina
```

> 💡 Regla de oro: **primero activo el entorno, después instalo**. Si instalan sin activar, la librería va al Python global.

### 3. Estructura de un proyecto y para qué sirve cada archivo

```text
mi_proyecto/
├── .venv/              ← entorno virtual (NO se sube a Git)
├── .gitignore          ← qué archivos ignora Git
├── README.md           ← qué hace y cómo se usa
├── requirements.txt    ← dependencias congeladas
├── main.py             ← punto de entrada
└── logica.py           ← módulo propio
```

| Archivo | Para qué sirve | ¿Se sube a Git? |
|---------|----------------|:---------------:|
| `.venv/` | Contiene el Python y las librerías instaladas del proyecto. Se puede recrear en cualquier momento con `requirements.txt`. Pesa mucho y depende de cada máquina. | ❌ |
| `.gitignore` | Lista lo que Git no debe versionar (`.venv/`, `__pycache__/`, archivos generados). | ✅ |
| `README.md` | La "carta de presentación": qué hace el proyecto, requisitos, cómo instalar y cómo ejecutar. Es lo primero que ve un compañero, un profesor o un futuro empleador. | ✅ |
| `requirements.txt` | La "receta" de dependencias con sus versiones. Permite que otro reproduzca exactamente el mismo entorno. | ✅ |
| `main.py` | Punto de entrada: lo que se ejecuta con `python main.py`. Coordina el programa y maneja los errores del usuario. | ✅ |
| Módulos propios (`*.py`) | Separan responsabilidades (ej: `generador.py` genera datos, `vista.py` los muestra). Código más ordenado y reutilizable. | ✅ |
| `__pycache__/` | Archivos compilados que Python genera solo. | ❌ |

### 4. Buenas prácticas de código

- **Zen de Python:** legible antes que ingenioso.
- **PEP 8:** 4 espacios, líneas cortas, nombres descriptivos en `snake_case`, imports arriba y ordenados.
- **Docstrings (PEP 257):** cada función explica qué hace, qué recibe y qué devuelve.
- **Anotación de tipos:** `def convertir(monto: float, cotizacion: float) -> float:`
- **Manejo de errores:** `try / except` con excepciones específicas (`ValueError`, `requests.RequestException`, etc.), nunca un `except:` vacío.

### 5. Flujo de trabajo recomendado

```bash
mkdir mi_proyecto && cd mi_proyecto
python -m venv .venv
source .venv/bin/activate          # o .venv\Scripts\activate en Windows
pip install <libreria_1> <libreria_2>
pip freeze > requirements.txt
# escribir main.py, módulos propios, README.md y .gitignore
python main.py
git init && git add . && git commit -m "feat: primera versión"
```
