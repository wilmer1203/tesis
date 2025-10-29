# TESTS UNITARIOS - REFACTORIZACION V3.0
## Sistema Odontologico - Tests Automatizados

**Fecha Creacion:** 2025-10-19
**Cobertura:** Funciones criticas V3.0
**Framework:** pytest

---

## ESTRUCTURA DE TESTS

```
tests/
├── __init__.py                      # Inicializador del paquete
├── conftest.py                      # Fixtures compartidos
├── test_normalizar_servicio.py      # Tests para _normalizar_servicio()
├── test_resolver_conflictos.py      # Tests para _resolver_conflictos_servicios()
├── test_modelos_v3.py               # Tests para modelos V3.0
└── README.md                        # Este archivo
```

---

## INSTALACION DE DEPENDENCIAS

### Instalar pytest

```bash
pip install pytest pytest-asyncio
```

### Verificar instalacion

```bash
pytest --version
```

---

## EJECUCION DE TESTS

### Ejecutar todos los tests

```bash
# Desde el directorio raiz del proyecto
cd C:\Users\wilme\Documents\tesis-main

# Ejecutar todos los tests
pytest tests/ -v
```

### Ejecutar archivo especifico

```bash
# Solo tests de normalizacion
pytest tests/test_normalizar_servicio.py -v

# Solo tests de resolucion de conflictos
pytest tests/test_resolver_conflictos.py -v

# Solo tests de modelos
pytest tests/test_modelos_v3.py -v
```

### Ejecutar test especifico

```bash
# Test especifico por nombre
pytest tests/test_normalizar_servicio.py::TestNormalizarServicio::test_normalizar_servicio_dict_completo -v
```

### Ejecutar con coverage

```bash
# Instalar coverage
pip install pytest-cov

# Ejecutar con reporte de cobertura
pytest tests/ --cov=dental_system.state --cov=dental_system.models --cov-report=html

# Ver reporte en navegador
# Abre: htmlcov/index.html
```

---

## DESCRIPCION DE TESTS

### 1. test_normalizar_servicio.py

**Proposito:** Validar la funcion `_normalizar_servicio()` que convierte 3 formatos de servicios a uno estandar.

**Casos cubiertos:**
- Normalizacion desde diccionario completo
- Normalizacion desde ServicioModel
- Normalizacion desde ServicioIntervencionTemporal (formato antiguo)
- Manejo de campos faltantes
- Manejo de superficies (string con comas, lista, vacio)
- Servicios preventivos (condicion_resultante = None)
- Compatibilidad con campo legacy nueva_condicion
- Edge cases: valores None, strings vacios, datos invalidos

**Total tests:** 22
**Clases:**
- TestNormalizarServicio (16 tests)
- TestNormalizarServicioEdgeCases (6 tests)

**Comando:**
```bash
pytest tests/test_normalizar_servicio.py -v
```

---

### 2. test_resolver_conflictos.py

**Proposito:** Validar la funcion `_resolver_conflictos_servicios()` que resuelve conflictos cuando multiples servicios afectan mismo diente/superficie.

**Casos cubiertos:**
- Sin conflictos (dientes diferentes)
- Sin conflictos (superficies diferentes)
- Conflicto resuelto por prioridad (gana mayor prioridad)
- Multiples superficies con conflictos parciales
- Servicios preventivos no generan conflictos
- Condicion no encontrada en catalogo (prioridad 0)
- Error al cargar catalogo (fallback seguro)
- Ausente con prioridad maxima siempre gana
- Misma prioridad (mantiene primero)
- Edge cases: lista vacia, superficies vacias, catalogo vacio

**Total tests:** 13
**Clases:**
- TestResolverConflictos (9 tests)
- TestResolverConflictosEdgeCases (4 tests)

**Comando:**
```bash
pytest tests/test_resolver_conflictos.py -v
```

**Nota:** Tests asyncronos requieren pytest-asyncio

---

### 3. test_modelos_v3.py

**Proposito:** Validar modelos de datos V3.0 y sus propiedades calculadas.

**Casos cubiertos:**

**CondicionCatalogoModel:**
- Creacion desde dict completo
- Valores por defecto
- Propiedad nombre_display con emoji
- Propiedad categoria_display
- Propiedad es_reversible
- Manejo de datos faltantes

**ActualizacionOdontogramaResult:**
- Creacion con valores default y especificos
- Propiedad total_procesados
- Propiedad tasa_exito_pct (100%, 0%, parcial, sin procesados)
- Propiedad tiene_advertencias
- Propiedad operacion_exitosa

**ServicioModel.condicion_resultante:**
- Servicio restaurativo con condicion
- Servicio preventivo sin condicion
- Metodo modifica_odontograma()
- Propiedad es_preventivo
- Propiedad tipo_servicio_display
- Propiedad condicion_display

**Integracion:**
- Flujo completo desde servicio hasta resultado
- Mapeo de codigo catalogo a servicio

**Total tests:** 30
**Clases:**
- TestCondicionCatalogoModel (6 tests)
- TestActualizacionOdontogramaResult (9 tests)
- TestServicioModelCondicionResultante (9 tests)
- TestModelosIntegracion (2 tests)

**Comando:**
```bash
pytest tests/test_modelos_v3.py -v
```

---

## FIXTURES DISPONIBLES (conftest.py)

