# Changelog - Ecosistema Comercial 360

Registro de cambios y versiones del sistema de estudios socioeconomicos.

---

## [0.4.1] - 12 de febrero de 2026 - CONFIGURACION Y BACKUPS

### Agregado

- **Dialogo de Configuracion de Empresa** accesible desde ventana principal
  - Editar nombre, direccion, telefono, email
  - Seleccionar y cambiar logo de la empresa
  - Guardado persistente en config.json
- **Sistema de Backup** para estudios socioeconomicos
  - Exportar todos los estudios y fotos a archivo ZIP
  - Importar backup con opcion de sobrescribir
  - Incluye metadata, config y empresas.json
  - Validacion de archivos de backup
- **Botones en header** de ventana principal: "Configuracion" y "Backup"

### Archivos nuevos

```
src/ui/dialogo_configuracion.py   # Configuracion de empresa
src/ui/dialogo_backup.py          # UI de backup
src/utils/gestor_backup.py        # Logica de export/import
```

---

## [0.4.0] - 12 de febrero de 2026 - SISTEMA DE DISTRIBUCION Y PROTECCION

### Agregado

- **Sistema de licencias offline** con validacion Hardware ID + License Key
- **Generador de ID de hardware** unico por equipo (MAC, CPU, disco)
- **Validador de licencias** con firma criptografica SHA256
- **Dialogo de activacion** integrado en la UI
- **Verificacion de licencia** al iniciar la aplicacion
- **Script de compilacion con Nuitka** para proteger codigo fuente
- **Script de Inno Setup** para crear instalador profesional
- **Terminos y condiciones (EULA)** legales completos
- **Documentacion de distribucion** paso a paso

### Estructura nueva

```
src/licensing/          # Sistema de licencias
  hardware_id.py        # Generador de Hardware ID
  license_validator.py  # Validacion de licencias

src/ui/
  dialogo_activacion.py # UI de activacion

scripts/
  build_nuitka.py       # Compilacion
  privado/              # NO distribuir
    license_generator.py

installer/
  setup.iss             # Inno Setup

assets/installer/
  EULA.txt              # Terminos y condiciones
```

---

## [0.3.7] - 12 de febrero de 2026 - LIMPIEZA DE ARCHIVOS

### Eliminado

- 13 archivos MD redundantes: QUICKSTART, BIENVENIDA, INICIO_RAPIDO, PROJECT_SUMMARY, PROYECTO_COMPLETADO, ACTUALIZACION_V02, RESUMEN_EJECUTIVO_V02, IMPLEMENTACION_COMPLETA_V02, CHANGELOG_v030, GUIA_AGREGAR_CAMPOS, LISTA_COMPLETA_PREGUNTAS, SOLUCION_ENTORNO, WORKSPACE-CREATION-PROMPT
- Script de verificacion verify.py

### Mejorado

- .gitignore actualizado con reglas para archivos de IA, scripts de testing, temporales y datos sensibles

---

## [0.3.6] - 11 de febrero de 2026 - WORD WRAP EN TODAS LAS TABLAS PDF

### Corregido

- Encabezados de tabla de riesgos con texto negro (ahora blanco sobre fondo oscuro)
- Texto desbordado en "Motivo Salida" de historial laboral
- Texto desbordado en "Condiciones" y "Seguridad Entorno" de vivienda
- Observaciones familiares que se salian de la tabla
- Gastos extraordinarios e historial de deudas desbordados
- Condiciones vivienda observadas y ambiente familiar observado desbordados

### Mejorado

- **TODAS las tablas** ahora usan Paragraphs para word wrap automatico:
  - Datos Personales: direccion, certificados, contactos de emergencia
  - Salud e Intereses: enfermedades, tratamientos, metas
  - Informacion Familiar: observaciones familiares
  - Situacion Financiera: gastos extraordinarios, historial deudas, apoyos
  - Historial Laboral: columnas proporcionales, motivo salida con wrap
  - Vivienda y Patrimonio: condiciones, seguridad entorno
  - Empleo Actual: prestaciones, observaciones
  - Estilo de Vida: hobbies, actividades
  - Referencias Personales: encabezados blancos
  - Miembros del Hogar: encabezados blancos, ocupacion
  - Observaciones Investigacion: condiciones vivienda, ambiente familiar, obs generales
