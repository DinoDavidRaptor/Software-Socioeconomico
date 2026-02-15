# Analisis Completo de Campos Duplicados - Software Socioeconomico

**Fecha:** 13 de febrero de 2026  
**Version:** 0.3.3

## Resumen Ejecutivo

Se identificaron **campos duplicados** entre paginas TRADICIONALES y MODULARES del wizard. Las paginas tradicionales contienen tablas y campos basicos, mientras que las modulares (con sufijo _ADICIONAL) agregan campos extras pero duplican algunos existentes.

---

## Estructura del Wizard (20 paginas)

| # | ID Pagina | Tipo | Descripcion | Archivo |
|---|-----------|------|-------------|---------|
| 0 | PAGE_EMPRESA | - | Selector de empresa solicitante | pagina_empresa.py |
| 1 | PAGE_DATOS_PERSONALES | Modular | Datos basicos del candidato | configuracion_campos.py |
| 2 | PAGE_SALUD | Modular | Informacion de salud | configuracion_campos.py |
| 3 | PAGE_FAMILIA | Tradicional | Tabla de miembros del hogar | paginas.py |
| 4 | PAGE_FAMILIA_ADICIONAL | Modular | Campos adicionales familia | configuracion_campos.py |
| 5 | PAGE_FINANZAS | Tradicional | Sueldo, gastos, prestamos | paginas_parte2.py |
| 6 | PAGE_FINANZAS_ADICIONAL | Modular | Ahorros, tarjetas, historial | configuracion_campos.py |
| 7 | PAGE_VIVIENDA | Tradicional | Datos basicos de vivienda | paginas_parte2.py |
| 8 | PAGE_VIVIENDA_ADICIONAL | Modular | Dimensiones, valor, propiedades | configuracion_campos.py |
| 9 | PAGE_EMPLEO_ACTUAL | Modular | Empleo actual detallado | configuracion_campos.py |
| 10 | PAGE_HISTORIAL | Tradicional | Historial laboral (tabla) | paginas.py |
| 11 | PAGE_ESTILO_VIDA | Modular | Estilo de vida y habitos | configuracion_campos.py |
| 12 | PAGE_REFERENCIAS | Tradicional | Referencias personales (tabla) | paginas.py |
| 13 | PAGE_VISUALIZACION | - | Graficas (no captura datos) | pagina_visualizacion.py |
| 14 | PAGE_VALIDACION_DOCUMENTAL | Modular | Verificacion de documentos | configuracion_campos.py |
| 15 | PAGE_INVESTIGACION_VECINAL | Modular | Investigacion con vecinos | configuracion_campos.py |
| 16 | PAGE_ANALISIS_CUALITATIVO | Modular | Analisis del investigador | configuracion_campos.py |
| 17 | PAGE_INVESTIGADOR | Modular | Datos del investigador | configuracion_campos.py |
| 18 | PAGE_CONCLUSIONES | Tradicional | Conclusion y recomendacion | paginas.py |
| 19 | PAGE_FOTOGRAFIAS | Tradicional | Fotos del estudio | paginas.py |

---

## DUPLICADOS IDENTIFICADOS

### 1. Informacion Familiar (PAGE_FAMILIA vs PAGE_FAMILIA_ADICIONAL)

**Campos en PAGE_FAMILIA (Tradicional - paginas.py):**
| Campo | Descripcion |
|-------|-------------|
| numero_hijos | Numero de hijos |
| numero_hijos_estudiando | Hijos que estudian |
| gasto_mensual_educacion_hijos | Gasto en educacion |
| miembros_hogar | TABLA de miembros |
| ingreso_familiar_total | Calculado |

**Campos en PAGE_FAMILIA_ADICIONAL (Modular - configuracion_campos.py):**
| Campo | Descripcion |
|-------|-------------|
| numero_hijos | Numero de hijos |
| numero_hijos_menores | Hijos menores de edad |
| numero_hijos_estudiando | Hijos que estudian |
| gasto_mensual_educacion_hijos | Gasto en educacion |
| total_miembros_hogar | Total personas en hogar |
| miembros_trabajando | Miembros con empleo |
| miembros_estudiando | Miembros estudiando |
| dependientes_sin_ingreso | Dependientes economicos |
| observaciones_familiares | Notas adicionales |

