"""Models package - ACTUALIZADO CON MODELOS DEL ADMIN"""

from .boss_models import (
    UsuarioModel,
    RolModel, 
    PersonalModel,
    ServicioModel,
    DashboardStatsModel,
    # PacientesStatsModel,
    PagosStatsModel
)

from .admin_models import (
    PacienteModel,
    AdminStatsModel,
    ConsultaModel,
    PagoModel,
    PacientesStatsModel
)

__all__ = [
    # Modelos del Boss
    "UsuarioModel",
    "RolModel",
    "PersonalModel", 
    "ServicioModel",
    "DashboardStatsModel",
    # "PacientesStatsModel",
    "PagosStatsModel",
    
    # Modelos del Admin
    "PacienteModel",
    "AdminStatsModel", 
    "ConsultaModel",
    "PagoModel",
    "PacientesStatsModel"
]
