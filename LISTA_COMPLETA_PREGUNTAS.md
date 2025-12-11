# LISTA COMPLETA DE PREGUNTAS Y DATOS CAPTURADOS
## Software de Estudios Socioeconómicos v0.2.0

**DINOS Tech** - 9 de diciembre de 2025

---

## RESUMEN EJECUTIVO

El sistema captura **230+ campos de información** organizados en **11 secciones** para realizar análisis socioeconómicos exhaustivos y profesionales.

### CAMPOS POR CATEGORÍA:
- ✅ Datos Personales: **19 campos**
- ✅ Salud: **20 campos** (13 descriptivos + 7 cuantitativos)
- ✅ Familia: **14 campos** (8 base + listas dinámicas)
- ✅ Finanzas: **35 campos** (25+ cuantitativos)
- ✅ Vivienda: **40 campos** (30+ incluyendo equipamiento)
- ✅ Empleo Actual: **23 campos** (15+ cuantitativos)
- ✅ Historial Laboral: **Lista dinámica** con 13 campos por empleo
- ✅ Estilo de Vida: **24 campos** (20+ cuantitativos)
- ✅ Referencias: **Lista dinámica** con 6 campos por referencia
- ✅ Conclusiones: **Texto libre del evaluador**
- ✅ Fotografías: **Lista de archivos adjuntos**

**TOTAL: 230+ campos individuales + listas dinámicas**

---

## SECCIÓN 1: DATOS PERSONALES (19 CAMPOS)

### Identificación Básica
1. **Nombre Completo** (Texto, REQUERIDO)
   - Apellido Paterno + Apellido Materno + Nombre(s)

2. **Fecha de Nacimiento** (Fecha, REQUERIDO)
   - Para cálculo automático de edad

3. **Edad** (Número, REQUERIDO)
   - Años cumplidos

4. **Nacionalidad** (Texto, REQUERIDO)
   - País de origen (Ej: Mexicana, Estadounidense)

5. **Estado de Nacimiento** (Texto)
   - Estado o región donde nació

6. **Estado Civil** (Selección, REQUERIDO)
   - Opciones: Soltero(a), Casado(a), Unión libre, Divorciado(a), Viudo(a)

### Documentos Oficiales
7. **CURP** (Texto)
   - Clave Única de Registro de Población (18 caracteres)

8. **INE/IFE** (Texto)
   - Número de credencial de elector

### Contacto
9. **Teléfono** (Texto, REQUERIDO)
   - Número de contacto principal (Ej: 55-1234-5678)

10. **Email** (Texto)
    - Correo electrónico de contacto

11. **Dirección** (Texto largo, REQUERIDO)
    - Domicilio completo: Calle, número, colonia, CP, ciudad, estado

### Educación
12. **Escolaridad** (Selección, REQUERIDO)
    - Opciones: Sin estudios, Primaria, Secundaria, Preparatoria/Bachillerato, Carrera técnica, Licenciatura, Posgrado

13. **Institución de Último Grado** (Texto)
    - Escuela donde obtuvo su último grado

14. **Certificados y Capacitaciones** (Texto largo)
    - Cursos, diplomados, certificaciones obtenidas

### Emergencia y Legal
15. **Contacto de Emergencia** (Texto, REQUERIDO)
    - Nombre de persona a contactar en caso de emergencia

16. **Teléfono de Emergencia** (Texto, REQUERIDO)
    - Teléfono del contacto de emergencia

17. **Antecedentes Legales** (Sí/No)
    - ¿Tiene antecedentes penales o procesos legales?

18. **Detalle de Antecedentes** (Texto largo)
    - Si marcó que sí, describir la situación

19. **Dependencia Económica** (Texto)
    - ¿De quién depende económicamente? (si aplica)

---

## SECCIÓN 2: SALUD E INTERESES (20 CAMPOS)

### Estado de Salud General
20. **Padecimientos Generales** (Texto largo)
    - Enfermedades o condiciones de salud generales

