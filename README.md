# 🦖 SoftSE - Sistema de Estudios Socioeconómicos

**Versión:** 0.3.0 ⭐ ACTUALIZADO  
**Autor:** DINOS Tech  
**Fecha:** 9 de diciembre de 2025

---

## 🎉 NOVEDADES VERSIÓN 0.3.0

### ✅ Nuevas Funcionalidades Implementadas

#### 1. 🏢 **Selector de Empresa Solicitante**

- Primera página del wizard con selección de empresa
- Guardado persistente en `empresas.json`
- Botón "+ Nueva" para agregar empresas dinámicamente

#### 2. 🎲 **Generador de Datos Aleatorios de Prueba**

- Botón "🎲 Generar Datos de Prueba" en el wizard
- Genera estudios completos con datos realistas en segundos
- Perfecto para testing y demos

#### 3. 📊 **Campos Cuantitativos Mejorados**

- **Historial Laboral**: Ahora usa `duracion_meses` (número) en lugar de fechas
- **Referencias**: Ahora usa `tiempo_conocerse_meses` (número)
- **Total**: 100+ campos cuantitativos para análisis estadístico

#### 4. 📈 **Sistema de Visualización con Gráficas Profesionales**

- **Nueva página**: "📊 Análisis Visual de Datos"
- **4 Tabs de análisis**:
  - 💰 **Finanzas**: Ingresos vs Gastos, Distribución de Deudas, Indicadores Clave
  - 📉 **Gastos**: Distribución mensual con gráfica de pastel
  - ⚠️ **Riesgos**: Gráfica de radar con 6 indicadores
  - 🎨 **Estilo de Vida**: Frecuencia de actividades
- **Colores profesionales** y diseño corporativo
- **7 gráficas interactivas** con matplotlib

---

## Descripción

Sistema integral de **próxima generación** para la elaboración, gestión y análisis de estudios socioeconómicos. Esta aplicación permite capturar información exhaustiva de candidatos con más de **230 campos de datos**, evaluar riesgos con justificaciones automáticas, detectar contradicciones, y generar reportes profesionales completos con **visualizaciones gráficas**.

## 🚀 Novedades de la Versión 0.2.0

### **Expansión Masiva de Datos**

- ✅ **100+ campos nuevos** distribuidos en todas las secciones
- ✅ **3 nuevas secciones**: Salud detallada, Empleo Actual, Estilo de Vida
- ✅ Información personal expandida: nacionalidad, RFC, NSS, licencia, antecedentes legales
- ✅ Salud completa: enfermedades crónicas, tratamientos, alergias, consumo de sustancias
- ✅ Familia detallada: dependientes económicos, enfermedades familiares
- ✅ Finanzas avanzadas: ahorros, tarjetas de crédito, historial de deudas

### **Justificaciones Automáticas de Riesgo**

- ✅ Cada puntaje de riesgo viene acompañado de **razones específicas**
- ✅ Ejemplos: "Gastos exceden el ingreso (105.3%)", "3 dependientes sin ingreso propio"
- ✅ Transparencia total en la evaluación de riesgos
- ✅ Incluido en todos los formatos de exportación (PDF, Word, Excel)

### **Sistema de Validación Inteligente**

- ✅ **Detección automática de contradicciones**:
  - Balance declarado vs calculado
  - Trabajo actual vs sueldo reportado
  - Vivienda propia con renta
  - Número de hijos vs menores en listado
- ✅ **Alertas en tiempo real**:
  - Gastos excesivos (>80% del ingreso)
  - Dependientes sin ingreso
  - Hacinamiento crítico
  - Falta de servicios básicos

### **Arquitectura Modular Revolucionaria**

- ✅ **Sistema de configuración de campos**: Agregar campos nuevos en 5 minutos
- ✅ **Generación automática de UI**: Sin escribir código Qt manualmente
- ✅ **Reducción del 80% en código**: De 50 líneas a 10 líneas por campo
- ✅ **Documentación completa** con ejemplos y guías paso a paso

## Características Principales

### Gestión de Estudios

- Creación de estudios socioeconómicos mediante asistente paso a paso
- Edición y actualización de estudios existentes
- Eliminación segura de registros
- Listado organizado con búsqueda y filtrado

