"""
Generador de datos aleatorios para pruebas de estudios socioeconómicos.
Autor: DINOS Tech
Versión: 0.3.0
"""

import random
from datetime import datetime, timedelta
from typing import Dict, Any


class GeneradorDatosPrueba:
    """Genera datos aleatorios realistas para todos los campos del estudio."""
    
    # Listas de datos para generar valores aleatorios
    NOMBRES = ["Juan", "María", "Pedro", "Ana", "Carlos", "Laura", "José", "Carmen", "Luis", "Rosa"]
    APELLIDOS = ["García", "Rodríguez", "Martínez", "López", "González", "Hernández", "Pérez", "Sánchez"]
    ESTADOS = ["Aguascalientes", "Baja California", "CDMX", "Jalisco", "Nuevo León", "Puebla", "Querétaro", "Yucatán"]
    NACIONALIDADES = ["Mexicana", "Estadounidense", "Colombiana", "Española", "Argentina"]
    GENEROS = ["Femenino", "Masculino", "Otro", "Prefiero no especificar"]
    ESTADOS_CIVILES = ["Soltero(a)", "Casado(a)", "Divorciado(a)", "Unión libre", "Viudo(a)"]
    ESCOLARIDADES = ["Secundaria", "Preparatoria", "Licenciatura", "Maestría", "Doctorado"]
    INSTITUCIONES = ["UNAM", "IPN", "ITESM", "UAM", "BUAP", "UDG", "UANL"]
    
    EMPRESAS = ["TechCorp SA", "InnovaSoft", "Grupo Industrial MX", "Consultores Unidos", "Digital Solutions"]
    PUESTOS = ["Analista", "Desarrollador", "Gerente", "Coordinador", "Especialista", "Supervisor"]
    TIPOS_CONTRATO = ["Planta/Base", "Temporal", "Por proyecto", "Honorarios"]
    
    HOBBIES = ["Leer", "Hacer ejercicio", "Cocinar", "Viajar", "Videojuegos", "Música", "Pintura", "Fotografía"]
    DEPORTES = ["Fútbol", "Basquetbol", "Natación", "Ciclismo", "Yoga", "Gimnasio", "Tenis", "Correr"]
    
    @classmethod
    def generar_nombre_completo(cls) -> str:
        """Genera un nombre completo aleatorio."""
        nombre = random.choice(cls.NOMBRES)
        apellido1 = random.choice(cls.APELLIDOS)
        apellido2 = random.choice(cls.APELLIDOS)
        return f"{nombre} {apellido1} {apellido2}"
    
    @classmethod
    def generar_fecha_nacimiento(cls, edad: int) -> str:
        """Genera una fecha de nacimiento coherente con la edad."""
        hoy = datetime.now()
        anio_nacimiento = hoy.year - edad
        mes = random.randint(1, 12)
        dia = random.randint(1, 28)
        return f"{dia:02d}/{mes:02d}/{anio_nacimiento}"
    
    @classmethod
    def generar_curp(cls) -> str:
        """Genera un CURP ficticio."""
        letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        numeros = "0123456789"
        return ''.join(random.choices(letras, k=4)) + ''.join(random.choices(numeros, k=6)) + \
               ''.join(random.choices(letras + numeros, k=8))
    
    @classmethod
    def generar_telefono(cls) -> str:
        """Genera un número de teléfono ficticio."""
        return f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    
    @classmethod
    def generar_email(cls, nombre: str) -> str:
        """Genera un email basado en el nombre."""
        dominios = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com"]
        nombre_limpio = nombre.lower().replace(" ", ".").split()[0]
        return f"{nombre_limpio}{random.randint(10, 99)}@{random.choice(dominios)}"
    
    @classmethod
    def generar_direccion(cls) -> str:
        """Genera una dirección ficticia."""
        calles = ["Av. Reforma", "Calle Juárez", "Blvd. Insurgentes", "Privada Hidalgo", "Calzada México"]
        return f"{random.choice(calles)} #{random.randint(100, 999)}, Col. Centro, CP {random.randint(10000, 99999)}"
    
    @classmethod
    def generar_datos_personales(cls) -> Dict[str, Any]:
        """Genera la sección de datos personales."""
        edad = random.randint(22, 65)
        nombre = cls.generar_nombre_completo()
        
        return {
            "nombre_completo": nombre,
            "edad": edad,
            "fecha_nacimiento": cls.generar_fecha_nacimiento(edad),
            "genero": random.choice(cls.GENEROS),
            "nacionalidad": random.choice(cls.NACIONALIDADES),
            "estado_nacimiento": random.choice(cls.ESTADOS),
            "estado_civil": random.choice(cls.ESTADOS_CIVILES),
            "curp": cls.generar_curp(),
            "rfc": ''.join(random.choices("ABCDEFGHIJKLMNPQRSTUVWXYZ", k=4)) + random.randint(1900, 2000).__str__() + random.choice("AEIOU") + random.randint(10, 99).__str__() + "A1",
            "ine": f"XXXXXXXXXX{random.randint(100, 999)}",
            "nss": f"{random.randint(100, 999)}-{random.randint(100000, 999999)}-{random.randint(10, 99)}",
            "telefono": cls.generar_telefono(),
            "email": cls.generar_email(nombre),
            "direccion": cls.generar_direccion(),
            "escolaridad": random.choice(cls.ESCOLARIDADES),
            "carrera_especialidad": random.choice(["Ingeniería en Sistemas", "Administración", "Contaduría", "Derecho", "Medicina", "Psicología", "Ninguna"]),
            "institucion_ultimo_grado": random.choice(cls.INSTITUCIONES),
            "estado_estudios": random.choice(["Completos", "En curso", "Truncos"]),
            "certificados": random.choice(["Inglés avanzado", "Certificación profesional", "Diplomado", "Ninguno"]),
            "licencia_conducir": random.choice([True, False]),
            "licencia_tipo": random.choice(["A", "B", "C", "D", "Ninguna"]) if random.random() > 0.5 else "",
            "licencia_vigencia": f"{random.randint(2025, 2030)}" if random.random() > 0.5 else "",
            "contactos_emergencia": [
                {
                    "nombre": cls.generar_nombre_completo(),
                    "telefono": cls.generar_telefono(),
                    "parentesco": random.choice(["Padre", "Madre", "Cónyuge", "Hermano", "Amigo"])
                }
            ],
            "antecedentes_legales": random.choice([True, False]),
            "antecedentes_legales_detalle": random.choice(["Ninguno", "Infracción de tránsito menor", "Ninguno"]),
            "detalle_antecedentes": random.choice(["Ninguno", "Infracción de tránsito menor"]),
            "dependencia_economica": random.choice(["Independiente", "Padre/Madre", "Cónyuge", "Ambos padres"])
        }
    
    @classmethod
    def generar_salud_intereses(cls) -> Dict[str, Any]:
        """Genera la sección de salud."""
        num_enfermedades = random.randint(0, 3)
        num_tratamientos = random.randint(0, 2)
        copas_semana = random.randint(0, 10)
        cigarros_dia = random.randint(0, 20) if random.random() > 0.7 else 0
        
        return {
            "padecimientos": random.choice(["Ninguno", "Diabetes", "Hipertensión", "Asma"]),
            "numero_enfermedades_cronicas": num_enfermedades,
            "enfermedades_cronicas": random.choice(["Ninguna", "Diabetes tipo 2", "Hipertensión"]),
            "tratamientos_actuales": random.choice(["Ninguno", "Medicamento diario", "Terapia física"]),
            "gasto_mensual_medicamentos": round(random.uniform(0, 3000), 2) if num_tratamientos > 0 else 0,
            "numero_tratamientos_activos": num_tratamientos,
            "alergias": random.choice(["Ninguna", "Polen", "Alimentos", "Medicamentos"]),
            "antecedentes_psicologicos": random.choice(["Ninguno", "Ansiedad", "Depresión"]),
            "en_tratamiento_psicologico": random.choice([True, False]),
            "frecuencia_consultas_psicologicas": random.choice(["Ninguna", "Mensual", "Quincenal", "Semanal"]),
            "consumo_alcohol": random.choice(["Ocasional", "Social", "Frecuente", "No consume"]),
            "copas_por_semana": copas_semana,
            "consumo_tabaco": "Sí" if cigarros_dia > 0 else "No",
            "cigarros_por_dia": cigarros_dia,
            "consumo_otras_sustancias": "No",
            "seguro_medico": random.choice(["IMSS", "ISSSTE", "Privado", "Ninguno"]),
            "tipo_seguro": random.choice(["Institucional", "Privado", "Ninguno"]),
            "costo_mensual_seguro": round(random.uniform(500, 5000), 2) if random.random() > 0.5 else 0,
            "metas_corto_plazo": "Mejorar salud física, ahorrar más",
            "metas_largo_plazo": "Comprar casa, retiro anticipado"
        }
    
    @classmethod
    def generar_miembro_familia(cls) -> Dict[str, Any]:
        """Genera un miembro de familia aleatorio."""
        edad = random.randint(1, 75)
        return {
            "nombre": cls.generar_nombre_completo(),
            "edad": edad,
            "parentesco": random.choice(["Hijo(a)", "Cónyuge", "Padre/Madre", "Hermano(a)"]),
            "estudia_trabaja": random.choice(["Trabaja", "Estudia", "Ambos", "Ninguno"]),
            "aporta_ingreso": random.choice([True, False]),
            "enfermedades_cronicas": random.choice(["Ninguna", "Diabetes", "Hipertensión"]),
            "dependencia_tipo": random.choice(["Ninguna", "Económica", "Total"]),
            "ingreso": round(random.uniform(0, 15000), 2) if random.random() > 0.4 else 0
        }
    
    @classmethod
    def generar_informacion_familiar(cls) -> Dict[str, Any]:
        """Genera la sección de información familiar."""
        num_hijos = random.randint(0, 4)
        num_miembros = random.randint(2, 6)
        num_hijos_menores = random.randint(0, num_hijos) if num_hijos > 0 else 0
        num_trabajando = random.randint(1, num_miembros)
        
        miembros = [cls.generar_miembro_familia() for _ in range(num_miembros)]
        ingreso_total = sum(m["ingreso"] for m in miembros)
        ingreso_per_capita = round(ingreso_total / num_miembros, 2) if num_miembros > 0 else 0
        
        return {
            "numero_hijos": num_hijos,
            "numero_hijos_menores": num_hijos_menores,
            "numero_hijos_estudiando": random.randint(0, num_hijos) if num_hijos > 0 else 0,
            "gasto_mensual_educacion_hijos": round(random.uniform(500, 5000), 2) if num_hijos > 0 else 0,
            "miembros_hogar": miembros,
            "total_miembros_hogar": num_miembros,
            "miembros_trabajando": num_trabajando,
            "miembros_estudiando": random.randint(0, num_miembros),
            "miembros_con_enfermedades": random.randint(0, 2),
            "ingreso_familiar_total": ingreso_total,
            "ingreso_per_capita": ingreso_per_capita,
            "dependientes_sin_ingreso": num_miembros - num_trabajando,
            "porcentaje_dependientes": round((num_miembros - num_trabajando) / num_miembros * 100, 2) if num_miembros > 0 else 0,
            "gasto_promedio_por_persona": round(random.uniform(2000, 6000), 2),
            "observaciones_familiares": "Familia estable con buena comunicación"
        }
    
    @classmethod
    def generar_situacion_financiera(cls) -> Dict[str, Any]:
        """Genera la sección de situación financiera."""
        ingreso = round(random.uniform(8000, 50000), 2)
        ahorros = round(random.uniform(500, 5000), 2)
        num_tarjetas = random.randint(0, 5)
        limite_credito = round(random.uniform(10000, 100000), 2) if num_tarjetas > 0 else 0
        deuda_tarjetas = round(random.uniform(0, limite_credito * 0.6), 2) if num_tarjetas > 0 else 0
        
        total_deudas = deuda_tarjetas + round(random.uniform(0, 50000), 2)
        porcentaje_ahorro = round((ahorros / ingreso * 100), 2) if ingreso > 0 else 0
        porcentaje_deudas = round((total_deudas / ingreso * 100), 2) if ingreso > 0 else 0
        
        # Generar gastos individuales
        gasto_alimentacion = round(random.uniform(2000, 6000), 2)
        gasto_salud = round(random.uniform(500, 2000), 2)
        gasto_educacion = round(random.uniform(500, 3000), 2)
        gasto_vivienda = round(random.uniform(1000, 5000), 2)
        gasto_transporte = round(random.uniform(500, 3000), 2)
        gasto_servicios = round(random.uniform(800, 2500), 2)
        gasto_otros = round(random.uniform(500, 2000), 2)
        
        total_gastos = gasto_alimentacion + gasto_salud + gasto_educacion + gasto_vivienda + gasto_transporte + gasto_servicios + gasto_otros
        
        return {
            # Campos para empleo (página tradicional)
            "trabaja_actualmente": True,
            "empresa_actual": random.choice(cls.EMPRESAS),
            "puesto_actual": random.choice(cls.PUESTOS),
            "sueldo_mensual": ingreso,
            "horario": "9:00 AM - 6:00 PM",
            # Campos de gastos
            "gastos": {
                "alimentacion": gasto_alimentacion,
                "salud": gasto_salud,
                "educacion": gasto_educacion,
                "vivienda": gasto_vivienda,
                "transporte": gasto_transporte,
                "servicios": gasto_servicios,
                "otros": gasto_otros,
                "total": total_gastos
            },
            "balance": ingreso - total_gastos,
            # Campos adicionales (calculados)
            "ingreso_total_mensual": ingreso,
            "monto_ahorros_mensuales": ahorros,
            "numero_cuentas_bancarias": random.randint(1, 4),
            "numero_tarjetas_credito": num_tarjetas,
            "limite_credito_total": limite_credito,
            "deuda_tarjetas_total": deuda_tarjetas,
            "monto_prestamos_personales": round(random.uniform(0, 50000), 2),
            "monto_hipoteca": round(random.uniform(0, 500000), 2) if random.random() > 0.6 else 0,
            "pago_mensual_hipoteca": round(random.uniform(3000, 15000), 2) if random.random() > 0.6 else 0,
            "monto_prestamo_auto": round(random.uniform(0, 200000), 2) if random.random() > 0.5 else 0,
            "pago_mensual_auto": round(random.uniform(2000, 8000), 2) if random.random() > 0.5 else 0,
            "monto_apoyos_gubernamentales": round(random.uniform(0, 3000), 2) if random.random() > 0.3 else 0,
            "gasto_promedio_comida_diaria": round(random.uniform(100, 500), 2),
            "gasto_mensual_medicamentos": round(random.uniform(0, 2000), 2),
            "gasto_mensual_gasolina": round(random.uniform(500, 3000), 2),
            "total_deudas": total_deudas,
            "total_pagos_mensuales_deudas": round(random.uniform(2000, 10000), 2),
            "porcentaje_ahorro": porcentaje_ahorro,
            "porcentaje_deudas_ingreso": porcentaje_deudas,
            "capacidad_pago": round(ingreso - total_deudas * 0.1, 2),
            "deudas": random.choice(["Tarjeta de crédito", "Préstamo personal", "Ninguna"]),
            "monto_deuda": total_deudas,
            "ingresos_adicionales": random.choice(["Ninguno", "Freelance", "Rentas", "Inversiones"]),
            "observaciones_financieras": "Situación financiera estable"
        }
    
    @classmethod
    def generar_vivienda(cls) -> Dict[str, Any]:
        """Genera la sección de vivienda."""
        num_habitaciones = random.randint(1, 5)
        num_banos = random.randint(1, 3)
        metros_cuadrados = round(random.uniform(40, 250), 2)
        num_personas = random.randint(2, 6)
        tenencia = random.choice(["Propia", "Rentada", "Prestada", "Pagándose"])
        
        return {
            # Campos para página tradicional
            "tipo_vivienda": random.choice(["Casa", "Departamento", "Cuarto rentado"]),
            "tenencia": tenencia,
            "tipo_zona": random.choice(["Urbana céntrica", "Urbana periférica", "Rural", "Suburbana", "Residencial"]),
            "materiales_construccion": "Concreto, ladrillo, techo de losa",
            "tiempo_residencia": f"{random.randint(1, 10)} años",
            "numero_cuartos": num_habitaciones,
            # Servicios (para checkboxes)
            "servicios": {
                "agua": True,
                "luz": True,
                "drenaje": True,
                "telefono": random.choice([True, False]),
                "internet": random.choice([True, False]),
                "transporte_publico": True,
                "pavimentacion": random.choice([True, False]),
                "areas_verdes": random.choice([True, False])
            },
            # Equipamiento (para spinboxes)
            "equipamiento": {
                "refrigerador": 1,
                "lavadora": 1,
                "estufa": 1,
                "televisor": random.randint(1, 3),
                "computadora": random.randint(0, 2),
                "microondas": 1
            },
            # Vehículos
            "vehiculos_cantidad": {
                "automovil": random.randint(0, 2),
                "motocicleta": random.randint(0, 1),
                "bicicleta": random.randint(0, 3)
            },
            # Campos adicionales (calculados)
            "regimen": tenencia,
            "costo_renta_mensual": round(random.uniform(3000, 15000), 2) if tenencia == "Rentada" else 0,
            "numero_habitaciones": num_habitaciones,
            "numero_banos": num_banos,
            "metros_cuadrados_construccion": metros_cuadrados,
            "indice_hacinamiento": round(num_personas / num_habitaciones, 2) if num_habitaciones > 0 else 0,
            "numero_servicios_basicos": random.randint(4, 7),
            "porcentaje_equipamiento": round(random.uniform(60, 100), 2),
            "electrodomesticos": ["Refrigerador", "Estufa", "Lavadora", "Microondas"],
            "condiciones_generales": random.choice(["Excelente", "Buena", "Regular", "Requiere mantenimiento"]),
            "valor_estimado_vivienda": round(random.uniform(500000, 3000000), 2),
            "antiguedad_vivienda_anos": random.randint(0, 30),
            "numero_propiedades_adicionales": random.randint(0, 2),
            "valor_propiedades_adicionales": round(random.uniform(0, 1000000), 2),
            "tiene_vehiculos": random.choice([True, False]),
            "valor_aproximado_vehiculos": round(random.uniform(50000, 300000), 2) if random.random() > 0.4 else 0,
            "observaciones_vivienda": "Vivienda en buenas condiciones"
        }
    
    @classmethod
    def generar_empleo_actual(cls) -> Dict[str, Any]:
        """Genera la sección de empleo actual."""
        salario_bruto = round(random.uniform(10000, 60000), 2)
        antiguedad = random.randint(1, 120)
        
        return {
            "empresa": random.choice(cls.EMPRESAS),
            "empresa_actual": random.choice(cls.EMPRESAS),
            "puesto": random.choice(cls.PUESTOS),
            "puesto_actual": random.choice(cls.PUESTOS),
            "antiguedad": f"{antiguedad // 12} años {antiguedad % 12} meses",
            "antiguedad_meses": antiguedad,
            "tipo_contrato": random.choice(cls.TIPOS_CONTRATO),
            "salario_mensual_bruto": salario_bruto,
            "salario_mensual_neto": round(salario_bruto * 0.85, 2),
            "numero_prestaciones": random.randint(3, 10),
            "prestaciones": ["Seguro médico", "Aguinaldo", "Vacaciones", "Prima vacacional"],
            "valor_prestaciones_anuales": round(salario_bruto * 2, 2),
            "horas_semanales": random.randint(40, 48),
            "dias_laborales_semana": random.randint(5, 6),
            "horario": "9:00 AM - 6:00 PM",
            "tiempo_traslado": f"{random.randint(15, 90)} minutos",
            "tiempo_traslado_minutos": random.randint(15, 90),
            "costo_mensual_transporte": round(random.uniform(500, 3000), 2),
            "tiene_home_office": random.choice([True, False]),
            "dias_home_office_semana": random.randint(0, 5),
            "jefe_inmediato": cls.generar_nombre_completo(),
            "telefono_empresa": cls.generar_telefono(),
            "satisfaccion_laboral": random.choice(["Muy satisfecho", "Satisfecho", "Neutral", "Insatisfecho"]),
            "calificacion_ultima_evaluacion": round(random.uniform(7.0, 10.0), 1),
            "recibe_bonos": random.choice([True, False]),
            "monto_promedio_bonos_anuales": round(random.uniform(5000, 30000), 2) if random.random() > 0.5 else 0,
            "observaciones_empleo": "Ambiente laboral positivo",
            "plan_carrera": "En desarrollo con evaluaciones anuales"
        }
    
    @classmethod
    def generar_historial_laboral(cls) -> list:
        """Genera empleos anteriores."""
        num_empleos = random.randint(1, 4)
        empleos = []
        
        for i in range(num_empleos):
            duracion_meses = random.randint(6, 60)
            empleos.append({
                "empresa": random.choice(cls.EMPRESAS),
                "puesto": random.choice(cls.PUESTOS),
                "duracion_meses": duracion_meses,
                "fecha_inicio": f"01/{random.randint(1,12)}/{random.randint(2010, 2022)}",
                "fecha_fin": f"01/{random.randint(1,12)}/{random.randint(2015, 2024)}",
                "salario": round(random.uniform(7000, 40000), 2),
                "motivo_salida": random.choice(["Mejor oferta", "Reubicación", "Fin de contrato", "Crecimiento profesional"]),
                "jefe": cls.generar_nombre_completo(),
                "contacto_jefe": cls.generar_telefono()
            })
        
        return empleos
    
    @classmethod
    def generar_estilo_vida(cls) -> Dict[str, Any]:
        """Genera la sección de estilo de vida."""
        num_hobbies = random.randint(2, 6)
        num_mascotas = random.randint(0, 3)
        
        return {
            "numero_hobbies": num_hobbies,
            "hobbies": ", ".join(random.sample(cls.HOBBIES, min(num_hobbies, len(cls.HOBBIES)))),
            "gasto_mensual_hobbies": round(random.uniform(500, 3000), 2),
            "actividades_culturales": random.choice(["Cine", "Teatro", "Museos", "Conciertos", "Ninguna"]),
            "frecuencia_salidas_mes": random.randint(2, 12),
            "gasto_promedio_por_salida": round(random.uniform(200, 1500), 2),
            "numero_viajes_ultimo_ano": random.randint(0, 5),
            "gasto_total_viajes_ano": round(random.uniform(0, 30000), 2),
            "frecuencia_actividades_culturales_mes": random.randint(0, 8),
            "gasto_mensual_cultura": round(random.uniform(0, 2000), 2),
            "practica_deporte": random.choice([True, False]),
            "frecuencia_ejercicio_semana": random.randint(0, 7),
            "deportes": ", ".join(random.sample(cls.DEPORTES, min(2, len(cls.DEPORTES)))),
            "gasto_mensual_gimnasio": round(random.uniform(0, 1500), 2),
            "pertenece_clubes": random.choice([True, False]),
            "numero_clubes_asociaciones": random.randint(0, 3),
            "costo_mensual_membrestas": round(random.uniform(0, 2000), 2),
            "tiene_mascotas": num_mascotas > 0,
            "numero_mascotas": num_mascotas,
            "tipo_mascotas": random.choice(["Perro", "Gato", "Ambos", "Otro"]) if num_mascotas > 0 else "Ninguna",
            "gasto_mensual_mascotas": round(random.uniform(500, 2000), 2) if num_mascotas > 0 else 0,
            "fuma": random.choice([True, False]),
            "gasto_mensual_tabaco": round(random.uniform(0, 1500), 2),
            "gasto_mensual_alcohol": round(random.uniform(0, 2000), 2)
        }
    
    @classmethod
    def generar_referencias(cls) -> list:
        """Genera referencias personales."""
        referencias = []
        for i in range(3):
            referencias.append({
                "nombre": cls.generar_nombre_completo(),
                "relacion": random.choice(["Amigo", "Familiar", "Colega", "Vecino"]),
                "tiempo_conocerse_meses": random.randint(12, 240),
                "telefono": cls.generar_telefono(),
                "ocupacion": random.choice(cls.PUESTOS),
                "observaciones": "Referencia confiable"
            })
        return referencias
    
    @classmethod
    def generar_estudio_completo(cls) -> Dict[str, Any]:
        """Genera un estudio socioeconómico completo con datos aleatorios."""
        return {
            "empresa_solicitante": random.choice(["TechCorp SA", "InnovaSoft", "Grupo Industrial MX"]),
            "datos_personales": cls.generar_datos_personales(),
            "salud_intereses": cls.generar_salud_intereses(),
            "informacion_familiar": cls.generar_informacion_familiar(),
            "situacion_financiera": cls.generar_situacion_financiera(),
            "vivienda": cls.generar_vivienda(),
            "empleo_actual": cls.generar_empleo_actual(),
            "historial_laboral": cls.generar_historial_laboral(),
            "estilo_vida": cls.generar_estilo_vida(),
            "referencias": cls.generar_referencias(),
            "conclusiones": (
                "FORTALEZAS: Candidato con buena estabilidad laboral y financiera. "
                "Perfil completo y verificable.\n\n"
                "ÁREAS DE MEJORA: Puede optimizar gastos mensuales y aumentar ahorro.\n\n"
                "RECOMENDACIÓN: VIABLE para contratación.\n\n"
                "OBSERVACIONES: Perfil profesional estable con buenos antecedentes."
            ),
            "fotografias": []
        }