21. **Enfermedades Crónicas** (Texto largo)
    - Diabetes, hipertensión, asma, etc.

22. **Número de Enfermedades Crónicas** (Número) ⭐ CUANTITATIVO
    - Cantidad total de enfermedades crónicas diagnosticadas

23. **Tratamientos Actuales** (Texto largo)
    - Medicamentos o terapias que está recibiendo

24. **Número de Tratamientos Activos** (Número) ⭐ CUANTITATIVO
    - Cantidad de tratamientos médicos actuales

25. **Gasto Mensual en Medicamentos** (Decimal) ⭐ CUANTITATIVO
    - Monto aproximado que gasta al mes en medicinas ($)

26. **Alergias** (Texto)
    - Alergias a medicamentos, alimentos, etc.

### Salud Mental
27. **Antecedentes Psicológicos** (Texto largo)
    - Tratamientos psicológicos o psiquiátricos previos o actuales

28. **Actualmente en Tratamiento Psicológico** (Sí/No)
    - ¿Está en terapia psicológica actualmente?

29. **Frecuencia de Consultas Psicológicas** (Texto)
    - Si está en tratamiento, ¿cada cuánto asiste?

### Consumo de Sustancias
30. **Consumo de Alcohol** (Selección)
    - Opciones: No consume, Ocasional, Social, Frecuente, Diario

31. **Copas/Bebidas por Semana** (Número) ⭐ CUANTITATIVO
    - Número promedio de bebidas alcohólicas por semana

32. **Consumo de Tabaco** (Selección)
    - Opciones: No fuma, Ex fumador, Ocasional, Menos de 10 al día, Más de 10 al día

33. **Cigarros por Día** (Número) ⭐ CUANTITATIVO
    - Número promedio de cigarros que fuma al día

34. **Consumo de Otras Sustancias** (Texto)
    - Uso de otras sustancias (si aplica)

### Seguro Médico
35. **¿Tiene Seguro Médico?** (Selección)
    - Opciones: Sí, No

36. **Tipo de Seguro** (Selección)
    - Opciones: IMSS, ISSSTE, Seguro Popular/INSABI, Privado, Otro

37. **Costo Mensual del Seguro** (Decimal) ⭐ CUANTITATIVO
    - Monto mensual si tiene seguro privado ($)

### Metas y Aspiraciones
38. **Metas a Corto Plazo** (Texto largo)
    - Objetivos para los próximos 1-2 años

39. **Metas a Largo Plazo** (Texto largo)
    - Objetivos a 5-10 años

---

## SECCIÓN 3: INFORMACIÓN FAMILIAR (14 CAMPOS BASE + LISTA DINÁMICA)

### Composición del Hogar
40. **Número de Hijos** (Número)
    - Cantidad de hijos propios

41. **Número de Hijos Menores** (Número) ⭐ CUANTITATIVO
    - Menores de 18 años

42. **Número de Hijos Estudiando** (Número) ⭐ CUANTITATIVO
    - Hijos que actualmente estudian

43. **Gasto Mensual en Educación de Hijos** (Decimal) ⭐ CUANTITATIVO
    - Colegiaturas, útiles, uniformes, etc. ($)

### Lista de Miembros del Hogar (Dinámica)
**Por cada miembro se captura:**
- Nombre completo
- Edad
- Parentesco (padre, madre, hijo, hermano, etc.)
- ¿Estudia o trabaja? (Estudiante/Trabajador/Ambos/Ninguno)
- ¿Aporta ingreso? (Sí/No)
- Enfermedades crónicas
- Tipo de dependencia (Total/Parcial/Ninguna)
- Ingreso mensual ($)

### Métricas Familiares Calculadas
44. **Total de Miembros del Hogar** (Número) ⭐ CUANTITATIVO
    - Contador automático de personas en casa

45. **Miembros Trabajando** (Número) ⭐ CUANTITATIVO
    - Cantidad de personas con empleo

46. **Miembros Estudiando** (Número) ⭐ CUANTITATIVO
    - Cantidad de personas en escuela

