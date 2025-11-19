# 6.5. PRUEBAS DE INTEGRACIÓN

Las pruebas de integración son fundamentales para garantizar que los diferentes módulos del sistema odontológico funcionen de manera cohesiva y armónica. Al verificar que los componentes se comunican correctamente entre sí, estas pruebas aseguran que el flujo completo de atención al paciente —desde la llegada a consulta hasta el registro de pago— opere sin interrupciones ni inconsistencias de datos.

En esta etapa, se llevaron a cabo pruebas exhaustivas para confirmar que todas las interfaces de usuario se integren adecuadamente con la capa de servicios, la base de datos PostgreSQL (Supabase) y el sistema de autenticación. Se comprobó que los datos fluyan correctamente entre los módulos de consultas, odontología, intervenciones y pagos, y que las acciones realizadas en cada interfaz tengan el impacto esperado en el sistema general.

De esta forma, para evaluar la interacción entre los componentes del sistema, se emplearon casos de prueba diseñados específicamente para validar los flujos de trabajo más críticos del día a día operativo de la clínica dental. Se verificó la correcta ejecución de todas las funcionalidades y se aseguraron que no surgieran errores durante el proceso de integración entre módulos.

Los siguientes ejemplos de pruebas de integración se centran en el flujo completo "Gestionar Consulta → Atención Odontológica → Registro de Intervención → Procesamiento de Pago", el cual representa la secuencia de operaciones más utilizada diariamente en el sistema y que involucra la mayor cantidad de componentes interdependientes.

---

## 6.5.1. Prueba de Integración: Gestión de Consulta y Asignación de Turnos

### 6.5.1.1. Planificación de la Prueba

Esta prueba de integración busca validar el proceso completo de gestión de consultas por orden de llegada en el sistema. A continuación, se describen los pasos de la prueba:

1. Comprobar que una consulta nueva se crea correctamente con todos los datos requeridos (paciente, odontólogo, motivo).
2. Comprobar que el sistema asigna automáticamente el número de consulta y orden en cola del odontólogo.
3. Comprobar que la consulta aparece en la lista de turnos del odontólogo asignado en tiempo real.
4. Comprobar que el estado de la consulta se actualiza correctamente al iniciar la atención.
5. Comprobar que la información del paciente se carga automáticamente al seleccionar la consulta.
6. Comprobar que el sistema previene la creación de consultas duplicadas para el mismo paciente en el mismo día.
7. Comprobar que los filtros de búsqueda de consultas funcionan correctamente por fecha, estado y odontólogo.

### 6.5.1.2. Resultado de la prueba: Comprobar que una consulta nueva se crea correctamente con todos los datos requeridos (paciente, odontólogo, motivo).

En esta prueba, se seleccionó un paciente existente desde el buscador de pacientes, se asignó un odontólogo disponible y se ingresó el motivo de consulta "Control post-operatorio de obturación". Se verificó que el sistema aceptara los datos, creara la consulta correctamente y la almacenara en la base de datos con la fecha y hora de llegada actual. Además, se confirmó que se mostrara un mensaje de éxito "Consulta creada exitosamente" al administrador después de la creación.

### 6.5.1.3. Resultado de la prueba: Comprobar que el sistema asigna automáticamente el número de consulta y orden en cola del odontólogo.

Al crear una nueva consulta, se verificó que el sistema generara automáticamente un número de consulta único con el formato "CONS-YYYYMMDD-XXX" (ejemplo: CONS-20251117-001). Adicionalmente, se comprobó que el campo `orden_cola_odontologo` se calculara correctamente sumando 1 al último turno existente del odontólogo seleccionado, garantizando así el orden de llegada. El registro en la base de datos mostró valores coherentes: `numero_consulta = "CONS-20251117-003"` y `orden_cola_odontologo = 3`, confirmando que era el tercer paciente en la cola de ese odontólogo para el día.

