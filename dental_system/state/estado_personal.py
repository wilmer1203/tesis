"""
👨‍⚕️ ESTADO DE PERSONAL - SUBSTATE SEPARADO
============================================

PROPÓSITO: Manejo centralizado y especializado de gestión de personal
- CRUD completo de empleados (solo Gerente)
- Gestión de roles y especialidades
- Vinculación personal ↔ usuario automática
- Cache inteligente para performance
- Estadísticas y métricas de empleados

USADO POR: AppState como coordinador principal  
PATRÓN: Substate con get_estado_personal() en AppState
"""

import reflex as rx
from typing import Dict, List, Optional
import logging

# Servicios y modelos
from dental_system.services.personal_service import personal_service
from dental_system.models import PersonalModel, PersonalFormModel

logger = logging.getLogger(__name__)

class EstadoPersonal(rx.State, mixin=True):
    # ==========================================
    # 👨‍⚕️ VARIABLES PRINCIPALES DE PERSONAL
    # ==========================================

    # Lista principal de empleados (modelos tipados)
    lista_personal: List[PersonalModel] = []

    # Personal seleccionado para operaciones
    empleado_seleccionado: Optional[PersonalModel] = None
    accion_personal: bool = False  # True = activar, False = desactivar

    # Formulario de empleado (datos temporales) - MODELO TIPADO
    formulario_empleado: PersonalFormModel = PersonalFormModel()
    errores_validacion_empleado: Dict[str, str] = {}

    # ==========================================
    # 👨‍⚕️ FILTROS
    # ==========================================

    filtro_rol: str = "todos"  # todos, Gerente, Administrador, Odontólogo, Asistente
    filtro_estado_empleado: str = "activos"  # todos, activos, inactivos
    termino_busqueda_personal: str = ""

    # ==========================================
    # 👨‍⚕️ ESTADOS DE CARGA
    # ==========================================
    cargando_operacion_personal: bool = False
    modal_crear_personal_abierto: bool = False
    modal_editar_personal_abierto: bool = False
    # ==========================================
    # 💡 COMPUTED VARS OPTIMIZADAS CON CACHE
    # ==========================================

    @rx.var(cache=True)
    def personal_filtrado(self) -> List[PersonalModel]:
        """
        Lista de personal filtrada con cache
        Aplica búsqueda por nombre, documento, celular
        """
        if not self.lista_personal:
            return []

        try:
            resultado = self.lista_personal.copy()

            # Aplicar búsqueda si hay término (mínimo 2 caracteres)
            if self.termino_busqueda_personal and len(self.termino_busqueda_personal) >= 2:
                termino_lower = self.termino_busqueda_personal.lower()
                resultado = [
                    emp for emp in resultado
                    if (termino_lower in emp.nombre_completo.lower() or
                        termino_lower in emp.numero_documento.lower() or
                        termino_lower in emp.celular.lower() or
                        (emp.especialidad and termino_lower in emp.especialidad.lower()))
                ]

            # Nota: Filtros por rol y estado ya aplicados en backend via service

            return resultado

        except Exception as e:  
            return []

    @rx.var(cache=True)
    def odontologos_disponibles(self) -> List[PersonalModel]:
        """Lista de odontólogos activos disponibles"""
        try:
            return [
                emp for emp in self.lista_personal
                if emp.rol_nombre_computed == "odontologo" and emp.estado_laboral == "activo"
            ]
        except Exception:
            return []

    @rx.var(cache=True)
    def total_personal(self) -> int:
        """Total de empleados en el sistema"""
        return len(self.lista_personal)

    @rx.var(cache=True)
    def total_odontologos(self) -> int:
        """Total de odontólogos (activos e inactivos)"""
        try:
            return len([
                emp for emp in self.lista_personal
                if emp.tipo_personal == "Odontólogo"
            ])
        except Exception:
            return 0

    @rx.var(cache=True)
    def total_administrativos(self) -> int:
        """Total de personal administrativo (Gerente, Administrador, Asistente)"""
        try:
            return len([
                emp for emp in self.lista_personal
                if emp.tipo_personal in ["Gerente", "Administrador", "Asistente"]
            ])
        except Exception:
            return 0

    # ==========================================
    # 🔄 MÉTODOS DE CARGA DE DATOS
    # ==========================================
    
    async def cargar_lista_personal(self):
        """
        Carga la lista de personal desde el servicio
        Validando permisos de usuario (solo Gerente)
        """
        self.cargando_operacion_personal = True
        
        try:
            # Establecer contexto de usuario en el servicio (disponible directamente por mixin)
            personal_service.set_user_context(user_id=self.id_usuario, user_profile=self.perfil_usuario)
            
            # Obtener personal con filtros actuales
            personal_data = await personal_service.get_filtered_personal(
                search=self.termino_busqueda_personal if len(self.termino_busqueda_personal) >= 2 else None,
                tipo_personal=self.filtro_rol if self.filtro_rol != "todos" else None,
                activos_only=self.filtro_estado_empleado == "activos"
            )
            
            # Convertir a modelos tipados
            self.lista_personal = personal_data
            print(f"✅ Lista personal cargada: {len(personal_data)} empleados")
            
        except PermissionError as e:
            logger.warning(f"Error de permisos al cargar personal: {e}")
            # Mostrar toast de error (ya disponible por mixin)
            if hasattr(self, 'mostrar_toast_error'):
                self.mostrar_toast_error("Sin permisos para acceder al personal")
            
        except Exception as e:
            logger.error(f"❌ Error cargando lista personal: {e}")

        finally:
            self.cargando_operacion_personal = False

    # ==========================================
    # 🔍 MÉTODOS DE BÚSQUEDA Y FILTROS
    # ==========================================
    
    @rx.event
    async def buscar_personal(self, termino: str):
        """
        Búsqueda de personal
        Solo busca si hay al menos 2 caracteres
        """
        self.termino_busqueda_personal = termino.strip()

        # Solo recargar si hay término válido o si se está limpiando
        if len(termino.strip()) >= 2 or termino.strip() == "":
            await self.cargar_lista_personal()
    
    async def filtrar_por_rol(self, rol: str):
        """Filtrar personal por rol"""
        self.filtro_rol = rol
        await self.cargar_lista_personal()

    async def filtrar_por_estado(self, estado: str):
        """Filtrar personal por estado (activo/inactivo)"""
        self.filtro_estado_empleado = estado
        await self.cargar_lista_personal()
    
    # ==========================================
    # ➕ MÉTODOS CRUD DE PERSONAL
    # ==========================================

    async def crear_personal(self):
        """
        Crear nuevo empleado con validaciones
        """

        # Validar formulario
        if not self.validar_formulario_empleado():
            return
        
        self.cargando_operacion_personal = True
        
        try:
            # Establecer contexto de usuario en el servicio
            personal_service.set_user_context(user_id=self.id_usuario,user_profile=self.perfil_usuario)            
            # Crear empleado
            nuevo_empleado = await personal_service.create_staff_member(self.formulario_empleado)
            # Limpiar formulario
            self.limpiar_formulario_empleado()
            logger.info(f"✅ Empleado creado: {nuevo_empleado.nombre_completo}")
            
        except Exception as e:
            logger.error(f"❌ Error creando empleado: {e}")
            if hasattr(self, 'mostrar_toast_error'):
                self.mostrar_toast_error("Error al crear empleado")
            
        finally:
            self.cargando_operacion_personal = False
    
    async def actualizar_personal(self):
        """Actualizar empleado existente"""

        if not self.validar_formulario_empleado():
            return
        
        # Métodos disponibles directamente por mixin
        self.cargando_operacion_personal = True
        
        try:
            # Establecer contexto de usuario en el servicio
            personal_service.set_user_context(user_id=self.id_usuario,user_profile=self.perfil_usuario)
            
            # Actualizar empleado
            empleado_actualizado = await personal_service.update_staff_member(personal_id=self.empleado_seleccionado.id,personal_form=self.formulario_empleado,)
            # Actualizar seleccionado
            self.empleado_seleccionado = empleado_actualizado

        except Exception as e:
            logger.error(f"❌ Error actualizando empleado: {e}")
            if hasattr(self, 'mostrar_toast_error'):
                self.mostrar_toast_error("Error al actualizar empleado")
            
        finally:
            self.cargando_operacion_personal = False
    
    @rx.event
    async def guardar_personal_formulario(self):
        """
        💾 GUARDAR PERSONAL - CREAR O ACTUALIZAR AUTOMÁTICAMENTE

        Decide automáticamente si crear nuevo empleado o actualizar existente
        basándose en si hay un empleado seleccionado
        """
        try:
            # ✅ DECISIÓN AUTOMÁTICA: Crear o Actualizar
            if self.empleado_seleccionado and getattr(self.empleado_seleccionado, 'id', None):
                # MODO EDITAR: Actualizar empleado existente
                print(f"✏️ Modo EDITAR - Actualizando empleado {self.empleado_seleccionado.id}")
                await self.actualizar_personal()
            else:
                # MODO CREAR: Crear nuevo empleado
                print("➕ Modo CREAR - Creando nuevo empleado")
                await self.crear_personal()

            await self.cargar_lista_personal()  # Recargar lista para reflejar cambios
        except Exception as e:
            logger.error(f"❌ Error guardando personal: {e}")
            if hasattr(self, 'mostrar_toast_error'):
                self.mostrar_toast_error("Error al guardar empleado")

    async def activar_desactivar_personal(self, personal_id: str, activar: bool):
        """
        🔄 Preparar activación o desactivación de empleado

        Args:
            personal_id: ID del empleado
            activar: True para activar, False para desactivar
        """
        try:
            # Buscar el empleado en la lista
            empleado_encontrado = None
            for empleado in self.lista_personal:
                if empleado.id == personal_id:
                    empleado_encontrado = empleado
                    break

            if empleado_encontrado:
                # Establecer el empleado a modificar y la acción
                self.empleado_seleccionado = empleado_encontrado
                self.accion_personal = activar

                nombre_completo = f"{empleado_encontrado.primer_nombre} {empleado_encontrado.primer_apellido}"

                # Mostrar modal apropiado según la acción
                if activar:
                    # Modal de reactivación
                    await self.abrir_modal_confirmacion(
                        "Confirmar Reactivación",
                        f"¿Estás seguro de que deseas reactivar a {nombre_completo}? El empleado podrá volver a iniciar sesión en el sistema.",
                        "activar_personal"
                    )
                else:
                    # Modal de inhabilitación
                    await self.abrir_modal_confirmacion(
                        "Confirmar Inhabilitación",
                        f"¿Estás seguro de que deseas inhabilitar a {nombre_completo}? Esta acción impedirá que el empleado inicie sesión en el sistema.",
                        "desactivar_personal"
                    )

                logger.info(f"❓ Confirmación {'activar' if activar else 'desactivar'} personal: {personal_id}")
            else:
                logger.warning(f"⚠️ Empleado {personal_id} no encontrado")

        except Exception as e:
            logger.error(f"❌ Error preparando acción de empleado: {e}")
            if hasattr(self, 'mostrar_toast_error'):
                self.mostrar_toast_error("Error al preparar la acción")
    
    # ==========================================
    # 📝 GESTIÓN DE FORMULARIOS
    # ==========================================
    
    def cargar_empleado_en_formulario(self, empleado: PersonalModel):
        """Cargar datos de empleado en el formulario para edición"""
        self.empleado_seleccionado = empleado
        
        # ✅ MAPEAR MODELO A FORMULARIO TIPADO
        empleado_dict = {
            # Nombres completos
            "primer_nombre": empleado.primer_nombre or "",
            "segundo_nombre": empleado.segundo_nombre or "",
            "primer_apellido": empleado.primer_apellido or "",
            "segundo_apellido": empleado.segundo_apellido or "",
            
            # Identificación y contacto
            "numero_documento": empleado.numero_documento or "",
            "celular": empleado.celular or "",            # Solo celular
            "email": empleado.usuario.email or "",
            "direccion": empleado.direccion or "",
            
            # Información laboral
            "fecha_ingreso": empleado.fecha_contratacion or "",
            "comision_servicios": "0",  # Campo no disponible en PersonalModel
            "especialidad": empleado.especialidad or "",
            "numero_colegiatura": empleado.numero_licencia or "",
            
            # Tipo y rol
            "tipo_personal": empleado.tipo_personal or "asistente",
            "rol_id": empleado.rol_id or "",
            "estado_laboral": empleado.estado_laboral or "activo",
            
            # Información adicional
            "fecha_nacimiento": empleado.fecha_nacimiento or "",
            
            # ✅ CAMPOS CRÍTICOS PARA SISTEMA DE COLAS

            "tipo_documento": empleado.tipo_documento or "CI",
        }
        
        # ✅ CONVERTIR A MODELO TIPADO
        self.formulario_empleado = PersonalFormModel.from_dict(empleado_dict)
        
        # Limpiar errores
        self.errores_validacion_empleado = {}
    
    def limpiar_formulario_empleado(self):
        """Limpiar todos los datos del formulario"""
        self.formulario_empleado = PersonalFormModel()  # ✅ RESET CON MODELO TIPADO
        self.errores_validacion_empleado = {}
        self.empleado_seleccionado = None
        
    def actualizar_campo_formulario_empleado(self, campo: str, valor: str):
        """Actualizar campo específico del formulario tipado"""
        # ✅ ACTUALIZAR CAMPO EN MODELO TIPADO usando setattr
        if hasattr(self.formulario_empleado, campo):
            setattr(self.formulario_empleado, campo, valor)
        else:
            print(f"⚠️ Campo {campo} no existe en PersonalFormModel")
        
        # Limpiar error específico del campo
        if campo in self.errores_validacion_empleado:
            del self.errores_validacion_empleado[campo]
    
    def validar_formulario_empleado(self) -> bool:
        """
        Validar datos del formulario de empleado
        Returns True si es válido, False caso contrario
        """
        self.errores_validacion_empleado = {}
        
        # ✅ CAMPOS REQUERIDOS - SINCRONIZADO CON PERSONAL_SERVICE.PY
        campos_requeridos = [
            "primer_nombre", "primer_apellido", "numero_documento", "celular", "tipo_personal"
        ]

        # ✅ AGREGAR CONTRASEÑA PARA USUARIOS NUEVOS (igual que servicio)
        if not self.empleado_seleccionado:  # Solo para nuevos usuarios
            campos_requeridos.append("usuario_password")
        
        for campo in campos_requeridos:
            valor = getattr(self.formulario_empleado, campo, "")
            if isinstance(valor, str):
                valor = valor.strip()
            if not valor:
                self.errores_validacion_empleado[campo] = "Este campo es requerido"
        
        # ✅ VALIDACIONES ESPECÍFICAS CON MODELO TIPADO
        
        # Número de documento único
        numero_documento = self.formulario_empleado.numero_documento.strip() if self.formulario_empleado.numero_documento else ""
        if numero_documento and len(numero_documento) < 7:
            self.errores_validacion_empleado["numero_documento"] = "El número de documento debe tener al menos 7 dígitos"
        
        # Celular válido (requerido)
        celular = self.formulario_empleado.celular.strip() if self.formulario_empleado.celular else ""
        if celular and len(celular) < 10:
            self.errores_validacion_empleado["celular"] = "Celular debe tener al menos 10 dígitos"
        
        
        # ✅ CONTRASEÑA VÁLIDA (solo para usuarios nuevos)
        if not self.empleado_seleccionado:
            password = self.formulario_empleado.usuario_password.strip() if self.formulario_empleado.usuario_password else ""
            if password and len(password) < 6:
                self.errores_validacion_empleado["usuario_password"] = "La contraseña debe tener al menos 6 caracteres"


        return len(self.errores_validacion_empleado) == 0

    # ==========================================
    # 📱 FUNCIONES DE MODAL
    # ==========================================
    
    @rx.event
    async def seleccionar_empleado(self, personal_id: str):
        """🎯 Seleccionar empleado para operaciones"""
        try:
            # Buscar empleado en la lista local
            empleado_encontrado = None
            for empleado in self.lista_personal:
                if empleado.id == personal_id:
                    empleado_encontrado = empleado
                    break
            
            if empleado_encontrado:
                self.empleado_seleccionado = empleado_encontrado
                logger.info(f"🎯 Empleado seleccionado: {empleado_encontrado.nombre_completo}")
            else:
                logger.warning(f"⚠️ Empleado {personal_id} no encontrado en lista local")
                self.empleado_seleccionado = None
                
        except Exception as e:
            logger.error(f"❌ Error seleccionando empleado: {e}")
            self.empleado_seleccionado = None
    
    @rx.event
    async def seleccionar_y_abrir_modal_personal(self, personal_id: str = ""):
        """
        📱 Seleccionar empleado y abrir modal - Crear o Editar según ID
        
        Args:
            personal_id: Si está vacío → Crear, Si tiene valor → Editar
        """
        try:
            if personal_id:
                # Modo editar: seleccionar el personal primero
                await self.seleccionar_empleado(personal_id)
                # Cargar datos en el formulario
                if self.empleado_seleccionado:
                    self.cargar_empleado_en_formulario(self.empleado_seleccionado)
                # Abrir modal editar
                self.modal_editar_personal_abierto = True

            else:
                # Modo crear: limpiar selección y abrir modal
                self.empleado_seleccionado = None
                self.limpiar_formulario_empleado()  
                # Abrir modal crear
                self.modal_crear_personal_abierto = True 

        except Exception as e:
            logger.error(f"❌ Error abriendo modal personal: {e}")
    
    @rx.event
    async def ejecutar_accion_personal(self):
        """
        ✅ EJECUTAR ACCIÓN DE ACTIVAR/DESACTIVAR PERSONAL

        """
        if self.empleado_seleccionado and self.empleado_seleccionado.id:
            nombre_completo = f"{self.empleado_seleccionado.primer_nombre} {self.empleado_seleccionado.primer_apellido}"
            personal_id = self.empleado_seleccionado.id
            activar = self.accion_personal

            try:
                # Establecer contexto de usuario en el servicio
                personal_service.set_user_context(user_id=self.id_usuario,user_profile=self.perfil_usuario)

                # Ejecutar la acción apropiada
                if activar:
                    success = await personal_service.reactivate_staff_member(personal_id)
                    accion_texto = "reactivado"
                else:
                    success = await personal_service.deactivate_staff_member(personal_id)
                    accion_texto = "inhabilitado"

                if success:
                    # Actualizar en la lista local
                    for i, emp in enumerate(self.lista_personal):
                        if emp.id == personal_id:
                            self.lista_personal[i].estado_laboral = "activo" if activar else "inactivo"
                            break

                    # Recargar lista para reflejar cambios
                    await self.cargar_lista_personal()

                    # Mostrar éxito
                    if hasattr(self, 'mostrar_toast_exito'):
                        self.mostrar_toast_exito(f"Empleado {nombre_completo} {accion_texto} exitosamente")

                    logger.info(f"✅ Personal {nombre_completo} {accion_texto} exitosamente")

                # Limpiar variables temporales
                self.empleado_seleccionado = PersonalModel()
                self.accion_personal = False

            except Exception as e:
                logger.error(f"❌ Error ejecutando acción de personal: {e}")
                if hasattr(self, 'mostrar_toast_error'):
                    self.mostrar_toast_error(f"Error al modificar a {nombre_completo}")
        else:
            logger.warning("❌ No hay personal seleccionado para modificar")

