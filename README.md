# 🛠️ DataToolBox: Framework Modular de ETL

<p align="center">
  <a href="#english">English Version</a> • 
  <a href="#español">Versión en Español</a>
</p>

---

<a name="español"></a>
## ES Version en español

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/Status-Optimizing-orange.svg)]()

> "¡¡Es muy bueno!!" — **Zach Wilson**, Fundador de EcritData, sobre la arquitectura de este pipeline.

## 📌 Descripción General
**DataToolBox** es un kit de herramientas ETL (Extracción, Transformación y Carga) desarrollado en Python, diseñado para convertir datos crudos y caóticos en formatos estructurados listos para el análisis. Este proyecto se enfoca en la **escalabilidad**, el **código modular** y la **limpieza estadística de datos**.
---

# 🚀 Funcionalidades Principales

- **Limpieza Inteligente de Números:** Motor de extracción selectiva que rescata valores numéricos de cadenas de texto mezcladas (ej: `"ID-102A"` ➔ `102`) sin pérdida de registros.
- **Normalización de Texto:** Estandarización de nombres, correcciones de capitalización y eliminación de espacios redundantes.
- **Motor de Reglas (CalculadoraPlus):** Inyección de lógica aritmética y de fechas dinámica para crear columnas de valor añadido (puntos de fidelidad, turnos horarios, etc.).
- **Validación de Integridad:** Gestión avanzada de nulos y duplicados bajo demanda.
- **Conectividad Multi-formato:** Soporte nativo para CSV, Parquet, JSON y carga directa a bases de datos mediante SQLAlchemy.

# 📦 Instalación
Para utilizar esta herramienta, clona el repositorio e instala las dependencias necesarias:

```
1.  **En GitHub:** Entra a tu repositorio, dale al icono del lápiz en el archivo `README.md`.
2.  **Pegar:** Borra todo lo que haya y pega el bloque de arriba.
3.  **Personalizar:**
    * Cambia `TU_USUARIO` en el link de `git clone` por tu nombre de usuario de GitHub.
    * Cambia `[Tu Nombre]` al final por tu nombre real.
4.  **Guardar:** Dale a "Commit changes".
5.  **requirements.txt:** Asegúrate de que en tu repositorio exista un archivo llamado `requirements.txt`. Si no lo tienes, créalo y pon dentro:
    ```text
    pandas
    numpy
    sqlalchemy
    pyarrow
    ```
```
**¡Con esto, tu repositorio pasa de ser un proyecto de estudiante a una herramienta de ingeniería profesional!** ¿Quieres que hagamos la versión en español para ponerla justo debajo en el mismo archivo? 🚀🔥

## 🏗️ Flexibilidad de Instancia y Conexión SQL
DataToolBox está diseñado para adaptarse a diferentes flujos de trabajo, permitiendo desde la carga tradicional de archivos hasta la integración directa con motores de bases de datos.

# 1. Inicialización Versátil
El objeto puede ser instanciado de dos formas, permitiendo el "Lazy Loading" (carga tardía) de datos:

- **Instancia con Origen:** Carga un archivo CSV inmediatamente al crear el objeto.
- **Instancia Vacía:** Crea la estructura del framework sin datos iniciales. Útil para pipelines donde el origen se define en tiempo de ejecución o proviene de una base de datos.

```
# Opción A: Carga inmediata
db = DataToolBox("datos_venta.csv")

# Opción B: Instancia preparada para conexión externa
db = DataToolBox()
```

# 2. Conexión a Bases de Datos (DB_Connect)
El sistema integra SQLAlchemy para conectarse a diversos motores (PostgreSQL, MySQL, SQLite, SQL Server). Esto permite transformar consultas SQL directamente en DataFrames listos para ser procesados por los módulos MATH y PLUS.

Estructura de Configuración:
Para conectar, se debe pasar un diccionario con las credenciales y el query deseado:

```
db.DB_Connect({
    "driver": "postgresql",
    "user": "admin_user",
    "pass": "mi_password_seguro",
    "host": "localhost",
    "port": "5432",
    "db": "warehouse_db",
    "query": "SELECT * FROM ventas WHERE total > 1000"
})
```

