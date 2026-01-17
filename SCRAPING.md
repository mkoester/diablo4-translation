# Wowhead Scraping Tools

This directory contains multiple scraping tools for extracting Diablo 4 translations from Wowhead.

## Available Scrapers

### 1. `scrape_wowhead.py` - Basic Scraper
**Simple, lightweight scraper using only `requests`.**

**Pros:**
- No browser dependencies
- Fast and lightweight
- Good for initial data extraction

**Cons:**
- Only sees initial page load (no JavaScript execution)
- Misses dynamically loaded content
- Limited pagination support
- May only get ~100 items instead of full 997+ items

**Usage:**
```bash
python scrape_wowhead.py
```

### 2. `scrape_wowhead_selenium.py` - Enhanced Scraper
**Uses Selenium WebDriver for JavaScript support.**

**Pros:**
- Executes JavaScript, sees all dynamically loaded content
- Attempts to handle pagination ("Show All" buttons)
- More comprehensive data extraction

**Cons:**
- Requires Firefox/geckodriver installation
- Slower than basic scraper
- Simple alphabetical matching (not ID-based)

**Usage:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run scraper
python scrape_wowhead_selenium.py
```

### 3. `scrape_wowhead_advanced.py` - Advanced Scraper (RECOMMENDED)
**Uses Selenium with ID-based matching for accurate translations.**

**Pros:**
- ✅ Executes JavaScript for full content
- ✅ Matches German-English pairs by Wowhead item IDs
- ✅ Accurate translations (not alphabetical guessing)
- ✅ Handles pagination
- ✅ Exports to both JSON and JavaScript formats

**Cons:**
- Requires Firefox/geckodriver installation
- Slower (needs to fetch both German and English pages)

**Usage:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run scraper
python scrape_wowhead_advanced.py
```

**Output:**
- `wowhead_translations.json` - JSON format for programmatic use
- `translations_output.js` - JavaScript format ready to copy into `content.js`

## Installation

### Prerequisites

1. **Python 3.8+**

2. **Firefox** (for Selenium scrapers)

3. **geckodriver** (for Selenium scrapers)
   ```bash
   # Linux (Arch/CachyOS)
   sudo pacman -S firefox geckodriver

   # Ubuntu/Debian
   sudo apt install firefox-geckodriver

   # macOS
   brew install geckodriver

   # Or download manually from:
   # https://github.com/mozilla/geckodriver/releases
   ```

4. **Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Quick Start

**Recommended workflow for comprehensive extraction:**

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run advanced scraper
python scrape_wowhead_advanced.py

# 3. Check output
cat wowhead_translations.json  # View JSON format
cat translations_output.js     # View JavaScript format

# 4. Copy translations to content.js
# The translations_output.js file contains properly formatted
# JavaScript objects ready to replace the translation dictionaries
# in content.js
```

## Understanding Wowhead's Pagination

Wowhead uses JavaScript-based lazy loading for large datasets:

- **Glyphs**: ~138 items - loads all on initial page ✅
- **Items**: 997+ items - only loads ~100 initially ⚠️
- **Aspects**: ~466 items - only loads sample initially ⚠️

The Selenium-based scrapers attempt to trigger "Show All" buttons and pagination, but Wowhead's implementation may still limit results. The advanced scraper gets significantly more data than the basic scraper.

## Translation Matching

### Basic Scraper
- Extracts German terms only
- Returns with "TODO" placeholders
- Requires manual English matching

### Selenium Scraper
- Extracts both German and English
- Simple alphabetical pairing (unreliable)
- May mismatch items

### Advanced Scraper (RECOMMENDED)
- Extracts with Wowhead item IDs
- Matches German → English by ID
- Accurate 1:1 translations
- Any unmatched items marked "TODO"

## Example Output

### JSON Format (`wowhead_translations.json`)
```json
{
  "glyphs": {
    "Macht": "Might",
    "Ausweiden": "Disembowel"
  },
  "items": {
    "Ring der Sternenlosen Himmel": "Ring of Starless Skies"
  },
  "aspects": {
    "Keilender Aspekt": "Aspect of Shredding Blades"
  }
}
```

### JavaScript Format (`translations_output.js`)
```javascript
// Paragon Glyphs
const glyphTranslations = {
  "Macht": "Might",
  "Ausweiden": "Disembowel",
};

// Unique and Mythic Items
const itemTranslations = {
  "Ring der Sternenlosen Himmel": "Ring of Starless Skies",
};

// Legendary Aspects
const aspectTranslations = {
  "Keilender Aspekt": "Aspect of Shredding Blades",
};
```

## Troubleshooting

### "geckodriver not found"
```bash
# Verify installation
which geckodriver

# If not found, install:
# Linux
sudo pacman -S geckodriver  # Arch
sudo apt install firefox-geckodriver  # Ubuntu

# Or download and add to PATH
```

### "Selenium TimeoutException"
- Increase wait times in scraper (modify `WebDriverWait` timeout)
- Check internet connection
- Verify Wowhead is accessible

### "Found 0 items"
- JavaScript data extraction failed
- Try running with `headless=False` to see browser:
  ```python
  with WowheadTranslationScraper(headless=False) as scraper:
  ```

### Getting incomplete data
- Wowhead may be rate-limiting
- Try adding delays between requests
- Some items may require multiple pagination clicks

## Limitations

1. **Wowhead's Dynamic Loading**: Even with Selenium, Wowhead may not load all 997+ items
2. **Rate Limiting**: Aggressive scraping may be throttled
3. **Tempering Recipes**: Not available on Wowhead - must be added manually from in-game
4. **Season Updates**: New items/glyphs require re-running scraper

## Future Improvements

- [ ] API approach if Wowhead provides one
- [ ] Headless Chrome support
- [ ] Parallel scraping for speed
- [ ] Incremental updates (only fetch new items)
- [ ] Automatic detection of new season content
- [ ] Integration with Diablo 4 API (if available)

## Contributing

When adding new translations manually:
1. Always verify format matches vitablo.de (not Wowhead)
2. For aspects: use "Name Aspekt" not "Aspekt: Name"
3. Test on actual vitablo.de build guides
4. Update appropriate dictionary in `content.js`