47. **Miembros con Enfermedades** (Número) ⭐ CUANTITATIVO
    - Cantidad con enfermedades crónicas

48. **Ingreso Familiar Total** (Decimal) ⭐ CUANTITATIVO
    - Suma de todos los ingresos ($)

49. **Ingreso Per Cápita** (Decimal) ⭐ CUANTITATIVO
    - Ingreso total / número de personas ($)

50. **Dependientes Sin Ingreso** (Número) ⭐ CUANTITATIVO
    - Cantidad de personas que no aportan dinero

51. **Porcentaje de Dependientes** (Decimal) ⭐ CUANTITATIVO
    - % de personas dependientes (%)

52. **Gasto Promedio por Persona** (Decimal) ⭐ CUANTITATIVO
    - Gastos totales / número de personas ($)

53. **Observaciones Familiares** (Texto largo)
    - Notas adicionales sobre la dinámica familiar

---

## SECCIÓN 4: SITUACIÓN FINANCIERA (35 CAMPOS)

### Ingresos
54. **Trabaja Actualmente** (Sí/No)
    - Estado laboral actual

55. **Sueldo Mensual** (Decimal) ⭐ CUANTITATIVO
    - Salario principal mensual ($)

### Otros Ingresos (Lista Dinámica)
**Por cada ingreso adicional:**
- Fuente del ingreso
- Monto mensual
- Frecuencia (mensual/quincenal/semanal)

56. **Ingreso Total Mensual** (Decimal) ⭐ CUANTITATIVO
    - Suma automática de todos los ingresos ($)

### Ahorros e Inversiones
57. **Ahorros Actuales** (Decimal) ⭐ CUANTITATIVO
    - Dinero ahorrado a la fecha ($)

58. **Monto de Ahorros Mensuales** (Decimal) ⭐ CUANTITATIVO
    - Cuánto ahorra cada mes ($)

59. **Cuentas Bancarias** (Texto)
    - Bancos donde tiene cuentas

60. **Número de Cuentas Bancarias** (Número) ⭐ CUANTITATIVO
    - Cantidad de cuentas activas

### Tarjetas de Crédito (Lista Dinámica)
**Por cada tarjeta:**
- Banco emisor
- Límite de crédito
- Saldo actual

61. **Número de Tarjetas de Crédito** (Número) ⭐ CUANTITATIVO
    - Cantidad de tarjetas

62. **Límite de Crédito Total** (Decimal) ⭐ CUANTITATIVO
    - Suma de todos los límites ($)

63. **Deuda en Tarjetas Total** (Decimal) ⭐ CUANTITATIVO
    - Suma de todos los saldos ($)

### Préstamos y Deudas
64. **Historial de Deudas** (Texto largo)
    - Descripción de deudas pasadas o actuales

65. **Tiene Préstamos Personales** (Sí/No)
    - ¿Tiene créditos personales activos?

66. **Monto de Préstamos Personales** (Decimal) ⭐ CUANTITATIVO
    - Suma de préstamos personales ($)

67. **Tiene Préstamo Hipotecario** (Sí/No)
    - ¿Tiene hipoteca de vivienda?

68. **Monto de Hipoteca** (Decimal) ⭐ CUANTITATIVO
    - Capital adeudado de hipoteca ($)

69. **Pago Mensual de Hipoteca** (Decimal) ⭐ CUANTITATIVO
    - Mensualidad de hipoteca ($)

70. **Tiene Préstamo de Auto** (Sí/No)
    - ¿Tiene crédito automotriz?

71. **Monto de Préstamo de Auto** (Decimal) ⭐ CUANTITATIVO
    - Capital adeudado de auto ($)

72. **Pago Mensual de Auto** (Decimal) ⭐ CUANTITATIVO
    - Mensualidad de auto ($)

### Apoyos Gubernamentales
73. **Apoyos Gubernamentales** (Texto)
    - Programas sociales que recibe

74. **Monto de Apoyos Gubernamentales** (Decimal) ⭐ CUANTITATIVO
    - Monto mensual de apoyos ($)

