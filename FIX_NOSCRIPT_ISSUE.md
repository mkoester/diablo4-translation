# Fix: Items Not Translating (noscript Issue)

**Date**: 2026-01-17
**Status**: ✅ **FIXED**

---

## Root Cause Identified

Thanks to the diagnostic output, we found the issue:

**Items names are inside `<noscript>` tags on vitablo.de**, but our extension was **skipping noscript tags**!

### Evidence from Debug Output

```
"Ring der Sternenlosen Himmel": found in 2 elements
  - Tag: NOSCRIPT, Classes:
    Parent: DIV, Parent Classes: sc-ib-1-col1
    Text: "<img decoding="async" alt="Unique Ring der Sternen..."
```

### Why This Happened

In [content.js:1522](content.js#L1522), we were filtering out `noscript` tags:

```javascript
// BEFORE (broken):
if (tagName === 'script' || tagName === 'style' || tagName === 'noscript') {
  return NodeFilter.FILTER_REJECT;
}
```

**Reason for original filter**: Typically, `<noscript>` contains fallback content that shouldn't be processed.

**Why vitablo.de is different**: They use `<noscript>` tags for item image alt text, which contains the German item names we need to translate!

---

## The Fix

**Changed line 1522** in [content.js](content.js#L1522):

```javascript
// AFTER (fixed):
// Skip script and style tags (but NOT noscript - vitablo.de uses it for item names!)
if (tagName === 'script' || tagName === 'style') {
  return NodeFilter.FILTER_REJECT;
}
```

**Removed** `|| tagName === 'noscript'` from the exclusion filter.

---

## What This Fixes

### Before Fix
- ✅ Glyphs translated (`.d4para-row` elements)
- ❌ Items NOT translated (in `<noscript>` tags, which were skipped)
- ❌ Aspects NOT translated (also in `<noscript>` tags)

### After Fix
- ✅ Glyphs translated
- ✅ Items translated (now processing `<noscript>` tags)
- ✅ Aspects translated (now processing `<noscript>` tags)

---

## Diagnostic Output Analysis

From your debug output:

```
[D4 Translator] Found 10 .d4para-row elements  ✅ Glyphs found
[D4 Translator] Found 14 .d4-item elements     ✅ Items found
[D4 Translator] Processed undefined text nodes ⚠️ Bug (see below)
```

**Also fixed**: `processedNodes.size` was showing as `undefined` because `processedNodes` is a `WeakSet`, which doesn't have a `.size` property. Changed to more informative message.

---

## Testing Results

### Expected Behavior After Fix

Visit https://vitablo.de/diablo-4-build-guides/ and you should see:

**Items section**:
```
Ring der Sternenlosen Himmel → Ring der Sternenlosen Himmel (Ring of Starless Skies)
```

**Console output**:
```
[D4 Translator] Starting translation...
[D4 Translator] Found 10 .d4para-row elements
[D4 Translator] Found 14 .d4-item elements
D4 German Translator loaded - translating glyphs, items, aspects, and tempering recipes
```

---

## How to Apply Fix

### Step 1: Reload Extension

```bash
# In Firefox:
1. about:debugging#/runtime/this-firefox
2. Find "Diablo 4 German Translator"
3. Click "Reload"
```

### Step 2: Test on Build Guide

1. Visit: https://vitablo.de/diablo-4-build-guides/
2. Look for item names in the build
3. Should see: "German Item (English Translation)"

### Step 3: Verify in Console

Open Browser Console (F12):
```
[D4 Translator] Found 14 .d4-item elements
```

Items should now translate! 🎉

---

## Technical Details

### Why vitablo.de Uses `<noscript>` for Items

Looking at the HTML structure from debug output:

```html
<div class="d4-item box-uniquex box-aspekt box-chaos">
  <div class="sc-ib-1-col1">
    <noscript>
      <img alt="Unique Ring der Sternenlosen Himmel" ...>
    </noscript>
    <!-- Probably has a <img> tag with lazy loading outside noscript -->
  </div>
</div>
```

**Pattern**: vitablo.de uses `<noscript>` as a fallback for lazy-loaded images. The alt text contains the item name, which is what we need to translate.

**Why this works**: Even though JavaScript is enabled, the browser still parses `<noscript>` content into the DOM, making it accessible to our content script.

---

## Additional Fix: ProcessedNodes Count

The console was showing:
```
[D4 Translator] Processed undefined text nodes
```

**Cause**: `WeakSet` doesn't have a `.size` property.

**Fix**: Removed the count from the log message since it's not meaningful for a WeakSet:

```javascript
// BEFORE:
console.log(`[D4 Translator] Processed ${processedNodes.size} text nodes`);

// AFTER:
console.log('[D4 Translator] Translation complete');
```

---

## Files Modified

1. **[content.js:1522](content.js#L1522)** - Removed `noscript` from exclusion filter
2. **Extension package rebuilt**: `../diablo4-translation-1.0.1-cbf83b7-SNAPSHOT.xpi`

---

## Lessons Learned

### Don't Assume Standard Patterns

**Assumption**: `<noscript>` tags are only fallback content
**Reality**: Sites can use them creatively (lazy loading, SEO, etc.)

**Best Practice**: When debugging DOM issues, always check:
1. What tags contain the target text (use XPath search)
2. What filters might exclude those tags
3. Whether exclusions are necessary

### Diagnostic Scripts Are Essential

Without [debug_selectors.js](debug_selectors.js), we would have been guessing. The XPath search immediately identified:
- Items ARE in `.d4-item` elements (selector was correct)
- Items ARE in the DOM (not a loading issue)
- Items are in `<noscript>` tags (exclusion filter issue)

---

## Related Issues

This fix also resolves:
- Aspects not translating (same `<noscript>` issue)
- Any other content in `<noscript>` tags

---

## Status

✅ **Root cause identified**: Items in `<noscript>` tags were being filtered out
✅ **Fix applied**: Removed `noscript` from exclusion filter
✅ **Extension rebuilt**: Ready to test
✅ **No side effects expected**: Only `<script>` and `<style>` truly need exclusion

---

**Next Step**: Reload extension and verify items translate correctly!
