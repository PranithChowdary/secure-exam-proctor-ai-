import os
import threading
import socketio
import sounddevice as sd
import numpy as np
import speech_recognition as sr

sio = socketio.Client()
try:
    sio.connect('http://localhost:5501')
    print("Connected to the Socket.IO server")
except Exception as e:
    print(f"Failed to connect to the Socket.IO server: {e}")


def convert_and_emit():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening for speech...")
        try:
            while True:
                audio = r.listen(source)
                value = r.recognize_google(audio, show_all=False)

                if value:
                    print("Someone is talking!")
                    sio.emit('canvas-color', 'red')
                else:
                    print("Silence detected.")
                    sio.emit('canvas-color', 'green')

        except sr.UnknownValueError:
            print("No speech detected.")
        except sr.RequestError as e:
            print("Speech recognition request failed: {0}".format(e))
        except KeyboardInterrupt:
            pass

def main():
    t1 = threading.Thread(target=convert_and_emit)
    t1.start()
    t1.join()

if __name__ == "__main__":
    main()
