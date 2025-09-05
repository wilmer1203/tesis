# 📋 GUÍA DE REFACTORIZACIÓN DE MÓDULOS
## Template basado en la refactorización exitosa del Módulo PERSONAL

---

## 🎯 **PROPÓSITO DE ESTA GUÍA**

Esta guía documenta la **metodología completa** aplicada exitosamente en el módulo PERSONAL para:
- ✅ Alinear con **esquema de BD v4.1** 
- ✅ Implementar **Type Safety 100%**
- ✅ Consolidar **formularios por cohesión funcional**
- ✅ Eliminar **campos obsoletos** del sistema

**Usar como template para refactorizar módulos PACIENTES y CONSULTAS.**

---

## 🗄️ **PASO 1: ANÁLISIS DE ESQUEMA DE BD**

### **A. Identificar Cambios en Esquema v4.1**
```sql
-- Revisar archivo: esquema_final_corregido.sql
-- Comparar con modelos actuales

-- Ejemplo Personal:
ALTER TABLE personal 
ADD COLUMN acepta_pacientes_nuevos BOOLEAN DEFAULT TRUE,
ADD COLUMN orden_preferencia INTEGER DEFAULT 1;

-- Cambios de tipo/formato:
tipo_documento VARCHAR(2) DEFAULT 'CI'  -- Cambio: CC → CI
```

### **B. Checklist de Verificación BD**
- [ ] Campos nuevos requeridos por el negocio
- [ ] Campos obsoletos a eliminar
- [ ] Cambios de tipo de datos
- [ ] Defaults actualizados
- [ ] Constraints y validaciones

### **C. Documentar Cambios Encontrados**
```markdown
## CAMPOS A AGREGAR:
- acepta_pacientes_nuevos: bool = True
- orden_preferencia: int = 1

## CAMPOS A CAMBIAR:
- tipo_documento: "CC" → "CI" 

## CAMPOS A ELIMINAR:
- telefono → solo celular
- comision_servicios → no requerido
```

---

## 🏗️ **PASO 2: ACTUALIZAR MODELOS DE ENTIDAD**

### **A. [Módulo]Model - Entidad Principal**
```python
# Archivo: dental_system/models/[modulo]_models.py

class [Módulo]Model(rx.Base):
    """Modelo principal del módulo"""
    
    # ✅ AGREGAR campos nuevos del esquema
    acepta_pacientes_nuevos: bool = True
    orden_preferencia: int = 1
    
    # ✅ ACTUALIZAR tipos y defaults
    tipo_documento: str = "CI"  # Cambio de CC → CI
    
    # ✅ ELIMINAR campos obsoletos (comentar primero, luego eliminar)
    # telefono: str = ""  # OBSOLETO - usar celular
    
    # ✅ AGREGAR propiedades computadas
    @property
    def disponible_para_cola(self) -> bool:
        return self.activo and self.acepta_pacientes_nuevos
    
    @property
    def [campo]_display(self) -> str:
        """Formateo para UI"""
        return f"Formato: {self.[campo]}"
    
    # ✅ ACTUALIZAR from_dict() con nuevos campos
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "[Módulo]Model":
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            # ... campos existentes
            acepta_pacientes_nuevos=bool(data.get("acepta_pacientes_nuevos", True)),
            orden_preferencia=int(data.get("orden_preferencia", 1)),
            tipo_documento=str(data.get("tipo_documento", "CI")),
        )
```

