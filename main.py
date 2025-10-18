import argparse

from src.instagram_reel_analyser import reels, video_audio, transcriber, ai_analyser


def main():
    parser = argparse.ArgumentParser(description="Compare your Instagram reels using AI")
    parser.add_argument("-u", "--url", help="URL of the Instagram reel to download")
    parser.add_argument("-cu", "--compare_url", help="URL of the Instagram reel to compare")
    args = parser.parse_args()
    reels.download_instagram_reel(args.url, args.compare_url)
    audio_output_files_path = video_audio.convert_mp4_to_mp3()
    transcribed_text_list = transcriber.transcribe_audio(audio_output_files_path)
    ai_analyser.analyse_transcript(transcribed_text_list)


if __name__ == "__main__":
    main()
