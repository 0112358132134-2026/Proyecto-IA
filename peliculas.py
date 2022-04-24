from sympy import resultant


def cargar_peliculas(csv):
    resultado = ""
    for fila in csv:
        if fila == "":
            resultado = "OK"
    return resultado