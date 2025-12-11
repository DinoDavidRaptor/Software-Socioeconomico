# Inicio Rápido - Ecosistema Comercial 360

## ⚡ Instalación Rápida (Recomendada)

```bash
python3 install.py
```

Este script automático:
- ✅ Crea un entorno virtual
- ✅ Instala todas las dependencias
- ✅ Prepara los directorios

## 🚀 Ejecutar la Aplicación

### Forma Fácil (Recomendada)

**macOS/Linux:**
```bash
./run.sh
```

**Windows:**
```cmd
run.bat
```

### Forma Manual

**macOS/Linux:**
```bash
source venv/bin/activate
python main.py
```

**Windows:**
```cmd
venv\Scripts\activate
python main.py
```

## 📝 Configuración Inicial (Opcional)

Edite `config.json` con los datos de su empresa:
- Nombre
- Dirección
- Teléfono
- Email
- Logo (coloque su logo.png en `assets/`)

## Ejecutar la Aplicación

```bash
python main.py
```

## Primer Uso

1. La aplicación creará automáticamente las carpetas necesarias
2. Haga clic en "Crear Nuevo Estudio" para comenzar
3. Complete el asistente paso a paso
4. Guarde y exporte en el formato deseado

## Solución Rápida de Problemas

### Error: Entorno Virtual no Encontrado

```bash
python3 install.py
```

### Error: Dependencias Faltantes

**En el entorno virtual:**
```bash
source venv/bin/activate  # macOS/Linux
# o
venv\Scripts\activate  # Windows

pip install -r requirements.txt
```

### La Aplicación no Inicia

1. Asegúrese de estar en el entorno virtual
2. Verifique con: `python verify.py`
3. Reinstale si es necesario: `python3 install.py`
2. Verifique permisos de las carpetas `data/` y `export/`
3. Ejecute desde la terminal para ver mensajes de error

## Estructura de Archivos

```
software socioeconomico/
├── main.py                 # Ejecutar este archivo
├── config.json             # Configuración de empresa
├── requirements.txt        # Dependencias
├── data/
│   ├── estudios/          # Estudios guardados (JSON)
│   └── fotos/             # Fotografías adjuntas
├── export/                 # Reportes exportados
└── src/                    # Código fuente
```

## Documentación Completa

Consulte `README.md` para el manual completo de usuario.

---

**DINOS Tech** - Ecosistema Comercial 360 v0.1.0
