import hashlib

class TablaSimbolos:
    def __init__(self):
        self.variables_validas = {"void", "int", "float", "string","if", "return"}
        self.tabla = {}

    def es_valido(self, tipo_dato):
        return tipo_dato in self.variables_validas

    def insertar_variable(self, nombre_variable, tipo_variable, alcance, linea):
        if self.es_valido(tipo_variable):
            #toma el contenido y lo codifica en bytes
            variable_hash = hashlib.md5(nombre_variable.encode()).hexdigest()
            self.tabla[variable_hash] = {"nombre": nombre_variable, "tipo": tipo_variable, "alcance": alcance}
        else:
            return f"Error – Linea {linea}: '{nombre_variable}' no está declarado"

    def insertar_funcion(self, nombre_function, tipo_r , parameters, alcance_function, linea):
        if self.es_valido(tipo_r):
            function_hash = hashlib.md5(nombre_function.encode()).hexdigest()
            self.tabla[function_hash] = {"nombre": nombre_function, "tipo": tipo_r, "parameters": parameters, "alcance": alcance_function}
        else:
            return f"Error – Linea {linea}: el valor de retorno no coincide con '{nombre_function}'"

    def buscar(self, nombre, alcance):
        for s_hash, s_info in self.tabla.items():
            # Verificar si el nombre es una palabra clave 'if' o 'while'
            if nombre.lower() in {"if", "while"}:
                return None
            if s_info["nombre"] == nombre and s_info["alcance"] == alcance:
                return s_hash
        # Si no se encuentra ninguna coincidencia después de recorrer todo el bucle
        return None

    def borrar(self, nombre):
        if nombre in self.tabla:
            del self.tabla[nombre]
        else:
            return f"'{nombre}' no se encontro el simbolo."
