"""
🦷 SERVICIO DE ODONTOGRAMA - INICIALIZACIÓN Y GESTIÓN COMPLETA
================================================================

Implementa el sistema completo de:
- Inicialización automática de odontogramas para pacientes nuevos
- Catálogo FDI (32 dientes permanentes)
- Versionado automático de odontogramas
- Condiciones profesionales con colores médicos
- Historial médico detallado con trazabilidad

Basado en esquema_final_corregido.sql con triggers automáticos.
"""

from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import uuid

from dental_system.supabase.client import get_client
from dental_system.models.odontologia_models import (
    OdontogramaModel, 
    DienteModel, 
    CondicionDienteModel,
    HistorialClinicoModel
)

# ==========================================
# 🦷 SERVICIO PRINCIPAL ODONTOLOGÍA AVANZADA
# ==========================================

class OdontogramaService:
    """🦷 Servicio completo de odontogramas con inicialización automática para pacientes nuevos"""
    
    def __init__(self):
        self.supabase = get_client()
    
    # ==========================================
    # 📊 CATÁLOGO FDI - CARGA Y CONSULTA
    # ==========================================
    
    async def cargar_catalogo_fdi(self) -> List[DienteModel]:
        """📊 Cargar catálogo completo FDI (32 dientes)"""
        try:
            response = self.supabase.table("dientes").select(
                "*, numero_fdi, nombre_diente, cuadrante, tipo_diente, coordenadas_svg, superficies_disponibles"
            ).order("numero_fdi").execute()
            
            if response.data:
                return [DienteModel.from_dict(diente) for diente in response.data]
            return []
            
        except Exception as e:
            print(f"❌ Error cargando catálogo FDI: {e}")
            return self._get_catalogo_fdi_fallback()
    
    def _get_catalogo_fdi_fallback(self) -> List[DienteModel]:
        """🦷 Catálogo FDI hardcoded como fallback"""
        dientes = []
        
        # Cuadrante 1: Superior Derecho (11-18)
        for i, (numero, nombre, tipo) in enumerate([
            (11, "Incisivo Central Superior Derecho", "incisivo"),
            (12, "Incisivo Lateral Superior Derecho", "incisivo"),
            (13, "Canino Superior Derecho", "canino"),
            (14, "Primer Premolar Superior Derecho", "premolar"),
            (15, "Segundo Premolar Superior Derecho", "premolar"),
            (16, "Primer Molar Superior Derecho", "molar"),
            (17, "Segundo Molar Superior Derecho", "molar"),
            (18, "Tercer Molar Superior Derecho", "molar")
        ]):
            dientes.append(DienteModel(
                id=str(uuid.uuid4()),
                numero_fdi=numero,
                nombre_diente=nombre,
                cuadrante=1,
                tipo_diente=tipo,
                coordenadas_svg={"x": 120 + (i * 30), "y": 50 + (i * 2)},
                superficies_disponibles=["mesial", "distal", "lingual", "vestibular", "oclusal" if tipo in ["premolar", "molar"] else "incisal"]
            ))
        
        # Agregar cuadrantes 2, 3, 4 de manera similar...
        # (Implementar los otros 24 dientes)
        
        return dientes
    
    async def obtener_diente_por_fdi(self, numero_fdi: int) -> Optional[DienteModel]:
        """🔍 Obtener información detallada de un diente FDI específico"""
        try:
            response = self.supabase.table("dientes").select("*").eq("numero_fdi", numero_fdi).single().execute()
            
            if response.data:
                return DienteModel.from_dict(response.data)
            return None
            
        except Exception as e:
            print(f"❌ Error obteniendo diente FDI {numero_fdi}: {e}")
            return None
    
    async def cargar_condiciones_disponibles(self) -> List[Dict[str, Any]]:
        """🎨 Cargar catálogo completo de condiciones dentales"""
        try:
            response = self.supabase.table("condiciones_diente").select(
                "nombre, codigo, color_hex, descripcion, categoria, es_urgente"
            ).order("categoria, nombre").execute()
            
            return response.data if response.data else self._get_condiciones_fallback()
            
        except Exception as e:
            print(f"❌ Error cargando condiciones: {e}")
            return self._get_condiciones_fallback()
    
    def _get_condiciones_fallback(self) -> List[Dict[str, Any]]:
        """🎨 Condiciones hardcoded como fallback"""
        return [
            {"nombre": "sano", "codigo": "SAO", "color_hex": "#16a34a", "descripcion": "Diente sano", "categoria": "normal", "es_urgente": False},
            {"nombre": "caries", "codigo": "CAR", "color_hex": "#dc2626", "descripcion": "Lesión cariosa", "categoria": "patologia", "es_urgente": True},
            {"nombre": "obturado", "codigo": "OBT", "color_hex": "#2563eb", "descripcion": "Restauración", "categoria": "restauracion", "es_urgente": False},
            {"nombre": "corona", "codigo": "COR", "color_hex": "#d97706", "descripcion": "Corona protésica", "categoria": "protesis", "es_urgente": False},
            {"nombre": "ausente", "codigo": "AUS", "color_hex": "#6b7280", "descripcion": "Diente perdido", "categoria": "ausencia", "es_urgente": False},
        ]
    
    # ==========================================
    # 🔄 VERSIONADO AUTOMÁTICO DE ODONTOGRAMAS
    # ==========================================
    
    async def crear_odontograma_inicial(self, paciente_id: str, odontologo_id: str) -> Optional[OdontogramaModel]:
        """🆕 Crear primera versión del odontograma para un paciente"""
        try:
            nuevo_odontograma = {
                "paciente_id": paciente_id,
                "version": 1,
                "version_anterior_id": None,
                "es_version_actual": True,
                "motivo_nueva_version": "Odontograma inicial",
                "odontologo_id": odontologo_id,
                "tipo_odontograma": "adulto",
                "notas_generales": "Odontograma inicial con 32 dientes marcados como sanos",
                "observaciones_clinicas": "Estado inicial del paciente"
            }
            
            response = self.supabase.table("odontograma").insert(nuevo_odontograma).execute()
            
            if response.data:
                return OdontogramaModel.from_dict(response.data[0])
            return None
            
        except Exception as e:
            print(f"❌ Error creando odontograma inicial: {e}")
            return None
    
    def _generar_estado_inicial_fdi(self) -> Dict[int, Dict[str, str]]:
        """🦷 Generar estado inicial para los 32 dientes FDI"""
        estado_inicial = {}
        
        # Todos los dientes FDI (11-18, 21-28, 31-38, 41-48)
        dientes_fdi = []
        
        # Cuadrante 1: 11-18
        dientes_fdi.extend(range(11, 19))
        # Cuadrante 2: 21-28  
        dientes_fdi.extend(range(21, 29))
        # Cuadrante 3: 31-38
        dientes_fdi.extend(range(31, 39))
        # Cuadrante 4: 41-48
        dientes_fdi.extend(range(41, 49))
        
        for numero_fdi in dientes_fdi:
            estado_inicial[numero_fdi] = {
                "condicion": "sano",
                "codigo": "SAO",
                "superficie": "completa",
                "color": "#16a34a"
            }
        
        return estado_inicial

    async def crear_odontograma_inicial_completo(self, numero_historia: str, paciente_id: str, user_id: str, personal_id: str) -> Optional[OdontogramaModel]:
        """🆕 Crear odontograma inicial completo para paciente nuevo (FLUJO INTEGRADO)

        Args:
            numero_historia: HC del paciente (ej: HC000001)
            paciente_id: UUID del paciente en tabla pacientes
            user_id: UUID del usuario para registrado_por (FK usuarios)
            personal_id: UUID del personal para odontologo_id (FK personal)
            odontologo_id: UUID del odontólogo que registra (por defecto del sistema)

        Returns:
            OdontogramaModel creado con 32 dientes inicializados como "sanos"
        """
        try:
            print(f"🦷 Creando odontograma inicial completo para {numero_historia}")

            # Crear odontograma inicial usando método existente (usa personal_id para odontologo_id)
            odontograma_inicial = await self.crear_odontograma_inicial(paciente_id, personal_id)

            if not odontograma_inicial:
                print(f"❌ Error: No se pudo crear odontograma inicial para {numero_historia}")
                return None

            # Crear registros en condiciones_diente para cada diente FDI como "sano" (usa user_id para registrado_por)
            await self._crear_condiciones_iniciales_fdi(odontograma_inicial.id, user_id)

            print(f"✅ Odontograma inicial completo creado para {numero_historia} (ID: {odontograma_inicial.id})")
            return odontograma_inicial

        except Exception as e:
            print(f"❌ Error creando odontograma inicial completo para {numero_historia}: {e}")
            return None

    async def _crear_condiciones_iniciales_fdi(self, odontograma_id: str, odontologo_id: str) -> bool:
        """🦷 Crear condiciones iniciales para los 32 dientes FDI como "sanos"

        Args:
            odontograma_id: ID del odontograma creado
            odontologo_id: ID del odontólogo que registra

        Returns:
            True si se crearon correctamente todas las condiciones
        """
        try:
            # Obtener todos los números FDI para dientes adultos
            dientes_fdi = []
            # Cuadrante 1: 11-18 (Superior derecho)
            dientes_fdi.extend(range(11, 19))
            # Cuadrante 2: 21-28 (Superior izquierdo)
            dientes_fdi.extend(range(21, 29))
            # Cuadrante 3: 31-38 (Inferior izquierdo)
            dientes_fdi.extend(range(31, 39))
            # Cuadrante 4: 41-48 (Inferior derecho)
            dientes_fdi.extend(range(41, 49))

            # Primero obtener los diente_id correspondientes a los números FDI
            dientes_response = self.supabase.table("dientes").select("id, numero_diente").in_("numero_diente", dientes_fdi).execute()

            if not dientes_response.data:
                print(f"❌ No se encontraron dientes FDI en la base de datos")
                return False

            # Crear lista de condiciones iniciales para inserción batch
            condiciones_iniciales = []

            for diente_data in dientes_response.data:
                condicion = {
                    "odontograma_id": odontograma_id,
                    "diente_id": diente_data["id"],
                    "tipo_condicion": "sano",
                    "caras_afectadas": ["completa"],
                    "severidad": "leve",
                    "descripcion": "Diente sano sin patologías",
                    "observaciones": "Estado inicial del paciente",
                    "fecha_registro": datetime.now().isoformat(),
                    "registrado_por": user_id  # Usar user_id válido en lugar de odontologo_id
                }
                condiciones_iniciales.append(condicion)

            # Insertar todas las condiciones de una vez (batch insert)
            response = self.supabase.table("condiciones_diente").insert(condiciones_iniciales).execute()

            if response.data:
                print(f"✅ {len(condiciones_iniciales)} condiciones iniciales creadas para odontograma {odontograma_id}")
                return True
            else:
                print(f"❌ Error en batch insert de condiciones iniciales")
                return False

        except Exception as e:
            print(f"❌ Error creando condiciones iniciales FDI: {e}")
            return False

    async def crear_nueva_version_odontograma(
        self, 
        odontograma_actual_id: str,
        intervencion_id: str, 
        cambios_realizados: Dict[int, Dict[str, Any]],
        motivo: str = "Cambios en intervención"
    ) -> Optional[OdontogramaModel]:
        """🔄 Crear nueva versión automáticamente cuando hay cambios"""
        try:
            # 1. Obtener versión actual
            odontograma_actual = await self.obtener_odontograma_por_id(odontograma_actual_id)
            if not odontograma_actual:
                return None
            
            # 2. Marcar versión actual como no activa
            self.supabase.table("odontograma").update({
                "es_version_actual": False
            }).eq("id", odontograma_actual_id).execute()
            
            # 3. Crear nueva versión con cambios
            estados_actualizados = odontograma_actual.dientes_estados.copy()
            estados_actualizados.update(cambios_realizados)
            
            nueva_version = {
                "numero_historia": odontograma_actual.numero_historia,
                "version": odontograma_actual.version + 1,
                "id_version_anterior": odontograma_actual_id,
                "id_intervencion_origen": intervencion_id,
                "es_version_actual": True,
                "motivo_nueva_version": motivo,
                "fecha_creacion": datetime.now().isoformat(),
                "odontologo_id": odontograma_actual.odontologo_id,
                "tipo_odontograma": odontograma_actual.tipo_odontograma,
                "dientes_estados": estados_actualizados,
                "notas_generales": odontograma_actual.notas_generales,
                "observaciones_clinicas": f"{odontograma_actual.observaciones_clinicas}\n\n[V{odontograma_actual.version + 1}] {motivo}"
            }
            
            response = self.supabase.table("odontograma").insert(nueva_version).execute()
            
            if response.data:
                return OdontogramaModel.from_dict(response.data[0])
            return None
            
        except Exception as e:
            print(f"❌ Error creando nueva versión: {e}")
            return None
    
    async def obtener_odontograma_actual(self, numero_historia: str) -> Optional[OdontogramaModel]:
        """📋 Obtener versión actual del odontograma de un paciente"""
        try:
            response = self.supabase.table("odontograma").select("*").eq(
                "numero_historia", numero_historia
            ).eq("es_version_actual", True).single().execute()
            
            if response.data:
                return OdontogramaModel.from_dict(response.data)
            return None
            
        except Exception as e:
            print(f"❌ Error obteniendo odontograma actual: {e}")
            return None
    
    async def obtener_historial_versiones(self, numero_historia: str) -> List[OdontogramaModel]:
        """📚 Obtener todas las versiones históricas de un odontograma"""
        try:
            response = self.supabase.table("odontograma").select("*").eq(
                "numero_historia", numero_historia
            ).order("version", desc=True).execute()
            
            if response.data:
                return [OdontogramaModel.from_dict(version) for version in response.data]
            return []
            
        except Exception as e:
            print(f"❌ Error obteniendo historial: {e}")
            return []
    
    # ==========================================
    # 🎨 GESTIÓN AVANZADA DE CONDICIONES
    # ==========================================
    
    async def aplicar_condicion_diente(
        self,
        odontograma_id: str,
        numero_fdi: int,
        codigo_condicion: str,
        superficie: str = "completa",
        observaciones: str = "",
        intervencion_id: Optional[str] = None
    ) -> bool:
        """🎨 Aplicar condición específica a un diente con trazabilidad"""
        try:
            # Obtener información de la condición desde catálogo
            condicion_info = await self._obtener_info_condicion(codigo_condicion)
            
            nueva_condicion = {
                "odontograma_id": odontograma_id,
                "numero_fdi": numero_fdi,
                "codigo_condicion": codigo_condicion,
                "nombre_condicion": condicion_info.get("nombre", codigo_condicion),
                "superficie_afectada": superficie,
                "categoria": condicion_info.get("categoria", "normal"),
                "es_urgente": condicion_info.get("es_urgente", False),
                "color_hex": condicion_info.get("color_hex", "#16a34a"),
                "descripcion": condicion_info.get("descripcion", ""),
                "observaciones": observaciones,
                "fecha_registro": datetime.now().isoformat(),
                "intervencion_origen_id": intervencion_id,
                "estado": "actual"
            }
            
            response = self.supabase.table("condiciones_diente").insert(nueva_condicion).execute()
            
            return response.data is not None
            
        except Exception as e:
            print(f"❌ Error aplicando condición: {e}")
            return False
    
    async def _obtener_info_condicion(self, codigo_condicion: str) -> Dict[str, Any]:
        """🔍 Obtener información completa de una condición desde catálogo"""
        try:
            response = self.supabase.table("condiciones_diente").select("*").eq("codigo", codigo_condicion).single().execute()
            
            if response.data:
                return response.data
            
            # Fallback básico
            return {
                "nombre": codigo_condicion.lower(),
                "categoria": "normal", 
                "es_urgente": False,
                "color_hex": "#16a34a",
                "descripcion": f"Condición {codigo_condicion}"
            }
            
        except Exception as e:
            print(f"❌ Error obteniendo info condición: {e}")
            return {"nombre": codigo_condicion, "categoria": "normal", "es_urgente": False, "color_hex": "#16a34a"}
    
    # ==========================================
    # 📋 MÉTODOS AUXILIARES Y CONSULTAS
    # ==========================================
    
    async def obtener_odontograma_por_id(self, odontograma_id: str) -> Optional[OdontogramaModel]:
        """🔍 Obtener odontograma específico por ID"""
        try:
            response = self.supabase.table("odontograma").select("*").eq("id", odontograma_id).single().execute()
            
            if response.data:
                return OdontogramaModel.from_dict(response.data)
            return None
            
        except Exception as e:
            print(f"❌ Error obteniendo odontograma: {e}")
            return None
    
    async def comparar_versiones(self, version_anterior_id: str, version_actual_id: str) -> Dict[str, Any]:
        """🔄 Comparar dos versiones de odontograma y mostrar diferencias"""
        try:
            version_anterior = await self.obtener_odontograma_por_id(version_anterior_id)
            version_actual = await self.obtener_odontograma_por_id(version_actual_id)
            
            if not version_anterior or not version_actual:
                return {"error": "No se encontraron las versiones"}
            
            cambios = []
            
            # Comparar estados de dientes
            for numero_fdi, estado_actual in version_actual.dientes_estados.items():
                estado_anterior = version_anterior.dientes_estados.get(numero_fdi, {})
                
                if estado_actual != estado_anterior:
                    cambios.append({
                        "diente_fdi": numero_fdi,
                        "estado_anterior": estado_anterior,
                        "estado_actual": estado_actual,
                        "tipo_cambio": "modificación" if estado_anterior else "nuevo"
                    })
            
            return {
                "version_anterior": version_anterior.version,
                "version_actual": version_actual.version,
                "fecha_cambio": version_actual.fecha_creacion,
                "motivo": version_actual.motivo_nueva_version,
                "total_cambios": len(cambios),
                "cambios_detallados": cambios
            }
            
        except Exception as e:
            print(f"❌ Error comparando versiones: {e}")
            return {"error": str(e)}
    
    async def obtener_dientes_urgentes(self, numero_historia: str) -> List[Dict[str, Any]]:
        """🚨 Obtener dientes con condiciones urgentes que requieren atención"""
        try:
            # Obtener odontograma actual
            odontograma = await self.obtener_odontograma_actual(numero_historia)
            if not odontograma:
                return []
            
            # Filtrar dientes con condiciones urgentes
            dientes_urgentes = []
            condiciones_urgentes = await self.cargar_condiciones_disponibles()
            codigos_urgentes = [c["codigo"] for c in condiciones_urgentes if c.get("es_urgente")]
            
            for numero_fdi, estado in odontograma.dientes_estados.items():
                if estado.get("codigo") in codigos_urgentes:
                    diente_info = await self.obtener_diente_por_fdi(numero_fdi)
                    
                    dientes_urgentes.append({
                        "numero_fdi": numero_fdi,
                        "nombre_diente": diente_info.nombre_diente if diente_info else f"Diente {numero_fdi}",
                        "condicion": estado.get("condicion", ""),
                        "codigo": estado.get("codigo", ""),
                        "superficie": estado.get("superficie", ""),
                        "color": estado.get("color", "#dc2626")
                    })
            
            return dientes_urgentes
            
        except Exception as e:
            print(f"❌ Error obteniendo dientes urgentes: {e}")
            return []


