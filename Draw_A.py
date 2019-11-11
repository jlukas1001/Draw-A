from tkinter import *
from tkinter import messagebox

import Punto

class Aplicacion:
    def __init__(self, ventanaPrincipal):

        self.ventana = ventanaPrincipal # Creacion de la ventana principal
        self.ventana.title("Draw_A") # Titulo de la ventana
        self.ventana.geometry("1366x768") # Tamano de la ventana 1366x768 pixeles
        self.ventana.resizable(False,False) # No redimensionar la pantalla

        # Creacion de variables importantes que se necesitaran a lo largo del codigo

        self.boton = "seleccionar" # Variable que guardara el boton que este presionado, por defecto seleccionar
        self.color = "black" # Variable que guardara el color de las figuras, por defecto negro
        self.figura = [] # Lista en la cual se guardara la coleccion de objetos, con todas las figuras que el usuario cree

        self.dictFiguras = {} # Diccionario qie permitira separan por figuras los elementos clave-->figura |  elemento-->indice
        self.contadorFiguras = 0 # Contador que lleva la cuenta de cuantos objetos se han creado

        self.primeraX = 0 # Variable que guarda la primera cordena x que el usuario ingresa o selecciona
        self.primeraY = 0 # Variable que guarda la primera cordena y que el usuario ingresa o selecciona

        self.ultimaX = 0 # Variable que guarda la ultima cordenada x que el usuario ingresa o selecciona
        self.ultimaY = 0 # Variable que guarda la ultima cordenada y que el usuario ingresa o selecciona

        self.figuraSeleccionada = -1 # Variable que almacena el indice de la figura que se selecciono, si ninguna es seleccionada su valor es de -1

        # ------------------------------------------- LIENZO DE PINTURA ---------------------------------------------------------------

        self.frameLienzo = Frame(self.ventana,width=800,bg="white",height=600,borderwidth=3, relief="solid")
        self.frameLienzo.place(x=20,y=120)

        self.lienzoCanvas = Canvas(self.frameLienzo,width=800, height=600, bg='white')
        self.lienzoCanvas.pack()
            
        # El proceso en el cual crearan las figuras consiste en tres etapas:
        #         1 ---> El usuario hace click en un boton (punto,linea,etc) luego hace click en el canvas, esas seran las primeras cordenadas x,y del objeto, seran almacenadas en self.primeraX,self.primeraY respectivamente
        #         2 ---> El usuario se desplaza con el click sostenido dentro del canvas, se capturan constantemente las cordenadas y se va bocetando la figura con las cordenadas en la que esta el cursor, estos son atributos de event (event.x,event.y)
        #         3 ---> El usuario deja de oprimir el click, en ese momento se crea un objeto del tipo seleccionado anteriormente con las coordenadas del paso 1 y las cordenadas x,y donde se solto el click, estas seran almacenadas en self.ultimaX,self.ultimaY
         
        self.lienzoCanvas.bind("<Motion>", self.posMouse) # evento de movimiento en el canvas, este permite mostrar las cordenadas del mouse dentro del canvas en un label
        self.lienzoCanvas.bind("<Button-1>",self.PosicionIncialFigura) # evento de click en el canvas cuando este ocurre empieza la creacion o modificacion de las figuras
        self.lienzoCanvas.bind("<B1-Motion>", self.dibujarFigura) # evento de movimiento con el click sostenido dentro del canvas, permite mover o crear las figuras en tiempo real
        self.lienzoCanvas.bind("<ButtonRelease-1>", self.crearFigura) # evento cuando se suelta el click del mouse dentro del canvas, aqui se finaliza la creacion y modificacion de las figuras

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

        # Todos los botones comparten un metodo en comun llamado self.botonPresionado la cual recibe de parametro el objeto al cual esta asociado ese boton
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

        # Se utilizan los eventos de los botones Entre y Leave para poner etiquetas con el nombre y la funcion cuando se pasa el cursor por ahi
       
        # El evento Enter --> captura cuando el cursor esta dentro del boton
        # El evento Leave --> captura cuando el cursor esta afuera del boton

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

    def ventanaOpcionTexto(self): # Creacion de la ventana que permite ingresar texto usuario
        self.botonTexto.config(state=DISABLED) # Cuando se abre la ventana se desabilita el boton del texto, esto para que no se abra mas de una ventana
        self.ventanaTexto = Toplevel(self.ventana) # Se declara que la ventana de texto hereda de la ventana principal
        self.ventanaTexto.transient(self.ventana) # Como la ventana del texto hereda de la ventana principal, con este comando la ventana del texto no se cierra hasta que se finalice
        self.ventanaTexto.geometry("400x260+400+130") # Se le da un tamaño de 400x260 pixeles, ademas cuando se le suma se corre 400 pixeles a la derecha y 130 pixeles abajo
        self.ventanaTexto.resizable(False,False)  # No deja redimensionar la pantalla
        self.ventanaTexto.title("Configurar texto") # Configura un titulo a la ventana

        # ---------------------------------------------------- CREANDO ELEMENTOS DE LA VENTANA -------------------------------------------------
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

        self.botonColor = Button(self.frame1,bg="black", activebackground="black",width=2,height=1,command=self.ventanaOpcionColorTexto,state=ACTIVE) # Boton que abre una ventana en la cual salen todos los colores a seleccionar al presionar se ejecuta el metodo self.ventanaOpcionColorTexto
        self.botonColor.place(x=340,rely=0.5, anchor=CENTER)
        self.colorTextoUsuario = "black"
        
        self.labelTexto = Label(self.frame2,text="Texto: ",font=("Calibri",14))
        self.labelTexto.grid(column=0,row=0,padx=15)

        self.entryTexto = Text(self.frame2,height=4,width=30,state=NORMAL,font=("Arial",12))
        self.entryTexto.grid(column=1,row=0,columnspan=6)

        self.scrollTexto = Scrollbar(self.frame2,command=self.entryTexto.yview)
        self.scrollTexto.grid(column=8,row=0,sticky="nsew")

        self.entryTexto.config(yscrollcommand=self.scrollTexto.set)

        self.botonAceptar = Button(self.frame3,text="Aceptar",command=self.guardarTexto,font=("Calibri",14),borderwidth=3,relief="groove") # Boton aceptar, es el encargado de cerrar la ventana y guardar datos como color,tamano y texto en el metodo self.guardarTexto
        self.botonAceptar.place(relx=0.5,rely=0.5, anchor=CENTER)

        self.ventanaTexto.protocol("WM_DELETE_WINDOW", self.borrarVentanaTexto) # Evento que se ejecuta cuando se presiona el boton de cerrar ventana, este redirige al metodo self.borrarVentanaTexto

    def ventanaOpcionColorTexto(self): # Ventana que tiene los posibles colores que puede escoger el usuario para el texto
        self.botonColor.config(state=DISABLED) # Cuando se abre la ventana se desabilita el boton color, esto para que no se abra mas de una ventana
        self.ventanaColor = Toplevel(self.ventanaTexto) # La ventanaColor hereda de la ventanaTexto
        self.ventanaColor.transient(self.ventanaTexto) # Como la ventana color hereda de texto, entonces hasta que no se cierre la ventana color no se puede quitar
        self.ventanaColor.geometry("148x120+770+60") # Se le da un tamaño de 148x120 pixeles, ademas cuando se le suma se corre 770 pixeles a la derecha y 60 pixeles abajo
        self.ventanaColor.resizable(False,False) # No deja redimensionar la pantalla
        self.ventanaColor.title("Cambiar color") # Configura el titulo de la ventana

        # ------------------------------------------ BOTONES QUE TIENE COMO BACKGROUND LOS POSIBLES COLORES HA ESCOGER ----------------------------------------------------
        # Todos los botones tienen como command el mismo metodo el cual recibe como parametro el color del boton
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

        self.ventanaColor.protocol("WM_DELETE_WINDOW", self.borrarVentanaColor) # Evento que se ejecuta cuando se cierra la ventana, se llama el metodo self.borrarVentanaColor

    def ventanaOpcionColorFigura(self):  # Ventana que tiene los posibles colores que puede escoger el usuario para la figura
        self.botonColores.config(state=DISABLED) # Cuando se abre la ventana se desabilita el boton color, esto para que no se abra mas de una ventana
        self.ventanaColorF = Toplevel(self.ventana) # La ventanaColor hereda de la ventana principal
        self.ventanaColorF.transient(self.ventana) # Como la ventana color hereda de la ventana principal, entonces hasta que no se cierre la ventana color no se puede quitar
        self.ventanaColorF.geometry("148x120+800+60") # Se le da un tamaño de 148x120 pixeles, ademas cuando se le suma se corre 800 pixeles a la derecha y 60 pixeles abajo
        self.ventanaColorF.resizable(False,False) # No deja redimensionar la pantalla
        self.ventanaColorF.title("Cambiar color") # Configura el titulo de la ventana

        # ------------------------------------------ BOTONES QUE TIENE COMO BACKGROUND LOS POSIBLES COLORES HA ESCOGER ----------------------------------------------------
        # Todos los botones tienen como command el mismo metodo el cual recibe como parametro el color del boton
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

        self.ventanaColorF.protocol("WM_DELETE_WINDOW", self.borrarVentanaColorFigura) # Evento que se ejecuta cuando se cierra la ventana, se llama el metodo self.borrarVentanaColorFigura

    def colorTextoFig(self,clr): # Metodo que almacena el color seleccionado para figura
        self.color = clr # El color que se pasa como parametro y es almacenado en la variable self.color
        self.botonColores.config(state=ACTIVE) # Activa el boton de color que fue deshabilitado al abrir la pestaña
        self.ventanaColorF.destroy() # Cierra la ventana

    def colorTextoFun(self,clr): # Metodo que almacena el color seleccionado para el texto
        self.colorTextoUsuario = clr # El color que se pasa como parametro y es almacenado en la variable self.colorTextoUsuario
        self.entryTexto.config(fg=clr) # Cambia el color de la fuente donde se escribe el texto 
        self.botonColor.config(bg=clr,activebackground=clr,state=ACTIVE) # Activa el boton del color que fue deshabilitado al abrir la pestaña, cambia el color de fondo del boton por el escogido
        self.ventanaColor.destroy() # Cierra la ventana
        
    def guardarTexto(self): # Metodo que almacena el texto ingresado por el usuario
        self.botonTexto.config(state=ACTIVE) # Activa el boton de texto que fue deshabilitado al abrir la pestaña
        self.ventana.config(cursor="crosshair") # Cambia el estilo de cursor, este estilo es el que indica al usuario que esta listo para dibujar en el lienzo
        self.textoUsuario = self.entryTexto.get(1.0,END) # Se guarda el texto que el usuario ingreso en la variable self.textoUsuario desde el indice 1.0,hasta el final
        self.tamanoLetraUsuario = self.entryTamano.get() # Se guarda el tamañano de la fuente
        self.textoTamano.config(text=self.textoUsuario[:-1],font=("Calibri",self.tamanoLetraUsuario)) # Se guarda el texto en un label invisible, para luego usar los metodos winfo_height() y winfo_width() que permiten saber el largo y el ancho en pixeles que ocupa un texto, esto es necesario para seleccionar, y borrar luego el texto, se pone un caracter menos porque daba un salto de linea
        self.ventanaTexto.destroy() # Cierra la ventana

    def borrarVentanaTexto(self): # Metodo que borra la ventana del texto
        try: # Si se le pasa una letra en el tamaño el programa se queda quieto, por esta razon esta dentro de un try / except
            var = int(self.entryTamano.get()) # almacena en var el valor entero del tamaño, en caso que no se pudiera simplemente no se cierra la pestaña hasta que se ingrese un numero
            self.botonTexto.config(state=ACTIVE) # Se activa el boton de texto que habia sido deshabilitado
            self.ventanaTexto.destroy() # Se destruye la ventana del texto
        except:
            pass

    def borrarVentanaColor(self): # Metodo que borra la ventana del color
        try: # intenta cerrar la ventana, en algunos casos puede mandar error
            self.botonColor.config(state=ACTIVE) # Activa el boton de color
            self.ventanaColor.destroy() # Se destruye la ventana de color
        except:
            pass

    def borrarVentanaColorFigura(self): # Metodo que borra la ventana del color
        try: # intenta cerrar la ventana, en algunos casos puede mandar error
            self.botonColores.config(state=ACTIVE) # Activa el boton de color
            self.ventanaColorF.destroy() # Se destruye la ventana de color
        except:
            pass
    

    def borrarTodosLosCampos(self): # Metodo que borra los entry de las cordenadas
        self.entryPosX.delete(0, END) # Borra los indices desde el cero hasta el ultimo
        self.entryPosY.delete(0, END) # Borra los indices desde el cero hasta el ultimo
        self.entryLargo.delete(0, END) # Borra los indices desde el cero hasta el ultimo
        self.entryAncho.delete(0, END) # Borra los indices desde el cero hasta el ultimo

    def botonPresionado(self,btn): # Metodo que se ejecuta cuando se presiona un boton de las herramientas o figuras
        self.boton = btn # La variable self.boton almacena el boton que fue presionado, esta variable ya fue declarada al inicio del codigo

        if(btn == "punto"): # Se ejecuta si se presiona el boton punto 
            self.entryPosX.config(state="normal") # Activa el entry para la cordenada x
            self.entryPosY.config(state="normal") # Activa el entry para la cordenada y

            self.entryLargo.config(state="readonly") # Desactiva el entry para la cordenada x1
            self.entryAncho.config(state="readonly") # Desativa el entry para la cordenada y1

            self.labelLargo.config(text="") # Borra la etiqueta de final x, dando a entender que esta deshabilitada
            self.labelAncho.config(text="") # Borra la etiqueta de final y, dando a entender que esta deshabilitada
            
            self.ventana.config(cursor="crosshair") # Cambia el estilo de cursor, este estilo es el que indica al usuario que esta listo para dibujar en el lienzo
            self.borrarTodosLosCampos() # Borra todos los campos de los entrys de cordenadas

        elif(btn == "linea"): # Se ejecuta si se presiona el boton linea
            self.entryPosX.config(state="normal") # Activa el entry para la cordenada x
            self.entryPosY.config(state="normal") # Activa el entry para la cordenada y

            self.entryLargo.config(state="normal") # Activa el entry para la cordenada x1
            self.entryAncho.config(state="normal") # Activa el entry para la cordenada y1

            self.labelLargo.config(text="FINAL X: ") # Le da nombre a la etiqueta que en este objeto si esta habilitada
            self.labelAncho.config(text="FINAL Y:") # Le da nombre a la etiqueta que en este objeto si esta habilitada
            
            self.ventana.config(cursor="crosshair") # Cambia el estilo de cursor, este estilo es el que indica al usuario que esta listo para dibujar en el lienzo

            self.borrarTodosLosCampos()# Borra todos los campos de los entrys de cordenadas

        elif(btn == "recta"): # Se ejecuta si se presiona el boton rectangulo
            self.entryPosX.config(state="normal") # Activa el entry para la cordenada x
            self.entryPosY.config(state="normal") # Activa el entry para la cordenada y

            self.entryLargo.config(state="normal") # Activa el entry para la cordenada x1
            self.entryAncho.config(state="normal") # Activa el entry para la cordenada y1

            self.labelLargo.config(text="FINAL X: ") # Le da nombre a la etiqueta que en este objeto si esta habilitada
            self.labelAncho.config(text="FINAL Y: ") # Le da nombre a la etiqueta que en este objeto si esta habilitada
            
            self.ventana.config(cursor="crosshair") # Cambia el estilo de cursor, este estilo es el que indica al usuario que esta listo para dibujar en el lienzo

            self.borrarTodosLosCampos() # Borra todos los campos de los entrys de cordenadas

        elif(btn == "circulo"): # Se ejecuta si se presiona el boton circulo
            self.entryPosX.config(state="normal") # Activa el entry para la cordenada x
            self.entryPosY.config(state="normal") # Activa el entry para la cordenada y

            self.entryLargo.config(state="normal") # Activa el entry para la cordenada x1
            self.entryAncho.config(state="normal") # Activa el entry para la cordenada y1

            self.labelLargo.config(text="FINAL X: ") # Le da nombre a la etiqueta que en este objeto si esta habilitada
            self.labelAncho.config(text="FINAL Y: ") # Le da nombre a la etiqueta que en este objeto si esta habilitada

            self.ventana.config(cursor="crosshair") # Cambia el estilo de cursor, este estilo es el que indica al usuario que esta listo para dibujar en el lienzo

            self.borrarTodosLosCampos() # Borra todos los campos de los entrys de cordenadas

        elif(btn == "trian"): # Se ejecuta si se presiona el boton triangulo
            self.entryPosX.config(state="normal") # Activa el entry para la cordenada x
            self.entryPosY.config(state="normal") # Activa el entry para la cordenada y

            self.entryLargo.config(state="normal") # Activa el entry para la cordenada x1
            self.entryAncho.config(state="normal") # Activa el entry para la cordenada y1

            self.labelLargo.config(text=" FINAL X: ") # Le da nombre a la etiqueta que en este objeto si esta habilitada
            self.labelAncho.config(text="FINAL Y:") # Le da nombre a la etiqueta que en este objeto si esta habilitada
            
            self.ventana.config(cursor="crosshair") # Cambia el estilo de cursor, este estilo es el que indica al usuario que esta listo para dibujar en el lienzo

            self.borrarTodosLosCampos() # Borra todos los campos de los entrys de cordenadas

        elif(btn == "texto"): # Se ejecuta si se presiona el boton texto
            self.entryPosX.config(state="normal") # Activa el entry para la cordenada x
            self.entryPosY.config(state="normal") # Activa el entry para la cordenada y

            self.entryLargo.config(state="readonly") # Desactiva el entry para la cordenada x1
            self.entryAncho.config(state="readonly") # Desactiva el entry para la cordenada y1

            self.labelLargo.config(text="") # Borra la etiqueta de final x, dando a entender que esta deshabilitada
            self.labelAncho.config(text="") # Borra la etiqueta de final y dando a entender que esta deshabilitada

            self.borrarTodosLosCampos() # Borra todos los campos de los entrys de cordenadas

            self.ventanaOpcionTexto() # Abre la ventana de texto, para que el usuario ingrese el texto deseado, este metodo fue declarado antes

        elif(btn == "seleccion"): # Se ejecuta si se presiona el boton seleccion
            self.ventana.config(cursor="hand2") # Cambia el estilo de cursor, este estilo es el que indica al usuario que puede seleccionar un objeto en el lienzo
            self.entryLargo.config(state="readonly") # Desactiva el entry para la cordenada x1
            self.entryAncho.config(state="readonly") # Desactiva el entry para la cordenada y1

        elif(btn == "mover"): # Se ejecuta si se presiona el boton mover
            self.ventana.config(cursor="fleur") # Cambia el estilo de cursor, este estilo es el que indica al usuario que puede mover un objeto en el lienzo
        elif(btn == "copiar"): # Se ejecuta si se presiona el boton copiar
            self.ventana.config(cursor="target") # Cambia el estilo de cursor, este estilo es el que indica al usuario que puede copiar un objeto en el lienzo
        elif(btn == "borrar"): # Se ejecuta si se presiona el boton borrar

            self.ventana.config(cursor="hand2") # Cambia el estilo de cursor, este estilo es el que indica al usuario que puede seleccionar un objeto en el lienzo
            if(self.figuraSeleccionada != -1): # cuando self.figuraSeleccionada != -1 quiere decir que ya hay un objeto seleccionado
                if("Punto.Texto" not in str(type(self.figura[self.figuraSeleccionada]))): # Esto evalua si el objeto seleccionado es diferente de un texto, ya que el texto maneja propiedades distintas que los otros objetos
                    self.figura[self.figuraSeleccionada].borrarFigura(self.lienzoCanvas) # Este metodo colorea la figura seleccionada de blanco dentro del lienzo, es decir, lo borra del lienzo solamente
                    self.figura[self.figuraSeleccionada].borrarObjeto() # Este metodo borra el objeto, es decir, ahora si ya no existe el objeto en el programa
                else: # Esto quiere decir que el objeto es texto, por lo que tiene que trabajar con parametros adicionales como el texto y el tamaño
                    self.figura[self.figuraSeleccionada].borrarFigura(self.lienzoCanvas) # Este metodo colorea el texto seleccionada de blanco dentro del lienzo, es decir, lo borra del lienzo solamente
                    self.figura[self.figuraSeleccionada].borrarObjeto() # Este metodo borra el texto, es decir, ahora si ya no existe el objeto en el programa

        elif(btn == "colores"):  # Se ejecuta si se presiona el boton color
            self.ventanaOpcionColorFigura() # Este metodo abre una ventana para cambiar el color
            self.ventana.config(cursor="") # Deja el cursor como estaba de serie

    def adentro(self,event,btn,X,Y): # Este metodo se ejecuta cuando el cursor esta adentro de un boton
        self.infoBoton.config(text=btn) # Dibuja una etiqueta con el nombre del boton
        self.infoBoton.place(x=X,y=Y) # Posiciona la etiqueta en las cordenadas X,Y establecidas previamente

        # Esta seccion colorea el boton de azul (#ADD8E6) cuando  el mouse esta encima
        if(btn[:2] == "Pu"):self.botonPunto.config(bg="#ADD8E6")
        elif(btn[:2] == "Li"):self.botonLinea.config(bg="#ADD8E6")
        elif(btn[:2] == "Re"):self.botonRectangulo.config(bg="#ADD8E6")
        elif(btn[:2] == "Ci"):self.botonCirculo.config(bg="#ADD8E6")
        elif(btn[:2] == "Tr"):self.botonTriangulo.config(bg="#ADD8E6")
        elif(btn[:2] == "Te"):
            if(self.botonTexto.cget('state') == 'normal'):# Esto impide que se coloree cuando el boton esta deshabilitado, esto cuando se abre una ventana extra
                self.botonTexto.config(bg="#ADD8E6")
        if(btn == "Seleccionar"):self.botonSeleccionar.config(bg="#ADD8E6")
        elif(btn == "Mover"):self.botonMover.config(bg="#ADD8E6")
        elif(btn == "Copiar"):self.botonCopiar.config(bg="#ADD8E6")
        elif(btn == "Borrar"):self.botonBorrar.config(bg="#ADD8E6")
        elif(btn == "Color"):# Esto impide que se coloree cuando el boton esta deshabilitado, esto cuando se abre una ventana extra
            if(self.botonColores.cget('state') == 'normal'):
                self.botonColores.config(bg="#ADD8E6")

    def afuera(self,event): # Este metodo se ejecuta cuando el cursor esta afuera de un boton
        #Colorea el boton otra vez al color de fabrica self.ventana.cget('bg'), este es el color de fondo actual
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

        self.infoBoton.config(text="") # Borra el texto de la etiqueta para desaparecerla
        self.infoBoton.place(x=-10,y=0) # Posiciona en un lugar que no es relevante

    def posMouse(self,event): # Metodo que se ejecuta cada vez que se mueve el mouse en el lienzo
        self.entryPosMoX.config(text=event.x) # Guarda en el label de posMox la cordenada del mouse en x
        self.entryPosMoY.config(text=event.y) # Guarda en el label de posMoy la cordenada del mouse en y

        return(event.x,event.y) # Devuelve las cordenadas

    def btnCordenadas(self): # Este metodo se ejecuta cuando se presiona el boton enviar de las coordenadas
        cordenadas = Punto.Evento(int(self.entryPosX.get()),int(self.entryPosY.get())) # Crea un objeto Evento, el cual simula los atributos event.x y event.y necesarios para correr los metodos que se asocian a eventos 
        if(self.boton == "punto"): # Si se presiono antes punto
            self.primeraX = int(self.entryPosX.get()) # Modifica la primeraX con el valor ingresado en el entry de inicioX
            self.primeraY = int(self.entryPosY.get()) # Modifica la primeraY con el valor ingresado en el entry de inicioY
            self.crearFigura(cordenadas) # Ingresa al metodo crear figura con el parametro cordenadas, en este caso ese parametro solo se da para que no de error
        elif(self.boton == "linea"): # Si se presiono antes linea
            self.primeraX = int(self.entryPosX.get()) # Modifica la primeraX con el valor ingresado en el entry de inicioX
            self.primeraY = int(self.entryPosY.get()) # Modifica la primeraY con el valor ingresado en el entry de inicioY
            self.ultimaX = int(self.entryLargo.get()) # Modifica la ultimaX con el valor ingresado en el entry de finalX
            self.ultimaY = int(self.entryAncho.get()) # Modifica la ultimaY con el valor ingresado en el entry de finalY
            self.crearFigura(cordenadas) # Ingresa al metodo crear figura con el parametro cordenadas, en este caso ese parametro solo se da para que no de error
        elif(self.boton == "recta"): # Si se presiono antes rectangulo
            self.primeraX = int(self.entryPosX.get()) # Modifica la primeraX con el valor ingresado en el entry de inicioX
            self.primeraY = int(self.entryPosY.get()) # Modifica la primeraY con el valor ingresado en el entry de inicioY
            self.ultimaX = int(self.entryLargo.get()) # Modifica la ultimaX con el valor ingresado en el entry de finalX
            self.ultimaY = int(self.entryAncho.get()) # Modifica la ultimaY con el valor ingresado en el entry de finalY
            self.crearFigura(cordenadas) # Ingresa al metodo crear figura con el parametro cordenadas, en este caso ese parametro solo se da para que no de error
        elif(self.boton == "circulo"): # Si se presiono antes circulo
            self.primeraX = int(self.entryPosX.get()) # Modifica la primeraX con el valor ingresado en el entry de inicioX
            self.primeraY = int(self.entryPosY.get()) # Modifica la primeraY con el valor ingresado en el entry de inicioY
            self.ultimaX = int(self.entryLargo.get()) # Modifica la ultimaX con el valor ingresado en el entry de finalX
            self.ultimaY = int(self.entryAncho.get()) # Modifica la ultimaY con el valor ingresado en el entry de finalY
            self.crearFigura(cordenadas) # Ingresa al metodo crear figura con el parametro cordenadas, en este caso ese parametro solo se da para que no de error
        elif(self.boton == "trian"): # Si se presiono antes triangulo
            self.primeraX = int(self.entryPosX.get()) # Modifica la primeraX con el valor ingresado en el entry de inicioX
            self.primeraY = int(self.entryPosY.get()) # Modifica la primeraY con el valor ingresado en el entry de inicioY
            self.ultimaX = int(self.entryLargo.get()) # Modifica la ultimaX con el valor ingresado en el entry de finalX
            self.ultimaY = int(self.entryAncho.get()) # Modifica la ultimaY con el valor ingresado en el entry de finalY
            self.crearFigura(cordenadas)  # Ingresa al metodo crear figura con el parametro cordenadas, en este caso ese parametro solo se da para que no de error
        elif(self.boton == "texto"): # Si se presiono antes texto
            self.primeraX = int(self.entryPosX.get()) # Modifica la primeraX con el valor ingresado en el entry de inicioX
            self.primeraY = int(self.entryPosY.get()) # Modifica la primeraY con el valor ingresado en el entry de inicioY
            self.crearFigura(cordenadas) # Ingresa al metodo crear figura con el parametro cordenadas, en este caso ese parametro solo se da para que no de error

        if(self.boton == "seleccion"): # Si se presiono antes seleccionar
            self.PosicionIncialFigura(cordenadas) # Se pasan las cordenadas x,y que se ingresaron en el entry

        if(self.boton == "mover"): # Si se presiono antes mover
            self.crearFigura(cordenadas) # Se pasan las cordenadas x,y que se ingresaron en el entry

        if(self.boton == "copiar"): # Si se presiono antes copiar
            self.crearFigura(cordenadas) # Se pasan las cordenadas x,y que se ingresaron en el entry

    #----------------------------------------------- INICIO DE CREACION DE FIGURAS --------------------------------------------------

    def PosicionIncialFigura(self,event): # Paso 1  -----> de creacion para las figuras, este se ejecuta cuando se hace click en el lienzo
        if(self.boton != "seleccion" and self.boton != "mover" and self.boton != "copiar" and self.boton != "borrar"): # Si se va a crear una figura
            print("dibujar en cordenadas iniciales X:{0} Y:{1}".format(event.x,event.y))
            self.primeraX = event.x # La primera cordena x va a ser donde se hizo click
            self.primeraY = event.y # La primera cordena y va a ser donde se hizo click
            self.ultimaX = event.x # se inicializa la ultimaX como posicion de inicio, esto con el fin de borrar la figura
            self.ultimaY = event.y # se inicializa la ultimaY como posicion de inicio, esto con el fin de borrar la figura
            self.entryPosX.insert(END,self.primeraX) # Se pone el valor inicial de x en el entry inicio x
            self.entryPosY.insert(END,self.primeraY) # Se pone el valor inicial de y en el entry inicio y

        if(self.boton == "seleccion"): # Si se va a seleccionar el objeto
            self.dibujarTodo() # Dibujamos todos los elementos que han sido creados previamente
            for i in range(self.contadorFiguras): # Se crea un ciclo que recorre el indice de todas las figuras creadas
                if(self.figura[i].seleccionar(event.x,event.y)): # Se hace uso del metodo seleccionar que poseen todos los objetos, el cual retorna True, si es selecionado el objeto
                    self.consola.insert(END, "figura seleccionada en X1: {0}, Y1: {1}, X2: {2} Y2: {3}\n".format(self.figura[i].x1(),self.figura[i].y1(),self.figura[i].x2(),self.figura[i].y2())) # Escribe en la consola los datos de seleccion
                    self.figura[i].dibujarSeleccion(self.lienzoCanvas) # Metodo que dibuja la figura en las cordenadas pero con un color diferente, dando a entender que esta seleccionada
                    self.figuraSeleccionada = i # Se guarda el indice de la figura seleccionada
                    return 1 # Apenas se selecciona una figura, se sale de la funcion
            self.figuraSeleccionada = -1 # Si no es seleccionada ninguna figura  figuraSeleccionada tiene valor de -1
            return 0 # Si no es seleccionado nada se retorna 0

        if(self.boton == "mover"): # Si se va a mover el objeto
            if(self.figuraSeleccionada != -1): # Si hay ina figura seleccionada
                 self.figura[self.figuraSeleccionada].borrarFigura(self.lienzoCanvas) # Borra la figura del lienzo pintandola en blanco, esto para iniciar a moverla

        if(self.boton == "copiar"): # Si se va a copiar el objeto
            self.ultimaX = 0 # Se ponen en 0 las cordenadas finales
            self.ultimaY = 0 # Se ponen en 0 las cordenadas finales
               
    def dibujarFigura(self,event): # Paso 2  -----> de creacion de las figuras, este boceta las figuras con unas cordenadas iniciales ya dadas, varia en las finales, hasta que el usuario finalice
        if(self.boton == "punto"): # Si es un punto no hace nada, ya que un punto no se tiene que mover
            pass
        elif(self.boton == "linea"): # Si es una linea
            self.lienzoCanvas.create_line(self.primeraX,self.primeraY,event.x,event.y,fill=self.color) # Dibuja una linea con las cordenadas iniciales, y con las actuales del mouse
            self.lienzoCanvas.create_line(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY,fill="white") # Dibuja una linea de color blanco (borrando) con las cordenadas iniciales, y con el estado anterior del mouse
        elif(self.boton == "recta"): # Si es un rectangulo
            self.lienzoCanvas.create_rectangle(self.primeraX,self.primeraY,event.x,event.y,outline=self.color) # Dibuja un rectangulo con las cordenadas iniciales, y con las actuales del mouse
            self.lienzoCanvas.create_rectangle(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY,outline="white") # Dibuja un rectangulo de color blanco (borrando) con las cordenadas iniciales, y con el estado anterior del mouse
        elif(self.boton == "circulo"): # Si es un circulo
            self.lienzoCanvas.create_oval(self.primeraX,self.primeraY,event.x,event.y,outline=self.color) # Dibuja un circulo con las cordenadas iniciales, y con las actuales del mouse
            self.lienzoCanvas.create_oval(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY,outline="white") # Dibuja un circulo de color blanco (borrando) con las cordenadas iniciales, y con el estado anterior del mouse
        elif(self.boton == "trian"): # Si es un triangulo
            # Dibuja un triangulo rectangulo a partir de tres lineas
            self.lienzoCanvas.create_line(self.primeraX,self.primeraY,event.x,event.y,fill=self.color) # HIPOTENUSA  # Dibuja un triangulo con las cordenadas iniciales, y con las actuales del mouse
            self.lienzoCanvas.create_line(self.primeraX,self.primeraY,event.x,self.primeraY,fill=self.color) # BASE  # Dibuja un triangulo con las cordenadas iniciales, y con las actuales del mouse
            self.lienzoCanvas.create_line(event.x,self.primeraY,event.x,event.y,fill=self.color) # ALTURA # Dibuja un triangulo con las cordenadas iniciales, y con las actuales del mouse

            self.lienzoCanvas.create_line(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY,fill="white") # HIPOTENUSA # Dibuja un triangulo de color blanco (borrando) con las cordenadas iniciales, y con el estado anterior del mouse
            self.lienzoCanvas.create_line(self.primeraX,self.primeraY,self.ultimaX,self.primeraY,fill="white") # BASE  # Dibuja un triangulo de color blanco (borrando) con las cordenadas iniciales, y con el estado anterior del mouse
            self.lienzoCanvas.create_line(self.ultimaX,self.primeraY,self.ultimaX,self.ultimaY,fill="white") # ALTURA  # Dibuja un triangulo de color blanco (borrando) con las cordenadas iniciales, y con el estado anterior del mouse

        elif(self.boton == "texto"): # Si es un texto
            self.lienzoCanvas.create_text(event.x,event.y,text=self.textoUsuario,font=("Calibri",self.tamanoLetraUsuario),fill=self.colorTextoUsuario,anchor="nw") # Dibuja un texto con las cordenadas iniciales, y con las actuales del mouse y con el texto ingresado por el usuario anteriormente
            self.lienzoCanvas.create_rectangle(self.ultimaX,self.ultimaY,self.ultimaX+self.textoTamano.winfo_width(),self.ultimaY+self.textoTamano.winfo_height(),fill="white",outline="white") # Dibuja un rectangulo de color blanco (borrando) con las cordenadas iniciales y la "caja" delimitadora que encierra el texto
            import time # importamos la libreria time, de manera local, esto permite que solo puede ser usada dentro del if
            time.sleep(0.09) # Esperamos 90 ms para colorear la otra, esto con el fin de que se pueda apreciar por el usuario

        if(self.boton == "mover" or self.boton == "copiar"): # Si se va a copiar o a mover
            if(self.figuraSeleccionada != -1): # Si ya hay una figura previamente seleccionada
                if("Punto.Texto" not in str(type(self.figura[self.figuraSeleccionada]))): # Si el objeto seleccionado es diferente de un texto
                    self.figura[self.figuraSeleccionada].dibujarMovido(self.lienzoCanvas,event.x,event.y,self.figura[self.figuraSeleccionada].co()) # Accede al metodo dibujarMovido que dibuja la figura con caracteristicas iguales, pero trasladada a nuevas coordenadas
                    self.figura[self.figuraSeleccionada].dibujarMovido(self.lienzoCanvas,self.ultimaX,self.ultimaY,"white") # Dibjua la figura de color blanco (borrando)
                else: # Si es un texto 
                    self.figura[self.figuraSeleccionada].dibujarMovido(self.lienzoCanvas,event.x,event.y,self.color) # Accede al metodo dibujarMovido que dibuja la figura con caracteristicas iguales, pero trasladada a nuevas coordenadas
                    self.figura[self.figuraSeleccionada].dibujarMovidoRectangulo(self.lienzoCanvas,self.ultimaX,self.ultimaY,"white") # Dibjua la figura (rectangulo relleno) de color blanco (borrando)
                    import time # importamos la libreria time, de manera local, esto permite que solo puede ser usada dentro del if
                    time.sleep(0.09) # Esperamos 90 ms para colorear la otra, esto con el fin de que se pueda apreciar por el usuario

        # Como el evento genera un ciclo el cual no permite salir hasta que se deje presionar y mover, se deben actualizar las cordenadas del lienzo dentro del ciclo
        self.entryPosMoX.config(text=event.x) # Posicion x del mouse
        self.entryPosMoY.config(text=event.y) # Posicion y del mouse

        self.ultimaX = event.x # Almacena el estado anterior del mouse
        self.ultimaY = event.y # Almacena el estado anterior del mouse

    def crearFigura(self,event):  # Paso 3  -----> de creacion de las figuras, crea el objeto con las cordenadas iniciales almacenadas en el paso 1, y con las cordenadas finales donde el mouse se levanta
        if(self.boton == "copiar"): # Si se copia
            if(self.figuraSeleccionada != -1): # Si hay una figura seleccionada
                self.primeraX = event.x # Almacena las cordenadas iniciales como las ultimas de la interaccion
                self.primeraY = event.y # Almacena las cordenadas iniciales como las ultimas de la interaccion
              
                self.ultimaX,self.ultimaY = self.figura[self.figuraSeleccionada].dibujarMovido(self.lienzoCanvas,event.x,event.y,self.color) # Almacena las ultimas dos cordenas del valor de retonro que da dibujar movido, para ver los valores mirar Punto.py

                # Guarda en self.boton el valor del tipo de objeto que esta seleccionado
                if("Punto.Punto" in str(type(self.figura[self.figuraSeleccionada]))):
                    self.boton = "punto"
                elif("Punto.Linea" in str(type(self.figura[self.figuraSeleccionada]))):
                    self.boton = "linea"
                elif("Punto.Rectangulo" in str(type(self.figura[self.figuraSeleccionada]))):
                    self.boton = "recta"
                elif("Punto.Circulo" in str(type(self.figura[self.figuraSeleccionada]))):
                    self.boton = "circulo"
                elif("Punto.Triangulo" in str(type(self.figura[self.figuraSeleccionada]))):
                    self.boton = "trian"
                elif("Punto.Texto" in str(type(self.figura[self.figuraSeleccionada]))):
                    self.boton = "texto"
                self.figuraSeleccionada = -1

        if(self.boton == "punto"): # Si es un punto
            self.consola.insert(END, "punto creado en X1: {0}, Y1: {1}, X2: {2} Y2: {3}\n".format(self.primeraX,self.primeraY,self.primeraX,self.primeraY)) # Escribe en la consola los datos del punto que se creo
            self.figura.append(Punto.Punto(self.primeraX,self.primeraY,self.primeraX+5,self.primeraY+5,self.color,self.contadorFiguras)) # instancia un nuevo punto en la lista con los datos recogidos anteriormente
            self.figura[self.contadorFiguras].dibujar(self.lienzoCanvas) # dibuja el objeto en el lienzo con el metodo dibujar
            if(self.boton not in self.dictFiguras.keys()): self.dictFiguras[self.boton] = [self.contadorFiguras] # Crea un diccionario con clave el objeto y como valor el indice con el cual fue creado
            else: self.dictFiguras[self.boton].append(self.contadorFiguras)
            self.contadorFiguras +=1 # Se incrementa el contador de figura en 1, indicando que se creo una nueva
        elif(self.boton == "linea"): # Si es una linea
            self.consola.insert(END, "Linea creada en X1: {0}, Y1: {1}, X2: {2} Y2: {3}\n".format(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY)) # Escribe en la consola los datos de la linea que se creo
            self.figura.append(Punto.Linea(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY,self.color,self.contadorFiguras)) # instancia una nueva linea en la lista con los datos recogidos anteriormente
            self.figura[self.contadorFiguras].dibujar(self.lienzoCanvas) # dibuja el objeto en el lienzo con el metodo dibujar
            if(self.boton not in self.dictFiguras.keys()): self.dictFiguras[self.boton] = [self.contadorFiguras] # Crea un diccionario con clave el objeto y como valor el indice con el cual fue creado
            else: self.dictFiguras[self.boton].append(self.contadorFiguras)
            self.contadorFiguras +=1 # Se incrementa el contador de figura en 1, indicando que se creo una nueva
        elif(self.boton == "recta"): # Si es un rectangulo
            self.consola.insert(END, "Rectangulo creado en X1: {0}, Y1: {1}, X2: {2} Y2: {3}\n".format(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY)) # Escribe en la consola los datos del rectangulo que se creo
            self.figura.append(Punto.Rectangulo(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY,self.color,self.contadorFiguras)) # instancia un nuevo rectangulo en la lista con los datos recogidos anteriormente
            self.figura[self.contadorFiguras].dibujar(self.lienzoCanvas) # dibuja el objeto en el lienzo con el metodo dibujar
            if(self.boton not in self.dictFiguras.keys()): self.dictFiguras[self.boton] = [self.contadorFiguras] # Crea un diccionario con clave el objeto y como valor el indice con el cual fue creado
            else: self.dictFiguras[self.boton].append(self.contadorFiguras)
            self.contadorFiguras +=1 # Se incrementa el contador de figura en 1, indicando que se creo una nueva
        elif(self.boton == "circulo"): # Si es un circulo
            self.consola.insert(END, "Circulo creado en X1: {0}, Y1: {1}, X2: {2} Y2: {3}\n".format(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY)) # Escribe en la consola los datos del circulo que se creo
            self.figura.append(Punto.Circulo(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY,self.color,self.contadorFiguras)) # instancia un nuevo circulo en la lista con los datos recogidos anteriormente
            self.figura[self.contadorFiguras].dibujar(self.lienzoCanvas) # dibuja el objeto en el lienzo con el metodo dibujar
            if(self.boton not in self.dictFiguras.keys()): self.dictFiguras[self.boton] = [self.contadorFiguras] # Crea un diccionario con clave el objeto y como valor el indice con el cual fue creado
            else: self.dictFiguras[self.boton].append(self.contadorFiguras)
            self.contadorFiguras +=1 # Se incrementa el contador de figura en 1, indicando que se creo una nueva
        elif(self.boton == "trian"): # Si es un triangulo
            self.consola.insert(END, "Triangulo creado en X1: {0}, Y1: {1}, X2: {2} Y2: {3}\n".format(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY)) # Escribe en la consola los datos del triangulo que se creo
            self.figura.append(Punto.Triangulo(self.primeraX,self.primeraY,self.ultimaX,self.ultimaY,self.color,self.contadorFiguras)) # instancia un nuevo triangulo en la lista con los datos recogidos anteriormente
            self.figura[self.contadorFiguras].dibujar(self.lienzoCanvas) # dibuja el objeto en el lienzo con el metodo dibujar
            if(self.boton not in self.dictFiguras.keys()): self.dictFiguras[self.boton] = [self.contadorFiguras] # Crea un diccionario con clave el objeto y como valor el indice con el cual fue creado
            else: self.dictFiguras[self.boton].append(self.contadorFiguras)
            self.contadorFiguras +=1 # Se incrementa el contador de figura en 1, indicando que se creo una nueva
        elif(self.boton == "texto"): # Si es un texto
            self.consola.insert(END, "Texto creado en X1: {0}, Y1: {1}\n".format(self.ultimaX,self.ultimaY)) # Escribe en la consola los datos del texto que se creo
            self.figura.append(Punto.Texto(self.ultimaX,self.ultimaY,self.textoUsuario,self.tamanoLetraUsuario,self.ultimaX+self.textoTamano.winfo_width(),self.ultimaY+self.textoTamano.winfo_height(),self.colorTextoUsuario,self.contadorFiguras)) # instancia un nuevo texto en la lista con los datos recogidos anteriormente
            self.figura[self.contadorFiguras].dibujar(self.lienzoCanvas) # dibuja el objeto en el lienzo con el metodo dibujar
            if(self.boton not in self.dictFiguras.keys()): self.dictFiguras[self.boton] = [self.contadorFiguras] # Crea un diccionario con clave el objeto y como valor el indice con el cual fue creado
            else: self.dictFiguras[self.boton].append(self.contadorFiguras)
            self.contadorFiguras +=1 # Se incrementa el contador de figura en 1, indicando que se creo una nueva          

        if(self.boton != "seleccion" and self.boton != "mover" and self.boton != "copiar" and self.boton != "borrar"): # Si se esta creando una figura
           self.dibujarTodo() # Dibujar todos los objetos en el lienzo nuevamente

        if(self.boton == "mover"): # Si se va mover
            if(self.figuraSeleccionada != -1): # Si hay una figura seleccionada
                self.figura[self.figuraSeleccionada].moverObjeto(event.x,event.y) # Cambia los atributos del objeto, esto para mover el objeto
                self.figura[self.figuraSeleccionada].dibujar(self.lienzoCanvas) # Dibuja el objeto con los nuevos atributos
                self.dibujarTodo() # Dibujar todos los objetos en el lienzo nuevamente
                self.figuraSeleccionada = -1 # Deselecciona el objeto seleccionado anteriormente

        self.borrarTodosLosCampos() # Borra todos los entry de las cordenadas luego de crear una figura

        self.ventana.config(cursor="hand2") # Cambia el cursor a modo seleccionar
        self.boton = "seleccion" # Selecciona como boton el de seleccionar, siempre se va a usar seleccionar cuando se termine de hacer cualquier cosa
        self.entryLargo.config(state="readonly") # Desactiva el entry para la cordenada x1
        self.entryAncho.config(state="readonly") # Desactiva el entry para la cordenada y1

    def dibujarTodo(self): # Metodo que dibuja todos los elementos de nuevo en el lienzo
        self.lienzoCanvas.delete("all") # Borra todo antes de la creacion, esto para evitar la saturacion de la aplicacion
        for x in self.dictFiguras.keys(): # Bucle que recorre las claves del diccionario, es decir, (punto,circulo,linea,etc)
                if(x == "punto"): # Si la clave es un punto
                    for i in self.dictFiguras[x]: # i toma los valores de los indices que son un punto
                        self.lienzoCanvas.create_oval(self.figura[i].x1(),self.figura[i].y1(),self.figura[i].x2(),self.figura[i].y2(),fill=self.figura[i].co()) # crea la figura con los datos que tiene el objeto[i]

                elif(x == "linea"): # Si la clave es una linea
                    for i in self.dictFiguras[x]: # i toma los valores de los indices que son una linea
                        self.lienzoCanvas.create_line(self.figura[i].x1(),self.figura[i].y1(),self.figura[i].x2(),self.figura[i].y2(),fill=self.figura[i].co()) # crea la figura con los datos que tiene el objeto[i]

                elif(x == "recta"): # Si la clave es un rectangulo
                    for i in self.dictFiguras[x]: # i toma los valores de los indices que son un rectangulo
                        self.lienzoCanvas.create_rectangle(self.figura[i].x1(),self.figura[i].y1(),self.figura[i].x2(),self.figura[i].y2(),outline=self.figura[i].co()) # crea la figura con los datos que tiene el objeto[i]

                elif(x == "circulo"): # Si la clave es un circulo
                    for i in self.dictFiguras[x]: # i toma los valores de los indices que son un circulo
                        self.lienzoCanvas.create_oval(self.figura[i].x1(),self.figura[i].y1(),self.figura[i].x2(),self.figura[i].y2(),outline=self.figura[i].co()) # crea la figura con los datos que tiene el objeto[i]

                elif(x == "trian"): # Si la clave es un triangulo
                    for i in self.dictFiguras[x]: # i toma los valores de los indices que son un triangulo
                        self.lienzoCanvas.create_line(self.figura[i].x1(),self.figura[i].y1(),self.figura[i].x2(),self.figura[i].y2(),fill=self.figura[i].co()) # HIPOTENUSA # crea la figura con los datos que tiene el objeto[i]
                        self.lienzoCanvas.create_line(self.figura[i].x1(),self.figura[i].y1(),self.figura[i].x2(),self.figura[i].y1(),fill=self.figura[i].co()) # BASE # crea la figura con los datos que tiene el objeto[i]
                        self.lienzoCanvas.create_line(self.figura[i].x2(),self.figura[i].y1(),self.figura[i].x2(),self.figura[i].y2(),fill=self.figura[i].co()) # ALTURA # crea la figura con los datos que tiene el objeto[i]
                elif(x == "texto"): # Si la clave es un texto
                    for i in self.dictFiguras[x]: # i toma los valores de los indices que son un texto
                        self.lienzoCanvas.create_text(self.figura[i].x1(),self.figura[i].y1(),text=self.figura[i].tex(),font=("Calibri", self.figura[i].ttex()),fill=self.figura[i].co(),anchor="nw") # crea la figura con los datos que tiene el objeto[i]
    # ---------------------------------------- FIN DE CREACION DE FIGURAS -------------------------------------------------

def main():  # Funcion principal de la aplicacion
    ventanaDrawA = Tk() # Crea la ventana Tk() de la aplicacion
    app = Aplicacion(ventanaDrawA) # Instanciamos un objeto tipo aplicaion, recibe como parametros la ventana principal de la aplicacion

    ventanaDrawA.mainloop() # Bucle de tkinter

main() # ejecutamos la funcion