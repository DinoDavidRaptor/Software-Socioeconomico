#!/bin/bash
# Script de ejecucion para SoftSE en macOS
# Usa venv_mac con Python 3.9 del sistema (mas estable que Python 3.14)

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "============================================================"
echo "  SoftSE - macOS"
echo "  DINOS Tech"
echo "============================================================"
echo ""

# Verificar si existe el entorno virtual para Mac
if [ ! -d "venv_mac" ]; then
    echo -e "${RED}ERROR: No se encontro el entorno virtual para Mac.${NC}"
    echo "Creando entorno virtual con Python del sistema..."
    /usr/bin/python3 -m venv venv_mac
    source venv_mac/bin/activate
    pip install --upgrade pip
    pip install PyQt5 reportlab python-docx openpyxl pillow matplotlib numpy
    echo -e "${GREEN}Entorno virtual creado exitosamente.${NC}"
else
    source venv_mac/bin/activate
fi

# Verificar si main.py existe
if [ ! -f "main.py" ]; then
    echo -e "${RED}ERROR: No se encontro main.py${NC}"
    exit 1
fi

# Ejecutar la aplicacion
echo -e "${GREEN}Iniciando aplicacion...${NC}"
echo ""
python main.py

# El entorno virtual se desactiva automaticamente al salir
