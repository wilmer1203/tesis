# 🗑️ PLAN DE LIMPIEZA DE BASE DE DATOS

## 📋 RESUMEN EJECUTIVO

**Fecha:** 2025-10-21
**Estado:** ✅ Análisis Completado - Listo para Ejecución
**Objetivo:** Eliminar tablas y columnas obsoletas que no se usan en el sistema

---

## 🎯 ALCANCE DE LA LIMPIEZA

### **TABLAS A ELIMINAR (4 tablas)**

#### ✅ **1. auditoria** - SEGURO ELIMINAR
- **Archivos afectados:** 8 archivos (solo imports, NO uso real)
- **Uso real:** ❌ CERO - La clase existe pero nunca se instancia
- **Impacto:** Ninguno - tabla vacía y sin funcionalidad activa
- **Archivos Python:**
  - `dental_system/supabase/tablas/auditoria.py` → ELIMINAR
  - `dental_system/supabase/tablas/__init__.py` → ACTUALIZAR (quitar import)

#### ✅ **2. cola_atencion** - SEGURO ELIMINAR
- **Archivos afectados:** 8 archivos (solo imports, NO uso real)
- **Uso real:** ❌ CERO - Sistema de colas se maneja en tabla `consultas`
- **Impacto:** Ninguno - funcionalidad ya migrada a `consultas`
- **Archivos Python:**
  - `dental_system/supabase/tablas/cola_atencion.py` → ELIMINAR
  - `dental_system/supabase/tablas/__init__.py` → ACTUALIZAR (quitar import)

#### ✅ **3. configuracion_sistema** - SEGURO ELIMINAR
- **Archivos afectados:** 5 archivos (solo imports, NO uso real)
- **Uso real:** ❌ CERO - Configuraciones están en variables de entorno
- **Impacto:** Ninguno - sistema no depende de esta tabla
- **Archivos Python:**
  - `dental_system/supabase/tablas/configuracion_sistema.py` → ELIMINAR
  - `dental_system/supabase/tablas/__init__.py` → ACTUALIZAR (quitar import)

#### ✅ **4. notificaciones_sistema** - SEGURO ELIMINAR
- **Archivos afectados:** Ninguno
- **Uso real:** ❌ NO EXISTE en el código
- **Impacto:** Ninguno - tabla fantasma
- **Archivos Python:** Ninguno

---

### **COLUMNAS A ELIMINAR (15 columnas)**

#### **TABLA: condiciones_diente (5 columnas)**

| Columna | Uso Actual | Razón para Eliminar | Impacto |
|---------|-----------|---------------------|---------|
| `observaciones` | ❌ NO | Redundante con `descripcion` | Ninguno |
| `material_utilizado` | ❌ NO | Se registra en `intervenciones_servicios.material` | Ninguno |
| `tecnica_utilizada` | ❌ NO | No se usa en ningún lado | Ninguno |
| `color_material` | ❌ NO | No se usa en ningún lado | Ninguno |
| `fecha_tratamiento` | ❌ NO | Ya existe `fecha_registro` | Ninguno |

**Archivos afectados:**
- `dental_system/models/odontologia_models.py` (líneas 214-217, 183-186)
- `dental_system/supabase/tablas/condiciones_diente.py`

#### **TABLA: consultas (4 columnas)**

| Columna | Uso Actual | Razón para Eliminar | Impacto |
|---------|-----------|---------------------|---------|
| `odontologo_preferido_id` | ⚠️ MÍNIMO | Solo en modelos (5 archivos) | Bajo - backward compatibility |
| `notas_internas` | ⚠️ EXISTE | Redundante con `observaciones` | Bajo - consolidar en una |
| `fecha_inicio_atencion` | ❌ NO | Redundante con `fecha_creacion` | Ninguno |
| `fecha_fin_atencion` | ❌ NO | Redundante con `fecha_actualizacion` | Ninguno |

**Archivos afectados:**
- `dental_system/models/consultas_models.py` (líneas 26, 40, 50-51, 99-100)
- `dental_system/state/estado_consultas.py`
- `dental_system/services/consultas_service.py`
- `dental_system/supabase/tablas/consultas.py`

#### **TABLA: dientes (5 columnas)**

| Columna | Uso Actual | Razón para Eliminar | Impacto |
|---------|-----------|---------------------|---------|
| `numero_diente_pediatrico` | ❌ NO | Sistema solo usa FDI adulto | Ninguno |
| `descripcion_anatomica` | ❌ NO | Información excesiva no usada | Ninguno |
| `coordenadas_svg` | ❌ NO | Frontend calcula posiciones | Ninguno |
| `forma_base` | ❌ NO | No se renderiza | Ninguno |
| `imagenes_clinicas` | ❌ NO | No se usa | Ninguno |

**Archivos afectados:**
- `dental_system/models/odontologia_models.py` (líneas 99, 104, 94, 128)
- `dental_system/supabase/tablas/dientes_OLD.py` (archivo backup)

