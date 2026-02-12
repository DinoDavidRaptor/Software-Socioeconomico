"""
Modelo de datos para estudios socioeconómicos.
Autor: DINOS Tech
Versión: 0.1.0
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class EstudioSocioeconomico:
    """
    Clase que representa un estudio socioeconómico completo.
    Maneja la estructura de datos y operaciones de persistencia.
    """
    
    def __init__(self, id_estudio: Optional[str] = None):
        """
        Inicializa un nuevo estudio socioeconómico.
        
        Args:
            id_estudio: Identificador único del estudio. Si es None, se genera automáticamente.
        """
        self.id = id_estudio or self._generar_id()
        self.fecha_creacion = datetime.now().isoformat()
        self.fecha_modificacion = datetime.now().isoformat()
        
        # Estructura de datos del estudio
        self.datos = {
            "id": self.id,
            "fecha_creacion": self.fecha_creacion,
            "fecha_modificacion": self.fecha_modificacion,
            "empresa_solicitante": "",  # ⭐ NUEVO v0.3.0 - Empresa que solicita el estudio
            
            # Sección 1: Datos Personales (Extendidos)
            "datos_personales": {
                "nombre_completo": "",
                "edad": 0,
                "fecha_nacimiento": "",
                "genero": "",  # ⭐ NUEVO
                "nacionalidad": "",
                "estado_nacimiento": "",
                "estado_civil": "",
                "curp": "",
                "rfc": "",  # ⭐ NUEVO
                "ine": "",
                "nss": "",  # ⭐ NUEVO
                "telefono": "",
                "email": "",
                "direccion": "",
                "escolaridad": "",
                "carrera_especialidad": "",  # ⭐ NUEVO
                "institucion_ultimo_grado": "",
                "estado_estudios": "",  # ⭐ NUEVO
                "certificados": "",
                "licencia_conducir": False,  # ⭐ NUEVO
                "licencia_tipo": "",  # ⭐ NUEVO
                "licencia_vigencia": "",  # ⭐ NUEVO
                "contactos_emergencia": [],  # ⭐ NUEVO - Array de contactos
                "antecedentes_legales": False,
                "antecedentes_legales_detalle": "",  # ⭐ NUEVO
                "detalle_antecedentes": "",
                "dependencia_economica": ""
            },
            
            # Sección 2: Salud (Expandida)
            "salud_intereses": {
                "padecimientos": "",
                "numero_enfermedades_cronicas": 0,  # ⭐ NUEVO - Cantidad
                "enfermedades_cronicas": "",
                "tratamientos_actuales": "",
                "gasto_mensual_medicamentos": 0.0,  # ⭐ NUEVO
                "numero_tratamientos_activos": 0,  # ⭐ NUEVO
                "alergias": "",
                "antecedentes_psicologicos": "",
                "en_tratamiento_psicologico": False,  # ⭐ NUEVO
                "frecuencia_consultas_psicologicas": "",  # ⭐ NUEVO
                "consumo_alcohol": "",
                "copas_por_semana": 0,  # ⭐ NUEVO - Cantidad específica
                "consumo_tabaco": "",
                "cigarros_por_dia": 0,  # ⭐ NUEVO - Cantidad específica
                "consumo_otras_sustancias": "",
                "seguro_medico": "",
                "tipo_seguro": "",
                "costo_mensual_seguro": 0.0,  # ⭐ NUEVO
                "metas_corto_plazo": "",
                "metas_largo_plazo": ""
            },
            
            # Sección 3: Información Familiar (Extendida)
            "informacion_familiar": {
                "numero_hijos": 0,
                "numero_hijos_menores": 0,  # ⭐ NUEVO - Menores de 18
                "numero_hijos_estudiando": 0,  # ⭐ NUEVO
                "gasto_mensual_educacion_hijos": 0.0,  # ⭐ NUEVO
                "miembros_hogar": [],  # Lista de {nombre, edad, parentesco, ocupacion, ingreso, es_dependiente}  # ⭐ NUEVO - Agregado es_dependiente
                "total_miembros_hogar": 0,  # ⭐ NUEVO - Contador
                "miembros_trabajando": 0,  # ⭐ NUEVO
                "miembros_estudiando": 0,  # ⭐ NUEVO
                "miembros_con_enfermedades": 0,  # ⭐ NUEVO
                "ingreso_familiar_total": 0.0,
                "ingreso_per_capita": 0.0,  # ⭐ NUEVO - Ingreso/personas
                "dependientes_sin_ingreso": 0,
                "porcentaje_dependientes": 0.0,  # ⭐ NUEVO - % de dependientes
                "gasto_promedio_por_persona": 0.0,  # ⭐ NUEVO
                "observaciones_familiares": ""
            },
            
            # Sección 4: Situación Financiera (Expandida)
            "situacion_financiera": {
                "trabaja_actualmente": True,
                "empresa_actual": "",  # ⭐ NUEVO
                "puesto_actual": "",  # ⭐ NUEVO
                "sueldo_mensual": 0.0,
                "otros_ingresos": [],  # Lista de {fuente, monto, frecuencia}
                "ingreso_total_mensual": 0.0,  # Calculado automáticamente
                "ahorros": 0.0,
                "monto_ahorros_mensuales": 0.0,  # ⭐ NUEVO - Cuanto ahorra al mes
                "cuentas_bancarias": "",
                "numero_cuentas_bancarias": 0,  # ⭐ NUEVO - Cantidad de cuentas
                "tarjetas_credito": [],  # Lista de {banco, limite, saldo_actual}
                "numero_tarjetas_credito": 0,  # ⭐ NUEVO - Cantidad de tarjetas
                "limite_credito_total": 0.0,  # ⭐ NUEVO - Suma de todos los límites
                "deuda_tarjetas_total": 0.0,  # ⭐ NUEVO - Suma de saldos actuales
                "historial_deudas": "",
                "tiene_prestamos_personales": False,  # ⭐ NUEVO
                "monto_prestamos_personales": 0.0,  # ⭐ NUEVO
                "tiene_prestamo_hipotecario": False,  # ⭐ NUEVO
                "monto_hipoteca": 0.0,  # ⭐ NUEVO
                "pago_mensual_hipoteca": 0.0,  # ⭐ NUEVO
                "tiene_prestamo_auto": False,  # ⭐ NUEVO
                "monto_prestamo_auto": 0.0,  # ⭐ NUEVO
                "pago_mensual_auto": 0.0,  # ⭐ NUEVO
                "apoyos_gubernamentales": "",
                "monto_apoyos_gubernamentales": 0.0,  # ⭐ NUEVO
                "gastos": {
                    "alimentacion": 0.0,
                    "salud": 0.0,
                    "educacion": 0.0,
                    "vivienda": 0.0,
                    "transporte": 0.0,
                    "servicios": 0.0,
                    "recreacion": 0.0,
                    "otros": 0.0,
                    "total": 0.0
                },
                "gasto_promedio_comida_diaria": 0.0,  # ⭐ NUEVO
                "gasto_mensual_medicamentos": 0.0,  # ⭐ NUEVO
                "gasto_mensual_gasolina": 0.0,  # ⭐ NUEVO
                "gastos_extraordinarios": "",
                "deudas": [],  # Lista de {acreedor, monto, pago_mensual}
                "total_deudas": 0.0,  # ⭐ NUEVO - Suma de todas las deudas
                "total_pagos_mensuales_deudas": 0.0,  # ⭐ NUEVO
                "balance": 0.0,
                "porcentaje_gastos_ingreso": 0.0,
                "porcentaje_ahorro": 0.0,  # ⭐ NUEVO
                "porcentaje_deudas_ingreso": 0.0,  # ⭐ NUEVO
                "capacidad_pago": 0.0,  # ⭐ NUEVO - Ingreso menos gastos fijos
                "discrepancia_ingresos": False,
                "observaciones_financieras": ""
            },
            
            # Sección 5: Vivienda (Expandida)
            "vivienda": {
                "zona": "",
                "tipo_zona": "",
                "tipo_vivienda": "",
                "tenencia": "",
                "renta_mensual": 0.0,
                "tiempo_residencia": "",
                "tiempo_viviendo_ahi": "",
                "materiales_construccion": "",
                "condicion_fisica": {
                    "humedad": False,
                    "filtraciones": False,
                    "sobrecupo": False,
                    "buena_ventilacion": True,
                    "iluminacion_natural": True
                },
                "servicios": {
                    "agua": False,
                    "luz": False,
                    "drenaje": False,
                    "gas": False,
                    "telefono": False,
                    "internet": False,
                    "transporte_publico": False,
                    "pavimentacion": False,
                    "areas_verdes": False
                },
                "equipamiento": {
                    "refrigerador": 0,
                    "lavadora": 0,
                    "estufa": 0,
                    "televisor": 0,
                    "computadora": 0,
                    "microondas": 0,
                    "aire_acondicionado": 0,
                    "calentador": 0
                },
                "mobiliario": {
                    "camas": 0,
                    "mesas": 0,
                    "sillas": 0,
                    "armarios": 0,
                    "sillones": 0
                },
                "vehiculos": {
                    "automovil": 0,
                    "motocicleta": 0,
                    "bicicleta": 0
                },
                "valor_aproximado_vehiculos": 0.0,  # ⭐ NUEVO
                "numero_cuartos": 0,
                "numero_banos": 0,  # ⭐ NUEVO
                "metros_cuadrados_construccion": 0.0,  # ⭐ NUEVO
                "numero_habitantes": 0,
                "indice_hacinamiento": 0.0,  # ⭐ NUEVO - Personas por cuarto
                "numero_servicios_basicos": 0,  # ⭐ NUEVO - Conteo automático
                "porcentaje_equipamiento": 0.0,  # ⭐ NUEVO - % de equipamiento completo
                "valor_estimado_vivienda": 0.0,  # ⭐ NUEVO
                "antiguedad_vivienda_anos": 0,  # ⭐ NUEVO
                "seguridad_entorno": "",
                "otras_propiedades": "",
                "numero_propiedades_adicionales": 0,  # ⭐ NUEVO
                "valor_propiedades_adicionales": 0.0  # ⭐ NUEVO
            },
            
            # Sección 6: Empleo Actual (Detallado)
            "empleo_actual": {
                "empresa": "",
                "empresa_actual": "",  # ⭐ NUEVO
                "puesto": "",
                "puesto_actual": "",  # ⭐ NUEVO
                "antiguedad": "",
                "antiguedad_meses": 0,  # ⭐ NUEVO - En meses para cálculos
                "tipo_contrato": "",
                "salario_mensual_bruto": 0.0,  # ⭐ NUEVO
                "salario_mensual_neto": 0.0,  # ⭐ NUEVO
                "prestaciones": [],
                "numero_prestaciones": 0,  # ⭐ NUEVO - Contador
                "valor_prestaciones_anuales": 0.0,  # ⭐ NUEVO - Aguinaldo, etc.
                "horario": "",
                "horas_semanales": 0,  # ⭐ NUEVO
                "dias_laborales_semana": 0,  # ⭐ NUEVO
                "tiempo_traslado": "",
                "tiempo_traslado_minutos": 0,  # ⭐ NUEVO - En minutos
                "costo_mensual_transporte": 0.0,  # ⭐ NUEVO
                "tiene_home_office": False,  # ⭐ NUEVO
                "dias_home_office_semana": 0,  # ⭐ NUEVO
                "jefe_inmediato": "",  # ⭐ NUEVO
                "telefono_empresa": "",  # ⭐ NUEVO
                "satisfaccion_laboral": "",  # ⭐ NUEVO
                "plan_carrera": "",
                "oportunidades_ascenso": "",  # ⭐ NUEVO
                "ultima_evaluacion_desempeno": "",  # ⭐ NUEVO
                "calificacion_ultima_evaluacion": 0.0,  # ⭐ NUEVO - De 1 a 10
                "recibe_bonos": False,  # ⭐ NUEVO
                "monto_promedio_bonos_anuales": 0.0,  # ⭐ NUEVO
                "observaciones_empleo": ""  # ⭐ NUEVO
            },
            
            # Sección 7: Historial Laboral (Profundo)
            "historial_laboral": [],  # Lista de empleos anteriores
            # Cada empleo: {empresa, puesto, duracion_meses, fecha_inicio (opcional), fecha_fin (opcional),
            #               salario_inicial, salario_final, jefe_nombre, jefe_puesto, telefono_contacto, 
            #               motivo_separacion, evaluaciones, conflictos, verificacion_referencia}
            # ⭐ NUEVO v0.3.0: duracion_meses es el campo CUANTITATIVO principal
            
            # Sección 8: Estilo de Vida
            "estilo_vida": {
                "hobbies": "",
                "numero_hobbies": 0,  # ⭐ NUEVO
                "gasto_mensual_hobbies": 0.0,  # ⭐ NUEVO
                "actividades_fin_semana": "",
                "frecuencia_salidas_mes": 0,  # ⭐ NUEVO
                "gasto_promedio_por_salida": 0.0,  # ⭐ NUEVO
                "frecuencia_viajes": "",
                "numero_viajes_ultimo_ano": 0,  # ⭐ NUEVO
                "gasto_total_viajes_ano": 0.0,  # ⭐ NUEVO
                "destinos_frecuentes": "",
                "gastos_recreativos": 0.0,
                "actividades_culturales": "",
                "frecuencia_actividades_culturales_mes": 0,  # ⭐ NUEVO
                "gasto_mensual_cultura": 0.0,  # ⭐ NUEVO - Cine, teatro, etc.
                "deportes": "",
                "frecuencia_ejercicio_semana": 0,  # ⭐ NUEVO
                "gasto_mensual_gimnasio": 0.0,  # ⭐ NUEVO
                "pertenece_clubes": False,  # ⭐ NUEVO
                "numero_clubes_asociaciones": 0,  # ⭐ NUEVO
                "costo_mensual_membrestas": 0.0,  # ⭐ NUEVO
                "tiene_mascotas": False,  # ⭐ NUEVO
                "numero_mascotas": 0,  # ⭐ NUEVO
                "gasto_mensual_mascotas": 0.0,  # ⭐ NUEVO
                "fuma": False,  # ⭐ NUEVO
                "gasto_mensual_tabaco": 0.0,  # ⭐ NUEVO
                "consume_alcohol_socialmente": False,  # ⭐ NUEVO
                "gasto_mensual_alcohol": 0.0  # ⭐ NUEVO
            },
            
            # Sección 9: Referencias Personales
            "referencias": [],  # Lista de referencias
            # Cada referencia: {nombre, relacion, domicilio_empresa, telefono, ocupacion, 
            #                   tiempo_conocerse_meses, observaciones}
            # ⭐ NUEVO v0.3.0: tiempo_conocerse_meses es CUANTITATIVO (meses de conocer a la persona)
            
            # Sección 10: Conclusiones
            "conclusiones": "",
            
            # Fotografías adjuntas
            "fotos": [],  # Lista de {archivo, tipo, descripcion}
            
            # Métricas calculadas con justificaciones
            "riesgos": {
                "financiero": 0,
                "financiero_justificacion": [],
                "familiar": 0,
                "familiar_justificacion": [],
                "vivienda": 0,
                "vivienda_justificacion": [],
                "laboral": 0,
                "laboral_justificacion": [],
                "global": 0,
                "global_justificacion": []
            },
            
            # Validaciones y alertas
            "alertas": {
                "gastos_excesivos": False,
                "contradicciones": [],
                "dependientes_sin_ingreso_detectado": False,
                "discrepancia_ingresos": False
            },
            
            # ============================================
            # SECCIONES INSTITUCIONALES v0.3.2
            # ============================================
            
            # Seccion 11: Validacion Documental
            "validacion_documental": {
                "ine_verificada": False,
                "ine_observaciones": "",
                "curp_validada": False,
                "curp_observaciones": "",
                "rfc_validado_sat": False,
                "rfc_observaciones": "",
                "nss_validado_imss": False,
                "nss_observaciones": "",
                "comprobante_domicilio_verificado": False,
                "comprobante_domicilio_tipo": "",  # Recibo luz, agua, etc.
                "comprobante_domicilio_fecha": "",
                "recibo_nomina_verificado": False,
                "recibo_nomina_periodo": "",
                "constancia_laboral_verificada": False,
                "estados_cuenta_verificados": False,
                "estados_cuenta_meses": 0,
                "documentacion_completa": False,
                "observaciones_documentacion": ""
            },
            
            # Seccion 12: Investigacion Vecinal
            "investigacion_vecinal": {
                "visita_domiciliaria_realizada": False,
                "fecha_visita": "",
                "hora_visita": "",
                "persona_atendio": "",
                "parentesco_persona_atendio": "",
                "vecino_entrevistado": False,
                "vecino_nombre": "",
                "vecino_direccion": "",
                "vecino_tiempo_conocerlo": "",
                "vecino_opinion_comportamiento": "",  # Bueno/Regular/Malo
                "vecino_comentarios": "",
                "tiempo_residencia_confirmado": False,
                "tiempo_residencia_segun_vecino": "",
                "arrendador_contactado": False,
                "arrendador_nombre": "",
                "arrendador_telefono": "",
                "arrendador_opinion": "",
                "arrendador_historial_pagos": "",  # Puntual/Irregular/Moroso
                "condiciones_vivienda_observadas": "",
                "ambiente_familiar_observado": "",  # Estable/Conflictivo/No observado
                "observaciones_investigacion": ""
            },
            
            # Seccion 13: Analisis Cualitativo
            "analisis_cualitativo": {
                "estabilidad_emocional": "",  # Estable/Inestable/No evaluado
                "estabilidad_emocional_observaciones": "",
                "perfil_responsabilidad": "",  # Alto/Medio/Bajo
                "responsabilidad_indicadores": "",
                "congruencia_nivel_vida_ingresos": "",  # Congruente/Incongruente/Dudoso
                "congruencia_observaciones": "",
                "riesgo_reputacional": "",  # Bajo/Medio/Alto
                "riesgo_reputacional_motivo": "",
                "nivel_arraigo": "",  # Alto/Medio/Bajo
                "arraigo_indicadores": "",  # Propiedad, familia, tiempo residencia
                "actitud_entrevista": "",  # Cooperativa/Evasiva/Hostil
                "coherencia_respuestas": "",  # Alta/Media/Baja
                "observaciones_cualitativas": ""
            },
            
            # Seccion 14: Datos del Investigador y Firma
            "investigador": {
                "nombre_investigador": "",
                "cedula_profesional": "",
                "empresa_investigadora": "",
                "telefono_investigador": "",
                "email_investigador": "",
                "fecha_elaboracion": "",
                "lugar_elaboracion": "",
                "declaracion_veracidad": False,
                "firma_digital": "",  # Puede ser ruta a imagen de firma
                "observaciones_finales": ""
            }
        }
    
    def _generar_id(self) -> str:
        """Genera un ID único basado en timestamp."""
        return datetime.now().strftime("%Y%m%d%H%M%S%f")
    
    def actualizar_fecha_modificacion(self):
        """Actualiza la fecha de última modificación."""
        self.fecha_modificacion = datetime.now().isoformat()
        self.datos["fecha_modificacion"] = self.fecha_modificacion
    
    def guardar(self, ruta_base: str = "data/estudios") -> bool:
        """
        Guarda el estudio en formato JSON.
        
        Args:
            ruta_base: Directorio donde se guardará el archivo.
            
        Returns:
            True si se guardó correctamente, False en caso contrario.
        """
        try:
            os.makedirs(ruta_base, exist_ok=True)
            self.actualizar_fecha_modificacion()
            
            archivo = os.path.join(ruta_base, f"{self.id}.json")
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(self.datos, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"Error al guardar estudio: {e}")
            return False
    
    @classmethod
    def cargar(cls, id_estudio: str, ruta_base: str = "data/estudios") -> Optional['EstudioSocioeconomico']:
        """
        Carga un estudio desde archivo JSON.
        
        Args:
            id_estudio: ID del estudio a cargar.
            ruta_base: Directorio donde se encuentra el archivo.
            
        Returns:
            Instancia de EstudioSocioeconomico o None si hay error.
        """
        try:
            archivo = os.path.join(ruta_base, f"{id_estudio}.json")
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            estudio = cls(id_estudio)
            estudio.datos = datos
            estudio.fecha_creacion = datos.get("fecha_creacion", estudio.fecha_creacion)
            estudio.fecha_modificacion = datos.get("fecha_modificacion", estudio.fecha_modificacion)
            
            return estudio
        except Exception as e:
            print(f"Error al cargar estudio: {e}")
            return None
    
    @staticmethod
    def listar_estudios(ruta_base: str = "data/estudios") -> List[Dict]:
        """
        Lista todos los estudios disponibles.
        
        Args:
            ruta_base: Directorio donde buscar los archivos.
            
        Returns:
            Lista de diccionarios con información básica de cada estudio.
        """
        estudios = []
        
        try:
            os.makedirs(ruta_base, exist_ok=True)
            archivos = [f for f in os.listdir(ruta_base) if f.endswith('.json')]
            
            for archivo in archivos:
                try:
                    with open(os.path.join(ruta_base, archivo), 'r', encoding='utf-8') as f:
                        datos = json.load(f)
                    
                    estudios.append({
                        "id": datos.get("id", ""),
                        "nombre": datos.get("datos_personales", {}).get("nombre_completo", "Sin nombre"),
                        "fecha_creacion": datos.get("fecha_creacion", ""),
                        "fecha_modificacion": datos.get("fecha_modificacion", ""),
                        "riesgo_global": datos.get("riesgos", {}).get("global", 0)
                    })
                except:
                    continue
            
            # Ordenar por fecha de modificación descendente
            estudios.sort(key=lambda x: x["fecha_modificacion"], reverse=True)
            
        except Exception as e:
            print(f"Error al listar estudios: {e}")
        
        return estudios
    
    @staticmethod
    def eliminar(id_estudio: str, ruta_base: str = "data/estudios") -> bool:
        """
        Elimina un estudio y sus fotografías asociadas.
        
        Args:
            id_estudio: ID del estudio a eliminar.
            ruta_base: Directorio donde se encuentra el archivo.
            
        Returns:
            True si se eliminó correctamente, False en caso contrario.
        """
        try:
            # Cargar estudio para obtener las fotos
            estudio = EstudioSocioeconomico.cargar(id_estudio, ruta_base)
            
            if estudio:
                # Eliminar fotografías asociadas
                for foto in estudio.datos.get("fotos", []):
                    if isinstance(foto, dict):
                        ruta_foto = foto.get("archivo", "")
                        if ruta_foto and os.path.exists(ruta_foto):
                            os.remove(ruta_foto)
            
            # Eliminar archivo JSON
            archivo = os.path.join(ruta_base, f"{id_estudio}.json")
            if os.path.exists(archivo):
                os.remove(archivo)
            
            return True
        except Exception as e:
            print(f"Error al eliminar estudio: {e}")
            return False
    
    def obtener_resumen_ia(self) -> str:
        """
        Genera un resumen en texto plano del estudio para análisis externo.
        
        Returns:
            String con el resumen formateado.
        """
        d = self.datos
        dp = d.get("datos_personales", {})
        fam = d.get("informacion_familiar", {})
        fin = d.get("situacion_financiera", {})
        viv = d.get("vivienda", {})
        riesgos = d.get("riesgos", {})
        
        resumen = f"""Dame un estudio socioeconómico completo con riesgo socioeconómico y toda la info de la siguiente persona:

Nombre: {dp.get('nombre_completo', 'N/A')}
Edad: {dp.get('edad', 'N/A')}
Estado civil: {dp.get('estado_civil', 'N/A')}
CURP: {dp.get('curp', 'N/A')}
Teléfono: {dp.get('telefono', 'N/A')}
Email: {dp.get('email', 'N/A')}
Dirección: {dp.get('direccion', 'N/A')}

COMPOSICIÓN FAMILIAR:
Número de hijos: {fam.get('numero_hijos', 0)}
Personas en el hogar: {len(fam.get('miembros_hogar', []))}
Ingreso familiar mensual: ${fam.get('ingreso_familiar_total', 0):,.2f}

SITUACIÓN LABORAL Y FINANCIERA:
Empresa actual: {fin.get('empresa_actual', 'N/A')}
Puesto: {fin.get('puesto_actual', 'N/A')}
Sueldo mensual: ${fin.get('sueldo_mensual', 0):,.2f}
Total gastos mensuales: ${fin.get('gastos', {}).get('total', 0):,.2f}
Balance mensual: ${fin.get('balance', 0):,.2f}
Número de deudas: {len(fin.get('deudas', []))}

VIVIENDA:
Tipo: {viv.get('tipo_vivienda', 'N/A')}
Tenencia: {viv.get('tenencia', 'N/A')}
Zona: {viv.get('tipo_zona', 'N/A')}
Materiales: {viv.get('materiales_construccion', 'N/A')}

HISTORIAL LABORAL:
Empleos anteriores: {len(d.get('historial_laboral', []))}

REFERENCIAS:
Referencias personales: {len(d.get('referencias', []))}

INDICADORES DE RIESGO (Escala 1-5):
Riesgo Financiero: {riesgos.get('financiero', 0)}
Riesgo Familiar: {riesgos.get('familiar', 0)}
Riesgo Vivienda: {riesgos.get('vivienda', 0)}
Riesgo Laboral: {riesgos.get('laboral', 0)}
RIESGO SOCIOECONÓMICO GLOBAL: {riesgos.get('global', 0)}

OBSERVACIONES FINANCIERAS:
{fin.get('observaciones_financieras', 'Sin observaciones')}
"""
        return resumen
