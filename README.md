# DataToolBox
Framework de Ingeniería de Datos en Python para procesos de ETL, limpieza y normalización de bases de datos

# 🛠️ SkrtNull Kit - DataToolBox

**SkrtNull Kit** es una librería de automatización **ETL (Extract, Transform, Load)** desarrollada en Python. Está diseñada para ingenieros de datos que buscan una forma rápida y robusta de normalizar datasets, limpiar estructuras corruptas y preparar datos para análisis o carga en bases de datos SQL.

---

## 🚀 Funcionalidades Principales

- **Limpieza Inteligente de Números:** Motor de extracción selectiva que rescata valores numéricos de cadenas de texto mezcladas (ej: `"ID-102A"` ➔ `102`) sin pérdida de registros.
- **Normalización de Texto:** Estandarización de nombres, correcciones de capitalización y eliminación de espacios redundantes.
- **Motor de Reglas (CalculadoraPlus):** Inyección de lógica aritmética y de fechas dinámica para crear columnas de valor añadido (puntos de fidelidad, turnos horarios, etc.).
- **Validación de Integridad:** Gestión avanzada de nulos y duplicados bajo demanda.
- **Conectividad Multi-formato:** Soporte nativo para CSV, Parquet, JSON y carga directa a bases de datos mediante SQLAlchemy.

## 📦 Instalación

Para utilizar esta herramienta, clona el repositorio e instala las dependencias necesarias:

```
git clone [https://github.com/tu-usuario/DataToolBox.git](https://github.com/tu-usuario/DataToolBox.git)
cd DataToolBox
pip install -r requirements.txt
```

🛠️ Ejemplo de Uso (Pipeline de Datos)
Aquí un ejemplo de cómo integrar el kit en un flujo de procesamiento real (ETL):

```
from kit import DataToolBox
import pandas as pd

# 1. EXTRACCIÓN (Constructor)
print("🚀 Iniciando Pipeline de Pruebas...")
db = DataToolBox("bandeja/prueba1.csv")

# 2. VISUALIZACIÓN INICIAL
print("\n--- Vista Previa Original ---")
db.View(filas=5)

db.CleanStruct()
# 3. TRANSFORMACIÓN: Limpieza de Texto (Nombres a Mayúsculas)
db.CleanText("nombre")

# 5. TRANSFORMACIÓN: Limpieza Numérica y de Nulos
# Eliminamos la fila vacía que tiene el CSV
db.CleanNumb("ID_Cliente") # Convertimos el ID a número puro
db.CleanFalse("ID_Cliente")

# 6. TRANSFORMACIÓN: Extracción de Información (Regex)
# Vamos a intentar rescatar solo correos válidos
db.ExtractInfo("email", patron=r"[\w\.-]+@[\w\.-]+\.\w+")

# 7. CÁLCULOS (CalculadoraPlus)
# Vamos a inventar una columna de 'Puntos' basada en el ID

db.Calculadora({
    "op": "+",           # Sumamos
    "res": "ID_Mas_Diez", # Nueva columna
    "col1": "ID_Cliente",
    "col2": "ID_Cliente"  # Tu código actual requiere que sea otra columna
})

# 5. Exportación final
db.Export("dataset_limpio.csv")
```

## 🛠️ Ejemplos de Configuración (Diccionarios)

Para evitar errores de `KeyError`, asegúrate de usar los nombres exactos de las llaves que el motor espera:

### 1. Cálculos de Tiempo (Función Time)
Ideal para segmentar datos por periodos temporales.
* **Llave Obligatoria:** `dt1` (Nombre de la columna con fechas).

```
# ✅ Configuración Correcta
db.Time({
    'op': 'D',            # 'D' para día, 'H' para hora
    'dt1': 'Fecha_Venta'  # <--- USAR SIEMPRE 'dt1'
})
```

📊 Módulo MATH: Documentación Técnica de Cálculos
El sistema utiliza un motor basado en diccionarios (kwargs) para ejecutar operaciones. A continuación, se detallan los parámetros exactos para cada funcionalidad del módulo MATH.

1. Calculadora (Lógica y Aritmética)

Dependiendo de la llave tipo, el motor activa diferentes procesos lógicos:

```
Operaciones Aritméticas Manuales

- Parámetros: op (+, -, *, /), col1, col2, res
- Uso: Realiza cálculos directos entre dos columnas existentes y guarda el resultado en una nueva.

Clasificación de Horarios

- Parámetros: tipo: "horarios", date1: "nombre_columna"
- Uso: Analiza una columna de tiempo y genera una nueva clasificación por turnos (Mañana, Tarde, Noche, Madrugada).

Análisis Semanal

- Parámetros: tipo: "semanas", date1: "nombre_columna"
- Uso: Determina si una fecha corresponde a un "Día de semana" o "Fin de semana".
```

🧪 CalculadoraPlus: Cálculos Financieros Preconfigurados
Esta función automatiza fórmulas de negocio sin necesidad de escribir la operación manual. El sistema identifica el case y procesa los datos:

```
- Costo Unitario: Requiere col1 (Total) y col2 (Cantidad).
- Subtotal: Requiere col1 (Precio) y col2 (Cantidad).
- IVA: Calcula el impuesto basado en col1 y col2.
- Descuento: Aplica reducción porcentual usando col1 y col2.
- Precio Final: Caso especial que requiere tres parámetros: col1, col2 y col3.
- Margen Bruto y Margen PCT: Cálculos de rentabilidad basados en costo y venta.
- Envío KG y Conversión Divisa: Operaciones de logística y finanzas internacionales.
```

