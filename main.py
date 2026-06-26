class VehiculoDuplicadoError(Exception):
    pass        

class ClienteNoEncontradoError(Exception):
    pass

class VehiculoOcupadoError(Exception):
    pass

class Vehiculo:
    def __init__(self, placa, marca, modelo, precio_diario):
        self._placa = placa
        self._marca = marca
        self._modelo = modelo
        self._precio_diario = precio_diario
        self._disponible = True

    def get_placa(self):
        return self._placa
    
    def get_marca(self):
        return self._marca
    
    def get_modelo(self):
        return self._modelo
    
    def get_precio_diario(self):
        return self._precio_diario
    
    def is_disponible(self):
        return self._disponible
    
    def set_disponibilidad(self, estado: bool):
        self._disponible = estado

    def __str__(self):
        estado = "Disponible" if self._disponible else "Alquilado"
        return f"[{self._placa}] {self._marca} {self._modelo} - S/ {self._precio_diario} por día ({estado})"

class Cliente:
    def __init__(self, dni, nombre, categoria_licencia, anio_emision):
        self._dni = dni
        self._nombre = nombre
        self._licencia = (categoria_licencia, anio_emision)
        self._historial_reservas = []

    # Métodos públicos (Getters)
    def get_dni(self):
        return self._dni

    def get_nombre(self):
        return self._nombre

    def get_licencia(self):
        return self._licencia

    def get_historial(self):
        return self._historial_reservas

    def agregar_al_historial(self, id_reserva):
        self._historial_reservas.append(id_reserva)

    def __str__(self):
        categoria, anio = self._licencia
        cantidad_reservas = len(self._historial_reservas)
        return f"[{self._dni}] Cliente: {self._nombre} | Licencia: {categoria} ({anio}) | Alquileres previos: {cantidad_reservas}"

class Reserva:
    def __init__(self, id_reserva, cliente, vehiculo, dias):
        self._id_reserva = id_reserva
        self._cliente = cliente
        self._vehiculo = vehiculo
        self._dias = dias
        self._costo_total = self._vehiculo.get_precio_diario() * self._dias
        self._activa = True

    def get_id(self):
        return self._id_reserva

    def get_vehiculo(self):
        return self._vehiculo

    def get_cliente(self):
        return self._cliente
        
    def get_costo_total(self):
        return self._costo_total

    def is_activa(self):
        return self._activa

    def finalizar_reserva(self):
        self._activa = False

    def __str__(self):
        estado = "EN CURSO" if self._activa else "FINALIZADA"
        placa = self._vehiculo.get_placa()
        nombre_cliente = self._cliente.get_nombre()
        return f"[{self._id_reserva}] Auto {placa} -> {nombre_cliente} por {self._dias} días | Total: S/{self._costo_total} ({estado})"
    
