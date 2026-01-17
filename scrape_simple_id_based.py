#!/usr/bin/env python3
"""
Simple ID-based scraper using requests (no Selenium required).
Falls back to the working regex approach from scrape_wowhead.py.
"""

import requests
import re
import json
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class TranslationEntry:
    id: int
    de: str
    en: str
    quality: int = None

def extract_with_ids(de_url: str, en_url: str, category: str) -> List[TranslationEntry]:
    """Extract German and English with IDs."""
    print(f"\nExtracting {category}...")
    
    # Fetch German page
    print(f"  Fetching German: {de_url}")
    de_response = requests.get(de_url, headers={'User-Agent': 'Mozilla/5.0'})
    de_source = de_response.text
    
    # Fetch English page
    print(f"  Fetching English: {en_url}")
    en_response = requests.get(en_url, headers={'User-Agent': 'Mozilla/5.0'})
    en_source = en_response.text
    
    # Extract with IDs using regex
    id_name_pattern = r'"id":(\d+),"name":"([^"]+)"'
    
    de_matches = re.findall(id_name_pattern, de_source)
    en_matches = re.findall(id_name_pattern, en_source)
    
    print(f"  German: {len(de_matches)} items")
    print(f"  English: {len(en_matches)} items")
    
    # Build dictionaries by ID
    de_by_id = {int(item_id): name for item_id, name in de_matches}
    en_by_id = {int(item_id): name for item_id, name in en_matches}
    
    # Match by ID
    translations = []
    for item_id in de_by_id.keys():
        if item_id in en_by_id:
            de_name = de_by_id[item_id]
            en_name = en_by_id[item_id]
            
            # Special handling for German aspects
            if category == 'aspects' and de_name.startswith('Aspekt:'):
                de_name = de_name.replace('Aspekt:', '').strip() + ' Aspekt'
            
            # Try to find quality
            quality = None
            quality_pattern = rf'"id":{item_id}[^}}]*"quality":(\d+)'
            quality_match = re.search(quality_pattern, de_source)
            if quality_match:
                quality = int(quality_match.group(1))
            
            translations.append(TranslationEntry(
                id=item_id,
                de=de_name,
                en=en_name,
                quality=quality
            ))
    
    print(f"  Matched: {len(translations)} translations")
    return translations

def main():
    print("=" * 80)
    print("Simple ID-Based Translation Scraper")
    print("=" * 80)
    
    # Extract all categories
    glyphs = extract_with_ids(
        'https://www.wowhead.com/diablo-4/de/paragon-glyphs',
        'https://www.wowhead.com/diablo-4/paragon-glyphs',
        'glyphs'
    )
    
    items = extract_with_ids(
        'https://www.wowhead.com/diablo-4/de/items/quality:5,6',
        'https://www.wowhead.com/diablo-4/items/quality:5,6',
        'items'
    )
    
    aspects = extract_with_ids(
        'https://www.wowhead.com/diablo-4/de/aspects',
        'https://www.wowhead.com/diablo-4/aspects',
        'aspects'
    )
    
    # Export ID-based format
    id_based = {
        'glyphs': {str(t.id): {'de': t.de, 'en': t.en, 'quality': t.quality} for t in glyphs},
        'items': {str(t.id): {'de': t.de, 'en': t.en, 'quality': t.quality} for t in items},
        'aspects': {str(t.id): {'de': t.de, 'en': t.en, 'quality': t.quality} for t in aspects}
    }
    
    with open('translations_by_id.json', 'w', encoding='utf-8') as f:
        json.dump(id_based, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Exported: translations_by_id.json")
    
    # Export string-based format
    string_based = {
        'glyphs': {t.de: t.en for t in glyphs},
        'items': {t.de: t.en for t in items},
        'aspects': {t.de: t.en for t in aspects}
    }
    
    with open('translations_by_string.json', 'w', encoding='utf-8') as f:
        json.dump(string_based, f, ensure_ascii=False, indent=2)
    print(f"✅ Exported: translations_by_string.json")
    
    # Print statistics
    print("\n" + "=" * 80)
    print("STATISTICS")
    print("=" * 80)
    print(f"Glyphs: {len(glyphs)}")
    print(f"Items: {len(items)} (unique: {sum(1 for t in items if t.quality == 5)}, mythic: {sum(1 for t in items if t.quality == 6)})")
    print(f"Aspects: {len(aspects)}")
    print(f"TOTAL: {len(glyphs) + len(items) + len(aspects)} translations")

if __name__ == '__main__':
    main()
