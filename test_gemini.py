import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = os.getenv("GEMINI_MODEL")

print(f"Testing model: {model}")

try:
    response = client.models.generate_content(
        model=model,
        contents="Write a short Instagram caption about learning Python."
    )

    print("\nSUCCESS! Gemini API is working.")
    print(response.text)

except Exception as error:
    print("\nAPI ERROR:")
    print(error)