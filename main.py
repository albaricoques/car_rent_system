# ==============================================================================
# TRABAJO PARCIAL - SISTEMA DE GESTIÓN DE ALQUILER DE VEHÍCULOS
# PARADIGMA: PROGRAMACIÓN ORIENTADA A OBJETOS (POO)
# ==============================================================================

# ===========================
# Excepciones personalizads
# ===========================
class VehiculoDuplicadoError(Exception):
    pass

class ClienteNoEncontradoError(Exception):
    pass

class VehiculoOcupadoError(Exception):
    pass

# ==========================
# Módulo de flota
# ==========================
class Vehiculo:
    def __init__(self, placa, marca, modelo, precio_diario):
        self._placa = placa
        self._marca = marca
        self._modelo = modelo
        self._precio_diario = precio_diario
        self._disponible = True

    def get_placa(self): return self._placa
    def get_marca(self): return self._marca
    def get_modelo(self): return self._modelo
    def get_precio_diario(self): return self._precio_diario
    def is_disponible(self): return self._disponible
    def set_disponibilidad(self, estado: bool): self._disponible = estado

    #Método polimórfico
    def calcular_tarifa(self, dias):
        return self._precio_diario * dias

    def __str__(self):
        estado = "Disponible" if self._disponible else "Alquilado"
        return f"[{self._placa}] {self._marca} {self._modelo} - S/ {self._precio_diario:.2f}/día ({estado})"

# Subclases (Herencia)
# --------------------

# Subclase 1
class AutoCompacto(Vehiculo):
    def __init__(self, placa, marca, modelo, precio_diario, rendimiento_km):
        super().__init__(placa, marca, modelo, precio_diario)
        self._rendimiento_km = rendimiento_km

    def __str__(self):
        return super().__str__() + f" | Económico: {self._rendimiento_km} km/gal"

# Subclase 2
class CamionetaSUV(Vehiculo):
    def __init__(self, placa, marca, modelo, precio_diario, traccion_4x4: bool):
        super().__init__(placa, marca, modelo, precio_diario)
        self._traccion_4x4 = traccion_4x4

    def calcular_tarifa(self, dias):
        tarifa_base = super().calcular_tarifa(dias)
        seguro_todoterreno = 20.0 * dias
        return tarifa_base + seguro_todoterreno

    def __str__(self):
        traccion = "4x4" if self._traccion_4x4 else "4x2"
        return super().__str__() + f" | SUV Todoterreno ({traccion})"
    
#============================
# Modulo de clientes
#============================
class Cliente:
    def __init__(self, dni, nombre, categoria_licencia, anio_emision):
        self._dni = dni
        self._nombre = nombre
        self._licencia = (categoria_licencia, anio_emision)
        self._historial_reservas = []

    def get_dni(self): return self._dni
    def get_nombre(self): return self._nombre
    def get_licencia(self): return self._licencia
    def get_historial(self): return self._historial_reservas
    def agregar_al_historial(self, id_reserva): self._historial_reservas.append(id_reserva)

    def aplicar_descuento(self, monto):
        return monto

    def __str__(self):
        cat, anio = self._licencia
        return f"[{self._dni}] {self._nombre} | Licencia: {cat} ({anio}) | Alquileres: {len(self._historial_reservas)}"


class ClienteRegular(Cliente):
    def __init__(self, dni, nombre, categoria_licencia, anio_emision):
        super().__init__(dni, nombre, categoria_licencia, anio_emision)

    def __str__(self):
        return "[REGULAR] " + super().__str__()


class ClienteVip(Cliente):
    def __init__(self, dni, nombre, categoria_licencia, anio_emision, codigo_membresia):
        super().__init__(dni, nombre, categoria_licencia, anio_emision)
        self._codigo_membresia = codigo_membresia

    def aplicar_descuento(self, monto):
        return monto * 0.85

    def __str__(self):
        return f"[VIP - {self._codigo_membresia}] " + super().__str__()


# =============================
# Módulo de operaciones
# =============================
class Reserva:
    def __init__(self, id_reserva, cliente, vehiculo, dias):
        self._id_reserva = id_reserva
        self._cliente = cliente
        self._vehiculo = vehiculo
        self._dias = dias
        self._activa = True
        
        # El auto calcula su tarifa (tarifa normal o con seguro 4x4)
        tarifa_bruta = self._vehiculo.calcular_tarifa(self._dias)
        
        # El cliente aplica su beneficio (precio regular o descuento VIP)
        self._costo_total = self._cliente.aplicar_descuento(tarifa_bruta)

    def get_id(self): return self._id_reserva
    def get_vehiculo(self): return self._vehiculo
    def get_cliente(self): return self._cliente
    def get_costo_total(self): return self._costo_total
    def is_activa(self): return self._activa
    def finalizar_reserva(self): self._activa = False

    def __str__(self):
        estado = "EN CURSO" if self._activa else "FINALIZADA"
        placa = self._vehiculo.get_placa()
        nombre = self._cliente.get_nombre()
        return f"[{self._id_reserva}] {placa} -> {nombre} por {self._dias} días | Total: S/ {self._costo_total:.2f} ({estado})"


