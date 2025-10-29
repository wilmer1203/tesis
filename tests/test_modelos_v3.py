"""
Tests unitarios para modelos V3.0

Valida:
1. CondicionCatalogoModel
2. ActualizacionOdontogramaResult
3. ServicioModel.condicion_resultante
"""
import pytest
from decimal import Decimal


class TestCondicionCatalogoModel:
    """Tests para CondicionCatalogoModel"""

    def test_crear_modelo_desde_dict_completo(self):
        """Test: Crear modelo desde diccionario completo"""
        # Arrange
        from dental_system.models import CondicionCatalogoModel

        data = {
            "codigo": "caries",
            "nombre": "Caries",
            "categoria": "patologia",
            "prioridad": 8,
            "es_estado_final": False,
            "permite_reversion": True,
            "color_hex": "#FF6B6B",
            "descripcion": "Lesion dental"
        }

        # Act
        modelo = CondicionCatalogoModel.from_dict(data)

        # Assert
        assert modelo.codigo == "caries"
        assert modelo.nombre == "Caries"
        assert modelo.categoria == "patologia"
        assert modelo.prioridad == 8
        assert modelo.es_estado_final is False
        assert modelo.permite_reversion is True
        assert modelo.color_hex == "#FF6B6B"

    def test_crear_modelo_valores_default(self):
        """Test: Modelo con valores por defecto"""
        # Arrange
        from dental_system.models import CondicionCatalogoModel

        # Act
        modelo = CondicionCatalogoModel()

        # Assert
        assert modelo.codigo == ""
        assert modelo.nombre == ""
        assert modelo.categoria == ""
        assert modelo.prioridad == 1
        assert modelo.es_estado_final is False
        assert modelo.permite_reversion is True

    def test_nombre_display_con_emoji(self):
        """Test: Propiedad nombre_display incluye emoji segun categoria"""
        # Arrange
        from dental_system.models import CondicionCatalogoModel

        condicion = CondicionCatalogoModel.from_dict({
            "codigo": "sano",
            "nombre": "Sano",
            "categoria": "normal"
        })

        # Act
        display = condicion.nombre_display

        # Assert
        # Debe tener formato "emoji Nombre"
        assert "Sano" in display
        assert len(display) > len("Sano")  # Incluye emoji

    def test_categoria_display_formateada(self):
        """Test: categoria_display formatea correctamente"""
        # Arrange
        from dental_system.models import CondicionCatalogoModel

        condicion = CondicionCatalogoModel.from_dict({
            "codigo": "obturacion",
            "nombre": "Obturacion",
            "categoria": "restauracion"
        })

        # Act
        display = condicion.categoria_display

        # Assert
        assert display == "Restauracion"  # Capitalizado

    def test_es_reversible_property(self):
        """Test: Propiedad es_reversible"""
        # Arrange
        from dental_system.models import CondicionCatalogoModel

        reversible = CondicionCatalogoModel.from_dict({
            "codigo": "caries",
            "permite_reversion": True
        })

        irreversible = CondicionCatalogoModel.from_dict({
            "codigo": "ausente",
            "permite_reversion": False
        })

        # Assert
        assert reversible.es_reversible is True
        assert irreversible.es_reversible is False

    def test_from_dict_con_datos_faltantes(self):
        """Test: from_dict con diccionario incompleto usa defaults"""
        # Arrange
        from dental_system.models import CondicionCatalogoModel

        data_incompleto = {
            "codigo": "test"
            # Faltan otros campos
        }

        # Act
        modelo = CondicionCatalogoModel.from_dict(data_incompleto)

        # Assert
        assert modelo.codigo == "test"
        assert modelo.nombre == ""  # Default
        assert modelo.prioridad == 1  # Default


