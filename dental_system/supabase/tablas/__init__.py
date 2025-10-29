"""
Módulo de tablas CRUD para Supabase - LIMPIEZA 2025-10-21.

Este módulo exporta todas las clases de tablas y sus instancias únicas
para facilitar el acceso desde otros módulos del sistema.

✅ 12/12 TABLAS ACTIVAS (limpiadas 3 obsoletas)
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

# ✅ TABLAS ESPECIALIZADAS ACTIVAS
from .roles import RolesTable, roles_table
# ❌ OBSOLETO: from .dientes import DientesTable, dientes_table (tabla eliminada en migración V2.0)
from .condiciones_diente import CondicionesDienteTable, condiciones_diente_table
# ❌ OBSOLETO: from .odontograma import OdontogramsTable, odontograms_table (tabla eliminada en migración V2.0)
from .historial_medico import HistorialMedicoTable, historial_medico_table
from .imagenes_clinicas import ImagenesClinicasTable, imagenes_clinicas_table
# ❌ ELIMINADO 2025-10-21: from .configuracion_sistema import ConfiguracionSistemaTable, configuracion_sistema_table
# ❌ ELIMINADO 2025-10-21: from .auditoria import AuditoriaTable, auditoria_table
# ❌ ELIMINADO 2025-10-21: from .cola_atencion import ColaAtencionTable, cola_atencion_table

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

    # ✅ CLASES DE TABLAS ESPECIALIZADAS
    "RolesTable", "CondicionesDienteTable",
    "HistorialMedicoTable", "ImagenesClinicasTable",

    # ✅ INSTANCIAS PRINCIPALES (BACKWARD COMPATIBLE)
    "users_table", "personal_table", "services_table", "servicios_table", "pacientes_table",
    "consultas_table", "interventions_table", "payments_table", "pagos_table",

    # ✅ INSTANCIAS ESPECIALIZADAS
    "usuarios_table", "roles_table", "condiciones_diente_table",
    "historial_medico_table", "imagenes_clinicas_table"
]