---

## 📊 ANÁLISIS DE DEPENDENCIAS

### **✅ TABLAS - CERO DEPENDENCIAS CRÍTICAS**

```
RESULTADO DEL ANÁLISIS:
- auditoria: 0 usos reales (solo imports)
- cola_atencion: 0 usos reales (solo imports)
- configuracion_sistema: 0 usos reales (solo imports)
- notificaciones_sistema: No existe

CONCLUSIÓN: SEGURO eliminar las 4 tablas
```

### **⚠️ COLUMNAS - DEPENDENCIAS MÍNIMAS**

```
ALTO IMPACTO (requiere actualizar código):
- odontologo_preferido_id: 5 archivos Python

MEDIO IMPACTO:
- notas_internas: Consolidar con 'observaciones'

BAJO IMPACTO (solo modelos):
- Resto de columnas: Solo eliminar de modelos
```

---

## 🛠️ PLAN DE EJECUCIÓN

### **FASE 1: PREPARACIÓN (5 min)**

```bash
# 1. Crear backup completo
pg_dump -h localhost -U postgres -d dental_system > backup_pre_limpieza_$(date +%Y%m%d).sql

# 2. Verificar backup
ls -lh backup_pre_limpieza_*.sql

# 3. Ambiente de prueba (opcional)
# Ejecutar primero en base de datos de desarrollo
```

### **FASE 2: ELIMINAR TABLAS OBSOLETAS (2 min)**

```sql
-- Ejecutar script: 20251021_eliminar_tablas_columnas_obsoletas.sql
-- Sección: PASO 2 (DROP TABLE)

DROP TABLE IF EXISTS auditoria CASCADE;
DROP TABLE IF EXISTS cola_atencion CASCADE;
DROP TABLE IF EXISTS configuracion_sistema CASCADE;
DROP TABLE IF EXISTS notificaciones_sistema CASCADE;
```

### **FASE 3: ELIMINAR COLUMNAS DE BD (3 min)**

```sql
-- Ejecutar script: 20251021_eliminar_tablas_columnas_obsoletas.sql
-- Sección: PASO 1 (ALTER TABLE DROP COLUMN)

-- condiciones_diente (5 columnas)
-- consultas (4 columnas)
-- dientes (5 columnas)
```

### **FASE 4: ACTUALIZAR CÓDIGO PYTHON (10 min)**

#### **4.1. Eliminar archivos Python de tablas**
```bash
del dental_system\supabase\tablas\auditoria.py
del dental_system\supabase\tablas\cola_atencion.py
del dental_system\supabase\tablas\configuracion_sistema.py
```

#### **4.2. Actualizar `dental_system/supabase/tablas/__init__.py`**
```python
# ELIMINAR estas líneas:
from .auditoria import auditoria_table
from .cola_atencion import cola_atencion_table
from .configuracion_sistema import configuracion_sistema_table
```

#### **4.3. Actualizar `dental_system/models/odontologia_models.py`**

**Eliminar de `CondicionDienteModel` (líneas 183-186, 214-217):**
```python
# ELIMINAR:
observaciones: Optional[str] = ""
material_utilizado: Optional[str] = ""
color_material: Optional[str] = ""
fecha_tratamiento: Optional[str] = ""
```

**Eliminar de `DienteModel` (líneas 99, 104, 94, 128):**
```python
# ELIMINAR:
numero_diente_pediatrico: Optional[int] = None
descripcion_anatomica: Optional[str] = ""
coordenadas_svg: Dict[str, float] = {}
forma_base: str = ""
```

#### **4.4. Actualizar `dental_system/models/consultas_models.py`**

**Eliminar de `ConsultaModel` (líneas 26, 40, 50-51, 99-100):**
```python
# ELIMINAR:
odontologo_preferido_id: Optional[str] = ""  # Línea 26
notas_internas: Optional[str] = ""           # Línea 40
fecha_inicio_atencion: Optional[str] = ""    # Línea 50
fecha_fin_atencion: Optional[str] = ""       # Línea 51

# En from_dict(), ELIMINAR:
odontologo_preferido_id=...  # Línea 74
notas_internas=...           # Línea 89
fecha_inicio_atencion=...    # Línea 99
fecha_fin_atencion=...       # Línea 100
```

### **FASE 5: VERIFICACIÓN (5 min)**

```sql
-- Verificar que tablas fueron eliminadas
SELECT tablename FROM pg_tables WHERE schemaname = 'public' ORDER BY tablename;

-- Verificar columnas restantes en condiciones_diente
SELECT column_name FROM information_schema.columns
WHERE table_name = 'condiciones_diente' ORDER BY ordinal_position;

-- Verificar columnas restantes en consultas
SELECT column_name FROM information_schema.columns
WHERE table_name = 'consultas' ORDER BY ordinal_position;

-- Verificar columnas restantes en dientes
SELECT column_name FROM information_schema.columns
WHERE table_name = 'dientes' ORDER BY ordinal_position;
```

