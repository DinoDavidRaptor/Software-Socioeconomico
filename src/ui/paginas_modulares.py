"""
Páginas del wizard - VERSIÓN MODULAR 0.2.0
Sistema automático de generación de formularios.
Para agregar campos: solo modificar configuracion_campos.py
Autor: DINOS Tech
"""

from PyQt5.QtWidgets import (
    QWizardPage, QVBoxLayout, QLabel, QMessageBox
)
from PyQt5.QtCore import Qt
from .configuracion_campos import ConfiguracionCampos
from .generador_formularios import GeneradorFormularios
from typing import Dict, Any


class PaginaBaseModular(QWizardPage):
    """
    Clase base modular para páginas del wizard.
    Genera automáticamente formularios desde configuración.
    """
    
    def __init__(self, estudio, titulo: str, seccion_datos: str, parent=None):
        super().__init__(parent)
        self.estudio = estudio
        self.seccion_datos = seccion_datos
        self.setTitle(titulo)
        
        self.form_data = None  # Se llenará con crear_formulario_desde_config
        
    def crear_formulario_desde_config(self, campos_config, subtitulo: str = ""):
        """
        Crea el formulario automáticamente desde configuración de campos.
        
        Args:
            campos_config: Lista de configuraciones de campos
            subtitulo: Texto explicativo para mostrar arriba
        """
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        if subtitulo:
            self.setSubTitle(subtitulo)
        
        # Agregar ayuda contextual
        ayuda = GeneradorFormularios.crear_etiqueta_ayuda(
            "Los campos marcados con * son obligatorios. "
            "Puede usar Tab para navegar entre campos."
        )
        layout.addWidget(ayuda)
        
        # Generar formulario completo
        self.form_data = GeneradorFormularios.crear_formulario_completo(
            campos_config,
            self
        )
        
        layout.addWidget(self.form_data['scroll'])
    
    def guardar_datos(self):
        """Guarda los valores del formulario en el estudio."""
        if not self.form_data:
            return
        
        seccion = self.estudio.datos.get(self.seccion_datos, {})
        
        for campo_id, get_func in self.form_data['getters'].items():
            valor = get_func()
            seccion[campo_id] = valor
        
        self.estudio.datos[self.seccion_datos] = seccion
    
    def cargar_datos(self):
        """Carga los datos del estudio en el formulario."""
        if not self.form_data:
            return
        
        seccion = self.estudio.datos.get(self.seccion_datos, {})
        
        for campo_id, set_func in self.form_data['setters'].items():
            valor = seccion.get(campo_id, None)
            if valor is not None:
                try:
                    set_func(valor)
                except Exception as e:
                    print(f"Error cargando campo {campo_id}: {e}")
    
    def validatePage(self):
        """Valida la página antes de continuar."""
        # Guardar datos automáticamente
        self.guardar_datos()
        return True


class PaginaDatosPersonalesModular(PaginaBaseModular):
    """
    Página 1: Datos Personales (Modular)
    Para agregar campos: editar ConfiguracionCampos.obtener_campos_datos_personales()
    """
    
    def __init__(self, estudio):
        super().__init__(
            estudio,
            "Datos Personales",
            "datos_personales"
        )
        self.init_ui()
        self.cargar_datos()
    
    def init_ui(self):
        """Inicializa la interfaz automáticamente."""
        campos = ConfiguracionCampos.obtener_campos_datos_personales()
        
        self.crear_formulario_desde_config(
            campos,
            subtitulo="Capture la información personal del candidato. "
                     "Esta información es fundamental para el análisis."
        )
        
        # Registrar campos requeridos para la validación de PyQt5
        if self.form_data:
            if 'nombre_completo' in self.form_data['widgets']:
                self.registerField("nombre_completo*", self.form_data['widgets']['nombre_completo'])


class PaginaSaludModular(PaginaBaseModular):
    """
    Página 2: Salud e Intereses (Modular)
    Para agregar campos: editar ConfiguracionCampos.obtener_campos_salud()
    """
    
    def __init__(self, estudio):
        super().__init__(
            estudio,
            "Salud e Intereses",
            "salud_intereses"
        )
        self.init_ui()
        self.cargar_datos()
    
    def init_ui(self):
        """Inicializa la interfaz automáticamente."""
        campos = ConfiguracionCampos.obtener_campos_salud()
        
        self.crear_formulario_desde_config(
            campos,
            subtitulo="Información sobre salud física y mental del candidato. "
                     "Esta sección ayuda a identificar riesgos de salud."
        )


