import concurrent
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import whisper
from concurrent.futures import ThreadPoolExecutor
from rich.console import Console
from src.instagram_reel_analyser import console_styles

console = Console(force_terminal=True)

def transcribe(file_path):
    console.print(f"[INFO] Transcribing file: {file_path}", style=console_styles.console_blue_styles)
    try:
        model = whisper.load_model("large")
        result = model.transcribe(audio=file_path, language="en")
        console.print(f"[SUCCESS] Transcription complete for: {file_path}", style=console_styles.console_green_styles)
        return result["text"]
    except Exception as e:
        console.print(f"[ERROR] Failed to transcribe {file_path}: {e}", style=console_styles.console_red_styles)
        return ""

def transcribe_audio(audio_output_file_path):
    transcribed_text = []
    console.print("[INFO] Starting batch audio transcription...", style=console_styles.console_blue_styles)
    with ThreadPoolExecutor() as executor:
        futures = []
        for audio_file in audio_output_file_path:
            futures.append(executor.submit(transcribe, audio_file))
        for future in concurrent.futures.as_completed(futures):
            transcribed_text.append(future.result())
    save_transcribed_texts(transcribed_text, "transcribed_texts.txt")
    console.print("[SUCCESS] All audio files transcribed.", style=console_styles.console_green_styles)
    return transcribed_text

def save_transcribed_texts(transcribed_texts, file_path):
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            for text in transcribed_texts:
                f.write(text + "\n")
        console.print(f"[SUCCESS] Transcribed texts saved to {file_path}", style=console_styles.console_green_styles)
    except Exception as e:
        console.print(f"[ERROR] Failed to save transcribed texts: {e}", style=console_styles.console_red_styles)
