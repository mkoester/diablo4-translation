#!/usr/bin/env python3
"""
Complete ID-based scraper that extracts glyphs, items, and aspects.
Uses multiple extraction strategies to handle different Wowhead page structures.
"""

import requests
import re
import json
from typing import Dict, List, Tuple
from dataclasses import dataclass, asdict

@dataclass
class TranslationEntry:
    id: int
    de: str
    en: str
    quality: int = None

def extract_with_regex_ids(de_url: str, en_url: str, use_flexible_pattern: bool = False) -> Tuple[Dict[int, str], Dict[int, str], str]:
    """Extract using regex pattern for id and name."""
    print(f"  Fetching German...")
    de_response = requests.get(de_url, headers={'User-Agent': 'Mozilla/5.0'})
    de_source = de_response.text

    print(f"  Fetching English...")
    en_response = requests.get(en_url, headers={'User-Agent': 'Mozilla/5.0'})
    en_source = en_response.text

    # Extract with IDs - try strict pattern first, then flexible
    patterns = [
        r'"id":(\d+),"name":"([^"]+)"',  # Strict: id immediately followed by name
        r'"id":(\d+).*?"name":"([^"]+)"'  # Flexible: id and name with stuff between
    ]

    pattern_to_use = patterns[1] if use_flexible_pattern else patterns[0]

    de_matches = re.findall(pattern_to_use, de_source)
    en_matches = re.findall(pattern_to_use, en_source)

    # If strict didn't work, try flexible
    if not de_matches and not use_flexible_pattern:
        print(f"  Retrying with flexible pattern...")
        de_matches = re.findall(patterns[1], de_source)
        en_matches = re.findall(patterns[1], en_source)

    de_by_id = {int(item_id): name for item_id, name in de_matches}
    en_by_id = {int(item_id): name for item_id, name in en_matches}

    print(f"  German: {len(de_by_id)} items")
    print(f"  English: {len(en_by_id)} items")

    return de_by_id, en_by_id, de_source

def extract_glyphs() -> List[TranslationEntry]:
    """Extract paragon glyphs with IDs."""
    print("\n" + "="*80)
    print("EXTRACTING GLYPHS")
    print("="*80)
    
    de_by_id, en_by_id, de_source = extract_with_regex_ids(
        'https://www.wowhead.com/diablo-4/de/paragon-glyphs',
        'https://www.wowhead.com/diablo-4/paragon-glyphs'
    )
    
    translations = []
    for item_id in de_by_id.keys():
        if item_id in en_by_id:
            # Try to find quality
            quality_pattern = rf'"id":{item_id}[^}}]*"quality":(\d+)'
            quality_match = re.search(quality_pattern, de_source)
            quality = int(quality_match.group(1)) if quality_match else None
            
            translations.append(TranslationEntry(
                id=item_id,
                de=de_by_id[item_id],
                en=en_by_id[item_id],
                quality=quality
            ))
    
    print(f"  Matched: {len(translations)} translations")
    return translations

def extract_items() -> List[TranslationEntry]:
    """Extract unique/mythic items with IDs."""
    print("\n" + "="*80)
    print("EXTRACTING ITEMS")
    print("="*80)
    
    # For items, use a different approach - look in script tags
    de_url = 'https://www.wowhead.com/diablo-4/de/items/quality:5,6'
    en_url = 'https://www.wowhead.com/diablo-4/items/quality:5,6'
    
    print(f"  Fetching German...")
    de_response = requests.get(de_url, headers={'User-Agent': 'Mozilla/5.0'})
    de_source = de_response.text
    
    print(f"  Fetching English...")
    en_response = requests.get(en_url, headers={'User-Agent': 'Mozilla/5.0'})
    en_source = en_response.text
    
    # Try multiple patterns
    de_by_id = {}
    en_by_id = {}
    
    # Pattern 1: Look for item data in scripts
    patterns = [
        r'"id":(\d+),"name":"([^"]+)".*?"quality":([56])',
        r'\{[^}]*"id":(\d+)[^}]*"name":"([^"]+)"[^}]*"quality":([56])[^}]*\}',
    ]
    
    for pattern in patterns:
        de_matches = re.findall(pattern, de_source, re.DOTALL)
        en_matches = re.findall(pattern, en_source, re.DOTALL)
        
        if de_matches:
            de_by_id = {int(m[0]): (m[1], int(m[2])) for m in de_matches}
            print(f"  German: {len(de_by_id)} items (pattern {patterns.index(pattern)+1})")
            break
    
    for pattern in patterns:
        en_matches = re.findall(pattern, en_source, re.DOTALL)
        
        if en_matches:
            en_by_id = {int(m[0]): (m[1], int(m[2])) for m in en_matches}
            print(f"  English: {len(en_by_id)} items (pattern {patterns.index(pattern)+1})")
            break
    
    # If regex didn't work, try simpler approach
    if not de_by_id:
        print("  Trying alternative extraction for German...")
        # Look for any id/name/quality combo
        script_pattern = r'<script[^>]*>(.*?)</script>'
        scripts = re.findall(script_pattern, de_source, re.DOTALL)
        for script in scripts:
            item_pattern = r'"name":"([^"]+)".*?"quality":([56])'
            matches = re.findall(item_pattern, script)
            if matches:
                # Without IDs, we'll need to match by name order
                print(f"  Found {len(matches)} German items (no IDs)")
                break
    
    if not en_by_id:
        print("  Trying alternative extraction for English...")
        script_pattern = r'<script[^>]*>(.*?)</script>'
        scripts = re.findall(script_pattern, en_source, re.DOTALL)
        for script in scripts:
            item_pattern = r'"name":"([^"]+)".*?"quality":([56])'
            matches = re.findall(item_pattern, script)
            if matches:
                print(f"  Found {len(matches)} English items (no IDs)")
                break
    
    # Match by ID
    translations = []
    for item_id in de_by_id.keys():
        if item_id in en_by_id:
            de_name, de_quality = de_by_id[item_id]
            en_name, en_quality = en_by_id[item_id]
            
            translations.append(TranslationEntry(
                id=item_id,
                de=de_name,
                en=en_name,
                quality=de_quality
            ))
    
    print(f"  Matched: {len(translations)} translations")
    return translations

