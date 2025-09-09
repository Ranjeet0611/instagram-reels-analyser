import os

from moviepy import VideoFileClip
from rich.console import Console

console = Console(force_terminal=True)
def get_mp4_file_in_current_dir():
    for dirpath, dirnames, filenames in os.walk(os.curdir):
        for file in filenames:
            if file.lower().endswith('.mp4'):
                return os.path.abspath(os.path.join(dirpath, file))
    return None

def convert_mp4_to_mp3():
    audio_file = get_mp4_file_in_current_dir()
    if audio_file is not None:
        video = VideoFileClip(audio_file)
        audio = video.audio
        audio.write_audiofile("extracted_audio.mp3")
        audio.close()
        video.close()
        console.print("Audio extracted and saved as 'extracted_audio.mp3'", style="bold green")
    return os.path.abspath("extracted_audio.mp3")

