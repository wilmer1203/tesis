"""
Configuracion de pytest para tests del sistema odontologico
"""
import pytest
import sys
from pathlib import Path
from typing import Dict, Any, List
from unittest.mock import Mock, AsyncMock

# Agregar directorio raiz al path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))


@pytest.fixture
def mock_paciente_actual():
    """Fixture: Paciente mock para tests"""
    return Mock(
        id="pac_123456",
        primer_nombre="Juan",
        primer_apellido="Perez",
        numero_documento="12345678"
    )


@pytest.fixture
def mock_servicio_dict():
    """Fixture: Servicio en formato diccionario"""
    return {
        "nombre_servicio": "Obturacion Composite",
        "condicion_resultante": "obturacion",
        "diente_numero": 36,
        "superficies": ["oclusal", "mesial"],
        "material": "Composite A2",
        "observaciones": "Caries profunda"
    }


@pytest.fixture
def mock_servicio_modelo():
    """Fixture: Servicio como ServicioModel"""
    servicio = Mock()
    servicio.nombre = "Endodoncia"
    servicio.condicion_resultante = "endodoncia"
    servicio.diente_numero = 16
    servicio.superficies = ["oclusal", "mesial", "distal"]
    servicio.material = "Gutapercha"
    servicio.observaciones = "Tratamiento conducto"
    return servicio


@pytest.fixture
def mock_servicio_temporal():
    """Fixture: Servicio como ServicioIntervencionTemporal (formato antiguo)"""
    servicio = Mock()
    servicio.nombre_servicio = "Corona Porcelana"
    servicio.nueva_condicion = "corona"
    servicio.diente_numero = 11
    servicio.superficie = "oclusal, vestibular"
    servicio.material_utilizado = "Porcelana"
    servicio.observaciones = "Preparacion dental"
    return servicio


@pytest.fixture
def mock_servicios_con_conflicto():
    """Fixture: Lista de servicios que afectan mismo diente/superficie"""
    return [
        {
            "nombre": "Limpieza",
            "condicion_resultante": "sano",
            "diente_numero": 36,
            "superficies": ["oclusal"],
            "material": "",
            "observaciones": "Limpieza profunda"
        },
        {
            "nombre": "Obturacion",
            "condicion_resultante": "obturacion",
            "diente_numero": 36,
            "superficies": ["oclusal"],
            "material": "Composite",
            "observaciones": "Caries detectada"
        },
        {
            "nombre": "Endodoncia",
            "condicion_resultante": "endodoncia",
            "diente_numero": 36,
            "superficies": ["oclusal"],
            "material": "Gutapercha",
            "observaciones": "Pulpitis irreversible"
        }
    ]


@pytest.fixture
def mock_catalogo_condiciones():
    """Fixture: Catalogo de condiciones mock con prioridades"""
    return [
        {
            "codigo": "sano",
            "nombre": "Sano",
            "categoria": "normal",
            "prioridad": 1,
            "es_estado_final": False,
            "permite_reversion": True,
            "color_hex": "#90EE90"
        },
        {
            "codigo": "obturacion",
            "nombre": "Obturacion",
            "categoria": "restauracion",
            "prioridad": 5,
            "es_estado_final": False,
            "permite_reversion": True,
            "color_hex": "#4ECDC4"
        },
        {
            "codigo": "endodoncia",
            "nombre": "Endodoncia",
            "categoria": "restauracion",
            "prioridad": 6,
            "es_estado_final": False,
            "permite_reversion": False,
            "color_hex": "#A8E6CF"
        },
        {
            "codigo": "caries",
            "nombre": "Caries",
            "categoria": "patologia",
            "prioridad": 8,
            "es_estado_final": False,
            "permite_reversion": True,
            "color_hex": "#FF6B6B"
        },
        {
            "codigo": "ausente",
            "nombre": "Ausente",
            "categoria": "ausencia",
            "prioridad": 10,
            "es_estado_final": True,
            "permite_reversion": False,
            "color_hex": "#808080"
        }
    ]


@pytest.fixture
def mock_odontologia_service():
    """Fixture: Mock del servicio de odontologia"""
    service = Mock()
    service.get_catalogo_condiciones = AsyncMock(return_value=[])
    service.actualizar_condiciones_batch = AsyncMock(return_value={
        "success": True,
        "exitosos": 2,
        "fallidos": 0,
        "ids_creados": ["cond_1", "cond_2"]
    })
    service.set_user_context = Mock()
    return service


@pytest.fixture
def mock_actualizacion_result():
    """Fixture: Resultado de actualizacion mock"""
    from dental_system.models import ActualizacionOdontogramaResult
    return ActualizacionOdontogramaResult(
        exitosos=2,
        fallidos=0,
        advertencias=[],
        ids_creados=["cond_1", "cond_2"]
    )


@pytest.fixture
def mock_estado_servicios():
    """Fixture: Estado de servicios mock"""
    estado = Mock()
    estado.id_usuario = "user_123"
    estado.perfil_usuario = {"rol": "odontologo"}
    estado.catalogo_condiciones = []
    estado.condiciones_cargadas = False
    estado.cargando_catalogo_condiciones = False
    return estado
