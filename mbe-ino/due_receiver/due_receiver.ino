#include <DueTimer.h>
#include <Arduino.h>

#define PPS_PIN 5

#define SENSOR_PIN0 A0
#define SENSOR_PIN1 A1
#define SENSOR_PIN2 A2
#define SENSOR_PIN3 A3
#define INT2POINTER(a) ((char*)(intptr_t)(a))

int sensor_read0 = 0;
int sensor_read1 = 0;
int sensor_read2 = 0;
int sensor_read3 = 0;
int acc = 0;

long int last_pps = 0;

void setup() {
  SerialUSB.begin(500000);
  while (!SerialUSB) {
    continue;
  }

  pinMode(PPS_PIN, INPUT);
  attachInterrupt(digitalPinToInterrupt(PPS_PIN), pps_isr, RISING);
  __enable_irq();
  
  Timer3.attachInterrupt(periodic_sensor_readings);
  Timer3.start(625); // 1600Hz
}

void loop() {
  // put your main code here, to run repeatedly:
  delay(1000);
}

void pps_isr() {
  last_pps = micros();
  char bigString[20];     /* I never know how much to allocate... */
  char *p = bigString;
  bigString[0] = '\0';
  char delay_str[18];
  sprintf(delay_str, "%12ld", last_pps);
  p = mystrcat(p, delay_str);
  p = mystrcat(p, "\r\n");
  SerialUSB.print("SY");
  SerialUSB.print(bigString);
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
  sensor_read0 = analogRead(SENSOR_PIN0);
  sensor_read1 = analogRead(SENSOR_PIN1);
  sensor_read2 = analogRead(SENSOR_PIN2);
  sensor_read3 = analogRead(SENSOR_PIN3);
  
  char sensor_str0[5];
  sprintf(sensor_str0, "%05d", sensor_read0);
  
  char sensor_str1[5];
  sprintf(sensor_str1, "%05d", sensor_read1);
  
  char sensor_str2[5];
  sprintf(sensor_str2, "%05d", sensor_read2);
  
  char sensor_str3[5];
  sprintf(sensor_str3, "%05d", sensor_read3);
  
  char *separator = ",";
  
  if (sensor_read1) {

    SerialUSB.print("CA");
    
    p = mystrcat(p, sensor_str0);
    p = mystrcat(p, separator);
    
    p = mystrcat(p, sensor_str1);
    p = mystrcat(p, separator);
    
    p = mystrcat(p, sensor_str2);
    p = mystrcat(p, separator);
    
    p = mystrcat(p, sensor_str3);
    p = mystrcat(p, separator);
    
    char delay_str[100];

    if (last_pps != 0) {
      sprintf(delay_str, "%12ld", (micros()-last_pps));
    } else {
      sprintf(delay_str, "%12ld", (-micros()));
    }
    p = mystrcat(p, delay_str);
    p = mystrcat(p, "\r\n");
    SerialUSB.print(bigString);
  }
}