### **B. [Módulo]FormModel - Formulario Tipado**
```python
# ✅ MOVER desde form_models.py a [modulo]_models.py

class [Módulo]FormModel(rx.Base):
    """
    📝 FORMULARIO DE CREACIÓN/EDICIÓN DE [MÓDULO]
    
    Consolidado en el mismo archivo que la entidad principal
    """
    
    # ✅ CAMPOS limpios (sin obsoletos)
    primer_nombre: str = ""
    primer_apellido: str = ""
    celular: str = ""  # Sin telefono
    
    # ✅ CAMPOS NUEVOS del esquema
    acepta_pacientes_nuevos: bool = True
    orden_preferencia: int = 1
    
    # ✅ VALIDACIÓN robusta
    def validate_form(self) -> Dict[str, List[str]]:
        """Validar campos requeridos"""
        errors = {}
        
        if not self.primer_nombre.strip():
            errors.setdefault("primer_nombre", []).append("Campo requerido")
            
        # ... más validaciones
        return errors
    
    # ✅ MAPEO inteligente para servicios
    def to_dict(self) -> Dict[str, str]:
        """Convertir a dict para compatibilidad con servicios"""
        return {
            "primer_nombre": self.primer_nombre,
            "celular": self.celular,  # telefono → celular
            
            # Campos nuevos
            "acepta_pacientes_nuevos": self.acepta_pacientes_nuevos,
            "orden_preferencia": self.orden_preferencia,
            
            # Mapeos especiales si necesarios
            "email": self.usuario_email,  # Ejemplo de mapeo
        }
    
    # ✅ FACTORY method desde BD
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "[Módulo]FormModel":
        """Crear instancia desde diccionario de BD"""
        if not data or not isinstance(data, dict):
            return cls()
        
        return cls(
            primer_nombre=str(data.get("primer_nombre", "")),
            celular=str(data.get("celular", "")),
            acepta_pacientes_nuevos=bool(data.get("acepta_pacientes_nuevos", True)),
            orden_preferencia=int(data.get("orden_preferencia", 1)),
        )
```

---

## 🔧 **PASO 3: ACTUALIZAR SERVICIOS**

### **A. [Módulo]Service - Lógica de Negocio**
```python
# Archivo: dental_system/services/[modulo]_service.py

class [Módulo]Service(BaseService):
    
    # ✅ ACTUALIZAR métodos principales con nuevos parámetros
    def create_[entidad](
        self,
        form_data: Dict[str, str],
        # Nuevos parámetros del esquema
        acepta_pacientes_nuevos: bool = True,
        orden_preferencia: int = 1,
        **kwargs
    ) -> Dict[str, Any]:
        """Crear nueva entidad con campos actualizados"""
        
        # ✅ MAPEO de campos actualizado
        entity_data = {
            "primer_nombre": form_data.get("primer_nombre", ""),
            "celular": form_data.get("celular", ""),  # telefono → celular
            
            # Campos nuevos
            "acepta_pacientes_nuevos": acepta_pacientes_nuevos,
            "orden_preferencia": orden_preferencia,
            "tipo_documento": "CI",  # Default correcto
        }
        
        # ✅ VALIDAR usando modelo tipado
        form_model = [Módulo]FormModel.from_dict(form_data)
        validation_errors = form_model.validate_form()
        
        if validation_errors:
            return {
                "success": False,
                "message": "Errores de validación",
                "errors": validation_errors
            }
        
        # ✅ LLAMAR tabla con parámetros actualizados
        result = self.[modulo]_table.create_[entidad](
            **entity_data,
            **kwargs
        )
        
        return result
```

---

## 🗃️ **PASO 4: ACTUALIZAR TABLAS (Repository)**

### **A. [Módulo]Table - Operaciones BD**
```python
# Archivo: dental_system/supabase/tablas/[modulo].py

class [Módulo]Table(BaseTable):
    
    # ✅ ACTUALIZAR métodos con nuevos campos
    def create_[entidad](
        self,
        primer_nombre: str,
        primer_apellido: str,
        celular: str,  # Cambio: telefono → celular
        
        # Nuevos parámetros
        acepta_pacientes_nuevos: bool = True,
        orden_preferencia: int = 1,
        **kwargs
    ) -> Dict[str, Any]:
        """Crear entidad con esquema actualizado"""
        
        # ✅ DATA con campos del esquema v4.1
        entity_data = {
            "primer_nombre": primer_nombre,
            "primer_apellido": primer_apellido,
            "celular": celular,  # Campo correcto
            
            # Campos nuevos requeridos
            "acepta_pacientes_nuevos": acepta_pacientes_nuevos,
            "orden_preferencia": orden_preferencia,
            "tipo_documento": "CI",  # Default correcto
            
            "fecha_creacion": datetime.now().isoformat(),
            "activo": True,
        }
        
        try:
            # ✅ INSERT con campos actualizados
            result = self.supabase.table(self.table_name).insert(entity_data).execute()
            
            if result.data and len(result.data) > 0:
                return {
                    "success": True,
                    "data": result.data[0],
                    "message": f"{self.entity_name} creado exitosamente"
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Error creando {self.entity_name}: {str(e)}"
            }
    
    # ✅ ACTUALIZAR get_by_id() para incluir nuevos campos
    def get_by_id(self, entity_id: str) -> Optional[Dict[str, Any]]:
        """Obtener por ID con todos los campos"""
        try:
            result = self.supabase.table(self.table_name)\
                .select("*, acepta_pacientes_nuevos, orden_preferencia")\
                .eq("id", entity_id)\
                .execute()
                
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error obteniendo {self.entity_name}: {e}")
            return None
```

