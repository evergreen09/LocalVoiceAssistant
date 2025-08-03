import os
import edge_tts
from playsound3 import playsound

def text_to_voice(text: str):
    voice = "af-ZA-AdriNeural"
    tts = edge_tts.Communicate(text, voice)
    tts.save_sync('temp_tts.mp3')
    
    # Play TTS voice
    playsound('temp_tts.mp3', backend='afplay')
