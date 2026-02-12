"""
Páginas del wizard - Parte 2
Continúa las clases de páginas para el asistente.
Autor: DINOS Tech
Versión: 0.3.0
"""

from PyQt5.QtWidgets import (
    QWizardPage, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit,
    QSpinBox, QDoubleSpinBox, QTextEdit, QComboBox, QCheckBox,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem, QFileDialog,
    QGroupBox, QMessageBox, QScrollArea, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import os
import shutil
from datetime import datetime


class PaginaSituacionFinanciera(QWizardPage):
    """Página 4: Situación Financiera."""
    
    def __init__(self, estudio):
        super().__init__()
        self.estudio = estudio
        self.setTitle("Situación Financiera")
        self.init_ui()
        self.cargar_datos()
    
    def init_ui(self):
        """Inicializa la interfaz."""
        # Usar scroll area para todo el contenido
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        
        content_widget = QWidget()
        main_layout = QVBoxLayout()
        content_widget.setLayout(main_layout)
        
        self.setSubTitle("Información laboral, ingresos, gastos, préstamos y deudas del candidato.")
        
        # Empleo actual
        grupo_empleo = QGroupBox("Empleo Actual")
        empleo_layout = QFormLayout()
        
        self.campos = {}
        
        self.campos['trabaja_actualmente'] = QCheckBox("Actualmente empleado")
        self.campos['trabaja_actualmente'].setChecked(True)
        empleo_layout.addRow(self.campos['trabaja_actualmente'])
        
        self.campos['empresa_actual'] = QLineEdit()
        empleo_layout.addRow("Empresa:", self.campos['empresa_actual'])
        
        self.campos['puesto_actual'] = QLineEdit()
        empleo_layout.addRow("Puesto:", self.campos['puesto_actual'])
        
        self.campos['sueldo_mensual'] = QDoubleSpinBox()
        self.campos['sueldo_mensual'].setRange(0, 999999)
        self.campos['sueldo_mensual'].setPrefix("$ ")
        self.campos['sueldo_mensual'].setDecimals(2)
        empleo_layout.addRow("*Sueldo Mensual:", self.campos['sueldo_mensual'])
        
        self.campos['horario'] = QLineEdit()
        self.campos['horario'].setPlaceholderText("Ej: Lunes a Viernes 9:00-18:00")
        empleo_layout.addRow("Horario:", self.campos['horario'])
        
        grupo_empleo.setLayout(empleo_layout)
        main_layout.addWidget(grupo_empleo)
        
        # Gastos mensuales
        grupo_gastos = QGroupBox("Gastos Mensuales")
        gastos_layout = QFormLayout()
        
        categorias_gastos = [
            ('alimentacion', 'Alimentación'),
            ('salud', 'Salud'),
            ('educacion', 'Educación'),
            ('recreacion', 'Recreación y entretenimiento'),
            ('vivienda', 'Vivienda (renta/mantenimiento)'),
            ('transporte', 'Transporte'),
            ('servicios', 'Servicios (luz, agua, gas, etc.)'),
            ('otros', 'Otros gastos')
        ]
        
        for key, label in categorias_gastos:
            campo = QDoubleSpinBox()
            campo.setRange(0, 999999)
            campo.setPrefix("$ ")
            campo.setDecimals(2)
            campo.valueChanged.connect(self.calcular_totales)
            self.campos[f'gasto_{key}'] = campo
            gastos_layout.addRow(f"{label}:", campo)
        
        # Total de gastos
        self.campos['total_gastos'] = QLabel("$0.00")
        self.campos['total_gastos'].setStyleSheet("font-weight: bold; font-size: 13px;")
        gastos_layout.addRow("<b>Total de Gastos:</b>", self.campos['total_gastos'])
        
        grupo_gastos.setLayout(gastos_layout)
        main_layout.addWidget(grupo_gastos)
        
        # Préstamos y Deudas
        grupo_prestamos = QGroupBox("Préstamos y Deudas")
        prestamos_layout = QFormLayout()
        
        self.campos['tiene_prestamos_personales'] = QCheckBox("Sí tiene préstamos personales")
        prestamos_layout.addRow("Préstamos Personales:", self.campos['tiene_prestamos_personales'])
        
        self.campos['monto_prestamos_personales'] = QDoubleSpinBox()
        self.campos['monto_prestamos_personales'].setRange(0, 99999999)
        self.campos['monto_prestamos_personales'].setPrefix("$ ")
        self.campos['monto_prestamos_personales'].setDecimals(2)
        prestamos_layout.addRow("Monto Préstamos Personales:", self.campos['monto_prestamos_personales'])
        
        self.campos['tiene_prestamo_hipotecario'] = QCheckBox("Sí tiene hipoteca")
        prestamos_layout.addRow("Hipoteca:", self.campos['tiene_prestamo_hipotecario'])
        
        self.campos['monto_hipoteca'] = QDoubleSpinBox()
        self.campos['monto_hipoteca'].setRange(0, 99999999)
        self.campos['monto_hipoteca'].setPrefix("$ ")
        self.campos['monto_hipoteca'].setDecimals(2)
        prestamos_layout.addRow("Monto Hipoteca:", self.campos['monto_hipoteca'])
        
        self.campos['pago_mensual_hipoteca'] = QDoubleSpinBox()
        self.campos['pago_mensual_hipoteca'].setRange(0, 999999)
        self.campos['pago_mensual_hipoteca'].setPrefix("$ ")
        self.campos['pago_mensual_hipoteca'].setDecimals(2)
        prestamos_layout.addRow("Pago Mensual Hipoteca:", self.campos['pago_mensual_hipoteca'])
        
        self.campos['tiene_prestamo_auto'] = QCheckBox("Sí tiene préstamo de auto")
        prestamos_layout.addRow("Préstamo de Auto:", self.campos['tiene_prestamo_auto'])
        
        self.campos['monto_prestamo_auto'] = QDoubleSpinBox()
        self.campos['monto_prestamo_auto'].setRange(0, 99999999)
        self.campos['monto_prestamo_auto'].setPrefix("$ ")
        self.campos['monto_prestamo_auto'].setDecimals(2)
        prestamos_layout.addRow("Monto Préstamo Auto:", self.campos['monto_prestamo_auto'])
        
        self.campos['pago_mensual_auto'] = QDoubleSpinBox()
        self.campos['pago_mensual_auto'].setRange(0, 999999)
        self.campos['pago_mensual_auto'].setPrefix("$ ")
        self.campos['pago_mensual_auto'].setDecimals(2)
        prestamos_layout.addRow("Pago Mensual Auto:", self.campos['pago_mensual_auto'])
        
        # Total deudas
        self.campos['total_deudas'] = QLabel("$0.00")
        self.campos['total_deudas'].setStyleSheet("font-weight: bold; font-size: 13px; color: #e74c3c;")
        prestamos_layout.addRow("<b>Total Deudas:</b>", self.campos['total_deudas'])
        
        # Total pagos mensuales de deudas
        self.campos['total_pagos_mensuales_deudas'] = QLabel("$0.00")
        self.campos['total_pagos_mensuales_deudas'].setStyleSheet("font-weight: bold; font-size: 13px;")
        prestamos_layout.addRow("<b>Pagos Mensuales Deudas:</b>", self.campos['total_pagos_mensuales_deudas'])
        
        grupo_prestamos.setLayout(prestamos_layout)
        main_layout.addWidget(grupo_prestamos)
        
        # Balance
        balance_layout = QHBoxLayout()
        balance_layout.addWidget(QLabel("<b>Balance (Ingreso - Gastos):</b>"))
        self.campos['balance'] = QLabel("$0.00")
        self.campos['balance'].setStyleSheet("font-weight: bold; font-size: 14px;")
        balance_layout.addWidget(self.campos['balance'])
        balance_layout.addStretch()
        
        main_layout.addLayout(balance_layout)
        
        # Observaciones
        main_layout.addWidget(QLabel("<b>Observaciones Financieras:</b>"))
        self.campos['observaciones_financieras'] = QTextEdit()
        self.campos['observaciones_financieras'].setMaximumHeight(80)
        self.campos['observaciones_financieras'].setPlaceholderText(
            "Comentarios sobre la situación financiera, deudas, etc."
        )
        main_layout.addWidget(self.campos['observaciones_financieras'])
        
        scroll.setWidget(content_widget)
        
        page_layout = QVBoxLayout()
        page_layout.addWidget(scroll)
        self.setLayout(page_layout)
        
        # Conectar cambios de sueldo
        self.campos['sueldo_mensual'].valueChanged.connect(self.calcular_totales)
    
    def calcular_totales(self):
        """Calcula los totales de gastos y balance."""
        # Calcular total de gastos
        total_gastos = 0
        for key in ['alimentacion', 'salud', 'educacion', 'recreacion', 'vivienda', 'transporte', 'servicios', 'otros']:
            total_gastos += self.campos[f'gasto_{key}'].value()
        
        self.campos['total_gastos'].setText(f"${total_gastos:,.2f}")
        
        # Calcular total de deudas
        total_deudas = 0
        if self.campos['tiene_prestamos_personales'].isChecked():
            total_deudas += self.campos['monto_prestamos_personales'].value()
        if self.campos['tiene_prestamo_hipotecario'].isChecked():
            total_deudas += self.campos['monto_hipoteca'].value()
        if self.campos['tiene_prestamo_auto'].isChecked():
            total_deudas += self.campos['monto_prestamo_auto'].value()
        
        self.campos['total_deudas'].setText(f"${total_deudas:,.2f}")
        
        # Calcular total pagos mensuales de deudas
        total_pagos_deudas = 0
        if self.campos['tiene_prestamo_hipotecario'].isChecked():
            total_pagos_deudas += self.campos['pago_mensual_hipoteca'].value()
        if self.campos['tiene_prestamo_auto'].isChecked():
            total_pagos_deudas += self.campos['pago_mensual_auto'].value()
        
        self.campos['total_pagos_mensuales_deudas'].setText(f"${total_pagos_deudas:,.2f}")
        
        # Calcular balance (considerando gastos + pagos de deudas)
        sueldo = self.campos['sueldo_mensual'].value()
        balance = sueldo - total_gastos - total_pagos_deudas
        
        self.campos['balance'].setText(f"${balance:,.2f}")
        
        # Colorear balance
        if balance >= 0:
            self.campos['balance'].setStyleSheet("font-weight: bold; font-size: 14px; color: green;")
        else:
            self.campos['balance'].setStyleSheet("font-weight: bold; font-size: 14px; color: red;")
    
    def guardar_datos(self):
        """Guarda los datos en el estudio."""
        fin = self.estudio.datos['situacion_financiera']
        
        fin['trabaja_actualmente'] = self.campos['trabaja_actualmente'].isChecked()
        fin['empresa_actual'] = self.campos['empresa_actual'].text()
        fin['puesto_actual'] = self.campos['puesto_actual'].text()
        fin['sueldo_mensual'] = self.campos['sueldo_mensual'].value()
        fin['horario'] = self.campos['horario'].text()
        
        # Gastos
        gastos = {}
        for key in ['alimentacion', 'salud', 'educacion', 'recreacion', 'vivienda', 'transporte', 'servicios', 'otros']:
            gastos[key] = self.campos[f'gasto_{key}'].value()
        
        gastos['total'] = sum(gastos.values())
        fin['gastos'] = gastos
        
        # Préstamos y deudas
        fin['tiene_prestamos_personales'] = self.campos['tiene_prestamos_personales'].isChecked()
        fin['monto_prestamos_personales'] = self.campos['monto_prestamos_personales'].value()
        fin['tiene_prestamo_hipotecario'] = self.campos['tiene_prestamo_hipotecario'].isChecked()
        fin['monto_hipoteca'] = self.campos['monto_hipoteca'].value()
        fin['pago_mensual_hipoteca'] = self.campos['pago_mensual_hipoteca'].value()
        fin['tiene_prestamo_auto'] = self.campos['tiene_prestamo_auto'].isChecked()
        fin['monto_prestamo_auto'] = self.campos['monto_prestamo_auto'].value()
        fin['pago_mensual_auto'] = self.campos['pago_mensual_auto'].value()
        
        # Calcular totales
        total_deudas = 0
        if fin['tiene_prestamos_personales']:
            total_deudas += fin['monto_prestamos_personales']
        if fin['tiene_prestamo_hipotecario']:
            total_deudas += fin['monto_hipoteca']
        if fin['tiene_prestamo_auto']:
            total_deudas += fin['monto_prestamo_auto']
        
        fin['total_deudas'] = total_deudas
        fin['total_pagos_mensuales_deudas'] = fin['pago_mensual_hipoteca'] + fin['pago_mensual_auto']
        fin['balance'] = fin['sueldo_mensual'] - gastos['total'] - fin['total_pagos_mensuales_deudas']
        fin['observaciones_financieras'] = self.campos['observaciones_financieras'].toPlainText()
    
    def cargar_datos(self):
        """Carga los datos desde el estudio."""
        fin = self.estudio.datos['situacion_financiera']
        
        self.campos['trabaja_actualmente'].setChecked(fin.get('trabaja_actualmente', True))
        self.campos['empresa_actual'].setText(fin.get('empresa_actual', ''))
        self.campos['puesto_actual'].setText(fin.get('puesto_actual', ''))
        self.campos['sueldo_mensual'].setValue(fin.get('sueldo_mensual', 0))
        self.campos['horario'].setText(fin.get('horario', ''))
        
        gastos = fin.get('gastos', {})
        for key in ['alimentacion', 'salud', 'educacion', 'recreacion', 'vivienda', 'transporte', 'servicios', 'otros']:
            self.campos[f'gasto_{key}'].setValue(gastos.get(key, 0))
        
        self.campos['tiene_prestamos_personales'].setChecked(fin.get('tiene_prestamos_personales', False))
        self.campos['monto_prestamos_personales'].setValue(fin.get('monto_prestamos_personales', 0))
        self.campos['tiene_prestamo_hipotecario'].setChecked(fin.get('tiene_prestamo_hipotecario', False))
        self.campos['monto_hipoteca'].setValue(fin.get('monto_hipoteca', 0))
        self.campos['pago_mensual_hipoteca'].setValue(fin.get('pago_mensual_hipoteca', 0))
        self.campos['tiene_prestamo_auto'].setChecked(fin.get('tiene_prestamo_auto', False))
        self.campos['monto_prestamo_auto'].setValue(fin.get('monto_prestamo_auto', 0))
        self.campos['pago_mensual_auto'].setValue(fin.get('pago_mensual_auto', 0))
        
        self.campos['observaciones_financieras'].setPlainText(fin.get('observaciones_financieras', ''))
        
        self.calcular_totales()


class PaginaVivienda(QWizardPage):
    """Página 5: Vivienda y Patrimonio."""
    
    def __init__(self, estudio):
        super().__init__()
        self.estudio = estudio
        self.setTitle("Vivienda y Patrimonio")
        self.init_ui()
        self.cargar_datos()
    
    def init_ui(self):
        """Inicializa la interfaz."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QScrollArea.NoFrame)
        
        content_widget = QWidget()
        main_layout = QVBoxLayout()
        content_widget.setLayout(main_layout)
        
        self.setSubTitle("Características de la vivienda, servicios y patrimonio.")
        
        self.campos = {}
        
        # Información general
        form_layout = QFormLayout()
        
        self.campos['tipo_vivienda'] = QComboBox()
        self.campos['tipo_vivienda'].addItems(["Casa", "Departamento", "Cuarto rentado", "Otro"])
        form_layout.addRow("Tipo de Vivienda:", self.campos['tipo_vivienda'])
        
        self.campos['tenencia'] = QComboBox()
        self.campos['tenencia'].addItems(["Propia", "Rentada", "Prestada", "Pagándose"])
        form_layout.addRow("Tenencia:", self.campos['tenencia'])
        
        self.campos['tipo_zona'] = QComboBox()
        self.campos['tipo_zona'].addItems([
            "Urbana céntrica", "Urbana periférica", "Rural", "Suburbana", "Residencial"
        ])
        form_layout.addRow("Tipo de Zona:", self.campos['tipo_zona'])
        
        self.campos['materiales_construccion'] = QLineEdit()
        self.campos['materiales_construccion'].setPlaceholderText("Ej: Concreto, ladrillo, techo de losa")
        form_layout.addRow("Materiales de Construcción:", self.campos['materiales_construccion'])
        
        self.campos['tiempo_residencia'] = QLineEdit()
        self.campos['tiempo_residencia'].setPlaceholderText("Ej: 5 años")
        form_layout.addRow("Tiempo de Residencia:", self.campos['tiempo_residencia'])
        
        self.campos['numero_cuartos'] = QSpinBox()
        self.campos['numero_cuartos'].setRange(1, 20)
        form_layout.addRow("Número de Cuartos:", self.campos['numero_cuartos'])
        
        main_layout.addLayout(form_layout)
        
        # Servicios
        grupo_servicios = QGroupBox("Servicios con los que Cuenta")
        servicios_layout = QVBoxLayout()
        
        self.checkboxes_servicios = {}
        servicios = [
            ('agua', 'Agua potable'),
            ('luz', 'Electricidad'),
            ('drenaje', 'Drenaje'),
            ('telefono', 'Teléfono'),
            ('internet', 'Internet'),
            ('transporte_publico', 'Transporte público cercano'),
            ('pavimentacion', 'Calle pavimentada'),
            ('areas_verdes', 'Áreas verdes/parques')
        ]
        
        for key, label in servicios:
            checkbox = QCheckBox(label)
            self.checkboxes_servicios[key] = checkbox
            servicios_layout.addWidget(checkbox)
        
        grupo_servicios.setLayout(servicios_layout)
        main_layout.addWidget(grupo_servicios)
        
        # Equipamiento
        grupo_equip = QGroupBox("Equipamiento del Hogar")
        equip_layout = QFormLayout()
        
        equipos = [
            ('refrigerador', 'Refrigerador'),
            ('lavadora', 'Lavadora'),
            ('estufa', 'Estufa'),
            ('televisor', 'Televisor'),
            ('computadora', 'Computadora'),
            ('microondas', 'Microondas')
        ]
        
        self.spinboxes_equip = {}
        for key, label in equipos:
            spinbox = QSpinBox()
            spinbox.setRange(0, 10)
            self.spinboxes_equip[key] = spinbox
            equip_layout.addRow(f"{label}:", spinbox)
        
        grupo_equip.setLayout(equip_layout)
        main_layout.addWidget(grupo_equip)
        
        # Vehículos
        grupo_vehiculos = QGroupBox("Vehículos")
        vehiculos_layout = QFormLayout()
        
        self.spinboxes_vehiculos = {}
        vehiculos = [
            ('automovil', 'Automóvil'),
            ('motocicleta', 'Motocicleta'),
            ('bicicleta', 'Bicicleta')
        ]
        
        for key, label in vehiculos:
            spinbox = QSpinBox()
            spinbox.setRange(0, 10)
            self.spinboxes_vehiculos[key] = spinbox
            vehiculos_layout.addRow(f"{label}:", spinbox)
        
        grupo_vehiculos.setLayout(vehiculos_layout)
        main_layout.addWidget(grupo_vehiculos)
        
        # Otras propiedades
        main_layout.addWidget(QLabel("<b>Otras Propiedades:</b>"))
        self.campos['otras_propiedades'] = QTextEdit()
        self.campos['otras_propiedades'].setMaximumHeight(60)
        self.campos['otras_propiedades'].setPlaceholderText(
            "¿Posee otros inmuebles o propiedades?"
        )
        main_layout.addWidget(self.campos['otras_propiedades'])
        
        scroll.setWidget(content_widget)
        
        page_layout = QVBoxLayout()
        page_layout.addWidget(scroll)
        self.setLayout(page_layout)
    
    def guardar_datos(self):
        """Guarda los datos en el estudio."""
        viv = self.estudio.datos['vivienda']
        
        viv['tipo_vivienda'] = self.campos['tipo_vivienda'].currentText()
        viv['tenencia'] = self.campos['tenencia'].currentText()
        viv['tipo_zona'] = self.campos['tipo_zona'].currentText()
        viv['materiales_construccion'] = self.campos['materiales_construccion'].text()
        viv['tiempo_residencia'] = self.campos['tiempo_residencia'].text()
        viv['numero_cuartos'] = self.campos['numero_cuartos'].value()
        
        # Servicios
        servicios = {}
        for key, checkbox in self.checkboxes_servicios.items():
            servicios[key] = checkbox.isChecked()
        viv['servicios'] = servicios
        
        # Equipamiento
        equipamiento = {}
        for key, spinbox in self.spinboxes_equip.items():
            equipamiento[key] = spinbox.value()
        viv['equipamiento'] = equipamiento
        
        # Vehículos
        vehiculos = {}
        for key, spinbox in self.spinboxes_vehiculos.items():
            vehiculos[key] = spinbox.value()
        viv['vehiculos'] = vehiculos
        
        viv['otras_propiedades'] = self.campos['otras_propiedades'].toPlainText()
    
    def cargar_datos(self):
        """Carga los datos desde el estudio."""
        viv = self.estudio.datos['vivienda']
        
        tipo = viv.get('tipo_vivienda', '')
        if tipo:
            idx = self.campos['tipo_vivienda'].findText(tipo)
            if idx >= 0:
                self.campos['tipo_vivienda'].setCurrentIndex(idx)
        
        tenencia = viv.get('tenencia', '')
        if tenencia:
            idx = self.campos['tenencia'].findText(tenencia)
            if idx >= 0:
                self.campos['tenencia'].setCurrentIndex(idx)
        
        zona = viv.get('tipo_zona', '')
        if zona:
            idx = self.campos['tipo_zona'].findText(zona)
            if idx >= 0:
                self.campos['tipo_zona'].setCurrentIndex(idx)
        
        self.campos['materiales_construccion'].setText(viv.get('materiales_construccion', ''))
        self.campos['tiempo_residencia'].setText(viv.get('tiempo_residencia', ''))
        self.campos['numero_cuartos'].setValue(viv.get('numero_cuartos', 1))
        
        # Servicios
        servicios = viv.get('servicios', {})
        for key, checkbox in self.checkboxes_servicios.items():
            checkbox.setChecked(servicios.get(key, False))
        
        # Equipamiento
        equipamiento = viv.get('equipamiento', {})
        for key, spinbox in self.spinboxes_equip.items():
            spinbox.setValue(equipamiento.get(key, 0))
        
        # Vehículos
        vehiculos = viv.get('vehiculos', {})
        for key, spinbox in self.spinboxes_vehiculos.items():
            spinbox.setValue(vehiculos.get(key, 0))
        
        self.campos['otras_propiedades'].setPlainText(viv.get('otras_propiedades', ''))
