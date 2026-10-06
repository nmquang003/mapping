"""Compose an original, seamless ambient loop; no sampled or third-party music.
Requires numpy and ffmpeg. Run with the workspace Python runtime.
"""
from pathlib import Path
import subprocess
import tempfile
import wave
import numpy as np

RATE = 44100
SECONDS = 48
SIZE = RATE * SECONDS
mix = np.zeros((SIZE, 2), dtype=np.float64)

def frequency(note):
    return 440 * 2 ** ((note - 69) / 12)

def add_note(note, start, duration, amplitude, pan, pad=False):
    t = np.arange(round(duration * RATE)) / RATE
    f = frequency(note)
    if pad:
        envelope = np.sin(np.pi * t / duration) ** 2
        sound = sum(weight * np.sin(2*np.pi*(f*harmonic+detune)*t)
                    for harmonic, weight, detune in [(1, .8, -.25), (1, .7, .25), (2, .12, 0), (3, .03, 0)])
    else:
        envelope = (1-np.exp(-t/.025)) * np.exp(-t/2.8) * np.minimum((duration-t)/.5, 1)
        sound = np.sin(2*np.pi*f*t) + .28*np.sin(2*np.pi*2*f*t)*np.exp(-t/.7)
        sound += .08*np.sin(2*np.pi*3*f*t)*np.exp(-t/.3)
    sound *= envelope * amplitude
    indices = (round(start * RATE) + np.arange(len(t))) % SIZE
    # Wrap note tails around the loop for a continuous musical boundary.
    for delay, gain in [(0, 1), (.29, .16), (.61, .09), (.97, .045)]:
        stereo = sound[:, None] * np.array([np.cos(pan*np.pi/2), np.sin(pan*np.pi/2)]) * gain
        mix[(indices + round(delay*RATE)) % SIZE] += stereo

# Dmaj9, Gmaj9, Bm7, Asus: slow, open voicings without a drum beat.
chords = [[50,57,61,66,69], [43,54,57,62,69], [47,54,57,62,66], [45,52,57,62,64]]
melodies = [[74,78,81,78], [79,78,74,69], [78,81,85,81], [76,74,73,69]]
for bar, chord in enumerate(chords):
    for j, note in enumerate(chord):
        add_note(note, bar*12-2, 16, .045, .2+j*.15, pad=True)
    for j, note in enumerate(melodies[bar]):
        add_note(note, bar*12+j*3+.6, 9, .13, .3+(j%2)*.4)

mix *= .58 / np.max(np.abs(mix))
output = Path(__file__).resolve().parents[1] / 'dist/assets/audio'
output.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory() as tmp:
    wav = Path(tmp) / 'peaceful.wav'
    with wave.open(str(wav), 'wb') as file:
        file.setnchannels(2); file.setsampwidth(2); file.setframerate(RATE)
        file.writeframes((mix*32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(wav),
                    '-codec:a','libmp3lame','-b:a','128k',str(output/'peaceful-tour.mp3')],check=True)
print(f'Generated original {SECONDS}s ambient loop; peak={np.max(np.abs(mix)):.2f}, RMS={np.sqrt(np.mean(mix**2)):.3f}')
