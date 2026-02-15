"""
Módulo de exportación a PDF.
Autor: DINOS Tech
Versión: 0.3.0
"""

import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, 
    Spacer, Image, PageBreak, KeepTogether, CondPageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from typing import Dict, Optional
import tempfile

# matplotlib se carga de forma lazy para evitar bloqueos en Mac
# Las variables globales se inicializan en _cargar_matplotlib()
MATPLOTLIB_AVAILABLE = None  # None = no probado, True/False = resultado
_plt = None
_np = None


def _cargar_matplotlib():
    """
    Carga matplotlib de forma lazy.
    Esto evita bloqueos al importar el modulo en Mac con Python 3.14.
    """
    global MATPLOTLIB_AVAILABLE, _plt, _np
    
    if MATPLOTLIB_AVAILABLE is not None:
        return MATPLOTLIB_AVAILABLE
    
    try:
        import os
        os.environ.setdefault('MPLBACKEND', 'Agg')
        
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend
        import matplotlib.pyplot as plt
        import numpy as np
        
        _plt = plt
        _np = np
        MATPLOTLIB_AVAILABLE = True
    except ImportError:
        MATPLOTLIB_AVAILABLE = False
    
    return MATPLOTLIB_AVAILABLE


class ExportadorPDF:
    """Clase para exportar estudios socioeconómicos a PDF."""
    
    def __init__(self, config_empresa: Dict):
        """
        Inicializa el exportador con la configuración de la empresa.
        
        Args:
            config_empresa: Diccionario con datos de la empresa.
        """
        self.config = config_empresa
        self.styles = getSampleStyleSheet()
        self._configurar_estilos()
        self._temp_files = []  # Lista de archivos temporales para limpar después
    
    def _configurar_estilos(self):
        """Configura estilos personalizados para el documento."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#2c3e50'),
            spaceAfter=6,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            alignment=TA_JUSTIFY,
            spaceAfter=6
        ))
    
    def _crear_tabla_sin_cortar(self, data: list, colWidths: list, estilo: TableStyle, 
                                 max_filas_por_pagina: int = 15) -> list:
        """
        Crea una tabla que evita cortes entre paginas.
        Si la tabla tiene muchas filas, la divide en subtablas.
        
        Args:
            data: Datos de la tabla (lista de filas)
            colWidths: Anchos de columnas
            estilo: Estilo de la tabla
            max_filas_por_pagina: Maximo de filas antes de dividir
            
        Returns:
            Lista de elementos (tabla o tablas) para agregar al documento
        """
        elements = []
        
        if len(data) <= max_filas_por_pagina:
            # Tabla pequena - usar KeepTogether
            tabla = Table(data, colWidths=colWidths)
            tabla.setStyle(estilo)
            elements.append(KeepTogether([tabla]))
        else:
            # Tabla grande - dividirla para evitar cortes feos
            header = [data[0]] if data else []
            filas = data[1:] if len(data) > 1 else []
            
            # Dividir en chunks
            for i in range(0, len(filas), max_filas_por_pagina - 1):
                chunk = filas[i:i + max_filas_por_pagina - 1]
                if header:
                    chunk_data = header + chunk
                else:
                    chunk_data = chunk
                
                tabla = Table(chunk_data, colWidths=colWidths)
                tabla.setStyle(estilo)
                elements.append(tabla)
                
                if i + max_filas_por_pagina - 1 < len(filas):
                    elements.append(Spacer(1, 0.1*inch))
        
        return elements
    
    def _agregar_seccion_con_keepttogether(self, elements: list, titulo: str, 
                                           contenido: list, forzar_nueva_pagina: bool = False):
        """
        Agrega una seccion al documento intentando mantenerla junta.
        Si el contenido es muy grande, al menos mantiene el titulo con el inicio.
        
        Args:
            elements: Lista de elementos del documento
            titulo: Titulo de la seccion
            contenido: Lista de elementos de contenido
            forzar_nueva_pagina: Si True, agrega PageBreak antes
        """
        if forzar_nueva_pagina:
            elements.append(PageBreak())
        
        # Crear titulo
        titulo_elem = Paragraph(titulo, self.styles['CustomHeading'])
        
        # Si el contenido es pequeno (1-2 elementos), mantener todo junto
        if len(contenido) <= 2:
            elementos_juntos = [titulo_elem] + contenido
            elements.append(KeepTogether(elementos_juntos))
        else:
            # Mantener al menos el titulo con el primer elemento
            elementos_inicio = [titulo_elem, contenido[0]]
            elements.append(KeepTogether(elementos_inicio))
            
            # Agregar el resto
            for elem in contenido[1:]:
                elements.append(elem)
    
    def _crear_encabezado(self, elements: list, datos: Dict = None):
        """
        Crea el encabezado del documento con logo, datos de la empresa y ejecutor del estudio.
        
        Args:
            elements: Lista de elementos del documento.
            datos: Datos del estudio (opcional) para obtener info del ejecutor.
        """
        # Agregar logo si existe - con dimensiones adaptadas al formato del logo
        logo_path = self.config.get("logo", "")
        logo_agregado = False
        if logo_path and os.path.exists(logo_path):
            try:
                # Verificar si es SVG
                if logo_path.lower().endswith('.svg'):
                    try:
                        from svglib.svglib import svg2rlg
                        from reportlab.graphics import renderPDF
                        
                        drawing = svg2rlg(logo_path)
                        if drawing:
                            # Escalar SVG a dimensiones apropiadas
                            max_width = 3.0 * inch
                            max_height = 1.5 * inch
                            
                            scale_x = max_width / drawing.width if drawing.width > max_width else 1
                            scale_y = max_height / drawing.height if drawing.height > max_height else 1
                            scale = min(scale_x, scale_y, 1)
                            
                            drawing.width *= scale
                            drawing.height *= scale
                            drawing.scale(scale, scale)
                            drawing.hAlign = 'CENTER'
                            
                            elements.append(drawing)
                            elements.append(Spacer(1, 0.15*inch))
                            logo_agregado = True
                    except ImportError:
                        print("Error: svglib no esta instalado. Ejecute: pip install svglib")
                else:
                    # Intentar usar PIL para obtener dimensiones (PNG, JPG, etc.)
                    try:
                        from PIL import Image as PILImage
                        with PILImage.open(logo_path) as pil_img:
                            orig_width, orig_height = pil_img.size
                            aspect_ratio = orig_width / orig_height if orig_height > 0 else 1
                            
                            max_width = 3.0 * inch
                            max_height = 1.5 * inch
                            
                            if orig_width > orig_height:
                                new_width = min(max_width, orig_width * 0.5)
                                new_height = new_width / aspect_ratio
                            else:
                                new_height = min(max_height, orig_height * 0.5)
                                new_width = new_height * aspect_ratio
                            
                            if new_width > max_width:
                                new_width = max_width
                                new_height = new_width / aspect_ratio
                            if new_height > max_height:
                                new_height = max_height
                                new_width = new_height * aspect_ratio
                            
                            img = Image(logo_path, width=new_width, height=new_height)
                    except ImportError:
                        # Fallback sin PIL - usar dimensiones fijas adaptadas
                        img = Image(logo_path, width=2.5*inch, height=1*inch)
                    
                    img.hAlign = 'CENTER'
                    elements.append(img)
                    elements.append(Spacer(1, 0.15*inch))
                    logo_agregado = True
                
            except Exception as e:
                print(f"Error al procesar logo: {e}")
                logo_agregado = False
        
        # Datos de la empresa (omitir nombre si ya hay logo que lo contiene)
        empresa_data = []
        if not logo_agregado:
            empresa_data.append([Paragraph(f"<b>{self.config.get('nombre', 'N/A')}</b>", self.styles['CustomTitle'])])
        
        direccion = self.config.get('direccion', '')
        if direccion and direccion != '-':
            empresa_data.append([Paragraph(direccion, self.styles['Normal'])])
        
        empresa_data.append([Paragraph(f"Tel: {self.config.get('telefono', '')} | Email: {self.config.get('email', '')}", 
                      self.styles['Normal'])])
        
        empresa_table = Table(empresa_data, colWidths=[6.5*inch])
        empresa_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(empresa_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Información del estudio/ejecutor
        if datos:
            ejecutor = datos.get('ejecutor_estudio', '') or self.config.get('ejecutor', '')
            fecha_estudio = datos.get('fecha_estudio', datetime.now().strftime('%d/%m/%Y'))
            
            info_estudio = []
            if ejecutor:
                info_estudio.append([f"Ejecutado por: {ejecutor}"])
            info_estudio.append([f"Fecha del estudio: {fecha_estudio}"])
            
            if info_estudio:
                estudio_table = Table(info_estudio, colWidths=[6.5*inch])
                estudio_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Oblique'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#555555')),
                ]))
                elements.append(estudio_table)
                elements.append(Spacer(1, 0.15*inch))
        
        # Linea separadora
        line_data = [['']]
        line_table = Table(line_data, colWidths=[6.5*inch])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#2c3e50')),
        ]))
        elements.append(line_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Seccion de Empresa Solicitante (cliente que pidio el estudio)
        if datos:
            empresa_solicitante = datos.get('empresa_solicitante', '')
            if empresa_solicitante:
                # Titulo de la seccion
                elements.append(Paragraph("ESTUDIO SOLICITADO POR:", self.styles['CustomHeading']))
                
                # Recuadro con nombre de empresa solicitante
                empresa_sol_data = [
                    [Paragraph(f"<b>{empresa_solicitante}</b>", 
                              ParagraphStyle('EmpresaSol', parent=self.styles['Normal'], 
                                           fontSize=14, alignment=TA_CENTER, 
                                           textColor=colors.HexColor('#1a5276')))]
                ]
                
                empresa_sol_table = Table(empresa_sol_data, colWidths=[6.5*inch])
                empresa_sol_table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#1a5276')),
                    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ebf5fb')),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ]))
                elements.append(empresa_sol_table)
                elements.append(Spacer(1, 0.3*inch))
    
    def _crear_seccion_datos_personales(self, datos: Dict, elements: list):
        """Crea la sección de datos personales."""
        # Se construye la seccion localmente y se agrega con KeepTogether al final
        dp = datos.get("datos_personales", {})
        
        # Usar Paragraphs para word wrap automatico en campos largos
        label_style = ParagraphStyle('DPLabel', parent=self.styles['Normal'], 
                                      fontName='Helvetica-Bold', fontSize=9)
        datos_tabla = [
            [Paragraph("Nombre Completo:", label_style), Paragraph(dp.get("nombre_completo", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Edad:", label_style), Paragraph(str(dp.get("edad", "N/A")), self.styles['Normal'])],
            [Paragraph("Fecha de Nacimiento:", label_style), Paragraph(dp.get("fecha_nacimiento", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Genero:", label_style), Paragraph(dp.get("genero", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Estado Civil:", label_style), Paragraph(dp.get("estado_civil", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Nacionalidad:", label_style), Paragraph(dp.get("nacionalidad", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Lugar de Nacimiento:", label_style), Paragraph(dp.get("estado_nacimiento", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("CURP:", label_style), Paragraph(dp.get("curp", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("RFC:", label_style), Paragraph(dp.get("rfc", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("INE:", label_style), Paragraph(dp.get("ine", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("NSS:", label_style), Paragraph(dp.get("nss", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Telefono:", label_style), Paragraph(dp.get("telefono", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Email:", label_style), Paragraph(dp.get("email", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Direccion:", label_style), Paragraph(dp.get("direccion", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Escolaridad:", label_style), Paragraph(dp.get("escolaridad", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Carrera/Especialidad:", label_style), Paragraph(dp.get("carrera_especialidad", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Ultimo Grado:", label_style), Paragraph(dp.get("institucion_ultimo_grado", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Estado Estudios:", label_style), Paragraph(dp.get("estado_estudios", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Certificados:", label_style), Paragraph(dp.get("certificados", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Licencia de Conducir:", label_style), Paragraph("Si" if dp.get("licencia_conducir") else "No", self.styles['Normal'])],
            [Paragraph("Tipo Licencia:", label_style), Paragraph(dp.get("licencia_tipo", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Vigencia Licencia:", label_style), Paragraph(dp.get("licencia_vigencia", "N/A") or "N/A", self.styles['Normal'])],
        ]
        
        # Agregar antecedentes legales si existen
        if dp.get("antecedentes_legales"):
            detalle = dp.get("antecedentes_legales_detalle") or dp.get("detalle_antecedentes", "Si")
            datos_tabla.append([Paragraph("Antecedentes Legales:", label_style), Paragraph(detalle or "Si", self.styles['Normal'])])
        
        # Agregar contactos de emergencia
        contactos = dp.get("contactos_emergencia", [])
        if contactos and isinstance(contactos, list) and len(contactos) > 0:
            for i, contacto in enumerate(contactos[:3]):  # Mostrar maximo 3
                if isinstance(contacto, dict):
                    nombre = contacto.get("nombre", "")
                    telefono = contacto.get("telefono", "")
                    parentesco = contacto.get("parentesco", "")
                    datos_tabla.append([Paragraph(f"Contacto Emergencia {i+1}:", label_style), Paragraph(f"{nombre} ({parentesco}) - {telefono}", self.styles['Normal'])])
        elif dp.get("persona_contacto_emergencia"):
            datos_tabla.append([Paragraph("Contacto Emergencia:", label_style), Paragraph(f"{dp.get('persona_contacto_emergencia', '')} - {dp.get('telefono_emergencia', '')}", self.styles['Normal'])])
        
        datos_tabla.append([Paragraph("Dependencia Economica:", label_style), Paragraph(dp.get("dependencia_economica", "N/A") or "N/A", self.styles['Normal'])])
        
        tabla = Table(datos_tabla, colWidths=[2*inch, 4.5*inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        
        # Para tablas grandes como Datos Personales, NO usar KeepTogether completo
        # Solo mantener titulo con primeras filas visibles, permitir division de tabla
        titulo_datos = Paragraph("DATOS PERSONALES", self.styles['CustomHeading'])
        elements.append(titulo_datos)
        elements.append(tabla)
        elements.append(Spacer(1, 0.2*inch))
    
    def _crear_seccion_salud(self, datos: Dict, elements: list):
        """Crea la sección de salud e intereses."""
        # Se construye la seccion localmente y se agrega con KeepTogether al final
        
        salud = datos.get("salud_intereses", {})
        
        # Usar Paragraphs para word wrap en campos largos
        label_style = ParagraphStyle('SaludLabel', parent=self.styles['Normal'], 
                                      fontName='Helvetica-Bold', fontSize=8)
        info_salud = [
            [Paragraph("Numero de Enfermedades Cronicas:", label_style), Paragraph(str(salud.get("numero_enfermedades_cronicas", 0)), self.styles['Normal'])],
            [Paragraph("Enfermedades Cronicas:", label_style), Paragraph(salud.get("enfermedades_cronicas", "Ninguna") or "Ninguna", self.styles['Normal'])],
            [Paragraph("Padecimientos:", label_style), Paragraph(salud.get("padecimientos", "Ninguno") or "Ninguno", self.styles['Normal'])],
            [Paragraph("Alergias:", label_style), Paragraph(salud.get("alergias", "Ninguna") or "Ninguna", self.styles['Normal'])],
            [Paragraph("Tratamientos Actuales:", label_style), Paragraph(salud.get("tratamientos_actuales", "Ninguno") or "Ninguno", self.styles['Normal'])],
            [Paragraph("Numero Tratamientos Activos:", label_style), Paragraph(str(salud.get("numero_tratamientos_activos", 0)), self.styles['Normal'])],
            [Paragraph("Gasto Mensual Medicamentos:", label_style), Paragraph(f"${salud.get('gasto_mensual_medicamentos', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Antecedentes Psicologicos:", label_style), Paragraph(salud.get("antecedentes_psicologicos", "Ninguno") or "Ninguno", self.styles['Normal'])],
            [Paragraph("En Tratamiento Psicologico:", label_style), Paragraph("Si" if salud.get("en_tratamiento_psicologico") else "No", self.styles['Normal'])],
            [Paragraph("Frecuencia Consultas:", label_style), Paragraph(salud.get("frecuencia_consultas_psicologicas", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Consumo Alcohol:", label_style), Paragraph(salud.get("consumo_alcohol", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Copas por Semana:", label_style), Paragraph(str(salud.get("copas_por_semana", 0)), self.styles['Normal'])],
            [Paragraph("Consumo Tabaco:", label_style), Paragraph(salud.get("consumo_tabaco", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Cigarros por Dia:", label_style), Paragraph(str(salud.get("cigarros_por_dia", 0)), self.styles['Normal'])]
        ]
        
        # BUG FIX: Check consumo_alcohol field instead of consume_alcohol_socialmente
        # If consumo_alcohol is not "No" or "Ninguno", show "Si"
        consumo_alcohol = salud.get("consumo_alcohol", "")
        consume_socialmente = "Si" if consumo_alcohol and consumo_alcohol.lower() not in ["no", "ninguno", "n/a", "n\\a"] else "No"
        info_salud.append([Paragraph("Consume Alcohol Socialmente:", label_style), Paragraph(consume_socialmente, self.styles['Normal'])])
        info_salud.append([Paragraph("Consumo Otras Sustancias:", label_style), Paragraph(salud.get("consumo_otras_sustancias", "N/A") or "N/A", self.styles['Normal'])])
        info_salud.append([Paragraph("Seguro Medico:", label_style), Paragraph(salud.get("seguro_medico", "N/A") or "N/A", self.styles['Normal'])])
        info_salud.append([Paragraph("Tipo Seguro:", label_style), Paragraph(salud.get("tipo_seguro", "N/A") or "N/A", self.styles['Normal'])])
        info_salud.append([Paragraph("Costo Mensual Seguro:", label_style), Paragraph(f"${salud.get('costo_mensual_seguro', 0):,.2f}", self.styles['Normal'])])
        info_salud.append([Paragraph("Metas Corto Plazo:", label_style), Paragraph(salud.get("metas_corto_plazo", "N/A") or "N/A", self.styles['Normal'])])
        info_salud.append([Paragraph("Metas Largo Plazo:", label_style), Paragraph(salud.get("metas_largo_plazo", "N/A") or "N/A", self.styles['Normal'])])
        
        tabla_salud = Table(info_salud, colWidths=[2.2*inch, 4.3*inch])
        tabla_salud.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        
        # Usar KeepTogether para mantener titulo y tabla juntos
        titulo_salud = Paragraph("SALUD E INTERESES", self.styles['CustomHeading'])
        elements.append(KeepTogether([titulo_salud, tabla_salud, Spacer(1, 0.2*inch)]))
    
    def _crear_seccion_familiar(self, datos: Dict, elements: list):
        """Crea la sección de información familiar."""
        fam = datos.get("informacion_familiar", {})
        
        # Usar Paragraphs para word wrap en observaciones
        label_style = ParagraphStyle('FamLabel', parent=self.styles['Normal'], 
                                      fontName='Helvetica-Bold', fontSize=9)
        info_general = [
            [Paragraph("Numero de Hijos:", label_style), Paragraph(str(fam.get("numero_hijos", 0)), self.styles['Normal'])],
            [Paragraph("Hijos Menores:", label_style), Paragraph(str(fam.get("numero_hijos_menores", 0)), self.styles['Normal'])],
            [Paragraph("Hijos Estudiando:", label_style), Paragraph(str(fam.get("numero_hijos_estudiando", 0)), self.styles['Normal'])],
            [Paragraph("Gasto Educacion Hijos:", label_style), Paragraph(f"${fam.get('gasto_mensual_educacion_hijos', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Numero Personas Hogar:", label_style), Paragraph(str(fam.get("total_miembros_hogar", 0)), self.styles['Normal'])],
            [Paragraph("Integrantes Trabajan:", label_style), Paragraph(str(fam.get("miembros_trabajando", 0)), self.styles['Normal'])],
            [Paragraph("Integrantes Estudiando:", label_style), Paragraph(str(fam.get("miembros_estudiando", 0)), self.styles['Normal'])],
            [Paragraph("Dependientes Sin Ingreso:", label_style), Paragraph(str(fam.get("dependientes_sin_ingreso", 0)), self.styles['Normal'])],
            [Paragraph("Porcentaje Dependientes:", label_style), Paragraph(f"{fam.get('porcentaje_dependientes', 0):,.1f}%", self.styles['Normal'])],
            [Paragraph("Gasto Promedio por Persona:", label_style), Paragraph(f"${fam.get('gasto_promedio_por_persona', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Observaciones:", label_style), Paragraph(fam.get("observaciones_familiares", "N/A") or "N/A", self.styles['Normal'])]
        ]
        
        tabla_general = Table(info_general, colWidths=[2.5*inch, 4*inch])
        tabla_general.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        # Usar KeepTogether para evitar cortes de pagina
        titulo_familiar = Paragraph("INFORMACION FAMILIAR", self.styles['CustomHeading'])
        elements.append(KeepTogether([titulo_familiar, tabla_general, Spacer(1, 0.1*inch)]))
        
        # Tabla de ingresos
        ingreso_familiar = fam.get("ingreso_familiar", [])
        if ingreso_familiar and isinstance(ingreso_familiar, list):
            ingreso_data = [["Fuente", "Monto"]]
            for ing in ingreso_familiar:
                if isinstance(ing, dict):
                    ingreso_data.append([ing.get("fuente", "N/A"), f"${ing.get('monto', 0):,.2f}"])
            
            if len(ingreso_data) > 1:
                elements.append(Paragraph("<b>Ingresos Familiares:</b>", self.styles['CustomBody']))
                tabla_ingreso = Table(ingreso_data, colWidths=[4*inch, 2.5*inch])
                tabla_ingreso.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('PADDING', (0, 0), (-1, -1), 4),
                ]))
                elements.append(tabla_ingreso)
                elements.append(Spacer(1, 0.1*inch))
        
        # Mostrar resumen de ingresos
        elements.append(Paragraph(
            f"<b>Ingreso Familiar Total:</b> ${fam.get('ingreso_familiar_total', 0):,.2f} | "
            f"<b>Ingreso Per Cápita:</b> ${fam.get('ingreso_per_capita', 0):,.2f}",
            self.styles['CustomBody']
        ))
        
        # Tabla de miembros del hogar
        miembros = fam.get("miembros_hogar", [])
        if miembros and isinstance(miembros, list) and len(miembros) > 0:
            elements.append(Spacer(1, 0.1*inch))
            
            # Headers de la tabla con texto blanco
            header_style = ParagraphStyle('MiembrosHeader', parent=self.styles['Normal'], 
                                           textColor=colors.white, fontName='Helvetica-Bold', fontSize=8)
            miembros_data = [
                [Paragraph("Nombre", header_style),
                 Paragraph("Parentesco", header_style),
                 Paragraph("Edad", header_style),
                 Paragraph("Ocupacion", header_style),
                 Paragraph("Ingreso", header_style)]
            ]
            
            for miembro in miembros:
                if isinstance(miembro, dict):
                    nombre = miembro.get("nombre", "N/A") or "N/A"
                    parentesco = miembro.get("parentesco", "N/A") or "N/A"
                    edad = str(miembro.get("edad", 0))
                    ocupacion = miembro.get("ocupacion", "N/A") or "N/A"
                    # BUG FIX: Usar 'ingreso' en lugar de 'ingreso_mensual'
                    ingreso_valor = miembro.get('ingreso', miembro.get('ingreso_mensual', 0))
                    ingreso = f"${ingreso_valor:,.2f}"
                    miembros_data.append([
                        Paragraph(nombre, self.styles['Normal']),
                        Paragraph(parentesco, self.styles['Normal']),
                        Paragraph(edad, self.styles['Normal']),
                        Paragraph(ocupacion, self.styles['Normal']),
                        Paragraph(ingreso, self.styles['Normal'])
                    ])
            
            tabla_miembros = Table(miembros_data, colWidths=[1.8*inch, 1.5*inch, 0.6*inch, 1.5*inch, 1.2*inch])
            tabla_miembros.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('PADDING', (0, 0), (-1, -1), 4),
                ('ALIGN', (2, 1), (2, -1), 'CENTER'),
                ('ALIGN', (4, 1), (4, -1), 'RIGHT'),
            ]))
            
            # Usar KeepTogether para titulo y tabla de miembros
            titulo_miembros = Paragraph("<b>Miembros del Hogar:</b>", self.styles['CustomBody'])
            elements.append(KeepTogether([titulo_miembros, tabla_miembros]))
        
        elements.append(Spacer(1, 0.2*inch))
    
    def _crear_seccion_financiera(self, datos: Dict, elements: list):
        """Crea la sección de situación financiera."""
        # Titulo se agrega con KeepTogether al final con la primera tabla
        fin = datos.get("situacion_financiera", {})
        
        # Calculate percentages if not already stored
        porcentaje_gastos_ingreso = fin.get('porcentaje_gastos_ingreso', None)
        if porcentaje_gastos_ingreso is None:
            ingreso_total = fin.get('ingreso_total_mensual', 0) or fin.get('sueldo_mensual', 0)
            gastos_totales = fin.get('gastos', {}).get('total', 0)
            if ingreso_total > 0:
                porcentaje_gastos_ingreso = (gastos_totales / ingreso_total) * 100
            else:
                porcentaje_gastos_ingreso = 0
        
        porcentaje_ahorro = fin.get('porcentaje_ahorro', None)
        if porcentaje_ahorro is None:
            ingreso_total = fin.get('ingreso_total_mensual', 0) or fin.get('sueldo_mensual', 0)
            monto_ahorros = fin.get('monto_ahorros_mensuales', 0)
            if ingreso_total > 0:
                porcentaje_ahorro = (monto_ahorros / ingreso_total) * 100
            else:
                porcentaje_ahorro = 0
        
        porcentaje_deudas_ingreso = fin.get('porcentaje_deudas_ingreso', None)
        if porcentaje_deudas_ingreso is None:
            ingreso_total = fin.get('ingreso_total_mensual', 0) or fin.get('sueldo_mensual', 0)
            total_deudas = fin.get('total_deudas', 0)
            if ingreso_total > 0:
                porcentaje_deudas_ingreso = (total_deudas / (ingreso_total * 12)) * 100  # Annualized
            else:
                porcentaje_deudas_ingreso = 0
        
        # Informacion laboral actual con Paragraphs para word wrap
        # Procesar otros_ingresos (puede ser lista de dicts)
        otros_ingresos_raw = fin.get("otros_ingresos", [])
        if isinstance(otros_ingresos_raw, list) and otros_ingresos_raw:
            otros_ingresos_str = "; ".join([
                f"{item.get('fuente', 'N/A')}: ${item.get('monto', 0):,.2f} ({item.get('frecuencia', '')})"
                for item in otros_ingresos_raw if isinstance(item, dict)
            ]) or "N/A"
        else:
            otros_ingresos_str = str(otros_ingresos_raw) if otros_ingresos_raw else "N/A"
        
        label_style = ParagraphStyle('FinLabel', parent=self.styles['Normal'], 
                                      fontName='Helvetica-Bold', fontSize=9)
        info_laboral = [
            [Paragraph("Trabaja Actualmente:", label_style), Paragraph("Si" if fin.get("trabaja_actualmente", False) else "No", self.styles['Normal'])],
            [Paragraph("Empresa:", label_style), Paragraph(fin.get("empresa_actual", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Puesto:", label_style), Paragraph(fin.get("puesto_actual", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Sueldo Mensual:", label_style), Paragraph(f"${fin.get('sueldo_mensual', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Ingresos Adicionales:", label_style), Paragraph(fin.get("ingresos_adicionales", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Otros Ingresos:", label_style), Paragraph(otros_ingresos_str, self.styles['Normal'])],
            [Paragraph("Ingreso Total Mensual:", label_style), Paragraph(f"${fin.get('ingreso_total_mensual', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Ahorro Acumulado:", label_style), Paragraph(f"${fin.get('ahorros', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Ahorro Mensual:", label_style), Paragraph(f"${fin.get('monto_ahorros_mensuales', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Numero Cuentas Bancarias:", label_style), Paragraph(str(fin.get("numero_cuentas_bancarias", 0)), self.styles['Normal'])],
            [Paragraph("Cuentas Bancarias:", label_style), Paragraph(fin.get("cuentas_bancarias", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Numero Tarjetas Credito:", label_style), Paragraph(str(fin.get("numero_tarjetas_credito", 0)), self.styles['Normal'])],
            [Paragraph("Limite Credito Total:", label_style), Paragraph(f"${fin.get('limite_credito_total', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Deuda Tarjetas Total:", label_style), Paragraph(f"${fin.get('deuda_tarjetas_total', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Tiene Prestamos Personales:", label_style), Paragraph("Si" if fin.get("tiene_prestamos_personales") else "No", self.styles['Normal'])],
            [Paragraph("Prestamos Personales:", label_style), Paragraph(f"${fin.get('monto_prestamos_personales', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Tiene Hipoteca:", label_style), Paragraph("Si" if fin.get("tiene_prestamo_hipotecario") else "No", self.styles['Normal'])],
            [Paragraph("Monto Hipoteca:", label_style), Paragraph(f"${fin.get('monto_hipoteca', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Pago Hipoteca Mensual:", label_style), Paragraph(f"${fin.get('pago_mensual_hipoteca', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Tiene Prestamo Auto:", label_style), Paragraph("Si" if fin.get("tiene_prestamo_auto") else "No", self.styles['Normal'])],
            [Paragraph("Monto Prestamo Auto:", label_style), Paragraph(f"${fin.get('monto_prestamo_auto', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Pago Auto Mensual:", label_style), Paragraph(f"${fin.get('pago_mensual_auto', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Apoyos Gubernamentales:", label_style), Paragraph(fin.get("apoyos_gubernamentales", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Monto Apoyos:", label_style), Paragraph(f"${fin.get('monto_apoyos_gubernamentales', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Gasto Promedio Comida Diaria:", label_style), Paragraph(f"${fin.get('gasto_promedio_comida_diaria', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Gasto Mensual Gasolina:", label_style), Paragraph(f"${fin.get('gasto_mensual_gasolina', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Gastos Extraordinarios:", label_style), Paragraph(fin.get("gastos_extraordinarios", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Historial Deudas:", label_style), Paragraph(fin.get("historial_deudas", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Total Deudas:", label_style), Paragraph(f"${fin.get('total_deudas', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Pagos Deudas Mensuales:", label_style), Paragraph(f"${fin.get('total_pagos_mensuales_deudas', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Porcentaje Gastos/Ingreso:", label_style), Paragraph(f"{porcentaje_gastos_ingreso:.2f}%", self.styles['Normal'])],
            [Paragraph("Porcentaje Ahorro:", label_style), Paragraph(f"{porcentaje_ahorro:.2f}%", self.styles['Normal'])],
            [Paragraph("Porcentaje Deudas/Ingreso:", label_style), Paragraph(f"{porcentaje_deudas_ingreso:.2f}%", self.styles['Normal'])],
            [Paragraph("Capacidad Pago:", label_style), Paragraph(f"${fin.get('capacidad_pago', 0):,.2f}", self.styles['Normal'])]
        ]
        
        tabla_laboral = Table(info_laboral, colWidths=[2.2*inch, 4.3*inch])
        tabla_laboral.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        # Usar KeepTogether para titulo y primera tabla
        titulo_financiera = Paragraph("SITUACION FINANCIERA", self.styles['CustomHeading'])
        elements.append(KeepTogether([titulo_financiera, tabla_laboral, Spacer(1, 0.1*inch)]))
        
        # Gastos mensuales - usar KeepTogether para titulo y tabla
        gastos = fin.get("gastos", {})
        gastos_data = [
            ["Categoría", "Monto"],
            ["Alimentación", f"${gastos.get('alimentacion', 0):,.2f}"],
            ["Salud", f"${gastos.get('salud', 0):,.2f}"],
            ["Educación", f"${gastos.get('educacion', 0):,.2f}"],
            ["Vivienda", f"${gastos.get('vivienda', 0):,.2f}"],
            ["Transporte", f"${gastos.get('transporte', 0):,.2f}"],
            ["Servicios", f"${gastos.get('servicios', 0):,.2f}"],
            ["Recreación", f"${gastos.get('recreacion', 0):,.2f}"],
            ["Otros", f"${gastos.get('otros', 0):,.2f}"],
        ]
        
        gastos_data.append(["TOTAL", f"${gastos.get('total', 0):,.2f}"])
        
        tabla_gastos = Table(gastos_data, colWidths=[3*inch, 3.5*inch])
        tabla_gastos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        # KeepTogether para titulo y tabla de gastos
        titulo_gastos = Paragraph("<b>Gastos Mensuales:</b>", self.styles['CustomBody'])
        elements.append(KeepTogether([titulo_gastos, tabla_gastos, Spacer(1, 0.1*inch)]))
        
        # Balance
        balance_data = [[
            "Balance Mensual (Ingreso - Gastos):",
            f"${fin.get('balance', 0):,.2f}"
        ]]
        
        tabla_balance = Table(balance_data, colWidths=[3*inch, 3.5*inch])
        balance_color = colors.green if fin.get('balance', 0) >= 0 else colors.red
        tabla_balance.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (1, 0), (1, 0), balance_color),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(tabla_balance)
        
        # Observaciones Financieras (fuera de tabla para mejor wrap)
        if fin.get("observaciones_financieras"):
            elements.append(Spacer(1, 0.1*inch))
            elements.append(Paragraph("<b>Observaciones Financieras:</b>", self.styles['CustomBody']))
            # Usar estilo con wrap automatico
            obs_text = fin.get("observaciones_financieras", "")
            elements.append(Paragraph(obs_text, self.styles['CustomBody']))
        
        elements.append(Spacer(1, 0.2*inch))
    
    def _crear_seccion_empleo_actual(self, datos: Dict, elements: list):
        """Crea la sección de empleo actual detallado."""
        empleo = datos.get("empleo_actual", {})
        
        # Mostrar siempre si hay datos de empleo
        if not empleo or not empleo.get("empresa"):
            return
        
        # Usar Paragraphs para word wrap en campos largos
        label_style = ParagraphStyle('EmpLabel', parent=self.styles['Normal'], 
                                      fontName='Helvetica-Bold', fontSize=8)
        info_empleo = [
            [Paragraph("Empresa:", label_style), Paragraph(empleo.get("empresa", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Empresa Actual:", label_style), Paragraph(empleo.get("empresa_actual", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Puesto:", label_style), Paragraph(empleo.get("puesto", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Puesto Actual:", label_style), Paragraph(empleo.get("puesto_actual", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Antiguedad:", label_style), Paragraph(empleo.get("antiguedad", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Antiguedad (meses):", label_style), Paragraph(str(empleo.get("antiguedad_meses", 0)), self.styles['Normal'])],
            [Paragraph("Tipo de Contrato:", label_style), Paragraph(empleo.get("tipo_contrato", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Salario Mensual Bruto:", label_style), Paragraph(f"${empleo.get('salario_mensual_bruto', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Salario Mensual Neto:", label_style), Paragraph(f"${empleo.get('salario_mensual_neto', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Numero Prestaciones:", label_style), Paragraph(str(empleo.get("numero_prestaciones", 0)), self.styles['Normal'])],
            [Paragraph("Prestaciones:", label_style), Paragraph(", ".join(empleo.get("prestaciones", [])) or "N/A", self.styles['Normal'])],
            [Paragraph("Valor Prestaciones Anuales:", label_style), Paragraph(f"${empleo.get('valor_prestaciones_anuales', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Horario:", label_style), Paragraph(empleo.get("horario", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Horas Semanales:", label_style), Paragraph(str(empleo.get("horas_semanales", 0)), self.styles['Normal'])],
            [Paragraph("Dias Laborales:", label_style), Paragraph(str(empleo.get("dias_laborales_semana", 0)), self.styles['Normal'])],
            [Paragraph("Tiempo Traslado:", label_style), Paragraph(empleo.get("tiempo_traslado", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Tiempo Traslado (min):", label_style), Paragraph(str(empleo.get("tiempo_traslado_minutos", 0)), self.styles['Normal'])],
            [Paragraph("Costo Mensual Transporte:", label_style), Paragraph(f"${empleo.get('costo_mensual_transporte', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Home Office:", label_style), Paragraph("Si" if empleo.get("tiene_home_office") else "No", self.styles['Normal'])],
            [Paragraph("Dias Home Office:", label_style), Paragraph(str(empleo.get("dias_home_office_semana", 0)), self.styles['Normal'])],
            [Paragraph("Jefe Inmediato:", label_style), Paragraph(empleo.get("jefe_inmediato", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Telefono Empresa:", label_style), Paragraph(empleo.get("telefono_empresa", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Satisfaccion Laboral:", label_style), Paragraph(empleo.get("satisfaccion_laboral", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Oportunidades Ascenso:", label_style), Paragraph(empleo.get("oportunidades_ascenso", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Ultima Evaluacion:", label_style), Paragraph(empleo.get("ultima_evaluacion_desempeno", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Calificacion Evaluacion:", label_style), Paragraph(str(empleo.get("calificacion_ultima_evaluacion", 0)), self.styles['Normal'])],
            [Paragraph("Recibe Bonos:", label_style), Paragraph("Si" if empleo.get("recibe_bonos") else "No", self.styles['Normal'])],
            [Paragraph("Monto Promedio Bonos Anuales:", label_style), Paragraph(f"${empleo.get('monto_promedio_bonos_anuales', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Plan Carrera:", label_style), Paragraph(empleo.get("plan_carrera", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Observaciones:", label_style), Paragraph(empleo.get("observaciones_empleo", "N/A") or "N/A", self.styles['Normal'])]
        ]
        
        tabla_empleo = Table(info_empleo, colWidths=[2*inch, 4.5*inch])
        tabla_empleo.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        
        # Usar KeepTogether para titulo y tabla de empleo
        titulo_empleo = Paragraph("EMPLEO ACTUAL", self.styles['CustomHeading'])
        elements.append(KeepTogether([titulo_empleo, tabla_empleo, Spacer(1, 0.2*inch)]))
    
    def _crear_seccion_estilo_vida(self, datos: Dict, elements: list):
        """Crea la sección de estilo de vida."""
        estilo = datos.get("estilo_vida", {})
        
        if not estilo:
            return
        
        # Usar Paragraphs para word wrap en campos largos como hobbies, actividades
        label_style = ParagraphStyle('EstiloLabel', parent=self.styles['Normal'], 
                                      fontName='Helvetica-Bold', fontSize=8)
        info_estilo = [
            [Paragraph("Numero de Hobbies:", label_style), Paragraph(str(estilo.get("numero_hobbies", 0)), self.styles['Normal'])],
            [Paragraph("Hobbies:", label_style), Paragraph(estilo.get("hobbies", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Gasto Mensual Hobbies:", label_style), Paragraph(f"${estilo.get('gasto_mensual_hobbies', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Actividades Fin de Semana:", label_style), Paragraph(estilo.get("actividades_fin_semana", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Frecuencia Salidas Mes:", label_style), Paragraph(str(estilo.get("frecuencia_salidas_mes", 0)), self.styles['Normal'])],
            [Paragraph("Gasto Promedio por Salida:", label_style), Paragraph(f"${estilo.get('gasto_promedio_por_salida', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Numero de Viajes Ultimo Ano:", label_style), Paragraph(str(estilo.get("numero_viajes_ultimo_ano", 0)), self.styles['Normal'])],
            [Paragraph("Gasto Total Viajes Ano:", label_style), Paragraph(f"${estilo.get('gasto_total_viajes_ano', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Actividades Culturales:", label_style), Paragraph(estilo.get("actividades_culturales", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Frecuencia Cultura Mes:", label_style), Paragraph(str(estilo.get("frecuencia_actividades_culturales_mes", 0)), self.styles['Normal'])],
            [Paragraph("Gasto Mensual Cultura:", label_style), Paragraph(f"${estilo.get('gasto_mensual_cultura', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Deportes:", label_style), Paragraph(estilo.get("deportes", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Frecuencia Ejercicio Semana:", label_style), Paragraph(str(estilo.get("frecuencia_ejercicio_semana", 0)), self.styles['Normal'])],
            [Paragraph("Gasto Mensual Gimnasio:", label_style), Paragraph(f"${estilo.get('gasto_mensual_gimnasio', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Pertenece a Clubs:", label_style), Paragraph("Si" if estilo.get("pertenece_clubes") else "No", self.styles['Normal'])],
            [Paragraph("Numero de Clubes:", label_style), Paragraph(str(estilo.get("numero_clubes_asociaciones", 0)), self.styles['Normal'])],
            [Paragraph("Costo Mensual Membresias:", label_style), Paragraph(f"${estilo.get('costo_mensual_membrestas', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Tiene Mascotas:", label_style), Paragraph("Si" if estilo.get("tiene_mascotas") else "No", self.styles['Normal'])],
            [Paragraph("Numero de Mascotas:", label_style), Paragraph(str(estilo.get("numero_mascotas", 0)), self.styles['Normal'])],
            [Paragraph("Gasto Mensual Mascotas:", label_style), Paragraph(f"${estilo.get('gasto_mensual_mascotas', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Fuma:", label_style), Paragraph("Si" if estilo.get("fuma") else "No", self.styles['Normal'])],
            [Paragraph("Gasto Mensual Tabaco:", label_style), Paragraph(f"${estilo.get('gasto_mensual_tabaco', 0):,.2f}", self.styles['Normal'])]
        ]
        
        # BUG FIX: Check consumo_alcohol field instead of consume_alcohol_socialmente
        # If consumo_alcohol is not "No" or "Ninguno", show "Si"
        consumo_alcohol = datos.get("salud_intereses", {}).get("consumo_alcohol", "")
        consume_socialmente = "Si" if consumo_alcohol and consumo_alcohol.lower() not in ["no", "ninguno", "n/a", "n\\a"] else "No"
        info_estilo.append([Paragraph("Consume Alcohol Socialmente:", label_style), Paragraph(consume_socialmente, self.styles['Normal'])])
        info_estilo.append([Paragraph("Gasto Mensual Alcohol:", label_style), Paragraph(f"${estilo.get('gasto_mensual_alcohol', 0):,.2f}", self.styles['Normal'])])
        
        tabla_estilo = Table(info_estilo, colWidths=[2.2*inch, 4.3*inch])
        tabla_estilo.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        
        # Usar KeepTogether para titulo y tabla de estilo de vida
        titulo_estilo = Paragraph("ESTILO DE VIDA", self.styles['CustomHeading'])
        elements.append(KeepTogether([titulo_estilo, tabla_estilo, Spacer(1, 0.2*inch)]))
    
    def _crear_seccion_vivienda(self, datos: Dict, elements: list):
        """Crea la seccion de vivienda."""
        viv = datos.get("vivienda", {})
        
        # Usar Paragraphs para word wrap automatico en campos largos
        label_style = ParagraphStyle('VivLabel', parent=self.styles['Normal'], 
                                      fontName='Helvetica-Bold', fontSize=9)
        info_vivienda = [
            [Paragraph("Tipo de Vivienda:", label_style), Paragraph(viv.get("tipo_vivienda", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Tenencia:", label_style), Paragraph(viv.get("tenencia", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Regimen:", label_style), Paragraph(viv.get("regimen", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Zona:", label_style), Paragraph(viv.get("tipo_zona", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Materiales:", label_style), Paragraph(viv.get("materiales_construccion", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Tiempo de Residencia:", label_style), Paragraph(viv.get("tiempo_residencia", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Numero de Cuartos:", label_style), Paragraph(str(viv.get("numero_cuartos", 0)), self.styles['Normal'])],
            [Paragraph("Numero de Banos:", label_style), Paragraph(str(viv.get("numero_banos", 0)), self.styles['Normal'])],
            [Paragraph("Metros Cuadrados:", label_style), Paragraph(f"{viv.get('metros_cuadrados_construccion', 0):,.2f} m2", self.styles['Normal'])],
            [Paragraph("Costo Renta Mensual:", label_style), Paragraph(f"${viv.get('costo_renta_mensual', 0) or viv.get('renta_mensual', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Valor Estimado:", label_style), Paragraph(f"${viv.get('valor_estimado_vivienda', 0):,.2f}", self.styles['Normal'])],
            [Paragraph("Antiguedad (anos):", label_style), Paragraph(str(viv.get("antiguedad_vivienda_anos", 0)), self.styles['Normal'])],
            [Paragraph("Condiciones:", label_style), Paragraph(viv.get("condiciones_generales", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Seguridad Entorno:", label_style), Paragraph(viv.get("seguridad_entorno", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Otras Propiedades:", label_style), Paragraph(viv.get("otras_propiedades", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Num. Prop. Adicionales:", label_style), Paragraph(str(viv.get("numero_propiedades_adicionales", 0)), self.styles['Normal'])],
            [Paragraph("Valor Prop. Adicionales:", label_style), Paragraph(f"${viv.get('valor_propiedades_adicionales', 0):,.2f}", self.styles['Normal'])]
        ]
        
        tabla_viv = Table(info_vivienda, colWidths=[2*inch, 4.5*inch])
        tabla_viv.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        # Usar KeepTogether para titulo y tabla de vivienda
        titulo_vivienda = Paragraph("VIVIENDA Y PATRIMONIO", self.styles['CustomHeading'])
        elements.append(KeepTogether([titulo_vivienda, tabla_viv, Spacer(1, 0.1*inch)]))
        
        # Servicios
        servicios = viv.get("servicios", {})
        servicios_lista = [k.replace("_", " ").title() for k, v in servicios.items() if v]
        
        if servicios_lista:
            elements.append(Paragraph(
                f"<b>Servicios:</b> {', '.join(servicios_lista)}", 
                self.styles['CustomBody']
            ))
        
        elements.append(Spacer(1, 0.2*inch))
    
    def _crear_seccion_historial_laboral(self, datos: Dict, elements: list):
        """Crea la seccion de historial laboral."""
        historial = datos.get("historial_laboral", [])
        
        if not historial:
            return
        
        # Encabezados con texto blanco
        header_style = ParagraphStyle('HistHeader', parent=self.styles['Normal'], 
                                       textColor=colors.white, fontName='Helvetica-Bold', fontSize=8)
        hist_data = [
            [Paragraph("Empresa", header_style),
             Paragraph("Puesto", header_style),
             Paragraph("Duracion", header_style),
             Paragraph("Salario", header_style),
             Paragraph("Motivo Salida", header_style)]
        ]
        
        for emp in historial:
            if isinstance(emp, dict):
                salario = emp.get('salario_final', 0) or emp.get('salario_inicial', 0) or emp.get('salario', 0)
                hist_data.append([
                    Paragraph(emp.get("empresa", "") or "-", self.styles['Normal']),
                    Paragraph(emp.get("puesto", "") or "-", self.styles['Normal']),
                    Paragraph(str(emp.get("duracion_meses", 0)) + " meses", self.styles['Normal']),
                    Paragraph(f"${salario:,.0f}", self.styles['Normal']),
                    Paragraph(emp.get("motivo_separacion", "") or "-", self.styles['Normal'])
                ])
        
        # Anchos proporcionales: Empresa 25%, Puesto 20%, Duracion 15%, Salario 15%, Motivo 25%
        tabla_hist = Table(hist_data, colWidths=[1.6*inch, 1.3*inch, 1*inch, 1*inch, 1.6*inch])
        tabla_hist.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        
        # Usar KeepTogether para evitar cortes de pagina
        titulo = Paragraph("HISTORIAL LABORAL", self.styles['CustomHeading'])
        if len(hist_data) <= 8:  # Si son pocas filas, mantener todo junto
            elements.append(KeepTogether([titulo, tabla_hist, Spacer(1, 0.2*inch)]))
        else:
            # Para tablas grandes, al menos mantener titulo con encabezado
            elements.append(KeepTogether([titulo, Spacer(1, 0.05*inch)]))
            elements.append(tabla_hist)
            elements.append(Spacer(1, 0.2*inch))
    
    def _crear_seccion_referencias(self, datos: Dict, elements: list):
        """Crea la sección de referencias personales."""
        referencias = datos.get("referencias", [])
        
        if not referencias:
            return
        
        # Encabezados con texto blanco
        header_style = ParagraphStyle('RefHeader', parent=self.styles['Normal'], 
                                       textColor=colors.white, fontName='Helvetica-Bold', fontSize=9)
        ref_data = [
            [Paragraph("Nombre", header_style),
             Paragraph("Relacion", header_style),
             Paragraph("Telefono", header_style),
             Paragraph("Tiempo Conocido", header_style)]
        ]
        
        for ref in referencias:
            if isinstance(ref, dict):
                # Obtener tiempo conocido (puede estar en diferentes campos)
                tiempo = ref.get("tiempo_conocido", "")
                if not tiempo:
                    meses = ref.get("tiempo_conocerse_meses", 0)
                    if meses > 0:
                        if meses >= 12:
                            anos = meses // 12
                            meses_resto = meses % 12
                            if meses_resto > 0:
                                tiempo = f"{anos} ano(s) {meses_resto} mes(es)"
                            else:
                                tiempo = f"{anos} ano(s)"
                        else:
                            tiempo = f"{meses} mes(es)"
                
                ref_data.append([
                    Paragraph(ref.get("nombre", "") or "-", self.styles['Normal']),
                    Paragraph(ref.get("relacion", ref.get("parentesco", "")) or "-", self.styles['Normal']),
                    Paragraph(ref.get("telefono", "") or "-", self.styles['Normal']),
                    Paragraph(tiempo or "-", self.styles['Normal'])
                ])
        
        tabla_ref = Table(ref_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        tabla_ref.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        
        # Usar KeepTogether para evitar cortes de pagina
        titulo = Paragraph("REFERENCIAS PERSONALES", self.styles['CustomHeading'])
        if len(ref_data) <= 6:  # Si son pocas referencias, mantener todo junto
            elements.append(KeepTogether([titulo, tabla_ref, Spacer(1, 0.2*inch)]))
        else:
            elements.append(KeepTogether([titulo, Spacer(1, 0.05*inch)]))
            elements.append(tabla_ref)
            elements.append(Spacer(1, 0.2*inch))
    
    def _crear_seccion_analisis_riesgos(self, datos: Dict, elements: list):
        """Crea la sección de análisis de riesgos."""
        # BUG FIX: Usar primero los riesgos almacenados en el JSON si existen
        riesgos_almacenados = datos.get("riesgos", {})
        
        riesgos = {}
        justificaciones = []
        
        # Verificar si hay riesgos almacenados con puntajes válidos
        tiene_riesgos_almacenados = False
        for categoria, data in riesgos_almacenados.items():
            if isinstance(data, dict) and 'puntaje' in data:
                tiene_riesgos_almacenados = True
                break
        
        if tiene_riesgos_almacenados:
            # Usar los valores almacenados del JSON
            for categoria, data in riesgos_almacenados.items():
                if isinstance(data, dict):
                    if 'puntaje' in data:
                        riesgos[categoria] = data['puntaje']
                    if 'justificaciones' in data:
                        justificaciones.extend(data['justificaciones'])
        else:
            # Solo recalcular si no hay riesgos almacenados
            try:
                from src.logic.calculador_riesgos import CalculadorRiesgos
                riesgos_data = CalculadorRiesgos.calcular_todos_riesgos(datos)
                for categoria, data in riesgos_data.items():
                    if isinstance(data, dict):
                        if 'justificaciones' in data:
                            justificaciones.extend(data['justificaciones'])
                        if 'puntaje' in data:
                            riesgos[categoria] = data['puntaje']
            except Exception as e:
                print(f"Error calculando riesgos: {e}")
                riesgos = {}
                justificaciones = []
        
        # Categorías de riesgo con descripciones
        categorias = {
            "financiero": "Riesgo Financiero",
            "laboral": "Riesgo Laboral", 
            "salud": "Riesgo de Salud",
            "familiar": "Riesgo Familiar",
            "vivienda": "Riesgo de Vivienda",
            "estilo_vida": "Riesgo Estilo de Vida"
        }
        
        # Niveles de riesgo
        niveles = {
            1: ("Muy Bajo", colors.green),
            2: ("Bajo", colors.HexColor("#4CAF50")),
            3: ("Medio", colors.HexColor("#FFC107")),
            4: ("Alto", colors.HexColor("#FF9800")),
            5: ("Muy Alto", colors.red)
        }
        
        # Crear tabla de riesgos con Paragraphs para word wrap
        # Encabezados con texto blanco para fondo oscuro
        header_style = ParagraphStyle('HeaderWhite', parent=self.styles['Normal'], 
                                       textColor=colors.white, fontName='Helvetica-Bold')
        riesgo_data = [
            [Paragraph("Categoria", header_style),
             Paragraph("Nivel", header_style),
             Paragraph("Puntaje", header_style),
             Paragraph("Interpretacion", header_style)]
        ]
        
        riesgo_global = 0
        num_riesgos = 0
        
        for key, label in categorias.items():
            if key in riesgos:
                puntaje = riesgos[key]
                nivel, color = niveles.get(int(puntaje), ("Desconocido", colors.grey))
                riesgo_data.append([
                    Paragraph(label, self.styles['Normal']),
                    Paragraph(f"{puntaje:.1f}", self.styles['Normal']),
                    Paragraph(f"{int(puntaje)}/5", self.styles['Normal']),
                    Paragraph(f"<b>{nivel}</b>", self.styles['Normal'])
                ])
                riesgo_global += float(puntaje)
                num_riesgos += 1
        
        # Calcular riesgo global
        if num_riesgos > 0:
            riesgo_global = riesgo_global / num_riesgos
            riesgo_global_redondeado = int(round(riesgo_global))
            nivel_global, color_global = niveles.get(riesgo_global_redondeado, ("Desconocido", colors.grey))
            riesgo_data.append([
                Paragraph("<b>RIESGO GLOBAL</b>", self.styles['Normal']),
                Paragraph(f"<b>{riesgo_global:.2f}</b>", self.styles['Normal']),
                Paragraph(f"<b>{riesgo_global_redondeado}/5</b>", self.styles['Normal']),
                Paragraph(f"<b>{nivel_global}</b>", self.styles['Normal'])
            ])
        
        # Anchos proporcionales: Categoria 30%, Nivel 15%, Puntaje 15%, Interpretacion 40%
        tabla_riesgos = Table(riesgo_data, colWidths=[1.95*inch, 0.97*inch, 0.97*inch, 2.6*inch])
        tabla_riesgos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (1, 0), (2, -1), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        # Usar KeepTogether para mantener titulo y tabla de riesgos juntos
        titulo_riesgos = Paragraph("ANALISIS DE RIESGOS", self.styles['CustomHeading'])
        elements.append(KeepTogether([titulo_riesgos, tabla_riesgos, Spacer(1, 0.2*inch)]))
        
        # Justificaciones - formato compacto en tabla de 2 columnas si hay muchas
        if justificaciones:
            # Filtrar justificaciones vacias
            justificaciones_validas = [j for j in justificaciones if j and j.strip()]
            
            if justificaciones_validas:
                titulo_just = Paragraph("<b>Justificaciones de Riesgos:</b>", self.styles['CustomHeading'])
                
                if len(justificaciones_validas) > 6:
                    # Formato compacto: tabla de 2 columnas
                    mitad = (len(justificaciones_validas) + 1) // 2
                    col1 = justificaciones_validas[:mitad]
                    col2 = justificaciones_validas[mitad:]
                    
                    # Crear filas con ambas columnas
                    just_data = []
                    for i in range(mitad):
                        item1 = Paragraph(f"<bullet>&bull;</bullet> {col1[i]}", self.styles['Normal'])
                        item2 = Paragraph(f"<bullet>&bull;</bullet> {col2[i]}", self.styles['Normal']) if i < len(col2) else Paragraph("", self.styles['Normal'])
                        just_data.append([item1, item2])
                    
                    just_table = Table(just_data, colWidths=[3.25*inch, 3.25*inch])
                    just_table.setStyle(TableStyle([
                        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                        ('LEFTPADDING', (0, 0), (-1, -1), 3),
                        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
                        ('TOPPADDING', (0, 0), (-1, -1), 2),
                        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                    ]))
                    # KeepTogether para titulo y tabla de justificaciones
                    elements.append(KeepTogether([titulo_just, just_table, Spacer(1, 0.2*inch)]))
                else:
                    # Formato normal para pocas justificaciones - crear lista y usar KeepTogether
                    lista_just = [titulo_just]
                    for just in justificaciones_validas:
                        lista_just.append(Paragraph(f"<bullet>&bull;</bullet> {just}", self.styles['CustomBody']))
                    lista_just.append(Spacer(1, 0.2*inch))
                    elements.append(KeepTogether(lista_just))
    
    def _crear_graficos_completos(self, datos: Dict, elements: list):
        """Crea todas las graficas del estudio (6 graficas en total)."""
        # Cargar matplotlib de forma lazy
        if not _cargar_matplotlib():
            return
        
        try:
            elements.append(PageBreak())
            elements.append(Paragraph("GRAFICAS Y ANALISIS VISUAL", self.styles['CustomHeading']))
            elements.append(Spacer(1, 0.1*inch))
            
            # ============================================
            # GRAFICA 1: Ingresos vs Gastos vs Ahorros
            # ============================================
            fig1 = self._crear_grafica_ingresos_vs_gastos(datos)
            if fig1:
                temp_path1 = self._guardar_figura_temporal(fig1)
                if temp_path1:
                    titulo1 = Paragraph("<b>1. Analisis Financiero: Ingresos vs Gastos</b>", self.styles['CustomBody'])
                    img1 = Image(temp_path1, width=6*inch, height=3*inch)
                    elements.append(KeepTogether([titulo1, img1, Spacer(1, 0.2*inch)]))
            
            # ============================================
            # GRAFICA 2: Distribucion de Deudas
            # ============================================
            fig2 = self._crear_grafica_distribucion_deudas(datos)
            if fig2:
                temp_path2 = self._guardar_figura_temporal(fig2)
                if temp_path2:
                    titulo2 = Paragraph("<b>2. Distribucion de Deudas</b>", self.styles['CustomBody'])
                    img2 = Image(temp_path2, width=6*inch, height=3*inch)
                    elements.append(KeepTogether([titulo2, img2, Spacer(1, 0.2*inch)]))
            
            # ============================================
            # GRAFICA 3: Indicadores Financieros
            # ============================================
            fig3 = self._crear_grafica_indicadores_financieros(datos)
            if fig3:
                temp_path3 = self._guardar_figura_temporal(fig3)
                if temp_path3:
                    titulo3 = Paragraph("<b>3. Indicadores Financieros Clave</b>", self.styles['CustomBody'])
                    img3 = Image(temp_path3, width=6*inch, height=3*inch)
                    elements.append(KeepTogether([titulo3, img3, Spacer(1, 0.2*inch)]))
            
            elements.append(PageBreak())
            
            # ============================================
            # GRAFICA 4: Distribucion de Gastos
            # ============================================
            fig4 = self._crear_grafica_distribucion_gastos(datos)
            if fig4:
                temp_path4 = self._guardar_figura_temporal(fig4)
                if temp_path4:
                    titulo4 = Paragraph("<b>4. Distribucion de Gastos Mensuales</b>", self.styles['CustomBody'])
                    img4 = Image(temp_path4, width=6*inch, height=4*inch)
                    elements.append(KeepTogether([titulo4, img4, Spacer(1, 0.2*inch)]))
            
            # ============================================
            # GRAFICA 5: Radar de Riesgos
            # ============================================
            fig5 = self._crear_grafica_radar_riesgos(datos)
            if fig5:
                temp_path5 = self._guardar_figura_temporal(fig5)
                if temp_path5:
                    titulo5 = Paragraph("<b>5. Radar de Indicadores de Riesgo</b>", self.styles['CustomBody'])
                    img5 = Image(temp_path5, width=6*inch, height=4*inch)
                    elements.append(KeepTogether([titulo5, img5, Spacer(1, 0.2*inch)]))
            
            # ============================================
            # GRAFICA 6: Actividades y Habitos
            # ============================================
            fig6 = self._crear_grafica_actividades(datos)
            if fig6:
                temp_path6 = self._guardar_figura_temporal(fig6)
                if temp_path6:
                    titulo6 = Paragraph("<b>6. Frecuencia de Actividades y Habitos</b>", self.styles['CustomBody'])
                    img6 = Image(temp_path6, width=6*inch, height=3.5*inch)
                    elements.append(KeepTogether([titulo6, img6, Spacer(1, 0.2*inch)]))
            
        except Exception as e:
            print(f"Error creando graficos completos: {e}")
            import traceback
            traceback.print_exc()
    
    def _guardar_figura_temporal(self, fig) -> Optional[str]:
        """Guarda una figura matplotlib en archivo temporal y retorna la ruta."""
        try:
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                temp_path = tmp.name
            fig.savefig(temp_path, dpi=150, bbox_inches='tight', facecolor='white')
            self._temp_files.append(temp_path)
            _plt.close(fig)
            return temp_path
        except Exception as e:
            print(f"Error guardando figura: {e}")
            return None
    
    def _crear_grafica_ingresos_vs_gastos(self, datos: Dict):
        """Crea grafica de barras: Ingresos vs Gastos vs Ahorros."""
        try:
            fig, ax = _plt.subplots(figsize=(10, 5))
            
            finanzas = datos.get('situacion_financiera', {})
            ingreso = finanzas.get('ingreso_total_mensual', 0) or finanzas.get('sueldo_mensual', 0) or 0
            ahorros = finanzas.get('monto_ahorros_mensuales', 0) or 0
            gastos_dict = finanzas.get('gastos', {})
            total_gastos = gastos_dict.get('total', 0) if isinstance(gastos_dict, dict) else 0
            balance = finanzas.get('balance', ingreso - total_gastos)
            
            categorias = ['Ingresos\nMensuales', 'Gastos\nTotales', 'Ahorros\nMensuales', 'Balance\nDisponible']
            valores = [ingreso, total_gastos, ahorros, balance]
            colores = ['#27ae60', '#e74c3c', '#3498db', '#f39c12']
            
            barras = ax.bar(categorias, valores, color=colores, edgecolor='black', linewidth=1.5, alpha=0.8)
            
            for barra in barras:
                altura = barra.get_height()
                ax.text(barra.get_x() + barra.get_width()/2., altura,
                       f'${altura:,.0f}', ha='center', va='bottom', fontweight='bold', fontsize=9)
            
            ax.set_ylabel('Monto ($)', fontweight='bold')
            ax.set_title('Ingresos vs Gastos vs Ahorros Mensuales', fontweight='bold', fontsize=12)
            ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
            ax.grid(axis='y', alpha=0.3)
            fig.tight_layout()
            return fig
        except Exception as e:
            print(f"Error en grafica ingresos vs gastos: {e}")
            return None
    
    def _crear_grafica_distribucion_deudas(self, datos: Dict):
        """Crea grafica de pastel: Distribucion de Deudas."""
        try:
            fig, ax = _plt.subplots(figsize=(10, 5))
            
            finanzas = datos.get('situacion_financiera', {})
            deuda_tarjetas = finanzas.get('deuda_tarjetas_total', 0) or 0
            prestamos = finanzas.get('monto_prestamos_personales', 0) if finanzas.get('tiene_prestamos_personales') else 0
            hipoteca = finanzas.get('monto_hipoteca', 0) if finanzas.get('tiene_prestamo_hipotecario') else 0
            auto = finanzas.get('monto_prestamo_auto', 0) if finanzas.get('tiene_prestamo_auto') else 0
            
            total = deuda_tarjetas + prestamos + hipoteca + auto
            
            if total == 0:
                ax.text(0.5, 0.5, 'Sin Deudas Registradas', ha='center', va='center', 
                       fontsize=14, fontweight='bold', color='#27ae60')
                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)
                ax.axis('off')
            else:
                etiquetas = []
                valores = []
                colores_pastel = ['#e74c3c', '#e67e22', '#f39c12', '#3498db']
                
                if prestamos > 0:
                    etiquetas.append(f'Prestamos\n${prestamos:,.0f}')
                    valores.append(prestamos)
                if hipoteca > 0:
                    etiquetas.append(f'Hipoteca\n${hipoteca:,.0f}')
                    valores.append(hipoteca)
                if auto > 0:
                    etiquetas.append(f'Auto\n${auto:,.0f}')
                    valores.append(auto)
                if deuda_tarjetas > 0:
                    etiquetas.append(f'Tarjetas\n${deuda_tarjetas:,.0f}')
                    valores.append(deuda_tarjetas)
                
                if valores:
                    wedges, texts, autotexts = ax.pie(valores, labels=etiquetas, autopct='%1.1f%%',
                                                      colors=colores_pastel[:len(valores)],
                                                      startangle=90, textprops={'fontweight': 'bold'})
                    for autotext in autotexts:
                        autotext.set_color('white')
                        autotext.set_fontsize(10)
                    ax.set_title(f'Distribucion de Deudas - Total: ${sum(valores):,.0f}', fontweight='bold', fontsize=12)
            
            fig.tight_layout()
            return fig
        except Exception as e:
            print(f"Error en grafica distribucion deudas: {e}")
            return None
    
    def _crear_grafica_indicadores_financieros(self, datos: Dict):
        """Crea grafica de indicadores financieros clave."""
        try:
            fig, ax = _plt.subplots(figsize=(10, 5))
            
            finanzas = datos.get('situacion_financiera', {})
            ingreso = finanzas.get('ingreso_total_mensual', 0) or finanzas.get('sueldo_mensual', 0) or 1
            ahorros = finanzas.get('monto_ahorros_mensuales', 0) or 0
            total_deudas = finanzas.get('total_deudas', 0) or 0
            
            porcentaje_ahorro = (ahorros / ingreso * 100) if ingreso > 0 else 0
            porcentaje_deudas = (total_deudas / (ingreso * 12) * 100) if ingreso > 0 else 0
            
            ahorro_saludable = 20
            deuda_maxima = 35
            
            indicadores = ['% Ahorro\n(meta: 20%)', '% Deudas/Ingreso Anual\n(max: 35%)']
            valores_actuales = [porcentaje_ahorro, min(porcentaje_deudas, 100)]
            valores_referencia = [ahorro_saludable, deuda_maxima]
            
            x = _np.arange(len(indicadores))
            ancho = 0.35
            
            barras1 = ax.bar(x - ancho/2, valores_actuales, ancho, label='Valor Actual',
                            color=['#3498db', '#e74c3c'], alpha=0.8, edgecolor='black')
            barras2 = ax.bar(x + ancho/2, valores_referencia, ancho, label='Valor Referencia',
                            color=['#95a5a6', '#95a5a6'], alpha=0.5, edgecolor='black')
            
            ax.set_ylabel('Porcentaje (%)', fontweight='bold')
            ax.set_title('Indicadores Financieros Clave', fontweight='bold', fontsize=12)
            ax.set_xticks(x)
            ax.set_xticklabels(indicadores, fontweight='bold')
            ax.legend(loc='upper right')
            ax.grid(axis='y', alpha=0.3)
            
            for barras in [barras1, barras2]:
                for barra in barras:
                    altura = barra.get_height()
                    ax.text(barra.get_x() + barra.get_width()/2., altura,
                           f'{altura:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=9)
            
            fig.tight_layout()
            return fig
        except Exception as e:
            print(f"Error en grafica indicadores financieros: {e}")
            return None
    
    def _crear_grafica_distribucion_gastos(self, datos: Dict):
        """Crea grafica de pastel con distribucion de gastos."""
        try:
            fig, ax = _plt.subplots(figsize=(10, 6))
            
            finanzas = datos.get('situacion_financiera', {})
            gastos = finanzas.get('gastos', {}) or {}
            
            gastos_data = {
                'Alimentacion': gastos.get('alimentacion', 0) or 0,
                'Salud': gastos.get('salud', 0) or 0,
                'Educacion': gastos.get('educacion', 0) or 0,
                'Recreacion': gastos.get('recreacion', 0) or 0,
                'Vivienda': gastos.get('vivienda', 0) or 0,
                'Transporte': gastos.get('transporte', 0) or 0,
                'Servicios': gastos.get('servicios', 0) or 0,
                'Otros': gastos.get('otros', 0) or 0
            }
            
            gastos_filtrados = {k: v for k, v in gastos_data.items() if v > 0}
            
            if not gastos_filtrados:
                ax.text(0.5, 0.5, 'Sin Gastos Registrados', ha='center', va='center', 
                       fontsize=14, fontweight='bold', color='#7f8c8d')
                ax.set_xlim(0, 1)
                ax.set_ylim(0, 1)
                ax.axis('off')
            else:
                etiquetas = [f'{k}\n${v:,.0f}' for k, v in gastos_filtrados.items()]
                valores = list(gastos_filtrados.values())
                colores = ['#3498db', '#e74c3c', '#f39c12', '#27ae60', '#9b59b6', 
                          '#1abc9c', '#e67e22', '#34495e']
                
                wedges, texts, autotexts = ax.pie(valores, labels=etiquetas, autopct='%1.1f%%',
                                                  colors=colores[:len(valores)], startangle=90,
                                                  textprops={'fontweight': 'bold', 'fontsize': 9})
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontsize(9)
                
                total = sum(valores)
                ax.set_title(f'Distribucion de Gastos Mensuales - Total: ${total:,.0f}', fontweight='bold', fontsize=12)
            
            fig.tight_layout()
            return fig
        except Exception as e:
            print(f"Error en grafica distribucion gastos: {e}")
            return None
    
    def _crear_grafica_radar_riesgos(self, datos: Dict):
        """Crea grafica de radar para indicadores de riesgo."""
        try:
            fig, ax = _plt.subplots(figsize=(10, 7), subplot_kw=dict(projection='polar'))
            
            riesgos_data = datos.get('riesgos', {})
            
            def get_riesgo_valor(key):
                data = riesgos_data.get(key, {})
                if isinstance(data, dict):
                    return float(data.get('puntaje', data.get('nivel', 1)))
                elif isinstance(data, (int, float)):
                    return float(data)
                return 1.0
            
            categorias = ['Financiero', 'Familiar', 'Vivienda', 'Laboral', 'Salud', 'Estilo Vida']
            valores = [
                get_riesgo_valor('financiero'),
                get_riesgo_valor('familiar'),
                get_riesgo_valor('vivienda'),
                get_riesgo_valor('laboral'),
                get_riesgo_valor('salud'),
                get_riesgo_valor('estilo_vida')
            ]
            
            valores_plot = valores + valores[:1]
            angulos = _np.linspace(0, 2 * _np.pi, len(categorias), endpoint=False).tolist()
            angulos += angulos[:1]
            
            ax.plot(angulos, valores_plot, 'o-', linewidth=2, color='#e74c3c', label='Nivel de Riesgo')
            ax.fill(angulos, valores_plot, alpha=0.25, color='#e74c3c')
            
            zona_segura = [3] * len(angulos)
            ax.plot(angulos, zona_segura, '--', linewidth=1.5, color='#27ae60', alpha=0.7, label='Zona Segura (< 3)')
            ax.fill(angulos, zona_segura, alpha=0.1, color='#27ae60')
            
            ax.set_xticks(angulos[:-1])
            ax.set_xticklabels(categorias, fontweight='bold', fontsize=9)
            ax.set_ylim(0, 5)
            ax.set_yticks([1, 2, 3, 4, 5])
            ax.set_yticklabels(['1', '2', '3', '4', '5'], fontsize=8)
            ax.set_title('Indicadores de Riesgo (Escala 1-5)', fontweight='bold', fontsize=12, pad=20)
            ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
            ax.grid(True, alpha=0.3)
            
            fig.tight_layout()
            return fig
        except Exception as e:
            print(f"Error en grafica radar riesgos: {e}")
            return None
    
    def _crear_grafica_actividades(self, datos: Dict):
        """Crea grafica de barras horizontales para actividades."""
        try:
            fig, ax = _plt.subplots(figsize=(10, 5))
            
            estilo = datos.get('estilo_vida', {})
            salud = datos.get('salud_intereses', {})
            
            actividades = {
                'Hobbies': estilo.get('numero_hobbies', 0) or 0,
                'Salidas/Mes': estilo.get('frecuencia_salidas_mes', 0) or 0,
                'Viajes/Ano': estilo.get('numero_viajes_ultimo_ano', 0) or 0,
                'Ejercicio/Semana': estilo.get('frecuencia_ejercicio_semana', 0) or 0,
                'Cultura/Mes': estilo.get('frecuencia_actividades_culturales_mes', 0) or 0,
                'Copas/Semana': salud.get('copas_por_semana', 0) or 0,
                'Cigarros/Dia': salud.get('cigarros_por_dia', 0) or 0
            }
            
            colores = {
                'Hobbies': '#9b59b6',
                'Salidas/Mes': '#3498db',
                'Viajes/Ano': '#1abc9c',
                'Ejercicio/Semana': '#27ae60',
                'Cultura/Mes': '#f39c12',
                'Copas/Semana': '#e67e22',
                'Cigarros/Dia': '#e74c3c'
            }
            
            categorias = list(actividades.keys())
            valores = list(actividades.values())
            colores_barras = [colores.get(cat, '#34495e') for cat in categorias]
            
            barras = ax.barh(categorias, valores, color=colores_barras, edgecolor='black', linewidth=1, alpha=0.8)
            
            for i, (barra, valor) in enumerate(zip(barras, valores)):
                ax.text(valor + 0.2, i, str(int(valor)), va='center', fontweight='bold', fontsize=9)
            
            ax.set_xlabel('Frecuencia', fontweight='bold')
            ax.set_title('Frecuencia de Actividades y Habitos', fontweight='bold', fontsize=12)
            ax.grid(axis='x', alpha=0.3)
            ax.invert_yaxis()
            
            fig.tight_layout()
            return fig
        except Exception as e:
            print(f"Error en grafica actividades: {e}")
            return None
    
    def _crear_graficos_riesgos(self, datos: Dict, elements: list):
        """Metodo legacy - ahora llama a _crear_graficos_completos."""
        self._crear_graficos_completos(datos, elements)
    
    def _crear_seccion_validacion_documental(self, datos: Dict, elements: list):
        """Crea la seccion de validacion documental."""
        elements.append(PageBreak())
        
        val = datos.get("validacion_documental", {})
        
        # Usar Paragraphs para word wrap automatico en observaciones
        # Encabezados con texto blanco para fondo oscuro
        header_style = ParagraphStyle('ValDocHeader', parent=self.styles['Normal'], 
                                       textColor=colors.white, fontName='Helvetica-Bold', fontSize=9)
        docs_data = [
            [Paragraph("Documento", header_style),
             Paragraph("Verificado", header_style),
             Paragraph("Observaciones", header_style)],
            [Paragraph("INE", self.styles['Normal']),
             Paragraph("Si" if val.get("ine_verificada") else "No", self.styles['Normal']),
             Paragraph(val.get("ine_observaciones", "") or "-", self.styles['Normal'])],
            [Paragraph("CURP", self.styles['Normal']),
             Paragraph("Si" if val.get("curp_validada") else "No", self.styles['Normal']),
             Paragraph(val.get("curp_observaciones", "") or "-", self.styles['Normal'])],
            [Paragraph("RFC (SAT)", self.styles['Normal']),
             Paragraph("Si" if val.get("rfc_validado_sat") else "No", self.styles['Normal']),
             Paragraph(val.get("rfc_observaciones", "") or "-", self.styles['Normal'])],
            [Paragraph("NSS (IMSS)", self.styles['Normal']),
             Paragraph("Si" if val.get("nss_validado_imss") else "No", self.styles['Normal']),
             Paragraph(val.get("nss_observaciones", "") or "-", self.styles['Normal'])],
            [Paragraph("Comprobante Domicilio", self.styles['Normal']),
             Paragraph("Si" if val.get("comprobante_domicilio_verificado") else "No", self.styles['Normal']),
             Paragraph(f"{val.get('comprobante_tipo', '')} - {val.get('comprobante_fecha', '')}" or "-", self.styles['Normal'])],
            [Paragraph("Recibo de Nomina", self.styles['Normal']),
             Paragraph("Si" if val.get("recibo_nomina_verificado") else "No", self.styles['Normal']),
             Paragraph(val.get("nomina_periodo", "") or val.get("nomina_observaciones", "") or "-", self.styles['Normal'])],
            [Paragraph("Constancia Laboral", self.styles['Normal']),
             Paragraph("Si" if val.get("constancia_laboral_verificada") else "No", self.styles['Normal']),
             Paragraph(val.get("constancia_observaciones", "") or "-", self.styles['Normal'])],
            [Paragraph("Estados de Cuenta", self.styles['Normal']),
             Paragraph("Si" if val.get("estados_cuenta_verificados") else "No", self.styles['Normal']),
             Paragraph(f"{val.get('estados_cuenta_meses', 0)} meses - {val.get('estados_cuenta_observaciones', '')}" if val.get("estados_cuenta_meses") else "-", self.styles['Normal'])]
        ]
        
        # Anchos proporcionales: Documento 23%, Verificado 15%, Observaciones 62%
        tabla_docs = Table(docs_data, colWidths=[1.5*inch, 1*inch, 4*inch])
        tabla_docs.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        # Resumen
        doc_completa = "SI" if val.get("documentacion_completa") else "NO"
        resumen = Paragraph(f"<b>Documentacion Completa:</b> {doc_completa}", self.styles['CustomBody'])
        
        # Usar KeepTogether para mantener titulo y tabla juntos
        titulo_val = Paragraph("VALIDACION DOCUMENTAL", self.styles['CustomHeading'])
        elements.append(KeepTogether([titulo_val, tabla_docs, Spacer(1, 0.1*inch), resumen]))
        
        if val.get("observaciones_documentacion"):
            elements.append(Paragraph(f"<b>Observaciones:</b> {val.get('observaciones_documentacion')}", 
                                     self.styles['CustomBody']))
        
        elements.append(Spacer(1, 0.2*inch))
    
    def _crear_seccion_investigacion_vecinal(self, datos: Dict, elements: list):
        """Crea la seccion de investigacion vecinal."""
        inv = datos.get("investigacion_vecinal", {})
        
        # Datos de la visita
        info_visita = [
            ["Visita Domiciliaria Realizada:", "Si" if inv.get("visita_domiciliaria_realizada") else "No"],
            ["Fecha de Visita:", inv.get("fecha_visita", "N/A")],
            ["Hora de Visita:", inv.get("hora_visita", "N/A")],
            ["Persona que Atendio:", inv.get("persona_atendio", "N/A")],
            ["Parentesco:", inv.get("parentesco_persona_atendio", "N/A")]
        ]
        
        tabla_visita = Table(info_visita, colWidths=[2.5*inch, 4*inch])
        tabla_visita.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        # Usar KeepTogether para titulo y tabla de visita
        titulo_vecinal = Paragraph("INVESTIGACION VECINAL", self.styles['CustomHeading'])
        elements.append(KeepTogether([titulo_vecinal, tabla_visita, Spacer(1, 0.1*inch)]))
        
        # Entrevista con vecino
        if inv.get("vecino_entrevistado"):
            elements.append(Paragraph("<b>Entrevista con Vecino:</b>", self.styles['CustomBody']))
            
            # Usar Paragraphs para word wrap en comentarios
            label_style_vecino = ParagraphStyle('VecinoLabel', parent=self.styles['Normal'], 
                                                 fontName='Helvetica-Bold', fontSize=9)
            info_vecino = [
                [Paragraph("Nombre del Vecino:", label_style_vecino), Paragraph(inv.get("vecino_nombre", "N/A") or "N/A", self.styles['Normal'])],
                [Paragraph("Direccion:", label_style_vecino), Paragraph(inv.get("vecino_direccion", "N/A") or "N/A", self.styles['Normal'])],
                [Paragraph("Tiempo de Conocerlo:", label_style_vecino), Paragraph(inv.get("vecino_tiempo_conocerlo", "N/A") or "N/A", self.styles['Normal'])],
                [Paragraph("Opinion sobre Comportamiento:", label_style_vecino), Paragraph(inv.get("vecino_opinion_comportamiento", "N/A") or "N/A", self.styles['Normal'])],
                [Paragraph("Comentarios:", label_style_vecino), Paragraph(inv.get("vecino_comentarios", "N/A") or "N/A", self.styles['Normal'])],
                [Paragraph("Tiempo Residencia Confirmado:", label_style_vecino), Paragraph("Si" if inv.get("tiempo_residencia_confirmado") else "No", self.styles['Normal'])],
                [Paragraph("Tiempo segun Vecino:", label_style_vecino), Paragraph(inv.get("tiempo_residencia_segun_vecino", "N/A") or "N/A", self.styles['Normal'])]
            ]
            
            tabla_vecino = Table(info_vecino, colWidths=[2.5*inch, 4*inch])
            tabla_vecino.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('PADDING', (0, 0), (-1, -1), 6),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            
            elements.append(tabla_vecino)
            elements.append(Spacer(1, 0.1*inch))
        
        # Contacto con arrendador (si aplica)
        if inv.get("arrendador_contactado"):
            elements.append(Paragraph("<b>Contacto con Arrendador:</b>", self.styles['CustomBody']))
            
            info_arrendador = [
                ["Nombre:", inv.get("arrendador_nombre", "N/A")],
                ["Telefono:", inv.get("arrendador_telefono", "N/A")],
                ["Opinion:", inv.get("arrendador_opinion", "N/A")],
                ["Historial de Pagos:", inv.get("arrendador_historial_pagos", "N/A")]
            ]
            
            tabla_arrendador = Table(info_arrendador, colWidths=[2.5*inch, 4*inch])
            tabla_arrendador.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('PADDING', (0, 0), (-1, -1), 6),
            ]))
            
            elements.append(tabla_arrendador)
            elements.append(Spacer(1, 0.1*inch))
        
        # Observaciones con word wrap automatico
        label_style = ParagraphStyle('ObsLabel', parent=self.styles['Normal'], 
                                      fontName='Helvetica-Bold', fontSize=9)
        info_obs = [
            [Paragraph("Condiciones Vivienda Observadas:", label_style), Paragraph(inv.get("condiciones_vivienda_observadas", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Ambiente Familiar Observado:", label_style), Paragraph(inv.get("ambiente_familiar_observado", "N/A") or "N/A", self.styles['Normal'])],
            [Paragraph("Observaciones Generales:", label_style), Paragraph(inv.get("observaciones_investigacion", "N/A") or "N/A", self.styles['Normal'])]
        ]
        
        tabla_obs = Table(info_obs, colWidths=[2.5*inch, 4*inch])
        tabla_obs.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(tabla_obs)
        elements.append(Spacer(1, 0.2*inch))
    
    def _crear_seccion_analisis_cualitativo(self, datos: Dict, elements: list):
        """Crea la seccion de analisis cualitativo."""
        anal = datos.get("analisis_cualitativo", {})
        
        # Usar Paragraphs para word wrap automatico
        # Encabezados con texto blanco para fondo oscuro
        header_style = ParagraphStyle('CualHeader', parent=self.styles['Normal'], 
                                       textColor=colors.white, fontName='Helvetica-Bold', fontSize=9)
        info_cualitativo = [
            [Paragraph("Aspecto", header_style),
             Paragraph("Evaluacion", header_style),
             Paragraph("Observaciones", header_style)],
            [Paragraph("Estabilidad Emocional", self.styles['Normal']),
             Paragraph(anal.get("estabilidad_emocional", "No evaluado"), self.styles['Normal']),
             Paragraph(anal.get("estabilidad_emocional_observaciones", "") or "-", self.styles['Normal'])],
            [Paragraph("Perfil de Responsabilidad", self.styles['Normal']),
             Paragraph(anal.get("responsabilidad_percibida", "") or anal.get("perfil_responsabilidad", "No evaluado"), self.styles['Normal']),
             Paragraph(anal.get("responsabilidad_observaciones", "") or anal.get("responsabilidad_indicadores", "") or "-", self.styles['Normal'])],
            [Paragraph("Congruencia Nivel de Vida/Ingresos", self.styles['Normal']),
             Paragraph(anal.get("congruencia_nivel_vida_ingresos", "No evaluado"), self.styles['Normal']),
             Paragraph(anal.get("congruencia_observaciones", "") or "-", self.styles['Normal'])],
            [Paragraph("Riesgo Reputacional", self.styles['Normal']),
             Paragraph(anal.get("riesgo_reputacional", "No evaluado"), self.styles['Normal']),
             Paragraph(anal.get("riesgo_reputacional_observaciones", "") or anal.get("riesgo_reputacional_motivo", "") or "-", self.styles['Normal'])],
            [Paragraph("Nivel de Arraigo", self.styles['Normal']),
             Paragraph(anal.get("arraigo_local", "") or anal.get("nivel_arraigo", "No evaluado"), self.styles['Normal']),
             Paragraph(anal.get("arraigo_observaciones", "") or anal.get("arraigo_indicadores", "") or "-", self.styles['Normal'])],
            [Paragraph("Actitud en Entrevista", self.styles['Normal']),
             Paragraph(anal.get("actitud_durante_entrevista", "") or anal.get("actitud_entrevista", "No evaluado"), self.styles['Normal']),
             Paragraph(anal.get("actitud_observaciones", "") or "-", self.styles['Normal'])],
            [Paragraph("Coherencia de Respuestas", self.styles['Normal']),
             Paragraph(anal.get("coherencia_respuestas", "No evaluado"), self.styles['Normal']),
             Paragraph("-", self.styles['Normal'])]
        ]
        
        # Anchos proporcionales: Aspecto 28%, Evaluacion 17%, Observaciones 55%
        tabla_cualitativo = Table(info_cualitativo, colWidths=[1.8*inch, 1.1*inch, 3.6*inch])
        tabla_cualitativo.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        # Usar KeepTogether para titulo y tabla de analisis cualitativo
        titulo_cualitativo = Paragraph("ANALISIS CUALITATIVO", self.styles['CustomHeading'])
        elements.append(KeepTogether([titulo_cualitativo, tabla_cualitativo]))
        
        if anal.get("observaciones_cualitativas"):
            elements.append(Spacer(1, 0.1*inch))
            elements.append(Paragraph(f"<b>Observaciones Cualitativas:</b> {anal.get('observaciones_cualitativas')}", 
                                     self.styles['CustomBody']))
        
        elements.append(Spacer(1, 0.2*inch))
    
    def _crear_seccion_fotos(self, datos: Dict, elements: list):
        """Crea la seccion de fotos del estudio (fachada, interior, etc.)."""
        fotos = datos.get("fotos", [])
        if not fotos:
            return
        
        elements.append(PageBreak())
        elements.append(Paragraph("ANEXO FOTOGRAFICO", self.styles['CustomHeading']))
        elements.append(Spacer(1, 0.2*inch))
        
        for i, foto in enumerate(fotos):
            archivo = foto.get("archivo", "")
            tipo = foto.get("tipo", f"Foto {i+1}")
            descripcion = foto.get("descripcion", "")
            
            if archivo and os.path.exists(archivo):
                try:
                    # Titulo de la foto
                    titulo_foto = Paragraph(f"<b>{tipo}</b>", self.styles['CustomBody'])
                    
                    # Cargar imagen con dimensiones apropiadas
                    from PIL import Image as PILImage
                    with PILImage.open(archivo) as pil_img:
                        orig_width, orig_height = pil_img.size
                        aspect_ratio = orig_width / orig_height if orig_height > 0 else 1
                        
                        # Dimensiones maximas para fotos - usar todo el ancho disponible
                        max_width = 6.0 * inch
                        max_height = 7.0 * inch
                        
                        # Escalar manteniendo proporcion
                        if aspect_ratio > 1:  # Horizontal
                            new_width = max_width
                            new_height = new_width / aspect_ratio
                        else:  # Vertical
                            new_height = max_height
                            new_width = new_height * aspect_ratio
                        
                        # Ajustar si excede limites
                        if new_width > max_width:
                            new_width = max_width
                            new_height = new_width / aspect_ratio
                        if new_height > max_height:
                            new_height = max_height
                            new_width = new_height * aspect_ratio
                        
                        img = Image(archivo, width=new_width, height=new_height)
                    
                    img.hAlign = 'CENTER'
                    
                    # Descripcion si existe
                    foto_elements = [titulo_foto, Spacer(1, 0.1*inch), img]
                    if descripcion:
                        foto_elements.append(Spacer(1, 0.05*inch))
                        foto_elements.append(Paragraph(descripcion, self.styles['CustomBody']))
                    
                    foto_elements.append(Spacer(1, 0.3*inch))
                    
                    # Usar KeepTogether para mantener foto con su titulo
                    elements.append(KeepTogether(foto_elements))
                    
                except Exception as e:
                    print(f"Error al procesar foto {archivo}: {e}")
                    elements.append(Paragraph(f"[Error al cargar imagen: {tipo}]", self.styles['Normal']))
                    elements.append(Spacer(1, 0.2*inch))
    
    def _crear_seccion_conclusiones_firma(self, datos: Dict, elements: list):
        """Crea la seccion de conclusiones y firma del investigador."""
        elements.append(PageBreak())
        elements.append(Paragraph("CONCLUSIONES Y RECOMENDACION", self.styles['CustomHeading']))
        
        # Conclusiones del estudio - dividir en parrafos si es muy largo
        conclusiones = datos.get("conclusiones", "")
        if conclusiones:
            # Dividir por puntos para mejor legibilidad
            # Si tiene mas de 300 caracteres, dividir en parrafos
            if len(conclusiones) > 300:
                # Buscar separadores naturales (. seguido de espacio y mayuscula)
                import re
                parrafos = re.split(r'(?<=[.!?])\s+(?=[A-Z])', conclusiones)
                for i, parrafo in enumerate(parrafos):
                    if parrafo.strip():
                        elements.append(Paragraph(parrafo.strip(), self.styles['CustomBody']))
                        if i < len(parrafos) - 1:
                            elements.append(Spacer(1, 0.08*inch))
            else:
                elements.append(Paragraph(conclusiones, self.styles['CustomBody']))
        else:
            elements.append(Paragraph("<i>Sin conclusiones registradas.</i>", self.styles['CustomBody']))
        
        elements.append(Spacer(1, 0.3*inch))
        
        # Datos del investigador
        elements.append(Paragraph("DATOS DEL INVESTIGADOR", self.styles['CustomHeading']))
        
        inv = datos.get("investigador", {})
        
        info_investigador = [
            ["Nombre del Investigador:", inv.get("nombre_investigador", "") or self.config.get("ejecutor", "")],
            ["Cedula Profesional:", inv.get("cedula_profesional", "N/A")],
            ["Empresa Investigadora:", inv.get("empresa_investigadora", "") or self.config.get("nombre", "")],
            ["Telefono:", inv.get("telefono_investigador", "") or self.config.get("telefono", "")],
            ["Email:", inv.get("email_investigador", "") or self.config.get("email", "")],
            ["Fecha de Elaboracion:", inv.get("fecha_elaboracion", datos.get("fecha_estudio", ""))],
            ["Lugar de Elaboracion:", inv.get("lugar_elaboracion", "")]
        ]
        
        tabla_inv = Table(info_investigador, colWidths=[2.5*inch, 4*inch])
        tabla_inv.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(tabla_inv)
        elements.append(Spacer(1, 0.3*inch))
        
        # Declaracion de veracidad - usar KeepTogether con la firma
        declaracion_titulo = Paragraph("DECLARACION DE VERACIDAD", self.styles['CustomHeading'])
        
        declaracion_texto = """
        El suscrito declara bajo protesta de decir verdad que la informacion contenida en el 
        presente estudio socioeconomico es veraz y fue obtenida mediante entrevista directa, 
        verificacion documental y/o investigacion de campo. Los datos aqui presentados 
        reflejan fielmente la situacion del evaluado al momento de la investigacion.
        """
        declaracion_parrafo = Paragraph(declaracion_texto.strip(), self.styles['CustomBody'])
        
        # Espacio para firma con imagen opcional
        firma_path = self.config.get("firma", "")
        nombre_investigador = inv.get("nombre_investigador", "") or self.config.get("ejecutor", "")
        
        if firma_path and os.path.exists(firma_path):
            # Crear estructura con imagen de firma sobrepuesta a la linea
            try:
                # Intentar obtener dimensiones con PIL
                try:
                    from PIL import Image as PILImage
                    with PILImage.open(firma_path) as pil_img:
                        orig_width, orig_height = pil_img.size
                        aspect_ratio = orig_width / orig_height if orig_height > 0 else 1
                        
                        # Dimensiones maximas para la firma
                        max_width = 2.0 * inch
                        max_height = 0.8 * inch
                        
                        new_width = min(max_width, orig_width * 0.5)
                        new_height = new_width / aspect_ratio
                        
                        if new_height > max_height:
                            new_height = max_height
                            new_width = new_height * aspect_ratio
                        
                        firma_img = Image(firma_path, width=new_width, height=new_height)
                except ImportError:
                    # Fallback sin PIL
                    firma_img = Image(firma_path, width=1.5*inch, height=0.6*inch)
                
                firma_img.hAlign = 'CENTER'
                
                # Tabla con firma grafica
                firma_data = [
                    [firma_img],
                    ["_" * 40],
                    ["Firma del Investigador"],
                    [nombre_investigador]
                ]
                
                tabla_firma = Table(firma_data, colWidths=[4*inch])
                tabla_firma.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 2), (0, 2), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (0, 0), 0),
                    ('BOTTOMPADDING', (0, 0), (0, 0), -10),  # Sobreponer firma a la linea
                    ('TOPPADDING', (0, 1), (-1, -1), 4),
                ]))
                
            except Exception as e:
                print(f"Error al cargar imagen de firma: {e}")
                # Fallback: usar tabla sin imagen
                firma_data = [
                    ["_" * 40],
                    ["Firma del Investigador"],
                    [nombre_investigador]
                ]
                
                tabla_firma = Table(firma_data, colWidths=[4*inch])
                tabla_firma.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 1), (0, 1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                ]))
        else:
            # Sin imagen de firma - solo linea y texto
            firma_data = [
                ["_" * 40],
                ["Firma del Investigador"],
                [nombre_investigador]
            ]
            
            tabla_firma = Table(firma_data, colWidths=[4*inch])
            tabla_firma.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 1), (0, 1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
            ]))
        
        # Centrar la tabla de firma y mantener declaracion + firma juntas
        seccion_firma = [
            declaracion_titulo,
            declaracion_parrafo,
            Spacer(1, 0.5*inch),
            tabla_firma
        ]
        elements.append(KeepTogether(seccion_firma))
        
        # Observaciones finales - manejar parrafos largos
        obs_finales = inv.get("observaciones_finales", "") or datos.get("observaciones_finales", "")
        if obs_finales:
            elements.append(Spacer(1, 0.3*inch))
            titulo_obs = Paragraph("<b>OBSERVACIONES FINALES</b>", self.styles['CustomHeading'])
            
            # Dividir por saltos de linea si existen
            parrafos_obs = obs_finales.split('\n')
            if len(parrafos_obs) == 1:
                # Sin saltos de linea, buscar separadores naturales
                import re
                parrafos_obs = re.split(r'(?<=[.!?])\s+(?=[A-Z])', obs_finales)
            
            # Filtrar parrafos vacios
            parrafos_obs = [p.strip() for p in parrafos_obs if p.strip()]
            
            if parrafos_obs:
                # Crear lista de elementos para KeepTogether
                obs_elements = [titulo_obs]
                for parrafo in parrafos_obs:
                    obs_elements.append(Paragraph(parrafo, self.styles['CustomBody']))
                    obs_elements.append(Spacer(1, 0.05*inch))
                
                # Si hay pocos parrafos, mantener juntos
                if len(parrafos_obs) <= 4:
                    elements.append(KeepTogether(obs_elements))
                else:
                    # Si hay muchos, al menos mantener titulo con primer parrafo
                    elements.append(KeepTogether([titulo_obs, Paragraph(parrafos_obs[0], self.styles['CustomBody'])]))
                    for parrafo in parrafos_obs[1:]:
                        elements.append(Paragraph(parrafo, self.styles['CustomBody']))
                        elements.append(Spacer(1, 0.05*inch))
    
    def exportar(self, datos: Dict, ruta_salida: str):
        """
        Genera el PDF del estudio socioeconómico.
        
        Args:
            datos: Diccionario con todos los datos del estudio.
            ruta_salida: Ruta donde se guardará el PDF.
        """
        doc = SimpleDocTemplate(
            ruta_salida,
            pagesize=letter,
            rightMargin=0.5*inch,
            leftMargin=0.5*inch,
            topMargin=0.5*inch,
            bottomMargin=0.5*inch
        )
        
        elements = []
        
        # Crear encabezado
        self._crear_encabezado(elements, datos)
        
        # Secciones del documento
        self._crear_seccion_datos_personales(datos, elements)
        self._crear_seccion_salud(datos, elements)
        self._crear_seccion_familiar(datos, elements)
        self._crear_seccion_financiera(datos, elements)
        self._crear_seccion_empleo_actual(datos, elements)
        self._crear_seccion_estilo_vida(datos, elements)
        self._crear_seccion_vivienda(datos, elements)
        self._crear_seccion_historial_laboral(datos, elements)
        self._crear_seccion_referencias(datos, elements)
        
        # Análisis de riesgos y gráficos
        self._crear_seccion_analisis_riesgos(datos, elements)
        self._crear_graficos_riesgos(datos, elements)
        
        # Secciones institucionales
        self._crear_seccion_validacion_documental(datos, elements)
        self._crear_seccion_investigacion_vecinal(datos, elements)
        self._crear_seccion_analisis_cualitativo(datos, elements)
        self._crear_seccion_fotos(datos, elements)
        self._crear_seccion_conclusiones_firma(datos, elements)
        
        # Construir PDF
        doc.build(elements)
        
        # Limpiar archivos temporales
        for temp_file in self._temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            except Exception:
                pass
        self._temp_files.clear()
        
        return ruta_salida
