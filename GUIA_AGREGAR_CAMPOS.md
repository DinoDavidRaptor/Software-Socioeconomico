# Guía para Agregar Preguntas al Sistema

## Sistema Modular v0.2.0 - Facilidad de Expansión

El sistema ahora utiliza una arquitectura modular que hace **extremadamente fácil** agregar nuevas preguntas o campos sin necesidad de programar UI manualmente.

---

## Resumen Rápido

### Para agregar UN campo nuevo:

1. **Editar** `src/ui/configuracion_campos.py` (1 minuto)
2. **Actualizar** `src/models/estudio.py` si es necesario (30 segundos)
3. **Listo** - El sistema hace el resto automáticamente

### Para agregar UNA página nueva completa:

1. **Crear** nueva función en `configuracion_campos.py` (5 minutos)
2. **Crear** nueva clase en `paginas_modulares.py` (2 minutos)
3. **Agregar** al wizard (1 minuto)
4. **Listo**

---

## Paso a Paso Detallado

### Ejemplo 1: Agregar "RFC" a Datos Personales

#### Paso 1: Configurar el campo

Abrir: `src/ui/configuracion_campos.py`

Buscar: `obtener_campos_datos_personales()`

Agregar en la lista:

```python
{
    'id': 'rfc',                        # Identificador único
    'etiqueta': 'RFC',                  # Lo que verá el usuario
    'tipo': TipoCampo.TEXTO,            # Tipo de control
    'requerido': False,                 # ¿Es obligatorio?
    'ayuda': 'Registro Federal de Contribuyentes',
    'placeholder': 'AAAA######XXX'
},
```

#### Paso 2: Actualizar modelo de datos

Abrir: `src/models/estudio.py`

Buscar: `"datos_personales": {`

Agregar:

```python
"rfc": "",
```

#### Paso 3: ¡Terminado!

Al ejecutar la aplicación:
- ✅ El campo aparecerá en el formulario
- ✅ Se guardará automáticamente
- ✅ Se cargará automáticamente
- ✅ Se validará si es requerido
- ✅ Se mostrará la ayuda en tooltip

---

## Tipos de Campo Disponibles

### TipoCampo.TEXTO
Línea de texto simple (nombre, dirección, etc.)

```python
{
    'id': 'nombre',
    'etiqueta': 'Nombre',
    'tipo': TipoCampo.TEXTO,
    'placeholder': 'Juan Pérez'
}
```

### TipoCampo.TEXTO_LARGO
Área de texto multilínea (observaciones, descripciones)

```python
{
    'id': 'observaciones',
    'etiqueta': 'Observaciones',
    'tipo': TipoCampo.TEXTO_LARGO,
    'placeholder': 'Escriba observaciones detalladas...'
}
```

### TipoCampo.NUMERO
Número entero con controles +/-

```python
{
    'id': 'num_hijos',
    'etiqueta': 'Número de Hijos',
    'tipo': TipoCampo.NUMERO
}
```

### TipoCampo.DECIMAL
Número decimal, ideal para dinero

```python
{
    'id': 'sueldo',
    'etiqueta': 'Sueldo Mensual',
    'tipo': TipoCampo.DECIMAL
}
```

### TipoCampo.FECHA
Selector de fecha con calendario

```python
{
    'id': 'fecha_ingreso',
    'etiqueta': 'Fecha de Ingreso',
    'tipo': TipoCampo.FECHA
}
```

### TipoCampo.COMBO
Lista desplegable de opciones

```python
{
    'id': 'turno',
    'etiqueta': 'Turno de Trabajo',
    'tipo': TipoCampo.COMBO,
    'opciones': ['Matutino', 'Vespertino', 'Nocturno', 'Mixto']
}
```

### TipoCampo.CHECKBOX
Casilla de verificación (sí/no)

```python
{
    'id': 'tiene_auto',
    'etiqueta': '¿Tiene automóvil?',
    'tipo': TipoCampo.CHECKBOX
}
```

### TipoCampo.LISTA
Lista editable de múltiples items

```python
{
    'id': 'idiomas',
    'etiqueta': 'Idiomas que Habla',
    'tipo': TipoCampo.LISTA,
    'placeholder': 'Agregar idiomas'
}
```

---

## Ejemplo Completo: Nueva Sección "Habilidades"

### Paso 1: Crear configuración de campos

En `configuracion_campos.py`, agregar:

```python
@staticmethod
def obtener_campos_habilidades() -> List[Dict[str, Any]]:
    """Campos de la sección Habilidades."""
    return [
        {
            'id': 'habilidades_tecnicas',
            'etiqueta': 'Habilidades Técnicas',
            'tipo': TipoCampo.TEXTO_LARGO,
            'requerido': False,
            'ayuda': 'Software, herramientas, maquinaria que sabe operar',
            'placeholder': 'Excel, AutoCAD, Torno CNC, etc.'
        },
        {
            'id': 'nivel_ingles',
            'etiqueta': 'Nivel de Inglés',
            'tipo': TipoCampo.COMBO,
            'requerido': False,
            'ayuda': 'Capacidad para leer, escribir y hablar inglés',
            'opciones': ['Nulo', 'Básico', 'Intermedio', 'Avanzado', 'Nativo']
        },
        {
            'id': 'certificaciones',
            'etiqueta': 'Certificaciones Profesionales',
            'tipo': TipoCampo.LISTA,
            'requerido': False,
            'ayuda': 'Certificaciones vigentes relevantes al puesto'
        },
        {
            'id': 'licencia_conducir',
            'etiqueta': '¿Tiene Licencia de Conducir?',
            'tipo': TipoCampo.CHECKBOX,
            'requerido': False,
            'ayuda': 'Licencia vigente para conducir'
        }
    ]
```

