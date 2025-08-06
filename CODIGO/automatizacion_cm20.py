import pandas as pd
import openpyxl
import os

def generar_reporte_final_con_condicional(codigo_programa, base_path):
    """
    Versión final corregida que maneja errores en la columna 'Periodo'
    y es compatible con la API.
    """
    print(f"--- INICIANDO PROCESO FINAL CON LÓGICA CONDICIONAL (CORREGIDO) ---")
    print(f"Programa a procesar: {codigo_programa}")

    # --- Definición de rutas ---
    ruta_datos = os.path.join(base_path, 'REPOSITORIO_CM', 'CMd 20 - Becas, subsidios, descuentos y patrocinios.xlsx')
    ruta_plantilla = os.path.join(base_path, 'REPOSITORIO_PLANTILLAS_CM', 'CM 20 - Becas, subsidios, descuentos y patrocinios.xlsx')
    ruta_salida = os.path.join(base_path, 'RESULTADOS')

    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)

    # --- 1. Leer y filtrar datos ---
    print("Leyendo archivo de datos...")
    df_fuente = pd.read_excel(ruta_datos)
    
    # ¡IMPORTANTE! Revisa en tu Excel si la columna se llama 'Snies' o 'Código' y usa el nombre correcto aquí.
    # El archivo original usaba 'Snies'.
    columna_programa = 'Código' 
    df_programa = df_fuente[df_fuente[columna_programa] == codigo_programa].copy()

    if df_programa.empty:
        return None, f"No se encontraron datos para el programa {codigo_programa} usando la columna '{columna_programa}'."

    # --- 2. Agrupar y sumar los datos ---
    print("Agrupando y sumando datos por Año y Periodo...")
    columnas_para_sumar = [
        'Subsidio', 'Beca', 'Descuento Total', 'Patrocinio',
        'Subsidios ($)', 'Becas ($)', 'Descuentos ($)', 'Patrocinios ($)'
    ]
    df_agregado = df_programa.groupby(['Año', 'Periodo'])[columnas_para_sumar].sum().reset_index()
    
    # --- !! CORRECCIÓN APLICADA AQUÍ !! ---
    # Se limpia la columna 'Periodo' extrayendo solo los números antes de convertir.
    df_agregado['Año'] = df_agregado['Año'].astype(int)
    df_agregado['Periodo'] = df_agregado['Periodo'].astype(str).str.extract('(\d+)').astype(int)
    print("Datos listos para procesar.")

    # --- 3. Decidir qué pestaña usar ---
    max_periodo = df_agregado['Periodo'].max()
    sheet_name = '20-2P' if max_periodo <= 2 else '20-3P'
    print(f"Se usará la pestaña: '{sheet_name}'")

    # --- 4. Mapeo de columnas ---
    column_map = {
        'Subsidio': 'D', 'Beca': 'E', 'Descuento Total': 'F', 'Patrocinio': 'G',
        'Subsidios ($)': 'I', 'Becas ($)': 'J', 'Descuentos ($)': 'K', 'Patrocinios ($)': 'L'
    }

    # --- 5. Cargar plantilla y escribir datos ---
    print("Abriendo plantilla y escribiendo datos...")
    wb = openpyxl.load_workbook(ruta_plantilla)
    sheet = wb[sheet_name]

    # --- BUCLE DINÁMICO ---
    for index, data_row in df_agregado.iterrows():
        año = data_row['Año']
        periodo = data_row['Periodo']
        
        # --- LÓGICA CONDICIONAL PARA CALCULAR LA FILA ---
        if sheet_name == '20-2P':
            target_row = int(29 + (año - 2010) * 2 + (periodo - 1))
        else: # Si es '20-3P'
            target_row = int(58 + (año - 2020) * 3 + (periodo - 1))

        # Escribe los datos
        for col_name, excel_col in column_map.items():
            if col_name in data_row and pd.notna(data_row[col_name]):
                cell_to_write = f"{excel_col}{target_row}"
                sheet[cell_to_write] = data_row[col_name]

    # --- 6. Guardar el resultado y devolverlo a la API ---
    final_filename = os.path.join(ruta_salida, f"CM_20_generado_para_{codigo_programa}.xlsx")
    wb.save(final_filename)
    return final_filename, None