### Gastos Mensuales
75. **Gasto en Alimentación** (Decimal) ⭐ CUANTITATIVO ($)
76. **Gasto en Salud** (Decimal) ⭐ CUANTITATIVO ($)
77. **Gasto en Educación** (Decimal) ⭐ CUANTITATIVO ($)
78. **Gasto en Vivienda** (Decimal) ⭐ CUANTITATIVO ($)
79. **Gasto en Transporte** (Decimal) ⭐ CUANTITATIVO ($)
80. **Gasto en Servicios** (Decimal) ⭐ CUANTITATIVO ($)
81. **Gasto en Recreación** (Decimal) ⭐ CUANTITATIVO ($)
82. **Otros Gastos** (Decimal) ⭐ CUANTITATIVO ($)
83. **Total de Gastos** (Decimal) ⭐ CUANTITATIVO - Suma automática ($)

84. **Gasto Promedio en Comida Diaria** (Decimal) ⭐ CUANTITATIVO ($)
85. **Gasto Mensual en Medicamentos** (Decimal) ⭐ CUANTITATIVO ($)
86. **Gasto Mensual en Gasolina** (Decimal) ⭐ CUANTITATIVO ($)

87. **Gastos Extraordinarios** (Texto largo)
    - Gastos únicos o imprevistos

### Deudas Listadas (Lista Dinámica)
**Por cada deuda:**
- Acreedor
- Monto total
- Pago mensual

88. **Total de Deudas** (Decimal) ⭐ CUANTITATIVO
    - Suma de todas las deudas ($)

89. **Total de Pagos Mensuales de Deudas** (Decimal) ⭐ CUANTITATIVO
    - Suma de todos los pagos mensuales ($)

### Indicadores Financieros Calculados
90. **Balance Mensual** (Decimal) ⭐ CUANTITATIVO
    - Ingresos - Gastos ($)

91. **Porcentaje de Gastos vs Ingreso** (Decimal) ⭐ CUANTITATIVO
    - (Gastos / Ingresos) × 100 (%)

92. **Porcentaje de Ahorro** (Decimal) ⭐ CUANTITATIVO
    - (Ahorros / Ingresos) × 100 (%)

93. **Porcentaje de Deudas vs Ingreso** (Decimal) ⭐ CUANTITATIVO
    - (Deudas / Ingresos) × 100 (%)

94. **Capacidad de Pago** (Decimal) ⭐ CUANTITATIVO
    - Ingreso - (Gastos fijos + Deudas) ($)

95. **Discrepancia de Ingresos** (Sí/No)
    - Flag automático si hay inconsistencias

96. **Observaciones Financieras** (Texto largo)
    - Notas del evaluador sobre finanzas

---

## SECCIÓN 5: VIVIENDA Y PATRIMONIO (40 CAMPOS)

### Ubicación y Tipo
97. **Zona** (Texto)
    - Colonia o zona donde vive

98. **Tipo de Zona** (Texto)
    - Urbana, suburbana, rural

99. **Tipo de Vivienda** (Texto)
    - Casa, departamento, vecindad, etc.

100. **Tenencia** (Texto)
     - Propia, rentada, prestada, familiar

101. **Renta Mensual** (Decimal) ⭐ CUANTITATIVO
     - Monto de renta si aplica ($)

102. **Tiempo Viviendo Ahí** (Texto)
     - Años y meses de residencia

### Características Físicas
103. **Materiales de Construcción** (Texto)
     - Concreto, madera, lámina, etc.

104. **Condición Física - Humedad** (Sí/No)
105. **Condición Física - Filtraciones** (Sí/No)
106. **Condición Física - Sobrecupo** (Sí/No)
107. **Buena Ventilación** (Sí/No)
108. **Iluminación Natural** (Sí/No)

