"""
Sistema modular de configuración de campos para formularios.
Permite agregar/modificar campos fácilmente sin tocar código UI.
Autor: DINOS Tech
Versión: 0.2.0
"""

from typing import Dict, List, Any
from enum import Enum


class TipoCampo(Enum):
    """Tipos de campo disponibles en formularios."""
    TEXTO = "texto"
    TEXTO_LARGO = "texto_largo"
    NUMERO = "numero"
    DECIMAL = "decimal"
    FECHA = "fecha"
    COMBO = "combo"
    CHECKBOX = "checkbox"
    LISTA = "lista"
    GRUPO = "grupo"


class ConfiguracionCampos:
    """
    Configuración centralizada de campos para facilitar expansión futura.
    Para agregar un nuevo campo: simplemente añadir su definición aquí.
    """
    
    @staticmethod
    def obtener_campos_datos_personales() -> List[Dict[str, Any]]:
        """
        Define todos los campos de la sección Datos Personales.
        
        Estructura de cada campo:
        {
            'id': str - Identificador único del campo en el dict de datos
            'etiqueta': str - Texto a mostrar al usuario
            'tipo': TipoCampo - Tipo de control a usar
            'requerido': bool - Si es obligatorio
            'ayuda': str - Texto de ayuda contextual
            'opciones': List[str] - Para campos tipo combo
            'placeholder': str - Texto de ejemplo en el campo
            'grupo': str - Para agrupar campos relacionados
        }
        """
        return [
            {
                'id': 'nombre_completo',
                'etiqueta': 'Nombre Completo',
                'tipo': TipoCampo.TEXTO,
                'requerido': True,
                'ayuda': 'Nombre completo del candidato',
                'placeholder': 'Apellido Paterno Apellido Materno Nombre(s)'
            },
            {
                'id': 'fecha_nacimiento',
                'etiqueta': 'Fecha de Nacimiento',
                'tipo': TipoCampo.FECHA,
                'requerido': True,
                'ayuda': 'Fecha de nacimiento para calcular edad'
            },
            {
                'id': 'edad',
                'etiqueta': 'Edad',
                'tipo': TipoCampo.NUMERO,
                'requerido': True,
                'ayuda': 'Edad en años cumplidos'
            },
            {
                'id': 'nacionalidad',
                'etiqueta': 'Nacionalidad',
                'tipo': TipoCampo.TEXTO,
                'requerido': True,
                'ayuda': 'País de origen',
                'placeholder': 'Mexicana, Estadounidense, etc.'
            },
            {
                'id': 'estado_nacimiento',
                'etiqueta': 'Estado de Nacimiento',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Estado o región donde nació'
            },
            {
                'id': 'estado_civil',
                'etiqueta': 'Estado Civil',
                'tipo': TipoCampo.COMBO,
                'requerido': True,
                'ayuda': 'Situación civil actual',
                'opciones': ['Soltero(a)', 'Casado(a)', 'Unión libre', 'Divorciado(a)', 'Viudo(a)']
            },
            {
                'id': 'curp',
                'etiqueta': 'CURP',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Clave Única de Registro de Población',
                'placeholder': 'AAAA######HAAAAA##'
            },
            {
                'id': 'ine',
                'etiqueta': 'INE/IFE',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Número de credencial de elector'
            },
            {
                'id': 'telefono',
                'etiqueta': 'Teléfono',
                'tipo': TipoCampo.TEXTO,
                'requerido': True,
                'ayuda': 'Número de contacto principal',
                'placeholder': '(55) 1234-5678'
            },
            {
                'id': 'email',
                'etiqueta': 'Email',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Correo electrónico de contacto',
                'placeholder': 'correo@ejemplo.com'
            },
            {
                'id': 'direccion',
                'etiqueta': 'Dirección',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': True,
                'ayuda': 'Domicilio completo',
                'placeholder': 'Calle, número, colonia, CP, ciudad, estado'
            },
            {
                'id': 'escolaridad',
                'etiqueta': 'Escolaridad',
                'tipo': TipoCampo.COMBO,
                'requerido': True,
                'ayuda': 'Último nivel de estudios',
                'opciones': [
                    'Sin estudios',
                    'Primaria',
                    'Secundaria',
                    'Preparatoria/Bachillerato',
                    'Carrera técnica',
                    'Licenciatura',
                    'Posgrado'
                ]
            },
            {
                'id': 'institucion_ultimo_grado',
                'etiqueta': 'Institución de Último Grado',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Escuela donde obtuvo su último grado',
                'placeholder': 'Nombre de la institución educativa'
            },
            {
                'id': 'certificados',
                'etiqueta': 'Certificados y Capacitaciones',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Cursos, diplomados, certificaciones obtenidas',
                'placeholder': 'Lista de certificados relevantes'
            },
            {
                'id': 'persona_contacto_emergencia',
                'etiqueta': 'Contacto de Emergencia',
                'tipo': TipoCampo.TEXTO,
                'requerido': True,
                'ayuda': 'Nombre de persona a contactar en caso de emergencia'
            },
            {
                'id': 'telefono_emergencia',
                'etiqueta': 'Teléfono de Emergencia',
                'tipo': TipoCampo.TEXTO,
                'requerido': True,
                'ayuda': 'Teléfono del contacto de emergencia'
            },
            {
                'id': 'antecedentes_legales',
                'etiqueta': 'Antecedentes Legales',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': '¿Tiene antecedentes penales o procesos legales?'
            },
            {
                'id': 'detalle_antecedentes',
                'etiqueta': 'Detalle de Antecedentes',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Si marcó que sí, describa brevemente la situación',
                'placeholder': 'Naturaleza del antecedente, fecha, resolución'
            },
            {
                'id': 'dependencia_economica',
                'etiqueta': 'Dependencia Económica',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': '¿De quién depende económicamente? (si aplica)',
                'placeholder': 'Padre, cónyuge, etc. o "Independiente"'
            }
        ]
    
    @staticmethod
    def obtener_campos_salud() -> List[Dict[str, Any]]:
        """Campos de la sección Salud e Intereses."""
        return [
            {
                'id': 'padecimientos',
                'etiqueta': 'Padecimientos Generales',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Enfermedades o condiciones de salud generales'
            },
            {
                'id': 'enfermedades_cronicas',
                'etiqueta': 'Enfermedades Crónicas',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Diabetes, hipertensión, asma, etc.',
                'placeholder': 'Enumere enfermedades crónicas que requieren control constante'
            },
            {
                'id': 'numero_enfermedades_cronicas',
                'etiqueta': 'Número de Enfermedades Crónicas',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Cantidad total de enfermedades crónicas diagnosticadas'
            },
            {
                'id': 'tratamientos_actuales',
                'etiqueta': 'Tratamientos Actuales',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Medicamentos o terapias que está recibiendo',
                'placeholder': 'Nombre del medicamento, dosis, frecuencia'
            },
            {
                'id': 'numero_tratamientos_activos',
                'etiqueta': 'Número de Tratamientos Activos',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Cantidad de tratamientos médicos actuales'
            },
            {
                'id': 'gasto_mensual_medicamentos',
                'etiqueta': 'Gasto Mensual en Medicamentos',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Monto aproximado que gasta al mes en medicinas',
                'placeholder': '0.00'
            },
            {
                'id': 'alergias',
                'etiqueta': 'Alergias',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Alergias a medicamentos, alimentos, etc.',
                'placeholder': 'Penicilina, mariscos, polen, etc.'
            },
            {
                'id': 'antecedentes_psicologicos',
                'etiqueta': 'Antecedentes Psicológicos',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Tratamientos psicológicos o psiquiátricos previos o actuales',
                'placeholder': 'Terapia, diagnósticos, tratamientos'
            },
            {
                'id': 'en_tratamiento_psicologico',
                'etiqueta': 'Actualmente en Tratamiento Psicológico',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': '¿Está en terapia psicológica actualmente?'
            },
            {
                'id': 'consumo_alcohol',
                'etiqueta': 'Consumo de Alcohol',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Frecuencia de consumo de alcohol',
                'opciones': ['No consume', 'Ocasional', 'Social', 'Frecuente', 'Diario']
            },
            {
                'id': 'copas_por_semana',
                'etiqueta': 'Copas/Bebidas por Semana',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Número promedio de bebidas alcohólicas por semana'
            },
            {
                'id': 'consumo_tabaco',
                'etiqueta': 'Consumo de Tabaco',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Frecuencia de consumo de tabaco',
                'opciones': ['No fuma', 'Ex fumador', 'Ocasional', 'Menos de 10 al día', 'Más de 10 al día']
            },
            {
                'id': 'cigarros_por_dia',
                'etiqueta': 'Cigarros por Día',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Número promedio de cigarros que fuma al día'
            },
            {
                'id': 'consumo_otras_sustancias',
                'etiqueta': 'Consumo de Otras Sustancias',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Uso de otras sustancias (si aplica)',
                'placeholder': 'Especificar solo si es relevante'
            },
            {
                'id': 'seguro_medico',
                'etiqueta': '¿Tiene Seguro Médico?',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Acceso a servicios de salud',
                'opciones': ['Sí', 'No']
            },
            {
                'id': 'tipo_seguro',
                'etiqueta': 'Tipo de Seguro',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Institución de salud a la que tiene acceso',
                'opciones': ['IMSS', 'ISSSTE', 'Seguro Popular/INSABI', 'Privado', 'Otro']
            },
            {
                'id': 'costo_mensual_seguro',
                'etiqueta': 'Costo Mensual del Seguro',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Monto mensual si tiene seguro privado',
                'placeholder': '0.00'
            },
            {
                'id': 'metas_corto_plazo',
                'etiqueta': 'Metas a Corto Plazo',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Objetivos para los próximos 1-2 años'
            },
            {
                'id': 'metas_largo_plazo',
                'etiqueta': 'Metas a Largo Plazo',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Objetivos a 5-10 años'
            }
        ]
    
    @staticmethod
    def obtener_campos_empleo_actual() -> List[Dict[str, Any]]:
        """Campos de la sección Empleo Actual."""
        return [
            {
                'id': 'empresa',
                'etiqueta': 'Empresa Actual',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Nombre de la empresa donde trabaja actualmente'
            },
            {
                'id': 'puesto',
                'etiqueta': 'Puesto',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Puesto o cargo actual'
            },
            {
                'id': 'antiguedad',
                'etiqueta': 'Antigüedad',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Tiempo trabajando en la empresa actual',
                'placeholder': 'Ej: 2 años 3 meses'
            },
            {
                'id': 'antiguedad_meses',
                'etiqueta': 'Antigüedad en Meses',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Antigüedad total en meses (para cálculos)'
            },
            {
                'id': 'tipo_contrato',
                'etiqueta': 'Tipo de Contrato',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Modalidad de contratación',
                'opciones': [
                    'Indefinido/Planta',
                    'Temporal',
                    'Por honorarios',
                    'Por obra',
                    'Otro'
                ]
            },
            {
                'id': 'salario_mensual_bruto',
                'etiqueta': 'Salario Mensual Bruto',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Salario antes de deducciones',
                'placeholder': '0.00'
            },
            {
                'id': 'salario_mensual_neto',
                'etiqueta': 'Salario Mensual Neto',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Salario después de deducciones (lo que recibe)',
                'placeholder': '0.00'
            },
            {
                'id': 'prestaciones',
                'etiqueta': 'Prestaciones',
                'tipo': TipoCampo.LISTA,
                'requerido': False,
                'ayuda': 'Lista de prestaciones que recibe',
                'placeholder': 'Aguinaldo, vacaciones, IMSS, etc.'
            },
            {
                'id': 'numero_prestaciones',
                'etiqueta': 'Número de Prestaciones',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Cantidad total de prestaciones'
            },
            {
                'id': 'valor_prestaciones_anuales',
                'etiqueta': 'Valor de Prestaciones Anuales',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Valor estimado de aguinaldo, bonos, etc.',
                'placeholder': '0.00'
            },
            {
                'id': 'horario',
                'etiqueta': 'Horario',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Horario de trabajo',
                'placeholder': 'Ej: Lunes a viernes 9:00-18:00'
            },
            {
                'id': 'horas_semanales',
                'etiqueta': 'Horas Semanales',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Total de horas trabajadas por semana'
            },
            {
                'id': 'dias_laborales_semana',
                'etiqueta': 'Días Laborales por Semana',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Número de días que trabaja por semana'
            },
            {
                'id': 'tiempo_traslado',
                'etiqueta': 'Tiempo de Traslado',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Tiempo que tarda en llegar al trabajo',
                'placeholder': 'Ej: 45 minutos'
            },
            {
                'id': 'tiempo_traslado_minutos',
                'etiqueta': 'Tiempo de Traslado (minutos)',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Tiempo de traslado en minutos (ida)'
            },
            {
                'id': 'costo_mensual_transporte',
                'etiqueta': 'Costo Mensual de Transporte',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Gasto mensual en transporte al trabajo',
                'placeholder': '0.00'
            },
            {
                'id': 'tiene_home_office',
                'etiqueta': 'Tiene Home Office',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': '¿Tiene opción de trabajo desde casa?'
            },
            {
                'id': 'dias_home_office_semana',
                'etiqueta': 'Días de Home Office por Semana',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Número de días que trabaja desde casa'
            },
            {
                'id': 'plan_carrera',
                'etiqueta': 'Plan de Carrera',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Oportunidades de crecimiento en la empresa',
                'placeholder': 'Ascensos posibles, capacitación, etc.'
            },
            {
                'id': 'calificacion_ultima_evaluacion',
                'etiqueta': 'Calificación Última Evaluación (1-10)',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Calificación de la evaluación de desempeño más reciente',
                'placeholder': '0.0'
            },
            {
                'id': 'recibe_bonos',
                'etiqueta': 'Recibe Bonos',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': '¿Recibe bonos o incentivos adicionales?'
            },
            {
                'id': 'monto_promedio_bonos_anuales',
                'etiqueta': 'Monto Promedio Bonos Anuales',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Promedio anual de bonos recibidos',
                'placeholder': '0.00'
            }
        ]
    
    @staticmethod
    def obtener_campos_estilo_vida() -> List[Dict[str, Any]]:
        """Campos de la sección Estilo de Vida."""
        return [
            {
                'id': 'hobbies',
                'etiqueta': 'Hobbies y Pasatiempos',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Actividades que realiza en tiempo libre',
                'placeholder': 'Deportes, manualidades, colecciones, etc.'
            },
            {
                'id': 'numero_hobbies',
                'etiqueta': 'Número de Hobbies',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Cantidad de hobbies que practica regularmente'
            },
            {
                'id': 'gasto_mensual_hobbies',
                'etiqueta': 'Gasto Mensual en Hobbies',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Monto que invierte en sus hobbies',
                'placeholder': '0.00'
            },
            {
                'id': 'actividades_fin_semana',
                'etiqueta': 'Actividades de Fin de Semana',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': '¿Qué hace típicamente los fines de semana?',
                'placeholder': 'Reuniones familiares, deportes, salidas, descanso, etc.'
            },
            {
                'id': 'frecuencia_salidas_mes',
                'etiqueta': 'Frecuencia de Salidas al Mes',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Número de veces que sale al mes (cine, restaurantes, etc.)'
            },
            {
                'id': 'gasto_promedio_por_salida',
                'etiqueta': 'Gasto Promedio por Salida',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Monto aproximado que gasta por salida recreativa',
                'placeholder': '0.00'
            },
            {
                'id': 'frecuencia_viajes',
                'etiqueta': 'Frecuencia de Viajes',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': '¿Con qué frecuencia viaja?',
                'opciones': ['No viaja', 'Una vez al año', 'Varias veces al año', 'Mensualmente']
            },
            {
                'id': 'numero_viajes_ultimo_ano',
                'etiqueta': 'Número de Viajes el Último Año',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Cantidad de viajes en los últimos 12 meses'
            },
            {
                'id': 'gasto_total_viajes_ano',
                'etiqueta': 'Gasto Total en Viajes (Último Año)',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Monto total invertido en viajes',
                'placeholder': '0.00'
            },
            {
                'id': 'destinos_frecuentes',
                'etiqueta': 'Destinos Frecuentes',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Lugares que suele visitar',
                'placeholder': 'Ciudad, playa, montaña, etc.'
            },
            {
                'id': 'gastos_recreativos',
                'etiqueta': 'Gastos Recreativos Mensuales',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Cantidad aproximada que destina a entretenimiento',
                'placeholder': '0.00'
            },
            {
                'id': 'actividades_culturales',
                'etiqueta': 'Actividades Culturales',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Teatro, cine, museos, conciertos, etc.',
                'placeholder': 'Frecuencia y tipo de actividades culturales'
            },
            {
                'id': 'frecuencia_actividades_culturales_mes',
                'etiqueta': 'Actividades Culturales al Mes',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Número de veces que asiste a eventos culturales'
            },
            {
                'id': 'gasto_mensual_cultura',
                'etiqueta': 'Gasto Mensual en Cultura',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Monto invertido en cine, teatro, museos, etc.',
                'placeholder': '0.00'
            },
            {
                'id': 'deportes',
                'etiqueta': 'Deportes que Practica',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Deportes o ejercicio físico regular',
                'placeholder': 'Fútbol, gimnasio, natación, etc.'
            },
            {
                'id': 'frecuencia_ejercicio_semana',
                'etiqueta': 'Frecuencia de Ejercicio (días/semana)',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Número de días que hace ejercicio por semana'
            },
            {
                'id': 'gasto_mensual_gimnasio',
                'etiqueta': 'Gasto Mensual en Gimnasio/Deportes',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Costo de membresías deportivas',
                'placeholder': '0.00'
            },
            {
                'id': 'pertenece_clubes',
                'etiqueta': 'Pertenece a Clubes/Asociaciones',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': '¿Es miembro de algún club o asociación?'
            },
            {
                'id': 'numero_clubes_asociaciones',
                'etiqueta': 'Número de Clubes/Asociaciones',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Cantidad de clubes a los que pertenece'
            },
            {
                'id': 'costo_mensual_membrestas',
                'etiqueta': 'Costo Mensual de Membresías',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Total de cuotas mensuales de clubes',
                'placeholder': '0.00'
            },
            {
                'id': 'tiene_mascotas',
                'etiqueta': 'Tiene Mascotas',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': '¿Tiene mascotas en casa?'
            },
            {
                'id': 'numero_mascotas',
                'etiqueta': 'Número de Mascotas',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Cantidad de mascotas'
            },
            {
                'id': 'gasto_mensual_mascotas',
                'etiqueta': 'Gasto Mensual en Mascotas',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Costo de alimento, veterinario, etc.',
                'placeholder': '0.00'
            }
        ]
    
    @staticmethod
    def obtener_todos_los_campos() -> Dict[str, List[Dict[str, Any]]]:
        """
        Retorna todos los campos organizados por sección.
        Útil para generación automática de formularios completos.
        """
        return {
            'datos_personales': ConfiguracionCampos.obtener_campos_datos_personales(),
            'salud_intereses': ConfiguracionCampos.obtener_campos_salud(),
            'empleo_actual': ConfiguracionCampos.obtener_campos_empleo_actual(),
            'estilo_vida': ConfiguracionCampos.obtener_campos_estilo_vida()
        }
