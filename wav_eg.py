import threading
import time
import wave
import pyaudio

def play_wav(filename):
    CHUNK = 1024

    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while data:
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()

# Main function
def main():
    wav_file = 'temp.wav' #filename

    wav_thread = threading.Thread(target=play_wav, args=(wav_file,))
    wav_thread.daemon = True
    wav_thread.start()

    for i in range(5):
        print("Main program is running...")
        time.sleep(1)

# Run the main function
if __name__ == "__main__":
    main()
