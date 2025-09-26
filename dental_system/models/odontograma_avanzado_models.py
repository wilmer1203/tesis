"""
Modelos Avanzados para Odontograma Interactivo V2.0
Sistema completo de dientes interactivos con superficies clickeables
"""
import reflex as rx
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from enum import Enum


class TipoCondicion(str, Enum):
    """Tipos de condiciones dentales disponibles"""
    SANO = "sano"
    CARIES = "caries"
    RESTAURACION = "restauracion"
    CORONA = "corona"
    ENDODONCIA = "endodoncia"
    EXTRACCION = "extraccion"
    IMPLANTE = "implante"
    AUSENTE = "ausente"
    FRACTURA = "fractura"
    PROTESIS = "protesis"
    SELLANTE = "sellante"
    DESMINERALIZACION = "desmineralizacion"


class SeveridadCondicion(str, Enum):
    """Niveles de severidad para condiciones"""
    LEVE = "leve"
    MODERADA = "moderada"
    SEVERA = "severa"
    CRITICA = "critica"


class CaraDiente(str, Enum):
    """Caras/superficies de un diente"""
    OCLUSAL = "oclusal"      # Superficie de masticación
    MESIAL = "mesial"        # Superficie hacia el centro
    DISTAL = "distal"        # Superficie hacia afuera
    VESTIBULAR = "vestibular" # Superficie hacia los labios/mejillas
    LINGUAL = "lingual"      # Superficie hacia la lengua


class CondicionCaraModel(rx.Base):
    """
    Modelo para condición específica de una cara del diente

    Cada cara del diente puede tener su propia condición independiente
    """
    cara: str = CaraDiente.OCLUSAL
    tipo_condicion: str = TipoCondicion.SANO
    severidad: str = SeveridadCondicion.LEVE
    color_hex: str = "#4ECDC4"  # Verde para sano por defecto
    fecha_registro: str = ""
    fecha_ultima_modificacion: str = ""
    notas: str = ""
    requiere_atencion: bool = False
    costo_estimado_usd: float = 0.0

    @property
    def tiene_condicion(self) -> bool:
        """Verificar si la cara tiene alguna condición diferente a sano"""
        return self.tipo_condicion != TipoCondicion.SANO

    @property
    def es_condicion_critica(self) -> bool:
        """Verificar si la condición requiere atención inmediata"""
        condiciones_criticas = [
            TipoCondicion.CARIES,
            TipoCondicion.FRACTURA,
            TipoCondicion.EXTRACCION
        ]
        return (self.tipo_condicion in condiciones_criticas or
                self.severidad == SeveridadCondicion.CRITICA)

    @property
    def color_por_condicion(self) -> str:
        """Obtener color automático según tipo de condición"""
        colores_condiciones = {
            TipoCondicion.SANO: "#4ECDC4",           # Verde agua
            TipoCondicion.CARIES: "#FF6B6B",         # Rojo
            TipoCondicion.RESTAURACION: "#45B7D1",   # Azul
            TipoCondicion.CORONA: "#96CEB4",         # Verde claro
            TipoCondicion.ENDODONCIA: "#FFEAA7",     # Amarillo
            TipoCondicion.EXTRACCION: "#2D3436",     # Negro
            TipoCondicion.IMPLANTE: "#A29BFE",       # Morado
            TipoCondicion.AUSENTE: "#DDD",           # Gris claro
            TipoCondicion.FRACTURA: "#E17055",       # Naranja
            TipoCondicion.PROTESIS: "#F39C12",       # Naranja dorado
            TipoCondicion.SELLANTE: "#00B894",       # Verde
            TipoCondicion.DESMINERALIZACION: "#FDCB6E" # Amarillo claro
        }
        return colores_condiciones.get(self.tipo_condicion, "#4ECDC4")

    @property
    def descripcion_condicion(self) -> str:
        """Descripción legible de la condición"""
        descripciones = {
            TipoCondicion.SANO: "Superficie sana",
            TipoCondicion.CARIES: "Caries dental",
            TipoCondicion.RESTAURACION: "Restauración/Obturación",
            TipoCondicion.CORONA: "Corona dental",
            TipoCondicion.ENDODONCIA: "Tratamiento endodóntico",
            TipoCondicion.EXTRACCION: "Extracción indicada",
            TipoCondicion.IMPLANTE: "Implante dental",
            TipoCondicion.AUSENTE: "Superficie ausente",
            TipoCondicion.FRACTURA: "Fractura dental",
            TipoCondicion.PROTESIS: "Prótesis",
            TipoCondicion.SELLANTE: "Sellante de fosas",
            TipoCondicion.DESMINERALIZACION: "Desmineralización"
        }
        return descripciones.get(self.tipo_condicion, "Condición desconocida")

    @classmethod
    def crear_sana(cls, cara: str) -> "CondicionCaraModel":
        """Factory method para crear cara sana"""
        return cls(
            cara=cara,
            tipo_condicion=TipoCondicion.SANO,
            severidad=SeveridadCondicion.LEVE,
            color_hex="#4ECDC4",
            fecha_registro=datetime.now().isoformat(),
            requiere_atencion=False
        )

    @classmethod
    def crear_con_condicion(cls,
                           cara: str,
                           tipo_condicion: str,
                           severidad: str = SeveridadCondicion.LEVE,
                           notas: str = "") -> "CondicionCaraModel":
        """Factory method para crear cara con condición específica"""
        condicion = cls(
            cara=cara,
            tipo_condicion=tipo_condicion,
            severidad=severidad,
            fecha_registro=datetime.now().isoformat(),
            fecha_ultima_modificacion=datetime.now().isoformat(),
            notas=notas
        )

        # Asignar color automático
        condicion.color_hex = condicion.color_por_condicion

        # Determinar si requiere atención
        condicion.requiere_atencion = condicion.es_condicion_critica

        return condicion


