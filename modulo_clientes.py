"""
En este modulo
"""

class ClienteNoEncontradoError(Exception):
    pass

class Cliente:
    def __init__(self, dni, nombre, categoria_licencia, anio_emision):
        self._dni = dni
        self._nombre = nombre
        self._licensia = (categoria_licencia, anio_emision)
        self._historia_reservas = []

    def get_dni(self):
        return self._dni
    
    def get_nombre(self):
        return self._nombre
    
    def get_licensia(self):
        return self._licencia
    
    def get_historial(self):
        return self._historia_reservas
    
    def agreagar_al_historia(self, id_reservas):
        self._historia_reservas.append(id_reservas)
    def __str__(self):
        cat, anio = self._licencia
        return f"[{self._dni}] {self._nombre} | licencia: {cat}({anio}) | Alquileres realizados: {len(self._historia_reservas)}"

class SistemaAlquiler:
    def __init__(self):
        self._clientes = {}

def registrar_cliente(self, cliente):
    dni = cliente.get_dni()
    if dni in self._clientes:
        print(f"El cliente con el DNI {dni} ya se encuentra registrado.")
    else:
        self.clientes[dni] = cliente
        print(f"Èxito: Cliente {cliente.get_nombre()} registrado correctamente.")

def bucar_cliente(self, dni):
    if dni not in self._clientes:
        raise ClienteNoEncontradoError(f"Error: No se encontro ningùn cliente con el DNI de '{dni}'.")
    return self.clientes[dni]

def validar_licencia(self, dni, categoria_requerida):
    cliente = self.buscar_cliente(dni)
    categoria_cliente, anio = cliente.get_licencia()

    if categoria_cliente == categoria_requerida:
        print(f"Validacion exitosa{cliente.get_nombre} cumple con la categoria {categoria_requerida}.")
        return True
    
    elif categoria_cliente == "A-III":
        print(f"Validacion profecional: Licencia A-III autoriza a {cliente.get_nombre()} para cualquier vehiculo.")
        return True
    else:
        print(f"Validacion denegada {cliente.get_nombre} tiene {categoria_cliente} pero requiere {categoria_requerida}.")

def mostrar_clientes(self):
    print("\n---Directorio de clientes---")
    if not self._clientes:
        print("No hay clientes en el sistema.")
    else:
        for cliente in self._clientes.value():
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