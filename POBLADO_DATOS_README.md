# 🏥 POBLADO DE DATOS - CLÍNICA DENTAL ODONTOMARVA

Scripts para poblar la base de datos con datos realistas para pruebas y demostración.

## 📋 ¿Qué hace cada script?

### 1. 🎬 `poblar_datos_clinica.py` - POBLADO COMPLETO
**Lo que crea:**
- ✅ **6 Odontólogos** con especialidades reales (Endodoncia, Periodoncia, Ortodoncía, etc.)
- ✅ **1 Administrador** para gestión de consultas
- ✅ **50 Pacientes** con datos venezolanos realistas
- ✅ **3 semanas** de consultas simuladas (aprox. 150+ consultas)
- ✅ **Intervenciones** odontológicas con servicios reales
- ✅ **Pagos** con diferentes estados (completos, parciales, pendientes)

**Tiempo estimado:** 2-3 minutos

### 2. ⚡ `ejecutar_poblado.py` - VERSIÓN SIMPLE
Ejecuta el poblado completo pero sin preguntas ni interrupciones.

### 3. 📅 `poblar_hoy.py` - SOLO CONSULTAS DE HOY
Crea 10 consultas para el día actual usando datos existentes.
**Útil para:** Pruebas rápidas del sistema de colas.

---

## 🚀 CÓMO USAR

### Opción 1: Poblado Completo (RECOMENDADO)
```bash
cd C:\Users\wilme\Documents\tesis-main
python ejecutar_poblado.py
```

### Opción 2: Solo consultas para hoy
```bash
cd C:\Users\wilme\Documents\tesis-main
python poblar_hoy.py
```

### Opción 3: Poblado interactivo
```bash
cd C:\Users\wilme\Documents\tesis-main
python poblar_datos_clinica.py
```

---

## 🎯 DATOS CREADOS

### 👨‍⚕️ **ODONTÓLOGOS CREADOS:**
1. **Dr. Carlos García** - Endodoncia
2. **Dra. María Rodríguez** - Periodoncia  
3. **Dr. Luis Martínez** - Ortodoncía
4. **Dra. Ana González** - Odontopediatría
5. **Dr. Roberto Fernández** - Cirugía Oral
6. **Dra. Gabriela Morales** - Implantología

### 👥 **PACIENTES:**
- 50 pacientes con nombres venezolanos
- Edades entre 18-80 años
- Datos médicos realistas (alergias, condiciones)
- Contactos de emergencia
- Direcciones en ciudades venezolanas

### 📅 **CONSULTAS SIMULADAS:**
- **Horarios:** 8:00 AM - 6:30 PM
- **Tipos:** General, Control, Urgencia
- **Estados:** Completadas (pasadas), En espera (hoy)
- **Distribución realista** por odontólogo
- **Motivos variados:** Dolor, limpieza, control, etc.

### 🦷 **INTERVENCIONES:**
- Procedimientos odontológicos reales
- Dientes afectados con numeración FDI
- Anestesia utilizada
- Instrucciones post-tratamiento
- Materiales utilizados

### 💰 **PAGOS:**
- **90% completados**, 10% parciales
- Métodos: Efectivo, tarjeta, transferencia
- Montos en BS y USD
- Tasa de cambio actual
- Recibos auto-numerados

---

## 🎯 FLUJO SIMULADO

### Día Típico en la Clínica:
1. **8:00 AM** - Llegan primeros pacientes
2. **Administrador** crea consultas y asigna colas
3. **Odontólogos** atienden por orden de llegada
4. **Intervenciones** se registran con servicios
5. **Pagos** se procesan al finalizar

### Estados Realistas:
- **En espera** → **En atención** → **Completada**
- Algunos pacientes **derivados** entre odontólogos
- **Pagos parciales** con saldos pendientes
- **Urgencias** con prioridad alta

---

## ⚠️ IMPORTANTE

### ✅ **ÚSALO CUANDO:**
- Necesites probar el sistema completo
- Quieras demostrar la funcionalidad
- Tengas tiempo para ver datos realistas
- Estés preparando la presentación de tesis

### ❌ **NO LO USES SI:**
- Tienes datos importantes en la BD
- Estás en producción
- No quieres muchos datos de prueba

### 🔄 **PARA LIMPIAR DESPUÉS:**
Si necesitas limpiar los datos de prueba, puedes eliminar desde Supabase:
```sql
-- ⚠️ CUIDADO: Esto elimina TODOS los datos
DELETE FROM pagos;
DELETE FROM intervenciones_servicios;
DELETE FROM intervenciones;
DELETE FROM consultas;
DELETE FROM pacientes;
DELETE FROM personal WHERE numero_documento IN ('12345678', '23456789', '34567890', '45678901', '56789012', '67890123', '98765432');
```

---

## 🎉 RESULTADOS ESPERADOS

Después del poblado tendrás:

### En el **Dashboard:**
- Estadísticas reales de los últimos días
- Gráficos con datos significativos
- Métricas financieras reales

### En **Consultas:**
- Cola actual del día con pacientes esperando
- Historial de 3 semanas de consultas
- Diferentes estados y prioridades

### En **Odontología:**
- Pacientes asignados por odontólogo
- Intervenciones completadas
- Estadísticas por especialidad

### En **Pagos:**
- Recibos generados automáticamente
- Saldos pendientes realistas
- Métodos de pago variados

### En **Pacientes:**
- 50 historiales clínicos completos
- Datos médicos detallados
- Contactos de emergencia

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### Error: "No se puede conectar a Supabase"
```bash
# Verifica que el servicio esté corriendo
reflex run
```

### Error: "Módulo no encontrado"
```bash
# Asegúrate de estar en el directorio correcto
cd C:\Users\wilme\Documents\tesis-main
```

### Error: "Personal no encontrado"
```bash
# Ejecuta el poblado completo primero
python ejecutar_poblado.py
```

---

## 📊 ESTADÍSTICAS DEL POBLADO

**Tiempo total:** ~3 minutos  
**Registros creados:** ~250+
- 7 empleados (6 odontólogos + 1 admin)
- 50 pacientes
- ~150 consultas
- ~200 intervenciones  
- ~120 pagos

**Memoria usada:** ~50MB  
**Espacio en BD:** ~10MB

---

## 💡 CONSEJOS DE USO

1. **Ejecuta el poblado completo** la primera vez
2. **Usa `poblar_hoy.py`** para agregar consultas diarias
3. **Revisa las estadísticas** en el dashboard después
4. **Prueba todos los módulos** con los datos generados
5. **Toma screenshots** para tu documentación de tesis

¡Perfecto para demostrar tu sistema funcionando con datos realistas! 🚀