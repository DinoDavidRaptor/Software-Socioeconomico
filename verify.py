#!/usr/bin/env python3
"""
Script de verificación del sistema.
Verifica que todos los módulos se puedan importar correctamente.
Autor: DINOS Tech
"""

import sys


def verificar_modulos():
    """Verifica que todos los módulos del proyecto se puedan importar."""
    
    print("Verificando módulos del proyecto...")
    print("-" * 50)
    
    modulos = [
        ("Modelo de Estudio", "src.models.estudio"),
        ("Calculador de Riesgos", "src.logic.calculador_riesgos"),
        ("Exportador PDF", "src.export.exportador_pdf"),
        ("Exportador Word", "src.export.exportador_word"),
        ("Exportador Excel", "src.export.exportador_excel"),
        ("Ventana Principal", "src.ui.ventana_principal"),
        ("Wizard de Estudio", "src.ui.wizard_estudio"),
        ("Páginas del Wizard", "src.ui.paginas"),
        ("Diálogo Info IA", "src.ui.dialogo_info_ia"),
    ]
    
    errores = []
    
    for nombre, modulo in modulos:
        try:
            __import__(modulo)
            print(f"✓ {nombre}: OK")
        except Exception as e:
            print(f"✗ {nombre}: ERROR - {e}")
            errores.append((nombre, str(e)))
    
    print("-" * 50)
    
    if errores:
        print(f"\n{len(errores)} módulo(s) con errores:")
        for nombre, error in errores:
            print(f"  - {nombre}: {error}")
        return False
    else:
        print("\n✓ Todos los módulos se importaron correctamente")
        return True


def verificar_dependencias():
    """Verifica las dependencias externas."""
    
    print("\nVerificando dependencias externas...")
    print("-" * 50)
    
    dependencias = [
        ("PyQt5", "PyQt5"),
        ("ReportLab", "reportlab"),
        ("python-docx", "docx"),
        ("openpyxl", "openpyxl"),
        ("Pillow", "PIL"),
    ]
    
    errores = []
    
    for nombre, modulo in dependencias:
        try:
            __import__(modulo)
            print(f"✓ {nombre}: Instalado")
        except ImportError:
            print(f"✗ {nombre}: No instalado")
            errores.append(nombre)
    
    print("-" * 50)
    
    if errores:
        print(f"\n{len(errores)} dependencia(s) faltante(s):")
        for nombre in errores:
            print(f"  - {nombre}")
        print("\nInstale las dependencias con:")
        print("  pip install -r requirements.txt")
        return False
    else:
        print("\n✓ Todas las dependencias están instaladas")
        return True


def verificar_estructura():
    """Verifica la estructura de directorios."""
    
    print("\nVerificando estructura de directorios...")
    print("-" * 50)
    
    import os
    
    directorios = [
        "data/estudios",
        "data/fotos",
        "export",
        "assets",
        "src/models",
        "src/logic",
        "src/ui",
        "src/export"
    ]
    
    todos_ok = True
    
    for directorio in directorios:
        if os.path.isdir(directorio):
            print(f"✓ {directorio}/")
        else:
            print(f"✗ {directorio}/ - No existe")
            todos_ok = False
    
    print("-" * 50)
    
    if todos_ok:
        print("\n✓ Estructura de directorios correcta")
    else:
        print("\nAlgunos directorios no existen.")
        print("Ejecute: python install.py")
    
    return todos_ok


def main():
    """Función principal."""
    
    print("=" * 50)
    print("  VERIFICACIÓN DEL SISTEMA")
    print("  Ecosistema Comercial 360 v0.1.0")
    print("=" * 50)
    print()
    
    dep_ok = verificar_dependencias()
    est_ok = verificar_estructura()
    mod_ok = verificar_modulos()
    
    print("\n" + "=" * 50)
    
    if dep_ok and est_ok and mod_ok:
        print("  ✓ VERIFICACIÓN EXITOSA")
        print("=" * 50)
        print("\nEl sistema está listo para usarse.")
        print("Para ejecutar la aplicación:")
        print("  python main.py")
        return 0
    else:
        print("  ✗ VERIFICACIÓN FALLIDA")
        print("=" * 50)
        print("\nCorrija los errores antes de ejecutar la aplicación.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