class SistemaAlquiler:
    def __init__(self):
        self._flota = {}
        self._clientes = {}
        self._reservas = {}
        self._vehiculos_en_ruta = set()

    #Metodos del modulo flota

    def registrar_vehiculo(self, vehiculo):
        placa = vehiculo.get_placa()

        if placa in self._flota:
            raise VehiculoDuplicadoError(f"Error: El vehículo con placa {placa} ya está registrado.")
        else:
            self._flota[placa] = vehiculo
            print(f"Éxito: Vehículo {placa} registrado correctamente.")

    def buscar_vehiculo(self, placa):
        return self._flota.get(placa)
    
    def mostrar_disponibles(self):
        print("\n --- Vehículos Disponibles ---")
        hay_disponibles = False

        for vehiculo in self._flota.values():
            if vehiculo.is_disponible():
                print(vehiculo)
                hay_disponibles = True
        
        if not hay_disponibles:
            print("No hay vehículos disponibles en este momento.")
        print("-----------------------------\n")

    #Metodos del modulo clientes

    def registrar_cliente(self, cliente):
        dni = cliente.get_dni()
        
        if dni in self._clientes:
            print(f"Atención: El cliente con DNI {dni} ya está registrado en el sistema.")
        else:
            self._clientes[dni] = cliente
            print(f"Éxito: Cliente {cliente.get_nombre()} registrado correctamente.")

    def buscar_cliente(self, dni):
        if dni not in self._clientes:
            raise ClienteNoEncontradoError(f"Error: No se encontró ningún cliente con el DNI '{dni}'.")
        
        return self._clientes[dni]

    def validar_licencia(self, dni, categoria_requerida):
        cliente = self.buscar_cliente(dni)
        
        categoria_cliente, anio_emision = cliente.get_licencia()
        
        if categoria_cliente == categoria_requerida:
            print(f"Validación exitosa: {cliente.get_nombre()} tiene la licencia exacta ({categoria_requerida}).")
            return True
        elif categoria_cliente == "A-III":
            print(f"Validación exitosa: {cliente.get_nombre()} tiene licencia profesional (A-III), apto para todo.")
            return True
        else:
            print(f"Denegado: {cliente.get_nombre()} tiene {categoria_cliente}, necesita {categoria_requerida}.")
            return False
            
    def mostrar_clientes(self):
        print("\n--- Directorio de Clientes ---")
        if not self._clientes:
            print("No hay clientes registrados.")
        else:
            for cliente in self._clientes.values():
                print(cliente)
        print("------------------------------\n")
    
    #Metodos del modulo operaciones

    def generar_reserva(self, id_reserva, cliente, vehiculo, dias):
        placa = vehiculo.get_placa()
        
        if placa in self._vehiculos_en_ruta:
            raise VehiculoOcupadoError(f"Error: El vehículo {placa} ya se encuentra alquilado.")

        nueva_reserva = Reserva(id_reserva, cliente, vehiculo, dias)
        self._reservas[id_reserva] = nueva_reserva
        self._vehiculos_en_ruta.add(placa)
        cliente.agregar_al_historial(id_reserva)
        print(f"Éxito: Reserva {id_reserva} generada por S/{nueva_reserva.get_costo_total()}.")

    def procesar_devolucion(self, id_reserva):
        if id_reserva not in self._reservas:
            print(f"Error: La reserva {id_reserva} no existe.")
            return
            
        reserva = self._reservas[id_reserva]
        
        if not reserva.is_activa():
            print(f"Aviso: La reserva {id_reserva} ya había sido finalizada.")
            return
            
        # Finalizamos la reserva
        reserva.finalizar_reserva()
        
        # Sacamos la placa del SET de ocupados
        placa = reserva.get_vehiculo().get_placa()
        self._vehiculos_en_ruta.discard(placa)
        
        print(f"Éxito: Vehículo {placa} devuelto. La reserva {id_reserva} ha finalizado.")

    def calcular_ingresos_totales(self):
        total = 0
        for reserva in self._reservas.values():
            total += reserva.get_costo_total()
        print(f"\n--- Ingresos Totales del Sistema: S/{total} ---")

