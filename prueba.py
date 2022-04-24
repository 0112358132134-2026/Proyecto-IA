import tkinter
from turtle import position

ventana = tkinter.Tk()
ventana.geometry("300x200")

lbl_titulo = tkinter.Label(ventana, text="IMDB 5000", bg = "orange", pady=15)
lbl_titulo.pack(fill = tkinter.X)

lbl_usuario = tkinter.Label(ventana, text="Ingrese su usuario: ")
lbl_usuario.pack()

txt_usuario = tkinter.Entry(ventana, justify="center")
txt_usuario.pack()

lbl_contraseña = tkinter.Label(ventana, text="Ingrese su contraseña: ")
lbl_contraseña.pack()

txt_contraseña = tkinter.Entry(ventana, justify="center",show="*")
txt_contraseña.pack()


def ingresar():
    usuario = txt_usuario.get()
    contraseña = txt_contraseña.get()
    print(usuario + " " + contraseña)

btn_ingresar = tkinter.Button(ventana, text="Ingresar", command=ingresar)
btn_ingresar.pack()

ventana.mainloop()