class PaginaEmpleoActualModular(PaginaBaseModular):
    """
    Página NUEVA: Empleo Actual (Modular)
    Para agregar campos: editar ConfiguracionCampos.obtener_campos_empleo_actual()
    """
    
    def __init__(self, estudio):
        super().__init__(
            estudio,
            "Empleo Actual",
            "empleo_actual"
        )
        self.init_ui()
        self.cargar_datos()
    
    def init_ui(self):
        """Inicializa la interfaz automáticamente."""
        campos = ConfiguracionCampos.obtener_campos_empleo_actual()
        
        self.crear_formulario_desde_config(
            campos,
            subtitulo="Detalles del empleo actual del candidato. "
                     "Información sobre estabilidad laboral y condiciones de trabajo."
        )


class PaginaEstiloVidaModular(PaginaBaseModular):
    """
    Página NUEVA: Estilo de Vida (Modular)
    Para agregar campos: editar ConfiguracionCampos.obtener_campos_estilo_vida()
    """
    
    def __init__(self, estudio):
        super().__init__(
            estudio,
            "Estilo de Vida",
            "estilo_vida"
        )
        self.init_ui()
        self.cargar_datos()
    
    def init_ui(self):
        """Inicializa la interfaz automáticamente."""
        campos = ConfiguracionCampos.obtener_campos_estilo_vida()
        
        self.crear_formulario_desde_config(
            campos,
            subtitulo="Actividades recreativas y estilo de vida del candidato. "
                     "Ayuda a entender patrones de gastos y equilibrio vida-trabajo."
        )


class PaginaValidacionDocumentalModular(PaginaBaseModular):
    """
    Pagina: Validacion Documental (Modular)
    Para agregar campos: editar ConfiguracionCampos.obtener_campos_validacion_documental()
    """
    
    def __init__(self, estudio):
        super().__init__(
            estudio,
            "Validacion Documental",
            "validacion_documental"
        )
        self.init_ui()
        self.cargar_datos()
    
    def init_ui(self):
        """Inicializa la interfaz automaticamente."""
        campos = ConfiguracionCampos.obtener_campos_validacion_documental()
        
        self.crear_formulario_desde_config(
            campos,
            subtitulo="Registro de verificacion de documentos oficiales. "
                     "Marque los documentos verificados y agregue observaciones."
        )


class PaginaInvestigacionVecinalModular(PaginaBaseModular):
    """
    Pagina: Investigacion Vecinal (Modular)
    Para agregar campos: editar ConfiguracionCampos.obtener_campos_investigacion_vecinal()
    """
    
    def __init__(self, estudio):
        super().__init__(
            estudio,
            "Investigacion Vecinal",
            "investigacion_vecinal"
        )
        self.init_ui()
        self.cargar_datos()
    
    def init_ui(self):
        """Inicializa la interfaz automaticamente."""
        campos = ConfiguracionCampos.obtener_campos_investigacion_vecinal()
        
        self.crear_formulario_desde_config(
            campos,
            subtitulo="Datos de la visita domiciliaria e investigacion con vecinos. "
                     "Complete esta seccion despues de realizar la visita de campo."
        )


class PaginaAnalisisCualitativoModular(PaginaBaseModular):
    """
    Pagina: Analisis Cualitativo (Modular)
    Para agregar campos: editar ConfiguracionCampos.obtener_campos_analisis_cualitativo()
    """
    
    def __init__(self, estudio):
        super().__init__(
            estudio,
            "Analisis Cualitativo",
            "analisis_cualitativo"
        )
        self.init_ui()
        self.cargar_datos()
    
    def init_ui(self):
        """Inicializa la interfaz automaticamente."""
        campos = ConfiguracionCampos.obtener_campos_analisis_cualitativo()
        
        self.crear_formulario_desde_config(
            campos,
            subtitulo="Evaluacion cualitativa del candidato basada en observaciones. "
                     "Incluye estabilidad emocional, responsabilidad y arraigo."
        )


class PaginaInvestigadorModular(PaginaBaseModular):
    """
    Pagina: Datos del Investigador (Modular)
    Para agregar campos: editar ConfiguracionCampos.obtener_campos_investigador()
    """
    
    def __init__(self, estudio):
        super().__init__(
            estudio,
            "Datos del Investigador",
            "investigador"
        )
        self.init_ui()
        self.cargar_datos()
    
    def init_ui(self):
        """Inicializa la interfaz automaticamente."""
        campos = ConfiguracionCampos.obtener_campos_investigador()
        
        self.crear_formulario_desde_config(
            campos,
            subtitulo="Informacion del investigador que realiza el estudio. "
                     "Estos datos apareceran en el PDF final para validacion."
        )


class PaginaInformacionFamiliarModular(PaginaBaseModular):
    """
    Pagina: Informacion Familiar Adicional (Modular)
    Campos complementarios a la tabla de miembros del hogar.
    """
    
    def __init__(self, estudio):
        super().__init__(
            estudio,
            "Informacion Familiar Adicional",
            "informacion_familiar"
        )
        self.init_ui()
        self.cargar_datos()
    
    def init_ui(self):
        """Inicializa la interfaz automaticamente."""
        campos = ConfiguracionCampos.obtener_campos_informacion_familiar()
        
        self.crear_formulario_desde_config(
            campos,
            subtitulo="Informacion adicional sobre la composicion familiar. "
                     "Completa los datos de hijos, dependientes y miembros del hogar."
        )