# --- INICIO DEL PROGRAMA PRINCIPAL ---
if __name__ == "__main__":
    sistema = SistemaAlquiler()
    
    #DATOS QUEMADOS
    sistema.registrar_vehiculo(Vehiculo("ABC-123", "Toyota", "Corolla", 120.0))
    sistema.registrar_vehiculo(Vehiculo("XYZ-987", "Kia", "Rio", 95.0))
    sistema.registrar_cliente(Cliente("77778888", "Carlos Rojas", "A-I", 2020))
    sistema.registrar_cliente(Cliente("11122233", "Ana Peralta", "A-III", 2018))
    
    contador_reservas = 1

    #BUCLE PRINCIPAL DEL MENÚ
    while True:
        print("\n" + "="*45)
        print("   SISTEMA DE ALQUILER DE VEHÍCULOS")
        print("="*45)
        print("1. Registrar nuevo Vehículo")
        print("2. Registrar nuevo Cliente")
        print("3. Generar Reserva (Alquilar)")
        print("4. Procesar Devolución")
        print("5. Ver Directorio de Clientes")          
        print("6. Ver Historial de un Cliente")         
        print("7. Buscar un Vehículo Específico")      
        print("8. Ver Flota Disponible e Ingresos")     
        print("9. Salir")
        print("="*45)
        
        opcion = input("Seleccione una opción (1-9): ")

        if opcion == "1":
            print("\n--- REGISTRO DE VEHÍCULO ---")
            placa = input("Ingrese la placa: ").upper()
            marca = input("Ingrese la marca: ").capitalize()
            modelo = input("Ingrese el modelo: ").capitalize()
            try:
                precio = float(input("Ingrese el precio diario (S/): "))
                sistema.registrar_vehiculo(Vehiculo(placa, marca, modelo, precio))
            except ValueError:
                print("Error: El precio debe ser numérico.")
            except VehiculoDuplicadoError as e:
                print(e)

        elif opcion == "2":
            print("\n--- REGISTRO DE CLIENTE ---")
            dni = input("Ingrese el DNI (8 dígitos): ")
            nombre = input("Ingrese el nombre completo: ").title()
            licencia = input("Ingrese la categoría de licencia (ej. A-I): ").upper()
            try:
                anio = int(input("Ingrese el año de emisión: "))
                sistema.registrar_cliente(Cliente(dni, nombre, licencia, anio))
            except ValueError:
                print("Error: El año debe ser numérico.")

        elif opcion == "3":
            print("\n--- GENERAR RESERVA ---")
            dni_cliente = input("Ingrese el DNI del cliente: ")
            placa_auto = input("Ingrese la placa del vehículo: ").upper()
            
            try:
                dias = int(input("¿Por cuántos días desea alquilar?: "))
                cliente_encontrado = sistema.buscar_cliente(dni_cliente)
                vehiculo_encontrado = sistema.buscar_vehiculo(placa_auto)
                
                if vehiculo_encontrado is None:
                    print(f"Error: El vehículo con placa {placa_auto} no existe.")
                else:
                    if sistema.validar_licencia(dni_cliente, "A-I"):
                        id_generado = f"RES-{contador_reservas}"
                        sistema.generar_reserva(id_generado, cliente_encontrado, vehiculo_encontrado, dias)
                        
                        vehiculo_encontrado.set_disponibilidad(False)
                        
                        contador_reservas += 1
            except ValueError:
                print("Error: La cantidad de días debe ser un número entero.")
            except (ClienteNoEncontradoError, VehiculoOcupadoError) as e:
                print(e)

        elif opcion == "4":
            print("\n--- PROCESAR DEVOLUCIÓN ---")
            id_reserva = input("Ingrese el ID de la reserva (ej. RES-1): ").upper()
            
            if id_reserva in sistema._reservas:
                auto_devuelto = sistema._reservas[id_reserva].get_vehiculo()
                auto_devuelto.set_disponibilidad(True)
                
            sistema.procesar_devolucion(id_reserva)

        elif opcion == "5":
            sistema.mostrar_clientes()

        elif opcion == "6":
            print("\n--- HISTORIAL DE CLIENTE ---")
            dni_buscar = input("Ingrese el DNI a consultar: ")
            try:
                cliente = sistema.buscar_cliente(dni_buscar)
                print(f"Cliente: {cliente.get_nombre()}") 
                historial = cliente.get_historial()
                
                if len(historial) == 0:
                    print("Este cliente aún no ha realizado alquileres.")
                else:
                    print(f"IDs de reservas realizadas: {historial}")
            except ClienteNoEncontradoError as e:
                print(e)

        elif opcion == "7":
            print("\n--- BUSCADOR DE VEHÍCULOS ---")
            placa_buscar = input("Ingrese la placa a buscar: ").upper()
            vehiculo = sistema.buscar_vehiculo(placa_buscar)
            if vehiculo:
                print("Vehículo encontrado:")
                print(vehiculo)
            else:
                print(f"No se encontró ningún vehículo con la placa {placa_buscar}.")

        elif opcion == "8":
            sistema.mostrar_disponibles()
            sistema.calcular_ingresos_totales()

        elif opcion == "9":
            print("\nCerrando el Sistema de Alquiler. ¡Hasta pronto!")
            break

        else:
            print("\nError: Opción no válida. Intente de nuevo.")
