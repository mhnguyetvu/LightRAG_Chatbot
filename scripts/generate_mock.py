"""
Script to generate mock data and insert into LightRAG
"""
import json
import os
from pathlib import Path

MOCK_DATA_DIR = Path(__file__).parent.parent / "mock_data"


def load_mock_data():
    """Load all mock data from mock_data directory"""
    documents = []
    
    # Load JSON files
    for json_file in MOCK_DATA_DIR.glob("*.json"):
        print(f"📄 Loading {json_file.name}")
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # Convert JSON to text representation
            if isinstance(data, list):
                for item in data:
                    documents.append(json.dumps(item, ensure_ascii=False, indent=2))
            else:
                documents.append(json.dumps(data, ensure_ascii=False, indent=2))
    
    # Load Markdown files
    for md_file in MOCK_DATA_DIR.glob("*.md"):
        print(f"📄 Loading {md_file.name}")
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
            documents.append(content)
    
    print(f"\n✅ Loaded {len(documents)} documents")
    return documents


def main():
    """Generate and display mock data statistics"""
    documents = load_mock_data()
    
    print("\n📊 Mock Data Statistics:")
    print(f"Total documents: {len(documents)}")
    
    total_chars = sum(len(doc) for doc in documents)
    print(f"Total characters: {total_chars:,}")
    print(f"Average document length: {total_chars // len(documents):,} chars")
    
    print("\n💡 To insert into LightRAG, run:")
    print("   python scripts/ingest.py")


if __name__ == "__main__":
    main()
