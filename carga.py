import csv

def normalizar_csv(nombre_archivo, cantidad):
    diccionario = {}
    with open(nombre_archivo, encoding='UTF8') as archivo:
        lector = csv.reader(archivo, delimiter=",")        
        next(lector, None)
        contador = 1       
        for fila in lector:
            diccionario[fila[11]] = fila            
            contador += 1
            if contador == cantidad:
                break
    print("¡Archivo \"" + nombre_archivo + "\" cargado exitosamente!")
    return diccionario

def encontrar_generos(diccionario,posicion,separador):
    resultado = []
    for k,v in diccionario.items():
        generos = v[posicion].split(separador)
        for genero in generos:
            if not genero in resultado:
                resultado.append(genero)
    return resultado
