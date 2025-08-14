# 🗄️ BASE DE DATOS - SISTEMA ODONTOLÓGICO
## Documentación Completa de Supabase PostgreSQL

---

## 📊 RESUMEN EJECUTIVO

**Tecnología:** PostgreSQL 15.8 + Supabase  
**Tablas:** 15 tablas principales + vistas optimizadas  
**Triggers:** 10 triggers automáticos implementados  
**Funciones:** 12+ funciones de negocio  
**Política:** Row Level Security (RLS) preparado  
**Numeración:** Sistema automático para todos los documentos  

---

## 🏗️ ARQUITECTURA DE BASE DE DATOS

### **📋 TABLA DE CORRESPONDENCIA**
| **Tabla DB** | **Archivo Python** | **Estado** | **Descripción** |
|--------------|-------------------|------------|-----------------|
| ✅ **usuarios** | `usuarios.py` | Completo | Usuarios del sistema con roles |
| ✅ **roles** | `roles.py` | ✅ Creado | Roles y permisos del sistema |
| ✅ **personal** | `personal.py` | Completo | Empleados de la clínica |
| ✅ **pacientes** | `pacientes.py` | Completo | Pacientes con HC automática |
| ✅ **servicios** | `servicios.py` | Completo | Catálogo de servicios odontológicos |
| ✅ **consultas** | `consultas.py` | Completo | Sistema de orden de llegada |
| ✅ **intervenciones** | `intervenciones.py` | Completo | Tratamientos realizados |
| ✅ **pagos** | `pagos.py` | Completo | Facturación y pagos |
| ✅ **odontograma** | `odontograma.py` | Completo | Odontogramas de pacientes |
| ✅ **dientes** | `dientes.py` | ✅ Creado | Catálogo FDI de 52 dientes |
| ✅ **condiciones_diente** | `condiciones_diente.py` | ✅ Creado | Estados específicos por diente |
| ✅ **historial_medico** | `historial_medico.py` | Completo | Historia clínica detallada |
| ✅ **imagenes_clinicas** | `imagenes_clinicas.py` | ✅ Creado | Radiografías y fotografías |
| ✅ **configuracion_sistema** | `configuracion_sistema.py` | ✅ Creado | Configuraciones globales |
| ✅ **auditoria** | `auditoria.py` | ✅ Creado | Sistema de auditoría completo |

**🎯 RESULTADO:** 15/15 tablas con archivos Python = **100% COMPLETITUD**

---

## 🤖 SISTEMA DE AUTOMATIZACIÓN (TRIGGERS Y FUNCIONES)

### **🔥 TRIGGERS ACTIVOS (10 implementados)**

#### **1. AUTO-NUMERACIÓN INTELIGENTE**
```sql
-- ✅ PACIENTES: HC000001, HC000002, HC000003...
trigger_generar_numero_historia → generar_numero_historia()

-- ✅ CONSULTAS: 20250807001, 20250807002... (por día)
trigger_generar_numero_consulta → generar_numero_consulta() 

-- ✅ PAGOS: REC2025080001, REC2025080002... (por mes)
trigger_generar_numero_recibo → generar_numero_recibo()
```

#### **2. CÁLCULOS AUTOMÁTICOS**
```sql
-- ✅ EDAD AUTOMÁTICA desde fecha_nacimiento
trigger_calcular_edad_paciente → calcular_edad_paciente()

-- ✅ SALDO AUTOMÁTICO: monto_total - monto_pagado  
trigger_calcular_saldo_pendiente → calcular_saldo_pendiente()
```

#### **3. TIMESTAMPS AUTOMÁTICOS**
```sql
-- ✅ FECHA_ACTUALIZACION en cada UPDATE
trigger_pacientes_fecha_actualizacion
trigger_consultas_fecha_actualizacion  
trigger_odontograma_fecha_actualizacion
trigger_personal_fecha_actualizacion
trigger_usuarios_fecha_actualizacion
```

### **🛠️ FUNCIONES PRINCIPALES**

#### **📝 Autonumeración**
```sql
generar_numero_historia()      -- HC + padding automático
generar_numero_consulta()      -- YYYYMMDD + secuencial por día  
generar_numero_recibo()        -- REC + YYYYMM + secuencial por mes
```

#### **🧮 Cálculos**
```sql
calcular_edad_paciente()       -- EXTRACT(YEAR FROM AGE())
calcular_saldo_pendiente()     -- Manejo de pagos parciales
actualizar_fecha_modificacion() -- CURRENT_TIMESTAMP automático
```

