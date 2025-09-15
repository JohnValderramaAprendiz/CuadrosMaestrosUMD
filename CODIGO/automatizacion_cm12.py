import openpyxl
import os

def generar_reporte_inmuebles(codigo_programa, base_path):
    """
    Automatiza el llenado de la plantilla CM-12 (Inmuebles) realizando
    múltiples copias de bloques y celdas desde el archivo de datos.
    El 'codigo_programa' se recibe por compatibilidad con la API, pero no se utiliza.
    """
    print(f"--- INICIANDO PROCESO PARA CM-12: INMUEBLES (CÓDIGO RECIBIDO: {codigo_programa}) ---")

    # --- 1. Definición de rutas ---
    ruta_datos = os.path.join(base_path, 'REPOSITORIO_CM', 'CMd12- Inmuebles.xlsx')
    ruta_plantilla = os.path.join(base_path, 'REPOSITORIO_PLANTILLAS_CM', 'CM 12 - Inmuebles.xlsx')
    ruta_salida = os.path.join(base_path, 'RESULTADOS')

    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)

    try:
        # --- 2. Cargar ambos libros de trabajo ---
        wb_datos = openpyxl.load_workbook(ruta_datos, data_only=True)
        sheet_datos = wb_datos.active

        wb_plantilla = openpyxl.load_workbook(ruta_plantilla)
        sheet_plantilla = wb_plantilla.active
        print("Archivos de datos y plantilla cargados correctamente.")

    except FileNotFoundError as e:
        return None, f"No se encontró el archivo: {e.filename}"

    # --- 3. Bucle para el primer bloque (B2:I13) ---
    print("Copiando bloque principal de datos (filas 2 a 13)...")
    columnas_origen_bloque1 = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    columnas_destino_bloque1 = ['C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    for fila_origen in range(2, 14):
        fila_destino = fila_origen - 2 + 27
        for i in range(len(columnas_origen_bloque1)):
            celda_origen = f"{columnas_origen_bloque1[i]}{fila_origen}"
            celda_destino = f"{columnas_destino_bloque1[i]}{fila_destino}"
            sheet_plantilla[celda_destino] = sheet_datos[celda_origen].value
    
    # --- 4. Copia de columnas adicionales (B16:E18) con mapeo específico ---
    print("Copiando datos adicionales de columnas específicas (filas 16 a 18)...")
    column_map_adicional = {'B': 'C', 'C': 'E', 'D': 'G', 'E': 'I'}
    for col_origen, col_destino in column_map_adicional.items():
        for fila_origen in range(16, 19):
            fila_destino = fila_origen - 16 + 43
            celda_origen = f"{col_origen}{fila_origen}"
            celda_destino = f"{col_destino}{fila_destino}"
            sheet_plantilla[celda_destino] = sheet_datos[celda_origen].value

    # --- 5. Copia de celda individual (B20) ---
    print("Copiando dato intermedio (celda B20)...")
    sheet_plantilla['C47'] = sheet_datos['B20'].value

    # --- 6. Copia de celdas finales (fila 23 a 55) ---
    print("Copiando bloque final de datos (fila 23)...")
    map_celdas_finales = {
        'A23': 'C55',
        'B23': 'E55',
        'C23': 'G55',
        'D23': 'I55',
        'E23': 'K55'
    }
    for celda_origen, celda_destino in map_celdas_finales.items():
        sheet_plantilla[celda_destino] = sheet_datos[celda_origen].value

    # --- 7. Guardar el resultado ---
    nombre_final = f"CM_12_generado_FINAL_COMPLETO.xlsx"
    ruta_final = os.path.join(ruta_salida, nombre_final)
    wb_plantilla.save(ruta_final)
    print(f"¡Proceso completado! Archivo guardado en: {ruta_final}")

    return ruta_final, None

# --- BLOQUE PARA EJECUTAR EL SCRIPT DIRECTAMENTE (NO SE USA CON LA API) ---
if __name__ == '__main__':
    print("--- MODO DE PRUEBA: Ejecutando script de forma local ---")
    
    ruta_principal_del_proyecto = r"C:\Users\daniel.prieto.r.UMD\uniminuto.edu\G- Storage OEDE - VAC - Documentos\VICERRECTORIA ACADÉMICA\5_PROYECTOS_DATA\DESARROLLOS\CUADROS_MAESTROS"

    # Se simula un código de programa, aunque no se use en la función
    codigo_simulado = 99999 

    resultado, error = generar_reporte_inmuebles(
        codigo_programa=codigo_simulado,
        base_path=ruta_principal_del_proyecto
    )

    if resultado:
        print(f"\n✅ ¡PRUEBA EXITOSA! Archivo generado en: {resultado}")
    else:
        print(f"\n❌ ERROR EN LA PRUEBA: {error}")