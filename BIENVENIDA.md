# ¡Bienvenido a Ecosistema Comercial 360!

**Sistema Profesional de Estudios Socioeconómicos**  
**DINOS Tech - Versión 0.1.0**

---

## 🎯 ¿Qué es este Sistema?

Este software le permite crear, gestionar y analizar estudios socioeconómicos completos de manera profesional. Incluye:

- Captura guiada de información en 9 secciones
- Cálculo automático de indicadores de riesgo
- Generación de reportes profesionales en PDF, Word y Excel
- Gestión de fotografías y evidencias
- Sistema de análisis comparativo

---

## 🚀 Inicio Rápido

### Paso 1: Instalar Dependencias

Abra una terminal en esta carpeta y ejecute:

```bash
python install.py
```

O manualmente:

```bash
pip install -r requirements.txt
```

### Paso 2: Configurar su Empresa (Opcional)

Edite el archivo `config.json` con los datos de su empresa:
- Nombre de su empresa
- Dirección
- Teléfono y email
- Ruta a su logo (colóquelo en la carpeta `assets/`)

### Paso 3: Ejecutar la Aplicación

```bash
python main.py
```

---

## 📖 Documentación Disponible

- **README.md** - Manual completo de usuario (LÉALO PRIMERO)
- **QUICKSTART.md** - Guía rápida de 3 minutos
- **PROJECT_SUMMARY.md** - Resumen técnico del proyecto
- **CHANGELOG.md** - Registro de versiones y cambios

---

## 🔧 Solución de Problemas

### La aplicación no inicia

1. Verifique que tiene Python 3.8 o superior:
   ```bash
   python --version
   ```

2. Verifique las dependencias:
   ```bash
   python verify.py
   ```

3. Si faltan dependencias:
   ```bash
   pip install -r requirements.txt
   ```

### Error: "No se puede guardar"

Verifique que las carpetas `data/` y `export/` tengan permisos de escritura.

### Las fotografías no se adjuntan

Asegúrese de que:
- La carpeta `data/fotos/` existe
- Los archivos son JPG, PNG o BMP
- Tiene espacio en disco disponible

---

## 📋 Flujo de Trabajo Recomendado

1. **Preparación**
   - Configure los datos de su empresa en `config.json`
   - Coloque su logo en `assets/logo.png`

2. **Captura de Datos**
   - Clic en "Crear Nuevo Estudio"
   - Complete las 8 secciones de información
   - Adjunte fotografías en la última sección
   - Guarde el estudio

3. **Edición y Actualización**
   - Seleccione un estudio de la lista
   - Clic en "Editar"
   - Modifique los datos necesarios
   - Agregue o elimine fotografías
   - Guarde los cambios

4. **Generación de Reportes**
   - Seleccione un estudio
   - Clic en "Exportar a PDF" o "Exportar a Word" para un informe individual
   - Clic en "Exportar a Excel" para comparar múltiples estudios

5. **Análisis Externo**
   - Abra un estudio en modo edición
   - Clic en "Info Concentrada"
   - Copie el texto generado
   - Péguelo en su herramienta de análisis preferida

---

## ✨ Características Destacadas

### Análisis de Riesgos Automático

El sistema calcula automáticamente 5 indicadores de riesgo:
- **Financiero** - Basado en ingresos vs gastos
- **Familiar** - Dependientes y composición del hogar
- **Vivienda** - Condiciones y tenencia
- **Laboral** - Estabilidad y historial
- **Global** - Evaluación integral

Escala de 1 (Muy Bajo) a 5 (Muy Alto) con colores visuales.

### Reportes Profesionales

- **PDF** - Documento completo con imágenes listo para imprimir
- **Word** - Formato editable para personalización
- **Excel** - Tabla comparativa para análisis de múltiples candidatos

### Ayuda Contextual

Durante la captura, encontrará notas de ayuda que le guían sobre qué preguntar y cómo interpretar las respuestas.

---

## 📞 Soporte

**DINOS Tech**
- Email: soporte@dinostech.com
- Teléfono: +52 (55) XXXX-XXXX

Para reportar problemas o sugerir mejoras, contacte al equipo de soporte.

---

## 📄 Licencia

Este software está bajo Licencia MIT. Consulte el archivo `LICENSE` para más detalles.

---

## 🎓 Consejos para Nuevos Usuarios

1. **Lea el README.md** antes de usar por primera vez
2. **Haga pruebas** con un estudio de ejemplo
3. **Personalice** el archivo config.json con sus datos
4. **Respalde** regularmente la carpeta `data/`
5. **Actualice** el software cuando haya nuevas versiones

---

**¡Gracias por usar Ecosistema Comercial 360!**

*Sistema desarrollado profesionalmente para estudios socioeconómicos completos y análisis de riesgo.*

---

© 2025 DINOS Tech. Todos los derechos reservados.