# ⚠️ Requisitos para SQL
 NOTA TECNICA: Para utilizar la conexión a base de datos, asegúrate de tener instalada la librería sqlalchemy y el driver correspondiente a tu motor (ej: psycopg2 para PostgreSQL o pymysql para MySQL).

## 🧼 Módulo de Limpieza de Datos (kit.py)
El corazón de DataToolBox es su motor de normalización selectiva. A diferencia de los scripts lineales, este kit permite aplicar transformaciones avanzadas a múltiples columnas simultáneamente, optimizando el tiempo de procesamiento y la legibilidad del código.

#🚀 Funciones de Limpieza y Estandarización

- **CleanText(columna, drop=True):** Normaliza cadenas de texto eliminando caracteres especiales y acentos. Convierte a formato Capitalize y elimina espacios residuales. Si drop=True, elimina símbolos no alfanuméricos.
- **CleanNumb(columna, sib=None, drop=True):** Especializada en columnas financieras o de inventario. Elimina símbolos de moneda (ej: $), extrae solo los valores numéricos y convierte el dato a tipo entero o flotante de forma segura.
- **CleanFalse(columna):** Identifica y elimina "datos mentirosos". Utiliza el método de Rango Intercuartílico (IQR) para detectar outliers y valores que no cumplen con las métricas de negocio (como errores de base de datos tipo BBDD_ERR).
- **CleanDate(fecha, drop=True):** Estandariza formatos temporales. Corrige errores de digitación y asegura que todas las fechas del dataset sigan el estándar ISO para análisis de series temporales.
- **ExtractInfo(columna, patron):** Utiliza Expresiones Regulares (Regex) para recuperar información específica (como correos electrónicos o números telefónicos) incrustada en columnas con datos corruptos o ilegibles.
- **CleanStruct():** Realiza una limpieza estructural completa del archivo, eliminando filas totalmente vacías o registros inconsistentes que comprometen la integridad del análisis.

Ejemplo:

```
#
#eliminar filas vacias
db.CleanStruct()

#Estandarizacion de columna de numeros
db.CleanNumb("id")

#Nomralizar columana de texto
db.CleanText("nombre_cliente")

#Normalizar fechas, por defecto eliminara las filas donde las fechas sean nulas
db.CleanDate("fecha_compra")

#extrae informacion por patrones complejos, se puede usar para extraer emails o numeros de telefono
db.ExtractInfo("email")
```

## 🛠️ Módulo MATH: Documentación Técnica de Cálculos
Para evitar errores de `KeyError`, asegúrate de usar los nombres exactos de las llaves que el motor espera. El sistema utiliza un motor basado en diccionarios (kwargs) para ejecutar operaciones. A continuación, se detallan los parámetros exactos para cada funcionalidad del módulo MATH.

# 🚀 Glosario de Llaves (Keys) de Configuración
Para que las funciones de DataToolBox procesen la información correctamente, los diccionarios de configuración deben utilizar estas llaves estandarizadas. Es fundamental respetar los nombres en minúsculas:

- **"tipo" / "preset":** Define la operación específica o el caso de negocio que se va a ejecutar (ejemplo: "iva", "M", "Lead_time").
- **"op":** Define el operador aritmético manual para la calculadora (ejemplo: "+", "-", "*", "/").
- **"col1":** Nombre de la primera columna numérica involucrada en el cálculo.
- **"col2":** Nombre de la segunda columna numérica (o valor comparativo).
- **"col3":** Columna adicional requerida para casos complejos (como en case "precio_final").
- **"date1":** Nombre de la columna de fecha principal o fecha de inicio para análisis temporal.
- **"date2":** Nombre de la columna de fecha secundaria o fecha de finalización.
- **"res":** Nombre que recibirá la nueva columna donde se guardará el resultado del proceso.

# ⚠️ Reglas de Oro para el Usuario:

- **Sensibilidad:** Las llaves del diccionario deben estar siempre en minúsculas ("col1", no "Col1").
- Nombres de Columnas: El valor que asignes a la llave (ejemplo: "Fecha_Venta") debe coincidir exactamente con el nombre de la columna en tu set de datos.
- Orden: Si no defines la llave "res", el sistema generará un nombre automático, pero se recomienda definirlo para mantener la claridad en el reporte final.

