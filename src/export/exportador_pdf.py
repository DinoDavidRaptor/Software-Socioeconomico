"""
Módulo de exportación a PDF.
Autor: DINOS Tech
Versión: 0.2.0
"""

import os
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, 
    Spacer, Image, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from typing import Dict


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
    
    def _crear_encabezado(self, elements: list):
        """
        Crea el encabezado del documento con logo y datos de la empresa.
        
        Args:
            elements: Lista de elementos del documento.
        """
        # Agregar logo si existe
        logo_path = self.config.get("logo", "")
        if logo_path and os.path.exists(logo_path):
            try:
                img = Image(logo_path, width=1.5*inch, height=1.5*inch)
                img.hAlign = 'CENTER'
                elements.append(img)
                elements.append(Spacer(1, 0.2*inch))
            except:
                pass
        
        # Datos de la empresa
        empresa_data = [
            [Paragraph(f"<b>{self.config.get('nombre', 'N/A')}</b>", self.styles['CustomTitle'])],
            [Paragraph(self.config.get('direccion', ''), self.styles['Normal'])],
            [Paragraph(f"Tel: {self.config.get('telefono', '')} | Email: {self.config.get('email', '')}", 
                      self.styles['Normal'])]
        ]
        
        empresa_table = Table(empresa_data, colWidths=[6.5*inch])
        empresa_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elements.append(empresa_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Línea separadora
        line_data = [['']]
        line_table = Table(line_data, colWidths=[6.5*inch])
        line_table.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, 0), 2, colors.HexColor('#2c3e50')),
        ]))
        elements.append(line_table)
        elements.append(Spacer(1, 0.2*inch))
    
    def _crear_seccion_datos_personales(self, datos: Dict, elements: list):
        """Crea la sección de datos personales."""
        elements.append(Paragraph("DATOS PERSONALES", self.styles['CustomHeading']))
        
        dp = datos.get("datos_personales", {})
        
        datos_tabla = [
            ["Nombre Completo:", dp.get("nombre_completo", "N/A")],
            ["Edad:", str(dp.get("edad", "N/A"))],
            ["Fecha de Nacimiento:", dp.get("fecha_nacimiento", "N/A")],
            ["Género:", dp.get("genero", "N/A")],
            ["Estado Civil:", dp.get("estado_civil", "N/A")],
            ["Nacionalidad:", dp.get("nacionalidad", "N/A")],
            ["Lugar de Nacimiento:", dp.get("lugar_nacimiento", "N/A")],
            ["CURP:", dp.get("curp", "N/A")],
            ["RFC:", dp.get("rfc", "N/A")],
            ["INE:", dp.get("ine", "N/A")],
            ["NSS:", dp.get("nss", "N/A")],
            ["Teléfono:", dp.get("telefono", "N/A")],
            ["Email:", dp.get("email", "N/A")],
            ["Dirección:", dp.get("direccion", "N/A")],
            ["Escolaridad:", dp.get("escolaridad", "N/A")],
            ["Carrera/Especialidad:", dp.get("carrera_especialidad", "N/A")],
            ["Estado de Estudios:", dp.get("estado_estudios", "N/A")]
        ]
        
        # Agregar antecedentes legales si existen
        if dp.get("antecedentes_legales"):
            datos_tabla.append(["Antecedentes Legales:", dp.get("antecedentes_legales_detalle", "Sí")])
        
        # Agregar contacto de emergencia
        contactos = dp.get("contactos_emergencia", [])
        if contactos and len(contactos) > 0:
            contacto = contactos[0]
            datos_tabla.append(["Contacto de Emergencia:", 
                f"{contacto.get('nombre', 'N/A')} - {contacto.get('telefono', 'N/A')} ({contacto.get('relacion', 'N/A')})"])
        
        datos_tabla.append(["Licencia de Conducir:", "Sí" if dp.get("licencia_conducir") else "No"])
        
        if dp.get("licencia_conducir"):
            datos_tabla.append(["Tipo Licencia:", dp.get("licencia_tipo", "N/A")])
            datos_tabla.append(["Vigencia Licencia:", dp.get("licencia_vigencia", "N/A")])
        
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
        
        elements.append(tabla)
        elements.append(Spacer(1, 0.2*inch))
    
    def _crear_seccion_salud(self, datos: Dict, elements: list):
        """Crea la sección de salud e intereses."""
        elements.append(Paragraph("SALUD E INTERESES", self.styles['CustomHeading']))
        
        salud = datos.get("salud_intereses", {})
        
        # Información básica de salud
        info_salud = [
            ["Estado de Salud General:", salud.get("estado_salud", "N/A")],
            ["Tipo de Sangre:", salud.get("tipo_sangre", "N/A")],
            ["Alergias:", salud.get("alergias", "Ninguna")],
            ["Fuma:", "Sí" if salud.get("fuma") else "No"],
            ["Consume Alcohol:", "Sí" if salud.get("consume_alcohol") else "No"]
        ]
        
        # Agregar frecuencias si aplica
        if salud.get("fuma"):
            info_salud.append(["Frecuencia Tabaco:", salud.get("frecuencia_tabaco", "N/A")])
        if salud.get("consume_alcohol"):
            info_salud.append(["Frecuencia Alcohol:", salud.get("frecuencia_alcohol", "N/A")])
        
        # Otras sustancias
        if salud.get("consume_otras_sustancias"):
            info_salud.append(["Otras Sustancias:", salud.get("otras_sustancias_detalle", "Sí")])
        
        tabla_salud = Table(info_salud, colWidths=[2.5*inch, 4*inch])
        tabla_salud.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(tabla_salud)
        elements.append(Spacer(1, 0.1*inch))
        
        # Enfermedades crónicas
        enfermedades = salud.get("enfermedades_cronicas", [])
        if enfermedades and len(enfermedades) > 0:
            elements.append(Paragraph("<b>Enfermedades Crónicas:</b>", self.styles['CustomBody']))
            
            enf_data = [["Enfermedad", "Tratamiento", "Frecuencia Médico"]]
            for enf in enfermedades:
                enf_data.append([
                    enf.get("nombre", ""),
                    enf.get("tratamiento", "N/A"),
                    enf.get("frecuencia_visita_medico", "N/A")
                ])
            
            tabla_enf = Table(enf_data, colWidths=[2*inch, 2.5*inch, 2*inch])
            tabla_enf.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e74c3c')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('PADDING', (0, 0), (-1, -1), 4),
            ]))
            
            elements.append(tabla_enf)
            elements.append(Spacer(1, 0.1*inch))
        
        # Actividades e intereses
        actividades = salud.get("actividades_tiempo_libre", "")
        deportes = salud.get("deportes_practica", "")
        
        if actividades or deportes:
            intereses_text = ""
            if actividades:
                intereses_text += f"<b>Actividades de Tiempo Libre:</b> {actividades}<br/>"
            if deportes:
                intereses_text += f"<b>Deportes que Practica:</b> {deportes}"
            
            elements.append(Paragraph(intereses_text, self.styles['CustomBody']))
        
        elements.append(Spacer(1, 0.2*inch))
    
    def _crear_seccion_familiar(self, datos: Dict, elements: list):
        """Crea la sección de información familiar."""
        elements.append(Paragraph("INFORMACIÓN FAMILIAR", self.styles['CustomHeading']))
        
        fam = datos.get("informacion_familiar", {})
        
        info_general = [
            ["Número de Hijos:", str(fam.get("numero_hijos", 0))],
            ["Número de Dependientes:", str(fam.get("numero_dependientes_economicos", 0))],
            ["Personas en el Hogar:", str(fam.get("personas_hogar", 0))],
            ["Ingreso Familiar Total:", f"${fam.get('ingreso_familiar_total', 0):,.2f}"]
        ]
        
        tabla_general = Table(info_general, colWidths=[2.5*inch, 4*inch])
        tabla_general.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(tabla_general)
        elements.append(Spacer(1, 0.1*inch))
        
        # Miembros del hogar con más detalles
        miembros = fam.get("miembros_hogar", [])
        if miembros:
            elements.append(Paragraph("<b>Miembros del Hogar:</b>", self.styles['CustomBody']))
            
            miembros_data = [["Nombre", "Edad", "Parentesco", "Ocupación", "Ingreso", "¿Depende?"]]
            for m in miembros:
                miembros_data.append([
                    m.get("nombre", ""),
                    str(m.get("edad", "")),
                    m.get("parentesco", ""),
                    m.get("ocupacion", ""),
                    f"${m.get('ingreso', 0):,.2f}",
                    "Sí" if m.get("es_dependiente") else "No"
                ])
            
            tabla_miembros = Table(miembros_data, colWidths=[1.3*inch, 0.6*inch, 1*inch, 1.2*inch, 1.1*inch, 0.8*inch])
            tabla_miembros.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 7),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('PADDING', (0, 0), (-1, -1), 3),
            ]))
            
            elements.append(tabla_miembros)
            elements.append(Spacer(1, 0.1*inch))
            
            # Mostrar enfermedades de familiares si existen
            miembros_con_enfermedad = [m for m in miembros if m.get("enfermedad_cronica")]
            if miembros_con_enfermedad:
                elements.append(Paragraph("<b>Familiares con Enfermedades Crónicas:</b>", self.styles['CustomBody']))
                enf_fam_data = [["Nombre", "Enfermedad", "Tratamiento"]]
                
                for m in miembros_con_enfermedad:
                    enf_fam_data.append([
                        m.get("nombre", ""),
                        m.get("enfermedad_cronica", ""),
                        m.get("tratamiento_enfermedad", "N/A")
                    ])
                
                tabla_enf_fam = Table(enf_fam_data, colWidths=[2*inch, 2.5*inch, 2*inch])
                tabla_enf_fam.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e67e22')),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('PADDING', (0, 0), (-1, -1), 4),
                ]))
                
                elements.append(tabla_enf_fam)
        
        elements.append(Spacer(1, 0.2*inch))
    
    def _crear_seccion_financiera(self, datos: Dict, elements: list):
        """Crea la sección de situación financiera."""
        elements.append(Paragraph("SITUACIÓN FINANCIERA", self.styles['CustomHeading']))
        
        fin = datos.get("situacion_financiera", {})
        
        # Información laboral actual
        info_laboral = [
            ["Trabaja Actualmente:", "Sí" if fin.get("trabaja_actualmente", False) else "No"],
            ["Empresa:", fin.get("empresa_actual", "N/A")],
            ["Puesto:", fin.get("puesto_actual", "N/A")],
            ["Sueldo Mensual:", f"${fin.get('sueldo_mensual', 0):,.2f}"],
            ["Horario:", fin.get("horario", "N/A")]
        ]
        
        tabla_laboral = Table(info_laboral, colWidths=[2*inch, 4.5*inch])
        tabla_laboral.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(tabla_laboral)
        elements.append(Spacer(1, 0.1*inch))
        
        # Gastos mensuales
        elements.append(Paragraph("<b>Gastos Mensuales:</b>", self.styles['CustomBody']))
        
        gastos = fin.get("gastos", {})
        gastos_data = [
            ["Categoría", "Monto"],
            ["Alimentación", f"${gastos.get('alimentacion', 0):,.2f}"],
            ["Salud", f"${gastos.get('salud', 0):,.2f}"],
            ["Educación", f"${gastos.get('educacion', 0):,.2f}"],
            ["Vivienda", f"${gastos.get('vivienda', 0):,.2f}"],
            ["Transporte", f"${gastos.get('transporte', 0):,.2f}"],
            ["Servicios", f"${gastos.get('servicios', 0):,.2f}"],
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
        
        elements.append(tabla_gastos)
        elements.append(Spacer(1, 0.1*inch))
        
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
        
        # Observaciones
        if fin.get("observaciones_financieras"):
            elements.append(Spacer(1, 0.1*inch))
            elements.append(Paragraph("<b>Observaciones:</b>", self.styles['CustomBody']))
            elements.append(Paragraph(fin.get("observaciones_financieras", ""), self.styles['CustomBody']))
        
        elements.append(Spacer(1, 0.2*inch))
    
    def _crear_seccion_empleo_actual(self, datos: Dict, elements: list):
        """Crea la sección de empleo actual detallado."""
        empleo = datos.get("empleo_actual", {})
        
        # Solo mostrar si está trabajando
        if not empleo.get("tiene_empleo"):
            return
        
        elements.append(Paragraph("EMPLEO ACTUAL", self.styles['CustomHeading']))
        
        info_empleo = [
            ["Empresa:", empleo.get("empresa", "N/A")],
            ["Puesto:", empleo.get("puesto", "N/A")],
            ["Área/Departamento:", empleo.get("area_departamento", "N/A")],
            ["Antigüedad:", empleo.get("antiguedad", "N/A")],
            ["Tipo de Contrato:", empleo.get("tipo_contrato", "N/A")],
            ["Teléfono de la Empresa:", empleo.get("telefono_empresa", "N/A")],
            ["Dirección de la Empresa:", empleo.get("direccion_empresa", "N/A")],
            ["Jefe Directo:", empleo.get("nombre_jefe", "N/A")],
            ["Puesto del Jefe:", empleo.get("puesto_jefe", "N/A")]
        ]
        
        tabla_empleo = Table(info_empleo, colWidths=[2.5*inch, 4*inch])
        tabla_empleo.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(tabla_empleo)
        elements.append(Spacer(1, 0.2*inch))
    
    def _crear_seccion_estilo_vida(self, datos: Dict, elements: list):
        """Crea la sección de estilo de vida."""
        estilo = datos.get("estilo_vida", {})
        
        if not estilo:
            return
        
        elements.append(Paragraph("ESTILO DE VIDA", self.styles['CustomHeading']))
        
        info_estilo = []
        
        if estilo.get("vehiculo_propio"):
            info_estilo.append(["Vehículo Propio:", f"{estilo.get('marca_vehiculo', '')} {estilo.get('modelo_vehiculo', '')} ({estilo.get('ano_vehiculo', 'N/A')})"])
        else:
            info_estilo.append(["Vehículo Propio:", "No"])
        
        if estilo.get("viajes_ultimo_ano"):
            info_estilo.append(["Viajes en el Último Año:", estilo.get("destinos_viajes", "Sí")])
        
        if estilo.get("hobbies"):
            info_estilo.append(["Hobbies:", estilo.get("hobbies", "")])
        
        if estilo.get("pertenece_asociaciones"):
            info_estilo.append(["Asociaciones/Clubes:", estilo.get("asociaciones_detalle", "Sí")])
        
        if info_estilo:
            tabla_estilo = Table(info_estilo, colWidths=[2.5*inch, 4*inch])
            tabla_estilo.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('PADDING', (0, 0), (-1, -1), 6),
            ]))
            
            elements.append(tabla_estilo)
        
        elements.append(Spacer(1, 0.2*inch))
    
    def _crear_seccion_vivienda(self, datos: Dict, elements: list):
        """Crea la sección de vivienda."""
        elements.append(Paragraph("VIVIENDA Y PATRIMONIO", self.styles['CustomHeading']))
        
        viv = datos.get("vivienda", {})
        
        info_vivienda = [
            ["Tipo de Vivienda:", viv.get("tipo_vivienda", "N/A")],
            ["Tenencia:", viv.get("tenencia", "N/A")],
            ["Zona:", viv.get("tipo_zona", "N/A")],
            ["Materiales:", viv.get("materiales_construccion", "N/A")],
            ["Tiempo de Residencia:", viv.get("tiempo_residencia", "N/A")],
            ["Número de Cuartos:", str(viv.get("numero_cuartos", "N/A"))]
        ]
        
        tabla_viv = Table(info_vivienda, colWidths=[2*inch, 4.5*inch])
        tabla_viv.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(tabla_viv)
        elements.append(Spacer(1, 0.1*inch))
        
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
        """Crea la sección de historial laboral."""
        historial = datos.get("historial_laboral", [])
        
        if not historial:
            return
        
        elements.append(Paragraph("HISTORIAL LABORAL", self.styles['CustomHeading']))
        
        hist_data = [["Empresa", "Puesto", "Periodo", "Motivo Salida"]]
        
        for emp in historial:
            hist_data.append([
                emp.get("empresa", ""),
                emp.get("puesto", ""),
                f"{emp.get('fecha_inicio', '')} - {emp.get('fecha_fin', '')}",
                emp.get("motivo_separacion", "")
            ])
        
        tabla_hist = Table(hist_data, colWidths=[1.8*inch, 1.5*inch, 1.7*inch, 1.5*inch])
        tabla_hist.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        
        elements.append(tabla_hist)
        elements.append(Spacer(1, 0.2*inch))
    
    def _crear_seccion_referencias(self, datos: Dict, elements: list):
        """Crea la sección de referencias personales."""
        referencias = datos.get("referencias", [])
        
        if not referencias:
            return
        
        elements.append(Paragraph("REFERENCIAS PERSONALES", self.styles['CustomHeading']))
        
        ref_data = [["Nombre", "Relación", "Teléfono", "Tiempo Conocido"]]
        
        for ref in referencias:
            ref_data.append([
                ref.get("nombre", ""),
                ref.get("relacion", ""),
                ref.get("telefono", ""),
                ref.get("tiempo_conocido", "")
            ])
        
        tabla_ref = Table(ref_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        tabla_ref.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 4),
        ]))
        
        elements.append(tabla_ref)
        elements.append(Spacer(1, 0.2*inch))
    
    def _crear_seccion_riesgos(self, datos: Dict, elements: list):
        """Crea la sección de análisis de riesgos con justificaciones."""
        from src.logic.calculador_riesgos import CalculadorRiesgos
        
        elements.append(Paragraph("ANÁLISIS DE RIESGOS", self.styles['CustomHeading']))
        
        # Crear instancia del calculador
        calc = CalculadorRiesgos(datos)
        
        # Calcular todos los riesgos con justificaciones
        resultados = calc.calcular_todos_riesgos()
        
        # Tabla resumen de riesgos
        riesgos_data = [
            ["Indicador", "Nivel", "Interpretación"]
        ]
        
        categorias = [
            ("financiero", "Riesgo Financiero"),
            ("familiar", "Riesgo Familiar"),
            ("vivienda", "Riesgo Vivienda"),
            ("laboral", "Riesgo Laboral"),
            ("salud", "Riesgo Salud"),
            ("estilo_vida", "Riesgo Estilo de Vida")
        ]
        
        for key, label in categorias:
            if key in resultados:
                nivel = resultados[key]["puntaje"]
                riesgos_data.append([
                    label,
                    str(nivel),
                    CalculadorRiesgos.obtener_interpretacion_riesgo(nivel)
                ])
        
        # Agregar riesgo global con estilo destacado
        if "global" in resultados:
            riesgo_global = resultados["global"]["puntaje"]
            riesgos_data.append([
                "RIESGO GLOBAL",
                str(riesgo_global),
                CalculadorRiesgos.obtener_interpretacion_riesgo(riesgo_global)
            ])
        
        tabla_riesgos = Table(riesgos_data, colWidths=[2.5*inch, 1.5*inch, 2.5*inch])
        tabla_riesgos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#ecf0f1')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        
        elements.append(tabla_riesgos)
        elements.append(Spacer(1, 0.2*inch))
        
        # JUSTIFICACIONES DETALLADAS
        elements.append(Paragraph("JUSTIFICACIONES Y DETALLES", self.styles['CustomHeading']))
        
        for key, label in categorias:
            if key in resultados and resultados[key]["justificaciones"]:
                # Título de la categoría
                elements.append(Paragraph(f"<b>{label}:</b>", self.styles['CustomBody']))
                
                # Lista de justificaciones
                justificaciones = resultados[key]["justificaciones"]
                for just in justificaciones:
                    elements.append(Paragraph(f"• {just}", self.styles['Normal']))
                
                elements.append(Spacer(1, 0.1*inch))
        
        elements.append(Spacer(1, 0.1*inch))
    
    def _crear_seccion_conclusiones(self, datos: Dict, elements: list):
        """Crea la sección de conclusiones del evaluador."""
        conclusiones = datos.get("conclusiones", "")
        
        if not conclusiones:
            return
        
        elements.append(Paragraph("CONCLUSIONES Y RECOMENDACIONES", self.styles['CustomHeading']))
        
        # Crear un marco para las conclusiones
        conclusiones_data = [[Paragraph(conclusiones, self.styles['CustomBody'])]]
        
        tabla_conclusiones = Table(conclusiones_data, colWidths=[6.5*inch])
        tabla_conclusiones.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fffacd')),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('PADDING', (0, 0), (-1, -1), 12),
        ]))
        
        elements.append(tabla_conclusiones)
        elements.append(Spacer(1, 0.2*inch))
    
    def _crear_seccion_fotografias(self, datos: Dict, elements: list):
        """Crea la sección de fotografías."""
        fotos = datos.get("fotos", [])
        
        if not fotos:
            return
        
        elements.append(PageBreak())
        elements.append(Paragraph("EVIDENCIA FOTOGRÁFICA", self.styles['CustomHeading']))
        elements.append(Spacer(1, 0.1*inch))
        
        for foto in fotos:
            archivo = foto.get("archivo", "")
            tipo = foto.get("tipo", "Sin categoría")
            descripcion = foto.get("descripcion", "")
            
            if archivo and os.path.exists(archivo):
                try:
                    # Agregar la imagen
                    img = Image(archivo, width=4*inch, height=3*inch, kind='proportional')
                    img.hAlign = 'CENTER'
                    
                    # Pie de foto
                    pie = f"<b>{tipo}</b>"
                    if descripcion:
                        pie += f" - {descripcion}"
                    
                    foto_elementos = [
                        img,
                        Spacer(1, 0.1*inch),
                        Paragraph(pie, self.styles['CustomBody']),
                        Spacer(1, 0.2*inch)
                    ]
                    
                    elements.extend(foto_elementos)
                    
                except Exception as e:
                    print(f"Error al incluir fotografía: {e}")
    
    def exportar(self, estudio_datos: Dict, ruta_salida: str) -> bool:
        """
        Exporta un estudio socioeconómico a PDF.
        
        Args:
            estudio_datos: Diccionario con los datos del estudio.
            ruta_salida: Ruta completa del archivo PDF de salida.
            
        Returns:
            True si se exportó correctamente, False en caso contrario.
        """
        try:
            os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
            
            doc = SimpleDocTemplate(
                ruta_salida,
                pagesize=letter,
                rightMargin=0.75*inch,
                leftMargin=0.75*inch,
                topMargin=0.75*inch,
                bottomMargin=0.75*inch
            )
            
            elements = []
            
            # Crear documento
            self._crear_encabezado(elements)
            
            # Título del reporte
            nombre = estudio_datos.get("datos_personales", {}).get("nombre_completo", "Sin nombre")
            elements.append(Paragraph(
                f"ESTUDIO SOCIOECONÓMICO<br/>{nombre}",
                self.styles['CustomTitle']
            ))
            elements.append(Paragraph(
                f"Fecha de elaboración: {datetime.now().strftime('%d/%m/%Y')}",
                self.styles['Normal']
            ))
            elements.append(Spacer(1, 0.3*inch))
            
            # Secciones del reporte
            self._crear_seccion_datos_personales(estudio_datos, elements)
            self._crear_seccion_salud(estudio_datos, elements)
            self._crear_seccion_familiar(estudio_datos, elements)
            self._crear_seccion_financiera(estudio_datos, elements)
            self._crear_seccion_empleo_actual(estudio_datos, elements)
            self._crear_seccion_estilo_vida(estudio_datos, elements)
            self._crear_seccion_vivienda(estudio_datos, elements)
            self._crear_seccion_historial_laboral(estudio_datos, elements)
            self._crear_seccion_referencias(estudio_datos, elements)
            self._crear_seccion_riesgos(estudio_datos, elements)
            self._crear_seccion_conclusiones(estudio_datos, elements)
            self._crear_seccion_fotografias(estudio_datos, elements)
            
            # Generar PDF
            doc.build(elements)
            
            return True
            
        except Exception as e:
            print(f"Error al exportar PDF: {e}")
            import traceback
            traceback.print_exc()
            return False
