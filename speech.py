from openai import OpenAI
import os
from dotenv import load_dotenv
import speech_recognition as sr
from pydub import AudioSegment

load_dotenv()

r = sr.Recognizer()

mic = sr.Microphone()

client = OpenAI(api_key=os.getenv("OPEN_AI_API_KEY"))

def text_to_speech(prompt):
    with client.audio.speech.with_streaming_response.create(
        model="tts-1",
        voice="alloy",
        input=prompt,
    ) as response:
        response.stream_to_file("korean.mp3")

def speech_to_text(file_name):
    audio_file = open(f"{file_name}", "rb")
    transcription = client.audio.transcriptions.create(
        model="whisper-1", 
        file=audio_file, 
        response_format="text"
    )
    print(transcription)

# 음성 녹음 함수
def record_audio():
    with mic as source:
        print("Start")
        audio_data = r.listen(source)
        print("END")
        return audio_data

if __name__ == "__main__":
    '''# 음성 녹음
    audio_data = record_audio()

    # 오디오 파일로 저장
    with open("sample.wav", "wb") as f:
        f.write(audio_data.get_wav_data())'''
    speech_to_text('sample.wav')