### Servicios Básicos (11 servicios)
109. **Agua Potable** (Sí/No)
110. **Luz Eléctrica** (Sí/No)
111. **Drenaje** (Sí/No)
112. **Gas** (Sí/No)
113. **Teléfono** (Sí/No)
114. **Internet** (Sí/No)
115. **Transporte Público** (Sí/No)
116. **Pavimentación** (Sí/No)
117. **Áreas Verdes** (Sí/No)

118. **Número de Servicios Básicos** (Número) ⭐ CUANTITATIVO
     - Conteo automático de servicios disponibles

### Equipamiento (8 electrodomésticos)
119. **Refrigerador** (Número) - Cantidad
120. **Lavadora** (Número) - Cantidad
121. **Estufa** (Número) - Cantidad
122. **Televisor** (Número) - Cantidad
123. **Computadora** (Número) - Cantidad
124. **Microondas** (Número) - Cantidad
125. **Aire Acondicionado** (Número) - Cantidad
126. **Calentador** (Número) - Cantidad

### Mobiliario (5 tipos)
127. **Camas** (Número) - Cantidad
128. **Mesas** (Número) - Cantidad
129. **Sillas** (Número) - Cantidad
130. **Armarios** (Número) - Cantidad
131. **Sillones** (Número) - Cantidad

### Vehículos
132. **Automóviles** (Número) - Cantidad
133. **Motocicletas** (Número) - Cantidad
134. **Bicicletas** (Número) - Cantidad

135. **Valor Aproximado de Vehículos** (Decimal) ⭐ CUANTITATIVO
     - Valor estimado total ($)

### Dimensiones y Ocupación
136. **Número de Cuartos** (Número) ⭐ CUANTITATIVO
137. **Número de Baños** (Número) ⭐ CUANTITATIVO
138. **Metros Cuadrados de Construcción** (Decimal) ⭐ CUANTITATIVO (m²)
139. **Número de Habitantes** (Número) ⭐ CUANTITATIVO
140. **Índice de Hacinamiento** (Decimal) ⭐ CUANTITATIVO
     - Personas por cuarto (calculado)

141. **Porcentaje de Equipamiento** (Decimal) ⭐ CUANTITATIVO
     - % de equipamiento completo (%)

### Valor y Patrimonio
142. **Valor Estimado de la Vivienda** (Decimal) ⭐ CUANTITATIVO ($)
143. **Antigüedad de la Vivienda (años)** (Número) ⭐ CUANTITATIVO

144. **Seguridad del Entorno** (Texto)
     - Descripción de la seguridad del área

145. **Otras Propiedades** (Texto)
     - Descripción de propiedades adicionales

146. **Número de Propiedades Adicionales** (Número) ⭐ CUANTITATIVO
147. **Valor de Propiedades Adicionales** (Decimal) ⭐ CUANTITATIVO ($)

---

## SECCIÓN 6: EMPLEO ACTUAL (23 CAMPOS)

### Información de la Empresa
148. **Empresa** (Texto)
     - Nombre de la empresa actual

149. **Puesto** (Texto)
     - Cargo o puesto que desempeña

150. **Antigüedad** (Texto)
     - Tiempo en la empresa (Ej: 2 años 3 meses)

151. **Antigüedad en Meses** (Número) ⭐ CUANTITATIVO
     - Para cálculos precisos

152. **Tipo de Contrato** (Selección)
     - Opciones: Indefinido/Planta, Temporal, Por honorarios, Por obra, Otro

### Compensación
153. **Salario Mensual Bruto** (Decimal) ⭐ CUANTITATIVO
     - Antes de deducciones ($)

154. **Salario Mensual Neto** (Decimal) ⭐ CUANTITATIVO
     - Después de deducciones ($)

### Prestaciones (Lista + Métricas)
155. **Prestaciones** (Lista)
     - Aguinaldo, vacaciones, IMSS, etc.

156. **Número de Prestaciones** (Número) ⭐ CUANTITATIVO
157. **Valor de Prestaciones Anuales** (Decimal) ⭐ CUANTITATIVO ($)

### Horario y Jornada
158. **Horario** (Texto)
     - Ej: Lunes a viernes 9:00-18:00