# ===================================
# Controlador central del sistema
# ====================================
class SistemaAlquiler:
    def __init__(self):
        self._flota = {}           
        self._clientes = {}         
        self._reservas = {}         
        self._vehiculos_en_ruta = set() 

    # Métodos del modulo flota
    #-------------------------
    def registrar_vehiculo(self, vehiculo):
        placa = vehiculo.get_placa()
        if placa in self._flota:
            raise VehiculoDuplicadoError(f"Error: El vehículo con placa {placa} ya está registrado.")
        self._flota[placa] = vehiculo
        print(f"Éxito: Vehículo {placa} registrado correctamente.")

    def buscar_vehiculo(self, placa):
        return self._flota.get(placa)

    def mostrar_disponibles(self):
        print("\n--- VEHÍCULOS DISPONIBLES PARA ALQUILER ---")
        hay_disponibles = False
        for vehiculo in self._flota.values():
            if vehiculo.is_disponible():
                print(vehiculo)
                hay_disponibles = True
        if not hay_disponibles:
            print("No hay vehículos disponibles en este momento.")
        print("-------------------------------------------\n")

    # Métodos del modulo clientes
    #-----------------------------
    def registrar_cliente(self, cliente):
        dni = cliente.get_dni()
        if dni in self._clientes:
            print(f"Aviso: El cliente con DNI {dni} ya se encuentra registrado.")
        else:
            self._clientes[dni] = cliente
            print(f"Éxito: Cliente {cliente.get_nombre()} registrado correctamente.")

    def buscar_cliente(self, dni):
        if dni not in self._clientes:
            raise ClienteNoEncontradoError(f"Error: No se encontró ningún cliente con el DNI '{dni}'.")
        return self._clientes[dni]

    def validar_licencia(self, dni, categoria_requerida):
        cliente = self.buscar_cliente(dni)
        categoria_cliente, _ = cliente.get_licencia()
        
        if categoria_cliente == categoria_requerida or categoria_cliente == "A-III":
            return True
        else:
            print(f"Denegado: {cliente.get_nombre()} tiene licencia {categoria_cliente}, pero requiere {categoria_requerida} o profesional.")
            return False

    def mostrar_clientes(self):
        print("\n--- DIRECTORIO DE CLIENTES REGISTRADOS ---")
        if not self._clientes:
            print("No hay clientes registrados.")
        else:
            for cliente in self._clientes.values():
                print(cliente)
        print("------------------------------------------\n")

    # Métodos del modulo operaciones
    #--------------------------------
    def generar_reserva(self, id_reserva, cliente, vehiculo, dias):
        placa = vehiculo.get_placa()
        if placa in self._vehiculos_en_ruta:
            raise VehiculoOcupadoError(f"Error: El vehículo {placa} ya se encuentra alquilado.")

        nueva_reserva = Reserva(id_reserva, cliente, vehiculo, dias)
        self._reservas[id_reserva] = nueva_reserva
        self._vehiculos_en_ruta.add(placa)
        cliente.agregar_al_historial(id_reserva)
        print(f"Éxito: Reserva {id_reserva} generada exitosamente. Total a pagar: S/ {nueva_reserva.get_costo_total():.2f}")

    def procesar_devolucion(self, id_reserva):
        if id_reserva not in self._reservas:
            print(f"Error: La reserva {id_reserva} no existe.")
            return
        reserva = self._reservas[id_reserva]
        if not reserva.is_activa():
            print(f"Aviso: La reserva {id_reserva} ya había sido finalizada anteriormente.")
            return
            
        reserva.finalizar_reserva()
        placa = reserva.get_vehiculo().get_placa()
        self._vehiculos_en_ruta.discard(placa)
        print(f"Éxito: Vehículo {placa} devuelto en perfectas condiciones. Reserva {id_reserva} cerrada.")

    def calcular_ingresos_totales(self):
        total = sum(res.get_costo_total() for res in self._reservas.values())
        print(f"\n>>> INGRESOS TOTALES DEL SISTEMA: S/ {total:.2f} <<<")


