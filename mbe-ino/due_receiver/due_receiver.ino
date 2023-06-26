#include <DueTimer.h>
#include <Arduino.h>

#define SENSOR_PIN A5
#define INT2POINTER(a) ((char*)(intptr_t)(a))

int sensor_read = 0;
int acc = 0;

void setup() {
  SerialUSB.begin(500000);

  while (!SerialUSB) {
    continue;
  }
  
  Timer3.attachInterrupt(periodic_sensor_readings);
  Timer3.start(625); // 1600Hz
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(1000);
}

char* mystrcat( char* dest, char* src )
{
     while (*dest) dest++;
     while (*dest++ = *src++);
     return --dest;
}

void periodic_sensor_readings() {
  long int init = micros();
  char bigString[100];     /* I never know how much to allocate... */
  char *p = bigString;
  bigString[0] = '\0';
  sensor_read = analogRead(SENSOR_PIN);
  char sensor_str[5];
  sprintf(sensor_str, "%d", sensor_read);
  char *separator = ",";
  
  if (sensor_read) {
    
    p = mystrcat(p, sensor_str);
    p = mystrcat(p, separator);
    
    p = mystrcat(p, sensor_str);
    p = mystrcat(p, separator);
    
    p = mystrcat(p, sensor_str);
    p = mystrcat(p, separator);
    
    p = mystrcat(p, sensor_str);
    p = mystrcat(p, separator);
    
    char delay_str[100];
    
    sprintf(delay_str, "%ld", (micros()-init));
    p = mystrcat(p, delay_str);
    p = mystrcat(p, "\r\n");
    SerialUSB.print(bigString);
  }
}
