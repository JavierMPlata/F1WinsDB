# F1WinsDB - Sistema ETL para Análisis de Victorias en Fórmula 1

## 📋 Descripción del Proyecto

F1WinsDB es un proyecto de Big Data que implementa un pipeline ETL (Extract, Transform, Load) para el procesamiento y análisis de datos históricos de victorias en carreras de Fórmula 1. El sistema extrae datos de un archivo CSV, realiza un proceso completo de limpieza y transformación de datos, y genera un dataset limpio listo para análisis.

## 🏁 Características Principales

- **Extracción de Datos**: Lectura y procesamiento de datos históricos de F1 desde archivos CSV
- **Limpieza Inteligente**: Sistema avanzado de limpieza que maneja valores faltantes sin pérdida de información
- **Transformación de Tipos**: Conversión automática de tipos de datos para optimizar el análisis
- **Procesamiento Completo**: Pipeline automatizado con reportes detallados de cada etapa
- **Preservación de Datos**: Proceso que mantiene la integridad y completitud del dataset original

## 🗂️ Estructura del Proyecto

```
F1WinsDB/
├── main.py                    # Script principal del pipeline ETL
├── README.md                  # Documentación del proyecto
├── requirements.txt           # Dependencias de Python
├── Config/
│   ├── __init__.py
│   └── Config.py             # Configuración de rutas y parámetros
├── Extract/
│   ├── __init__.py
│   └── F1WinsExtract.py      # Módulo de extracción de datos
├── Limpieza/
│   ├── __init__.py
│   └── F1WinsClean.py        # Módulo de limpieza y transformación
└── Files/
    ├── F1Wins.csv            # Dataset original
    └── F1Wins_clean.csv      # Dataset limpio generado
```

## 📊 Dataset

### Datos Originales
El dataset contiene información histórica de victorias en Fórmula 1 con las siguientes columnas:
- **GRAND PRIX**: Nombre del Gran Premio
- **DATE**: Fecha de la carrera (formato dd-mmm-yy)
- **WINNER**: Nombre del piloto ganador
- **CAR**: Marca y modelo del automóvil
- **LAPS**: Número de vueltas completadas
- **TIME**: Tiempo total de la carrera

### Datos Procesados
Después del proceso ETL, los datos incluyen:
- Valores faltantes completados con algoritmos inteligentes
- Tipos de datos optimizados (fechas, números enteros)
- Corrección automática de años en fechas históricas
- Tiempos de carrera normalizados

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.7 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clonar o descargar el repositorio**
```bash
git clone https://github.com/JavierMPlata/F1WinsDB.git
cd F1WinsDB
```

2. **Crear un entorno virtual (recomendado)**
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

## 🔧 Uso del Sistema

### Ejecución Básica

Para ejecutar el pipeline ETL completo:

```bash
python main.py
```

### Proceso de Ejecución

El sistema ejecutará automáticamente las siguientes etapas:

1. **Extracción**: 
   - Carga del dataset desde `Files/F1Wins.csv`
   - Análisis inicial de la estructura de datos
   - Muestra de las primeras 15 filas

2. **Limpieza**:
   - Reporte detallado de valores faltantes
   - Limpieza inteligente de datos sin pérdida de filas
   - Conversión de tipos de datos
   - Corrección de fechas históricas

3. **Guardado**:
   - Exportación del dataset limpio a `Files/F1Wins_clean.csv`
   - Resumen final con estadísticas del proceso

### Ejemplo de Salida

```
EXTRAYENDO DATOS...
==================================================
Primeras 5 filas de los datos extraídos:
    GRAND PRIX        DATE              WINNER              CAR  LAPS    TIME
0  Great Britain  13-May-50         Nino Farina       ALFA ROMEO    70  13:23.6
1         Monaco  21-May-50  Juan Manuel Fangio       ALFA ROMEO   100  13:18.7
...

==================================================
PROCESO DE LIMPIEZA DE DATOS
==================================================
REPORTE DE DATOS FALTANTES
==================================================
Total de filas: 1040
Filas con datos faltantes: 0
...
```

## 🔍 Características Técnicas

### Módulo de Extracción (`F1WinsExtract.py`)
- **Clase**: `f1dbExtract`
- **Funcionalidad**: Carga y análisis inicial de datos CSV
- **Métodos principales**:
  - `queries()`: Carga el dataset y obtiene información básica
  - `response()`: Retorna una vista previa de los datos

### Módulo de Limpieza (`F1WinsClean.py`)
- **Clase**: `F1WinnersClean`
- **Funcionalidades**:
  - Detección y reporte de valores faltantes
  - Limpieza inteligente sin pérdida de datos
  - Conversión de tipos de datos
  - Corrección de fechas históricas
  - Cálculo de tiempos promedio para valores faltantes

### Módulo de Configuración (`Config.py`)
- **Clase**: `Config`
- **Parámetros configurables**:
  - `INPUT_PATH`: Ruta del archivo CSV original
  - `OUTPUT_PATH`: Ruta del archivo CSV limpio

## 📈 Algoritmos de Limpieza

### Tratamiento de Valores Faltantes
1. **LAPS**: Reemplazo con la mediana del dataset
2. **TIME**: Cálculo de tiempo promedio basado en datos existentes
3. **Fechas**: Corrección automática de años de 2 dígitos (1950-2030)
4. **Textos**: Reemplazo con el valor más frecuente o 'Unknown'

### Conversiones de Tipos
- **LAPS**: String/Float → Integer
- **DATE**: String → DateTime con corrección de siglo
- **Preservación**: Mantenimiento de tipos apropiados para análisis

## 🛠️ Dependencias

- **pandas**: Manipulación y análisis de datos
- **numpy**: Operaciones numéricas y arrays
- **requests**: Solicitudes HTTP (preparado para futuras extensiones)


## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📚 Fuente de Datos

**Dataset Original**: [F1 All Race Winners (1950-2021)](https://www.kaggle.com/datasets/saiishwaram/f1-all-race-winners-19502021)  
Fuente: Kaggle - Dataset público con datos históricos de ganadores de carreras de Fórmula 1 desde 1950 hasta 2021.

---

*Proyecto desarrollado con fines educativos para el análisis de datos históricos de Fórmula 1*