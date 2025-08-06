import pandas as pd
import openpyxl
import os

def generar_reporte_practicas(codigo_programa, base_path):
    """
    Automatiza el llenado de la plantilla CM-9 (Prácticas) para un programa,
    con los nombres de columna corregidos.
    """
    print(f"--- INICIANDO PROCESO PARA CM-9: PRÁCTICAS (CORREGIDO) ---")
    print(f"Programa a procesar (SNIES): {codigo_programa}")

    # --- Definición de rutas ---
    ruta_datos = os.path.join(base_path, 'REPOSITORIO_CM', 'CMd 9 - Prácticas.xlsx')
    ruta_plantilla = os.path.join(base_path, 'REPOSITORIO_PLANTILLAS_CM', 'CM 9 - Prácticas.xlsx')
    ruta_salida = os.path.join(base_path, 'RESULTADOS')

    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)

    # --- 1. Leer y filtrar datos ---
    print("Leyendo archivo de datos...")
    df_fuente = pd.read_excel(ruta_datos)
    df_programa = df_fuente[df_fuente['SNIES'] == codigo_programa].copy()

    if df_programa.empty:
        return None, f"No se encontraron datos para el programa {codigo_programa}."

    # --- 2. Agrupar y sumar los datos ---
    print("Agrupando y sumando datos por Año y Periodo...")
    # --- CORRECCIÓN AQUÍ: Nombres de columna actualizados ---
    columnas_para_sumar = [
        'Contrato de aprendizaje', 'Contrato laboral', 'Proyecto o convenio especial',
        'En emprendimiento', 'En investigación', 'En escenario internacional',
        'Prácticas en responsabilidad social'
    ]
    df_agregado = df_programa.groupby(['Año', 'Periodo'])[columnas_para_sumar].sum().reset_index()
    df_agregado['Año'] = df_agregado['Año'].astype(int)
    df_agregado['Periodo'] = df_agregado['Periodo'].astype(int)
    print("Datos listos para procesar.")

    # --- 3. Decidir qué pestaña usar ---
    max_periodo = df_agregado['Periodo'].max()
    sheet_name = '9-2P' if max_periodo <= 2 else '9-3P'
    print(f"Se usará la pestaña: '{sheet_name}'")

    # --- 4. Mapeo de columnas ---
    # --- CORRECCIÓN AQUÍ: Nombres de columna actualizados ---
    column_map = {
        'Contrato de aprendizaje': 'D',
        'Contrato laboral': 'E',
        'Proyecto o convenio especial': 'F',
        'En emprendimiento': 'H',
        'En investigación': 'I',
        'En escenario internacional': 'J',
        'Prácticas en responsabilidad social': 'M'
    }

    # --- 5. Cargar plantilla y escribir datos ---
    print("Abriendo plantilla y escribiendo datos...")
    wb = openpyxl.load_workbook(ruta_plantilla)
    sheet = wb[sheet_name]

    # --- Bucle dinámico ---
    for index, data_row in df_agregado.iterrows():
        año = data_row['Año']
        periodo = data_row['Periodo']
        
        # --- Lógica condicional para calcular la fila ---
        if sheet_name == '9-2P':
            # Fórmula para la hoja de 2 períodos (base año 2015, fila 28)
            target_row = int(28 + (año - 2015) * 2 + (periodo - 1))
        else: # Si es '9-3P'
            # Fórmula para la hoja de 3 períodos (base año 2015, fila 27)
            target_row = int(27 + (año - 2015) * 3 + (periodo - 1))

        # Escribe los datos de todas las columnas definidas
        for col_name, excel_col in column_map.items():
            if col_name in data_row and pd.notna(data_row[col_name]):
                cell_to_write = f"{excel_col}{target_row}"
                value = data_row[col_name]
                sheet[cell_to_write] = value

    # --- 6. Guardar el resultado ---
    final_filename = os.path.join(ruta_salida, f"FINAL_CM_9_generado_para_{codigo_programa}.xlsx")
    wb.save(final_filename)
    return final_filename, None

# --- CÓDIGO PRINCIPAL PARA EJECUTAR ---
if __name__ == '__main__':
    programa_a_buscar = 91237
    ruta_principal = r"C:\Users\daniel.prieto.r.UMD\uniminuto.edu\G- Storage OEDE - VAC - Documentos\VICERRECTORIA ACADÉMICA\5_PROYECTOS_DATA\DESARROLLOS\CUADROS_MAESTROS"
    resultado, mensaje_error = generar_reporte_practicas(
        codigo_programa=programa_a_buscar,
        base_path=ruta_principal
    )
    if resultado:
        print(f"\n¡PROCESO COMPLETADO! Archivo guardado en: {resultado}")
    else:
        print(f"\nError: {mensaje_error}")