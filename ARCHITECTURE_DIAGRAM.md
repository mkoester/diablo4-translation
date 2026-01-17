# Translation Architecture Diagram

## Current String-Based Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Wowhead German Pages                     │
│  https://www.wowhead.com/diablo-4/de/paragon-glyphs         │
│  https://www.wowhead.com/diablo-4/de/items/quality:5,6      │
│  https://www.wowhead.com/diablo-4/de/aspects                │
└────────────────────┬────────────────────────────────────────┘
                     │ scrape (basic/selenium/advanced)
                     ▼
         ┌───────────────────────┐
         │  Extract German Names │
         │   "Macht"             │
         │   "Zorn"              │
         │   "Kontrolle"  ⚠️      │
         │   "Kontrolle"  ⚠️      │ ← COLLISION!
         └───────────┬───────────┘
                     │
                     ▼
      ┌──────────────────────────────┐
      │   content.js (String-Based)  │
      │                              │
      │  const glyphTranslations = { │
      │    "Macht": "Might",         │
      │    "Zorn": "Wrath",          │
      │    "Kontrolle": "Control"    │ ← Lost one!
      │  };                          │
      └──────────────┬───────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │   Translation Logic   │
         │  (Regex replacement)  │
         └───────────┬───────────┘
                     │
                     ▼
              ┌─────────────┐
              │  vitablo.de │
              │   "Macht    │
              │   (Might)"  │
              └─────────────┘
```

## New ID-Based Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   Wowhead German Pages                      │
│  https://www.wowhead.com/diablo-4/de/...                    │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  Extract with IDs     │
         │  12345: "Macht"       │
         │  12346: "Zorn"        │
         │  12347: "Kontrolle"   │✅ Unique by ID!
         │  12348: "Kontrolle"   │✅ Unique by ID!
         └───────────┬───────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
┌───────────┐ ┌──────────┐ ┌──────────────────┐
│ German DB │ │English DB│ │   Metadata DB    │
│           │ │          │ │                  │
│ 12345: {  │ │12345: {  │ │ 12345: {         │
│   de:     │ │  en:     │ │   quality: 5,    │
│  "Macht"  │ │ "Might"  │ │   class: "barb", │
│ }         │ │ }        │ │   season: 7      │
└─────┬─────┘ └────┬─────┘ └────┬─────────────┘
      │            │            │
      └────────────┴────────────┘
                   │
                   ▼
      ┌──────────────────────────────────┐
      │   content_v2.js (ID-Based)       │
      │                                  │
      │  // ID Database (primary)        │
      │  const glyphsById = {            │
      │    12345: {                      │
      │      de: "Macht",                │
      │      en: "Might",                │
      │      quality: ...                │
      │    },                            │
      │    12347: {                      │
      │      de: "Kontrolle",            │
      │      en: "Control"               │
      │    },                            │
      │    12348: {                      │
      │      de: "Kontrolle",  ✅ Both!  │
      │      en: "Domination"            │
      │    }                             │
      │  };                              │
      │                                  │
      │  // String Lookup (for regex)    │
      │  const glyphsTranslations = {    │
      │    "Macht": "Might",             │
      │    "Kontrolle": "Control"        │
      │  };                              │
      └──────────────┬───────────────────┘
                     │
            ┌────────┴────────┐
            │                 │
            ▼                 ▼
    ┌───────────────┐  ┌─────────────────┐
    │ ID-Based      │  │ String-Based    │
    │ Translation   │  │ Translation     │
    │ (future)      │  │ (current/regex) │
    └───────┬───────┘  └────────┬────────┘
            │                   │
            └─────────┬─────────┘
                      │
                      ▼
               ┌─────────────┐
               │ vitablo.de  │
               │  "Macht     │
               │  (Might)"   │
               └─────────────┘
```

## Data Flow Comparison

### String-Based Flow
```
Wowhead → Extract Name → Store as Key → Lookup → Translate
          ⚠️ collision  ⚠️ no metadata  ❌ hard updates
```

### ID-Based Flow
```
Wowhead → Extract ID+Name → Store by ID → Multi-Format → Translate
          ✅ unique      ✅ metadata    ✅ easy updates
```

## Benefits Visualization

