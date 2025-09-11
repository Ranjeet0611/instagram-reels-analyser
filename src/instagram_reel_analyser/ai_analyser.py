import requests
import json
import os


def analyse_transcript(transcript):
    ollama_url = "http://localhost:11434/api/generate"
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(base_dir, "prompt.txt")
    with open(prompt_path, "r", encoding="utf-8") as file:
        prompt_template = file.read()
    prompt = prompt_template.replace("{{REEL_TEXT}}", transcript)
    response = requests.post(ollama_url,
                  json={
                      "model": "llama3.2",
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
