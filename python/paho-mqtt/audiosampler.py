import pyaudio
import time
import functools
import numpy as np
from matplotlib import pyplot as plt

CHANNELS = 1
RATE = 1024


class AudioSampler(object):
    def __init__(self):
        self.paudio = pyaudio.PyAudio()
        self.stream = self.paudio.open(
            format=pyaudio.paFloat32,
            channels=CHANNELS,
            rate=RATE,
            # output=True,
            input=True,
            stream_callback=functools.partial(AudioSampler.callback, self),
        )
        self.dry_data = np.array([])

    def main(self):
        self.stream.start_stream()
        while self.stream.is_active():
            time.sleep(10)
            self.stream.stop_stream()
        self.stream.close()
        self.paudio.terminate()

        numpydata = np.hstack(self.dry_data)
        plt.plot(numpydata)
        plt.title("Wet")
        plt.show()

    def callback(self, in_data, frame_count, time_info, flag):
        audio_data = np.frombuffer(in_data, dtype=np.float32)
        print(frame_count, audio_data[0:10])
        # Snip out 512 values expand from [-1:1] to [0:1024]
        # Pack into {"time": "2021-01-01T12:00:00", "data": {"ACCX": [...]}}
        # Publish on "mls160a/0/v"
        self.dry_data = np.append(self.dry_data, audio_data)
        # do processing here
        return (audio_data, pyaudio.paContinue)


if __name__ == '__main__':
    AudioSampler().main()
