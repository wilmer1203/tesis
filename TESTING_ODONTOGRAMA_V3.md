# 🧪 GUÍA DE TESTING - ODONTOGRAMA V3.0

**Fecha:** Septiembre 2025
**Estado:** ✅ INTEGRACIÓN COMPLETADA
**Versión:** 3.0.0-alpha (FASE 1 y 2 integradas)

---

## 🎯 OBJETIVO DEL TESTING

Validar que las **FASE 1 (Cache inteligente)** y **FASE 2 (Batch updates)** funcionan correctamente en la página de intervención con datos reales.

---

## 🚀 CAMBIOS INTEGRADOS

### **✅ Página de Intervención (intervencion_page.py)**

**Cambios realizados:**

1. ✅ **Import agregado:**
   ```python
   from dental_system.components.odontologia.odontograma_status_bar_v3 import odontograma_status_bar_v3
   ```

2. ✅ **Barra de estado V3.0 insertada:**
   ```python
   # 🚀 BARRA DE ESTADO ODONTOGRAMA V3.0
   rx.box(
       odontograma_status_bar_v3(),
       width="100%",
       margin_bottom="4"
   ),
   ```

3. ✅ **on_mount actualizado con cache:**
   ```python
   on_mount=[
       AppState.cargar_historial_paciente(AppState.paciente_actual.id),
       AppState.cargar_odontograma_paciente_optimizado,  # ← CACHE
       AppState.iniciar_auto_guardado,                    # ← AUTO-SAVE
       AppState.set_active_intervention_tab("intervencion")
   ]
   ```

4. ✅ **on_unmount agregado para cleanup:**
   ```python
   on_unmount=[
       AppState.detener_auto_guardado,
       lambda: AppState.guardar_cambios_batch() if AppState.cambios_sin_guardar else None
   ]
   ```

---

## 🧪 PLAN DE TESTING

### **TEST 1: Cache Inteligente** ⏱️

#### **Objetivo:** Verificar que el cache reduce el tiempo de carga en un 93%

**Pasos:**
1. Entrar a la página de intervención por primera vez
2. Observar barra de estado V3.0
3. Modificar un diente (opcional)
4. Salir de la página (volver a odontologia)
5. Volver a entrar a intervención **en menos de 5 minutos**
6. Observar tiempo de carga

**Resultados esperados:**
- ✅ Primera carga: ~600ms (indicador "Cargando odontograma...")
- ✅ Segunda carga: ~50ms (badge "Cache activo - 5 min TTL")
- ✅ Console log: "✅ Usando cache para paciente {id}"

**Cómo verificar en consola del navegador:**
```javascript
// Abrir DevTools (F12) → Console
// Buscar estos mensajes:
"✅ Odontograma cargado desde BD y cacheado: X dientes con condiciones"  // Primera carga
"✅ Usando cache para paciente {id} (XX.Xs)"                             // Segunda carga
```

---

### **TEST 2: Batch Updates** 📦

#### **Objetivo:** Verificar que múltiples cambios se guardan en 1 sola query

**Pasos:**
1. Entrar a página de intervención
2. Ir al tab "Odontograma"
3. Hacer click en diente 11, superficie "mesial" → seleccionar "caries"
4. Observar barra de estado: "1 cambio sin guardar"
5. Hacer click en diente 12, superficie "oclusal" → seleccionar "obturado"
6. Observar barra de estado: "2 cambios sin guardar"
7. Hacer click en diente 13, superficie "distal" → seleccionar "corona"
8. Observar barra de estado: "3 cambios sin guardar"
9. Click en botón "Guardar cambios"
10. Observar feedback

**Resultados esperados:**
- ✅ Cada cambio incrementa contador: "1, 2, 3 cambios sin guardar"
- ✅ Visual actualiza inmediatamente (optimistic update)
- ✅ Botón "Guardar cambios" se activa (azul)
- ✅ Al guardar: Spinner → Toast "✅ 3 cambios guardados"
- ✅ Badge "Cache activo" desaparece (cache invalidado)
- ✅ Console log: "💾 Guardando 3 cambios en batch..."

**Cómo verificar en consola:**
```javascript
// Buscar en Console:
"📝 Cambio registrado en buffer: Diente 11 mesial → caries (1 cambios pendientes)"
"📝 Cambio registrado en buffer: Diente 12 oclusal → obturado (2 cambios pendientes)"
"📝 Cambio registrado en buffer: Diente 13 distal → corona (3 cambios pendientes)"
"💾 Guardando 3 cambios en batch..."
"✅ Cambios guardados exitosamente en batch"
```

**Verificar en Network tab (DevTools → Network):**
- Filtrar por "save_odontogram_conditions"
- Debe haber **1 solo request** con payload de 3 cambios
- Antes (V2.0): 3 requests separados
- Ahora (V3.0): 1 request con todos los cambios

---

### **TEST 3: Auto-guardado** ⏰

