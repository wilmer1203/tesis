"""
Estado específico para el rol de Gerente/Jefe - VERSIÓN CORREGIDA CON CRUD COMPLETO
Corrigida la gestión de personal para usar Supabase Auth correctamente
"""

import reflex as rx
import datetime
from datetime import date
import random
from typing import List, Dict, Any, Optional, Union
from .base import BaseState
from dental_system.supabase.client import supabase_client

from dental_system.supabase.tablas import personal_table, users_table, services_table
from dental_system.models import (
PersonalModel,
ServicioModel,
DashboardStatsModel,
PacientesStatsModel,
PagosStatsModel,
PacienteModel,
)

class BossState(BaseState):
"""Estado específico para el gerente/jefe del sistema odontológico"""

    # ==========================================
    # NAVEGACIÓN Y UI
    # ==========================================
    current_page: str = "dashboard"
    sidebar_collapsed: bool = False

    # ==========================================
    # DATOS DEL DASHBOARD - TIPADOS
    # ==========================================
    dashboard_stats: DashboardStatsModel = DashboardStatsModel()

    # ==========================================
    # GESTIÓN DE PERSONAL - TIPADO
    # ==========================================
    personal_list: List[PersonalModel] = []
    selected_personal: Dict = {}
    show_personal_modal: bool = False
    personal_form: Dict[str, str] = {
    # Nombres separados
    "primer_nombre": "",
    "segundo_nombre": "",
    "primer_apellido": "",
    "segundo_apellido": "",

    # Resto de campos
    "email": "",
    "telefono": "",
    "tipo_personal": "",
    "especialidad": "",
    "numero_licencia": "",
    "numero_documento": "",
    "celular": "",
    "direccion": "",
    "salario": "",
    "password": ""  # Solo para creación

}

    # Estado para confirmación de eliminación
    show_delete_confirmation: bool = False
    personal_to_delete: dict[str, dict[str, str]] = {}

    # Filtros y búsqueda
    personal_search: str = ""
    personal_filter_tipo: str = ""
    personal_filter_estado: str = ""

    # ==========================================
    # GESTIÓN DE SERVICIOS - TIPADO
    # ==========================================
    servicios_list: List[ServicioModel] = []
    selected_servicio: Dict = {}
    show_servicio_modal: bool = False
    servicio_form: Dict[str, str] = {
        "codigo": "",
        "nombre": "",
        "descripcion": "",
        "categoria": "",
        "subcategoria": "",
        "duracion_estimada": "30",
        "precio_base": "",
        "precio_minimo": "",
        "precio_maximo": ""
    }

    # ==========================================
    # VISTA DE PACIENTES - TIPADO
    # ==========================================
    pacientes_list: List[Dict] = []
    pacientes_stats: PacientesStatsModel = PacientesStatsModel()

    # ==========================================
    # VISTA DE CONSULTAS
    # ==========================================
    consultas_list: List[Dict] = []
    consultas_hoy: List[Dict] = []

    # ==========================================
    # VISTA DE PAGOS - TIPADO
    # ==========================================
    pagos_list: List[Dict] = []
    pagos_stats: PagosStatsModel = PagosStatsModel()


    # ==========================================
    # VISTA DE Graficos - resumen del mes
    # ==========================================
    area_toggle: bool = True
    selected_tab: str = "Pacientes"
    timeframe: str = "Mensual"
    pacientes_data = []
    ingresos_data = []
    citas_data = []

    def toggle_areachart(self):
        """Alterna entre gráfico de área y barras."""
        self.area_toggle = not self.area_toggle

    def set_selected_tab(self, selected_tab: Union[str, List[str]]):
        """Cambia la pestaña seleccionada."""
        # Siempre manejarlo como un string
        if isinstance(selected_tab, list):
            self.selected_tab = selected_tab[0]# Si por alguna razón llega como lista, tomar el primer elemento
        else:
            self.selected_tab = selected_tab

    @rx.var(cache=False)
    def get_current_data(self) -> list:
        match self.selected_tab:
            case "Pacientes":
                return self.pacientes_data
            case "Ingresos":
                return self.ingresos_data
            case "Citas":
                return self.citas_data
        return []

    #estos datos los tengo que sacaar de la base de datos por lo menos los 30 ultimos dias

    def randomize_data(self):
        if self.pacientes_data:
            return

        for i in range(30, -1, -1):
            self.ingresos_data.append({
                "name": (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%d-%m"),
                "Ingresos": random.randint(1000, 5000)  # Clave unificada
            })

        for i in range(30, -1, -1):
            self.citas_data.append({
                "name": (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%d-%m"),
                "Citas": random.randint(10, 50)  # Clave unificada
            })

        for i in range(30, -1, -1):
            self.pacientes_data.append({
                "name": (datetime.datetime.now() - datetime.timedelta(days=i)).strftime("%d-%m"),
                "Pacientes": random.randint(5, 20)  # Clave unificada
            })


    # ==========================================
    # MÉTODOS DE NAVEGACIÓN
    # ==========================================

    @rx.event
    async def navigate_to(self, page: str):
        print(f"[DEBUG] Navegando a página: {page}")
        self.current_page = page
        self.clear_global_message()

        if page == "dashboard":
            await self.load_dashboard_data()
        elif page == "personal":
            await self.load_personal_data()
        elif page == "servicios":
            await self.load_servicios_data()
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
    # MÉTODOS DE CARGA DE DATOS - ACTUALIZADOS
    # ==========================================
    async def load_dashboard_data(self):
        """Cargar datos principales del dashboard"""
        print("[DEBUG] Cargando datos del dashboard...")
        self.set_loading(True)
        try:
            # Obtener estadísticas reales de Supabase
            stats_dict = await self._get_dashboard_stats_real()
            self.dashboard_stats = DashboardStatsModel(**stats_dict)
            self.randomize_data()
            print(f"[DEBUG] Estadísticas cargadas: {stats_dict}")

        except Exception as e:
            print(f"[ERROR] Error cargando dashboard: {e}")
            self.show_error(f"Error cargando datos del dashboard: {str(e)}")
        finally:
            self.set_loading(False)

    async def load_personal_data(self):
        """Cargar datos del personal"""
        print("[DEBUG] Cargando datos del personal")
        self.set_loading(True)

        try:

            personal_data = personal_table.get_filtered_personal(
                tipo_personal=self.personal_filter_tipo if self.personal_filter_tipo != "todos" else None,
                estado_laboral=self.personal_filter_estado if self.personal_filter_estado != "todos" else None,
                solo_activos=True,
                busqueda=self.personal_search if self.personal_search else None
            )

            print(f"[DEBUG] ✅ Personal obtenido: {len(personal_data)} registros")

            # Convertir datos a modelos
            self.personal_list = []
            for item in personal_data:
                try:
                    model = PersonalModel.from_dict(item)
                    self.personal_list.append(model)
                except Exception as e:
                    print(f"[WARNING] Error convirtiendo registro: {e}")
                    print(f"[DEBUG] Datos problemáticos: {item}")

            print(f"[DEBUG] ✅ Personal convertido a modelos: {len(self.personal_list)} registros")

        except Exception as e:
            print(f"[ERROR] Error cargando personal: {e}")
            self.show_error(f"Error cargando personal: {str(e)}")

            # Fallback simple
            try:
                print("[DEBUG] Intentando fallback con vista directa...")
                personal_data = personal_table.get_all_from_view({
                    'completamente_activo': True
                })

                self.personal_list = []
                for item in personal_data:
                    try:
                        model = PersonalModel.from_dict(item)
                        self.personal_list.append(model)
                    except Exception as e:
                        print(f"[WARNING] Error en fallback: {e}")

                print(f"[DEBUG] ✅ Fallback exitoso: {len(self.personal_list)} registros")

            except Exception as ve:
                print(f"[ERROR] Error en fallback: {ve}")
                self.personal_list = []
                self.show_error("Error crítico cargando personal")

        finally:
            self.set_loading(False)

    async def load_servicios_data(self):
        """Cargar datos de servicios """
        print("[DEBUG] Cargando datos de servicios con ServicesTable...")
        self.set_loading(True)
        try:
            # Usar ServicesTable en lugar de consulta directa
            servicios_data = services_table.get_all(filters={"activo": True})

            # Convertir datos a modelos tipados
            self.servicios_list = [ServicioModel.from_dict(item) for item in servicios_data]

            print(f"[DEBUG] Servicios cargados con ServicesTable: {len(self.servicios_list)} registros")

        except Exception as e:
            print(f"[ERROR] Error cargando servicios: {e}")
            self.show_error(f"Error cargando servicios: {str(e)}")
            # Datos de respaldo para desarrollo
            backup_data = {
                "id": "1",
                "codigo": "CONS001",
                "nombre": "Consulta General",
                "categoria": "Consulta",
                "precio_base": 50000,
                "duracion_estimada": "30 minutes",
                "activo": True
            }
            self.servicios_list = [ServicioModel.from_dict(backup_data)]
        finally:
            self.set_loading(False)

    # [RESTO DE MÉTODOS DE CARGA SIN CAMBIOS]
    async def load_pacientes_data(self):
        """✅ ACTUALIZADO: Cargar datos de pacientes con campos separados"""
        print("[DEBUG] Cargando datos de pacientes para vista de jefe...")
        self.set_loading(True)
        try:
            # Estadísticas de pacientes usando la tabla actualizada
            total_response = supabase_client.get_client().table('pacientes').select('id', count='exact').eq('activo', True).execute()

            # Pacientes nuevos este mes
            current_month = datetime.datetime.now().strftime('%Y-%m')
            nuevos_response = supabase_client.get_client().table('pacientes').select('id', count='exact').gte('fecha_registro', f"{current_month}-01").execute()

            # ✅ ESTADÍSTICAS POR GÉNERO USANDO CAMPOS ACTUALIZADOS
            hombres_response = supabase_client.get_client().table('pacientes').select('id', count='exact').eq('genero', 'masculino').eq('activo', True).execute()
            mujeres_response = supabase_client.get_client().table('pacientes').select('id', count='exact').eq('genero', 'femenino').eq('activo', True).execute()

            stats_dict = {
                "total": total_response.count or 0,
                "nuevos_mes": nuevos_response.count or 0,
                "activos": total_response.count or 0,
                "hombres": hombres_response.count or 0,
                "mujeres": mujeres_response.count or 0
            }

            self.pacientes_stats = PacientesStatsModel(**stats_dict)

            print(f"[DEBUG] Estadísticas de pacientes para jefe: {stats_dict}")

        except Exception as e:
            print(f"[ERROR] Error cargando pacientes para jefe: {e}")
            self.show_error(f"Error cargando pacientes: {str(e)}")
            self.pacientes_stats = PacientesStatsModel()
        finally:
            self.set_loading(False)

    async def load_consultas_data(self):
        """Cargar datos de consultas"""
        print("[DEBUG] Cargando datos de consultas...")
        self.set_loading(True)
        try:
            # Consultas de hoy
            today = datetime.date.today().isoformat()
            response = supabase_client.get_client().table('consultas').select('''
                *,
                pacientes:paciente_id (nombre_completo),
                personal:odontologo_id (
                    usuarios:usuario_id (nombre_completo)
                )
            ''').gte('fecha_programada', today).lt('fecha_programada', f"{today}T23:59:59").execute()

            self.consultas_hoy = response.data if response.data else []
            print(f"[DEBUG] Consultas de hoy: {len(self.consultas_hoy)} registros")

        except Exception as e:
            print(f"[ERROR] Error cargando consultas: {e}")
            self.show_error(f"Error cargando consultas: {str(e)}")
            self.consultas_hoy = []
        finally:
            self.set_loading(False)

    async def load_pagos_data(self):
        """Cargar datos de pagos - ACTUALIZADO CON MODELOS"""
        print("[DEBUG] Cargando datos de pagos...")
        self.set_loading(True)
        try:
            # Estadísticas de pagos del mes
            current_month = datetime.datetime.now().strftime('%Y-%m')

            # Total del mes
            pagos_mes = supabase_client.get_client().table('pagos').select('monto_pagado').gte('fecha_pago', f"{current_month}-01").eq('estado_pago', 'completado').execute()
            total_mes = sum([pago['monto_pagado'] for pago in pagos_mes.data]) if pagos_mes.data else 0

            # Pendientes
            pendientes = supabase_client.get_client().table('pagos').select('monto_total', 'monto_pagado').eq('estado_pago', 'pendiente').execute()
            total_pendientes = sum([pago['monto_total'] - pago['monto_pagado'] for pago in pendientes.data]) if pendientes.data else 0

            stats_dict = {
                "total_mes": total_mes,
                "pendientes": total_pendientes,
                "completados": total_mes
            }

            self.pagos_stats = PagosStatsModel(**stats_dict)

            print(f"[DEBUG] Estadísticas de pagos: {stats_dict}")

        except Exception as e:
            print(f"[ERROR] Error cargando pagos: {e}")
            self.show_error(f"Error cargando pagos: {str(e)}")
            self.pagos_stats = PagosStatsModel()
        finally:
            self.set_loading(False)

    # ==========================================
    # GESTIÓN DE MODALES Y FILTROS
    # ==========================================
    def open_personal_modal(self, personal_data: Dict = None):
        """Abrir modal de personal - CORREGIDO PARA CAMPOS SEPARADOS"""
        if personal_data:
            self.selected_personal = personal_data
            usuarios_data = personal_data.get("usuarios", {})

            # USAR CAMPOS SEPARADOS (NO nombre_completo)
            self.personal_form = {
                "primer_nombre": personal_data.get("primer_nombre", ""),
                "segundo_nombre": personal_data.get("segundo_nombre", ""),
                "primer_apellido": personal_data.get("primer_apellido", ""),
                "segundo_apellido": personal_data.get("segundo_apellido", ""),
                "email": usuarios_data.get("email", ""),
                "telefono": usuarios_data.get("telefono", ""),
                "tipo_personal": personal_data.get("tipo_personal", ""),
                "especialidad": personal_data.get("especialidad", ""),
                "numero_licencia": personal_data.get("numero_licencia", ""),
                "numero_documento": personal_data.get("numero_documento", ""),
                "celular": personal_data.get("celular", ""),
                "direccion": personal_data.get("direccion", ""),
                "salario": str(personal_data.get("salario", "")),
                "password": ""  # Nunca mostrar password
            }
        else:
            self.selected_personal = {}
            self.personal_form = {
                "primer_nombre": "",
                "segundo_nombre": "",
                "primer_apellido": "",
                "segundo_apellido": "",
                "email": "",
                "telefono": "",
                "tipo_personal": "",
                "especialidad": "",
                "numero_licencia": "",
                "numero_documento": "",
                "celular": "",
                "direccion": "",
                "salario": "",
                "password": ""
            }
        self.show_personal_modal = True

    def close_personal_modal(self):
        """Cerrar modal de personal"""
        self.show_personal_modal = False
        self.selected_personal = {}
        self.clear_global_message()

    def open_delete_confirmation(self, personal_data: Dict):
        """Abrir confirmación de eliminación"""
        self.personal_to_delete = personal_data
        self.show_delete_confirmation = True

    def close_delete_confirmation(self):
        """Cerrar confirmación de eliminación"""
        self.show_delete_confirmation = False
        self.personal_to_delete = {}

    def set_personal_search(self, search_term: str):
        """Establecer término de búsqueda"""
        self.personal_search = search_term

    def set_personal_filter_tipo(self, tipo: str):
        """Establecer filtro por tipo de personal"""
        self.personal_filter_tipo = tipo

    def set_personal_filter_estado(self, estado: str):
        """Establecer filtro por estado laboral"""
        self.personal_filter_estado = estado

    @rx.event
    async def apply_personal_filters(self):
        """Aplicar filtros y recargar datos"""
        await self.load_personal_data()

    def open_servicio_modal(self, servicio_data: Dict = None):
        """Abrir modal de servicio"""
        if servicio_data:
            self.selected_servicio = servicio_data
            self.servicio_form = {
                "codigo": servicio_data.get("codigo", ""),
                "nombre": servicio_data.get("nombre", ""),
                "descripcion": servicio_data.get("descripcion", ""),
                "categoria": servicio_data.get("categoria", ""),
                "subcategoria": servicio_data.get("subcategoria", ""),
                "duracion_estimada": str(servicio_data.get("duracion_estimada", "30")).replace(" minutes", ""),
                "precio_base": str(servicio_data.get("precio_base", "")),
                "precio_minimo": str(servicio_data.get("precio_minimo", "")),
                "precio_maximo": str(servicio_data.get("precio_maximo", ""))
            }
        else:
            self.selected_servicio = {}
            self.servicio_form = {
                "codigo": "",
                "nombre": "",
                "descripcion": "",
                "categoria": "",
                "subcategoria": "",
                "duracion_estimada": "30",
                "precio_base": "",
                "precio_minimo": "",
                "precio_maximo": ""
            }
        self.show_servicio_modal = True

    def close_servicio_modal(self):
        """Cerrar modal de servicio"""
        self.show_servicio_modal = False
        self.selected_servicio = {}
        self.clear_global_message()

    # ==========================================
    # HANDLERS DE FORMULARIOS
    # ==========================================
    def update_personal_form(self, field: str, value: str):
        """Actualizar campo del formulario de personal"""
        self.personal_form[field] = value

    def update_servicio_form(self, field: str, value: str):
        """Actualizar campo del formulario de servicio"""
        self.servicio_form[field] = value

    # ==========================================
    # OPERACIONES CRUD PERSONAL - CORREGIDO
    # ==========================================


    async def save_personal(self):
            """Guardar personal (crear o actualizar) - REFACTORIZADO"""
            print("[DEBUG] ===== GUARDANDO PERSONAL CON TABLAS SEPARADAS =====")
            self.set_loading(True)
            try:
                # Validaciones BÁSICAS del formulario (las complejas las maneja users_table)
                if not self.personal_form["primer_nombre"].strip():
                    self.show_error("El primer nombre es requerido")
                    return

                if not self.personal_form["primer_apellido"].strip():
                    self.show_error("El primer apellido es requerido")
                    return

                if not self.personal_form["email"]:
                    self.show_error("El email es requerido")
                    return

                if not self.personal_form["tipo_personal"]:
                    self.show_error("El tipo de personal es requerido")
                    return

                if self.selected_personal:
                    # ACTUALIZAR EXISTENTE
                    await self._update_personal_simplified()
                else:
                    # CREAR NUEVO - USAR TABLAS SEPARADAS
                    await self._create_personal()

            except Exception as e:
                print(f"[ERROR] Error guardando personal: {e}")
                self.show_error(f"Error guardando personal: {str(e)}")
            finally:
                self.set_loading(False)


    """
    MÉTODOS CREACIÓN DE USUARIOS CON SUPABASE AUTH

    """


    async def _create_personal(self):
        """Crear nuevo personal usando Supabase Auth - VERSIÓN FINAL CORREGIDA"""
        print("[DEBUG] 🚀 ===== CREANDO PERSONAL  =====")

        try:
            # 1. USAR users_table PARA CREAR USUARIO + AUTH
            primer_nombre = self.personal_form["primer_nombre"].strip()
            primer_apellido = self.personal_form["primer_apellido"].strip()

            print(f"[DEBUG] Creando usuario para: {primer_nombre} {primer_apellido}")

            # Llamar a la función que YA SABEMOS que funciona
            user_result = users_table.crear_usuario(
                email=self.personal_form["email"].strip().lower(),
                password=self.personal_form["password"].strip(),
                rol=self.personal_form["tipo_personal"].strip(),
                telefono=self.personal_form.get("celular", ""),
                nombre=primer_nombre,
                apellido=primer_apellido
            )

            if not user_result or not user_result.get('success'):
                raise Exception("Error creando usuario en el sistema")

            usuario_id = user_result['user_id']
            print(f"[DEBUG] ✅ Usuario creado: {usuario_id}")

            # 2. USAR personal_table PARA CREAR REGISTRO DE PERSONAL
            print("[DEBUG] 👥 Creando registro de personal...")

            personal_result = personal_table.create_staff_complete(
                usuario_id=usuario_id,
                primer_nombre=primer_nombre,
                primer_apellido=primer_apellido,
                numero_documento=self.personal_form["numero_documento"],
                celular=self.personal_form.get("celular", "0000000000"),
                tipo_personal=self.personal_form["tipo_personal"],
                segundo_nombre=self.personal_form.get("segundo_nombre", "").strip() or None,
                segundo_apellido=self.personal_form.get("segundo_apellido", "").strip() or None,
                direccion=self.personal_form.get("direccion", "").strip() or None,
                especialidad=self.personal_form.get("especialidad", "").strip() or None,
                numero_licencia=self.personal_form.get("numero_licencia", "").strip() or None,
                salario=float(self.personal_form["salario"]) if self.personal_form.get("salario") else None
            )

            if not personal_result:
                # Si falla personal, limpiar usuario creado
                print("[DEBUG] ❌ Error creando personal, limpiando usuario...")
                try:
                    users_table.delete(usuario_id)
                except:
                    pass
                raise Exception("Error creando registro de personal")

            print(f"[DEBUG] ✅ Personal creado: {personal_result['id']}")

            # 3. ÉXITO COMPLETO
            nombre_display = f"{primer_nombre} {primer_apellido}"
            self.show_success(f"✅ Personal '{nombre_display}' creado exitosamente")

            self.close_personal_modal()
            # Recargar datos y cerrar modal
            await self.load_personal_data()


        except Exception as e:
            print(f"[ERROR] ❌ Error en create_personal: {e}")
            error_msg = str(e)

            # Mensajes más específicos
            if "already_registered" in error_msg or "ya está registrado" in error_msg:
                self.show_error("El email ya está en uso por otro usuario")
            elif "contraseña" in error_msg.lower() or "password" in error_msg.lower():
                self.show_error("Error con la contraseña: debe tener al menos 8 caracteres")
            elif "documento" in error_msg.lower():
                self.show_error("El número de documento ya está en uso")
            else:
                self.show_error(f"Error creando personal: {error_msg}")


    async def _update_personal_simplified(self):
        """Actualizar personal existente - VERSIÓN SIMPLIFICADA USANDO TABLAS"""
        print("[DEBUG] Actualizando personal con tablas separadas...")

        try:
            personal_id = self.selected_personal.get("id")
            usuario_id = self.selected_personal.get("usuarios", {}).get("id")

            if not personal_id or not usuario_id:
                self.show_error("Error: Datos de personal incompletos")
                return

            # 1. ACTUALIZAR TABLA USUARIOS usando users_table
            primer_nombre = self.personal_form["primer_nombre"].strip()
            segundo_nombre = self.personal_form.get("segundo_nombre", "").strip() or None
            primer_apellido = self.personal_form["primer_apellido"].strip()
            segundo_apellido = self.personal_form.get("segundo_apellido", "").strip() or None

            # Construir nombre completo
            nombres = [primer_nombre]
            if segundo_nombre:
                nombres.append(segundo_nombre)
            nombres.append(primer_apellido)
            if segundo_apellido:
                nombres.append(segundo_apellido)

            nombre_completo = " ".join(nombres)

            usuario_data = {
                "telefono": self.personal_form.get("telefono", "")
            }

            # Verificar cambio de email
            current_email = self.selected_personal.get("usuarios", {}).get("email", "")
            new_email = self.personal_form["email"]

            if new_email != current_email:
                existing_user = users_table.get_by_email(new_email)
                if existing_user and existing_user.get("id") != usuario_id:
                    self.show_error("El nuevo email ya está en uso por otro usuario")
                    return
                usuario_data["email"] = new_email

            usuario_updated = users_table.update(usuario_id, usuario_data)

            if not usuario_updated:
                self.show_error("Error actualizando datos del usuario")
                return

            # 2. ACTUALIZAR TABLA PERSONAL usando personal_table
            personal_data = {
                "primer_nombre": primer_nombre,
                "primer_apellido": primer_apellido,
                "numero_documento": self.personal_form["numero_documento"],
                "celular": self.personal_form.get("celular", ""),
                "direccion": self.personal_form.get("direccion", ""),
                "tipo_personal": self.personal_form["tipo_personal"],
                "especialidad": self.personal_form.get("especialidad", ""),
                "numero_licencia": self.personal_form.get("numero_licencia", "")
            }

            # Campos opcionales
            if segundo_nombre:
                personal_data["segundo_nombre"] = segundo_nombre
            if segundo_apellido:
                personal_data["segundo_apellido"] = segundo_apellido

            # Salario
            salario_str = self.personal_form.get("salario", "")
            if salario_str:
                try:
                    personal_data["salario"] = float(salario_str)
                except (ValueError, TypeError):
                    print("[WARNING] Salario inválido, manteniendo valor actual")
            print(personal_data)
            personal_updated = personal_table.update(personal_id, personal_data)

            if personal_updated:
                self.show_success(f"Personal {nombre_completo} actualizado exitosamente")
                await self.load_personal_data()
                self.close_personal_modal()
            else:
                self.show_error("Error actualizando datos del personal")

        except Exception as e:
            print(f"[ERROR] Error en _update_personal_simplified: {e}")
            self.show_error(f"Error actualizando personal: {str(e)}")

    async def delete_personal(self):
        """Eliminar personal - USANDO TABLAS SEPARADAS"""
        print("[DEBUG] Eliminando personal con tablas separadas...")
        self.set_loading(True)

        try:
            if not self.personal_to_delete:
                self.show_error("No hay personal seleccionado para eliminar")
                return

            personal_id = self.personal_to_delete.get("id")
            usuario_id = self.personal_to_delete.get("usuarios", {}).get("id")

            print(f"[DEBUG] Eliminando personal_id: {personal_id}, usuario_id: {usuario_id}")

            # 1. Verificar que no tenga consultas activas
            consultas_activas = supabase_client.get_client().table('consultas').select('id', count='exact').eq('odontologo_id', personal_id).in_('estado', ['programada', 'confirmada', 'en_progreso']).execute()

            if consultas_activas.count and consultas_activas.count > 0:
                self.show_error("No se puede eliminar: el personal tiene consultas activas")
                return

            # 2. Desactivar usando personal_table
            personal_updated = personal_table.update_work_status(
                personal_id,
                "inactivo",
                f"Personal desactivado desde dashboard por {self.user_profile.get('nombre_completo', 'Admin')}"
            )

            # 3. Desactivar usuario usando users_table
            usuario_updated = users_table.update(usuario_id, {"activo": False})

            if personal_updated and usuario_updated:
                nombre = self.personal_to_delete.get("usuarios", {}).get("nombre_completo", "")
                self.show_success(f"Personal {nombre} desactivado exitosamente")
                await self.load_personal_data()
                self.close_delete_confirmation()
            else:
                self.show_error("Error desactivando personal")

        except Exception as e:
            print(f"[ERROR] Error eliminando personal: {e}")
            self.show_error(f"Error eliminando personal: {str(e)}")
        finally:
            self.set_loading(False)

    async def reactivate_personal(self, personal_data: Dict):
        """Reactivar personal - USANDO TABLAS SEPARADAS"""
        print("[DEBUG] Reactivando personal con tablas separadas...")
        self.set_loading(True)

        try:
            personal_id = personal_data.get("id")
            usuario_id = personal_data.get("usuarios", {}).get("id")

            # Reactivar usando las tablas correspondientes
            personal_updated = personal_table.update_work_status(
                personal_id,
                "activo",
                f"Personal reactivado desde dashboard por {self.user_profile.get('nombre_completo', 'Admin')}"
            )

            usuario_updated = users_table.update(usuario_id, {"activo": True})

            if personal_updated and usuario_updated:
                nombre = personal_data.get("usuarios", {}).get("nombre_completo", "")
                self.show_success(f"Personal {nombre} reactivado exitosamente")
                await self.load_personal_data()
            else:
                self.show_error("Error reactivando personal")

        except Exception as e:
            print(f"[ERROR] Error reactivando personal: {e}")
            self.show_error(f"Error reactivando personal: {str(e)}")
        finally:
            self.set_loading(False)

    # ==========================================
    # OPERACIONES CRUD SERVICIOS
    # ==========================================

    async def save_servicio(self):
        """Guardar servicio (crear o actualizar) - REFACTORIZADO PARA USAR ServicesTable"""
        print("[DEBUG] Guardando servicio con ServicesTable...")
        self.set_loading(True)
        try:
            # Validaciones básicas
            if not self.servicio_form["nombre"]:
                self.show_error("El nombre del servicio es requerido")
                return

            if not self.servicio_form["precio_base"]:
                self.show_error("El precio base es requerido")
                return

            servicio_data = {
                "codigo": self.servicio_form["codigo"],
                "nombre": self.servicio_form["nombre"],
                "descripcion": self.servicio_form.get("descripcion"),
                "categoria": self.servicio_form["categoria"],
                "subcategoria": self.servicio_form.get("subcategoria"),
                "duracion_estimada": f"{self.servicio_form.get('duracion_estimada', 30)} minutes",
                "precio_base": float(self.servicio_form["precio_base"]),
                "precio_minimo": float(self.servicio_form.get("precio_minimo", 0)) if self.servicio_form.get("precio_minimo") else None,
                "precio_maximo": float(self.servicio_form.get("precio_maximo", 0)) if self.servicio_form.get("precio_maximo") else None,
                "activo": True
            }

            if self.selected_servicio:
                # Actualizar existente usando ServicesTable.update()
                updated_servicio = services_table.update(self.selected_servicio['id'], servicio_data)
                if updated_servicio:
                    self.show_success("Servicio actualizado exitosamente")
                else:
                    self.show_error("Error actualizando servicio")
            else:
                # Crear nuevo usando ServicesTable.create()
                if self.user_profile:
                    servicio_data["creado_por"] = self.user_profile["id"]

                new_servicio = services_table.create(servicio_data)
                if new_servicio:
                    self.show_success("Servicio creado exitosamente")
                else:
                    self.show_error("Error creando servicio")

            # Recargar datos y cerrar modal
            await self.load_servicios_data()
            self.close_servicio_modal()

        except Exception as e:
            print(f"[ERROR] Error guardando servicio: {e}")
            self.show_error(f"Error guardando servicio: {str(e)}")
        finally:
            self.set_loading(False)

    # ==========================================
    # MÉTODOS AUXILIARES
    # ==========================================
    async def _get_dashboard_stats_real(self) -> Dict[str, Any]:
        """Obtener estadísticas reales del dashboard"""
        try:
            # Total pacientes
            pacientes_response = supabase_client.get_client().table('pacientes').select('id', count='exact').eq('activo', True).execute()

            # Personal activo
            personal_response = supabase_client.get_client().table('personal').select('id', count='exact').eq('estado_laboral', 'activo').execute()

            # Servicios activos
            servicios_response = supabase_client.get_client().table('servicios').select('id', count='exact').eq('activo', True).execute()

            # Consultas de hoy
            today = date.today().isoformat()
            consultas_response = supabase_client.get_client().table('consultas').select('id', count='exact').gte('fecha_programada', today).lt('fecha_programada', f"{today}T23:59:59").execute()

            # Ingresos del mes
            current_month = datetime.datetime.now().strftime('%Y-%m')
            pagos_response = supabase_client.get_client().table('pagos').select('monto_pagado').gte('fecha_pago', f"{current_month}-01").eq('estado_pago', 'completado').execute()

            total_ingresos = sum([pago['monto_pagado'] for pago in pagos_response.data]) if pagos_response.data else 0

            # Pagos pendientes
            pagos_pendientes_response = supabase_client.get_client().table('pagos').select('id', count='exact').eq('estado_pago', 'pendiente').execute()

            return {
                "total_pacientes": pacientes_response.count or 0,
                "consultas_hoy": consultas_response.count or 0,
                "ingresos_mes": total_ingresos,
                "personal_activo": personal_response.count or 0,
                "servicios_activos": servicios_response.count or 0,
                "pagos_pendientes": pagos_pendientes_response.count or 0
            }

        except Exception as e:
            print(f"[ERROR] Error obteniendo estadísticas: {e}")
            # Retornar datos por defecto en caso de error
            return {
                "total_pacientes": 0,
                "consultas_hoy": 0,
                "ingresos_mes": 0,
                "personal_activo": 0,
                "servicios_activos": 0,
                "pagos_pendientes": 0
            }

    # ==========================================
    # PROPIEDADES COMPUTADAS
    # ==========================================
    @rx.var
    def total_personal(self) -> int:
        return len(self.personal_list)

    @rx.var
    def total_activos(self) -> int:
        return len([p for p in self.personal_list if p.estado_laboral == "activo"])

    @rx.var
    def total_odontologos(self) -> int:
        return len([p for p in self.personal_list if p.tipo_personal == "Odontólogo"])

    @rx.var
    def total_otros_roles(self) -> int:
        return len([p for p in self.personal_list if p.tipo_personal != "Odontólogo"])

    @rx.var
    def filtered_personal_list(self) -> List[PersonalModel]:
        """Lista de personal filtrada"""
        return self.personal_list

    @rx.var
    def total_pacientes_activos(self) -> int:
        """Total de pacientes activos en el sistema"""
        return self.pacientes_stats.activos

    @rx.var
    def pacientes_nuevos_mes(self) -> int:
        """Pacientes nuevos este mes"""
        return self.pacientes_stats.nuevos_mes

    @rx.var
    def distribucion_genero_pacientes(self) -> str:
        """Distribución de género en formato texto"""
        total = self.pacientes_stats.total
        if total == 0:
            return "Sin datos"

        hombres_pct = (self.pacientes_stats.hombres / total) * 100
        mujeres_pct = (self.pacientes_stats.mujeres / total) * 100

        return f"Hombres: {hombres_pct:.1f}% | Mujeres: {mujeres_pct:.1f}%"


    # ==========================================
    # INICIALIZACIÓN
    # ==========================================
    def on_load(self):
        """Cargar datos iniciales"""
        print("[DEBUG] Inicializando BossState...")
        return self.load_dashboard_data()