**DUPLICADOS:** `numero_hijos`, `numero_hijos_estudiando`, `gasto_mensual_educacion_hijos`

---

### 2. Situacion Financiera (PAGE_FINANZAS vs PAGE_FINANZAS_ADICIONAL)

**Campos en PAGE_FINANZAS (Tradicional - paginas_parte2.py):**
| Campo | Descripcion |
|-------|-------------|
| trabaja_actualmente | Checkbox empleo |
| empresa_actual | Nombre empresa |
| puesto_actual | Cargo |
| sueldo_mensual | Sueldo neto |
| horario | Horario trabajo |
| gasto_alimentacion | Gasto comida |
| gasto_salud | Gasto salud |
| gasto_educacion | Gasto educacion |
| gasto_recreacion | Gasto entretenimiento |
| gasto_vivienda | Gasto vivienda |
| gasto_transporte | Gasto transporte |
| gasto_servicios | Gasto servicios |
| gasto_otros | Otros gastos |
| tiene_prestamos_personales | Checkbox prestamos |
| monto_prestamos_personales | Monto prestamos |
| tiene_prestamo_hipotecario | Checkbox hipoteca |
| monto_hipoteca | Monto hipoteca |
| pago_mensual_hipoteca | Mensualidad hipoteca |
| tiene_prestamo_auto | Checkbox auto |
| monto_prestamo_auto | Monto prestamo auto |
| pago_mensual_auto | Mensualidad auto |
| observaciones_financieras | Notas |

**Campos en PAGE_FINANZAS_ADICIONAL (Modular - configuracion_campos.py):**
| Campo | Descripcion |
|-------|-------------|
| trabaja_actualmente | Checkbox empleo |
| empresa_actual | Nombre empresa |
| puesto_actual | Cargo |
| sueldo_mensual | Sueldo neto |
| ingresos_adicionales | Descripcion otros ingresos |
| otros_ingresos | Monto otros ingresos |
| ahorros | Ahorro acumulado |
| monto_ahorros_mensuales | Ahorro mensual |
| numero_cuentas_bancarias | Cuentas bancarias |
| cuentas_bancarias | Descripcion cuentas |
| numero_tarjetas_credito | Tarjetas credito |
| limite_credito_total | Limite tarjetas |
| deuda_tarjetas_total | Deuda tarjetas |
| tiene_prestamos_personales | Checkbox prestamos |
| monto_prestamos_personales | Monto prestamos |
| tiene_prestamo_hipotecario | Checkbox hipoteca |
| monto_hipoteca | Monto hipoteca |
| pago_mensual_hipoteca | Mensualidad hipoteca |
| tiene_prestamo_auto | Checkbox auto |
| monto_prestamo_auto | Monto prestamo auto |
| pago_mensual_auto | Mensualidad auto |
| apoyos_gubernamentales | Programas apoyo |
| monto_apoyos_gubernamentales | Monto apoyos |
| gasto_promedio_comida_diaria | Gasto diario comida |
| gasto_mensual_gasolina | Gasto gasolina |
| gastos_extraordinarios | Gastos especiales |
| historial_deudas | Historial pagos |
| observaciones_financieras | Notas |

**DUPLICADOS (13 campos):**
- `trabaja_actualmente`
- `empresa_actual`
- `puesto_actual`
- `sueldo_mensual`
- `tiene_prestamos_personales`
- `monto_prestamos_personales`
- `tiene_prestamo_hipotecario`
- `monto_hipoteca`
- `pago_mensual_hipoteca`
- `tiene_prestamo_auto`
- `monto_prestamo_auto`
- `pago_mensual_auto`
- `observaciones_financieras`

---

### 3. Vivienda (PAGE_VIVIENDA vs PAGE_VIVIENDA_ADICIONAL)