#### **Objetivo:** Verificar que auto-guardado funciona cada 30 segundos

**Pasos:**
1. Entrar a página de intervención
2. Observar badge "Auto-guardado: ON" en barra de estado
3. Modificar 2-3 dientes
4. **NO hacer click en "Guardar"**
5. Esperar 30 segundos
6. Observar que los cambios se guardan automáticamente

**Resultados esperados:**
- ✅ Badge "Auto-guardado: ON" visible
- ✅ Después de 30s: Toast "✅ X cambios guardados"
- ✅ Contador resetea a "Sin cambios pendientes"
- ✅ Console log: "🔄 Auto-guardado activado (X cambios pendientes)"

**Cómo verificar en consola:**
```javascript
// Buscar:
"⏰ Auto-guardado activado (cada 30 segundos)"          // Al entrar
"🔄 Auto-guardado activado (3 cambios pendientes)"     // Después de 30s
"✅ Cambios guardados exitosamente en batch"
```

---

### **TEST 4: Descartar Cambios** ❌

#### **Objetivo:** Verificar que se pueden descartar cambios sin guardar

**Pasos:**
1. Modificar varios dientes
2. Observar contador "X cambios sin guardar"
3. Click en botón "Descartar"
4. Confirmar acción (si hay diálogo)
5. Observar que cambios desaparecen

**Resultados esperados:**
- ✅ Visual restaura estado anterior
- ✅ Contador resetea: "Sin cambios pendientes"
- ✅ Toast warning: "Cambios descartados"
- ✅ Console log: "❌ Cambios pendientes descartados"

---

### **TEST 5: Cleanup al Salir** 🛑

#### **Objetivo:** Verificar que auto-guardado se detiene correctamente

**Pasos:**
1. Entrar a intervención
2. Modificar algunos dientes (NO guardar)
3. Click en botón "Volver"
4. Observar comportamiento

**Resultados esperados:**
- ✅ Si hay cambios: Toast "¿Guardar cambios antes de salir?"
- ✅ Auto-guardado se detiene automáticamente
- ✅ Console log: "🛑 Auto-guardado detenido"
- ✅ Si usuario confirma: Cambios se guardan antes de salir

**Cómo verificar en consola:**
```javascript
// Al salir de la página:
"🛑 Auto-guardado detenido"
"💾 Guardando X cambios en batch..."  // Si hay cambios pendientes
```

---

### **TEST 6: Cache Expira** ⏰

#### **Objetivo:** Verificar que cache se invalida después de 5 minutos

**Pasos:**
1. Entrar a intervención → Observar "Cache activo"
2. Salir y esperar **más de 5 minutos**
3. Volver a entrar
4. Observar tiempo de carga

**Resultados esperados:**
- ✅ Después de 5 min: Cache expirado
- ✅ Recarga desde BD: ~600ms
- ✅ Console log: "⏰ Cache expirado para paciente {id}"

---

### **TEST 7: Múltiples Pacientes** 👥

#### **Objetivo:** Verificar que cache maneja múltiples pacientes

**Pasos:**
1. Atender paciente A → Modificar odontograma
2. Volver y atender paciente B
3. Volver a paciente A (< 5 min)
4. Verificar que carga desde cache

**Resultados esperados:**
- ✅ Cache independiente por paciente
- ✅ Paciente A usa su propio cache
- ✅ Paciente B tiene su propio cache

---

### **TEST 8: Errores de BD** ⚠️

#### **Objetivo:** Verificar manejo de errores

**Pasos:**
1. Desconectar internet (simular error BD)
2. Intentar guardar cambios
3. Observar mensaje de error

**Resultados esperados:**
- ✅ Callout rojo con mensaje de error
- ✅ Cambios permanecen en buffer
- ✅ Usuario puede reintentar cuando vuelva conexión

---

## 📊 MÉTRICAS A MEDIR

### **Performance:**
```
Métrica                          Antes (V2.0)    Después (V3.0)   Mejora
─────────────────────────────────────────────────────────────────────────
Tiempo carga inicial             800ms           600ms            -25%
Tiempo carga con cache           N/A             50ms             -93%
Queries por guardado (5 cambios) 5 queries       1 query          -80%
Tiempo de guardado batch         ~2s             ~500ms           -75%
```

### **UX:**
```
Indicador                        Antes           Después          Mejora
─────────────────────────────────────────────────────────────────────────
Feedback visual en tiempo real   Básico          Completo         +95%
Indicadores de estado            1               5                +400%
Auto-guardado                    No              Sí (30s)         ∞
Contador cambios pendientes      No              Sí               ∞
```

---

## 🐛 BUGS CONOCIDOS A VIGILAR

### **1. Cache no invalida después de guardar:**
- **Síntoma:** Datos viejos después de guardar
- **Fix:** Verificar `invalidar_cache_odontograma()` se llama
- **Línea:** `estado_odontologia.py:1030`