#### **🔒 Sistema de Usuarios**
```sql
crear_usuario_seguro()         -- Creación con validaciones
get_role_id_by_name()          -- Resolución de roles con fallbacks
verificar_permiso()            -- Sistema de permisos granular
obtener_usuario_completo()     -- Info completa con relaciones
```

#### **📈 Reportes y Estadísticas**
```sql
obtener_stats_dashboard()      -- Métricas en tiempo real
cleanup_orphaned_auth_users()  -- Limpieza de usuarios huérfanos
```

---

## 📊 VISTAS OPTIMIZADAS (4 vistas)

### **🏥 Vista Personal Completo**
```sql
vista_personal_completo
-- Información consolidada de personal + usuarios + roles
-- Campos: id, nombre_completo, email, tipo_personal, especialidad, estado_laboral
-- Usado en: Dropdowns de odontólogos, reportes de personal
```

### **👤 Vista Usuarios Completo**
```sql
vista_usuarios_completo  
-- Información completa de usuarios con roles y permisos
-- Campos: id, email, nombre_completo, rol_nombre, permisos, activo
-- Usado en: Gestión de usuarios, validaciones de permisos
```

### **💰 Vista Ingresos Mensuales**
```sql
vista_ingresos_mensuales
-- Reportes financieros agrupados por mes
-- Campos: año, mes, total_ingresos, cantidad_pagos, promedio_pago
-- Usado en: Dashboard financiero, reportes gerenciales
```

### **🦷 Vista Servicios Populares**
```sql
vista_servicios_populares
-- Servicios ordenados por popularidad y rentabilidad
-- Campos: servicio_id, nombre, categoria, veces_usado, ingresos_totales
-- Usado en: Análisis de servicios, reportes de productividad
```

---

## 💾 DATOS PRECARGADOS (LISTO PARA PRODUCCIÓN)

### **👥 ROLES DEL SISTEMA (4 roles)**
```sql
1. gerente        -- Acceso total al sistema
2. administrador  -- Gestión operativa  
3. odontologo     -- Atención clínica
4. asistente      -- Apoyo básico
```

### **🦷 CATÁLOGO DE SERVICIOS (14 servicios)**
```sql
PREVENTIVA:     Consulta General, Limpieza Dental
RESTAURATIVA:   Obturación Simple, Obturación Compleja  
ENDODONCIA:     Endodoncia Unirradicular, Multirradicular
CIRUGÍA:        Extracción Simple, Extracción Compleja
PROTESIS:       Corona Individual, Puente Fijo
IMPLANTES:      Implante Dental + Corona
ESTÉTICA:       Blanqueamiento Dental
ORTODONCIA:     Ortodoncia (mensualidad)
DIAGNÓSTICO:    Radiografía Panorámica
```

### **🦷 CATÁLOGO FDI COMPLETO (52 dientes)**
```sql
ADULTOS:     11-18, 21-28, 31-38, 41-48 (32 dientes)
TEMPORALES:  51-55, 61-65, 71-75, 81-85 (20 dientes)

Información por diente:
- Número FDI y pediátrico
- Nombre anatómico completo
- Tipo (incisivo, canino, premolar, molar)
- Ubicación y cuadrante
- Caras disponibles (oclusal, mesial, distal, vestibular, lingual)
- Descripción anatómica
```

---

## 🔧 GUÍA DE USO DE ARCHIVOS PYTHON

### **🚀 PATRÓN ESTÁNDAR DE USO**

#### **1. Importación**
```python
from dental_system.supabase.tablas.pacientes import pacientes_table
from dental_system.supabase.tablas.consultas import consultas_table
# ... etc
```

#### **2. Operaciones CRUD Básicas**
```python
# ✅ CREAR
nuevo_paciente = pacientes_table.create_patient_complete(
    primer_nombre="Juan",
    primer_apellido="Pérez", 
    numero_documento="12345678",
    registrado_por=user_id
)

# ✅ LEER
paciente = pacientes_table.get_by_id(paciente_id)
pacientes = pacientes_table.get_filtered_patients(busqueda="Juan")

# ✅ ACTUALIZAR  
paciente_updated = pacientes_table.update(paciente_id, {"telefono_1": "123456789"})

# ✅ ELIMINAR (soft delete automático si tiene campo 'activo')
resultado = pacientes_table.delete(paciente_id)
```

