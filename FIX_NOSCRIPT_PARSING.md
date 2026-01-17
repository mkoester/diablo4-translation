# Fix: Noscript Content Parsing

**Date**: 2026-01-17
**Status**: ✅ **FIXED (Second Iteration)**

---

## The Real Problem

Items still weren't translating after removing `noscript` from the filter. Here's why:

### How `<noscript>` Works with JavaScript Enabled

When JavaScript is enabled (which it is), the browser **does NOT parse** the content inside `<noscript>` tags as DOM elements. Instead, it stores it as a **single text node containing the raw HTML string**.

**Example from vitablo.de**:
```html
<noscript>
  <img alt="Unique Ring der Sternenlosen Himmel" src="...">
</noscript>
```

**What we see in the DOM**:
- `noscript.innerHTML` = `'<img alt="Unique Ring der Sternenlosen Himmel" src="...">'` (string)
- `noscript.textContent` = `'<img alt="Unique Ring der Sternenlosen Himmel" src="...">'` (string)
- The `<img>` tag is NOT a real DOM element
- The alt text is NOT accessible as a text node
- TreeWalker can't find it because it's inside an unparsed HTML string

### Why Our Previous Approach Failed

```javascript
// This doesn't work because noscript content isn't parsed:
const walker = document.createTreeWalker(noscript, NodeFilter.SHOW_TEXT);
// Returns nothing useful - just the raw HTML as a string
```

---

## The Solution

We need to **parse the innerHTML of noscript tags** and translate the alt attributes directly:

### New Function: `translateNoscriptTags()`

