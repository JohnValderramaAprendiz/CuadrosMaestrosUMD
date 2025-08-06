import pandas as pd
import openpyxl
import os

def generar_reporte_profesores(codigo_programa, base_path):
    """
    Automatiza el llenado de la plantilla CM-3 (Profesores) para un programa.
    Implementación modular que comenzará con 3A-2P y se expandirá gradualmente.
    """
    print(f"--- INICIANDO PROCESO PARA CM-3: PROFESORES ---")
    print(f"Programa a procesar (SNIES): {codigo_programa}")

    # --- Definición de rutas ---
    ruta_datos = os.path.join(base_path, 'REPOSITORIO_CM', 'CMd 3 - Profesores.xlsx')
    ruta_plantilla = os.path.join(base_path, 'REPOSITORIO_PLANTILLAS_CM', 'CM 3 - Profesores.xlsx')
    ruta_salida = os.path.join(base_path, 'RESULTADOS')

    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)

    # --- 1. Leer datos y determinar períodos ---
    print("Leyendo datos de profesores...")
    
    # Leer pestaña 3A-2P (por ahora la única disponible)
    # Los encabezados están en la fila 2 (índice 2)
    try:
        df_3a = pd.read_excel(ruta_datos, sheet_name='3A-2P', header=2)
        print(f"Columnas disponibles en 3A-2P: {list(df_3a.columns)}")
        print(f"Dimensiones de datos: {df_3a.shape}")
    except Exception as e:
        return None, f"Error al leer la pestaña 3A-2P: {str(e)}"

    # --- 2. Filtrar datos por código SNIES ---
    # Buscar la columna correcta para el código SNIES
    posibles_columnas = ['Snies', 'SNIES', 'Codigo', 'Código', 'Código SNIES actual vigente']
    columna_codigo = None
    
    for col in posibles_columnas:
        if col in df_3a.columns:
            columna_codigo = col
            print(f"Usando columna: '{columna_codigo}' para filtrar en 3A-2P")
            break
    
    if columna_codigo is None:
        return None, f"No se encontró columna de código SNIES en 3A-2P. Columnas disponibles: {list(df_3a.columns)}"
    
    df_programa_3a = df_3a[df_3a[columna_codigo] == codigo_programa]
    
    if df_programa_3a.empty:
        return None, f"No se encontraron datos para el programa {codigo_programa} en 3A-2P."

    # --- 3. Determinar si es 2P o 3P ---
    max_periodo = df_programa_3a['Periodo'].max() if 'Periodo' in df_programa_3a.columns else 2
    print(f"Máximo período encontrado: {max_periodo}")
    
    # --- 4. Procesar según el período ---
    if max_periodo <= 2:
        resultado = procesar_pestanas_2P(codigo_programa, df_programa_3a, ruta_plantilla, ruta_salida)
    else:
        # TODO: Implementar cuando tengamos datos de 3P
        return None, "Procesamiento de 3 períodos aún no implementado"
    
    return resultado, None

def procesar_pestanas_2P(codigo_programa, df_programa_3a, ruta_plantilla, ruta_salida):
    """
    Procesa las pestañas para programas de 2 períodos.
    Por ahora solo 3A-2P, se expandirá gradualmente.
    """
    print("Procesando pestañas para 2 períodos...")
    
    # --- Cargar plantilla ---
    wb = openpyxl.load_workbook(ruta_plantilla)
    
    # --- Procesar 3A-2P ---
    procesar_pestaña_3A_2P(df_programa_3a, wb)
    
    # TODO: Agregar otras pestañas cuando estén disponibles
    # procesar_pestaña_3B_2P(df_programa_3b, wb)
    # procesar_pestaña_3C_2P(df_programa_3c, wb)
    # etc...
    
    # --- Guardar resultado ---
    final_filename = os.path.join(ruta_salida, f"FINAL_CM_3_generado_para_{codigo_programa}.xlsx")
    wb.save(final_filename)
    print(f"Archivo guardado: {final_filename}")
    
    return final_filename

