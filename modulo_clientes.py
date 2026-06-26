"""
En este modulo
"""

class ClienteNoEncontradoError(Exception):
    pass

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

class SistemaAlquiler:
    def __init__(self):
        self._clientes = {}

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

"""
# --- ZONA DE PRUEBAS DEL INTEGRANTE 2 ---
if __name__ == "__main__":
    # Instanciamos el sistema de prueba
    mi_sistema = SistemaAlquiler()

    # Creamos un par de objetos Cliente
    cliente1 = Cliente("77778888", "Carlos Mendoza", "A-I", 2021)
    cliente2 = Cliente("11122233", "Ana Peralta", "A-III", 2018)

    # 1. Probamos el registro
    mi_sistema.registrar_cliente(cliente1)
    mi_sistema.registrar_cliente(cliente2)
    mi_sistema.mostrar_clientes()

    # 2. Probamos el manejo de excepciones (Forzamos la búsqueda de un DNI inexistente)
    try:
        mi_sistema.buscar_cliente("99999999")
    except ClienteNoEncontradoError as e:
        print(f"Excepción capturada con éxito: {e}\n")

    # 3. Probamos la estructura de control de licencias
    # Carlos tiene A-I e intenta pedir un vehículo que requiere A-II (Debe denegar)
    mi_sistema.validar_licencia("77778888", "A-II")
    
    # Ana tiene A-III e intenta pedir un vehículo que requiere A-I (Debe aprobar por ser profesional)
    mi_sistema.validar_licencia("11122233", "A-I")

    # 4. Probamos la mutabilidad de la lista (Simulación de historial)
    cliente_test = mi_sistema.buscar_cliente("77778888")
    cliente_test.agregar_al_historial("ALQ-1001")
    print("\n--- Historial Actualizado ---")
    print(cliente_test)  # El contador de alquileres debe subir a 1
"""