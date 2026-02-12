"""
Lógica de cálculo de riesgos socioeconómicos con justificaciones.
Autor: DINOS Tech
Versión: 0.2.0
"""

from typing import Dict, Tuple, List


class CalculadorRiesgos:
    """
    Clase para calcular indicadores de riesgo socioeconómico con justificaciones automáticas.
    Escala de riesgo: 1 (muy bajo) a 5 (muy alto)
    """
    
    @staticmethod
    def calcular_riesgo_financiero(datos: Dict) -> Tuple[int, List[str]]:
        """
        Calcula el riesgo financiero con justificaciones detalladas.
        
        Returns:
            Tupla (nivel_riesgo, lista_justificaciones)
        """
        fin = datos.get("situacion_financiera", {})
        justificaciones = []
        
        # Usar ingreso_total_mensual si está disponible, sino calcularlo
        ingreso_total = fin.get("ingreso_total_mensual", 0)
        if ingreso_total <= 0:
            # Calcular desde componentes
            sueldo = fin.get("sueldo_mensual", 0)
            otros_ingresos = sum(ing.get("monto", 0) for ing in fin.get("otros_ingresos", []) if isinstance(ing, dict))
            ingreso_total = sueldo + otros_ingresos
        
        if ingreso_total <= 0:
            justificaciones.append("Sin ingresos reportados")
            return 5, justificaciones
        
        gastos_totales = fin.get("gastos", {}).get("total", 0)
        balance = fin.get("balance", 0)
        # BUG 5 FIX: Use monto_ahorros_mensuales instead of ahorros
        ahorros = fin.get("monto_ahorros_mensuales", fin.get("ahorros", 0))
        
        # BUG 3 & 10 FIX: Properly aggregate all debts
        # First check if total_deudas is already calculated
        total_deudas = fin.get("total_deudas", 0)
        if total_deudas <= 0:
            # Aggregate from all debt sources
            deuda_tarjetas = fin.get("deuda_tarjetas_total", 0)
            prestamos_personales = fin.get("monto_prestamos_personales", 0)
            hipoteca = fin.get("monto_hipoteca", 0)
            prestamo_auto = fin.get("monto_prestamo_auto", 0)
            total_deudas = deuda_tarjetas + prestamos_personales + hipoteca + prestamo_auto
        
        # Manejar tanto deudas como lista como string
        deudas_raw = fin.get("deudas", [])
        if isinstance(deudas_raw, str):
            # BUG 10 FIX: Check for actual debt amounts in other fields
            if total_deudas > 0:
                # Count based on actual debt entries if available
                num_deudas = 0
                if fin.get("deuda_tarjetas_total", 0) > 0:
                    num_deudas += 1
                if fin.get("tiene_prestamos_personales") and fin.get("monto_prestamos_personales", 0) > 0:
                    num_deudas += 1
                if fin.get("tiene_prestamo_hipotecario") and fin.get("monto_hipoteca", 0) > 0:
                    num_deudas += 1
                if fin.get("tiene_prestamo_auto") and fin.get("monto_prestamo_auto", 0) > 0:
                    num_deudas += 1
                # If still no count but total_deudas > 0, count as 1
                if num_deudas == 0:
                    num_deudas = 1
                monto_deudas = total_deudas
            else:
                # Fallback: check if string has content
                num_deudas = 1 if deudas_raw.strip() and deudas_raw.strip().lower() not in ['none', 'n/a', ''] else 0
                monto_deudas = 0
        elif isinstance(deudas_raw, list):
            num_deudas = len(deudas_raw)
            monto_deudas = sum(d.get("monto", 0) for d in deudas_raw if isinstance(d, dict))
            # Also add other debt sources if not already included
            if total_deudas > monto_deudas:
                monto_deudas = total_deudas
        else:
            num_deudas = 0
            monto_deudas = total_deudas
        
        porcentaje_gastos = (gastos_totales / ingreso_total) * 100 if ingreso_total > 0 else 0
        
        riesgo = 1
        
        # Evaluar porcentaje de gastos vs ingresos
        if porcentaje_gastos < 50:
            riesgo = 1
            justificaciones.append(f"Gastos representan {porcentaje_gastos:.1f}% del ingreso (saludable)")
        elif porcentaje_gastos < 60:
            riesgo = 2
            justificaciones.append(f"Gastos representan {porcentaje_gastos:.1f}% del ingreso (aceptable)")
        elif porcentaje_gastos < 80:
            riesgo = 3
            justificaciones.append(f"Gastos representan {porcentaje_gastos:.1f}% del ingreso (ajustado)")
        elif porcentaje_gastos < 100:
            riesgo = 4
            justificaciones.append(f"Gastos representan {porcentaje_gastos:.1f}% del ingreso (crítico)")
        else:
            riesgo = 5
            justificaciones.append(f"Gastos exceden el ingreso ({porcentaje_gastos:.1f}%)")
        
        # Evaluar balance
        if balance < 0:
            riesgo = max(riesgo, 4)
            justificaciones.append(f"Balance negativo: ${balance:,.2f}")
        elif balance > ingreso_total * 0.2:
            justificaciones.append(f"Balance positivo saludable: ${balance:,.2f}")
        
        # Evaluar ahorros
        if ahorros == 0:
            riesgo = min(5, riesgo + 1)
            justificaciones.append("Sin ahorros reportados")
        elif ahorros < ingreso_total * 3:
            justificaciones.append(f"Ahorros limitados: ${ahorros:,.2f}")
        else:
            justificaciones.append(f"Cuenta con ahorros: ${ahorros:,.2f}")
        
        # Evaluar deudas
        if num_deudas > 3:
            riesgo = min(5, riesgo + 1)
            justificaciones.append(f"Múltiples deudas activas ({num_deudas})")
        elif num_deudas > 0:
            justificaciones.append(f"Tiene {num_deudas} deuda(s) por ${monto_deudas:,.2f}")
        
        proporcion_deuda = monto_deudas / (ingreso_total * 12) if ingreso_total > 0 else 0
        if proporcion_deuda > 0.5:
            riesgo = min(5, riesgo + 1)
            justificaciones.append(f"Deudas representan {proporcion_deuda*100:.1f}% del ingreso anual")
        
        # Verificar discrepancia de ingresos
        if fin.get("discrepancia_ingresos", False):
            justificaciones.append("Posible discrepancia entre ingresos declarados y reales")
        
        return int(round(riesgo)), justificaciones
    
    @staticmethod
    def calcular_riesgo_familiar(datos: Dict) -> Tuple[int, List[str]]:
        """
        Calcula el riesgo familiar con justificaciones detalladas.
        
        Returns:
            Tupla (nivel_riesgo, lista_justificaciones)
        """
        fam = datos.get("informacion_familiar", {})
        fin = datos.get("situacion_financiera", {})
        justificaciones = []
        
        num_hijos = fam.get("numero_hijos", 0)
        miembros = fam.get("miembros_hogar", [])
        num_miembros = len(miembros)
        dependientes_sin_ingreso = fam.get("dependientes_sin_ingreso", 0)
        
        # Contar aportantes
        aportantes = sum(1 for m in miembros if isinstance(m, dict) and (m.get("aporta_ingreso", False) or m.get("ingreso", 0) > 0))
        
        # Contar miembros con enfermedades crónicas
        con_enfermedades = sum(1 for m in miembros if isinstance(m, dict) and m.get("enfermedades_cronicas", "").strip())
        
        # Contar dependencia total
        dependencia_total = sum(1 for m in miembros if isinstance(m, dict) and m.get("dependencia_tipo", "") == "total")
        
        # BUG 6 FIX: Use pre-calculated ingreso_per_capita from JSON instead of recalculating
        ingreso_per_capita = fam.get("ingreso_per_capita", 0)
        if ingreso_per_capita <= 0:
            # Fallback calculation only if not available
            ingreso_total = fin.get("sueldo_mensual", 0) + sum(
                ing.get("monto", 0) for ing in fin.get("otros_ingresos", []) if isinstance(ing, dict)
            )
            ingreso_per_capita = ingreso_total / max(1, num_miembros) if num_miembros > 0 else ingreso_total
        else:
            ingreso_total = fam.get("ingreso_familiar_total", 0)
        
        riesgo = 1
        
        # Evaluar composición familiar
        if num_hijos == 0 and num_miembros <= 2:
            riesgo = 1
            justificaciones.append("Núcleo familiar pequeño sin dependientes menores")
        elif num_hijos <= 2 and num_miembros <= 4:
            riesgo = 2
            justificaciones.append(f"Familia de {num_miembros} integrantes con {num_hijos} hijo(s)")
        elif num_hijos <= 3 and num_miembros <= 5:
            riesgo = 3
            justificaciones.append(f"Familia numerosa: {num_miembros} integrantes, {num_hijos} hijos")
        else:
            riesgo = 4
            justificaciones.append(f"Familia extensa: {num_miembros} integrantes, {num_hijos} hijos")
        
        # Evaluar aportantes vs dependientes
        if num_miembros > 0:
            proporcion_aportantes = aportantes / num_miembros
            if proporcion_aportantes < 0.3:
                riesgo = min(5, riesgo + 1)
                justificaciones.append(f"Solo {aportantes} de {num_miembros} integrantes aportan ingreso")
            elif aportantes > 1:
                justificaciones.append(f"{aportantes} integrantes aportan ingreso al hogar")
        
        # Evaluar dependientes sin ingreso
        if dependientes_sin_ingreso > 3:
            riesgo = min(5, riesgo + 1)
            justificaciones.append(f"{dependientes_sin_ingreso} dependientes sin ingreso propio")
        elif dependientes_sin_ingreso > 0:
            justificaciones.append(f"{dependientes_sin_ingreso} dependiente(s) sin ingreso")
        
        # Evaluar ingreso per cápita
        if ingreso_per_capita < 2000:
            riesgo = min(5, riesgo + 1)
            justificaciones.append(f"Ingreso per cápita crítico: ${ingreso_per_capita:,.2f}")
        elif ingreso_per_capita < 3500:
            justificaciones.append(f"Ingreso per cápita ajustado: ${ingreso_per_capita:,.2f}")
        else:
            justificaciones.append(f"Ingreso per cápita adecuado: ${ingreso_per_capita:,.2f}")
        
        # Evaluar enfermedades crónicas
        if con_enfermedades > 0:
            riesgo = min(5, riesgo + 0.5)
            justificaciones.append(f"{con_enfermedades} integrante(s) con enfermedades crónicas")
        
        # Evaluar dependencia total
        if dependencia_total > 0:
            riesgo = min(5, riesgo + 0.5)
            justificaciones.append(f"{dependencia_total} integrante(s) con dependencia total")
        
        return int(round(riesgo)), justificaciones
    
    @staticmethod
    def calcular_riesgo_vivienda(datos: Dict) -> Tuple[int, List[str]]:
        """
        Calcula el riesgo de vivienda con justificaciones detalladas.
        
        Returns:
            Tupla (nivel_riesgo, lista_justificaciones)
        """
        viv = datos.get("vivienda", {})
        justificaciones = []
        
        tenencia = viv.get("tenencia", "").lower()
        tipo_zona = viv.get("tipo_zona", "").lower()
        servicios = viv.get("servicios", {})
        condicion = viv.get("condicion_fisica", {})
        num_cuartos = viv.get("numero_cuartos", 0)
        num_habitantes = viv.get("numero_habitantes", 0)
        seguridad = viv.get("seguridad_entorno", "").lower()
        
        # Contar servicios básicos
        servicios_basicos = {"agua", "luz", "drenaje"}
        servicios_disponibles = sum(1 for s in servicios_basicos if servicios.get(s, False))
        
        # Contar servicios adicionales
        servicios_adicionales = sum(1 for s in ["gas", "internet", "pavimentacion", "transporte_publico"] 
                                    if servicios.get(s, False))
        
        riesgo = 3  # Base media
        
        # Evaluar tenencia
        if "propia" in tenencia:
            riesgo -= 1
            justificaciones.append("Vivienda propia (estabilidad patrimonial)")
        elif "rentada" in tenencia or "renta" in tenencia:
            justificaciones.append("Vivienda rentada")
            renta = viv.get("renta_mensual", 0)
            if renta > 0:
                justificaciones.append(f"Renta mensual: ${renta:,.2f}")
        elif "prestada" in tenencia or "familiar" in tenencia:
            justificaciones.append("Vivienda prestada o familiar (sin patrimonio)")
        else:
            riesgo += 1
            justificaciones.append("Situación de tenencia irregular")
        
        # Evaluar servicios básicos
        if servicios_disponibles < 2:
            riesgo += 2
            justificaciones.append(f"Servicios básicos incompletos ({servicios_disponibles}/3)")
        elif servicios_disponibles < 3:
            riesgo += 1
            justificaciones.append(f"Carece de algún servicio básico ({servicios_disponibles}/3)")
        else:
            justificaciones.append("Cuenta con servicios básicos completos")
        
        # Evaluar servicios adicionales
        if servicios_adicionales == 0:
            justificaciones.append("Sin servicios adicionales")
        else:
            justificaciones.append(f"Cuenta con {servicios_adicionales} servicio(s) adicional(es)")
        
        # Evaluar condiciones físicas
        problemas = []
        if condicion.get("humedad", False):
            problemas.append("humedad")
        if condicion.get("filtraciones", False):
            problemas.append("filtraciones")
        if condicion.get("sobrecupo", False):
            problemas.append("sobrecupo")
        
        if len(problemas) > 0:
            riesgo = min(5, riesgo + 1)
            justificaciones.append(f"Problemas en la vivienda: {', '.join(problemas)}")
        else:
            justificaciones.append("Vivienda en buenas condiciones físicas")
        
        # Evaluar hacinamiento
        if num_cuartos > 0 and num_habitantes > 0:
            personas_por_cuarto = num_habitantes / num_cuartos
            if personas_por_cuarto > 3:
                riesgo = min(5, riesgo + 1)
                justificaciones.append(f"Hacinamiento crítico: {personas_por_cuarto:.1f} personas/cuarto")
            elif personas_por_cuarto > 2:
                riesgo = min(5, riesgo + 0.5)
                justificaciones.append(f"Sobrecupo: {personas_por_cuarto:.1f} personas/cuarto")
        
        # Evaluar seguridad del entorno
        if "inseguro" in seguridad or "peligroso" in seguridad or "alta" in seguridad:
            riesgo = min(5, riesgo + 1)
            justificaciones.append("Zona con problemas de seguridad")
        elif "seguro" in seguridad or "tranquilo" in seguridad:
            justificaciones.append("Entorno seguro")
        
        # Evaluar tipo de zona
        if "marginada" in tipo_zona or "irregular" in tipo_zona:
            riesgo = min(5, riesgo + 1)
            justificaciones.append("Zona marginada o asentamiento irregular")
        elif "residencial" in tipo_zona or "centrica" in tipo_zona:
            riesgo = max(1, riesgo - 0.5)
            justificaciones.append("Zona bien ubicada")
        
        riesgo = max(1, min(5, riesgo))
        return int(round(riesgo)), justificaciones
    
    @staticmethod
    def calcular_riesgo_laboral(datos: Dict) -> Tuple[int, List[str]]:
        """
        Calcula el riesgo laboral con justificaciones detalladas.
        
        Returns:
            Tupla (nivel_riesgo, lista_justificaciones)
        """
        fin = datos.get("situacion_financiera", {})
        empleo = datos.get("empleo_actual", {})
        hist = datos.get("historial_laboral", [])
        justificaciones = []
        
        trabaja = fin.get("trabaja_actualmente", False)
        
        if not trabaja:
            justificaciones.append("Sin empleo actual")
            return 5, justificaciones
        
        antiguedad = empleo.get("antiguedad", "")
        tipo_contrato = empleo.get("tipo_contrato", "").lower()
        prestaciones = empleo.get("prestaciones", [])
        
        num_empleos = len(hist)
        riesgo = 1
        
        # Evaluar empleo actual
        justificaciones.append(f"Empleo actual: {fin.get('puesto_actual', 'No especificado')}")
        
        # Evaluar antigüedad
        if antiguedad:
            if "año" in antiguedad.lower() or "años" in antiguedad.lower():
                try:
                    anos = int(''.join(filter(str.isdigit, antiguedad.split()[0]))) if antiguedad else 0
                    if anos >= 3:
                        justificaciones.append(f"Antigüedad considerable: {antiguedad}")
                    elif anos >= 1:
                        riesgo += 0.5
                        justificaciones.append(f"Antigüedad moderada: {antiguedad}")
                    else:
                        riesgo += 1
                        justificaciones.append(f"Antigüedad reciente: {antiguedad}")
                except:
                    justificaciones.append(f"Antigüedad: {antiguedad}")
        else:
            riesgo += 1
            justificaciones.append("Antigüedad no especificada")
        
        # Evaluar tipo de contrato
        if "indefinido" in tipo_contrato or "planta" in tipo_contrato:
            justificaciones.append("Contrato indefinido (estabilidad)")
        elif "temporal" in tipo_contrato or "honorarios" in tipo_contrato:
            riesgo += 1
            justificaciones.append("Contrato temporal o por honorarios")
        elif tipo_contrato:
            justificaciones.append(f"Tipo de contrato: {tipo_contrato}")
        
        # Evaluar prestaciones
        if len(prestaciones) >= 5:
            justificaciones.append(f"Prestaciones completas ({len(prestaciones)} prestaciones)")
        elif len(prestaciones) >= 3:
            justificaciones.append(f"Prestaciones básicas ({len(prestaciones)} prestaciones)")
        elif len(prestaciones) > 0:
            riesgo += 0.5
            justificaciones.append(f"Prestaciones limitadas ({len(prestaciones)} prestaciones)")
        else:
            riesgo += 1
            justificaciones.append("Sin prestaciones reportadas")
        
        # Evaluar historial laboral
        if num_empleos == 0:
            justificaciones.append("Primer empleo o sin historial previo")
        elif num_empleos <= 2:
            justificaciones.append(f"Historial estable: {num_empleos} empleo(s) anterior(es)")
        elif num_empleos <= 4:
            riesgo += 0.5
            justificaciones.append(f"Varios cambios de empleo: {num_empleos} trabajos anteriores")
        else:
            riesgo += 1
            justificaciones.append(f"Alta rotación laboral: {num_empleos} empleos anteriores")
        
        # Evaluar duraciones y motivos de salida
        empleos_cortos = 0
        motivos_negativos = 0
        
        for empleo_prev in hist:
            motivo = empleo_prev.get("motivo_separacion", "").lower()
            
            # Detectar motivos negativos
            if any(palabra in motivo for palabra in ["despido", "conflicto", "renuncia forzada", "liquidado"]):
                motivos_negativos += 1
            
            # Calcular duración si hay fechas
            fecha_inicio = empleo_prev.get("fecha_inicio", "")
            fecha_fin = empleo_prev.get("fecha_fin", "")
            
            # Simplificación: si menciona "meses" y es menos de 6, es corto
            if "mes" in fecha_inicio or "mes" in fecha_fin:
                try:
                    # Intentar extraer número de meses
                    if any(str(i) in (fecha_inicio + fecha_fin) for i in range(1, 7)):
                        empleos_cortos += 1
                except:
                    pass
        
        if motivos_negativos > 0:
            riesgo = min(5, riesgo + 1)
            justificaciones.append(f"{motivos_negativos} salida(s) con motivo negativo")
        
        if empleos_cortos >= 2:
            riesgo = min(5, riesgo + 0.5)
            justificaciones.append(f"{empleos_cortos} empleo(s) de corta duración")
        
        riesgo = max(1, min(5, riesgo))
        return int(round(riesgo)), justificaciones
    
    @staticmethod
    def calcular_riesgo_global(datos: Dict) -> Tuple[int, List[str]]:
        """
        Calcula el riesgo socioeconómico global con justificaciones.
        
        Returns:
            Tupla (nivel_riesgo, lista_justificaciones)
        """
        # Calcular cada riesgo individual
        riesgo_fin, just_fin = CalculadorRiesgos.calcular_riesgo_financiero(datos)
        riesgo_fam, just_fam = CalculadorRiesgos.calcular_riesgo_familiar(datos)
        riesgo_viv, just_viv = CalculadorRiesgos.calcular_riesgo_vivienda(datos)
        riesgo_lab, just_lab = CalculadorRiesgos.calcular_riesgo_laboral(datos)
        
        # Ponderar: financiero 35%, familiar 25%, vivienda 20%, laboral 20%
        riesgo_global = (
            riesgo_fin * 0.35 +
            riesgo_fam * 0.25 +
            riesgo_viv * 0.20 +
            riesgo_lab * 0.20
        )
        
        justificaciones = [
            f"Riesgo financiero: {riesgo_fin}/5",
            f"Riesgo familiar: {riesgo_fam}/5",
            f"Riesgo vivienda: {riesgo_viv}/5",
            f"Riesgo laboral: {riesgo_lab}/5",
            f"Promedio ponderado: {riesgo_global:.2f}/5"
        ]
        
        # Identificar áreas críticas
        areas_criticas = []
        if riesgo_fin >= 4:
            areas_criticas.append("financiera")
        if riesgo_fam >= 4:
            areas_criticas.append("familiar")
        if riesgo_viv >= 4:
            areas_criticas.append("vivienda")
        if riesgo_lab >= 4:
            areas_criticas.append("laboral")
        
        if areas_criticas:
            justificaciones.append(f"Áreas críticas: {', '.join(areas_criticas)}")
        
        return int(round(riesgo_global)), justificaciones
    
    @staticmethod
    def calcular_todos_riesgos(datos: Dict) -> Dict:
        """
        Calcula todos los riesgos y retorna estructura completa con justificaciones.
        
        Returns:
            Diccionario con estructura {categoria: {puntaje: int, justificaciones: List[str]}}
        """
        calc = CalculadorRiesgos(datos)
        
        riesgo_fin, just_fin = calc.calcular_riesgo_financiero(datos)
        riesgo_fam, just_fam = calc.calcular_riesgo_familiar(datos)
        riesgo_viv, just_viv = calc.calcular_riesgo_vivienda(datos)
        riesgo_lab, just_lab = calc.calcular_riesgo_laboral(datos)
        riesgo_sal, just_sal = calc.calcular_riesgo_salud(datos)
        riesgo_est, just_est = calc.calcular_riesgo_estilo_vida(datos)
        riesgo_glo, just_glo = calc.calcular_riesgo_global(datos)
        
        return {
            "financiero": {"puntaje": riesgo_fin, "justificaciones": just_fin},
            "familiar": {"puntaje": riesgo_fam, "justificaciones": just_fam},
            "vivienda": {"puntaje": riesgo_viv, "justificaciones": just_viv},
            "laboral": {"puntaje": riesgo_lab, "justificaciones": just_lab},
            "salud": {"puntaje": riesgo_sal, "justificaciones": just_sal},
            "estilo_vida": {"puntaje": riesgo_est, "justificaciones": just_est},
            "global": {"puntaje": riesgo_glo, "justificaciones": just_glo}
        }
    
    @staticmethod
    def calcular_riesgo_salud(datos: Dict) -> Tuple[int, List[str]]:
        """Calcula el riesgo relacionado con salud."""
        salud = datos.get("salud_intereses", {})
        justificaciones = []
        riesgo = 1
        
        # BUG 2 FIX: Use numero_enfermedades_cronicas field directly, not count string
        enfermedades = salud.get("enfermedades_cronicas", [])
        if isinstance(enfermedades, list):
            num_enf = len(enfermedades)
        else:
            # If it's a string, use the pre-calculated count field
            num_enf = salud.get("numero_enfermedades_cronicas", 0)
        
        if num_enf > 0:
            riesgo = min(5, 2 + num_enf)
            justificaciones.append(f"{num_enf} enfermedad(es) crónica(s) reportada(s)")
            
            sin_tratamiento = [e for e in enfermedades if isinstance(e, dict) and not e.get("tratamiento")]
            if sin_tratamiento:
                riesgo = min(5, riesgo + 1)
                justificaciones.append(f"{len(sin_tratamiento)} enfermedad(es) sin tratamiento")
        
        # Consumo de sustancias
        if salud.get("fuma"):
            freq = salud.get("frecuencia_tabaco", "")
            if freq in ["Diario", "Frecuente"]:
                riesgo = min(5, riesgo + 1)
                justificaciones.append(f"Consumo de tabaco {freq.lower()}")
        
        if salud.get("consume_alcohol"):
            freq = salud.get("frecuencia_alcohol", "")
            if freq in ["Diario", "Frecuente"]:
                riesgo = min(5, riesgo + 1)
                justificaciones.append(f"Consumo de alcohol {freq.lower()}")
        
        if salud.get("consume_otras_sustancias"):
            riesgo = 5
            justificaciones.append("Consumo de otras sustancias reportado")
        
        # Estado general
        estado = salud.get("estado_salud", "")
        if estado == "Malo":
            riesgo = min(5, riesgo + 2)
            justificaciones.append("Estado de salud general: Malo")
        elif estado == "Regular":
            riesgo = min(5, riesgo + 1)
            justificaciones.append("Estado de salud general: Regular")
        
        if not justificaciones:
            justificaciones.append("Sin problemas de salud significativos")
        
        return riesgo, justificaciones
    
    @staticmethod
    def calcular_riesgo_estilo_vida(datos: Dict) -> Tuple[int, List[str]]:
        """Calcula el riesgo relacionado con estilo de vida."""
        estilo = datos.get("estilo_vida", {})
        vivienda = datos.get("vivienda", {})
        salud = datos.get("salud_intereses", {})
        justificaciones = []
        riesgo = 1
        
        # BUG FIX: Verificar vehículo en vivienda.vehiculos o vivienda.tiene_vehiculos
        tiene_vehiculo = vivienda.get("tiene_vehiculos", False)
        if not tiene_vehiculo:
            vehiculos = vivienda.get("vehiculos", {})
            if isinstance(vehiculos, dict):
                tiene_vehiculo = any(v > 0 for v in vehiculos.values() if isinstance(v, (int, float)))
        
        if not tiene_vehiculo:
            riesgo = min(5, riesgo + 1)
            justificaciones.append("Sin vehículo propio")
        else:
            justificaciones.append("Cuenta con vehículo propio")
        
        # BUG FIX: Verificar numero_viajes_ultimo_ano > 0 en lugar de boolean
        num_viajes = estilo.get("numero_viajes_ultimo_ano", 0)
        if num_viajes <= 0:
            justificaciones.append("Sin viajes recreativos en el último año")
        else:
            justificaciones.append(f"Viajes en el último año: {num_viajes}")
        
        # Hobbies y actividades
        hobbies = estilo.get("hobbies", "")
        num_hobbies = estilo.get("numero_hobbies", 0)
        if not hobbies and num_hobbies <= 0:
            riesgo = min(5, riesgo + 1)
            justificaciones.append("Sin hobbies o actividades recreativas reportadas")
        else:
            justificaciones.append(f"Hobbies activos: {num_hobbies}")
        
        # BUG FIX: Verificar pertenece_clubes en lugar de pertenece_asociaciones
        pertenece_clubes = estilo.get("pertenece_clubes", False)
        num_clubes = estilo.get("numero_clubes_asociaciones", 0)
        if not pertenece_clubes and num_clubes <= 0:
            justificaciones.append("Sin membresía en asociaciones o clubes")
        else:
            justificaciones.append(f"Membresías activas: {num_clubes}")
        
        # Evaluar actividad física
        freq_ejercicio = estilo.get("frecuencia_ejercicio_semana", 0)
        if freq_ejercicio >= 3:
            justificaciones.append(f"Actividad física regular ({freq_ejercicio} veces/semana)")
        elif freq_ejercicio > 0:
            justificaciones.append(f"Actividad física moderada ({freq_ejercicio} veces/semana)")
        
        # Evaluar consumo de tabaco
        fuma = estilo.get("fuma", False)
        if not fuma:
            justificaciones.append("No fuma")
        else:
            riesgo = min(5, riesgo + 1)
            justificaciones.append("Consumo de tabaco activo")
        
        # Mascotas (indicador de estabilidad)
        if estilo.get("tiene_mascotas"):
            num_mascotas = estilo.get("numero_mascotas", 0)
            justificaciones.append(f"Tiene mascotas ({num_mascotas})")
        
        return riesgo, justificaciones
    
    @staticmethod
    def obtener_interpretacion_riesgo(nivel: int) -> str:
        """
        Retorna la interpretación textual del nivel de riesgo.
        
        Args:
            nivel: Nivel de riesgo de 1 a 5
            
        Returns:
            Interpretación textual del riesgo
        """
        interpretaciones = {
            1: "Muy Bajo - Situación muy favorable",
            2: "Bajo - Situación favorable",
            3: "Medio - Situación aceptable con precauciones",
            4: "Alto - Situación que requiere atención",
            5: "Muy Alto - Situación crítica que requiere acción inmediata"
        }
        
        return interpretaciones.get(nivel, "Sin evaluar")
    
    def __init__(self, datos: Dict):
        """Inicializa el calculador con los datos del estudio."""
        self.datos = datos

