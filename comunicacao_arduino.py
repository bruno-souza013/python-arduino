import sounddevice as sd
import numpy as np
import serial
import time
import scipy.io.wavfile as wav
from threading import Thread
from datetime import datetime
import os

try:
    arduino = serial.Serial('COM4', 9600)
    time.sleep(2)
except Exception as e:
    print(f"Erro ao conectar ao Arduino. {e}")

gravando = False
audio_data = []
samplerate = 44100  # Taxa padrão (44.1 kHz)

# calcula nivel audio
def calcular_nivel(audio_chunk):
    rms = np.sqrt(np.mean(audio_chunk**2)) 
    return rms

# controla leds (tipo equalizador visual)
def controlar_leds(volume):
    volume_amplificado = volume * 10
    som = 0.04  

    if volume_amplificado < som:
        # Sem som
        arduino.write(b'L')  
    elif volume_amplificado < 0.08: 
        # Som baixo
        arduino.write(b'T')  
    elif volume_amplificado < 0.1:  
        # Som médio
        arduino.write(b'U') 
    else:  
        # Som alto
        arduino.write(b'V')
         
# gravar áudio
def gravar_audio():
    global gravando, audio_data
    #verificar no arquivo 'verificar_mics' o índice do microfone desejado para incluir na linha abaixo... 
    #with sd.InputStream(device= 'aqui vai o indice do mic',samplerate=samplerate, channels=1, dtype='float32') as stream:
    with sd.InputStream(samplerate=samplerate, channels=1, dtype='float32') as stream:
        while gravando:
            data, _ = stream.read(1024)
            audio_data.append(data)
            if not gravando:  
                break
            volume = calcular_nivel(data)
            controlar_leds(volume)  

# salvar o áudio
def salvar_audio(arquivo):
    global audio_data
    if audio_data:
        timest = datetime.now().strftime("%Y%m%d_%H%M%S")
        pasta_input = os.path.join(os.path.dirname(__file__), 'input')
        arquivo = os.path.join(pasta_input, f"gravacao_{timest}.wav")
        audio_array = np.concatenate(audio_data, axis=0)

        fator_amplificacao = 5.0
        audio_amplificado = np.clip(audio_array * fator_amplificacao, -1.0, 1.0)
        
        wav.write(arquivo, samplerate, (audio_amplificado * 32767).astype(np.int32))
        print(f"Áudio salvo com sucesso. Arquivo: {arquivo}")
    else:
        print("Sem áudio para salvar.")

# iniciar a gravação
def iniciar_gravacao():
    global gravando, audio_data
    if not gravando:
        gravando = True
        audio_data = []  
        arduino.write(b'R')  
        Thread(target=gravar_audio).start()
        print("Gravação Iniciada.")

# parar a gravação
def parar_gravacao():
    global gravando
    if gravando:
        gravando = False
        arduino.write(b'S')  
        print("Finalizando Gravação.")
        salvar_audio("gravacao.wav")  

print("1 - Gravar \n2 - Parar \nAperte o botão ou Digite o comando desejado")

try:
    while True:
        if arduino.in_waiting > 0:  
            comando_serial = arduino.readline().decode('utf-8').strip()
            if comando_serial == '1':  
                iniciar_gravacao()
            elif comando_serial == '2':  
                parar_gravacao()

        if os.name == 'nt':
            import msvcrt
            if msvcrt.kbhit():
                comando_teclado = msvcrt.getch().decode('utf-8')
        else:
            import sys, select
            if select.select([sys.stdin], [], [], 0)[0]:
                comando_teclado = sys.stdin.read(1)

        if 'comando_teclado' in locals():
            if comando_teclado == '1':  
                iniciar_gravacao()
            elif comando_teclado == '2':  
                parar_gravacao()
            del comando_teclado
except KeyboardInterrupt:
    parar_gravacao()
    arduino.close()

