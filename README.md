# 📊 SISTEMA DE AUTOMATIZACIÓN DE CUADROS MAESTROS - UNIMINUTO

## 🎯 **DESCRIPCIÓN DEL PROYECTO**

Sistema de automatización para la generación de Cuadros Maestros académicos en UNIMINUTO. Permite generar reportes Excel automáticamente a partir de bases de datos institucionales mediante una interfaz web moderna.

---

## 🏗️ **ARQUITECTURA DEL SISTEMA**

### **Stack Tecnológico Actual:**
- **Backend:** Python Flask + pandas + openpyxl
- **Frontend:** HTML5 + TailwindCSS + JavaScript
- **Datos:** Archivos Excel (bases de datos y plantillas)
- **API:** REST con endpoint `/generar_reporte`

### **Estructura del Proyecto:**
```
CUADROS_MAESTROS/
├── 📁 CODIGO/                    # Scripts de automatización (16 archivos)
├── 📁 REPOSITORIO_CM/            # Bases de datos Excel (5 archivos)
├── 📁 REPOSITORIO_PLANTILLAS_CM/ # Plantillas Excel (23 archivos)
├── 📁 RESULTADOS/                # Archivos generados (11 archivos)
├── 📄 principal.html             # Página principal del sistema
├── 📄 plantillas.html            # Interfaz para generar reportes
├── 📄 instructivo.html           # Documentación del sistema
├── 📄 BD_CM.xlsx                 # Base de datos principal
├── 📄 Encargados CM.xlsx         # Información de responsables
└── 📄 README.md                  # Este archivo
```

---

## ✅ **PLANTILLAS AUTOMATIZADAS (5 COMPLETADAS)**

### **CM-1 - Identificación** ✅
- **Tipo:** Mapeo directo (formulario)
- **Fuente:** `CMd 1 - Promociones - Graduados.xlsx`
- **Lógica:** Datos de `Data_programas` y `Data_CM1` → celdas específicas
- **Características:**
  - Mapeo de 23 columnas de información institucional
  - Lógica condicional para "Referentes de organización"
  - Conteo de promociones y suma de graduados
- **Estado:** ✅ Completamente funcional e integrado

### **CM-3 - Profesores** ✅
- **Tipo:** Mapeo por grupos (TC, MT, TP x 4 categorías)
- **Fuente:** `CMd 3 - Profesores.xlsx`
- **Lógica:** Agrupación por Año/Período → columnas D-O
- **Características:**
  - Mapeo de 12 columnas (TC, MT, TP y sus variantes .1, .2, .3)
  - Fórmula dinámica: `43 + (año - 2010) * 2 + (periodo - 1)`
  - Solo implementada pestaña 3A-2P (expandible a 3B, 3C, etc.)
- **Estado:** ✅ Funcional (pestaña 3A-2P)

### **CM-9 - Prácticas** ✅
- **Tipo:** Agrupación temporal (preexistente)
- **Fuente:** Base de datos de prácticas
- **Lógica:** Suma por Año/Período → pestañas 2P/3P
- **Estado:** ✅ Funcional desde antes del proyecto

### **CM-10 - Proyección Social** ✅ 🆕
- **Tipo:** Registro por registro (tabla)
- **Fuente:** `CMd10 - Proyectos de proyección social.xlsx`
- **Lógica:** Cada proyecto = 1 fila desde B27
- **Características:**
  - Mapeo de 11 columnas (Año, Nombre, Coordinadores, etc.)
  - 118 registros procesados para programa ejemplo (2051)
  - Mapeo: B=Año, C=Nombre, D=Coordinadores, E=Profesores, F=Profesionales, G=Estudiantes, I=Beneficiarios, J=Población, K=Propia, L=Nacional, M=Internacional
- **Estado:** ✅ Funcional (formato básico)

### **CM-20 - Becas, Subsidios y Patrocinios** ✅
- **Tipo:** Agrupación temporal (preexistente)
- **Fuente:** Base de datos de becas
- **Lógica:** Suma por Año/Período → pestañas 2P/3P
- **Estado:** ✅ Funcional desde antes del proyecto

---

## 💻 **COMPONENTES TÉCNICOS**

### **Backend (Python Flask):**
- **`api_backend.py`** - API REST principal
- **`automatizacion_cm01.py`** - Script para CM-1 Identificación
- **`automatizacion_cm03.py`** - Script para CM-3 Profesores
- **`automatizacion_cm09.py`** - Script para CM-9 Prácticas
- **`automatizacion_cm10.py`** - Script para CM-10 Proyección Social
- **`automatizacion_cm20.py`** - Script para CM-20 Becas

### **Frontend (HTML/CSS/JS):**
- **`plantillas.html`** - Interfaz principal con 5 tarjetas de plantillas
- **`principal.html`** - Página de bienvenida corporativa
- **Estilo:** TailwindCSS con diseño UNIMINUTO

### **API REST:**
```http
POST /generar_reporte
Content-Type: application/json

{
  "plantilla": 1,  // 1, 3, 9, 10, 20
  "codigo": 2051   // Código SNIES del programa
}
```

---

## 🚀 **FUNCIONALIDADES ACTUALES**

### **Sistema Web Completo:**
1. **Interfaz gráfica** moderna para seleccionar plantillas
2. **Formulario modal** para ingresar código SNIES
3. **Generación automática** de reportes Excel
4. **Descarga directa** de archivos generados
5. **Manejo de errores** y validaciones

