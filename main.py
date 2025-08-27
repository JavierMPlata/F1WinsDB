from Extract.F1WinsExtract import f1dbExtract
from Limpieza.F1WinsClean import F1WinnersClean

# Extracción de datos
print("EXTRAYENDO DATOS...")
print("=" * 50)
response1 = f1dbExtract(r"F1Wins.csv")
response1.queries()

print("Primeras 5 filas de los datos extraídos:")
print(response1.response())
