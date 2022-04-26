import tkinter, carga

ventana = tkinter.Tk()
ventana.title("Inicio Sesión")
ventana.geometry("200x300")
ventana.resizable(width=False, height=False)
imagen = tkinter.PhotoImage(file="inicio_sesion.png")
fondo = tkinter.Label(ventana, image=imagen).place(x=0,y=0,relwidth=1,relheight=1)

def csv():
    carga.normalizar_csv("movie_metadata.csv",5000)

boton = tkinter.Button(ventana,text="Cargar archivo CSV",cursor="hand2",bg="#002D66",width=14,relief="flat",font=("Comic Sans MS",8,"bold"),command=csv)
boton.place(x=46,y=233)

ventana.mainloop()

#import tkinter, carga
#
#def csv():
#    carga.normalizar_csv("movie_metadata.csv",5000)
#
#ventana_principal = tkinter.Tk()
#ventana_principal.geometry("300x200")
#
#lbl_titulo = tkinter.Label(ventana_principal, text="IMDB 5000", bg = "orange", pady=15)
#lbl_titulo.pack(fill = tkinter.X)
#
#btn_cargar_CSV= tkinter.Button(ventana_principal, text="Cargar CSV", command=csv)
#btn_cargar_CSV.pack()
#
#if __name__ == "__main__":
#    ventana_principal.mainloop()