### **Automatización Robusta:**
- **Filtrado inteligente** por código SNIES
- **Mapeo automático** de columnas con variaciones de nombres
- **Manejo de datos faltantes** (NaN → cadena vacía)
- **Debugging completo** con logs detallados
- **Agrupación temporal** para plantillas que lo requieren

---

## 📈 **ROADMAP DE DESARROLLO**

### ✅ **FASE 1 - AUTOMATIZACIÓN (80% COMPLETADA)**
- ✅ 5 plantillas automatizadas y funcionales
- ✅ Sistema web con interfaz moderna
- ✅ API backend robusta e integrada
- 🔄 **Pendiente:** Más plantillas (CM-2, CM-4, CM-5, CM-6, etc.)
- 🔄 **Pendiente:** Expandir CM-3 a todas las pestañas (3B-2P, 3C-2P, etc.)

### 📋 **FASE 2 - MIGRACIÓN A BASE DE DATOS (PENDIENTE)**
- Diseñar esquema relacional para datos
- Migrar datos de Excel → SQL Database
- Optimizar consultas y rendimiento
- Mantener compatibilidad con sistema actual

### ☁️ **FASE 3 - MIGRACIÓN A AZURE (PENDIENTE)**
- **Azure SQL Database** para datos relacionales
- **CosmosDB** para plantillas y configuraciones
- **Azure App Service** para frontend y API
- **Azure Storage** para archivos generados

### 🔧 **FASE 4 - OPTIMIZACIÓN (PENDIENTE)**
- Implementar cache para consultas frecuentes
- Añadir autenticación y autorización
- Dashboard de estadísticas y uso
- Notificaciones automáticas

---

## 🎉 **LOGROS PRINCIPALES**

1. **✅ Sistema completamente funcional** con 5 plantillas automatizadas
2. **✅ Interfaz web moderna** y fácil de usar
3. **✅ API REST robusta** con manejo completo de errores
4. **✅ Arquitectura escalable** para agregar nuevas plantillas
5. **✅ Documentación completa** del proceso y código
6. **✅ Integración exitosa** de diferentes tipos de lógica (mapeo directo, agrupación, registro por registro)

---

## 🔧 **LIMITACIONES CONOCIDAS**

### **Técnicas:**
1. **Formato Excel:** openpyxl tiene limitaciones con formatos complejos
2. **CM-3:** Solo implementada pestaña 3A-2P (faltan 3B, 3C, 3D, 3E, 3F)
3. **Rendimiento:** Procesamiento secuencial (no paralelo)

### **Funcionales:**
1. **Plantillas pendientes:** CM-2, CM-4, CM-5, CM-6, etc.
2. **Validaciones:** Falta validación avanzada de datos de entrada
3. **Logs:** Sistema de logging básico

---

## 🛠️ **INSTALACIÓN Y USO**

### **Requisitos:**
```bash
pip install flask flask-cors pandas openpyxl
```

### **Ejecución:**
```bash
# Iniciar servidor API
cd CODIGO
python api_backend.py

# Abrir navegador en:
# http://localhost:5000 (API)
# Abrir plantillas.html en navegador (Frontend)
```

### **Uso:**
1. Abrir `plantillas.html` en navegador
2. Seleccionar plantilla deseada (CM-1, CM-3, CM-9, CM-10, CM-20)
3. Ingresar código SNIES del programa
4. Hacer clic en "Generar"
5. Descargar archivo Excel generado

---

## 📊 **ESTADÍSTICAS DEL PROYECTO**

- **📁 Directorios:** 4 principales
- **📄 Archivos de código:** 16 scripts Python
- **📊 Bases de datos:** 5 archivos Excel
- **📋 Plantillas:** 23 plantillas Excel
- **🎯 Plantillas automatizadas:** 5 (CM-1, CM-3, CM-9, CM-10, CM-20)
- **⚡ Funcionalidad:** Sistema web completo con API REST

---

## 👥 **EQUIPO DE DESARROLLO**

- **Institución:** UNIMINUTO - Vicerrectoría Académica
- **Proyecto:** Automatización de Cuadros Maestros
- **Tecnología:** Python Flask + Excel + Web

---

## 📝 **BITÁCORA DE CAMBIOS**

### **2025-08-06**
- ✅ **CM-10 Proyección Social** implementado y funcional
- ✅ Integración completa en API y frontend
- ✅ Procesamiento de 118 registros para programa 2051
- ✅ Mapeo de 11 columnas con lógica registro por registro
- ⚠️ Limitación de formato Excel identificada y documentada

### **2025-08-05**
- ✅ **CM-3 Profesores** implementado para pestaña 3A-2P
- ✅ Mapeo completo de 12 columnas (TC, MT, TP x 4 grupos)
- ✅ Fórmula dinámica de filas implementada
- ✅ Integración en API y frontend completada

### **Anteriormente**
- ✅ **CM-1 Identificación** completamente implementado
- ✅ Sistema base con CM-9 y CM-20 preexistentes
- ✅ Arquitectura web y API establecida

---

## 🔮 **PRÓXIMOS PASOS**

1. **Implementar CM-2 Estudiantes** (siguiente prioridad)
2. **Expandir CM-3** a todas las pestañas (3B-2P, 3C-2P, etc.)
3. **Mejorar formato Excel** (plantillas pre-formateadas)
4. **Agregar más plantillas** según prioridades institucionales
5. **Planificar migración** a base de datos relacional

---

*Última actualización: 2025-08-06*
*Sistema en producción y funcionando correctamente* ✅
