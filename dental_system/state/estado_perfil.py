"""
Estado para gestión de perfil de usuario
"""
import reflex as rx
from typing import Dict, Any
import re
from ..services.perfil_service import perfil_service
from ..supabase.auth import auth
import logging

logger = logging.getLogger(__name__)


class EstadoPerfil(rx.State, mixin=True):
    """
    Estado para gestión de perfil de usuario propio
    Permite actualizar celular, dirección, cambiar password y email
    """

    # ========================================
    # DATOS DEL PERFIL
    # ========================================

    # Formulario principal (datos completos del perfil)
    formulario_perfil: Dict[str, Any] = {}
    datos_originales: Dict[str, Any] = {}

    # ========================================
    # UI STATES
    # ========================================

    cargando_perfil: bool = False
    guardando_cambios: bool = False
    errores_validacion: Dict[str, str] = {}

    # ========================================
    # MODALES
    # ========================================

    modal_cambio_password_abierto: bool = False
    modal_cambio_email_abierto: bool = False
    cambiando_password: bool = False
    cambiando_email: bool = False

    # ========================================
    # FORMULARIOS DE MODALES
    # ========================================

    # Cambio de contraseña
    current_password: str = ""
    new_password: str = ""
    confirm_password: str = ""
    errores_password: Dict[str, str] = {}

    # Cambio de email
    new_email: str = ""
    password_for_email: str = ""
    errores_email: Dict[str, str] = {}

    # ========================================
    # COMPUTED VARS
    # ========================================

    @rx.var
    def tiene_cambios_pendientes(self) -> bool:
        """Detecta si hay cambios sin guardar en celular o dirección"""
        if not self.datos_originales:
            return False

        celular_cambio = self.formulario_perfil.get("celular", "") != self.datos_originales.get("celular", "")
        direccion_cambio = self.formulario_perfil.get("direccion", "") != self.datos_originales.get("direccion", "")

        return celular_cambio or direccion_cambio

    @rx.var
    def tiene_registro_personal(self) -> bool:
        """Verifica si el usuario tiene registro en tabla personal"""
        return self.formulario_perfil.get("personal") is not None

    @rx.var
    def estado_laboral_str(self) -> str:
        """Retorna estado laboral en mayúsculas o vacío"""
        estado = self.formulario_perfil.get("estado_laboral", "")
        return estado.upper() if estado else ""

    @rx.var
    def estado_laboral_activo(self) -> bool:
        """Verifica si el estado laboral es activo"""
        return self.formulario_perfil.get("estado_laboral", "") == "activo"

    @rx.var
    def fecha_nacimiento_formateada(self) -> str:
        """Fecha de nacimiento en formato DD/MM/YYYY"""
        fecha = self.formulario_perfil.get("fecha_nacimiento", "")
        if not fecha:
            return "No especificada"

        try:
            from datetime import datetime
            fecha_obj = datetime.fromisoformat(str(fecha).split('T')[0])
            return fecha_obj.strftime("%d/%m/%Y")
        except:
            return str(fecha)

    @rx.var
    def fecha_contratacion_formateada(self) -> str:
        """Fecha de contratación en formato DD/MM/YYYY"""
        fecha = self.formulario_perfil.get("fecha_contratacion", "")
        if not fecha:
            return "No especificada"

        try:
            from datetime import datetime
            fecha_obj = datetime.fromisoformat(str(fecha).split('T')[0])
            return fecha_obj.strftime("%d/%m/%Y")
        except:
            return str(fecha)

    @rx.var
    def iniciales_usuario(self) -> str:
        """Obtiene las iniciales del nombre completo para el avatar"""
        nombre_completo = self.formulario_perfil.get("nombre_completo", "")
        if not nombre_completo:
            return "?"

        palabras = nombre_completo.split()
        if len(palabras) >= 2:
            return f"{palabras[0][0]}{palabras[1][0]}".upper()
        elif len(palabras) == 1:
            return palabras[0][0].upper()
        return "?"

    # ========================================
    # MÉTODOS PRINCIPALES
    # ========================================

    async def cargar_datos_perfil(self):
        """Carga datos completos del perfil del usuario actual"""
        self.cargando_perfil = True

        try:
            # Obtener perfil completo
            user_id = self.id_usuario  # type: ignore # Viene de EstadoAuth
            if not user_id:
                logger.error("❌ No hay usuario autenticado")
                return

            perfil = await perfil_service.get_own_profile_complete(user_id)

            if perfil:
                self.formulario_perfil = perfil
                self.datos_originales = {
                    "celular": perfil.get("celular", ""),
                    "direccion": perfil.get("direccion", ""),
                }
                logger.info(f"✅ Perfil cargado: {perfil.get('nombre_completo')}")
            else:
                logger.error("❌ No se pudo cargar el perfil")
                self.mostrar_toast_error("Error al cargar perfil")  # type: ignore # Viene de EstadoUI

        except Exception as e:
            logger.error(f"❌ Error cargando perfil: {str(e)}")
            self.mostrar_toast_error(f"Error: {str(e)}")  # type: ignore

        finally:
            self.cargando_perfil = False

    def actualizar_campo_perfil(self, field: str, value: Any):
        """Actualiza un campo del formulario de perfil"""
        self.formulario_perfil[field] = value

        # Limpiar error de ese campo si existe
        if field in self.errores_validacion:
            self.errores_validacion.pop(field)

    async def guardar_cambios_perfil(self):
        """Guarda cambios de celular y dirección"""
        self.guardando_cambios = True

        try:
            # 1. Validar formulario
            if not self.validar_formulario_perfil():
                self.mostrar_toast_error("Corrige los errores del formulario")  # type: ignore
                return

            # 2. Guardar cambios
            user_id = self.id_usuario  # type: ignore
            celular = self.formulario_perfil.get("celular", "")
            direccion = self.formulario_perfil.get("direccion", "")

            exito, mensaje = await perfil_service.update_own_contact_info(
                user_id=user_id,
                celular=celular,
                direccion=direccion
            )

            if exito:
                self.mostrar_toast_exito(mensaje)  # type: ignore
                # Actualizar datos originales
                self.datos_originales = {
                    "celular": celular,
                    "direccion": direccion,
                }
                # Recargar perfil
                await self.cargar_datos_perfil()
            else:
                self.mostrar_toast_error(mensaje)  # type: ignore

        except Exception as e:
            logger.error(f"❌ Error guardando cambios: {str(e)}")
            self.mostrar_toast_error(f"Error: {str(e)}")  # type: ignore

        finally:
            self.guardando_cambios = False

    def cancelar_edicion(self):
        """Restaura valores originales"""
        if self.datos_originales:
            self.formulario_perfil["celular"] = self.datos_originales.get("celular", "")
            self.formulario_perfil["direccion"] = self.datos_originales.get("direccion", "")
        self.errores_validacion = {}
        self.mostrar_toast_info("Cambios descartados")  # type: ignore

    # ========================================
    # MODAL CAMBIO DE CONTRASEÑA
    # ========================================

    def abrir_modal_cambio_password(self):
        """Abre modal de cambio de contraseña"""
        self.modal_cambio_password_abierto = True
        self.limpiar_formulario_password()

    def cerrar_modal_cambio_password(self):
        """Cierra modal y limpia campos"""
        self.modal_cambio_password_abierto = False
        self.limpiar_formulario_password()

    def limpiar_formulario_password(self):
        """Limpia formulario de contraseña"""
        self.current_password = ""
        self.new_password = ""
        self.confirm_password = ""
        self.errores_password = {}

    async def confirmar_cambio_password(self):
        """Valida y cambia contraseña"""
        self.cambiando_password = True

        try:
            # 1. Validar formulario
            if not self.validar_cambio_password():
                return

            # 2. Cambiar contraseña
            user_email = self.email_usuario  # type: ignore # Viene de EstadoAuth

            exito, mensaje = await auth.update_user_password(
                current_password=self.current_password,
                new_password=self.new_password,
                user_email=user_email
            )

            if exito:
                self.mostrar_toast_exito(mensaje)  # type: ignore
                self.cerrar_modal_cambio_password()
            else:
                self.mostrar_toast_error(mensaje)  # type: ignore

        except Exception as e:
            logger.error(f"❌ Error cambiando contraseña: {str(e)}")
            self.mostrar_toast_error(f"Error: {str(e)}")  # type: ignore

        finally:
            self.cambiando_password = False

    # ========================================
    # MODAL CAMBIO DE EMAIL
    # ========================================

    def abrir_modal_cambio_email(self):
        """Abre modal de cambio de email"""
        self.modal_cambio_email_abierto = True
        self.limpiar_formulario_email()

    def cerrar_modal_cambio_email(self):
        """Cierra modal y limpia campos"""
        self.modal_cambio_email_abierto = False
        self.limpiar_formulario_email()

    def limpiar_formulario_email(self):
        """Limpia formulario de email"""
        self.new_email = ""
        self.password_for_email = ""
        self.errores_email = {}

    async def confirmar_cambio_email(self):
        """Valida y cambia email"""
        self.cambiando_email = True

        try:
            # 1. Validar formulario
            if not self.validar_cambio_email():
                return

            # 2. Cambiar email
            user_id = self.id_usuario  # type: ignore
            current_email = self.email_usuario  # type: ignore

            exito, mensaje = await auth.update_user_email(
                new_email=self.new_email,
                current_password=self.password_for_email,
                user_id=user_id,
                current_email=current_email
            )

            if exito:
                self.mostrar_toast_exito(mensaje)  # type: ignore
                self.cerrar_modal_cambio_email()
                # Actualizar email en formulario
                self.formulario_perfil["email"] = self.new_email
                # Nota: El usuario deberá verificar el nuevo email
            else:
                self.mostrar_toast_error(mensaje)  # type: ignore

        except Exception as e:
            logger.error(f"❌ Error cambiando email: {str(e)}")
            self.mostrar_toast_error(f"Error: {str(e)}")  # type: ignore

        finally:
            self.cambiando_email = False

    # ========================================
    # VALIDACIONES
    # ========================================

    def validar_formulario_perfil(self) -> bool:
        """Valida formulario principal (celular y dirección)"""
        celular = self.formulario_perfil.get("celular", "")
        direccion = self.formulario_perfil.get("direccion", "")

        es_valido, errores = perfil_service.validate_contact_info(celular, direccion)
        self.errores_validacion = errores

        return es_valido

    def validar_cambio_password(self) -> bool:
        """Valida formulario de cambio de contraseña"""
        errores = {}

        # Contraseña actual no vacía
        if not self.current_password:
            errores["current_password"] = "Ingresa tu contraseña actual"

        # Nueva contraseña mínimo 6 caracteres
        if len(self.new_password) < 6:
            errores["new_password"] = "La contraseña debe tener al menos 6 caracteres"

        # Confirmar coincide
        if self.new_password != self.confirm_password:
            errores["confirm_password"] = "Las contraseñas no coinciden"

        # No puede ser igual a la actual
        if self.new_password and self.current_password and self.new_password == self.current_password:
            errores["new_password"] = "La nueva contraseña debe ser diferente a la actual"

        self.errores_password = errores
        return len(errores) == 0

    def validar_cambio_email(self) -> bool:
        """Valida formulario de cambio de email"""
        errores = {}

        # Email válido (regex del esquema)
        if not self.new_email:
            errores["new_email"] = "Ingresa un email"
        elif not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', self.new_email):
            errores["new_email"] = "Email inválido"

        # No puede ser el mismo email actual
        if self.new_email and self.new_email == self.email_usuario:  # type: ignore
            errores["new_email"] = "El nuevo email debe ser diferente al actual"

        # Password no vacío
        if not self.password_for_email:
            errores["password"] = "Ingresa tu contraseña para confirmar"

        self.errores_email = errores
        return len(errores) == 0



    @rx.var
    def fecha_nacimiento_formateada(self) -> str:
        """Fecha de nacimiento en formato DD/MM/YYYY"""
        fecha = self.formulario_perfil.get("fecha_nacimiento", "")
        if not fecha:
            return "No especificada"
        try:
            from datetime import datetime
            fecha_obj = datetime.fromisoformat(str(fecha).split('T')[0])
            return fecha_obj.strftime("%d/%m/%Y")
        except:
            return str(fecha)

 

    @rx.var

    def fecha_contratacion_formateada(self) -> str:

        """Fecha de contratación en formato DD/MM/YYYY"""

        fecha = self.formulario_perfil.get("fecha_contratacion", "")

        if not fecha:

            return "No especificada"

 

        try:

            from datetime import datetime

            fecha_obj = datetime.fromisoformat(str(fecha).split('T')[0])

            return fecha_obj.strftime("%d/%m/%Y")

        except:

            return str(fecha)

 

    @rx.var
    def iniciales_usuario(self) -> str:
        """Obtiene las iniciales del nombre completo para el avatar"""
        nombre_completo = self.formulario_perfil.get("nombre_completo", "")
        if not nombre_completo:
            return "?"
        palabras = nombre_completo.split()
        if len(palabras) >= 2:
            return f"{palabras[0][0]}{palabras[1][0]}".upper()
        elif len(palabras) == 1:
            return palabras[0][0].upper()
        return "?"
