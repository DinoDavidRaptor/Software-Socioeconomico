"""
Validador de licencias offline.
Sistema de proteccion basado en Hardware ID + License Key.
Copyright (c) 2026 DINOS Tech. Todos los derechos reservados.
"""

import hashlib
import json
import os
from datetime import datetime
from typing import Optional, Tuple

from .hardware_id import get_hardware_id


class LicenseValidator:
    """
    Valida licencias offline usando Hardware ID.
    
    Las licencias son generadas por DINOS Tech y vinculadas
    al hardware especifico del cliente.
    """
    
    # Secreto usado para validar licencias (ofuscado en el binario)
    _SECRET_SALT = "D1N0S_T3CH_2026_S0C10EC0N0M1C0"
    
    def __init__(self, license_file: str = "license.dat"):
        """
        Inicializa el validador.
        
        Args:
            license_file: Ruta al archivo de licencia
        """
        self.license_file = license_file
        self._license_data: Optional[dict] = None
        self._is_valid = False
        self._error_message = ""
    
    def _generate_expected_key(self, hardware_id: str, license_type: str, 
                                expiry_date: str) -> str:
        """
        Genera la key esperada basada en los datos de licencia.
        Esta funcion debe coincidir con la del generador.
        """
        data = f"{hardware_id}|{license_type}|{expiry_date}|{self._SECRET_SALT}"
        hash_obj = hashlib.sha256(data.encode('utf-8'))
        full_hash = hash_obj.hexdigest().upper()
        
        # Formato: XXXX-XXXX-XXXX-XXXX-XXXX
        return f"{full_hash[:4]}-{full_hash[4:8]}-{full_hash[8:12]}-{full_hash[12:16]}-{full_hash[16:20]}"
    
    def _load_license_file(self) -> bool:
        """Carga el archivo de licencia."""
        if not os.path.exists(self.license_file):
            self._error_message = "Archivo de licencia no encontrado"
            return False
        
        try:
            with open(self.license_file, 'r', encoding='utf-8') as f:
                self._license_data = json.load(f)
            return True
        except json.JSONDecodeError:
            self._error_message = "Archivo de licencia corrupto"
            return False
        except Exception as e:
            self._error_message = f"Error al leer licencia: {str(e)}"
            return False
    
    def validate(self) -> Tuple[bool, str]:
        """
        Valida la licencia del software.
        
        Returns:
            Tuple[bool, str]: (es_valida, mensaje)
        """
        # Cargar archivo
        if not self._load_license_file():
            return False, self._error_message
        
        # Verificar campos requeridos
        required_fields = ['hardware_id', 'license_key', 'license_type', 
                          'expiry_date', 'licensed_to']
        for field in required_fields:
            if field not in self._license_data:
                return False, f"Licencia invalida: falta campo {field}"
        
        # Verificar Hardware ID
        current_hw_id = get_hardware_id()
        licensed_hw_id = self._license_data['hardware_id']
        
        if current_hw_id != licensed_hw_id:
            return False, "Licencia no valida para este equipo"
        
        # Verificar fecha de expiracion
        expiry_str = self._license_data['expiry_date']
        if expiry_str != "PERPETUA":
            try:
                expiry_date = datetime.strptime(expiry_str, "%Y-%m-%d")
                if datetime.now() > expiry_date:
                    return False, f"Licencia expirada el {expiry_str}"
            except ValueError:
                return False, "Fecha de expiracion invalida"
        
        # Verificar firma de la licencia
        expected_key = self._generate_expected_key(
            licensed_hw_id,
            self._license_data['license_type'],
            expiry_str
        )
        
        if self._license_data['license_key'] != expected_key:
            return False, "Licencia invalida o manipulada"
        
        # Licencia valida
        self._is_valid = True
        license_type = self._license_data['license_type']
        licensed_to = self._license_data['licensed_to']
        
        if expiry_str == "PERPETUA":
            return True, f"Licencia {license_type} activa para: {licensed_to}"
        else:
            return True, f"Licencia {license_type} activa hasta {expiry_str} para: {licensed_to}"
    
    def is_valid(self) -> bool:
        """Retorna si la licencia es valida."""
        return self._is_valid
    
    def get_license_info(self) -> Optional[dict]:
        """Retorna informacion de la licencia si es valida."""
        if self._is_valid and self._license_data:
            return {
                'licensed_to': self._license_data.get('licensed_to', ''),
                'license_type': self._license_data.get('license_type', ''),
                'expiry_date': self._license_data.get('expiry_date', ''),
                'company': self._license_data.get('company', ''),
            }
        return None
    
    def activate_license(self, license_key: str, licensed_to: str, 
                         company: str = "") -> Tuple[bool, str]:
        """
        Activa una licencia con la key proporcionada.
        
        Args:
            license_key: Key de licencia en formato XXXX-XXXX-XXXX-XXXX-XXXX
            licensed_to: Nombre del licenciatario
            company: Nombre de la empresa (opcional)
            
        Returns:
            Tuple[bool, str]: (exito, mensaje)
        """
        # Validar formato de key
        parts = license_key.strip().upper().split('-')
        if len(parts) != 5 or not all(len(p) == 4 for p in parts):
            return False, "Formato de licencia invalido. Use: XXXX-XXXX-XXXX-XXXX-XXXX"
        
        # Obtener Hardware ID actual
        hw_id = get_hardware_id()
        
        # Probar diferentes tipos de licencia y fechas
        license_types = ['PROFESIONAL', 'EMPRESARIAL', 'BASICA']
        expiry_options = ['PERPETUA']
        
        # Agregar fechas futuras para probar (1, 2, 3 anos)
        from datetime import timedelta
        for years in [1, 2, 3, 5, 10]:
            future_date = datetime.now() + timedelta(days=365 * years)
            expiry_options.append(future_date.strftime("%Y-%m-%d"))
        
        # Buscar combinacion valida
        for license_type in license_types:
            for expiry in expiry_options:
                expected_key = self._generate_expected_key(hw_id, license_type, expiry)
                if expected_key == license_key.upper():
                    # Key valida - guardar licencia
                    license_data = {
                        'hardware_id': hw_id,
                        'license_key': license_key.upper(),
                        'license_type': license_type,
                        'expiry_date': expiry,
                        'licensed_to': licensed_to,
                        'company': company,
                        'activation_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    
                    try:
                        with open(self.license_file, 'w', encoding='utf-8') as f:
                            json.dump(license_data, f, indent=2, ensure_ascii=False)
                        
                        self._license_data = license_data
                        self._is_valid = True
                        
                        if expiry == 'PERPETUA':
                            return True, f"Licencia {license_type} perpetua activada correctamente"
                        else:
                            return True, f"Licencia {license_type} activada hasta {expiry}"
                    except Exception as e:
                        return False, f"Error al guardar licencia: {str(e)}"
        
        return False, "Licencia invalida para este equipo"


def check_license_on_startup(license_file: str = "license.dat") -> Tuple[bool, str, Optional[dict]]:
    """
    Funcion helper para verificar licencia al iniciar la aplicacion.
    
    Returns:
        Tuple[bool, str, Optional[dict]]: (es_valida, mensaje, info_licencia)
    """
    validator = LicenseValidator(license_file)
    is_valid, message = validator.validate()
    license_info = validator.get_license_info() if is_valid else None
    return is_valid, message, license_info