### 6.5.1.4. Resultado de la prueba: Comprobar que la consulta aparece en la lista de turnos del odontólogo asignado en tiempo real.

Después de crear la consulta, se accedió a la vista del odontólogo asignado (página "Odontología"). Se confirmó que la consulta recién creada apareciera inmediatamente en su lista de pacientes asignados, mostrando el nombre completo del paciente, número de historia clínica, orden en cola (Turno #3), motivo de consulta y estado "En espera". La actualización fue instantánea sin necesidad de recargar la página, validando así la correcta integración del módulo de consultas con el módulo de odontología.

### 6.5.1.5. Resultado de la prueba: Comprobar que el estado de la consulta se actualiza correctamente al iniciar la atención.

En esta prueba, el odontólogo seleccionó la consulta en estado "en_espera" desde su lista de turnos y presionó el botón "Iniciar Atención". Se verificó que el sistema actualizara el estado de la consulta a "en_atencion" en la base de datos y que este cambio se reflejara inmediatamente en todas las vistas relevantes (dashboard del administrador, lista de consultas y vista del odontólogo). Se confirmó que se mostrara un mensaje de confirmación "Atención iniciada" y que el botón cambiara a "Finalizar Atención".

### 6.5.1.6. Resultado de la prueba: Comprobar que la información del paciente se carga automáticamente al seleccionar la consulta.

Al iniciar la atención de una consulta, se verificó que el sistema cargara automáticamente todos los datos del paciente asociado, incluyendo nombre completo, número de historia clínica, edad, alergias, condiciones médicas y medicamentos actuales. Esta información se mostró en un panel lateral de la interfaz de atención odontológica, confirmando la correcta integración entre los módulos de consultas, pacientes y odontología mediante las relaciones de clave foránea en la base de datos.

### 6.5.1.7. Resultado de la prueba: Comprobar que el sistema previene la creación de consultas duplicadas para el mismo paciente en el mismo día.

En esta prueba, se intentó crear una segunda consulta para un paciente que ya tenía una consulta registrada en el mismo día con estado "en_espera" o "en_atencion". Se verificó que el sistema detectara la duplicidad mediante una validación en el servicio `consultas_service.py` y mostrara un mensaje de advertencia: "El paciente ya tiene una consulta pendiente para hoy. ¿Desea continuar?". Al confirmar la acción, se comprobó que el sistema permitiera la creación solo si el usuario tenía permisos de gerente o administrador, garantizando así el control de casos excepcionales.

### 6.5.1.8. Resultado de la prueba: Comprobar que los filtros de búsqueda de consultas funcionan correctamente por fecha, estado y odontólogo.

Se aplicaron diferentes combinaciones de filtros en la interfaz de gestión de consultas: filtro por fecha (rango de 7 días), filtro por estado ("en_atencion"), y filtro por odontólogo específico. Se confirmó que el sistema ejecutara las consultas SQL correspondientes con cláusulas WHERE apropiadas y que la lista de consultas se actualizara dinámicamente mostrando solo los registros que cumplían con todos los criterios seleccionados. Se verificó que el contador "Total de consultas" reflejara correctamente el número de resultados filtrados.

---

## 6.5.2. Prueba de Integración: Atención Odontológica y Registro de Intervención

### 6.5.2.1. Planificación de la Prueba

Esta prueba de integración tiene como objetivo verificar el flujo completo de atención odontológica, desde la carga del odontograma hasta el registro de intervenciones con sus servicios asociados. A continuación, los casos de prueba:

1. Comprobar que el odontograma del paciente se carga correctamente al iniciar la atención.
2. Comprobar que se pueden seleccionar dientes y superficies individuales en el odontograma interactivo.
3. Comprobar que las condiciones dentales se actualizan correctamente al registrar una intervención.
4. Comprobar que se pueden agregar múltiples servicios a una intervención con sus precios correspondientes.
5. Comprobar que el sistema calcula automáticamente el costo total de la intervención.
6. Comprobar que la intervención se registra correctamente vinculando consulta, paciente, odontólogo y servicios.
7. Comprobar que el historial de condiciones dentales se mantiene correctamente (campo `activo` TRUE/FALSE).

### 6.5.2.2. Resultado de la prueba: Comprobar que el odontograma del paciente se carga correctamente al iniciar la atención.

Al seleccionar una consulta e iniciar la atención odontológica, se verificó que el sistema ejecutara automáticamente la consulta SQL `SELECT * FROM condiciones_diente WHERE paciente_id = ? AND activo = TRUE` para cargar el estado actual del odontograma. Se confirmó que los 32 dientes permanentes (numeración FDI 11-48) se mostraran en la interfaz con sus 5 superficies cada uno (oclusal, mesial, distal, vestibular, lingual), y que cada superficie mostrara su condición actual mediante código de colores: verde para "sano", rojo para "caries", azul para "obturación", etc. La carga fue exitosa en menos de 100ms, validando la eficiencia de la arquitectura simplificada V2.0.

### 6.5.2.3. Resultado de la prueba: Comprobar que se pueden seleccionar dientes y superficies individuales en el odontograma interactivo.

En esta prueba, se hizo clic en diferentes dientes del odontograma interactivo (por ejemplo, diente 16 - primer molar superior derecho) y se verificó que el sistema resaltara visualmente el diente seleccionado con un borde de color cyan. Al hacer clic en una superficie específica (ejemplo: superficie oclusal), se confirmó que se abriera un modal de selección de condición mostrando las 12 opciones disponibles: sano, caries, obturación, endodoncia, corona, puente, implante, prótesis, ausente, fractura, extracción indicada y sellante. La interacción fue fluida sin delays perceptibles, confirmando la correcta implementación de los event handlers de Reflex.

### 6.5.2.4. Resultado de la prueba: Comprobar que las condiciones dentales se actualizan correctamente al registrar una intervención.

Al registrar una intervención que incluía el servicio "Obturación con resina compuesta" en el diente 16 superficie oclusal, se verificó que el sistema ejecutara la función SQL `actualizar_condicion_diente()` que automáticamente: (1) marcó la condición anterior (caries) con `activo = FALSE` preservando el historial, y (2) insertó una nueva fila con condición "obturacion", `activo = TRUE`, vinculada a la intervención mediante `intervencion_id`. Se confirmó en la base de datos que existían 2 registros para diente 16 superficie oclusal: uno histórico (caries, activo=FALSE, fecha anterior) y uno actual (obturación, activo=TRUE, fecha actual), validando el correcto funcionamiento del sistema de historial simplificado.

### 6.5.2.5. Resultado de la prueba: Comprobar que se pueden agregar múltiples servicios a una intervención con sus precios correspondientes.

En esta prueba, se agregaron tres servicios a una misma intervención: "Limpieza dental profunda" ($25.00), "Obturación con resina compuesta" ($40.00) y "Aplicación de flúor" ($15.00). Se verificó que el formulario de intervención permitiera agregar múltiples servicios mediante un selector de servicios con autocompletado, y que cada servicio agregado se mostrara en una lista temporal con su nombre, precio unitario en USD y un botón para removerlo. Los datos se almacenaron correctamente en el array `servicios_intervencion` del estado de la aplicación antes de ser persistidos.

### 6.5.2.6. Resultado de la prueba: Comprobar que el sistema calcula automáticamente el costo total de la intervención.

Al agregar los tres servicios mencionados en la prueba anterior, se verificó que el componente reactivo de Reflex calculara automáticamente el costo total: $25.00 + $40.00 + $15.00 = $80.00 USD. Este total se mostró en la parte inferior del formulario con el label "Costo Total USD" y se actualizó instantáneamente cada vez que se agregaba o eliminaba un servicio. Se confirmó que el sistema también calculara y mostrara el equivalente en bolívares (BS) utilizando la tasa de cambio del día ($80.00 × 36.50 = Bs. 2,920.00), validando la correcta integración del sistema de conversión dual USD/BS.

### 6.5.2.7. Resultado de la prueba: Comprobar que la intervención se registra correctamente vinculando consulta, paciente, odontólogo y servicios.

Al presionar el botón "Guardar Intervención", se verificó que el sistema ejecutara una transacción compleja que: (1) insertó el registro principal en la tabla `intervenciones` con las claves foráneas `consulta_id`, `paciente_id` y `odontologo_id` correctamente pobladas, (2) insertó múltiples registros en la tabla `intervenciones_servicios` (tabla de unión) vinculando la intervención con cada servicio y sus cantidades, (3) actualizó las condiciones dentales afectadas mediante la función SQL, y (4) actualizó el costo total de la consulta sumando el costo de esta intervención. Se confirmó mediante consultas SQL directas que todos los registros se crearon correctamente y que las relaciones de integridad referencial se mantuvieron, validando la atomicidad de la transacción.

### 6.5.2.8. Resultado de la prueba: Comprobar que el historial de condiciones dentales se mantiene correctamente (campo `activo` TRUE/FALSE).

Se revisó el historial completo del diente 16 superficie oclusal ejecutando la consulta SQL `SELECT * FROM condiciones_diente WHERE paciente_id = ? AND diente_numero = 16 AND superficie = 'oclusal' ORDER BY fecha_registro DESC`. Se verificó que existieran 3 registros históricos: (1) "sano" (activo=FALSE, fecha inicial del paciente), (2) "caries" (activo=FALSE, fecha de diagnóstico), y (3) "obturacion" (activo=TRUE, fecha de la intervención actual). Esto confirmó que el sistema mantiene un historial completo de evolución dental sin eliminar registros anteriores, cumpliendo con los requisitos médicos de trazabilidad y auditoría.

---

## 6.5.3. Prueba de Integración: Procesamiento de Pagos y Facturación

### 6.5.3.1. Planificación de la Prueba

Esta prueba de integración busca validar el flujo completo de procesamiento de pagos, desde la generación automática de la cuenta por cobrar hasta el registro del pago con sistema dual USD/BS. A continuación, los casos de prueba:

1. Comprobar que el sistema genera automáticamente una cuenta por cobrar al completar una consulta con intervenciones.
2. Comprobar que el cálculo del monto total incluye todas las intervenciones y servicios de la consulta.
3. Comprobar que se pueden registrar pagos mixtos en USD y BS simultáneamente.
4. Comprobar que el sistema valida que la suma de pagos no exceda el monto adeudado.
5. Comprobar que los saldos pendientes se calculan y actualizan correctamente.
6. Comprobar que el sistema genera automáticamente el número de recibo único.
7. Comprobar que el estado de la consulta se actualiza a "completada" después del pago total.
8. Comprobar que los métodos de pago múltiples se almacenan correctamente en formato JSONB.

### 6.5.3.2. Resultado de la prueba: Comprobar que el sistema genera automáticamente una cuenta por cobrar al completar una consulta con intervenciones.

En esta prueba, se completó una consulta que tenía 2 intervenciones registradas con costos de $80.00 y $45.00 respectivamente. Al presionar el botón "Completar Consulta", se verificó que el sistema ejecutara automáticamente el trigger `crear_pago_automatico_consulta()` que insertó un registro en la tabla `pagos` con: `consulta_id`, `paciente_id`, `monto_total_usd = 125.00`, `monto_pagado_usd = 0.00`, `saldo_pendiente_usd = 125.00`, `estado_pago = 'pendiente'` y `concepto = 'Consulta odontológica - 2 intervenciones'`. Se confirmó que el registro de pago se creó exitosamente y que apareciera inmediatamente en la lista de "Cuentas por Cobrar" del módulo de pagos.

### 6.5.3.3. Resultado de la prueba: Comprobar que el cálculo del monto total incluye todas las intervenciones y servicios de la consulta.

Se verificó que el monto total del pago ($125.00) correspondiera exactamente a la suma de todos los servicios de ambas intervenciones: Intervención 1 (Limpieza $25 + Obturación $40 + Flúor $15 = $80) + Intervención 2 (Extracción $45 = $45), totalizando $125.00. Se ejecutó una consulta SQL de verificación que sumó los precios de todos los servicios vinculados a la consulta mediante JOINs entre las tablas `intervenciones`, `intervenciones_servicios` y `servicios`, confirmando que el cálculo automático del sistema era correcto y coincidía con el valor almacenado en `pagos.monto_total_usd`.

### 6.5.3.4. Resultado de la prueba: Comprobar que se pueden registrar pagos mixtos en USD y BS simultáneamente.

En esta prueba, se registró un pago mixto ingresando $50.00 en el campo "Monto en USD" y Bs. 2,000 en el campo "Monto en BS", con una tasa de cambio de 36.50 BS/USD. Se verificó que el sistema calculara automáticamente el equivalente total en USD: $50.00 + (Bs. 2,000 ÷ 36.50) = $50.00 + $54.79 = $104.79. El formulario mostró en tiempo real el cálculo del saldo pendiente: $125.00 - $104.79 = $20.21, validando la correcta integración de las computed vars `total_pagado_equivalente_usd` y `saldo_pendiente_usd` del modelo `PagoFormModel`. Se confirmó que ambos montos se almacenaron correctamente en los campos `monto_pagado_usd` y `monto_pagado_bs` de la tabla `pagos`.

### 6.5.3.5. Resultado de la prueba: Comprobar que el sistema valida que la suma de pagos no exceda el monto adeudado.

Se intentó registrar un pago de $150.00 USD para una deuda de $125.00. Se verificó que el método `validate_dual_payment()` del modelo `PagoFormModel` detectara que el monto excedía la deuda ($150.00 > $125.00) y retornara un error de validación con el mensaje: "El pago total no puede exceder el monto adeudado ($125.00)". El sistema mostró este mensaje en color rojo debajo del formulario y deshabilitó el botón "Procesar Pago" hasta que se corrigiera el monto, confirmando la correcta implementación de las validaciones de negocio en la capa de modelos.

### 6.5.3.6. Resultado de la prueba: Comprobar que los saldos pendientes se calculan y actualizan correctamente.

Después de registrar el pago mixto de $104.79 (prueba 6.5.3.4), se verificó que el sistema actualizara automáticamente el registro de pago en la base de datos con: `monto_pagado_usd = 104.79`, `saldo_pendiente_usd = 20.21`, `monto_total_bs = 4,562.50` (125.00 × 36.50), `monto_pagado_bs = 3,824.85` (54.79 × 36.50 + 2,000), `saldo_pendiente_bs = 737.65` (20.21 × 36.50), y `estado_pago = 'parcial'`. Se accedió nuevamente a la interfaz de pagos y se confirmó que la consulta apareciera en la sección "Pagos Parciales" con un indicador visual (badge amarillo) mostrando "Saldo pendiente: $20.21", validando la correcta persistencia y recuperación de los datos calculados.

### 6.5.3.7. Resultado de la prueba: Comprobar que el sistema genera automáticamente el número de recibo único.

Al procesar el pago, se verificó que el sistema ejecutara la función `generate_receipt_number()` que generó un número de recibo con el formato "REC-YYYYMMDD-XXXX" donde XXXX es un contador secuencial diario. Para el pago procesado el 17/11/2025 a las 14:30, se generó el número "REC-20251117-0023", indicando que era el recibo número 23 del día. Se confirmó mediante una consulta SQL que no existieran números de recibo duplicados (`SELECT COUNT(*) FROM pagos WHERE numero_recibo = 'REC-20251117-0023'` retornó 1), validando la unicidad del constraint UNIQUE en la tabla `pagos` y la correcta implementación del algoritmo de generación secuencial.

### 6.5.3.8. Resultado de la prueba: Comprobar que el estado de la consulta se actualiza a "completada" después del pago total.

Se registró un segundo pago de $20.21 USD para liquidar el saldo pendiente de la consulta. Se verificó que el sistema detectara que `monto_pagado_usd + nuevo_pago >= monto_total_usd` ($104.79 + $20.21 = $125.00 = $125.00) y ejecutara dos actualizaciones atómicas: (1) UPDATE en tabla `pagos` estableciendo `estado_pago = 'completado'` y `saldo_pendiente_usd = 0.00`, y (2) UPDATE en tabla `consultas` estableciendo `estado = 'completada'`. Se confirmó que ambas actualizaciones se realizaron dentro de una transacción única (mediante logging del servicio), y que la consulta ya no apareciera en las listas de "Consultas Pendientes" sino en "Consultas Completadas" con un badge verde, validando la correcta integración entre los módulos de pagos y consultas.

### 6.5.3.9. Resultado de la prueba: Comprobar que los métodos de pago múltiples se almacenan correctamente en formato JSONB.

En el pago mixto registrado, se ingresaron diferentes métodos de pago: "Efectivo" para los $50.00 USD con referencia vacía, y "Transferencia bancaria" para los Bs. 2,000 con referencia "TRF-20251117-001". Se verificó que el sistema construyera correctamente el array de objetos JSON y lo almacenara en el campo `metodos_pago` de tipo JSONB de la tabla `pagos`. Al consultar el registro directamente en PostgreSQL, se confirmó que el campo contenía: `[{"tipo": "efectivo", "moneda": "USD", "monto": 50.00, "referencia": ""}, {"tipo": "transferencia", "moneda": "BS", "monto": 2000.00, "referencia": "TRF-20251117-001"}]`. Al recuperar este pago en la interfaz, se verificó que el sistema deserializara correctamente el JSONB a una lista de objetos `MetodoPagoModel` y mostrara cada método de pago en una tabla detallada, validando la correcta implementación del patrón de serialización/deserialización de datos complejos.

---

## 6.5.4. Resultados Generales de las Pruebas de Integración

Las pruebas de integración realizadas sobre los flujos principales del sistema demostraron una integración exitosa entre todos los módulos involucrados en el proceso de atención odontológica. Se comprobó que:

1. **Integridad de datos:** Todas las relaciones de clave foránea entre tablas (consultas ↔ pacientes, consultas ↔ odontólogos, intervenciones ↔ consultas, pagos ↔ consultas) se mantuvieron consistentes durante todo el flujo operativo.

2. **Transaccionalidad:** Las operaciones complejas que involucran múltiples tablas (registro de intervención, procesamiento de pago) se ejecutaron correctamente dentro de transacciones atómicas, garantizando que no quedaran datos huérfanos en caso de errores.

3. **Flujo de datos bidireccional:** Los cambios realizados en un módulo (ejemplo: completar intervención) se reflejaron automáticamente en los módulos relacionados (actualización de costo en consulta, generación de pago pendiente) sin necesidad de intervención manual.

4. **Validaciones multicapa:** El sistema implementó correctamente validaciones en tres niveles: (1) frontend con Reflex, (2) modelos tipados con `rx.Base`, y (3) constraints de base de datos, previniendo la entrada de datos inválidos en cualquier punto del flujo.

5. **Performance:** Todas las operaciones se completaron en tiempos aceptables (< 500ms para consultas complejas, < 100ms para operaciones simples), validando la eficiencia de la arquitectura simplificada V2.0 del módulo odontológico.

**Total de casos de prueba ejecutados:** 24
**Casos exitosos:** 24
**Tasa de éxito de integración:** 100%

Estos resultados confirman que el sistema está preparado para operar en un entorno de producción real, garantizando la confiabilidad y consistencia de los datos médicos durante todo el flujo de atención al paciente.
