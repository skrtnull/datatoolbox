# 🛠️ DataToolBox: Framework Modular de ETL

<p align="center">
  <a href="#english">English Version</a> • 
  <a href="#español">Versión en Español</a>
</p>

---

<a name="español"></a>
## ES Version en español

DataToolBox es una solución robusta de ingeniería de datos diseñada para automatizar la ingesta, limpieza y transformación de archivos masivos. El sistema utiliza una arquitectura basada en eventos para procesar información en tiempo real, transformando datos "caóticos" en tablas estructuradas listas para producción.

###🚀 Características Principales

- Monitoreo Automático (Hot Folder): Implementación de Watchdog para detectar archivos en la carpeta bandeja/. El proceso inicia instantáneamente sin intervención manual.
- Limpieza Vectorizada: Uso intensivo de Pandas y NumPy para procesar miles de filas en milisegundos, evitando bucles for lentos.
- Pipeline Configurable: El motor Autorun desacopla la lógica del código, leyendo las reglas de transformación desde metadatos (SQL/JSON).
- Resiliencia ante Datos Corruptos: Manejo avanzado de errores (errors='coerce') para procesar archivos con nulos, strings en columnas numéricas y fechas mal formateadas.

##🛠️ Tech Stack

- Lenguaje: Python 3.10+
- Manipulación de Datos: Pandas, NumPy
- Automatización: Watchdog (File System Events)
- Base de Datos: SQLAlchemy (ORM para integración con SQL Server, SQLite, etc.)

##📁 Estructura del Proyecto

```
├── bandeja/              # Input: Carpeta monitoreada
├── procesados/           # Output: Archivos estandarizados
├── src/
│   ├── kit.py            # Clase principal (Motor de Limpieza)
│   └── pipeline.py       # Punto de entrada y Orquestador
├── requirements.txt      # Dependencias del sistema
└── README.md
```

##⚙️ Instalación y Uso

Clonar el repositorio:

```
git clone https://github.com/tu-usuario/datatoolbox-etl.git
cd datatoolbox-etl
```

Instalar dependencias necesarias:

```
pip install -r requirements.txt
```

Ejecutar la Pipeline:

```
python src/pipeline.py
```

Nota: Una vez ejecutado, el sistema entrará en modo "escucha". Solo debes arrastrar un archivo a la carpeta bandeja/ para ver la magia ocurrir en la terminal.

📊 Caso de Prueba: caos_total.csv

El proyecto incluye un dataset de prueba diseñado para romper cualquier script convencional. DataToolBox lo resuelve aplicando:

- Normalización Numérica: Conversión de tipos object a float64 con manejo de símbolos de moneda.
- Estandarización de Fechas: Inferencia de formatos mixtos y limpieza de valores NaT.
- Cálculo de Turnos: Clasificación automática de registros según la hora de captura.

🗺️ Roadmap Profesional

[ ] Implementación de contenedores con Docker.
[ ] Despliegue de infraestructura en Azure mediante Terraform.
[ ] Sistema de alertas y logs avanzados para monitoreo remoto.

📧 Contacto

Desarrollado por [Jonaiker Millan] - Especialista en Automatización de Datos.
LinkedIn: [https://www.linkedin.com/in/jonaiker-dataengineer/]
GitHub: [SkrtNull]

<a name="english"></a>

## Spanish Version

DataToolBox is a robust data engineering solution designed to automate the ingestion, cleaning, and transformation of large-scale files. The system uses an event-driven architecture to process information in real time, transforming “raw” data into structured tables ready for production.

###🚀 Key Features

- Automatic Monitoring (Hot Folder): Watchdog implementation to detect files in the input folder. The process starts instantly without manual intervention.
- Vectorized Cleaning: Intensive use of Pandas and NumPy to process thousands of rows in milliseconds, avoiding slow for loops.
- Configurable Pipeline: The Autorun engine decouples logic from code, reading transformation rules from metadata (SQL/JSON).
- Resilience to Corrupt Data: Advanced error handling (errors=‘coerce’) to process files with nulls, strings in numeric columns, and malformed dates.

##🛠️ Tech Stack

- Language: Python 3.10+
- Data Manipulation: Pandas, NumPy
- Automation: Watchdog (File System Events)
- Database: SQLAlchemy (ORM for integration with SQL Server, SQLite, etc.)

##📁 Project Structure

```
├── tray/              # Input: Monitored folder
├── processed/           # Output: Standardized files
├── src/
│   ├── kit.py            # Main class (Cleaning Engine)
│   └── pipeline.py       # Entry point and Orchestrator
├── requirements.txt      # System dependencies
└── README.md
```

##⚙️ Installation and Usage

Clone the repository:

```
git clone https://github.com/tu-usuario/datatoolbox-etl.git
cd datatoolbox-etl
```

Install required dependencies:

```
pip install -r requirements.txt
```

Run the Pipeline:

```
python src/pipeline.py
```

Note: Once executed, the system will enter “listening” mode. Simply drag a file into the tray/ folder to watch the magic happen in the terminal.

📊 Test Case: caos_total.csv

The project includes a test dataset designed to break any conventional script. DataToolBox resolves it by applying:

- Numeric Normalization: Conversion of object types to float64 with currency symbol handling.
- Date Standardization: Inference of mixed formats and cleaning of NaT values.
- Shift Calculation: Automatic classification of records based on capture time.

🗺️ Professional Roadmap

[ ] Container implementation with Docker.
[ ] Infrastructure deployment on Azure using Terraform.
[ ] Advanced alerting and logging system for remote monitoring.

📧 Contact

Developed by [Jonaiker Millan] - Data Automation Specialist.
LinkedIn: [https://www.l

Translated with DeepL.com (free version)