class DienteInteractivoModel(rx.Base):
    """
    Modelo para diente completamente interactivo con 5 caras clickeables

    Cada diente del odontograma FDI con estado interactivo completo
    """
    numero_fdi: int = 11
    nombre_diente: str = ""
    tipo_diente: str = "permanente"  # permanente, temporal
    cuadrante: int = 1  # 1, 2, 3, 4
    posicion_en_cuadrante: int = 1  # 1-8

    # Coordenadas para posicionamiento en UI
    posicion_x: float = 0.0
    posicion_y: float = 0.0

    # Estados por cara (5 caras por diente)
    cara_oclusal: CondicionCaraModel = CondicionCaraModel.crear_sana(CaraDiente.OCLUSAL)
    cara_mesial: CondicionCaraModel = CondicionCaraModel.crear_sana(CaraDiente.MESIAL)
    cara_distal: CondicionCaraModel = CondicionCaraModel.crear_sana(CaraDiente.DISTAL)
    cara_vestibular: CondicionCaraModel = CondicionCaraModel.crear_sana(CaraDiente.VESTIBULAR)
    cara_lingual: CondicionCaraModel = CondicionCaraModel.crear_sana(CaraDiente.LINGUAL)

    # Estados interactivos de UI
    is_selected: bool = False
    is_hovered: bool = False
    show_details: bool = False
    cara_seleccionada: str = ""

    # Metadatos del diente
    fecha_ultima_actualizacion: str = ""
    version_odontograma_id: str = ""
    notas_generales: str = ""

    @property
    def tiene_condiciones(self) -> bool:
        """Verificar si el diente tiene alguna condición registrada"""
        return any([
            self.cara_oclusal.tiene_condicion,
            self.cara_mesial.tiene_condicion,
            self.cara_distal.tiene_condicion,
            self.cara_vestibular.tiene_condicion,
            self.cara_lingual.tiene_condicion
        ])

    @property
    def condiciones_criticas(self) -> List[CondicionCaraModel]:
        """Obtener lista de caras con condiciones críticas"""
        caras = [
            self.cara_oclusal,
            self.cara_mesial,
            self.cara_distal,
            self.cara_vestibular,
            self.cara_lingual
        ]
        return [cara for cara in caras if cara.es_condicion_critica]

    @property
    def numero_condiciones_activas(self) -> int:
        """Contar número de caras con condiciones"""
        caras = [
            self.cara_oclusal,
            self.cara_mesial,
            self.cara_distal,
            self.cara_vestibular,
            self.cara_lingual
        ]
        return sum(1 for cara in caras if cara.tiene_condicion)

    @property
    def color_estado_general(self) -> str:
        """Color del diente según estado general (prioritario)"""
        # Prioridad: crítico > tiene condiciones > sano
        if len(self.condiciones_criticas) > 0:
            return "#FF6B6B"  # Rojo para crítico
        elif self.tiene_condiciones:
            return "#FFEAA7"  # Amarillo para atención
        else:
            return "#4ECDC4"  # Verde para sano

    @property
    def estado_display(self) -> str:
        """Estado legible para mostrar en UI"""
        if len(self.condiciones_criticas) > 0:
            return f"⚠️ {len(self.condiciones_criticas)} condiciones críticas"
        elif self.tiene_condiciones:
            return f"📋 {self.numero_condiciones_activas} condiciones"
        else:
            return "✅ Sano"

    @property
    def costo_total_estimado(self) -> float:
        """Costo total estimado de tratamientos necesarios"""
        caras = [
            self.cara_oclusal,
            self.cara_mesial,
            self.cara_distal,
            self.cara_vestibular,
            self.cara_lingual
        ]
        return sum(cara.costo_estimado_usd for cara in caras if cara.tiene_condicion)

    @property
    def es_numero_fdi_valido(self) -> bool:
        """Validar si el número FDI es válido"""
        # Números FDI válidos para dientes permanentes
        numeros_validos = set()

        # Cuadrantes 1-4, posiciones 1-8
        for cuadrante in [1, 2, 3, 4]:
            for posicion in [1, 2, 3, 4, 5, 6, 7, 8]:
                numeros_validos.add(cuadrante * 10 + posicion)

        return self.numero_fdi in numeros_validos

    def get_cara_por_nombre(self, nombre_cara: str) -> Optional[CondicionCaraModel]:
        """Obtener cara específica por nombre"""
        caras_map = {
            CaraDiente.OCLUSAL: self.cara_oclusal,
            CaraDiente.MESIAL: self.cara_mesial,
            CaraDiente.DISTAL: self.cara_distal,
            CaraDiente.VESTIBULAR: self.cara_vestibular,
            CaraDiente.LINGUAL: self.cara_lingual
        }
        return caras_map.get(nombre_cara)

    def actualizar_cara(self,
                       nombre_cara: str,
                       tipo_condicion: str,
                       severidad: str = SeveridadCondicion.LEVE,
                       notas: str = "") -> bool:
        """
        Actualizar condición de una cara específica

        Args:
            nombre_cara: Nombre de la cara a actualizar
            tipo_condicion: Nuevo tipo de condición
            severidad: Severidad de la condición
            notas: Notas adicionales

        Returns:
            True si se actualizó correctamente
        """
        cara = self.get_cara_por_nombre(nombre_cara)
        if not cara:
            return False

        cara.tipo_condicion = tipo_condicion
        cara.severidad = severidad
        cara.notas = notas
        cara.color_hex = cara.color_por_condicion
        cara.fecha_ultima_modificacion = datetime.now().isoformat()
        cara.requiere_atencion = cara.es_condicion_critica

        # Actualizar metadatos del diente
        self.fecha_ultima_actualizacion = datetime.now().isoformat()

        return True

    def resetear_cara(self, nombre_cara: str) -> bool:
        """Resetear cara a estado sano"""
        return self.actualizar_cara(
            nombre_cara,
            TipoCondicion.SANO,
            SeveridadCondicion.LEVE,
            ""
        )

    def get_resumen_condiciones(self) -> Dict[str, Any]:
        """Obtener resumen completo de condiciones del diente"""
        caras = [
            ("oclusal", self.cara_oclusal),
            ("mesial", self.cara_mesial),
            ("distal", self.cara_distal),
            ("vestibular", self.cara_vestibular),
            ("lingual", self.cara_lingual)
        ]

        resumen = {
            "numero_fdi": self.numero_fdi,
            "nombre_diente": self.nombre_diente,
            "estado_general": self.estado_display,
            "color_estado": self.color_estado_general,
            "tiene_condiciones": self.tiene_condiciones,
            "condiciones_criticas": len(self.condiciones_criticas),
            "costo_estimado": self.costo_total_estimado,
            "caras": {}
        }

        for nombre_cara, cara in caras:
            resumen["caras"][nombre_cara] = {
                "tipo_condicion": cara.tipo_condicion,
                "severidad": cara.severidad,
                "descripcion": cara.descripcion_condicion,
                "color": cara.color_hex,
                "requiere_atencion": cara.requiere_atencion,
                "tiene_condicion": cara.tiene_condicion,
                "costo_estimado": cara.costo_estimado_usd,
                "notas": cara.notas
            }

        return resumen

    @classmethod
    def crear_diente_fdi(cls, numero_fdi: int) -> "DienteInteractivoModel":
        """
        Factory method para crear diente según número FDI

        Args:
            numero_fdi: Número FDI del diente (11-18, 21-28, 31-38, 41-48)

        Returns:
            Diente interactivo configurado
        """
        # Extraer cuadrante y posición del número FDI
        cuadrante = numero_fdi // 10
        posicion = numero_fdi % 10

        # Nombres de dientes según posición FDI
        nombres_dientes = {
            1: "Incisivo central",
            2: "Incisivo lateral",
            3: "Canino",
            4: "Primer premolar",
            5: "Segundo premolar",
            6: "Primer molar",
            7: "Segundo molar",
            8: "Tercer molar (cordal)"
        }

        # Nombres de cuadrantes
        nombres_cuadrantes = {
            1: "superior derecho",
            2: "superior izquierdo",
            3: "inferior izquierdo",
            4: "inferior derecho"
        }

        nombre_completo = f"{nombres_dientes.get(posicion, 'Diente')} {nombres_cuadrantes.get(cuadrante, '')}"

        # Calcular posición aproximada en grid
        # Esto se puede ajustar según el layout final
        pos_x = (posicion - 1) * 100 + (100 if cuadrante in [2, 3] else 0)
        pos_y = 100 if cuadrante in [1, 2] else 200

        return cls(
            numero_fdi=numero_fdi,
            nombre_diente=nombre_completo,
            tipo_diente="permanente",
            cuadrante=cuadrante,
            posicion_en_cuadrante=posicion,
            posicion_x=pos_x,
            posicion_y=pos_y,
            fecha_ultima_actualizacion=datetime.now().isoformat()
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DienteInteractivoModel":
        """Factory method desde diccionario (para cargar desde BD)"""
        if not data or not isinstance(data, dict):
            return cls()

        # Crear diente base
        diente = cls.crear_diente_fdi(data.get("numero_fdi", 11))

        # Actualizar con datos específicos
        diente.nombre_diente = data.get("nombre_diente", diente.nombre_diente)
        diente.tipo_diente = data.get("tipo_diente", "permanente")
        diente.posicion_x = data.get("posicion_x", diente.posicion_x)
        diente.posicion_y = data.get("posicion_y", diente.posicion_y)
        diente.notas_generales = data.get("notas_generales", "")

        # Cargar condiciones de caras si existen
        if "cara_oclusal" in data:
            diente.cara_oclusal = CondicionCaraModel(**data["cara_oclusal"])
        if "cara_mesial" in data:
            diente.cara_mesial = CondicionCaraModel(**data["cara_mesial"])
        if "cara_distal" in data:
            diente.cara_distal = CondicionCaraModel(**data["cara_distal"])
        if "cara_vestibular" in data:
            diente.cara_vestibular = CondicionCaraModel(**data["cara_vestibular"])
        if "cara_lingual" in data:
            diente.cara_lingual = CondicionCaraModel(**data["cara_lingual"])

        return diente


class OdontogramaInteractivoModel(rx.Base):
    """
    Modelo para odontograma interactivo completo

    Contiene los 32 dientes con estado interactivo completo
    """
    id: str = ""
    numero_historia: str = ""
    version: int = 1
    tipo_odontograma: str = "adulto"  # adulto (32), pediatrico (20), mixto

    # Metadatos de versión
    es_version_actual: bool = True
    id_version_anterior: str = ""
    motivo_nueva_version: str = ""
    fecha_creacion: str = ""
    fecha_ultima_modificacion: str = ""

    # Dientes del odontograma (32 dientes para adulto)
    dientes: List[DienteInteractivoModel] = []

    # Estados de UI
    diente_seleccionado_fdi: int = 0
    cara_seleccionada: str = ""
    modo_edicion: bool = False

    # Metadatos clínicos
    notas_clinicas: str = ""
    plan_tratamiento: str = ""
    costo_total_estimado: float = 0.0

    @property
    def tiene_condiciones_activas(self) -> bool:
        """Verificar si hay condiciones activas en el odontograma"""
        return any(diente.tiene_condiciones for diente in self.dientes)

    @property
    def numero_dientes_afectados(self) -> int:
        """Contar dientes con condiciones"""
        return sum(1 for diente in self.dientes if diente.tiene_condiciones)

    @property
    def dientes_criticos(self) -> List[DienteInteractivoModel]:
        """Obtener dientes con condiciones críticas"""
        return [diente for diente in self.dientes if len(diente.condiciones_criticas) > 0]

    @property
    def resumen_estado(self) -> str:
        """Resumen del estado general del odontograma"""
        if len(self.dientes_criticos) > 0:
            return f"⚠️ {len(self.dientes_criticos)} dientes requieren atención urgente"
        elif self.numero_dientes_afectados > 0:
            return f"📋 {self.numero_dientes_afectados} dientes con condiciones"
        else:
            return "✅ Odontograma sin condiciones patológicas"

    def get_diente_por_fdi(self, numero_fdi: int) -> Optional[DienteInteractivoModel]:
        """Obtener diente específico por número FDI"""
        for diente in self.dientes:
            if diente.numero_fdi == numero_fdi:
                return diente
        return None

    def actualizar_diente_cara(self,
                              numero_fdi: int,
                              nombre_cara: str,
                              tipo_condicion: str,
                              severidad: str = SeveridadCondicion.LEVE,
                              notas: str = "") -> bool:
        """Actualizar condición de cara específica de un diente"""
        diente = self.get_diente_por_fdi(numero_fdi)
        if not diente:
            return False

        success = diente.actualizar_cara(nombre_cara, tipo_condicion, severidad, notas)

        if success:
            self.fecha_ultima_modificacion = datetime.now().isoformat()
            self._recalcular_costo_total()

        return success

    def _recalcular_costo_total(self):
        """Recalcular costo total estimado del odontograma"""
        self.costo_total_estimado = sum(
            diente.costo_total_estimado for diente in self.dientes
        )

    @classmethod
    def crear_odontograma_adulto(cls, numero_historia: str) -> "OdontogramaInteractivoModel":
        """
        Factory method para crear odontograma adulto completo (32 dientes)

        Args:
            numero_historia: HC del paciente

        Returns:
            Odontograma interactivo con 32 dientes
        """
        # Crear dientes FDI estándar para adulto
        numeros_fdi = []

        # Cuadrante 1 (superior derecho): 11-18
        numeros_fdi.extend([11, 12, 13, 14, 15, 16, 17, 18])

        # Cuadrante 2 (superior izquierdo): 21-28
        numeros_fdi.extend([21, 22, 23, 24, 25, 26, 27, 28])

        # Cuadrante 3 (inferior izquierdo): 31-38
        numeros_fdi.extend([31, 32, 33, 34, 35, 36, 37, 38])

        # Cuadrante 4 (inferior derecho): 41-48
        numeros_fdi.extend([41, 42, 43, 44, 45, 46, 47, 48])

        # Crear dientes interactivos
        dientes = [
            DienteInteractivoModel.crear_diente_fdi(numero_fdi)
            for numero_fdi in numeros_fdi
        ]

        return cls(
            numero_historia=numero_historia,
            version=1,
            tipo_odontograma="adulto",
            es_version_actual=True,
            fecha_creacion=datetime.now().isoformat(),
            fecha_ultima_modificacion=datetime.now().isoformat(),
            dientes=dientes,
            motivo_nueva_version="Odontograma inicial"
        )


# Constantes para uso en componentes
CONDICIONES_DISPONIBLES = [
    {"tipo": TipoCondicion.SANO, "nombre": "Sano", "color": "#4ECDC4"},
    {"tipo": TipoCondicion.CARIES, "nombre": "Caries", "color": "#FF6B6B"},
    {"tipo": TipoCondicion.RESTAURACION, "nombre": "Restauración", "color": "#45B7D1"},
    {"tipo": TipoCondicion.CORONA, "nombre": "Corona", "color": "#96CEB4"},
    {"tipo": TipoCondicion.ENDODONCIA, "nombre": "Endodoncia", "color": "#FFEAA7"},
    {"tipo": TipoCondicion.EXTRACCION, "nombre": "Extracción", "color": "#2D3436"},
    {"tipo": TipoCondicion.IMPLANTE, "nombre": "Implante", "color": "#A29BFE"},
    {"tipo": TipoCondicion.AUSENTE, "nombre": "Ausente", "color": "#DDD"},
    {"tipo": TipoCondicion.FRACTURA, "nombre": "Fractura", "color": "#E17055"},
    {"tipo": TipoCondicion.PROTESIS, "nombre": "Prótesis", "color": "#F39C12"},
    {"tipo": TipoCondicion.SELLANTE, "nombre": "Sellante", "color": "#00B894"},
    {"tipo": TipoCondicion.DESMINERALIZACION, "nombre": "Desmineralización", "color": "#FDCB6E"}
]

CARAS_DIENTE = [
    {"nombre": CaraDiente.OCLUSAL, "display": "Oclusal"},
    {"nombre": CaraDiente.MESIAL, "display": "Mesial"},
    {"nombre": CaraDiente.DISTAL, "display": "Distal"},
    {"nombre": CaraDiente.VESTIBULAR, "display": "Vestibular"},
    {"nombre": CaraDiente.LINGUAL, "display": "Lingual"}
]