def procesar_pestaña_3A_2P(df_programa_3a, wb):
    """
    Procesa específicamente la pestaña 3A-2P de la plantilla.
    Mapeo: D43 = TC P1 2010, D44 = TC P2 2010
    Base de datos: Columna E = TC, desde fila 4
    """
    print("Procesando pestaña 3A-2P...")
    print(f"Datos disponibles: {len(df_programa_3a)} registros")
    
    # --- Mostrar estructura de datos para debugging ---
    print(f"Columnas en datos: {list(df_programa_3a.columns)}")
    if len(df_programa_3a) > 0:
        print(f"Primeras filas de datos:")
        print(df_programa_3a.head())
    
    # --- Agrupar y sumar datos por Año y Periodo ---
    if 'Año' in df_programa_3a.columns and 'Periodo' in df_programa_3a.columns:
        # Definir columnas numéricas para sumar (empezando con TC en columna E)
        columnas_numericas = []
        for col in df_programa_3a.columns:
            if df_programa_3a[col].dtype in ['int64', 'float64'] and col not in ['Año', 'Periodo']:
                columnas_numericas.append(col)
        
        print(f"Columnas numéricas identificadas: {columnas_numericas}")
        
        df_agregado = df_programa_3a.groupby(['Año', 'Periodo'])[columnas_numericas].sum().reset_index()
        df_agregado['Año'] = df_agregado['Año'].astype(int)
        df_agregado['Periodo'] = df_agregado['Periodo'].astype(int)
        print(f"Datos agrupados: {len(df_agregado)} registros")
        print("Datos agrupados:")
        print(df_agregado)
    else:
        print("Advertencia: No se encontraron columnas Año/Periodo para agrupar")
        df_agregado = df_programa_3a
    
    # --- Seleccionar pestaña en la plantilla ---
    sheet_name = '3A-2P'  # Para 2 períodos
    if sheet_name in wb.sheetnames:
        sheet = wb[sheet_name]
        print(f"Escribiendo en pestaña: {sheet_name}")
    else:
        print(f"Advertencia: No se encontró la pestaña {sheet_name} en la plantilla")
        return
    
    # --- Mapeo completo de columnas según instrucciones del usuario ---
    # Patrón: TC,MT,TP se repite 4 veces en columnas D-O de la plantilla
    # Datos: TC(4), MT(5), TP(6), TC.1(7), MT.1(8), TP.1(9), TC.2(10), MT.2(11), TP.2(12), TC.3(13), MT.3(14), TP.3(15)
    column_map = {
        # Grupo 1: D, E, F
        'TC': 'D',
        'MT': 'E', 
        'TP': 'F',
        # Grupo 2: G, H, I
        'TC.1': 'G',
        'MT.1': 'H',
        'TP.1': 'I',
        # Grupo 3: J, K, L
        'TC.2': 'J',
        'MT.2': 'K',
        'TP.2': 'L',
        # Grupo 4: M, N, O
        'TC.3': 'M',
        'MT.3': 'N',
        'TP.3': 'O'
    }
    
    print(f"Mapeo completo configurado: {len(column_map)} columnas")
    print("Columnas mapeadas:")
    for col_datos, col_excel in column_map.items():
        print(f"  '{col_datos}' → '{col_excel}'")
    
    # --- Lógica de escritura dinámica ---
    for index, data_row in df_agregado.iterrows():
        año = data_row['Año']
        periodo = data_row['Periodo']
        
        # Fórmula: D43 = P1 2010, D44 = P2 2010
        # Fila = 43 + (año - 2010) * 2 + (periodo - 1)
        target_row = 43 + (año - 2010) * 2 + (periodo - 1)
        
        print(f"Escribiendo datos para {año}-P{periodo} en fila {target_row}")
        
        # Escribir cada columna mapeada
        for col_datos, col_excel in column_map.items():
            if col_datos in data_row:
                valor = data_row[col_datos]
                celda = f"{col_excel}{target_row}"
                sheet[celda] = valor
                print(f"  {celda} = {valor} (de columna '{col_datos}')")
    
    print("Pestaña 3A-2P procesada con mapeo inicial de TC")

# --- CÓDIGO PRINCIPAL PARA EJECUTAR ---
if __name__ == '__main__':
    programa_a_buscar = 2051
    ruta_principal = r"C:\Users\daniel.prieto.r.UMD\uniminuto.edu\G- Storage OEDE - VAC - Documentos\VICERRECTORIA ACADÉMICA\5_PROYECTOS_DATA\DESARROLLOS\CUADROS_MAESTROS"
    resultado, mensaje_error = generar_reporte_profesores(
        codigo_programa=programa_a_buscar,
        base_path=ruta_principal
    )
    if resultado:
        print(f"\n¡PROCESO COMPLETADO! Archivo guardado en: {resultado}")
    else:
        print(f"\nError: {mensaje_error}")
