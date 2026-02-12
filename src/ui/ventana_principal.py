"""
Ventana principal del sistema de estudios socioeconómicos.
Autor: DINOS Tech
Versión: 0.4.0
"""

import sys
import os
import json
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QTableWidget, QTableWidgetItem, QLabel, QMessageBox, QFileDialog,
    QHeaderView, QDialog, QMenuBar, QMenu, QAction
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QIcon
from src.models.estudio import EstudioSocioeconomico
from src.logic.calculador_riesgos import CalculadorRiesgos
from src.ui.wizard_estudio import WizardEstudio
from src.ui.dialogo_info_ia import DialogoInfoIA
from src.ui.dialogo_configuracion import DialogoConfiguracion
from src.ui.dialogo_backup import DialogoBackup
from src.export.exportador_pdf import ExportadorPDF
from src.export.exportador_word import ExportadorWord
from src.export.exportador_excel import ExportadorExcel


class VentanaPrincipal(QMainWindow):
    """Ventana principal de la aplicación."""
    
    def __init__(self):
        super().__init__()
        self.config_empresa = self.cargar_configuracion()
        self.init_ui()
        self.cargar_estudios()
    
    def cargar_configuracion(self):
        """Carga la configuración de la empresa desde config.json."""
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config.get('empresa', {})
        except Exception as e:
            QMessageBox.warning(None, "Advertencia", 
                              f"No se pudo cargar la configuración: {e}\nSe usarán valores predeterminados.")
            return {
                "nombre": "DINOS Tech",
                "direccion": "",
                "telefono": "",
                "email": "",
                "logo": ""
            }
    
    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        self.setWindowTitle(f"Ecosistema Comercial 360 - {self.config_empresa.get('nombre', 'DINOS Tech')}")
        self.setGeometry(100, 100, 1200, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Encabezado con logo y título
        header_layout = QHBoxLayout()
        
        # Logo
        logo_path = self.config_empresa.get('logo', '')
        if logo_path and os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            if not pixmap.isNull():
                logo_label.setPixmap(pixmap.scaled(80, 80, Qt.KeepAspectRatio, Qt.SmoothTransformation))
                header_layout.addWidget(logo_label)
        
        # Información de la empresa
        info_layout = QVBoxLayout()
        
        nombre_label = QLabel(self.config_empresa.get('nombre', 'DINOS Tech'))
        nombre_font = QFont()
        nombre_font.setPointSize(16)
        nombre_font.setBold(True)
        nombre_label.setFont(nombre_font)
        info_layout.addWidget(nombre_label)
        
        subtitulo_label = QLabel("Sistema de Estudios Socioeconómicos")
        subtitulo_font = QFont()
        subtitulo_font.setPointSize(10)
        subtitulo_label.setFont(subtitulo_font)
        subtitulo_label.setStyleSheet("color: #666;")
        info_layout.addWidget(subtitulo_label)
        
        direccion = self.config_empresa.get('direccion', '')
        if direccion:
            dir_label = QLabel(direccion)
            dir_label.setStyleSheet("color: #888;")
            info_layout.addWidget(dir_label)
        
        header_layout.addLayout(info_layout)
        header_layout.addStretch()
        
        # Botones de configuracion y backup (lado derecho del header)
        config_buttons_layout = QVBoxLayout()
        
        btn_configuracion = QPushButton("Configuracion")
        btn_configuracion.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 8px 15px;
                font-size: 11px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #7f8c8d; }
        """)
        btn_configuracion.clicked.connect(self.abrir_configuracion)
        config_buttons_layout.addWidget(btn_configuracion)
        
        btn_backup = QPushButton("Backup")
        btn_backup.setStyleSheet("""
            QPushButton {
                background-color: #34495e;
                color: white;
                padding: 8px 15px;
                font-size: 11px;
                border: none;
                border-radius: 4px;
            }
            QPushButton:hover { background-color: #2c3e50; }
        """)
        btn_backup.clicked.connect(self.abrir_backup)
        config_buttons_layout.addWidget(btn_backup)
        
        header_layout.addLayout(config_buttons_layout)
        
        main_layout.addLayout(header_layout)
        
        # Línea separadora
        line = QLabel()
        line.setFrameStyle(QLabel.HLine | QLabel.Sunken)
        main_layout.addWidget(line)
        
        # Botones de acción
        buttons_layout = QHBoxLayout()
        
        self.btn_nuevo = QPushButton("Crear Nuevo Estudio")
        self.btn_nuevo.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 10px 20px;
                font-size: 12px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        self.btn_nuevo.clicked.connect(self.crear_nuevo_estudio)
        buttons_layout.addWidget(self.btn_nuevo)
        
        self.btn_editar = QPushButton("Editar Estudio")
        self.btn_editar.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                padding: 10px 20px;
                font-size: 12px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.btn_editar.clicked.connect(self.editar_estudio)
        self.btn_editar.setEnabled(False)
        buttons_layout.addWidget(self.btn_editar)
        
        self.btn_eliminar = QPushButton("Eliminar Estudio")
        self.btn_eliminar.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 10px 20px;
                font-size: 12px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.btn_eliminar.clicked.connect(self.eliminar_estudio)
        self.btn_eliminar.setEnabled(False)
        buttons_layout.addWidget(self.btn_eliminar)
        
        buttons_layout.addStretch()
        
        self.btn_exportar_pdf = QPushButton("Exportar a PDF")
        self.btn_exportar_pdf.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                padding: 10px 20px;
                font-size: 12px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        self.btn_exportar_pdf.clicked.connect(self.exportar_pdf)
        self.btn_exportar_pdf.setEnabled(False)
        buttons_layout.addWidget(self.btn_exportar_pdf)
        
        self.btn_exportar_word = QPushButton("Exportar a Word")
        self.btn_exportar_word.setStyleSheet("""
            QPushButton {
                background-color: #2c3e50;
                color: white;
                padding: 10px 20px;
                font-size: 12px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #1a252f;
            }
        """)
        self.btn_exportar_word.clicked.connect(self.exportar_word)
        self.btn_exportar_word.setEnabled(False)
        buttons_layout.addWidget(self.btn_exportar_word)
        
        self.btn_exportar_excel = QPushButton("Exportar a Excel")
        self.btn_exportar_excel.setStyleSheet("""
            QPushButton {
                background-color: #16a085;
                color: white;
                padding: 10px 20px;
                font-size: 12px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #138d75;
            }
        """)
        self.btn_exportar_excel.clicked.connect(self.exportar_excel)
        buttons_layout.addWidget(self.btn_exportar_excel)
        
        main_layout.addLayout(buttons_layout)
        
        # Tabla de estudios
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(5)
        self.tabla.setHorizontalHeaderLabels([
            "Nombre del Candidato", 
            "Fecha de Creación", 
            "Última Modificación",
            "Riesgo Global",
            "ID"
        ])
        
        # Configurar tabla
        self.tabla.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla.horizontalHeader().setStretchLastSection(False)
        self.tabla.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla.setColumnWidth(1, 150)
        self.tabla.setColumnWidth(2, 150)
        self.tabla.setColumnWidth(3, 120)
        self.tabla.setColumnWidth(4, 150)
        
        self.tabla.itemSelectionChanged.connect(self.actualizar_botones)
        self.tabla.doubleClicked.connect(self.editar_estudio)
        
        main_layout.addWidget(self.tabla)
        
        # Barra de estado
        self.statusBar().showMessage("Listo")
    
    def cargar_estudios(self):
        """Carga la lista de estudios en la tabla."""
        self.tabla.setRowCount(0)
        estudios = EstudioSocioeconomico.listar_estudios()
        
        for estudio in estudios:
            row = self.tabla.rowCount()
            self.tabla.insertRow(row)
            
            # Nombre
            self.tabla.setItem(row, 0, QTableWidgetItem(estudio['nombre']))
            
            # Fecha creación
            fecha_creacion = estudio['fecha_creacion'].split('T')[0] if 'T' in estudio['fecha_creacion'] else estudio['fecha_creacion']
            self.tabla.setItem(row, 1, QTableWidgetItem(fecha_creacion))
            
            # Fecha modificación
            fecha_mod = estudio['fecha_modificacion'].split('T')[0] if 'T' in estudio['fecha_modificacion'] else estudio['fecha_modificacion']
            self.tabla.setItem(row, 2, QTableWidgetItem(fecha_mod))
            
            # Riesgo global con color
            riesgo_raw = estudio.get('riesgo_global', 1)
            # Handle case where riesgo_global is a dict instead of a number
            if isinstance(riesgo_raw, dict):
                riesgo = riesgo_raw.get('nivel', 1) if isinstance(riesgo_raw.get('nivel'), (int, float)) else 1
            elif isinstance(riesgo_raw, (int, float)):
                riesgo = float(riesgo_raw)
            else:
                riesgo = 1
            riesgo_item = QTableWidgetItem(f"{riesgo:.1f} - {CalculadorRiesgos.obtener_interpretacion_riesgo(int(riesgo))}")
            riesgo_item.setTextAlignment(Qt.AlignCenter)
            
            # Colorear según riesgo
            if riesgo <= 1.5:
                riesgo_item.setBackground(Qt.green)
            elif riesgo <= 2.5:
                riesgo_item.setBackground(Qt.yellow)
            elif riesgo <= 3.5:
                riesgo_item.setBackground(Qt.GlobalColor(208))  # Naranja
            else:
                riesgo_item.setBackground(Qt.red)
                riesgo_item.setForeground(Qt.white)
            
            self.tabla.setItem(row, 3, riesgo_item)
            
            # ID (oculto pero útil)
            self.tabla.setItem(row, 4, QTableWidgetItem(estudio['id']))
        
        self.statusBar().showMessage(f"{len(estudios)} estudio(s) cargado(s)")
    
    def actualizar_botones(self):
        """Actualiza el estado de los botones según la selección."""
        hay_seleccion = len(self.tabla.selectedItems()) > 0
        self.btn_editar.setEnabled(hay_seleccion)
        self.btn_eliminar.setEnabled(hay_seleccion)
        self.btn_exportar_pdf.setEnabled(hay_seleccion)
        self.btn_exportar_word.setEnabled(hay_seleccion)
    
    def crear_nuevo_estudio(self):
        """Abre el wizard para crear un nuevo estudio."""
        wizard = WizardEstudio(self, self.config_empresa)
        if wizard.exec_() == QDialog.Accepted:
            self.cargar_estudios()
            QMessageBox.information(self, "Éxito", "Estudio creado correctamente")
    
    def editar_estudio(self):
        """Abre el wizard para editar el estudio seleccionado."""
        row = self.tabla.currentRow()
        if row < 0:
            return
        
        id_estudio = self.tabla.item(row, 4).text()
        estudio = EstudioSocioeconomico.cargar(id_estudio)
        
        if not estudio:
            QMessageBox.critical(self, "Error", "No se pudo cargar el estudio")
            return
        
        wizard = WizardEstudio(self, self.config_empresa, estudio)
        if wizard.exec_() == QDialog.Accepted:
            self.cargar_estudios()
            QMessageBox.information(self, "Éxito", "Estudio actualizado correctamente")
    
    def eliminar_estudio(self):
        """Elimina el estudio seleccionado."""
        row = self.tabla.currentRow()
        if row < 0:
            return
        
        nombre = self.tabla.item(row, 0).text()
        id_estudio = self.tabla.item(row, 4).text()
        
        respuesta = QMessageBox.question(
            self, 
            "Confirmar eliminación",
            f"¿Está seguro de eliminar el estudio de {nombre}?\nEsta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if respuesta == QMessageBox.Yes:
            if EstudioSocioeconomico.eliminar(id_estudio):
                self.cargar_estudios()
                QMessageBox.information(self, "Éxito", "Estudio eliminado correctamente")
            else:
                QMessageBox.critical(self, "Error", "No se pudo eliminar el estudio")
    
    def exportar_pdf(self):
        """Exporta el estudio seleccionado a PDF."""
        row = self.tabla.currentRow()
        if row < 0:
            return
        
        id_estudio = self.tabla.item(row, 4).text()
        estudio = EstudioSocioeconomico.cargar(id_estudio)
        
        if not estudio:
            QMessageBox.critical(self, "Error", "No se pudo cargar el estudio")
            return
        
        # Nombre de archivo sugerido
        nombre = estudio.datos.get("datos_personales", {}).get("nombre_completo", "estudio")
        nombre_archivo = f"Estudio_{nombre.replace(' ', '_')}_{estudio.id}.pdf"
        
        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar PDF",
            os.path.join("export", nombre_archivo),
            "Archivos PDF (*.pdf)"
        )
        
        if ruta:
            exportador = ExportadorPDF(self.config_empresa)
            if exportador.exportar(estudio.datos, ruta):
                QMessageBox.information(self, "Éxito", f"PDF exportado correctamente:\n{ruta}")
            else:
                QMessageBox.critical(self, "Error", "No se pudo exportar el PDF")
    
    def exportar_word(self):
        """Exporta el estudio seleccionado a Word."""
        row = self.tabla.currentRow()
        if row < 0:
            return
        
        id_estudio = self.tabla.item(row, 4).text()
        estudio = EstudioSocioeconomico.cargar(id_estudio)
        
        if not estudio:
            QMessageBox.critical(self, "Error", "No se pudo cargar el estudio")
            return
        
        # Nombre de archivo sugerido
        nombre = estudio.datos.get("datos_personales", {}).get("nombre_completo", "estudio")
        nombre_archivo = f"Estudio_{nombre.replace(' ', '_')}_{estudio.id}.docx"
        
        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Word",
            os.path.join("export", nombre_archivo),
            "Archivos Word (*.docx)"
        )
        
        if ruta:
            exportador = ExportadorWord(self.config_empresa)
            if exportador.exportar(estudio.datos, ruta):
                QMessageBox.information(self, "Éxito", f"Word exportado correctamente:\n{ruta}")
            else:
                QMessageBox.critical(self, "Error", "No se pudo exportar el Word")
    
    def exportar_excel(self):
        """Exporta todos los estudios a Excel."""
        estudios_lista = EstudioSocioeconomico.listar_estudios()
        
        if not estudios_lista:
            QMessageBox.warning(self, "Advertencia", "No hay estudios para exportar")
            return
        
        # Cargar todos los estudios
        estudios_datos = []
        for info in estudios_lista:
            estudio = EstudioSocioeconomico.cargar(info['id'])
            if estudio:
                estudios_datos.append(estudio.datos)
        
        if not estudios_datos:
            QMessageBox.warning(self, "Advertencia", "No se pudieron cargar los estudios")
            return
        
        # Nombre de archivo
        from datetime import datetime
        nombre_archivo = f"Comparativa_Estudios_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Excel",
            os.path.join("export", nombre_archivo),
            "Archivos Excel (*.xlsx)"
        )
        
        if ruta:
            exportador = ExportadorExcel(self.config_empresa)
            if exportador.exportar(estudios_datos, ruta):
                QMessageBox.information(self, "Éxito", 
                    f"Excel exportado correctamente:\n{ruta}\n\n"
                    f"Se incluyeron {len(estudios_datos)} estudio(s)")
            else:
                QMessageBox.critical(self, "Error", "No se pudo exportar el Excel")
    
    def abrir_configuracion(self):
        """Abre el dialogo de configuracion de empresa."""
        dialogo = DialogoConfiguracion(self)
        if dialogo.exec_() and dialogo.cambios_guardados:
            # Recargar configuracion
            self.config_empresa = self.cargar_configuracion()
            # Notificar al usuario
            QMessageBox.information(
                self,
                "Configuracion",
                "Los cambios se aplicaran completamente al reiniciar la aplicacion."
            )
    
    def abrir_backup(self):
        """Abre el dialogo de gestion de backups."""
        dialogo = DialogoBackup(self)
        dialogo.exec_()
        
        # Si se importo un backup, recargar estudios
        if dialogo.backup_importado:
            self.cargar_estudios()
            self.statusBar().showMessage("Estudios actualizados desde backup")
