# Solution: Items Not Translating

**Issue**: Unique and mythic items not being translated on vitablo.de
**Date**: 2026-01-17
**Status**: Diagnostic version created

---

## What I Did

### 1. Enhanced content.js with Diagnostics

Modified [content.js:1542-1574](content.js#L1542-L1574) to:

**Added console logging**:
```javascript
console.log('[D4 Translator] Found X .d4para-row elements');
console.log('[D4 Translator] Found X .d4-item elements');
console.log('[D4 Translator] Processed X text nodes');
```

**Added fallback logic**:
If `.d4-item` elements are not found (length === 0), the extension now:
1. Tries to find main content area (`main`, `article`, `.content`, etc.)
2. If that fails, translates the entire `body`

This ensures items will be translated even if they're not in `.d4-item` containers.

### 2. Created Diagnostic Tools

**[debug_selectors.js](debug_selectors.js)** - Browser console script that:
- Searches for `.d4-item` and `.d4para-row` elements
- Searches for German item names in the DOM
- Identifies what tags/classes contain items
- Suggests correct selectors

**[DEBUG_ITEMS_NOT_TRANSLATING.md](DEBUG_ITEMS_NOT_TRANSLATING.md)** - Complete debugging guide with:
- Step-by-step diagnostic process
- Possible causes and fixes
- Quick fixes to try
- How to interpret debug output

### 3. Rebuilt Extension

New package: `../diablo4-translation-1.0.1-cbf83b7-SNAPSHOT.xpi`

---

## How to Test

### Step 1: Reload the Extension

```bash
# In Firefox:
1. about:debugging#/runtime/this-firefox
2. Find "Diablo 4 German Translator"
3. Click "Reload"
```

### Step 2: Open Build Guide

Visit any build guide: https://vitablo.de/diablo-4-build-guides/

### Step 3: Check Console

Open Browser Console (F12 → Console):

**Look for these messages**:
```
[D4 Translator] Starting translation...
[D4 Translator] Found X .d4para-row elements
[D4 Translator] Found X .d4-item elements
[D4 Translator] Processed X text nodes
D4 German Translator loaded - translating glyphs, items, aspects, and tempering recipes
```

**Interpret the output**:

| Output | Meaning | Next Step |
|--------|---------|-----------|
| `.d4-item elements: 0` | Items not in `.d4-item` | Fallback should activate |
| `.d4-item elements: 50+` | Items found, should work | Check if items translate |
| `Processed X nodes: 0` | Nothing translated | Run debug_selectors.js |
| `Processed X nodes: 1000+` | Lots translated | Check if items included |

### Step 4: Test Translation

**If items still don't translate**, run the diagnostic script:

1. Open Console (F12)
2. Copy entire contents of [debug_selectors.js](debug_selectors.js)
3. Paste into console and press Enter
4. **Share the output** - it will tell us exactly where items are

---

## Expected Results

### Scenario A: Items in .d4-item Elements

**Console output**:
```
[D4 Translator] Found 50 .d4-item elements
[D4 Translator] Processed 500 text nodes
```

**Result**: Items should translate ✅

### Scenario B: Items NOT in .d4-item Elements

**Console output**:
```
[D4 Translator] Found 0 .d4-item elements
[D4 Translator] No .d4-item elements found, trying main content area
[D4 Translator] Found main content area, translating...
[D4 Translator] Processed 2000 text nodes
```

**Result**: Items should translate via fallback ✅

### Scenario C: No Translation Happening

**Console output**:
```
[D4 Translator] Processed 0 text nodes
```

**Problem**: Either:
- German text not present (wrong page?)
- Text in script/style tags (excluded)
- Text hasn't loaded yet (dynamic loading)

**Next step**: Run debug_selectors.js to find where items are

---

## Possible Issues & Solutions

### Issue 1: .d4-item Selector is Wrong

**Symptoms**:
- Console shows `Found 0 .d4-item elements`
- Glyphs work (`.d4para-row` is correct)
- Items don't translate even with fallback

**Solution**: Identified by debug_selectors.js
- Update selector in content.js
- Example: if items are in `.gear-item`, change:
  ```javascript
  document.querySelectorAll('.gear-item').forEach(item => {
    walkTextNodes(item);
  });
  ```

### Issue 2: Items Load Dynamically

**Symptoms**:
- Console shows correct element count
- Items don't translate initially
- Refreshing extension makes them work

**Solution**: Add delayed retry
```javascript
// Add to content.js after setupObserver()
setTimeout(() => {
  console.log('[D4 Translator] Delayed retry...');
  initialTranslation();
}, 3000);
```

### Issue 3: Item Names Don't Match Exactly

**Symptoms**:
- Some items translate, others don't
- Console shows items found and processed

**Solution**: Text normalization or regex adjustments

**Debug**: In console, check exact text:
```javascript
// Find item elements
const items = document.querySelectorAll('.d4-item, [class*="item"]');
items.forEach(item => {
  const text = item.textContent;
  if (text.includes('Ring') || text.includes('Ozelot')) {
    console.log('Item text:', JSON.stringify(text.substring(0, 100)));
  }
});
```

---

## What Changed

### Before (Original content.js)

```javascript
function initialTranslation() {
  document.querySelectorAll('.d4para-row').forEach(row => {
    walkTextNodes(row);
  });
  document.querySelectorAll('.d4-item').forEach(item => {
    walkTextNodes(item);
  });
}
```

**Problem**: If `.d4-item` doesn't exist, items never get translated.

### After (Enhanced content.js)

```javascript
function initialTranslation() {
  console.log('[D4 Translator] Starting translation...');

  const paraRows = document.querySelectorAll('.d4para-row');
  console.log(`[D4 Translator] Found ${paraRows.length} .d4para-row elements`);
  paraRows.forEach(row => walkTextNodes(row));

  const d4Items = document.querySelectorAll('.d4-item');
  console.log(`[D4 Translator] Found ${d4Items.length} .d4-item elements`);
  d4Items.forEach(item => walkTextNodes(item));

  // FALLBACK: If no .d4-item elements, try main content
  if (d4Items.length === 0) {
    console.log('[D4 Translator] No .d4-item elements found, trying main content area');
    const mainContent = document.querySelector('main, article, .content, .build-content, #content');
    if (mainContent) {
      console.log('[D4 Translator] Found main content area, translating...');
      walkTextNodes(mainContent);
    } else {
      console.log('[D4 Translator] No main content area found, translating body');
      walkTextNodes(document.body);
    }
  }

  console.log(`[D4 Translator] Processed ${processedNodes.size} text nodes`);
}
```

**Benefits**:
- Console logging for diagnostics
- Fallback to main content area
- Counts processed nodes

---

## Next Actions

1. **Reload extension** in Firefox
2. **Visit build guide** page
3. **Check console** for diagnostic messages
4. **Report back** with:
   - Console output (especially the `[D4 Translator]` messages)
   - Are glyphs translating? (Yes/No)
   - Are items translating? (Yes/No)
   - URL of page you're testing

If items still don't translate:
5. **Run debug_selectors.js** in console
6. **Share the output** so we can identify the correct selectors

---

## Files Modified

- [content.js](content.js:1542-1574) - Enhanced with logging and fallback
- Extension package rebuilt: `../diablo4-translation-1.0.1-cbf83b7-SNAPSHOT.xpi`

## Files Created

- [debug_selectors.js](debug_selectors.js) - Diagnostic script for browser console
- [DEBUG_ITEMS_NOT_TRANSLATING.md](DEBUG_ITEMS_NOT_TRANSLATING.md) - Full debugging guide
- [ITEMS_NOT_TRANSLATING_SOLUTION.md](ITEMS_NOT_TRANSLATING_SOLUTION.md) - This file
- [content.js.backup](content.js.backup) - Backup of original

---

**Status**: ✅ Diagnostic version ready to test
**Next**: Reload extension and check console output
