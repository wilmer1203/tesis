# 🚀 INSTRUCCIONES: MIGRACIÓN A ODONTOGRAMA PLANO

**Fecha:** 2025-10-07
**Objetivo:** Simplificar sistema de odontograma eliminando complejidad innecesaria
**Tiempo estimado:** 30 minutos

---

## ✅ **QUÉ SE VA A LOGRAR**

### **ANTES (Complejo):**
```
pacientes
    ↓
odontograma (con versiones, es_version_actual, etc.)
    ↓
condiciones_diente
    ↓
dientes (catálogo FDI)
```

**Queries:** 3-4 joins, filtros complejos
**Crear paciente:** Manual, odontograma no se crea automáticamente
**Historial:** Sistema de versiones no utilizado

---

### **DESPUÉS (Simple):**
```
pacientes → condiciones_diente (directo)
```

**Queries:** 1 tabla, filtro simple `activo = true`
**Crear paciente:** ✨ **AUTO-CREA 160 condiciones "sano" vía trigger SQL**
**Historial:** Campo `activo` (true = actual, false = histórico)

---

## 📋 **PASO A PASO**

### **PASO 1: RESPALDAR BASE DE DATOS** ⚠️

```bash
# Desde terminal/PowerShell
npx supabase db dump -f backup_antes_migracion_$(date +%Y%m%d).sql
```

O desde interfaz web de Supabase:
1. Dashboard → Database → Backups
2. Create backup → "Pre-migración odontograma plano"

---

### **PASO 2: EJECUTAR SCRIPT DE MIGRACIÓN**

Tienes 2 opciones:

#### **OPCIÓN A: Desde Supabase Dashboard (Recomendado)**

1. Ir a Supabase Dashboard → SQL Editor
2. Abrir archivo `dental_system/supabase/migrations/20251007_simplificar_odontograma_plano.sql`
3. Copiar TODO el contenido
4. Pegar en SQL Editor
5. Click en **Run**
6. Verificar mensajes de NOTICE (debe decir "MIGRACIÓN COMPLETADA EXITOSAMENTE")

#### **OPCIÓN B: Desde CLI de Supabase**

```bash
cd c:\Users\wilme\Documents\tesis-main
npx supabase db push --include-all
```

---

### **PASO 3: VERIFICAR MIGRACIÓN**

Ejecutar queries de verificación en SQL Editor:

```sql
-- 1. Verificar que tabla odontograma ya no existe
SELECT table_name
FROM information_schema.tables
WHERE table_name = 'odontograma';
-- Debe retornar: 0 filas

-- 2. Verificar nueva estructura de condiciones_diente
\d condiciones_diente;
-- Debe tener columnas: paciente_id, diente_numero, superficie, activo

-- 3. Verificar trigger de auto-creación
SELECT trigger_name, event_manipulation, event_object_table
FROM information_schema.triggers
WHERE trigger_name = 'trigger_crear_odontograma_inicial';
-- Debe mostrar: AFTER INSERT en tabla pacientes

-- 4. Verificar datos migrados
SELECT COUNT(*) FROM condiciones_diente WHERE activo = TRUE;
-- Debe mostrar cantidad de condiciones actuales migradas

-- 5. Ver estadísticas por paciente
SELECT
    paciente_id,
    COUNT(*) as total_condiciones,
    COUNT(*) FILTER (WHERE activo = TRUE) as activas,
    COUNT(*) FILTER (WHERE activo = FALSE) as historicas
FROM condiciones_diente
GROUP BY paciente_id;
```

---

### **PASO 4: ACTUALIZAR CÓDIGO PYTHON**

#### **4.1 Actualizar imports en `estado_odontologia.py`**

```python
# ANTES:
from dental_system.services.odontologia_service import odontologia_service

# DESPUÉS:
from dental_system.services.odontologia_service_v2_plano import odontologia_service_v2 as odontologia_service
```

#### **4.2 Actualizar método de carga en `estado_odontologia.py`**

Buscar método `cargar_odontograma_paciente_actual()` y simplificar:

```python
async def cargar_odontograma_paciente_actual(self):
    """📋 Cargar odontograma actual del paciente seleccionado"""
    try:
        if not self.paciente_actual_id:
            return

        self.odontograma_cargando = True

        # SIMPLIFICADO: Solo un método
        result = await odontologia_service.get_patient_odontogram(
            self.paciente_actual_id
        )

        # Asignar condiciones
        self.condiciones_por_diente = result["conditions"]
        self.odontograma_actual_id = self.paciente_actual_id  # Ahora es el mismo ID

        self.odontograma_cargando = False
        logger.info(f"✅ Odontograma cargado: {result['total_condiciones']} condiciones")

    except Exception as e:
        logger.error(f"❌ Error cargando odontograma: {e}")
        self.odontograma_cargando = False
```

#### **4.3 Actualizar método de guardado**

