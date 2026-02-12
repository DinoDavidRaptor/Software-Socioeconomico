"""
Dialogo de gestion de backups.
Permite exportar e importar estudios.
Copyright (c) 2026 DINOS Tech. Todos los derechos reservados.
"""

import os
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QMessageBox, QGroupBox, QFileDialog, QCheckBox, QProgressBar
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from src.utils.gestor_backup import GestorBackup, generar_nombre_backup


class DialogoBackup(QDialog):
    """Dialogo para exportar e importar backups."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gestor = GestorBackup()
        self.backup_importado = False
        
        self.setWindowTitle("Gestion de Backups")
        self.setFixedSize(500, 400)
        self.setModal(True)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Titulo
        titulo = QLabel("Gestion de Backups")
        titulo.setFont(QFont("Arial", 14, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)
        
        descripcion = QLabel(
            "Exporte sus estudios para crear un respaldo o importe\n"
            "un backup anterior para restaurar sus datos."
        )
        descripcion.setAlignment(Qt.AlignCenter)
        descripcion.setStyleSheet("color: #666;")
        layout.addWidget(descripcion)
        
        # Seccion Exportar
        grupo_export = QGroupBox("Exportar Backup")
        export_layout = QVBoxLayout(grupo_export)
        
        export_desc = QLabel(
            "Crea un archivo ZIP con todos sus estudios, fotos y configuracion.\n"
            "Guarde este archivo en un lugar seguro."
        )
        export_desc.setStyleSheet("color: #555;")
        export_layout.addWidget(export_desc)
        
        btn_exportar = QPushButton("Exportar Backup...")
        btn_exportar.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 12px 20px;
                font-size: 13px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #229954; }
        """)
        btn_exportar.clicked.connect(self._exportar)
        export_layout.addWidget(btn_exportar)
        
        layout.addWidget(grupo_export)
        
        # Seccion Importar
        grupo_import = QGroupBox("Importar Backup")
        import_layout = QVBoxLayout(grupo_import)
        
        import_desc = QLabel(
            "Restaura estudios desde un archivo de backup.\n"
            "Los estudios existentes no se sobrescriben por defecto."
        )
        import_desc.setStyleSheet("color: #555;")
        import_layout.addWidget(import_desc)
        
        self.chk_sobrescribir = QCheckBox("Sobrescribir estudios existentes")
        self.chk_sobrescribir.setToolTip(
            "Si esta marcado, los estudios con el mismo ID seran reemplazados"
        )
        import_layout.addWidget(self.chk_sobrescribir)
        
        btn_importar = QPushButton("Importar Backup...")
        btn_importar.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 12px 20px;
                font-size: 13px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover { background-color: #2980b9; }
        """)
        btn_importar.clicked.connect(self._importar)
        import_layout.addWidget(btn_importar)
        
        layout.addWidget(grupo_import)
        
        # Barra de progreso (oculta por defecto)
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        layout.addWidget(self.progress)
        
        # Boton cerrar
        layout.addStretch()
        
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(self.accept)
        layout.addWidget(btn_cerrar)
    
    def _exportar(self):
        """Exporta un backup."""
        nombre_default = generar_nombre_backup()
        
        archivo, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Backup",
            nombre_default,
            "Archivos ZIP (*.zip)"
        )
        
        if not archivo:
            return
        
        # Mostrar progreso
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)  # Indeterminado
        
        try:
            exito, mensaje, count = self.gestor.exportar_backup(archivo)
            
            self.progress.setVisible(False)
            
            if exito:
                QMessageBox.information(
                    self,
                    "Backup Exportado",
                    f"{mensaje}\n\nArchivo guardado en:\n{archivo}"
                )
            else:
                QMessageBox.critical(self, "Error", mensaje)
                
        except Exception as e:
            self.progress.setVisible(False)
            QMessageBox.critical(self, "Error", f"Error inesperado: {e}")
    
    def _importar(self):
        """Importa un backup."""
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Backup",
            "",
            "Archivos ZIP (*.zip)"
        )
        
        if not archivo:
            return
        
        # Obtener info del backup
        info = self.gestor.obtener_info_backup(archivo)
        
        if not info:
            QMessageBox.warning(
                self,
                "Archivo Invalido",
                "El archivo seleccionado no es un backup valido."
            )
            return
        
        # Confirmar importacion
        tamano_mb = info['tamano'] / (1024 * 1024)
        confirmacion = QMessageBox.question(
            self,
            "Confirmar Importacion",
            f"Backup del: {info['fecha'][:10]}\n"
            f"Estudios: {info['estudios']}\n"
            f"Fotos: {info['fotos']}\n"
            f"Tamano: {tamano_mb:.2f} MB\n\n"
            f"¿Desea importar este backup?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirmacion != QMessageBox.Yes:
            return
        
        # Mostrar progreso
        self.progress.setVisible(True)
        self.progress.setRange(0, 0)
        
        try:
            sobrescribir = self.chk_sobrescribir.isChecked()
            exito, mensaje, count = self.gestor.importar_backup(archivo, sobrescribir)
            
            self.progress.setVisible(False)
            
            if exito:
                self.backup_importado = True
                QMessageBox.information(
                    self,
                    "Backup Importado",
                    f"{mensaje}\n\n"
                    "La lista de estudios se actualizara al cerrar este dialogo."
                )
            else:
                QMessageBox.critical(self, "Error", mensaje)
                
        except Exception as e:
            self.progress.setVisible(False)
            QMessageBox.critical(self, "Error", f"Error inesperado: {e}")
