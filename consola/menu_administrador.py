from consola.menu import Menu
from consola.lectura import (
    leer_entero, leer_texto, leer_opcional_texto, leer_flotante,
    leer_opcional_flotante, leer_opcional_entero, leer_enum, confirmar_accion
)
from enums.rol import Rol
from enums.estado import Estado
from enums.forma_pago import FormaPago
from excepciones.food_store_exceptions import FoodStoreError

class MenuAdministrador(Menu):
    def mostrar(self) -> bool:
        while True:
            print(f"\n=== FOOD STORE ADMINISTRADOR ({self._usuario.nombre} {self._usuario.apellido}) ===")
            print("1. Categorías")
            print("2. Productos")
            print("3. Usuarios")
            print("4. Pedidos")
            print("9. Cerrar sesión")
            print("0. Salir")
            op = leer_entero("Seleccione: ")

            if op == 1:
                self._menu_categorias()
            elif op == 2:
                self._menu_productos()
            elif op == 3:
                self._menu_usuarios()
            elif op == 4:
                self._menu_pedidos()
            elif op == 9:
                return True
            elif op == 0:
                return False
            else:
                print(">> Opción no válida.")

    def _menu_categorias(self) -> None:
        while True:
            print("\n--- CATEGORÍAS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver")
            op = leer_entero("Seleccione: ")

            try:
                if op == 1:
                    cats = self._categoria_servicio.listar_todas()
                    if not cats:
                        print("No hay categorías cargadas.")
                    else:
                        for c in cats:
                            print(c)
                elif op == 2:
                    nom = leer_texto("Nombre de la categoría: ")
                    desc = input("Descripción: ").strip()
                    cat = self._categoria_servicio.crear_categoria(nom, desc)
                    print(f"Categoría creada con éxito. ID: {cat.id}")
                elif op == 3:
                    cat_id = leer_entero("ID de la categoría a editar: ")
                    cat = self._categoria_servicio.buscar_por_id(cat_id)
                    n_nom = leer_opcional_texto("Nuevo nombre", cat.nombre)
                    n_desc = leer_opcional_texto("Nueva descripción", cat.descripcion)
                    self._categoria_servicio.editar_categoria(cat_id, n_nom, n_desc)
                    print("Categoría actualizada correctamente.")
                elif op == 4:
                    cat_id = leer_entero("ID de la categoría a eliminar: ")
                    if confirmar_accion("¿Está seguro de eliminar la categoría?"):
                        self._categoria_servicio.eliminar_categoria(cat_id, self._producto_servicio)
                        print("Categoría eliminada con éxito.")
                elif op == 0:
                    break
            except FoodStoreError as e:
                print(f">> Error de Negocio: {e}")

    def _menu_productos(self) -> None:
        while True:
            print("\n--- PRODUCTOS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver")
            op = leer_entero("Seleccione: ")

            try:
                if op == 1:
                    prods = self._producto_servicio.listar_todos()
                    if not prods:
                        print("No hay productos registrados.")
                    else:
                        for p in prods:
                            print(p)
                elif op == 2:
                    nom = leer_texto("Nombre del producto: ")
                    precio = leer_flotante("Precio: ")
                    desc = input("Descripción: ").strip()
                    stk = leer_entero("Stock inicial: ")
                    img = input("URL/Ruta imagen: ").strip()
                    disp = confirmar_accion("¿Está disponible para la venta?")
                    cat_id = leer_entero("ID de la Categoría asociada: ")
                    cat = self._categoria_servicio.buscar_por_id(cat_id)
                    p = self._producto_servicio.crear_producto(nom, precio, desc, stk, img, disp, cat)
                    print(f"Producto creado con éxito. ID: {p.id}")
                elif op == 3:
                    p_id = leer_entero("ID del producto a editar: ")
                    p = self._producto_servicio.buscar_por_id(p_id)
                    n_nom = leer_opcional_texto("Nuevo nombre", p.nombre)
                    n_prec = leer_opcional_flotante("Nuevo precio", p.precio)
                    n_desc = leer_opcional_texto("Nueva descripción", p.descripcion)
                    n_stk = leer_opcional_entero("Nuevo stock", p.stock)
                    n_img = leer_opcional_texto("Nueva imagen", p.imagen)
                    n_disp = confirmar_accion("¿Está disponible?") if input("¿Cambiar disponibilidad? (Enter omite): ").strip() else p.disponible
                    
                    cat_opt = input("ID de nueva categoría (Enter conserva): ").strip()
                    n_cat = self._categoria_servicio.buscar_por_id(int(cat_opt)) if cat_opt else p.categoria

                    self._producto_servicio.editar_producto(
                        p_id, n_nom, n_prec, n_desc, n_stk, n_img, n_disp, n_cat
                    )
                    print("Producto actualizado.")
                elif op == 4:
                    p_id = leer_entero("ID del producto a eliminar: ")
                    if confirmar_accion("¿Confirmar eliminación lógica del producto?"):
                        self._producto_servicio.eliminar_producto(p_id)
                        print("Producto eliminado.")
                elif op == 0:
                    break
            except FoodStoreError as e:
                print(f">> Error de Negocio: {e}")

    def _menu_usuarios(self) -> None:
        while True:
            print("\n--- USUARIOS ---")
            print("1. Listar")
            print("2. Crear")
            print("3. Editar")
            print("4. Eliminar")
            print("0. Volver")
            op = leer_entero("Seleccione: ")

            try:
                if op == 1:
                    usrs = self._usuario_servicio.listar_todos()
                    if not usrs:
                        print("No hay usuarios cargados.")
                    else:
                        for u in usrs:
                            print(u)
                elif op == 2:
                    nom = leer_texto("Nombre: ")
                    ape = leer_texto("Apellido: ")
                    mail = leer_texto("Mail: ")
                    cel = input("Celular: ").strip()
                    pwd = leer_texto("Contraseña: ")
                    rol = leer_enum(Rol, "Rol de usuario")
                    u = self._usuario_servicio.crear_usuario(nom, ape, mail, cel, pwd, rol)
                    print(f"Usuario registrado con éxito. ID: {u.id}")
                elif op == 3:
                    u_id = leer_entero("ID del usuario a editar: ")
                    u = self._usuario_servicio.buscar_por_id(u_id)
                    n_nom = leer_opcional_texto("Nuevo nombre", u.nombre)
                    n_ape = leer_opcional_texto("Nuevo apellido", u.apellido)
                    n_mail = leer_opcional_texto("Nuevo mail", u.mail)
                    n_cel = leer_opcional_texto("Nuevo celular", u.celular)
                    n_rol = leer_enum(Rol, "Nuevo Rol") if input("¿Cambiar rol? (Enter omite): ").strip() else u.rol

                    self._usuario_servicio.editar_usuario(u_id, n_nom, n_ape, n_mail, n_cel, n_rol)
                    print("Usuario actualizado.")
                elif op == 4:
                    u_id = leer_entero("ID del usuario a eliminar: ")
                    if confirmar_accion("¿Confirmar baja lógica del usuario?"):
                        self._usuario_servicio.eliminar_usuario(u_id, self._usuario.id)
                        print("Usuario eliminado.")
                elif op == 0:
                    break
            except FoodStoreError as e:
                print(f">> Error de Negocio: {e}")

    def _menu_pedidos(self) -> None:
        while True:
            print("\n--- PEDIDOS ---")
            print("1. Listar pedidos")
            print("2. Crear pedido")
            print("3. Cambiar estado / forma de pago")
            print("4. Eliminar pedido")
            print("0. Volver")
            op = leer_entero("Seleccione: ")

            try:
                if op == 1:
                    peds = self._pedido_servicio.listar_todos()
                    if not peds:
                        print("No hay pedidos registrados.")
                    else:
                        for ped in peds:
                            print(ped)
                            for d in ped.detalles:
                                if not d.eliminado:
                                    print(f"   -> {d}")
                elif op == 2:
                    u_id = leer_entero("ID del cliente asignado: ")
                    usr = self._usuario_servicio.buscar_por_id(u_id)
                    fp = leer_enum(FormaPago, "Forma de Pago")

                    items = []
                    while True:
                        p_id = leer_entero("ID del Producto a agregar: ")
                        prod = self._producto_servicio.buscar_por_id(p_id)
                        cant = leer_entero(f"Cantidad para '{prod.nombre}': ")
                        items.append((prod, cant))

                        if not confirmar_accion("¿Agregar otro producto a este pedido?"):
                            break

                    nuevo_ped = self._pedido_servicio.crear_pedido(usr, fp, items)
                    print(f"Pedido registrado exitosamente. ID: {nuevo_ped.id} | Total: ${nuevo_ped.total:.2f}")
                elif op == 3:
                    p_id = leer_entero("ID del pedido a modificar: ")
                    ped = self._pedido_servicio.buscar_por_id(p_id)
                    print(f"Pedido seleccionado: {ped}")
                    if confirmar_accion("¿Desea cambiar el estado?"):
                        nuevo_est = leer_enum(Estado, "Nuevo Estado")
                        self._pedido_servicio.cambiar_estado(p_id, nuevo_est)
                    if confirmar_accion("¿Desea cambiar la forma de pago?"):
                        nueva_fp = leer_enum(FormaPago, "Nueva Forma de Pago")
                        ped.forma_pago = nueva_fp
                    print("Pedido actualizado.")
                elif op == 4:
                    p_id = leer_entero("ID del pedido a eliminar: ")
                    if confirmar_accion("¿Confirmar eliminación del pedido?"):
                        self._pedido_servicio.eliminar_pedido(p_id)
                        print("Pedido eliminado correctamente.")
                elif op == 0:
                    break
            except FoodStoreError as e:
                print(f">> Error de Negocio: {e}")