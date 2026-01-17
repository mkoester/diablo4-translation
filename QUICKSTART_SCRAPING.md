# Quick Start: Scraping Wowhead Translations

## TL;DR

```bash
# Install dependencies
pip install -r requirements.txt
sudo pacman -S firefox geckodriver  # or equivalent for your OS

# Run the best scraper (V2 with ID-based architecture)
python3 scrape_wowhead_v2.py

# Output files:
# - translations_by_id.json (ID-based format)
# - translations_by_string.json (string-based format)
# - content_v2.js (enhanced content.js with both formats)
```

## Which Scraper Should I Use?

### Just want to test quickly?
→ `python3 scrape_wowhead.py`
- No extra dependencies needed
- Gets ~100-150 items
- Good for testing the concept

### Want comprehensive data with future-proof architecture? ⭐
→ `python3 scrape_wowhead_v2.py`
- Needs Firefox + geckodriver
- Gets 400+ items with accurate German→English matching
- ID-based data structure (no collisions, metadata support)
- Backward compatible (exports string-based format too)
- **Recommended for production use**

### Want comprehensive data (legacy)?
→ `python3 scrape_wowhead_advanced.py`
- Same as V2 but only exports string-based format
- Use this if you don't need ID-based features

### Want to experiment?
→ `python3 scrape_wowhead_selenium.py`
- Middle ground between basic and advanced
- Uses Selenium but simpler matching logic

## Installation (Advanced Scraper)

### 1. Install Firefox
```bash
# Arch/CachyOS
sudo pacman -S firefox geckodriver

# Ubuntu/Debian
sudo apt install firefox firefox-geckodriver

# macOS
brew install firefox geckodriver
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Setup Check
```bash
./setup_scraper.sh
```

## Running the Scraper

### Basic Usage
```bash
python3 scrape_wowhead_advanced.py
```

### What Happens
1. Opens Firefox in headless mode
2. Visits German Wowhead pages (glyphs, items, aspects)
3. Visits English Wowhead pages
4. Matches German → English by item ID
5. Saves results to files

### Expected Output
```
================================================================================
Wowhead Advanced Translation Scraper
================================================================================

================================================================================
EXTRACTING GLYPHS
================================================================================
Loading https://www.wowhead.com/diablo-4/de/paragon-glyphs...
Found 138 German glyphs
Loading https://www.wowhead.com/diablo-4/paragon-glyphs...
Found 138 English glyphs
Matched 138 translations

================================================================================
EXTRACTING ITEMS
================================================================================
Loading https://www.wowhead.com/diablo-4/de/items/quality:5,6...
Found 127 German items
Loading https://www.wowhead.com/diablo-4/items/quality:5,6...
Found 127 English items
Matched 127 translations

================================================================================
EXTRACTING ASPECTS
================================================================================
Loading https://www.wowhead.com/diablo-4/de/aspects...
Found 466 German aspects
Loading https://www.wowhead.com/diablo-4/aspects...
Found 466 English aspects
Matched 466 translations

Exported to wowhead_translations.json
Exported to translations_output.js

================================================================================
EXTRACTION COMPLETE
================================================================================

Files created:
  - wowhead_translations.json (JSON format)
  - translations_output.js (JavaScript format for content.js)
```

## Using the Results

### Option 1: Copy JavaScript Directly
1. Open `translations_output.js`
2. Copy the relevant sections
3. Paste into [content.js](content.js) to replace existing translation objects

### Option 2: Use JSON Programmatically
```python
import json

with open('wowhead_translations.json') as f:
    data = json.load(f)

# Access translations
glyphs = data['glyphs']
items = data['items']
aspects = data['aspects']

print(glyphs['Macht'])  # "Might"
```

## Troubleshooting

### "geckodriver not found"
```bash
# Check if installed
which geckodriver

# Install if missing
sudo pacman -S geckodriver  # Arch
sudo apt install firefox-geckodriver  # Ubuntu
```

### "Module not found: selenium"
```bash
pip install -r requirements.txt
```

### "Found 0 items"
- Wowhead may be down or changed structure
- Try with `headless=False` to see what's happening:
  Edit the script and change:
  ```python
  with WowheadTranslationScraper(headless=False) as scraper:
  ```

### Scraper is slow
- Normal! It needs to load 6 full pages (3 German + 3 English)
- Takes ~30-60 seconds total
- Add more time.sleep() if pages aren't loading fully

### Getting incomplete data
- Wowhead pagination is tricky
- The scraper gets much more than the basic version
- Some items may still be missed (Wowhead shows 997 but may not expose all via HTML)

## Next Steps

1. Run the scraper to get latest data
2. Review `translations_output.js` for accuracy
3. Copy translations into [content.js](content.js)
4. Test the extension on vitablo.de
5. Manually add any missing tempering recipes (not on Wowhead)

## Full Documentation

See [SCRAPING.md](SCRAPING.md) for complete documentation.