- Encabezados de tablas con fondo oscuro tienen texto blanco consistente
- Filas de tablas se expanden verticalmente cuando el texto es largo

---

## [0.3.5] - 11 de febrero de 2026 - MEJORAS DE LAYOUT PDF

### Corregido

- Parrafo duplicado de observaciones financieras en PDF (aparecia 2 veces)
- Texto cortado/comprimido en tablas - ahora usa Paragraphs con word wrap automatico
- Columna "Observaciones" muy angosta en Validacion Documental y Analisis Cualitativo

### Mejorado

- **Tabla de Riesgos**: Anchos proporcionales (Categoria 30%, Interpretacion 40%)
- **Tabla Validacion Documental**: Columna Observaciones ampliada al 63% del ancho
- **Tabla Analisis Cualitativo**: Columna Observaciones ampliada al 55% del ancho
- **Justificaciones**: Formato compacto en 2 columnas cuando hay mas de 6 items
- **Conclusiones**: Parrafos largos ahora se dividen automaticamente para mejor legibilidad
- Todas las tablas ahora usan Paragraphs para calculo dinamico de altura de fila

---

## [0.3.4] - 11 de febrero de 2026 - EMPRESA SOLICITANTE Y ESTUDIOS DEMO

### Agregado

- Seccion "Estudio Solicitado Por" en el encabezado del PDF exportado
  - Muestra el nombre de la empresa solicitante en recuadro destacado
  - Estilo profesional con fondo azul claro y borde
- 2 estudios de ejemplo con datos completamente consistentes:
  - **ejemplo_alto_riesgo.json**: Roberto Mendoza, riesgo global 81.25%
    - Gastos superan ingresos, deudas de $75K, empleo eventual
    - Antecedentes legales, vivienda rentada con problemas
    - Historial laboral inestable (5 empleos en 2 anos)
  - **ejemplo_bajo_riesgo.json**: Fernando Gutierrez, riesgo global 11.25%
    - Ingreso familiar $128K/mes, ahorro 19.5%
    - 12 anos en misma empresa, casa propia
    - Patrimonio inmobiliario de $7.7M, score crediticio 780

### Modificado

- exportador_pdf.py: Nueva seccion de empresa solicitante despues del encabezado

### Corregido

- Error al exportar PDF cuando otros_ingresos es lista de diccionarios
  - Campo otros_ingresos ahora se convierte a string legible: "fuente: $monto (frecuencia)"

---

## [0.3.3] - 11 de febrero de 2026 - CAMPOS FALTANTES DEL PDF

### Agregado

- 3 nuevas paginas modulares en wizard:
  - Informacion Familiar Adicional: numero de hijos, miembros trabajando/estudiando, dependientes, observaciones
  - Situacion Financiera Adicional: ahorros, tarjetas de credito, deudas, apoyos gubernamentales, historial
  - Vivienda Adicional: dimensiones, valor, propiedades adicionales, condiciones, seguridad
- Campos nuevos en secciones existentes:
  - datos_personales: carrera_especialidad, estado_estudios
  - salud: frecuencia_consultas_psicologicas
  - empleo_actual: jefe_inmediato, telefono_empresa, satisfaccion_laboral, oportunidades_ascenso, ultima_evaluacion_desempeno, observaciones_empleo
  - estilo_vida: fuma, gasto_mensual_tabaco, gasto_mensual_alcohol
- 56 campos adicionales para cubrir todos los campos del PDF

### Modificado

- Wizard expandido de 17 a 20 paginas
- configuracion_campos.py: 3 nuevos metodos (obtener_campos_informacion_familiar, obtener_campos_situacion_financiera, obtener_campos_vivienda)
- paginas_modulares.py: 3 nuevas clases (PaginaInformacionFamiliarModular, PaginaSituacionFinancieraModular, PaginaViviendaModular)
- Total de campos editables: 217 campos en 11 secciones

---

## [0.3.2] - 11 de febrero de 2026 - SECCIONES INSTITUCIONALES

### Agregado

- 4 nuevas secciones editables en el wizard:
  - Validacion Documental: verificacion de INE, CURP, RFC, NSS, comprobantes
  - Investigacion Vecinal: visita domiciliaria, entrevistas con vecinos y arrendador
  - Analisis Cualitativo: estabilidad emocional, responsabilidad, arraigo, coherencia
  - Datos del Investigador: nombre, cedula, empresa, contacto, fecha
