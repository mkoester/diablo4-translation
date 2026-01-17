#!/usr/bin/env python3
"""
Enhanced Wowhead scraper using Selenium for JavaScript-rendered content and pagination.
Extracts German and English terms from Wowhead Diablo 4 database.
"""

import time
import json
import re
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException


@dataclass
class Translation:
    """Represents a German-English translation pair."""
    german: str
    english: str
    category: str  # 'glyph', 'item', 'aspect', 'tempering'


class WowheadScraper:
    """Scrapes Wowhead with JavaScript support and pagination handling."""

    def __init__(self, headless: bool = True):
        """Initialize the scraper with Firefox WebDriver."""
        options = Options()
        if headless:
            options.add_argument('--headless')

        # Disable images and other resources for faster loading
        options.set_preference('permissions.default.image', 2)
        options.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)

        self.driver = webdriver.Firefox(options=options)
        self.wait = WebDriverWait(self.driver, 10)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def _wait_for_listview(self):
        """Wait for the Wowhead listview table to load."""
        try:
            self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "listview-mode-default"))
            )
            # Additional wait for JavaScript to populate data
            time.sleep(2)
        except TimeoutException:
            print("Warning: Listview table not found or timed out")

    def _extract_from_page_source(self) -> List[Dict]:
        """Extract data from embedded JavaScript in page source."""
        page_source = self.driver.page_source

        # Look for Listview data structure
        pattern = r'new Listview\(\{[^}]*data:\s*(\[.*?\])\s*[,}]'
        matches = re.findall(pattern, page_source, re.DOTALL)

        all_data = []
        for match in matches:
            try:
                # Clean up the JSON (remove trailing commas, etc.)
                cleaned = re.sub(r',(\s*[}\]])', r'\1', match)
                data = json.loads(cleaned)
                all_data.extend(data)
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                continue

        return all_data

    def _click_show_all(self):
        """Try to click 'Show All' or pagination buttons to load all data."""
        try:
            # Look for "Display: All" or similar buttons
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for button in buttons:
                if "all" in button.text.lower():
                    button.click()
                    time.sleep(2)
                    return True

            # Look for pagination controls
            pagination = self.driver.find_elements(By.CLASS_NAME, "listview-pagination")
            if pagination:
                # Click "Show more" or "All" if available
                show_more = self.driver.find_elements(By.LINK_TEXT, "Show more")
                for link in show_more:
                    link.click()
                    time.sleep(2)

        except Exception as e:
            print(f"Could not expand pagination: {e}")

        return False

    def extract_glyphs(self, lang: str = 'de') -> List[str]:
        """Extract glyph names from Wowhead."""
        url = f'https://www.wowhead.com/diablo-4/{lang}/paragon-glyphs' if lang != 'en' else 'https://www.wowhead.com/diablo-4/paragon-glyphs'
        print(f"Fetching glyphs from {url}...")

        self.driver.get(url)
        self._wait_for_listview()
        self._click_show_all()

        # Extract from JavaScript data
        data = self._extract_from_page_source()
        glyphs = set()

        for item in data:
            name_key = f'name_{lang}' if lang != 'en' else 'name'
            if name_key in item:
                glyphs.add(item[name_key])
            elif 'name' in item:
                glyphs.add(item['name'])

        # Fallback: extract from HTML table
        if not glyphs:
            try:
                rows = self.driver.find_elements(By.CSS_SELECTOR, "tr[data-id]")
                for row in rows:
                    try:
                        name_cell = row.find_element(By.CLASS_NAME, "listview-cell-name")
                        link = name_cell.find_element(By.TAG_NAME, "a")
                        glyphs.add(link.text.strip())
                    except NoSuchElementException:
                        continue
            except Exception as e:
                print(f"Error extracting from HTML: {e}")

        return sorted(glyphs)

    def extract_items(self, lang: str = 'de', quality: str = '5,6') -> List[str]:
        """Extract unique/mythic item names from Wowhead."""
        url = f'https://www.wowhead.com/diablo-4/{lang}/items/quality:{quality}' if lang != 'en' else f'https://www.wowhead.com/diablo-4/items/quality:{quality}'
        print(f"Fetching items from {url}...")

        self.driver.get(url)
        self._wait_for_listview()
        self._click_show_all()

        # Extract from JavaScript data
        data = self._extract_from_page_source()
        items = set()

        for item in data:
            # Verify quality
            if item.get('quality') not in [5, 6]:
                continue

            name_key = f'name_{lang}' if lang != 'en' else 'name'
            if name_key in item:
                items.add(item[name_key])
            elif 'name' in item:
                items.add(item['name'])

        # Fallback: extract from HTML table
        if not items:
            try:
                rows = self.driver.find_elements(By.CSS_SELECTOR, "tr[data-id]")
                for row in rows:
                    try:
                        # Check quality class (quality5 for unique, quality6 for mythic)
                        if 'quality5' in row.get_attribute('class') or 'quality6' in row.get_attribute('class'):
                            name_cell = row.find_element(By.CLASS_NAME, "listview-cell-name")
                            link = name_cell.find_element(By.TAG_NAME, "a")
                            items.add(link.text.strip())
                    except NoSuchElementException:
                        continue
            except Exception as e:
                print(f"Error extracting from HTML: {e}")

        return sorted(items)

    def extract_aspects(self, lang: str = 'de') -> List[str]:
        """Extract aspect names from Wowhead."""
        url = f'https://www.wowhead.com/diablo-4/{lang}/aspects' if lang != 'en' else 'https://www.wowhead.com/diablo-4/aspects'
        print(f"Fetching aspects from {url}...")

        self.driver.get(url)
        self._wait_for_listview()
        self._click_show_all()

        # Extract from JavaScript data
        data = self._extract_from_page_source()
        aspects = set()

        for item in data:
            name_key = f'name_{lang}' if lang != 'en' else 'name'
            if name_key in item:
                name = item[name_key]
            elif 'name' in item:
                name = item['name']
            else:
                continue

            # Convert German format "Aspekt: Name" to "Name Aspekt" for vitablo.de compatibility
            if lang == 'de' and name.startswith('Aspekt:'):
                name = name.replace('Aspekt:', '').strip() + ' Aspekt'

            aspects.add(name)

        # Fallback: extract from HTML table
        if not aspects:
            try:
                rows = self.driver.find_elements(By.CSS_SELECTOR, "tr[data-id]")
                for row in rows:
                    try:
                        name_cell = row.find_element(By.CLASS_NAME, "listview-cell-name")
                        link = name_cell.find_element(By.TAG_NAME, "a")
                        name = link.text.strip()

                        # Convert format
                        if lang == 'de' and name.startswith('Aspekt:'):
                            name = name.replace('Aspekt:', '').strip() + ' Aspekt'

                        aspects.add(name)
                    except NoSuchElementException:
                        continue
            except Exception as e:
                print(f"Error extracting from HTML: {e}")

        return sorted(aspects)

    def create_translation_pairs(self) -> Dict[str, List[Translation]]:
        """Extract both German and English terms and create translation pairs."""
        print("\n" + "=" * 80)
        print("Creating German-English Translation Pairs")
        print("=" * 80 + "\n")

        results = {
            'glyphs': [],
            'items': [],
            'aspects': []
        }

        # Extract glyphs
        print("Extracting glyphs...")
        german_glyphs = set(self.extract_glyphs('de'))
        print(f"Found {len(german_glyphs)} German glyphs")

        english_glyphs = set(self.extract_glyphs('en'))
        print(f"Found {len(english_glyphs)} English glyphs")

        # Create pairs (this is approximate - would need ID matching for perfect pairs)
        for de, en in zip(sorted(german_glyphs), sorted(english_glyphs)):
            results['glyphs'].append(Translation(de, en, 'glyph'))

        print()

        # Extract items
        print("Extracting items...")
        german_items = set(self.extract_items('de'))
        print(f"Found {len(german_items)} German items")

        english_items = set(self.extract_items('en'))
        print(f"Found {len(english_items)} English items")

        for de, en in zip(sorted(german_items), sorted(english_items)):
            results['items'].append(Translation(de, en, 'item'))

        print()

        # Extract aspects
        print("Extracting aspects...")
        german_aspects = set(self.extract_aspects('de'))
        print(f"Found {len(german_aspects)} German aspects")

        english_aspects = set(self.extract_aspects('en'))
        print(f"Found {len(english_aspects)} English aspects")

        for de, en in zip(sorted(german_aspects), sorted(english_aspects)):
            results['aspects'].append(Translation(de, en, 'aspect'))

        return results