```
╔════════════════════════════════════════════════════════════╗
║                   STRING-BASED (Current)                   ║
╠════════════════════════════════════════════════════════════╣
║  {                                                         ║
║    "Macht": "Might"                                        ║
║  }                                                         ║
║                                                            ║
║  Problems:                                                 ║
║  ❌ Collision if two items named "Macht"                   ║
║  ❌ No metadata (quality, class, etc.)                     ║
║  ❌ Hard to detect Wowhead updates                         ║
║  ❌ Hard to add more languages                             ║
║  ❌ Hard to find new items                                 ║
╚════════════════════════════════════════════════════════════╝

                         ⬇️ UPGRADE ⬇️

╔════════════════════════════════════════════════════════════╗
║                     ID-BASED (New)                         ║
╠════════════════════════════════════════════════════════════╣
║  {                                                         ║
║    12345: {                                                ║
║      de: "Macht",                                          ║
║      en: "Might",                                          ║
║      fr: "Puissance",  ← Easy multi-lang                   ║
║      quality: 5,       ← Metadata                          ║
║      class: "barbarian"                                    ║
║    }                                                       ║
║  }                                                         ║
║                                                            ║
║  Plus string lookup for backward compatibility:            ║
║  { "Macht": "Might" }                                      ║
║                                                            ║
║  Benefits:                                                 ║
║  ✅ No collisions (ID is unique)                           ║
║  ✅ Rich metadata support                                  ║
║  ✅ Easy update detection                                  ║
║  ✅ Easy multi-language                                    ║
║  ✅ Incremental updates                                    ║
║  ✅ Backward compatible                                    ║
╚════════════════════════════════════════════════════════════╝
```

## Migration Strategy

```
Phase 1: Generate ID-Based Data
┌─────────────────────────┐
│ scrape_wowhead_v2.py    │
│                         │
│ Outputs:                │
│ • translations_by_id    │
│ • translations_by_str   │
│ • content_v2.js         │
└────────────┬────────────┘
             │
             ▼
Phase 2: Backward Compatible Deployment
┌─────────────────────────┐
│ content_v2.js includes: │
│                         │
│ ✅ ID database          │
│ ✅ String lookup        │
│ ✅ Helper functions     │
│                         │
│ Current code works!     │
└────────────┬────────────┘
             │
             ▼
Phase 3: Add Enhanced Features
┌─────────────────────────┐
│ • Quality filters       │
│ • Class filters         │
│ • Multi-language        │
│ • Update detection      │
│ • Wowhead links         │
└─────────────────────────┘
```

## Real-World Example

### Scenario: Two items with same German name

```
Wowhead Database:
├─ Glyph ID 12347: "Kontrolle" → "Control"
└─ Glyph ID 12348: "Kontrolle" → "Domination"
```

**String-Based (FAILS):**
```javascript
const glyphs = {
  "Kontrolle": "Control",
  "Kontrolle": "Domination"  // ❌ Overwrites first!
};

// Result: Only "Domination" survives
glyphs["Kontrolle"] // → "Domination" only
```

**ID-Based (WORKS):**
```javascript
const glyphsById = {
  12347: { de: "Kontrolle", en: "Control" },
  12348: { de: "Kontrolle", en: "Domination" }
};

// Both preserved!
glyphsById[12347].en // → "Control"
glyphsById[12348].en // → "Domination"

// String lookup still works (picks first match)
const glyphsTranslations = {
  "Kontrolle": "Control"  // Or create "Kontrolle (1)", "Kontrolle (2)"
};
```

## File Size Comparison

```
┌──────────────────────────────────────────────────┐
│                String-Based Only                 │
├──────────────────────────────────────────────────┤
│  translations.json: ~50 KB                       │
│  content.js: ~55 KB                              │
│  Total: ~105 KB                                  │
└──────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────┐
│            ID-Based + String Lookup              │
├──────────────────────────────────────────────────┤
│  translations_by_id.json: ~70 KB                 │
│  translations_by_string.json: ~50 KB             │
│  content_v2.js: ~85 KB                           │
│  Total: ~205 KB                                  │
│                                                  │
│  Overhead: ~100 KB (~0.1 MB)                     │
│  ✅ Negligible for modern browsers               │
└──────────────────────────────────────────────────┘
```

## Summary

```
                 String-Based    ID-Based
Uniqueness       ❌ Collisions   ✅ Guaranteed
Metadata         ❌ No           ✅ Yes
Updates          ❌ Manual       ✅ Automatic
Multi-Lang       ❌ Hard         ✅ Easy
File Size        ✅ ~105 KB      ⚠️ ~205 KB
Backward Compat  ✅ Native       ✅ Included
Maintainability  ❌ Difficult    ✅ Easy

Recommendation: Use ID-Based! ⭐
```
