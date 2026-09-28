# Melody Piano Player

A command-line Python application for playing, writing, editing, and deleting piano melodies. Melodies are stored as note sequences and rendered to audio in real time using generated sine waves.

## Features

- **Play a saved melody** — select from a list of stored melodies and hear it played back.
- **Write and save a new melody** — enter a name and a note sequence (e.g. `E4-C4-E4`) to add a new melody.
- **Edit a saved melody** — replace or delete notes, either by name (all occurrences) or by position.
- **Delete a saved melody** — remove a melody from the saved list.

Melodies support a pause/rest token (`P`) for silence between notes.

## Project structure

```
melody-piano-player/
├── main.py              # Entry point: menu loop and all melody operations
├── usefulFunctions.py   # Audio synthesis and playback (sine wave generation, crossfading)
├── piano_keys.txt        # Piano key index, note name, and frequency (Hz) lookup table
├── melodies_data.txt     # Saved melodies (name, note sequence)
├── requirements.txt
└── .gitignore
```

## Requirements

- Python 3.8+
- A working audio output device (uses [`sounddevice`](https://python-sounddevice.readthedocs.io/), which relies on PortAudio)

## Setup

```bash
git clone <this-repo-url>
cd melody-piano-player
pip install -r requirements.txt
python main.py
```

> **Note:** `sounddevice` depends on the PortAudio library. On most systems `pip install sounddevice` pulls in a working PortAudio automatically. If you hit a `PortAudioError` on Linux, install it manually first:
> ```bash
> sudo apt-get install libportaudio2
> ```

## Data file formats

**`piano_keys.txt`** — one key per line:
```
<index>,<note name>,<frequency in Hz>
```

**`melodies_data.txt`** — one melody per line:
```
<melody name>,<note1>-<note2>-<note3>-...
```
Use `P` in place of a note to insert a silent beat (rest).

## Usage

Run the app and choose an option from the menu:

```
Menu Options
 ==============================
 1: Play a saved melody
 2: Write and save a new melody
 3: Edit a saved melody
 4: Delete a saved melody
 5: Quit
```

New and edited melodies are written back to `melodies_data.txt` so they persist between runs.

## Author

Danielis Litvinovas
