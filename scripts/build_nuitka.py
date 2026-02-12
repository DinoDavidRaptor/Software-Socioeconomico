"""
Script de compilacion con Nuitka para DINOS Tech.
Genera un ejecutable protegido y optimizado.

Requisitos:
    pip install nuitka ordered-set zstandard

Uso:
    python build_nuitka.py

Copyright (c) 2026 DINOS Tech. Todos los derechos reservados.
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime


# Configuracion
APP_NAME = "SoftSE"
VERSION = "0.3.7"
COMPANY = "DINOS Tech"
DESCRIPTION = "Sistema de Estudios Socioeconomicos"

# Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)  # Subir un nivel desde scripts/
OUTPUT_DIR = os.path.join(ROOT_DIR, "dist")
MAIN_SCRIPT = os.path.join(ROOT_DIR, "main.py")


def limpiar_dist():
    """Elimina la carpeta dist anterior."""
    if os.path.exists(OUTPUT_DIR):
        print(f"Limpiando {OUTPUT_DIR}...")
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR)


def verificar_nuitka():
    """Verifica que Nuitka este instalado."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "nuitka", "--version"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"Nuitka encontrado: {result.stdout.strip()}")
            return True
    except Exception:
        pass
    
    print("ERROR: Nuitka no esta instalado.")
    print("Instale con: pip install nuitka ordered-set zstandard")
    return False


def compilar():
    """Compila la aplicacion con Nuitka."""
    print("=" * 60)
    print(f"  Compilando {APP_NAME} v{VERSION}")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Cambiar al directorio raiz
    os.chdir(ROOT_DIR)
    
    # Comando Nuitka
    cmd = [
        sys.executable, "-m", "nuitka",
        
        # Tipo de compilacion
        "--standalone",                    # Crear ejecutable independiente
        "--onefile",                       # Todo en un solo archivo
        
        # Configuracion de Windows
        "--windows-disable-console",       # Sin ventana de consola
        f"--windows-company-name={COMPANY}",
        f"--windows-product-name={APP_NAME}",
        f"--windows-file-version={VERSION}",
        f"--windows-product-version={VERSION}",
        f"--windows-file-description={DESCRIPTION}",
        
        # Icono (si existe)
        # "--windows-icon-from-ico=assets/installer/icon.ico",
        
        # Incluir modulos necesarios
        "--enable-plugin=pyqt5",           # Plugin PyQt5
        "--include-package=src",           # Todo el paquete src
        "--include-package-data=src",      # Datos del paquete
        
        # Optimizaciones
        "--lto=yes",                       # Link-time optimization
        "--assume-yes-for-downloads",      # Descargar dependencias automaticamente
        
        # Proteccion (ofuscacion basica)
        "--remove-output",                 # Limpiar archivos temporales
        
        # Output
        f"--output-dir={OUTPUT_DIR}",
        f"--output-filename={APP_NAME}.exe",
        
        # Archivo principal
        MAIN_SCRIPT
    ]
    
    # Agregar icono si existe
    icon_path = os.path.join(ROOT_DIR, "assets", "installer", "icon.ico")
    if os.path.exists(icon_path):
        cmd.insert(-1, f"--windows-icon-from-ico={icon_path}")
    
    print("\nEjecutando Nuitka...")
    print(f"Comando: {' '.join(cmd[:10])}...")
    print("\nEsto puede tomar varios minutos...\n")
    
    # Ejecutar compilacion
    process = subprocess.run(cmd)
    
    if process.returncode == 0:
        print("\n" + "=" * 60)
        print("  COMPILACION EXITOSA")
        print("=" * 60)
        print(f"\nEjecutable creado en: {OUTPUT_DIR}")
        return True
    else:
        print("\n" + "=" * 60)
        print("  ERROR EN COMPILACION")
        print("=" * 60)
        return False


def copiar_recursos():
    """Copia recursos necesarios junto al ejecutable."""
    print("\nCopiando recursos adicionales...")
    
    recursos = [
        ("config.json", "config.json"),
    ]
    
    for src, dst in recursos:
        src_path = os.path.join(ROOT_DIR, src)
        dst_path = os.path.join(OUTPUT_DIR, dst)
        
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
            print(f"  + {dst}")
    
    # Crear directorios necesarios
    for directorio in ["data/estudios", "data/fotos", "export"]:
        dir_path = os.path.join(OUTPUT_DIR, directorio)
        os.makedirs(dir_path, exist_ok=True)
        print(f"  + {directorio}/")


def main():
    """Funcion principal."""
    print("\n" + "=" * 60)
    print("  DINOS Tech - Build System")
    print("=" * 60 + "\n")
    
    # Verificar Nuitka
    if not verificar_nuitka():
        sys.exit(1)
    
    # Limpiar dist anterior
    limpiar_dist()
    
    # Compilar
    if not compilar():
        sys.exit(1)
    
    # Copiar recursos
    copiar_recursos()
    
    print("\n" + "=" * 60)
    print("  BUILD COMPLETADO")
    print("=" * 60)
    print(f"\nArchivos en: {OUTPUT_DIR}")
    print("\nSiguiente paso:")
    print("  1. Copie los archivos de dist/ a la carpeta del instalador")
    print("  2. Ejecute Inno Setup con installer/setup.iss")
    print()


if __name__ == "__main__":
    main()
