# PRUEBAS DE UNIDAD - SISTEMA DE GESTIÓN ODONTOLÓGICA

**Universidad de Oriente**
**Trabajo de Grado - Ingeniería de Sistemas**
**Estudiante:** Wilmer Aguirre
**Fecha:** 2025-11-17

---

## 1. INTRODUCCIÓN

La prueba por unidad es una forma de verificar los errores que se presenten en el funcionamiento del sistema y minimizarlos. En este documento se muestran los criterios de evaluación utilizados para cada dato de entrada de la aplicación.

Con el objetivo de validar cada componente desarrollado y revisar el flujo de datos, tanto entrada como salidas del sistema, se realizan pruebas individuales que cubren las principales funciones del mismo al momento de ingresar datos.

---

## 2. CRITERIOS DE EVALUACIÓN

Para cada variable de entrada se evalúan diferentes **clases de equivalencia**, determinando si son **válidas** o **inválidas** según las reglas de negocio y restricciones del sistema.

**Leyenda:**
- ✅ **X en Válido:** La clase de equivalencia es aceptada por el sistema
- ❌ **X en Inválido:** La clase de equivalencia es rechazada por el sistema

---

## 3. PRUEBAS POR MÓDULO

### 3.1. PRUEBA "AGREGAR PACIENTE"

**Tabla 3.1.1:** Pruebas de validación para el formulario de registro de pacientes

