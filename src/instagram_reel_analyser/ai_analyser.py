import requests
import json
import os
from rich.console import Console

from src.instagram_reel_analyser import constants, console_styles

console = Console(force_terminal=True)


def analyse_transcript(transcript_text_list):
    console.print("[INFO] Starting AI transcript analysis...", style=console_styles.console_blue_styles)
    ollama_url = constants.OLLAMA_URL
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(base_dir, constants.PROMPT_FILE_NAME)
    try:
        with open(prompt_path, "r", encoding="utf-8") as file:
            prompt_template = file.read()
        prompt = prompt_template.replace(constants.PROMPT_TEXT_REEL_PLACEHOLDER, transcript_text_list[0])
        prompt = prompt.replace(constants.PROMPT_TEXT_COMPARE_REEL_PLACEHOLDER, transcript_text_list[1])
        response = requests.post(ollama_url,
                      json={
                          "model": constants.MODEL_NAME,
                          "prompt": prompt,
                          "stream": True
                      },
                      stream=True
                      )
        ai_response = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if "response" in data:
                    ai_response += data["response"]
        analysis_path = os.path.join(base_dir, "ai_analysis.txt")
        with open(analysis_path, "w", encoding="utf-8") as file:
            file.write(ai_response)
        console.print(f"[SUCCESS] AI analysis complete. Results saved to {analysis_path}", style=console_styles.console_green_styles)
    except Exception as e:
        console.print(f"[ERROR] Failed to analyse transcript: {e}", style=console_styles.console_red_styles)
