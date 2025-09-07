import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import whisper

def transcribe_audio(file_path):
    model = whisper.load_model("large")
    result = model.transcribe(file_path,language="en")
    return result["text"]

