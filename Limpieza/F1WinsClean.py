import pandas as pd
import numpy as np

class F1WinnersClean:
    def __init__(self, dataframe):
        """
        Inicializa la clase de limpieza con el DataFrame de F1 Winners
        
        Args:
            dataframe (pd.DataFrame): DataFrame con los datos de ganadores de F1
        """
        self.data = dataframe.copy()
        self.original_data = dataframe.copy()
    
    def check_missing_values(self):
        """
        Verifica y reporta valores nulos y NA en el dataset
        
        Returns:
            dict: Diccionario con información sobre valores faltantes
        """
        missing_info = {
            'total_rows': len(self.data),
            'null_values': self.data.isnull().sum().to_dict(),
            'na_values': self.data.isna().sum().to_dict(),
            'rows_with_missing': len(self.data[self.data.isnull().any(axis=1)]),
            'missing_data_percentage': (self.data.isnull().sum() / len(self.data) * 100).to_dict()
        }
        
        return missing_info
    
    def display_missing_data_report(self):
        """
        Muestra un reporte detallado de los datos faltantes
        """
        missing_info = self.check_missing_values()
        
        print("=" * 50)
        print("REPORTE DE DATOS FALTANTES")
        print("=" * 50)
        print(f"Total de filas: {missing_info['total_rows']}")
        print(f"Filas con datos faltantes: {missing_info['rows_with_missing']}")
        print()
        
        print("Valores nulos por columna:")
        print("-" * 30)
        for col, count in missing_info['null_values'].items():
            percentage = missing_info['missing_data_percentage'][col]
            if count > 0:
                print(f"{col}: {count} ({percentage:.2f}%)")
            else:
                print(f"{col}: {count}")
        
        print("\nFilas con valores faltantes:")
        print("-" * 30)
        missing_rows = self.data[self.data.isnull().any(axis=1)]
        if len(missing_rows) > 0:
            print(missing_rows[['GRAND PRIX', 'DATE', 'WINNER', 'LAPS', 'TIME']])
        else:
            print("No hay filas con valores faltantes")
    
    def clean_missing_values(self):
        """
        Limpia los valores faltantes reemplazándolos con valores apropiados
        No elimina filas, solo reemplaza valores
        """
        print("Iniciando limpieza de datos...")
        
        # Para LAPS (número de vueltas)
        if self.data['LAPS'].isnull().any():
            # Calcular la mediana de laps por grand prix similar o año similar
            median_laps = self.data['LAPS'].median()
            print(f"Reemplazando valores nulos en LAPS con la mediana: {median_laps}")
            self.data['LAPS'] = self.data['LAPS'].fillna(median_laps)
        
        # Para TIME (tiempo de carrera)
        if self.data['TIME'].isnull().any():
            # Calcular un tiempo promedio basado en los datos existentes
            # Si no hay datos válidos, usar un tiempo típico de F1 (aproximadamente 1:30:00)
            tiempo_promedio = self._calculate_average_race_time()
            print(f"Reemplazando valores nulos en TIME con tiempo promedio: '{tiempo_promedio}'")
            self.data['TIME'] = self.data['TIME'].fillna(tiempo_promedio)
        
        # Verificar si hay otros tipos de valores que podrían considerarse como faltantes
        # Como 'null', 'N/A', 'nan', etc. en formato string
        self._clean_string_nulls()
        
        print("Limpieza completada!")
    
    def _calculate_average_race_time(self):
        """
        Calcula un tiempo promedio de carrera basado en los datos existentes
        Si no hay datos válidos, retorna un tiempo típico de F1
        
        Returns:
            str: Tiempo promedio en formato string
        """
        import re
        
        # Filtrar valores válidos de TIME (no nulos, no N/A, no vacíos)
        valid_times = self.data['TIME'].dropna()
        valid_times = valid_times[~valid_times.isin(['N/A', 'n/a', 'NULL', 'null', ''])]
        
        if len(valid_times) > 0:
            # Intentar extraer tiempos en formato típico de F1 (ej: "1:34:50.616")
            time_pattern = r'(\d+):(\d+):(\d+\.?\d*)'
            total_seconds = []
            
            for time_str in valid_times:
                match = re.search(time_pattern, str(time_str))
                if match:
                    hours = int(match.group(1))
                    minutes = int(match.group(2))
                    seconds = float(match.group(3))
                    total_sec = hours * 3600 + minutes * 60 + seconds
                    total_seconds.append(total_sec)
            
            if total_seconds:
                # Calcular promedio
                avg_seconds = sum(total_seconds) / len(total_seconds)
                hours = int(avg_seconds // 3600)
                minutes = int((avg_seconds % 3600) // 60)
                seconds = avg_seconds % 60
                return f"{hours}:{minutes:02d}:{seconds:06.3f}"
        
        # Si no se pueden analizar los tiempos existentes, usar un tiempo típico de F1
        return "1:32:15.000"  # Tiempo promedio típico de una carrera de F1
    
    def _clean_string_nulls(self):
        """
        Limpia valores que pueden estar representados como strings pero son efectivamente nulos
        """
        null_representations = ['null', 'NULL', 'Null', 'nan', 'NaN', 'NAN', 'n/a', 'N/A', '']
        
        for col in self.data.columns:
            if self.data[col].dtype == 'object':  # Solo para columnas de texto
                # Reemplazar representaciones de null con valores apropiados
                mask = self.data[col].isin(null_representations)
                if mask.any():
                    if col == 'TIME':
                        tiempo_promedio = self._calculate_average_race_time()
                        self.data.loc[mask, col] = tiempo_promedio
                        print(f"Reemplazados {mask.sum()} valores nulos en {col} con '{tiempo_promedio}'")
                    elif col == 'LAPS':
                        # Si LAPS es string pero debería ser numérico
                        median_laps = pd.to_numeric(self.data[col], errors='coerce').median()
                        self.data.loc[mask, col] = str(int(median_laps))
                        print(f"Reemplazados {mask.sum()} valores nulos en {col} con '{int(median_laps)}'")
                    else:
                        # Para otras columnas texto, usar 'Unknown' o el valor más común
                        mode_value = self.data[col].mode()[0] if len(self.data[col].mode()) > 0 else 'Unknown'
                        self.data.loc[mask, col] = mode_value
                        print(f"Reemplazados {mask.sum()} valores nulos en {col} con '{mode_value}'")
    
    def convert_data_types(self):
        """
        Convierte los tipos de datos a formatos más apropiados
        """
        # Convertir LAPS a entero si es posible
        try:
            self.data['LAPS'] = pd.to_numeric(self.data['LAPS'], errors='coerce').fillna(0).astype(int)
            print("Columna LAPS convertida a tipo entero")
        except:
            print("No se pudo convertir LAPS a entero")
        
        # Convertir DATE a datetime con manejo correcto de años de 2 dígitos
        try:
            # Función para convertir fechas con años de 2 dígitos correctamente
            def parse_f1_date(date_str):
                import datetime
                try:
                    # Parsear la fecha asumiendo formato dd-mmm-yy
                    parsed_date = pd.to_datetime(date_str, format='%d-%b-%y', errors='coerce')
                    if pd.isna(parsed_date):
                        return parsed_date
                    
                    # Si el año resulta mayor a 2030, asumimos que es del siglo XX
                    if parsed_date.year > 2030:
                        # Convertir de 20xx a 19xx
                        corrected_year = parsed_date.year - 100
                        parsed_date = parsed_date.replace(year=corrected_year)
                    
                    return parsed_date
                except:
                    return pd.NaT
            
            self.data['DATE'] = self.data['DATE'].apply(parse_f1_date)
            print("Columna DATE convertida a tipo datetime con corrección de años")
        except Exception as e:
            print(f"No se pudo convertir DATE a datetime: {e}")
    
    def get_cleaned_data(self):
        """
        Retorna el DataFrame limpio
        
        Returns:
            pd.DataFrame: DataFrame con los datos limpios
        """
        return self.data
    
    def get_cleaning_summary(self):
        """
        Retorna un resumen de las operaciones de limpieza realizadas
        
        Returns:
            dict: Resumen de la limpieza
        """
        original_missing = self.original_data.isnull().sum().sum()
        current_missing = self.data.isnull().sum().sum()
        
        summary = {
            'original_missing_values': original_missing,
            'current_missing_values': current_missing,
            'values_cleaned': original_missing - current_missing,
            'original_shape': self.original_data.shape,
            'current_shape': self.data.shape,
            'rows_preserved': self.original_data.shape[0] == self.data.shape[0]
        }
        
        return summary
    
    def full_cleaning_process(self):
        """
        Ejecuta el proceso completo de limpieza:
        1. Reporta datos faltantes
        2. Limpia valores faltantes
        3. Convierte tipos de datos
        4. Muestra resumen final
        
        Returns:
            pd.DataFrame: DataFrame limpio
        """
        print("INICIANDO PROCESO COMPLETO DE LIMPIEZA")
        print("=" * 50)
        
        # 1. Mostrar reporte inicial
        self.display_missing_data_report()
        
        # 2. Limpiar valores faltantes
        print("\n" + "=" * 50)
        self.clean_missing_values()
        
        # 3. Convertir tipos de datos
        print("\n" + "=" * 50)
        print("Convirtiendo tipos de datos...")
        self.convert_data_types()
        
        # 4. Mostrar resumen final
        print("\n" + "=" * 50)
        print("RESUMEN FINAL DE LIMPIEZA")
        print("=" * 50)
        summary = self.get_cleaning_summary()
        print(f"Valores faltantes originales: {summary['original_missing_values']}")
        print(f"Valores faltantes actuales: {summary['current_missing_values']}")
        print(f"Valores limpiados: {summary['values_cleaned']}")
        print(f"Filas preservadas: {summary['rows_preserved']}")
        print(f"Shape original: {summary['original_shape']}")
        print(f"Shape actual: {summary['current_shape']}")
        
        # Verificación final
        final_missing = self.check_missing_values()
        print(f"\nVerificación final - Total valores nulos: {sum(final_missing['null_values'].values())}")
        
        return self.data
    
    def export_cleaned_data(self, file_path):
        """
        Exporta los datos limpios a un archivo CSV
        
        Args:
            file_path (str): Ruta donde guardar el archivo CSV limpio
        """
        try:
            self.data.to_csv(file_path, index=False)
            print(f"Datos limpios exportados exitosamente a: {file_path}")
        except Exception as e:
            print(f"Error al exportar los datos: {e}")