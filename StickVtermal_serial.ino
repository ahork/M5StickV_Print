#include <M5Stack.h>
#include "Adafruit_Thermal.h"


Adafruit_Thermal printer(&Serial2);     // Pass addr to printer constructor

 
void setup()
{
    M5.begin(true, true, true);
  
    M5.Lcd.fillScreen(BLACK);
    M5.Lcd.setCursor(0, 0);
    M5.Lcd.println("GO");
    
    // Connect M5Stack
    // vert 2 jaune 5 Noir gnd
    Serial2.begin(19200, SERIAL_8N1, 2, 5);
    printer.begin();    
    Serial1.begin(115200,SERIAL_8N1 ,21,22);
    printer.println(F("Start"));
}


void loop()
{
M5.update();

    if (M5.BtnA.wasReleased()) 
        {          
          M5.Lcd.fillScreen(BLACK);
          M5.Lcd.setCursor(0, 0);
          M5.Lcd.print('A');
          Serial1.print('/');
        }
        
     
    if(Serial1.available()> 0)
    {
      String str = Serial1.readString();
      M5.Lcd.println(str); 
        
      uint8_t dataArray[400];
      char string[400*4+1];
      
      str.toCharArray(string, 400*4+1);
      Serial.print("ch:");
      Serial.println(string);
      Serial.println("****************");
      char* ptr = strtok(string, ",");
        int i = 0;
        while(ptr != NULL) {         
          dataArray[i] = atol(ptr);
          i= i +1; 
        // create next part
        ptr = strtok(NULL, ",");
        }
 
       Serial.print("fin"); 
       Serial.println(i);               
      printer.printBitmap(320, 10, dataArray);    
            
    }
    
  
    
    

}