class TestActualizacionOdontogramaResult:
    """Tests para ActualizacionOdontogramaResult"""

    def test_crear_modelo_default(self):
        """Test: Crear modelo con valores por defecto"""
        # Arrange
        from dental_system.models import ActualizacionOdontogramaResult

        # Act
        resultado = ActualizacionOdontogramaResult()

        # Assert
        assert resultado.exitosos == 0
        assert resultado.fallidos == 0
        assert resultado.advertencias == []
        assert resultado.ids_creados == []

    def test_modelo_con_valores(self):
        """Test: Crear modelo con valores especificos"""
        # Arrange
        from dental_system.models import ActualizacionOdontogramaResult

        # Act
        resultado = ActualizacionOdontogramaResult(
            exitosos=5,
            fallidos=1,
            advertencias=["Advertencia 1"],
            ids_creados=["id1", "id2", "id3"]
        )

        # Assert
        assert resultado.exitosos == 5
        assert resultado.fallidos == 1
        assert len(resultado.advertencias) == 1
        assert len(resultado.ids_creados) == 3

    def test_total_procesados_computed(self):
        """Test: Propiedad total_procesados suma exitosos + fallidos"""
        # Arrange
        from dental_system.models import ActualizacionOdontogramaResult

        resultado = ActualizacionOdontogramaResult(
            exitosos=8,
            fallidos=2
        )

        # Act
        total = resultado.total_procesados

        # Assert
        assert total == 10

    def test_tasa_exito_pct_100(self):
        """Test: Tasa de exito 100% cuando todos exitosos"""
        # Arrange
        from dental_system.models import ActualizacionOdontogramaResult

        resultado = ActualizacionOdontogramaResult(
            exitosos=10,
            fallidos=0
        )

        # Act
        tasa = resultado.tasa_exito_pct

        # Assert
        assert tasa == 100.0

    def test_tasa_exito_pct_cero(self):
        """Test: Tasa de exito 0% cuando todos fallidos"""
        # Arrange
        from dental_system.models import ActualizacionOdontogramaResult

        resultado = ActualizacionOdontogramaResult(
            exitosos=0,
            fallidos=10
        )

        # Act
        tasa = resultado.tasa_exito_pct

        # Assert
        assert tasa == 0.0

    def test_tasa_exito_pct_parcial(self):
        """Test: Tasa de exito parcial"""
        # Arrange
        from dental_system.models import ActualizacionOdontogramaResult

        resultado = ActualizacionOdontogramaResult(
            exitosos=7,
            fallidos=3
        )

        # Act
        tasa = resultado.tasa_exito_pct

        # Assert
        assert tasa == 70.0

    def test_tasa_exito_pct_sin_procesados(self):
        """Test: Tasa de exito cuando no hay procesados"""
        # Arrange
        from dental_system.models import ActualizacionOdontogramaResult

        resultado = ActualizacionOdontogramaResult(
            exitosos=0,
            fallidos=0
        )

        # Act
        tasa = resultado.tasa_exito_pct

        # Assert
        assert tasa == 0.0  # Debe retornar 0 y no dividir por cero

    def test_tiene_advertencias_property(self):
        """Test: Propiedad tiene_advertencias"""
        # Arrange
        from dental_system.models import ActualizacionOdontogramaResult

        sin_advertencias = ActualizacionOdontogramaResult()
        con_advertencias = ActualizacionOdontogramaResult(
            advertencias=["Advertencia 1"]
        )

        # Assert
        assert sin_advertencias.tiene_advertencias is False
        assert con_advertencias.tiene_advertencias is True

    def test_operacion_exitosa_property(self):
        """Test: Propiedad operacion_exitosa"""
        # Arrange
        from dental_system.models import ActualizacionOdontogramaResult

        exitoso = ActualizacionOdontogramaResult(exitosos=5, fallidos=0)
        con_fallos = ActualizacionOdontogramaResult(exitosos=5, fallidos=1)
        sin_operaciones = ActualizacionOdontogramaResult(exitosos=0, fallidos=0)

        # Assert
        assert exitoso.operacion_exitosa is True
        assert con_fallos.operacion_exitosa is False
        assert sin_operaciones.operacion_exitosa is False