- 6 graficas completas en exportacion PDF:
  - Ingresos vs Gastos vs Ahorro Acumulado
  - Distribucion de Deudas
  - Indicadores Financieros
  - Distribucion de Gastos
  - Radar de Riesgos
  - Actividades y Habitos
- Secciones institucionales en PDF: Validacion Documental, Investigacion Vecinal, Analisis Cualitativo, Conclusiones y Firma del Investigador
- ~90 campos nuevos en modelo de datos para secciones institucionales
- Wizard expandido de 13 a 17 paginas

### Modificado

- Modelo estudio.py ampliado con 4 nuevas secciones de datos
- configuracion_campos.py con 4 nuevos metodos de configuracion
- paginas_modulares.py con 4 nuevas clases de pagina
- wizard_estudio.py actualizado para 17 paginas

---

## [0.3.2] - 11 de febrero de 2026 - MEJORAS INSTITUCIONALES PDF

### Agregado

- Sistema completo de 6 graficas en exportacion PDF:
  - Grafica de Ingresos vs Gastos vs Ahorro Acumulado (barras comparativas)
  - Distribucion de Deudas por tipo (pastel)
  - Indicadores Financieros: Ratio deuda/ingreso, gastos/ingreso, ahorro (barras dobles)
  - Distribucion detallada de Gastos (pastel con todas las categorias)
  - Radar de Riesgos (grafico polar con 6 categorias)
  - Actividades y Habitos de estilo de vida (barras horizontales)
- Nueva seccion "Validacion Documental" con verificacion de:
  - INE, CURP, RFC (SAT), NSS (IMSS)
  - Comprobante de domicilio con tipo y fecha
  - Recibo de nomina con periodo
  - Constancia laboral
  - Estados de cuenta bancarios
- Nueva seccion "Investigacion Vecinal" que documenta:
  - Visita domiciliaria (fecha, hora, persona que atendio)
  - Entrevista con vecino (opinion, tiempo de conocerlo)
  - Contacto con arrendador (opinion, historial de pagos)
  - Condiciones de vivienda y ambiente familiar observados
- Nueva seccion "Analisis Cualitativo" con evaluacion de:
  - Estabilidad emocional
  - Perfil de responsabilidad
  - Congruencia nivel de vida/ingresos
  - Riesgo reputacional
  - Nivel de arraigo
  - Actitud en entrevista
  - Coherencia de respuestas
- Seccion "Conclusiones y Firma del Investigador":
  - Conclusiones del estudio
  - Datos completos del investigador (nombre, cedula, empresa)
  - Declaracion de veracidad bajo protesta
  - Espacio para firma del investigador

### Modificado

- Modelo de datos (estudio.py) expandido con 4 nuevas secciones institucionales
- Metodo de generacion de graficos completamente reescrito para incluir las 6 graficas

---

## [0.3.1] - 11 de febrero de 2026 - CORRECCIONES PDF

### Corregido

- Tabla "Miembros del Hogar" ahora muestra ingresos correctamente (usaba campo incorrecto `ingreso_mensual` en lugar de `ingreso`)
- Seccion de riesgos ahora usa valores almacenados del JSON en lugar de recalcularlos, respetando los puntajes guardados
- Justificaciones de estilo de vida corregidas:
  - Verifica vehiculos en `vivienda.vehiculos` y `vivienda.tiene_vehiculos`
  - Usa `numero_viajes_ultimo_ano` en lugar de boolean inexistente
  - Usa `pertenece_clubes` en lugar de `pertenece_asociaciones`
  - Agrega justificaciones positivas para actividad fisica, mascotas y no fumar
- Graficos de riesgos tambien usan valores almacenados del JSON
- Eliminada impresion de lista cruda de "Miembros Hogar" en seccion familiar (ya se muestra la tabla formateada)
- Etiqueta "Ahorros" cambiada a "Ahorro Acumulado" para diferenciar de "Ahorro Mensual"
- Riesgo Global ahora muestra valor exacto con 2 decimales (ej: 2.67 en lugar de 2.7) para mayor claridad
- Tabla de Referencias Personales corregida: ahora usa campos correctos (`relacion` en lugar de `parentesco`, `tiempo_conocido`/`tiempo_conocerse_meses` en lugar de `antiguedad_conocimiento`)

---

