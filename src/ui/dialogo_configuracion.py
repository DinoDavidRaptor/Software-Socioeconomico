"""
Dialogo de configuracion de empresa.
Permite editar nombre, direccion, telefono, email y logo.
Copyright (c) 2026 DINOS Tech. Todos los derechos reservados.
"""

import os
import json
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QGroupBox, QFormLayout, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap


class DialogoConfiguracion(QDialog):
    """Dialogo para configurar datos de la empresa."""
    
    def __init__(self, parent=None, config_file: str = "config.json"):
        super().__init__(parent)
        self.config_file = config_file
        self.config = self._cargar_config()
        self.logo_path = self.config.get('empresa', {}).get('logo', '')
        self.cambios_guardados = False
        
        self.setWindowTitle("Configuracion de Empresa")
        self.setFixedSize(500, 450)
        self.setModal(True)
        
        self._setup_ui()
        self._cargar_datos()
    
    def _cargar_config(self) -> dict:
        """Carga la configuracion actual."""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {'empresa': {}}
    
    def _setup_ui(self):
        """Configura la interfaz."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Titulo
        titulo = QLabel("Configuracion de Empresa")
        titulo.setFont(QFont("Arial", 14, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        # Grupo de datos
        grupo = QGroupBox("Datos de la Empresa")
        form = QFormLayout(grupo)
        
        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Nombre de la empresa")
        form.addRow("Nombre:", self.txt_nombre)
        
        self.txt_direccion = QLineEdit()
        self.txt_direccion.setPlaceholderText("Direccion completa")
        form.addRow("Direccion:", self.txt_direccion)
        
        self.txt_telefono = QLineEdit()
        self.txt_telefono.setPlaceholderText("+52 (XX) XXXX-XXXX")
        form.addRow("Telefono:", self.txt_telefono)
        
        self.txt_email = QLineEdit()
        self.txt_email.setPlaceholderText("correo@empresa.com")
        form.addRow("Email:", self.txt_email)
        
        layout.addWidget(grupo)
        
        # Grupo de logo
        grupo_logo = QGroupBox("Logo de la Empresa")
        logo_layout = QVBoxLayout(grupo_logo)
        
        # Preview del logo
        self.lbl_logo_preview = QLabel("Sin logo")
        self.lbl_logo_preview.setAlignment(Qt.AlignCenter)
        self.lbl_logo_preview.setFixedHeight(80)
        self.lbl_logo_preview.setStyleSheet("border: 1px dashed #ccc; background: #f9f9f9;")
        logo_layout.addWidget(self.lbl_logo_preview)
        
        # Ruta del logo
        logo_path_layout = QHBoxLayout()
        self.txt_logo = QLineEdit()
        self.txt_logo.setPlaceholderText("Ruta al archivo de logo")
        self.txt_logo.setReadOnly(True)
        logo_path_layout.addWidget(self.txt_logo)
        
        btn_seleccionar = QPushButton("Seleccionar...")
        btn_seleccionar.clicked.connect(self._seleccionar_logo)
        logo_path_layout.addWidget(btn_seleccionar)
        
        btn_quitar = QPushButton("Quitar")
        btn_quitar.clicked.connect(self._quitar_logo)
        logo_path_layout.addWidget(btn_quitar)
        
        logo_layout.addLayout(logo_path_layout)
        layout.addWidget(grupo_logo)
        
        # Botones
        btn_layout = QHBoxLayout()
        
        btn_guardar = QPushButton("Guardar Cambios")
        btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #229954; }
        """)
        btn_guardar.clicked.connect(self._guardar)
        btn_layout.addWidget(btn_guardar)
        
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)
        btn_layout.addWidget(btn_cancelar)
        
        layout.addLayout(btn_layout)
    
    def _cargar_datos(self):
        """Carga los datos actuales en los campos."""
        empresa = self.config.get('empresa', {})
        self.txt_nombre.setText(empresa.get('nombre', ''))
        self.txt_direccion.setText(empresa.get('direccion', ''))
        self.txt_telefono.setText(empresa.get('telefono', ''))
        self.txt_email.setText(empresa.get('email', ''))
        
        logo = empresa.get('logo', '')
        if logo:
            self.txt_logo.setText(logo)
            self._mostrar_preview_logo(logo)
    
    def _seleccionar_logo(self):
        """Abre dialogo para seleccionar logo."""
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Logo",
            "",
            "Imagenes (*.png *.jpg *.jpeg *.bmp *.ico);;Todos (*.*)"
        )
        
        if archivo:
            # Copiar a assets si no esta ahi
            assets_dir = "assets"
            os.makedirs(assets_dir, exist_ok=True)
            
            nombre_archivo = os.path.basename(archivo)
            destino = os.path.join(assets_dir, nombre_archivo)
            
            if archivo != destino:
                import shutil
                try:
                    shutil.copy2(archivo, destino)
                    self.logo_path = destino
                except Exception as e:
                    QMessageBox.warning(self, "Error", f"No se pudo copiar el logo: {e}")
                    self.logo_path = archivo
            else:
                self.logo_path = archivo
            
            self.txt_logo.setText(self.logo_path)
            self._mostrar_preview_logo(self.logo_path)
    
    def _quitar_logo(self):
        """Quita el logo seleccionado."""
        self.logo_path = ""
        self.txt_logo.setText("")
        self.lbl_logo_preview.setPixmap(QPixmap())
        self.lbl_logo_preview.setText("Sin logo")
    
    def _mostrar_preview_logo(self, path: str):
        """Muestra preview del logo."""
        if path and os.path.exists(path):
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                self.lbl_logo_preview.setPixmap(
                    pixmap.scaled(150, 70, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                )
                self.lbl_logo_preview.setText("")
    
    def _guardar(self):
        """Guarda la configuracion."""
        nombre = self.txt_nombre.text().strip()
        
        if not nombre:
            QMessageBox.warning(self, "Error", "El nombre de la empresa es obligatorio")
            return
        
        self.config['empresa'] = {
            'nombre': nombre,
            'direccion': self.txt_direccion.text().strip(),
            'telefono': self.txt_telefono.text().strip(),
            'email': self.txt_email.text().strip(),
            'logo': self.logo_path
        }
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            self.cambios_guardados = True
            QMessageBox.information(
                self, "Guardado",
                "Configuracion guardada correctamente.\n\n"
                "Reinicie la aplicacion para ver los cambios en el encabezado."
            )
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo guardar: {e}")