Ejemplo de uso:

```
# Ejemplo: Generando Precio Final con Descuento
# Requerimiento: sub_total y monto_descuento

db.CalculadoraPlus({
    "tipo": "precio_final"   # tipo de operacion
    "col1": "Sub_Total",     # Monto base
    "col2": "Monto_Dcto",    # Valor a restar
    "res": "Precio_Neto"     # Columna nueva
})
```

⏱️ Time & TimePlus: Inteligencia Temporal
Módulo especializado en la extracción y análisis de series de tiempo.

```
Extracción Básica (Time)

- Parámetros: op ("D" para día, "H" para hora), dt1: "nombre_columna"
- Nota: Es estrictamente necesario usar la llave dt1 para este método.

Análisis Avanzado (TimePlus)

- Lead Time: Requiere date1 (Inicio) y date2 (Fin). Calcula el tiempo de ciclo.
- Inventario: Requiere date1 y date2. Analiza días de rotación.
- Proyecciones: Utiliza date1 y date2 para estimar tendencias futuras.
- Estacionalidad: Requiere date1. Clasifica por Mes, Año o Trimestre.
```

Ejemplo para TimePlus:

```
# Ejemplo: Calculando el Lead Time (Tiempo de entrega)
# Basado en el submenú de base.py (opción 2)

db.TimePlus({
    "tipo": "lead_time"
    "date1": "Fecha_Pedido",
    "date2": "Fecha_Entrega"
})
```

# Invocación: El primer argumento es el caso, el segundo desempaqueta el dict
db.TimePlus("lead_time", **config_logistica)

🔗 Módulo de Unión de Datos (Merge & MergePlus)
Este módulo permite consolidar múltiples archivos o fuentes de datos en un único DataFrame maestro, ya sea de forma incremental o masiva.

1. Merge (Unión entre Objetos)
La función Merge permite unir el DataFrame actual con otro objeto DataToolBox. Soporta orientaciones tanto verticales como horizontales.

Parámetros:

- add: Debe ser otro objeto de tipo DataToolBox.
- lado: Dirección de la unión. "v" o "V" para Vertical (filas), "h" o "H" para Horizontal (columnas). Por defecto es Vertical.
- rutas: Puede ser una ruta única (String) o una lista de rutas (['file1.csv', 'file2.csv']).
- lado: Dirección de la unión (por defecto "v").
  
Ejemplo de uso:

```
lista_A = DataToolBox("ventas_enero.csv")
lista_B = DataToolBox("ventas_febrero.csv")

# Une las ventas de febrero debajo de las de enero
lista_A.Merge(lista_B, lado="v")

NOTA: tanto lista_A como Lista_B deben de ser un objeto
```

2. MergePlus (Unión Masiva Automática)
Es la herramienta de "paracaídas" para procesar múltiples archivos a la vez. Incluye filtros de seguridad y gestión de errores (archivos corruptos o inexistentes).

Parámetros:

- rutas: Puede ser una ruta única (String) o una lista de rutas (['file1.csv', 'file2.csv']).
- lado: Dirección de la unión (por defecto "v").

Características especiales de MergePlus:

- Filtro de Autoduplicado: Detecta si intentas unir el archivo base consigo mismo y lo ignora automáticamente.
- Sistema de Rezagados: Si un archivo falla por estar corrupto o no existir, el sistema no se detiene; guarda el nombre en una lista de "rezagados" y te informa al final del proceso.
- Validación de Integridad: Si las columnas no coinciden exactamente, el sistema lanza una alerta antes de proceder para evitar pérdida de datos o valores NaN inesperados.

Ejemplo de uso masivo:

```
mis_archivos = ["sucursal_norte.csv", "sucursal_sur.csv", "sucursal_este.csv"]
db.MergePlus(mis_archivos)
```

⚠️ Guía de Consistencia para Desarrolladores

Para garantizar que el flujo de datos no se interrumpa (evitar KeyError: None), se deben seguir estas reglas de nombrado:

- Uso de Fechas: - En la función Time(), la llave debe ser obligatoriamente dt1. Mientras que en las funciones Calculadora() (horarios/semanas) y TimePlus(), la llave debe ser date1.
- Pre-procesamiento: Siempre ejecutar CleanStruct() antes de cualquier cálculo para normalizar los nombres de las columnas y eliminar espacios residuales.
- Validación de Columnas: El sistema verifica la existencia de col1 y col2 antes de operar. Si una columna no existe, el proceso se detendrá para proteger la integridad del DataFrame.

🛠️ Tecnologías Utilizadas

Python 3.x

- Pandas & NumPy: Para manipulación masiva de datos.
- SQLAlchemy: Conector de base de datos de grado industrial.
- Regex: Motores de búsqueda y extracción de patrones.
- Type Hinting: Código tipado para mayor mantenibilidad y robustez.

🚧 Roadmap (Próximas Mejoras)

[ ] Implementación de logs automáticos de errores en archivos externos.
[ ] Optimización del motor de duplicados para manejo selectivo de registros.
[ ] Soporte para archivos Excel (.xlsx) con múltiples pestañas.

Desarrollado por [Tu Nombre/SkrtNull] - Data Engineer en formación
