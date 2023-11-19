class AnalizadorSemantico:
    def __init__(self, tabla_simbolos):
        self.tabla_simbolos = tabla_simbolos
        self.alcance_global = "global"
        self.errors = set()
        self.variables_pendientes = []

    def analizador(self, lineas):
        esta_en_funcion = False
        variables_golobales = set() 
        
        for numero_linea, linea in enumerate(lineas, start = 1):
            linea = linea.strip()

            if not linea:
                continue
            
            elif "void" in linea:
                # Verificar que este fuera de una funcion
                if not esta_en_funcion:
                    esta_en_funcion = True
                    partes = linea.split()
                    nombre_funcion = partes[1].split('(')[0]
                    tipo_retorno = "void"
                    parametros = []
                    if "(" in linea:
                        parte_param = linea.split('(')[1].split(')')[0]
                        parametros = [param.strip() for param in parte_param.split(',')]
                        # Insertar los parametros como variables globales en la tabla de simbolos
                        for param in parametros:
                            tipo_param, nombre_param = param.split()
                            error = self.tabla_simbolos.insertar_variable(nombre_param, tipo_param, "global", numero_linea)
                            if error:
                                self.errors.add(error)

                    error = self.tabla_simbolos.insertar_funcion(nombre_funcion, tipo_retorno, parametros, self.alcance_global, numero_linea)
                    if error:
                        self.errors.add(error)
                    # Cambio de alcance al entrar en la funcion
                    self.alcance_global = nombre_funcion

                    # Registrar las variables pendientes dentro de la funcion
                    for nombre_variable, tipo_variable, numero_linea in self.variables_pendientes:
                        error = self.tabla_simbolos.insertar_variable(nombre_variable, tipo_variable, self.alcance_global, numero_linea)
                        if error:
                            self.errors.add(error)
                            self.variables_pendientes = []


            elif "int" in linea or "float" in linea or "string" in linea:
                # Verificar que este fuera o dentro de una funcion
                partes = linea.split()
                tipo_variable = partes[0]
                nombre_variable = partes[1].rstrip(';')
                if not esta_en_funcion:
                    error = self.tabla_simbolos.insertar_variable(nombre_variable, tipo_variable, self.alcance_global, numero_linea)
                    if error:
                        self.errors.add(error)
                else:
                    self.variables_pendientes.append((nombre_variable, tipo_variable, numero_linea))


            elif "void" in linea:
                # Verificar que este fuera de una funcion
                if not esta_en_funcion:
                    esta_en_funcion = True
                    partes = linea.split()
                    nombre_funcion = partes[1].split('(')[0]
                    tipo_retorno = "void"
                    parametros = []
                    if "(" in linea:
                        parte_param = linea.split('(')[1].split(')')[0]
                        parametros = [param.strip() for param in parte_param.split(',')]
                        # Inserta los parametros como variables globales en la tabla de simbolos
                        for param in parametros:
                            tipo_param, nombre_param = param.split()
                            error = self.tabla_simbolos.insertar_variable(nombre_param, tipo_param, "global", numero_linea)
                            if error:
                                self.errors.add(error)

                    error = self.tabla_simbolos.insertar_funcion(nombre_funcion, tipo_retorno, parametros, self.alcance_global, numero_linea)
                    if error:
                        self.errors.add(error)
                    # Cambio de alcance al entrar en una funcion
                    self.alcance_global = nombre_funcion

                    # Registrar las variables pendientes dentro de la funcion
                    for nombre_variable, tipo_variable, numero_linea in self.variables_pendientes:
                        error = self.tabla_simbolos.insertar_variable(nombre_variable, tipo_variable, self.alcance_global, numero_linea)
                        if error:
                            self.errors.add(error)
                            self.variables_pendientes = []


            elif "}" in linea:
                # Verificar que esté dentro de una funcion 
                if esta_en_funcion:
                    esta_en_funcion = False
                    # Cambio de alcance al salir de una funcion
                    self.alcance_global = "global"
        

            elif esta_en_funcion and not any(reservada in linea.split('(')[0] for reservada in {"if", "while", "void"}):
                words = linea.split()

                if "(" in linea and ")" in linea:  # Verifica si hay parentesis
                    nombre_funcion = linea.split("(")[0].split()[-1]  # Obtiene el nombre de la funcion

                    # Obtener los parametros de la funcion
                    fun_paramentros = []
                    for func_hash, informacion_func in self.tabla_simbolos.table.items():
                        if informacion_func.get("nombre") == nombre_funcion and informacion_func.get("parametros"):
                            fun_paramentros = informacion_func.get("parametros")
                            break

                      # Analizar las variables en la linea actual
                    for variable in words:
                        variable = variable.strip('();')

                        # Verifica la variable si esta en los parametros o es una palabra reservada
                        if variable in fun_paramentros or variable in {"if", "while", "void"}:
                            continue

                        if variable.isidentifier() and not self.tabla_simbolos.buscar(variable, self.alcance_global):
                            if variable in variables_golobales:
                                continue  # Si la variable es global, sigue con la siguiente variable
                            else:
                                self.errors.add(f"Error – Linea {numero_linea}: '{variable}' no esta declarado")
                                
            elif "return" in linea:
                # Verifica que este dentro de una funcion y maneja el retorno
                if esta_en_funcion:
                    partes = linea.split()
                    if len(partes) > 1:
                        tipo_retorno = partes[1].rstrip(';')
                        alcance_funcion = self.alcance_global
                        # Buscar la funcion actual en la tabla
                        funcion_hash = self.tabla_simbolos.buscar(alcance_funcion, self.alcance_global)
                        if funcion_hash is not None:
                            tipo_declarado = self.tabla_simbolos.table[funcion_hash]["tipo"]
                            if tipo_retorno != tipo_declarado:
                                self.errors.add(f"Error – Linea {numero_linea}: valor de retorno no coincide con la declaracin de '{alcance_funcion}'")
                else:
                    self.errors.add(f"Error – Linea {numero_linea}: Sentencia 'return' fuera del alcance de la funcion")


        for numero_linea, line in enumerate(lineas, start=1):
            palabras = [palabra.strip('();') for palabra in line.split()]
            for palabra in palabras:
                if palabra in self.tabla_simbolos.variables_validas:
                    # Es un tipo de dato, no hacer nada
                    pass
                elif palabra.isidentifier() and not self.tabla_simbolos.buscar(palabra, self.alcance_global):
                    self.errors.add(f"Error – Linea {numero_linea}: '{palabra}' no esta declarado")

