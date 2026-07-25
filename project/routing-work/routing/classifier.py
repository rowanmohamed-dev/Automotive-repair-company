import os
import time
from dotenv import load_dotenv

from categories import (
    CATEGORIES,
    get_workflow,
    infer_category_from_text,
    is_valid_category,
)

load_dotenv()

try:
    from google import genai
except ImportError:
    genai = None

CLIENT = None
if genai is not None and os.getenv("GEMINI_API_KEY"):
    CLIENT = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL = "gemini-flash-latest"
MAX_RETRIES = 2
DEFAULT_CATEGORY = "OTHER"


def build_prompt(complaint: str) -> str:
    categories = "\n".join(CATEGORIES)

    return f"""
You are an intent classifier for a Vehicle Repair Assistant.

Classify the customer's complaint into exactly ONE of the following categories:

{categories}

Customer Complaint:
"{complaint}"

Rules:
- Return only one category.
- Use uppercase.
- Do not explain your answer.
- Do not add punctuation or extra words.
"""


def call_model(prompt: str) -> dict:
    if CLIENT is None:
        return {
            "text": "",
            "input_tokens": 0,
            "output_tokens": 0,
        }

    response = CLIENT.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    usage = getattr(response, "usage_metadata", None)

    return {
        "text": response.text.strip().upper(),
        "input_tokens": getattr(usage, "prompt_token_count", 0) or 0,
        "output_tokens": getattr(usage, "candidates_token_count", 0) or 0,
    }


def classify(complaint: str) -> dict:
    prompt = build_prompt(complaint)

    raw_response = ""
    total_input_tokens = 0
    total_output_tokens = 0
    calls_made = 0

    for attempt in range(MAX_RETRIES + 1):

        result = call_model(prompt)

        raw_response = result["text"]
        total_input_tokens += result["input_tokens"]
        total_output_tokens += result["output_tokens"]
        calls_made += 1

        if CLIENT is not None and is_valid_category(raw_response):
            return {
                "category": raw_response,
                "raw_response": raw_response,
                "workflow": get_workflow(raw_response),
                "retries_used": attempt,
                "calls_made": calls_made,
                "input_tokens": total_input_tokens,
                "output_tokens": total_output_tokens,
            }

        if CLIENT is None:
            category = infer_category_from_text(complaint)
            return {
                "category": category,
                "raw_response": category,
                "workflow": get_workflow(category),
                "retries_used": 0,
                "calls_made": 0,
                "input_tokens": 0,
                "output_tokens": 0,
            }

        prompt = f"""
Your previous answer "{raw_response}" is invalid.

You must return exactly one of these categories:

{", ".join(CATEGORIES)}

Customer Complaint:
"{complaint}"

Return only the category name.
"""

        time.sleep(1)

    return {
        "category": DEFAULT_CATEGORY,
        "raw_response": raw_response,
        "workflow": get_workflow(DEFAULT_CATEGORY),
        "retries_used": MAX_RETRIES,
        "calls_made": calls_made,
        "input_tokens": total_input_tokens,
        "output_tokens": total_output_tokens,
    }


if __name__ == "__main__":

    test_complaints = [
        "My brakes are making a grinding noise.",
        "The engine keeps overheating.",
        "The transmission is slipping.",
        "My battery is dead.",
        "The exhaust is producing black smoke.",
        "The headlights are very dim.",
        "The tire is flat.",
        "I want a refund.",
    ]

    for complaint in test_complaints:

        result = classify(complaint)

        print("-" * 60)
        print(f"Complaint: {complaint}")
        print(f"Category: {result['category']}")
        print(f"Workflow: {result['workflow']}")
        print(f"Retries: {result['retries_used']}")
        print(f"Calls: {result['calls_made']}")
        print(f"Tokens: Input={result['input_tokens']} | Output={result['output_tokens']}")