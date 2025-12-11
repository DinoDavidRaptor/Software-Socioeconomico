"""
Sistema de Estudios Socioeconómicos - Ecosistema Comercial 360
Autor: DINOS Tech
Versión: 0.1.0
Fecha: 9 de diciembre de 2025

Este sistema permite crear, gestionar y analizar estudios socioeconómicos completos
con capacidades de exportación a PDF, Word y Excel.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from src.ui.ventana_principal import VentanaPrincipal


def verificar_estructura_directorios():
    """
    Verifica y crea la estructura de directorios necesaria para la aplicación.
    """
    directorios = [
        'data/estudios',
        'data/fotos',
        'export',
        'assets'
    ]
    
    for directorio in directorios:
        try:
            os.makedirs(directorio, exist_ok=True)
        except Exception as e:
            print(f"Advertencia: No se pudo crear el directorio {directorio}: {e}")


def verificar_dependencias():
    """
    Verifica que todas las dependencias necesarias estén instaladas.
    """
    modulos_requeridos = [
        'PyQt5',
        'reportlab',
        'docx',
        'openpyxl',
        'PIL'
    ]
    
    modulos_faltantes = []
    
    for modulo in modulos_requeridos:
        try:
            __import__(modulo)
        except ImportError:
            modulos_faltantes.append(modulo)
    
    if modulos_faltantes:
        mensaje = (
            "Faltan las siguientes dependencias:\n\n" +
            "\n".join(f"- {m}" for m in modulos_faltantes) +
            "\n\nPor favor, instálelas ejecutando:\n" +
            "pip install -r requirements.txt"
        )
        print(mensaje)
        return False
    
    return True


def main():
    """
    Función principal que inicia la aplicación.
    """
    # Verificar dependencias
    if not verificar_dependencias():
        print("\nNo se puede iniciar la aplicación debido a dependencias faltantes.")
        print("Ejecute: pip install -r requirements.txt")
        sys.exit(1)
    
    # Verificar estructura de directorios
    verificar_estructura_directorios()
    
    # Crear aplicación Qt
    app = QApplication(sys.argv)
    app.setApplicationName("Ecosistema Comercial 360")
    app.setOrganizationName("DINOS Tech")
    app.setOrganizationDomain("dinostech.com")
    
    # Establecer estilo
    app.setStyle('Fusion')
    
    # Crear y mostrar ventana principal
    try:
        ventana = VentanaPrincipal()
        ventana.show()
    except Exception as e:
        QMessageBox.critical(
            None,
            "Error Fatal",
            f"No se pudo iniciar la aplicación:\n\n{str(e)}\n\n"
            f"Verifique que el archivo config.json exista y sea válido."
        )
        print(f"Error al iniciar la aplicación: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Ejecutar bucle de eventos
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