**Campos en PAGE_VIVIENDA (Tradicional - paginas_parte2.py):**
| Campo | Descripcion |
|-------|-------------|
| tipo_vivienda | Casa/Depto/etc |
| tenencia | Propia/Rentada/etc |
| tipo_zona | Tipo de zona |
| materiales_construccion | Materiales |
| tiempo_residencia | Tiempo viviendo |
| numero_cuartos | Cuartos totales |
| servicios | Agua/Luz/Drenaje (checkboxes) |
| equipamiento | Electrodomesticos (spinboxes) |
| vehiculos | Autos/Motos (spinboxes) |
| otras_propiedades | Otras propiedades |

**Campos en PAGE_VIVIENDA_ADICIONAL (Modular - configuracion_campos.py):**
| Campo | Descripcion |
|-------|-------------|
| tipo_vivienda | Casa/Depto/etc |
| tenencia | Propia/Rentada/etc |
| regimen | Regimen propiedad |
| tipo_zona | Tipo de zona |
| materiales_construccion | Materiales |
| tiempo_residencia | Tiempo viviendo |
| tiempo_viviendo_ahi | Tiempo en vivienda |
| numero_cuartos | Cuartos totales |
| numero_banos | Banos |
| numero_habitaciones | Recamaras |
| metros_cuadrados_construccion | Area |
| costo_renta_mensual | Renta |
| valor_estimado_vivienda | Valor comercial |
| antiguedad_vivienda_anos | Anos construccion |
| condiciones_generales | Estado vivienda |
| seguridad_entorno | Seguridad zona |
| otras_propiedades | Otras propiedades |
| numero_propiedades_adicionales | Cantidad propiedades |
| valor_propiedades_adicionales | Valor propiedades |

**DUPLICADOS (7 campos):**
- `tipo_vivienda`
- `tenencia`
- `tipo_zona`
- `materiales_construccion`
- `tiempo_residencia`
- `numero_cuartos`
- `otras_propiedades`

---

## TOTAL DE DUPLICADOS

| Seccion | Cantidad |
|---------|----------|
| Familia | 3 |
| Finanzas | 13 |
| Vivienda | 7 |
| **TOTAL** | **23** |

---

## PLAN DE CORRECCION

### Opcion Recomendada: Eliminar duplicados de paginas MODULARES

Los campos basicos ya existen en las paginas tradicionales. Las paginas ADICIONALES solo deben contener campos EXTRAS que complementen la informacion.

**Campos a ELIMINAR de configuracion_campos.py:**

#### obtener_campos_informacion_familiar():
- `numero_hijos`
- `numero_hijos_estudiando`
- `gasto_mensual_educacion_hijos`

#### obtener_campos_situacion_financiera():
- `trabaja_actualmente`
- `empresa_actual`
- `puesto_actual`
- `sueldo_mensual`
- `tiene_prestamos_personales`
- `monto_prestamos_personales`
- `tiene_prestamo_hipotecario`
- `monto_hipoteca`
- `pago_mensual_hipoteca`
- `tiene_prestamo_auto`
- `monto_prestamo_auto`
- `pago_mensual_auto`
- `observaciones_financieras`

#### obtener_campos_vivienda():
- `tipo_vivienda`
- `tenencia`
- `tipo_zona`
- `materiales_construccion`
- `tiempo_residencia`
- `numero_cuartos`
- `otras_propiedades`

---

## IMPACTO EN EXPORTADOR PDF

El exportador PDF (`src/export/exportador_pdf.py`) obtiene datos del objeto `estudio.datos` que es un diccionario compartido. Los campos duplicados se guardan en el mismo diccionario, por lo que el ultimo en guardar sobreescribe al anterior.

Despues de eliminar duplicados, los datos seguiran disponibles desde las paginas tradicionales.

---

## RESUMEN DE ACCIONES

1. Eliminar 23 campos duplicados de `configuracion_campos.py`
2. Verificar que el exportador PDF funcione correctamente
3. Probar el wizard completo para confirmar que no hay errores
