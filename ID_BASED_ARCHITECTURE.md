# ID-Based Translation Architecture

## Overview

Instead of using German strings as dictionary keys, use **Wowhead item IDs** as the primary key. This provides a more robust, scalable, and maintainable translation system.

## Current vs. ID-Based Architecture

### Current Architecture (String-Based)

```javascript
// content.js - Current approach
const glyphTranslations = {
  "Macht": "Might",
  "Zorn": "Wrath",
  // ...
};

// Usage: Direct string lookup
const english = glyphTranslations["Macht"]; // "Might"
```

**Problems:**
- ❌ String collisions possible (same German name for different items)
- ❌ Hard to track which items are missing
- ❌ No metadata (quality, class, etc.)
- ❌ Difficult to sync with Wowhead updates
- ❌ Can't easily add more languages

### ID-Based Architecture (Proposed)

```javascript
// content_v2.js - ID-based approach
const glyphsById = {
  12345: { de: "Macht", en: "Might" },
  12346: { de: "Zorn", en: "Wrath" },
  // ...
};

// Also provide string lookup for regex matching
const glyphsTranslations = {
  "Macht": "Might",
  "Zorn": "Wrath",
  // ...
};
```

**Benefits:**
- ✅ Guaranteed unique by Wowhead ID
- ✅ Can store metadata (quality, class restrictions, etc.)
- ✅ Easy to track new/changed items
- ✅ Future-proof for multi-language support
- ✅ Can detect when Wowhead IDs change (item renamed)
- ✅ Still supports fast string lookup for regex

## Data Structure

### ID-Based Format

```json
{
  "glyphs": {
    "12345": {
      "de": "Macht",
      "en": "Might"
    }
  },
  "items": {
    "67890": {
      "de": "Ring der Sternenlosen Himmel",
      "en": "Ring of Starless Skies",
      "quality": 5
    }
  }
}
```

### String-Based Format (for backward compatibility)

```json
{
  "glyphs": {
    "Macht": "Might"
  },
  "items": {
    "Ring der Sternenlosen Himmel": "Ring of Starless Skies"
  }
}
```

## Implementation Strategy

### Phase 1: Dual Format (Backward Compatible)
Keep both ID-based and string-based lookups in content.js:

```javascript
// ID database (primary source of truth)
const glyphsById = { ... };

// String lookup (derived from ID database, used for regex)
const glyphsTranslations = { ... };

// Current translation logic continues to work unchanged
```

### Phase 2: Enhanced Features
Once ID data is available, add new capabilities:

```javascript
// Check if vitablo.de page contains Wowhead IDs
if (element.dataset.wowheadId) {
  const id = parseInt(element.dataset.wowheadId);
  const translation = getTranslationById('items', id);
  // More accurate than string matching
}

// Filter by quality
function getMythicItems() {
  return Object.values(itemsById)
    .filter(item => item.quality === 6);
}

// Find missing translations
function getMissingTranslations() {
  return Object.entries(glyphsById)
    .filter(([id, data]) => !data.en)
    .map(([id, data]) => ({ id, de: data.de }));
}
```

### Phase 3: Multi-Language Support
Easily add more languages:

```javascript
const glyphsById = {
  12345: {
    de: "Macht",
    en: "Might",
    fr: "Puissance",  // French
    es: "Poder",      // Spanish
    ja: "力"          // Japanese
  }
};

// Select language
const userLang = navigator.language.slice(0, 2);
const translation = glyphsById[12345][userLang] || glyphsById[12345].en;
```

## Use Cases

### 1. Accurate Translation Updates

**Problem:** Wowhead changes "Ring der Sternenlosen Himmel" to "Ring der Sternenlos Himmel"

**String-based approach:**
- Old translation no longer matches
- Must manually find and update
- No way to know what changed

**ID-based approach:**
```javascript
// ID 67890 German name changed from:
// "Ring der Sternenlosen Himmel" → "Ring der Sternenlos Himmel"

// Automatic detection:
const oldData = previousTranslations.items[67890];
const newData = currentTranslations.items[67890];
if (oldData.de !== newData.de) {
  console.log(`ID ${67890} name changed: ${oldData.de} → ${newData.de}`);
}
```

