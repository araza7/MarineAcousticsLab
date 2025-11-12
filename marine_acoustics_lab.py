import os
import numpy as np
import scipy
from scipy.io import wavfile
import scipy.fft as fft
from scipy import signal
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from IPython.display import Audio
import plotly.io as pio

# Use current working directory for input and output
audio_dir = "."  # Current directory for WAV files
output_dir = "."  # Current directory for HTML and JPG plots

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Maximum samples to process (to avoid memory issues)
MAX_SAMPLES = 100000  # ~6.25s at 16 kHz, ~0.2s at 500 kHz

# Main processing loop
print("Starting audio analysis...")
for file in os.listdir(audio_dir):
    if file.endswith(".wav"):
        file_path = os.path.join(audio_dir, file)
        file_name = os.path.splitext(file)[0]
        print(f"Processing {file_name}...")

        # Read WAV file using scipy.io.wavfile
        try:
            sampling_rate, data = wavfile.read(file_path)
        except Exception as e:
            print(f"Error reading {file_name} with scipy.io.wavfile.read: {e}")
            continue

        # If stereo, take first channel
        if len(data.shape) > 1:
            data = data[:, 0]

        # Downsample if too many samples
        if len(data) > MAX_SAMPLES:
            print(f"Downsampling {file_name} from {len(data)} to {MAX_SAMPLES} samples...")
            step = len(data) // MAX_SAMPLES
            data = data[::step]
            sampling_rate = sampling_rate // step
            print(f"New sampling rate: {sampling_rate} Hz")

        # Normalize data to float
        X = data.astype(float) / np.max(np.abs(data))

        # Time vector for waveform
        duration = len(X) / sampling_rate
        time = np.linspace(0, duration, len(X))

        # Compute FFT using scipy.fft
        Y = fft.fft(X)
        L = len(Y)
        P2 = np.abs(Y / L)
        P1 = P2[:L//2 + 1]
        P1[1:-1] = 2 * P1[1:-1]  # Double amplitudes except DC and Nyquist
        f = sampling_rate * np.arange(0, L//2 + 1) / L

        # Create interactive plot with Plotly
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=("Waveform", "Single-Sided Amplitude Spectrum", "Spectrogram"),
            vertical_spacing=0.1
        )

        # Waveform
        fig.add_trace(
            go.Scatter(x=time, y=X, mode='lines', name='Waveform'),
            row=1, col=1
        )
        fig.update_xaxes(title_text="Time (s)", row=1, col=1)
        fig.update_yaxes(title_text="Amplitude", row=1, col=1)

        # FFT
        fig.add_trace(
            go.Scatter(x=f, y=P1, mode='lines', name='FFT'),
            row=2, col=1
        )
        fig.update_xaxes(title_text="f (Hz)", row=2, col=1, range=[0, sampling_rate / 2])
        fig.update_yaxes(title_text="|P1(f)|", row=2, col=1)

        # Compute spectrogram using scipy.signal, adjusting for short or large signals
        if len(X) >= 64:  # Minimum length for meaningful spectrogram
            # Adjust nperseg for large files to reduce memory usage
            window_size = min(1280, len(X), 256 if sampling_rate > 100000 else 1280)
            overlap = int(window_size * 0.9)  # Set noverlap to 90% of nperseg
            hop_length = window_size - overlap
            try:
                freqs, times, Sxx = signal.spectrogram(
                    X, fs=sampling_rate, nperseg=window_size, noverlap=overlap, nfft=window_size
                )

                # Convert to dB for visualization
                Sxx_db = 10 * np.log10(Sxx + 1e-10)  # Avoid log(0)

                # Spectrogram
                fig.add_trace(
                    go.Heatmap(
                        x=times, y=freqs, z=Sxx_db,
                        colorscale='Viridis',
                        colorbar=dict(title="Power (dB)"),
                        showscale=True
                    ),
                    row=3, col=1
                )
                fig.update_xaxes(title_text="Time (s)", row=3, col=1)
                fig.update_yaxes(title_text="Frequency (Hz)", row=3, col=1, range=[0, min(sampling_rate / 2, 10000)])
            except MemoryError:
                print(f"MemoryError: Spectrogram too large for {file_name}. Skipping spectrogram.")
        else:
            print(f"Warning: {file_name} too short ({len(X)} samples) for spectrogram. Skipping spectrogram.")

        # Update layout
        fig.update_layout(
            title=f"Analysis: {file_name}",
            height=800,
            showlegend=False
        )

        # Save as HTML for interactivity, using CDN to reduce file size
        output_path_html = os.path.join(output_dir, f"{file_name}_analysis.html")
        try:
            fig.write_html(output_path_html, include_plotlyjs='cdn')
        except MemoryError:
            print(f"MemoryError: Failed to save HTML for {file_name}. Skipping HTML output.")
            continue

        # Save as JPG for static image, with fallback
        output_path_jpg = os.path.join(output_dir, f"{file_name}_analysis.jpg")
        try:
            fig.write_image(output_path_jpg, format="jpg", width=1200, height=800)
        except ImportError as e:
            print(f"Error saving JPG for {file_name}: {e}. Install kaleido with 'pip install -U kaleido'. Skipping JPG export.")
        except Exception as e:
            print(f"Error saving JPG for {file_name}: {e}. Skipping JPG export.")

        # Play audio
        print(f"Playing {file_name}...")
        display(Audio(data=X, rate=sampling_rate))

print("Analysis complete. Interactive plots saved as HTML and JPG (if possible) in", output_dir)
