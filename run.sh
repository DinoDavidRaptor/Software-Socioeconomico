#!/bin/bash
# Script de ejecución para SoftSE
# Activa el entorno virtual y ejecuta la aplicación

# Colores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "============================================================"
echo "  SoftSE"
echo "  DINOS Tech"
echo "============================================================"
echo ""

# Verificar si existe el entorno virtual
if [ ! -d "venv" ]; then
    echo -e "${RED}ERROR: No se encontró el entorno virtual.${NC}"
    echo "Ejecute primero: python3 install.py"
    exit 1
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Verificar si main.py existe
if [ ! -f "main.py" ]; then
    echo -e "${RED}ERROR: No se encontró main.py${NC}"
    exit 1
fi

# Ejecutar la aplicación
echo -e "${GREEN}Iniciando aplicación...${NC}"
echo ""
python main.py

# El entorno virtual se desactiva automáticamente al salir
