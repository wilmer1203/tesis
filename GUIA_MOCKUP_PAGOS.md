# 🎨 GUÍA: MOCKUP DEL MÓDULO DE PAGOS

## 📋 ¿Qué se ha creado?

### Archivos nuevos:

```
dental_system/pages/mockup/
├── __init__.py
├── mock_data_pagos.py          # Datos estáticos variados y realistas
├── pagos_page_mockup.py        # UI completa con componentes visuales (versión original)
└── pagos_page_mockup_v2.py     # ✨ UI V2.0 HÍBRIDA (React + Reflex + Dual USD/BS)
```

---

## 🚀 CÓMO PROBAR EL MOCKUP

### 1. **Iniciar el servidor de desarrollo**

```bash
cd C:\Users\wilme\Documents\tesis-main
reflex run
```

### 2. **Acceder a los mockups en el navegador**

#### **Versión Original (Simple):**
```
http://localhost:3000/pagos-mockup
```

#### **✨ Versión V2.0 Híbrida (RECOMENDADA):**
```
http://localhost:3000/pagos-mockup-v2
```

**✅ No requieren login**, son páginas independientes para ver el diseño.

---

## 🎨 LO QUE VAS A VER

### **✨ NUEVO EN V2.0 HÍBRIDA:**

La versión V2.0 combina lo mejor del template React con nuestro sistema dual USD/BS:

#### **🎯 Layout Mejorado (5/7 ratio):**
- **Columna Izquierda (5/12):** Lista compacta de consultas pendientes + acciones rápidas
- **Columna Derecha (7/12):** Formulario completo de pago dual USD/BS

#### **💰 Formulario de Pago Completo:**
- ✅ **Sección 1:** Montos totales a pagar (USD + BS)
- ✅ **Sección 2:** Configuración pago dual:
  - Monto a pagar en USD + método de pago USD
  - Monto a pagar en BS + método de pago BS
  - Auto-cálculo de equivalencias entre monedas
- ✅ **Sección 3:** Descuentos opcionales con justificación
- ✅ **Sección 4:** Notas y observaciones
- ✅ **Sección 5:** Resumen final con breakdown detallado

#### **📊 Estadísticas con Tendencias:**
- Indicadores de cambio (▲ +15.2%, ▼ -5%, — sin cambios)
- Colores por tipo de tendencia
- Hover effects mejorados

#### **🔍 Filtros Avanzados Plegables:**
- Búsqueda rápida
- Rango de fechas
- Estado (pendiente/completado/parcial)
- Método de pago
- Botones limpiar/aplicar filtros

#### **⚡ Acciones Rápidas:**
- Nueva factura
- Reporte del día
- Imprimir recibos
- Exportar a Excel

---

### **Versión Original - LO QUE VAS A VER:**

### **Estadísticas Superiores (4 cards):**
- 📊 Consultas pendientes de facturación
- 💵 Recaudación del día en USD
- 💰 Recaudación del día en BS
- 📈 Tasa de cambio (editable)

### **Columna Izquierda: Consultas Pendientes**
- ✅ **8 consultas variadas** con diferentes características:
  - Consultas del día (0 días pendientes)
  - Consultas atrasadas (1-5 días)
  - Diferentes rangos de precio ($35 - $400)
  - Diferentes cantidades de servicios (1-5)
  - Badges de prioridad (normal/alta)
- ✅ **Servicios expandibles** al hacer clic
- ✅ **Detalles completos:**
  - Número de consulta
  - Paciente (nombre + documento)
  - Odontólogo asignado
  - Lista de servicios con precios
  - Total en USD y BS
  - Botón FACTURAR

### **Columna Derecha: Historial de Pagos**
- ✅ **10 pagos procesados** con diferentes estados:
  - Completados (USD, BS, mixtos)
  - Pendientes (pagos parciales)
- ✅ **Información detallada:**
  - Número de recibo (REC2025100001...)
  - Paciente
  - Concepto
  - Montos en USD y BS
  - Estado con badge de color
  - Fecha de pago
- ✅ **Búsqueda** (input funcional en el futuro)
- ✅ **Scroll** si hay muchos pagos

---

## 📊 DATOS INCLUIDOS EN EL MOCKUP

### **Consultas Pendientes (8 casos):**

1. **CONS-20251020001** - Juan Pérez
   - 3 servicios: Limpieza + Extracción + Radiografía
   - Total: $120 USD / 4,380 BS
   - Hoy, prioridad normal

2. **CONS-20251019005** - María López
   - 2 servicios: Obturación + Consulta
   - Total: $100 USD / 3,650 BS
   - 1 día pendiente

3. **CONS-20251015002** - Pedro Gómez
   - 2 servicios: Endodoncia + Corona
   - Total: $400 USD / 14,600 BS
   - **5 días pendiente (PRIORIDAD ALTA)**

4. **CONS-20251020003** - Carolina Martínez
   - 1 servicio: Blanqueamiento
   - Total: $150 USD / 5,475 BS
   - Hoy

5. **CONS-20251018010** - Roberto Ramírez
   - 3 servicios: Limpieza + Flúor + Sellantes
   - Total: $120 USD / 4,380 BS
   - 2 días pendiente

6. **CONS-20251020006** - Sofía Herrera
   - 4 servicios: Consulta ortodoncia + evaluaciones
   - Total: $145 USD / 5,292.50 BS
   - Hoy

