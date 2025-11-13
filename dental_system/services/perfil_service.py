"""
Servicio para gestión de perfil de usuario propio
Permite a cualquier usuario actualizar SU PROPIO perfil sin restricciones de rol
"""
import re
from typing import Dict, Optional, Tuple, Any
from ..supabase.client import handle_supabase_error
from .base_service import BaseService
import logging

logger = logging.getLogger(__name__)


class PerfilService(BaseService):
    """
    Servicio especializado para gestión de perfil propio
    Cualquier usuario puede actualizar su propia información de contacto
    """

    def __init__(self):
        super().__init__()

    @handle_supabase_error
    async def get_own_profile_complete(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene perfil completo del usuario combinando datos de usuario y personal

        Args:
            user_id: ID del usuario

        Returns:
            Dict con todos los datos del perfil o None
        """
        try:
            logger.info(f"📋 Obteniendo perfil completo para usuario: {user_id}")

            # 1. Obtener datos de usuario con rol
            user_response = self.client.table("usuario").select(
                "id, email, rol_id, activo, fecha_creacion"
            ).eq("id", user_id).execute()

            if not user_response.data:
                logger.error(f"❌ Usuario {user_id} no encontrado")
                return None

            user_data = user_response.data[0]

            # 2. Obtener rol
            rol_response = self.client.table("rol").select("nombre, descripcion").eq(
                "id", user_data["rol_id"]
            ).execute()

            if rol_response.data:
                user_data["rol"] = rol_response.data[0]
            else:
                user_data["rol"] = {"nombre": "sin_rol", "descripcion": "Sin rol"}

            # 3. Obtener datos de personal (si existe)
            personal_response = self.client.table("personal").select("*").eq(
                "usuario_id", user_id
            ).execute()

            if personal_response.data:
                personal_data = personal_response.data[0]

                # Construir nombre completo
                nombres = []
                if personal_data.get("primer_nombre"):
                    nombres.append(personal_data["primer_nombre"])
                if personal_data.get("segundo_nombre"):
                    nombres.append(personal_data["segundo_nombre"])
                if personal_data.get("primer_apellido"):
                    nombres.append(personal_data["primer_apellido"])
                if personal_data.get("segundo_apellido"):
                    nombres.append(personal_data["segundo_apellido"])

                nombre_completo = " ".join(nombres) if nombres else "Usuario"

                # Combinar datos
                perfil_completo = {
                    **user_data,
                    "personal": personal_data,
                    "nombre_completo": nombre_completo,
                    "celular": personal_data.get("celular", ""),
                    "direccion": personal_data.get("direccion", ""),
                    "tipo_personal": personal_data.get("tipo_personal", ""),
                    "especialidad": personal_data.get("especialidad", ""),
                    "numero_licencia": personal_data.get("numero_licencia", ""),
                    "estado_laboral": personal_data.get("estado_laboral", ""),
                    "fecha_contratacion": str(personal_data.get("fecha_contratacion", "")) if personal_data.get("fecha_contratacion") else "",
                    "tipo_documento": personal_data.get("tipo_documento", ""),
                    "numero_documento": personal_data.get("numero_documento", ""),
                    "fecha_nacimiento": str(personal_data.get("fecha_nacimiento", "")) if personal_data.get("fecha_nacimiento") else "",
                }
            else:
                # Usuario sin registro en personal
                perfil_completo = {
                    **user_data,
                    "personal": None,
                    "nombre_completo": user_data.get("email", "Usuario").split("@")[0],
                    "celular": "",
                    "direccion": "",
                    "tipo_personal": "",
                    "especialidad": "",
                    "numero_licencia": "",
                    "estado_laboral": "",
                    "fecha_contratacion": "",
                    "tipo_documento": "",
                    "numero_documento": "",
                    "fecha_nacimiento": "",
                }

            logger.info(f"✅ Perfil completo obtenido: {perfil_completo.get('nombre_completo')}")
            return perfil_completo

        except Exception as e:
            logger.error(f"❌ Error obteniendo perfil completo: {str(e)}")
            return None

    @handle_supabase_error
    async def update_own_contact_info(
        self,
        user_id: str,
        celular: str,
        direccion: str
    ) -> Tuple[bool, str]:
        """
        Actualiza información de contacto del usuario (celular y dirección)

        Args:
            user_id: ID del usuario
            celular: Nuevo celular
            direccion: Nueva dirección

        Returns:
            Tupla (éxito, mensaje)
        """
        try:
            logger.info(f"📝 Actualizando info de contacto para usuario: {user_id}")

            # 1. Validar datos
            es_valido, errores = self.validate_contact_info(celular, direccion)
            if not es_valido:
                return False, "; ".join(errores.values())

            # 2. Buscar registro en personal
            personal_response = self.client.table("personal").select("id").eq(
                "usuario_id", user_id
            ).execute()

            if not personal_response.data:
                return False, "No se encontró registro de personal para este usuario"

            personal_id = personal_response.data[0]["id"]

            # 3. Actualizar en tabla personal
            update_response = self.client.table("personal").update({
                "celular": celular,
                "direccion": direccion,
                "fecha_actualizacion": "now()"
            }).eq("id", personal_id).execute()

            if update_response.data:
                logger.info("✅ Información de contacto actualizada correctamente")
                return True, "Información de contacto actualizada correctamente"
            else:
                logger.error("❌ Error al actualizar información de contacto")
                return False, "Error al actualizar la información"

        except Exception as e:
            logger.error(f"❌ Error actualizando contacto: {str(e)}")
            return False, f"Error: {str(e)}"

    def validate_contact_info(
        self,
        celular: str,
        direccion: str
    ) -> Tuple[bool, Dict[str, str]]:
        """
        Valida información de contacto según esquema de BD

        Args:
            celular: Número de celular
            direccion: Dirección

        Returns:
            Tupla (es_válido, diccionario_de_errores)
        """
        errores = {}

        # Validar celular: regex del esquema '^[\+]?[\d\s\-\(\)]{7,20}$'
        if not celular or not celular.strip():
            errores["celular"] = "El celular es requerido"
        elif not re.match(r'^[\+]?[\d\s\-\(\)]{7,20}$', celular):
            errores["celular"] = "Formato de celular inválido (ej: +58 412 1234567)"

        # Validar dirección: no vacía, max 200 caracteres
        if not direccion or not direccion.strip():
            errores["direccion"] = "La dirección es requerida"
        elif len(direccion) > 200:
            errores["direccion"] = "La dirección no puede exceder 200 caracteres"

        es_valido = len(errores) == 0
        return es_valido, errores


# Instancia singleton
perfil_service = PerfilService()
