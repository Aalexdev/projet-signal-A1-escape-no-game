from sink import Sink

import pyaudio
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from matplotlib.animation import FuncAnimation

class Receiver:
    def __init__(self, sink:Sink):
        self.format = pyaudio.paInt16
        self.rate = 44100
        self.chunk = 1024
        self.range = (0, 20000)

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
        FREQ_RANGE = self.range
        RATE = self.rate
        stream = self.stream


        fig, ax = plt.subplots()
        x = np.fft.rfftfreq(CHUNK, 1 / RATE)  # Frequency bins
        line, = ax.semilogy(x, np.zeros_like(x))  # Logarithmic scale for better visualization
        ax.set_ylim(1, 10**6)  # Adjust based on your signal strength
        ax.set_xlim(FREQ_RANGE[0], FREQ_RANGE[1])  # Focus on the frequency range of interest
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Magnitude')
        ax.set_title('Real-Time Spectrogram')

        def update(frame):
            # Read audio data from the stream
            data = stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)

            # Perform FFT to convert to frequency domain
            fft_data = np.fft.rfft(audio_data)
            magnitudes = np.abs(fft_data)

            # Update the plot
            line.set_ydata(magnitudes)
            return line,

        # Create animation
        ani = FuncAnimation(fig, update, blit=True, interval=50, cache_frame_data=False)

        # Show the plot
        plt.show()

        # Clean up
        stream.stop_stream()
        stream.close()
        self.p.terminate()
        # stream = self.stream
        # try:
        #     while True:
        #         # Read audio data from the stream
        #         data = stream.read(self.chunk, exception_on_overflow=False)
        #         audio_data = np.frombuffer(data, dtype=np.int16)

        #         # Perform FFT to convert to frequency domain
        #         fft_data = scipy.fftpack.fft(audio_data)
        #         freqs = scipy.fftpack.fftfreq(len(fft_data), 1 / self.rate)

        #         # Find magnitudes of frequencies
        #         magnitudes = np.abs(fft_data)

        #         # Check if frequencies in the desired range are present
        #         for i, freq in enumerate(freqs):
        #             if self.range[0] <= abs(freq) <= self.range[1] and magnitudes[i] > 1000:  # Threshold to filter noise
        #                 print(f"Detected signal at {abs(freq):.2f} Hz")

        # except KeyboardInterrupt:
        #     print("Stopping...")

        # finally:
        #     # Clean up
        #     stream.stop_stream()
        #     stream.close()
        #     self.p.terminate()