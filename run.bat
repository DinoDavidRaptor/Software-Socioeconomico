@echo off
REM Script de ejecución para Ecosistema Comercial 360 (Windows)
REM Activa el entorno virtual y ejecuta la aplicación

echo ============================================================
echo   Ecosistema Comercial 360
echo   DINOS Tech
echo ============================================================
echo.

REM Verificar si existe el entorno virtual
if not exist "venv\" (
    echo ERROR: No se encontró el entorno virtual.
    echo Ejecute primero: python install.py
    pause
    exit /b 1
)

REM Activar entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate.bat

REM Verificar si main.py existe
if not exist "main.py" (
    echo ERROR: No se encontró main.py
    pause
    exit /b 1
)

REM Ejecutar la aplicación
echo Iniciando aplicación...
echo.
python main.py

REM Desactivar entorno virtual
deactivate

pause