159. **Horas Semanales** (Número) ⭐ CUANTITATIVO
     - Total de horas trabajadas por semana

160. **Días Laborales por Semana** (Número) ⭐ CUANTITATIVO

### Traslado
161. **Tiempo de Traslado** (Texto)
     - Ej: 45 minutos

162. **Tiempo de Traslado en Minutos** (Número) ⭐ CUANTITATIVO
     - Tiempo en minutos (ida)

163. **Costo Mensual de Transporte** (Decimal) ⭐ CUANTITATIVO ($)

### Home Office
164. **Tiene Home Office** (Sí/No)
165. **Días de Home Office por Semana** (Número) ⭐ CUANTITATIVO

### Desarrollo Profesional
166. **Plan de Carrera** (Texto largo)
     - Oportunidades de crecimiento

167. **Oportunidades de Ascenso** (Texto)
     - Posibles promociones

168. **Última Evaluación de Desempeño** (Texto)
     - Descripción de la evaluación

169. **Calificación de Última Evaluación (1-10)** (Decimal) ⭐ CUANTITATIVO

### Bonos e Incentivos
170. **Recibe Bonos** (Sí/No)
171. **Monto Promedio de Bonos Anuales** (Decimal) ⭐ CUANTITATIVO ($)

---

## SECCIÓN 7: HISTORIAL LABORAL (LISTA DINÁMICA)

**Por cada empleo anterior se captura:**

172. Empresa
173. Puesto
174. Fecha de Inicio
175. Fecha de Fin
176. Salario Inicial ($) ⭐ CUANTITATIVO
177. Salario Final ($) ⭐ CUANTITATIVO
178. Nombre del Jefe
179. Puesto del Jefe
180. Teléfono de Contacto
181. Motivo de Separación
182. Evaluaciones Recibidas
183. Conflictos Reportados
184. Verificación de Referencia (Sí/No/Pendiente)

---

## SECCIÓN 8: ESTILO DE VIDA (24 CAMPOS)

### Hobbies y Pasatiempos
185. **Hobbies y Pasatiempos** (Texto largo)
     - Actividades que realiza en tiempo libre

186. **Número de Hobbies** (Número) ⭐ CUANTITATIVO
187. **Gasto Mensual en Hobbies** (Decimal) ⭐ CUANTITATIVO ($)

### Actividades de Fin de Semana
188. **Actividades de Fin de Semana** (Texto largo)
     - ¿Qué hace típicamente los fines de semana?

189. **Frecuencia de Salidas al Mes** (Número) ⭐ CUANTITATIVO
     - Veces que sale (cine, restaurantes, etc.)

190. **Gasto Promedio por Salida** (Decimal) ⭐ CUANTITATIVO ($)

### Viajes
191. **Frecuencia de Viajes** (Selección)
     - Opciones: No viaja, Una vez al año, Varias veces al año, Mensualmente

192. **Número de Viajes el Último Año** (Número) ⭐ CUANTITATIVO
193. **Gasto Total en Viajes (Último Año)** (Decimal) ⭐ CUANTITATIVO ($)
194. **Destinos Frecuentes** (Texto)
     - Lugares que suele visitar

### Gastos Recreativos
195. **Gastos Recreativos Mensuales** (Decimal) ⭐ CUANTITATIVO
     - Cantidad total destinada a entretenimiento ($)

### Cultura
196. **Actividades Culturales** (Texto largo)
     - Teatro, cine, museos, conciertos, etc.

197. **Actividades Culturales al Mes** (Número) ⭐ CUANTITATIVO
     - Frecuencia mensual

198. **Gasto Mensual en Cultura** (Decimal) ⭐ CUANTITATIVO ($)

### Deportes y Ejercicio
199. **Deportes que Practica** (Texto)
     - Fútbol, gimnasio, natación, etc.

200. **Frecuencia de Ejercicio (días/semana)** (Número) ⭐ CUANTITATIVO
201. **Gasto Mensual en Gimnasio/Deportes** (Decimal) ⭐ CUANTITATIVO ($)