class TestServicioModelCondicionResultante:
    """Tests para campo condicion_resultante en ServicioModel"""

    def test_servicio_con_condicion_resultante(self):
        """Test: Servicio restaurativo con condicion_resultante"""
        # Arrange
        from dental_system.models import ServicioModel

        data = {
            "id": "serv_001",
            "nombre": "Obturacion Composite",
            "categoria": "Restaurativa",
            "precio_base": 50.0,
            "condicion_resultante": "obturacion"  # Campo V3.0
        }

        # Act
        servicio = ServicioModel.from_dict(data)

        # Assert
        assert servicio.condicion_resultante == "obturacion"

    def test_servicio_preventivo_sin_condicion(self):
        """Test: Servicio preventivo sin condicion_resultante"""
        # Arrange
        from dental_system.models import ServicioModel

        data = {
            "id": "serv_002",
            "nombre": "Limpieza Dental",
            "categoria": "Preventiva",
            "precio_base": 30.0,
            "condicion_resultante": None  # Preventivo
        }

        # Act
        servicio = ServicioModel.from_dict(data)

        # Assert
        assert servicio.condicion_resultante is None

    def test_modifica_odontograma_true(self):
        """Test: modifica_odontograma() retorna True si tiene condicion"""
        # Arrange
        from dental_system.models import ServicioModel

        servicio = ServicioModel.from_dict({
            "nombre": "Endodoncia",
            "condicion_resultante": "endodoncia"
        })

        # Act
        modifica = servicio.modifica_odontograma()

        # Assert
        assert modifica is True

    def test_modifica_odontograma_false(self):
        """Test: modifica_odontograma() retorna False si es preventivo"""
        # Arrange
        from dental_system.models import ServicioModel

        servicio = ServicioModel.from_dict({
            "nombre": "Consulta",
            "condicion_resultante": None
        })

        # Act
        modifica = servicio.modifica_odontograma()

        # Assert
        assert modifica is False

    def test_es_preventivo_property(self):
        """Test: Propiedad es_preventivo"""
        # Arrange
        from dental_system.models import ServicioModel

        preventivo = ServicioModel.from_dict({
            "nombre": "Fluoracion",
            "condicion_resultante": None
        })

        restaurativo = ServicioModel.from_dict({
            "nombre": "Obturacion",
            "condicion_resultante": "obturacion"
        })

        # Assert
        assert preventivo.es_preventivo is True
        assert restaurativo.es_preventivo is False

    def test_tipo_servicio_display_preventivo(self):
        """Test: tipo_servicio_display para servicio preventivo"""
        # Arrange
        from dental_system.models import ServicioModel

        servicio = ServicioModel.from_dict({
            "nombre": "Limpieza",
            "condicion_resultante": None
        })

        # Act
        display = servicio.tipo_servicio_display

        # Assert
        assert "Preventivo" in display

    def test_tipo_servicio_display_restaurativo(self):
        """Test: tipo_servicio_display para servicio restaurativo"""
        # Arrange
        from dental_system.models import ServicioModel

        servicio = ServicioModel.from_dict({
            "nombre": "Corona",
            "condicion_resultante": "corona"
        })

        # Act
        display = servicio.tipo_servicio_display

        # Assert
        assert "Restaurativo" in display
        assert "Corona" in display or "corona" in display.lower()

    def test_condicion_display_mapeo_correcto(self):
        """Test: condicion_display mapea codigos a labels"""
        # Arrange
        from dental_system.models import ServicioModel

        servicio = ServicioModel.from_dict({
            "nombre": "Test",
            "condicion_resultante": "caries"
        })

        # Act
        display = servicio.condicion_display

        # Assert
        # Debe tener formato con emoji
        assert "Caries" in display or "caries" in display.lower()
        assert len(display) > len("Caries")  # Incluye emoji

    def test_condicion_display_preventivo(self):
        """Test: condicion_display para servicio preventivo"""
        # Arrange
        from dental_system.models import ServicioModel

        servicio = ServicioModel.from_dict({
            "nombre": "Test",
            "condicion_resultante": None
        })

        # Act
        display = servicio.condicion_display

        # Assert
        assert "Preventivo" in display or "preventivo" in display.lower()


class TestModelosIntegracion:
    """Tests de integracion entre modelos"""

    def test_flujo_completo_actualizacion(self):
        """Test: Flujo completo desde servicio hasta resultado"""
        # Arrange
        from dental_system.models import ServicioModel, ActualizacionOdontogramaResult

        # 1. Crear servicio con condicion
        servicio = ServicioModel.from_dict({
            "nombre": "Obturacion",
            "condicion_resultante": "obturacion"
        })

        # 2. Verificar que modifica odontograma
        assert servicio.modifica_odontograma() is True

        # 3. Simular resultado de actualizacion
        resultado = ActualizacionOdontogramaResult(
            exitosos=1,
            fallidos=0,
            ids_creados=["cond_123"]
        )

        # Assert
        assert resultado.operacion_exitosa is True
        assert resultado.tasa_exito_pct == 100.0

    def test_condicion_catalogo_mapea_a_servicio(self):
        """Test: Codigo de catalogo se usa en servicio"""
        # Arrange
        from dental_system.models import CondicionCatalogoModel, ServicioModel

        # 1. Condicion del catalogo
        condicion = CondicionCatalogoModel.from_dict({
            "codigo": "endodoncia",
            "nombre": "Endodoncia",
            "prioridad": 6
        })

        # 2. Servicio que usa ese codigo
        servicio = ServicioModel.from_dict({
            "nombre": "Tratamiento de Conducto",
            "condicion_resultante": condicion.codigo
        })

        # Assert
        assert servicio.condicion_resultante == "endodoncia"
        assert servicio.modifica_odontograma() is True
