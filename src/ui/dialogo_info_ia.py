"""
Diálogo para mostrar información concentrada para análisis externo (IA).
Autor: DINOS Tech
Versión: 0.1.0
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QTextEdit, QPushButton, QLabel,
    QHBoxLayout, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class DialogoInfoIA(QDialog):
    """Diálogo que muestra el resumen del estudio para copiar."""
    
    def __init__(self, resumen: str, parent=None):
        super().__init__(parent)
        self.resumen = resumen
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz del diálogo."""
        self.setWindowTitle("Info Concentrada para Análisis Externo")
        self.setGeometry(200, 200, 700, 600)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Instrucciones
        instrucciones = QLabel(
            "El siguiente resumen está listo para copiar y pegar en herramientas de análisis externo.\n"
            "Contiene la información completa del estudio en formato texto."
        )
        instrucciones.setWordWrap(True)
        instrucciones.setStyleSheet("background-color: #e8f4f8; padding: 10px; border-radius: 5px;")
        layout.addWidget(instrucciones)
        
        # Área de texto con el resumen
        self.texto = QTextEdit()
        self.texto.setPlainText(self.resumen)
        self.texto.setReadOnly(True)
        
        font = QFont("Courier")
        font.setPointSize(10)
        self.texto.setFont(font)
        
        layout.addWidget(self.texto)
        
        # Botones
        botones_layout = QHBoxLayout()
        
        btn_copiar = QPushButton("Copiar al Portapapeles")
        btn_copiar.setStyleSheet("""
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
        btn_copiar.clicked.connect(self.copiar_al_portapapeles)
        botones_layout.addWidget(btn_copiar)
        
        botones_layout.addStretch()
        
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 10px 20px;
                font-size: 12px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        btn_cerrar.clicked.connect(self.close)
        botones_layout.addWidget(btn_cerrar)
        
        layout.addLayout(botones_layout)
    
    def copiar_al_portapapeles(self):
        """Copia el texto al portapapeles."""
        from PyQt5.QtWidgets import QApplication
        
        clipboard = QApplication.clipboard()
        clipboard.setText(self.resumen)
        
        QMessageBox.information(
            self,
            "Copiado",
            "El resumen ha sido copiado al portapapeles.\nPuede pegarlo en su herramienta de análisis."
        )
