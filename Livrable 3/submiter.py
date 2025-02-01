from sources import Source
import numpy as np
from matplotlib import pyplot as plt
import sounddevice as sd
from scipy.fft import fft, fftfreq
from scipy.signal import hilbert
from scipy.io.wavfile import write

audio = []

class Note:
    def __init__(self, frequency):
        self.frequency = frequency
    
    def generate_signal(self, t):
        return np.sin(2 * np.pi * t * self.frequency)

class Submiter:
    def __init__(self, source:Source, variables:dict):
        self.source = source
        self.variables = variables

        self.notes = []
        self.populate_notes()

        self.sync_sequence()
        self.start_streaming()
    
    def sync_sequence(self):
        # Aquire constants
        period = 1/self.variables["data_frequency"]
        sampling_frequency = self.variables["sampling_frequency"]
        sampling_period = 1/sampling_frequency
        note_samples = int(period * sampling_frequency)
        
        t = np.linspace(0, period, note_samples, dtype=np.float32)
        carrier_range = self.variables["output_range"]

        low = np.sin(2 * np.pi * t * carrier_range[0])
        high = np.sin(2 * np.pi * t * carrier_range[1])


        with sd.OutputStream(samplerate=sampling_frequency, channels=1, blocksize=1024) as s:
            s.start()

            for i in range(self.variables["sync_call_duration"]):
                s.write(high)
                s.write(low)
            
            for i in range(self.variables["sync_transition_duration"]):
                s.write(low)
            
            arity = self.variables["arity"]
            bits = [int(i) for i in format(arity, "08b")]

            for b in bits:
                if b == 0:
                    s.write(low)
                else:
                    s.write(high)

            for i in range(self.variables["sync_transition_duration"]):
                s.write(low)


    def populate_notes(self):
        max_frequency = self.variables["data_frequency"]
        arity = self.variables["arity"]

        frequencies = []
        
        current_frequency = max_frequency
        for i in range(arity):
            frequencies.append(current_frequency)
            current_frequency += max_frequency
        
        self.notes = [Note(f) for f in frequencies]

    def start(self):
        period = 1/self.variables["data_frequency"]
        sampling_frequency = self.variables["sampling_frequency"]
        sampling_period = 1/sampling_frequency
        note_samples = int(period * sampling_frequency)

        t = np.linspace(0, period, note_samples)

        carrier_range = self.variables["output_range"]
        carrier_frequency = (carrier_range[0] + carrier_range[1])/2
        frequency_deviation = carrier_range[0] - carrier_frequency

        while self.source.valid():
            modulating_signal = np.zeros(note_samples)

            char = self.source.next()

            bits = [int(i) for i in format(ord(char), "08b")]

            for i in range(8):
                b = bits[i]
                if b == 0: continue
                modulating_signal += self.notes[i].generate_signal(t)

            modulating_signal /= np.max(np.abs(modulating_signal))      

            integrated_signal = np.cumsum(modulating_signal) * sampling_period
            signal = np.cos(2 * np.pi * carrier_frequency * t + 2 * np.pi * frequency_deviation * integrated_signal)

            sd.wait()
            print(char, end='', flush=True)
            sd.play(signal)
        
        sd.wait()
        print()
        print("Finished !")
    
    def start_streaming(self):
        
        # constants
        period = 1/self.variables["data_frequency"]
        sampling_frequency = self.variables["sampling_frequency"]
        sampling_period = 1/sampling_frequency
        note_samples = int(period * sampling_frequency)

        # generate the time array
        t = np.linspace(0, period, note_samples, dtype=np.float32)

        # carrier properties
        carrier_range = self.variables["output_range"]
        carrier_frequency = (carrier_range[0] + carrier_range[1])/2
        frequency_deviation = carrier_range[0] - carrier_frequency

        print("[Transmiting] : ", end='')

        # Streaming out the message
        with sd.OutputStream(samplerate=sampling_frequency, channels=1) as s:
            s.start()

            # Run until the source is empty
            while self.source.valid():

                # The modulating signal
                modulating_signal = np.zeros(note_samples, dtype=np.float32)

                # The character we want to stransmit
                char = self.source.next()

                # The 8 bits of the char
                bits = [int(i) for i in format(ord(char), "08b")]

                # for all 8 bits
                for i in range(8):

                    # Aquire the current bit
                    b = bits[i]

                    # If the bit is not set, we ignore it
                    if b == 0: continue

                    # If it is set, we add up it's signal to the modulating signal
                    modulating_signal += self.notes[i].generate_signal(t)

                # Normalize the output signal
                modulating_signal /= np.max(np.abs(modulating_signal))      

                # integrate the modulating signal for final modulation
                integrated_signal = np.cumsum(modulating_signal) * sampling_period

                # Generate output signal
                signal = np.cos(2 * np.pi * carrier_frequency * t + 2 * np.pi * frequency_deviation * integrated_signal)

                # sd.wait()
                # sd.play(signal)
                print(char, end='', flush=True)

                # Send the array to the stream
                s.write(signal)
            
            # Ensure the stream has finished
            s.stop()
            s.close()

        print()
        print("Finished !")
        

"""
analytic_signal = np.fft.ifft(np.fft.fft(signal) * np.where(np.fft.fftfreq(len(signal)) >= 0, 2, 0))
            phase = np.unwrap(np.angle(analytic_signal))  # Unwrap to avoid phase jumps

            # Differentiate the phase to get the instantaneous frequency
            instantaneous_frequency = np.diff(phase) / (2 * np.pi * period)

            # Remove the carrier frequency to isolate the modulating signal
            modulating_signal = (instantaneous_frequency - carrier_frequency) / frequency_deviation

            # Pad the modulating signal to match the original length
            modulating_signal = np.pad(modulating_signal, (0, 1), mode='edge')
"""