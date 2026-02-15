"""
Modulo de exportacion a Word (DOCX) via conversion de PDF.
Genera primero el PDF y luego lo convierte a DOCX para mantener el mismo estilo.
Autor: DINOS Tech
Version: 0.4.0
"""

import os
import tempfile
from typing import Dict

# Importar el exportador PDF
from src.export.exportador_pdf import ExportadorPDF


class ExportadorWord:
    """Clase para exportar estudios socioeconomicos a formato Word via PDF."""
    
    def __init__(self, config_empresa: Dict):
        """
        Inicializa el exportador con la configuracion de la empresa.
        
        Args:
            config_empresa: Diccionario con datos de la empresa.
        """
        self.config = config_empresa
        self.exportador_pdf = ExportadorPDF(config_empresa)
    
    def exportar(self, estudio_datos: Dict, ruta_salida: str) -> bool:
        """
        Exporta un estudio socioeconomico a formato Word.
        Primero genera el PDF y luego lo convierte a DOCX.
        
        Args:
            estudio_datos: Diccionario con los datos del estudio.
            ruta_salida: Ruta completa del archivo DOCX de salida.
            
        Returns:
            True si se exporto correctamente, False en caso contrario.
        """
        try:
            # Importar pdf2docx
            from pdf2docx import Converter
            
            # Crear directorio si no existe
            os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
            
            # Generar PDF temporal
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
                pdf_temp_path = tmp_pdf.name
            
            try:
                # Exportar a PDF primero
                self.exportador_pdf.exportar(estudio_datos, pdf_temp_path)
                
                # Convertir PDF a DOCX
                cv = Converter(pdf_temp_path)
                cv.convert(ruta_salida)
                cv.close()
                
                return True
                
            finally:
                # Limpiar archivo temporal
                if os.path.exists(pdf_temp_path):
                    os.remove(pdf_temp_path)
            
        except ImportError:
            print("Error: pdf2docx no esta instalado. Ejecute: pip install pdf2docx")
            return False
        except Exception as e:
            print(f"Error al exportar Word: {e}")
            import traceback
            traceback.print_exc()
            return False