### Clubes y Asociaciones
202. **Pertenece a Clubes/Asociaciones** (Sí/No)
203. **Número de Clubes/Asociaciones** (Número) ⭐ CUANTITATIVO
204. **Costo Mensual de Membresías** (Decimal) ⭐ CUANTITATIVO ($)

### Mascotas
205. **Tiene Mascotas** (Sí/No)
206. **Número de Mascotas** (Número) ⭐ CUANTITATIVO
207. **Gasto Mensual en Mascotas** (Decimal) ⭐ CUANTITATIVO ($)

---

## SECCIÓN 9: REFERENCIAS PERSONALES (LISTA DINÁMICA)

**Por cada referencia se captura:**

208. Nombre Completo
209. Relación con el Candidato
210. Domicilio o Empresa
211. Teléfono de Contacto
212. Ocupación
213. Tiempo de Conocerse

Se recomienda capturar **mínimo 3 referencias personales**.

---

## SECCIÓN 10: CONCLUSIONES DEL EVALUADOR

214. **Conclusiones** (Texto libre largo)
     - Análisis, observaciones y conclusiones del evaluador

---

## SECCIÓN 11: FOTOGRAFÍAS ADJUNTAS (LISTA DINÁMICA)

**Por cada fotografía:**

215. Archivo de imagen
216. Tipo (fachada, interior, identificación, etc.)
217. Descripción

---

## INDICADORES DE RIESGO CALCULADOS AUTOMÁTICAMENTE

El sistema calcula **7 indicadores de riesgo** con justificaciones automáticas:

### Riesgo Financiero
**Factores evaluados:**
- Porcentaje de gastos vs ingresos
- Balance mensual (positivo/negativo)
- Número de deudas
- Monto total de deudas
- Ausencia de ahorros
- Tarjetas de crédito al límite
- Dependencia de apoyos gubernamentales

**Escala:** 1 (Muy Bajo) a 5 (Muy Alto)

### Riesgo Familiar
**Factores evaluados:**
- Número de dependientes sin ingreso
- Ingreso per cápita
- Porcentaje de dependientes vs trabajadores
- Enfermedades crónicas en familia
- Hacinamiento

**Escala:** 1 (Muy Bajo) a 5 (Muy Alto)

### Riesgo de Vivienda
**Factores evaluados:**
- Tenencia (propia/rentada/prestada)
- Servicios básicos disponibles
- Condición física (humedad, filtraciones)
- Índice de hacinamiento
- Seguridad del entorno
- Equipamiento básico

**Escala:** 1 (Muy Bajo) a 5 (Muy Alto)

### Riesgo Laboral
**Factores evaluados:**
- Estado laboral actual
- Tipo de contrato
- Antigüedad en el empleo
- Prestaciones disponibles
- Estabilidad laboral (historial)

**Escala:** 1 (Muy Bajo) a 5 (Muy Alto)

### Riesgo de Salud ⭐ NUEVO
**Factores evaluados:**
- Número de enfermedades crónicas
- Tratamientos activos
- Gasto mensual en medicamentos
- Sin seguro médico
- Consumo de sustancias (alcohol, tabaco)
- Estado de salud general

**Escala:** 1 (Muy Bajo) a 5 (Muy Alto)

### Riesgo de Estilo de Vida ⭐ NUEVO
**Factores evaluados:**
- Gastos recreativos vs ingreso
- Frecuencia de viajes
- Gastos en entretenimiento
- Membresías y clubes
- Vehículos de lujo
- Desproporción gasto/ingreso

**Escala:** 1 (Muy Bajo) a 5 (Muy Alto)

### Riesgo Socioeconómico Global
**Cálculo:** Promedio ponderado de todos los riesgos anteriores

**Escala:** 1 (Muy Bajo) a 5 (Muy Alto)

---

## VALIDACIONES AUTOMÁTICAS

El sistema realiza **17+ validaciones** para detectar contradicciones:

