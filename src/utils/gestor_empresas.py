"""
Gestor de empresas solicitantes de estudios socioeconómicos.
Autor: DINOS Tech
Versión: 0.3.0
"""

import json
import os
from typing import List, Dict


class GestorEmpresas:
    """Gestiona las empresas que solicitan estudios socioeconómicos."""
    
    ARCHIVO_EMPRESAS = "empresas.json"
    
    @classmethod
    def cargar_empresas(cls) -> List[str]:
        """
        Carga la lista de empresas desde el archivo JSON.
        
        Returns:
            Lista de nombres de empresas
        """
        if not os.path.exists(cls.ARCHIVO_EMPRESAS):
            # Crear archivo con empresa por defecto
            cls.guardar_empresas(["DINOS Tech"])
            return ["DINOS Tech"]
        
        try:
            with open(cls.ARCHIVO_EMPRESAS, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("empresas", ["DINOS Tech"])
        except Exception as e:
            print(f"Error cargando empresas: {e}")
            return ["DINOS Tech"]
    
    @classmethod
    def guardar_empresas(cls, empresas: List[str]) -> bool:
        """
        Guarda la lista de empresas en el archivo JSON.
        
        Args:
            empresas: Lista de nombres de empresas
            
        Returns:
            True si se guardó correctamente, False en caso contrario
        """
        try:
            data = {"empresas": empresas}
            with open(cls.ARCHIVO_EMPRESAS, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error guardando empresas: {e}")
            return False
    
    @classmethod
    def agregar_empresa(cls, nombre_empresa: str) -> bool:
        """
        Agrega una nueva empresa a la lista.
        
        Args:
            nombre_empresa: Nombre de la empresa a agregar
            
        Returns:
            True si se agregó correctamente, False si ya existe o hay error
        """
        if not nombre_empresa or not nombre_empresa.strip():
            return False
        
        nombre_empresa = nombre_empresa.strip()
        empresas = cls.cargar_empresas()
        
        if nombre_empresa in empresas:
            return False  # Ya existe
        
        empresas.append(nombre_empresa)
        return cls.guardar_empresas(empresas)
    
    @classmethod
    def eliminar_empresa(cls, nombre_empresa: str) -> bool:
        """
        Elimina una empresa de la lista.
        
        Args:
            nombre_empresa: Nombre de la empresa a eliminar
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        empresas = cls.cargar_empresas()
        
        if nombre_empresa not in empresas:
            return False
        
        # No permitir eliminar si es la única empresa
        if len(empresas) == 1:
            return False
        
        empresas.remove(nombre_empresa)
        return cls.guardar_empresas(empresas)