#### **3. Métodos Especializados**
```python
# 🔍 BÚSQUEDAS AVANZADAS
pacientes_filtrados = pacientes_table.get_filtered_patients(
    activos_only=True,
    busqueda="Juan", 
    genero="masculino"
)

# 📊 ESTADÍSTICAS
stats = pacientes_table.get_patient_stats()
# Resultado: {"total": 150, "nuevos_mes": 12, "hombres": 80, "mujeres": 70}

# 📅 CONSULTAS POR FECHA
consultas_hoy = consultas_table.get_today_consultations(odontologo_id)
consultas_rango = consultas_table.get_by_date_range(fecha_inicio, fecha_fin)
```

---

## ⚠️ VALIDACIONES AUTOMÁTICAS IMPLEMENTADAS

### **🔒 Restricciones a Nivel de BD**
```sql
-- ✅ DOCUMENTOS: Solo números, 6-20 dígitos
numero_documento CHECK (numero_documento ~ '^\d{6,20}$')

-- ✅ EMAILS: Formato válido obligatorio
email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')

-- ✅ TELÉFONOS: Formato internacional flexible
celular CHECK (celular ~ '^[\+]?[\d\s\-\(\)]{7,20}$')

-- ✅ CÓDIGOS DE SERVICIO: Solo mayúsculas y números
codigo CHECK (codigo ~ '^[A-Z0-9]+$')

-- ✅ MONTOS: Siempre positivos
precio_base CHECK (precio_base > 0)
costo_total CHECK (costo_total >= 0)
```

### **📋 Estados Controlados**
```sql
-- ✅ ESTADOS DE CONSULTA
estado CHECK (estado IN ('programada', 'confirmada', 'en_progreso', 'completada', 'cancelada', 'no_asistio'))

-- ✅ TIPOS DE CONSULTA  
tipo_consulta CHECK (tipo_consulta IN ('general', 'control', 'urgencia', 'cirugia', 'otro'))

-- ✅ MÉTODOS DE PAGO
metodo_pago CHECK (metodo_pago IN ('efectivo', 'tarjeta_credito', 'tarjeta_debito', 'transferencia', 'cheque', 'otro'))

-- ✅ CONDICIONES DE DIENTE (20 tipos)
tipo_condicion CHECK (tipo_condicion IN ('sano', 'caries', 'obturacion', 'corona', 'puente', 'implante', 'ausente', ...))
```

---

## 🎯 OPTIMIZACIONES PARA SISTEMA DE CONSULTAS

### **📋 FLUJO DE CONSULTAS POR ORDEN DE LLEGADA**

#### **1. Creación de Consulta**
```python
# ✅ ADMINISTRADOR crea consulta cuando paciente llega
nueva_consulta = consultas_table.create_consultation(
    paciente_id=paciente_id,
    odontologo_id=odontologo_id,  # Primer disponible o específico
    fecha_programada=datetime.now(),  # Momento de llegada
    tipo_consulta="general",
    estado="programada"  # = En espera por orden de llegada
)
# 📝 AUTO-GENERA: numero_consulta = "20250807001" 
```

#### **2. Sistema de Turnos**
```python
# ✅ OBTENER consultas del día por odontólogo (en orden de llegada)
consultas_hoy = consultas_table.get_today_consultations(odontologo_id)
# Resultado ordenado por fecha_programada (orden de llegada)

# ✅ CAMBIAR estado cuando inicia atención
consultas_table.update_status(consulta_id, "en_progreso")

# ✅ FINALIZAR consulta
consultas_table.update_status(consulta_id, "completada")
```

#### **3. Múltiples Intervenciones**
```python
# ✅ UNA CONSULTA → MÚLTIPLES INTERVENCIONES → DIFERENTES ODONTÓLOGOS
intervencion1 = intervenciones_table.create({
    "consulta_id": consulta_id,
    "servicio_id": servicio_limpieza_id,
    "odontologo_id": odontologo1_id,
    "procedimiento_realizado": "Profilaxis dental completa",
    "precio_final": 50000
})

intervencion2 = intervenciones_table.create({
    "consulta_id": consulta_id,  # ← MISMA CONSULTA
    "servicio_id": servicio_obturacion_id,
    "odontologo_id": odontologo2_id,  # ← DIFERENTE ODONTÓLOGO
    "procedimiento_realizado": "Obturación de caries en molar",
    "precio_final": 80000
})

# ✅ COSTO TOTAL automático = suma de intervenciones
```

