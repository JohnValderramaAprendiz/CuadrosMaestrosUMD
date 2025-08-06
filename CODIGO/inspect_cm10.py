import pandas as pd

# Inspeccionar la estructura del archivo CM-10
ruta_datos = r"c:\Users\daniel.prieto.r.UMD\uniminuto.edu\G- Storage OEDE - VAC - Documentos\VICERRECTORIA ACADÉMICA\5_PROYECTOS_DATA\DESARROLLOS\CUADROS_MAESTROS\REPOSITORIO_CM\CMd10 - Proyectos de proyección social.xlsx"

print("=== INSPECCIONANDO ESTRUCTURA DEL ARCHIVO CM-10 ===")

# Primero, ver qué pestañas tiene el archivo
try:
    xl_file = pd.ExcelFile(ruta_datos)
    print(f"Pestañas disponibles: {xl_file.sheet_names}")
    
    # Inspeccionar cada pestaña
    for sheet_name in xl_file.sheet_names:
        print(f"\n--- PESTAÑA: {sheet_name} ---")
        
        # Leer sin encabezados para ver estructura
        df = pd.read_excel(ruta_datos, sheet_name=sheet_name, header=None)
        print(f"Dimensiones: {df.shape}")
        
        print("Primeras 5 filas:")
        for i in range(min(5, len(df))):
            fila = df.iloc[i].tolist()
            print(f"  Fila {i}: {fila}")
        
        # Buscar programa 2051 si existe
        for i in range(len(df)):
            fila = df.iloc[i].tolist()
            if 2051 in fila:
                print(f"\n  *** Programa 2051 encontrado en fila {i}: {fila}")
                break
        else:
            print(f"\n  No se encontró programa 2051 en {sheet_name}")
            
except Exception as e:
    print(f"Error al leer el archivo: {e}")

print("\n=== ANÁLISIS COMPLETADO ===")
