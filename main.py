from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio
from servicios.pedido_servicio import PedidoServicio
from enums.rol import Rol
from consola.menu import crear_menu
from excepciones.food_store_exceptions import CredencialesInvalidasError
import getpass

def cargar_datos_iniciales(
    u_srv: UsuarioServicio,
    c_srv: CategoriaServicio,
    p_srv: ProductoServicio
) -> None:
    admin = u_srv.crear_usuario(
        nombre="Ana",
        apellido="Pérez",
        mail="admin@foodstore.com",
        celular="1122334455",
        contrasenia="admin123",
        rol=Rol.ADMIN
    )
    
    cliente = u_srv.crear_usuario(
        nombre="Juan",
        apellido="Gómez",
        mail="juan@foodstore.com",
        celular="1199887766",
        contrasenia="user123",
        rol=Rol.USUARIO
    )

    cat_pizzas = c_srv.crear_categoria("Pizzas", "Pizzas artesanales al horno de barro")
    cat_bebidas = c_srv.crear_categoria("Bebidas", "Gaseosas y jugos frescos")

    p_srv.crear_producto("Pizza Muzarella", 8500.0, "Salsa de tomate, muzarella y orégano", 15, "muzza.jpg", True, cat_pizzas)
    p_srv.crear_producto("Coca-Cola 1.5L", 2500.0, "Gaseosa cola", 30, "coca.jpg", True, cat_bebidas)

def main() -> None:
    cat_srv = CategoriaServicio()
    prod_srv = ProductoServicio()
    usr_srv = UsuarioServicio()
    ped_srv = PedidoServicio()

    cargar_datos_iniciales(usr_srv, cat_srv, prod_srv)

    ejecutando_sistema = True

    while ejecutando_sistema:
        print("\n===================================")
        print("=== FOOD STORE INICIO DE SESIÓN ===")
        print("===================================")

        intentos = 0
        usuario_logueado = None

        while intentos < 3:
            mail = input("Mail: ").strip()
            try:
                contrasenia = getpass.getpass("Contraseña: ")
            except Exception:
                contrasenia = input("Contraseña: ")

            try:
                usuario_logueado = usr_srv.autenticar(mail, contrasenia)
                print(f"\n¡Bienvenido/a, {usuario_logueado.nombre} {usuario_logueado.apellido} [{usuario_logueado.rol.name}]!")
                break
            except CredencialesInvalidasError as e:
                intentos += 1
                print(f">> {e}. Intentos restantes: {3 - intentos}")

        if not usuario_logueado:
            print("\n>> Se ha superado el número máximo de intentos de inicio de sesión. Programa finalizado.")
            ejecutando_sistema = False
            break

        menu_usuario = crear_menu(usuario_logueado, cat_srv, prod_srv, usr_srv, ped_srv)
        cerrar_sesion = menu_usuario.mostrar()

        if not cerrar_sesion:
            print("\n¡Gracias por utilizar Food Store! Hasta luego.")
            ejecutando_sistema = False

if __name__ == "__main__":
    main()