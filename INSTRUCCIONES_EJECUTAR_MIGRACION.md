# INSTRUCCIONES PARA RESOLVER PROBLEMA DE ACTUALIZACIÓN DE ODONTOGRAMA

## PROBLEMA

Cuando finalizas una intervención como odontólogo, **las condiciones del diente NO se están actualizando**.

## CAUSA RAÍZ

La función SQL `actualizar_condiciones_batch()` **NO EXISTE** en la base de datos.

## SOLUCIÓN

### OPCIÓN 1: Supabase Studio (RECOMENDADO - MÁS FÁCIL)

1. **Abre Supabase Studio:**
   - Visita: http://localhost:54323
   - Login: `postgres` / `2024Belu$`

2. **Ve a SQL Editor:**
   - En el menú lateral izquierdo, haz clic en "SQL Editor"

3. **Ejecuta el script:**
   - Haz clic en "+ New query"
   - Copia TODO el contenido del archivo: `crear_funcion_batch.sql`
   - Pega en el editor
   - Haz clic en "RUN" (botón verde)

4. **Verifica el resultado:**
   - Deberías ver: "Success. No rows returned"
   - Eso significa que la función se creó correctamente

### OPCIÓN 2: Línea de comandos (Alternativa)

Si tienes `psql` instalado:

```bash
psql "postgresql://postgres:2024Belu$@localhost:54322/postgres" -f crear_funcion_batch.sql
```

## VERIFICACIÓN

Después de ejecutar el SQL, verifica que funcionó:

```bash
python verificar_funcion_batch.py
```

Deberías ver:
```
OK: Función actualizar_condiciones_batch existe y funciona
```

## FLUJO COMPLETO DE ACTUALIZACIÓN

Una vez que la función exista, el flujo funciona así:

```
1. Usuario finaliza intervención
   ↓
2. finalizar_mi_intervencion_odontologo()
   ↓
3. crear_intervencion_con_servicios() → Guarda en BD
   ↓
4. _actualizar_odontograma_por_servicios() → Actualiza condiciones
   ↓
5. actualizar_condiciones_batch() (SQL) → Ejecuta UPDATE en BD
   ↓
6. Condiciones actualizadas en tabla condiciones_diente
```

## IMPORTANTE

Cada servicio debe tener configurado `condicion_resultante` en el catálogo:

- **Obturación** → `condicion_resultante = 'obturacion'`
- **Extracción** → `condicion_resultante = 'ausente'`
- **Endodoncia** → `condicion_resultante = 'endodoncia'`
- **Corona** → `condicion_resultante = 'corona'`
- **Servicios preventivos** (limpieza, blanqueamiento) → `condicion_resultante = NULL`

Esto ya fue configurado con el script `ejecutar_migracion_condicion_resultante.py`.

## PRUEBA

1. Ejecuta el SQL en Supabase Studio
2. Verifica con: `python verificar_funcion_batch.py`
3. Inicia una intervención como odontólogo
4. Agrega un servicio (ej: Obturación en diente 11)
5. Finaliza la intervención
6. Verifica en Supabase Studio que la condición del diente se actualizó:

```sql
SELECT * FROM condiciones_diente
WHERE activo = TRUE
ORDER BY fecha_registro DESC
LIMIT 10;
```

## LOGS PARA DEBUG

Si aún no funciona, revisa los logs de Python para ver dónde falla:

```python
# En estado_intervencion_servicios.py línea 498
# Se llama a _actualizar_odontograma_por_servicios()

# Busca en consola mensajes como:
# "V4.0 Iniciando actualización odontograma"
# "Servicios activos: X/Y"
# "Batch completado | Exitosos: X | Fallidos: Y"
```

---

**Última actualización:** 2025-01-10
**Estado:** Listo para ejecutar
