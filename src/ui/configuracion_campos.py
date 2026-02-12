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
                'id': 'genero',
                'etiqueta': 'Género',
                'tipo': TipoCampo.COMBO,
                'requerido': True,
                'ayuda': 'Género del candidato',
                'opciones': ['Femenino', 'Masculino', 'Otro', 'Prefiero no especificar']
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
                'id': 'rfc',
                'etiqueta': 'RFC',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Registro Federal de Contribuyentes',
                'placeholder': 'AAAA####XXXXXX'
            },
            {
                'id': 'nss',
                'etiqueta': 'NSS',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Número de Seguridad Social',
                'placeholder': 'NNN-NNNN-NN'
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
                'id': 'carrera_especialidad',
                'etiqueta': 'Carrera/Especialidad',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Nombre de la carrera o especialidad estudiada',
                'placeholder': 'Ej: Ingenieria en Sistemas, Contaduria, etc.'
            },
            {
                'id': 'institucion_ultimo_grado',
                'etiqueta': 'Institucion de Ultimo Grado',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Escuela donde obtuvo su ultimo grado',
                'placeholder': 'Nombre de la institucion educativa'
            },
            {
                'id': 'estado_estudios',
                'etiqueta': 'Estado de Estudios',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Estado actual de los estudios',
                'opciones': ['Terminado', 'En curso', 'Trunco', 'Pasante', 'Titulado']
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
                'id': 'licencia_conducir',
                'etiqueta': 'Licencia de Conducir',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': '¿Tiene licencia de conducir vigente?'
            },
            {
                'id': 'tipo_licencia',
                'etiqueta': 'Tipo de Licencia',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Tipo de licencia de conducir',
                'opciones': ['A', 'B', 'C', 'D', 'E', 'F']
            },
            {
                'id': 'vigencia_licencia',
                'etiqueta': 'Vigencia de Licencia',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Año de vigencia de la licencia',
                'placeholder': '2025'
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
                'etiqueta': 'Actualmente en Tratamiento Psicologico',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': 'Esta en terapia psicologica actualmente?'
            },
            {
                'id': 'frecuencia_consultas_psicologicas',
                'etiqueta': 'Frecuencia Consultas Psicologicas',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Con que frecuencia asiste a terapia',
                'opciones': ['N/A', 'Semanal', 'Quincenal', 'Mensual', 'Ocasional']
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
            },
            {
                'id': 'jefe_inmediato',
                'etiqueta': 'Nombre del Jefe Inmediato',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Nombre del supervisor o jefe directo',
                'placeholder': 'Nombre completo'
            },
            {
                'id': 'telefono_empresa',
                'etiqueta': 'Telefono de la Empresa',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Telefono para verificacion laboral',
                'placeholder': '(55) 1234-5678'
            },
            {
                'id': 'satisfaccion_laboral',
                'etiqueta': 'Satisfaccion Laboral',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Nivel de satisfaccion con el trabajo actual',
                'opciones': ['Muy satisfecho', 'Satisfecho', 'Neutral', 'Insatisfecho', 'Muy insatisfecho']
            },
            {
                'id': 'oportunidades_ascenso',
                'etiqueta': 'Oportunidades de Ascenso',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Percepcion sobre oportunidades de crecimiento',
                'opciones': ['Excelentes', 'Buenas', 'Moderadas', 'Pocas', 'Ninguna']
            },
            {
                'id': 'ultima_evaluacion_desempeno',
                'etiqueta': 'Ultima Evaluacion de Desempeno',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Fecha o periodo de la ultima evaluacion',
                'placeholder': 'Ej: Diciembre 2025'
            },
            {
                'id': 'observaciones_empleo',
                'etiqueta': 'Observaciones del Empleo',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Notas adicionales sobre el empleo actual'
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
            },
            {
                'id': 'fuma',
                'etiqueta': 'Fuma',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': 'Indica si fuma actualmente'
            },
            {
                'id': 'gasto_mensual_tabaco',
                'etiqueta': 'Gasto Mensual en Tabaco',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Gasto mensual aproximado en cigarros',
                'placeholder': '0.00'
            },
            {
                'id': 'gasto_mensual_alcohol',
                'etiqueta': 'Gasto Mensual en Alcohol',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Gasto mensual aproximado en bebidas alcoholicas',
                'placeholder': '0.00'
            }
        ]
    
    @staticmethod
    def obtener_campos_informacion_familiar() -> List[Dict[str, Any]]:
        """Define los campos de la seccion Informacion Familiar."""
        return [
            {
                'id': 'numero_hijos',
                'etiqueta': 'Numero de Hijos',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Total de hijos'
            },
            {
                'id': 'numero_hijos_menores',
                'etiqueta': 'Hijos Menores de Edad',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Hijos menores de 18 anos'
            },
            {
                'id': 'numero_hijos_estudiando',
                'etiqueta': 'Hijos Estudiando',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Hijos que actualmente estudian'
            },
            {
                'id': 'gasto_mensual_educacion_hijos',
                'etiqueta': 'Gasto Mensual Educacion Hijos',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Gasto total mensual en educacion de hijos',
                'placeholder': '0.00'
            },
            {
                'id': 'total_miembros_hogar',
                'etiqueta': 'Total Miembros del Hogar',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Numero total de personas que viven en el hogar'
            },
            {
                'id': 'miembros_trabajando',
                'etiqueta': 'Miembros que Trabajan',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Cuantos miembros del hogar trabajan'
            },
            {
                'id': 'miembros_estudiando',
                'etiqueta': 'Miembros que Estudian',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Cuantos miembros del hogar estudian'
            },
            {
                'id': 'dependientes_sin_ingreso',
                'etiqueta': 'Dependientes Sin Ingreso',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Miembros que dependen economicamente sin ingresos propios'
            },
            {
                'id': 'observaciones_familiares',
                'etiqueta': 'Observaciones Familiares',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Notas adicionales sobre la situacion familiar'
            }
        ]
    
    @staticmethod
    def obtener_campos_situacion_financiera() -> List[Dict[str, Any]]:
        """Define los campos de la seccion Situacion Financiera."""
        return [
            {
                'id': 'trabaja_actualmente',
                'etiqueta': 'Trabaja Actualmente',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': 'Indica si tiene empleo actualmente'
            },
            {
                'id': 'empresa_actual',
                'etiqueta': 'Empresa Actual',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Nombre de la empresa donde trabaja'
            },
            {
                'id': 'puesto_actual',
                'etiqueta': 'Puesto Actual',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Cargo o puesto que desempena'
            },
            {
                'id': 'sueldo_mensual',
                'etiqueta': 'Sueldo Mensual',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Sueldo mensual neto',
                'placeholder': '0.00'
            },
            {
                'id': 'ingresos_adicionales',
                'etiqueta': 'Ingresos Adicionales',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Descripcion de ingresos adicionales',
                'placeholder': 'Freelance, rentas, inversiones, etc.'
            },
            {
                'id': 'otros_ingresos',
                'etiqueta': 'Monto Otros Ingresos',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Monto total de otros ingresos mensuales',
                'placeholder': '0.00'
            },
            {
                'id': 'ahorros',
                'etiqueta': 'Ahorro Acumulado',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Total de ahorros acumulados',
                'placeholder': '0.00'
            },
            {
                'id': 'monto_ahorros_mensuales',
                'etiqueta': 'Ahorro Mensual',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Cantidad que ahorra mensualmente',
                'placeholder': '0.00'
            },
            {
                'id': 'numero_cuentas_bancarias',
                'etiqueta': 'Numero de Cuentas Bancarias',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Cantidad de cuentas bancarias activas'
            },
            {
                'id': 'cuentas_bancarias',
                'etiqueta': 'Descripcion Cuentas Bancarias',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Detalle de bancos y tipo de cuentas',
                'placeholder': 'Ej: BBVA debito, Banamex nomina'
            },
            {
                'id': 'numero_tarjetas_credito',
                'etiqueta': 'Numero de Tarjetas de Credito',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Cantidad de tarjetas de credito'
            },
            {
                'id': 'limite_credito_total',
                'etiqueta': 'Limite de Credito Total',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Suma de limites de todas las tarjetas',
                'placeholder': '0.00'
            },
            {
                'id': 'deuda_tarjetas_total',
                'etiqueta': 'Deuda Total en Tarjetas',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Saldo deudor total en tarjetas de credito',
                'placeholder': '0.00'
            },
            {
                'id': 'tiene_prestamos_personales',
                'etiqueta': 'Tiene Prestamos Personales',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': 'Indica si tiene prestamos personales vigentes'
            },
            {
                'id': 'monto_prestamos_personales',
                'etiqueta': 'Monto Prestamos Personales',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Deuda total en prestamos personales',
                'placeholder': '0.00'
            },
            {
                'id': 'tiene_prestamo_hipotecario',
                'etiqueta': 'Tiene Hipoteca',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': 'Indica si tiene credito hipotecario'
            },
            {
                'id': 'monto_hipoteca',
                'etiqueta': 'Monto de Hipoteca',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Saldo pendiente de la hipoteca',
                'placeholder': '0.00'
            },
            {
                'id': 'pago_mensual_hipoteca',
                'etiqueta': 'Pago Mensual Hipoteca',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Mensualidad del credito hipotecario',
                'placeholder': '0.00'
            },
            {
                'id': 'tiene_prestamo_auto',
                'etiqueta': 'Tiene Prestamo de Auto',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': 'Indica si tiene credito automotriz'
            },
            {
                'id': 'monto_prestamo_auto',
                'etiqueta': 'Monto Prestamo Auto',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Saldo pendiente del credito automotriz',
                'placeholder': '0.00'
            },
            {
                'id': 'pago_mensual_auto',
                'etiqueta': 'Pago Mensual Auto',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Mensualidad del credito de auto',
                'placeholder': '0.00'
            },
            {
                'id': 'apoyos_gubernamentales',
                'etiqueta': 'Apoyos Gubernamentales',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Programas de apoyo del gobierno que recibe',
                'placeholder': 'Ej: Becas Benito Juarez, Pension Bienestar'
            },
            {
                'id': 'monto_apoyos_gubernamentales',
                'etiqueta': 'Monto Apoyos Gubernamentales',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Monto mensual de apoyos recibidos',
                'placeholder': '0.00'
            },
            {
                'id': 'gasto_promedio_comida_diaria',
                'etiqueta': 'Gasto Promedio Comida Diaria',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Gasto diario aproximado en alimentos',
                'placeholder': '0.00'
            },
            {
                'id': 'gasto_mensual_gasolina',
                'etiqueta': 'Gasto Mensual en Gasolina',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Gasto mensual en combustible',
                'placeholder': '0.00'
            },
            {
                'id': 'gastos_extraordinarios',
                'etiqueta': 'Gastos Extraordinarios',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Gastos no recurrentes o imprevistos recientes'
            },
            {
                'id': 'historial_deudas',
                'etiqueta': 'Historial de Deudas',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Historial de pagos y deudas previas',
                'placeholder': 'Buen historial, atrasos, reestructuraciones, etc.'
            },
            {
                'id': 'observaciones_financieras',
                'etiqueta': 'Observaciones Financieras',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Notas adicionales sobre la situacion financiera'
            }
        ]
    
    @staticmethod
    def obtener_campos_vivienda() -> List[Dict[str, Any]]:
        """Define los campos de la seccion Vivienda."""
        return [
            {
                'id': 'tipo_vivienda',
                'etiqueta': 'Tipo de Vivienda',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Tipo de inmueble donde vive',
                'opciones': ['Casa', 'Departamento', 'Cuarto', 'Otro']
            },
            {
                'id': 'tenencia',
                'etiqueta': 'Tenencia',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Tipo de posesion de la vivienda',
                'opciones': ['Propia', 'Rentada', 'Prestada', 'Familiar', 'Otro']
            },
            {
                'id': 'regimen',
                'etiqueta': 'Regimen de Propiedad',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Regimen legal de la propiedad',
                'opciones': ['Propietario unico', 'Copropiedad', 'Condominio', 'N/A']
            },
            {
                'id': 'tipo_zona',
                'etiqueta': 'Tipo de Zona',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Clasificacion de la zona residencial',
                'opciones': ['Residencial', 'Media', 'Popular', 'Rural', 'Industrial']
            },
            {
                'id': 'materiales_construccion',
                'etiqueta': 'Materiales de Construccion',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Material predominante de la vivienda',
                'opciones': ['Concreto/Ladrillo', 'Block', 'Madera', 'Lamina', 'Mixto', 'Otro']
            },
            {
                'id': 'tiempo_residencia',
                'etiqueta': 'Tiempo de Residencia',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Tiempo viviendo en esta direccion',
                'placeholder': 'Ej: 3 anos, 6 meses'
            },
            {
                'id': 'tiempo_viviendo_ahi',
                'etiqueta': 'Tiempo Viviendo en el Lugar',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Tiempo total en esta vivienda',
                'placeholder': 'Ej: 5 anos'
            },
            {
                'id': 'numero_cuartos',
                'etiqueta': 'Numero de Cuartos',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Total de cuartos en la vivienda'
            },
            {
                'id': 'numero_banos',
                'etiqueta': 'Numero de Banos',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Cantidad de banos completos'
            },
            {
                'id': 'numero_habitaciones',
                'etiqueta': 'Numero de Habitaciones',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Recamaras o dormitorios'
            },
            {
                'id': 'metros_cuadrados_construccion',
                'etiqueta': 'Metros Cuadrados',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Area construida aproximada',
                'placeholder': '0.00'
            },
            {
                'id': 'costo_renta_mensual',
                'etiqueta': 'Costo de Renta Mensual',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Monto de renta si aplica',
                'placeholder': '0.00'
            },
            {
                'id': 'valor_estimado_vivienda',
                'etiqueta': 'Valor Estimado de la Vivienda',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Valor comercial aproximado de la propiedad',
                'placeholder': '0.00'
            },
            {
                'id': 'antiguedad_vivienda_anos',
                'etiqueta': 'Antiguedad de la Vivienda (anos)',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Anos de antiguedad de la construccion'
            },
            {
                'id': 'condiciones_generales',
                'etiqueta': 'Condiciones Generales',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Estado general de la vivienda',
                'opciones': ['Excelente', 'Bueno', 'Regular', 'Malo', 'Precario']
            },
            {
                'id': 'seguridad_entorno',
                'etiqueta': 'Seguridad del Entorno',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Percepcion de seguridad en la zona',
                'opciones': ['Muy seguro', 'Seguro', 'Moderado', 'Inseguro', 'Muy inseguro']
            },
            {
                'id': 'otras_propiedades',
                'etiqueta': 'Otras Propiedades',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Descripcion de otras propiedades que posee'
            },
            {
                'id': 'numero_propiedades_adicionales',
                'etiqueta': 'Numero Propiedades Adicionales',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Cantidad de propiedades adicionales'
            },
            {
                'id': 'valor_propiedades_adicionales',
                'etiqueta': 'Valor Propiedades Adicionales',
                'tipo': TipoCampo.DECIMAL,
                'requerido': False,
                'ayuda': 'Valor total estimado de otras propiedades',
                'placeholder': '0.00'
            }
        ]

    @staticmethod
    def obtener_campos_validacion_documental() -> List[Dict[str, Any]]:
        """Define los campos de la seccion Validacion Documental."""
        return [
            {
                'id': 'ine_verificada',
                'etiqueta': 'INE Verificada',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': 'Se verifico la autenticidad de la INE'
            },
            {
                'id': 'ine_observaciones',
                'etiqueta': 'Observaciones INE',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Notas sobre la verificacion de INE'
            },
            {
                'id': 'curp_validada',
                'etiqueta': 'CURP Validada',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': 'Se valido la CURP en RENAPO'
            },
            {
                'id': 'curp_observaciones',
                'etiqueta': 'Observaciones CURP',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Notas sobre la validacion de CURP'
            },
            {
                'id': 'rfc_validado_sat',
                'etiqueta': 'RFC Validado en SAT',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': 'Se verifico el RFC en el portal del SAT'
            },
            {
                'id': 'rfc_observaciones',
                'etiqueta': 'Observaciones RFC',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Notas sobre la validacion de RFC'
            },
            {
                'id': 'nss_validado_imss',
                'etiqueta': 'NSS Validado en IMSS',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': 'Se verifico el NSS en el IMSS'
            },
            {
                'id': 'nss_observaciones',
                'etiqueta': 'Observaciones NSS',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Notas sobre la validacion de NSS'
            },
            {
                'id': 'comprobante_domicilio_verificado',
                'etiqueta': 'Comprobante de Domicilio Verificado',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': 'Se verifico el comprobante de domicilio'
            },
            {
                'id': 'comprobante_domicilio_tipo',
                'etiqueta': 'Tipo de Comprobante',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Tipo de documento presentado',
                'opciones': ['Recibo CFE', 'Recibo Agua', 'Recibo Gas', 'Estado de Cuenta Bancario', 'Telefono/Internet', 'Predial', 'Otro']
            },
            {
                'id': 'comprobante_domicilio_fecha',
                'etiqueta': 'Fecha del Comprobante',
                'tipo': TipoCampo.FECHA,
                'requerido': False,
                'ayuda': 'Fecha de emision del comprobante'
            },
            {
                'id': 'recibo_nomina_verificado',
                'etiqueta': 'Recibo de Nomina Verificado',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': 'Se verifico el recibo de nomina'
            },
            {
                'id': 'recibo_nomina_periodo',
                'etiqueta': 'Periodo del Recibo',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Periodo que cubre el recibo',
                'placeholder': 'Ej: Enero 2026'
            },
            {
                'id': 'constancia_laboral_verificada',
                'etiqueta': 'Constancia Laboral Verificada',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': 'Se verifico la constancia laboral'
            },
            {
                'id': 'estados_cuenta_verificados',
                'etiqueta': 'Estados de Cuenta Verificados',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': 'Se revisaron estados de cuenta bancarios'
            },
            {
                'id': 'estados_cuenta_meses',
                'etiqueta': 'Meses de Estados de Cuenta',
                'tipo': TipoCampo.NUMERO,
                'requerido': False,
                'ayuda': 'Cantidad de meses revisados'
            },
            {
                'id': 'documentacion_completa',
                'etiqueta': 'Documentacion Completa',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': 'Se reunio toda la documentacion requerida'
            },
            {
                'id': 'observaciones_documentacion',
                'etiqueta': 'Observaciones Generales',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Notas adicionales sobre la documentacion'
            }
        ]
    
    @staticmethod
    def obtener_campos_investigacion_vecinal() -> List[Dict[str, Any]]:
        """Define los campos de la seccion Investigacion Vecinal."""
        return [
            {
                'id': 'visita_domiciliaria_realizada',
                'etiqueta': 'Visita Domiciliaria Realizada',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': 'Se realizo visita al domicilio'
            },
            {
                'id': 'fecha_visita',
                'etiqueta': 'Fecha de Visita',
                'tipo': TipoCampo.FECHA,
                'requerido': False,
                'ayuda': 'Fecha en que se realizo la visita'
            },
            {
                'id': 'hora_visita',
                'etiqueta': 'Hora de Visita',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Hora aproximada de la visita',
                'placeholder': 'Ej: 10:30 AM'
            },
            {
                'id': 'persona_atendio',
                'etiqueta': 'Persona que Atendio',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Nombre de quien recibio al investigador'
            },
            {
                'id': 'parentesco_persona_atendio',
                'etiqueta': 'Parentesco de Quien Atendio',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Relacion con el evaluado',
                'opciones': ['El mismo evaluado', 'Conyuge', 'Padre/Madre', 'Hijo(a)', 'Hermano(a)', 'Otro familiar', 'Roommate', 'Empleado domestico', 'Otro']
            },
            {
                'id': 'vecino_entrevistado',
                'etiqueta': 'Vecino Entrevistado',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': 'Se entrevisto a un vecino'
            },
            {
                'id': 'vecino_nombre',
                'etiqueta': 'Nombre del Vecino',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Nombre del vecino entrevistado'
            },
            {
                'id': 'vecino_direccion',
                'etiqueta': 'Direccion del Vecino',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Direccion o referencia del vecino'
            },
            {
                'id': 'vecino_tiempo_conocerlo',
                'etiqueta': 'Tiempo de Conocer al Evaluado',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Cuanto tiempo conoce el vecino al evaluado',
                'placeholder': 'Ej: 5 anos'
            },
            {
                'id': 'vecino_opinion_comportamiento',
                'etiqueta': 'Opinion sobre Comportamiento',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Como describe el vecino el comportamiento',
                'opciones': ['Excelente', 'Bueno', 'Regular', 'Malo', 'No lo conoce bien']
            },
            {
                'id': 'vecino_comentarios',
                'etiqueta': 'Comentarios del Vecino',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Comentarios adicionales del vecino'
            },
            {
                'id': 'tiempo_residencia_confirmado',
                'etiqueta': 'Tiempo de Residencia Confirmado',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': 'El vecino confirma el tiempo de residencia'
            },
            {
                'id': 'tiempo_residencia_segun_vecino',
                'etiqueta': 'Tiempo segun Vecino',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Tiempo que el vecino dice que vive ahi',
                'placeholder': 'Ej: Aproximadamente 3 anos'
            },
            {
                'id': 'arrendador_contactado',
                'etiqueta': 'Arrendador Contactado',
                'tipo': TipoCampo.CHECKBOX,
                'requerido': False,
                'ayuda': 'Se contacto al arrendador (si aplica)'
            },
            {
                'id': 'arrendador_nombre',
                'etiqueta': 'Nombre del Arrendador',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Nombre del dueno o arrendador'
            },
            {
                'id': 'arrendador_telefono',
                'etiqueta': 'Telefono del Arrendador',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Telefono de contacto del arrendador'
            },
            {
                'id': 'arrendador_opinion',
                'etiqueta': 'Opinion del Arrendador',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Opinion general del arrendador',
                'opciones': ['Excelente inquilino', 'Buen inquilino', 'Regular', 'Problematico', 'No disponible']
            },
            {
                'id': 'arrendador_historial_pagos',
                'etiqueta': 'Historial de Pagos',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Como ha sido el historial de pagos',
                'opciones': ['Siempre puntual', 'Ocasionalmente tarde', 'Frecuentemente tarde', 'Impago', 'No aplica']
            },
            {
                'id': 'condiciones_vivienda_observadas',
                'etiqueta': 'Condiciones de Vivienda Observadas',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Estado general de la vivienda',
                'opciones': ['Excelente', 'Buenas', 'Regulares', 'Malas', 'Precarias']
            },
            {
                'id': 'ambiente_familiar_observado',
                'etiqueta': 'Ambiente Familiar Observado',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Ambiente durante la visita',
                'opciones': ['Armonioso', 'Estable', 'Tenso', 'Conflictivo', 'No observable']
            },
            {
                'id': 'observaciones_investigacion',
                'etiqueta': 'Observaciones de la Investigacion',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Notas generales de la visita e investigacion'
            }
        ]
    
    @staticmethod
    def obtener_campos_analisis_cualitativo() -> List[Dict[str, Any]]:
        """Define los campos de la seccion Analisis Cualitativo."""
        return [
            {
                'id': 'estabilidad_emocional',
                'etiqueta': 'Estabilidad Emocional',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Evaluacion de la estabilidad emocional',
                'opciones': ['Alta', 'Media-Alta', 'Media', 'Media-Baja', 'Baja', 'No evaluada']
            },
            {
                'id': 'estabilidad_emocional_observaciones',
                'etiqueta': 'Observaciones Estabilidad Emocional',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Notas sobre la estabilidad emocional'
            },
            {
                'id': 'perfil_responsabilidad',
                'etiqueta': 'Perfil de Responsabilidad',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Nivel de responsabilidad observado',
                'opciones': ['Muy responsable', 'Responsable', 'Moderadamente responsable', 'Poco responsable', 'Irresponsable', 'No evaluado']
            },
            {
                'id': 'responsabilidad_indicadores',
                'etiqueta': 'Indicadores de Responsabilidad',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Evidencias que sustentan la evaluacion'
            },
            {
                'id': 'congruencia_nivel_vida_ingresos',
                'etiqueta': 'Congruencia Nivel de Vida/Ingresos',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'El nivel de vida corresponde a los ingresos',
                'opciones': ['Totalmente congruente', 'Mayormente congruente', 'Parcialmente congruente', 'Incongruente', 'Muy incongruente', 'No evaluado']
            },
            {
                'id': 'congruencia_observaciones',
                'etiqueta': 'Observaciones de Congruencia',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Notas sobre la congruencia observada'
            },
            {
                'id': 'riesgo_reputacional',
                'etiqueta': 'Riesgo Reputacional',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Nivel de riesgo reputacional detectado',
                'opciones': ['Ninguno', 'Bajo', 'Medio', 'Alto', 'Muy alto', 'No evaluado']
            },
            {
                'id': 'riesgo_reputacional_motivo',
                'etiqueta': 'Motivo del Riesgo Reputacional',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Explicacion del riesgo reputacional'
            },
            {
                'id': 'nivel_arraigo',
                'etiqueta': 'Nivel de Arraigo',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Que tan arraigado esta en su comunidad',
                'opciones': ['Muy arraigado', 'Arraigado', 'Moderadamente arraigado', 'Poco arraigado', 'Sin arraigo', 'No evaluado']
            },
            {
                'id': 'arraigo_indicadores',
                'etiqueta': 'Indicadores de Arraigo',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Factores que demuestran el arraigo'
            },
            {
                'id': 'actitud_entrevista',
                'etiqueta': 'Actitud en Entrevista',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Actitud mostrada durante la entrevista',
                'opciones': ['Muy cooperativa', 'Cooperativa', 'Neutral', 'Evasiva', 'Hostil', 'No evaluada']
            },
            {
                'id': 'coherencia_respuestas',
                'etiqueta': 'Coherencia de Respuestas',
                'tipo': TipoCampo.COMBO,
                'requerido': False,
                'ayuda': 'Las respuestas fueron coherentes entre si',
                'opciones': ['Totalmente coherentes', 'Mayormente coherentes', 'Algunas inconsistencias', 'Muchas inconsistencias', 'Contradictorias', 'No evaluadas']
            },
            {
                'id': 'observaciones_cualitativas',
                'etiqueta': 'Observaciones Cualitativas Generales',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Resumen del analisis cualitativo'
            }
        ]
    
    @staticmethod
    def obtener_campos_investigador() -> List[Dict[str, Any]]:
        """Define los campos de la seccion Datos del Investigador."""
        return [
            {
                'id': 'nombre_investigador',
                'etiqueta': 'Nombre del Investigador',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Nombre completo del investigador',
                'placeholder': 'Nombre completo'
            },
            {
                'id': 'cedula_profesional',
                'etiqueta': 'Cedula Profesional',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Numero de cedula profesional (si aplica)'
            },
            {
                'id': 'empresa_investigadora',
                'etiqueta': 'Empresa Investigadora',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Nombre de la empresa o despacho'
            },
            {
                'id': 'telefono_investigador',
                'etiqueta': 'Telefono del Investigador',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Telefono de contacto del investigador'
            },
            {
                'id': 'email_investigador',
                'etiqueta': 'Email del Investigador',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Correo electronico del investigador',
                'placeholder': 'correo@empresa.com'
            },
            {
                'id': 'fecha_elaboracion',
                'etiqueta': 'Fecha de Elaboracion',
                'tipo': TipoCampo.FECHA,
                'requerido': False,
                'ayuda': 'Fecha en que se elaboro el estudio'
            },
            {
                'id': 'lugar_elaboracion',
                'etiqueta': 'Lugar de Elaboracion',
                'tipo': TipoCampo.TEXTO,
                'requerido': False,
                'ayuda': 'Ciudad o ubicacion donde se elaboro',
                'placeholder': 'Ej: Ciudad de Mexico'
            },
            {
                'id': 'observaciones_finales',
                'etiqueta': 'Observaciones Finales del Investigador',
                'tipo': TipoCampo.TEXTO_LARGO,
                'requerido': False,
                'ayuda': 'Comentarios finales o notas del investigador'
            }
        ]
    
    @staticmethod
    def obtener_todos_los_campos() -> Dict[str, List[Dict[str, Any]]]:
        """
        Retorna todos los campos organizados por seccion.
        Util para generacion automatica de formularios completos.
        """
        return {
            'datos_personales': ConfiguracionCampos.obtener_campos_datos_personales(),
            'salud_intereses': ConfiguracionCampos.obtener_campos_salud(),
            'informacion_familiar': ConfiguracionCampos.obtener_campos_informacion_familiar(),
            'situacion_financiera': ConfiguracionCampos.obtener_campos_situacion_financiera(),
            'vivienda': ConfiguracionCampos.obtener_campos_vivienda(),
            'empleo_actual': ConfiguracionCampos.obtener_campos_empleo_actual(),
            'estilo_vida': ConfiguracionCampos.obtener_campos_estilo_vida(),
            'validacion_documental': ConfiguracionCampos.obtener_campos_validacion_documental(),
            'investigacion_vecinal': ConfiguracionCampos.obtener_campos_investigacion_vecinal(),
            'analisis_cualitativo': ConfiguracionCampos.obtener_campos_analisis_cualitativo(),
            'investigador': ConfiguracionCampos.obtener_campos_investigador()
        }
