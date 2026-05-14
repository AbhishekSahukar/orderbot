import json
import os

import requests
from dotenv import load_dotenv

# --------------------------------------------------
# Environment
# --------------------------------------------------
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv(
    "OPENROUTER_BASE_URL",
    "https://openrouter.ai/api/v1/chat/completions",
)
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek/deepseek-chat")

if not OPENROUTER_API_KEY:
    raise RuntimeError("Missing OPENROUTER_API_KEY")

# --------------------------------------------------
# Low-level OpenRouter call
# --------------------------------------------------
def _call_llm(messages):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:8000",
        "X-Title": "OrderBot",
    }

    payload = {
        "model": LLM_MODEL,
        "messages": messages,
        "temperature": 0,
        "max_tokens": 500,
    }

    response = requests.post(
        OPENROUTER_BASE_URL,
        headers=headers,
        json=payload,
        timeout=30,
    )

    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


# --------------------------------------------------
# LLM-assisted filter extraction
# (unchanged behavior, safe fallback)
# --------------------------------------------------
def extract_parameters_llm(user_query: str, schema: dict) -> dict:
    """
    Attempts to extract filters using LLM.
    Always returns: { "filters": { ... } }
    Never raises.
    """

    prompt = [
        {
            "role": "system",
            "content": (
                "Extract filters from the user query.\n"
                "Allowed keys: customer, product, status.\n"
                "Return ONLY valid JSON in this format:\n"
                "{ \"filters\": { \"customer\": \"Bob Smith\" } }\n"
                "If nothing is found, return { \"filters\": {} }.\n"
                "Do not add explanations or markdown."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Query: {user_query}\n\n"
                f"Schema: {json.dumps(schema)}"
            ),
        },
    ]

    try:
        raw = _call_llm(prompt)

        # Strip markdown if present
        if "```" in raw:
            raw = raw.split("```")[1].strip()

        data = json.loads(raw)
        return data if isinstance(data, dict) else {"filters": {}}

    except Exception:
        # IMPORTANT: Never crash the app
        return {"filters": {}}


# --------------------------------------------------
# FINAL, LOCKED response formatting
# (this is the only behavior change you asked for)
# --------------------------------------------------
def generate_response(user_query: str, orders: list) -> str:
    """
    Deterministic formatter.
    Does NOT change logic or intent handling.
    Only formats DB results.
    """

    if not orders:
        return "I couldn't find any orders matching your request. Try asking with a different name, product, or status."

    customer_name = orders[0].customer.name
    total = len(orders)

    lines = [f"{customer_name} has {total} order{'s' if total != 1 else ''}:"]

    for o in orders:
        lines.append(
            f"- Order #{o.id} ({o.product}) — {o.status.upper()}"
        )

    return "\n".join(lines)
