import tkinter, carga

def csv():
    carga.normalizar_csv("movie_metadata.csv",5000)

ventana_principal = tkinter.Tk()
ventana_principal.geometry("300x200")

lbl_titulo = tkinter.Label(ventana_principal, text="IMDB 5000", bg = "orange", pady=15)
lbl_titulo.pack(fill = tkinter.X)

btn_cargar_CSV= tkinter.Button(ventana_principal, text="Cargar CSV", command=csv)
btn_cargar_CSV.pack()

if __name__ == "__main__":
    ventana_principal.mainloop()