### Captura de Información (140+ Campos)

#### **Datos Personales** (19 campos)

- Identificación completa: CURP, RFC, INE, NSS
- Nacionalidad, lugar de nacimiento
- Escolaridad completa: nivel, carrera, estado
- Licencia de conducir con tipo y vigencia
- Contactos de emergencia
- Antecedentes legales

#### **Salud e Intereses** (13 campos)

- Estado de salud general y tipo de sangre
- Enfermedades crónicas con tratamientos
- Alergias y medicamentos
- Consumo de sustancias (tabaco, alcohol, otras)
- Actividades de tiempo libre y deportes

#### **Información Familiar** (expandida)

- Composición del hogar completa
- Dependientes económicos identificados
- Enfermedades de familiares
- Ingresos por miembro
- Personas en el hogar

#### **Situación Financiera** (mejorada)

- Ingresos completos con otros ingresos
- Gastos detallados por 7+ categorías
- Ahorros e inversiones
- Tarjetas de crédito y deudas
- Balance automático con alertas

#### **Empleo Actual** (9 campos - NUEVO)

- Empresa con teléfono y dirección
- Área/Departamento
- Antigüedad
- Tipo de contrato
- Jefe directo con puesto

#### **Estilo de Vida** (7 campos - NUEVO)

- Vehículo propio (marca, modelo, año)
- Viajes en el último año
- Hobbies y pasatiempos
- Asociaciones/Clubes

#### **Vivienda y Patrimonio** (expandida)

- Condición física de la vivienda
- Mobiliario completo
- Cálculo de hacinamiento
- Seguridad del entorno
- Calidad de construcción

#### **Historial Laboral**

- Empleos anteriores con fechas
- Motivos de separación
- Referencias laborales

#### **Referencias Personales**

- Contactos con relación y antigüedad
- Teléfonos verificables

### Análisis de Riesgos con Justificaciones

Cálculo automático en **6 dimensiones** con razones específicas:

1. **Riesgo Financiero**
   - Justificaciones: balance, porcentaje de gastos, ahorros, deudas
2. **Riesgo Familiar**
   - Justificaciones: dependientes, ingresos familiares, enfermedades

3. **Riesgo de Vivienda**
   - Justificaciones: tenencia, condición, hacinamiento, servicios

4. **Riesgo Laboral**
   - Justificaciones: estabilidad, antigüedad, tipo de contrato

5. **Riesgo de Salud** (NUEVO)
   - Justificaciones: enfermedades, tratamientos, hábitos

6. **Riesgo de Estilo de Vida** (NUEVO)
   - Justificaciones: patrimonio, estabilidad, proyección

7. **Riesgo Socioeconómico Global**
   - Promedio ponderado con interpretación global

## Requisitos del Sistema

### Exportación de Reportes

Todos los formatos incluyen las nuevas secciones y justificaciones de riesgo:

#### **PDF** - Informe Profesional Completo

- Encabezado con logo de empresa
- Todas las secciones expandidas
- Tabla de riesgos con puntajes
- **Sección "JUSTIFICACIONES Y DETALLES"** con explicaciones
- Fotografías con categorías
- Formato profesional listo para imprimir

#### **Word (DOCX)** - Documento Editable

- Estructura similar al PDF
- Formato editable para personalizaciones
- Tablas con estilos predefinidos
- Justificaciones en listas con viñetas
- Compatible con Microsoft Word y LibreOffice

#### **Excel (XLSX)** - Tabla Comparativa

- **33 columnas** con todos los datos clave
- Columnas alternadas: Riesgo + Justificaciones
- Formato condicional con colores de riesgo
- Celdas con ajuste de texto automático
- Ideal para comparar múltiples candidatos

### Funciones Adicionales

- Generación de resumen concentrado para análisis externo
- Ayuda contextual durante la captura
- Validaciones automáticas de datos
- Sistema de respaldo integrado
- **Sistema modular para agregar campos fácilmente**

## Requisitos del Sistema

- **Sistema Operativo:** Windows 10/11, macOS 10.14+, Linux (Ubuntu 18.04+)
- **Python:** Versión 3.8 o superior
- **RAM:** Mínimo 4 GB (recomendado 8 GB para estudios con muchas fotos)
- **Espacio en Disco:** 1 GB libre

