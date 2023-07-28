from dotenv import load_dotenv
from elevenlabs import set_api_key
import os
import requests

load_dotenv()
API_KEY = os.getenv('ELEVEN_LABS_API_KEY')

if API_KEY is not None:
    set_api_key(API_KEY)

"""
def get_all_voices():
    url = "https://api.elevenlabs.io/v1/voices"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        data = response.json()

        # Extract voice_id and name for each voice
        # voices = [(voice["voice_id"], voice["name"]) for voice in data]

        return data

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


all_voices = get_all_voices()
# print(all_voices)
"""


voice_id = "21m00Tcm4TlvDq8ikWAM"
CHUNK_SIZE = 1024
url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": API_KEY
}

text="Hi! My name is Bella, nice to meet you!I'm powered by AI, so surprises and mistakes are possible. Make sure to verify any generated code or suggestions, and share feedback so that we can learn and improve.Welcome @puneetmpatil, I'm your Copilot and I'm here to help you get things done faster. I can identify issues, explain and even improve code.GitHub Copilot is an AI-powered code assistant that helps developers write better code, faster. It is built on top of OpenAI's GPT-3 language model and uses machine learning to suggest code snippets and completions based on the context of the code being written.Copilot can be used in a variety of programming languages and integrated development environments (IDEs), including Visual Studio Code. It can suggest entire functions, classes, and even entire files based on the context of the code being written."

data = {
    "text": text,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
    }
}

response = requests.post(url, json=data, headers=headers, stream=True)

with open('output.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)

