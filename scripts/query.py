"""
Script to query LightRAG
"""
import asyncio
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from app.services.lightrag_service import lightrag_service
from app.core.config import get_settings


async def query(question: str, mode: str = "hybrid"):
    """Query LightRAG"""
    settings = get_settings()
    print(f"\n🔍 Querying in {settings.LIGHTRAG_MODE} mode...")
    print(f"Question: {question}")
    print(f"Query mode: {mode}\n")
    
    result = await lightrag_service.query(question, mode)
    
    print("=" * 80)
    print("📝 ANSWER:")
    print("=" * 80)
    print(result["answer"])
    print("=" * 80)


def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python scripts/query.py <question> [mode]")
        print("Example: python scripts/query.py 'Chính sách bảo hiểm là gì?' hybrid")
        sys.exit(1)
    
    question = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else "hybrid"
    
    asyncio.run(query(question, mode))


if __name__ == "__main__":
    main()
