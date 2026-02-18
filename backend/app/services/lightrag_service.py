from lightrag import LightRAG, QueryParam
from lightrag.llm.openai import openai_complete_if_cache, openai_embed
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.utils import EmbeddingFunc
from app.core.config import get_settings
from app.core.openrouter_llm import openrouter_model_if_cache
from app.core.vnpay_llm import vnpay_model_if_cache
from loguru import logger
import os
import numpy as np

settings = get_settings()


def get_local_embedding_func():
    """
    Local embedding using sentence-transformers.
    Runs on M1 Mac CPU - no API key needed, completely FREE!
    Model: BAAI/bge-small-en-v1.5 (384-dim, fast & lightweight)
    """
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("BAAI/bge-small-en-v1.5")
    
    async def embed(texts: list[str]) -> np.ndarray:
        embeddings = model.encode(texts, normalize_embeddings=True)
        return embeddings
    
    return EmbeddingFunc(
        embedding_dim=384,
        max_token_size=512,
        func=embed,
    )


class LightRAGService:
    def __init__(self):
        self.rag = None
        self._initialized = False
        self._build_rag()
    
    async def initialize(self):
        """Must be called before first use - initializes storages"""
        if not self._initialized:
            await self.rag.initialize_storages()
            self._initialized = True
    
    def _build_rag(self):
        """Initialize LightRAG with appropriate mode and provider"""
        os.makedirs(settings.WORKING_DIR, exist_ok=True)
        
        if settings.LIGHTRAG_MODE == "local":
            if settings.LLM_PROVIDER == "openrouter":
                logger.info("🏠 Initializing LightRAG in LOCAL mode with OPENROUTER")
                logger.info(f"   Model: {settings.OPENROUTER_MODEL}")
                logger.info("   📦 Embeddings: local sentence-transformers (FREE, no API needed)")
                
                self.rag = LightRAG(
                    working_dir=settings.WORKING_DIR,
                    llm_model_func=openrouter_model_if_cache,
                    llm_model_name=settings.OPENROUTER_MODEL,
                    llm_model_max_async=2,  # Limit concurrent calls for free tier
                    llm_model_kwargs={
                        "temperature": 0.7,
                        "max_tokens": 2048,
                        "model_name": settings.OPENROUTER_MODEL,
                    },
                    embedding_func=get_local_embedding_func(),
                )
            elif settings.LLM_PROVIDER == "vnpay":
                logger.info("🏠 Initializing LightRAG in LOCAL mode with VNPAY AI GATEWAY")
                logger.info(f"   Model: {settings.VNPAY_MODEL}")
                logger.info(f"   URL: {settings.VNPAY_BASE_URL}")

                self.rag = LightRAG(
                    working_dir=settings.WORKING_DIR,
                    llm_model_func=vnpay_model_if_cache,
                    llm_model_name=settings.VNPAY_MODEL,
                    llm_model_max_async=4,
                    llm_model_kwargs={
                        "temperature": 0.7,
                        "max_tokens": 2048,
                        "model_name": settings.VNPAY_MODEL,
                    },
                    embedding_func=get_local_embedding_func(),
                )
            else:
                # OpenAI fallback
                logger.info("🏠 Initializing LightRAG in LOCAL mode with OPENAI")
                logger.info(f"   Model: {settings.OPENAI_MODEL}")
                
                embedding_func = EmbeddingFunc(
                    embedding_dim=1536,
                    max_token_size=8192,
                    func=lambda texts: openai_embed(
                        texts,
                        model=settings.OPENAI_EMBEDDING_MODEL,
                        api_key=settings.OPENAI_API_KEY,
                    )
                )
                
                self.rag = LightRAG(
                    working_dir=settings.WORKING_DIR,
                    llm_model_func=openai_complete_if_cache,
                    llm_model_name=settings.OPENAI_MODEL,
                    embedding_func=embedding_func,
                )
        else:
            # RunPod mode - use Ollama
            logger.info("☁️ Initializing LightRAG in RUNPOD mode (Ollama)")
            logger.info(f"   Ollama URL: {settings.OLLAMA_BASE_URL}")
            logger.info(f"   Model: {settings.OLLAMA_MODEL}")
            
            embedding_func = EmbeddingFunc(
                embedding_dim=1024,  # bge-m3
                max_token_size=8192,
                func=lambda texts: ollama_embed(
                    texts,
                    embed_model=settings.EMBEDDING_MODEL,
                    host=settings.OLLAMA_BASE_URL,
                )
            )
            
            self.rag = LightRAG(
                working_dir=settings.WORKING_DIR,
                llm_model_func=ollama_model_complete,
                llm_model_name=settings.OLLAMA_MODEL,
                llm_model_kwargs={
                    "host": settings.OLLAMA_BASE_URL,
                    "options": {"num_ctx": 32768}
                },
                embedding_func=embedding_func,
            )
    
    async def insert_documents(self, documents: list[str]) -> dict:
        """Insert documents into LightRAG"""
        await self.initialize()
        try:
            for doc in documents:
                await self.rag.ainsert(doc)
            return {"status": "success", "count": len(documents)}
        except Exception as e:
            logger.error(f"Error inserting documents: {e}")
            raise
    
    async def query(
        self, 
        question: str, 
        mode: str = "hybrid"
    ) -> dict:
        """Query LightRAG
        
        Args:
            question: User question
            mode: naive, local, global, hybrid
        """
        await self.initialize()
        try:
            result = await self.rag.aquery(
                question,
                param=QueryParam(mode=mode)
            )
            # Handle None result (empty database - no documents ingested yet)
            if result is None or result == "":
                result = "⚠️ Chưa có dữ liệu trong hệ thống. Vui lòng chạy `python scripts/ingest.py` để load documents trước."
            return {
                "question": question,
                "answer": str(result),
                "mode": mode,
                "provider": settings.LLM_PROVIDER
            }
        except Exception as e:
            logger.error(f"Error querying: {e}")
            raise


# Singleton instance
lightrag_service = LightRAGService()

