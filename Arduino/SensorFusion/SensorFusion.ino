
#include <SoftwareSerial.h>
#include <TinyGPS.h>
#include<Wire.h>
const int MPU_addr=0x68;  // I2C address of the MPU-6050
int16_t AcX,AcY,AcZ;

const int buttonPort = 13;
const int ledPort = 12;
boolean start = false;
int lastButtonVal = 0;

SoftwareSerial serialGPS(10,9);
TinyGPS gps;

void gpsdump(TinyGPS &gps);
void printFloat(double f, int digits = 2);

void setup()  
{
  Serial.begin(9600);
  serialGPS.begin(9600);
  delay(1000);
  Serial.println("Starting acquiring data...");
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true); 
  pinMode(buttonPort, INPUT);
  pinMode(ledPort, OUTPUT);
}

void loop() // run over and over
{
  
  int buttonVal = digitalRead(buttonPort);
  if(buttonVal == 1){
    if(buttonVal != lastButtonVal){
      if(start){
        Serial.println("STOP ");
      }else{
        Serial.println("START ");
      }
      start = !start;
    }
  }
  lastButtonVal = buttonVal;
  if(Serial.available()>0){
    Serial.print("Received: ");
    String response = getValue(Serial.readString(),' ',0);
    Serial.println(response);
    if(response == "START_OK"){
      digitalWrite(ledPort,1);
    }
    else if(response == "STOP_OK"){
      digitalWrite(ledPort,0);
    }
  }
  
  
  bool newdata = false;
  unsigned long start = millis();
  while (millis() - start < 50){
    if (serialGPS.available()) {
      char c = serialGPS.read();
      if (gps.encode(c)) {
        float flat, flon;
        unsigned long age, date, cur_time;
        gps.f_get_position(&flat, &flon, &age);
        //gps.get_datetime(&date, &cur_time, &age); per tempo dato da gps
        Serial.print("GPS: ");
        printFloat(flat, 5); 
        Serial.print(" "); 
        printFloat(flon, 5);
        Serial.print(" ");
        /*Serial.print(date);
        Serial.print(" ");
        Serial.println(cur_time);*/  //per tempo dato da gps
        Serial.println(millis());
      }
    }
  }
  
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_addr,14,true);  // request a total of 14 registers
  AcX=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)    
  AcY=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  AcZ=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)
  Serial.print("ACC: ");
  Serial.print(AcX);
  Serial.print(" ");
  Serial.print(AcY);
  Serial.print(" ");
  Serial.print(AcZ);
  Serial.print(" ");
  Serial.println(millis());

}


void printFloat(double number, int digits)
{
  // Handle negative numbers
  if (number < 0.0) 
  {
     Serial.print('-');
     number = -number;
  }

  // Round correctly so that print(1.999, 2) prints as "2.00"
  double rounding = 0.5;
  for (uint8_t i=0; i<digits; ++i)
    rounding /= 10.0;
  
  number += rounding;

  // Extract the integer part of the number and print it
  unsigned long int_part = (unsigned long)number;
  double remainder = number - (double)int_part;
  Serial.print(int_part);

  // Print the decimal point, but only if there are digits beyond
  if (digits > 0)
    Serial.print("."); 

  // Extract digits from the remainder one at a time
  while (digits-- > 0) 
  {
    remainder *= 10.0;
    int toPrint = int(remainder);
    Serial.print(toPrint);
    remainder -= toPrint;
  }
}

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;

  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }

  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}
