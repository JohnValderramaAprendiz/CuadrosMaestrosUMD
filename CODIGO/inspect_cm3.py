import pandas as pd

# Leer archivo sin encabezados para ver estructura real
ruta = r"c:\Users\daniel.prieto.r.UMD\uniminuto.edu\G- Storage OEDE - VAC - Documentos\VICERRECTORIA ACADÉMICA\5_PROYECTOS_DATA\DESARROLLOS\CUADROS_MAESTROS\REPOSITORIO_CM\CMd 3 - Profesores.xlsx"

print("=== INSPECCIONANDO ESTRUCTURA DEL ARCHIVO CM-3 ===")

df = pd.read_excel(ruta, sheet_name='3A-2P', header=None)
print(f"Dimensiones: {df.shape}")
print("\nPrimeras 10 filas para ver encabezados:")
for i in range(min(10, len(df))):
    fila = df.iloc[i].tolist()
    print(f"Fila {i}: {fila}")

print("\n=== BUSCANDO PROGRAMA 2051 ===")
# Buscar donde aparece 2051 y mostrar algunas filas alrededor
for i in range(len(df)):
    fila = df.iloc[i].tolist()
    if 2051 in fila:
        print(f"\nPrograma 2051 encontrado en fila {i}:")
        # Mostrar esta fila y las siguientes 3
        for j in range(i, min(i+4, len(df))):
            fila_contexto = df.iloc[j].tolist()
            print(f"  Fila {j}: {fila_contexto}")
        break

print("\n=== IDENTIFICANDO ENCABEZADOS ===")
# Los encabezados probablemente están en las primeras filas
# Vamos a ver si podemos identificar la estructura
print("Buscando fila de encabezados que contenga 'TC', 'MT', 'Año', 'Periodo'...")
for i in range(min(10, len(df))):
    fila = [str(x).upper() if pd.notna(x) else '' for x in df.iloc[i].tolist()]
    if any(keyword in ' '.join(fila) for keyword in ['TC', 'MT', 'AÑO', 'PERIODO', 'SNIES']):
        print(f"Posible fila de encabezados en {i}: {df.iloc[i].tolist()}")
