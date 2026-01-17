#!/usr/bin/env python3
"""
Scrape mythic items (quality 6) from Wowhead and add to translations.
Mythics need separate extraction because Wowhead may list them differently.
"""

import requests
import re
import json
from typing import Dict, List

def scrape_mythic_items() -> Dict[str, str]:
    """Scrape mythic items from Wowhead."""
    print("Scraping mythic items from Wowhead...")

    # URLs for mythic items (quality 6)
    de_url = "https://www.wowhead.com/diablo-4/de/items/quality:6"
    en_url = "https://www.wowhead.com/diablo-4/items/quality:6"

    print(f"Fetching German mythics from: {de_url}")
    de_response = requests.get(de_url)
    de_source = de_response.text

    print(f"Fetching English mythics from: {en_url}")
    en_response = requests.get(en_url)
    en_source = en_response.text

    # Extract items with IDs
    de_pattern = r'"id":(\d+).*?"name":"([^"]+)".*?"quality":6'
    en_pattern = r'"id":(\d+).*?"name":"([^"]+)".*?"quality":6'

    de_matches = re.findall(de_pattern, de_source, re.DOTALL)
    en_matches = re.findall(en_pattern, en_source, re.DOTALL)

    print(f"Found {len(de_matches)} German mythics")
    print(f"Found {len(en_matches)} English mythics")

    # Create ID to name mappings
    de_items = {int(item_id): name for item_id, name in de_matches}
    en_items = {int(item_id): name for item_id, name in en_matches}

    # Match by ID
    translations = {}
    for item_id, de_name in de_items.items():
        if item_id in en_items:
            en_name = en_items[item_id]
            translations[de_name] = en_name
            print(f"  {de_name} → {en_name}")

    return translations


def main():
    """Main entry point."""
    print("=" * 80)
    print("Mythic Item Scraper for Diablo 4")
    print("=" * 80)

    # Scrape mythics
    mythic_translations = scrape_mythic_items()

    if not mythic_translations:
        print("\n❌ No mythic items found!")
        print("This could mean:")
        print("  - Wowhead doesn't have mythics listed separately")
        print("  - The quality:6 filter doesn't work")
        print("  - Mythics are listed under a different URL")
        return 1

    print(f"\n✅ Successfully scraped {len(mythic_translations)} mythic items")

    # Load existing translations
    print("\nLoading existing translations...")
    with open('translations_by_string.json', 'r', encoding='utf-8') as f:
        existing = json.load(f)

    # Add mythics to items
    print("Adding mythics to item translations...")
    before_count = len(existing['items'])
    existing['items'].update(mythic_translations)
    after_count = len(existing['items'])

    print(f"Items before: {before_count}")
    print(f"Items after: {after_count}")
    print(f"New mythics added: {after_count - before_count}")

    # Save updated translations
    print("\nSaving updated translations...")
    with open('translations_by_string.json', 'w', encoding='utf-8') as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    print("\n✅ translations_by_string.json updated with mythic items!")
    print("\nNext steps:")
    print("  1. Run: python3 update_content_js.py")
    print("  2. Run: ./build.sh")
    print("  3. Reload extension in Firefox")

    return 0


if __name__ == '__main__':
    exit(main())