## 🛠️ Cómo utilizar las Funciones
La potencia de DataToolBox reside en su motor de procesamiento basado en configuraciones. En lugar de escribir código complejo para cada cálculo, el framework utiliza diccionarios de parámetros. Esto permite que las funciones sean modulares, fáciles de leer y altamente escalables.

A continuación, se detallan los módulos principales y los casos que puedes ejecutar enviando una configuración simple.

# 🧪 Calculadora (Operaciones Manuales)
El método Calculadora() es el motor lógico principal. Se utiliza para realizar operaciones aritméticas personalizadas o clasificaciones automáticas basadas en una sola columna. Ideal para crear nuevas columnas basadas en operaciones matemáticas simples entre dos columnas existentes, aquí tienes el desglose de lo que puedes hacer:

- **"+":** Realiza la Suma de dos columnas. Requiere col1, col2 y res.
- **"-":** Realiza la Resta de dos columnas. Requiere col1, col2 y res.
- **"*":** Realiza la Multiplicación de dos columnas. Requiere col1, col2 y res.
- **"/":** Realiza la División de dos columnas. Requiere col1, col2 y res.

NOTA: las operaciones aritmeticas usa las llaves "col1", "col2" y "res".

#🛠️ Ejemplo para Calculadora:

```
# Sumar dos columnas y guardar el resultado
db.Calculadora({
    "op": "+",
    "col1": "Ventas_Enero",
    "col2": "Ventas_Febrero",
    "res": "Total_Bimestre"
})
```

# 1.🧪 CalculadoraPlus: Cálculos Financieros Preconfigurados
Esta función automatiza fórmulas de negocio sin necesidad de escribir la operación manual. El sistema identifica el case y procesa los datos:

- **"costo_unitario":** Requiere col1 (Total) y col2 (Cantidad).
- **"subtotal":** Requiere col1 (Precio) y col2 (Cantidad).
- **"iva":** Calcula el impuesto basado en col1 y col2.
- **"descuento":** Aplica reducción porcentual usando col1 y col2.
- **"precio_final":** Caso especial que requiere tres parámetros: col1, col2 y col3.
- **"margen_bruto":** Cálculos de rentabilidad basados en costo y venta.
- **"margen_pct":** Cálculos de rentabilidad basados en costo y venta.
- **"margen_porcent":** Cálculos de rentabilidad basados en costo y venta con porcentaje.
- **"envio_KG":** Operación de cálculo logístico por peso.
- **"conversion_divisa":** Operación de finanzas internacionales.

#🛠️ Ejemplo de CalculadoraPlus:

```
# Ejemplo: Generando sub-total
# Requerimiento: precio y cantidad

db.CalculadoraPlus({
    "tipo": "sub-total"    # tipo de operacion
    "col1": "Precio",      # Monto base
    "col2": "Cantidad",    # Valor a restar
    "res": "Sub-total"     # Columna nueva
})

```

## 2.⏱️ Time & TimePlus: Inteligencia Temporal
Módulo especializado en la extracción y análisis de series de tiempo.

# 2.1 Extracción Básica (Time)

Para el análisis temporal, el método TimePlus() utiliza identificadores cortos de una sola letra para definir la escala del cálculo. Asegúrate de respetar las mayúsculas y minúsculas tal como se muestran a continuación:

Análisis de Diferencia entre Fechas
Requiere las llaves "date1" y "date2" en el diccionario de configuración.

- **"D":** Calcula la diferencia total en Días. Ideal para Lead Times operativos.
- **"D2":** Variante para cálculo de días (revisar lógica específica en kit.py).
- **"S":** Calcula la diferencia en Semanas.
- **"M":** Calcula la diferencia en Meses.
- **"H":** Calcula la diferencia en Horas. Útil para análisis de turnos o tiempos de respuesta.
- **"Y":** Calcula la diferencia en Años.

Operaciones Especiales
Requieren únicamente la llave "date1".

- **"+":** Suma de periodos o normalización de fechas (según tu lógica en kit.py).
- **"=":** Comparación de igualdad o validación de formatos entre fechas.

