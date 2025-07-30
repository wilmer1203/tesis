"""
Estado específico para el rol de Administrador - VERSIÓN OPTIMIZADA
REDUCIDO de 1000 líneas a ~400 líneas usando servicios centralizados
"""

import reflex as rx
import datetime
from datetime import date
from typing import List, Dict, Any, Optional
from .shared_manager_state import SharedManagerState
# Servicios centralizados
from dental_system.services.dashboard_service import dashboard_service
from dental_system.services.pacientes_service import pacientes_service
from dental_system.services.consultas_service import consultas_service
# from dental_system.services.pagos_service import pagos_service

# Modelos tipados
from dental_system.models import (
    PacienteModel,
    AdminStatsModel,
    ConsultaModel,
    PagoModel,
    PacientesStatsModel
)

class AdminState(SharedManagerState):
    """
    Estado específico para el administrador - OPTIMIZADO
    Hereda funcionalidad común y agrega CRUD completo de pacientes/consultas
    """
    
    # ==========================================
    # DATOS ESPECÍFICOS DEL ADMIN - TIPADOS
    # ==========================================
    admin_stats: AdminStatsModel = AdminStatsModel()
    pacientes_stats: PacientesStatsModel = PacientesStatsModel()
    
    # ==========================================
    # GESTIÓN DE PACIENTES - CRUD COMPLETO
    # ==========================================
    # pacientes_list: List[PacienteModel] = []
    selected_paciente: Dict = {}
    show_paciente_modal: bool = False
    
    # Formulario actualizado con campos separados
    paciente_form: Dict[str, str] = {
        # Nombres separados
        "primer_nombre": "",
        "segundo_nombre": "",
        "primer_apellido": "",
        "segundo_apellido": "",
        
        # Documentación
        "numero_documento": "",
        "tipo_documento": "CC",
        "fecha_nacimiento": "",
        "genero": "",
        
        # Teléfonos separados
        "telefono_1": "",
        "telefono_2": "",
        
        # Contacto y ubicación
        "email": "",
        "direccion": "",
        "ciudad": "",
        "departamento": "",
        "ocupacion": "",
        "estado_civil": "",
        
        # Información médica
        "alergias": "",
        "medicamentos_actuales": "",
        "condiciones_medicas": "",
        "antecedentes_familiares": "",
        "observaciones": ""
    }
    
    # Estado para confirmación de eliminación
    show_delete_confirmation: bool = False
    paciente_to_delete: Dict = {}
    
    # ==========================================
    # GESTIÓN DE CONSULTAS - CRUD COMPLETO
    # ==========================================
    selected_consulta: Dict = {}
    show_consulta_modal: bool = False
    
    # Formulario de consulta
    consulta_form: Dict[str, str] = {
        "paciente_id": "",
        "odontologo_id": "",
        "motivo_consulta": "",
        "observaciones_cita": "",
        "notas_internas": "",
        "tipo_consulta": "general",
        "prioridad": "normal"
    }
    
    # Datos de apoyo
    # odontologos_list: List[Dict] = []
    # servicios_list: List[Dict] = []
    
    # ==========================================
    # GESTIÓN DE PAGOS - VISTA Y ESTADÍSTICAS
    # ==========================================
    pagos_list: List[PagoModel] = []
    
    # ==========================================
    # NAVEGACIÓN ESPECÍFICA DEL ADMIN
    # ==========================================
    
    @rx.event
    async def navigate_to(self, page: str):
        """Navegación específica del admin con carga de datos"""
        print(f"[DEBUG] Admin navegando a página: {page}")
        self.current_page = page
        self.clear_global_message()
        
        # Reconfigurar servicios
        self._ensure_services_configured()
        
        if page == "dashboard":
            await self.load_dashboard_data()
        elif page == "pacientes":
            await self.load_pacientes_data()
        elif page == "consultas":
            await self.load_consultas_data()
        elif page == "pagos":
            await self.load_pagos_data()
        yield
    
    # ==========================================
    # IMPLEMENTACIÓN DE MÉTODOS ABSTRACTOS
    # ==========================================
    
    async def _apply_dashboard_stats(self, stats: Dict[str, Any]):
        """Aplica estadísticas específicas del admin"""
        self.admin_stats = AdminStatsModel(**stats)
        
        # Cargar estadísticas específicas de pacientes
        pacientes_stats = await dashboard_service.get_pacientes_stats()
        enhanced_stats = {
            **pacientes_stats,
            "edad_promedio": 0.0,  # TODO: Implementar cálculo real
            "pacientes_con_email": 0,  # TODO: Implementar
            "pacientes_con_telefono": 0,  # TODO: Implementar
            "registros_ultima_semana": 0  # TODO: Implementar
        }
        self.pacientes_stats = PacientesStatsModel(**enhanced_stats)  
    
    async def _apply_consultas_data(self, consultas: List, for_boss: bool = False):
        """Aplica datos de consultas (CRUD completo para admin)"""
        self.consultas_list = consultas
        
        # Cargar datos de apoyo si no están cargados
        if not self.odontologos_list or not self.servicios_list:
            await self._load_support_data()
    
    async def _load_support_data(self):
        """Carga datos de apoyo para consultas"""
        try:
            support_data = await self.get_support_data_for_consultas()
            self.odontologos_list = support_data.get("odontologos", [])
            self.servicios_list = support_data.get("servicios", [])
            print(f"[DEBUG] ✅ Datos de apoyo cargados: {len(self.odontologos_list)} odontólogos, {len(self.servicios_list)} servicios")
        except Exception as e:
            print(f"[ERROR] Error cargando datos de apoyo: {e}")
    
    # ==========================================
    # GESTIÓN DE MODALES PACIENTES
    # ==========================================
    
    def open_paciente_modal(self, paciente_data: PacienteModel = None):
        """Abrir modal de paciente con campos separados"""
        if paciente_data:
            self.selected_paciente = {
                "id": paciente_data.id,
                "numero_documento": paciente_data.numero_documento,
                "activo": paciente_data.activo
            }
            
            self.paciente_form = {
                # Nombres separados
                "primer_nombre": paciente_data.primer_nombre,
                "segundo_nombre": paciente_data.segundo_nombre or "",
                "primer_apellido": paciente_data.primer_apellido,
                "segundo_apellido": paciente_data.segundo_apellido or "",
                
                # Documentación
                "numero_documento": paciente_data.numero_documento,
                "tipo_documento": paciente_data.tipo_documento,
                "fecha_nacimiento": paciente_data.fecha_nacimiento or "",
                "genero": paciente_data.genero or "",
                
                # Teléfonos separados
                "telefono_1": paciente_data.telefono_1 or "",
                "telefono_2": paciente_data.telefono_2 or "",
                
                # Contacto y ubicación
                "email": paciente_data.email or "",
                "direccion": paciente_data.direccion or "",
                "ciudad": paciente_data.ciudad or "",
                "departamento": paciente_data.departamento or "",
                "ocupacion": paciente_data.ocupacion or "",
                "estado_civil": paciente_data.estado_civil or "",
                
                # Información médica
                "alergias": ", ".join(paciente_data.alergias),
                "medicamentos_actuales": ", ".join(paciente_data.medicamentos_actuales),
                "condiciones_medicas": ", ".join(paciente_data.condiciones_medicas),
                "antecedentes_familiares": ", ".join(paciente_data.antecedentes_familiares),
                "observaciones": paciente_data.observaciones or ""
            }
        else:
            self.selected_paciente = {}
            self.paciente_form = {
                "primer_nombre": "",
                "segundo_nombre": "",
                "primer_apellido": "",
                "segundo_apellido": "",
                "numero_documento": "",
                "tipo_documento": "CC",
                "fecha_nacimiento": "",
                "genero": "",
                "telefono_1": "",
                "telefono_2": "",
                "email": "",
                "direccion": "",
                "ciudad": "",
                "departamento": "",
                "ocupacion": "",
                "estado_civil": "",
                "alergias": "",
                "medicamentos_actuales": "",
                "condiciones_medicas": "",
                "antecedentes_familiares": "",
                "observaciones": ""
            }
        self.show_paciente_modal = True
    
    def close_paciente_modal(self):
        """Cerrar modal de paciente"""
        self.show_paciente_modal = False
        self.selected_paciente = {}
        self.clear_global_message()
    
    def update_paciente_form(self, field: str, value: str):
        """Actualizar campo del formulario de paciente"""
        self.paciente_form[field] = value
    
    def open_delete_confirmation(self, paciente_data: PacienteModel):
        """Abrir confirmación de eliminación"""
        self.paciente_to_delete = {
            "id": paciente_data.id,
            "nombre_completo": paciente_data.nombre_completo
        }
        self.show_delete_confirmation = True
    
    def close_delete_confirmation(self):
        """Cerrar confirmación de eliminación"""
        self.show_delete_confirmation = False
        self.paciente_to_delete = {}
    
    # ==========================================
    # OPERACIONES CRUD PACIENTES - OPTIMIZADAS
    # ==========================================
    
    async def save_paciente(self):
        """
        Guardar paciente usando servicio centralizado
        REDUCIDO de 100+ líneas a 15 líneas
        """
        print("[DEBUG] ===== GUARDANDO PACIENTE CON SERVICIO =====")
        self.set_loading(True)
        
        try:
            # Reconfigurar servicios
            self._ensure_services_configured()
            
            user_id = self._get_current_user_id()
            
            if self.selected_paciente:
                # Actualizar existente
                result = await pacientes_service.update_patient(
                    self.selected_paciente["id"], 
                    self.paciente_form
                )
                message = "Paciente actualizado exitosamente"
            else:
                # Crear nuevo
                result = await pacientes_service.create_patient(
                    self.paciente_form, 
                    user_id
                )
                message = "Paciente creado exitosamente"
            
            if result:
                self.show_success(message)
                self.close_paciente_modal()
                await self.load_pacientes_data()
            
        except Exception as e:
            self.handle_service_error(e, "guardando paciente")
        finally:
            self.set_loading(False)
    
    async def delete_paciente(self):
        """
        Eliminar paciente usando servicio centralizado
        REDUCIDO de 50+ líneas a 10 líneas
        """
        print("[DEBUG] Desactivando paciente con servicio...")
        self.set_loading(True)
        
        try:
            if not self.paciente_to_delete:
                self.show_error("No hay paciente seleccionado para eliminar")
                return
            
            # Reconfigurar servicios
            self._ensure_services_configured()
            
            paciente_id = self.paciente_to_delete.get("id")
            user_name = self._get_current_user_name()
            motivo = f"Desactivado desde dashboard por {user_name}"
            
            success = await pacientes_service.deactivate_patient(paciente_id, motivo)
            
            if success:
                nombre = self.paciente_to_delete.get("nombre_completo", "")
                self.show_success(f"Paciente {nombre} desactivado exitosamente")
                await self.load_pacientes_data()
                self.close_delete_confirmation()
            
        except Exception as e:
            self.handle_service_error(e, "eliminando paciente")
        finally:
            self.set_loading(False)
    
    async def reactivate_paciente(self, paciente_data: PacienteModel):
        """
        Reactivar paciente usando servicio centralizado
        REDUCIDO de 30+ líneas a 8 líneas
        """
        print("[DEBUG] Reactivando paciente con servicio...")
        self.set_loading(True)
        
        try:
            self._ensure_services_configured()
            
            success = await pacientes_service.reactivate_patient(paciente_data.id)
            
            if success:
                self.show_success(f"Paciente {paciente_data.nombre_completo} reactivado exitosamente")
                await self.load_pacientes_data()
            
        except Exception as e:
            self.handle_service_error(e, "reactivando paciente")
        finally:
            self.set_loading(False)
    
    # ==========================================
    # GESTIÓN DE MODALES CONSULTAS
    # ==========================================
    
    def open_consulta_modal(self, consulta_data: ConsultaModel = None):
        """Abrir modal de consulta"""
        if consulta_data:
            self.selected_consulta = {
                "id": consulta_data.id,
                "numero_consulta": consulta_data.numero_consulta
            }
            
            self.consulta_form = {
                "paciente_id": consulta_data.paciente_id,
                "odontologo_id": consulta_data.odontologo_id,
                "motivo_consulta": consulta_data.motivo_consulta or "",
                "observaciones_cita": consulta_data.observaciones_cita or "",
                "notas_internas": "",
                "tipo_consulta": consulta_data.tipo_consulta,
                "prioridad": consulta_data.prioridad
            }
        else:
            self.selected_consulta = {}
            self.consulta_form = {
                "paciente_id": "",
                "odontologo_id": "",
                "motivo_consulta": "",
                "observaciones_cita": "",
                "notas_internas": "",
                "tipo_consulta": "general",
                "prioridad": "normal"
            }
        
        self.show_consulta_modal = True
    
    def close_consulta_modal(self):
        """Cerrar modal de consulta"""
        self.show_consulta_modal = False
        self.selected_consulta = {}
        self.clear_global_message()
    
    def update_consulta_form(self, field: str, value: str):
        """Actualizar campo del formulario de consulta"""
        self.consulta_form[field] = value
    
    # ==========================================
    # OPERACIONES CRUD CONSULTAS - OPTIMIZADAS
    # ==========================================
    
    async def save_consulta(self):
        """
        Guardar consulta usando servicio centralizado
        REDUCIDO de 80+ líneas a 15 líneas
        """
        print("[DEBUG] ===== GUARDANDO CONSULTA CON SERVICIO =====")
        self.set_loading(True)
        
        try:
            # Reconfigurar servicios
            self._ensure_services_configured()
            
            user_id = self._get_current_user_id()
            
            if self.selected_consulta:
                # Actualizar existente
                result = await consultas_service.update_consultation(
                    self.selected_consulta["id"],
                    self.consulta_form
                )
                message = "Consulta actualizada exitosamente"
            else:
                # Crear nueva
                result = await consultas_service.create_consultation(
                    self.consulta_form,
                    user_id
                )
                message = "Consulta creada exitosamente"
            
            if result:
                self.show_success(message)
                self.close_consulta_modal()
                await self.load_consultas_data()
            
        except Exception as e:
            self.handle_service_error(e, "guardando consulta")
        finally:
            self.set_loading(False)
    
    async def change_consulta_status(self, consulta_id: str, nuevo_estado: str, consulta_data: ConsultaModel = None):
        """
        Cambiar estado de consulta usando servicio centralizado
        REDUCIDO de 50+ líneas a 10 líneas
        """
        print(f"[DEBUG] Cambiando estado de consulta {consulta_id} a {nuevo_estado}")
        self.set_loading(True)
        
        try:
            self._ensure_services_configured()
            
            success = await consultas_service.change_consultation_status(
                consulta_id, 
                nuevo_estado
            )
            
            if success:
                estado_display = {
                    "programada": "Programada",
                    "confirmada": "Confirmada", 
                    "en_progreso": "En Progreso",
                    "completada": "Completada",
                    "cancelada": "Cancelada",
                    "no_asistio": "No Asistió"
                }
                
                self.show_success(f"Estado cambiado a: {estado_display.get(nuevo_estado, nuevo_estado)}")
                await self.load_consultas_data()
            
        except Exception as e:
            self.handle_service_error(e, "cambiando estado de consulta")
        finally:
            self.set_loading(False)
    
    async def cancel_consulta(self, consulta_id: str, motivo: str = ""):
        """Cancelar consulta con motivo"""
        await self.change_consulta_status(consulta_id, "cancelada")
    
    # ==========================================
    # GESTIÓN DE PAGOS - VISTA
    # ==========================================
    
    async def load_pagos_data(self):
        """Cargar datos de pagos usando servicio"""
        print("[DEBUG] Admin cargando datos de pagos")
        self.set_loading(True)
        
        try:
            self._ensure_services_configured()
            
            # Obtener pagos recientes usando el servicio
            pagos = await pagos_service.get_recent_payments(limit=100)
            self.pagos_list = pagos
            
            print(f"[DEBUG] Pagos cargados: {len(self.pagos_list)} registros")
            
        except Exception as e:
            print(f"[ERROR] Error cargando pagos: {e}")
            self.show_error(f"Error cargando pagos: {str(e)}")
            self.pagos_list = []
        finally:
            self.set_loading(False)
    
    # ==========================================
    # MÉTODOS AUXILIARES ESPECÍFICOS
    # ==========================================
    
    def get_odontologo_name_by_id(self, odontologo_id: str) -> str:
        """Obtener nombre del odontólogo por ID"""
        for odontologo in self.odontologos_list:
            if odontologo['id'] == odontologo_id:
                return odontologo['nombre_completo']
        return "Odontólogo no encontrado"
    
    def get_paciente_name_by_id(self, paciente_id: str) -> str:
        """Obtener nombre del paciente por ID"""
        for paciente in self.pacientes_list:
            if paciente.id == paciente_id:
                return paciente.nombre_completo
        return "Paciente no encontrado"
    
    def get_next_orden_llegada(self) -> int:
        """Obtener siguiente número de orden de llegada"""
        if not self.consultas_list:
            return 1
        return len(self.consultas_list) + 1
    
    # ==========================================
    # PROPIEDADES COMPUTADAS ESPECÍFICAS
    # ==========================================
    
    @rx.var
    def total_pacientes(self) -> int:
        return len(self.pacientes_list)
    
    @rx.var
    def pacientes_activos(self) -> int:
        return len([p for p in self.pacientes_list if p.activo])
    
    @rx.var
    def pacientes_hombres(self) -> int:
        return len([p for p in self.pacientes_list if p.genero == "masculino"])
    
    @rx.var
    def pacientes_mujeres(self) -> int:
        return len([p for p in self.pacientes_list if p.genero == "femenino"])
    
    @rx.var
    def total_consultas_hoy(self) -> int:
        """Total de consultas de hoy"""
        return len(self.consultas_list)
    
    @rx.var
    def consultas_programadas(self) -> int:
        """Consultas en estado programada/confirmada"""
        return len([c for c in self.consultas_list if c.estado in ["programada", "confirmada"]])
    
    @rx.var
    def consultas_en_progreso(self) -> int:
        """Consultas en progreso"""
        return len([c for c in self.consultas_list if c.estado == "en_progreso"])
    
    @rx.var
    def consultas_completadas(self) -> int:
        """Consultas completadas"""
        return len([c for c in self.consultas_list if c.estado == "completada"])
    
    @rx.var
    def filtered_consultas_list(self) -> List[ConsultaModel]:
        """Lista de consultas filtrada"""
        filtered = self.consultas_list
        
        # Filtrar por estado
        if self.consultas_filter_estado != "todos":
            filtered = [c for c in filtered if c.estado == self.consultas_filter_estado]
        
        # Filtrar por odontólogo
        if self.consultas_filter_odontologo != "todos":
            filtered = [c for c in filtered if c.odontologo_id == self.consultas_filter_odontologo]
        
        # Filtrar por búsqueda
        if self.consultas_search:
            search_lower = self.consultas_search.lower()
            filtered = [c for c in filtered if 
                    search_lower in c.paciente_nombre.lower() or
                    search_lower in c.numero_consulta.lower() or
                    search_lower in (c.motivo_consulta or "").lower() or
                    search_lower in c.odontologo_nombre.lower()]
        
        return filtered
    
    @rx.var
    def pagos_pendientes_count(self) -> int:
        return len([p for p in self.pagos_list if p.estado_pago == "pendiente"])
    
    # ==========================================
    # INICIALIZACIÓN
    # ==========================================
    
    def on_load(self):
        """Cargar datos iniciales del admin"""
        print("[DEBUG] Inicializando AdminState optimizado...")
        return self.on_load_shared()