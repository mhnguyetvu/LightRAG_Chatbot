"""
OpenRouter LLM wrapper for LightRAG
Async-compatible using AsyncOpenAI client
Supports FREE models like Gemma 3N 4B
"""
import os
import asyncio
from pathlib import Path
from openai import AsyncOpenAI
from loguru import logger

# Load .env from backend/ directory
try:
    from dotenv import load_dotenv
    _backend_env = Path(__file__).parent.parent.parent / ".env"
    if _backend_env.exists():
        load_dotenv(_backend_env)
except ImportError:
    pass


def get_openrouter_client() -> AsyncOpenAI:
    """Get configured async OpenRouter client"""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment")
    return AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )


async def openrouter_model_if_cache(
    prompt: str,
    system_prompt: str = None,
    history_messages: list = None,
    **kwargs,
) -> str:
    """
    Async LightRAG-compatible completion function for OpenRouter.
    Retries on 429 with short delays (stay within LightRAG's 360s timeout).
    """
    model = kwargs.get("model_name", os.getenv("OPENROUTER_MODEL", "google/gemma-3n-e4b-it:free"))

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if history_messages:
        messages.extend(history_messages)
    messages.append({"role": "user", "content": prompt})

    extra_headers = {}
    if os.getenv("OPENROUTER_SITE_URL"):
        extra_headers["HTTP-Referer"] = os.getenv("OPENROUTER_SITE_URL")
    if os.getenv("OPENROUTER_SITE_NAME"):
        extra_headers["X-Title"] = os.getenv("OPENROUTER_SITE_NAME")

    # Retry delays: 15s, 30s, 45s → total max ~90s, well within 360s timeout
    retry_delays = [15, 30, 45]

    for attempt, delay in enumerate(retry_delays + [None]):
        try:
            client = get_openrouter_client()
            completion = await client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2048),
                extra_headers=extra_headers if extra_headers else None,
            )
            return completion.choices[0].message.content

        except Exception as e:
            is_rate_limit = "429" in str(e) or "rate limit" in str(e).lower()

            if is_rate_limit and delay is not None:
                logger.warning(f"⏳ Rate limit (429). Waiting {delay}s... (attempt {attempt+1}/{len(retry_delays)})")
                await asyncio.sleep(delay)
            else:
                logger.error(f"OpenRouter error: {e}")
                raise
