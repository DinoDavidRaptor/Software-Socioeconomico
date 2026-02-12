"""
Sistema de validación y detección de alertas para estudios socioeconómicos.
Autor: DINOS Tech
Versión: 0.2.0
"""

from typing import Dict, List, Tuple


class ValidadorEstudio:
    """
    Clase para validar datos y detectar contradicciones o alertas en estudios.
    """
    
    @staticmethod
    def validar_estudio_completo(datos: Dict) -> Dict:
        """
        Ejecuta todas las validaciones y retorna un dict con alertas detectadas.
        
        Returns:
            Dict con: {
                'gastos_excesivos': bool,
                'contradicciones': List[str],
                'dependientes_sin_ingreso_detectado': bool,
                'discrepancia_ingresos': bool,
                'alertas_generales': List[str]
            }
        """
        resultado = {
            "gastos_excesivos": False,
            "contradicciones": [],
            "dependientes_sin_ingreso_detectado": False,
            "discrepancia_ingresos": False,
            "alertas_generales": []
        }
        
        # Validar finanzas
        alertas_fin = ValidadorEstudio._validar_finanzas(datos)
        resultado["gastos_excesivos"] = alertas_fin["gastos_excesivos"]
        resultado["contradicciones"].extend(alertas_fin["contradicciones"])
        resultado["discrepancia_ingresos"] = alertas_fin["discrepancia_ingresos"]
        resultado["alertas_generales"].extend(alertas_fin["alertas"])
        
        # Validar familia
        alertas_fam = ValidadorEstudio._validar_familia(datos)
        resultado["dependientes_sin_ingreso_detectado"] = alertas_fam["dependientes_sin_ingreso"]
        resultado["contradicciones"].extend(alertas_fam["contradicciones"])
        resultado["alertas_generales"].extend(alertas_fam["alertas"])
        
        # Validar vivienda
        alertas_viv = ValidadorEstudio._validar_vivienda(datos)
        resultado["contradicciones"].extend(alertas_viv["contradicciones"])
        resultado["alertas_generales"].extend(alertas_viv["alertas"])
        
        # Validar empleo
        alertas_emp = ValidadorEstudio._validar_empleo(datos)
        resultado["contradicciones"].extend(alertas_emp["contradicciones"])
        resultado["alertas_generales"].extend(alertas_emp["alertas"])
        
        return resultado
    
    @staticmethod
    def _validar_finanzas(datos: Dict) -> Dict:
        """Valida la sección financiera."""
        fin = datos.get("situacion_financiera", {})
        alertas = []
        contradicciones = []
        
        sueldo = fin.get("sueldo_mensual", 0)
        otros_ingresos = sum(ing.get("monto", 0) for ing in fin.get("otros_ingresos", []) if isinstance(ing, dict))
        ingreso_total = sueldo + otros_ingresos
        
        gastos_totales = fin.get("gastos", {}).get("total", 0)
        
        # Calcular porcentaje de gastos
        porcentaje = (gastos_totales / ingreso_total * 100) if ingreso_total > 0 else 0
        gastos_excesivos = porcentaje > 80
        
        if gastos_excesivos:
            alertas.append(f"ALERTA: Gastos representan {porcentaje:.1f}% del ingreso (>80%)")
        
        # Verificar balance vs cálculo
        balance_declarado = fin.get("balance", 0)
        balance_calculado = ingreso_total - gastos_totales
        
        if abs(balance_declarado - balance_calculado) > 100:
            contradicciones.append(
                f"Balance declarado (${balance_declarado:,.2f}) no coincide con cálculo "
                f"(${balance_calculado:,.2f})"
            )
        
        # Detectar discrepancia de ingresos
        discrepancia = False
        ahorros = fin.get("ahorros", 0)
        
        # Si tiene ahorros altos pero ingreso bajo, puede haber discrepancia
        if ahorros > ingreso_total * 12 and ingreso_total < 10000:
            discrepancia = True
            alertas.append(
                f"Posible discrepancia: Ahorros (${ahorros:,.2f}) muy altos "
                f"para ingreso mensual de ${ingreso_total:,.2f}"
            )
        
        # Verificar trabajo vs ingreso
        trabaja = fin.get("trabaja_actualmente", False)
        if trabaja and sueldo == 0:
            contradicciones.append("Indica que trabaja actualmente pero no reporta sueldo")
        elif not trabaja and sueldo > 0:
            contradicciones.append("Indica que no trabaja pero reporta sueldo mensual")
        
        # Verificar deudas vs balance
        deudas = fin.get("deudas", [])
        monto_deudas = sum(d.get("monto", 0) for d in deudas if isinstance(d, dict))
        
        if len(deudas) > 0 and monto_deudas == 0:
            contradicciones.append("Reporta deudas pero sin montos especificados")
        
        return {
            "gastos_excesivos": gastos_excesivos,
            "discrepancia_ingresos": discrepancia,
            "contradicciones": contradicciones,
            "alertas": alertas
        }
    
    @staticmethod
    def _validar_familia(datos: Dict) -> Dict:
        """Valida la sección familiar."""
        fam = datos.get("informacion_familiar", {})
        alertas = []
        contradicciones = []
        
        num_hijos = fam.get("numero_hijos", 0)
        miembros = fam.get("miembros_hogar", [])
        
        # Contar menores de edad
        menores = sum(1 for m in miembros if isinstance(m, dict) and m.get("edad", 99) < 18)
        
        if num_hijos != menores and menores > 0:
            contradicciones.append(
                f"Número de hijos declarado ({num_hijos}) no coincide "
                f"con menores de edad en listado ({menores})"
            )
        
        # Contar dependientes sin ingreso
        sin_ingreso = 0
        for m in miembros:
            aporta = m.get("aporta_ingreso", False)
            ingreso = m.get("ingreso", 0)
            edad = m.get("edad", 0)
            estudia_trabaja = m.get("estudia_trabaja", "").lower()
            
            if not aporta and ingreso == 0 and edad >= 18:
                sin_ingreso += 1
            
            # Contradicción: dice que trabaja pero no aporta ingreso
            if "trabaja" in estudia_trabaja and not aporta and ingreso == 0:
                nombre = m.get("nombre", "integrante")
                contradicciones.append(
                    f"{nombre} indica que trabaja pero no reporta ingreso"
                )
        
        dependientes_detectado = sin_ingreso > 0
        
        if sin_ingreso > 3:
            alertas.append(f"ALERTA: {sin_ingreso} dependientes mayores de edad sin ingreso")
        elif sin_ingreso > 0:
            alertas.append(f"{sin_ingreso} dependiente(s) mayor(es) de edad sin ingreso")
        
        # Verificar ingreso familiar total vs suma
        ingreso_declarado = fam.get("ingreso_familiar_total", 0)
        ingreso_calculado = sum(m.get("ingreso", 0) for m in miembros if isinstance(m, dict))
        
        # Agregar ingreso del candidato
        fin = datos.get("situacion_financiera", {})
        ingreso_calculado += fin.get("sueldo_mensual", 0)
        ingreso_calculado += sum(ing.get("monto", 0) for ing in fin.get("otros_ingresos", []) if isinstance(ing, dict))
        
        if ingreso_declarado > 0 and abs(ingreso_declarado - ingreso_calculado) > 500:
            contradicciones.append(
                f"Ingreso familiar declarado (${ingreso_declarado:,.2f}) difiere "
                f"de la suma de ingresos individuales (${ingreso_calculado:,.2f})"
            )
        
        return {
            "dependientes_sin_ingreso": dependientes_detectado,
            "contradicciones": contradicciones,
            "alertas": alertas
        }
    
    @staticmethod
    def _validar_vivienda(datos: Dict) -> Dict:
        """Valida la sección de vivienda."""
        viv = datos.get("vivienda", {})
        alertas = []
        contradicciones = []
        
        tenencia = viv.get("tenencia", "").lower()
        renta = viv.get("renta_mensual", 0)
        
        # Verificar renta vs tenencia
        if ("propia" in tenencia or "pagando" in tenencia) and renta > 0:
            contradicciones.append("Indica vivienda propia pero reporta renta mensual")
        elif "rentada" in tenencia and renta == 0:
            alertas.append("Vivienda rentada sin monto de renta especificado")
        
        # Verificar hacinamiento
        num_cuartos = viv.get("numero_cuartos", 0)
        num_habitantes = viv.get("numero_habitantes", 0)
        
        if num_habitantes == 0:
            # Intentar obtener de miembros del hogar
            miembros = datos.get("informacion_familiar", {}).get("miembros_hogar", [])
            num_habitantes = len(miembros) + 1  # +1 por el candidato
        
        if num_cuartos > 0 and num_habitantes > 0:
            personas_por_cuarto = num_habitantes / num_cuartos
            if personas_por_cuarto > 3:
                alertas.append(
                    f"ALERTA: Hacinamiento severo - {personas_por_cuarto:.1f} personas por cuarto"
                )
            elif personas_por_cuarto > 2:
                alertas.append(f"Sobrecupo - {personas_por_cuarto:.1f} personas por cuarto")
        
        # Verificar servicios básicos
        servicios = viv.get("servicios", {})
        sin_servicios = []
        for servicio in ["agua", "luz", "drenaje"]:
            if not servicios.get(servicio, False):
                sin_servicios.append(servicio)
        
        if len(sin_servicios) > 0:
            alertas.append(f"ALERTA: Sin servicios básicos: {', '.join(sin_servicios)}")
        
        # Verificar condiciones físicas
        condicion = viv.get("condicion_fisica", {})
        problemas = []
        if condicion.get("humedad", False):
            problemas.append("humedad")
        if condicion.get("filtraciones", False):
            problemas.append("filtraciones")
        if condicion.get("sobrecupo", False):
            problemas.append("sobrecupo")
        
        if len(problemas) >= 2:
            alertas.append(f"ALERTA: Múltiples problemas en vivienda: {', '.join(problemas)}")
        
        return {
            "contradicciones": contradicciones,
            "alertas": alertas
        }
    
    @staticmethod
    def _validar_empleo(datos: Dict) -> Dict:
        """Valida la sección de empleo."""
        fin = datos.get("situacion_financiera", {})
        empleo = datos.get("empleo_actual", {})
        alertas = []
        contradicciones = []
        
        trabaja = fin.get("trabaja_actualmente", False)
        
        if trabaja:
            empresa_fin = fin.get("empresa_actual", "")
            empresa_emp = empleo.get("empresa", "")
            
            if empresa_fin and empresa_emp and empresa_fin != empresa_emp:
                contradicciones.append(
                    f"Empresa actual difiere entre secciones: '{empresa_fin}' vs '{empresa_emp}'"
                )
            
            puesto_fin = fin.get("puesto_actual", "")
            puesto_emp = empleo.get("puesto", "")
            
            if puesto_fin and puesto_emp and puesto_fin != puesto_emp:
                contradicciones.append(
                    f"Puesto actual difiere entre secciones: '{puesto_fin}' vs '{puesto_emp}'"
                )
            
            # Verificar prestaciones vs tipo de contrato
            tipo_contrato = empleo.get("tipo_contrato", "").lower()
            prestaciones = empleo.get("prestaciones", [])
            
            if ("honorarios" in tipo_contrato or "temporal" in tipo_contrato) and len(prestaciones) > 3:
                alertas.append(
                    "Contrato temporal/honorarios con prestaciones extensas (revisar)"
                )
        
        # Verificar historial laboral
        hist = datos.get("historial_laboral", [])
        
        if len(hist) > 5:
            # Calcular promedio de tiempo en cada empleo
            empleos_cortos = sum(1 for e in hist 
                                if "mes" in str(e.get("fecha_inicio", "")).lower() 
                                or "mes" in str(e.get("fecha_fin", "")).lower())
            
            if empleos_cortos >= len(hist) * 0.6:  # Más del 60% son cortos
                alertas.append(
                    f"ALERTA: Alta rotación laboral - {empleos_cortos} de {len(hist)} "
                    f"empleos con duración menor a 1 año"
                )
        
        return {
            "contradicciones": contradicciones,
            "alertas": alertas
        }
    
    @staticmethod
    def obtener_resumen_validacion(resultado_validacion: Dict) -> str:
        """
        Genera un resumen legible de las validaciones.
        
        Args:
            resultado_validacion: Dict retornado por validar_estudio_completo
            
        Returns:
            String con resumen formateado
        """
        lineas = []
        
        if resultado_validacion["gastos_excesivos"]:
            lineas.append("ALERTA CRÍTICA: Gastos exceden el 80% del ingreso")
        
        if resultado_validacion["dependientes_sin_ingreso_detectado"]:
            lineas.append("ALERTA: Dependientes sin ingreso detectados")
        
        if resultado_validacion["discrepancia_ingresos"]:
            lineas.append("ALERTA: Posible discrepancia en ingresos declarados")
        
        contradicciones = resultado_validacion["contradicciones"]
        if len(contradicciones) > 0:
            lineas.append(f"\nCONTRADICCIONES DETECTADAS ({len(contradicciones)}):")
            for i, c in enumerate(contradicciones, 1):
                lineas.append(f"  {i}. {c}")
        
        alertas = resultado_validacion["alertas_generales"]
        if len(alertas) > 0:
            lineas.append(f"\nALERTAS GENERALES ({len(alertas)}):")
            for i, a in enumerate(alertas, 1):
                lineas.append(f"  {i}. {a}")
        
        if len(lineas) == 0:
            return "No se detectaron alertas ni contradicciones"
        
        return "\n".join(lineas)
