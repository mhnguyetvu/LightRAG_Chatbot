"""
Gemini LLM wrapper for LightRAG
Provides compatibility layer between Google Gemini API and LightRAG
"""
import os
from typing import Any
import google.generativeai as genai
from loguru import logger


def gemini_complete(
    prompt: str,
    model: str = "gemini-1.5-flash",
    **kwargs
) -> str:
    """
    Complete text using Gemini API
    
    Args:
        prompt: Input prompt
        model: Gemini model name
        **kwargs: Additional arguments (temperature, max_tokens, etc.)
    
    Returns:
        Generated text
    """
    try:
        # Configure Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        genai.configure(api_key=api_key)
        
        # Create model
        gemini_model = genai.GenerativeModel(model)
        
        # Generate response
        response = gemini_model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                temperature=kwargs.get("temperature", 0.7),
                max_output_tokens=kwargs.get("max_tokens", 2048),
                top_p=kwargs.get("top_p", 0.95),
            )
        )
        
        return response.text
    
    except Exception as e:
        logger.error(f"Gemini completion error: {e}")
        raise


async def gemini_complete_async(
    prompt: str,
    model: str = "gemini-1.5-flash",
    **kwargs
) -> str:
    """
    Async version of gemini_complete
    """
    # Gemini SDK doesn't have native async, so we use sync version
    # In production, you might want to use asyncio.to_thread
    return gemini_complete(prompt, model, **kwargs)


def gemini_embedding(
    texts: list[str],
    model: str = "models/text-embedding-004",
    **kwargs
) -> list[list[float]]:
    """
    Generate embeddings using Gemini API
    
    Args:
        texts: List of texts to embed
        model: Embedding model name
        **kwargs: Additional arguments
    
    Returns:
        List of embedding vectors
    """
    try:
        # Configure Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment")
        
        genai.configure(api_key=api_key)
        
        # Generate embeddings
        embeddings = []
        for text in texts:
            result = genai.embed_content(
                model=model,
                content=text,
                task_type="retrieval_document"
            )
            embeddings.append(result['embedding'])
        
        return embeddings
    
    except Exception as e:
        logger.error(f"Gemini embedding error: {e}")
        raise


async def gemini_embedding_async(
    texts: list[str],
    model: str = "models/text-embedding-004",
    **kwargs
) -> list[list[float]]:
    """
    Async version of gemini_embedding
    """
    return gemini_embedding(texts, model, **kwargs)


# LightRAG-compatible wrapper functions
def gemini_model_complete(
    prompt: str,
    system_prompt: str = None,
    history_messages: list = None,
    **kwargs
) -> str:
    """
    LightRAG-compatible completion function
    """
    # Combine system prompt and user prompt
    full_prompt = prompt
    if system_prompt:
        full_prompt = f"{system_prompt}\n\n{prompt}"
    
    return gemini_complete(full_prompt, **kwargs)


def gemini_model_if_cache(
    prompt: str,
    system_prompt: str = None,
    history_messages: list = None,
    **kwargs
) -> str:
    """
    LightRAG-compatible completion with caching support
    For now, just calls gemini_model_complete
    TODO: Implement caching layer
    """
    return gemini_model_complete(prompt, system_prompt, history_messages, **kwargs)
