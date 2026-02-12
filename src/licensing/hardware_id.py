"""
Generador de ID unico de hardware.
Utilizado para vincular licencias a maquinas especificas.
Copyright (c) 2026 DINOS Tech. Todos los derechos reservados.
"""

import hashlib
import platform
import subprocess
import uuid


def get_mac_address() -> str:
    """Obtiene la direccion MAC del dispositivo."""
    mac = uuid.getnode()
    return ':'.join(('%012X' % mac)[i:i+2] for i in range(0, 12, 2))


def get_cpu_id() -> str:
    """Obtiene identificador del procesador."""
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ['wmic', 'cpu', 'get', 'ProcessorId'],
                capture_output=True, text=True, timeout=5
            )
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                return lines[1].strip()
        elif platform.system() == "Darwin":  # macOS
            result = subprocess.run(
                ['sysctl', '-n', 'machdep.cpu.brand_string'],
                capture_output=True, text=True, timeout=5
            )
            return result.stdout.strip()
        else:  # Linux
            with open('/proc/cpuinfo', 'r') as f:
                for line in f:
                    if 'model name' in line.lower():
                        return line.split(':')[1].strip()
    except Exception:
        pass
    return "UNKNOWN_CPU"


def get_disk_serial() -> str:
    """Obtiene el serial del disco principal."""
    try:
        if platform.system() == "Windows":
            result = subprocess.run(
                ['wmic', 'diskdrive', 'get', 'SerialNumber'],
                capture_output=True, text=True, timeout=5
            )
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                return lines[1].strip()
        elif platform.system() == "Darwin":  # macOS
            result = subprocess.run(
                ['system_profiler', 'SPHardwareDataType'],
                capture_output=True, text=True, timeout=10
            )
            for line in result.stdout.split('\n'):
                if 'Serial Number' in line or 'Hardware UUID' in line:
                    return line.split(':')[1].strip()
    except Exception:
        pass
    return "UNKNOWN_DISK"


def get_hardware_id() -> str:
    """
    Genera un ID unico basado en el hardware de la maquina.
    Este ID se usa para vincular licencias a dispositivos especificos.
    
    Returns:
        str: Hash SHA256 truncado del hardware ID (16 caracteres)
    """
    components = [
        get_mac_address(),
        get_cpu_id(),
        get_disk_serial(),
        platform.node(),  # Nombre del equipo
    ]
    
    # Combinar componentes y crear hash
    combined = "|".join(components)
    hash_obj = hashlib.sha256(combined.encode('utf-8'))
    
    # Retornar primeros 16 caracteres en mayusculas
    return hash_obj.hexdigest()[:16].upper()


def get_hardware_id_display() -> str:
    """
    Retorna el Hardware ID formateado para mostrar al usuario.
    Formato: XXXX-XXXX-XXXX-XXXX
    """
    hw_id = get_hardware_id()
    return f"{hw_id[:4]}-{hw_id[4:8]}-{hw_id[8:12]}-{hw_id[12:16]}"


if __name__ == "__main__":
    print("=" * 50)
    print("DINOS Tech - Generador de Hardware ID")
    print("=" * 50)
    print(f"\nHardware ID: {get_hardware_id_display()}")
    print(f"\nMAC Address: {get_mac_address()}")
    print(f"CPU ID: {get_cpu_id()}")
    print(f"Disk Serial: {get_disk_serial()}")
    print(f"Computer Name: {platform.node()}")