---

## 🔄 **PASO 5: REFACTORIZAR ESTADO (TYPE SAFETY)**

### **A. Estado[Módulo] - Dict → Typed Model**
```python
# Archivo: dental_system/state/estado_[modulo].py

class Estado[Módulo](rx.State):
    
    # ❌ ANTES - Dict sin tipos
    # formulario_[entidad]: Dict[str, Any] = {}
    
    # ✅ DESPUÉS - Modelo tipado
    formulario_[entidad]: [Módulo]FormModel = [Módulo]FormModel()
    
    # ✅ REFACTORIZAR métodos para usar modelo tipado
    def limpiar_formulario_[entidad](self):
        """Limpiar formulario con modelo tipado"""
        self.formulario_[entidad] = [Módulo]FormModel()
    
    def cargar_[entidad]_en_formulario(self, entity_data: Dict[str, Any]):
        """Cargar datos en formulario tipado"""
        if entity_data:
            self.formulario_[entidad] = [Módulo]FormModel.from_dict(entity_data)
    
    def actualizar_campo_formulario_[entidad](self, field: str, value: Any):
        """Actualizar campo usando setattr type-safe"""
        if hasattr(self.formulario_[entidad], field):
            setattr(self.formulario_[entidad], field, value)
            self.validar_formulario_[entidad]()  # Auto-validación
    
    def validar_formulario_[entidad](self) -> bool:
        """Validar usando método del modelo tipado"""
        errors = self.formulario_[entidad].validate_form()
        self.errores_validacion_[entidad] = {}
        
        # Procesar errores para UI
        for field, field_errors in errors.items():
            self.errores_validacion_[entidad][field] = field_errors[0] if field_errors else ""
        
        return len(errors) == 0
    
    # ✅ MÉTODO de creación actualizado
    async def crear_[entidad](self):
        """Crear entidad usando formulario tipado"""
        if not self.validar_formulario_[entidad]():
            return
        
        # Convertir a dict para servicio
        form_data = self.formulario_[entidad].to_dict()
        
        # Llamar servicio con datos tipados
        result = await self.[modulo]_service.create_[entidad](
            form_data=form_data,
            # Pasar parámetros adicionales si necesarios
        )
        
        if result.get("success"):
            self.mostrar_mensaje_exito(result.get("message", ""))
            self.limpiar_formulario_[entidad]()
            await self.cargar_lista_[entidades]()
        else:
            self.mostrar_mensaje_error(result.get("message", "Error desconocido"))
```

---

## 📝 **PASO 6: ACTUALIZAR FORMULARIOS UI**

### **A. Limpiar Forms.py - Eliminar Campos Obsoletos**
```python
# Archivo: dental_system/components/forms.py

def [modulo]_form() -> rx.Component:
    """Formulario actualizado sin campos obsoletos"""
    
    return rx.vstack(
        # ✅ CAMPOS LIMPIOS (sin obsoletos)
        enhanced_form_field(
            label="Nombres",
            field_name="primer_nombre",
            value=rx.cond(AppState.formulario_[entidad], AppState.formulario_[entidad].primer_nombre, ""),
            on_change=AppState.actualizar_campo_formulario_[entidad],
            required=True,
            validation_error=rx.cond(AppState.errores_validacion_[entidad], AppState.errores_validacion_[entidad].get("primer_nombre", ""), "")
        ),
        
        # ✅ CAMBIAR telefono → celular
        enhanced_form_field(
            label="Celular",  # Cambio de "Teléfono"
            field_name="celular",  # Cambio de "telefono"
            value=rx.cond(AppState.formulario_[entidad], AppState.formulario_[entidad].celular, ""),
            on_change=AppState.actualizar_campo_formulario_[entidad],
            placeholder="0414-1234567",
            icon="phone",
        ),
        
        # ❌ ELIMINAR campos obsoletos
        # enhanced_form_field("Comisión Servicios")  # ELIMINADO
        # enhanced_form_field("Años Experiencia")    # ELIMINADO
        
        # ✅ AGREGAR campos nuevos si aplican
        rx.cond(
            AppState.formulario_[entidad].tipo_personal == "odontologo",
            enhanced_form_field(
                label="Acepta Pacientes Nuevos",
                field_name="acepta_pacientes_nuevos",
                field_type="checkbox",
                value=rx.cond(AppState.formulario_[entidad], AppState.formulario_[entidad].acepta_pacientes_nuevos, True),
                on_change=AppState.actualizar_campo_formulario_[entidad],
            )
        ),
        
        spacing="4",
        width="100%"
    )
```

