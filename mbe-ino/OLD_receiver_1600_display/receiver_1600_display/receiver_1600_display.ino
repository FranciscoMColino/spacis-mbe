#include <LiquidCrystal.h>

#define SENSOR_PIN A5

LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

int ledPin = 9;
int sensor_read = 0;
int acc = 0;

const uint16_t t1_load = 0;
const uint16_t t1_comp = 1250;
//const uint16_t t1_comp = 5000;

void reset_timer1(){ 
  //Reset Timer1 Control Reg A
  TCCR1A = 0;
  TCCR1B = 0;
}

void setup_timer1(){
 
  // Set CTC mode (resets load after reaching comp goal)
  TCCR1B &= ~(1 << WGM13);
  TCCR1B |= (1 << WGM12);

  // Set to prescaler of 8
  TCCR1B &= ~(1 << CS12);
  TCCR1B |= (1 << CS11);
  TCCR1B &= ~(1 << CS10);

  // Reset Timer1 and set compare value
  TCNT1 = t1_load;
  OCR1A = t1_comp;

  // Enable Timer1 compare interrupt
  TIMSK1 = (1 << OCIE1A);
}

void setup() {
  // Enable global interrupts
  sei();
  reset_timer1();
  setup_timer1();
  lcd.begin(16, 2);
  pinMode(ledPin, OUTPUT);
  Serial.begin(500000);
}

void loop() {
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print(sensor_read);
  delay(100);
}

char* mystrcat( char* dest, char* src )
{
     while (*dest) dest++;
     while (*dest++ = *src++);
     return --dest;
}

#define INT2POINTER(a) ((char*)(intptr_t)(a))

ISR(TIMER1_COMPA_vect) {
  long int init = micros();
  //digitalWrite(ledPin, 1);
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
    Serial.print(bigString);
  }
}
