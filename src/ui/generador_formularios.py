"""
Generador automático de formularios basado en configuración de campos.
Facilita la creación de páginas de wizard sin código repetitivo.
Autor: DINOS Tech
Versión: 0.2.0
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel,
    QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox, QComboBox,
    QCheckBox, QDateEdit, QGroupBox, QPushButton, QListWidget,
    QFrame, QScrollArea
)
from PyQt5.QtCore import Qt, QDate
from typing import Dict, List, Any
from .configuracion_campos import TipoCampo


class GeneradorFormularios:
    """
    Genera automáticamente controles de formulario basados en configuración.
    Hace muy fácil agregar nuevos campos sin programar UI manualmente.
    """
    
    @staticmethod
    def crear_campo(config: Dict[str, Any], parent: QWidget = None) -> tuple:
        """
        Crea un control de formulario basado en configuración.
        
        Args:
            config: Diccionario con configuración del campo
            parent: Widget padre
            
        Returns:
            Tupla (widget, get_value_func, set_value_func)
            - widget: Control visual creado
            - get_value_func: Función para obtener el valor
            - set_value_func: Función para establecer el valor
        """
        tipo = config.get('tipo')
        
        if tipo == TipoCampo.TEXTO:
            return GeneradorFormularios._crear_campo_texto(config, parent)
        elif tipo == TipoCampo.TEXTO_LARGO:
            return GeneradorFormularios._crear_campo_texto_largo(config, parent)
        elif tipo == TipoCampo.NUMERO:
            return GeneradorFormularios._crear_campo_numero(config, parent)
        elif tipo == TipoCampo.DECIMAL:
            return GeneradorFormularios._crear_campo_decimal(config, parent)
        elif tipo == TipoCampo.FECHA:
            return GeneradorFormularios._crear_campo_fecha(config, parent)
        elif tipo == TipoCampo.COMBO:
            return GeneradorFormularios._crear_campo_combo(config, parent)
        elif tipo == TipoCampo.CHECKBOX:
            return GeneradorFormularios._crear_campo_checkbox(config, parent)
        elif tipo == TipoCampo.LISTA:
            return GeneradorFormularios._crear_campo_lista(config, parent)
        else:
            # Por defecto, texto simple
            return GeneradorFormularios._crear_campo_texto(config, parent)
    
    @staticmethod
    def _crear_campo_texto(config: Dict[str, Any], parent: QWidget) -> tuple:
        """Crea campo de texto simple."""
        widget = QLineEdit(parent)
        
        placeholder = config.get('placeholder', '')
        if placeholder:
            widget.setPlaceholderText(placeholder)
        
        get_func = lambda: widget.text()
        set_func = lambda v: widget.setText(str(v) if v else "")
        
        return widget, get_func, set_func
    
    @staticmethod
    def _crear_campo_texto_largo(config: Dict[str, Any], parent: QWidget) -> tuple:
        """Crea campo de texto multilínea."""
        widget = QTextEdit(parent)
        widget.setMaximumHeight(100)
        
        placeholder = config.get('placeholder', '')
        if placeholder:
            widget.setPlaceholderText(placeholder)
        
        get_func = lambda: widget.toPlainText()
        set_func = lambda v: widget.setPlainText(str(v) if v else "")
        
        return widget, get_func, set_func
    
    @staticmethod
    def _crear_campo_numero(config: Dict[str, Any], parent: QWidget) -> tuple:
        """Crea campo numérico entero."""
        widget = QSpinBox(parent)
        widget.setRange(0, 999999)
        
        get_func = lambda: widget.value()
        set_func = lambda v: widget.setValue(int(v) if v else 0)
        
        return widget, get_func, set_func
    
    @staticmethod
    def _crear_campo_decimal(config: Dict[str, Any], parent: QWidget) -> tuple:
        """Crea campo numérico decimal."""
        widget = QDoubleSpinBox(parent)
        widget.setRange(0, 999999.99)
        widget.setDecimals(2)
        widget.setPrefix("$")
        
        get_func = lambda: widget.value()
        set_func = lambda v: widget.setValue(float(v) if v else 0.0)
        
        return widget, get_func, set_func
    
    @staticmethod
    def _crear_campo_fecha(config: Dict[str, Any], parent: QWidget) -> tuple:
        """Crea campo de fecha."""
        widget = QDateEdit(parent)
        widget.setCalendarPopup(True)
        widget.setDate(QDate.currentDate())
        widget.setDisplayFormat("dd/MM/yyyy")
        
        get_func = lambda: widget.date().toString("yyyy-MM-dd")
        set_func = lambda v: widget.setDate(QDate.fromString(str(v), "yyyy-MM-dd") if v else QDate.currentDate())
        
        return widget, get_func, set_func
    
    @staticmethod
    def _crear_campo_combo(config: Dict[str, Any], parent: QWidget) -> tuple:
        """Crea campo de selección (combo box)."""
        widget = QComboBox(parent)
        
        opciones = config.get('opciones', [])
        widget.addItem("")  # Opción vacía
        widget.addItems(opciones)
        
        get_func = lambda: widget.currentText()
        set_func = lambda v: widget.setCurrentText(str(v) if v else "")
        
        return widget, get_func, set_func
    
    @staticmethod
    def _crear_campo_checkbox(config: Dict[str, Any], parent: QWidget) -> tuple:
        """Crea campo de checkbox."""
        widget = QCheckBox(parent)
        
        get_func = lambda: widget.isChecked()
        set_func = lambda v: widget.setChecked(bool(v) if v is not None else False)
        
        return widget, get_func, set_func
    
    @staticmethod
    def _crear_campo_lista(config: Dict[str, Any], parent: QWidget) -> tuple:
        """Crea campo de lista editable."""
        container = QWidget(parent)
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        
        list_widget = QListWidget()
        list_widget.setMaximumHeight(100)
        
        btn_layout = QHBoxLayout()
        btn_agregar = QPushButton("Agregar")
        btn_eliminar = QPushButton("Eliminar")
        btn_layout.addWidget(btn_agregar)
        btn_layout.addWidget(btn_eliminar)
        btn_layout.addStretch()
        
        layout.addWidget(list_widget)
        layout.addLayout(btn_layout)
        
        def agregar_item():
            from PyQt5.QtWidgets import QInputDialog
            texto, ok = QInputDialog.getText(parent, "Agregar", "Ingrese el texto:")
            if ok and texto:
                list_widget.addItem(texto)
        
        def eliminar_item():
            current = list_widget.currentRow()
            if current >= 0:
                list_widget.takeItem(current)
        
        btn_agregar.clicked.connect(agregar_item)
        btn_eliminar.clicked.connect(eliminar_item)
        
        def get_value():
            items = []
            for i in range(list_widget.count()):
                items.append(list_widget.item(i).text())
            return items
        
        def set_value(items):
            list_widget.clear()
            if items:
                for item in items:
                    list_widget.addItem(str(item))
        
        return container, get_value, set_value
    
    @staticmethod
    def crear_formulario_completo(campos: List[Dict[str, Any]], parent: QWidget = None) -> Dict:
        """
        Crea un formulario completo con todos los campos especificados.
        
        Args:
            campos: Lista de configuraciones de campos
            parent: Widget padre
            
        Returns:
            Dict con:
            - 'layout': QLayout con todos los controles
            - 'widgets': Dict {id_campo: widget}
            - 'getters': Dict {id_campo: func_get_value}
            - 'setters': Dict {id_campo: func_set_value}
        """
        # Crear scroll area para manejar muchos campos
        scroll = QScrollArea(parent)
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        container = QWidget()
        main_layout = QVBoxLayout(container)
        form_layout = QFormLayout()
        form_layout.setSpacing(10)
        
        widgets = {}
        getters = {}
        setters = {}
        
        for config in campos:
            campo_id = config['id']
            etiqueta = config['etiqueta']
            requerido = config.get('requerido', False)
            ayuda = config.get('ayuda', '')
            
            # Crear etiqueta con indicador de requerido
            label_text = etiqueta
            if requerido:
                label_text += " *"
            
            label = QLabel(label_text)
            if ayuda:
                label.setToolTip(ayuda)
            
            # Crear el control
            widget, get_func, set_func = GeneradorFormularios.crear_campo(config, container)
            
            if ayuda:
                widget.setToolTip(ayuda)
            
            # Agregar al formulario
            form_layout.addRow(label, widget)
            
            # Guardar referencias
            widgets[campo_id] = widget
            getters[campo_id] = get_func
            setters[campo_id] = set_func
            
            # Agregar separador visual cada 5 campos
            if len(widgets) % 5 == 0 and len(widgets) < len(campos):
                separator = QFrame()
                separator.setFrameShape(QFrame.HLine)
                separator.setFrameShadow(QFrame.Sunken)
                form_layout.addRow(separator)
        
        main_layout.addLayout(form_layout)
        main_layout.addStretch()
        
        scroll.setWidget(container)
        
        return {
            'scroll': scroll,
            'layout': main_layout,
            'widgets': widgets,
            'getters': getters,
            'setters': setters
        }
    
    @staticmethod
    def crear_etiqueta_ayuda(texto: str, parent: QWidget = None) -> QLabel:
        """Crea una etiqueta de ayuda contextual."""
        label = QLabel(texto, parent)
        label.setWordWrap(True)
        label.setStyleSheet("""
            QLabel {
                background-color: #E3F2FD;
                border: 1px solid #90CAF9;
                border-radius: 4px;
                padding: 8px;
                color: #1976D2;
                font-size: 11px;
            }
        """)
        return label
    
    @staticmethod
    def crear_grupo_campos(titulo: str, campos: List[Dict[str, Any]], parent: QWidget = None) -> Dict:
        """
        Crea un grupo de campos dentro de un QGroupBox.
        
        Returns:
            Dict similar a crear_formulario_completo pero dentro de un grupo
        """
        group = QGroupBox(titulo, parent)
        layout = QVBoxLayout(group)
        
        form_result = GeneradorFormularios.crear_formulario_completo(campos, group)
        
        # Reemplazar el scroll con el contenido directo para grupos
        container = form_result['scroll'].widget()
        layout.addWidget(container)
        
        return {
            'group': group,
            'widgets': form_result['widgets'],
            'getters': form_result['getters'],
            'setters': form_result['setters']
        }
