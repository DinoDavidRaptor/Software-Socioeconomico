"""
Wizard (asistente) para crear y editar estudios socioeconómicos.
Autor: DINOS Tech
Versión: 0.2.0 - Sistema modular con 150+ campos
"""

from PyQt5.QtWidgets import QWizard, QWizardPage, QMessageBox
from PyQt5.QtCore import Qt
from src.models.estudio import EstudioSocioeconomico
from src.logic.calculador_riesgos import CalculadorRiesgos
from src.utils.generador_datos_prueba import GeneradorDatosPrueba

# Importar página de empresa (NUEVA v0.3.0)
from src.ui.pagina_empresa import PaginaEmpresaSolicitante

# Importar página de visualización (NUEVA v0.3.0)
from src.ui.pagina_visualizacion import PaginaVisualizacionDatos

# Importar páginas MODULARES (nuevas - v0.2.0)
from src.ui.paginas_modulares import (
    PaginaDatosPersonalesModular,
    PaginaSaludModular,
    PaginaEmpleoActualModular,
    PaginaEstiloVidaModular,
    PaginaValidacionDocumentalModular,
    PaginaInvestigacionVecinalModular,
    PaginaAnalisisCualitativoModular,
    PaginaInvestigadorModular,
    PaginaInformacionFamiliarModular,
    PaginaSituacionFinancieraModular,
    PaginaViviendaModular
)

# Importar páginas ANTIGUAS que aún no están modularizadas
from src.ui.paginas import (
    PaginaInformacionFamiliar,
    PaginaSituacionFinanciera,
    PaginaVivienda,
    PaginaHistorialLaboral,
    PaginaReferencias,
    PaginaConclusiones,
    PaginaFotografias
)