---

## 📈 MÉTRICAS Y ESTADÍSTICAS DISPONIBLES

### **🏥 Dashboard en Tiempo Real**
```python
# ✅ ESTADÍSTICAS DE PACIENTES
paciente_stats = pacientes_table.get_patient_stats()
# {"total": 150, "nuevos_mes": 12, "activos": 150, "hombres": 80, "mujeres": 70}

# ✅ ESTADÍSTICAS DE CONSULTAS  
consultas_stats = consultas_table.get_today_consultations()
# Lista con todas las consultas del día + nombres completos

# ✅ ESTADÍSTICAS DE PAGOS
pagos_stats = pagos_table.get_payment_stats()
# {"total_mes": 2500000, "pendientes": 150000, "completados": 2350000}

# ✅ AUDITORÍA
auditoria_stats = auditoria_table.get_estadisticas_auditoria()
# {"total_acciones": 1250, "inserts": 400, "updates": 750, "deletes": 100}
```

---

## 🔒 SEGURIDAD Y AUDITORÍA

### **📊 Sistema de Auditoría Automático**
```python
# ✅ REGISTRO AUTOMÁTICO de todas las acciones
auditoria_table.registrar_accion(
    tabla_afectada="pacientes",
    registro_id=paciente_id,
    accion="INSERT",
    usuario_id=user_id,
    datos_nuevos=nuevo_paciente_data,
    modulo="pacientes",
    ip_address="192.168.1.100"
)

# ✅ HISTORIAL COMPLETO de cualquier registro
historial = auditoria_table.get_registro_history("pacientes", paciente_id)
# Lista cronológica de todos los cambios del paciente

# ✅ LIMPIEZA AUTOMÁTICA de registros antiguos
eliminados = auditoria_table.cleanup_old_records(days_to_keep=365)
```

### **🛡️ Row Level Security (RLS) - PREPARADO**
```sql
-- ✅ POLÍTICAS LISTAS PARA IMPLEMENTAR
CREATE POLICY "gerente_full_access" ON pacientes FOR ALL TO gerente;
CREATE POLICY "admin_crud_pacientes" ON pacientes FOR SELECT, INSERT, UPDATE TO administrador;  
CREATE POLICY "odontologo_read_own_patients" ON consultas FOR SELECT TO odontologo 
    USING (odontologo_id = auth.uid());
CREATE POLICY "asistente_read_today" ON consultas FOR SELECT TO asistente
    USING (DATE(fecha_programada) = CURRENT_DATE);
```

---

## 🚀 RECOMENDACIONES DE DESARROLLO

### **✅ BUENAS PRÁCTICAS IMPLEMENTADAS**

1. **Consistencia de Nombres:**
   - Todas las tablas tienen archivos Python correspondientes
   - Naming convention uniforme (snake_case)
   - Instancias únicas para importar (`pacientes_table`)

2. **Manejo de Errores:**
   - Decorador `@handle_supabase_error` en todos los métodos
   - Logging consistente con niveles apropiados
   - Return types tipados con Optional[Dict]

3. **Validaciones Automáticas:**
   - Triggers para cálculos automáticos
   - Restricciones CHECK a nivel de BD
   - Soft delete automático cuando existe campo 'activo'

4. **Optimización de Consultas:**
   - Vistas para consultas frecuentes
   - Joins optimizados para reducir N+1
   - Paginación y límites en consultas grandes

### **🎯 PRÓXIMOS PASOS SUGERIDOS**

1. **Implementar RLS:** Activar políticas de seguridad por rol
2. **Índices Adicionales:** Para consultas frecuentes de búsqueda
3. **Backup Automático:** Configurar respaldos programados
4. **Monitoreo:** Alertas para operaciones críticas
5. **Cache:** Implementar caché para vistas frecuentes

---

## 📚 REFERENCIAS TÉCNICAS

**Base de Datos:** PostgreSQL 15.8  
**Framework:** Supabase  
**ORM:** Supabase Python Client  
**Patrón:** Repository Pattern con BaseTable  
**Logging:** Python logging estándar  
**Validaciones:** PostgreSQL CHECK constraints + Python  
**Seguridad:** RLS + JWT tokens  
**Auditoría:** Tabla dedicada con triggers  

**📝 Última actualización:** $(date)  
**👨‍💻 Documentación generada por:** Claude Code

---

**💡 Este documento debe actualizarse cuando se implementen nuevas tablas, triggers o funciones.**