### Fixtures de Datos Mock

- `mock_paciente_actual`: Paciente mock con id, nombre, documento
- `mock_servicio_dict`: Servicio en formato diccionario
- `mock_servicio_modelo`: Servicio como ServicioModel
- `mock_servicio_temporal`: Servicio formato antiguo
- `mock_servicios_con_conflicto`: Lista de servicios conflictivos
- `mock_catalogo_condiciones`: Catalogo con 5 condiciones y prioridades
- `mock_odontologia_service`: Mock del servicio con AsyncMock
- `mock_actualizacion_result`: Resultado de actualizacion mock
- `mock_estado_servicios`: Estado de servicios mock

### Uso de Fixtures

```python
def test_ejemplo(mock_paciente_actual, mock_servicio_dict):
    # Fixtures disponibles automaticamente
    assert mock_paciente_actual.id == "pac_123456"
    assert mock_servicio_dict["nombre_servicio"] == "Obturacion Composite"
```

---

## INTERPRETACION DE RESULTADOS

### Salida exitosa

```
============================== test session starts ==============================
collected 65 items

tests/test_normalizar_servicio.py ......................              [ 33%]
tests/test_resolver_conflictos.py .............                       [ 53%]
tests/test_modelos_v3.py ..............................                [100%]

============================== 65 passed in 2.35s ===============================
```

### Salida con fallos

```
============================== FAILURES ========================================
________ TestNormalizarServicio.test_normalizar_servicio_dict_completo ________

    def test_normalizar_servicio_dict_completo(self, mock_servicio_dict):
>       assert resultado["nombre"] == "Obturacion Composite"
E       AssertionError: assert 'Obturacion' == 'Obturacion Composite'

tests/test_normalizar_servicio.py:45: AssertionError
============================== 1 failed, 64 passed in 2.50s =====================
```

---

## TROUBLESHOOTING

### Error: ModuleNotFoundError

```
ModuleNotFoundError: No module named 'dental_system'
```

**Solucion:**
```bash
# Asegurate de estar en el directorio correcto
cd C:\Users\wilme\Documents\tesis-main

# O agrega el path manualmente
export PYTHONPATH="${PYTHONPATH}:C:\Users\wilme\Documents\tesis-main"
```

---

### Error: Import circular

```
ImportError: cannot import name 'EstadoIntervencionServicios'
```

**Solucion:**
Los tests ya manejan esto con try/except y pytest.skip(). Si persiste:
1. Verificar que todos los imports en el codigo fuente sean correctos
2. Ejecutar tests individuales en vez del suite completo

---

### Error: AsyncMock no encontrado

```
AttributeError: module 'unittest.mock' has no attribute 'AsyncMock'
```

**Solucion:**
```bash
# Instalar pytest-asyncio
pip install pytest-asyncio

# Python 3.7 no tiene AsyncMock, actualizar a Python 3.8+
python --version
```

---

### Tests asyncronos no se ejecutan

```
RuntimeWarning: coroutine was never awaited
```

**Solucion:**
```bash
# Instalar pytest-asyncio
pip install pytest-asyncio

# Agregar decorador @pytest.mark.asyncio a tests async
```

---

## COBERTURA ACTUAL

### Funciones Cubiertas

- `_normalizar_servicio()`: 22 tests
- `_resolver_conflictos_servicios()`: 13 tests
- `CondicionCatalogoModel`: 6 tests
- `ActualizacionOdontogramaResult`: 9 tests
- `ServicioModel.condicion_resultante`: 9 tests
- Integracion: 2 tests

**Total:** 65 tests unitarios

### Funciones NO Cubiertas (requieren tests de integracion)

- `_actualizar_odontograma_por_servicios()`: Requiere mock de BD y estado completo
- `cargar_catalogo_condiciones()`: Requiere conexion a BD
- `actualizar_condiciones_batch()`: Requiere BD transaccional

---

## PROXIMOS PASOS

### Tests de Integracion (Manual)

Para probar el flujo completo:

1. Ejecutar migracion SQL
```sql
-- Aplicar migracion
\i supabase/migrations/20251019_catalogo_condiciones_dentales.sql
```

2. Iniciar servidor Reflex
```bash
reflex run
```

3. Probar manualmente:
   - Crear servicio con condicion_resultante
   - Aplicar servicio en intervencion
   - Verificar actualizacion de odontograma
   - Verificar logs sin errores

---

## MANTENIMIENTO DE TESTS

### Agregar Nuevos Tests

1. Crear archivo `test_nueva_funcionalidad.py`
2. Importar fixtures de conftest.py
3. Crear clase TestNuevaFuncionalidad
4. Agregar tests con prefijo `test_`

### Actualizar Fixtures

Editar `conftest.py` y agregar/modificar fixtures segun necesidad.

### Ejecutar Tests en CI/CD

Agregar a pipeline:
```yaml
- name: Run tests
  run: |
    pip install pytest pytest-asyncio pytest-cov
    pytest tests/ -v --cov=dental_system --cov-report=xml
```

---

## CONTACTO

Para issues o mejoras de tests:
- Revisar REVISION_INTEGRACION_V3.md
- Consultar documentacion de pytest: https://docs.pytest.org/

---

**Generado:** 2025-10-19
**Autor:** Refactorizacion V3.0
**Version Tests:** 1.0