# ============================
# Menú interactivo
# =============================
if __name__ == "__main__":
    sistema = SistemaAlquiler()
    
    # Datos inicialis (todas las subclases cubiertas)
    sistema.registrar_vehiculo(AutoCompacto("ABC-123", "Toyota", "Yaris", 100.0, 55))
    sistema.registrar_vehiculo(CamionetaSUV("XYZ-987", "Ford", "Explorer", 200.0, True))
    sistema.registrar_cliente(ClienteRegular("77778888", "Carlos Rojas", "A-I", 2020))
    sistema.registrar_cliente(ClienteVip("11122233", "Ana Peralta", "A-III", 2018, "VIP-GOLD"))
    
    contador_reservas = 1

    while True:
        print("\n" + "="*50)
        print("     SISTEMA DE ALQUILER DE VEHÍCULOS (POO)")
        print("="*50)
        print("1. Registrar nuevo Vehículo (Compacto / SUV)")
        print("2. Registrar nuevo Cliente (Regular / VIP)")
        print("3. Generar Reserva (Demostración de Polimorfismo)")
        print("4. Procesar Devolución")
        print("5. Ver Directorio de Clientes")
        print("6. Ver Historial de Alquileres de un Cliente")
        print("7. Buscar un Vehículo por Placa")
        print("8. Ver Flota Disponible y Cuadre de Caja")
        print("9. Salir")
        print("="*50)
        
        opcion = input("Seleccione una opción (1-9): ")

        if opcion == "1":
            print("\n--- REGISTRO DE VEHÍCULO ---")
            tipo = input("Tipo de vehículo (1: Auto Compacto | 2: Camioneta SUV): ")
            placa = input("Placa: ").upper()
            marca = input("Marca: ").capitalize()
            modelo = input("Modelo: ").capitalize()
            
            try:
                precio = float(input("Precio diario base (S/): "))
                if tipo == "1":
                    rendimiento = int(input("Rendimiento (km/gal): "))
                    sistema.registrar_vehiculo(AutoCompacto(placa, marca, modelo, precio, rendimiento))
                elif tipo == "2":
                    traccion = input("¿Tiene tracción 4x4? (s/n): ").lower() == 's'
                    sistema.registrar_vehiculo(CamionetaSUV(placa, marca, modelo, precio, traccion))
                else:
                    print("Opción de tipo inválida.")
            except ValueError:
                print("Error: Los valores numéricos son incorrectos.")
            except VehiculoDuplicadoError as e:
                print(e)

        elif opcion == "2":
            print("\n--- REGISTRO DE CLIENTE ---")
            tipo = input("Tipo de cliente (1: Regular | 2: VIP con 15% Dscto): ")
            dni = input("DNI (8 dígitos): ")
            nombre = input("Nombre completo: ").title()
            licencia = input("Categoría de Licencia (ej. A-I): ").upper()
            
            try:
                anio = int(input("Año de emisión de la licencia: "))
                if tipo == "1":
                    sistema.registrar_cliente(ClienteRegular(dni, nombre, licencia, anio))
                elif tipo == "2":
                    codigo = input("Código de Membresía VIP: ").upper()
                    sistema.registrar_cliente(ClienteVip(dni, nombre, licencia, anio, codigo))
                else:
                    print("Opción de tipo inválida.")
            except ValueError:
                print("Error: El año debe ser un número entero.")

        elif opcion == "3":
            print("\n--- GENERAR RESERVA ---")
            dni_cliente = input("DNI del cliente: ")
            placa_auto = input("Placa del vehículo: ").upper()
            
            try:
                dias = int(input("Días de alquiler: "))
                cliente = sistema.buscar_cliente(dni_cliente)
                auto = sistema.buscar_vehiculo(placa_auto)
                
                if not auto:
                    print(f"Error: No existe el vehículo con placa {placa_auto}.")
                elif sistema.validar_licencia(dni_cliente, "A-I"):
                    id_res = f"RES-{contador_reservas}"
                    sistema.generar_reserva(id_res, cliente, auto, dias)
                    auto.set_disponibilidad(False)
                    contador_reservas += 1
            except ValueError:
                print("Error: Días debe ser un entero.")
            except (ClienteNoEncontradoError, VehiculoOcupadoError) as e:
                print(e)

        elif opcion == "4":
            print("\n--- PROCESAR DEVOLUCIÓN ---")
            id_res = input("ID de Reserva (ej. RES-1): ").upper()
            if id_res in sistema._reservas:
                sistema._reservas[id_res].get_vehiculo().set_disponibilidad(True)
            sistema.procesar_devolucion(id_res)

        elif opcion == "5":
            sistema.mostrar_clientes()

        elif opcion == "6":
            dni_busqueda = input("Ingrese el DNI del cliente a consultar: ")
            try:
                c = sistema.buscar_cliente(dni_busqueda)
                print(f"\nHistorial de {c.get_nombre()}: {c.get_historial() if c.get_historial() else 'Sin alquileres registrados.'}")
            except ClienteNoEncontradoError as e:
                print(e)

        elif opcion == "7":
            placa_busqueda = input("Ingrese placa a consultar: ").upper()
            v = sistema.buscar_vehiculo(placa_busqueda)
            print(f"\nResultado: {v if v else 'Vehículo no encontrado en el sistema.'}")

        elif opcion == "8":
            sistema.mostrar_disponibles()
            sistema.calcular_ingresos_totales()

        elif opcion == "9":
            print("\n¡Gracias por utilizar el sistema! Cerrando sesión...")
            break

        else:
            print("\nOpción inválida. Seleccione un número entre 1 y 9.")