---

## 🖥️ **PASO 7: ACTUALIZAR PÁGINA UI**

### **A. [Módulo]Page - Referencias Tipadas**
```python
# Archivo: dental_system/pages/[modulo]_page.py

def [modulo]_page() -> rx.Component:
    """Página actualizada con referencias tipadas"""
    
    return rx.vstack(
        # ✅ ACCESO TIPADO a campos
        rx.text(
            rx.cond(
                AppState.formulario_[entidad],
                AppState.formulario_[entidad].primer_nombre,  # Autocompletado ✅
                ""
            )
        ),
        
        # ✅ MOSTRAR campos nuevos
        rx.cond(
            AppState.[entidad]_seleccionado,
            rx.badge(
                "Cola Activa" if AppState.[entidad]_seleccionado.acepta_pacientes_nuevos else "Cola Inactiva",
                color="green" if AppState.[entidad]_seleccionado.acepta_pacientes_nuevos else "gray"
            )
        ),
        
        # ✅ UI para campos del esquema v4.1
        [modulo]_form(),
        
        spacing="6",
        padding="4"
    )
```

---

## 🔐 **PASO 8: ACTUALIZAR AUTENTICACIÓN (Si aplica)**

### **A. EstadoAuth - Cargar Datos Completos**
```python
# Archivo: dental_system/state/estado_auth.py

async def iniciar_sesion(self, form_data: Dict[str, str]):
    """Login con carga de datos completos del usuario"""
    
    # ... autenticación existente
    
    # ✅ CARGAR datos completos según esquema v4.1
    if user_data.get("role") in ["odontologo"]:
        personal_data = personal_table.get_by_usuario_id(self.id_usuario)
        if personal_data:
            personal_model = PersonalModel.from_dict(personal_data)
            
            # Cargar campos críticos para la sesión
            self.perfil_usuario.update({
                'acepta_pacientes_nuevos': personal_model.acepta_pacientes_nuevos,
                'orden_preferencia': personal_model.orden_preferencia,
                'disponible_para_cola': personal_model.disponible_para_cola,
                # ... otros campos necesarios para la sesión
            })
```

---

## 🔄 **PASO 9: ACTUALIZAR IMPORTS**

### **A. models/__init__.py - Imports Consolidados**
```python
# ✅ IMPORTS consolidados por módulo
from .[modulo]_models import (
    [Módulo]Model,
    [Módulo]StatsModel,
    [Módulo]FormModel,  # ✅ Ahora en el mismo archivo
    # ... otros modelos del módulo
)

# ❌ ELIMINAR imports obsoletos
# from .form_models import [Módulo]FormModel  # YA NO EXISTE
```

### **B. Verificar Imports en Archivos de Uso**
```bash
# Buscar y actualizar imports obsoletos
grep -r "from.*form_models import" . --include="*.py"
grep -r "form_models\.[Módulo]FormModel" . --include="*.py"

# Actualizar a:
from dental_system.models.[modulo]_models import [Módulo]FormModel
```

---

## ✅ **PASO 10: TESTING Y VALIDACIÓN**

### **A. Checklist de Verificación**
```python
# ✅ TESTS de importación
from dental_system.models.[modulo]_models import [Módulo]Model, [Módulo]FormModel

# ✅ TESTS de funcionalidad básica  
model = [Módulo]Model(primer_nombre="Test")
form = [Módulo]FormModel(primer_nombre="Test")

# ✅ TESTS de conversión
form_data = form.to_dict()
form_loaded = [Módulo]FormModel.from_dict(form_data)

# ✅ TESTS de validación
errors = form.validate_form()
print(f"Errores: {errors}")

print("✅ Módulo [MÓDULO] refactorizado exitosamente!")
```

### **B. Testing de Compilación**
```bash
cd /ruta/proyecto
timeout 15 reflex run  # Verificar que compila sin errores
```

