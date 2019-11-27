from tkinter import *
import math

class Figura():
    def __init__(self,corX,corY,finX,finY,colo,id):
        self.x = corX
        self.y = corY

        self.fX = finX
        self.fY = finY

        self.color = colo
        self.id = id

    def moverObjeto(self,corX,corY):
        self.fX = self.fX-self.x+corX
        self.fY = self.fY-self.y+corY

        self.x = corX
        self.y = corY

    def borrarObjeto(self):
        self.fX = 0
        self.fY = 0

        self.x = 0
        self.y = 0

    def x1(self):
        return self.x

    def y1(self):
        return self.y

    def x2(self):
        return self.fX

    def y2(self):
        return self.fY

    def co(self):
        return self.color
    def num(self):
        return self.id

    def ordenarCordenadas(self):

        if((self.x<=self.fX) and (self.y>self.fY)):
            yy = self.y
            self.y = self.fY
            self.fY = yy
        elif((self.x>self.fX) and (self.y<=self.fY)):
            xx = self.x
            self.x = self.fX
            self.fX = xx
        elif((self.x>self.fX) and (self.y>self.fY)):
            yy = self.y
            self.y = self.fY
            self.fY = yy      
       
            xx = self.x
            self.x = self.fX
            self.fX = xx


class Punto(Figura):
    def dibujar(self,lienzo):
        lienzo.create_oval(self.x,self.y,self.x+5,self.y+5,fill=self.color,tag="punto"+str(self.id))

    def seleccionar(self,corX,corY):
        print("Se presiono en: X:{0} y en Y:{1} ||| objeto en X1: {2} y X2:{3}".format(corX,corY,self.x,self.y))
        self.tolerancia = 2
        if (corX >= self.x-self.tolerancia and corX <= self.fX+self.tolerancia):
            if((corY >= self.y-self.tolerancia and corY <= self.y+self.tolerancia)  or (corY >= self.fY-self.tolerancia and corY <= self.fY+self.tolerancia)):
                return True
    def dibujarSeleccion(self,lienzo):
        lienzo.create_oval(self.x,self.y,self.x+5,self.y+5,fill="tan2",tag="seleccion")

    def dibujarMovido(self,lienzo,corX,corY,color):
        lienzo.create_oval(corX,corY,corX+5,corY+5,fill=color,outline="white",tag="mover")
        return (corX+5,corY+5)

    def borrarFigura(self,lienzo):
         lienzo.create_oval(self.x,self.y,self.x+5,self.y+5,fill="white",outline="white")
         lienzo.delete("seleccion")


class Rectangulo(Figura):
    def dibujar(self,lienzo):
        self.ordenarCordenadas()
        lienzo.create_rectangle(self.x,self.y,self.fX,self.fY,outline=self.color,tag="rectangulo"+str(self.id))

    def dibujarMovido(self,lienzo,corX,corY,color):
        lienzo.create_rectangle(corX,corY,self.fX-self.x+corX,self.fY-self.y+corY,outline=color,tag="mover")
        return (self.fX-self.x+corX,self.fY-self.y+corY)

    def borrarFigura(self,lienzo):
        lienzo.create_rectangle(self.x,self.y,self.fX,self.fY,outline="white")
        lienzo.delete("seleccion")

    def seleccionar(self,corX,corY):
        print("Se presiono en: X:{0} y en Y:{1} ||| objeto en X1: {2} y X2:{3}".format(corX,corY,self.x,self.y))
        self.tolerancia = 2
        if (corX >= self.x and corX <= self.fX):
            if((corY >= self.y-self.tolerancia and corY <= self.y+self.tolerancia)  or (corY >= self.fY-self.tolerancia and corY <= self.fY+self.tolerancia)):
                return True
        elif(corY >= self.y and corY <= self.fY):
            if((corX >= self.x-self.tolerancia and corX <= self.x+self.tolerancia)  or (corX >= self.fX-self.tolerancia and corX <= self.fX+self.tolerancia)):
                return True

    def dibujarSeleccion(self,lienzo):
        lienzo.create_rectangle(self.x,self.y,self.fX,self.fY,outline="tan2",tag="seleccion")

