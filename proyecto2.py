from TablaSimbolos import TablaSimbolos
from Analizador import AnalizadorSemantico

if __name__ == "__main__":
    
    tabla = TablaSimbolos()
    analizador = AnalizadorSemantico(tabla)

    # Lee el archivo y lo analiza, variar entre txt correcto e incorrecto
    file_path = r"C:\Users\alfon\OneDrive\Escritorio\Proyecto2\correcto.txt"
    with open(file_path, "r", encoding="utf-8") as file:
        code_lines = file.readlines()

    analizador.analizador(code_lines)

    # Mostrar errores o indicar que el código es correcto
    if analizador.errors:
        for error in sorted(analizador.errors):
            print(error)
    else:
        print("El codigo fuente es correcto.")