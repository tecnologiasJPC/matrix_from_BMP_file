#include <Wire.h>                 //libreria para comunicacion I2C
#include <Adafruit_SSD1306.h>     //libreria para OLED
#include <Adafruit_GFX.h>         //libreria para graficar en pantalla OLED
#include "image_code.h"

#define SCREEN_WIDTH    128        // ancho de pantalla OLED en pixeles
#define SCREEN_HEIGHT   64         // alto de pantalla OLED en pixeles  
#define OLED128         0x3C       // direccion para pantalla OLED

// crea el objeto para la pantalla OLED
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

void testdrawbitmap(void) {
  display.clearDisplay();
  display.drawBitmap(
    (display.width()  - LOGO_WIDTH ) / 2,
    (display.height() - LOGO_HEIGHT) / 2,
    logo_bmp, LOGO_WIDTH, LOGO_HEIGHT, 1);
  display.display();
  delay(1000);
}

void setup() {
  Serial.begin(9600); // initialize serial communication at 9600 bits per second:
  while (!Serial);
  
   // inicializa la pantalla OLED
  if(!display.begin(SSD1306_SWITCHCAPVCC, OLED128)) {
    Serial.println(F("Failed to initialize OLED. Verify connections"));
    while (1);
  }
  display.clearDisplay();                 // comando para limpiar la pantalla OLED
  display.setTextSize(1);                 // Normal 1:1 pixel scale
  display.setTextColor(SSD1306_WHITE);    // write white text on OLED screen

  testdrawbitmap();    // Draw a small bitmap image
}

void loop() {
  // put your main code here, to run repeatedly:
}