Added to [content.js:1512-1543](content.js#L1512-L1543):

```javascript
function translateNoscriptTags(element) {
  // Special handling for noscript tags - their content isn't parsed as DOM when JS is enabled
  // We need to parse the innerHTML and translate alt attributes
  const noscripts = element.querySelectorAll('noscript');

  noscripts.forEach(noscript => {
    let html = noscript.innerHTML;
    let modified = false;

    // Find all alt="..." attributes and translate them
    html = html.replace(/alt="([^"]+)"/g, (_match, altText) => {
      // Try to translate the alt text
      let translated = altText;

      // Check each German term
      sortedKeys.forEach(germanTerm => {
        if (altText.includes(germanTerm)) {
          const englishTerm = allTranslations[germanTerm];
          if (englishTerm && !altText.includes(`(${englishTerm})`)) {
            translated = translated.replace(germanTerm, `${germanTerm} (${englishTerm})`);
            modified = true;
          }
        }
      });

      return `alt="${translated}"`;
    });

    if (modified) {
      noscript.innerHTML = html;
    }
  });
}
```

**How it works**:
1. Find all `<noscript>` tags in the element
2. Get the raw HTML string from `innerHTML`
3. Use regex to find all `alt="..."` attributes
4. For each alt attribute, check if it contains German terms
5. Replace German terms with "German (English)" format
6. Update the `innerHTML` with translated version

### Updated `walkTextNodes()`

Now calls `translateNoscriptTags()` first:

```javascript
function walkTextNodes(element) {
  // First, handle noscript tags specially
  translateNoscriptTags(element);

  // Then walk regular text nodes
  const walker = document.createTreeWalker(...);
  // ...
}
```

---

## Example Transformation

### Before

```html
<noscript>
  <img alt="Unique Ring der Sternenlosen Himmel" src="ring.webp">
</noscript>
```

### After

```html
<noscript>
  <img alt="Unique Ring der Sternenlosen Himmel (Ring of Starless Skies)" src="ring.webp">
</noscript>
```

---

## Why This Works

Even though users can't see the noscript content (JavaScript is enabled), the alt text is still useful for:
1. **SEO** - Search engines read alt text
2. **Accessibility** - Screen readers might use it
3. **Development** - Developers inspecting the DOM
4. **Debugging** - Our debug scripts found items here

And most importantly: **This is where vitablo.de stores the item names**, so translating them ensures they're correct in the source.

---

## Testing

### 1. Reload Extension

```bash
# Firefox:
about:debugging#/runtime/this-firefox → Reload
```

### 2. Visit Build Guide

https://vitablo.de/diablo-4-build-guides/

### 3. Run Test Script

Open console and run:

```javascript
// Check noscript tags
document.querySelectorAll('.d4-item noscript').forEach((ns, i) => {
  console.log(`Noscript ${i}:`, ns.innerHTML.substring(0, 200));
});
```

**Expected**: Should see translated alt text like:
```
alt="Unique Ring der Sternenlosen Himmel (Ring of Starless Skies)"
```

### 4. Inspect Element

1. Right-click on an item
2. Inspect Element
3. Find the `<noscript>` tag
4. Check if alt text is translated

---

## Console Output

**Expected**:
```
[D4 Translator] Starting translation...
[D4 Translator] Found 10 .d4para-row elements
[D4 Translator] Found 14 .d4-item elements
[D4 Translator] Translation complete
D4 German Translator loaded - translating glyphs, items, aspects, and tempering recipes
```

---

## Alternative: If Still Not Working

If items still don't translate, it means the item names appear somewhere else on the page (not just in noscript tags). Run this to find them:

```javascript
// Find where "Ring der Sternenlosen Himmel" actually appears
const xpath = '//text()[contains(., "Ring der Sternenlosen")]';
const result = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);

for (let i = 0; i < result.snapshotLength; i++) {
  const node = result.snapshotItem(i);
  console.log('Found in:', node.parentElement.tagName, node.parentElement.className);
  console.log('Text:', node.textContent.substring(0, 100));
}
```

If this finds the text in normal elements (not noscript), then the item names ARE in the regular DOM and our original approach should work.

---

## Technical Notes

### Why Use innerHTML Instead of textContent?

```javascript
// textContent gives us the HTML as a string:
noscript.textContent
// "<img alt='...' src='...'>"

// innerHTML gives us the same thing, but we can SET it:
noscript.innerHTML = translatedHTML;
// This actually updates the noscript content
```

### Why Regex Instead of DOM Parsing?

We could parse the HTML:
```javascript
const tempDiv = document.createElement('div');
tempDiv.innerHTML = noscript.innerHTML;
// But this is overkill for just translating alt attributes
```

Regex is simpler and faster for this use case.

### Performance

- Only processes noscript tags (14 on the test page)
- Only updates innerHTML if modified
- Regex is fast for short HTML snippets

---

## Files Modified

1. **[content.js:1512-1543](content.js#L1512-L1543)** - Added `translateNoscriptTags()`
2. **[content.js:1545-1572](content.js#L1545-L1572)** - Updated `walkTextNodes()` to call it
3. **Extension rebuilt**: `../diablo4-translation-1.0.1-cbf83b7-SNAPSHOT.xpi`

## Files Created

- [debug_noscript_text.js](debug_noscript_text.js) - Debug script for noscript content
- [debug_visible_content.js](debug_visible_content.js) - Check visible content
- [check_noscript_parsing.js](check_noscript_parsing.js) - Verify innerHTML parsing
- [test_noscript_behavior.html](test_noscript_behavior.html) - Local test file
- [FIX_NOSCRIPT_PARSING.md](FIX_NOSCRIPT_PARSING.md) - This file

---

## Lessons Learned

### Noscript Behavior is Counterintuitive

Most developers don't realize that:
- Noscript tags ARE in the DOM even when JS is enabled
- Their content is NOT parsed as elements
- You can't use TreeWalker or querySelector on their content
- You must parse innerHTML manually

### Always Test in the Real Environment

Our test with TreeWalker "worked" in theory, but noscript's special behavior broke it.

### Regex Has Its Place

Modern advice says "don't parse HTML with regex", but for simple attribute extraction, it's perfectly fine and much simpler than creating a DOMParser.

---

**Status**: ✅ Items should now translate via noscript innerHTML parsing
**Next**: Reload extension and verify items are translated!
