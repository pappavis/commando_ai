"""
PROJEK RETRORECON — COMMODORE 64 SID KLANKGENERATOR EN KLANKBESTUURDER
Werkstroom A & C: Rob Hubbard SID-klankeffekte en Agtergrondmusiek
"""

import os
import math
import struct
import wave
import random
import subprocess
import threading
from typing import Dict, Optional

SOUNDS_DIR = "/tmp/commando_sounds"

def generate_wave(filename: str, samples: list, sample_rate: int = 22050):
    os.makedirs(SOUNDS_DIR, exist_ok=True)
    filepath = os.path.join(SOUNDS_DIR, filename)
    with wave.open(filepath, "wb") as wav_file:
        wav_file.setnchannels(1)      # Mono
        wav_file.setsampwidth(2)     # 16-bis
        wav_file.setframerate(sample_rate)
        data = bytearray()
        for s in samples:
            clamped = max(-1.0, min(1.0, s))
            val = int(clamped * 32767.0)
            data.extend(struct.pack("<h", val))
        wav_file.writeframes(data)
    return filepath

def generate_sid_shoot(sample_rate: int = 22050) -> str:
    duration = 0.12
    num_samples = int(sample_rate * duration)
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        env = math.exp(-35.0 * t)
        noise = (random.random() * 2.0 - 1.0)
        pitch = 300.0 * (1.0 - t / duration)
        tone = math.sin(2.0 * math.pi * pitch * t)
        sample = (0.75 * noise + 0.25 * tone) * env
        samples.append(sample)
    return generate_wave("shoot.wav", samples, sample_rate)

def generate_sid_explosion(sample_rate: int = 22050) -> str:
    duration = 0.55
    num_samples = int(sample_rate * duration)
    samples = []
    last_noise = 0.0
    for i in range(num_samples):
        t = i / sample_rate
        env = math.exp(-6.5 * t)
        raw_noise = (random.random() * 2.0 - 1.0)
        filtered_noise = last_noise + 0.12 * (raw_noise - last_noise)
        last_noise = filtered_noise
        rumble = math.sin(2.0 * math.pi * 55.0 * (1.0 - t*0.8) * t)
        sample = (filtered_noise * 3.5 + rumble * 0.4) * env
        samples.append(sample)
    return generate_wave("explosion.wav", samples, sample_rate)

def generate_sid_grenade_throw(sample_rate: int = 22050) -> str:
    duration = 0.18
    num_samples = int(sample_rate * duration)
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        env = math.sin(math.pi * (t / duration))
        freq = 320.0 + 480.0 * (t / duration)
        pulse = 1.0 if math.sin(2.0 * math.pi * freq * t) > 0.0 else -1.0
        sample = pulse * env * 0.45
        samples.append(sample)
    return generate_wave("grenade_throw.wav", samples, sample_rate)

def generate_sid_enemy_hit(sample_rate: int = 22050) -> str:
    duration = 0.10
    num_samples = int(sample_rate * duration)
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        env = math.exp(-25.0 * t)
        freq = 700.0 - 500.0 * (t / duration)
        tone = math.sin(2.0 * math.pi * freq * t)
        noise = (random.random() * 2.0 - 1.0)
        sample = (0.5 * tone + 0.5 * noise) * env * 0.6
        samples.append(sample)
    return generate_wave("enemy_hit.wav", samples, sample_rate)

def generate_sid_rescue(sample_rate: int = 22050) -> str:
    """Outentieke C64 SID arpeggio-chime wanneer 'n POW gered word."""
    duration = 0.28
    num_samples = int(sample_rate * duration)
    samples = []
    notes = [note_freq(72), note_freq(76), note_freq(79), note_freq(84)]
    for i in range(num_samples):
        t = i / sample_rate
        note_idx = min(3, int(t / (duration / 4.0)))
        freq = notes[note_idx]
        env = math.exp(-6.0 * (t % (duration / 4.0)))
        pulse = 1.0 if math.sin(2.0 * math.pi * freq * t) > 0.0 else -1.0
        sample = pulse * env * 0.4
        samples.append(sample)
    return generate_wave("hostage_rescue.wav", samples, sample_rate)

