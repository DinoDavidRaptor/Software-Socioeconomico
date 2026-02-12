"""
Página inicial del wizard con selector de empresa solicitante.
Autor: DINOS Tech
Versión: 0.3.0
"""

from PyQt5.QtWidgets import (
    QWizardPage, QVBoxLayout, QHBoxLayout, QLabel, 
    QComboBox, QPushButton, QLineEdit, QDialog, QMessageBox,
    QDialogButtonBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from src.utils.gestor_empresas import GestorEmpresas


class DialogoNuevaEmpresa(QDialog):
    """Diálogo para agregar una nueva empresa."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Nueva Empresa")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # Instrucciones
        instrucciones = QLabel("Ingrese el nombre de la empresa que solicita el estudio:")
        instrucciones.setWordWrap(True)
        layout.addWidget(instrucciones)
        
        # Campo de texto
        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ej: Corporativo XYZ S.A. de C.V.")
        layout.addWidget(self.input_nombre)
        
        # Botones
        botones = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        botones.accepted.connect(self.accept)
        botones.rejected.connect(self.reject)
        layout.addWidget(botones)
        
        self.setLayout(layout)
    
    def get_nombre_empresa(self) -> str:
        """Retorna el nombre de la empresa ingresado."""
        return self.input_nombre.text().strip()


class PaginaEmpresaSolicitante(QWizardPage):
    """Primera página del wizard: selección de empresa solicitante."""
    
    def __init__(self, estudio):
        super().__init__()
        self.estudio = estudio
        self.setTitle("Empresa Solicitante")
        self.setSubTitle("Seleccione la empresa para la cual se realizará este estudio socioeconómico")
        
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        layout = QVBoxLayout()
        
        # Espaciador superior
        layout.addSpacing(20)
        
        # Label informativo
        info_label = QLabel(
            "Este campo identifica la empresa u organización que solicita el estudio. "
            "Seleccione una empresa existente o agregue una nueva."
        )
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #555; font-size: 11pt; padding: 10px;")
        layout.addWidget(info_label)
        
        layout.addSpacing(10)
        
        # Selector de empresa
        selector_layout = QHBoxLayout()
        
        empresa_label = QLabel("Empresa:")
        empresa_label.setFont(QFont("Arial", 11, QFont.Bold))
        selector_layout.addWidget(empresa_label)
        
        self.combo_empresa = QComboBox()
        self.combo_empresa.setMinimumHeight(35)
        self.combo_empresa.setStyleSheet("""
            QComboBox {
                font-size: 11pt;
                padding: 5px;
                border: 2px solid #3498db;
                border-radius: 5px;
            }
            QComboBox:focus {
                border: 2px solid #2980b9;
            }
        """)
        self.cargar_empresas()
        self.combo_empresa.currentTextChanged.connect(self.on_empresa_changed)
        self.combo_empresa.currentTextChanged.connect(self.completeChanged)
        selector_layout.addWidget(self.combo_empresa, 1)
        
        # Botón para agregar empresa
        self.btn_agregar = QPushButton("+ Nueva")
        self.btn_agregar.setMinimumHeight(35)
        self.btn_agregar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                font-size: 10pt;
                font-weight: bold;
                border: none;
                border-radius: 5px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        self.btn_agregar.clicked.connect(self.agregar_nueva_empresa)
        selector_layout.addWidget(self.btn_agregar)
        
        layout.addLayout(selector_layout)
        
        layout.addSpacing(20)
        
        # Información adicional
        nota_label = QLabel(
            "💡 Tip: Las empresas se guardan automáticamente y estarán disponibles "
            "para futuros estudios."
        )
        nota_label.setWordWrap(True)
        nota_label.setStyleSheet("""
            background-color: #e8f5e9;
            color: #2e7d32;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #27ae60;
            font-size: 10pt;
        """)
        layout.addWidget(nota_label)
        
        # Espaciador para empujar todo hacia arriba
        layout.addStretch()
        
        self.setLayout(layout)
    
    def cargar_empresas(self):
        """Carga las empresas desde el gestor."""
        self.combo_empresa.clear()
        empresas = GestorEmpresas.cargar_empresas()
        self.combo_empresa.addItems(empresas)
        
        # Seleccionar la empresa guardada en el estudio, o la primera si no hay guardada
        empresa_guardada = self.estudio.datos.get("empresa_solicitante", "")
        if empresa_guardada and empresa_guardada in empresas:
            self.combo_empresa.setCurrentText(empresa_guardada)
        elif empresas:
            # Si no hay empresa guardada, seleccionar la primera y guardarla
            self.combo_empresa.setCurrentIndex(0)
            self.estudio.datos["empresa_solicitante"] = empresas[0]
        
        # Emitir señal para actualizar estado del botón Next
        self.completeChanged.emit()
    
    def agregar_nueva_empresa(self):
        """Abre el diálogo para agregar una nueva empresa."""
        dialogo = DialogoNuevaEmpresa(self)
        
        if dialogo.exec_() == QDialog.Accepted:
            nombre_empresa = dialogo.get_nombre_empresa()
            
            if not nombre_empresa:
                QMessageBox.warning(
                    self,
                    "Campo Vacío",
                    "Por favor ingrese un nombre para la empresa."
                )
                return
            
            if GestorEmpresas.agregar_empresa(nombre_empresa):
                self.cargar_empresas()
                self.combo_empresa.setCurrentText(nombre_empresa)
                QMessageBox.information(
                    self,
                    "Empresa Agregada",
                    f"La empresa '{nombre_empresa}' ha sido agregada exitosamente."
                )
            else:
                QMessageBox.warning(
                    self,
                    "Error",
                    f"No se pudo agregar la empresa. Puede que ya exista."
                )
    
    def on_empresa_changed(self, empresa):
        """Se ejecuta cuando cambia la empresa seleccionada."""
        self.estudio.datos["empresa_solicitante"] = empresa
    
    def initializePage(self):
        """Se ejecuta cuando se muestra la página."""
        # Cargar la empresa guardada si existe
        empresa_guardada = self.estudio.datos.get("empresa_solicitante", "")
        if empresa_guardada:
            self.combo_empresa.setCurrentText(empresa_guardada)
        elif self.combo_empresa.count() > 0:
            # Si no hay empresa guardada, usar la primera
            self.estudio.datos["empresa_solicitante"] = self.combo_empresa.currentText()
    
    def isComplete(self):
        """Verifica si la página está completa para habilitar el botón Next."""
        empresa = self.combo_empresa.currentText()
        return bool(empresa and empresa.strip())
    
    def validatePage(self):
        """Valida que haya una empresa seleccionada antes de continuar."""
        empresa = self.combo_empresa.currentText()
        if not empresa or empresa.strip() == "":
            QMessageBox.warning(
                self,
                "Empresa Requerida",
                "Por favor seleccione o agregue una empresa antes de continuar."
            )
            return False
        
        # Guardar la empresa seleccionada
        self.estudio.datos["empresa_solicitante"] = empresa
        return True