## [0.2.0] - 9 de diciembre de 2025 - EXPANSIÓN MAYOR

### Agregado

- Más de 100 campos nuevos distribuidos en todas las secciones
- Sistema automático de justificaciones de riesgo con explicaciones detalladas
- Validador inteligente que detecta contradicciones entre respuestas
- Sistema de alertas en tiempo real durante la captura de datos
- Detección automática cuando gastos superan 80% del ingreso
- Identificación de dependientes sin ingreso propio
- Análisis de discrepancias entre ingresos declarados y reales

#### Datos Personales Expandidos

- Nacionalidad y estado de nacimiento
- Escolaridad completa con institución y certificados
- Persona de contacto de emergencia
- Registro de antecedentes legales con detalles
- Información sobre dependencia económica

#### Composición Familiar Detallada

- Estado de cada integrante: estudia/trabaja
- Indicador de aporte al ingreso familiar
- Registro de enfermedades crónicas por integrante
- Tipo de dependencia (total/parcial/ninguna)
- Contador automático de dependientes sin ingreso

#### Salud Completa

- Registro específico de enfermedades crónicas
- Tratamientos médicos actuales
- Alergias documentadas
- Antecedentes psicológicos
- Consumo de sustancias (alcohol, tabaco, otras)

#### Vivienda Profunda

- Servicio de gas agregado a servicios básicos
- Equipamiento extendido (aire acondicionado, calentador)
- Mobiliario detallado (camas, mesas, sillas, armarios, sillones)
- Condición física: humedad, filtraciones, sobrecupo, ventilación, iluminación
- Evaluación de seguridad del entorno
- Tiempo exacto viviendo en la vivienda
- Número de habitantes para cálculo de hacinamiento

#### Finanzas Exhaustivas

- Registro de ahorros acumulados
- Detalle de cuentas bancarias
- Tarjetas de crédito (banco, límite, saldo actual)
- Historial completo de deudas anteriores
- Apoyos gubernamentales recibidos
- Categoría de gastos recreativos
- Gastos extraordinarios documentados
- Cálculo automático de porcentaje gastos/ingreso
- Flag de discrepancia automática

#### Empleo Actual Detallado (Nueva Sección)

- Información completa de empresa y puesto
- Antigüedad exacta en el empleo
- Tipo de contrato (indefinido/temporal/honorarios)
- Lista completa de prestaciones
- Horario laboral y tiempo de traslado
- Plan de carrera disponible
- Historial de evaluaciones de desempeño

#### Historial Laboral Profundo

- Evaluaciones de desempeño en empleos anteriores
- Registro de conflictos laborales
- Verificación de referencias empleador

#### Estilo de Vida (Nueva Sección)

- Hobbies y actividades recreativas
- Actividades típicas de fin de semana
- Frecuencia y destinos de viajes
- Gastos dedicados a recreación
- Participación en actividades culturales
- Deportes practicados

### Mejorado

- Sistema de cálculo de riesgos ahora genera justificaciones automáticas
- Cada puntaje de riesgo (1-5) incluye lista de razones específicas
- Riesgo financiero considera ahorros, tarjetas de crédito y discrepancias
- Riesgo familiar evalúa enfermedades crónicas y tipo de dependencia
- Riesgo de vivienda analiza hacinamiento y problemas físicos específicos
- Riesgo laboral profundiza en tipo de contrato y prestaciones
- Riesgo global identifica automáticamente áreas críticas

### Validaciones y Alertas Nuevas

- Detección de balance declarado vs calculado
- Alerta cuando gastos > 80% del ingreso
- Identificación de dependientes mayores sin ingreso
- Detección de contradicción: trabaja pero sin sueldo
- Validación de ingreso familiar vs suma de ingresos individuales
- Alerta de vivienda propia con renta declarada
- Cálculo y alerta de hacinamiento (personas/cuarto)
- Detección de falta de servicios básicos
- Identificación de múltiples problemas físicos en vivienda
- Validación de coherencia empresa/puesto entre secciones
- Detección de alta rotación laboral
- Alerta de empleos de muy corta duración

### Técnico

- Clase CalculadorRiesgos completamente reescrita
- Métodos ahora retornan tuplas (riesgo, justificaciones)
- Nueva clase ValidadorEstudio para detección de inconsistencias
- Modelo de datos expandido con retrocompatibilidad
- Sistema de alertas integrado en estructura de datos
- Método unificado calcular_todos_riesgos() para facilitar uso
- Validaciones ejecutadas en segundo plano sin bloquear guardado