def generate_sid_pickup(sample_rate: int = 22050) -> str:
    """Dubbele SID-bliep vir optel van granaatkratte."""
    duration = 0.16
    num_samples = int(sample_rate * duration)
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        freq = 880.0 if t < 0.08 else 1760.0
        env = math.exp(-20.0 * (t % 0.08))
        pulse = 1.0 if math.sin(2.0 * math.pi * freq * t) > 0.0 else -1.0
        sample = pulse * env * 0.35
        samples.append(sample)
    return generate_wave("crate_pickup.wav", samples, sample_rate)

def generate_sid_victory(sample_rate: int = 22050) -> str:
    """Rob Hubbard styl triomffanfare wanneer die laaste vesting val."""
    duration = 1.2
    num_samples = int(sample_rate * duration)
    samples = [0.0] * num_samples
    chords = [
        (0.00, 0.20, [note_freq(60), note_freq(67)]),
        (0.20, 0.40, [note_freq(64), note_freq(72)]),
        (0.40, 0.60, [note_freq(67), note_freq(76)]),
        (0.60, 1.20, [note_freq(72), note_freq(79), note_freq(84)]),
    ]
    for start_t, end_t, freqs in chords:
        start_idx = int(start_t * sample_rate)
        end_idx = min(num_samples, int(end_t * sample_rate))
        dur = end_t - start_t
        for i in range(start_idx, end_idx):
            t = (i - start_idx) / sample_rate
            env = math.exp(-2.5 * (t / dur))
            val = 0.0
            for f in freqs:
                pulse = 1.0 if math.sin(2.0 * math.pi * f * (i / sample_rate)) > 0.0 else -1.0
                val += pulse * 0.15
            samples[i] += val * env
    return generate_wave("victory_fanfare.wav", samples, sample_rate)

def note_freq(midi_note: int) -> float:
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))