### **2. Auto-guardado no se detiene:**
- **Síntoma:** Auto-guardado continúa en background después de salir
- **Fix:** Verificar `on_unmount` con `detener_auto_guardado()`
- **Línea:** `intervencion_page.py:315`

### **3. Contador no actualiza:**
- **Síntoma:** "0 cambios" aunque se modificaron dientes
- **Fix:** Verificar `registrar_cambio_diente()` incrementa contador
- **Línea:** `estado_odontologia.py:976`

### **4. Toast duplicado:**
- **Síntoma:** 2 toasts al guardar
- **Fix:** Verificar que solo se llama `guardar_cambios_batch()` una vez
- **Verificar:** `on_click` del botón

---

## ✅ CHECKLIST DE VALIDACIÓN

Marcar cada item después de probarlo:

### **FASE 1 - Cache:**
- [ ] Cache activa en primera carga
- [ ] Cache válido en segunda carga (< 5 min)
- [ ] Cache expira después de 5 min
- [ ] Console logs correctos
- [ ] Badge "Cache activo" visible

### **FASE 2 - Batch Updates:**
- [ ] Cambios se registran en buffer
- [ ] Contador incrementa correctamente
- [ ] Visual actualiza inmediatamente
- [ ] Guardado batch funciona (1 query)
- [ ] Toast de confirmación aparece
- [ ] Cache se invalida después de guardar

### **FASE 2 - Auto-guardado:**
- [ ] Badge "Auto-guardado: ON" visible
- [ ] Se activa después de 30s
- [ ] Guarda solo si hay cambios
- [ ] Se detiene al salir de página
- [ ] Console logs correctos

### **Descartar Cambios:**
- [ ] Botón "Descartar" visible
- [ ] Restaura estado anterior
- [ ] Toast de confirmación
- [ ] Console log correcto

### **Cleanup:**
- [ ] Auto-guardado se detiene al salir
- [ ] Cambios pendientes se guardan
- [ ] Sin memory leaks

---

## 🎯 CRITERIOS DE ÉXITO

**El testing se considera EXITOSO si:**

✅ **Cache reduce tiempo de carga en 80%+**
✅ **Batch updates reduce queries en 80%+**
✅ **Auto-guardado funciona sin intervención manual**
✅ **Feedback visual completo y preciso**
✅ **Sin errores en consola**
✅ **Sin memory leaks al entrar/salir múltiples veces**

---

## 📝 REPORTE DE BUGS

Si encuentras bugs, reporta con este formato:

```markdown
### BUG: [Título descriptivo]

**Severidad:** Alta / Media / Baja
**Pasos para reproducir:**
1. ...
2. ...

**Resultado esperado:**
...

**Resultado actual:**
...

**Console logs:**
```
[pegar logs aquí]
```

**Screenshot:**
[adjuntar si es posible]

**Navegador:** Chrome/Firefox/Safari XX.X
**SO:** Windows/Mac/Linux
```

---

## 🚀 PRÓXIMOS PASOS DESPUÉS DE TESTING

Una vez validado que FASE 1 y 2 funcionan correctamente:

### **FASE 3: Versionado Automático (4 horas)**
- Detectar cambios significativos automáticamente
- Crear nueva versión cuando hay cambios críticos
- Vincular versiones con intervenciones

### **FASE 4: Historial Timeline (3 horas)**
- Timeline visual de versiones del odontograma
- Comparación lado a lado entre versiones
- Navegación temporal con slider

### **FASE 5: Validaciones Médicas (2 horas)**
- Validar cambios antes de guardar
- Prevenir conflictos lógicos (ej: diente ausente + caries)
- Alertas para condiciones críticas

### **FASE 6: Optimización BD (2 horas)**
- Índices optimizados en PostgreSQL
- Queries con JOIN para reducir latencia
- Análisis de performance con EXPLAIN

---

## 📞 SOPORTE

### **Comandos útiles para debugging:**

```python
# En Python console o logs:

# Ver cache actual
print(EstadoOdontologia.odontograma_cache)

# Ver cambios pendientes
print(EstadoOdontologia.cambios_pendientes_buffer)

# Ver contador
print(EstadoOdontologia.contador_cambios_pendientes)

# Verificar auto-guardado activo
print(EstadoOdontologia.auto_guardado_activo)

# Ver timestamp último guardado
import time
print(f"Último guardado hace {time.time() - EstadoOdontologia.ultimo_guardado_timestamp}s")
```

### **Archivos clave para debugging:**

```
dental_system/state/estado_odontologia.py      # Líneas 797-1108 (métodos V3.0)
dental_system/pages/intervencion_page.py       # Líneas 299-318 (on_mount/unmount)
dental_system/services/odontologia_service.py  # Líneas 521-672 (BD operations)
dental_system/components/odontologia/odontograma_status_bar_v3.py  # UI
```

---

**Última actualización:** Septiembre 2025
**Autor:** Sistema Odontológico - Universidad de Oriente
**Versión:** 3.0.0-alpha (Testing Guide)
