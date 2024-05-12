from pydub import AudioSegment
import pyaudio
import time
import threading

def play_audio(file_path):
    audio = AudioSegment.from_mp3(file_path)
    raw_audio_data = audio.raw_data
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(audio.sample_width),
                    channels=audio.channels,
                    rate=audio.frame_rate,
                    output=True)
  
    while True:
        stream.write(raw_audio_data)
    stream.stop_stream()
    stream.close()
    p.terminate()

def play_audio_background(file_path):
    thread = threading.Thread(target=play_audio, args=(file_path,))
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    file_path = "1.mp3"
    play_audio_background(file_path)
    while True:
        print("test message")
        time.sleep(1)
