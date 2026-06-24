class VehiculoOcupadoError(Exception):
    pass

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
        # El Integrante 1 tiene self._flota = {}
        # El Integrante 2 tiene self._clientes = {}
        
        # Tú administrarás el diccionario de reservas y el SET de autos ocupados
        self._reservas = {}
        self._vehiculos_en_ruta = set()  # SET: Colección para controlar disponibilidad (Requisito técnico)

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

# --- ZONA DE PRUEBAS DEL INTEGRANTE 3 ---
if __name__ == "__main__":
    
    # 1. Creamos "Clases Falsas" (Mocks) solo para probar este archivo aisladamente
    class MockVehiculo:
        def __init__(self, placa, precio):
            self.placa, self.precio = placa, precio
        def get_placa(self): return self.placa
        def get_precio_diario(self): return self.precio

    class MockCliente:
        def __init__(self, nombre):
            self.nombre = nombre
        def get_nombre(self): return self.nombre
        def agregar_al_historial(self, id_res): pass # Simulamos que guarda el ID

    # 2. Instanciamos el sistema y nuestros objetos de prueba
    mi_sistema = SistemaAlquiler()
    auto_test = MockVehiculo("XYZ-999", 100.0)
    cliente_test = MockCliente("Luis Perez")

    # 3. Probamos generar una reserva
    mi_sistema.generar_reserva("RES-001", cliente_test, auto_test, 5) # 5 días a S/100 = S/500

    # 4. Probamos la Excepción: Intentamos alquilar el MISMO auto que ya está en el SET
    try:
        mi_sistema.generar_reserva("RES-002", cliente_test, auto_test, 2)
    except VehiculoOcupadoError as e:
        print(f"Excepción capturada con éxito: {e}")

    # 5. Probamos procesar la devolución (Saca el auto del SET)
    mi_sistema.procesar_devolucion("RES-001")

    # 6. Al estar devuelto, ahora SÍ debería dejarnos alquilarlo de nuevo
    mi_sistema.generar_reserva("RES-003", cliente_test, auto_test, 3)

    # 7. Verificamos ingresos (S/500 de la primera + S/300 de la segunda)
    mi_sistema.calcular_ingresos_totales()