"""
En este modulo se crea el inventario de la flota. Se programa la clase "Vehiculo"
implementando encapsulacuión (atributos privados y métodos "get"/"set" para acceder a ellos.)
También se desarrolla la lógica de negocio, usando los métodos registrar_vehiculo(), 
buscar_vehiculo() y mostrar_disponibles(). Por último, se hace uso de diccionarios para
almacenar los vehículos con sus respectivas placas, además de crear y lanzar un bloque try-except 
si se intenta registrar un vehículo con una placa ya existente (VehiculoDuplicadoError).
"""

class VehiculoDuplicadoError(Exception):
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
    
class SistemaAlquiler:
    def __init__(self):
        self._flota = {}

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

"""
# --- ZONA DE PRUEBAS ---
if __name__ == "__main__":
    # Instanciamos el sistema
    mi_sistema = SistemaAlquiler()

    # Creamos un par de vehículos
    auto1 = Vehiculo("ABC-123", "Toyota", "Corolla", 120.0)
    auto2 = Vehiculo("XYZ-987", "Kia", "Rio", 95.0)

    # 1. Probamos el registro exitoso
    mi_sistema.registrar_vehiculo(auto1)
    mi_sistema.registrar_vehiculo(auto2)

    # 2. Probamos la excepción (forzamos un error con try-except)
    auto_duplicado = Vehiculo("ABC-123", "Nissan", "Sentra", 110.0)
    try:
        mi_sistema.registrar_vehiculo(auto_duplicado)
    except VehiculoDuplicadoError as e:
        print(f"Excepción capturada con éxito: {e}")

    # 3. Probamos mostrar los disponibles
    mi_sistema.mostrar_disponibles()

    # 4. Simulamos que el Integrante 3 alquila un auto (cambiamos estado a False)
    auto_buscado = mi_sistema.buscar_vehiculo("ABC-123")
    if auto_buscado:
        auto_buscado.set_disponibilidad(False)
        print(f"El auto {auto_buscado.get_placa()} acaba de ser alquilado.\n")

    # 5. Volvemos a mostrar disponibles (ABC-123 ya no debería salir)
    mi_sistema.mostrar_disponibles() 
"""