# Changelog - Ecosistema Comercial 360

Registro de cambios y versiones del sistema de estudios socioeconómicos.

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

*Formato basado en [Keep a Changelog](https://keepachangelog.com/)*
