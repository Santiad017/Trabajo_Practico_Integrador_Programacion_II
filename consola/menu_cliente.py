from consola.menu import Menu
from consola.lectura import leer_entero
from excepciones.food_store_exceptions import FoodStoreError

class MenuCliente(Menu):
    def mostrar(self) -> bool:
        while True:
            print(f"\n=== FOOD STORE CLIENTE ({self._usuario.nombre} {self._usuario.apellido}) ===")
            print("1. Ver categorías")
            print("2. Ver productos disponibles")
            print("3. Mis pedidos")
            print("4. Mis datos")
            print("9. Cerrar sesión")
            print("0. Salir")
            op = leer_entero("Seleccione: ")

            try:
                if op == 1:
                    cats = self._categoria_servicio.listar_todas()
                    if not cats:
                        print("No hay categorías disponibles.")
                    else:
                        print("\n--- CATÁLOGO DE CATEGORÍAS ---")
                        for c in cats:
                            print(c)
                elif op == 2:
                    categorias = self._categoria_servicio.listar_todas()
                    if not categorias:
                        print(">> No hay categorías disponibles actualmente.")
                        continue

                    print("\n--- VER PRODUCTOS POR CATEGORÍA ---")
                    print("0. Mostrar TODOS los productos disponibles")
                    for idx, cat in enumerate(categorias, start=1):
                        print(f"{idx}. {cat.nombre}")
                    
                    op_cat = leer_entero("Seleccione una opción: ")
                    
                    if op_cat == 0:
                        prods = self._producto_servicio.listar_disponibles_con_stock()
                    elif 1 <= op_cat <= len(categorias):
                        cat_seleccionada = categorias[op_cat - 1]
                        prods = self._producto_servicio.listar_disponibles_con_stock_por_categoria(cat_seleccionada.id)
                    else:
                        print(">> Opción fuera de rango.")
                        continue

                    if not prods:
                        print("\nNo hay productos disponibles en stock para esta selección.")
                    else:
                        print("\n--- PRODUCTOS DISPONIBLES ---")
                        for p in prods:
                            print(p)
                elif op == 3:
                    mis_peds = self._pedido_servicio.listar_por_usuario(self._usuario.id)
                    if not mis_peds:
                        print("Usted no registra pedidos realizados.")
                    else:
                        print("\n--- MIS PEDIDOS ---")
                        for ped in mis_peds:
                            print(ped)
                        ver_det = input("\n¿Desea consultar detalles de un pedido? Ingrese el ID o Enter para volver: ").strip()
                        if ver_det:
                            ped_id = int(ver_det)
                            ped = self._pedido_servicio.buscar_por_id(ped_id)
                            if ped.usuario.id != self._usuario.id:
                                print(">> No se encontró el pedido solicitado.")
                            else:
                                print(f"\nDetalles del Pedido #{ped.id}:")
                                for d in ped.detalles:
                                    if not d.eliminado:
                                        print(f"  * {d}")
                                print(f"Total: ${ped.total:.2f}")
                elif op == 4:
                    print("\n--- MIS DATOS DE PERFIL ---")
                    print(f"Nombre completo: {self._usuario.nombre} {self._usuario.apellido}")
                    print(f"Email:           {self._usuario.mail}")
                    print(f"Teléfono:        {self._usuario.celular}")
                    print(f"Rol:             {self._usuario.rol.name}")
                elif op == 9:
                    return True
                elif op == 0:
                    return False
                else:
                    print(">> Opción no válida.")
            except FoodStoreError as e:
                print(f">> Error: {e}")