class WizardEstudio(QWizard):
    """
    Wizard para capturar o editar un estudio socioeconomico completo.
    Guia al usuario a traves de 20 secciones.
    """
    
    # IDs de las paginas (v0.3.3 - 20 paginas)
    PAGE_EMPRESA = 0  # Empresa Solicitante
    PAGE_DATOS_PERSONALES = 1
    PAGE_SALUD = 2
    PAGE_FAMILIA = 3  # Tabla de miembros
    PAGE_FAMILIA_ADICIONAL = 4  # Campos adicionales familia
    PAGE_FINANZAS = 5  # Campos basicos y tabla gastos
    PAGE_FINANZAS_ADICIONAL = 6  # Campos adicionales financieros
    PAGE_VIVIENDA = 7  # Campos basicos vivienda
    PAGE_VIVIENDA_ADICIONAL = 8  # Campos adicionales vivienda
    PAGE_EMPLEO_ACTUAL = 9
    PAGE_HISTORIAL = 10
    PAGE_ESTILO_VIDA = 11
    PAGE_REFERENCIAS = 12
    PAGE_VISUALIZACION = 13  # Graficas
    PAGE_VALIDACION_DOCUMENTAL = 14
    PAGE_INVESTIGACION_VECINAL = 15
    PAGE_ANALISIS_CUALITATIVO = 16
    PAGE_INVESTIGADOR = 17
    PAGE_CONCLUSIONES = 18
    PAGE_FOTOGRAFIAS = 19
    
    def __init__(self, parent=None, config_empresa=None, estudio=None):
        """
        Inicializa el wizard.
        
        Args:
            parent: Widget padre.
            config_empresa: Configuración de la empresa.
            estudio: EstudioSocioeconomico existente (None para crear nuevo).
        """
        super().__init__(parent)
        
        self.config_empresa = config_empresa or {}
        self.estudio = estudio or EstudioSocioeconomico()
        self.es_edicion = estudio is not None
        
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz del wizard."""
        titulo = "Editar Estudio Socioeconómico" if self.es_edicion else "Nuevo Estudio Socioeconómico"
        self.setWindowTitle(titulo)
        self.setWizardStyle(QWizard.ModernStyle)
        self.setOption(QWizard.HaveHelpButton, False)
        
        # Botón "Info Concentrada" (CustomButton1)
        self.setOption(QWizard.HaveCustomButton1, True)
        self.setButtonText(QWizard.CustomButton1, "Info Concentrada")
        self.customButtonClicked.connect(self.on_custom_button_clicked)
        
        # Botón "Datos de Prueba" (CustomButton2) - NUEVO v0.3.0
        self.setOption(QWizard.HaveCustomButton2, True)
        self.setButtonText(QWizard.CustomButton2, "🎲 Generar Datos de Prueba")
        
        # Solo mostrar el botón de Info Concentrada si es edición
        if not self.es_edicion:
            self.setOption(QWizard.HaveCustomButton1, False)
        
        self.resize(900, 700)
        
        # Agregar páginas (v0.3.0 - Ahora inicia con selector de empresa)
        # Página INICIAL: Empresa Solicitante
        self.setPage(self.PAGE_EMPRESA, PaginaEmpresaSolicitante(self.estudio))
        
        # Páginas MODULARES (generadas automáticamente desde configuración)
        self.setPage(self.PAGE_DATOS_PERSONALES, PaginaDatosPersonalesModular(self.estudio))
        self.setPage(self.PAGE_SALUD, PaginaSaludModular(self.estudio))
        
        # Paginas TRADICIONALES (tablas y campos basicos)
        self.setPage(self.PAGE_FAMILIA, PaginaInformacionFamiliar(self.estudio))
        # NUEVA v0.3.3: Campos adicionales de informacion familiar
        self.setPage(self.PAGE_FAMILIA_ADICIONAL, PaginaInformacionFamiliarModular(self.estudio))
        
        self.setPage(self.PAGE_FINANZAS, PaginaSituacionFinanciera(self.estudio))
        # NUEVA v0.3.3: Campos adicionales financieros (ahorros, tarjetas, historial)
        self.setPage(self.PAGE_FINANZAS_ADICIONAL, PaginaSituacionFinancieraModular(self.estudio))
        
        self.setPage(self.PAGE_VIVIENDA, PaginaVivienda(self.estudio))
        # NUEVA v0.3.3: Campos adicionales vivienda (dimensiones, valor, propiedades)
        self.setPage(self.PAGE_VIVIENDA_ADICIONAL, PaginaViviendaModular(self.estudio))
        
        # Paginas MODULARES v0.2.0
        self.setPage(self.PAGE_EMPLEO_ACTUAL, PaginaEmpleoActualModular(self.estudio))
        
        # Páginas TRADICIONALES (continúan)
        self.setPage(self.PAGE_HISTORIAL, PaginaHistorialLaboral(self.estudio))
        
        # Página NUEVA MODULAR v0.2.0
        self.setPage(self.PAGE_ESTILO_VIDA, PaginaEstiloVidaModular(self.estudio))
        
        # Páginas TRADICIONALES (finales)
        self.setPage(self.PAGE_REFERENCIAS, PaginaReferencias(self.estudio))
        
        # Página NUEVA v0.3.0: Visualización con Gráficas
        self.setPage(self.PAGE_VISUALIZACION, PaginaVisualizacionDatos(self.estudio))
        
        # Páginas NUEVAS v0.3.2: Secciones Institucionales
        self.setPage(self.PAGE_VALIDACION_DOCUMENTAL, PaginaValidacionDocumentalModular(self.estudio))
        self.setPage(self.PAGE_INVESTIGACION_VECINAL, PaginaInvestigacionVecinalModular(self.estudio))
        self.setPage(self.PAGE_ANALISIS_CUALITATIVO, PaginaAnalisisCualitativoModular(self.estudio))
        self.setPage(self.PAGE_INVESTIGADOR, PaginaInvestigadorModular(self.estudio))
        
        self.setPage(self.PAGE_CONCLUSIONES, PaginaConclusiones(self.estudio))
        self.setPage(self.PAGE_FOTOGRAFIAS, PaginaFotografias(self.estudio))
        
        # Conectar señal de finalización
        self.finished.connect(self.al_finalizar)
    
    def on_custom_button_clicked(self, which):
        """Maneja clics en botones personalizados."""
        if which == QWizard.CustomButton1:
            self.mostrar_info_concentrada()
        elif which == QWizard.CustomButton2:
            self.generar_datos_prueba()
    
    def generar_datos_prueba(self):
        """Genera datos aleatorios de prueba para el estudio."""
        respuesta = QMessageBox.question(
            self,
            "Generar Datos de Prueba",
            "¿Desea rellenar el estudio con datos aleatorios de prueba?\n\n"
            "⚠️ ADVERTENCIA: Esto sobrescribirá cualquier información actual.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            try:
                # Generar datos completos
                datos_prueba = GeneradorDatosPrueba.generar_estudio_completo()
                
                # Actualizar el estudio campo por campo
                for seccion, datos in datos_prueba.items():
                    # Siempre sobrescribir con los nuevos datos
                    self.estudio.datos[seccion] = datos
                
                # Recargar la página actual para mostrar los nuevos datos
                pagina_actual_id = self.currentId()
                pagina_actual = self.currentPage()
                
                # Si la página tiene método cargar_datos, llamarlo
                if hasattr(pagina_actual, 'cargar_datos'):
                    pagina_actual.cargar_datos()
                
                # Si es una página modular, reinicializar
                if hasattr(pagina_actual, 'initializePage'):
                    pagina_actual.initializePage()
                
                QMessageBox.information(
                    self,
                    "Datos Generados",
                    "✅ Se han generado datos de prueba exitosamente.\n\n"
                    "Los datos se han cargado en el estudio. Navegue por las páginas para verlos."
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Error",
                    f"❌ Error al generar datos de prueba:\n{str(e)}"
                )
    
    def mostrar_info_concentrada(self):
        """Muestra el diálogo con la información concentrada para IA."""
        from src.ui.dialogo_info_ia import DialogoInfoIA
        
        # Guardar datos actuales en el estudio temporalmente
        self.guardar_datos_temporales()
        
        # Generar resumen
        resumen = self.estudio.obtener_resumen_ia()
        
        # Mostrar diálogo
        dialogo = DialogoInfoIA(resumen, self)
        dialogo.exec_()
    
    def guardar_datos_temporales(self):
        """Guarda los datos actuales de todas las páginas en el estudio."""
        for page_id in range(self.PAGE_DATOS_PERSONALES, self.PAGE_FOTOGRAFIAS + 1):
            page = self.page(page_id)
            if page and hasattr(page, 'guardar_datos'):
                page.guardar_datos()
    
    def al_finalizar(self, result):
        """
        Se ejecuta cuando se finaliza el wizard.
        
        Args:
            result: Resultado del wizard (aceptado o rechazado).
        """
        if result == QWizard.Accepted:
            # Guardar datos de todas las páginas
            self.guardar_datos_temporales()
            
            # Calcular riesgos
            riesgos = CalculadorRiesgos.calcular_todos_riesgos(self.estudio.datos)
            self.estudio.datos['riesgos'] = riesgos
            
            # Guardar estudio
            if self.estudio.guardar():
                return True
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "No se pudo guardar el estudio. Verifique los permisos de escritura."
                )
                return False
        
        return False
