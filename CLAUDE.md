# D4 German Translator

Firefox extension that translates German Diablo 4 terms to English on vitablo.de, including:
- Paragon glyphs
- Unique and mythic items
- Legendary aspects
- Tempering recipes

## Structure

- `manifest.json` - Manifest V3, targets `*://vitablo.de/*build-guide*`
- `content.js` - MutationObserver-based translator with organized translation dictionaries

## How It Works

1. Content script runs on matching build guide pages
2. Translates text within:
   - `.d4para-row` elements (paragon board rows) - for glyphs
   - `.d4-item` elements (item containers) - for items, aspects, and tempering recipes
3. Replaces German terms with "German (English)" format
4. MutationObserver watches for dynamically loaded content

## Translation Architecture

The extension uses four separate translation dictionaries in `content.js`:

```javascript
// Paragon glyphs (~120 translations)
const glyphTranslations = {
  "Macht": "Might",
  // ...
};

// Unique and mythic items (~60 translations)
const itemTranslations = {
  "Ring der Sternenlosen Himmel": "Ring of Starless Skies",
  // ...
};

// Legendary aspects (~30 translations)
const aspectTranslations = {
  "Schneeverschleierter Aspekt": "Snowveiled Aspect",
  // ...
};

// Tempering recipes (~20 translations)
const temperingTranslations = {
  "Weltliche Beständigkeit": "Worldly Endurance",
  // ...
};
```

All dictionaries are merged into `allTranslations` for pattern matching.

## Adding New Translations

Add entries to the appropriate translation object in `content.js`:

1. **Glyphs**: Add to `glyphTranslations`
2. **Items**: Add to `itemTranslations`
3. **Aspects**: Add to `aspectTranslations`
4. **Tempering**: Add to `temperingTranslations`

### Important Notes

**Aspect Name Format Discrepancy:**
- Wowhead German database uses: `"Aspekt: Name"` (with colon) for some of the items
- Vitablo.de actually uses: `"Name Aspekt"` (without colon)
- **Always use the vitablo.de format** (without colon) in translations
- Examples:
  - ✅ Correct: `"Keilender Aspekt": "Aspect of Shredding Blades"`
  - ❌ Wrong: `"Aspekt: Keilender": "Aspect of Shredding Blades"`

## Testing

1. `about:debugging` → This Firefox → Load Temporary Add-on → select `manifest.json`
2. Visit any build guide: https://vitablo.de/diablo-4-build-guides/
3. Check both the Paragon section and "Items & Aspekte" section for translations

## Translation Sources

### Paragon Glyphs
- https://www.wowhead.com/diablo-4/paragon-glyphs (English)
- https://www.wowhead.com/diablo-4/de/paragon-glyphs (German)

### Unique Items
- https://www.wowhead.com/diablo-4/items/quality:5,6 (English - Unique/Mythic)
- https://www.wowhead.com/diablo-4/de/items/quality:5,6 (German - Unique/Mythic)

### Legendary Aspects
- https://www.wowhead.com/diablo-4/aspects (English)
- https://www.wowhead.com/diablo-4/de/aspects (German)

### Tempering Recipes
- Found in-game or on build guides

## Extraction Notes (2026-01-17)

### Wowhead Data Extraction Process

Extracted German terms from Wowhead and added to `content.js` with "TODO" placeholders for English translations.

#### Wowhead Pagination Challenges
- Wowhead uses dynamic JavaScript loading for data
- Direct WebFetch only captures initially loaded content
- **Glyphs**: Successfully extracted all 138 glyphs (single page load)
- **Items**: Page reports 997 unique items + mythic items, but only shows ~100 per initial load
- **Aspects**: Page reports 466 total aspects, but only shows sample in initial load

#### Added German Terms with TODO Placeholders

**Paragon Glyphs (11 new):**
- Fitness, Ausweiden, Hackbeil, Scharfrichter, Stalagmit, Ferne, Infusion, Geübt, Elektrifizieren, Torf, Bann

**Mythic Items (10 new):**
- Griswolds Opus, Orsivane, Dämmerfeuer, Herold der Zakarum, Geläutertes Horn Duriels, Siegel des Zweiten Horns, Geläutertes Auge Belials, Geläuterte Klaue Andariels, Geläuterte Zunge Azmodans, Silberschleier

**Unique Items (7 new):**
- Ende des Kaisers, Enigmawürfel, Schlangenstein, Tracht des Unheilvollen Vorhabens, Schmiedetruhe, Außergewöhnliche Rüstung, Skelettierter Beschützer

**Aspects (1 new):**
- Schlachthäuptlings Aspekt

#### Automated Translation Extraction (2026-01-17)

**Three scraping tools are now available** for automated Wowhead data extraction:

1. **`scrape_wowhead.py`** - Basic scraper (requests only)
   - Fast, lightweight, no browser dependencies
   - Limited to initial page load (~100 items max)

2. **`scrape_wowhead_selenium.py`** - Enhanced scraper with JavaScript support
   - Executes JavaScript for dynamic content
   - Attempts pagination handling
   - Requires Firefox/geckodriver

3. **`scrape_wowhead_advanced.py`** - ⭐ **RECOMMENDED**
   - ID-based German-English matching (accurate translations)
   - Full JavaScript support and pagination
   - Exports to JSON and JavaScript formats
   - Requires Firefox/geckodriver

**Setup:**
```bash
# Install dependencies
./setup_scraper.sh

# Or manually:
sudo pacman -S firefox geckodriver  # Arch/CachyOS
pip install -r requirements.txt
```

**Quick start:**
```bash
python3 scrape_wowhead_advanced.py
# Output: wowhead_translations.json, translations_output.js
```

**See [SCRAPING.md](SCRAPING.md) for detailed documentation.**

#### Wowhead URL Patterns
- Unique items only: `https://www.wowhead.com/diablo-4/de/items/quality:5`
- Mythic items only: `https://www.wowhead.com/diablo-4/de/items/quality:6`
- Combined: `https://www.wowhead.com/diablo-4/de/items/quality:5,6`

## Git Flow Convention

This project follows the git flow branching model:

### Branch Structure

- `main` - Production-ready code, tagged releases
- `develop` - Integration branch for features, default development branch
- `feature/*` - New features (branch from `develop`, merge back to `develop`)
- `bugfix/*` - Bug fixes for develop (branch from `develop`, merge back to `develop`)
- `hotfix/*` - Urgent production fixes (branch from `main`, merge to both `main` and `develop`)
- `release/*` - Release preparation (branch from `develop`, merge to both `main` and `develop`)

### Workflow

1. **New features**: Create `feature/feature-name` from `develop`
2. **Bug fixes**: Create `bugfix/bug-description` from `develop`
3. **Releases**: Create `release/x.y.z` from `develop`, merge to `main` and `develop`
4. **Hotfixes**: Create `hotfix/x.y.z` from `main`, merge to `main` and `develop`
5. **Pull requests**: Target `develop` for features/bugfixes, `main` for releases/hotfixes

### Commands

```bash
# Start a new feature
git checkout develop
git checkout -b feature/feature-name

# Finish a feature (via PR to develop)
git push -u origin feature/feature-name

# Start a release
git checkout develop
git checkout -b release/1.0.0

# Finish a release (via PR to main and develop)
git push -u origin release/1.0.0
```