def extract_aspects() -> List[TranslationEntry]:
    """Extract legendary aspects with IDs."""
    print("\n" + "="*80)
    print("EXTRACTING ASPECTS")
    print("="*80)

    # For aspects, we need a special pattern that filters for actual aspect names
    print(f"  Fetching German...")
    de_response = requests.get('https://www.wowhead.com/diablo-4/de/aspects',
                                headers={'User-Agent': 'Mozilla/5.0'})
    de_source = de_response.text

    print(f"  Fetching English...")
    en_response = requests.get('https://www.wowhead.com/diablo-4/aspects',
                                headers={'User-Agent': 'Mozilla/5.0'})
    en_source = en_response.text

    # Extract only items where name contains "Aspekt" or "aspekt" (German)
    # or "Aspect" (English)
    de_pattern = r'"id":(\d+).*?"name":"([^"]*[Aa]spekt[^"]*?)"'
    en_pattern = r'"id":(\d+).*?"name":"([^"]*[Aa]spect[^"]*?)"'

    de_matches = re.findall(de_pattern, de_source)
    en_matches = re.findall(en_pattern, en_source)

    de_by_id = {int(item_id): name for item_id, name in de_matches}
    en_by_id = {int(item_id): name for item_id, name in en_matches}

    print(f"  German: {len(de_by_id)} aspects")
    print(f"  English: {len(en_by_id)} aspects")

    translations = []
    for item_id in de_by_id.keys():
        if item_id in en_by_id:
            de_name = de_by_id[item_id]
            en_name = en_by_id[item_id]

            # Convert German aspect format from "Aspekt: Name" to "Name Aspekt"
            # for vitablo.de compatibility
            if de_name.startswith('Aspekt:'):
                de_name = de_name.replace('Aspekt:', '').strip() + ' Aspekt'

            translations.append(TranslationEntry(
                id=item_id,
                de=de_name,
                en=en_name,
                quality=None
            ))

    print(f"  Matched: {len(translations)} translations")
    return translations

