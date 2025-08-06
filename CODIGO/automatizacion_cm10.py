import pandas as pd
import openpyxl
import os

def generar_reporte_proyeccion_social(codigo_programa, base_path):
    """
    Automatiza el llenado de la plantilla CM-10 (Proyectos de proyección social) para un programa.
    Mapeo directo registro por registro, empezando en fila 27.
    """
    print(f"--- INICIANDO PROCESO PARA CM-10: PROYECTOS DE PROYECCIÓN SOCIAL ---")
    print(f"Programa a procesar (SNIES): {codigo_programa}")

    # --- Definición de rutas ---
    ruta_datos = os.path.join(base_path, 'REPOSITORIO_CM', 'CMd10 - Proyectos de proyección social.xlsx')
    ruta_plantilla = os.path.join(base_path, 'REPOSITORIO_PLANTILLAS_CM', 'CM 10 - Proyectos de proyección social.xlsx')
    ruta_salida = os.path.join(base_path, 'RESULTADOS')

    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)

    # --- 1. Leer datos ---
    print("Leyendo datos de proyectos de proyección social...")
    
    try:
        df_proyectos = pd.read_excel(ruta_datos, sheet_name='10', header=0)
        print(f"Columnas disponibles: {list(df_proyectos.columns)}")
        print(f"Dimensiones totales: {df_proyectos.shape}")
    except Exception as e:
        return None, f"Error al leer los datos: {str(e)}"

    # --- 2. Filtrar datos por código SNIES ---
    # Buscar la columna correcta para el código SNIES
    posibles_columnas = ['SNIES', 'SNIES ', 'Snies', 'Codigo', 'Código']
    columna_codigo = None
    
    for col in posibles_columnas:
        if col in df_proyectos.columns:
            columna_codigo = col
            print(f"Usando columna: '{columna_codigo}' para filtrar")
            break
    
    if columna_codigo is None:
        return None, f"No se encontró columna de código SNIES. Columnas disponibles: {list(df_proyectos.columns)}"
    
    df_programa = df_proyectos[df_proyectos[columna_codigo] == codigo_programa]
    
    if df_programa.empty:
        return None, f"No se encontraron datos para el programa {codigo_programa}."

    print(f"Registros encontrados para el programa {codigo_programa}: {len(df_programa)}")
    
    # --- Mostrar muestra de datos para debugging ---
    if len(df_programa) > 0:
        print("Primeras filas de datos del programa:")
        print(df_programa.head())

    # --- 3. Cargar plantilla ---
    try:
        wb = openpyxl.load_workbook(ruta_plantilla)
        # Buscar la pestaña correcta (podría ser '10', 'Hoja1', etc.)
        if '10' in wb.sheetnames:
            sheet = wb['10']
        else:
            sheet = wb.active
        print(f"Escribiendo en pestaña: {sheet.title}")
    except Exception as e:
        return None, f"Error al cargar la plantilla: {str(e)}"

    # --- 4. Mapeo de columnas según instrucciones ---
    column_map = {
        # Columna de datos → Columna de plantilla
        'Año': 'B',
        'Nombre de proyecto de extensión': 'C',
        'Coordinadores': 'D',
        'Profesores': 'E',
        'Profesionales de planta': 'F',
        'Estudiante': 'G',
        'N° beneficiarios': 'I',
        'Detalle de la población beneficiaria': 'J',
        'Propia': 'K',
        'Nacional': 'L',
        'Internacional': 'M'
    }
    
    # Identificar columnas reales en los datos (pueden tener espacios o variaciones)
    columnas_encontradas = {}
    for col_objetivo, col_excel in column_map.items():
        # Buscar la columna más similar en los datos
        for col_real in df_programa.columns:
            col_real_clean = str(col_real).strip()
            if col_objetivo.lower() in col_real_clean.lower() or col_real_clean.lower() in col_objetivo.lower():
                columnas_encontradas[col_real] = col_excel
                print(f"Mapeo identificado: '{col_real}' → '{col_excel}'")
                break
    
    print(f"Total columnas mapeadas: {len(columnas_encontradas)}")

    # --- 5. Copiar fila de plantilla y escribir datos ---
    fila_inicio = 27  # Empezar en fila 27 según instrucciones
    fila_plantilla = 27  # Fila de referencia con formato
    
    for index, (_, data_row) in enumerate(df_programa.iterrows()):
        fila_actual = fila_inicio + index
        
        print(f"Escribiendo registro {index + 1} en fila {fila_actual}")
        
        # Si no es la primera fila, copiar el formato de la fila plantilla
        if index > 0:
            # Copiar formato de toda la fila plantilla a la fila actual
            for col_letter in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O']:
                source_cell = sheet[f"{col_letter}{fila_plantilla}"]
                target_cell = sheet[f"{col_letter}{fila_actual}"]
                
                # Copiar formato si la celda fuente tiene formato
                if source_cell.has_style:
                    target_cell.font = source_cell.font
                    target_cell.fill = source_cell.fill
                    target_cell.border = source_cell.border
                    target_cell.alignment = source_cell.alignment
                    target_cell.number_format = source_cell.number_format
        
        # Escribir cada columna mapeada
        for col_datos, col_excel in columnas_encontradas.items():
            if col_datos in data_row:
                valor = data_row[col_datos]
                # Convertir NaN a cadena vacía
                if pd.isna(valor):
                    valor = ""
                
                celda = f"{col_excel}{fila_actual}"
                sheet[celda].value = valor
                
                # Solo mostrar los primeros registros para no saturar el log
                if index < 3:
                    print(f"  {celda} = {valor}")
    
    # --- 6. Guardar resultado ---
    final_filename = os.path.join(ruta_salida, f"FINAL_CM_10_generado_para_{codigo_programa}.xlsx")
    wb.save(final_filename)
    print(f"Archivo guardado: {final_filename}")
    print(f"Total registros procesados: {len(df_programa)}")
    
    return final_filename, None

# --- CÓDIGO PRINCIPAL PARA EJECUTAR ---
if __name__ == '__main__':
    programa_a_buscar = 2051
    ruta_principal = r"C:\Users\daniel.prieto.r.UMD\uniminuto.edu\G- Storage OEDE - VAC - Documentos\VICERRECTORIA ACADÉMICA\5_PROYECTOS_DATA\DESARROLLOS\CUADROS_MAESTROS"
    resultado, mensaje_error = generar_reporte_proyeccion_social(
        codigo_programa=programa_a_buscar,
        base_path=ruta_principal
    )
    if resultado:
        print(f"\n¡PROCESO COMPLETADO! Archivo guardado en: {resultado}")
    else:
        print(f"\nError: {mensaje_error}")
