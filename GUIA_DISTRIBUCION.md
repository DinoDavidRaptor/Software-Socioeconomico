# Guia de Empaquetado y Distribucion - DINOS Tech

## Resumen del Sistema

Este documento describe el proceso completo para compilar, proteger y distribuir SoftSE.

## Arquitectura de Proteccion

```
+-------------------+     +------------------+     +------------------+
|   Nuitka          |     |   Sistema de     |     |   Inno Setup     |
|   (Compilacion)   | --> |   Licencias      | --> |   (Instalador)   |
|                   |     |   (Offline)      |     |                  |
+-------------------+     +------------------+     +------------------+
        |                         |                        |
        v                         v                        v
   .exe protegido          Hardware ID +           Installer .exe
   (codigo C)              License Key             profesional
```

## Requisitos

### Software necesario

1. **Python 3.8+** con las dependencias del proyecto
2. **Nuitka** para compilacion:
   ```bash
   pip install nuitka ordered-set zstandard
   ```
3. **Inno Setup 6.x** para el instalador:
   - Descargar de: https://jrsoftware.org/isinfo.php
   - Instalar con soporte para idioma Espanol

### Archivos graficos (crear antes de compilar)

- `assets/installer/icon.ico` - Icono de la app (multiples resoluciones)
- `assets/installer/banner.bmp` - Banner lateral (164x314 px)
- `assets/installer/header.bmp` - Header del wizard (150x57 px)

---

## Proceso de Distribucion

### Paso 1: Compilar con Nuitka

```bash
cd scripts
python build_nuitka.py
```

El script:

- Compila main.py y todo el paquete src/ a codigo C
- Genera `dist/SoftSE.exe`
- Copia archivos necesarios (config.json, etc.)

**Tiempo estimado:** 5-15 minutos (primera vez)

### Paso 2: Crear el Instalador

1. Abre `installer/setup.iss` con Inno Setup Compiler
2. Verifica que las rutas sean correctas
3. Presiona `Ctrl+F9` para compilar
4. El instalador se genera en `installer_output/`

**Resultado:** `SoftSE_Setup_v0.3.7.exe`

### Paso 3: Distribuir al Cliente

Envia al cliente:

1. El instalador (`SoftSE_Setup_vX.X.X.exe`)
2. Instrucciones de instalacion

---

## Sistema de Licencias

### Como funciona

1. **Cliente instala** el software
2. **Software muestra** el Hardware ID del equipo
3. **Cliente envia** el Hardware ID a DINOS Tech
4. **Tu generas** una licencia con `license_generator.py`
5. **Cliente activa** con la key o archivo license.dat

### Generar Licencias (PRIVADO)

**IMPORTANTE:** El archivo `scripts/privado/license_generator.py` es CONFIDENCIAL. Nunca lo incluyas en la distribucion.

```bash
cd scripts/privado
python license_generator.py
```

Opciones de licencia:

- **BASICA**: Funciones limitadas
- **PROFESIONAL**: Todas las funciones
- **EMPRESARIAL**: Multiples usuarios + soporte premium

Opciones de expiracion:

- **PERPETUA**: Sin fecha de vencimiento
- **1/2/3 anos**: Suscripcion temporal

### Entregar Licencia al Cliente

**Opcion A: Solo License Key**

```
Enviar al cliente:
- License Key: XXXX-XXXX-XXXX-XXXX-XXXX

El cliente la ingresa en el dialogo de activacion.
```

**Opcion B: Archivo license.dat**

```
Enviar al cliente:
- Archivo: license.dat

El cliente lo coloca junto al ejecutable.
```

---

## Donde Poner tus Recursos

### Logo e icono

```
assets/installer/
├── icon.ico          # Tu logo en formato ICO
├── banner.bmp        # Banner vertical 164x314
├── header.bmp        # Header 150x57
└── EULA.txt          # Terminos y condiciones (ya creado)
```

### Informacion de empresa

Edita estos archivos:

- `installer/setup.iss` - Lineas 18-22:
  ```inno
  #define MyAppPublisher "TU EMPRESA"
  #define MyAppURL "https://tudominio.com"
  ```
- `config.json` - Datos de tu empresa por defecto

---

## Estructura de Archivos

```
Software-Socioeconomico/
├── src/
│   ├── licensing/           # Sistema de licencias
│   │   ├── __init__.py
│   │   ├── hardware_id.py   # Genera ID unico del hardware
│   │   └── license_validator.py  # Valida licencias
│   └── ui/
│       └── dialogo_activacion.py  # UI de activacion
│
├── scripts/
│   ├── build_nuitka.py      # Script de compilacion
│   └── privado/             # NO DISTRIBUIR
│       └── license_generator.py  # Genera licencias
│
├── installer/
│   └── setup.iss            # Script de Inno Setup
│
├── assets/installer/
│   ├── EULA.txt             # Terminos y condiciones
│   ├── README.md            # Instrucciones para graficos
│   ├── icon.ico             # (TU LOGO - crear)
│   ├── banner.bmp           # (BANNER - crear)
│   └── header.bmp           # (HEADER - crear)
│
└── dist/                    # Generado por Nuitka
    └── SoftSE.exe
```

---

## Seguridad y Proteccion

### Que protege el sistema

| Capa        | Proteccion                    | Nivel      |
| ----------- | ----------------------------- | ---------- |
| Nuitka      | Compila Python a C nativo     | Alto       |
| Hardware ID | Vincula licencia al equipo    | Alto       |
| License Key | Firma criptografica SHA256    | Medio-Alto |
| Inno Setup  | Instalador firmado (opcional) | Medio      |

### Que NO hacer

1. **NUNCA** incluir `scripts/privado/` en la distribucion
2. **NUNCA** compartir el `_SECRET_SALT` de los archivos de licencia
3. **NUNCA** distribuir el codigo fuente (.py)

### Recomendaciones adicionales

1. **Firma digital** del instalador (requiere certificado de Authenticode)
2. **Ofuscador adicional** si manejas datos muy sensibles
3. **Servidor de validacion** online para licencias premium

---

## Checklist de Distribucion

- [ ] Crear graficos (icon.ico, banner.bmp, header.bmp)
- [ ] Verificar EULA.txt con tus datos de contacto
- [ ] Compilar con Nuitka
- [ ] Probar el .exe en una maquina limpia
- [ ] Compilar instalador con Inno Setup
- [ ] Probar instalacion completa
- [ ] Probar sistema de licencias (generar key de prueba)
- [ ] Probar activacion y validacion
- [ ] Distribuir al cliente

---

## Contacto

DINOS Tech
Email: soporte@dinoraptor.tech
Telefono: 3333010376
Web: dinoraptor.tech/dinostech

---

_Documento confidencial - Solo para uso interno de DINOS Tech_
