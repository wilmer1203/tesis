"""
Módulo de tablas CRUD para Supabase.

Este módulo exporta todas las clases de tablas para facilitar
el acceso desde otros módulos del sistema.
"""

from .base import BaseTable
from .usuarios import UsersTable
from .personal import PersonalTable
from .servicios import ServicesTable
from .pacientes import PacientesTable
from .consultas import ConsultationsTable
from . intervenciones import InterventionsTable

# Instancias únicas para toda la aplicación (Singleton pattern)
users_table = UsersTable()
personal_table = PersonalTable()
services_table = ServicesTable()
pacientes_table = PacientesTable()
consultas_table = ConsultationsTable()
interventions_table = InterventionsTable()
__all__ = [
    "BaseTable",
    "UsersTable",
    "PersonalTable", 
    "ServicesTable",
    "PacientesTable",
    "ConsultationsTable",
    "InterventionsTable",
    # Instancias
    "users_table",
    "personal_table",
    "services_table",
    "pacientes_table",
    "consultas_table",
    "interventions_table"
]

