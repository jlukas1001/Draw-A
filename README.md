# Draw-A

Programa que sirve como herramienta de diseño para la pantalla TFT táctil 2.4 de Arduino. En el lienzo se pueden dibujar diferentes figuras (círculos, rectángulos, triángulos) así como escribir texto, además, tiene herramientas como (copiar, pegar, mover, borrar, seleccionar), de esta manera, se genera un Código el cual es usado en Arduino para dibujar exactamente lo mismo que se dibujó en el lienzo en la pantalla, logrando así, unos diseños mejores y de manera más eficiente para los proyectos en Arduino con la pantalla táctil TFT 2.4.

Esta aplicación la he usado en todos mis proyectos con Arduino, ya que para la mayoría utilizo muchas pantallas en las que navega el usuario, esta idea surge debido a que perdía mucho tiempo moviendo cada pixel, compilando y viendo como quedaba, si no me gustaba tocaba repetir de nuevo el proceso, por lo que, en el diseño de las ventanas gastaba mucho tiempo, el cual, podría ser aprovechado en mejorar la parte lógica de la aplicación.

## Interfaz
![image](https://user-images.githubusercontent.com/56893753/142348819-1e405afc-b51e-465e-a1da-0f0fe18725dc.png)

## Prueba de funcionamiento

### Diseño de prueba
![image](https://user-images.githubusercontent.com/56893753/142348460-5206f33e-332d-4389-a09d-469d7dd18441.png)

### Codigo arrojado por la aplicacion

```
void disenoApp(){ 
    tft.drawRect(12,15,138,72,BLACK);
    tft.drawRect(12,138,138,72,BLACK);

    tft.drawLine(165,209,301,17,BLACK);
    tft.drawLine(165,209,301,209,BLACK);
    tft.drawLine(301,209,301,17,BLACK);

    tft.setCursor(28.0,41.0);
    tft.setTextSize(3.0);
    tft.setTextColor(BLACK);
    tft.println("INICIO");
    tft.setCursor(40.0,164.0);
    tft.setTextSize(3.0);
    tft.setTextColor(BLACK);
    tft.println("FINAL");
    tft.setCursor(231.0,198.0);
    tft.setTextSize(1.0);
    tft.setTextColor(BLACK);
    tft.println("BASE");
    tft.setCursor(240.0,118.0);
    tft.setTextSize(1.0);
    tft.setTextColor(BLACK);
    tft.println("ALTURA");
    tft.setCursor(172.0,67.0);
    tft.setTextSize(1.0);
    tft.setTextColor(BLACK);
    tft.println("HIPOTENUSA");
    tft.setCursor(163.0,5.0);
    tft.setTextSize(1.0);
    tft.setTextColor(BLACK);
    tft.println("H = SQRT(B**2 + A**2)");

    tft.drawLine(302,122,286,122,BLACK);
    tft.drawLine(287,115,287,131,BLACK);
    tft.drawLine(287,116,279,122,BLACK);
    tft.drawLine(280,122,287,130,BLACK);
    tft.drawLine(237,105,201,105,BLACK);
    tft.drawLine(202,106,202,84,BLACK);
    tft.drawLine(199,85,206,86,BLACK);
    tft.drawLine(207,86,203,80,BLACK);
    tft.drawLine(203,81,200,85,BLACK);
    tft.drawLine(2,3,5,1,BLACK);

}

```

### Visualizacion en pantalla de Arduino

![IMG_20191127_130447](https://user-images.githubusercontent.com/56893753/142349057-4db50f2b-043b-4d18-92d5-0552ba635182.jpg)

