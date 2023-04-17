import os
import wave
import pyaudio

# Define the directory where the phoneme sound files are located
SOUNDS_DIR = 's'

# Define a dictionary that maps each phoneme to its sound file path
PHONEME_SOUND_MAP = {}
for filename in os.listdir(SOUNDS_DIR):
    if filename.endswith('.wav'):
        phoneme = filename[:-4]  # Remove the '.wav' extension
        sound_file_path = os.path.join(SOUNDS_DIR, filename)
        PHONEME_SOUND_MAP[phoneme] = sound_file_path

def play_phoneme_list(phoneme_list):
    # Concatenate the sounds corresponding to each phoneme in the list
    audio_data = b''
    for phoneme in phoneme_list:
        with wave.open(PHONEME_SOUND_MAP[phoneme], 'rb') as wav_file:
            audio_data += wav_file.readframes(wav_file.getnframes())

    # Play the resulting sound using PyAudio
    if audio_data:
        audio = pyaudio.PyAudio()
        stream = audio.open(format=audio.get_format_from_width(wav_file.getsampwidth()),
                            channels=wav_file.getnchannels(),
                            rate=wav_file.getframerate(),
                            output=True)
        stream.write(audio_data)
        # stream.close()
        # audio.terminate()