---

## [0.1.0] - 9 de diciembre de 2025 - VERSIÓN INICIAL COMPLETADA

### Agregado

- Versión inicial del sistema de estudios socioeconómicos
- Interfaz gráfica completa con PyQt5
- Sistema de captura mediante asistente paso a paso con 8 secciones de datos
- Sección adicional para adjuntar fotografías (9 secciones en total)
- Gestión completa de datos personales, familiares, financieros y laborales
- Sistema de adjuntar y categorizar fotografías con almacenamiento organizado
- Cálculo automático de indicadores de riesgo en 5 dimensiones:
  - Riesgo Financiero (basado en ingresos, gastos y deudas)
  - Riesgo Familiar (dependientes y composición del hogar)
  - Riesgo de Vivienda (condiciones, servicios y tenencia)
  - Riesgo Laboral (estabilidad y historial)
  - Riesgo Socioeconómico Global (promedio ponderado)
- Exportación a PDF con formato profesional e imágenes incluidas
- Exportación a Word (DOCX) completamente editable
- Exportación a Excel (XLSX) con tabla comparativa de múltiples estudios
- Función de generación de resumen concentrado para análisis externo
- Sistema de ayuda contextual en formularios para guiar al evaluador
- Validaciones automáticas de campos obligatorios y formatos
- Configuración de empresa mediante archivo JSON externo
- Almacenamiento de estudios en formato JSON individual por estudio
- Gestión automática de carpetas para fotos y exportaciones
- Botón "Info Concentrada" en modo edición para generar resumen
- Indicadores visuales de riesgo con códigos de color en tabla principal
- Sistema de navegación intuitivo con botones Anterior/Siguiente
- Confirmaciones de eliminación para evitar pérdidas accidentales

### Técnico

- Implementación en Python 3.8+ con tipado opcional
- Uso de PyQt5 para interfaz gráfica multiplataforma
- ReportLab para generación de PDF con tablas y formato avanzado
- python-docx para exportación Word con estilos personalizados
- openpyxl para exportación Excel con formato condicional
- Pillow para procesamiento de imágenes
- Arquitectura modular con separación de responsabilidades (MVC adaptado)
- Manejo robusto de errores y excepciones con mensajes user-friendly
- Sistema de logs para debugging (preparado para futuras versiones)
- Código documentado con docstrings en formato Google
- Estructura de directorios organizada por responsabilidad
- Compatibilidad con Windows, macOS y Linux

### Documentación

- README.md completo con manual de usuario detallado
- QUICKSTART.md con guía de inicio rápido en 3 pasos
- LICENSE con Licencia MIT
- PROJECT_SUMMARY.md con resumen ejecutivo del proyecto
- Comentarios profesionales en todo el código fuente
- Archivos de ayuda contextual integrados en la UI
- Script install.py para configuración inicial automatizada
- Script verify.py para verificación del sistema

### Scripts Incluidos

- `main.py` - Punto de entrada principal de la aplicación
- `install.py` - Asistente de instalación interactivo
- `verify.py` - Verificación de dependencias y estructura
- `requirements.txt` - Lista de dependencias de Python

### Estructura del Proyecto

```
src/
├── models/          # Modelos de datos
├── logic/           # Lógica de negocio y cálculos
├── ui/              # Componentes de interfaz gráfica
└── export/          # Módulos de exportación
```

### Notas de Versión

Esta es la versión inicial completa y lista para producción del sistema.
Incluye todas las funcionalidades especificadas en los requisitos originales.

El sistema ha sido diseñado con arquitectura extensible para facilitar
futuras mejoras y nuevas funcionalidades.

---

## Próximas Versiones Planeadas

### [0.2.0] - Futuro

- Sistema de backup automático programado
- Búsqueda y filtros avanzados en lista de estudios
- Gráficas de análisis estadístico
- Plantillas personalizables de reportes
- Exportación adicional a HTML y CSV

### [0.3.0] - Futuro

- Modo multiusuario con sistema de permisos
- Sincronización en la nube (opcional)
- Reportes estadísticos agregados
- Panel de análisis comparativo visual

---

_Formato basado en [Keep a Changelog](https://keepachangelog.com/)_
