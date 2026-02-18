"""
Document ingestion script for LightRAG
Supports both local (OpenRouter) and RunPod (Ollama) modes
"""
import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Add backend and root to path
ROOT_DIR = Path(__file__).parent.parent
BACKEND_DIR = ROOT_DIR / "backend"

sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(ROOT_DIR))

from loguru import logger

# Setup logging to file
LOG_DIR = ROOT_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = LOG_DIR / f"ingest_{timestamp}.log"

logger.add(
    LOG_FILE,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    encoding="utf-8",
)
logger.info(f"📝 Logging to: {LOG_FILE}")

from app.services.lightrag_service import lightrag_service
from app.core.config import get_settings


def load_mock_data() -> list[str]:
    """Load documents directly from mock_data folder"""
    import json
    
    mock_dir = ROOT_DIR / "mock_data"
    documents = []
    
    if not mock_dir.exists():
        logger.warning(f"mock_data folder not found at {mock_dir}")
        return documents
    
    for file_path in sorted(mock_dir.iterdir()):
        try:
            if file_path.suffix == ".json":
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, str):
                        documents.append(data)
                    elif isinstance(data, dict):
                        documents.append(json.dumps(data, ensure_ascii=False, indent=2))
                    elif isinstance(data, list):
                        for item in data:
                            if isinstance(item, str):
                                documents.append(item)
                            else:
                                documents.append(json.dumps(item, ensure_ascii=False))
                logger.info(f"� Loaded: {file_path.name}")
                
            elif file_path.suffix in [".md", ".txt"]:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    if content:
                        documents.append(content)
                logger.info(f"📄 Loaded: {file_path.name}")
                
        except Exception as e:
            logger.warning(f"⚠️ Could not load {file_path.name}: {e}")
    
    return documents


async def ingest_documents():
    """Ingest all mock documents into LightRAG"""
    settings = get_settings()
    
    logger.info("=" * 60)
    logger.info(f"🚀 Starting ingestion | Mode: {settings.LIGHTRAG_MODE} | Provider: {settings.LLM_PROVIDER}")
    logger.info("=" * 60)
    
    # Load mock data
    logger.info("📂 Loading mock data...")
    documents = load_mock_data()
    
    if not documents:
        logger.error("❌ No documents found in mock_data/ folder!")
        logger.info("💡 Add .json, .md, or .txt files to mock_data/ folder")
        return
    
    logger.info(f"✅ Loaded {len(documents)} documents")
    logger.info("📥 Inserting into LightRAG... (this may take a few minutes)")
    
    try:
        result = await lightrag_service.insert_documents(documents)
        
        logger.info("=" * 60)
        logger.info("✅ INGESTION COMPLETE!")
        logger.info("=" * 60)
        logger.info(f"Documents inserted: {result['count']}")
        logger.info("💡 Now query at: http://localhost:3000")
        logger.info("   Or CLI: python scripts/query.py 'Your question'")
        
    except Exception as e:
        logger.error(f"❌ Ingestion failed: {e}")
        raise


def main():
    asyncio.run(ingest_documents())


if __name__ == "__main__":
    main()
