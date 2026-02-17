### DataToolBox
Framework de Ingeniería de Datos en Python para procesos de ETL, limpieza y normalización de bases de datos

# 🛠️ SkrtNull Kit - DataToolBox

**SkrtNull Kit** es una librería de automatización **ETL (Extract, Transform, Load)** desarrollada en Python. Está diseñada para ingenieros de datos que buscan una forma rápida y robusta de normalizar datasets, limpiar estructuras corruptas y preparar datos para análisis o carga en bases de datos SQL.

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
git clone [https://github.com/tu-usuario/DataToolBox.git](https://github.com/tu-usuario/DataToolBox.git)
cd DataToolBox
pip install -r requirements.txt
```

## 🏗️ Flexibilidad de Instancia y Conexión SQL
DataToolBox está diseñado para adaptarse a diferentes flujos de trabajo, permitiendo desde la carga tradicional de archivos hasta la integración directa con motores de bases de datos.

# 1. Inicialización Versátil
El objeto puede ser instanciado de dos formas, permitiendo el "Lazy Loading" (carga tardía) de datos:

- Instancia con Origen: Carga un archivo CSV inmediatamente al crear el objeto.
- Instancia Vacía: Crea la estructura del framework sin datos iniciales. Útil para pipelines donde el origen se define en tiempo de ejecución o proviene de una base de datos.

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

## 🛠️ Ejemplo de Uso (Pipeline de Datos)
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

## 🛠️ Módulo MATH: Documentación Técnica de Cálculos
Para evitar errores de `KeyError`, asegúrate de usar los nombres exactos de las llaves que el motor espera. El sistema utiliza un motor basado en diccionarios (kwargs) para ejecutar operaciones. A continuación, se detallan los parámetros exactos para cada funcionalidad del módulo MATH.

# 🚀 Glosario de Llaves (Keys) de Configuración
Para que las funciones de DataToolBox procesen la información correctamente, los diccionarios de configuración deben utilizar estas llaves estandarizadas. Es fundamental respetar los nombres en minúsculas:

- "tipo" / "preset": Define la operación específica o el caso de negocio que se va a ejecutar (ejemplo: "iva", "M", "Lead_time").
- "op": Define el operador aritmético manual para la calculadora (ejemplo: "+", "-", "*", "/").
- "col1": Nombre de la primera columna numérica involucrada en el cálculo.
- "col2": Nombre de la segunda columna numérica (o valor comparativo).
- "col3": Columna adicional requerida para casos complejos (como en case "precio_final").
- "date1": Nombre de la columna de fecha principal o fecha de inicio para análisis temporal.
- "date2": Nombre de la columna de fecha secundaria o fecha de finalización.
- "res": Nombre que recibirá la nueva columna donde se guardará el resultado del proceso.

# ⚠️ Reglas de Oro para el Usuario:

- Sensibilidad: Las llaves del diccionario deben estar siempre en minúsculas ("col1", no "Col1").
- Nombres de Columnas: El valor que asignes a la llave (ejemplo: "Fecha_Venta") debe coincidir exactamente con el nombre de la columna en tu set de datos.
- Orden: Si no defines la llave "res", el sistema generará un nombre automático, pero se recomienda definirlo para mantener la claridad en el reporte final.

## 🛠️ Cómo utilizar las Funciones
La potencia de DataToolBox reside en su motor de procesamiento basado en configuraciones. En lugar de escribir código complejo para cada cálculo, el framework utiliza diccionarios de parámetros. Esto permite que las funciones sean modulares, fáciles de leer y altamente escalables.

A continuación, se detallan los módulos principales y los casos que puedes ejecutar enviando una configuración simple.

# 🧪 Calculadora (Operaciones Manuales)
El método Calculadora() es el motor lógico principal. Se utiliza para realizar operaciones aritméticas personalizadas o clasificaciones automáticas basadas en una sola columna. Ideal para crear nuevas columnas basadas en operaciones matemáticas simples entre dos columnas existentes, aquí tienes el desglose de lo que puedes hacer:

- case "+": Realiza la Suma de dos columnas. Requiere col1, col2 y res.
- case "-": Realiza la Resta de dos columnas. Requiere col1, col2 y res.
- case "*": Realiza la Multiplicación de dos columnas. Requiere col1, col2 y res.
- case "/": Realiza la División de dos columnas. Requiere col1, col2 y res.

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

- case "costo_unitario": Requiere col1 (Total) y col2 (Cantidad).
- case "subtotal": Requiere col1 (Precio) y col2 (Cantidad).
- case "iva": Calcula el impuesto basado en col1 y col2.
- case "descuento": Aplica reducción porcentual usando col1 y col2.
- case "precio_final": Caso especial que requiere tres parámetros: col1, col2 y col3.
- case "margen_bruto": Cálculos de rentabilidad basados en costo y venta.
- case "margen_pct": Cálculos de rentabilidad basados en costo y venta.
- case "margen_porcent": Cálculos de rentabilidad basados en costo y venta con porcentaje.
- case "envio_KG": Operación de cálculo logístico por peso.
- case "conversion_divisa": Operación de finanzas internacionales.

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

- case "D": Calcula la diferencia total en Días. Ideal para Lead Times operativos.
- case "D2": Variante para cálculo de días (revisar lógica específica en kit.py).
- case "S": Calcula la diferencia en Semanas.
- case "M": Calcula la diferencia en Meses.
- case "H": Calcula la diferencia en Horas. Útil para análisis de turnos o tiempos de respuesta.
- case "Y": Calcula la diferencia en Años.

Operaciones Especiales
Requieren únicamente la llave "date1".

- case "+": Suma de periodos o normalización de fechas (según tu lógica en kit.py).
- case "=": Comparación de igualdad o validación de formatos entre fechas.

# 🛠️ Ejemplo para Time:

```
# ✅ Configuración Correcta
db.Time({
    'op': 'D',            # 'D' para día, 'H' para hora
    'dt1': 'Fecha_Venta'  # <--- USAR SIEMPRE 'dt1'
})
```

# 2.2 Análisis Avanzado (TimePlus)

- case "Lead_time": Requiere date1 (Inicio) y date2 (Fin). Calcula el tiempo de ciclo total entre dos procesos.
- case "Inventario": Requiere date1 y date2. Analiza los días de rotación de stock y permanencia en bodega.
- case "proyecciones": Utiliza date1 y date2 para estimar tendencias y fechas estimadas de llegada/finalización.
- case "estacionalidad": Requiere date1. Clasifica automáticamente el registro por Mes, Año o Trimestre.
- case "horarios": Requiere date1. Clasifica los registros según el bloque horario (Mañana, Tarde, Noche, Madrugada).

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

- add: Debe ser otro objeto de tipo DataToolBox.
- lado: Dirección de la unión. "v" o "V" para Vertical (filas), "h" o "H" para Horizontal (columnas). Por defecto es Vertical.
- rutas: Puede ser una ruta única (String) o una lista de rutas (['file1.csv', 'file2.csv']).
  
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

- rutas: Puede ser una ruta única (String) o una lista de rutas (['file1.csv', 'file2.csv']).
- lado: Dirección de la unión (por defecto "v").

Características especiales de MergePlus:

- Filtro de Autoduplicado: Detecta si intentas unir el archivo base consigo mismo y lo ignora automáticamente.
- Sistema de Rezagados: Si un archivo falla por estar corrupto o no existir, el sistema no se detiene; guarda el nombre en una lista de "rezagados" y te informa al final del proceso.
- Validación de Integridad: Si las columnas no coinciden exactamente, el sistema lanza una alerta antes de proceder para evitar pérdida de datos o valores NaN inesperados.

# 🛠️ Ejemplo de MergePlus (para uso masivo):

```
mis_archivos = ["sucursal_norte.csv", "sucursal_sur.csv", "sucursal_este.csv"]
db.MergePlus(mis_archivos)
```

## ⚠️ Guía de Consistencia para Desarrolladores

Para garantizar que el flujo de datos no se interrumpa (evitar KeyError: None), se deben seguir estas reglas de nombrado:

- Uso de Fechas: - En la función Time(), la llave debe ser obligatoriamente dt1. Mientras que en las funciones Calculadora() (horarios/semanas) y TimePlus(), la llave debe ser date1.
- Pre-procesamiento: Siempre ejecutar CleanStruct() antes de cualquier cálculo para normalizar los nombres de las columnas y eliminar espacios residuales.
- Validación de Columnas: El sistema verifica la existencia de col1 y col2 antes de operar. Si una columna no existe, el proceso se detendrá para proteger la integridad del DataFrame.

# 🛠️ Resumen de Flujo de Trabajo (ETL)

Con estas funcionalidades, el flujo de trabajo estándar en DataToolBox sigue este orden lógico de Ingeniería de Datos:

- Extract: Conexión vía DB_Connect() o carga de múltiples archivos con MergePlus().
- Transform: Limpieza estructural con CleanStruct(), normalización numérica con CleanNumb() y enriquecimiento mediante el módulo MATH.
- Business Logic: Aplicación de capas avanzadas de negocio con CalculadoraPlus (Costos, Márgenes) y TimePlus (Lead Times).
- Load: (Próximamente) Exportación de datos optimizados.
- 
# 🛠️ Tecnologías Utilizadas

Python 3.x

- Pandas & NumPy: Para manipulación masiva de datos.
- SQLAlchemy: Conector de base de datos de grado industrial.
- Regex: Motores de búsqueda y extracción de patrones.
- Type Hinting: Código tipado para mayor mantenibilidad y robustez.

# 🚧 Roadmap (Próximas Mejoras)

- Implementación de logs automáticos de errores en archivos externos.
- Optimización del motor de duplicados para manejo selectivo de registros.
- Soporte para archivos Excel (.xlsx) con múltiples pestañas.

Desarrollado por [Jonaiker Millan/SkrtNull] - Data Engineer en formación
