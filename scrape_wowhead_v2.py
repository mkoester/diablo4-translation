#!/usr/bin/env python3
"""
ID-based Wowhead scraper - stores translations with Wowhead IDs as keys.
Enables better data management and multi-language support.
"""

import time
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options


@dataclass
class TranslationEntry:
    """Represents a translation with metadata."""
    id: int
    de: str
    en: str
    quality: Optional[int] = None  # For items: 5=unique, 6=mythic
    category: str = ""  # glyph, item, aspect, tempering


class WowheadIDScraper:
    """Scrapes Wowhead and creates ID-based translation database."""

    def __init__(self, headless: bool = True):
        """Initialize the scraper with Firefox WebDriver."""
        options = Options()
        if headless:
            options.add_argument('--headless')

        # Performance optimizations
        options.set_preference('permissions.default.image', 2)
        options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)

        self.driver = webdriver.Firefox(options=options)
        self.wait = WebDriverWait(self.driver, 15)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def _wait_for_load(self):
        """Wait for page to load."""
        time.sleep(3)

    def _extract_from_page(self, url: str) -> Dict[int, Dict]:
        """Extract items with IDs from a Wowhead page."""
        print(f"Loading {url}...")
        self.driver.get(url)
        self._wait_for_load()

        # Try to show all items
        try:
            script = """
            var buttons = document.querySelectorAll('button, a');
            for (var i = 0; i < buttons.length; i++) {
                var text = buttons[i].textContent.toLowerCase();
                if (text.includes('all') || text.includes('alle')) {
                    buttons[i].click();
                    break;
                }
            }
            """
            self.driver.execute_script(script)
            time.sleep(2)
        except Exception:
            pass

        items = {}

        # Extract from HTML table rows
        try:
            rows = self.driver.find_elements(By.CSS_SELECTOR, "tr[data-id]")
            print(f"  Found {len(rows)} items")

            for row in rows:
                try:
                    item_id = int(row.get_attribute('data-id'))

                    # Get name
                    name_cell = row.find_element(By.CLASS_NAME, "listview-cell-name")
                    link = name_cell.find_element(By.TAG_NAME, "a")
                    name = link.text.strip()

                    # Get quality if available
                    quality = None
                    classes = row.get_attribute('class') or ''
                    if 'quality5' in classes:
                        quality = 5
                    elif 'quality6' in classes:
                        quality = 6

                    items[item_id] = {
                        'name': name,
                        'quality': quality
                    }

                except Exception as e:
                    continue

        except Exception as e:
            print(f"  Error extracting: {e}")

        return items

    def extract_category(self, category: str, de_url: str, en_url: str) -> List[TranslationEntry]:
        """Extract translations for a category (glyphs, items, or aspects)."""
        print(f"\n{'='*80}")
        print(f"EXTRACTING {category.upper()}")
        print('='*80)

        # Extract German
        de_items = self._extract_from_page(de_url)
        print(f"German: {len(de_items)} items")

        # Extract English
        en_items = self._extract_from_page(en_url)
        print(f"English: {len(en_items)} items")

        # Match by ID
        translations = []
        matched = 0
        unmatched = 0

        for item_id, de_data in de_items.items():
            if item_id in en_items:
                de_name = de_data['name']
                en_name = en_items[item_id]['name']

                # Special handling for German aspects
                if category == 'aspects' and de_name.startswith('Aspekt:'):
                    de_name = de_name.replace('Aspekt:', '').strip() + ' Aspekt'

                entry = TranslationEntry(
                    id=item_id,
                    de=de_name,
                    en=en_name,
                    quality=de_data.get('quality'),
                    category=category
                )
                translations.append(entry)
                matched += 1
            else:
                unmatched += 1

        print(f"Matched: {matched}, Unmatched: {unmatched}")
        return translations

    def extract_all(self) -> Dict[str, List[TranslationEntry]]:
        """Extract all categories."""
        return {
            'glyphs': self.extract_category(
                'glyphs',
                'https://www.wowhead.com/diablo-4/de/paragon-glyphs',
                'https://www.wowhead.com/diablo-4/paragon-glyphs'
            ),
            'items': self.extract_category(
                'items',
                'https://www.wowhead.com/diablo-4/de/items/quality:5,6',
                'https://www.wowhead.com/diablo-4/items/quality:5,6'
            ),
            'aspects': self.extract_category(
                'aspects',
                'https://www.wowhead.com/diablo-4/de/aspects',
                'https://www.wowhead.com/diablo-4/aspects'
            )
        }


def export_id_based_json(data: Dict[str, List[TranslationEntry]], filename: str = 'translations_by_id.json'):
    """Export in ID-based format."""
    output = {}

    for category, entries in data.items():
        output[category] = {
            str(entry.id): {
                'de': entry.de,
                'en': entry.en,
                'quality': entry.quality
            }
            for entry in entries
        }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nExported ID-based format to: {filename}")


