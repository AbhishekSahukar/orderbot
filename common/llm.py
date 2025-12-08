import os
import json
import requests
from dotenv import load_dotenv

# 🔹 Load environment variables
load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1/chat/completions")
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek/deepseek-chat")

if not OPENROUTER_API_KEY:
    raise RuntimeError("❌ Missing OPENROUTER_API_KEY in environment")

# 🔹 Low-level call to OpenRouter
def _call_llm(messages):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"model": LLM_MODEL, "messages": messages}
    response = requests.post(OPENROUTER_BASE_URL, headers=headers, data=json.dumps(payload))
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# 🔹 Extract structured filters
def extract_parameters_llm(user_query: str, schema: dict):
    prompt = [
        {"role": "system", "content": "Extract filters from the user query that match schema. Output JSON only."},
        {"role": "user", "content": f"Query: {user_query}\nSchema: {schema}"}
    ]
    raw = _call_llm(prompt)
    try:
        return json.loads(raw)
    except:
        return {"filters": {}}

# 🔹 Generate response (DB → NL, no hardcoding)
def generate_response(user_query: str, orders: list):
    if not orders:
        return "I couldn’t find any orders matching your request."

    # ✅ Always build from DB values
    structured_info = [
        {
            "order_id": o.id,
            "customer": o.customer.name,
            "product": o.product,
            "status": o.status
        }
        for o in orders
    ]

    prompt = [
        {"role": "system", "content": (
            "You are an assistant answering customer order queries. "
            "Use only the database results provided. "
            "Always respond in short, natural conversational English. "
            "If one order matches, state it clearly. "
            "If multiple orders match, summarize them naturally. "
            "⚠️ Do not hallucinate names or products — only use DB values."
        )},
        {"role": "user", "content": f"User query: {user_query}\nDatabase results: {json.dumps(structured_info, indent=2)}"}
    ]

    return _call_llm(prompt).strip()