```python
async def guardar_cambios_odontograma(self):
    """💾 Guardar cambios del odontograma"""
    try:
        if not self.cambios_sin_guardar:
            return

        self.odontograma_guardando = True

        # Obtener intervención actual
        intervencion_id = self.intervencion_actual_id if hasattr(self, 'intervencion_actual_id') else None

        # SIMPLIFICADO: Actualizar cada cambio
        for diente_num, superficies in self.condiciones_por_diente.items():
            for superficie, condicion_data in superficies.items():
                await odontologia_service.actualizar_condicion_diente(
                    paciente_id=self.paciente_actual_id,
                    diente_numero=diente_num,
                    superficie=superficie,
                    nueva_condicion=condicion_data["condicion"],
                    intervencion_id=intervencion_id,
                    material=condicion_data.get("material")
                )

        self.cambios_sin_guardar = False
        self.odontograma_guardando = False
        self.mostrar_toast("Odontograma guardado correctamente", "success")

    except Exception as e:
        logger.error(f"❌ Error guardando odontograma: {e}")
        self.odontograma_guardando = False
        self.mostrar_toast(f"Error: {str(e)}", "error")
```

---

### **PASO 5: PROBAR CREACIÓN AUTOMÁTICA**

#### **5.1 Crear paciente de prueba**

Desde la interfaz del sistema:
1. Ir a módulo Pacientes
2. Crear nuevo paciente: "Prueba Migración"
3. Guardar

#### **5.2 Verificar auto-creación en BD**

```sql
-- Buscar el paciente recién creado
SELECT id, numero_historia, nombres, apellidos
FROM pacientes
WHERE nombres ILIKE '%Prueba%'
ORDER BY created_at DESC
LIMIT 1;

-- Copiar el ID y verificar condiciones
SELECT
    diente_numero,
    COUNT(*) as superficies,
    tipo_condicion
FROM condiciones_diente
WHERE paciente_id = '<ID_DEL_PACIENTE_DE_PRUEBA>'
  AND activo = TRUE
GROUP BY diente_numero, tipo_condicion;

-- Debe mostrar:
-- 32 dientes × 5 superficies = 160 filas
-- Todas con tipo_condicion = 'sano'
```

#### **5.3 Probar desde interfaz**

1. Ir a Odontología
2. Seleccionar el paciente de prueba
3. Verificar que se muestra odontograma con todos los dientes en verde (sano)
4. Hacer un cambio: marcar diente 11 superficie oclusal como "caries"
5. Guardar
6. Recargar página y verificar que el cambio se mantuvo

---

## 🔧 **PASO 6: LIMPIEZA (OPCIONAL)**

Si todo funciona correctamente, eliminar archivos viejos:

```bash
# Renombrar archivo viejo (por si acaso)
mv dental_system/services/odontologia_service.py dental_system/services/odontologia_service_OLD_COMPLEJO.py

# Renombrar nuevo archivo
mv dental_system/services/odontologia_service_v2_plano.py dental_system/services/odontologia_service.py
```

También eliminar archivos de tabla `odontograma`:

```bash
# Estos ya no se usan
rm dental_system/supabase/tablas/odontograma.py
```

---

## ✅ **CHECKLIST DE VERIFICACIÓN**

Marcar cada ítem al completarlo:

- [ ] Backup de base de datos creado
- [ ] Script SQL ejecutado sin errores
- [ ] Verificado que tabla `odontograma` fue eliminada
- [ ] Verificado que `condiciones_diente` tiene nueva estructura
- [ ] Trigger `trigger_crear_odontograma_inicial` existe
- [ ] Función `actualizar_condicion_diente()` existe
- [ ] Vista `vista_odontograma_actual` existe
- [ ] Código Python actualizado (imports y métodos)
- [ ] Creado paciente de prueba
- [ ] Verificado auto-creación de 160 condiciones "sano"
- [ ] Probado cargar odontograma desde interfaz
- [ ] Probado actualizar condición desde interfaz
- [ ] Probado historial de diente
- [ ] Limpieza de archivos viejos (opcional)

---

## 🚨 **ROLLBACK (Si algo sale mal)**

### **Opción 1: Restaurar desde backup**

```bash
npx supabase db restore backup_antes_migracion_<fecha>.sql
```

### **Opción 2: Revertir manualmente**

```sql
-- Detener trigger
DROP TRIGGER IF EXISTS trigger_crear_odontograma_inicial ON pacientes;

-- Restaurar estructura vieja (necesitas el esquema anterior)
-- Ver archivo esquema_final_corregido.sql secciones odontograma
```

---

## 📊 **BENEFICIOS OBTENIDOS**

✅ **Reducción de complejidad:** 3 tablas → 1 tabla
✅ **Auto-creación:** Trigger crea odontograma automáticamente
✅ **Queries más simples:** Sin joins complejos
✅ **Historial completo:** Campo `activo` mantiene todo
✅ **Menos errores:** Arquitectura más clara
✅ **Mejor mantenibilidad:** Código más fácil de entender

---

## 📞 **SOPORTE**

Si encuentras problemas:
1. Revisar logs de Supabase (Dashboard → Database → Logs)
2. Revisar logs de Python (`logs/dental_system.log`)
3. Verificar mensajes de NOTICE en SQL Editor
4. Comparar con queries de verificación arriba

---

**¡Listo! Sistema simplificado y funcionando. 🎉**
