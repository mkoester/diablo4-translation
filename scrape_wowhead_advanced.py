#!/usr/bin/env python3
"""
Advanced Wowhead scraper that matches German and English terms using item IDs.
Uses Selenium for JavaScript support and creates accurate translation pairs.
"""

import time
import json
import re
from typing import Dict, List, Set, Optional
from dataclasses import dataclass, asdict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException


@dataclass
class Item:
    """Represents an item/glyph/aspect with ID and name."""
    id: int
    name: str
    quality: Optional[int] = None


class WowheadTranslationScraper:
    """Advanced scraper that creates accurate German-English translation pairs."""

    def __init__(self, headless: bool = True):
        """Initialize the scraper with Firefox WebDriver."""
        options = Options()
        if headless:
            options.add_argument('--headless')

        # Performance optimizations
        options.set_preference('permissions.default.image', 2)
        options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
        options.set_preference('javascript.enabled', True)

        self.driver = webdriver.Firefox(options=options)
        self.wait = WebDriverWait(self.driver, 15)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def _wait_for_data_load(self):
        """Wait for JavaScript data to load."""
        time.sleep(3)  # Give JavaScript time to populate

    def _extract_items_from_javascript(self, url: str) -> Dict[int, Item]:
        """Extract items with IDs from JavaScript data structures."""
        print(f"Loading {url}...")
        self.driver.get(url)
        self._wait_for_data_load()

        # Try to expand pagination
        try:
            # Look for pagination controls and try to show all
            script = """
            // Try to find and trigger display all
            var buttons = document.querySelectorAll('button, a');
            for (var i = 0; i < buttons.length; i++) {
                if (buttons[i].textContent.toLowerCase().includes('all') ||
                    buttons[i].textContent.toLowerCase().includes('alle')) {
                    buttons[i].click();
                    break;
                }
            }
            """
            self.driver.execute_script(script)
            time.sleep(2)
        except Exception:
            pass

        page_source = self.driver.page_source
        items = {}

        # Extract from Listview JSON data
        pattern = r'new Listview\(\{[^}]*data:\s*(\[.*?\])\s*[,}]'
        matches = re.findall(pattern, page_source, re.DOTALL)

        for match in matches:
            try:
                # Clean JSON
                cleaned = re.sub(r',(\s*[}\]])', r'\1', match)
                # Handle JavaScript comments
                cleaned = re.sub(r'//.*?\n', '\n', cleaned)

                data = json.loads(cleaned)
                for item_data in data:
                    if 'id' in item_data and 'name' in item_data:
                        item = Item(
                            id=item_data['id'],
                            name=item_data['name'],
                            quality=item_data.get('quality')
                        )
                        items[item.id] = item

            except (json.JSONDecodeError, ValueError) as e:
                print(f"Warning: Could not parse JSON: {e}")
                continue

        # Fallback: extract from HTML data attributes
        if not items:
            try:
                rows = self.driver.find_elements(By.CSS_SELECTOR, "tr[data-id]")
                print(f"Found {len(rows)} rows in HTML table")

                for row in rows:
                    try:
                        item_id = int(row.get_attribute('data-id'))
                        name_cell = row.find_element(By.CLASS_NAME, "listview-cell-name")
                        link = name_cell.find_element(By.TAG_NAME, "a")
                        name = link.text.strip()

                        # Try to get quality from class
                        quality = None
                        classes = row.get_attribute('class')
                        if 'quality5' in classes:
                            quality = 5
                        elif 'quality6' in classes:
                            quality = 6

                        items[item_id] = Item(id=item_id, name=name, quality=quality)

                    except Exception as e:
                        continue

            except Exception as e:
                print(f"Error extracting from HTML: {e}")

        return items

    def extract_glyphs(self) -> Dict[str, str]:
        """Extract German-English glyph translation pairs."""
        print("\n" + "=" * 80)
        print("EXTRACTING GLYPHS")
        print("=" * 80)

        german_glyphs = self._extract_items_from_javascript(
            'https://www.wowhead.com/diablo-4/de/paragon-glyphs'
        )
        print(f"Found {len(german_glyphs)} German glyphs")

        english_glyphs = self._extract_items_from_javascript(
            'https://www.wowhead.com/diablo-4/paragon-glyphs'
        )
        print(f"Found {len(english_glyphs)} English glyphs")

        # Match by ID
        translations = {}
        for item_id, german_item in german_glyphs.items():
            if item_id in english_glyphs:
                translations[german_item.name] = english_glyphs[item_id].name
            else:
                translations[german_item.name] = "TODO"

        print(f"Matched {len(translations)} translations")
        return translations

    def extract_items(self, quality: str = '5,6') -> Dict[str, str]:
        """Extract German-English item translation pairs."""
        print("\n" + "=" * 80)
        print("EXTRACTING ITEMS")
        print("=" * 80)

        german_items = self._extract_items_from_javascript(
            f'https://www.wowhead.com/diablo-4/de/items/quality:{quality}'
        )
        print(f"Found {len(german_items)} German items")

        english_items = self._extract_items_from_javascript(
            f'https://www.wowhead.com/diablo-4/items/quality:{quality}'
        )
        print(f"Found {len(english_items)} English items")

        # Match by ID and filter by quality
        translations = {}
        for item_id, german_item in german_items.items():
            # Filter for unique/mythic only
            if german_item.quality not in [5, 6, None]:
                continue

            if item_id in english_items:
                translations[german_item.name] = english_items[item_id].name
            else:
                translations[german_item.name] = "TODO"

        print(f"Matched {len(translations)} translations")
        return translations

    def extract_aspects(self) -> Dict[str, str]:
        """Extract German-English aspect translation pairs."""
        print("\n" + "=" * 80)
        print("EXTRACTING ASPECTS")
        print("=" * 80)

        german_aspects = self._extract_items_from_javascript(
            'https://www.wowhead.com/diablo-4/de/aspects'
        )
        print(f"Found {len(german_aspects)} German aspects")

        english_aspects = self._extract_items_from_javascript(
            'https://www.wowhead.com/diablo-4/aspects'
        )
        print(f"Found {len(english_aspects)} English aspects")

        # Match by ID
        translations = {}
        for item_id, german_item in german_aspects.items():
            german_name = german_item.name

            # Convert German format "Aspekt: Name" to "Name Aspekt"
            if german_name.startswith('Aspekt:'):
                german_name = german_name.replace('Aspekt:', '').strip() + ' Aspekt'

            if item_id in english_aspects:
                translations[german_name] = english_aspects[item_id].name
            else:
                translations[german_name] = "TODO"

        print(f"Matched {len(translations)} translations")
        return translations

    def extract_all_translations(self) -> Dict[str, Dict[str, str]]:
        """Extract all translation categories."""
        return {
            'glyphs': self.extract_glyphs(),
            'items': self.extract_items(),
            'aspects': self.extract_aspects()
        }