## Instalación

### 🎯 Instalación Rápida (Recomendada)

La forma más sencilla de instalar y ejecutar la aplicación:

#### En macOS/Linux:

```bash
# 1. Instalar (crea entorno virtual automaticamente)
python3 install.py

# 2. Dar permisos de ejecucion (solo la primera vez)
chmod +x run.sh

# 3. Ejecutar
./run.sh
```

#### En Windows:

```bash
# 1. Instalar (crea entorno virtual automáticamente)
python install.py

# 2. Ejecutar
run.bat
```

El instalador `install.py` detecta automáticamente si necesita crear un entorno virtual (especialmente importante en macOS con Homebrew Python) y maneja todo el proceso.

### 📦 Instalación Manual (Alternativa)

Si prefiere instalar manualmente:

#### Paso 1: Instalar Python

Si no tiene Python instalado, descárguelo de [python.org](https://www.python.org/downloads/)

#### Paso 2: Crear Entorno Virtual (Recomendado)

```bash
python -m venv venv
source venv/bin/activate  # En macOS/Linux
venv\Scripts\activate     # En Windows
```

#### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

#### Paso 4: Ejecutar la Aplicación

```bash
python main.py
```

### ⚙️ Configurar Empresa

Antes del primer uso, edite el archivo `config.json` con la información de su empresa:

```json
{
  "empresa": {
    "nombre": "Tu Empresa S.A. de C.V.",
    "direccion": "Calle Principal #123, Col. Centro",
    "telefono": "(555) 123-4567",
    "email": "contacto@tuempresa.com",
    "logo": "logo.png"
  }
}
```

Coloque su logo en formato PNG en la carpeta del proyecto.

## Manual de Usuario

### 🆕 Configuración Inicial

1. Configure `config.json` con datos de su empresa
2. Coloque su logo (formato PNG, 300x300 px recomendado)
3. Ejecute la aplicación con `./run.sh` (macOS/Linux) o `run.bat` (Windows)

### ✨ Crear un Nuevo Estudio

1. En la ventana principal, haga clic en **"Crear Nuevo"**
2. Se abrirá el asistente con 8 secciones expandidas
3. Complete cada sección:

   **Datos Personales** (19 campos):
   - Identificación completa: CURP, RFC, INE, NSS
   - Datos de contacto y emergencia
   - Escolaridad y licencia de conducir
   - Antecedentes legales si aplica

   **Salud e Intereses** (13 campos):
   - Estado de salud y tipo de sangre
   - Enfermedades crónicas con tratamientos
   - Hábitos: tabaco, alcohol, sustancias
   - Actividades y deportes

   **Información Familiar**:
   - Lista completa de miembros del hogar
   - Dependientes económicos
   - Enfermedades de familiares
   - Ingresos por persona

   **Situación Financiera**:
   - Empleo actual con salario
   - Otros ingresos detallados
   - Gastos por categoría
   - Ahorros, tarjetas de crédito, deudas
   - Balance automático con alertas

   **Empleo Actual** (NUEVO):
   - Datos de la empresa actual
   - Jefe directo y puesto
   - Tipo de contrato y antigüedad

   **Estilo de Vida** (NUEVO):
   - Vehículos propios
   - Viajes recientes
   - Hobbies y asociaciones

   **Vivienda y Patrimonio**:
   - Tipo y tenencia
   - Condición física y hacinamiento
   - Mobiliario y servicios

   **Historial Laboral**:
   - Empleos anteriores
   - Motivos de separación

   **Referencias Personales**:
   - Mínimo 2 referencias
   - Con contacto verificable

4. Use **"Siguiente"** y **"Anterior"** para navegar
5. Al finalizar, **"Guardar Estudio"**

### 📸 Adjuntar Fotografías

1. Seleccione un estudio y haga clic en **"Editar"**
2. Vaya a la sección de fotografías
3. **"Agregar Fotografía"** → Seleccione archivo
4. Elija categoría: Fachada, Interior, Entorno, etc.
5. Agregue descripción opcional
6. Guarde cambios

### ✏️ Editar un Estudio

1. Seleccione el estudio de la lista
2. Haga clic en **"Editar"**
3. Modifique los campos necesarios
4. El sistema validará automáticamente contradicciones
5. Guarde los cambios

### 🗑️ Eliminar un Estudio

1. Seleccione el estudio de la lista
2. Haga clic en **"Eliminar"**
3. Confirme la acción

### 📄 Exportar Reportes

#### PDF o Word (Individual)

1. Seleccione un estudio
2. **"Exportar"** → Elija formato
3. El archivo se guarda en `export/`
4. Incluye todas las secciones y justificaciones

#### Excel (Comparativa)

1. **"Exportar a Excel"** en ventana principal
2. Seleccione múltiples estudios
3. Genera tabla con 33 columnas
4. Incluye puntajes y justificaciones de riesgo

### 🔍 Validación Automática

El sistema detecta automáticamente:

- ✅ Balance declarado vs calculado
- ✅ Trabajo actual vs sueldo
- ✅ Vivienda propia con renta
- ✅ Gastos excesivos (>80% ingreso)
- ✅ Dependientes sin ingreso
- ✅ Hacinamiento crítico

Las alertas aparecen durante la captura.

## 🛠️ Para Desarrolladores

### Agregar Nuevos Campos

Gracias al sistema modular, agregar campos es extremadamente fácil:

1. **Editar `src/ui/configuracion_campos.py`** (30 segundos):

```python
{
    'id': 'nuevo_campo',
    'etiqueta': 'Mi Nuevo Campo',
    'tipo': TipoCampo.TEXTO,
    'requerido': False,
    'ayuda': 'Descripción del campo'
}
```

2. **Editar `src/models/estudio.py`** (15 segundos):

```python
"nuevo_campo": "",
```

3. **¡Listo!** El sistema automáticamente:
   - Crea el widget visual
   - Agrega funciones de guardado/carga
   - Incluye validaciones
   - Muestra ayuda contextual

**Ver `GUIA_AGREGAR_CAMPOS.md` para ejemplos completos.**

### Estructura del Proyecto

```
software-socioeconomico/
├── src/
│   ├── models/          # Modelo de datos (estudio.py)
│   ├── logic/           # Lógica de negocio
│   │   ├── calculador_riesgos.py  # Cálculo con justificaciones
│   │   └── validador.py            # Validación y alertas
│   ├── ui/              # Interfaz de usuario
│   │   ├── configuracion_campos.py # Definición de campos
│   │   ├── generador_formularios.py # Generación automática
│   │   └── paginas_modulares.py    # Sistema modular
│   └── export/          # Exportadores (PDF, Word, Excel)
├── data/               # Almacenamiento de estudios (JSON)
├── export/             # Archivos exportados
├── config.json         # Configuracion de empresa
├── install.py          # Instalador automatico
├── run.sh / run.bat    # Scripts de ejecucion
└── main.py             # Punto de entrada

```

### Documentacion

- **`README.md`**: Este manual
- **`CHANGELOG.md`**: Historial de cambios
- **`tasks.md`**: Lista de tareas del proyecto

2. Haga clic en **"Generar Info Concentrada"**
3. Se mostrará un cuadro de diálogo con el texto generado
4. Haga clic en **"Copiar al Portapapeles"**
5. Pegue el texto en la herramienta de análisis externa

## Análisis de Riesgos

El sistema calcula automáticamente indicadores de riesgo basados en los datos capturados:

### Riesgo Financiero (1-5)

- **1 (Muy Bajo):** Gastos < 50% del ingreso, sin deudas, ahorros
- **3 (Medio):** Gastos 50-80% del ingreso
- **5 (Muy Alto):** Gastos > ingresos, deudas significativas

### Riesgo Familiar (1-5)

- **1 (Muy Bajo):** Pocos dependientes, red de apoyo, estabilidad
- **3 (Medio):** Dependientes moderados, situación estable
- **5 (Muy Alto):** Muchos dependientes, falta de apoyo

### Riesgo Vivienda (1-5)

- **1 (Muy Bajo):** Vivienda propia, buenas condiciones, zona segura
- **3 (Medio):** Vivienda rentada, condiciones aceptables
- **5 (Muy Alto):** Vivienda precaria, zona de riesgo

### Riesgo Laboral (1-5)

- **1 (Muy Bajo):** Empleo estable, buenas referencias, antigüedad
- **3 (Medio):** Algunos cambios de empleo, referencias aceptables
- **5 (Muy Alto):** Múltiples empleos cortos, referencias negativas

### Riesgo Global

Promedio ponderado de todos los riesgos anteriores, proporcionando una evaluación integral.

## Estructura de Archivos

```
software socioeconomico/
├── main.py                 # Archivo principal de la aplicación
├── config.json             # Configuración de empresa
├── requirements.txt        # Dependencias de Python
├── data/                   # Carpeta de datos
│   ├── estudios/          # Archivos JSON de estudios
│   └── fotos/             # Fotografías adjuntas
├── export/                 # Reportes exportados
├── src/                    # Código fuente
│   ├── ui/                # Componentes de interfaz
│   ├── models/            # Modelos de datos
│   ├── logic/             # Lógica de negocio
│   └── export/            # Módulos de exportación
└── assets/                # Recursos (iconos, logos)
```

## Solución de Problemas

## ❓ Preguntas Frecuentes (FAQ)

### ¿Puedo agregar más campos al formulario?

**¡Sí!** El sistema modular hace esto extremadamente fácil. Consulte `GUIA_AGREGAR_CAMPOS.md` para instrucciones detalladas. En resumen:

1. Edite `src/ui/configuracion_campos.py` (agregar definición)
2. Edite `src/models/estudio.py` (agregar campo al modelo)
3. ¡Listo! El sistema genera la UI automáticamente

### ¿Los estudios antiguos (v0.1.0) funcionan con v0.2.0?

**Sí**, hay completa compatibilidad hacia atrás. Los estudios v0.1.0 se cargan correctamente y los nuevos campos aparecen vacíos. Puede actualizarlos editándolos.

### ¿Cómo funcionan las justificaciones de riesgo?

Cada puntaje de riesgo (1-5) viene con una lista de razones específicas basadas en los datos reales del estudio. Por ejemplo:

- "Gastos exceden el ingreso (105.3%)"
- "Sin ahorros reportados"
- "3 dependientes sin ingreso propio"

Esto hace que los puntajes sean transparentes y explicables.

### ¿Puedo modificar los algoritmos de riesgo?

**Sí**. Los algoritmos están en `src/logic/calculador_riesgos.py`. Cada método retorna una tupla `(puntaje, justificaciones)`. Puede modificar los criterios y las justificaciones se actualizarán automáticamente en todos los exportadores.

### ¿Qué hacer si encuentro una contradicción en los datos?

El sistema detecta contradicciones automáticamente durante la edición. Aparecerán alertas indicando qué revisar. Puede:

1. Corregir el dato incorrecto
2. Documentar la explicación en "Observaciones"
3. Revisar manualmente antes de exportar

### ¿Cuántos estudios puedo almacenar?

No hay límite fijo. Cada estudio ocupa aproximadamente 50-100 KB (sin fotos). Con fotos, depende del tamaño de las imágenes. El sistema usa archivos JSON individuales para cada estudio, lo que permite escalar sin problemas.

### ¿Los reportes se pueden personalizar?

Los exportadores están en `src/export/`. Puede modificarlos para:

- Cambiar colores y estilos
- Agregar/quitar secciones
- Modificar el orden de presentación
- Agregar logotipos o marcas de agua

## 🐛 Solución de Problemas

### La aplicación no inicia

**En macOS:**

```bash
# Si aparece error de "externally-managed-environment"
python3 install.py  # Esto crea un entorno virtual automáticamente
./run.sh            # Ejecutar desde el entorno virtual
```

**En Windows/Linux:**

```bash
# Verificar versión de Python
python --version    # Debe ser 3.8 o superior

# Reinstalar dependencias
pip install -r requirements.txt

# Ejecutar
python main.py
```

### Error al guardar estudios

1. Verifique permisos de escritura en la carpeta `data/`
2. Asegúrese de que el disco tenga espacio disponible
3. En macOS/Linux: `chmod 755 data/`
4. Revise que no haya procesos bloqueando los archivos

### Las fotografías no se adjuntan

1. Verifique que la carpeta `data/fotos/` exista
2. Formatos soportados: JPG, JPEG, PNG, BMP
3. Tamaño máximo recomendado: 10 MB por foto
4. Verifique permisos de escritura

### Error al exportar PDF

```bash
# Reinstalar ReportLab
pip uninstall reportlab
pip install reportlab

# Verificar que export/ exista
mkdir export
```

### Error al exportar Word

```bash
# Reinstalar python-docx
pip uninstall python-docx
pip install python-docx
```

### Error al exportar Excel

```bash
# Reinstalar openpyxl
pip uninstall openpyxl
pip install openpyxl
```

### Las justificaciones no aparecen en los reportes

Esto puede ocurrir si el estudio se creó antes de v0.2.0. El sistema calcula riesgos en tiempo real durante la exportación. Si persiste:

1. Edite el estudio
2. Revise que todos los campos tengan datos válidos
3. Guarde cambios
4. Exporte nuevamente

### Entorno virtual no funciona (macOS Homebrew)

```bash
# Usar el instalador automatico que maneja esto
python3 install.py

# O crear manualmente con path completo
/usr/local/bin/python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### PyQt5 no instala en Mac Apple Silicon (M1/M2/M3)

```bash
# Asegurarse de usar Python nativo ARM
arch -arm64 python3 install.py

# Si persiste, instalar via Homebrew
brew install pyqt@5
pip install --upgrade pip
pip install -r requirements.txt
```

Consulte `SOLUCION_ENTORNO.md` para detalles completos.

## 📚 Documentación Adicional

- **`CHANGELOG.md`**: Historial completo de cambios por versión
- **`GUIA_AGREGAR_CAMPOS.md`**: Guía paso a paso para agregar campos con ejemplos
- **`ACTUALIZACION_V02.md`**: Resumen técnico de cambios en v0.2.0
- **`RESUMEN_EJECUTIVO_V02.md`**: Resumen ejecutivo del proyecto completo
- **`SOLUCION_ENTORNO.md`**: Solución al problema de entorno virtual en macOS
- **`tasks.md`**: Tareas pendientes y roadmap del proyecto

## 🚀 Roadmap Futuro

### Versión 0.3.0 (Planificada)

- Dashboard de métricas y tendencias
- Gráficas comparativas de riesgos
- Sistema de plantillas personalizables
- Exportación a formatos adicionales (JSON, XML)
- API REST para integración con otros sistemas

### Versión 0.4.0 (Planificada)

- Modo multi-usuario con permisos
- Base de datos SQL opcional
- Sincronización en la nube
- App móvil para captura en campo
- Firma digital de reportes

## 🤝 Contribuir

Para contribuir al proyecto:

1. Consulte la documentación técnica en `docs/`
2. Revise `GUIA_AGREGAR_CAMPOS.md` para entender la arquitectura modular
3. Realice pruebas exhaustivas antes de integrar cambios
4. Documente todos los cambios en `CHANGELOG.md`

## 📞 Soporte Técnico

Para soporte técnico, consultas o reportar problemas:

**DINOS Tech**  
Email: soporte@dinoraptor.tech  
Telefono: 3333010376  
Web: dinoraptor.tech/dinostech

## 📄 Licencia

Este software es propiedad de DINOS Tech. Consulte el archivo LICENSE para más información sobre términos de uso y distribución.

---

**Desarrollado con ❤️ por DINOS Tech**  
© 2025 DINOS Tech. Todos los derechos reservados.

---

## Cambios Principales por Versión

### v0.2.0 (9 de diciembre de 2025)

- ✅ 100+ campos nuevos en todas las secciones
- ✅ Sistema de justificaciones automáticas de riesgo
- ✅ Validación inteligente con detección de contradicciones
- ✅ Arquitectura modular para fácil expansión
- ✅ 3 nuevas secciones: Salud detallada, Empleo Actual, Estilo de Vida
- ✅ Exportadores actualizados con 6 categorías de riesgo
- ✅ Excel con 33 columnas y justificaciones
- ✅ Documentación completa y guías de desarrollo

### v0.1.0 (Versión inicial)

- ✅ Sistema básico de captura de estudios
- ✅ Exportación a PDF, Word y Excel
- ✅ Cálculo de riesgos en 4 dimensiones
- ✅ Gestión de fotografías
- ✅ Interfaz gráfica con PyQt5
