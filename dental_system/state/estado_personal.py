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
from datetime import date, datetime
from typing import Dict, Any, List, Optional, Union
import logging

# Servicios y modelos
from dental_system.services.personal_service import personal_service
from dental_system.models import (
    PersonalModel, 
    PersonalFormModel,
    UsuarioModel,
    RolModel,
    PersonalStatsModel
)

logger = logging.getLogger(__name__)

class EstadoPersonal(rx.State, mixin=True):
    """
    👨‍⚕️ ESTADO ESPECIALIZADO EN GESTIÓN DE PERSONAL
    
    RESPONSABILIDADES:
    - CRUD completo de empleados (solo Gerente)
    - Gestión de roles y especialidades médicas
    - Vinculación automática personal ↔ usuario
    - Cache inteligente para operaciones pesadas  
    - Estadísticas y métricas de empleados
    - Validaciones de integridad de datos
    """
    
    # ==========================================
    # 👨‍⚕️ VARIABLES PRINCIPALES DE PERSONAL
    # ==========================================
    
    # Lista principal de empleados (modelos tipados)
    lista_personal: List[PersonalModel] = []
    total_empleados: int = 0
    
    # Personal seleccionado para operaciones
    empleado_seleccionado: Optional[PersonalModel] = None
    id_empleado_seleccionado: str = ""
    personal_to_modify: Optional[PersonalModel] = None  # Personal marcado para activar/desactivar
    accion_personal: bool = False  # True = activar, False = desactivar
    
    # Formulario de empleado (datos temporales) - MODELO TIPADO
    formulario_empleado: PersonalFormModel = PersonalFormModel()
    errores_validacion_empleado: Dict[str, str] = {}
    
    # ==========================================
    # 👨‍⚕️ ROLES Y ESPECIALIDADES
    # ==========================================
    
    # Catálogos disponibles
    roles_disponibles: List[RolModel] = []
    especialidades_disponibles: List[str] = [
        "Odontología General",
        "Endodoncia", 
        "Periodoncia",
        "Cirugía Oral",
        "Ortodincia",
        "Odontopediatría",
        "Prótesis Dental",
        "Implantología",
        "Estética Dental"
    ]
    
    # Filtros por categoría
    filtro_rol: str = "todos"  # todos, Gerente, Administrador, Odontólogo, Asistente
    filtro_especialidad: str = "todas"
    filtro_estado_empleado: str = "activos"  # todos, activos, inactivos
    
    # ==========================================
    # 👨‍⚕️ BÚSQUEDAS Y FILTROS OPTIMIZADOS
    # ==========================================
    
    # Búsqueda principal con throttling
    termino_busqueda_personal: str = ""
    busqueda_activa_personal: bool = False
    
    # Ordenamiento
    campo_ordenamiento_personal: str = "nombre"  # nombre, fecha_ingreso, rol
    direccion_ordenamiento_personal: str = "asc"  # asc, desc
    
    # Paginación
    pagina_actual_personal: int = 1
    empleados_por_pagina: int = 15
    total_paginas_personal: int = 1
    
    # ==========================================
    # 👨‍⚕️ ESTADÍSTICAS Y MÉTRICAS CACHE
    # ==========================================
    
    # Estadísticas principales
    estadisticas_personal: PersonalStatsModel = PersonalStatsModel()
    ultima_actualizacion_stats_personal: str = ""
    
    # Estados de carga
    cargando_lista_personal: bool = False
    cargando_estadisticas_personal: bool = False
    cargando_operacion_personal: bool = False
    
    # ==========================================
    # 🔧 GESTIÓN DE USUARIOS VINCULADOS
    # ==========================================
    
    # Usuario para vinculación
    formulario_usuario_vinculado: Dict[str, str] = {
        "email": "",
        "password": "",
        "confirm_password": "",
        "rol_id": ""
    }
    errores_usuario: Dict[str, str] = {}
    creando_usuario_vinculado: bool = False
    
    # ==========================================
    # 💡 COMPUTED VARS OPTIMIZADAS CON CACHE
    # ==========================================
    
    @rx.var(cache=True)
    def formulario_personal_data(self) -> PersonalFormModel:
        """Formulario de personal como modelo tipado para UI"""
        try:
            if not self.formulario_empleado:
                return PersonalFormModel()
            return PersonalFormModel.from_dict(self.formulario_empleado)
        except Exception:
            return PersonalFormModel()
    
    @rx.var(cache=True)
    def personal_filtrado(self) -> List[PersonalModel]:
        """
        Lista de personal filtrada y optimizada con cache
        Aplica búsquedas, filtros y ordenamiento
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
                        (emp.especialidad and termino_lower in emp.especialidad.lower()) or
                        (emp.email and termino_lower in emp.email.lower()))
                ]
            
            # Filtro por rol: Ya aplicado en backend via service
            
            # Filtro por especialidad
            if self.filtro_especialidad != "todas":
                resultado = [emp for emp in resultado if emp.especialidad == self.filtro_especialidad]
            
            # Filtro por estado: Ya aplicado en backend via service
            
            # Aplicar ordenamiento
            if self.campo_ordenamiento_personal == "nombre":
                resultado = sorted(resultado, key=lambda x: x.nombre_completo_display)
            elif self.campo_ordenamiento_personal == "fecha_ingreso":
                resultado = sorted(resultado, key=lambda x: x.fecha_ingreso or "")
            elif self.campo_ordenamiento_personal == "rol":
                resultado = sorted(resultado, key=lambda x: x.rol_nombre_computed)
            
            # Aplicar dirección de ordenamiento
            if self.direccion_ordenamiento_personal == "desc":
                resultado.reverse()
            
            return resultado
            
        except Exception as e:
            logger.error(f"Error en personal_filtrado: {e}")
            return []
    
    @rx.var(cache=True)
    def personal_paginado(self) -> List[PersonalModel]:
        """Lista paginada del personal filtrado"""
        try:
            inicio = (self.pagina_actual_personal - 1) * self.empleados_por_pagina
            fin = inicio + self.empleados_por_pagina
            return self.personal_filtrado[inicio:fin]
        except Exception:
            return []
    
    @rx.var(cache=True)
    def info_paginacion_personal(self) -> Dict[str, int]:
        """Información de paginación de personal"""
        try:
            total_filtrado = len(self.personal_filtrado)
            total_paginas = max(1, (total_filtrado + self.empleados_por_pagina - 1) // self.empleados_por_pagina)
            
            return {
                "pagina_actual": self.pagina_actual_personal,
                "total_paginas": total_paginas,
                "total_items": total_filtrado,
                "items_por_pagina": self.empleados_por_pagina,
                "item_inicio": ((self.pagina_actual_personal - 1) * self.empleados_por_pagina) + 1,
                "item_fin": min(self.pagina_actual_personal * self.empleados_por_pagina, total_filtrado)
            }
        except Exception:
            return {
                "pagina_actual": 1,
                "total_paginas": 1,
                "total_items": 0,
                "items_por_pagina": self.empleados_por_pagina,
                "item_inicio": 0,
                "item_fin": 0
            }
    
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
    def personal_por_rol(self) -> Dict[str, int]:
        """Estadísticas de personal agrupado por rol"""
        try:
            stats = {}
            for empleado in self.lista_personal:
                if empleado.estado_laboral == "activo":  # Solo activos
                    rol = empleado.rol_nombre_computed
                    stats[rol] = stats.get(rol, 0) + 1
            return stats
        except Exception:
            return {}
    
    # UNUSED - [2025-01-04] - Computed vars no utilizados
    # @rx.var(cache=True)
    # def empleados_activos_count(self) -> int:
    #     """Cantidad de empleados activos"""
    #     try:
    #         return len([emp for emp in self.lista_personal if emp.estado_laboral == "activo"])
    #     except Exception:
    #         return 0
    
    # @rx.var(cache=True)
    # def especialidades_en_uso(self) -> List[str]:
    #     """Lista de especialidades que tienen empleados asignados"""
    #     try:
    #         especialidades = set()
    #         for emp in self.lista_personal:
    #             if emp.estado_laboral == "activo" and emp.especialidad:
    #                 especialidades.add(emp.especialidad)
    #         return sorted(list(especialidades))
    #     except Exception:
    #         return []
    
    # ==========================================
    # 🔄 MÉTODOS DE CARGA DE DATOS
    # ==========================================
    
    async def cargar_lista_personal(self):
        """
        Carga la lista de personal desde el servicio
        Validando permisos de usuario (solo Gerente)
        """
        # Verificar autenticación y permisos (ya disponible por mixin)
        if not self.esta_autenticado:
            logger.warning("Usuario no autenticado intentando cargar personal")
            return
        
        if not self.rol_usuario == "gerente":
            logger.warning(f"Usuario {self.rol_usuario} sin permisos para ver personal")
            return
        
        self.cargando_lista_personal = True
        
        try:
            # Establecer contexto de usuario en el servicio (disponible directamente por mixin)
            personal_service.set_user_context(
                user_id=self.id_usuario,
                user_profile=self.perfil_usuario
            )
            
            # Obtener personal con filtros actuales
            personal_data = await personal_service.get_filtered_personal(
                search=self.termino_busqueda_personal if len(self.termino_busqueda_personal) >= 2 else None,
                tipo_personal=self.filtro_rol if self.filtro_rol != "todos" else None,
                activos_only=self.filtro_estado_empleado == "activos"
            )
            
            # Convertir a modelos tipados
            self.lista_personal = personal_data
            self.total_empleados = len(personal_data)
            
            # Actualizar paginación
            self._calcular_paginacion_personal()
            
            # Log exitoso
            logger.info(f"✅ Lista personal cargada: {len(personal_data)} empleados")
            
        except PermissionError as e:
            logger.warning(f"Error de permisos al cargar personal: {e}")
            # Mostrar toast de error (ya disponible por mixin)
            if hasattr(self, 'mostrar_toast_error'):
                self.mostrar_toast_error("Sin permisos para acceder al personal")
            
        except Exception as e:
            logger.error(f"❌ Error cargando lista personal: {e}")
            self.handle_error("Error al cargar lista de personal", e)
            
        finally:
            self.cargando_lista_personal = False
    
    async def cargar_roles_disponibles(self):
        """Carga los roles disponibles del sistema"""
        try:
            roles_data = await personal_service.get_roles_disponibles()
            self.roles_disponibles = roles_data
            logger.info(f"✅ Roles disponibles cargados: {len(roles_data)}")
        except Exception as e:
            logger.error(f"❌ Error cargando roles: {e}")
    
    async def cargar_estadisticas_personal(self):
        """Carga estadísticas del personal con cache"""
        self.cargando_estadisticas_personal = True
        
        try:
            stats_data = await personal_service.get_personal_stats()
            # Convertir dict a modelo si es necesario
            if isinstance(stats_data, dict):
                self.estadisticas_personal = PersonalStatsModel.from_dict(stats_data)
            else:
                self.estadisticas_personal = stats_data
            self.ultima_actualizacion_stats_personal = datetime.now().strftime("%H:%M:%S")
            
            logger.info("✅ Estadísticas de personal actualizadas")
            
        except Exception as e:
            logger.error(f"❌ Error cargando estadísticas personal: {e}")
        finally:
            self.cargando_estadisticas_personal = False
    
    # ==========================================
    # 🔍 MÉTODOS DE BÚSQUEDA Y FILTROS
    # ==========================================
    
    @rx.event # Throttling para performance
    async def buscar_personal(self, termino: str):
        """
        Búsqueda de personal con throttling automático
        Solo busca si hay al menos 2 caracteres
        """
        self.termino_busqueda_personal = termino.strip()
        self.busqueda_activa_personal = True
        self.pagina_actual_personal = 1  # Reset a primera página
        
        # Solo recargar si hay término válido o si se está limpiando
        if len(termino.strip()) >= 2 or termino.strip() == "":
            await self.cargar_lista_personal()
        
        self.busqueda_activa_personal = False
    
    async def filtrar_por_rol(self, rol: str):
        """Filtrar personal por rol"""
        self.filtro_rol = rol
        self.pagina_actual_personal = 1
        await self.cargar_lista_personal()
    
    async def filtrar_por_especialidad(self, especialidad: str):
        """Filtrar personal por especialidad"""
        self.filtro_especialidad = especialidad
        self.pagina_actual_personal = 1
        await self.cargar_lista_personal()
    
    async def filtrar_por_estado(self, estado: str):
        """Filtrar personal por estado (activo/inactivo)"""
        self.filtro_estado_empleado = estado
        self.pagina_actual_personal = 1
        await self.cargar_lista_personal()
    
    # UNUSED - [2025-01-04] - Método de ordenamiento no utilizado
    # async def ordenar_personal(self, campo: str):
    #     """Cambiar ordenamiento de la lista"""
    #     if self.campo_ordenamiento_personal == campo:
    #         # Toggle dirección si es el mismo campo
    #         self.direccion_ordenamiento_personal = "desc" if self.direccion_ordenamiento_personal == "asc" else "asc"
    #     else:
    #         # Nuevo campo, empezar en ascendente
    #         self.campo_ordenamiento_personal = campo
    #         self.direccion_ordenamiento_personal = "asc"
    #     
    #     # Las computed vars se actualizarán automáticamente
    
    # ==========================================
    # ➕ MÉTODOS CRUD DE PERSONAL
    # ==========================================
    
    async def crear_empleado(self):
        """
        Crear nuevo empleado con validaciones
        Solo accesible por Gerente
        """
        # Verificar permisos (disponible directamente por mixin)
        if not self.rol_usuario == "gerente":
            # Mostrar toast de error (método directo disponible por mixin)
            if hasattr(self, 'mostrar_toast_error'):
                self.mostrar_toast_error("Solo el gerente puede crear empleados")
            return
        
        # Validar formulario
        if not self.validar_formulario_empleado():
            return
        
        self.cargando_operacion_personal = True
        
        try:
            # Establecer contexto de usuario en el servicio
            personal_service.set_user_context(
                user_id=self.id_usuario,
                user_profile=self.perfil_usuario
            )
            
            # Crear empleado
            nuevo_empleado = await personal_service.create_staff_member(
                self.formulario_empleado,
                self.id_usuario
            )
            
            # Agregar a la lista
            self.lista_personal.append(nuevo_empleado)
            self.total_empleados += 1
            
            # Limpiar formulario
            self.limpiar_formulario_empleado()
            
            # Cerrar modal y mostrar éxito (métodos directos disponibles por mixin)
            if hasattr(self, 'cerrar_modal'):
                self.cerrar_modal("modal_empleado")
            if hasattr(self, 'mostrar_toast_exito'):
                self.mostrar_toast_exito(f"Empleado {nuevo_empleado.nombre_completo} creado exitosamente")
            
            logger.info(f"✅ Empleado creado: {nuevo_empleado.nombre_completo}")
            
        except Exception as e:
            logger.error(f"❌ Error creando empleado: {e}")
            if hasattr(self, 'mostrar_toast_error'):
                self.mostrar_toast_error("Error al crear empleado")
            
        finally:
            self.cargando_operacion_personal = False
    
    async def actualizar_empleado(self):
        """Actualizar empleado existente"""
        if not self.empleado_seleccionado or not getattr(self.empleado_seleccionado, 'id', None):
            return
        
        if not self.validar_formulario_empleado():
            return
        
        # Métodos disponibles directamente por mixin
        self.cargando_operacion_personal = True
        
        try:
            # Establecer contexto de usuario en el servicio
            personal_service.set_user_context(
                user_id=self.id_usuario,
                user_profile=self.perfil_usuario
            )
            
            # Actualizar empleado
            empleado_actualizado = await personal_service.update_staff_member(
                personal_id=getattr(self.empleado_seleccionado, 'id', self.id_empleado_seleccionado),
                personal_form=self.formulario_empleado,
            )
            
            # Actualizar en la lista
            for i, emp in enumerate(self.lista_personal):
                if emp.id == empleado_actualizado.id:
                    self.lista_personal[i] = empleado_actualizado
                    break
            
            # Actualizar seleccionado
            self.empleado_seleccionado = empleado_actualizado
            
            # Limpiar y cerrar
            self.limpiar_formulario_empleado()
            if hasattr(self, 'cerrar_modal'):
                self.cerrar_modal("modal_empleado")
            if hasattr(self, 'mostrar_toast_exito'):
                self.mostrar_toast_exito("Empleado actualizado exitosamente")
            
            logger.info(f"✅ Empleado actualizado: {empleado_actualizado.nombre_completo}")
            
        except Exception as e:
            logger.error(f"❌ Error actualizando empleado: {e}")
            if hasattr(self, 'mostrar_toast_error'):
                self.mostrar_toast_error("Error al actualizar empleado")
            
        finally:
            self.cargando_operacion_personal = False
    
    @rx.event
    async def guardar_personal_formulario(self):
        """
        Guardar empleado - unifica crear y actualizar
        Decide automáticamente entre crear o actualizar según si hay empleado seleccionado
        """
        try:
            if self.empleado_seleccionado and getattr(self.empleado_seleccionado, 'id', None):
                # Modo editar: actualizar empleado existente
                await self.actualizar_empleado()
            else:
                # Modo crear: crear nuevo empleado
                await self.crear_empleado()
                
        except Exception as e:
            logger.error(f"❌ Error guardando personal: {e}")
            if hasattr(self, 'mostrar_toast_error'):
                self.mostrar_toast_error("Error al guardar empleado")
    
    async def activar_desactivar_empleado(self, personal_id: str, activar: bool):
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
                self.personal_to_modify = empleado_encontrado
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
        self.id_empleado_seleccionado = empleado.id
        
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
            "salario": str(empleado.salario) if empleado.salario else "",
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
            "acepta_pacientes_nuevos": empleado.acepta_pacientes_nuevos,
            "orden_preferencia": empleado.orden_preferencia,
            "tipo_documento": empleado.tipo_documento or "CI",
            "observaciones": empleado.observaciones or ""
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
        self.id_empleado_seleccionado = ""
        
        # También limpiar formulario de usuario vinculado
        self.formulario_usuario_vinculado = {
            "email": "",
            "password": "",
            "confirm_password": "",
            "rol_id": ""
        }
        self.errores_usuario = {}
    
    def actualizar_campo_formulario_empleado(self, campo: str, valor: str):
        """Actualizar campo específico del formulario tipado"""
        # ✅ ACTUALIZAR CAMPO EN MODELO TIPADO usando setattr
        if hasattr(self.formulario_empleado, campo):
            # Convertir valor según el tipo del campo
            if campo in ["acepta_pacientes_nuevos"]:
                valor = bool(valor)
            elif campo in ["orden_preferencia"]:
                valor = int(valor) if valor.isdigit() else 1
            
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
            "primer_nombre", "primer_apellido", "numero_documento", "email", "celular", "tipo_personal"
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
        
        # Email válido
        email = self.formulario_empleado.email.strip() if self.formulario_empleado.email else ""
        if email and "@" not in email:
            self.errores_validacion_empleado["email"] = "Email inválido"
        
        # Celular válido (requerido)
        celular = self.formulario_empleado.celular.strip() if self.formulario_empleado.celular else ""
        if celular and len(celular) < 10:
            self.errores_validacion_empleado["celular"] = "Celular debe tener al menos 10 dígitos"
        
        # Salario válido
        salario = self.formulario_empleado.salario.strip() if self.formulario_empleado.salario else ""
        if salario:
            try:
                float(salario)
            except ValueError:
                self.errores_validacion_empleado["salario"] = "Salario debe ser un número válido"
        
        # ✅ CONTRASEÑA VÁLIDA (solo para usuarios nuevos)
        if not self.empleado_seleccionado:
            password = self.formulario_empleado.usuario_password.strip() if self.formulario_empleado.usuario_password else ""
            if password and len(password) < 6:
                self.errores_validacion_empleado["usuario_password"] = "La contraseña debe tener al menos 6 caracteres"
        
        return len(self.errores_validacion_empleado) == 0
    
    # ==========================================
    # 📄 MÉTODOS DE PAGINACIÓN
    # ==========================================
    
    def siguiente_pagina_personal(self):
        """Ir a la siguiente página"""
        info = self.info_paginacion_personal
        if self.pagina_actual_personal < info["total_paginas"]:
            self.pagina_actual_personal += 1
    
    def pagina_anterior_personal(self):
        """Ir a la página anterior"""
        if self.pagina_actual_personal > 1:
            self.pagina_actual_personal -= 1
    
    def ir_a_pagina_personal(self, numero_pagina: int):
        """Ir a una página específica"""
        info = self.info_paginacion_personal
        if 1 <= numero_pagina <= info["total_paginas"]:
            self.pagina_actual_personal = numero_pagina
    
    def _calcular_paginacion_personal(self):
        """Recalcular paginación basado en filtros actuales"""
        total_filtrado = len(self.personal_filtrado)
        self.total_paginas_personal = max(1, (total_filtrado + self.empleados_por_pagina - 1) // self.empleados_por_pagina)
        
        # Asegurar que la página actual sea válida
        if self.pagina_actual_personal > self.total_paginas_personal:
            self.pagina_actual_personal = max(1, self.total_paginas_personal)
    
    # ==========================================
    # 🔧 MÉTODOS DE UTILIDAD Y CACHE
    # ==========================================
    
    def handle_error(self, contexto: str, error: Exception):
        """Manejar errores de manera centralizada"""
        logger.error(f"{contexto}: {str(error)}")
        
        # Mostrar notificación si está disponible por mixin
        try:
            if hasattr(self, 'mostrar_toast_error'):
                self.mostrar_toast_error(f"Error: {contexto}")
        except Exception:
            # Si no se puede mostrar toast, solo log
            pass
    
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
                self.id_empleado_seleccionado = personal_id
                logger.info(f"🎯 Empleado seleccionado: {empleado_encontrado.nombre_completo}")
            else:
                logger.warning(f"⚠️ Empleado {personal_id} no encontrado en lista local")
                self.empleado_seleccionado = None
                self.id_empleado_seleccionado = ""
                
        except Exception as e:
            logger.error(f"❌ Error seleccionando empleado: {e}")
            self.empleado_seleccionado = None
            self.id_empleado_seleccionado = ""
    
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
                self.abrir_modal_personal("editar")
                logger.info(f"📝 Modal editar personal abierto: {personal_id}")
            else:
                # Modo crear: limpiar selección y abrir modal
                self.empleado_seleccionado = None
                self.id_empleado_seleccionado = ""
                self.limpiar_formulario_empleado()  
                # Abrir modal crear
                self.abrir_modal_personal("crear")  
                logger.info("✅ Modal crear personal abierto")
                
        except Exception as e:
            self.handle_error("abrir modal personal", e)
    
    @rx.event
    async def ejecutar_accion_personal(self):
        """
        ✅ EJECUTAR ACCIÓN DE ACTIVAR/DESACTIVAR PERSONAL

        Ejecuta la acción almacenada en self.accion_personal
        sobre el empleado en self.personal_to_modify
        """
        if self.personal_to_modify and self.personal_to_modify.id:
            nombre_completo = f"{self.personal_to_modify.primer_nombre} {self.personal_to_modify.primer_apellido}"
            personal_id = self.personal_to_modify.id
            activar = self.accion_personal

            try:
                # Establecer contexto de usuario en el servicio
                personal_service.set_user_context(
                    user_id=self.id_usuario,
                    user_profile=self.perfil_usuario
                )

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
                self.personal_to_modify = None
                self.accion_personal = False

            except Exception as e:
                logger.error(f"❌ Error ejecutando acción de personal: {e}")
                if hasattr(self, 'mostrar_toast_error'):
                    self.mostrar_toast_error(f"Error al modificar a {nombre_completo}")
        else:
            logger.warning("❌ No hay personal seleccionado para modificar")

