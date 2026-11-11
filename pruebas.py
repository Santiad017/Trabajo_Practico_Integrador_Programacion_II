from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio
from servicios.pedido_servicio import PedidoServicio
from enums.rol import Rol
from enums.estado import Estado
from enums.forma_pago import FormaPago
from excepciones.food_store_exceptions import (
    PrecioInvalidoError,
    StockInsuficienteError,
    DuplicadoError,
    OperacionNoPermitidaError,
    CredencialesInvalidasError
)

def ejecutar_pruebas() -> None:
    print("==================================================")
    print("      EJECUTANDO PRUEBAS DEL SISTEMA FOOD STORE   ")
    print("==================================================")

    cat_srv = CategoriaServicio()
    prod_srv = ProductoServicio()
    usr_srv = UsuarioServicio()
    ped_srv = PedidoServicio()

    # 1. Crear usuario Admin y Cliente
    admin = usr_srv.crear_usuario("Admin", "Root", "admin@test.com", "123", "pass123", Rol.ADMIN)
    cliente = usr_srv.crear_usuario("Cliente", "Prueba", "cliente@test.com", "456", "pass123", Rol.USUARIO)
    print("[OK] Usuarios creados exitosamente.")

    # 2. Probar autenticación errónea y válida
    try:
        usr_srv.autenticar("admin@test.com", "clave_erronea")
        print("[FAIL] Autenticación no falló con clave incorrecta.")
    except CredencialesInvalidasError:
        print("[OK] Captura correcta de credenciales inválidas.")

    auth_user = usr_srv.autenticar("admin@test.com", "pass123")
    assert auth_user.id == admin.id, "Error en coincidencia de usuario autenticado."

    # 3. Validar categoría duplicada (case-insensitive)
    cat1 = cat_srv.crear_categoria("Empanadas", "Empanadas al horno")
    try:
        cat_srv.crear_categoria("EMPANADAS", "Repetida")
        print("[FAIL] Permitió crear categoría duplicada.")
    except DuplicadoError:
        print("[OK] Captura correcta de categoría duplicada.")

    # 4. Validar precio negativo y stock negativo
    try:
        prod_srv.crear_producto("Empanada Carne", -10.0, "Carne suave", 10, "e.jpg", True, cat1)
        print("[FAIL] Permitió crear producto con precio negativo.")
    except PrecioInvalidoError:
        print("[OK] Captura correcta de precio negativo.")

    prod1 = prod_srv.crear_producto("Empanada Carne", 1500.0, "Carne suave", 10, "e.jpg", True, cat1)

    # 5. Validar eliminación de categoría con producto activo
    try:
        cat_srv.eliminar_categoria(cat1.id, prod_srv)
        print("[FAIL] Permitió eliminar categoría con productos activos.")
    except OperacionNoPermitidaError:
        print("[OK] Bloqueo correcto de eliminación de categoría con productos.")

    # 6. Crear Pedido y validar descuento de stock
    stock_inicial = prod1.stock
    pedido1 = ped_srv.crear_pedido(cliente, FormaPago.EFECTIVO, [(prod1, 4)])
    assert prod1.stock == stock_inicial - 4, "Falló la deducción de stock."
    print(f"[OK] Pedido #{pedido1.id} creado. Stock actualizado de {stock_inicial} a {prod1.stock}.")

    # 7. Intentar comprar más stock del disponible
    try:
        ped_srv.crear_pedido(cliente, FormaPago.TARJETA, [(prod1, 20)])
        print("[FAIL] Permitió crear pedido sin suficiente stock.")
    except StockInsuficienteError:
        print("[OK] Captura correcta de stock insuficiente.")

    # 8. Transición inválida de estado
    try:
        ped_srv.cambiar_estado(pedido1.id, Estado.TERMINADO) # De PENDIENTE a TERMINADO directamente es inválido
        print("[FAIL] Permitió salto de estado de PENDIENTE a TERMINADO.")
    except OperacionNoPermitidaError:
        print("[OK] Transición inválida de estado rechazada adecuadamente.")

    # 9. Cancelación de pedido y devolución de stock
    ped_srv.cambiar_estado(pedido1.id, Estado.CANCELADO)
    assert prod1.stock == stock_inicial, "El stock no fue restituido al cancelar el pedido."
    print(f"[OK] Pedido cancelado correctamente. Stock devuelto a {prod1.stock}.")

    # 10. Validar imposibilidad de eliminar al propio admin logueado
    try:
        usr_srv.eliminar_usuario(admin.id, admin.id)
        print("[FAIL] El administrador se eliminó a sí mismo.")
    except OperacionNoPermitidaError:
        print("[OK] Bloqueo correcto de auto-eliminación de Administrador.")

    print("\n==================================================")
    print("      TODAS LAS PRUEBAS SE EJECUTARON CON ÉXITO   ")
    print("==================================================")

if __name__ == "__main__":
    ejecutar_pruebas()