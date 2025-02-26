import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content

load_dotenv()


if "GEMINI_API_KEY" not in os.environ:
    raise ValueError("GEMINI_API_KEY is missing!")

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_schema": content.Schema(
        type=content.Type.OBJECT,
        properties={
            "activity": content.Schema(
                type=content.Type.ARRAY,
                items=content.Schema(type=content.Type.STRING),
            ),
            "best-season": content.Schema(
                type=content.Type.ARRAY,
                items=content.Schema(type=content.Type.STRING),
            ),
            "amount-of-time": content.Schema(
                type=content.Type.ARRAY,
                items=content.Schema(
                    type=content.Type.OBJECT,
                    properties={
                        "activity": content.Schema(
                            type=content.Type.ARRAY,
                            items=content.Schema(type=content.Type.STRING),
                        ),
                        "time": content.Schema(
                            type=content.Type.ARRAY,
                            items=content.Schema(type=content.Type.STRING),
                        ),
                    },
                ),
            ),
        },
    ),
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", generation_config=generation_config
)

chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                "Here is an article about exciting things to do in New York City..."
            ],
        },
        {
            "role": "model",
            "parts": [
                "{\"activity\": [\"Exploring Central Park\", ... ]}"
            ],
        },
    ]
)