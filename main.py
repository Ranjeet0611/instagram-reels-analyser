import argparse

from src.instagram_reel_analyser import reels, video_audio, transcriber
def main():
    parser = argparse.ArgumentParser(description="Analyse Instagram reels using AI")
    parser.add_argument("reel_url", help="URL of the Instagram reel to download")
    args = parser.parse_args()
    reels.download_instagram_reel(args.reel_url)
    audio_url = video_audio.convert_audio_to_video()
    text = transcriber.transcribe_audio(audio_url)
    print(text)

if __name__ == "__main__":
    main()
