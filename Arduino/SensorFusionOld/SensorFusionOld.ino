#include <SoftwareSerial.h>
#include <TinyGPS.h>
#include<Wire.h>
const int MPU_addr=0x68;  // I2C address of the MPU-6050
int16_t AcX,AcY,AcZ;

SoftwareSerial serialGPS(10,9);
TinyGPS gps;
void printFloat(double f, int digits = 2);
void setup() {
  //Accelerometer
  Wire.begin();
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x6B);  // PWR_MGMT_1 register
  Wire.write(0);     // set to zero (wakes up the MPU-6050)
  Wire.endTransmission(true);
  //Raspberry
  Serial.begin(9600);
  //GPS
  serialGPS.begin(9600);
  //delay(1000);
  Serial.println("Starting acquiring data");
  

}

void loop() {
  
  //Accelerometer
  Wire.beginTransmission(MPU_addr);
  Wire.write(0x3B);  // starting with register 0x3B (ACCEL_XOUT_H)
  Wire.endTransmission(false);
  Wire.requestFrom(MPU_addr,14,true);  // request a total of 14 registers
  AcX=Wire.read()<<8|Wire.read();  // 0x3B (ACCEL_XOUT_H) & 0x3C (ACCEL_XOUT_L)    
  AcY=Wire.read()<<8|Wire.read();  // 0x3D (ACCEL_YOUT_H) & 0x3E (ACCEL_YOUT_L)
  AcZ=Wire.read()<<8|Wire.read();  // 0x3F (ACCEL_ZOUT_H) & 0x40 (ACCEL_ZOUT_L)

  
  //GPS
  bool newdataGPS = false;
  
  if (serialGPS.available()){
    char c = serialGPS.read();
    if (gps.encode(c)){
      newdataGPS = true;
    }
  }

  
  if(newdataGPS){
    delay(3000);
    Serial.print("*********************GPS: ");
    float flat, flon;
    unsigned long age, date, time;
    gps.f_get_position(&flat, &flon, &age);
    printFloat(flat, 5); Serial.print(" "); printFloat(flon, 5);
    gps.get_datetime(&date, &time, &age);
    Serial.print(date); 
    Serial.print(" ");
    Serial.print(time);
    Serial.println(" ");
  }
  Serial.print("Accelerometer: ");
  Serial.print(AcX);
  Serial.print(" ");
  Serial.print(AcY);
  Serial.print(" ");
  Serial.print(AcZ);
  Serial.println(" ");
  /*else{
   Serial.println("A"); 
   delay(3000);
  }*/
    /*
  
    delay(1000);*/
  
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
