import pyaudio
import time
import numpy as np
from matplotlib import pyplot as plt

CHANNELS = 1
RATE = 1024


p = pyaudio.PyAudio()
dry_data = np.array([])


def main():
    stream = p.open(
        format=pyaudio.paFloat32,
        channels=CHANNELS,
        rate=RATE,
        # output=True,
        input=True,
        stream_callback=callback,
    )
    stream.start_stream()

    while stream.is_active():
        time.sleep(10)
        stream.stop_stream()
    stream.close()

    numpydata = np.hstack(dry_data)
    plt.plot(numpydata)
    plt.title("Wet")
    plt.show()

    p.terminate()


def callback(in_data, frame_count, time_info, flag):
    global b, a, fulldata, dry_data, frames
    audio_data = np.frombuffer(in_data, dtype=np.float32)
    print(frame_count, audio_data[0:10])
    # Snip out 512 values expand from [-1:1] to [0:1024]
    # Pack into {"time": "2021-01-01T12:00:00", "data": {"ACCX": [...]}}
    # Publish on "mls160a/0/v"
    dry_data = np.append(dry_data, audio_data)
    # do processing here
    return (audio_data, pyaudio.paContinue)


if __name__ == '__main__':
    main()
