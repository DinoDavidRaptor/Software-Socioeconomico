"""
Sistema de Estudios Socioeconomicos - Ecosistema Comercial 360
Autor: DINOS Tech
Version: 0.3.7
Fecha: 12 de febrero de 2026

Este sistema permite crear, gestionar y analizar estudios socioeconomicos completos
con capacidades de exportacion a PDF, Word y Excel.

Copyright (c) 2026 DINOS Tech. Todos los derechos reservados.
Uso sujeto a licencia. Prohibida la copia o distribucion no autorizada.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QIcon
from src.ui.ventana_principal import VentanaPrincipal


# Ruta al archivo de licencia
LICENSE_FILE = "license.dat"


def verificar_licencia(app: QApplication) -> bool:
    """
    Verifica la licencia del software.
    Si no es valida, muestra dialogo de activacion.
    
    Returns:
        bool: True si la licencia es valida, False si el usuario cancela
    """
    from src.licensing import LicenseValidator
    from src.ui.dialogo_activacion import DialogoActivacion
    
    validator = LicenseValidator(LICENSE_FILE)
    is_valid, message = validator.validate()
    
    if is_valid:
        # Licencia valida
        license_info = validator.get_license_info()
        print(f"Licencia valida: {message}")
        return True
    else:
        # Mostrar dialogo de activacion
        print(f"Licencia no valida: {message}")
        dialogo = DialogoActivacion(license_file=LICENSE_FILE)
        
        if dialogo.exec_() and dialogo.activated:
            return True
        else:
            QMessageBox.warning(
                None,
                "Licencia Requerida",
                "Este software requiere una licencia valida para funcionar.\n\n"
                "Contacte a DINOS Tech para obtener su licencia."
            )
            return False


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
    
    # Crear aplicacion Qt
    app = QApplication(sys.argv)
    app.setApplicationName("Ecosistema Comercial 360")
    app.setOrganizationName("DINOS Tech")
    app.setOrganizationDomain("dinostech.com")
    
    # Establecer estilo
    app.setStyle('Fusion')
    
    # Verificar licencia antes de continuar
    if not verificar_licencia(app):
        sys.exit(0)
    
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