### Paso 2: Crear página modular

En `paginas_modulares.py`, agregar:

```python
class PaginaHabilidadesModular(PaginaBaseModular):
    """
    Página: Habilidades (Modular)
    Para agregar campos: editar ConfiguracionCampos.obtener_campos_habilidades()
    """
    
    def __init__(self, estudio):
        super().__init__(
            estudio,
            "Habilidades y Competencias",
            "habilidades"
        )
        self.init_ui()
        self.cargar_datos()
    
    def init_ui(self):
        """Inicializa la interfaz automáticamente."""
        campos = ConfiguracionCampos.obtener_campos_habilidades()
        
        self.crear_formulario_desde_config(
            campos,
            subtitulo="Habilidades técnicas y competencias del candidato."
        )
```

### Paso 3: Actualizar modelo de datos

En `estudio.py`, en el `__init__`, agregar:

```python
# Sección X: Habilidades
"habilidades": {
    "habilidades_tecnicas": "",
    "nivel_ingles": "",
    "certificaciones": [],
    "licencia_conducir": False
},
```

### Paso 4: Agregar al wizard

En `wizard_estudio.py`, en el método `__init__`:

```python
from .paginas_modulares import PaginaHabilidadesModular

# Agregar página
self.addPage(PaginaHabilidadesModular(self.estudio))
```

### ¡Listo!

La nueva sección aparecerá automáticamente con:
- ✅ Formulario completo generado
- ✅ Validaciones configuradas
- ✅ Guardado/cargado automático
- ✅ Ayuda contextual
- ✅ Navegación integrada

---

## Ventajas del Sistema Modular

### Antes (v0.1.0)
Para agregar un campo necesitabas:
1. Escribir código Qt manualmente
2. Crear el widget
3. Agregarlo al layout
4. Programar función de guardado
5. Programar función de carga
6. Manejar validaciones
7. Agregar ayuda
8. **~50 líneas de código por campo**

### Ahora (v0.2.0)
Para agregar un campo necesitas:
1. Agregar 10 líneas de configuración
2. **Listo**

**Resultado**: 80% menos código, 0 errores de UI, 100% consistente

---

## Personalización Avanzada

### Validación Custom

Si necesitas validación especial, sobrescribe `validatePage()`:

```python
def validatePage(self):
    # Guardar datos primero
    self.guardar_datos()
    
    # Validación custom
    if self.estudio.datos['habilidades']['nivel_ingles'] == 'Nativo':
        if not self.estudio.datos['datos_personales']['nacionalidad']:
            QMessageBox.warning(
                self,
                "Atención",
                "Si el inglés es nativo, especifique la nacionalidad"
            )
            return False
    
    return True
```

### Campos Condicionales

Para mostrar campos dependiendo de otros:

```python
def init_ui(self):
    campos = ConfiguracionCampos.obtener_campos_ejemplo()
    self.crear_formulario_desde_config(campos)
    
    # Conectar señal para mostrar/ocultar
    checkbox = self.form_data['widgets']['tiene_auto']
    campo_modelo = self.form_data['widgets']['modelo_auto']
    
    checkbox.stateChanged.connect(
        lambda: campo_modelo.setEnabled(checkbox.isChecked())
    )
```

---

## Mejores Prácticas

### ✅ Hacer

- Usar IDs descriptivos: `fecha_nacimiento` no `fn`
- Agregar ayuda contextual siempre
- Agrupar campos relacionados
- Usar tipo de campo apropiado
- Marcar campos requeridos correctamente

### ❌ Evitar

- IDs duplicados
- Etiquetas sin contexto: "Fecha" (¿de qué?)
- Mezclar español e inglés
- Campos sin ayuda
- Listas de opciones muy largas (>15)

---

## Solución de Problemas

### El campo no aparece
- ✓ Verificar que agregaste el campo en `configuracion_campos.py`
- ✓ Revisar que el ID es único
- ✓ Confirmar que la sintaxis del dict es correcta

### No se guarda el valor
- ✓ Verificar que el campo existe en `estudio.py`
- ✓ Confirmar que el ID coincide exactamente
- ✓ Revisar que llamaste `guardar_datos()`

### Error al cargar
- ✓ Verificar tipo de dato compatible
- ✓ Revisar que el valor en JSON es del tipo correcto
- ✓ Agregar manejo de excepciones si es necesario

---

## Preguntas Frecuentes

**¿Puedo cambiar el orden de los campos?**
Sí, simplemente reordena los elementos en la lista de configuración.

**¿Puedo usar este sistema en otras páginas?**
Sí, todas las páginas pueden usar `PaginaBaseModular`.

**¿Funciona con las páginas antiguas?**
Sí, ambos sistemas coexisten. Migra gradualmente.

**¿Afecta a estudios ya capturados?**
No, los campos nuevos aparecerán vacíos en estudios antiguos.

**¿Puedo crear tipos de campo custom?**
Sí, agrega tu tipo en `generador_formularios.py`.

---

## Soporte

Para dudas o problemas con el sistema modular:
1. Revisa esta guía completa
2. Verifica los ejemplos en `paginas_modulares.py`
3. Consulta `configuracion_campos.py` para referencias

---

**Versión**: 0.2.0  
**Última actualización**: 9 de diciembre de 2025  
**Autor**: DINOS Tech
