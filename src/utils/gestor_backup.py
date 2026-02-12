"""
Sistema de backup para estudios socioeconomicos.
Permite exportar e importar todos los estudios en un archivo ZIP.
Copyright (c) 2026 DINOS Tech. Todos los derechos reservados.
"""

import os
import json
import shutil
import zipfile
from datetime import datetime
from typing import Tuple, List


class GestorBackup:
    """Gestiona exportacion e importacion de backups."""
    
    def __init__(self, estudios_dir: str = "data/estudios", fotos_dir: str = "data/fotos"):
        self.estudios_dir = estudios_dir
        self.fotos_dir = fotos_dir
    
    def exportar_backup(self, destino: str) -> Tuple[bool, str, int]:
        """
        Exporta todos los estudios y fotos a un archivo ZIP.
        
        Args:
            destino: Ruta completa del archivo ZIP a crear
            
        Returns:
            Tuple[bool, str, int]: (exito, mensaje, numero_estudios)
        """
        try:
            # Asegurar extension .zip
            if not destino.lower().endswith('.zip'):
                destino += '.zip'
            
            estudios_count = 0
            fotos_count = 0
            
            with zipfile.ZipFile(destino, 'w', zipfile.ZIP_DEFLATED) as zf:
                # Agregar metadatos del backup
                metadata = {
                    'version': '1.0',
                    'fecha_backup': datetime.now().isoformat(),
                    'app': 'Ecosistema Comercial 360',
                    'empresa': 'DINOS Tech'
                }
                zf.writestr('backup_metadata.json', json.dumps(metadata, indent=2))
                
                # Agregar estudios
                if os.path.exists(self.estudios_dir):
                    for archivo in os.listdir(self.estudios_dir):
                        if archivo.endswith('.json'):
                            ruta_completa = os.path.join(self.estudios_dir, archivo)
                            zf.write(ruta_completa, f"estudios/{archivo}")
                            estudios_count += 1
                
                # Agregar fotos
                if os.path.exists(self.fotos_dir):
                    for archivo in os.listdir(self.fotos_dir):
                        if archivo.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                            ruta_completa = os.path.join(self.fotos_dir, archivo)
                            zf.write(ruta_completa, f"fotos/{archivo}")
                            fotos_count += 1
                
                # Agregar config y empresas si existen
                if os.path.exists('config.json'):
                    zf.write('config.json', 'config.json')
                if os.path.exists('empresas.json'):
                    zf.write('empresas.json', 'empresas.json')
            
            mensaje = f"Backup creado: {estudios_count} estudios, {fotos_count} fotos"
            return True, mensaje, estudios_count
            
        except Exception as e:
            return False, f"Error al crear backup: {str(e)}", 0
    
    def importar_backup(self, archivo_zip: str, sobrescribir: bool = False) -> Tuple[bool, str, int]:
        """
        Importa estudios desde un archivo ZIP de backup.
        
        Args:
            archivo_zip: Ruta al archivo ZIP
            sobrescribir: Si True, sobrescribe estudios existentes
            
        Returns:
            Tuple[bool, str, int]: (exito, mensaje, numero_estudios_importados)
        """
        try:
            if not os.path.exists(archivo_zip):
                return False, "Archivo de backup no encontrado", 0
            
            estudios_importados = 0
            fotos_importadas = 0
            estudios_omitidos = 0
            
            with zipfile.ZipFile(archivo_zip, 'r') as zf:
                # Verificar que sea un backup valido
                nombres = zf.namelist()
                if 'backup_metadata.json' not in nombres:
                    return False, "El archivo no parece ser un backup valido", 0
                
                # Leer metadata
                metadata = json.loads(zf.read('backup_metadata.json').decode('utf-8'))
                fecha_backup = metadata.get('fecha_backup', 'Desconocida')
                
                # Crear directorios si no existen
                os.makedirs(self.estudios_dir, exist_ok=True)
                os.makedirs(self.fotos_dir, exist_ok=True)
                
                # Importar estudios
                for nombre in nombres:
                    if nombre.startswith('estudios/') and nombre.endswith('.json'):
                        nombre_archivo = os.path.basename(nombre)
                        destino = os.path.join(self.estudios_dir, nombre_archivo)
                        
                        if os.path.exists(destino) and not sobrescribir:
                            estudios_omitidos += 1
                            continue
                        
                        with zf.open(nombre) as src, open(destino, 'wb') as dst:
                            dst.write(src.read())
                        estudios_importados += 1
                    
                    elif nombre.startswith('fotos/'):
                        nombre_archivo = os.path.basename(nombre)
                        if nombre_archivo:  # Ignorar entrada de directorio
                            destino = os.path.join(self.fotos_dir, nombre_archivo)
                            
                            if os.path.exists(destino) and not sobrescribir:
                                continue
                            
                            with zf.open(nombre) as src, open(destino, 'wb') as dst:
                                dst.write(src.read())
                            fotos_importadas += 1
            
            mensaje = f"Importados: {estudios_importados} estudios, {fotos_importadas} fotos"
            if estudios_omitidos > 0:
                mensaje += f" ({estudios_omitidos} omitidos por existir)"
            mensaje += f"\nBackup del: {fecha_backup[:10]}"
            
            return True, mensaje, estudios_importados
            
        except zipfile.BadZipFile:
            return False, "El archivo ZIP esta danado o no es valido", 0
        except Exception as e:
            return False, f"Error al importar backup: {str(e)}", 0
    
    def obtener_info_backup(self, archivo_zip: str) -> dict:
        """
        Obtiene informacion de un archivo de backup sin importarlo.
        
        Returns:
            dict con info del backup o None si no es valido
        """
        try:
            with zipfile.ZipFile(archivo_zip, 'r') as zf:
                if 'backup_metadata.json' not in zf.namelist():
                    return None
                
                metadata = json.loads(zf.read('backup_metadata.json').decode('utf-8'))
                
                # Contar archivos
                estudios = sum(1 for n in zf.namelist() if n.startswith('estudios/') and n.endswith('.json'))
                fotos = sum(1 for n in zf.namelist() if n.startswith('fotos/') and not n.endswith('/'))
                
                return {
                    'fecha': metadata.get('fecha_backup', ''),
                    'version': metadata.get('version', ''),
                    'estudios': estudios,
                    'fotos': fotos,
                    'tamano': os.path.getsize(archivo_zip)
                }
        except Exception:
            return None


def generar_nombre_backup() -> str:
    """Genera un nombre de archivo para el backup con fecha."""
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"backup_estudios_{fecha}.zip"