def print_results(results: Dict[str, List[Translation]]):
    """Print translation results in a readable format."""
    print("\n" + "=" * 80)
    print("TRANSLATION RESULTS")
    print("=" * 80 + "\n")

    for category, translations in results.items():
        print(f"{category.upper()} ({len(translations)} translations):")
        print("-" * 80)
        for t in translations:
            print(f'  "{t.german}": "{t.english}",')
        print()


def export_to_json(results: Dict[str, List[Translation]], filename: str = 'translations.json'):
    """Export translations to JSON file."""
    data = {}
    for category, translations in results.items():
        data[category] = [
            {'german': t.german, 'english': t.english}
            for t in translations
        ]

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nExported to {filename}")


def main():
    """Main entry point."""
    print("=" * 80)
    print("Wowhead Diablo 4 Scraper with Selenium")
    print("=" * 80)
    print()

    try:
        with WowheadScraper(headless=True) as scraper:
            # Option 1: Create translation pairs (requires matching logic)
            # results = scraper.create_translation_pairs()
            # print_results(results)
            # export_to_json(results)

            # Option 2: Extract German terms only for manual translation
            print("Extracting German terms...")
            german_glyphs = scraper.extract_glyphs('de')
            german_items = scraper.extract_items('de')
            german_aspects = scraper.extract_aspects('de')

            print("\n" + "=" * 80)
            print("GERMAN TERMS")
            print("=" * 80 + "\n")

            print(f"GLYPHS ({len(german_glyphs)}):")
            for glyph in german_glyphs:
                print(f'  "{glyph}": "TODO",')

            print(f"\nITEMS ({len(german_items)}):")
            for item in german_items:
                print(f'  "{item}": "TODO",')

            print(f"\nASPECTS ({len(german_aspects)}):")
            for aspect in german_aspects:
                print(f'  "{aspect}": "TODO",')

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