class Linea(Figura):
    def dibujar(self,lienzo):
        lienzo.create_line(self.x,self.y,self.fX,self.fY,fill=self.color,tag="linea"+str(self.id))

    def seleccionar(self,corX,corY):
        print("Se presiono en: X:{0} y en Y:{1} ||| objeto en X1: {2} y X2:{3}".format(corX,corY,self.x,self.y))
        self.tolerancia = 2
        rectaNoDefinida = False
        try:
           self.mOriginal = (self.fY - self.y) / (self.fX - self.x)
        except:
            rectaNoDefinida = True

        try:
            self.mClick = (corY - self.y) / (corX - self.x)
        except:
            if(rectaNoDefinida):
                if (corX >= self.x-self.tolerancia and corX <= self.fX+self.tolerancia):
                    return True
                elif (corX >= self.fX-self.tolerancia and corX <= self.x+self.tolerancia):
                    return True

        if(not rectaNoDefinida):
            self.bOriginal = self.y - (self.mOriginal*self.x)
            self.bClick = corY - (self.mClick*corX)

            self.rectaOriginal = (self.mOriginal*corX)+self.bOriginal
            self.rectaClick = (self.mClick*corX)+self.bClick


            if (corX >= self.x-self.tolerancia and corX <= self.fX+self.tolerancia):
                if(self.rectaClick >= self.rectaOriginal-self.tolerancia and self.rectaClick <= self.rectaOriginal+self.tolerancia):
                    return True

            elif (corX >= self.fX-self.tolerancia and corX <= self.x+self.tolerancia):
                if(self.rectaClick >= self.rectaOriginal-self.tolerancia and self.rectaClick <= self.rectaOriginal+self.tolerancia):
                    return True

    def dibujarSeleccion(self,lienzo):
        lienzo.create_line(self.x,self.y,self.fX,self.fY,fill="tan2",tag="seleccion")

    def dibujarMovido(self,lienzo,corX,corY,color):
        lienzo.create_line(corX,corY,self.fX-self.x+corX,self.fY-self.y+corY,fill=color,tag="mover")
        return (self.fX-self.x+corX,self.fY-self.y+corY)

    def borrarFigura(self,lienzo):
         lienzo.create_line(self.x,self.y,self.fX,self.fY,fill="white") 
         lienzo.delete("seleccion")

