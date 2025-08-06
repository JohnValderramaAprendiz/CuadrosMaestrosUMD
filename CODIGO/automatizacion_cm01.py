import pandas as pd
import openpyxl
import os

def generar_reporte_cm1(codigo_programa, base_path):
    """
    Automatiza el llenado de la plantilla CM-1 (Identificación) para un programa,
    usando datos de Data_programas y Data_CM1.
    """
    print(f"--- INICIANDO PROCESO PARA CM-1: IDENTIFICACIÓN ---")
    print(f"Programa a procesar (SNIES): {codigo_programa}")

    # --- Definición de rutas ---
    ruta_datos = os.path.join(base_path, 'REPOSITORIO_CM', 'CMd 1 - Promociones - Graduados.xlsx')
    ruta_plantilla = os.path.join(base_path, 'REPOSITORIO_PLANTILLAS_CM', 'CM 1 - Identificacion.xlsx')
    ruta_salida = os.path.join(base_path, 'RESULTADOS')

    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)

    # --- 1. Leer Data_programas y filtrar ---
    print("Leyendo datos de programas...")
    df_programas = pd.read_excel(ruta_datos, sheet_name='Data_programas')
    programa_info = df_programas[df_programas['Código SNIES actual vigente'] == codigo_programa]

    if programa_info.empty:
        return None, f"No se encontraron datos para el programa {codigo_programa} en Data_programas."
    
    # --- 1.5. Leer Data_CM1 y filtrar ---
    print("Leyendo datos de CM1...")
    df_cm1 = pd.read_excel(ruta_datos, sheet_name='Data_CM1')
    
    # DEBUG: Mostrar columnas disponibles
    print(f"Columnas disponibles en Data_CM1: {list(df_cm1.columns)}")
    
    # Buscar la columna correcta para el código SNIES
    posibles_columnas = ['Código SNIES actual vigente', 'Codigo SNIES actual vigente', 'SNIES', 'Codigo', 'Código']
    columna_codigo = None
    
    for col in posibles_columnas:
        if col in df_cm1.columns:
            columna_codigo = col
            print(f"Usando columna: '{columna_codigo}' para filtrar")
            break
    
    if columna_codigo is None:
        print(f"ERROR: No se encontró ninguna columna válida para el código SNIES en Data_CM1")
        return None, f"No se encontró columna de código SNIES en Data_CM1. Columnas disponibles: {list(df_cm1.columns)}"
    
    cm1_info = df_cm1[df_cm1[columna_codigo] == codigo_programa]
    
    if cm1_info.empty:
        print(f"Advertencia: No se encontraron datos para el programa {codigo_programa} en Data_CM1.")
        num_promociones = 0
        total_graduados = 0
    else:
        # Contar TODOS los registros (filas) en Data_CM1 para el programa
        num_promociones = len(cm1_info)
        print(f"Número de promociones encontradas: {num_promociones}")
        
        # Sumar todos los graduados
        if 'Graduados' in cm1_info.columns:
            total_graduados = cm1_info['Graduados'].sum()
            print(f"Total de graduados encontrados: {total_graduados}")
        else:
            total_graduados = 0
            print("Advertencia: No se encontró la columna 'Graduados' en Data_CM1")

    # --- 2. Cargar plantilla ---
    print("Abriendo plantilla y escribiendo datos...")
    wb = openpyxl.load_workbook(ruta_plantilla)
    sheet = wb.active  # Asumiendo que usamos la primera hoja

    # --- 3. Mapeo de Data_programas ---
    # Extraer los datos del programa (primera fila encontrada)
    programa_data = programa_info.iloc[0]
    
    # Mapeo completo de Data_programas
    mapeo_programas = {
        'Nombre de la Institución': 'C10',
        'Código SNIES de la IES ofertante': 'C11',
        'Naturaleza Jurídica': 'C12',
        'Carácter Académico': 'C13',
        'Domicilio': 'C14',
        'Denominación del Programa': 'E18',
        'Código SNIES actual vigente': 'C19',
        'Es ofertado en Registro Único Si o No': 'C20',
        'Si el programa ha cambiado su código SNIES en los últimos 8 años cuál era el SNIES anterior': 'J19',
        'Código Registro único': 'J20',
        'En que modalidades se oferta': 'C21',
        'Es ofertado en Ciclo Propedéutico Si o No': 'C22',
        'Códigos SNIES y nombres de los programas vinculados en ciclo propedéutico': 'C23',
        'Unidad Académica a la que esta adscrito el Programa': 'E24',
        # Nuevos mapeos agregados
        'Año de Creación': 'E26',
        'Duración total del programa  periodos, según RC': 'E27',
        'Periodicidad de admisión': 'E28',
        'Resolución Registro Calificado (No. y Fecha)': 'K27',
        'Resolución de Acreditación (No. y Fecha)': 'K28',
        'Vigencia de la última acreditación': 'K29',
        'Resolución de modificación RC de ampliación de lugar o lugares de desarrollo (para efecto de la renovación de la acreditación), entre otros posibles modificaciones presentadas': 'K30',
        'Si el programa es ofertado en diferentes modalidades discrimine estudiantes graduados y promociones por modalidad': 'E33',
        'La IES tiene proyectado realizar o está tramitando una modificación del RC del programa en cuanto a sus modalidades de oferta o sus lugares de desarrollo (describa el cambio que se va a hacer.  Igualmente, escriba el número de proceso o de radicación con el cual dio inicio al trámite en la plataforma correspondiente)': 'E34'
    }
    
    # Escribir datos de Data_programas
    for columna_origen, celda_destino in mapeo_programas.items():
        if columna_origen in programa_data and pd.notna(programa_data[columna_origen]):
            valor = programa_data[columna_origen]
            sheet[celda_destino] = valor
            print(f"Escribiendo {columna_origen} -> {celda_destino}: {valor}")
    
    # --- Lógica condicional para Referentes de organización ---
    if 'Referentes de organización' in programa_data and pd.notna(programa_data['Referentes de organización']):
        referente = str(programa_data['Referentes de organización']).strip()
        
        # Mapeo condicional basado en el valor
        referentes_map = {
            'Campus': 'D25',
            'Seccional': 'F25', 
            'Sede': 'H25',
            'Institución Multicampus': 'J25',
            'Multicampus': 'L25'
        }
        
        # Buscar coincidencia y marcar con X
        for referente_tipo, celda in referentes_map.items():
            if referente_tipo.lower() in referente.lower():
                sheet[celda] = 'X'
                print(f"Marcando {referente_tipo} en {celda}: X")
                break  # Solo marcar la primera coincidencia
    
    # --- Lógica condicional para Acreditación o Renovación ---
    if 'Acreditación o Renovación' in programa_data and pd.notna(programa_data['Acreditación o Renovación']):
        acreditacion = str(programa_data['Acreditación o Renovación']).strip().upper()
        
        # Mapeo condicional basado en el valor
        if 'R' in acreditacion:
            sheet['N26'] = 'X'
            print(f"Marcando Renovación (R) en N26: X")
        elif 'A' in acreditacion:
            sheet['L26'] = 'X'
            print(f"Marcando Acreditación (A) en L26: X")
    
    # --- 5. Escribir datos de Data_CM1 ---
    # Número de promociones (conteo de periodos únicos)
    sheet['E31'] = num_promociones
    print(f"Escribiendo Número de promociones en E31: {num_promociones}")
    
    # Total de graduados (suma de la columna Graduados)
    sheet['E32'] = total_graduados
    print(f"Escribiendo Total de graduados en E32: {total_graduados}")

    # --- PENDIENTE: Campos de otra base de datos ---
    # TODO: Cuando tengamos la base adicional, agregar:
    # - 'Nº de estudiantes admitidos en el primer periodo' -> E29
    # - 'Nº de créditos que establece el plan de estudios vigente' -> E30
    # Estos campos NO están en Data_programas, vienen de otra fuente

    # --- 4. Guardar el resultado ---
    final_filename = os.path.join(ruta_salida, f"FINAL_CM_1_generado_para_{codigo_programa}.xlsx")
    wb.save(final_filename)
    return final_filename, None