### 2. Quality Filtering

```javascript
// Show only mythic items in UI
function renderMythicItems() {
  return Object.entries(itemsById)
    .filter(([id, data]) => data.quality === 6)
    .map(([id, data]) => `${data.de} (${data.en})`);
}
```

### 3. Incremental Updates

```javascript
// Fetch only new items since last update
const existingIds = new Set(Object.keys(itemsById).map(Number));
const newItems = wowheadData.filter(item => !existingIds.has(item.id));

console.log(`Found ${newItems.length} new items to translate`);
```

### 4. Cross-Reference with Build Guides

If vitablo.de starts using Wowhead IDs in their HTML:

```html
<!-- vitablo.de might add data attributes -->
<div class="d4-item" data-wowhead-id="67890">
  Ring der Sternenlosen Himmel
</div>
```

```javascript
// Direct ID lookup (more accurate than regex)
function translateByWowheadId(element) {
  const id = parseInt(element.dataset.wowheadId);
  const item = itemsById[id];
  if (item) {
    element.textContent = `${item.de} (${item.en})`;
  }
}
```

## Migration Path

### Step 1: Extract with IDs
```bash
python3 scrape_wowhead_v2.py
# Creates: translations_by_id.json, content_v2.js
```

### Step 2: Test with current extension
- Keep existing string-based translation logic
- Add ID database alongside for future features
- No breaking changes

### Step 3: Add helper functions
```javascript
// content_v2.js provides:
function getTranslationById(category, id)
function getEnglishFromGerman(germanText)  // backward compatible
function findById(id)  // search all categories
```

### Step 4: Gradually enhance
- Use IDs where available
- Fall back to string matching where needed
- Add new features (quality filters, update detection, etc.)

## File Outputs

Running `scrape_wowhead_v2.py` creates:

### 1. `translations_by_id.json`
```json
{
  "glyphs": {
    "12345": { "de": "Macht", "en": "Might" },
    "12346": { "de": "Zorn", "en": "Wrath" }
  },
  "items": {
    "67890": {
      "de": "Ring der Sternenlosen Himmel",
      "en": "Ring of Starless Skies",
      "quality": 5
    }
  }
}
```

### 2. `translations_by_string.json`
Backward-compatible format (current content.js format)

### 3. `content_v2.js`
Enhanced content.js with both ID and string-based lookups

## Future Enhancements

With ID-based architecture, these become easy:

1. **Translation Dashboard**: Web UI showing translation coverage
2. **Auto-Update Checker**: Detect when Wowhead data changes
3. **Translation API**: Expose translations as API for other tools
4. **Quality Badges**: Show item quality (unique/mythic) in translations
5. **Class Filters**: Filter translations by character class
6. **Season Tracking**: Track which items belong to which season
7. **Diff Tool**: Compare translations between versions

## Comparison

| Feature | String-Based | ID-Based |
|---------|--------------|----------|
| Uniqueness | ❌ Potential collisions | ✅ Guaranteed unique |
| Metadata | ❌ No | ✅ Yes (quality, etc.) |
| Updates | ❌ Manual | ✅ Automated detection |
| Multi-language | ❌ Difficult | ✅ Easy |
| Backward compat | ✅ Current format | ✅ Includes strings |
| Performance | ✅ Fast regex | ✅ Same (string lookup preserved) |
| Maintenance | ❌ Hard | ✅ Easy |

## Recommendation

**Use ID-based architecture going forward:**

1. Run `scrape_wowhead_v2.py` to generate ID-based data
2. Use `content_v2.js` as a drop-in replacement
3. Keep string-based lookups for regex performance
4. Add ID-based features incrementally
5. Build tools around the ID database

This provides:
- ✅ Backward compatibility (no breaking changes)
- ✅ Future-proof architecture
- ✅ Easy maintenance and updates
- ✅ Foundation for advanced features
