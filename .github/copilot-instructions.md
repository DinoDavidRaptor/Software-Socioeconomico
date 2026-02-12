# Instrucciones para Agentes de IA - Software Socioeconomico

## Directivas Criticas

### Lenguaje y Comunicacion

- OBLIGATORIO: Comunicacion 100% en español
- SIN EMOJIS: Nunca usar emojis en codigo, commits, documentacion o respuestas
- Profesionalismo absoluto en todo momento

### Flujo de Trabajo Obligatorio para Cada Cambio

1. Validacion inicial: Preguntar si hay dudas sobre la solicitud
2. Agregar a tasks.md: Crear entrada con estado "POR HACER" antes de iniciar
3. Marcar como En Progreso: Cambiar estado a "EN PROGRESO" con fecha
4. Implementar: Ejecutar los cambios requeridos
5. Actualizar CHANGELOG.md: Documentar en seccion (Añadido/Modificado/Corregido)
6. Actualizar README.md: Solo si es funcion importante (mantener badges)
7. Testing Ligero: Verificar funcionalidad sin crear suites complejas
8. Revisar .gitignore: Verificar archivos sensibles esten ignorados
9. Solicitar Aprobacion: Preguntar antes de commit y push
10. Commit en Español: Mensaje descriptivo sin emojis
11. Marcar Completada: Cambiar estado en tasks.md a "COMPLETADA"
12. Resumen: Confirmar que funcione antes de declarar completado

### Archivos Sensibles a Ignorar

El .gitignore DEBE incluir:

- Archivos de IA: copilot-_.md, claude-_.md, agent-\*.md, AGENTS.md, CLAUDE.md
- Scripts de testing: test-_.js, test-_.ts, test-\*.py
- Configuracion sensible: .env*, config.local.*
- Datos de prueba: empresas.json, estudios/
- Archivos debug: debug_files/, _.debug, _.test.local
- Cache de Python: **pycache**/, \*.pyc

### Mantenimiento Periodico del Prompt

- Verificar cada 2 semanas o tras cambios arquitectonicos
- Si hay nuevas tecnologias o patrones: Integrar cambios
- NUNCA exceder 20-50 lineas de instrucciones clave
- Mantener enfoque en patrones reales, no hipoteticos

## Esencia del Proyecto

### Estructura Esencial

Software de evaluacion socieconomica desarrollado en Python con Tkinter.

- src/ui: Interfaz grafica (paginas modulares, wizard, formularios dinamicos)
- src/logic: Logica de negocio (validacion, calculo de riesgos)
- src/models: Modelos de datos (clase Estudio)
- src/export: Exportadores (PDF, Excel, Word)
- src/utils: Utilidades (gestion de empresas, datos de prueba)

### Convenciones de Codigo

- Python 3.x con type hints donde sea posible
- Tkinter para UI con arquitectura modular
- JSON para persistencia de datos
- Clases y metodos documentados en español
- Nombres de variables y funciones descriptivos en español

### Flujos de Trabajo

- Configuracion inicial via config.json
- Gestion de empresas via gestor_empresas.py
- Wizard paso a paso para crear estudios
- Exportacion multiple (PDF, Excel, Word) desde interfaz
- Validacion de datos antes de guardar
