from sink import Sink

import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from matplotlib.animation import FuncAnimation
from time import time

class Receiver:
    def __init__(self, sink:Sink):
        self.format = pyaudio.paInt16
        self.rate = 44100
        self.chunk = 1024
        self.range = (15000, 17000)
        self.threshold = 10e4

        self.p = pyaudio.PyAudio()

        self.stream = self.p.open(
            rate=self.rate,
            channels=1,
            format=self.format,
            input=True,
            frames_per_buffer=self.chunk
        )

        print("Waiting for signal...")

        

        self.wait_for_call()

    def wait_for_call(self):
        CHUNK = self.chunk
        RANGE = self.range
        RATE = self.rate
        stream = self.stream

        freq_LOW = int(RANGE[0] / (RATE / CHUNK))
        freq_HIGH = int(RANGE[1] / (RATE / CHUNK))

        state = 0
        last_change_time = time()
        count = 0

        times = []

        while True:
            # Read audio data from the stream
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)

            # Perform FFT to convert to frequency domain
            fft_data = np.fft.rfft(audio_data)
            
            magnitudes = np.abs(fft_data)

            delta = time() - last_change_time

            if delta > 0.01:

                if magnitudes[freq_HIGH] > self.threshold:
                    if state != 1:
                        print("high")
                        state = 1
                        times.append(time() - last_change_time)
                        last_change_time = time()
                        count += 1

                elif magnitudes[freq_LOW] > self.threshold:
                    if state != 0:
                        times.append(time() - last_change_time)
                        print("low")
                        state = 0
                        last_change_time = time()
                        count += 1

                if delta > 5:
                    print("timeout")
                    state = 0
                    last_change_time = time()
                    count = 0

                print(count)
                # if count >= 20:
                #     print("called !")
                #     break
        
        print(np.average(times))

        # Clean up
        stream.stop_stream()
        stream.close()
        self.p.terminate()