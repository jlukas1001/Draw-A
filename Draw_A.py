from tkinter import *
from tkinter import messagebox
import tkinter.font as tkf
import time
import Punto

class Aplicacion:
    def __init__(self, ventanaPrincipal):

        self.ventana = ventanaPrincipal
        self.ventana.title("Draw_A")
        self.ventana.geometry("1366x768")
        self.ventana.resizable(False,False)

        self.boton = "seleccionar"
        self.color = "black"
        self.figura = []

        self.dictFiguras = {}
        self.contadorFiguras = 0

        self.primeraX = 0
        self.primeraY = 0

        self.ultimaX = 0
        self.ultimaY = 0

        # ------------------------------------------- LIENZO DE PINTURA ---------------------------------------------------------------
        self.frameLienzo = Frame(self.ventana,width=800,bg="white",height=600,borderwidth=3, relief="solid")
        self.frameLienzo.place(x=20,y=120)

        self.lienzoCanvas = Canvas(self.frameLienzo,width=800, height=600, bg='white')
        self.lienzoCanvas.pack()

        self.lienzoCanvas.bind("<Motion>", self.posMouse)
        self.lienzoCanvas.bind("<Button-1>",self.PosicionIncialFigura)
        self.lienzoCanvas.bind("<B1-Motion>", self.dibujarFigura)
        self.lienzoCanvas.bind("<ButtonRelease-1>", self.crearFigura)
        # -------------------------------------- DECLARACION DE FRAMES ----------------------------------------------------------------
        self.frameBotonera = Frame(self.ventana,width=400,height=80)
        self.frameBotonera.place(x=20,y=30)

        self.frameBotoneraHerra = Frame(self.ventana,width=200,height=80)
        self.frameBotoneraHerra.place(x=492,y=30)

        self.frameConsola = Frame(self.ventana,width=506,height=400)
        self.frameConsola.place(x=840,y=35)

        self.frameCoordenados = Frame(self.ventana,width=506,height=276)
        self.frameCoordenados.place(x=840,y=450)

        # -------------------------------------- DECLARACION DE BOTONES HERRAMIENTAS --------------------------------------------

        self.imagenPunto = PhotoImage(file='punto.png')
        self.botonPunto = Button(self.frameBotonera,image=self.imagenPunto,height=50,width=50,borderwidth=3, relief="groove",command=lambda:self.botonPresionado("punto"))
        self.botonPunto.grid(column=0,row=0,pady=5)


        self.imagenLinea = PhotoImage(file='linea-diagonal.png')
        self.botonLinea = Button(self.frameBotonera,image=self.imagenLinea,height=50,width=50,borderwidth=3, relief="groove",command=lambda:self.botonPresionado("linea"))
        self.botonLinea.grid(column=1,row=0,padx=10,pady=5)

        self.imagenRectangulo = PhotoImage(file='rectangulo.png')
        self.botonRectangulo = Button(self.frameBotonera,image=self.imagenRectangulo,height=50,width=50,borderwidth=3, relief="groove",command=lambda:self.botonPresionado("recta"))
        self.botonRectangulo.grid(column=2,row=0,pady=5)

        self.imagenCirculo = PhotoImage(file='circulo.png')
        self.botonCirculo = Button(self.frameBotonera,image=self.imagenCirculo,height=50,width=50,borderwidth=3, relief="groove",command=lambda:self.botonPresionado("circulo"))
        self.botonCirculo.grid(column=3,row=0,padx=10,pady=5)

        self.imagenTriangulo = PhotoImage(file='triangulo.png')
        self.botonTriangulo = Button(self.frameBotonera,image=self.imagenTriangulo,height=50,width=50,borderwidth=3, relief="groove",command=lambda:self.botonPresionado("trian"))
        self.botonTriangulo.grid(column=4,row=0,pady=5)

        self.imagenTexto = PhotoImage(file='texto.png')
        self.botonTexto = Button(self.frameBotonera,image=self.imagenTexto,height=50,width=50,borderwidth=3, relief="groove",command=lambda:self.botonPresionado("texto"))
        self.botonTexto.grid(column=5,row=0,padx=10,pady=5,columnspan=4)

        self.imagenSeleccionar = PhotoImage(file='seleccionar.png')
        self.botonSeleccionar = Button(self.frameBotoneraHerra,image=self.imagenSeleccionar,height=50,width=50,borderwidth=3, relief="groove",command=lambda:self.botonPresionado("seleccion"))
        self.botonSeleccionar.grid(column=0,row=0,pady=5)

        self.imagenMover = PhotoImage(file='mover.png')
        self.botonMover = Button(self.frameBotoneraHerra,image=self.imagenMover,height=50,width=50,borderwidth=3, relief="groove",command=lambda:self.botonPresionado("mover"))
        self.botonMover.grid(column=1,row=0,padx=10,pady=5)

        self.imagenCopiar = PhotoImage(file='copiar.png')
        self.botonCopiar = Button(self.frameBotoneraHerra,image=self.imagenCopiar,height=50,width=50,borderwidth=3, relief="groove",command=lambda:self.botonPresionado("copiar"))
        self.botonCopiar.grid(column=2,row=0,pady=5)

        self.imagenBorrar = PhotoImage(file='borrador.png')
        self.botonBorrar = Button(self.frameBotoneraHerra,image=self.imagenBorrar,height=50,width=50,borderwidth=3, relief="groove",command=lambda:self.botonPresionado("borrar"))
        self.botonBorrar.grid(column=3,row=0,padx=10,pady=5)

        self.imagenColores = PhotoImage(file='colores.png')
        self.botonColores = Button(self.frameBotoneraHerra,image=self.imagenColores,height=50,width=50,borderwidth=3, relief="groove",command=lambda:self.botonPresionado("colores"))
        self.botonColores.grid(column=4,row=0,pady=5)

        #----------------------------------------------------- ETIQUETAS BOTONES ------------------------------------------

        self.infoBoton= Label(self.ventana,bg="#D3D3D3",fg="blue",borderwidth=1, relief="solid")
        self.infoBoton.place(x=-10,y=0)

        self.botonPunto.bind("<Enter>", lambda event, btn="Punto: coordenadas",X=45,Y=95 : self.adentro(event,btn,X,Y))
        self.botonPunto.bind("<Leave>", self.afuera)

        self.botonLinea.bind("<Enter>", lambda event, btn="Linea: coordenadas, longitud",X=110,Y=95 : self.adentro(event,btn,X,Y))
        self.botonLinea.bind("<Leave>", self.afuera)

        self.botonRectangulo.bind("<Enter>", lambda event, btn="Rectangulo: coordenadas, largo, ancho",X=180,Y=95 : self.adentro(event,btn,X,Y))
        self.botonRectangulo.bind("<Leave>", self.afuera)

        self.botonCirculo.bind("<Enter>", lambda event, btn="Circulo: coordenadas, radio",X=250,Y=95 : self.adentro(event,btn,X,Y))
        self.botonCirculo.bind("<Leave>", self.afuera)
        
        self.botonTriangulo.bind("<Enter>", lambda event, btn="Triangulo: coordenadas, base, altura",X=320,Y=95 : self.adentro(event,btn,X,Y))
        self.botonTriangulo.bind("<Leave>", self.afuera)

        self.botonTexto.bind("<Enter>", lambda event, btn="Texto: coordenadas",X=390,Y=95 : self.adentro(event,btn,X,Y))
        self.botonTexto.bind("<Leave>", self.afuera)

        self.botonSeleccionar.bind("<Enter>", lambda event, btn="Seleccionar",X=517,Y=95 : self.adentro(event,btn,X,Y))
        self.botonSeleccionar.bind("<Leave>", self.afuera)

        self.botonMover.bind("<Enter>", lambda event, btn="Mover",X=582,Y=95 : self.adentro(event,btn,X,Y))
        self.botonMover.bind("<Leave>", self.afuera)

        self.botonCopiar.bind("<Enter>", lambda event, btn="Copiar",X=652,Y=95 : self.adentro(event,btn,X,Y))
        self.botonCopiar.bind("<Leave>", self.afuera)

        self.botonBorrar.bind("<Enter>", lambda event, btn="Borrar",X=722,Y=95 : self.adentro(event,btn,X,Y))
        self.botonBorrar.bind("<Leave>", self.afuera)

        self.botonColores.bind("<Enter>", lambda event, btn="Color",X=792,Y=95 : self.adentro(event,btn,X,Y))
        self.botonColores.bind("<Leave>", self.afuera)
        #----------------------------------------------------- DECLARACION CONSOLA ---------------------------------------------

        self.consola=Text(self.frameConsola,height=25,width=62,state=NORMAL)
        self.consola.grid(column=0,row=0)

        self.scrollVert = Scrollbar(self.frameConsola,command=self.consola.yview)
        self.scrollVert.grid(column=1,row=0,sticky="nsew")

        self.consola.config(yscrollcommand=self.scrollVert.set)

        self.consola.insert(END, "---------- BIENVENIDO A DRAW-A: CONSOLA DE COMANDOS ----------\n")
        self.consola.insert(END,"\n")

        #------------------------------------------------- DECLARACION COORDENADAS ------------------------------------------------

        self.canvasLineas = Canvas(self.frameCoordenados, width=506,height=276,bg=self.ventana.cget('bg'))

        self.canvasLineas.place(x=0,y=0)
        self.canvasLineas.create_line(0,15,105,15,fill="black",width=3)
        self.canvasLineas.create_line(250,15,506,15,fill="black",width=3)
        self.canvasLineas.create_line(0,273,506,273,fill="black",width=3)
        self.canvasLineas.create_line(3,15,3,273,fill="black",width=3)
        self.canvasLineas.create_line(504,15,504,273,fill="black",width=3)


        self.labelTitulo = Label(self.frameCoordenados,text="COORDENADAS OBJETO",font=("Arial Narrow",14))
        self.labelTitulo.place(x=108,y=0)

        self.labelPosMo = Label(self.frameCoordenados,text="POSICION ACTUAL ---",font=("Arial Narrow",13))
        self.labelPosMo.place(x=20,y=240)

        self.textoTamano = Label(self.frameCoordenados,text="",font=("Calibri",12))
        self.textoTamano.place(x=20,y=500)

        # cordenadas del mouse cuando pasa por el lienzo
        self.labelPosMoX = Label(self.frameCoordenados,text="X: ",font=("Arial Narrow",13),fg="red")
        self.labelPosMoX.place(x=180,y=240)

        self.entryPosMoX = Label(self.frameCoordenados,font=("Arial Narrow",13),fg="white",bg="black",justify="center",width=6)
        self.entryPosMoX.place(x=205,y=240)

        self.labelPosMoY = Label(self.frameCoordenados,text="Y: ",font=("Arial Narrow",13),fg="red")
        self.labelPosMoY.place(x=300,y=240)

        self.dibujarCordenadas = Button(self.frameCoordenados,text="ENTER",width=20,borderwidth=3, relief="groove",command=self.btnCordenadas,bg="pale green")
        self.dibujarCordenadas.place(relx=0.5,y=200,anchor=CENTER)

        self.entryPosMoY = Label(self.frameCoordenados,font=("Arial Narrow",13),fg="white",bg="black",justify="center",width=6)
        self.entryPosMoY.place(x=325,y=240)

        #cordenadas del objeto creado o a crear
        self.labelPosX = Label(self.frameCoordenados,text="INICIO X: ",font=("Arial Narrow",13),fg="red")
        self.labelPosX.place(x=80,y=70)

        self.entryPosX = Entry(self.frameCoordenados,font=("Arial Narrow",13),fg="white",bg="black",justify="center",width=6,state="readonly",insertbackground ="white")
        self.entryPosX.place(x=155,y=70)

        self.labelPosY = Label(self.frameCoordenados,text="INICIO Y: ",font=("Arial Narrow",13),fg="red")
        self.labelPosY.place(x=80,y=150)

        self.entryPosY = Entry(self.frameCoordenados,font=("Arial Narrow",13),fg="white",bg="black",justify="center",width=6,state="readonly",insertbackground ="white")
        self.entryPosY.place(x=155,y=150)

        # informacion adicional del objeto
        self.labelLargo = Label(self.frameCoordenados,text="FINAL X: ",font=("Arial Narrow",13),fg="red")
        self.labelLargo.place(x=295,y=70)

        self.entryLargo = Entry(self.frameCoordenados,font=("Arial Narrow",13),fg="white",bg="black",justify="center",width=6,state="readonly",insertbackground ="white")
        self.entryLargo.place(x=370,y=70)

        self.labelAncho = Label(self.frameCoordenados,text="FINAL Y: ",font=("Arial Narrow",13),fg="red")
        self.labelAncho.place(x=295,y=150)

        self.entryAncho = Entry(self.frameCoordenados,font=("Arial Narrow",13),fg="white",bg="black",justify="center",width=6,state="readonly",insertbackground ="white")
        self.entryAncho.place(x=370,y=150)

    def ventanaOpcionTexto(self):
        self.botonTexto.config(state=DISABLED)
        self.ventanaTexto = Toplevel(self.ventana)
        self.ventanaTexto.transient(self.ventana)
        self.ventanaTexto.geometry("400x260+400+130")
        self.ventanaTexto.resizable(False,False)
        self.ventanaTexto.title("Configurar texto")
        self.comandoValidacion = self.ventanaTexto.register(self.numeroEntry)

        self.frame1 = Frame(self.ventanaTexto,width=400,height=100)
        self.frame1.grid(column=0,row=0,columnspan=10)

        self.frame2 = Frame(self.ventanaTexto,width=400,height=300)
        self.frame2.grid(column=0,row=1,columnspan=10)

        self.frame3 = Frame(self.ventanaTexto,width=400,height=100)
        self.frame3.grid(column=0,row=2,columnspan=10)

        self.labelTamano = Label(self.frame1,text="Tamaño: ",font=("Calibri",14))
        self.labelTamano.place(x=70,rely=0.5, anchor=CENTER)

        self.entryTamano = Entry(self.frame1,font=("Calibri",14),width=4,justify="center")
        self.entryTamano.place(x=140,rely=0.5, anchor=CENTER)
        self.entryTamano.insert(END,"12")

        self.labelPx = Label(self.frame1,text="px ",font=("Calibri",14))
        self.labelPx.place(x=190,rely=0.5, anchor=CENTER)

        self.labelColor = Label(self.frame1,text="Color: ",font=("Calibri",14))
        self.labelColor.place(x=300,rely=0.5, anchor=CENTER)

        self.botonColor = Button(self.frame1,bg="black", activebackground="black",width=2,height=1,command=self.ventanaOpcionColorTexto,state=ACTIVE)
        self.botonColor.place(x=340,rely=0.5, anchor=CENTER)
        self.colorTextoUsuario = "black"
        
        self.labelTexto = Label(self.frame2,text="Texto: ",font=("Calibri",14))
        self.labelTexto.grid(column=0,row=0,padx=15)

        self.entryTexto = Text(self.frame2,height=4,width=30,state=NORMAL,font=("Arial",12))
        self.entryTexto.grid(column=1,row=0,columnspan=6)

        self.scrollTexto = Scrollbar(self.frame2,command=self.entryTexto.yview)
        self.scrollTexto.grid(column=8,row=0,sticky="nsew")

        self.entryTexto.config(yscrollcommand=self.scrollTexto.set)

        self.botonAceptar = Button(self.frame3,text="Aceptar",command=self.guardarTexto,font=("Calibri",14),borderwidth=3,relief="groove")
        self.botonAceptar.place(relx=0.5,rely=0.5, anchor=CENTER)

        self.ventanaTexto.protocol("WM_DELETE_WINDOW", self.borrarVentanaTexto)

    def ventanaOpcionColorTexto(self):
        self.botonColor.config(state=DISABLED)
        self.ventanaColor = Toplevel(self.ventanaTexto)
        self.ventanaColor.transient(self.ventanaTexto)
        self.ventanaColor.geometry("148x120+770+60")
        self.ventanaColor.resizable(False,False)
        self.ventanaColor.title("Cambiar color")

        self.botonColorNegro = Button(self.ventanaColor,bg="black", activebackground="black",width=2,height=1, command=lambda:self.colorTextoFun("black"))
        self.botonColorNegro.grid(column=0,row=0,padx=10,pady=10)

        self.botonColorBlanco = Button(self.ventanaColor,bg="white", activebackground="white",width=2,height=1, command=lambda:self.colorTextoFun("white"))
        self.botonColorBlanco.grid(column=1,row=0,pady=10)

        self.botonColorGrisClaro = Button(self.ventanaColor,bg="light gray", activebackground="light gray",width=2,height=1, command=lambda:self.colorTextoFun("light gray"))
        self.botonColorGrisClaro.grid(column=2,row=0,padx=10,pady=10)

        self.botonColorGrisOscuro = Button(self.ventanaColor,bg="dark gray", activebackground="dark gray",width=2,height=1, command=lambda:self.colorTextoFun("dark gray"))
        self.botonColorGrisOscuro.grid(column=3,row=0,pady=10)

        self.botonColorRojo = Button(self.ventanaColor,bg="red", activebackground="red",width=2,height=1, command=lambda:self.colorTextoFun("red"))
        self.botonColorRojo.grid(column=0,row=1,padx=10)

        self.botonColorAmarillo = Button(self.ventanaColor,bg="yellow", activebackground="yellow",width=2,height=1, command=lambda:self.colorTextoFun("yellow"))
        self.botonColorAmarillo.grid(column=1,row=1)

        self.botonColorNaranja = Button(self.ventanaColor,bg="orange", activebackground="orange",width=2,height=1, command=lambda:self.colorTextoFun("orange"))
        self.botonColorNaranja.grid(column=2,row=1,padx=10)

        self.botonColorCafe = Button(self.ventanaColor,bg="brown", activebackground="brown",width=2,height=1, command=lambda:self.colorTextoFun("brown"))
        self.botonColorCafe.grid(column=3,row=1)

        self.botonColorVerde = Button(self.ventanaColor,bg="green", activebackground="green",width=2,height=1, command=lambda:self.colorTextoFun("green"))
        self.botonColorVerde.grid(column=0,row=2,padx=10,pady=10)

        self.botonColorCyan = Button(self.ventanaColor,bg="cyan", activebackground="cyan",width=2,height=1, command=lambda:self.colorTextoFun("cyan"))
        self.botonColorCyan.grid(column=1,row=2,pady=10)

        self.botonColorBlue = Button(self.ventanaColor,bg="blue", activebackground="blue",width=2,height=1, command=lambda:self.colorTextoFun("blue"))
        self.botonColorBlue.grid(column=2,row=2,padx=10,pady=10)

        self.botonColorRosa = Button(self.ventanaColor,bg="pink", activebackground="pink",width=2,height=1, command=lambda:self.colorTextoFun("pink"))
        self.botonColorRosa.grid(column=3,row=2,pady=10)

        self.ventanaColor.protocol("WM_DELETE_WINDOW", self.borrarVentanaColor)

    def ventanaOpcionColorFigura(self):
        self.botonColores.config(state=DISABLED)
        self.ventanaColorF = Toplevel(self.ventana)
        self.ventanaColorF.transient(self.ventana)
        self.ventanaColorF.geometry("148x120+800+60")
        self.ventanaColorF.resizable(False,False)
        self.ventanaColorF.title("Cambiar color")

        self.botonColorNegro = Button(self.ventanaColorF,bg="black", activebackground="black",width=2,height=1, command=lambda:self.colorTextoFig("black"))
        self.botonColorNegro.grid(column=0,row=0,padx=10,pady=10)

        self.botonColorBlanco = Button(self.ventanaColorF,bg="white", activebackground="white",width=2,height=1, command=lambda:self.colorTextoFig("white"))
        self.botonColorBlanco.grid(column=1,row=0,pady=10)

        self.botonColorGrisClaro = Button(self.ventanaColorF,bg="light gray", activebackground="light gray",width=2,height=1, command=lambda:self.colorTextoFig("light gray"))
        self.botonColorGrisClaro.grid(column=2,row=0,padx=10,pady=10)

        self.botonColorGrisOscuro = Button(self.ventanaColorF,bg="dark gray", activebackground="dark gray",width=2,height=1, command=lambda:self.colorTextoFig("dark gray"))
        self.botonColorGrisOscuro.grid(column=3,row=0,pady=10)

        self.botonColorRojo = Button(self.ventanaColorF,bg="red", activebackground="red",width=2,height=1, command=lambda:self.colorTextoFig("red"))
        self.botonColorRojo.grid(column=0,row=1,padx=10)

        self.botonColorAmarillo = Button(self.ventanaColorF,bg="yellow", activebackground="yellow",width=2,height=1, command=lambda:self.colorTextoFig("yellow"))
        self.botonColorAmarillo.grid(column=1,row=1)

        self.botonColorNaranja = Button(self.ventanaColorF,bg="orange", activebackground="orange",width=2,height=1, command=lambda:self.colorTextoFig("orange"))
        self.botonColorNaranja.grid(column=2,row=1,padx=10)

        self.botonColorCafe = Button(self.ventanaColorF,bg="brown", activebackground="brown",width=2,height=1, command=lambda:self.colorTextoFig("brown"))
        self.botonColorCafe.grid(column=3,row=1)

        self.botonColorVerde = Button(self.ventanaColorF,bg="green", activebackground="green",width=2,height=1, command=lambda:self.colorTextoFig("green"))
        self.botonColorVerde.grid(column=0,row=2,padx=10,pady=10)

        self.botonColorCyan = Button(self.ventanaColorF,bg="cyan", activebackground="cyan",width=2,height=1, command=lambda:self.colorTextoFig("cyan"))
        self.botonColorCyan.grid(column=1,row=2,pady=10)

        self.botonColorBlue = Button(self.ventanaColorF,bg="blue", activebackground="blue",width=2,height=1, command=lambda:self.colorTextoFig("blue"))
        self.botonColorBlue.grid(column=2,row=2,padx=10,pady=10)

        self.botonColorRosa = Button(self.ventanaColorF,bg="pink", activebackground="pink",width=2,height=1, command=lambda:self.colorTextoFig("pink"))
        self.botonColorRosa.grid(column=3,row=2,pady=10)

        self.ventanaColorF.protocol("WM_DELETE_WINDOW", self.borrarVentanaColorFigura)

    def colorTextoFig(self,clr):
        self.color = clr
        self.botonColores.config(state=ACTIVE)
        self.ventanaColorF.destroy()

    def colorTextoFun(self,clr):
        self.colorTextoUsuario = clr
        self.entryTexto.config(fg=clr)
        self.botonColor.config(bg=clr,activebackground=clr,state=ACTIVE)
        self.ventanaColor.destroy()
        
    def guardarTexto(self):
        self.botonTexto.config(state=ACTIVE)
        self.ventana.config(cursor="tcross")
        self.textoUsuario = self.entryTexto.get(1.0,END)
        self.tamanoLetraUsuario = self.entryTamano.get()
        self.textoTamano.config(text=self.textoUsuario[:-1],font=("Calibri",self.tamanoLetraUsuario))

        self.ventanaTexto.destroy()

    def borrarVentanaTexto(self):
        try:
            var = int(self.entryTamano.get())
            self.botonTexto.config(state=ACTIVE)
            self.ventanaTexto.destroy()
        except:
            pass

    def borrarVentanaColor(self):
        try:
            self.botonColor.config(state=ACTIVE)
            self.ventanaColor.destroy()
        except:
            pass

    def borrarVentanaColorFigura(self):
        try:
            self.botonColores.config(state=ACTIVE)
            self.ventanaColorF.destroy()
        except:
            pass
    
    def numeroEntry(action, char, text):
        if action != "1":
            return True
        return char in "0123456789" and len(text) < 3

    def borrarTodosLosCampos(self):
        self.entryPosX.delete(0, END)
        self.entryPosY.delete(0, END)
        self.entryLargo.delete(0, END)
        self.entryAncho.delete(0, END)

    def botonPresionado(self,btn):
        self.boton = btn
        if(btn == "punto"):
            self.entryPosX.config(state="normal")
            self.entryPosY.config(state="normal")

            self.entryLargo.config(state="readonly")
            self.entryAncho.config(state="readonly")

            self.labelLargo.config(text="")
            self.labelAncho.config(text="")
            
            self.ventana.config(cursor="tcross")
            self.borrarTodosLosCampos()

        elif(btn == "linea"):
            self.entryPosX.config(state="normal")
            self.entryPosY.config(state="normal")

            self.entryLargo.config(state="normal")
            self.entryAncho.config(state="normal")

            self.labelLargo.config(text="FINAL X: ")
            self.labelAncho.config(text="FINAL Y:")
            
            self.ventana.config(cursor="tcross")

            self.borrarTodosLosCampos()

        elif(btn == "recta"):
            self.entryPosX.config(state="normal")
            self.entryPosY.config(state="normal")

            self.entryLargo.config(state="normal")
            self.entryAncho.config(state="normal")

            self.labelLargo.config(text="FINAL X: ")
            self.labelAncho.config(text="FINAL Y: ")
            
            self.ventana.config(cursor="tcross")

            self.borrarTodosLosCampos()

        elif(btn == "circulo"):
            self.entryPosX.config(state="normal")
            self.entryPosY.config(state="normal")

            self.entryLargo.config(state="normal")
            self.entryAncho.config(state="normal")

            self.labelLargo.config(text="FINAL X: ")
            self.labelAncho.config(text="FINAL Y: ")
            
            self.ventana.config(cursor="tcross")

            self.borrarTodosLosCampos()

        elif(btn == "trian"):
            self.entryPosX.config(state="normal")
            self.entryPosY.config(state="normal")

            self.entryLargo.config(state="normal")
            self.entryAncho.config(state="normal")

            self.labelLargo.config(text=" FINAL X: ")
            self.labelAncho.config(text="FINAL Y:")
            
            self.ventana.config(cursor="tcross")

            self.borrarTodosLosCampos()

        elif(btn == "texto"):
            self.entryPosX.config(state="normal")
            self.entryPosY.config(state="normal")

            self.entryLargo.config(state="readonly")
            self.entryAncho.config(state="readonly")

            self.labelLargo.config(text="")
            self.labelAncho.config(text="")

            self.borrarTodosLosCampos()

            self.ventanaOpcionTexto()

        elif(btn == "seleccion"):
            self.ventana.config(cursor="")
            self.entryLargo.config(state="readonly")
            self.entryAncho.config(state="readonly")

        elif(btn == "mover"):
            self.ventana.config(cursor="")
        elif(btn == "copiar"):
            self.ventana.config(cursor="")
        elif(btn == "borrar"):
            self.ventana.config(cursor="")
        elif(btn == "colores"):
            self.ventanaOpcionColorFigura()
            self.ventana.config(cursor="")

    def adentro(self,event,btn,X,Y):
        self.infoBoton.config(text=btn)
        self.infoBoton.place(x=X,y=Y)

        if(btn[:2] == "Pu"):self.botonPunto.config(bg="#ADD8E6")
        elif(btn[:2] == "Li"):self.botonLinea.config(bg="#ADD8E6")
        elif(btn[:2] == "Re"):self.botonRectangulo.config(bg="#ADD8E6")
        elif(btn[:2] == "Ci"):self.botonCirculo.config(bg="#ADD8E6")
        elif(btn[:2] == "Tr"):self.botonTriangulo.config(bg="#ADD8E6")
        elif(btn[:2] == "Te"):
            if(self.botonTexto.cget('state') == 'normal'):
                self.botonTexto.config(bg="#ADD8E6")
        if(btn == "Seleccionar"):self.botonSeleccionar.config(bg="#ADD8E6")
        elif(btn == "Mover"):self.botonMover.config(bg="#ADD8E6")
        elif(btn == "Copiar"):self.botonCopiar.config(bg="#ADD8E6")
        elif(btn == "Borrar"):self.botonBorrar.config(bg="#ADD8E6")
        elif(btn == "Color"):
            if(self.botonColores.cget('state') == 'normal'):
                self.botonColores.config(bg="#ADD8E6")

    def afuera(self,event):
        self.botonPunto.config(bg=self.ventana.cget('bg'))
        self.botonLinea.config(bg=self.ventana.cget('bg'))
        self.botonRectangulo.config(bg=self.ventana.cget('bg'))
        self.botonCirculo.config(bg=self.ventana.cget('bg'))
        self.botonTriangulo.config(bg=self.ventana.cget('bg'))
        self.botonTexto.config(bg=self.ventana.cget('bg'))

        self.botonSeleccionar.config(bg=self.ventana.cget('bg'))
        self.botonMover.config(bg=self.ventana.cget('bg'))
        self.botonCopiar.config(bg=self.ventana.cget('bg'))
        self.botonBorrar.config(bg=self.ventana.cget('bg'))
        self.botonColores.config(bg=self.ventana.cget('bg'))

        self.infoBoton.config(text="")
        self.infoBoton.place(x=-10,y=0)

    def posMouse(self,event):
        self.entryPosMoX.config(text=event.x)
        self.entryPosMoY.config(text=event.y)

        return(event.x,event.y)

    def btnCordenadas(self):
        cordenadas = Punto.Evento(int(self.entryPosX.get()),int(self.entryPosY.get()))
        if(self.boton == "punto"):
            self.primeraX = int(self.entryPosX.get())
            self.primeraY = int(self.entryPosY.get())
            self.crearFigura(cordenadas)
        elif(self.boton == "linea"):
            self.primeraX = int(self.entryPosX.get())
            self.primeraY = int(self.entryPosY.get())
            self.ultimaX = int(self.entryLargo.get())
            self.ultimaY = int(self.entryAncho.get())
            self.crearFigura(cordenadas)
        elif(self.boton == "recta"):
            self.primeraX = int(self.entryPosX.get())
            self.primeraY = int(self.entryPosY.get())
            self.ultimaX = int(self.entryLargo.get())
            self.ultimaY = int(self.entryAncho.get())
            self.crearFigura(cordenadas)
        elif(self.boton == "circulo"):
            self.primeraX = int(self.entryPosX.get())
            self.primeraY = int(self.entryPosY.get())
            self.ultimaX = int(self.entryLargo.get())
            self.ultimaY = int(self.entryAncho.get())
            self.crearFigura(cordenadas)
        elif(self.boton == "trian"):
            self.primeraX = int(self.entryPosX.get())
            self.primeraY = int(self.entryPosY.get())
            self.ultimaX = int(self.entryLargo.get())
            self.ultimaY = int(self.entryAncho.get())
            self.crearFigura(cordenadas)
        elif(self.boton == "texto"):
            self.primeraX = int(self.entryPosX.get())
            self.primeraY = int(self.entryPosY.get())
            self.crearFigura(cordenadas)

    #----------------------------------------------- INICIO DE CREACION DE FIGURAS --------------------------------------------------
    def PosicionIncialFigura(self,event):
        if(self.boton != "seleccion" and self.boton != "mover" and self.boton != "copiar" and self.boton != "borrar"):
            print("dibujar en cordenadas iniciales X:{0} Y:{1}".format(event.x,event.y))
            self.primeraX = event.x
            self.primeraY = event.y
            self.ultimaX = event.x
            self.ultimaY = event.y
            self.entryPosX.insert(END,self.primeraX)
            self.entryPosY.insert(END,self.primeraY)

        if(self.boton == "seleccion"):
            self.dibujarTodo()
            for i in range(self.contadorFiguras):
                if(self.figura[i].seleccionar(event.x,event.y)):
                    self.consola.insert(END, "figura seleccionada en X1: {0}, Y1: {1}, X2: {2} Y2: {3}\n".format(self.figura[i].x1(),self.figura[i].y1(),self.figura[i].x2(),self.figura[i].y2()))
                    self.figura[i].dibujarSeleccion(self.lienzoCanvas)
                    return 0

    def dibujarFigura(self,event):
        if(self.boton == "punto"):
            pass
        elif(self.boton == "linea"):
            self.lienzoCanvas.create_line(self.primeraX,self.primeraY,event.x,event.y,fill=self.color)
            self.lienzoCanvas.create_line(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY,fill="white")
        elif(self.boton == "recta"):
            self.lienzoCanvas.create_rectangle(self.primeraX,self.primeraY,event.x,event.y,outline=self.color)
            self.lienzoCanvas.create_rectangle(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY,outline="white")
        elif(self.boton == "circulo"):
            self.lienzoCanvas.create_oval(self.primeraX,self.primeraY,event.x,event.y,outline=self.color)
            self.lienzoCanvas.create_oval(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY,outline="white")
        elif(self.boton == "trian"):
            self.lienzoCanvas.create_line(self.primeraX,self.primeraY,event.x,event.y,fill=self.color) # HIPOTENUSA
            self.lienzoCanvas.create_line(self.primeraX,self.primeraY,event.x,self.primeraY,fill=self.color) # BASE
            self.lienzoCanvas.create_line(event.x,self.primeraY,event.x,event.y,fill=self.color) # ALTURA

            self.lienzoCanvas.create_line(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY,fill="white") # HIPOTENUSA
            self.lienzoCanvas.create_line(self.primeraX,self.primeraY,self.ultimaX,self.primeraY,fill="white") # BASE
            self.lienzoCanvas.create_line(self.ultimaX,self.primeraY,self.ultimaX,self.ultimaY,fill="white") # ALTURA

        elif(self.boton == "texto"):
            self.lienzoCanvas.create_text(event.x,event.y,text=self.textoUsuario,font=("Calibri",self.tamanoLetraUsuario),fill=self.colorTextoUsuario,anchor="nw")
            self.lienzoCanvas.create_rectangle(self.ultimaX,self.ultimaY,self.ultimaX+self.textoTamano.winfo_width(),self.ultimaY+self.textoTamano.winfo_height(),fill="white",outline="white")
            import time
            time.sleep(0.09)

        self.entryPosMoX.config(text=event.x)
        self.entryPosMoY.config(text=event.y)

        self.ultimaX = event.x
        self.ultimaY = event.y

    def crearFigura(self,event):
        if(self.boton == "punto"):
            self.consola.insert(END, "punto creado en X1: {0}, Y1: {1}, X2: {2} Y2: {3}\n".format(self.primeraX,self.primeraY,self.primeraX,self.primeraY))
            self.figura.append(Punto.Punto(self.primeraX,self.primeraY,self.primeraX+5,self.primeraY+5,self.color,self.contadorFiguras))
            self.figura[self.contadorFiguras].dibujar(self.lienzoCanvas)
            if(self.boton not in self.dictFiguras.keys()): self.dictFiguras[self.boton] = [self.contadorFiguras]
            else: self.dictFiguras[self.boton].append(self.contadorFiguras)
            self.contadorFiguras +=1
        elif(self.boton == "linea"):
            self.consola.insert(END, "Linea creada en X1: {0}, Y1: {1}, X2: {2} Y2: {3}\n".format(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY))
            self.figura.append(Punto.Linea(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY,self.color,self.contadorFiguras))
            self.figura[self.contadorFiguras].dibujar(self.lienzoCanvas)
            if(self.boton not in self.dictFiguras.keys()): self.dictFiguras[self.boton] = [self.contadorFiguras]
            else: self.dictFiguras[self.boton].append(self.contadorFiguras)
            self.contadorFiguras +=1
        elif(self.boton == "recta"):
            self.consola.insert(END, "Rectangulo creado en X1: {0}, Y1: {1}, X2: {2} Y2: {3}\n".format(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY))
            self.figura.append(Punto.Rectangulo(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY,self.color,self.contadorFiguras))
            self.figura[self.contadorFiguras].dibujar(self.lienzoCanvas)
            if(self.boton not in self.dictFiguras.keys()): self.dictFiguras[self.boton] = [self.contadorFiguras]
            else: self.dictFiguras[self.boton].append(self.contadorFiguras)
            self.contadorFiguras +=1
        elif(self.boton == "circulo"):
            self.consola.insert(END, "Circulo creado en X1: {0}, Y1: {1}, X2: {2} Y2: {3}\n".format(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY))
            self.figura.append(Punto.Circulo(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY,self.color,self.contadorFiguras))
            self.figura[self.contadorFiguras].dibujar(self.lienzoCanvas)
            if(self.boton not in self.dictFiguras.keys()): self.dictFiguras[self.boton] = [self.contadorFiguras]
            else: self.dictFiguras[self.boton].append(self.contadorFiguras)
            self.contadorFiguras +=1
        elif(self.boton == "trian"):
            self.consola.insert(END, "Triangulo creado en X1: {0}, Y1: {1}, X2: {2} Y2: {3}\n".format(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY))
            self.figura.append(Punto.Triangulo(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY,self.color,self.contadorFiguras))
            self.figura[self.contadorFiguras].dibujar(self.lienzoCanvas)
            if(self.boton not in self.dictFiguras.keys()): self.dictFiguras[self.boton] = [self.contadorFiguras]
            else: self.dictFiguras[self.boton].append(self.contadorFiguras)
            self.contadorFiguras +=1
        elif(self.boton == "texto"):
            self.consola.insert(END, "Texto creado en X1: {0}, Y1: {1}\n".format(self.ultimaX,self.ultimaY))
            self.figura.append(Punto.Texto(self.ultimaX,self.ultimaY,self.textoUsuario,self.tamanoLetraUsuario,self.ultimaX+self.textoTamano.winfo_width(),self.ultimaY+self.textoTamano.winfo_height(),self.colorTextoUsuario,self.contadorFiguras))
            self.figura[self.contadorFiguras].dibujar(self.lienzoCanvas)
            if(self.boton not in self.dictFiguras.keys()): self.dictFiguras[self.boton] = [self.contadorFiguras]
            else: self.dictFiguras[self.boton].append(self.contadorFiguras)
            self.contadorFiguras +=1           

        if(self.boton != "seleccion" and self.boton != "mover" and self.boton != "copiar" and self.boton != "borrar"):
           self.dibujarTodo()

        self.borrarTodosLosCampos()

        self.ventana.config(cursor="")
        self.boton = "seleccion"
        self.entryLargo.config(state="readonly")
        self.entryAncho.config(state="readonly")

    def dibujarTodo(self):
        self.lienzoCanvas.delete("all")
        for x in self.dictFiguras.keys():
                if(x == "punto"):
                    for i in self.dictFiguras[x]:
                        self.lienzoCanvas.create_oval(self.figura[i].x1(),self.figura[i].y1(),self.figura[i].x2(),self.figura[i].y2(),fill=self.figura[i].co())

                elif(x == "linea"):
                    for i in self.dictFiguras[x]:
                        self.lienzoCanvas.create_line(self.figura[i].x1(),self.figura[i].y1(),self.figura[i].x2(),self.figura[i].y2(),fill=self.figura[i].co())

                elif(x == "recta"):
                    for i in self.dictFiguras[x]:
                        self.lienzoCanvas.create_rectangle(self.figura[i].x1(),self.figura[i].y1(),self.figura[i].x2(),self.figura[i].y2(),outline=self.figura[i].co())

                elif(x == "circulo"):
                    for i in self.dictFiguras[x]:
                        self.lienzoCanvas.create_oval(self.figura[i].x1(),self.figura[i].y1(),self.figura[i].x2(),self.figura[i].y2(),outline=self.figura[i].co())

                elif(x == "trian"):
                    for i in self.dictFiguras[x]:
                        self.lienzoCanvas.create_line(self.figura[i].x1(),self.figura[i].y1(),self.figura[i].x2(),self.figura[i].y2(),fill=self.figura[i].co())
                        self.lienzoCanvas.create_line(self.figura[i].x1(),self.figura[i].y1(),self.figura[i].x2(),self.figura[i].y1(),fill=self.figura[i].co()) # BASE
                        self.lienzoCanvas.create_line(self.figura[i].x2(),self.figura[i].y1(),self.figura[i].x2(),self.figura[i].y2(),fill=self.figura[i].co()) # ALTURA
                elif(x == "texto"):
                    for i in self.dictFiguras[x]:
                        self.lienzoCanvas.create_text(self.figura[i].x1(),self.figura[i].y1(),text=self.figura[i].tex(),font=("Calibri", self.figura[i].ttex()),fill=self.figura[i].co(),anchor="nw")
    # ---------------------------------------- FIN DE CREACION DE FIGURAS -------------------------------------------------

def main(): 
    ventanaDrawA = Tk()
    app = Aplicacion(ventanaDrawA)

    ventanaDrawA.mainloop()


main()