# 🛠️ Ejemplo para Time:

```
# ✅ Configuración Correcta
db.Time({
    'op': 'D',            # 'D' para día, 'H' para hora
    'dt1': 'Fecha_Venta'  # <--- USAR SIEMPRE 'dt1'
})
```

# 2.2 Análisis Avanzado (TimePlus)

- **"Lead_time":** Requiere date1 (Inicio) y date2 (Fin). Calcula el tiempo de ciclo total entre dos procesos.
- **"Inventario":** Requiere date1 y date2. Analiza los días de rotación de stock y permanencia en bodega.
- **"proyecciones":** Utiliza date1 y date2 para estimar tendencias y fechas estimadas de llegada/finalización.
- **"estacionalidad":** Requiere date1. Clasifica automáticamente el registro por Mes, Año o Trimestre.
- **"horarios":** Requiere date1. Clasifica los registros según el bloque horario (Mañana, Tarde, Noche, Madrugada).

# 🛠️ Ejemplo para TimePlus:

```
# Ejemplo: Calculando el Lead Time (Tiempo de entrega)
# Basado en el submenú de base.py (opción 2)

db.TimePlus({
    "tipo": "lead_time"
    "date1": "Fecha_Pedido",
    "date2": "Fecha_Entrega"
})

db.TimePlus("lead_time", **config_logistica)
```

## 🔗 Módulo de Unión de Datos (Merge & MergePlus)
Este módulo permite consolidar múltiples archivos o fuentes de datos en un único DataFrame maestro, ya sea de forma incremental o masiva.

# 1. Merge (Unión entre Objetos)
La función Merge permite unir el DataFrame actual con otro objeto DataToolBox. Soporta orientaciones tanto verticales como horizontales.

Parámetros:

- **add:** Debe ser otro objeto de tipo DataToolBox.
- **lado:** Dirección de la unión. "v" o "V" para Vertical (filas), "h" o "H" para Horizontal (columnas). Por defecto es Vertical.
- **rutas:** Puede ser una ruta única (String) o una lista de rutas (['file1.csv', 'file2.csv']).
  
# 🛠️ Ejemplo de Merge:

```
lista_A = DataToolBox("ventas_enero.csv")
lista_B = DataToolBox("ventas_febrero.csv")

# Une las ventas de febrero debajo de las de enero
lista_A.Merge(lista_B, lado="v")

NOTA: tanto lista_A como Lista_B deben de ser un objeto
```

# 2. MergePlus (Unión Masiva Automática)
Es la herramienta de "paracaídas" para procesar múltiples archivos a la vez. Incluye filtros de seguridad y gestión de errores (archivos corruptos o inexistentes).

Parámetros:

- **rutas:** Puede ser una ruta única (String) o una lista de rutas (['file1.csv', 'file2.csv']).
- **lado:** Dirección de la unión (por defecto "v").

Características especiales de MergePlus:

- **Filtro de Autoduplicado:** Detecta si intentas unir el archivo base consigo mismo y lo ignora automáticamente.
- **Sistema de Rezagados:** Si un archivo falla por estar corrupto o no existir, el sistema no se detiene; guarda el nombre en una lista de "rezagados" y te informa al final del proceso.
- **Validación de Integridad:** Si las columnas no coinciden exactamente, el sistema lanza una alerta antes de proceder para evitar pérdida de datos o valores NaN inesperados.

# 🛠️ Ejemplo de MergePlus (para uso masivo):

```
mis_archivos = ["sucursal_norte.csv", "sucursal_sur.csv", "sucursal_este.csv"]
db.MergePlus(mis_archivos)
```

## ⚠️ Guía de Consistencia para Desarrolladores

Para garantizar que el flujo de datos no se interrumpa (evitar KeyError: None), se deben seguir estas reglas de nombrado:

- **Uso de Fechas:** - En la función Time(), la llave debe ser obligatoriamente dt1. Mientras que en las funciones Calculadora() (horarios/semanas) y TimePlus(), la llave debe ser date1.
- **Pre-procesamiento:** Siempre ejecutar CleanStruct() antes de cualquier cálculo para normalizar los nombres de las columnas y eliminar espacios residuales.
- **Validación de Columnas:** El sistema verifica la existencia de col1 y col2 antes de operar. Si una columna no existe, el proceso se detendrá para proteger la integridad del DataFrame.

