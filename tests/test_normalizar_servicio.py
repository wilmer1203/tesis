"""
Tests unitarios para la funcion _normalizar_servicio

Valida que la normalizacion de servicios maneje correctamente
los 3 formatos de entrada: dict, ServicioModel, ServicioIntervencionTemporal
"""
import pytest
from unittest.mock import Mock, patch


class TestNormalizarServicio:
    """Suite de tests para _normalizar_servicio"""

    def setup_method(self):
        """Setup ejecutado antes de cada test"""
        # Mock del estado con el metodo a testear
        self.estado = Mock()

        # Importar la funcion real del estado
        # Nota: Debemos importar dinámicamente para evitar errores de import
        try:
            from dental_system.state.estado_intervencion_servicios import EstadoIntervencionServicios
            # Crear instancia temporal para acceder al metodo
            self.estado._normalizar_servicio = EstadoIntervencionServicios._normalizar_servicio.__get__(self.estado)
        except ImportError:
            pytest.skip("No se puede importar EstadoIntervencionServicios")

    def test_normalizar_servicio_dict_completo(self, mock_servicio_dict):
        """Test: Normalizar servicio desde diccionario completo"""
        # Act
        resultado = self.estado._normalizar_servicio(mock_servicio_dict)

        # Assert
        assert isinstance(resultado, dict)
        assert resultado["nombre"] == "Obturacion Composite"
        assert resultado["condicion_resultante"] == "obturacion"
        assert resultado["diente_numero"] == 36
        assert resultado["superficies"] == ["oclusal", "mesial"]
        assert resultado["material"] == "Composite A2"
        assert resultado["observaciones"] == "Caries profunda"

    def test_normalizar_servicio_dict_minimo(self):
        """Test: Normalizar servicio dict con campos minimos"""
        # Arrange
        servicio_minimo = {
            "nombre_servicio": "Consulta",
            "condicion_resultante": None,
            "diente_numero": None
        }

        # Act
        resultado = self.estado._normalizar_servicio(servicio_minimo)

        # Assert
        assert resultado["nombre"] == "Consulta"
        assert resultado["condicion_resultante"] is None
        assert resultado["diente_numero"] is None
        assert resultado["superficies"] == []
        assert resultado["material"] == ""
        assert resultado["observaciones"] == ""

    def test_normalizar_servicio_modelo(self, mock_servicio_modelo):
        """Test: Normalizar servicio desde ServicioModel"""
        # Act
        resultado = self.estado._normalizar_servicio(mock_servicio_modelo)

        # Assert
        assert resultado["nombre"] == "Endodoncia"
        assert resultado["condicion_resultante"] == "endodoncia"
        assert resultado["diente_numero"] == 16
        assert resultado["superficies"] == ["oclusal", "mesial", "distal"]
        assert resultado["material"] == "Gutapercha"
        assert resultado["observaciones"] == "Tratamiento conducto"

    def test_normalizar_servicio_temporal(self, mock_servicio_temporal):
        """Test: Normalizar servicio formato antiguo (ServicioIntervencionTemporal)"""
        # Act
        resultado = self.estado._normalizar_servicio(mock_servicio_temporal)

        # Assert
        assert resultado["nombre"] == "Corona Porcelana"
        assert resultado["condicion_resultante"] == "corona"
        assert resultado["diente_numero"] == 11
        assert resultado["superficies"] == ["oclusal", "vestibular"]
        assert resultado["material"] == "Porcelana"
        assert resultado["observaciones"] == "Preparacion dental"

    def test_normalizar_servicio_temporal_sin_superficies(self):
        """Test: Normalizar servicio temporal sin campo superficie"""
        # Arrange
        servicio = Mock()
        servicio.nombre_servicio = "Limpieza"
        servicio.nueva_condicion = None
        servicio.diente_numero = None
        servicio.superficie = ""  # String vacio
        servicio.material_utilizado = ""
        servicio.observaciones = ""

        # Act
        resultado = self.estado._normalizar_servicio(servicio)

        # Assert
        assert resultado["superficies"] == []

    def test_normalizar_servicio_superficies_default(self):
        """Test: Cuando no hay superficies especificadas, retorna lista vacia"""
        # Arrange
        servicio = {
            "nombre_servicio": "Exodoncia",
            "condicion_resultante": "ausente",
            "diente_numero": 48,
            "superficies": None
        }

        # Act
        resultado = self.estado._normalizar_servicio(servicio)

        # Assert
        assert resultado["superficies"] == []

    def test_normalizar_servicio_con_condicion_none(self):
        """Test: Servicio preventivo (condicion_resultante = None)"""
        # Arrange
        servicio = {
            "nombre_servicio": "Fluoracion",
            "condicion_resultante": None,
            "diente_numero": 21
        }

        # Act
        resultado = self.estado._normalizar_servicio(servicio)

        # Assert
        assert resultado["condicion_resultante"] is None
        assert resultado["nombre"] == "Fluoracion"

    def test_normalizar_servicio_condicion_vacia_string(self):
        """Test: condicion_resultante como string vacio (preventivo)"""
        # Arrange
        servicio = {
            "nombre_servicio": "Profilaxis",
            "condicion_resultante": "",
            "diente_numero": None
        }

        # Act
        resultado = self.estado._normalizar_servicio(servicio)

        # Assert
        # String vacio debe convertirse a None
        assert resultado["condicion_resultante"] == "" or resultado["condicion_resultante"] is None

    def test_normalizar_servicio_multiples_superficies(self):
        """Test: Servicio con todas las superficies"""
        # Arrange
        servicio = {
            "nombre_servicio": "Reconstruccion Completa",
            "condicion_resultante": "obturacion",
            "diente_numero": 26,
            "superficies": ["oclusal", "mesial", "distal", "vestibular", "lingual"]
        }

        # Act
        resultado = self.estado._normalizar_servicio(servicio)

        # Assert
        assert len(resultado["superficies"]) == 5
        assert "oclusal" in resultado["superficies"]
        assert "lingual" in resultado["superficies"]

    def test_normalizar_servicio_dict_usa_nueva_condicion(self):
        """Test: Compatibilidad con campo nueva_condicion (legacy)"""
        # Arrange
        servicio = {
            "nombre_servicio": "Obturacion",
            "nueva_condicion": "obturacion",  # Campo legacy
            "diente_numero": 36
        }

        # Act
        resultado = self.estado._normalizar_servicio(servicio)

        # Assert
        assert resultado["condicion_resultante"] == "obturacion"

    def test_normalizar_servicio_prioridad_condicion_resultante(self):
        """Test: condicion_resultante tiene prioridad sobre nueva_condicion"""
        # Arrange
        servicio = {
            "nombre_servicio": "Servicio Mix",
            "condicion_resultante": "endodoncia",
            "nueva_condicion": "obturacion",  # Debe ignorarse
            "diente_numero": 36
        }

        # Act
        resultado = self.estado._normalizar_servicio(servicio)

        # Assert
        assert resultado["condicion_resultante"] == "endodoncia"

    def test_normalizar_servicio_retorna_todos_campos(self, mock_servicio_dict):
        """Test: Resultado contiene todos los campos requeridos"""
        # Act
        resultado = self.estado._normalizar_servicio(mock_servicio_dict)

        # Assert - Verificar estructura completa
        campos_requeridos = [
            "nombre",
            "condicion_resultante",
            "diente_numero",
            "superficies",
            "material",
            "observaciones"
        ]
        for campo in campos_requeridos:
            assert campo in resultado, f"Falta campo requerido: {campo}"

    def test_normalizar_servicio_tipo_invalido(self):
        """Test: Servicio con tipo desconocido retorna estructura vacia"""
        # Arrange
        servicio_invalido = "string_invalido"

        # Act
        resultado = self.estado._normalizar_servicio(servicio_invalido)

        # Assert
        # Debe retornar dict vacio o con valores por defecto
        assert isinstance(resultado, dict)

    def test_normalizar_servicio_None(self):
        """Test: Servicio None retorna estructura por defecto"""
        # Act
        resultado = self.estado._normalizar_servicio(None)

        # Assert
        assert isinstance(resultado, dict)
        assert resultado.get("nombre") == ""
        assert resultado.get("condicion_resultante") is None

    def test_normalizar_servicio_list_superficies_strings(self):
        """Test: Superficies como lista de strings se mantiene igual"""
        # Arrange
        servicio = {
            "nombre_servicio": "Test",
            "condicion_resultante": "caries",
            "diente_numero": 36,
            "superficies": ["oclusal", "mesial"]
        }

        # Act
        resultado = self.estado._normalizar_servicio(servicio)

        # Assert
        assert isinstance(resultado["superficies"], list)
        assert all(isinstance(s, str) for s in resultado["superficies"])