7. **CONS-20251019012** - Daniel Moreno
   - 1 servicio: Emergencia
   - Total: $35 USD / 1,277.50 BS
   - 1 día pendiente

8. **CONS-20251017004** - Valentina Reyes
   - 5 servicios: Cirugía periodontal completa
   - Total: $268 USD / 9,782 BS
   - 3 días pendiente

### **Pagos en Historial (10 casos):**

- **REC2025100001**: Completado, solo USD ($95), efectivo
- **REC2025100002**: Completado, solo BS (2,920), transferencia
- **REC2025100003**: **Pendiente**, pago parcial mixto
- **REC2025100004**: Completado, mixto ($80 + 1,460 BS)
- **REC2025100005**: Completado, solo USD ($150), tarjeta
- **REC2025100006**: Completado, solo BS (2,190), pago móvil
- **REC2025100007**: **Pendiente**, pago inicial USD ($100 de $250)
- **REC2025100008**: Completado, alto valor ($450), transferencia
- **REC2025100009**: Completado, bajo valor (912.50 BS), efectivo
- **REC2025100010**: Completado, mixto con descuento

---

## 🔄 CÓMO MIGRAR A DATOS REALES

### **Paso 1: En cada componente, cambiar el import**

**ANTES (mockup):**
```python
from .mock_data_pagos import CONSULTAS_PENDIENTES_MOCK
```

**DESPUÉS (real):**
```python
# No import necesario, usar AppState directamente
```

### **Paso 2: Cambiar la fuente de datos**

**ANTES (mockup):**
```python
def consultas_pendientes_lista_mockup():
    consultas = CONSULTAS_PENDIENTES_MOCK
    return rx.vstack(
        *[consulta_card_mockup(c) for c in consultas]
    )
```

**DESPUÉS (real):**
```python
def consultas_pendientes_lista():
    return rx.vstack(
        rx.foreach(
            AppState.consultas_pendientes_facturacion,
            consulta_card
        )
    )
```

### **Paso 3: Agregar eventos de Reflex**

**ANTES (mockup):**
```python
rx.button("FACTURAR")  # Sin acción
```

**DESPUÉS (real):**
```python
rx.button(
    "FACTURAR",
    on_click=AppState.seleccionar_consulta_para_pago(consulta["consulta_id"])
)
```

---

## ✅ VENTAJAS DE ESTE ENFOQUE

1. **Iteración rápida de diseño**
   - Ver todos los casos visuales sin BD
   - Ajustar colores, espaciados, tamaños
   - Probar diferentes layouts

2. **Validación de estructura**
   - Los datos mock usan la misma estructura que los reales
   - Garantiza compatibilidad futura
   - IntelliSense completo

3. **Testing visual**
   - Ver cómo se comporta con muchos datos
   - Ver casos extremos (precios altos/bajos)
   - Ver estados diferentes (pendiente/completado)

4. **Migración trivial**
   - Solo cambiar fuente de datos
   - Componentes ya funcionan
   - Sin refactoring necesario

---

## 🎯 PRÓXIMOS PASOS

### **Ahora (Diseño):**
1. ✅ Ver el mockup en navegador
2. ✅ Ajustar colores, tamaños, espaciados
3. ✅ Iterar rápido en el diseño
4. ✅ Agregar/quitar elementos visuales

### **Después (Funcionalidad):**
1. Crear formulario de pago dual
2. Agregar modal de confirmación
3. Conectar eventos de click
4. Migrar a datos reales (cambiar 3-4 líneas)

---

## 🐛 TROUBLESHOOTING

### **Error: "Module not found"**
```bash
# Reiniciar el servidor
Ctrl+C
reflex run
```

### **Error: "Page not found"**
- Verificar que estás en: `http://localhost:3000/pagos-mockup`
- Verificar que el servidor está corriendo

### **No se ven los estilos**
- Los estilos están inline en el componente
- Si no se ven, recargar la página (F5)

---

## 📝 NOTAS IMPORTANTES

### **✅ Lo que funciona:**
- Visualización completa de UI
- Scroll en listas largas
- Hover effects
- Badges de estado
- Acordeones expandibles
- Layout responsive

### **❌ Lo que NO funciona (aún):**
- Botones de acción (no hacen nada)
- Búsqueda (input es solo visual)
- Editar tasa de cambio
- Formulario de pago (pendiente)
- Conexión a base de datos

### **🎯 Esto es NORMAL:**
Es un mockup para **diseño visual**, no para funcionalidad.
La funcionalidad se agregará en la siguiente fase.

---

## 💡 RECOMENDACIONES

1. **Toma capturas de pantalla** de lo que te gusta
2. **Anota cambios** que quieras hacer
3. **Prueba en diferentes tamaños** de ventana
4. **Comparte con el equipo** para feedback
5. **Itera rápido** en el diseño ahora que es fácil

---

## 🚀 ¿Listo para conectar a BD?

Cuando estés satisfecho con el diseño visual, avísame y te ayudo a:
1. Crear el formulario de pago interactivo
2. Conectar los eventos de los botones
3. Migrar de datos mock a datos reales
4. Integrar con el estado de AppState

**Tiempo estimado de migración:** 1-2 horas

---

**¡Disfruta explorando el mockup! 🎨**