class Circulo(Figura):
    def dibujar(self,lienzo):
        self.ordenarCordenadas()
        lienzo.create_oval(self.x,self.y,self.fX,self.fY,outline=self.color,tag="circulo"+str(self.id))

    def hallarDistancia(self,xy,ff):
        return math.sqrt((xy[0] - ff[0])**2 + (xy[1] - ff[1])**2)

    def seleccionar(self,corX,corY):
        print("Se presiono en: X:{0} y en Y:{1} ||| objeto en X1: {2} y X2:{3}".format(corX,corY,self.x,self.y))
        self.tolerancia = 2

        a = abs(self.fX - self.x)/2
        b = abs(self.fY - self.y)/2

        dictCordenadas = {}
        dictCordenadas["centro"] = (self.x+(abs((self.fX-self.x)/2)),self.y+(abs((self.fY-self.y)/2)))

        constante = 0

        if(a >= b): # Elipse horizontal
            c = math.sqrt((a**2)-(b**2))

            dictCordenadas["verticeA"] = (dictCordenadas["centro"][0]+a,dictCordenadas["centro"][1])
            dictCordenadas["verticeA'"] = (dictCordenadas["centro"][0]-a,dictCordenadas["centro"][1])
            dictCordenadas["foco"] = (dictCordenadas["centro"][0]+c,dictCordenadas["centro"][1])
            dictCordenadas["foco'"] = (dictCordenadas["centro"][0]-c,dictCordenadas["centro"][1])
            constante = (self.hallarDistancia(dictCordenadas["verticeA"],dictCordenadas["foco"]) + self.hallarDistancia(dictCordenadas["verticeA"],dictCordenadas["foco'"]))
        else: # Elipse vertical
            c = math.sqrt((b**2)-(a**2))

            dictCordenadas["verticeB"] = (dictCordenadas["centro"][0],dictCordenadas["centro"][1]+b)
            dictCordenadas["verticeB'"] = (dictCordenadas["centro"][0],dictCordenadas["centro"][1]-b)
            dictCordenadas["foco"] = (dictCordenadas["centro"][0],dictCordenadas["centro"][1]+c)
            dictCordenadas["foco'"] = (dictCordenadas["centro"][0],dictCordenadas["centro"][1]-c)
            constante = (self.hallarDistancia(dictCordenadas["verticeB"],dictCordenadas["foco"]) + self.hallarDistancia(dictCordenadas["verticeB"],dictCordenadas["foco'"]))

        valorDelClick = (self.hallarDistancia((corX,corY),dictCordenadas["foco"]) + self.hallarDistancia((corX,corY),dictCordenadas["foco'"]))
    
        if(valorDelClick >= constante-self.tolerancia and valorDelClick <= constante+self.tolerancia):
             return True

    def dibujarSeleccion(self,lienzo):
        lienzo.create_oval(self.x,self.y,self.fX,self.fY,outline="tan2",tag="seleccion")

    def dibujarMovido(self,lienzo,corX,corY,color):
        lienzo.create_oval(corX,corY,self.fX-self.x+corX,self.fY-self.y+corY,outline=color,tag="mover")
        return (self.fX-self.x+corX,self.fY-self.y+corY)

    def borrarFigura(self,lienzo):
         lienzo.create_oval(self.x,self.y,self.fX,self.fY,outline="white")
         lienzo.delete("seleccion")

class Triangulo(Figura):
    def dibujar(self,lienzo):
        lienzo.create_line(self.x,self.y,self.fX,self.fY,fill=self.color,tag="triangulo"+str(self.id)) # HIPOTENUSA
        lienzo.create_line(self.x,self.y,self.fX,self.y,fill=self.color,tag="triangulo"+str(self.id)) # BASE
        lienzo.create_line(self.fX,self.y,self.fX,self.fY,fill=self.color,tag="triangulo"+str(self.id)) # ALTURA

        self.listaLineasTriangulo = [(self.x,self.y,self.fX,self.fY), (self.x,self.y,self.fX,self.y), (self.fX,self.y,self.fX,self.fY)]

    def seleccionar(self,corX,corY):
        print("Se presiono en: X:{0} y en Y:{1} ||| objeto en X1: {2} y X2:{3}".format(corX,corY,self.x,self.y))
        self.tolerancia = 2
        for i in range(3):
            rectaNoDefinida = False
            try:
               self.mOriginal = (self.listaLineasTriangulo[i][3] - self.listaLineasTriangulo[i][1]) / (self.listaLineasTriangulo[i][2] - self.listaLineasTriangulo[i][0])
            except:
                rectaNoDefinida = True

            try:
                self.mClick = (corY - self.listaLineasTriangulo[i][1]) / (corX - self.listaLineasTriangulo[i][0])
            except:
                if(rectaNoDefinida):
                    if (corX >= self.listaLineasTriangulo[i][0]-self.tolerancia and corX <= self.listaLineasTriangulo[i][2]+self.tolerancia):
                        return True
                    elif (corX >= self.listaLineasTriangulo[i][2]-self.tolerancia and corX <= self.listaLineasTriangulo[i][0]+self.tolerancia):
                        return True

            if(not rectaNoDefinida):
                self.bOriginal = self.listaLineasTriangulo[i][1] - (self.mOriginal*self.listaLineasTriangulo[i][0])
                self.bClick = corY - (self.mClick*corX)

                self.rectaOriginal = (self.mOriginal*corX)+self.bOriginal
                self.rectaClick = (self.mClick*corX)+self.bClick


                if (corX >= self.listaLineasTriangulo[i][0]-self.tolerancia and corX <= self.listaLineasTriangulo[i][2]+self.tolerancia):
                    if(self.rectaClick >= self.rectaOriginal-self.tolerancia and self.rectaClick <= self.rectaOriginal+self.tolerancia):
                        return True

                elif (corX >= self.listaLineasTriangulo[i][2]-self.tolerancia and corX <= self.listaLineasTriangulo[i][0]+self.tolerancia):
                    if(self.rectaClick >= self.rectaOriginal-self.tolerancia and self.rectaClick <= self.rectaOriginal+self.tolerancia):
                        return True

    def dibujarSeleccion(self,lienzo):
        lienzo.create_line(self.x,self.y,self.fX,self.fY,fill="tan2",tag="seleccion") # HIPOTENUSA
        lienzo.create_line(self.x,self.y,self.fX,self.y,fill="tan2",tag="seleccion") # BASE
        lienzo.create_line(self.fX,self.y,self.fX,self.fY,fill="tan2",tag="seleccion") # ALTURA

    def dibujarMovido(self,lienzo,corX,corY,color):
        lienzo.create_line(corX,corY,self.fX-self.x+corX,self.fY-self.y+corY,fill=color,tag="mover")
        lienzo.create_line(corX,corY,self.fX-self.x+corX,corY,fill=color,tag="mover")
        lienzo.create_line(self.fX-self.x+corX,corY,self.fX-self.x+corX,self.fY-self.y+corY,fill=color,tag="mover")
        return (self.fX-self.x+corX,self.fY-self.y+corY)

    def borrarFigura(self,lienzo):
        lienzo.create_line(self.x,self.y,self.fX,self.fY,fill="white") # HIPOTENUSA
        lienzo.create_line(self.x,self.y,self.fX,self.y,fill="white") # BASE
        lienzo.create_line(self.fX,self.y,self.fX,self.fY,fill="white") # ALTURA

        lienzo.delete("seleccion")