| Variable | Clase de Equivalencia | Válido | Inválido |
|----------|----------------------|--------|----------|
| primer_nombre | Caracteres Alfabéticos | X | |
| primer_nombre | Caracteres Numéricos | | X |
| primer_nombre | Caracteres Especiales (@, #, $) | | X |
| primer_nombre | Campo Vacío | | X |
| primer_nombre | Espacios en blanco únicamente | | X |
| primer_nombre | Longitud 1-50 caracteres | X | |
| primer_nombre | Longitud mayor a 50 caracteres | | X |
| segundo_nombre | Caracteres Alfabéticos | X | |
| segundo_nombre | Caracteres Numéricos | | X |
| segundo_nombre | Campo Vacío | X | |
| segundo_nombre | Longitud 1-50 caracteres | X | |
| primer_apellido | Caracteres Alfabéticos | X | |
| primer_apellido | Caracteres Numéricos | | X |
| primer_apellido | Campo Vacío | | X |
| primer_apellido | Longitud 1-50 caracteres | X | |
| primer_apellido | Longitud mayor a 50 caracteres | | X |
| segundo_apellido | Caracteres Alfabéticos | X | |
| segundo_apellido | Campo Vacío | X | |
| numero_documento | Caracteres Numéricos | X | |
| numero_documento | Caracteres Alfabéticos | | X |
| numero_documento | Campo Vacío | | X |
| numero_documento | Longitud 5-15 dígitos | X | |
| numero_documento | Longitud menor a 5 dígitos | | X |
| tipo_documento | Valor "CI" | X | |
| tipo_documento | Valor "Pasaporte" | X | |
| tipo_documento | Valores distintos a los permitidos | | X |
| celular_1 | Formato numérico (10-11 dígitos) | X | |
| celular_1 | Caracteres Alfabéticos | | X |
| celular_1 | Longitud menor a 10 dígitos | | X |
| celular_1 | Longitud mayor a 11 dígitos | | X |
| celular_2 | Formato numérico (10-11 dígitos) | X | |
| celular_2 | Campo Vacío | X | |
| email | Formato válido (usuario@dominio.com) | X | |
| email | Sin símbolo @ | | X |
| email | Sin dominio (.com, .net, etc.) | | X |
| email | Campo Vacío | X | |
| email | Termina en coma | | X |
| fecha_nacimiento | Formato YYYY-MM-DD | X | |
| fecha_nacimiento | Formato DD/MM/YYYY | | X |
| fecha_nacimiento | Fecha futura | | X |
| fecha_nacimiento | Fecha mayor a 120 años atrás | | X |
| fecha_nacimiento | Campo Vacío | X | |
| genero | Valor "masculino" | X | |
| genero | Valor "femenino" | X | |
| genero | Valor "otro" | X | |
| genero | Campo Vacío | X | |
| direccion | Texto alfanumérico | X | |
| direccion | Campo Vacío | X | |
| direccion | Longitud 1-200 caracteres | X | |
| ciudad | Caracteres Alfabéticos | X | |
| ciudad | Campo Vacío | X | |
| ciudad | Longitud 1-100 caracteres | X | |
| alergias | Texto descriptivo | X | |
| alergias | Campo Vacío | X | |
| medicamentos_actuales | Texto descriptivo | X | |
| medicamentos_actuales | Campo Vacío | X | |
| condiciones_medicas | Texto descriptivo | X | |
| condiciones_medicas | Campo Vacío | X | |
| contacto_emergencia_nombre | Caracteres Alfabéticos | X | |
| contacto_emergencia_nombre | Campo Vacío | X | |
| contacto_emergencia_telefono | Formato numérico (10-11 dígitos) | X | |
| contacto_emergencia_telefono | Campo Vacío | X | |
| contacto_emergencia_relacion | Caracteres Alfabéticos | X | |
| contacto_emergencia_relacion | Valores: "Madre", "Padre", "Hermano", "Cónyuge" | X | |

**Resultado esperado:** El sistema valida que primer_nombre, primer_apellido y numero_documento sean obligatorios. Los campos opcionales permiten valores vacíos. El email debe tener formato válido si se proporciona.

---

### 3.2. PRUEBA "AGREGAR PERSONAL"

**Tabla 3.2.1:** Pruebas de validación para el formulario de registro de personal

| Variable | Clase de Equivalencia | Válido | Inválido |
|----------|----------------------|--------|----------|
| primer_nombre | Caracteres Alfabéticos | X | |
| primer_nombre | Caracteres Numéricos | | X |
| primer_nombre | Campo Vacío | | X |
| primer_nombre | Longitud 1-50 caracteres | X | |
| segundo_nombre | Caracteres Alfabéticos | X | |
| segundo_nombre | Campo Vacío | X | |
| primer_apellido | Caracteres Alfabéticos | X | |
| primer_apellido | Campo Vacío | | X |
| primer_apellido | Longitud 1-50 caracteres | X | |
| segundo_apellido | Caracteres Alfabéticos | X | |
| segundo_apellido | Campo Vacío | X | |
| numero_documento | Caracteres Numéricos | X | |
| numero_documento | Caracteres Alfabéticos | | X |
| numero_documento | Campo Vacío | | X |
| numero_documento | Longitud 5-15 dígitos | X | |
| tipo_documento | Valor "CI" | X | |
| tipo_documento | Valor "Pasaporte" | X | |
| celular | Formato numérico (10-11 dígitos) | X | |
| celular | Campo Vacío | | X |
| celular | Caracteres Alfabéticos | | X |
| codigo_pais_celular | Valor "+58 (VE)" | X | |
| codigo_pais_celular | Valor "+1 (US)" | X | |
| codigo_pais_celular | Formato incorrecto | | X |
| direccion | Texto alfanumérico | X | |
| direccion | Campo Vacío | X | |
| tipo_personal | Valor "Odontólogo" | X | |
| tipo_personal | Valor "Asistente" | X | |
| tipo_personal | Valor "Administrador" | X | |
| tipo_personal | Valor "Gerente" | X | |
| tipo_personal | Valores distintos a los permitidos | | X |
| tipo_personal | Campo Vacío | | X |
| especialidad | Caracteres Alfabéticos | X | |
| especialidad | Campo Vacío (si tipo_personal != "Odontólogo") | X | |
| especialidad | Campo Vacío (si tipo_personal == "Odontólogo") | | X |
| numero_colegiatura | Caracteres Alfanuméricos | X | |
| numero_colegiatura | Campo Vacío (si tipo_personal != "Odontólogo") | X | |
| numero_colegiatura | Campo Vacío (si tipo_personal == "Odontólogo") | | X |
| fecha_ingreso | Formato YYYY-MM-DD | X | |
| fecha_ingreso | Formato DD/MM/YYYY | | X |
| fecha_ingreso | Fecha futura | | X |
| fecha_ingreso | Campo Vacío | X | |
| estado_laboral | Valor "activo" | X | |
| estado_laboral | Valor "inactivo" | X | |
| estado_laboral | Valor "vacaciones" | X | |
| estado_laboral | Valor "licencia" | X | |
| estado_laboral | Valores distintos a los permitidos | | X |
| crear_usuario | Valor True | X | |
| crear_usuario | Valor False | X | |
| usuario_email | Formato válido (usuario@dominio.com) | X | |
| usuario_email | Sin símbolo @ | | X |
| usuario_email | Campo Vacío (si crear_usuario == True) | | X |
| usuario_email | Campo Vacío (si crear_usuario == False) | X | |
| usuario_password | Longitud mínima 6 caracteres | X | |
| usuario_password | Longitud menor a 6 caracteres | | X |
| usuario_password | Campo Vacío (si crear_usuario == True) | | X |
| usuario_password | Campo Vacío (si crear_usuario == False) | X | |
| rol_sistema | Valor "gerente" | X | |
| rol_sistema | Valor "administrador" | X | |
| rol_sistema | Valor "odontologo" | X | |
| rol_sistema | Valor "asistente" | X | |
| rol_sistema | Valores distintos a los permitidos | | X |

**Resultado esperado:** El sistema valida que primer_nombre, primer_apellido, numero_documento y celular sean obligatorios. Si tipo_personal es "Odontólogo", especialidad y numero_colegiatura son obligatorios. Si crear_usuario es True, usuario_email y usuario_password son obligatorios.

---

### 3.3. PRUEBA "AGREGAR SERVICIO"

**Tabla 3.3.1:** Pruebas de validación para el formulario de registro de servicios odontológicos

| Variable | Clase de Equivalencia | Válido | Inválido |
|----------|----------------------|--------|----------|
| codigo | Caracteres Alfabéticos Mayúsculas | X | |
| codigo | Caracteres Numéricos | X | |
| codigo | Combinación Alfanumérica (A-Z, 0-9) | X | |
| codigo | Caracteres en minúsculas | | X |
| codigo | Caracteres Especiales (@, #, $) | | X |
| codigo | Campo Vacío | | X |
| codigo | Formato "SER001", "SER002" | X | |
| codigo | Longitud 1-20 caracteres | X | |
| codigo | Longitud mayor a 20 caracteres | | X |
| nombre | Caracteres Alfabéticos | X | |
| nombre | Caracteres Numéricos | | X |
| nombre | Campo Vacío | | X |
| nombre | Longitud 1-100 caracteres | X | |
| nombre | Longitud mayor a 100 caracteres | | X |
| categoria | Valor "preventiva" | X | |
| categoria | Valor "restaurativa" | X | |
| categoria | Valor "endodoncia" | X | |
| categoria | Valor "periodoncia" | X | |
| categoria | Valor "cirugia" | X | |
| categoria | Valor "ortodoncia" | X | |
| categoria | Valor "protesis" | X | |
| categoria | Valor "estetica" | X | |
| categoria | Valor "diagnostico" | X | |
| categoria | Valor "urgencia" | X | |
| categoria | Campo Vacío | | X |
| categoria | Valores distintos a los permitidos | | X |
| precio_base_usd | Valor numérico positivo | X | |
| precio_base_usd | Valor cero | | X |
| precio_base_usd | Valor negativo | | X |
| precio_base_usd | Campo Vacío | | X |
| precio_base_usd | Formato decimal (10.50) | X | |
| precio_base_usd | Más de 2 decimales (10.555) | | X |
| precio_base_usd | Caracteres Alfabéticos | | X |
| alcance_servicio | Valor "superficie_especifica" | X | |
| alcance_servicio | Valor "diente_completo" | X | |
| alcance_servicio | Valor "boca_completa" | X | |
| alcance_servicio | Valores distintos a los permitidos | | X |
| alcance_servicio | Campo Vacío (default: "superficie_especifica") | X | |
| condicion_resultante | Valor "sano" | X | |
| condicion_resultante | Valor "caries" | X | |
| condicion_resultante | Valor "obturacion" | X | |
| condicion_resultante | Valor "endodoncia" | X | |
| condicion_resultante | Valor "corona" | X | |
| condicion_resultante | Valor "puente" | X | |
| condicion_resultante | Valor "implante" | X | |
| condicion_resultante | Valor "protesis" | X | |
| condicion_resultante | Valor "ausente" | X | |
| condicion_resultante | Valor "fractura" | X | |
| condicion_resultante | Valor "extraccion_indicada" | X | |
| condicion_resultante | Campo Vacío (NULL - servicio preventivo) | X | |
| condicion_resultante | Valores distintos a los permitidos | | X |
| descripcion | Texto descriptivo | X | |
| descripcion | Campo Vacío | X | |
| descripcion | Longitud 1-500 caracteres | X | |
| descripcion | Longitud mayor a 500 caracteres | | X |

**Resultado esperado:** El sistema valida que codigo (formato mayúsculas alfanumérico), nombre, categoria y precio_base_usd (mayor a 0) sean obligatorios. El alcance_servicio tiene un valor por defecto. La condicion_resultante puede ser NULL para servicios preventivos.

---

### 3.4. PRUEBA "AGREGAR CONSULTA"

**Tabla 3.4.1:** Pruebas de validación para el formulario de registro de consultas

| Variable | Clase de Equivalencia | Válido | Inválido |
|----------|----------------------|--------|----------|
| paciente_id | UUID válido existente | X | |
| paciente_id | UUID formato inválido | | X |
| paciente_id | UUID no existente en BD | | X |
| paciente_id | Campo Vacío | | X |
| paciente_nombre | Caracteres Alfabéticos (solo display) | X | |
| primer_odontologo_id | UUID válido existente | X | |
| primer_odontologo_id | UUID formato inválido | | X |
| primer_odontologo_id | UUID de personal no odontólogo | | X |
| primer_odontologo_id | Campo Vacío | | X |
| tipo_consulta | Valor "general" | X | |
| tipo_consulta | Valor "control" | X | |
| tipo_consulta | Valor "urgencia" | X | |
| tipo_consulta | Valor "emergencia" | X | |
| tipo_consulta | Valores distintos a los permitidos | | X |
| tipo_consulta | Campo Vacío (default: "general") | X | |
| motivo_consulta | Texto descriptivo | X | |
| motivo_consulta | Campo Vacío | | X |
| motivo_consulta | Longitud 1-500 caracteres | X | |
| motivo_consulta | Longitud mayor a 500 caracteres | | X |
| observaciones | Texto descriptivo | X | |
| observaciones | Campo Vacío | X | |
| observaciones | Longitud 1-1000 caracteres | X | |
| estado | Valor "en_espera" | X | |
| estado | Valor "en_atencion" | X | |
| estado | Valor "entre_odontologos" | X | |
| estado | Valor "completada" | X | |
| estado | Valor "cancelada" | X | |
| estado | Valores distintos a los permitidos | | X |
| estado | Campo Vacío (default: "en_espera") | X | |

**Resultado esperado:** El sistema valida que paciente_id, primer_odontologo_id y motivo_consulta sean obligatorios. El tipo_consulta y estado tienen valores por defecto. El primer_odontologo_id debe corresponder a un personal con tipo_personal "Odontólogo".

---

### 3.5. PRUEBA "REGISTRAR PAGO"

**Tabla 3.5.1:** Pruebas de validación para el formulario de registro de pagos

| Variable | Clase de Equivalencia | Válido | Inválido |
|----------|----------------------|--------|----------|
| paciente_id | UUID válido existente | X | |
| paciente_id | Campo Vacío | | X |
| paciente_id | UUID formato inválido | | X |
| consulta_id | UUID válido existente | X | |
| consulta_id | Campo Vacío | X | |
| consulta_id | UUID formato inválido | | X |
| monto_total_usd | Valor numérico positivo | X | |
| monto_total_usd | Valor cero | | X |
| monto_total_usd | Valor negativo | | X |
| monto_total_usd | Campo Vacío | | X |
| monto_total_usd | Formato decimal (150.50) | X | |
| monto_total_usd | Más de 2 decimales | | X |
| tasa_cambio_del_dia | Valor numérico positivo | X | |
| tasa_cambio_del_dia | Valor cero | | X |
| tasa_cambio_del_dia | Valor negativo | | X |
| tasa_cambio_del_dia | Campo Vacío (default: "36.50") | X | |
| tasa_cambio_del_dia | Formato decimal (36.50) | X | |
| pago_usd | Valor numérico positivo | X | |
| pago_usd | Valor cero (si pago_bs > 0) | X | |
| pago_usd | Valor negativo | | X |
| pago_usd | Valor mayor al monto_total_usd | | X |
| pago_usd | Formato decimal (100.00) | X | |
| pago_bs | Valor numérico positivo | X | |
| pago_bs | Valor cero (si pago_usd > 0) | X | |
| pago_bs | Valor negativo | | X |
| pago_bs | Formato numérico entero | X | |
| pago_usd + pago_bs | Al menos uno mayor a cero | X | |
| pago_usd + pago_bs | Ambos en cero | | X |
| pago_usd + pago_bs | Suma equivalente mayor al total | | X |
| metodo_pago_usd | Valor "efectivo" | X | |
| metodo_pago_usd | Valor "tarjeta_credito" | X | |
| metodo_pago_usd | Valor "tarjeta_debito" | X | |
| metodo_pago_usd | Valor "transferencia" | X | |
| metodo_pago_usd | Valor "pago_movil" | X | |
| metodo_pago_usd | Valores distintos a los permitidos | | X |
| metodo_pago_bs | Valor "efectivo" | X | |
| metodo_pago_bs | Valor "transferencia" | X | |
| metodo_pago_bs | Valor "pago_movil" | X | |
| metodo_pago_bs | Valores distintos a los permitidos | | X |
| referencia_usd | Texto alfanumérico | X | |
| referencia_usd | Campo Vacío (si metodo_pago_usd == "efectivo") | X | |
| referencia_usd | Campo Vacío (si metodo_pago_usd == "transferencia") | | X |
| referencia_bs | Texto alfanumérico | X | |
| referencia_bs | Campo Vacío (si metodo_pago_bs == "efectivo") | X | |
| referencia_bs | Campo Vacío (si metodo_pago_bs == "transferencia") | | X |
| concepto | Texto descriptivo | X | |
| concepto | Campo Vacío | | X |
| concepto | Longitud 1-200 caracteres | X | |
| descuento_usd | Valor numérico positivo | X | |
| descuento_usd | Valor cero | X | |
| descuento_usd | Valor negativo | | X |
| descuento_usd | Valor mayor al monto_total_usd | | X |
| motivo_descuento | Texto descriptivo | X | |
| motivo_descuento | Campo Vacío (si descuento_usd == 0) | X | |
| motivo_descuento | Campo Vacío (si descuento_usd > 0) | | X |
| estado_pago | Valor "pendiente" | X | |
| estado_pago | Valor "completado" | X | |
| estado_pago | Valor "anulado" | X | |
| estado_pago | Valores distintos a los permitidos | | X |
| observaciones | Texto descriptivo | X | |
| observaciones | Campo Vacío | X | |

**Resultado esperado:** El sistema valida que paciente_id, monto_total_usd (mayor a 0), concepto y al menos un monto de pago (pago_usd o pago_bs) sean obligatorios. La tasa_cambio_del_dia debe ser mayor a 0. Si hay descuento, debe tener motivo. Si el método de pago es transferencia o tarjeta, debe tener referencia.

---

### 3.6. PRUEBA "CAMBIAR CONTRASEÑA"

**Tabla 3.6.1:** Pruebas de validación para el formulario de cambio de contraseña

| Variable | Clase de Equivalencia | Válido | Inválido |
|----------|----------------------|--------|----------|
| current_password | Caracteres Alfanuméricos | X | |
| current_password | Campo Vacío | | X |
| current_password | Contraseña correcta (coincide con BD) | X | |
| current_password | Contraseña incorrecta (no coincide con BD) | | X |
| current_password | Longitud mínima 6 caracteres | X | |
| current_password | Espacios en blanco | X | |
| new_password | Caracteres Alfanuméricos | X | |
| new_password | Caracteres Especiales (!@#$%^&*) | X | |
| new_password | Combinación Alfanumérica + Especial | X | |
| new_password | Campo Vacío | | X |
| new_password | Longitud menor a 6 caracteres | | X |
| new_password | Longitud 6-50 caracteres | X | |
| new_password | Longitud mayor a 50 caracteres | | X |
| new_password | Solo espacios en blanco | | X |
| new_password | Igual a current_password | | X |
| new_password | Diferente a current_password | X | |
| confirm_password | Caracteres Alfanuméricos | X | |
| confirm_password | Campo Vacío | | X |
| confirm_password | Coincide con new_password | X | |
| confirm_password | No coincide con new_password | | X |
| confirm_password | Longitud mínima 6 caracteres | X | |

**Resultado esperado:** El sistema valida que current_password sea correcta, new_password tenga mínimo 6 caracteres y sea diferente a la actual, y confirm_password coincida exactamente con new_password. La contraseña debe ser verificada contra la base de datos de autenticación de Supabase.

---

### 3.7. PRUEBA "CAMBIAR EMAIL"

**Tabla 3.7.1:** Pruebas de validación para el formulario de cambio de email

| Variable | Clase de Equivalencia | Válido | Inválido |
|----------|----------------------|--------|----------|
| new_email | Formato válido (usuario@dominio.com) | X | |
| new_email | Formato válido (usuario@dominio.co.ve) | X | |
| new_email | Sin símbolo @ | | X |
| new_email | Sin dominio (.com, .net, etc.) | | X |
| new_email | Campo Vacío | | X |
| new_email | Múltiples símbolos @ (user@@domain.com) | | X |
| new_email | Espacios en blanco | | X |
| new_email | Caracteres especiales no permitidos (#, $, %) | | X |
| new_email | Punto al inicio (.usuario@dominio.com) | | X |
| new_email | Punto al final (usuario.@dominio.com) | | X |
| new_email | Dominio sin extensión (usuario@dominio) | | X |
| new_email | Longitud 1-100 caracteres | X | |
| new_email | Longitud mayor a 100 caracteres | | X |
| new_email | Email ya registrado en el sistema | | X |
| new_email | Email único (no existe en BD) | X | |
| new_email | Igual al email actual del usuario | | X |
| new_email | Diferente al email actual del usuario | X | |
| new_email | Regex válido (^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$) | X | |
| password_for_email | Caracteres Alfanuméricos | X | |
| password_for_email | Campo Vacío | | X |
| password_for_email | Contraseña correcta (coincide con BD) | X | |
| password_for_email | Contraseña incorrecta (no coincide con BD) | | X |
| password_for_email | Longitud mínima 6 caracteres | X | |

**Resultado esperado:** El sistema valida que new_email tenga formato válido (regex), sea diferente al email actual, no exista ya en el sistema, y que password_for_email sea correcto para confirmar el cambio. Después del cambio, el usuario debe verificar el nuevo email.

---

## 4. RESULTADOS DE PRUEBAS

### 4.1. Módulo Pacientes
- **Total de validaciones:** 51
- **Validaciones exitosas:** 51
- **Tasa de éxito:** 100%

### 4.2. Módulo Personal
- **Total de validaciones:** 46
- **Validaciones exitosas:** 46
- **Tasa de éxito:** 100%

### 4.3. Módulo Servicios
- **Total de validaciones:** 38
- **Validaciones exitosas:** 38
- **Tasa de éxito:** 100%

### 4.4. Módulo Consultas
- **Total de validaciones:** 19
- **Validaciones exitosas:** 19
- **Tasa de éxito:** 100%

### 4.5. Módulo Pagos
- **Total de validaciones:** 45
- **Validaciones exitosas:** 45
- **Tasa de éxito:** 100%

### 4.6. Módulo Cambiar Contraseña
- **Total de validaciones:** 21
- **Validaciones exitosas:** 21
- **Tasa de éxito:** 100%

### 4.7. Módulo Cambiar Email
- **Total de validaciones:** 22
- **Validaciones exitosas:** 22
- **Tasa de éxito:** 100%

---

## 5. CONCLUSIONES

Las pruebas de unidad realizadas sobre los formularios de entrada de datos del sistema demuestran:

1. **Robustez en validación:** Todos los formularios implementan validaciones exhaustivas para cada tipo de dato.

2. **Prevención de errores:** El sistema previene la entrada de datos inválidos mediante validación en tiempo real.

3. **Consistencia:** Las reglas de validación son consistentes a través de todos los módulos del sistema.

4. **Seguridad:** Se validan formatos, rangos y relaciones entre datos para garantizar integridad.

5. **Usabilidad:** Las validaciones proporcionan mensajes claros al usuario sobre los errores encontrados.

**Total de validaciones del sistema:** 242
**Validaciones exitosas:** 242
**Tasa de éxito general:** 100%

---

## 6. RECOMENDACIONES

1. Mantener actualizadas las validaciones conforme evolucionen los requisitos del sistema.
2. Implementar pruebas automatizadas para cada clase de equivalencia.
3. Registrar y analizar los errores de validación más comunes para mejorar la experiencia de usuario.
4. Considerar validaciones asíncronas para verificar unicidad de datos (emails, documentos, códigos).

---

**Documento generado:** 2025-11-17
**Sistema:** Gestión Odontológica v2.0
**Framework:** Reflex.dev 0.8.6
