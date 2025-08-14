"""
Módulo de tablas CRUD para Supabase - COMPLETO Y ACTUALIZADO.

Este módulo exporta todas las clases de tablas y sus instancias únicas
para facilitar el acceso desde otros módulos del sistema.

✅ 15/15 TABLAS IMPLEMENTADAS
"""

# ✅ TABLAS PRINCIPALES ORIGINALES
from .base import BaseTable
from .usuarios import UsersTable, usuarios_table
from .personal import PersonalTable, personal_table  
from .servicios import ServicesTable, services_table
from .pacientes import PacientesTable, pacientes_table
from .consultas import ConsultationsTable, consultas_table
from .intervenciones import InterventionsTable, interventions_table
from .pagos import PaymentsTable, payments_table

# ✅ NUEVAS TABLAS COMPLETADAS 
from .roles import RolesTable, roles_table
from .dientes import DientesTable, dientes_table
from .condiciones_diente import CondicionesDienteTable, condiciones_diente_table
from .odontograma import OdontogramsTable, odontograms_table
from .historial_medico import HistorialMedicoTable, historial_medico_table
from .imagenes_clinicas import ImagenesClinicasTable, imagenes_clinicas_table
from .configuracion_sistema import ConfiguracionSistemaTable, configuracion_sistema_table
from .auditoria import AuditoriaTable, auditoria_table

# ✅ INSTANCIAS ÚNICAS EXPORTADAS (Singleton pattern)
# Para importar: from dental_system.supabase.tablas import pacientes_table, consultas_table

# ✅ BACKWARD COMPATIBILITY - Alias para imports existentes
users_table = usuarios_table
personal_table = personal_table
services_table = services_table
servicios_table = services_table  # Alias adicional
pacientes_table = pacientes_table
consultas_table = consultas_table 
interventions_table = interventions_table
payments_table = payments_table
pagos_table = payments_table  # Alias adicional para pagos_service

__all__ = [
    # ✅ CLASES BASE
    "BaseTable",
    
    # ✅ CLASES DE TABLAS PRINCIPALES
    "UsersTable", "PersonalTable", "ServicesTable", "PacientesTable",
    "ConsultationsTable", "InterventionsTable", "PaymentsTable",
    
    # ✅ CLASES DE TABLAS NUEVAS
    "RolesTable", "DientesTable", "CondicionesDienteTable", "OdontogramsTable",
    "HistorialMedicoTable", "ImagenesClinicasTable", "ConfiguracionSistemaTable", "AuditoriaTable",
    
    # ✅ INSTANCIAS PRINCIPALES (BACKWARD COMPATIBLE)
    "users_table", "personal_table", "services_table", "servicios_table", "pacientes_table",
    "consultas_table", "interventions_table", "payments_table", "pagos_table",
    
    # ✅ INSTANCIAS NUEVAS
    "usuarios_table", "roles_table", "dientes_table", "condiciones_diente_table",
    "odontograms_table", "historial_medico_table", "imagenes_clinicas_table", 
    "configuracion_sistema_table", "auditoria_table"
]

