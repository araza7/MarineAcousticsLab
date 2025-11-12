🌊 MarineAcousticsLab

MarineAcousticsLab is a Python-based tool for analyzing and visualizing passive acoustic recordings from marine environments.
It helps researchers characterize sounds from dolphins, whales, and other ocean species using waveform, frequency, and spectrogram analysis.

🧠 Overview

This script automatically scans a folder for .wav files, performs signal analysis, and generates both interactive and static visualizations.
It is designed for marine bioacoustics work — allowing you to quickly inspect recordings, detect animal vocalizations, and compare signal features across datasets.

🎯 Key Features

📂 Batch Processing: Automatically analyzes all .wav files in a directory.

🧮 Signal Analysis:

Normalizes and downsamples large recordings.

Computes FFT spectra and spectrograms for sound characterization.

📊 Visualization:

Time-domain waveform.

Frequency-domain amplitude spectrum.

Time–frequency spectrogram (in dB).

💾 Output:

Interactive HTML plots (*_analysis.html).

Static JPG plots (*_analysis.jpg).

🔊 Playback Support: Listen to recordings directly when using Jupyter Notebook.

⚙️ Requirements
Python version

Python 3.8+

Dependencies

Install the required libraries with:

pip install numpy scipy plotly kaleido ipython


kaleido is required to export static .jpg images.

🚀 Usage

Place your .wav recordings in the same directory as the script.

Run:

python marine_acoustics_lab.py


The tool will:

Analyze each .wav file.

Generate an interactive HTML plot and a static image for each.

Save results in the same directory.

Optionally play audio (in Jupyter).

📂 Output Example

For a file named whale_click.wav, you’ll get:

whale_click.wav
whale_click_analysis.html
whale_click_analysis.jpg


The generated plots show:

Waveform: Amplitude vs. Time

FFT Spectrum: Frequency vs. Amplitude

Spectrogram: Frequency vs. Time (power in dB)

🔬 Parameters

You can modify these variables at the top of the script:

Variable	| Description	|Default
audio_dir|	Input directory for .wav files	|"."
output_dir|	Output directory for plots	|"."
MAX_SAMPLES	|Max number of samples processed (to prevent memory issues)	|100000
🐬 Use Cases

Characterizing dolphin echolocation clicks and whale vocalizations.

Comparing underwater acoustic profiles across locations or species.

Monitoring marine biodiversity and soundscapes from passive sensors.

Pre-screening data before deeper signal processing or ML classification.

⚠️ Notes

Stereo recordings are automatically converted to mono.

Large files are downsampled for memory efficiency.

Spectrogram computation adapts to sampling rate and duration.

HTML outputs use CDN-hosted Plotly for lightweight storage.
