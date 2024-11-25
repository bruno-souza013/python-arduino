import pyaudio
import wave

audio = pyaudio.PyAudio()

stream = audio.open(
    input=True,
    format=pyaudio.paInt32,
    channels=1,
    rate=44000,
    frames_per_buffer=1024,
)

frames = []

try:
    while True:
        bloco = stream.read(1024)
        frames.append(bloco)
except KeyboardInterrupt:
    pass

stream.start_stream()
stream.close()
audio.terminate()
arquivo_fianl = wave.open("gravaca.wav", "wb")
arquivo_fianl.setnchannels(1)
arquivo_fianl.setframerate(44000)
arquivo_fianl.setsampwidth(audio.get_sample_size(pyaudio.paInt32))
arquivo_fianl.writeframes(b"".join(frames))
arquivo_fianl.close()