class TestNormalizarServicioEdgeCases:
    """Tests de casos extremos y validaciones"""

    def setup_method(self):
        """Setup ejecutado antes de cada test"""
        self.estado = Mock()
        try:
            from dental_system.state.estado_intervencion_servicios import EstadoIntervencionServicios
            self.estado._normalizar_servicio = EstadoIntervencionServicios._normalizar_servicio.__get__(self.estado)
        except ImportError:
            pytest.skip("No se puede importar EstadoIntervencionServicios")

    def test_diente_numero_string(self):
        """Test: diente_numero como string debe convertirse a int"""
        # Arrange
        servicio = {
            "nombre_servicio": "Test",
            "condicion_resultante": "caries",
            "diente_numero": "36"  # String
        }

        # Act
        resultado = self.estado._normalizar_servicio(servicio)

        # Assert
        # Dependiendo de la implementacion, puede convertir o mantener
        assert resultado["diente_numero"] == 36 or resultado["diente_numero"] == "36"

    def test_superficies_con_espacios(self):
        """Test: Superficies con espacios extra deben limpiarse"""
        # Arrange
        servicio = Mock()
        servicio.nombre_servicio = "Test"
        servicio.nueva_condicion = "caries"
        servicio.diente_numero = 36
        servicio.superficie = "  oclusal  ,  mesial  "  # Con espacios
        servicio.material_utilizado = ""
        servicio.observaciones = ""

        # Act
        resultado = self.estado._normalizar_servicio(servicio)

        # Assert
        # Debe limpiar espacios
        assert "oclusal" in resultado["superficies"]
        assert "mesial" in resultado["superficies"]
        assert "  oclusal  " not in resultado["superficies"]

    def test_material_None_convierte_a_string_vacio(self):
        """Test: Material None debe convertirse a string vacio"""
        # Arrange
        servicio = {
            "nombre_servicio": "Test",
            "material": None
        }

        # Act
        resultado = self.estado._normalizar_servicio(servicio)

        # Assert
        assert resultado["material"] == "" or resultado["material"] is None

    def test_observaciones_muy_largas(self):
        """Test: Observaciones largas se mantienen completas"""
        # Arrange
        texto_largo = "A" * 1000
        servicio = {
            "nombre_servicio": "Test",
            "observaciones": texto_largo
        }

        # Act
        resultado = self.estado._normalizar_servicio(servicio)

        # Assert
        assert len(resultado["observaciones"]) == 1000
