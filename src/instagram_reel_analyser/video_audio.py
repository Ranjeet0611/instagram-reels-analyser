import concurrent
import os
from concurrent.futures import ThreadPoolExecutor
from moviepy import VideoFileClip
from rich.console import Console
from src.instagram_reel_analyser import console_styles

console = Console(force_terminal=True)

def get_mp4_file_in_current_dir():
    all_files = []
    console.print("[INFO] Searching for mp4 files in current directory...", style=console_styles.console_blue_styles)
    for dirpath, dirnames, filenames in os.walk(os.curdir):
        for file in filenames:
            if file.lower().endswith('.mp4'):
                all_files.append(os.path.abspath(os.path.join(dirpath, file)))
    if all_files:
        console.print(f"[SUCCESS] Found {len(all_files)} mp4 file(s).", style=console_styles.console_green_styles)
    else:
        console.print("[WARNING] No mp4 files found in the current directory.", style=console_styles.console_yellow_styles)
    return all_files

def convert_to_audio(video_file, output_file):
    console.print(f"[INFO] Extracting audio from: {video_file}", style=console_styles.console_blue_styles)
    try:
        video = VideoFileClip(video_file)
        audio = video.audio
        audio.write_audiofile(output_file)
        audio.close()
        video.close()
        console.print(f"[SUCCESS] Audio extracted and saved as '{output_file}'", style=console_styles.console_green_styles)
        return output_file
    except Exception as e:
        console.print(f"[ERROR] Failed to extract audio from {video_file}: {e}", style=console_styles.console_red_styles)
        return None

def convert_mp4_to_mp3():
    console.print("[INFO] Converting mp4 to mp3...", style=console_styles.console_blue_styles)
    all_video_files = get_mp4_file_in_current_dir()
    output_files_path = []
    if len(all_video_files) == 0:
        return None
    with ThreadPoolExecutor() as executor:
        futures = []
        for video_file in all_video_files:
            futures.append(executor.submit(convert_to_audio, video_file, video_file.split(".")[0]+".mp3"))
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                output_files_path.append(result)
    if output_files_path:
        console.print(f"[SUCCESS] Converted {len(output_files_path)} file(s) to mp3.", style=console_styles.console_green_styles)
    else:
        console.print("[WARNING] No files were converted to mp3.", style=console_styles.console_yellow_styles)
    return output_files_path