class PaginaSituacionFinancieraModular(PaginaBaseModular):
    """
    Pagina: Situacion Financiera Completa (Modular)
    Incluye todos los campos financieros del PDF.
    """
    
    def __init__(self, estudio):
        super().__init__(
            estudio,
            "Situacion Financiera Detallada",
            "situacion_financiera"
        )
        self.init_ui()
        self.cargar_datos()
    
    def init_ui(self):
        """Inicializa la interfaz automaticamente."""
        campos = ConfiguracionCampos.obtener_campos_situacion_financiera()
        
        self.crear_formulario_desde_config(
            campos,
            subtitulo="Informacion financiera detallada: ingresos, ahorros, deudas, "
                     "tarjetas de credito, prestamos y gastos adicionales."
        )


class PaginaViviendaModular(PaginaBaseModular):
    """
    Pagina: Vivienda Completa (Modular)
    Incluye todos los campos de vivienda del PDF.
    """
    
    def __init__(self, estudio):
        super().__init__(
            estudio,
            "Vivienda Detallada",
            "vivienda"
        )
        self.init_ui()
        self.cargar_datos()
    
    def init_ui(self):
        """Inicializa la interfaz automaticamente."""
        campos = ConfiguracionCampos.obtener_campos_vivienda()
        
        self.crear_formulario_desde_config(
            campos,
            subtitulo="Detalles completos de la vivienda: tipo, tenencia, dimensiones, "
                     "condiciones, valor estimado y seguridad del entorno."
        )


# ============================================================================
# GUÍA PARA AGREGAR NUEVAS PREGUNTAS O CAMPOS
# ============================================================================
#
# PASO 1: Agregar la configuración del campo
# -------------------------------------------
# Edite: src/ui/configuracion_campos.py
# 
# En la función correspondiente (ej: obtener_campos_datos_personales), agregue:
#
# {
#     'id': 'nombre_del_campo',           # ID único para guardar en JSON
#     'etiqueta': 'Etiqueta Visible',     # Lo que ve el usuario
#     'tipo': TipoCampo.TEXTO,            # Tipo de campo (ver TipoCampo)
#     'requerido': False,                 # Si es obligatorio
#     'ayuda': 'Texto de ayuda',          # Tooltip y guía
#     'placeholder': 'Ejemplo...',        # Texto de ejemplo
#     'opciones': ['Op1', 'Op2']          # Solo para combos
# }
#
# PASO 2: Actualizar el modelo de datos (si es nuevo campo)
# ----------------------------------------------------------
# Edite: src/models/estudio.py
#
# En la sección correspondiente del __init__, agregue:
# "nombre_del_campo": valor_por_defecto,
#
# PASO 3: ¡Listo!
# ---------------
# El sistema automáticamente:
# - Crea el control visual apropiado
# - Lo agrega al formulario en orden
# - Guarda/carga datos automáticamente
# - Valida campos requeridos
# - Muestra ayuda contextual
#
# NO necesita:
# - Escribir código de UI
# - Crear funciones de guardar/cargar
# - Manejar tipos de datos manualmente
# - Preocuparse por el layout
#
# TIPOS DE CAMPO DISPONIBLES:
# ---------------------------
# TipoCampo.TEXTO         - Línea de texto simple
# TipoCampo.TEXTO_LARGO   - Área de texto multilínea
# TipoCampo.NUMERO        - Número entero con spinner
# TipoCampo.DECIMAL       - Número decimal (dinero)
# TipoCampo.FECHA         - Selector de fecha
# TipoCampo.COMBO         - Lista desplegable (requiere 'opciones')
# TipoCampo.CHECKBOX      - Casilla de verificación
# TipoCampo.LISTA         - Lista editable de items
#
# EJEMPLO COMPLETO:
# -----------------
# Para agregar "Lugar de Nacimiento":
#
# 1. En configuracion_campos.py, dentro de obtener_campos_datos_personales():
#    {
#        'id': 'lugar_nacimiento',
#        'etiqueta': 'Lugar de Nacimiento',
#        'tipo': TipoCampo.TEXTO,
#        'requerido': False,
#        'ayuda': 'Ciudad y país donde nació',
#        'placeholder': 'Ej: Ciudad de México, México'
#    }
#
# 2. En estudio.py, dentro de datos_personales:
#    "lugar_nacimiento": "",
#
# 3. ¡Terminado! El campo aparecerá automáticamente en el formulario.
#
# ============================================================================
