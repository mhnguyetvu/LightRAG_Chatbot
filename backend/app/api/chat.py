from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.lightrag_service import lightrag_service
from loguru import logger

router = APIRouter()


class QueryRequest(BaseModel):
    question: str
    mode: str = "hybrid"  # naive, local, global, hybrid


class QueryResponse(BaseModel):
    question: str
    answer: str
    mode: str


class InsertRequest(BaseModel):
    documents: list[str]


class InsertResponse(BaseModel):
    status: str
    count: int


@router.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query documents using LightRAG"""
    try:
        logger.info(f"📝 Query: {request.question} (mode: {request.mode})")
        result = await lightrag_service.query(
            question=request.question,
            mode=request.mode
        )
        return result
    except Exception as e:
        logger.error(f"Query error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/insert", response_model=InsertResponse)
async def insert_documents(request: InsertRequest):
    """Insert documents into LightRAG"""
    try:
        logger.info(f"📥 Inserting {len(request.documents)} documents")
        result = await lightrag_service.insert_documents(request.documents)
        return result
    except Exception as e:
        logger.error(f"Insert error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "lightrag"}
