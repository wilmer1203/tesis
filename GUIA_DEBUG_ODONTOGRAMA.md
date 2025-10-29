# 🐛 GUÍA DE DEBUGGING - ACTUALIZACIÓN DE ODONTOGRAMA

## 📋 CÓMO USAR LOS LOGS

Ahora tienes **11 puntos de control** con logs super detallados. Aquí está cómo usarlos:

### 1. **Ejecuta una intervención:**
   - Login como odontólogo
   - Selecciona un paciente
   - Agrega un servicio (ej: Obturación Simple en diente 11, superficie oclusal)
   - **Finaliza la intervención**

### 2. **Revisa la consola de Reflex:**

Busca los siguientes puntos clave:

---

## 🔍 **PUNTO CRÍTICO 1: ¿Tiene condición el servicio?**

```
📦 [PUNTO 2] SERVICIOS ORIGINALES (antes de conversión):
  1. Obturación Simple
     - Condición resultante: obturacion  ← DEBE TENER VALOR
```

**SI DICE `None` O `NULL`:**
- El servicio NO tiene `condicion_resultante` configurado
- Ejecuta: `python ejecutar_migracion_condicion_resultante.py`

---

## 🔍 **PUNTO CRÍTICO 2: ¿Se filtra como activo?**

```
🔍 [PUNTO 8] FILTRANDO SERVICIOS ACTIVOS
  Servicio 1: Obturación Simple
    - Condición: obturacion
    - Diente: 11
    ✅ ACTIVO (modifica odontograma)  ← DEBE DECIR "ACTIVO"
```

**SI DICE `⚠️ PREVENTIVO`:**
- La condición es NULL o el diente es NULL
- El servicio NO modificará el odontograma
- Revisa el PUNTO 2 para ver qué dato falta

---

## 🔍 **PUNTO CRÍTICO 3: ¿Se generan actualizaciones?**

```
📦 TOTAL ACTUALIZACIONES PREPARADAS: 1  ← DEBE SER > 0

📋 DETALLE DE ACTUALIZACIONES QUE SE ENVIARÁN A SQL:
  1. Diente #11, superficie: oclusal
     → Condición: obturacion
```

**SI DICE `0 ACTUALIZACIONES`:**
- Los servicios son todos preventivos
- O no pasaron el filtro de activos
- Revisa el PUNTO 2 para confirmar que tienen `condicion_resultante`

---

## 🔍 **PUNTO CRÍTICO 4: ¿La BD responde exitosamente?**

```
📥 RESPUESTA DE SQL:
  - Exitosos: 1  ← DEBE SER igual al total
  - Fallidos: 0  ← DEBE SER 0
  - Tasa éxito: 100.0%
```

**SI DICE `Exitosos: 0` o `Fallidos > 0`:**
- Hay un error en la función SQL
- Ejecuta: `python verificar_funcion_batch.py`
- Si la función NO EXISTE, ejecuta `crear_funcion_batch.sql` en Supabase Studio

---

## ❌ **ERRORES COMUNES Y SOLUCIONES:**

### ERROR 1: "Todos los servicios son preventivos"
```
⚠️ TODOS LOS SERVICIOS SON PREVENTIVOS - NO HAY NADA QUE ACTUALIZAR
```
**CAUSA:** Servicios no tienen `condicion_resultante` configurado
**SOLUCIÓN:** Ejecuta `python ejecutar_migracion_condicion_resultante.py`

---

### ERROR 2: "Función actualizar_condiciones_batch no existe"
```
Could not find the function public.actualizar_condiciones_batch
```
**CAUSA:** Función SQL no está creada
**SOLUCIÓN:**
1. Abre Supabase Studio (http://localhost:54323)
2. Ve a SQL Editor
3. Ejecuta el archivo `crear_funcion_batch.sql`

---

### ERROR 3: "Exitosos: 0, Fallidos: X"
```
📥 RESPUESTA DE SQL:
  - Exitosos: 0
  - Fallidos: 1
```
**CAUSA:** Error en los datos enviados a SQL
**SOLUCIÓN:**
1. Revisa el PUNTO 10 (DETALLE DE ACTUALIZACIONES)
2. Verifica que `paciente_id`, `diente_numero`, `superficie`, `tipo_condicion` NO sean NULL
3. Revisa logs de PostgreSQL en Supabase Studio

---

## ✅ **FLUJO EXITOSO (EJEMPLO):**

```
[PUNTO 1] INICIO FINALIZAR INTERVENCIÓN
  ✓ Consulta ID: abc123
  ✓ Paciente ID: def456
  ✓ Odontólogo ID: ghi789

[PUNTO 2] SERVICIOS ORIGINALES
  ✓ Condición resultante: obturacion

[PUNTO 8] FILTRANDO SERVICIOS ACTIVOS
  ✓ ACTIVO (modifica odontograma)
  ✓ Servicios activos: 1

[PUNTO 10] PREPARANDO ACTUALIZACIONES
  ✓ TOTAL ACTUALIZACIONES PREPARADAS: 1
  ✓ Diente #11, oclusal → obturacion

[PUNTO 11] EJECUTANDO BATCH SQL
  ✓ Exitosos: 1
  ✓ Fallidos: 0
  ✓ Tasa éxito: 100%
```

---

## 🛠️ **VERIFICACIÓN POST-INTERVENCIÓN:**

Después de finalizar, ejecuta en Supabase Studio:

```sql
SELECT
    diente_numero,
    superficie,
    tipo_condicion,
    activo,
    fecha_registro,
    intervencion_id
FROM condiciones_diente
WHERE activo = TRUE
  AND paciente_id = 'TU_PACIENTE_ID'
ORDER BY fecha_registro DESC;
```

Deberías ver la nueva condición con:
- `activo = TRUE`
- `tipo_condicion = 'obturacion'` (o la que corresponda)
- `intervencion_id` vinculado a tu intervención

---

## 📞 **SI SIGUE SIN FUNCIONAR:**

Comparte en el chat:
1. Los logs completos de los 11 PUNTOS
2. El resultado de: `SELECT * FROM servicios WHERE id = 'ID_DEL_SERVICIO_QUE_USASTE';`
3. El resultado de: `python verificar_funcion_batch.py`

**Última actualización:** 2025-01-10
