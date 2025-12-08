from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from common.db import get_db
from common.llm import extract_parameters_llm, generate_response
from common.query_service import query_orders
from common.schema_utils import get_schema_info

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/query")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        schema = get_schema_info()
        params = extract_parameters_llm(request.query, schema)
        results = query_orders(params.get("filters", {}), db)
        answer = generate_response(request.query, results)
        return {"answer": answer}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
