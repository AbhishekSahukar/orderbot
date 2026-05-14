import traceback

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from common.db import get_db
from common.llm import extract_parameters, generate_response
from common.query_service import query_orders
from common.schema_utils import get_schema_info

router = APIRouter()


class ChatRequest(BaseModel):
    query: str


@router.post("/query")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        schema = get_schema_info()
        params = extract_parameters(request.query, schema)
        orders = query_orders(params.get("filters", {}), db)
        answer = generate_response(request.query, orders)
        return {"answer": answer}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))