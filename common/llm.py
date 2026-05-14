import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv(
    "OPENROUTER_BASE_URL",
    "https://openrouter.ai/api/v1/chat/completions",
)
LLM_MODEL = os.getenv("LLM_MODEL", "minimax/minimax-m2.5")

if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY is not set. Add it to your .env file.")


def _call_llm(messages: list[dict]) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"model": LLM_MODEL, "messages": messages}
    response = requests.post(OPENROUTER_BASE_URL, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]


def extract_parameters(user_query: str, schema: dict) -> dict:
    """Ask the LLM to extract database filters from a natural language query."""
    messages = [
        {
            "role": "system",
            "content": (
                "You extract database query filters from a user's question. "
                "Reply with a JSON object only — no markdown, no explanation. "
                'Example: {"filters": {"customer": "Bob", "status": "SHIPPED"}}'
            ),
        },
        {
            "role": "user",
            "content": f"Schema: {json.dumps(schema)}\n\nUser query: {user_query}",
        },
    ]
    raw = _call_llm(messages)
    try:
        # Strip accidental markdown fences
        clean = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        return json.loads(clean)
    except (json.JSONDecodeError, ValueError):
        return {"filters": {}}


def generate_response(user_query: str, orders: list) -> str:
    """Turn database results into a friendly natural language answer."""
    if not orders:
        return "I couldn't find any orders matching your request. Try asking with a different name, product, or status."

    structured = [
        {
            "order_id": o.id,
            "customer": o.customer.name,
            "product": o.product,
            "status": o.status,
        }
        for o in orders
    ]

    messages = [
        {
            "role": "system",
            "content": (
                "You are a friendly order tracking assistant. "
                "Answer the user's question using only the database results provided. "
                "Be concise and conversational. "
                "If one order matches, describe it briefly. "
                "If multiple orders match, summarise them clearly. "
                "Never invent customer names, products, or statuses — use only what is in the data."
            ),
        },
        {
            "role": "user",
            "content": (
                f"User question: {user_query}\n\n"
                f"Database results:\n{json.dumps(structured, indent=2)}"
            ),
        },
    ]

    return _call_llm(messages).strip()