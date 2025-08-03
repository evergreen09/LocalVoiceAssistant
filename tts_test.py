import os
import edge_tts

text = "Hello World!"

voice = "af-ZA-AdriNeural"

tts = edge_tts.Communicate(text, voice)

output = 'test_tts.mp3'
tts.save_sync(output)

#os.system(f'start {output}')

from playsound3 import playsound

playsound("test_tts.mp3", backend='afplay')
