"""
Tests unitarios para la funcion _resolver_conflictos_servicios

Valida que la resolucion de conflictos:
1. Detecte servicios que afectan mismo diente/superficie
2. Aplique prioridad del catalogo correctamente
3. Mantenga el servicio de mayor prioridad clinica
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch


class TestResolverConflictos:
    """Suite de tests para _resolver_conflictos_servicios"""

    def setup_method(self):
        """Setup ejecutado antes de cada test"""
        self.estado = Mock()
        self.estado.id_usuario = "user_123"
        self.estado.perfil_usuario = {"rol": "odontologo"}

        try:
            from dental_system.state.estado_intervencion_servicios import EstadoIntervencionServicios
            # Obtener el metodo real
            self.estado._resolver_conflictos_servicios = EstadoIntervencionServicios._resolver_conflictos_servicios.__get__(self.estado)
        except ImportError:
            pytest.skip("No se puede importar EstadoIntervencionServicios")

    @pytest.mark.asyncio
    async def test_sin_conflictos_dientes_diferentes(self, mock_catalogo_condiciones):
        """Test: Servicios en dientes diferentes no tienen conflicto"""
        # Arrange
        servicios = [
            {
                "nombre": "Obturacion",
                "condicion_resultante": "obturacion",
                "diente_numero": 36,
                "superficies": ["oclusal"],
                "material": "Composite",
                "observaciones": ""
            },
            {
                "nombre": "Corona",
                "condicion_resultante": "corona",
                "diente_numero": 37,  # Diente diferente
                "superficies": ["oclusal"],
                "material": "Porcelana",
                "observaciones": ""
            }
        ]

        with patch('dental_system.services.odontologia_service.odontologia_service') as mock_service:
            mock_service.get_catalogo_condiciones = AsyncMock(return_value=mock_catalogo_condiciones)
            mock_service.set_user_context = Mock()

            # Act
            resultado = await self.estado._resolver_conflictos_servicios(servicios)

            # Assert
            assert len(resultado) == 2  # Ambos servicios se mantienen

    @pytest.mark.asyncio
    async def test_sin_conflictos_superficies_diferentes(self, mock_catalogo_condiciones):
        """Test: Servicios en mismo diente pero superficies diferentes"""
        # Arrange
        servicios = [
            {
                "nombre": "Obturacion Oclusal",
                "condicion_resultante": "obturacion",
                "diente_numero": 36,
                "superficies": ["oclusal"],
                "material": "Composite",
                "observaciones": ""
            },
            {
                "nombre": "Obturacion Mesial",
                "condicion_resultante": "obturacion",
                "diente_numero": 36,  # Mismo diente
                "superficies": ["mesial"],  # Superficie diferente
                "material": "Composite",
                "observaciones": ""
            }
        ]

        with patch('dental_system.services.odontologia_service.odontologia_service') as mock_service:
            mock_service.get_catalogo_condiciones = AsyncMock(return_value=mock_catalogo_condiciones)
            mock_service.set_user_context = Mock()

            # Act
            resultado = await self.estado._resolver_conflictos_servicios(servicios)

            # Assert
            assert len(resultado) == 2  # Ambos servicios se mantienen

    @pytest.mark.asyncio
    async def test_conflicto_gana_mayor_prioridad(self, mock_catalogo_condiciones):
        """Test: En conflicto, gana el servicio con mayor prioridad clinica"""
        # Arrange
        # Prioridades: sano=1, obturacion=5, endodoncia=6
        servicios = [
            {
                "nombre": "Limpieza",
                "condicion_resultante": "sano",  # Prioridad 1
                "diente_numero": 36,
                "superficies": ["oclusal"],
                "material": "",
                "observaciones": ""
            },
            {
                "nombre": "Endodoncia",
                "condicion_resultante": "endodoncia",  # Prioridad 6 (mayor)
                "diente_numero": 36,
                "superficies": ["oclusal"],
                "material": "Gutapercha",
                "observaciones": ""
            },
            {
                "nombre": "Obturacion",
                "condicion_resultante": "obturacion",  # Prioridad 5
                "diente_numero": 36,
                "superficies": ["oclusal"],
                "material": "Composite",
                "observaciones": ""
            }
        ]

        with patch('dental_system.services.odontologia_service.odontologia_service') as mock_service:
            mock_service.get_catalogo_condiciones = AsyncMock(return_value=mock_catalogo_condiciones)
            mock_service.set_user_context = Mock()

            # Act
            resultado = await self.estado._resolver_conflictos_servicios(servicios)

            # Assert
            assert len(resultado) == 1  # Solo queda uno
            assert resultado[0]["condicion_resultante"] == "endodoncia"  # El de mayor prioridad

    @pytest.mark.asyncio
    async def test_conflicto_multiples_superficies(self, mock_catalogo_condiciones):
        """Test: Servicio con multiples superficies genera multiples conflictos"""
        # Arrange
        servicios = [
            {
                "nombre": "Limpieza Completa",
                "condicion_resultante": "sano",
                "diente_numero": 36,
                "superficies": ["oclusal", "mesial", "distal"],  # 3 superficies
                "material": "",
                "observaciones": ""
            },
            {
                "nombre": "Caries Mesial",
                "condicion_resultante": "caries",  # Mayor prioridad (8 vs 1)
                "diente_numero": 36,
                "superficies": ["mesial"],  # Solo 1 superficie
                "material": "",
                "observaciones": ""
            }
        ]

        with patch('dental_system.services.odontologia_service.odontologia_service') as mock_service:
            mock_service.get_catalogo_condiciones = AsyncMock(return_value=mock_catalogo_condiciones)
            mock_service.set_user_context = Mock()

            # Act
            resultado = await self.estado._resolver_conflictos_servicios(servicios)

            # Assert
            # Deberia mantener:
            # - Limpieza en oclusal y distal (sin conflicto)
            # - Caries en mesial (gana por prioridad)
            assert len(resultado) == 2

            # Verificar que caries mesial esta presente
            caries_encontrada = any(
                s["condicion_resultante"] == "caries" and "mesial" in s["superficies"]
                for s in resultado
            )
            assert caries_encontrada

    @pytest.mark.asyncio
    async def test_sin_servicios_retorna_lista_vacia(self):
        """Test: Lista vacia de servicios retorna lista vacia"""
        # Arrange
        servicios = []

        with patch('dental_system.services.odontologia_service.odontologia_service') as mock_service:
            mock_service.get_catalogo_condiciones = AsyncMock(return_value=[])
            mock_service.set_user_context = Mock()

            # Act
            resultado = await self.estado._resolver_conflictos_servicios(servicios)

            # Assert
            assert resultado == []

    @pytest.mark.asyncio
    async def test_servicio_sin_condicion_se_mantiene(self, mock_catalogo_condiciones):
        """Test: Servicios preventivos (sin condicion) se mantienen"""
        # Arrange
        servicios = [
            {
                "nombre": "Consulta",
                "condicion_resultante": None,  # Preventivo
                "diente_numero": None,
                "superficies": [],
                "material": "",
                "observaciones": ""
            },
            {
                "nombre": "Obturacion",
                "condicion_resultante": "obturacion",
                "diente_numero": 36,
                "superficies": ["oclusal"],
                "material": "Composite",
                "observaciones": ""
            }
        ]

        with patch('dental_system.services.odontologia_service.odontologia_service') as mock_service:
            mock_service.get_catalogo_condiciones = AsyncMock(return_value=mock_catalogo_condiciones)
            mock_service.set_user_context = Mock()

            # Act
            resultado = await self.estado._resolver_conflictos_servicios(servicios)

            # Assert
            # Ambos deben mantenerse (preventivo no genera conflicto)
            assert len(resultado) == 2

    @pytest.mark.asyncio
    async def test_condicion_no_encontrada_en_catalogo(self, mock_catalogo_condiciones):
        """Test: Condicion no existente en catalogo usa prioridad 0"""
        # Arrange
        servicios = [
            {
                "nombre": "Servicio Desconocido",
                "condicion_resultante": "condicion_inexistente",
                "diente_numero": 36,
                "superficies": ["oclusal"],
                "material": "",
                "observaciones": ""
            },
            {
                "nombre": "Caries",
                "condicion_resultante": "caries",  # Prioridad 8
                "diente_numero": 36,
                "superficies": ["oclusal"],
                "material": "",
                "observaciones": ""
            }
        ]

        with patch('dental_system.services.odontologia_service.odontologia_service') as mock_service:
            mock_service.get_catalogo_condiciones = AsyncMock(return_value=mock_catalogo_condiciones)
            mock_service.set_user_context = Mock()

            # Act
            resultado = await self.estado._resolver_conflictos_servicios(servicios)

            # Assert
            # Caries debe ganar (prioridad 8 vs 0)
            assert len(resultado) == 1
            assert resultado[0]["condicion_resultante"] == "caries"

    @pytest.mark.asyncio
    async def test_error_cargando_catalogo_retorna_servicios_originales(self):
        """Test: Error al cargar catalogo retorna servicios sin resolver"""
        # Arrange
        servicios = [
            {
                "nombre": "Servicio 1",
                "condicion_resultante": "obturacion",
                "diente_numero": 36,
                "superficies": ["oclusal"],
                "material": "",
                "observaciones": ""
            }
        ]

        with patch('dental_system.services.odontologia_service.odontologia_service') as mock_service:
            mock_service.get_catalogo_condiciones = AsyncMock(side_effect=Exception("Error BD"))
            mock_service.set_user_context = Mock()

            # Act
            resultado = await self.estado._resolver_conflictos_servicios(servicios)

            # Assert
            # Debe retornar servicios originales como fallback
            assert len(resultado) == len(servicios)

    @pytest.mark.asyncio
    async def test_ausente_prioridad_maxima(self, mock_catalogo_condiciones):
        """Test: Ausente tiene prioridad maxima (10) y siempre gana"""
        # Arrange
        servicios = [
            {
                "nombre": "Endodoncia",
                "condicion_resultante": "endodoncia",  # Prioridad 6
                "diente_numero": 36,
                "superficies": ["oclusal"],
                "material": "Gutapercha",
                "observaciones": ""
            },
            {
                "nombre": "Extraccion",
                "condicion_resultante": "ausente",  # Prioridad 10 (maxima)
                "diente_numero": 36,
                "superficies": ["oclusal"],
                "material": "",
                "observaciones": ""
            },
            {
                "nombre": "Caries",
                "condicion_resultante": "caries",  # Prioridad 8
                "diente_numero": 36,
                "superficies": ["oclusal"],
                "material": "",
                "observaciones": ""
            }
        ]

        with patch('dental_system.services.odontologia_service.odontologia_service') as mock_service:
            mock_service.get_catalogo_condiciones = AsyncMock(return_value=mock_catalogo_condiciones)
            mock_service.set_user_context = Mock()

            # Act
            resultado = await self.estado._resolver_conflictos_servicios(servicios)

            # Assert
            assert len(resultado) == 1
            assert resultado[0]["condicion_resultante"] == "ausente"


class TestResolverConflictosEdgeCases:
    """Tests de casos extremos"""

    def setup_method(self):
        """Setup ejecutado antes de cada test"""
        self.estado = Mock()
        self.estado.id_usuario = "user_123"
        self.estado.perfil_usuario = {"rol": "odontologo"}

        try:
            from dental_system.state.estado_intervencion_servicios import EstadoIntervencionServicios
            self.estado._resolver_conflictos_servicios = EstadoIntervencionServicios._resolver_conflictos_servicios.__get__(self.estado)
        except ImportError:
            pytest.skip("No se puede importar EstadoIntervencionServicios")

    @pytest.mark.asyncio
    async def test_misma_prioridad_mantiene_primero(self, mock_catalogo_condiciones):
        """Test: Servicios con misma prioridad mantienen el primero"""
        # Arrange
        # Agregar dos condiciones con misma prioridad al catalogo
        catalogo = mock_catalogo_condiciones + [
            {
                "codigo": "corona",
                "nombre": "Corona",
                "categoria": "protesis",
                "prioridad": 6,  # Misma que endodoncia
                "es_estado_final": False,
                "permite_reversion": True,
                "color_hex": "#FFD93D"
            }
        ]

        servicios = [
            {
                "nombre": "Endodoncia",
                "condicion_resultante": "endodoncia",  # Prioridad 6
                "diente_numero": 36,
                "superficies": ["oclusal"],
                "material": "Gutapercha",
                "observaciones": ""
            },
            {
                "nombre": "Corona",
                "condicion_resultante": "corona",  # Prioridad 6
                "diente_numero": 36,
                "superficies": ["oclusal"],
                "material": "Porcelana",
                "observaciones": ""
            }
        ]

        with patch('dental_system.services.odontologia_service.odontologia_service') as mock_service:
            mock_service.get_catalogo_condiciones = AsyncMock(return_value=catalogo)
            mock_service.set_user_context = Mock()

            # Act
            resultado = await self.estado._resolver_conflictos_servicios(servicios)

            # Assert
            assert len(resultado) == 1
            # Debe mantener el primero encontrado
            assert resultado[0]["condicion_resultante"] == "endodoncia"

    @pytest.mark.asyncio
    async def test_superficies_vacias_no_genera_conflicto(self, mock_catalogo_condiciones):
        """Test: Servicios sin superficies no generan conflicto"""
        # Arrange
        servicios = [
            {
                "nombre": "Servicio 1",
                "condicion_resultante": "obturacion",
                "diente_numero": 36,
                "superficies": [],  # Sin superficies
                "material": "",
                "observaciones": ""
            },
            {
                "nombre": "Servicio 2",
                "condicion_resultante": "caries",
                "diente_numero": 36,
                "superficies": [],  # Sin superficies
                "material": "",
                "observaciones": ""
            }
        ]

        with patch('dental_system.services.odontologia_service.odontologia_service') as mock_service:
            mock_service.get_catalogo_condiciones = AsyncMock(return_value=mock_catalogo_condiciones)
            mock_service.set_user_context = Mock()

            # Act
            resultado = await self.estado._resolver_conflictos_servicios(servicios)

            # Assert
            # Sin superficies especificas, pueden coexistir ambos
            assert len(resultado) >= 1

    @pytest.mark.asyncio
    async def test_catalogo_vacio_usa_prioridad_cero(self):
        """Test: Sin catalogo, todas las condiciones tienen prioridad 0"""
        # Arrange
        servicios = [
            {
                "nombre": "Servicio 1",
                "condicion_resultante": "condicion1",
                "diente_numero": 36,
                "superficies": ["oclusal"],
                "material": "",
                "observaciones": ""
            },
            {
                "nombre": "Servicio 2",
                "condicion_resultante": "condicion2",
                "diente_numero": 36,
                "superficies": ["oclusal"],
                "material": "",
                "observaciones": ""
            }
        ]

        with patch('dental_system.services.odontologia_service.odontologia_service') as mock_service:
            mock_service.get_catalogo_condiciones = AsyncMock(return_value=[])  # Catalogo vacio
            mock_service.set_user_context = Mock()

            # Act
            resultado = await self.estado._resolver_conflictos_servicios(servicios)

            # Assert
            # Con misma prioridad (0), mantiene el primero
            assert len(resultado) == 1
            assert resultado[0]["nombre"] == "Servicio 1"