# 🛠️ Resumen de Flujo de Trabajo (ETL)

Con estas funcionalidades, el flujo de trabajo estándar en DataToolBox sigue este orden lógico de Ingeniería de Datos:

- **Extract:** Conexión vía DB_Connect() o carga de múltiples archivos con MergePlus().
- **Transform:** Limpieza estructural con CleanStruct(), normalización numérica con CleanNumb() y enriquecimiento mediante el módulo MATH.
- **Business Logic:** Aplicación de capas avanzadas de negocio con CalculadoraPlus (Costos, Márgenes) y TimePlus (Lead Times).
- **Load:** (Próximamente) Exportación de datos optimizados.
- 
# 🛠️ Tecnologías Utilizadas

Python 3.x

- **Pandas & NumPy:** Para manipulación masiva de datos.
- **SQLAlchemy:** Conector de base de datos de grado industrial.
- **Regex:** Motores de búsqueda y extracción de patrones.
- **Type Hinting:** Código tipado para mayor mantenibilidad y robustez.

# 🚧 Roadmap (Próximas Mejoras)

- Implementación de logs automáticos de errores en archivos externos.
- Optimización del motor de duplicados para manejo selectivo de registros.
- Soporte para archivos Excel (.xlsx) con múltiples pestañas.

Desarrollado por [Jonaiker Millan/SkrtNull] - Data Engineer en formación

<a name="english"></a>
## 🇺🇸 English Version

# 🚀 DataToolBox: Modular ETL Framework

<p align="center">
  <a href="#english">English Version</a> • 
  <a href="#español">Versión en Español</a>
</p>

---

