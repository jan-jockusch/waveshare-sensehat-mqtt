import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


rng = np.random.default_rng()
# number of samples, sampling frequency
N = 2**8+1  # 2**17
fs = 2**13
# Time axis
time = np.arange(N) / float(fs)
# Amplitude and modulation of carrier signal
amp = 2 * np.sqrt(2)
# Modulation is an array of shape "time"
mod = 500*np.cos(2*np.pi*0.25*time)
# Do frequency modulation by offsetting the sine generator
carrier = amp * np.sin(2*np.pi*3e3*time + mod)
# Add noise of given power
noise_power = 0.01 * fs / 2
noise = rng.normal(scale=np.sqrt(noise_power),
                   size=time.shape)
# Modulate the noise amplitude
noise *= np.exp(-time/5)
x = carrier + noise

f, t, Zxx = signal.stft(x, fs, nperseg=256, boundary=None)

plt.pcolormesh(t, f, np.abs(Zxx), vmin=0, vmax=amp, )  # shading='gouraud')
plt.title('STFT Magnitude')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.show()
