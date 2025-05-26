import RPi.GPIO as GPIO
import time
import datetime
import pygame

# Configurações do Alarme

HORA_ALARME = "12:12"
CAMINHO_MUSICA = r"/home/aluno/projeto_1/O Descobridor Dos Sete Mares.mp3"

# Configuração do GPIO

GPIO.setmode(GPIO.BCM)
BOTAO_PIN = 18
GPIO.setup(BOTAO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Inicialização do mixer

pygame.mixer.init()
pygame.mixer.music.load(CAMINHO_MUSICA)


# Função para tocar alarme

def tocar_alarme():
    print("Alarme disparado! Tocando música...")
    pygame.mixer.music.play(-1)  # Repete infinitamente

# Loop Principal

alarme_acionado = False
ultima_data_alarme = None  # Armazena a data do último disparo

try:
    while True:
        agora = datetime.datetime.now()
        hora_atual = agora.strftime("%H:%M")
        data_atual = agora.date()

        # Verifica se é hora de disparar o alarme
        if hora_atual == HORA_ALARME and not alarme_acionado:
            if ultima_data_alarme != data_atual:  # Só dispara uma vez por dia
                tocar_alarme()
                alarme_acionado = True
                ultima_data_alarme = data_atual

        # Verifica se o botão foi pressionado
        if alarme_acionado and GPIO.input(BOTAO_PIN) == GPIO.HIGH:
            print("Botão pressionado. Alarme desligado.")
            pygame.mixer.music.stop()
            alarme_acionado = False
            time.sleep(1)  #

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nEncerrando o programa...")
    pygame.mixer.music.stop()
    GPIO.cleanup()
