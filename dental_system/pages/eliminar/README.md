# 📁 Archivos Descontinuados - Dental System

Este directorio contiene archivos que han sido descontinuados o reemplazados por versiones mejoradas. Se mantienen como referencia histórica pero no son parte del sistema activo.

## 🔄 Módulo de Consultas

### Archivos Movidos:
- `consultas_page_old.py` - Versión inicial (obsoleta)
- `consultas_page_new.py` - Segunda versión (reemplazada)
- `consultas_page_optimizada.py` - Versión de optimización (incorporada en v41)

### ✅ Versión Actual:
- **`consultas_page_v41.py`** - Versión definitiva que incluye:
  - Optimizaciones de rendimiento
  - Sistema de colas mejorado
  - Integración completa con el estado de autenticación
  - Manejo mejorado de errores

## 🏥 Módulo de Intervención

### Archivos Movidos:
- `intervencion_page.py` - Versión inicial básica
- `intervencion_page_simple.py` - Versión simplificada (no implementada)
- `intervencion_page_v2_fixed.py` - Correcciones incorporadas en v2
- `intervencion_page_v3_mejorada.py` - Mejoras no implementadas

### ✅ Versiones Actuales:
- **`intervencion_page_v2.py`** - Versión principal que incluye:
  - Sistema completo de intervenciones
  - Integración con odontograma
  - Manejo de estados avanzado
- **`intervencion_advanced_page.py`** - Módulo especializado para casos complejos

## 🧪 Archivos de Prueba

### Archivos Movidos:
- `test_fdi_page.py` - Pruebas antiguas del sistema FDI
- `testing_page.py` - Página de pruebas general

### ✅ Testing Actual:
Las pruebas ahora se manejan a través de:
- Tests unitarios en `/dental_system/components/testing/`
- Pruebas de integración automatizadas
- `test_selector.py` como única interfaz de pruebas en producción

## 📝 Notas Importantes

1. **No Eliminar**: Estos archivos se mantienen como referencia histórica
2. **No Importar**: No deben ser importados en código nuevo
3. **Documentación**: Ver CHANGELOG.md para detalles de los cambios
4. **Migración**: Todo el código útil ya ha sido migrado a las versiones actuales

## 🔄 Proceso de Limpieza (17/09/2025)

- [x] Identificación de archivos obsoletos
- [x] Movimiento a carpeta 'eliminar'
- [x] Verificación de imports y dependencias
- [x] Documentación de cambios
- [ ] Periodo de observación antes de eliminación definitiva

## 👥 Mantenimiento

Si encuentras código que podría ser útil en estos archivos, por favor:
1. Consulta primero si ya existe en las versiones actuales
2. Documenta la necesidad específica
3. Propón la migración a través del sistema de tickets