def export_string_lookup_json(data: Dict[str, List[TranslationEntry]], filename: str = 'translations_by_string.json'):
    """Export in string-lookup format (current content.js format)."""
    output = {}

    for category, entries in data.items():
        output[category] = {
            entry.de: entry.en
            for entry in entries
        }

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Exported string-lookup format to: {filename}")


def export_content_js_v2(data: Dict[str, List[TranslationEntry]], filename: str = 'content_v2.js'):
    """
    Export enhanced content.js with ID-based data structure.
    Provides both ID lookup and string lookup for flexibility.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("// D4 German Translator V2 - ID-based translation data\n")
        f.write("// Enables better data management and future enhancements\n\n")

        # Write ID-based data
        f.write("// ============================================================================\n")
        f.write("// ID-BASED TRANSLATION DATABASE\n")
        f.write("// ============================================================================\n\n")

        for category, entries in data.items():
            f.write(f"// {category.title()}\n")
            f.write(f"const {category}ById = {{\n")
            for entry in sorted(entries, key=lambda e: e.id):
                quality_str = f", quality: {entry.quality}" if entry.quality else ""
                f.write(f'  {entry.id}: {{ de: "{entry.de}", en: "{entry.en}"{quality_str} }},\n')
            f.write("};\n\n")

        # Write string-based lookup (for backward compatibility)
        f.write("// ============================================================================\n")
        f.write("// STRING-BASED LOOKUP (for regex matching)\n")
        f.write("// ============================================================================\n\n")

        for category, entries in data.items():
            f.write(f"// {category.title()}\n")
            f.write(f"const {category}Translations = {{\n")
            for entry in sorted(entries, key=lambda e: e.de):
                f.write(f'  "{entry.de}": "{entry.en}",\n')
            f.write("};\n\n")

        # Write merged lookup
        f.write("// Merge all string-based translations for regex pattern\n")
        f.write("const allTranslations = {\n")
        f.write("  ...glyphsTranslations,\n")
        f.write("  ...itemsTranslations,\n")
        f.write("  ...aspectsTranslations\n")
        f.write("};\n\n")

        # Write helper functions
        f.write("// ============================================================================\n")
        f.write("// HELPER FUNCTIONS\n")
        f.write("// ============================================================================\n\n")

        f.write("""
/**
 * Get translation by ID
 * @param {string} category - 'glyphs', 'items', or 'aspects'
 * @param {number} id - Wowhead item ID
 * @returns {Object|null} Translation object or null
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
 * @param {string} germanText - German term
 * @returns {string|null} English translation or null
 */
function getEnglishFromGerman(germanText) {
  return allTranslations[germanText] || null;
}

/**
 * Check if a Wowhead ID exists in our database
 * @param {number} id - Wowhead item ID
 * @returns {Object|null} { category, translation } or null
 */
function findById(id) {
  if (glyphsById[id]) return { category: 'glyph', translation: glyphsById[id] };
  if (itemsById[id]) return { category: 'item', translation: itemsById[id] };
  if (aspectsById[id]) return { category: 'aspect', translation: aspectsById[id] };
  return null;
}
""")

        f.write("\n// Rest of content.js remains the same (translation logic)\n")

    print(f"Exported enhanced content.js to: {filename}")


def print_statistics(data: Dict[str, List[TranslationEntry]]):
    """Print statistics."""
    print("\n" + "=" * 80)
    print("STATISTICS")
    print("=" * 80)

    total_translations = 0
    for category, entries in data.items():
        unique_count = len(entries)
        mythic_count = sum(1 for e in entries if e.quality == 6)
        unique_only = sum(1 for e in entries if e.quality == 5)

        print(f"\n{category.upper()}:")
        print(f"  Total: {unique_count}")
        if category == 'items':
            print(f"  - Unique (quality 5): {unique_only}")
            print(f"  - Mythic (quality 6): {mythic_count}")

        total_translations += unique_count

    print(f"\n{'='*80}")
    print(f"TOTAL TRANSLATIONS: {total_translations}")
    print('='*80)


def main():
    """Main entry point."""
    print("=" * 80)
    print("Wowhead ID-Based Translation Scraper V2")
    print("=" * 80)

    try:
        with WowheadIDScraper(headless=True) as scraper:
            data = scraper.extract_all()

            print_statistics(data)

            # Export in multiple formats
            export_id_based_json(data)
            export_string_lookup_json(data)
            export_content_js_v2(data)

            print("\n" + "=" * 80)
            print("EXTRACTION COMPLETE")
            print("=" * 80)
            print("\nFiles created:")
            print("  1. translations_by_id.json     - ID-based format")
            print("  2. translations_by_string.json - String-based format (current)")
            print("  3. content_v2.js               - Enhanced content.js with both formats")

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
