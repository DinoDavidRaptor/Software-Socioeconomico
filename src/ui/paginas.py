"""
Páginas del wizard de estudios socioeconómicos.
Autor: DINOS Tech
Versión: 0.3.0

Este módulo contiene todas las páginas del asistente de captura.
"""

from PyQt5.QtWidgets import (
    QWizardPage, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QSpinBox, QDoubleSpinBox, QTextEdit, QComboBox, QCheckBox,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog,
    QGroupBox, QRadioButton, QButtonGroup, QMessageBox, QScrollArea,
    QWidget, QDateEdit
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont
import os
import shutil
from datetime import datetime


class PaginaBase(QWizardPage):
    """Clase base para todas las páginas del wizard."""
    
    def __init__(self, estudio, titulo, parent=None):
        super().__init__(parent)
        self.estudio = estudio
        self.setTitle(titulo)
        self.campos = {}
    
    def guardar_datos(self):
        """Método abstracto para guardar datos. Debe ser implementado por cada página."""
        pass
    
    def cargar_datos(self):
        """Método abstracto para cargar datos. Debe ser implementado por cada página."""
        pass


class PaginaDatosPersonales(PaginaBase):
    """Página 1: Datos Personales."""
    
    def __init__(self, estudio):
        super().__init__(estudio, "Datos Personales")
        self.init_ui()
        self.cargar_datos()
    
    def init_ui(self):
        """Inicializa la interfaz."""
        layout = QFormLayout()
        self.setLayout(layout)
        
        self.setSubTitle(
            "Capture la información personal del candidato. "
            "Los campos marcados con * son obligatorios."
        )
        
        # Nombre completo
        self.campos['nombre_completo'] = QLineEdit()
        self.campos['nombre_completo'].setPlaceholderText("Nombre(s) y apellidos completos")
        layout.addRow("*Nombre Completo:", self.campos['nombre_completo'])
        self.registerField("nombre_completo*", self.campos['nombre_completo'])
        
        # Género
        self.campos['genero'] = QComboBox()
        self.campos['genero'].addItems([
            "Femenino", "Masculino", "Otro", "Prefiero no especificar"
        ])
        layout.addRow("*Género:", self.campos['genero'])
        
        # Edad
        self.campos['edad'] = QSpinBox()
        self.campos['edad'].setRange(18, 100)
        self.campos['edad'].setValue(25)
        layout.addRow("*Edad:", self.campos['edad'])
        
        # Fecha de nacimiento
        self.campos['fecha_nacimiento'] = QDateEdit()
        self.campos['fecha_nacimiento'].setCalendarPopup(True)
        self.campos['fecha_nacimiento'].setDate(QDate.currentDate().addYears(-25))
        self.campos['fecha_nacimiento'].setDisplayFormat("dd/MM/yyyy")
        layout.addRow("Fecha de Nacimiento:", self.campos['fecha_nacimiento'])
        
        # Nacionalidad
        self.campos['nacionalidad'] = QComboBox()
        self.campos['nacionalidad'].addItems([
            "Mexicana", "Estadounidense", "Colombiana", "Española", "Argentina", "Otra"
        ])
        layout.addRow("Nacionalidad:", self.campos['nacionalidad'])
        
        # Lugar de nacimiento
        self.campos['estado_nacimiento'] = QComboBox()
        self.campos['estado_nacimiento'].addItems([
            "Aguascalientes", "Baja California", "Baja California Sur", "Campeche", 
            "Chiapas", "Chihuahua", "CDMX", "Coahuila", "Colima", "Durango", 
            "Guanajuato", "Guerrero", "Hidalgo", "Jalisco", "Mexico", "Michoacán", 
            "Morelos", "Nayarit", "Nuevo León", "Oaxaca", "Puebla", "Querétaro", 
            "Quintana Roo", "San Luis Potosí", "Sinaloa", "Sonora", "Tabasco", 
            "Tamaulipas", "Tlaxcala", "Veracruz", "Yucatán", "Zacatecas"
        ])
        layout.addRow("Lugar de Nacimiento:", self.campos['estado_nacimiento'])
        
        # Estado civil
        self.campos['estado_civil'] = QComboBox()
        self.campos['estado_civil'].addItems([
            "Soltero(a)", "Casado(a)", "Unión Libre", "Divorciado(a)", "Viudo(a)"
        ])
        layout.addRow("*Estado Civil:", self.campos['estado_civil'])
        
        # CURP
        self.campos['curp'] = QLineEdit()
        self.campos['curp'].setPlaceholderText("18 caracteres")
        self.campos['curp'].setMaxLength(18)
        layout.addRow("CURP:", self.campos['curp'])
        
        # INE
        self.campos['ine'] = QLineEdit()
        self.campos['ine'].setPlaceholderText("Clave de elector")
        layout.addRow("Clave INE:", self.campos['ine'])
        
        # RFC
        self.campos['rfc'] = QLineEdit()
        self.campos['rfc'].setPlaceholderText("13 caracteres")
        self.campos['rfc'].setMaxLength(13)
        layout.addRow("RFC:", self.campos['rfc'])
        
        # NSS
        self.campos['nss'] = QLineEdit()
        self.campos['nss'].setPlaceholderText("Número de Seguridad Social")
        self.campos['nss'].setMaxLength(11)
        layout.addRow("NSS:", self.campos['nss'])
        
        # Licencia de conducir
        self.campos['licencia_conducir'] = QCheckBox("Sí tiene licencia de conducir")
        layout.addRow("Licencia de Conducir:", self.campos['licencia_conducir'])
        
        self.campos['tipo_licencia'] = QComboBox()
        self.campos['tipo_licencia'].addItems([
            "A - Motocicleta", "B - Automóvil", "C - Camión", "D - Autobús", 
            "E - Remolques", "F - Máquina pesada", "G - Especial"
        ])
        layout.addRow("Tipo de Licencia:", self.campos['tipo_licencia'])
        
        # Teléfono
        self.campos['telefono'] = QLineEdit()
        self.campos['telefono'].setPlaceholderText("10 dígitos")
        layout.addRow("*Teléfono:", self.campos['telefono'])
        self.registerField("telefono*", self.campos['telefono'])
        
        # Email
        self.campos['email'] = QLineEdit()
        self.campos['email'].setPlaceholderText("correo@ejemplo.com")
        layout.addRow("Email:", self.campos['email'])
        
        # Dirección
        self.campos['direccion'] = QTextEdit()
        self.campos['direccion'].setMaximumHeight(60)
        self.campos['direccion'].setPlaceholderText("Calle, número, colonia, CP, ciudad, estado")
        layout.addRow("*Dirección Completa:", self.campos['direccion'])
    
    def guardar_datos(self):
        """Guarda los datos en el estudio."""
        dp = self.estudio.datos['datos_personales']
        dp['nombre_completo'] = self.campos['nombre_completo'].text()
        dp['genero'] = self.campos['genero'].currentText()
        dp['edad'] = self.campos['edad'].value()
        dp['fecha_nacimiento'] = self.campos['fecha_nacimiento'].date().toString("dd/MM/yyyy")
        dp['nacionalidad'] = self.campos['nacionalidad'].currentText()
        dp['estado_nacimiento'] = self.campos['estado_nacimiento'].currentText()
        dp['estado_civil'] = self.campos['estado_civil'].currentText()
        dp['curp'] = self.campos['curp'].text()
        dp['rfc'] = self.campos['rfc'].text()
        dp['nss'] = self.campos['nss'].text()
        dp['licencia_conducir'] = self.campos['licencia_conducir'].isChecked()
        dp['licencia_tipo'] = self.campos['tipo_licencia'].currentText()
        dp['ine'] = self.campos['ine'].text()
        dp['telefono'] = self.campos['telefono'].text()
        dp['email'] = self.campos['email'].text()
        dp['direccion'] = self.campos['direccion'].toPlainText()
    
    def cargar_datos(self):
        """Carga los datos desde el estudio."""
        dp = self.estudio.datos['datos_personales']
        self.campos['nombre_completo'].setText(dp.get('nombre_completo', ''))
        
        genero = dp.get('genero', '')
        if genero:
            index = self.campos['genero'].findText(genero)
            if index >= 0:
                self.campos['genero'].setCurrentIndex(index)
        
        self.campos['edad'].setValue(dp.get('edad', 25))
        
        fecha_nac = dp.get('fecha_nacimiento', '')
        if fecha_nac:
            try:
                fecha = QDate.fromString(fecha_nac, "dd/MM/yyyy")
                self.campos['fecha_nacimiento'].setDate(fecha)
            except:
                pass
        
        nacionalidad = dp.get('nacionalidad', '')
        if nacionalidad:
            index = self.campos['nacionalidad'].findText(nacionalidad)
            if index >= 0:
                self.campos['nacionalidad'].setCurrentIndex(index)
        
        estado_nacimiento = dp.get('estado_nacimiento', '')
        if estado_nacimiento:
            index = self.campos['estado_nacimiento'].findText(estado_nacimiento)
            if index >= 0:
                self.campos['estado_nacimiento'].setCurrentIndex(index)
        
        estado_civil = dp.get('estado_civil', '')
        if estado_civil:
            index = self.campos['estado_civil'].findText(estado_civil)
            if index >= 0:
                self.campos['estado_civil'].setCurrentIndex(index)
        
        self.campos['curp'].setText(dp.get('curp', ''))
        self.campos['rfc'].setText(dp.get('rfc', ''))
        self.campos['nss'].setText(dp.get('nss', ''))
        self.campos['licencia_conducir'].setChecked(dp.get('licencia_conducir', False))
        
        licencia_tipo = dp.get('licencia_tipo', '')
        if licencia_tipo:
            index = self.campos['tipo_licencia'].findText(licencia_tipo)
            if index >= 0:
                self.campos['tipo_licencia'].setCurrentIndex(index)
        
        self.campos['ine'].setText(dp.get('ine', ''))
        self.campos['telefono'].setText(dp.get('telefono', ''))
        self.campos['email'].setText(dp.get('email', ''))
        self.campos['direccion'].setPlainText(dp.get('direccion', ''))


class PaginaSaludIntereses(PaginaBase):
    """Página 2: Salud e Intereses."""
    
    def __init__(self, estudio):
        super().__init__(estudio, "Salud e Intereses Personales")
        self.init_ui()
        self.cargar_datos()
    
    def init_ui(self):
        """Inicializa la interfaz."""
        layout = QFormLayout()
        self.setLayout(layout)
        
        self.setSubTitle(
            "Esta sección ayuda a conocer mejor al candidato. "
            "Las preguntas están diseñadas para generar confianza y obtener un perfil completo."
        )
        
        # Padecimientos
        layout.addRow(QLabel("<b>Información de Salud:</b>"))
        self.campos['padecimientos'] = QTextEdit()
        self.campos['padecimientos'].setMaximumHeight(60)
        self.campos['padecimientos'].setPlaceholderText(
            "¿Padece alguna enfermedad o condición de salud actual? "
            "(Diabetes, hipertensión, alergias, etc.)"
        )
        layout.addRow("Padecimientos:", self.campos['padecimientos'])
        
        # Seguro médico
        self.campos['seguro_medico'] = QComboBox()
        self.campos['seguro_medico'].addItems([
            "No tiene", "IMSS", "ISSSTE", "Seguro Privado", "Seguro Popular/INSABI", "Otro"
        ])
        layout.addRow("Seguro Médico:", self.campos['seguro_medico'])
        
        layout.addRow(QLabel(""))  # Espacio
        
        # Intereses personales
        layout.addRow(QLabel("<b>Intereses y Metas:</b>"))
        
        self.campos['hobbies'] = QTextEdit()
        self.campos['hobbies'].setMaximumHeight(60)
        self.campos['hobbies'].setPlaceholderText(
            "Deportes, lectura, música, pasatiempos, etc."
        )
        layout.addRow("¿Qué hace en su tiempo libre?", self.campos['hobbies'])
        
        # Agregar nota de ayuda
        nota = QLabel("💡 Esta pregunta ayuda a conocer los intereses del candidato y crear rapport.")
        nota.setStyleSheet("color: #666; font-size: 9px; font-style: italic;")
        layout.addRow("", nota)
        
        self.campos['metas_corto_plazo'] = QTextEdit()
        self.campos['metas_corto_plazo'].setMaximumHeight(60)
        self.campos['metas_corto_plazo'].setPlaceholderText(
            "Objetivos para los próximos 1-2 años"
        )
        layout.addRow("Metas a Corto Plazo:", self.campos['metas_corto_plazo'])
        
        self.campos['metas_largo_plazo'] = QTextEdit()
        self.campos['metas_largo_plazo'].setMaximumHeight(60)
        self.campos['metas_largo_plazo'].setPlaceholderText(
            "Objetivos a 5+ años"
        )
        layout.addRow("Metas a Largo Plazo:", self.campos['metas_largo_plazo'])
    
    def guardar_datos(self):
        """Guarda los datos en el estudio."""
        si = self.estudio.datos['salud_intereses']
        si['padecimientos'] = self.campos['padecimientos'].toPlainText()
        si['seguro_medico'] = self.campos['seguro_medico'].currentText()
        si['hobbies'] = self.campos['hobbies'].toPlainText()
        si['metas_corto_plazo'] = self.campos['metas_corto_plazo'].toPlainText()
        si['metas_largo_plazo'] = self.campos['metas_largo_plazo'].toPlainText()
    
    def cargar_datos(self):
        """Carga los datos desde el estudio."""
        si = self.estudio.datos['salud_intereses']
        self.campos['padecimientos'].setPlainText(si.get('padecimientos', ''))
        
        seguro = si.get('seguro_medico', '')
        if seguro:
            index = self.campos['seguro_medico'].findText(seguro)
            if index >= 0:
                self.campos['seguro_medico'].setCurrentIndex(index)
        
        self.campos['hobbies'].setPlainText(si.get('hobbies', ''))
        self.campos['metas_corto_plazo'].setPlainText(si.get('metas_corto_plazo', ''))
        self.campos['metas_largo_plazo'].setPlainText(si.get('metas_largo_plazo', ''))


class PaginaInformacionFamiliar(PaginaBase):
    """Página 3: Información Familiar."""
    
    def __init__(self, estudio):
        super().__init__(estudio, "Información Familiar")
        self.init_ui()
        self.cargar_datos()
    
    def init_ui(self):
        """Inicializa la interfaz."""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        self.setSubTitle("Información sobre la composición familiar y dependientes económicos.")
        
        # Información general
        form_layout = QFormLayout()
        
        self.campos['numero_hijos'] = QSpinBox()
        self.campos['numero_hijos'].setRange(0, 20)
        form_layout.addRow("Número de Hijos:", self.campos['numero_hijos'])
        
        self.campos['numero_hijos_estudiando'] = QSpinBox()
        self.campos['numero_hijos_estudiando'].setRange(0, 20)
        form_layout.addRow("Hijos Estudiando:", self.campos['numero_hijos_estudiando'])
        
        self.campos['gasto_mensual_educacion_hijos'] = QDoubleSpinBox()
        self.campos['gasto_mensual_educacion_hijos'].setRange(0, 999999)
        self.campos['gasto_mensual_educacion_hijos'].setPrefix("$ ")
        self.campos['gasto_mensual_educacion_hijos'].setDecimals(2)
        form_layout.addRow("Gasto Mensual Educación Hijos:", self.campos['gasto_mensual_educacion_hijos'])
        
        main_layout.addLayout(form_layout)
        
        # Tabla de miembros del hogar
        main_layout.addWidget(QLabel("<b>Miembros del Hogar:</b>"))
        
        self.tabla_miembros = QTableWidget()
        self.tabla_miembros.setColumnCount(6)
        self.tabla_miembros.setHorizontalHeaderLabels([
            "Nombre", "Edad", "Parentesco", "Ocupación", "Ingreso Mensual", "¿Depende?"
        ])
        self.tabla_miembros.setColumnWidth(0, 130)
        self.tabla_miembros.setColumnWidth(1, 50)
        self.tabla_miembros.setColumnWidth(2, 100)
        self.tabla_miembros.setColumnWidth(3, 130)
        self.tabla_miembros.setColumnWidth(4, 100)
        self.tabla_miembros.setColumnWidth(5, 70)
        
        main_layout.addWidget(self.tabla_miembros)
        
        # Botones para la tabla
        botones_layout = QHBoxLayout()
        
        btn_agregar = QPushButton("Agregar Miembro")
        btn_agregar.clicked.connect(self.agregar_miembro)
        botones_layout.addWidget(btn_agregar)
        
        btn_eliminar = QPushButton("Eliminar Seleccionado")
        btn_eliminar.clicked.connect(self.eliminar_miembro)
        botones_layout.addWidget(btn_eliminar)
        
        botones_layout.addStretch()
        
        main_layout.addLayout(botones_layout)
        
        # Ingreso familiar total (calculado)
        total_layout = QHBoxLayout()
        total_layout.addWidget(QLabel("<b>Ingreso Familiar Total:</b>"))
        self.campos['ingreso_familiar_total'] = QLabel("$0.00")
        self.campos['ingreso_familiar_total'].setStyleSheet("font-size: 14px; color: green;")
        total_layout.addWidget(self.campos['ingreso_familiar_total'])
        total_layout.addStretch()
        
        main_layout.addLayout(total_layout)
        
        # Conectar señal para recalcular total
        self.tabla_miembros.cellChanged.connect(self.calcular_ingreso_total)
    
    def agregar_miembro(self):
        """Agrega una fila a la tabla de miembros."""
        row = self.tabla_miembros.rowCount()
        self.tabla_miembros.insertRow(row)
        
        # Agregar items editables para las primeras 5 columnas
        for col in range(5):
            self.tabla_miembros.setItem(row, col, QTableWidgetItem(""))
        
        # Columna 5: Checkbox para dependencia
        checkbox = QCheckBox()
        checkbox.setChecked(True)  # Por defecto asume que depende
        self.tabla_miembros.setCellWidget(row, 5, checkbox)
    
    def eliminar_miembro(self):
        """Elimina la fila seleccionada."""
        row = self.tabla_miembros.currentRow()
        if row >= 0:
            self.tabla_miembros.removeRow(row)
            self.calcular_ingreso_total()
    
    def calcular_ingreso_total(self):
        """Calcula y muestra el ingreso familiar total."""
        total = 0.0
        for row in range(self.tabla_miembros.rowCount()):
            ingreso_item = self.tabla_miembros.item(row, 4)
            if ingreso_item:
                try:
                    ingreso = float(ingreso_item.text().replace(',', '').replace('$', ''))
                    total += ingreso
                except:
                    pass
        
        self.campos['ingreso_familiar_total'].setText(f"${total:,.2f}")
    
    def guardar_datos(self):
        """Guarda los datos en el estudio."""
        fam = self.estudio.datos['informacion_familiar']
        fam['numero_hijos'] = self.campos['numero_hijos'].value()
        fam['numero_hijos_estudiando'] = self.campos['numero_hijos_estudiando'].value()
        fam['gasto_mensual_educacion_hijos'] = self.campos['gasto_mensual_educacion_hijos'].value()
        
        # Guardar miembros
        miembros = []
        for row in range(self.tabla_miembros.rowCount()):
            nombre = self.tabla_miembros.item(row, 0).text() if self.tabla_miembros.item(row, 0) else ""
            edad_str = self.tabla_miembros.item(row, 1).text() if self.tabla_miembros.item(row, 1) else "0"
            parentesco = self.tabla_miembros.item(row, 2).text() if self.tabla_miembros.item(row, 2) else ""
            ocupacion = self.tabla_miembros.item(row, 3).text() if self.tabla_miembros.item(row, 3) else ""
            ingreso_str = self.tabla_miembros.item(row, 4).text() if self.tabla_miembros.item(row, 4) else "0"
            
            # Obtener checkbox de dependencia
            checkbox = self.tabla_miembros.cellWidget(row, 5)
            es_dependiente = checkbox.isChecked() if checkbox else True
            
            try:
                edad = int(edad_str)
            except:
                edad = 0
            
            try:
                ingreso = float(ingreso_str.replace(',', '').replace('$', ''))
            except:
                ingreso = 0.0
            
            if nombre:  # Solo guardar si tiene nombre
                miembros.append({
                    "nombre": nombre,
                    "edad": edad,
                    "parentesco": parentesco,
                    "ocupacion": ocupacion,
                    "ingreso": ingreso,
                    "es_dependiente": es_dependiente
                })
        
        fam['miembros_hogar'] = miembros
        
        # Calcular ingreso total
        total = sum(m['ingreso'] for m in miembros)
        fam['ingreso_familiar_total'] = total
    
    def cargar_datos(self):
        """Carga los datos desde el estudio."""
        fam = self.estudio.datos['informacion_familiar']
        self.campos['numero_hijos'].setValue(fam.get('numero_hijos', 0))
        self.campos['numero_hijos_estudiando'].setValue(fam.get('numero_hijos_estudiando', 0))
        self.campos['gasto_mensual_educacion_hijos'].setValue(fam.get('gasto_mensual_educacion_hijos', 0))
        
        # Cargar miembros
        miembros = fam.get('miembros_hogar', [])
        self.tabla_miembros.setRowCount(0)
        
        for miembro in miembros:
            row = self.tabla_miembros.rowCount()
            self.tabla_miembros.insertRow(row)
            
            self.tabla_miembros.setItem(row, 0, QTableWidgetItem(miembro.get('nombre', '')))
            self.tabla_miembros.setItem(row, 1, QTableWidgetItem(str(miembro.get('edad', ''))))
            self.tabla_miembros.setItem(row, 2, QTableWidgetItem(miembro.get('parentesco', '')))
            self.tabla_miembros.setItem(row, 3, QTableWidgetItem(miembro.get('ocupacion', '')))
            self.tabla_miembros.setItem(row, 4, QTableWidgetItem(f"{miembro.get('ingreso', 0):.2f}"))
            
            # Cargar checkbox de dependencia
            checkbox = QCheckBox()
            checkbox.setChecked(miembro.get('es_dependiente', True))
            self.tabla_miembros.setCellWidget(row, 5, checkbox)
        
        self.calcular_ingreso_total()


# Importar las páginas restantes
from src.ui.paginas_parte2 import PaginaSituacionFinanciera, PaginaVivienda


class PaginaHistorialLaboral(PaginaBase):
    """Página 6: Historial Laboral."""
    
    def __init__(self, estudio):
        super().__init__(estudio, "Historial Laboral")
        self.init_ui()
        self.cargar_datos()
    
    def init_ui(self):
        """Inicializa la interfaz."""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        self.setSubTitle(
            "Registro de empleos anteriores. "
            "Recuerde avisar al candidato que se contactarán referencias laborales."
        )
        
        # Tabla de empleos
        self.tabla_empleos = QTableWidget()
        self.tabla_empleos.setColumnCount(6)
        self.tabla_empleos.setHorizontalHeaderLabels([
            "Empresa", "Puesto", "Duración (meses)", "Salario", "Jefe/Contacto", "Motivo Salida"
        ])
        self.tabla_empleos.setColumnWidth(0, 140)
        self.tabla_empleos.setColumnWidth(1, 120)
        self.tabla_empleos.setColumnWidth(2, 110)
        self.tabla_empleos.setColumnWidth(3, 90)
        self.tabla_empleos.setColumnWidth(4, 140)
        self.tabla_empleos.setColumnWidth(5, 160)
        
        main_layout.addWidget(self.tabla_empleos)
        
        # Botones
        botones_layout = QHBoxLayout()
        
        btn_agregar = QPushButton("Agregar Empleo")
        btn_agregar.clicked.connect(self.agregar_empleo)
        botones_layout.addWidget(btn_agregar)
        
        btn_eliminar = QPushButton("Eliminar Seleccionado")
        btn_eliminar.clicked.connect(self.eliminar_empleo)
        botones_layout.addWidget(btn_eliminar)
        
        botones_layout.addStretch()
        
        main_layout.addLayout(botones_layout)
    
    def agregar_empleo(self):
        """Agrega una fila a la tabla."""
        row = self.tabla_empleos.rowCount()
        self.tabla_empleos.insertRow(row)
        for col in range(6):
            self.tabla_empleos.setItem(row, col, QTableWidgetItem(""))
    
    def eliminar_empleo(self):
        """Elimina la fila seleccionada."""
        row = self.tabla_empleos.currentRow()
        if row >= 0:
            self.tabla_empleos.removeRow(row)
    
    def guardar_datos(self):
        """Guarda los datos en el estudio."""
        empleos = []
        for row in range(self.tabla_empleos.rowCount()):
            empresa = self.tabla_empleos.item(row, 0).text() if self.tabla_empleos.item(row, 0) else ""
            if empresa:
                duracion_texto = self.tabla_empleos.item(row, 2).text() if self.tabla_empleos.item(row, 2) else "0"
                try:
                    duracion_meses = int(duracion_texto) if duracion_texto else 0
                except ValueError:
                    duracion_meses = 0
                
                salario_texto = self.tabla_empleos.item(row, 3).text() if self.tabla_empleos.item(row, 3) else "0"
                try:
                    salario = float(salario_texto.replace(',', '')) if salario_texto else 0.0
                except ValueError:
                    salario = 0.0
                
                empleos.append({
                    "empresa": empresa,
                    "puesto": self.tabla_empleos.item(row, 1).text() if self.tabla_empleos.item(row, 1) else "",
                    "duracion_meses": duracion_meses,
                    "salario": salario,
                    "jefe_nombre": self.tabla_empleos.item(row, 4).text() if self.tabla_empleos.item(row, 4) else "",
                    "motivo_separacion": self.tabla_empleos.item(row, 5).text() if self.tabla_empleos.item(row, 5) else "",
                    "fecha_inicio": "",
                    "fecha_fin": ""
                })
        
        self.estudio.datos['historial_laboral'] = empleos
    
    def cargar_datos(self):
        """Carga los datos desde el estudio."""
        empleos = self.estudio.datos.get('historial_laboral', [])
        self.tabla_empleos.setRowCount(0)
        
        for empleo in empleos:
            row = self.tabla_empleos.rowCount()
            self.tabla_empleos.insertRow(row)
            
            self.tabla_empleos.setItem(row, 0, QTableWidgetItem(empleo.get('empresa', '')))
            self.tabla_empleos.setItem(row, 1, QTableWidgetItem(empleo.get('puesto', '')))
            self.tabla_empleos.setItem(row, 2, QTableWidgetItem(str(empleo.get('duracion_meses', 0))))
            self.tabla_empleos.setItem(row, 3, QTableWidgetItem(str(empleo.get('salario', 0))))
            self.tabla_empleos.setItem(row, 4, QTableWidgetItem(empleo.get('jefe_nombre', '')))
            self.tabla_empleos.setItem(row, 5, QTableWidgetItem(empleo.get('motivo_separacion', '')))


class PaginaReferencias(PaginaBase):
    """Página 7: Referencias Personales."""
    
    def __init__(self, estudio):
        super().__init__(estudio, "Referencias Personales")
        self.init_ui()
        self.cargar_datos()
    
    def init_ui(self):
        """Inicializa la interfaz."""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        self.setSubTitle(
            "Capture al menos dos referencias personales o laborales que puedan dar opinión del candidato."
        )
        
        # Tabla de referencias
        self.tabla_referencias = QTableWidget()
        self.tabla_referencias.setColumnCount(5)
        self.tabla_referencias.setHorizontalHeaderLabels([
            "Nombre", "Relación", "Teléfono", "Ocupación", "Meses de Conocer"
        ])
        self.tabla_referencias.setColumnWidth(0, 150)
        self.tabla_referencias.setColumnWidth(1, 120)
        self.tabla_referencias.setColumnWidth(2, 110)
        self.tabla_referencias.setColumnWidth(3, 140)
        self.tabla_referencias.setColumnWidth(4, 130)
        
        main_layout.addWidget(self.tabla_referencias)
        
        # Botones
        botones_layout = QHBoxLayout()
        
        btn_agregar = QPushButton("Agregar Referencia")
        btn_agregar.clicked.connect(self.agregar_referencia)
        botones_layout.addWidget(btn_agregar)
        
        btn_eliminar = QPushButton("Eliminar Seleccionada")
        btn_eliminar.clicked.connect(self.eliminar_referencia)
        botones_layout.addWidget(btn_eliminar)
        
        botones_layout.addStretch()
        
        main_layout.addLayout(botones_layout)
        
        # Nota de ayuda
        nota = QLabel("💡 Se recomienda verificar las referencias antes de finalizar el estudio.")
        nota.setStyleSheet("color: #666; font-style: italic; margin-top: 10px;")
        main_layout.addWidget(nota)
    
    def agregar_referencia(self):
        """Agrega una fila a la tabla."""
        row = self.tabla_referencias.rowCount()
        self.tabla_referencias.insertRow(row)
        for col in range(5):
            self.tabla_referencias.setItem(row, col, QTableWidgetItem(""))
    
    def eliminar_referencia(self):
        """Elimina la fila seleccionada."""
        row = self.tabla_referencias.currentRow()
        if row >= 0:
            self.tabla_referencias.removeRow(row)
    
    def guardar_datos(self):
        """Guarda los datos en el estudio."""
        referencias = []
        for row in range(self.tabla_referencias.rowCount()):
            nombre = self.tabla_referencias.item(row, 0).text() if self.tabla_referencias.item(row, 0) else ""
            if nombre:
                meses_texto = self.tabla_referencias.item(row, 4).text() if self.tabla_referencias.item(row, 4) else "0"
                try:
                    meses = int(meses_texto) if meses_texto else 0
                except ValueError:
                    meses = 0
                
                referencias.append({
                    "nombre": nombre,
                    "relacion": self.tabla_referencias.item(row, 1).text() if self.tabla_referencias.item(row, 1) else "",
                    "telefono": self.tabla_referencias.item(row, 2).text() if self.tabla_referencias.item(row, 2) else "",
                    "ocupacion": self.tabla_referencias.item(row, 3).text() if self.tabla_referencias.item(row, 3) else "",
                    "tiempo_conocerse_meses": meses,
                    "domicilio_empresa": "",
                    "tiempo_conocido": f"{meses} meses"
                })
        
        self.estudio.datos['referencias'] = referencias
    
    def cargar_datos(self):
        """Carga los datos desde el estudio."""
        referencias = self.estudio.datos.get('referencias', [])
        self.tabla_referencias.setRowCount(0)
        
        for ref in referencias:
            row = self.tabla_referencias.rowCount()
            self.tabla_referencias.insertRow(row)
            
            self.tabla_referencias.setItem(row, 0, QTableWidgetItem(ref.get('nombre', '')))
            self.tabla_referencias.setItem(row, 1, QTableWidgetItem(ref.get('relacion', '')))
            self.tabla_referencias.setItem(row, 2, QTableWidgetItem(ref.get('telefono', '')))
            self.tabla_referencias.setItem(row, 3, QTableWidgetItem(ref.get('ocupacion', '')))
            self.tabla_referencias.setItem(row, 4, QTableWidgetItem(str(ref.get('tiempo_conocerse_meses', 0))))


class PaginaConclusiones(PaginaBase):
    """Página 8: Conclusiones del Evaluador."""
    
    def __init__(self, estudio):
        super().__init__(estudio, "Conclusiones y Recomendaciones")
        self.init_ui()
        self.cargar_datos()
    
    def init_ui(self):
        """Inicializa la interfaz."""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        self.setSubTitle(
            "Escriba su evaluación profesional, conclusiones y recomendaciones basadas en toda la información recopilada."
        )
        
        layout.addWidget(QLabel(
            "<b>Conclusiones del Evaluador:</b><br/>"
            "Incluya su análisis sobre la viabilidad del candidato, fortalezas, áreas de riesgo y recomendaciones."
        ))
        
        self.campos['conclusiones'] = QTextEdit()
        self.campos['conclusiones'].setPlaceholderText(
            "Basándome en la información recopilada...\n\n"
            "Fortalezas:\n- \n\n"
            "Áreas de atención:\n- \n\n"
            "Recomendación: ..."
        )
        layout.addWidget(self.campos['conclusiones'])
    
    def guardar_datos(self):
        """Guarda los datos en el estudio."""
        self.estudio.datos['conclusiones'] = self.campos['conclusiones'].toPlainText()
    
    def cargar_datos(self):
        """Carga los datos desde el estudio."""
        self.campos['conclusiones'].setPlainText(self.estudio.datos.get('conclusiones', ''))


class PaginaFotografias(PaginaBase):
    """Página 9: Fotografías."""
    
    def __init__(self, estudio):
        super().__init__(estudio, "Evidencia Fotográfica")
        self.init_ui()
        self.cargar_datos()
    
    def init_ui(self):
        """Inicializa la interfaz."""
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        self.setSubTitle(
            "Adjunte fotografías de la vivienda, entorno, etc. "
            "Las imágenes se incluirán en los reportes generados."
        )
        
        # Tabla de fotos
        self.tabla_fotos = QTableWidget()
        self.tabla_fotos.setColumnCount(3)
        self.tabla_fotos.setHorizontalHeaderLabels(["Archivo", "Categoría", "Descripción"])
        self.tabla_fotos.setColumnWidth(0, 300)
        self.tabla_fotos.setColumnWidth(1, 150)
        self.tabla_fotos.setColumnWidth(2, 250)
        
        main_layout.addWidget(self.tabla_fotos)
        
        # Botones
        botones_layout = QHBoxLayout()
        
        btn_agregar = QPushButton("Agregar Fotografía")
        btn_agregar.setStyleSheet("background-color: #27ae60; color: white; padding: 8px 16px;")
        btn_agregar.clicked.connect(self.agregar_fotografia)
        botones_layout.addWidget(btn_agregar)
        
        btn_eliminar = QPushButton("Eliminar Seleccionada")
        btn_eliminar.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px 16px;")
        btn_eliminar.clicked.connect(self.eliminar_fotografia)
        botones_layout.addWidget(btn_eliminar)
        
        botones_layout.addStretch()
        
        main_layout.addLayout(botones_layout)
        
        # Nota
        nota = QLabel("Formatos soportados: JPG, PNG, BMP")
        nota.setStyleSheet("color: #666; font-style: italic;")
        main_layout.addWidget(nota)
    
    def agregar_fotografia(self):
        """Permite seleccionar y agregar una fotografía."""
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar Fotografía",
            "",
            "Imágenes (*.jpg *.jpeg *.png *.bmp)"
        )
        
        if archivo:
            carpeta_fotos = "data/fotos"
            os.makedirs(carpeta_fotos, exist_ok=True)
            
            nombre_archivo = f"{self.estudio.id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{os.path.basename(archivo)}"
            ruta_destino = os.path.join(carpeta_fotos, nombre_archivo)
            
            try:
                shutil.copy2(archivo, ruta_destino)
                
                row = self.tabla_fotos.rowCount()
                self.tabla_fotos.insertRow(row)
                
                self.tabla_fotos.setItem(row, 0, QTableWidgetItem(ruta_destino))
                
                combo_cat = QComboBox()
                combo_cat.addItems(["Fachada", "Interior", "Entorno", "Cocina", "Baño", "Otro"])
                self.tabla_fotos.setCellWidget(row, 1, combo_cat)
                
                self.tabla_fotos.setItem(row, 2, QTableWidgetItem(""))
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo copiar la imagen: {e}")
    
    def eliminar_fotografia(self):
        """Elimina la fotografía seleccionada."""
        row = self.tabla_fotos.currentRow()
        if row >= 0:
            archivo_item = self.tabla_fotos.item(row, 0)
            if archivo_item:
                archivo = archivo_item.text()
                respuesta = QMessageBox.question(
                    self,
                    "Confirmar",
                    "¿Desea eliminar también el archivo de imagen del disco?",
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if respuesta == QMessageBox.Yes and os.path.exists(archivo):
                    try:
                        os.remove(archivo)
                    except:
                        pass
            
            self.tabla_fotos.removeRow(row)
    
    def guardar_datos(self):
        """Guarda los datos en el estudio."""
        fotos = []
        for row in range(self.tabla_fotos.rowCount()):
            archivo_item = self.tabla_fotos.item(row, 0)
            if archivo_item:
                archivo = archivo_item.text()
                
                combo_widget = self.tabla_fotos.cellWidget(row, 1)
                categoria = combo_widget.currentText() if combo_widget else "Sin categoría"
                
                desc_item = self.tabla_fotos.item(row, 2)
                descripcion = desc_item.text() if desc_item else ""
                
                fotos.append({
                    "archivo": archivo,
                    "tipo": categoria,
                    "descripcion": descripcion
                })
        
        self.estudio.datos['fotos'] = fotos
    
    def cargar_datos(self):
        """Carga los datos desde el estudio."""
        fotos = self.estudio.datos.get('fotos', [])
        self.tabla_fotos.setRowCount(0)
        
        for foto in fotos:
            row = self.tabla_fotos.rowCount()
            self.tabla_fotos.insertRow(row)
            
            self.tabla_fotos.setItem(row, 0, QTableWidgetItem(foto.get('archivo', '')))
            
            combo_cat = QComboBox()
            combo_cat.addItems(["Fachada", "Interior", "Entorno", "Cocina", "Baño", "Otro"])
            tipo = foto.get('tipo', '')
            if tipo:
                idx = combo_cat.findText(tipo)
                if idx >= 0:
                    combo_cat.setCurrentIndex(idx)
            self.tabla_fotos.setCellWidget(row, 1, combo_cat)
            
            self.tabla_fotos.setItem(row, 2, QTableWidgetItem(foto.get('descripcion', '')))