### **C. Testing de Funcionalidad**
- [ ] Crear entidad desde formulario
- [ ] Editar entidad existente  
- [ ] Validaciones funcionando
- [ ] Campos nuevos guardándose en BD
- [ ] UI sin campos obsoletos
- [ ] Autocompletado funcionando

---

## 📊 **CHECKLIST FINAL POR MÓDULO**

### **PACIENTES MODULE**
- [ ] ✅ **BD**: Verificar campos `tipo_documento`, teléfonos, contacto emergencia
- [ ] 🔄 **PacienteModel**: Actualizar con esquema v4.1
- [ ] ✅ **PacienteFormModel**: Ya consolidado en `pacientes_models.py`
- [ ] 🔄 **PacientesService**: Verificar mapeo y validaciones
- [ ] 🔄 **PacientesTable**: Alinear queries con esquema
- [ ] 🔄 **EstadoPacientes**: Cambiar Dict → PacienteFormModel
- [ ] 🔄 **PacientesPage**: Referencias tipadas
- [ ] 🔄 **Forms**: Limpiar campos obsoletos

### **CONSULTAS MODULE**
- [ ] ✅ **BD**: Verificar `orden_llegada`, `orden_cola_odontologo`, estados
- [ ] 🔄 **ConsultaModel**: Campos sistema de colas sin citas
- [ ] ✅ **ConsultaFormModel**: Ya consolidado en `consultas_models.py`
- [ ] 🔄 **ConsultasService**: Lógica orden de llegada
- [ ] 🔄 **ConsultasTable**: Sistema sin citas programadas
- [ ] 🔄 **EstadoConsultas**: Cambiar Dict → ConsultaFormModel  
- [ ] 🔄 **ConsultasPage**: UI sistema de colas en tiempo real
- [ ] 🔄 **Forms**: Formularios adaptados a "sin citas"

---

## 🏆 **RESULTADOS ESPERADOS**

Al completar esta guía para cada módulo:

### **✅ TÉCNICOS:**
- **Type Safety 100%** - Cero `Dict[str,Any]` en formularios
- **Esquema BD alineado** - Todos los campos del esquema v4.1 implementados
- **Formularios consolidados** - Cohesión funcional perfecta
- **Validaciones robustas** - Error handling completo y tipado
- **UI limpia** - Solo campos requeridos por el negocio

### **✅ ARQUITECTURA:**
- **Patrón consistente** - Misma estructura en todos los módulos
- **Código mantenible** - Fácil lectura y modificación
- **Imports lógicos** - Estructura clara y predecible  
- **Documentación inline** - Código auto-documentado

### **✅ FUNCIONALES:**
- **Sistema funcionando 100%** - Sin regresiones
- **Nuevas características** - Campos del esquema v4.1 operativos
- **Campos obsoletos eliminados** - Sistema limpio y eficiente
- **Validaciones mejoradas** - UX consistente

---

## 📅 **CRONOGRAMA SUGERIDO**

### **DÍA 1: PACIENTES**
- Mañana: Análisis BD + Actualizar modelos
- Tarde: Servicios + Tablas + Estado

### **DÍA 2: PACIENTES (continuación)**  
- Mañana: UI + Forms + Testing
- Tarde: Validación completa + Fixes

### **DÍA 3: CONSULTAS**
- Mañana: Análisis BD + Actualizar modelos  
- Tarde: Servicios + Tablas + Estado

### **DÍA 4: CONSULTAS (continuación)**
- Mañana: UI + Forms + Lógica de colas
- Tarde: Testing + Integración con Personal

### **DÍA 5: INTEGRACIÓN Y TESTING**
- Mañana: Testing completo del flujo
- Tarde: Documentación + Optimizaciones

---

## 💡 **NOTAS FINALES**

1. **Seguir exactamente esta guía** - Está basada en refactorización exitosa
2. **Un paso a la vez** - No saltar pasos para evitar errores
3. **Testing continuo** - Verificar cada cambio antes del siguiente
4. **Documentar cambios** - Actualizar comentarios y documentación
5. **Backup antes de empezar** - Git commit antes de cada módulo

**Esta metodología garantiza refactorización exitosa con calidad enterprise.**

---

**📝 Creado:** Agosto 2025  
**👨‍💻 Basado en:** Refactorización exitosa Módulo PERSONAL  
**🎯 Para:** Módulos PACIENTES y CONSULTAS  
**🏆 Objetivo:** Type Safety + BD v4.1 + Consolidación de formularios