def format_js_object(translations: Dict[str, str], indent: int = 2) -> str:
    """Format translations as a JavaScript object."""
    lines = []
    indent_str = ' ' * indent

    for german, english in sorted(translations.items()):
        # Escape quotes in strings
        german_escaped = german.replace('"', '\\"')
        english_escaped = english.replace('"', '\\"')
        lines.append(f'{indent_str}"{german_escaped}": "{english_escaped}",')

    return '\n'.join(lines)


def export_to_json(translations: Dict[str, Dict[str, str]], filename: str = 'wowhead_translations.json'):
    """Export translations to JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)
    print(f"\nExported to {filename}")


def export_to_js_format(translations: Dict[str, Dict[str, str]], filename: str = 'translations_output.js'):
    """Export translations in JavaScript object format for easy copy-paste."""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("// Paragon Glyphs\n")
        f.write("const glyphTranslations = {\n")
        f.write(format_js_object(translations['glyphs']))
        f.write("\n};\n\n")

        f.write("// Unique and Mythic Items\n")
        f.write("const itemTranslations = {\n")
        f.write(format_js_object(translations['items']))
        f.write("\n};\n\n")

        f.write("// Legendary Aspects\n")
        f.write("const aspectTranslations = {\n")
        f.write(format_js_object(translations['aspects']))
        f.write("\n};\n\n")

    print(f"Exported to {filename}")


def print_statistics(translations: Dict[str, Dict[str, str]]):
    """Print statistics about extracted translations."""
    print("\n" + "=" * 80)
    print("STATISTICS")
    print("=" * 80)

    for category, trans in translations.items():
        total = len(trans)
        completed = sum(1 for v in trans.values() if v != "TODO")
        todo = total - completed

        print(f"\n{category.upper()}:")
        print(f"  Total: {total}")
        print(f"  Completed: {completed}")
        print(f"  TODO: {todo}")

        if todo > 0:
            print(f"  Missing translations:")
            for german, english in trans.items():
                if english == "TODO":
                    print(f"    - {german}")


def main():
    """Main entry point."""
    print("=" * 80)
    print("Wowhead Advanced Translation Scraper")
    print("=" * 80)

    try:
        with WowheadTranslationScraper(headless=True) as scraper:
            translations = scraper.extract_all_translations()

            print_statistics(translations)

            # Export in multiple formats
            export_to_json(translations)
            export_to_js_format(translations)

            print("\n" + "=" * 80)
            print("EXTRACTION COMPLETE")
            print("=" * 80)
            print("\nFiles created:")
            print("  - wowhead_translations.json (JSON format)")
            print("  - translations_output.js (JavaScript format for content.js)")

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
