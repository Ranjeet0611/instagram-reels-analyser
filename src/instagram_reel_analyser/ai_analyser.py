from os import write

import requests
import json
import os

from src.instagram_reel_analyser import constants


def analyse_transcript(transcript):
    ollama_url = constants.OLLAMA_URL
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(base_dir, constants.PROMPT_FILE_NAME)
    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt_template = file.read()
    prompt = prompt_template.replace(constants.PROMPT_TEXT_PLACEHOLDER, transcript)
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
                print(data["response"], end="", flush=True)
    analysis_path = os.path.join(base_dir, "ai_analysis.txt")
    with open(analysis_path, "w", encoding="utf-8") as file:
        file.write(ai_response)


