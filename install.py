#!/usr/bin/env python3
"""
Script de instalación y verificación para SoftSE.
Autor: DINOS Tech
Versión: 0.1.0
"""

import os
import sys
import subprocess
import platform


def imprimir_banner():
    """Imprime el banner de bienvenida."""
    print("=" * 60)
    print("  SoftSE - Sistema de Estudios")
    print("  DINOS Tech - Versión 0.1.0")
    print("=" * 60)
    print()


def verificar_python():
    """Verifica la versión de Python."""
    print("Verificando versión de Python...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"ERROR: Se requiere Python 3.8 o superior.")
        print(f"Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"OK: Python {version.major}.{version.minor}.{version.micro}")
    return True


def crear_entorno_virtual():
    """Crea un entorno virtual para el proyecto."""
    print("\nCreando entorno virtual...")
    
    if os.path.exists('venv'):
        print("OK: Entorno virtual ya existe")
        return True
    
    try:
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
        print("OK: Entorno virtual creado en ./venv")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: No se pudo crear el entorno virtual: {e}")
        return False


def obtener_pip_ejecutable():
    """Obtiene la ruta al ejecutable pip del entorno virtual."""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "pip")
    else:
        return os.path.join("venv", "bin", "pip")


def obtener_python_ejecutable():
    """Obtiene la ruta al ejecutable python del entorno virtual."""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "python")
    else:
        return os.path.join("venv", "bin", "python")


def instalar_dependencias():
    """Instala las dependencias desde requirements.txt en el entorno virtual."""
    print("\nInstalando dependencias en el entorno virtual...")
    print("Esto puede tomar varios minutos...")
    
    pip_ejecutable = obtener_pip_ejecutable()
    
    try:
        subprocess.check_call([
            pip_ejecutable, "install", "-r", "requirements.txt"
        ])
        print("OK: Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"ERROR: No se pudieron instalar las dependencias: {e}")
        return False


def crear_estructura_directorios():
    """Crea la estructura de directorios necesaria."""
    print("\nCreando estructura de directorios...")
    
    directorios = [
        'data/estudios',
        'data/fotos',
        'export',
        'assets'
    ]
    
    for directorio in directorios:
        try:
            os.makedirs(directorio, exist_ok=True)
            print(f"  - {directorio}/")
        except Exception as e:
            print(f"ERROR: No se pudo crear {directorio}: {e}")
            return False
    
    print("OK: Estructura de directorios creada")
    return True


def verificar_config():
    """Verifica que exista el archivo de configuración."""
    print("\nVerificando configuración...")
    
    if os.path.exists('config.json'):
        print("OK: Archivo config.json encontrado")
        print("\nRECOMENDACIÓN: Edite config.json con los datos de su empresa")
        return True
    else:
        print("ADVERTENCIA: No se encontró config.json")
        print("La aplicación usará valores predeterminados")
        return True


def main():
    """Función principal del instalador."""
    imprimir_banner()
    
    # Verificaciones
    if not verificar_python():
        print("\nInstalación abortada.")
        sys.exit(1)
    
    if not crear_estructura_directorios():
        print("\nInstalación incompleta.")
        sys.exit(1)
    
    # Crear entorno virtual
    if not crear_entorno_virtual():
        print("\nInstalación incompleta.")
        sys.exit(1)
    
    # Preguntar si instalar dependencias
    print("\n¿Desea instalar las dependencias ahora? (s/n)")
    respuesta = input("> ").strip().lower()
    
    if respuesta in ['s', 'si', 'sí', 'y', 'yes']:
        if not instalar_dependencias():
            print("\nInstalación incompleta.")
            print("Puede instalar las dependencias manualmente con:")
            pip_cmd = obtener_pip_ejecutable()
            print(f"  {pip_cmd} install -r requirements.txt")
            sys.exit(1)
    else:
        print("\nRecuerde instalar las dependencias antes de ejecutar:")
        pip_cmd = obtener_pip_ejecutable()
        print(f"  {pip_cmd} install -r requirements.txt")
    
    verificar_config()
    
    print("\n" + "=" * 60)
    print("  INSTALACIÓN COMPLETADA")
    print("=" * 60)
    print("\nPara ejecutar la aplicación:")
    
    # Instrucciones según el sistema operativo
    if platform.system() == "Windows":
        print("  venv\\Scripts\\activate")
        print("  python main.py")
    else:
        print("  source venv/bin/activate")
        print("  python main.py")
    
    print("\nO use el script de ejecución:")
    if platform.system() == "Windows":
        print("  run.bat")
    else:
        print("  ./run.sh")
    
    print("\nPara mas informacion, consulte README.md")
    print()


if __name__ == '__main__':
    main()