class Texto(Figura):
    def __init__(self,corX,corY,texto,tLetra,rFinX,rFinY,colo,id):
        self.x = corX
        self.y = corY

        self.fX = rFinX
        self.fY = rFinY

        self.texto = texto
        self.tLetra = tLetra

        self.color = colo
        self.id = id

    def dibujar(self,lienzo):
        lienzo.create_text(self.x,self.y,text=self.texto,font=("Courier New",self.tLetra),fill=self.color,anchor="nw",tag="texto"+str(self.id))

    def seleccionar(self,corX,corY):
        print("Se presiono en: X:{0} y en Y:{1} ||| objeto en X1: {2} y X2:{3}".format(corX,corY,self.x,self.y))
        self.tolerancia = 2

        if (corX >= self.x and corX <= self.fX):
            if((corY >= self.y and corY <= self.fY)):
                return True

    def dibujarSeleccion(self,lienzo):
        lienzo.create_text(self.x,self.y,text=self.texto,font=("Courier New",self.tLetra),fill="tan2",anchor="nw",tag="seleccion")

    def tex(self):
        return self.texto
    def ttex(self):
        return self.tLetra

    def dibujarMovido(self,lienzo,corX,corY,color):
        lienzo.create_text(corX,corY,text=self.texto,font=("Courier New",self.tLetra),fill=self.color,anchor="nw",tag="mover")
        return(corX,corY)

    def dibujarMovidoRectangulo(self,lienzo,corX,corY,color):
        lienzo.create_rectangle(corX,corY,self.fX-self.x+corX,self.fY-self.y+corY,fill=color,outline=color,tag="mover")

    def borrarFigura(self,lienzo):
         lienzo.create_rectangle(self.x,self.y,self.fX,self.fY,fill="white",outline="white")
         lienzo.delete("seleccion")

    def borrarObjeto(self):
        self.fX = 0
        self.fY = 0

        self.x = 0
        self.y = 0

        self.texto = ""
        self.tLetra = 12

class Evento():
    def __init__(self, corX,corY):
        self.x = corX
        self.y = corY



