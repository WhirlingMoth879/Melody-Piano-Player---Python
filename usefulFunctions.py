import numpy as np
import sounddevice as sd

def gen_sin(f):
    """Generate a sine wave with exponential fade-out."""
    duration = 0.2
    sample_rate = 44100
    decay_factor = 5
    amplitude = 0.5
    n = np.arange(int(sample_rate * duration))  # Time array in samples
    decay = np.exp(-decay_factor * (n / sample_rate))  # Apply decay over time
    sine_wave = np.sin(2 * np.pi * f * (n / sample_rate))  # Generate sine wave

    # Apply fade-in and fade-out
    fade_len = int(0.05 * sample_rate)  # Fade length (5% of sample rate)
    fade_in = np.linspace(0, 1, fade_len)
    fade_out = np.linspace(1, 0, fade_len)

    sine_wave[:fade_len] *= fade_in  # Apply fade-in
    sine_wave[-fade_len:] *= fade_out  # Apply fade-out

    return amplitude * decay * sine_wave


def generate_melody_audio(melody_notes, overlap=0.01, sample_rate=44100):
    """Generates a full waveform for a melody, applying smooth transitions."""
    overlap_samples = int(overlap * sample_rate)  # Overlap in samples
    full_melody = np.array([])  # Start with empty array

    for i, note in enumerate(melody_notes):
        note_wave = gen_sin(note)  # Generate note

        if i > 0:  # Apply overlap to smooth transitions
            full_melody[-overlap_samples:] += note_wave[:overlap_samples]  # Crossfade
            note_wave = note_wave[overlap_samples:]  # Remove extra part

        full_melody = np.concatenate((full_melody, note_wave))  # Add to melody

    return full_melody

def play_melody_audio(melody_notes):
    """Play the generated melody."""

    wave = generate_melody_audio(melody_notes)
    sd.play(wave, samplerate=44100)
    sd.wait()