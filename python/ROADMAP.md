# Roadmap for audio analysis

Ingest audio data via MQTT

Pass audio through a detrend filter

Pass audio through windowing filter

Pass windowed data through STFT

Emit stream of STFT vectors

Detect total power spikes

Output image-like blocks of STFT * samples
using a maximum width.
A spike starts a new block. The previous block is 0-padded and sent out.
If a block is full (no spike) it is sent out.

Each block receives meta data on whether it was triggered or not.


## Detrend

Ingest N samples.

Calculate mean, subtract from all samples.

Emit detrended version.


## Windowing filter

Define a window width 2N. Calculate the N values into a table w(n), use
1-w(n) for the ramp down.

Process blocks of N samples.

Run the samples through the table, generating the left
half of the window w(n) and the right half of the window 1-w(n) at the same
time into two buffers of size N.

Emit the left haft of the previous sample block and the right half
of the current block.

Store the left half of the current block for the next run.


## Short Time Fourier Transform

Ingest the windowed sample groups of 2N from previous stage.

Calculate STFT yielding N amplitudes (dump phases in first iteration).

Emit the amplitudes.


## Detect Power Spikes

Collect STFT vector.

Calculate squared difference sum with stored vector. If above a threshold,
emit spike signal along with data.

Store STFT vector for next comparison.


## Collect in 2D-Blocks

Maintain a 2D storage, receive one row after the other.

If the row has a spike signal, and the previous had none, then flush
the current 2D storage, padding it with zeroes. Emit the 2D image.

In that case, mark the 2D image as "triggered".

If not, add the vector to the currently stored 2D image.

If the image is full, emit the 2D image.

In that case, do not mark the 2D image as "triggered", as it is factually a
spillover.


## Further Processing

Because the 2D images are tagged "triggered" or "spillover", the following
process can route these images through different ML channels.

Triggered images could be passed through a multilayered convolutional network,
with perhaps one consolidation layer (depending on the size).


## Calculation Example

To get an understanding for the dimensions used for sound analysis, use this
calculus:

Width of the 2D image = sample block size N (2N per window yields N frequency
amplitudes)

Height of the 2D image = number of blocks = time interval * sample rate / N

Example:
- Width = 256 frequency amplitudes
- Time covered per image = 1 second
- Height = 256 frequency spectra
- It follows that the sample rate is 65536 Hz
- 32x32, 1 second, sample rate follows as 1024 Hz
- 64x64, 1 second, sample rate follows as 4096 Hz