<a name="english"></a>
## 🇺🇸 English Version

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Status](https://img.shields.io/badge/Status-Optimizing-orange.svg)]()

> “It's really good!!” — **Zach Wilson**, Founder of EcritData, on the architecture of this pipeline.

## 📌 Overview
**DataToolBox** is an ETL (Extract, Transform, Load) toolkit developed in Python, designed to convert raw and chaotic data into structured formats ready for analysis. This project focuses on **scalability**, **modular code**, and **statistical data cleaning**.
---

# 🚀 Main Features

- **Intelligent Number Cleaning:** Selective extraction engine that rescues numeric values from mixed text strings (e.g., `“ID-102A”` ➔ `102`) without losing records.
- **Text Normalization:** Standardization of names, capitalization corrections, and removal of redundant spaces.
- **Rules Engine (CalculadoraPlus):** Injection of arithmetic and dynamic date logic to create value-added columns (loyalty points, shift schedules, etc.).
- **Integrity Validation:** Advanced management of nulls and duplicates on demand.
- **Multi-format Connectivity:** Native support for CSV, Parquet, JSON, and direct loading to databases using SQLAlchemy.

# 📦 Installation
To use this tool, clone the repository and install the necessary dependencies:

```
1.  **On GitHub:** Go to your repository, click on the pencil icon in the `README.md` file.
2.  **Paste:** Delete everything there and paste the block above.
3.  **Customize:**
    * Replace `YOUR_USERNAME` in the `git clone` link with your GitHub username.
    * Replace `[Your Name]` at the end with your real name.
4.  **Save:** Click “Commit changes.”
5.  **requirements.txt:** Make sure there is a file called `requirements.txt` in your repository. If you don't have it, create it and put the following inside:
```text
    pandas
    numpy
    sqlalchemy
    pyarrow
    ```
```
**With this, your repository goes from being a student project to a professional engineering tool!** Would you like us to make a Spanish version to put right below it in the same file? 🚀🔥

## 🏗️ Instance Flexibility and SQL Connection
DataToolBox is designed to adapt to different workflows, allowing everything from traditional file loading to direct integration with database engines.

# 1. Versatile Initialization
The object can be instantiated in two ways, allowing for “Lazy Loading” of data:

- **Instance with Source:** Loads a CSV file immediately when creating the object.
- **Empty Instance:** Creates the framework structure without initial data. Useful for pipelines where the source is defined at runtime or comes from a database.

```
# Option A: Immediate loading
db = DataToolBox(“sales_data.csv”)

# Option B: Instance prepared for external connection
db = DataToolBox()
```

# 2. Database Connection (DB_Connect)
The system integrates SQLAlchemy to connect to various engines (PostgreSQL, MySQL, SQLite, SQL Server). This allows SQL queries to be transformed directly into DataFrames ready to be processed by the MATH and PLUS modules.

Configuration Structure:
To connect, you must pass a dictionary with the credentials and the desired query:

```
db.DB_Connect({
    “driver”: “postgresql”,
    “user”: “admin_user”,
    “pass”: “my_secure_password”,
    “host”: “localhost”,
    “port”: “5432”,
    “db”: “warehouse_db”,
    “query”: “SELECT * FROM sales WHERE total > 1000”
})
```

# ⚠️ Requirements for SQL
TECHNICAL NOTE: To use the database connection, make sure you have the sqlalchemy library and the driver corresponding to your engine installed (e.g., psycopg2 for PostgreSQL or pymysql for MySQL).

## 🧼 Data Cleaning Module (kit.py)
The heart of DataToolBox is its selective normalization engine. Unlike linear scripts, this kit allows you to apply advanced transformations to multiple columns simultaneously, optimizing processing time and code readability.

#🚀 Cleaning and Standardization Functions

- **CleanText(column, drop=True):** Normalizes text strings by removing special characters and accents. Converts to Capitalize format and removes residual spaces. If drop=True, removes non-alphanumeric symbols.
- **CleanNumb(column, sib=None, drop=True):** Specialized for financial or inventory columns. Removes currency symbols (e.g., $), extracts only numeric values, and safely converts the data to integer or floating point type.
- **CleanFalse(column):** Identifies and removes “false data.” Uses the Interquartile Range (IQR) method to detect outliers and values that do not comply with business metrics (such as database errors like BBDD_ERR).
- **CleanDate(date, drop=True):** Standardizes date formats. Corrects typing errors and ensures that all dates in the dataset follow the ISO standard for time series analysis.
- **ExtractInfo(column, pattern):** Uses Regular Expressions (Regex) to retrieve specific information (such as email addresses or phone numbers) embedded in columns with corrupt or unreadable data.
- **CleanStruct():** Performs a complete structural cleanup of the file, removing completely empty rows or inconsistent records that compromise the integrity of the analysis.

Example:

```
#
#remove empty rows
db.CleanStruct()

#Standardize number column
db.CleanNumb(“id”)

#Normalize text column
db.CleanText(“customer_name”)

#Normalize dates; by default, it will delete rows where dates are null.
db.CleanDate(“purchase_date”)

#Extract information using complex patterns; can be used to extract emails or phone numbers.
db.ExtractInfo(“email”)
```

## 🛠️ MATH Module: Technical Documentation for Calculations
To avoid `KeyError` errors, make sure to use the exact names of the keys that the engine expects. The system uses a dictionary-based engine (kwargs) to execute operations. Below are the exact parameters for each feature of the MATH module.

# 🚀 Glossary of Configuration Keys
In order for DataToolBox functions to process information correctly, configuration dictionaries must use these standardized keys. It is essential to respect the lowercase names:

- **“tipo” / “preset”:** Defines the specific operation or business case to be executed (example: “iva”, ‘M’, “Lead_time”).
- **“op”:** Defines the manual arithmetic operator for the calculator (example: “+”, “-”, “*”, “/”).
- **“col1”:** Name of the first numeric column involved in the calculation.
- **“col2”:** Name of the second numeric column (or comparative value).
- **“col3”:** Additional column required for complex cases (such as in the “final_price” case).
- **“date1”:** Name of the main date column or start date for time analysis.
- **“date2”:** Name of the secondary date column or end date.
- **“res”:** Name that will be given to the new column where the result of the process will be saved.

# ⚠️ Golden Rules for Users:

- **Case sensitivity:** Dictionary keys must always be in lowercase (“col1,” not “Col1”).
- Column Names: The value you assign to the key (example: “Sale_Date”) must match exactly the name of the column in your dataset.
- Order: If you do not define the “res” key, the system will generate an automatic name, but it is recommended that you define it to maintain clarity in the final report.

## 🛠️ How to Use Functions
The power of DataToolBox lies in its configuration-based processing engine. Instead of writing complex code for each calculation, the framework uses parameter dictionaries. This allows functions to be modular, easy to read, and highly scalable.

Below are the main modules and the cases you can run by sending a simple configuration.

# 🧪 Calculator (Manual Operations)
The Calculator() method is the main logic engine. It is used to perform custom arithmetic operations or automatic classifications based on a single column. Ideal for creating new columns based on simple mathematical operations between two existing columns, here is a breakdown of what you can do:

- **“+”:** Performs the sum of two columns. Requires col1, col2, and res.
- **“-”:** Performs the subtraction of two columns. Requires col1, col2, and res.
- **“*”:** Performs the multiplication of two columns. Requires col1, col2, and res.
- **“/”:** Divides two columns. Requires col1, col2, and res.

NOTE: Arithmetic operations use the keys “col1,” “col2,” and “res.”

#🛠️ Example for Calculator:

```
# Add two columns and save the result
db.Calculator({
    “op”: “+”,
    “col1”: “January_Sales”,
    “col2”: “February_Sales”,
    “res”: “Two-Month_Total”
})
```

# 1.🧪 CalculatorPlus: Preconfigured Financial Calculations
This function automates business formulas without the need to write the operation manually. The system identifies the case and processes the data:

- **“costo_unitario”:** Requires col1 (Total) and col2 (Quantity).
- **“subtotal”:** Requires col1 (Price) and col2 (Quantity).
- **“iva”:** Calculates tax based on col1 and col2.
- **“descuento”:** Applies percentage reduction using col1 and col2.
- **“precio_final”:** Special case that requires three parameters: col1, col2, and col3.
- **“margen_bruto”:** Profitability calculations based on cost and sale.
- **“margen_pct”:** Profitability calculations based on cost and sale.
- **“margen_porcent”:** Profitability calculations based on cost and sales with percentage.
- **“envio_KG”:** Logistical calculation operation by weight.
- **“conversion_divisa”:** International finance operation.

#🛠️ CalculatorPlus example:

```
# Example: Generating subtotal
# Requirements: price and quantity

db.CalculadoraPlus({
    “type”: “subtotal”    # type of operation
    “col1”: “Price”,      # Base amount
    “col2”: “Quantity”,    # Value to subtract
    “res”: “Subtotal”     # New column
})

```

## 2.⏱️ Time & TimePlus: Temporal Intelligence
Module specialized in the extraction and analysis of time series.

# 2.1 Basic Extraction (Time)

For temporal analysis, the TimePlus() method uses short single-letter identifiers to define the scale of the calculation. Be sure to respect upper and lower case letters as shown below:

Date Difference Analysis
Requires the keys “date1” and “date2” in the configuration dictionary.

- **“D”:** Calculates the total difference in Days. Ideal for operational Lead Times.
- **“D2”:** Variant for calculating days (review specific logic in kit.py).
- **“S”:** Calculates the difference in Weeks.
- **“M”:** Calculates the difference in Months.
- **“H”:** Calculates the difference in Hours. Useful for shift analysis or response times.
- **“Y”:** Calculates the difference in Years.

Special Operations
Only require the “date1” key.

- **“+”:** Sum of periods or normalization of dates (according to your logic in kit.py).
- **“=”:** Comparison of equality or validation of formats between dates.

# 🛠️ Example for Time:

```
# ✅ Correct Configuration
db.Time({
    ‘op’: ‘D’,            # ‘D’ for day, ‘H’ for hour
    ‘dt1’: ‘Sale_Date’  # <--- ALWAYS USE ‘dt1’
})
```

# 2.2 Advanced Analysis (TimePlus)

- **“lead_time”:** Requires date1 (Start) and date2 (End). Calculates the total cycle time between two processes.
- **“inventario”:** Requires date1 and date2. Analyzes stock turnover days and warehouse permanence.
- **“proyecciones”:** Uses date1 and date2 to estimate trends and estimated arrival/completion dates.
- **“estacionalidad”:** Requires date1. Automatically sorts the record by Month, Year, or Quarter.
- **“horarios”:** Requires date1. Classifies records according to time block (Morning, Afternoon, Evening, Night).

# 🛠️ Example for TimePlus:

```
# Example: Calculating Lead Time (Delivery Time)
# Based on the base.py submenu (option 2)

db.TimePlus({
    “type”: ‘lead_time’
    “date1”: “Order_Date”,
    “date2”: “Delivery_Date”
})

db.TimePlus(“lead_time”, **config_logistica)
```

## 🔗 Data Merge Module (Merge & MergePlus)
This module allows you to consolidate multiple files or data sources into a single master DataFrame, either incrementally or in bulk.

# 1. Merge (Merge between Objects)
The Merge function allows you to merge the current DataFrame with another DataToolBox object. It supports both vertical and horizontal orientations.

Parameters:

- **add:** Must be another DataToolBox object.
- **side:** Direction of the join. “v” or “V” for Vertical (rows), ‘h’ or “H” for Horizontal (columns). The default is Vertical.
- **paths:** Can be a single path (String) or a list of paths ([‘file1.csv’, ‘file2.csv’]).
  
# 🛠️ Merge example:

```
list_A = DataToolBox(“sales_January.csv”)
list_B = DataToolBox(“sales_February.csv”)

# Merge February sales below January sales
list_A.Merge(list_B, lado="v")

NOTE: Both list_A and list_B must be objects.
```

# 2. MergePlus (Automatic Mass Merge)
This is the “parachute” tool for processing multiple files at once. It includes security filters and error management (corrupt or non-existent files).

Parameters:

- **paths:** Can be a single path (String) or a list of paths ([‘file1.csv’, ‘file2.csv’]).
- **side:** Direction of the merge (default “v”).

Special features of MergePlus:

- **Auto-Duplicate Filter:** Detects if you try to merge the base file with itself and automatically ignores it.
- **Lagging System:** If a file fails because it is corrupt or does not exist, the system does not stop; it saves the name in a “lagging” list and informs you at the end of the process.
- **Integrity Validation:** If the columns do not match exactly, the system issues an alert before proceeding to avoid data loss or unexpected NaN values.

  # 🛠️ MergePlus example (for mass use):

```
my_files = [“north_branch.csv”, “south_branch.csv”, “east_branch.csv”]
db.MergePlus(my_files)
```

## ⚠️ Consistency Guide for Developers

To ensure that the data flow is not interrupted (avoid KeyError: None), these naming rules must be followed:

- **Use of Dates:** - In the Time() function, the key must be dt1. In the Calculator() (schedules/weeks) and TimePlus() functions, the key must be date1.
- **Pre-processing:** Always run CleanStruct() before any calculations to normalize column names and remove residual spaces.
- **Column Validation:** The system checks for the existence of col1 and col2 before operating. If a column does not exist, the process will stop to protect the integrity of the DataFrame.

# 🛠️ Workflow Summary (ETL)

With these features, the standard workflow in DataToolBox follows this logical order of Data Engineering:

- **Extract:** Connection via DB_Connect() or loading multiple files with MergePlus().
- **Transform:** Structural cleaning with CleanStruct(), numerical normalization with CleanNumb(), and enrichment using the MATH module.
- **Business Logic:** Application of advanced business layers with CalculadoraPlus (Costs, Margins) and TimePlus (Lead Times).
- **Load:** (Coming soon) Export of optimized data.

# 🛠️ Technologies Used

Python 3.x

- **Pandas & NumPy:** For massive data manipulation.
- **SQLAlchemy:** Industrial-grade database connector.
- **Regex:** Search engines and pattern extraction.
- **Type Hinting:** Typed code for greater maintainability and robustness.

# 🚧 Roadmap (Upcoming Improvements)

- Implementation of automatic error logs in external files.
- Optimization of the duplicate engine for selective record handling.
- Support for Excel files (.xlsx) with multiple tabs.

Developed by [Jonaiker Millan/SkrtNull] - Data Engineer in training
