# Lista de Tareas - SoftSE

## Configuración Inicial

- [x] Crear estructura de directorios del proyecto
- [x] Configurar archivos de metadatos (README, LICENSE, CHANGELOG)
- [x] Crear archivo de configuración JSON para datos de empresa
- [x] Definir estructura de datos JSON para estudios socioeconómicos

## Modelo de Datos

- [x] Diseñar esquema JSON para estudios completos
- [x] Implementar funciones de carga y guardado de datos
- [x] Crear sistema de gestión de archivos de fotografías
- [x] Implementar validación de estructura de datos

## Interfaz Gráfica - Ventana Principal

- [x] Crear ventana principal con logo y título
- [x] Implementar lista/tabla de estudios guardados
- [x] Agregar botones: Crear Nuevo, Editar, Eliminar, Exportar
- [x] Implementar carga de configuración de empresa

## Interfaz Gráfica - Formulario de Captura

- [x] Sección 1: Datos Personales
- [x] Sección 2: Salud e Intereses
- [x] Sección 3: Información Familiar
- [x] Sección 4: Situación Financiera (ingresos y gastos)
- [x] Sección 5: Vivienda y Patrimonio
- [x] Sección 6: Historial Laboral
- [x] Sección 7: Referencias Personales
- [x] Sección 8: Conclusiones del Evaluador
- [x] Sistema de navegación paso a paso (wizard)
- [x] Agregar funcionalidad de adjuntar fotografías
- [x] Implementar validaciones de campos

## Lógica de Negocio

- [x] Calcular porcentaje de gastos vs ingresos
- [x] Implementar sistema de cálculo de riesgo financiero
- [x] Implementar cálculo de riesgo familiar
- [x] Implementar cálculo de riesgo de vivienda
- [x] Implementar cálculo de riesgo laboral
- [x] Calcular riesgo socioeconómico global
- [x] Guardar métricas calculadas en JSON

## Funcionalidades de Exportación

- [x] Exportar a PDF con formato profesional
- [x] Exportar a Word (DOCX)
- [x] Exportar a Excel (XLSX) con comparativa múltiple
- [x] Incluir imágenes en reportes PDF y Word
- [x] Aplicar formato y estilos profesionales a reportes

## Funcionalidades Adicionales

- [x] Implementar función "Info Concentrada" para IA
- [x] Agregar sistema de ayuda contextual en formularios
- [x] Implementar manejo robusto de errores
- [x] Crear sistema de respaldo de datos

## Documentación y Distribución

- [x] Completar README con instrucciones de instalación
- [x] Crear manual de usuario detallado
- [x] Documentar código con comentarios profesionales
- [x] Crear requirements.txt con dependencias
- [x] Actualizar CHANGELOG con versión 0.1.0

## Pruebas y Refinamiento

- [ ] Probar flujo completo de creación de estudio
- [ ] Verificar exportaciones en todos los formatos
- [ ] Validar cálculos de riesgo
- [ ] Revisar diseño y usabilidad de interfaz
- [x] Corregir bugs de exportación PDF (11/02/2026):
  - [x] Tabla miembros hogar: campo ingreso corregido
  - [x] Riesgos: usar valores almacenados del JSON
  - [x] Justificaciones estilo de vida: campos correctos
  - [x] Eliminar lista cruda de miembros en info familiar
  - [x] Clarificar etiqueta "Ahorro Acumulado" vs "Ahorro Mensual"
  - [x] Mostrar riesgo global con 2 decimales

## Mejoras v0.3.3 - Campos Faltantes del PDF

- [x] Analizar campos PDF vs campos GUI (43 campos faltantes identificados)
- [x] Agregar campos a datos_personales: carrera_especialidad, estado_estudios
- [x] Agregar campos a salud: frecuencia_consultas_psicologicas
- [x] Agregar campos a empleo_actual: jefe_inmediato, telefono_empresa, satisfaccion_laboral, etc.
- [x] Agregar campos a estilo_vida: fuma, gasto_mensual_tabaco, gasto_mensual_alcohol
- [x] Crear seccion informacion_familiar (9 campos)
- [x] Crear seccion situacion_financiera (28 campos: ahorros, tarjetas, historial deudas)
- [x] Crear seccion vivienda (19 campos: dimensiones, valor, propiedades adicionales)
- [x] Crear 3 nuevas paginas modulares en wizard
- [x] Integrar nuevas paginas al wizard (20 paginas totales)
- [x] Verificar sin errores de sintaxis

## Mejoras v0.3.4 - Empresa Solicitante y Estudios Demo

- [x] Agregar empresa solicitante al encabezado del PDF exportado
- [x] Crear estudio de ejemplo ALTO RIESGO (Roberto Mendoza - 81.25% riesgo)
- [x] Crear estudio de ejemplo BAJO RIESGO (Fernando Gutierrez - 11.25% riesgo)
- [x] Estudios con datos completamente consistentes y editables

## Mantenimiento - Limpieza de Archivos (12/02/2026)

- [x] Eliminar 13 archivos MD redundantes (QUICKSTART, BIENVENIDA, ACTUALIZACION_V02, etc.)
- [x] Eliminar script de prueba verify.py
- [x] Actualizar .gitignore con reglas para archivos de IA, testing y temporales

## Sistema de Distribucion y Proteccion (12/02/2026)

- [x] Crear sistema de licencias offline (Hardware ID + License Key)
- [x] Implementar generador de IDs de hardware unicos
- [x] Crear validador de licencias con firma SHA256
- [x] Crear dialogo de activacion de licencia en UI
- [x] Integrar verificacion de licencia en main.py
- [x] Crear generador de licencias (scripts/privado/ - NO distribuir)
- [x] Crear script de compilacion con Nuitka
- [x] Crear script de Inno Setup (.iss) para instalador
- [x] Crear terminos y condiciones (EULA.txt)
- [x] Documentar proceso completo de distribucion
- [ ] Crear graficos del instalador (icon.ico, banner.bmp, header.bmp)
- [ ] Compilar y probar instalador completo

## Configuracion y Backups (12/02/2026)

- [x] Crear dialogo de configuracion de empresa
- [x] Permitir editar nombre, direccion, telefono, email
- [x] Permitir seleccionar y cambiar logo
- [x] Crear sistema de backup (export/import ZIP)
- [x] Incluir estudios, fotos, config en backup
- [x] Agregar botones de Configuracion y Backup en ventana principal

## Rebranding a SoftSE (12/02/2026)

- [x] Reemplazar "Ecosistema Comercial 360" por "SoftSE" en todos los archivos
- [x] Actualizar URL de contacto a dinoraptor.tech/dinostech
- [x] Actualizar email de soporte a soporte@dinoraptor.tech
- [x] Agregar telefono de contacto 3333010376