1. ✅ Balance declarado vs balance calculado
2. ✅ Gastos > 80% del ingreso (alerta)
3. ✅ Gastos superan ingresos totales (error)
4. ✅ Número de hijos vs menores en lista
5. ✅ Ingreso familiar vs ingreso individual
6. ✅ Dependientes sin ingreso excesivos (crítico)
7. ✅ Vivienda propia pero paga renta
8. ✅ Hacinamiento crítico (>3 personas por cuarto)
9. ✅ Falta de servicios básicos (agua, drenaje)
10. ✅ Trabajo actual pero sin sueldo
11. ✅ No trabaja pero tiene sueldo
12. ✅ Deudas sin plan de pago
13. ✅ Tarjetas al límite (>90%)
14. ✅ Tiempo de traslado excesivo (>2 horas)
15. ✅ Enfermedades crónicas sin tratamiento
16. ✅ Problemas estructurales de vivienda
17. ✅ Balance positivo sin ahorros

---

## FORMATOS DE EXPORTACIÓN

### PDF Profesional
- 10-15 páginas completas
- 7 secciones principales
- Tabla de riesgos con 6 categorías
- **Sección de justificaciones detalladas**
- Fotografías incluidas
- Branding personalizable

### Word Editable
- Estructura idéntica al PDF
- Formato editable
- Tablas y listas con estilo profesional
- Justificaciones en bullets
- Fácil personalización

### Excel Comparativo
- **33 columnas de datos**
- Columnas A-S: Demografía
- Columnas T-AE: 6 pares (Riesgo + Justificación)
- Columnas AF-AG: Global + Interpretación
- Color-coding por nivel de riesgo
- Ideal para análisis masivo

---

## MÉTRICAS DEL SISTEMA

### Campos por Categoría
- **Cuantitativos (números/decimales):** 90+ campos
- **Cualitativos (texto):** 80+ campos
- **Selecciones (opciones):** 20+ campos
- **Booleanos (Sí/No):** 30+ campos
- **Listas dinámicas:** 6 (miembros, ingresos, tarjetas, deudas, empleos, referencias)

### Total de Datos Capturables
- **Campos fijos:** 214 campos
- **Campos dinámicos:** Ilimitados (listas)
- **TOTAL MÍNIMO:** 230+ datos por estudio

### Tiempo de Captura
- **Estudio básico:** 20-30 minutos
- **Estudio completo:** 45-60 minutos
- **Estudio exhaustivo:** 90+ minutos (con todas las listas llenas)

---

## VENTAJAS DEL SISTEMA v0.2.0

### 1. Información Cuantitativa Exhaustiva
- **90+ indicadores numéricos** para análisis estadístico
- Montos en pesos mexicanos ($)
- Cantidades precisas de elementos
- Porcentajes calculados automáticamente
- Métricas comparables entre estudios

### 2. Profesionalismo
- Justificaciones automáticas transparentes
- Detección de contradicciones
- Indicadores objetivos de riesgo
- Reportes listos para presentación

### 3. Escalabilidad
- Listas dinámicas sin límite
- Agregar campos nuevos en minutos
- Sistema modular extensible
- Compatible con versiones anteriores

### 4. Análisis Integral
- 7 dimensiones de riesgo evaluadas
- Interconexión entre secciones
- Validaciones cruzadas
- Visión 360° del candidato

---

## CONCLUSIÓN

El **Sistema de Estudios Socioeconómicos v0.2.0** captura **230+ datos individuales** organizados en **11 secciones**, con más de **90 indicadores cuantitativos** que permiten realizar análisis exhaustivos, comparaciones estadísticas y generar reportes profesionales con justificaciones automáticas basadas en datos reales.

Cada estudio proporciona una **fotografía completa** de la situación socioeconómica del candidato, incluyendo aspectos financieros, familiares, de salud, vivienda, empleo, estilo de vida y patrimonio, con indicadores de riesgo calculados científicamente.

---

**DINOS Tech** - Software Socioeconómico Profesional  
**Versión:** 0.2.0  
**Fecha:** 9 de diciembre de 2025
