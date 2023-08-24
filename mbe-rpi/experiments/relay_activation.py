# Importar a biblioteca RPi.GPIO
# Importar a biblioteca time para usar funções de tempo
import time

import RPi.GPIO as GPIO

# Configurar o modo de numeração dos pinos do gpio como BCM
GPIO.setmode(GPIO.BCM)
# Configurar o pino 18 como saída
GPIO.setup(23, GPIO.OUT)

# Criar um loop infinito
while True:
    input()
    print("ON")
    GPIO.output(23, GPIO.LOW)

    input()
    print("OFF")
    GPIO.output(23, GPIO.HIGH)