"""
Estado específico para el rol de Administrador - CORREGIDO COMPLETO
Actualizado para usar nombres y teléfonos separados según nueva estructura DB
"""

import reflex as rx
import datetime
from datetime import date
from typing import List, Dict, Any, Optional
from .base import BaseState
from dental_system.supabase.client import supabase_client
from dental_system.supabase.tablas import pacientes_table, consultas_table, services_table

# ✅ IMPORTAR MODELOS TIPADOS CORREGIDOS
from dental_system.models import (
    PacienteModel,
    AdminStatsModel,
    ConsultaModel,
    PagoModel,
    PacientesStatsAdminModel
)


class AdminState(BaseState):
    """Estado específico para el administrador del sistema odontológico - ACTUALIZADO PARA PACIENTES"""
    
    # ==========================================
    # NAVEGACIÓN Y UI
    # ==========================================
    current_page: str = "dashboard"
    sidebar_collapsed: bool = False
    
    # ==========================================
    # DATOS DEL DASHBOARD - TIPADO
    # ==========================================
    admin_stats: AdminStatsModel = AdminStatsModel()
    
    # ==========================================
    # ✅ GESTIÓN DE PACIENTES - FORMULARIO CORREGIDO PARA NUEVOS CAMPOS
    # ==========================================
    pacientes_list: List[PacienteModel] = []
    selected_paciente: Dict = {}
    show_paciente_modal: bool = False
    
    # ✅ FORMULARIO ACTUALIZADO CON CAMPOS SEPARADOS
    paciente_form: Dict[str, str] = {
        # ✅ NOMBRES SEPARADOS (según nueva estructura DB)
        "primer_nombre": "",
        "segundo_nombre": "",
        "primer_apellido": "",
        "segundo_apellido": "",
        
        # Documentación
        "numero_documento": "",
        "tipo_documento": "CC",
        "fecha_nacimiento": "",
        "genero": "",
        
        # ✅ TELÉFONOS SEPARADOS (según nueva estructura DB)
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
    
    # Filtros y búsqueda
    pacientes_search: str = ""
    pacientes_filter_genero: str = ""
    pacientes_filter_activos: str = "activos"
    
    # ==========================================
    # ESTADÍSTICAS DE PACIENTES - TIPADO
    # ==========================================
    pacientes_stats: PacientesStatsAdminModel = PacientesStatsAdminModel()
    
    # ==========================================
    # GESTIÓN DE CONSULTAS - CORREGIDO
    # ==========================================
    consultas_list: List[ConsultaModel] = []
    selected_consulta: Dict = {}
    show_consulta_modal: bool = False

    # FORMULARIO DE CONSULTA
    consulta_form: Dict[str, str] = {
        "paciente_id": "",
        "odontologo_id": "",
        "motivo_consulta": "",
        "observaciones_cita": "",
        "notas_internas": "",
        "tipo_consulta": "general",  # general, control, urgencia
        "prioridad": "normal"  # normal, alta, urgente
    }

    # DATOS DE APOYO
    odontologos_list: List[Dict] = []
    servicios_list: List[Dict] = []

    # FILTROS DE CONSULTAS
    consultas_filter_estado: str = "todos"
    consultas_filter_odontologo: str = "todos"
    consultas_search: str = ""

    # ==========================================
    # FUTURAS FUNCIONALIDADES - TIPADO
    # ==========================================
    consultas_hoy: List[ConsultaModel] = []
    pagos_list: List[PagoModel] = []
    
    # ==========================================
    # MÉTODOS DE NAVEGACIÓN
    # ==========================================
    
    @rx.event
    async def navigate_to(self, page: str):
        print(f"[DEBUG] Admin navegando a página: {page}")
        self.current_page = page
        self.clear_global_message()

        if page == "dashboard":
            await self.load_dashboard_data()
        elif page == "pacientes":
            await self.load_pacientes_data()
        elif page == "consultas":
            await self.load_consultas_data()
        elif page == "pagos":
            await self.load_pagos_data()
        yield
    
    def toggle_sidebar(self):
        """Alternar el estado del sidebar"""
        self.sidebar_collapsed = not self.sidebar_collapsed
    
    # ==========================================
    # MÉTODOS DE CARGA DE DATOS
    # ==========================================
    
    async def load_dashboard_data(self):
        """Cargar datos principales del dashboard del administrador"""
        print("[DEBUG] Cargando datos del dashboard admin...")
        self.set_loading(True)
        try:
            # Cargar estadísticas de pacientes
            await self._load_pacientes_stats()
            
            # Cargar datos generales del admin
            stats_dict = await self._get_admin_dashboard_stats()
            self.admin_stats = AdminStatsModel(**stats_dict)
            
            print(f"[DEBUG] Estadísticas admin cargadas: {stats_dict}")
        
        except Exception as e:
            print(f"[ERROR] Error cargando dashboard admin: {e}")
            self.show_error(f"Error cargando datos del dashboard: {str(e)}")
        finally:
            self.set_loading(False)
    
    async def load_pacientes_data(self):
        """Cargar datos de pacientes con tipado consistente"""
        print("[DEBUG] Cargando datos de pacientes con modelos tipados")
        self.set_loading(True)
        
        try:
            # Obtener pacientes filtrados
            pacientes_data = pacientes_table.get_filtered_patients(
                activos_only=self.pacientes_filter_activos == "activos",
                busqueda=self.pacientes_search if self.pacientes_search else None,
                genero=self.pacientes_filter_genero if self.pacientes_filter_genero != "todos" else None
            )
            
            # ✅ CONVERTIR A MODELOS TIPADOS 
            self.pacientes_list = []
            for item in pacientes_data:
                try:
                    paciente_model = PacienteModel.from_dict(item)
                    self.pacientes_list.append(paciente_model)
                except Exception as e:
                    print(f"[WARNING] Error convirtiendo paciente: {e}")
                    print(f"[DEBUG] Datos problemáticos: {item}")
            
            print(f"[DEBUG] ✅ Pacientes convertidos a modelos: {len(self.pacientes_list)} registros")
            
            # Cargar estadísticas
            await self._load_pacientes_stats()
           
        except Exception as e:
            print(f"[ERROR] Error cargando pacientes: {e}")
            self.show_error(f"Error cargando pacientes: {str(e)}")
            self.pacientes_list = []
                
        finally:
            self.set_loading(False)
    
    async def _load_pacientes_stats(self):
        """Cargar estadísticas de pacientes"""
        try:
            stats = pacientes_table.get_patient_stats()
            
            self.pacientes_stats = PacientesStatsAdminModel(
                total=stats.get("total", 0),
                nuevos_mes=stats.get("nuevos_mes", 0),
                activos=stats.get("activos", 0),
                hombres=stats.get("hombres", 0),
                mujeres=stats.get("mujeres", 0),
                # Estadísticas adicionales (placeholder por ahora)
                edad_promedio=0.0,
                pacientes_con_email=0,
                pacientes_con_telefono=0,
                registros_ultima_semana=0
            )
            
            print(f"[DEBUG] Estadísticas de pacientes tipadas: {stats}")
        except Exception as e:
            print(f"[ERROR] Error cargando estadísticas de pacientes: {e}")
            self.pacientes_stats = PacientesStatsAdminModel()
    
    # ==========================================
    # ✅ MÉTODOS DE CONSULTAS - CORREGIDOS PARA USAR VISTA
    # ==========================================
    
    async def load_consultas_data(self):
        """✅ CORREGIDO: Cargar datos de consultas del día con nombres desde vista"""
        print("[DEBUG] Cargando datos de consultas del día - CORREGIDO")
        self.set_loading(True)
        
        try:
            # Obtener consultas de hoy usando ConsultationsTable CORREGIDA
            consultas_data = consultas_table.get_today_consultations()
            
            # Convertir a modelos tipados
            self.consultas_list = []
            for i, item in enumerate(consultas_data, 1):
                try:
                    # El orden de llegada ya viene en los datos procesados
                    if not item.get('orden_llegada'):
                        item['orden_llegada'] = i
                    
                    consulta_model = ConsultaModel.from_dict(item)
                    self.consultas_list.append(consulta_model)
                    
                except Exception as e:
                    print(f"[WARNING] Error convirtiendo consulta: {e}")
                    print(f"[DEBUG] Datos problemáticos: {item}")
            
            print(f"[DEBUG] ✅ Consultas del día cargadas: {len(self.consultas_list)} registros")
            
            # Cargar datos de apoyo si no están cargados
            if not self.odontologos_list:
                await self._load_odontologos_list()
            if not self.servicios_list:
                await self._load_servicios_list()
                
        except Exception as e:
            print(f"[ERROR] Error cargando consultas: {e}")
            import traceback
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            self.show_error(f"Error cargando consultas: {str(e)}")
            self.consultas_list = []
        finally:
            self.set_loading(False)
    
    async def _load_odontologos_list(self):
        """✅ CORREGIDO: Cargar lista de odontólogos usando vista"""
        try:
            from dental_system.supabase.tablas import personal_table
            
            # Usar método que debería funcionar con la vista
            odontologos_data = personal_table.get_dentists(incluir_inactivos=False)
            self.odontologos_list = []
            
            for item in odontologos_data:
                # ✅ MANEJO ROBUSTO DE NOMBRES DESDE VISTA
                nombre_completo = ""
                
                # Si viene desde vista (método preferido)
                if 'nombre_completo' in item:
                    nombre_completo = item['nombre_completo']
                else:
                    # Fallback: construir desde campos separados si la vista falla
                    nombres = []
                    if item.get('primer_nombre'):
                        nombres.append(item['primer_nombre'])
                    if item.get('segundo_nombre'):
                        nombres.append(item['segundo_nombre'])
                    if item.get('primer_apellido'):
                        nombres.append(item['primer_apellido'])
                    if item.get('segundo_apellido'):
                        nombres.append(item['segundo_apellido'])
                    nombre_completo = ' '.join(nombres) if nombres else 'Sin nombre'
                
                self.odontologos_list.append({
                    'id': item.get('id', ''),
                    'nombre_completo': nombre_completo,
                    'especialidad': item.get('especialidad', ''),
                    'estado_laboral': item.get('estado_laboral', 'activo'),
                    'tipo_personal': item.get('tipo_personal', 'Odontólogo')
                })
            
            print(f"[DEBUG] ✅ Odontólogos cargados desde vista: {len(self.odontologos_list)}")
            
        except Exception as e:
            print(f"[ERROR] Error cargando odontólogos: {e}")
            import traceback
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            
            # ✅ FALLBACK: Cargar directamente desde tabla si vista falla
            await self._load_odontologos_fallback()

    async def _load_odontologos_fallback(self):
        """✅ NUEVO: Fallback para cargar odontólogos si vista falla"""
        try:
            print("[DEBUG] 🔄 Usando fallback para cargar odontólogos...")
            
            # Query directo a tabla personal + usuarios
            response = supabase_client.get_client().table('personal').select("""
                id, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido,
                especialidad, estado_laboral, tipo_personal,
                usuarios!inner(id, activo)
            """).eq('tipo_personal', 'Odontólogo').eq('estado_laboral', 'activo').eq('usuarios.activo', True).execute()
            
            self.odontologos_list = []
            
            for item in response.data or []:
                # Construir nombre completo
                nombres = []
                if item.get('primer_nombre'):
                    nombres.append(item['primer_nombre'])
                if item.get('segundo_nombre'):
                    nombres.append(item['segundo_nombre'])
                if item.get('primer_apellido'):
                    nombres.append(item['primer_apellido'])
                if item.get('segundo_apellido'):
                    nombres.append(item['segundo_apellido'])
                
                nombre_completo = ' '.join(nombres) if nombres else 'Sin nombre'
                
                self.odontologos_list.append({
                    'id': item['id'],
                    'nombre_completo': nombre_completo,
                    'especialidad': item.get('especialidad', ''),
                    'estado_laboral': item.get('estado_laboral', 'activo'),
                    'tipo_personal': item.get('tipo_personal', 'Odontólogo')
                })
            
            print(f"[DEBUG] ✅ Odontólogos cargados con fallback: {len(self.odontologos_list)}")
            
        except Exception as e:
            print(f"[ERROR] Error en fallback de odontólogos: {e}")
            self.odontologos_list = []

    async def _load_servicios_list(self):
        """Cargar lista de servicios activos"""
        try:
            servicios_data = services_table.get_active_services()
            self.servicios_list = []
            
            for item in servicios_data:
                self.servicios_list.append({
                    'id': item['id'],
                    'codigo': item.get('codigo', ''),
                    'nombre': item.get('nombre', ''),
                    'categoria': item.get('categoria', ''),
                    'precio_base': item.get('precio_base', 0)
                })
            
            print(f"[DEBUG] Servicios cargados: {len(self.servicios_list)}")
            
        except Exception as e:
            print(f"[ERROR] Error cargando servicios: {e}")
            self.servicios_list = []

    async def load_pagos_data(self):
        """Cargar datos de pagos - TIPADO CON MODELOS"""
        print("[DEBUG] Cargando datos de pagos (tipado)")
        self.set_loading(True)
        try:
            # Pagos recientes
            response = supabase_client.get_client().table('pagos').select('''
                *,
                pacientes:paciente_id (primer_nombre, primer_apellido)
            ''').order('fecha_pago', desc=True).limit(100).execute()
            
            # ✅ CONVERTIR A MODELOS TIPADOS
            self.pagos_list = []
            if response.data:
                for item in response.data:
                    try:
                        pago_model = PagoModel.from_dict(item)
                        self.pagos_list.append(pago_model)
                    except Exception as e:
                        print(f"[WARNING] Error convirtiendo pago: {e}")
            
            print(f"[DEBUG] Pagos tipados: {len(self.pagos_list)} registros")
            
        except Exception as e:
            print(f"[ERROR] Error cargando pagos: {e}")
            self.show_error(f"Error cargando pagos: {str(e)}")
            self.pagos_list = []
        finally:
            self.set_loading(False)
    
    # ==========================================
    #  GESTIÓN DE MODALES Paciente
    # ==========================================
    
    def open_paciente_modal(self, paciente_data: PacienteModel = None):
        """✅ CORREGIDO: Abrir modal de paciente con campos separados"""
        if paciente_data:
            # ✅ CONVERTIR MODELO A DICT PARA EL FORMULARIO
            self.selected_paciente = {
                "id": paciente_data.id,
                "numero_documento": paciente_data.numero_documento,
                "activo": paciente_data.activo
            }
            
            # ✅ LLENAR FORMULARIO CON CAMPOS SEPARADOS
            self.paciente_form = {
                # ✅ NOMBRES SEPARADOS
                "primer_nombre": paciente_data.primer_nombre,
                "segundo_nombre": paciente_data.segundo_nombre or "",
                "primer_apellido": paciente_data.primer_apellido,
                "segundo_apellido": paciente_data.segundo_apellido or "",
                
                # Documentación
                "numero_documento": paciente_data.numero_documento,
                "tipo_documento": paciente_data.tipo_documento,
                "fecha_nacimiento": paciente_data.fecha_nacimiento or "",
                "genero": paciente_data.genero or "",
                
                # ✅ TELÉFONOS SEPARADOS
                "telefono_1": paciente_data.telefono_1 or "",
                "telefono_2": paciente_data.telefono_2 or "",
                
                # Contacto y ubicación
                "email": paciente_data.email or "",
                "direccion": paciente_data.direccion or "",
                "ciudad": paciente_data.ciudad or "",
                "departamento": paciente_data.departamento or "",
                "ocupacion": paciente_data.ocupacion or "",
                "estado_civil": paciente_data.estado_civil or "",
                
                # Información médica (convertir arrays a strings)
                "alergias": ", ".join(paciente_data.alergias),
                "medicamentos_actuales": ", ".join(paciente_data.medicamentos_actuales),
                "condiciones_medicas": ", ".join(paciente_data.condiciones_medicas),
                "antecedentes_familiares": ", ".join(paciente_data.antecedentes_familiares),
                "observaciones": paciente_data.observaciones or ""
            }
        else:
            # ✅ FORMULARIO VACÍO CON CAMPOS SEPARADOS
            self.selected_paciente = {}
            self.paciente_form = {
                # ✅ NOMBRES SEPARADOS
                "primer_nombre": "",
                "segundo_nombre": "",
                "primer_apellido": "",
                "segundo_apellido": "",
                
                # Documentación
                "numero_documento": "",
                "tipo_documento": "CC",
                "fecha_nacimiento": "",
                "genero": "",
                
                # ✅ TELÉFONOS SEPARADOS
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
        self.show_paciente_modal = True
    
    def close_paciente_modal(self):
        """Cerrar modal de paciente"""
        self.show_paciente_modal = False
        self.selected_paciente = {}
        self.clear_global_message()
    
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
    
    def set_pacientes_search(self, search_term: str):
        """Establecer término de búsqueda"""
        self.pacientes_search = search_term
    
    def set_pacientes_filter_genero(self, genero: str):
        """Establecer filtro por género"""
        self.pacientes_filter_genero = genero
    
    def set_pacientes_filter_activos(self, activos: str):
        """Establecer filtro por estado activo"""
        self.pacientes_filter_activos = activos
    
    @rx.event
    async def apply_pacientes_filters(self):
        """Aplicar filtros y recargar datos"""
        await self.load_pacientes_data()
    
    def update_paciente_form(self, field: str, value: str):
        """Actualizar campo del formulario de paciente"""
        self.paciente_form[field] = value
    
    # ==========================================
    # ✅ OPERACIONES CRUD PACIENTES - ACTUALIZADAS PARA CAMPOS SEPARADOS
    # ==========================================
    
    async def save_paciente(self):
        """✅ ACTUALIZADO: Guardar paciente con campos separados"""
        print("[DEBUG] ===== GUARDANDO PACIENTE CON CAMPOS SEPARADOS =====")
        self.set_loading(True)
        try:
            # ✅ VALIDACIONES ACTUALIZADAS
            if not self.paciente_form["primer_nombre"].strip():
                self.show_error("El primer nombre es requerido")
                return
            
            if not self.paciente_form["primer_apellido"].strip():
                self.show_error("El primer apellido es requerido")
                return
            
            if not self.paciente_form["numero_documento"].strip():
                self.show_error("El número de documento es requerido")
                return
            
            if self.selected_paciente:
                # ACTUALIZAR EXISTENTE
                await self._update_paciente()
            else:
                # CREAR NUEVO
                await self._create_paciente()
                
        except Exception as e:
            print(f"[ERROR] Error guardando paciente: {e}")
            self.show_error(f"Error guardando paciente: {str(e)}")
        finally:
            self.set_loading(False)
    
    async def _create_paciente(self):
        """✅ ACTUALIZADO: Crear nuevo paciente con campos separados"""
        print("[DEBUG] 🚀 Creando nuevo paciente con campos separados")
        
        try:
            user_id = self._get_current_user_id()
            print(f"[DEBUG] Usuario ID para registro: {user_id}")
            
            # Verificar que no exista el documento
            existing = pacientes_table.get_by_documento(self.paciente_form["numero_documento"])
            if existing:
                self.show_error("Ya existe un paciente con este número de documento")
                return
            
            # Procesar arrays
            alergias = [a.strip() for a in self.paciente_form["alergias"].split(",") if a.strip()] if self.paciente_form["alergias"] else []
            medicamentos = [m.strip() for m in self.paciente_form["medicamentos_actuales"].split(",") if m.strip()] if self.paciente_form["medicamentos_actuales"] else []
            condiciones = [c.strip() for c in self.paciente_form["condiciones_medicas"].split(",") if c.strip()] if self.paciente_form["condiciones_medicas"] else []
            antecedentes = [a.strip() for a in self.paciente_form["antecedentes_familiares"].split(",") if a.strip()] if self.paciente_form["antecedentes_familiares"] else []
            
            # Convertir fecha
            fecha_nacimiento = None
            if self.paciente_form["fecha_nacimiento"]:
                try:
                    fecha_nacimiento = datetime.datetime.strptime(self.paciente_form["fecha_nacimiento"], "%Y-%m-%d").date()
                except ValueError:
                    self.show_error("Formato de fecha inválido. Use YYYY-MM-DD")
                    return
            
            # ✅ CREAR PACIENTE CON CAMPOS SEPARADOS
            result = pacientes_table.create_patient_complete(
                # ✅ NOMBRES SEPARADOS
                primer_nombre=self.paciente_form["primer_nombre"].strip(),
                primer_apellido=self.paciente_form["primer_apellido"].strip(),
                segundo_nombre=self.paciente_form["segundo_nombre"].strip() if self.paciente_form["segundo_nombre"].strip() else None,
                segundo_apellido=self.paciente_form["segundo_apellido"].strip() if self.paciente_form["segundo_apellido"].strip() else None,
                
                # Documentación
                numero_documento=self.paciente_form["numero_documento"],
                registrado_por=user_id,
                tipo_documento=self.paciente_form["tipo_documento"],
                fecha_nacimiento=fecha_nacimiento,
                genero=self.paciente_form["genero"] if self.paciente_form["genero"] else None,
                
                # ✅ TELÉFONOS SEPARADOS
                telefono_1=self.paciente_form["telefono_1"] if self.paciente_form["telefono_1"] else None,
                telefono_2=self.paciente_form["telefono_2"] if self.paciente_form["telefono_2"] else None,
                
                # Contacto y ubicación
                email=self.paciente_form["email"] if self.paciente_form["email"] else None,
                direccion=self.paciente_form["direccion"] if self.paciente_form["direccion"] else None,
                ciudad=self.paciente_form["ciudad"] if self.paciente_form["ciudad"] else None,
                departamento=self.paciente_form["departamento"] if self.paciente_form["departamento"] else None,
                ocupacion=self.paciente_form["ocupacion"] if self.paciente_form["ocupacion"] else None,
                estado_civil=self.paciente_form["estado_civil"] if self.paciente_form["estado_civil"] else None,
                
                # Información médica
                alergias=alergias if alergias else None,
                medicamentos_actuales=medicamentos if medicamentos else None,
                condiciones_medicas=condiciones if condiciones else None,
                antecedentes_familiares=antecedentes if antecedentes else None,
                observaciones=self.paciente_form["observaciones"] if self.paciente_form["observaciones"] else None
            )
            
            if result:
                # ✅ CONSTRUIR NOMBRE COMPLETO PARA MENSAJE
                nombre_display = f"{self.paciente_form['primer_nombre']} {self.paciente_form['primer_apellido']}"
                self.show_success(f"✅ Paciente '{nombre_display}' creado exitosamente")
                self.close_paciente_modal()
                await self.load_pacientes_data()
            else:
                self.show_error("Error creando paciente")
            
        except Exception as e:
            print(f"[ERROR] Error en _create_paciente: {e}")
            error_msg = str(e)
            if "documento" in error_msg.lower():
                self.show_error("El número de documento ya está en uso")
            elif "email" in error_msg.lower():
                self.show_error("El email ya está en uso")
            else:
                self.show_error(f"Error creando paciente: {error_msg}")
    
    async def _update_paciente(self):
        """✅ ACTUALIZADO: Actualizar paciente con campos separados"""
        print("[DEBUG] Actualizando paciente con campos separados...")
        
        try:
            paciente_id = self.selected_paciente.get("id")
            
            if not paciente_id:
                self.show_error("Error: ID de paciente no encontrado")
                return
            
            # Verificar documento único (excluyendo el actual)
            existing = pacientes_table.get_by_documento(self.paciente_form["numero_documento"])
            if existing and existing.get("id") != paciente_id:
                self.show_error("Ya existe otro paciente con este número de documento")
                return
            
            # Procesar arrays
            alergias = [a.strip() for a in self.paciente_form["alergias"].split(",") if a.strip()] if self.paciente_form["alergias"] else []
            medicamentos = [m.strip() for m in self.paciente_form["medicamentos_actuales"].split(",") if m.strip()] if self.paciente_form["medicamentos_actuales"] else []
            condiciones = [c.strip() for c in self.paciente_form["condiciones_medicas"].split(",") if c.strip()] if self.paciente_form["condiciones_medicas"] else []
            antecedentes = [a.strip() for a in self.paciente_form["antecedentes_familiares"].split(",") if a.strip()] if self.paciente_form["antecedentes_familiares"] else []
            
            # Convertir fecha
            fecha_nacimiento = None
            if self.paciente_form["fecha_nacimiento"]:
                try:
                    fecha_nacimiento = datetime.datetime.strptime(self.paciente_form["fecha_nacimiento"], "%Y-%m-%d").date()
                except ValueError:
                    self.show_error("Formato de fecha inválido. Use YYYY-MM-DD")
                    return
            
            # ✅ PREPARAR DATOS CON CAMPOS SEPARADOS
            data = {
                # ✅ NOMBRES SEPARADOS
                "primer_nombre": self.paciente_form["primer_nombre"].strip(),
                "primer_apellido": self.paciente_form["primer_apellido"].strip(),
                "segundo_nombre": self.paciente_form["segundo_nombre"].strip() if self.paciente_form["segundo_nombre"].strip() else None,
                "segundo_apellido": self.paciente_form["segundo_apellido"].strip() if self.paciente_form["segundo_apellido"].strip() else None,
                
                # Documentación
                "numero_documento": self.paciente_form["numero_documento"],
                "tipo_documento": self.paciente_form["tipo_documento"],
                "genero": self.paciente_form["genero"] if self.paciente_form["genero"] else None,
                
                # ✅ TELÉFONOS SEPARADOS
                "telefono_1": self.paciente_form["telefono_1"] if self.paciente_form["telefono_1"] else None,
                "telefono_2": self.paciente_form["telefono_2"] if self.paciente_form["telefono_2"] else None,
                
                # Contacto y ubicación
                "email": self.paciente_form["email"] if self.paciente_form["email"] else None,
                "direccion": self.paciente_form["direccion"] if self.paciente_form["direccion"] else None,
                "ciudad": self.paciente_form["ciudad"] if self.paciente_form["ciudad"] else None,
                "departamento": self.paciente_form["departamento"] if self.paciente_form["departamento"] else None,
                "ocupacion": self.paciente_form["ocupacion"] if self.paciente_form["ocupacion"] else None,
                "estado_civil": self.paciente_form["estado_civil"] if self.paciente_form["estado_civil"] else None,
                
                # Información médica
                "alergias": alergias if alergias else None,
                "medicamentos_actuales": medicamentos if medicamentos else None,
                "condiciones_medicas": condiciones if condiciones else None,
                "antecedentes_familiares": antecedentes if antecedentes else None,
                "observaciones": self.paciente_form["observaciones"] if self.paciente_form["observaciones"] else None
            }
            
            if fecha_nacimiento:
                data["fecha_nacimiento"] = fecha_nacimiento.isoformat()
            
            # Actualizar
            updated_paciente = pacientes_table.update(paciente_id, data)
            
            if updated_paciente:
                # ✅ CONSTRUIR NOMBRE COMPLETO PARA MENSAJE
                nombre_display = f"{self.paciente_form['primer_nombre']} {self.paciente_form['primer_apellido']}"
                self.show_success(f"Paciente {nombre_display} actualizado exitosamente")
                await self.load_pacientes_data()
                self.close_paciente_modal()
            else:
                self.show_error("Error actualizando paciente")
            
        except Exception as e:
            print(f"[ERROR] Error en _update_paciente: {e}")
            self.show_error(f"Error actualizando paciente: {str(e)}")
    
    async def delete_paciente(self):
        """Eliminar (desactivar) paciente"""
        print("[DEBUG] Desactivando paciente...")
        self.set_loading(True)
        
        try:
            if not self.paciente_to_delete:
                self.show_error("No hay paciente seleccionado para eliminar")
                return
            
            paciente_id = self.paciente_to_delete.get("id")
            print(f"[DEBUG] Desactivando paciente_id: {paciente_id}")
            
            # TODO: Verificar que no tenga consultas activas
            
            # Desactivar paciente
            result = pacientes_table.deactivate_patient(
                paciente_id, 
                f"Desactivado desde dashboard por {self._get_current_user_name()}"
            )
            
            if result:
                nombre = self.paciente_to_delete.get("nombre_completo", "")
                self.show_success(f"Paciente {nombre} desactivado exitosamente")
                await self.load_pacientes_data()
                self.close_delete_confirmation()
            else:
                self.show_error("Error desactivando paciente")
            
        except Exception as e:
            print(f"[ERROR] Error eliminando paciente: {e}")
            self.show_error(f"Error eliminando paciente: {str(e)}")
        finally:
            self.set_loading(False)
    
    async def reactivate_paciente(self, paciente_data: PacienteModel):
        """Reactivar paciente"""
        print("[DEBUG] Reactivando paciente...")
        self.set_loading(True)
        
        try:
            result = pacientes_table.reactivate_patient(paciente_data.id)
            
            if result:
                self.show_success(f"Paciente {paciente_data.nombre_completo} reactivado exitosamente")
                await self.load_pacientes_data()
            else:
                self.show_error("Error reactivando paciente")
            
        except Exception as e:
            print(f"[ERROR] Error reactivando paciente: {e}")
            self.show_error(f"Error reactivando paciente: {str(e)}")
        finally:
            self.set_loading(False)
    
    # ==========================================
    #  GESTIÓN DE MODALES CONSULTA
    # ==========================================

    def open_consulta_modal(self, consulta_data: ConsultaModel = None):
        """Abrir modal de consulta"""
        if consulta_data:
            # Editar consulta existente
            self.selected_consulta = {
                "id": consulta_data.id,
                "numero_consulta": consulta_data.numero_consulta
            }
            
            self.consulta_form = {
                "paciente_id": consulta_data.paciente_id,
                "odontologo_id": consulta_data.odontologo_id,
                "motivo_consulta": consulta_data.motivo_consulta or "",
                "observaciones_cita": consulta_data.observaciones_cita or "",
                "notas_internas": "",  # No mostramos notas internas en edición
                "tipo_consulta": consulta_data.tipo_consulta,
                "prioridad": consulta_data.prioridad
            }
        else:
            # Nueva consulta
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
    # ✅ OPERACIONES CRUD CONSULTAS - CORREGIDAS
    # ==========================================
    
    async def save_consulta(self):
        """✅ CORREGIDO: Guardar consulta (crear o actualizar)"""
        print("[DEBUG] ===== GUARDANDO CONSULTA - CORREGIDO =====")
        self.set_loading(True)
        
        try:
            # Validaciones básicas
            if not self.consulta_form["paciente_id"]:
                self.show_error("Debe seleccionar un paciente")
                return
            
            if not self.consulta_form["odontologo_id"]:
                self.show_error("Debe seleccionar un odontólogo")
                return
            
            if self.selected_consulta:
                # ACTUALIZAR EXISTENTE
                await self._update_consulta()
            else:
                # CREAR NUEVA
                await self._create_consulta()
                
        except Exception as e:
            print(f"[ERROR] Error guardando consulta: {e}")
            import traceback
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            self.show_error(f"Error guardando consulta: {str(e)}")
        finally:
            self.set_loading(False)

    async def _create_consulta(self):
        """✅ CORREGIDO: Crear nueva consulta"""
        print("[DEBUG] 🚀 Creando nueva consulta por orden de llegada - CORREGIDO")
        
        try:
            from datetime import datetime
            user_id = self._get_current_user_id()
            
            # Crear consulta con fecha/hora actual
            result = consultas_table.create_consultation(
                paciente_id=self.consulta_form["paciente_id"],
                odontologo_id=self.consulta_form["odontologo_id"],
                fecha_programada=datetime.now(),  # Fecha/hora actual
                tipo_consulta=self.consulta_form["tipo_consulta"],
                motivo_consulta=self.consulta_form["motivo_consulta"] if self.consulta_form["motivo_consulta"] else None,
                observaciones_cita=self.consulta_form["observaciones_cita"] if self.consulta_form["observaciones_cita"] else None,
                programada_por=user_id
            )
            
            if result:
                self.show_success("✅ Consulta creada exitosamente")
                self.close_consulta_modal()
                await self.load_consultas_data()
            else:
                self.show_error("Error creando consulta")
            
        except Exception as e:
            print(f"[ERROR] Error en _create_consulta: {e}")
            import traceback
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            self.show_error(f"Error creando consulta: {str(e)}")

    async def _update_consulta(self):
        """✅ CORREGIDO: Actualizar consulta existente"""
        print("[DEBUG] Actualizando consulta - CORREGIDO...")
        
        try:
            consulta_id = self.selected_consulta.get("id")
            
            if not consulta_id:
                self.show_error("Error: ID de consulta no encontrado")
                return
            
            # Preparar datos de actualización
            data = {
                "motivo_consulta": self.consulta_form["motivo_consulta"] if self.consulta_form["motivo_consulta"] else None,
                "observaciones_cita": self.consulta_form["observaciones_cita"] if self.consulta_form["observaciones_cita"] else None,
                "tipo_consulta": self.consulta_form["tipo_consulta"],
                "prioridad": self.consulta_form["prioridad"]
            }
            
            # Solo permitir cambiar odontólogo si está en estado programada
            current_consulta = consultas_table.get_by_id(consulta_id)
            if current_consulta and current_consulta.get("estado") == "programada":
                if self.consulta_form["odontologo_id"] != current_consulta.get("odontologo_id"):
                    data["odontologo_id"] = self.consulta_form["odontologo_id"]
            
            updated_consulta = consultas_table.update(consulta_id, data)
            
            if updated_consulta:
                self.show_success("Consulta actualizada exitosamente")
                await self.load_consultas_data()
                self.close_consulta_modal()
            else:
                self.show_error("Error actualizando consulta")
            
        except Exception as e:
            print(f"[ERROR] Error en _update_consulta: {e}")
            import traceback
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            self.show_error(f"Error actualizando consulta: {str(e)}")

    async def change_consulta_status(self, consulta_id: str, nuevo_estado: str, consulta_data: ConsultaModel = None):
        """✅ CORREGIDO: Cambiar estado de una consulta"""
        print(f"[DEBUG] Cambiando estado de consulta {consulta_id} a {nuevo_estado} - CORREGIDO")
        self.set_loading(True)
        
        try:
            # Validar transiciones de estado permitidas
            if consulta_data:
                estado_actual = consulta_data.estado
                if not self._is_valid_status_transition(estado_actual, nuevo_estado):
                    self.show_error(f"No se puede cambiar de {estado_actual} a {nuevo_estado}")
                    return
            
            # Actualizar estado
            result = consultas_table.update_status(consulta_id, nuevo_estado)
            
            if result:
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
            else:
                self.show_error("Error cambiando estado de consulta")
            
        except Exception as e:
            print(f"[ERROR] Error cambiando estado: {e}")
            import traceback
            print(f"[ERROR] Traceback: {traceback.format_exc()}")
            self.show_error(f"Error cambiando estado: {str(e)}")
        finally:
            self.set_loading(False)

    def _is_valid_status_transition(self, estado_actual: str, nuevo_estado: str) -> bool:
        """Validar si la transición de estado es válida"""
        valid_transitions = {
            "programada": ["confirmada", "en_progreso", "cancelada", "no_asistio"],
            "confirmada": ["en_progreso", "cancelada", "no_asistio"],
            "en_progreso": ["completada", "cancelada"],
            "completada": [],  # Estado final
            "cancelada": ["programada"],  # Puede reprogramarse
            "no_asistio": ["programada"]  # Puede reprogramarse
        }
        
        return nuevo_estado in valid_transitions.get(estado_actual, [])

    async def cancel_consulta(self, consulta_id: str, motivo: str = ""):
        """Cancelar consulta con motivo"""
        await self.change_consulta_status(consulta_id, "cancelada")

    # ==========================================
    # ✅ FILTROS DE CONSULTAS - ACTUALIZADOS
    # ==========================================
    
    def set_consultas_search(self, search_term: str):
        """Establecer término de búsqueda de consultas"""
        self.consultas_search = search_term

    def set_consultas_filter_estado(self, estado: str):
        """Establecer filtro por estado de consultas"""
        self.consultas_filter_estado = estado

    def set_consultas_filter_odontologo(self, odontologo_id: str):
        """Establecer filtro por odontólogo"""
        self.consultas_filter_odontologo = odontologo_id

    # ==========================================
    # MÉTODOS AUXILIARES
    # ==========================================
    
    def _get_current_user_id(self) -> str:
        """Obtener ID del usuario actual de forma segura"""
        if self.user_profile and isinstance(self.user_profile, dict):
            return self.user_profile.get("id", "")
        return ""
    
    def _get_current_user_name(self) -> str:
        """Obtener nombre del usuario actual de forma segura"""
        if self.user_profile and isinstance(self.user_profile, dict):
            return self.user_profile.get("nombre_completo", "Admin")
        return "Admin"
    
    async def _get_admin_dashboard_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas del dashboard del administrador"""
        try:
            return {
                "total_pacientes": self.pacientes_stats.total,
                "nuevos_pacientes_mes": self.pacientes_stats.nuevos_mes,
                "consultas_hoy": len(self.consultas_hoy),
                "pagos_pendientes": 0,  # TODO: Implementar cuando se carguen pagos
                "pacientes_activos": self.pacientes_stats.activos,
                "pacientes_hombres": self.pacientes_stats.hombres,
                "pacientes_mujeres": self.pacientes_stats.mujeres
            }
            
        except Exception as e:
            print(f"[ERROR] Error obteniendo estadísticas admin: {e}")
            return {
                "total_pacientes": 0,
                "nuevos_pacientes_mes": 0,
                "consultas_hoy": 0,
                "pagos_pendientes": 0,
                "pacientes_activos": 0,
                "pacientes_hombres": 0,
                "pacientes_mujeres": 0
            }
    
    def get_odontologo_name_by_id(self, odontologo_id: str) -> str:
        """✅ CORREGIDO: Obtener nombre del odontólogo por ID"""
        for odontologo in self.odontologos_list:
            if odontologo['id'] == odontologo_id:
                return odontologo['nombre_completo']
        return "Odontólogo no encontrado"

    def get_paciente_name_by_id(self, paciente_id: str) -> str:
        """✅ CORREGIDO: Obtener nombre del paciente por ID"""
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
    # ✅ PROPIEDADES COMPUTADAS - CORREGIDAS
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
    def consultas_hoy_count(self) -> int:
        return len(self.consultas_hoy)
    
    @rx.var
    def pagos_pendientes_count(self) -> int:
        return len([p for p in self.pagos_list if p.estado_pago == "pendiente"])
    
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
        """✅ CORREGIDO: Lista de consultas filtrada"""
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

    # ==========================================
    # INICIALIZACIÓN
    # ==========================================
    
    def on_load(self):
        """Cargar datos iniciales"""
        print("[DEBUG] Inicializando AdminState con campos separados...")
        return self.load_dashboard_data()