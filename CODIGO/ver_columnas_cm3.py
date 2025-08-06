import pandas as pd

# Leer archivo para ver todas las columnas
ruta = r"c:\Users\daniel.prieto.r.UMD\uniminuto.edu\G- Storage OEDE - VAC - Documentos\VICERRECTORIA ACADÉMICA\5_PROYECTOS_DATA\DESARROLLOS\CUADROS_MAESTROS\REPOSITORIO_CM\CMd 3 - Profesores.xlsx"

df = pd.read_excel(ruta, sheet_name='3A-2P', header=2)

print("=== TODAS LAS COLUMNAS DE 3A-2P ===")
for i, col in enumerate(df.columns):
    print(f"{i:2d}: {col}")

print(f"\nTotal columnas: {len(df.columns)}")

# Mostrar una muestra de datos del programa 2051
df_2051 = df[df['Snies'] == 2051]
print(f"\nRegistros para programa 2051: {len(df_2051)}")
if len(df_2051) > 0:
    print("\nPrimera fila de datos:")
    primera_fila = df_2051.iloc[0]
    for i, (col, val) in enumerate(primera_fila.items()):
        print(f"{i:2d}: {col} = {val}")
