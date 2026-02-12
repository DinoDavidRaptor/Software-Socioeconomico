"""
Dialogo de activacion de licencia.
Copyright (c) 2026 DINOS Tech. Todos los derechos reservados.
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QGroupBox, QFormLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from src.licensing import LicenseValidator, get_hardware_id
from src.licensing.hardware_id import get_hardware_id_display


class DialogoActivacion(QDialog):
    """Dialogo para activar licencia del software."""
    
    def __init__(self, parent=None, license_file: str = "license.dat"):
        super().__init__(parent)
        self.license_file = license_file
        self.validator = LicenseValidator(license_file)
        self.activated = False
        
        self.setWindowTitle("Activacion de Licencia - DINOS Tech")
        self.setFixedSize(550, 400)
        self.setModal(True)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Titulo
        titulo = QLabel("Ecosistema Comercial 360")
        titulo.setFont(QFont("Arial", 16, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        subtitulo = QLabel("Sistema de Estudios Socioeconomicos")
        subtitulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitulo)
        
        # Separador
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        layout.addWidget(line)
        
        # Informacion del equipo
        grupo_hw = QGroupBox("Informacion del Equipo")
        hw_layout = QFormLayout(grupo_hw)
        
        self.lbl_hardware_id = QLabel(get_hardware_id_display())
        self.lbl_hardware_id.setFont(QFont("Consolas", 12))
        self.lbl_hardware_id.setTextInteractionFlags(Qt.TextSelectableByMouse)
        hw_layout.addRow("Hardware ID:", self.lbl_hardware_id)
        
        btn_copiar_hw = QPushButton("Copiar Hardware ID")
        btn_copiar_hw.clicked.connect(self._copiar_hardware_id)
        hw_layout.addRow("", btn_copiar_hw)
        
        layout.addWidget(grupo_hw)
        
        # Activacion
        grupo_act = QGroupBox("Activar Licencia")
        act_layout = QFormLayout(grupo_act)
        
        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Nombre del licenciatario")
        act_layout.addRow("Nombre:", self.txt_nombre)
        
        self.txt_empresa = QLineEdit()
        self.txt_empresa.setPlaceholderText("Empresa (opcional)")
        act_layout.addRow("Empresa:", self.txt_empresa)
        
        self.txt_licencia = QLineEdit()
        self.txt_licencia.setPlaceholderText("XXXX-XXXX-XXXX-XXXX-XXXX")
        self.txt_licencia.setFont(QFont("Consolas", 11))
        act_layout.addRow("Licencia:", self.txt_licencia)
        
        layout.addWidget(grupo_act)
        
        # Instrucciones
        instrucciones = QLabel(
            "Para obtener una licencia, contacte a DINOS Tech\n"
            "proporcionando su Hardware ID."
        )
        instrucciones.setAlignment(Qt.AlignCenter)
        instrucciones.setStyleSheet("color: gray;")
        layout.addWidget(instrucciones)
        
        # Botones
        btn_layout = QHBoxLayout()
        
        btn_activar = QPushButton("Activar Licencia")
        btn_activar.setDefault(True)
        btn_activar.clicked.connect(self._activar)
        btn_layout.addWidget(btn_activar)
        
        btn_salir = QPushButton("Salir")
        btn_salir.clicked.connect(self.reject)
        btn_layout.addWidget(btn_salir)
        
        layout.addLayout(btn_layout)
    
    def _copiar_hardware_id(self):
        """Copia el Hardware ID al portapapeles."""
        from PyQt5.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        clipboard.setText(get_hardware_id_display())
        QMessageBox.information(
            self, "Copiado", 
            "Hardware ID copiado al portapapeles.\n\n"
            "Envie este ID a DINOS Tech para obtener su licencia."
        )
    
    def _activar(self):
        """Intenta activar la licencia."""
        nombre = self.txt_nombre.text().strip()
        empresa = self.txt_empresa.text().strip()
        licencia = self.txt_licencia.text().strip()
        
        if not nombre:
            QMessageBox.warning(self, "Error", "Ingrese su nombre")
            return
        
        if not licencia:
            QMessageBox.warning(self, "Error", "Ingrese la clave de licencia")
            return
        
        # Intentar activar
        success, message = self.validator.activate_license(licencia, nombre, empresa)
        
        if success:
            self.activated = True
            QMessageBox.information(
                self, "Licencia Activada",
                f"{message}\n\nGracias por elegir DINOS Tech."
            )
            self.accept()
        else:
            QMessageBox.critical(self, "Error de Activacion", message)


class DialogoLicenciaInfo(QDialog):
    """Dialogo para mostrar informacion de licencia activa."""
    
    def __init__(self, license_info: dict, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Informacion de Licencia")
        self.setFixedSize(400, 250)
        
        layout = QVBoxLayout(self)
        
        titulo = QLabel("Licencia Activa")
        titulo.setFont(QFont("Arial", 14, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        grupo = QGroupBox("Detalles")
        form = QFormLayout(grupo)
        
        form.addRow("Licenciatario:", QLabel(license_info.get('licensed_to', '')))
        form.addRow("Empresa:", QLabel(license_info.get('company', '') or 'N/A'))
        form.addRow("Tipo:", QLabel(license_info.get('license_type', '')))
        form.addRow("Expiracion:", QLabel(license_info.get('expiry_date', '')))
        form.addRow("Hardware ID:", QLabel(get_hardware_id_display()))
        
        layout.addWidget(grupo)
        
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.accept)
        layout.addWidget(btn_cerrar)
