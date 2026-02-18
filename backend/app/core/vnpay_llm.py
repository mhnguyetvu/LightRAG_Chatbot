"""
VNPay AI Gateway LLM wrapper for LightRAG
Uses OpenAI-compatible API with model v_chat4
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


def get_vnpay_client() -> AsyncOpenAI:
    """Get configured async VNPay AI Gateway client"""
    api_key = os.getenv("VNPAY_API_KEY")
    base_url = os.getenv("VNPAY_BASE_URL", "https://genai.vnpay.vn/aigateway/llm_v4/v1")

    if not api_key:
        raise ValueError("VNPAY_API_KEY not found in environment")

    return AsyncOpenAI(
        base_url=base_url,
        api_key=api_key,
        default_headers={
            "Content-Type": "application/json",
        }
    )


async def vnpay_model_if_cache(
    prompt: str,
    system_prompt: str = None,
    history_messages: list = None,
    **kwargs,
) -> str:
    """
    Async LightRAG-compatible completion function for VNPay AI Gateway.
    Uses OpenAI-compatible API format.
    """
    model = kwargs.get("model_name", os.getenv("VNPAY_MODEL", "v_chat4"))

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    if history_messages:
        messages.extend(history_messages)
    messages.append({"role": "user", "content": prompt})

    # Retry on transient errors
    retry_delays = [5, 15, 30]

    for attempt, delay in enumerate(retry_delays + [None]):
        try:
            client = get_vnpay_client()
            completion = await client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=kwargs.get("temperature", 0.7),
                max_tokens=kwargs.get("max_tokens", 2048),
                stream=False,
            )
            return completion.choices[0].message.content

        except Exception as e:
            err_str = str(e)
            is_retryable = any(x in err_str for x in ["429", "500", "502", "503", "timeout"])

            if is_retryable and delay is not None:
                logger.warning(f"⏳ VNPay API error, retrying in {delay}s... (attempt {attempt+1}): {e}")
                await asyncio.sleep(delay)
            else:
                logger.error(f"VNPay API error: {e}")
                raise
