from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from common.db import get_db
from common.llm import extract_parameters, generate_response
from common.query_service import query_orders
from common.schema_utils import get_schema_info
from common.name_utils import extract_name_fallback

router = APIRouter()


class ChatRequest(BaseModel):
    query: str


@router.post("/query")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    schema = get_schema_info()

    # Step 1: Try LLM extraction (as before)
    params = extract_parameters_llm(request.query, schema) or {}
    filters = params.get("filters", {}) or {}

    # Step 2: GUARANTEE customer name if present in sentence
    # (This is what DeepSeek was implicitly doing before)
    if "customer" not in filters or not filters["customer"]:
        name = extract_name_fallback(request.query)
        if name:
            filters["customer"] = name

    # Step 3: Query DB
    results = query_orders(filters, db)

    # Step 4: Generate response
    answer = generate_response(request.query, results)
    return {"answer": answer}
