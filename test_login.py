#!/usr/bin/env python3
"""
🔍 VERIFICACIÓN MANUAL DEL MÉTODO LOGIN
Script para verificar que el decorador esté correctamente aplicado
"""

def check_login_method_decorator():
    """Verificación detallada del decorador del método login"""
    print("🔍 VERIFICACIÓN MANUAL DEL DECORADOR @rx.event")
    print("=" * 60)
    
    try:
        # Import del AppState
        from dental_system.state.app_state import AppState
        print("✅ AppState importado exitosamente")
        
        # Obtener el método login
        login_method = getattr(AppState, 'login', None)
        if not login_method:
            print("❌ Método login no encontrado en AppState")
            return False
        
        print("✅ Método login encontrado")
        
        # Verificar todos los atributos del método
        print("\n📋 Atributos del método login:")
        for attr_name in dir(login_method):
            if not attr_name.startswith('_'):
                continue
            attr_value = getattr(login_method, attr_name, None)
            print(f"  {attr_name}: {attr_value}")
        
        # Verificaciones específicas de Reflex
        reflex_checks = {
            '_reflex_event': hasattr(login_method, '_reflex_event'),
            '__qualname__': hasattr(login_method, '__qualname__'),
            '__annotations__': hasattr(login_method, '__annotations__'),
            'callable': callable(login_method)
        }
        
        print("\n🎯 Verificaciones específicas de Reflex:")
        for check, result in reflex_checks.items():
            print(f"  {'✅' if result else '❌'} {check}: {result}")
        
        # Verificar firma del método
        import inspect
        signature = inspect.signature(login_method)
        print(f"\n📝 Firma del método: {signature}")
        print(f"📝 Parámetros: {list(signature.parameters.keys())}")
        
        # Verificar que sea async
        is_async = inspect.iscoroutinefunction(login_method)
        print(f"⚡ Es función async: {'✅' if is_async else '❌'}")
        
        return all(reflex_checks.values()) and is_async
        
    except Exception as e:
        print(f"❌ Error en verificación: {e}")
        import traceback
        traceback.print_exc()
        return False

def show_app_state_structure():
    """Mostrar estructura del AppState"""
    print("\n🏗️ ESTRUCTURA DE APPSTATE")
    print("=" * 60)
    
    try:
        from dental_system.state.app_state import AppState
        
        # Obtener todos los métodos
        methods = [method for method in dir(AppState) if not method.startswith('_')]
        event_methods = []
        regular_methods = []
        
        for method_name in methods:
            method = getattr(AppState, method_name)
            if callable(method):
                if hasattr(method, '_reflex_event'):
                    event_methods.append(method_name)
                else:
                    regular_methods.append(method_name)
        
        print(f"📊 Total de métodos: {len(methods)}")
        print(f"🎯 Métodos con @rx.event: {len(event_methods)}")
        print(f"🔧 Métodos regulares: {len(regular_methods)}")
        
        print(f"\n🎯 Métodos con @rx.event detectados:")
        for method in event_methods:
            print(f"  ✅ {method}")
        
        if 'login' not in event_methods:
            print(f"\n❌ 'login' NO está en la lista de métodos con @rx.event")
            if 'login' in regular_methods:
                print(f"⚠️ 'login' está en métodos regulares - falta @rx.event")
        else:
            print(f"\n✅ 'login' está correctamente detectado como @rx.event")
        
        return 'login' in event_methods
        
    except Exception as e:
        print(f"❌ Error obteniendo estructura: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 VERIFICACIÓN MANUAL COMPLETA")
    print("=" * 70)
    
    # Test 1: Verificar decorador
    decorator_ok = check_login_method_decorator()
    
    # Test 2: Verificar estructura
    structure_ok = show_app_state_structure()
    
    # Resumen
    print(f"\n📊 RESUMEN FINAL")
    print("=" * 60)
    print(f"Decorador aplicado: {'✅' if decorator_ok else '❌'}")
    print(f"Estructura correcta: {'✅' if structure_ok else '❌'}")
    
    if decorator_ok and structure_ok:
        print("\n🎉 ¡TODO ESTÁ CORRECTO!")
        print("Si el login aún no funciona, el problema está en:")
        print("  1. 🌐 El frontend (JavaScript/navegador)")
        print("  2. 🔄 Cache del navegador")
        print("  3. 📡 La comunicación frontend-backend")
    else:
        print("\n⚠️ AÚN HAY PROBLEMAS:")
        if not decorator_ok:
            print("  ❌ El decorador @rx.event no está correctamente aplicado")
        if not structure_ok:
            print("  ❌ La estructura del AppState tiene problemas")

if __name__ == "__main__":
    main()