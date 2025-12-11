"""
Página de visualización con gráficas para estudios socioeconómicos.
Autor: DINOS Tech
Versión: 0.3.0
"""

# NO importar matplotlib al inicio - usar lazy loading
from PyQt5.QtWidgets import (
    QWizardPage, QVBoxLayout, QHBoxLayout, QLabel, 
    QScrollArea, QWidget, QPushButton, QTabWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

# Variables globales para lazy loading de matplotlib
_matplotlib_loaded = False
Figure = None
FigureCanvas = None
np = None
plt = None


def _load_matplotlib():
    """Carga matplotlib solo cuando se necesita."""
    global _matplotlib_loaded, Figure, FigureCanvas, np, plt
    if not _matplotlib_loaded:
        import matplotlib.pyplot as mplt
        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC
        from matplotlib.figure import Fig
        import numpy as numpy
        
        plt = mplt
        FigureCanvas = FC
        Figure = Fig
        np = numpy
        plt.style.use('seaborn-v0_8-darkgrid')
        _matplotlib_loaded = True


class PaginaVisualizacionDatos(QWizardPage):
    """Página que muestra visualizaciones gráficas de los datos del estudio."""
    
    def __init__(self, estudio):
        super().__init__()
        self.estudio = estudio
        self.setTitle("📊 Análisis Visual de Datos")
        self.setSubTitle("Visualización gráfica de la información cuantitativa recopilada")
        self.matplotlib_initialized = False
        
        self.init_ui()
    
    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        main_layout = QVBoxLayout()
        
        # Tabs para diferentes categorías de gráficas
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #cccccc;
                background: white;
            }
            QTabBar::tab {
                background: #f0f0f0;
                padding: 8px 20px;
                margin-right: 2px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background: #3498db;
                color: white;
            }
        """)
        
        # Tab 1: Análisis Financiero
        self.tab_financiero = QScrollArea()
        self.tab_financiero.setWidgetResizable(True)
        self.tabs.addTab(self.tab_financiero, "💰 Finanzas")
        
        # Tab 2: Análisis de Gastos
        self.tab_gastos = QScrollArea()
        self.tab_gastos.setWidgetResizable(True)
        self.tabs.addTab(self.tab_gastos, "📉 Gastos")
        
        # Tab 3: Indicadores de Riesgo
        self.tab_riesgos = QScrollArea()
        self.tab_riesgos.setWidgetResizable(True)
        self.tabs.addTab(self.tab_riesgos, "⚠️ Riesgos")
        
        # Tab 4: Estilo de Vida
        self.tab_estilo = QScrollArea()
        self.tab_estilo.setWidgetResizable(True)
        self.tabs.addTab(self.tab_estilo, "🎨 Estilo de Vida")
        
        main_layout.addWidget(self.tabs)
        
        # Botón para regenerar gráficas
        btn_regenerar = QPushButton("🔄 Actualizar Gráficas")
        btn_regenerar.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                font-size: 11pt;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        btn_regenerar.clicked.connect(self.generar_graficas)
        main_layout.addWidget(btn_regenerar)
        
        self.setLayout(main_layout)
    
    def _init_matplotlib(self):
        """Inicializa matplotlib solo cuando se necesita (lazy loading)."""
        if not self.matplotlib_initialized:
            _load_matplotlib()
            self.matplotlib_initialized = True
    
    def initializePage(self):
        """Se ejecuta cuando se muestra la página."""
        self._init_matplotlib()
        self.generar_graficas()
    
    def generar_graficas(self):
        """Genera todas las gráficas."""
        try:
            self.generar_tab_financiero()
            self.generar_tab_gastos()
            self.generar_tab_riesgos()
            self.generar_tab_estilo_vida()
        except Exception as e:
            print(f"Error generando gráficas: {e}")
    
    def generar_tab_financiero(self):
        """Genera gráficas de análisis financiero."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Título
        titulo = QLabel("📊 Análisis Financiero Completo")
        titulo.setFont(QFont("Arial", 14, QFont.Bold))
        titulo.setStyleSheet("color: #2c3e50; margin: 10px;")
        layout.addWidget(titulo)
        
        # Datos financieros
        finanzas = self.estudio.datos.get('situacion_financiera', {})
        
        # Gráfica 1: Ingresos vs Gastos vs Ahorros
        fig1 = self.crear_grafica_ingresos_vs_gastos(finanzas)
        canvas1 = FigureCanvas(fig1)
        canvas1.setMinimumHeight(350)
        layout.addWidget(canvas1)
        
        # Gráfica 2: Distribución de Deudas
        fig2 = self.crear_grafica_distribucion_deudas(finanzas)
        canvas2 = FigureCanvas(fig2)
        canvas2.setMinimumHeight(350)
        layout.addWidget(canvas2)
        
        # Gráfica 3: Indicadores Financieros
        fig3 = self.crear_grafica_indicadores_financieros(finanzas)
        canvas3 = FigureCanvas(fig3)
        canvas3.setMinimumHeight(350)
        layout.addWidget(canvas3)
        
        widget.setLayout(layout)
        self.tab_financiero.setWidget(widget)
    
    def crear_grafica_ingresos_vs_gastos(self, finanzas):
        """Crea gráfica de barras: Ingresos vs Gastos vs Ahorros."""
        fig = Figure(figsize=(10, 5), facecolor='white')
        ax = fig.add_subplot(111)
        
        ingreso = finanzas.get('ingreso_total_mensual', 0)
        ahorros = finanzas.get('monto_ahorros_mensuales', 0)
        pagos_deudas = finanzas.get('total_pagos_mensuales_deudas', 0)
        gastos_comida = finanzas.get('gasto_promedio_comida_diaria', 0) * 30
        gastos_medicamentos = finanzas.get('gasto_mensual_medicamentos', 0)
        gastos_gasolina = finanzas.get('gasto_mensual_gasolina', 0)
        
        total_gastos = pagos_deudas + gastos_comida + gastos_medicamentos + gastos_gasolina
        
        categorias = ['Ingresos\nMensuales', 'Gastos\nTotales', 'Ahorros\nMensuales', 'Saldo\nDisponible']
        valores = [ingreso, total_gastos, ahorros, ingreso - total_gastos - ahorros]
        colores = ['#27ae60', '#e74c3c', '#3498db', '#f39c12']
        
        barras = ax.bar(categorias, valores, color=colores, edgecolor='black', linewidth=1.5, alpha=0.8)
        
        # Añadir valores sobre las barras
        for barra in barras:
            altura = barra.get_height()
            ax.text(barra.get_x() + barra.get_width()/2., altura,
                   f'${altura:,.0f}',
                   ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        ax.set_ylabel('Monto ($)', fontweight='bold', fontsize=12)
        ax.set_title('Ingresos vs Gastos vs Ahorros Mensuales', fontweight='bold', fontsize=14, pad=20)
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
        ax.grid(axis='y', alpha=0.3)
        
        fig.tight_layout()
        return fig
    
    def crear_grafica_distribucion_deudas(self, finanzas):
        """Crea gráfica de pastel: Distribución de Deudas."""
        fig = Figure(figsize=(10, 5), facecolor='white')
        ax = fig.add_subplot(111)
        
        deuda_tarjetas = finanzas.get('deuda_tarjetas_total', 0)
        prestamos = finanzas.get('monto_prestamos_personales', 0)
        hipoteca = finanzas.get('monto_hipoteca', 0)
        auto = finanzas.get('monto_prestamo_auto', 0)
        
        if deuda_tarjetas + prestamos + hipoteca + auto == 0:
            ax.text(0.5, 0.5, '✅ Sin Deudas Registradas', 
                   ha='center', va='center', fontsize=16, fontweight='bold', color='#27ae60')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        else:
            etiquetas = []
            valores = []
            colores_pastel = ['#e74c3c', '#e67e22', '#f39c12', '#3498db']
            
            if deuda_tarjetas > 0:
                etiquetas.append(f'Tarjetas\n${deuda_tarjetas:,.0f}')
                valores.append(deuda_tarjetas)
            if prestamos > 0:
                etiquetas.append(f'Préstamos\n${prestamos:,.0f}')
                valores.append(prestamos)
            if hipoteca > 0:
                etiquetas.append(f'Hipoteca\n${hipoteca:,.0f}')
                valores.append(hipoteca)
            if auto > 0:
                etiquetas.append(f'Auto\n${auto:,.0f}')
                valores.append(auto)
            
            wedges, texts, autotexts = ax.pie(valores, labels=etiquetas, autopct='%1.1f%%',
                                              colors=colores_pastel[:len(valores)],
                                              startangle=90, textprops={'fontweight': 'bold'})
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(11)
            
            ax.set_title(f'Distribución de Deudas\nTotal: ${sum(valores):,.0f}', 
                        fontweight='bold', fontsize=14, pad=20)
        
        fig.tight_layout()
        return fig
    
    def crear_grafica_indicadores_financieros(self, finanzas):
        """Crea gráfica de indicadores financieros clave."""
        fig = Figure(figsize=(10, 5), facecolor='white')
        ax = fig.add_subplot(111)
        
        porcentaje_ahorro = finanzas.get('porcentaje_ahorro', 0)
        porcentaje_deudas = finanzas.get('porcentaje_deudas_ingreso', 0)
        
        # Límites saludables
        ahorro_saludable = 20  # 20% ideal
        deuda_maxima = 35  # 35% máximo recomendado
        
        indicadores = ['% Ahorro\n(meta: 20%)', '% Deudas/Ingreso\n(max: 35%)']
        valores_actuales = [porcentaje_ahorro, porcentaje_deudas]
        valores_referencia = [ahorro_saludable, deuda_maxima]
        
        x = np.arange(len(indicadores))
        ancho = 0.35
        
        barras1 = ax.bar(x - ancho/2, valores_actuales, ancho, label='Valor Actual',
                        color=['#3498db', '#e74c3c'], alpha=0.8, edgecolor='black')
        barras2 = ax.bar(x + ancho/2, valores_referencia, ancho, label='Valor Referencia',
                        color=['#95a5a6', '#95a5a6'], alpha=0.5, edgecolor='black')
        
        ax.set_ylabel('Porcentaje (%)', fontweight='bold', fontsize=12)
        ax.set_title('Indicadores Financieros Clave', fontweight='bold', fontsize=14, pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(indicadores, fontweight='bold')
        ax.legend(loc='upper right')
        ax.grid(axis='y', alpha=0.3)
        
        # Añadir valores sobre las barras
        for barras in [barras1, barras2]:
            for barra in barras:
                altura = barra.get_height()
                ax.text(barra.get_x() + barra.get_width()/2., altura,
                       f'{altura:.1f}%',
                       ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        fig.tight_layout()
        return fig
    
    def generar_tab_gastos(self):
        """Genera gráficas de distribución de gastos."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        titulo = QLabel("💸 Análisis de Gastos Mensuales")
        titulo.setFont(QFont("Arial", 14, QFont.Bold))
        titulo.setStyleSheet("color: #2c3e50; margin: 10px;")
        layout.addWidget(titulo)
        
        # Gráfica de distribución de gastos
        fig = self.crear_grafica_distribucion_gastos()
        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(400)
        layout.addWidget(canvas)
        
        widget.setLayout(layout)
        self.tab_gastos.setWidget(widget)
    
    def crear_grafica_distribucion_gastos(self):
        """Crea gráfica de pastel con distribución de gastos."""
        fig = Figure(figsize=(10, 6), facecolor='white')
        ax = fig.add_subplot(111)
        
        finanzas = self.estudio.datos.get('situacion_financiera', {})
        estilo = self.estudio.datos.get('estilo_vida', {})
        
        # Recopilar gastos
        gastos = {
            'Comida': finanzas.get('gasto_promedio_comida_diaria', 0) * 30,
            'Medicamentos': finanzas.get('gasto_mensual_medicamentos', 0),
            'Gasolina/Transporte': finanzas.get('gasto_mensual_gasolina', 0),
            'Hobbies': estilo.get('gasto_mensual_hobbies', 0),
            'Mascotas': estilo.get('gasto_mensual_mascotas', 0),
            'Gimnasio': estilo.get('gasto_mensual_gimnasio', 0),
            'Cultura': estilo.get('gasto_mensual_cultura', 0),
            'Tabaco': estilo.get('gasto_mensual_tabaco', 0),
            'Alcohol': estilo.get('gasto_mensual_alcohol', 0)
        }
        
        # Filtrar gastos mayores a 0
        gastos_filtrados = {k: v for k, v in gastos.items() if v > 0}
        
        if not gastos_filtrados:
            ax.text(0.5, 0.5, '📊 Sin Gastos Registrados', 
                   ha='center', va='center', fontsize=16, fontweight='bold', color='#7f8c8d')
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
        else:
            etiquetas = [f'{k}\n${v:,.0f}' for k, v in gastos_filtrados.items()]
            valores = list(gastos_filtrados.values())
            
            # Paleta de colores profesional
            colores = ['#3498db', '#e74c3c', '#f39c12', '#27ae60', '#9b59b6', 
                      '#1abc9c', '#e67e22', '#34495e', '#16a085']
            
            wedges, texts, autotexts = ax.pie(valores, labels=etiquetas, autopct='%1.1f%%',
                                              colors=colores[:len(valores)], startangle=90,
                                              textprops={'fontweight': 'bold', 'fontsize': 10})
            
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontsize(10)
            
            total = sum(valores)
            ax.set_title(f'Distribución de Gastos Mensuales\nTotal: ${total:,.0f}', 
                        fontweight='bold', fontsize=14, pad=20)
        
        fig.tight_layout()
        return fig
    
    def generar_tab_riesgos(self):
        """Genera gráficas de indicadores de riesgo."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        titulo = QLabel("⚠️ Análisis de Indicadores de Riesgo")
        titulo.setFont(QFont("Arial", 14, QFont.Bold))
        titulo.setStyleSheet("color: #2c3e50; margin: 10px;")
        layout.addWidget(titulo)
        
        # Gráfica de radar para riesgos
        fig = self.crear_grafica_radar_riesgos()
        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(450)
        layout.addWidget(canvas)
        
        widget.setLayout(layout)
        self.tab_riesgos.setWidget(widget)
    
    def crear_grafica_radar_riesgos(self):
        """Crea gráfica de radar para indicadores de riesgo."""
        fig = Figure(figsize=(10, 7), facecolor='white')
        ax = fig.add_subplot(111, projection='polar')
        
        riesgos = self.estudio.datos.get('riesgos', {})
        
        categorias = ['Financiero', 'Familiar', 'Vivienda', 'Laboral', 'Salud', 'Global']
        valores = [
            riesgos.get('financiero', 0),
            riesgos.get('familiar', 0),
            riesgos.get('vivienda', 0),
            riesgos.get('laboral', 0),
            riesgos.get('salud', 0),
            riesgos.get('global', 0)
        ]
        
        # Completar el círculo
        valores += valores[:1]
        
        # Ángulos
        angulos = np.linspace(0, 2 * np.pi, len(categorias), endpoint=False).tolist()
        angulos += angulos[:1]
        
        # Dibujar
        ax.plot(angulos, valores, 'o-', linewidth=2, color='#e74c3c', label='Nivel de Riesgo')
        ax.fill(angulos, valores, alpha=0.25, color='#e74c3c')
        
        # Zona segura (riesgo < 3)
        zona_segura = [3] * len(angulos)
        ax.plot(angulos, zona_segura, '--', linewidth=1.5, color='#27ae60', alpha=0.7, label='Zona Segura (< 3)')
        ax.fill(angulos, zona_segura, alpha=0.1, color='#27ae60')
        
        ax.set_xticks(angulos[:-1])
        ax.set_xticklabels(categorias, fontweight='bold', fontsize=10)
        ax.set_ylim(0, 5)
        ax.set_yticks([1, 2, 3, 4, 5])
        ax.set_yticklabels(['1\nBajo', '2', '3\nMedio', '4', '5\nAlto'], fontsize=9)
        ax.set_title('Indicadores de Riesgo\n(Escala 1-5)', fontweight='bold', fontsize=14, pad=30)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        ax.grid(True, alpha=0.3)
        
        fig.tight_layout()
        return fig
    
    def generar_tab_estilo_vida(self):
        """Genera gráficas de estilo de vida."""
        widget = QWidget()
        layout = QVBoxLayout()
        
        titulo = QLabel("🎨 Análisis de Estilo de Vida")
        titulo.setFont(QFont("Arial", 14, QFont.Bold))
        titulo.setStyleSheet("color: #2c3e50; margin: 10px;")
        layout.addWidget(titulo)
        
        # Gráfica de actividades
        fig = self.crear_grafica_actividades()
        canvas = FigureCanvas(fig)
        canvas.setMinimumHeight(400)
        layout.addWidget(canvas)
        
        widget.setLayout(layout)
        self.tab_estilo.setWidget(widget)
    
    def crear_grafica_actividades(self):
        """Crea gráfica de barras horizontales para actividades."""
        fig = Figure(figsize=(10, 6), facecolor='white')
        ax = fig.add_subplot(111)
        
        estilo = self.estudio.datos.get('estilo_vida', {})
        salud = self.estudio.datos.get('salud_intereses', {})
        
        actividades = {
            'Hobbies': estilo.get('numero_hobbies', 0),
            'Salidas/Mes': estilo.get('frecuencia_salidas_mes', 0),
            'Viajes/Año': estilo.get('numero_viajes_ultimo_ano', 0),
            'Ejercicio/Semana': estilo.get('frecuencia_ejercicio_semana', 0),
            'Actividades Culturales/Mes': estilo.get('frecuencia_actividades_culturales_mes', 0),
            'Copas/Semana': salud.get('copas_por_semana', 0),
            'Cigarros/Día': salud.get('cigarros_por_dia', 0)
        }
        
        # Colores según tipo de actividad
        colores = {
            'Hobbies': '#9b59b6',
            'Salidas/Mes': '#3498db',
            'Viajes/Año': '#1abc9c',
            'Ejercicio/Semana': '#27ae60',
            'Actividades Culturales/Mes': '#f39c12',
            'Copas/Semana': '#e67e22',
            'Cigarros/Día': '#e74c3c'
        }
        
        categorias = list(actividades.keys())
        valores = list(actividades.values())
        colores_barras = [colores[cat] for cat in categorias]
        
        barras = ax.barh(categorias, valores, color=colores_barras, edgecolor='black', linewidth=1, alpha=0.8)
        
        # Añadir valores al final de las barras
        for i, (barra, valor) in enumerate(zip(barras, valores)):
            ax.text(valor + 0.3, i, str(int(valor)), va='center', fontweight='bold', fontsize=10)
        
        ax.set_xlabel('Frecuencia', fontweight='bold', fontsize=12)
        ax.set_title('Frecuencia de Actividades y Hábitos', fontweight='bold', fontsize=14, pad=20)
        ax.grid(axis='x', alpha=0.3)
        
        # Invertir eje Y para que el primer elemento esté arriba
        ax.invert_yaxis()
        
        fig.tight_layout()
        return fig