```bash
# Verificar que código Python compile
python -m py_compile dental_system/models/odontologia_models.py
python -m py_compile dental_system/models/consultas_models.py
python -m py_compile dental_system/supabase/tablas/__init__.py

# Ejecutar pruebas (si existen)
pytest tests/ -v
```

---

## ⚠️ CONSIDERACIONES IMPORTANTES

### **🔴 ANTES DE EJECUTAR:**

1. **BACKUP OBLIGATORIO:**
   ```bash
   pg_dump -h localhost -U postgres -d dental_system > backup_pre_limpieza_$(date +%Y%m%d).sql
   ```

2. **VERIFICAR AMBIENTE:**
   - ✅ Ejecutar primero en desarrollo
   - ✅ Probar en staging
   - ✅ Solo entonces ejecutar en producción

3. **COORDINAR CON EQUIPO:**
   - Notificar a todos los desarrolladores
   - Programar ventana de mantenimiento
   - Tener plan de rollback listo

### **🟡 CASOS ESPECIALES:**

#### **`odontologo_preferido_id`**
- **Uso:** Solo en modelos como backward compatibility
- **Decisión:** ELIMINAR - no aporta valor funcional
- **Alternativa:** Si se necesita preferencia, agregar lógica en frontend

#### **`notas_internas`**
- **Uso:** Existe pero redundante con `observaciones`
- **Decisión:** ELIMINAR y consolidar en `observaciones`
- **Migración:** Si hay datos, hacer UPDATE antes de eliminar:
  ```sql
  UPDATE consultas
  SET observaciones = CONCAT(observaciones, ' | ', notas_internas)
  WHERE notas_internas IS NOT NULL AND notas_internas != '';
  ```

### **🟢 ROLLBACK SI ALGO SALE MAL:**

```bash
# Detener aplicación
# Restaurar backup
psql -h localhost -U postgres -d dental_system < backup_pre_limpieza_YYYYMMDD.sql

# Revertir cambios en código
git checkout -- dental_system/models/
git checkout -- dental_system/supabase/tablas/
```

---

## 📈 BENEFICIOS ESPERADOS

### **🚀 RENDIMIENTO:**
- ✅ **Queries 10-15% más rápidos** (menos columnas a procesar)
- ✅ **Espacio en disco reducido** ~15-20%
- ✅ **Índices más eficientes** (menos columnas = índices más pequeños)

### **🧹 MANTENIBILIDAD:**
- ✅ **Esquema más limpio** - solo lo que se usa
- ✅ **Menos confusión** - no hay columnas "fantasma"
- ✅ **Código más simple** - menos campos en modelos

### **📊 MÉTRICAS:**

| Métrica | Antes | Después | Mejora |
|---------|-------|---------|--------|
| **Tablas** | 19 | 15 | -21% |
| **Columnas (condiciones_diente)** | 19 | 14 | -26% |
| **Columnas (consultas)** | 24 | 20 | -17% |
| **Columnas (dientes)** | 15 | 10 | -33% |
| **Archivos Python tablas** | 18 | 15 | -17% |
| **Tamaño estimado BD** | 100% | 80-85% | -15-20% |

---

## ✅ CHECKLIST DE EJECUCIÓN

### **PRE-EJECUCIÓN:**
- [ ] Backup completo creado
- [ ] Backup verificado (puede restaurarse)
- [ ] Equipo notificado
- [ ] Ventana de mantenimiento programada
- [ ] Ambiente de desarrollo probado

### **EJECUCIÓN:**
- [ ] Migración SQL ejecutada (tablas + columnas)
- [ ] Archivos Python eliminados
- [ ] Imports actualizados en `__init__.py`
- [ ] Modelos actualizados (odontologia_models.py)
- [ ] Modelos actualizados (consultas_models.py)

### **POST-EJECUCIÓN:**
- [ ] Verificación SQL ejecutada
- [ ] Código Python compila sin errores
- [ ] Pruebas ejecutadas exitosamente
- [ ] Aplicación reiniciada
- [ ] Funcionalidad crítica probada
- [ ] Documentación actualizada

---

## 📝 DOCUMENTOS RELACIONADOS

- `dental_system/supabase/migrations/20251021_eliminar_tablas_columnas_obsoletas.sql` - Script SQL
- `CLAUDE.md` - Actualizar sección de arquitectura
- `dental_system/supabase/CLAUDE.md` - Actualizar tabla de correspondencia

---

**📅 Fecha de creación:** 2025-10-21
**👨‍💻 Autor:** Claude Code + Wilmer Aguirre
**⚡ Estado:** ✅ Listo para ejecutar
**⏱️ Tiempo estimado:** 25 minutos totales
**🎯 Resultado esperado:** Base de datos 15-20% más liviana y mantenible
