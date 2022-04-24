import csv

def cargar_csv(nombre_archivo):
    with open(nombre_archivo, encoding='UTF8') as archivo:
        lector = csv.reader(archivo, delimiter=",")        
        next(lector, None)        
        for fila in lector:
            columna_0 = str(fila[0])
    print("¡Archivo \"" + nombre_archivo + "\" cargado exitosamente!")  