def generate_rob_hubbard_theme(sample_rate: int = 22050) -> str:
    """
    Sintetiseer Rob Hubbard se wêreldberoemde C64 Commando-wysie (C mineur).
    Bevat vinnige 16de-noot funk baslyn, SID arpeggios en melodielyn!
    """
    bpm = 136.0
    beat_dur = 60.0 / bpm
    step_dur = beat_dur / 4.0  # 16de noot
    
    # 8 mate van 4/4 tyd = 32 maatslae = 128 stappe
    total_steps = 64
    duration = total_steps * step_dur
    total_samples = int(sample_rate * duration)
    samples = [0.0] * total_samples

    # C mineur nootwaardes
    C2, Eb2, F2, G2, Bb2 = 36, 39, 41, 43, 46
    C3, D3, Eb3, F3, G3 = 48, 50, 51, 53, 55
    C4, D4, Eb4, F4, G4, Ab4, Bb4 = 60, 62, 63, 65, 67, 68, 70
    C5, D5, Eb5 = 72, 74, 75

    # 1. Groovy 16th-Note SID Bass Pattern (Stem 1: Rob Hubbard Puls/Square)
    bass_pattern = [
        C2, C2, C3, C2,  Eb2, C2, F2, G2,
        C2, C2, C3, C2,  Bb2, G2, F2, Eb2,
        C2, C2, C3, C2,  Eb2, C2, F2, G2,
        G2, G2, Bb2, G2, F2, Eb2, D2 := 38, C2
    ] * 2

    # 2. Hoofmelodie (Stem 2: SID Driehoek/Pols met vibrato)
    # G4, C5, Bb4, Ab4, G4, F4, G4...
    melody_notes = [
        (0,  4, G4), (4,  2, G4), (6,  2, Ab4), (8,  6, G4), (14, 2, F4),
        (16, 4, Eb4),(20, 2, F4), (22, 2, G4),  (24, 8, C4),
        (32, 4, G4), (36, 2, C5), (38, 2, Bb4), (40, 4, Ab4),(44, 4, G4),
        (48, 4, F4), (52, 2, G4), (54, 2, Ab4), (56, 8, G4)
    ]

    # Syntheseer Baslyn
    step_samples = int(sample_rate * step_dur)
    for step_idx, note in enumerate(bass_pattern):
        start_samp = step_idx * step_samples
        f = note_freq(note)
        for s in range(step_samples):
            idx = start_samp + s
            if idx >= total_samples: break
            t = s / sample_rate
            env = math.exp(-12.0 * t) # Vinnige pluk
            # Pulse met veranderlike breedte (PWM)
            pwm = 0.5 + 0.3 * math.sin(2.0 * math.pi * 3.0 * (idx / sample_rate))
            phase = (t * f) % 1.0
            pulse = 1.0 if phase < pwm else -1.0
            samples[idx] += pulse * env * 0.32

    # Syntheseer Melodie
    for start_step, length_steps, note in melody_notes:
        start_samp = start_step * step_samples
        note_len_samp = length_steps * step_samples
        f = note_freq(note)
        for s in range(note_len_samp):
            idx = start_samp + s
            if idx >= total_samples: break
            t = s / sample_rate
            # Sagte mantel
            env = min(1.0, s / 200.0) * math.exp(-1.5 * t)
            # Vibrato
            vib = 1.0 + 0.015 * math.sin(2.0 * math.pi * 5.5 * t)
            phase = (t * f * vib) % 1.0
            # Gemengde driehoek/pols vir die klassieke Hubbard klank
            triangle = 4.0 * abs(phase - 0.5) - 1.0
            pulse = 1.0 if phase < 0.5 else -1.0
            samples[idx] += (0.6 * triangle + 0.4 * pulse) * env * 0.38

    # 3. Tromme (Noise snares op maatslae 2 en 4)
    for beat in range(0, total_steps // 4):
        if beat % 2 == 1: # Beats 2 en 4
            snare_start = int(beat * 4 * step_samples)
            for s in range(int(sample_rate * 0.15)):
                idx = snare_start + s
                if idx >= total_samples: break
                t = s / sample_rate
                env = math.exp(-24.0 * t)
                noise = (random.random() * 2.0 - 1.0)
                samples[idx] += noise * env * 0.22

    return generate_wave("commando_theme.wav", samples, sample_rate)


def generate_rob_hubbard_highscore_theme(sample_rate: int = 22050) -> str:
    """
    Sintetiseer Rob Hubbard se beroemde C64 Commando High Score / Game Over tema (Subtune 2).
    Liries, warm SID arpeggio-akkoorde en melodie in F-mineur.
    """
    bpm = 98.0
    beat_dur = 60.0 / bpm
    step_dur = beat_dur / 4.0  # 16de noot
    total_steps = 64
    duration = total_steps * step_dur
    total_samples = int(sample_rate * duration)
    samples = [0.0] * total_samples
    step_samples = int(sample_rate * step_dur)

    # Note in F mineur
    F2, G2, Ab2, Bb2, C3, Eb3, F3, G3, Ab3, Bb3 = 41, 43, 44, 46, 48, 51, 53, 55, 56, 58
    C4, Db4, Eb4, F4, G4, Ab4, Bb4, C5 = 60, 61, 63, 65, 67, 68, 70, 72

    # 4 mate: Fm -> Eb -> Db -> C
    chords = [
        [F2, C3, Ab3, C4],
        [39, Bb2, G3, Bb3],
        [37, Ab2, F3, Ab3],
        [36, G2, 52, G3],
    ]

    for bar in range(4):
        chord = chords[bar]
        for step in range(16):
            step_idx = bar * 16 + step
            start_samp = step_idx * step_samples
            note = chord[step % 4]
            f = note_freq(note)
            for s in range(step_samples):
                idx = start_samp + s
                if idx >= total_samples: break
                t = s / sample_rate
                env = math.exp(-10.0 * t)
                phase = (t * f) % 1.0
                triangle = 4.0 * abs(phase - 0.5) - 1.0
                samples[idx] += triangle * env * 0.22

    # Melodie vir High Score tema
    melody_notes = [
        (0,  6, C5), (6,  2, Bb4), (8,  4, Ab4), (12, 4, G4),
        (16, 6, Bb4),(22, 2, Ab4), (24, 4, G4),  (28, 4, F4),
        (32, 6, Ab4),(38, 2, G4),  (40, 4, F4),  (44, 4, Eb4),
        (48, 8, G4), (56, 8, F4)
    ]

    for start_step, length_steps, note in melody_notes:
        start_samp = start_step * step_samples
        note_len_samp = length_steps * step_samples
        f = note_freq(note)
        for s in range(note_len_samp):
            idx = start_samp + s
            if idx >= total_samples: break
            t = s / sample_rate
            env = min(1.0, s / 300.0) * math.exp(-0.8 * t)
            vib = 1.0 + 0.018 * math.sin(2.0 * math.pi * 5.0 * t)
            phase = (t * f * vib) % 1.0
            pulse = 1.0 if phase < 0.45 else -1.0
            triangle = 4.0 * abs(phase - 0.5) - 1.0
            samples[idx] += (0.5 * triangle + 0.5 * pulse) * env * 0.35

    return generate_wave("commando_highscore.wav", samples, sample_rate)


class SoundManager:
    _instance = None

    def __init__(self):
        self.sound_paths: Dict[str, str] = {}
        self.enabled = True
        self.music_process: Optional[subprocess.Popen] = None
        self.music_thread: Optional[threading.Thread] = None
        self.is_playing_music = False
        self.current_track: Optional[str] = None
        self._init_sounds()

    def _init_sounds(self):
        self.sound_paths["shoot"] = generate_sid_shoot()
        self.sound_paths["explosion"] = generate_sid_explosion()
        self.sound_paths["grenade_throw"] = generate_sid_grenade_throw()
        self.sound_paths["enemy_hit"] = generate_sid_enemy_hit()
        self.sound_paths["rescue"] = generate_sid_rescue()
        self.sound_paths["pickup"] = generate_sid_pickup()
        self.sound_paths["victory"] = generate_sid_victory()
        self.sound_paths["theme"] = generate_rob_hubbard_theme()
        self.sound_paths["highscore"] = generate_rob_hubbard_highscore_theme()

    def play(self, sound_name: str, volume: float = 0.5):
        if not self.enabled:
            return
        path = self.sound_paths.get(sound_name)
        if path and os.path.exists(path):
            try:
                subprocess.Popen(
                    ["/usr/bin/afplay", "-v", str(volume), path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except Exception:
                pass

    def start_music(self, track_name: str = "theme", volume: float = 0.4):
        """Begin deurlopende herhaling van 'n Rob Hubbard klankbaan ('theme' of 'highscore')."""
        if not self.enabled:
            return
        if self.is_playing_music and self.current_track == track_name:
            return
        self.stop_music()

        theme_path = self.sound_paths.get(track_name)
        if not theme_path or not os.path.exists(theme_path):
            return

        self.current_track = track_name
        self.is_playing_music = True

        def music_loop():
            while self.is_playing_music:
                try:
                    self.music_process = subprocess.Popen(
                        ["/usr/bin/afplay", "-v", str(volume), theme_path],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                    self.music_process.wait()
                except Exception:
                    break

        self.music_thread = threading.Thread(target=music_loop, daemon=True)
        self.music_thread.start()

    def stop_music(self):
        """Stop die agtergrondmusiek."""
        self.is_playing_music = False
        self.current_track = None
        if self.music_process:
            try:
                self.music_process.terminate()
            except Exception:
                pass
            self.music_process = None

sounds = SoundManager()