def export_results(glyphs: List[TranslationEntry], items: List[TranslationEntry], aspects: List[TranslationEntry]):
    """Export translations in multiple formats."""
    
    # ID-based format
    id_based = {
        'glyphs': {str(t.id): {'de': t.de, 'en': t.en, 'quality': t.quality} for t in glyphs},
        'items': {str(t.id): {'de': t.de, 'en': t.en, 'quality': t.quality} for t in items},
        'aspects': {str(t.id): {'de': t.de, 'en': t.en, 'quality': t.quality} for t in aspects}
    }
    
    with open('translations_by_id.json', 'w', encoding='utf-8') as f:
        json.dump(id_based, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Exported: translations_by_id.json")
    
    # String-based format
    string_based = {
        'glyphs': {t.de: t.en for t in glyphs},
        'items': {t.de: t.en for t in items},
        'aspects': {t.de: t.en for t in aspects}
    }
    
    with open('translations_by_string.json', 'w', encoding='utf-8') as f:
        json.dump(string_based, f, ensure_ascii=False, indent=2)
    print(f"✅ Exported: translations_by_string.json")
    
    # Enhanced content_v2.js
    with open('content_v2.js', 'w', encoding='utf-8') as f:
        f.write("// D4 German Translator V2 - ID-based translation data\n")
        f.write("// Auto-generated by scrape_complete_id_based.py\n\n")
        
        # ID-based data
        f.write("// ============================================================================\n")
        f.write("// ID-BASED TRANSLATION DATABASE\n")
        f.write("// ============================================================================\n\n")
        
        for category, translations in [('glyphs', glyphs), ('items', items), ('aspects', aspects)]:
            f.write(f"// {category.title()}\n")
            f.write(f"const {category}ById = {{\n")
            for t in sorted(translations, key=lambda x: x.id):
                quality_str = f", quality: {t.quality}" if t.quality else ""
                de_escaped = t.de.replace('\\', '\\\\').replace('"', '\\"')
                en_escaped = t.en.replace('\\', '\\\\').replace('"', '\\"')
                f.write(f'  {t.id}: {{ de: "{de_escaped}", en: "{en_escaped}"{quality_str} }},\n')
            f.write("};\n\n")
        
        # String-based lookups
        f.write("// ============================================================================\n")
        f.write("// STRING-BASED LOOKUP (for regex matching)\n")
        f.write("// ============================================================================\n\n")
        
        for category, translations in [('glyphs', glyphs), ('items', items), ('aspects', aspects)]:
            f.write(f"// {category.title()}\n")
            f.write(f"const {category}Translations = {{\n")
            for t in sorted(translations, key=lambda x: x.de):
                de_escaped = t.de.replace('\\', '\\\\').replace('"', '\\"')
                en_escaped = t.en.replace('\\', '\\\\').replace('"', '\\"')
                f.write(f'  "{de_escaped}": "{en_escaped}",\n')
            f.write("};\n\n")
        
        # Merged lookup
        f.write("// Merge all translations for regex pattern\n")
        f.write("const allTranslations = {\n")
        f.write("  ...glyphsTranslations,\n")
        f.write("  ...itemsTranslations,\n")
        f.write("  ...aspectsTranslations\n")
        f.write("};\n\n")
        
        # Helper functions
        f.write("// ============================================================================\n")
        f.write("// HELPER FUNCTIONS\n")
        f.write("// ============================================================================\n\n")
        f.write('''
/**
 * Get translation by Wowhead ID
 */
function getTranslationById(category, id) {
  const db = {
    'glyphs': glyphsById,
    'items': itemsById,
    'aspects': aspectsById
  };
  return db[category]?.[id] || null;
}

/**
 * Get English translation from German string
 */
function getEnglishFromGerman(germanText) {
  return allTranslations[germanText] || null;
}

/**
 * Find translation by ID across all categories
 */
function findById(id) {
  if (glyphsById[id]) return { category: 'glyph', translation: glyphsById[id] };
  if (itemsById[id]) return { category: 'item', translation: itemsById[id] };
  if (aspectsById[id]) return { category: 'aspect', translation: aspectsById[id] };
  return null;
}

// Rest of content.js translation logic goes here...
''')
    
    print(f"✅ Exported: content_v2.js")

def print_statistics(glyphs: List[TranslationEntry], items: List[TranslationEntry], aspects: List[TranslationEntry]):
    """Print extraction statistics."""
    print("\n" + "="*80)
    print("STATISTICS")
    print("="*80)
    
    print(f"\nGlyphs: {len(glyphs)}")
    if glyphs:
        qualities = {}
        for t in glyphs:
            qualities[t.quality] = qualities.get(t.quality, 0) + 1
        for q, count in sorted(qualities.items()):
            print(f"  - Quality {q}: {count}")
    
    print(f"\nItems: {len(items)}")
    if items:
        unique_count = sum(1 for t in items if t.quality == 5)
        mythic_count = sum(1 for t in items if t.quality == 6)
        print(f"  - Unique (quality 5): {unique_count}")
        print(f"  - Mythic (quality 6): {mythic_count}")
    
    print(f"\nAspects: {len(aspects)}")
    
    print(f"\nTOTAL TRANSLATIONS: {len(glyphs) + len(items) + len(aspects)}")
    print("="*80)

def main():
    print("="*80)
    print("Complete ID-Based Translation Scraper")
    print("="*80)
    
    # Extract all categories
    glyphs = extract_glyphs()
    items = extract_items()
    aspects = extract_aspects()
    
    # Export results
    export_results(glyphs, items, aspects)
    
    # Print statistics
    print_statistics(glyphs, items, aspects)
    
    print("\nFiles created:")
    print("  1. translations_by_id.json     - ID-based format")
    print("  2. translations_by_string.json - String-based format")
    print("  3. content_v2.js               - Enhanced content.js with both formats")

if __name__ == '__main__':
    main()
