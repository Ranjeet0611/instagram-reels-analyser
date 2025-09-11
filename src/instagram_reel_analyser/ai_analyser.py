import requests
import json
import os
import constants

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
    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            if "response" in data:
                print(data["response"], end="", flush=True)