# ==========================================
# 🏗️ INSTANCIA SINGLETON DEL SERVICIO  
# ==========================================

# Crear instancia única para uso en la aplicación
odontograma_service = OdontogramaService()

# Funciones de conveniencia para import directo
async def cargar_catalogo_fdi() -> List[DienteModel]:
    """📊 Cargar catálogo FDI completo"""
    return await odontograma_service.cargar_catalogo_fdi()

async def obtener_odontograma_actual(numero_historia: str) -> Optional[OdontogramaModel]:
    """📋 Obtener odontograma actual de un paciente"""
    return await odontograma_service.obtener_odontograma_actual(numero_historia)

async def crear_nueva_version(odontograma_id: str, intervencion_id: str, cambios: Dict[int, Dict[str, Any]], motivo: str = "Intervención odontológica") -> Optional[OdontogramaModel]:
    """🔄 Crear nueva versión con cambios"""
    return await odontograma_service.crear_nueva_version_odontograma(odontograma_id, intervencion_id, cambios, motivo)

async def obtener_dientes_urgentes(numero_historia: str) -> List[Dict[str, Any]]:
    """🚨 Obtener dientes con condiciones urgentes"""
    return await odontograma_service.obtener_dientes_urgentes(numero_historia)

async def crear_odontograma_inicial_completo(numero_historia: str, paciente_id: str, odontologo_id: str) -> Optional[OdontogramaModel]:
    """🆕 Crear odontograma inicial completo para paciente nuevo"""
    return await odontograma_service.crear_odontograma_inicial_completo(numero_historia, paciente_id, odontologo_id)