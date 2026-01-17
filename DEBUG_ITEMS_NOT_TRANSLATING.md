# Debugging: Items Not Translating

**Issue**: Unique and mythic items are not being translated on vitablo.de build guides
**Date**: 2026-01-17

---

## Quick Diagnostic Steps

### Step 1: Run the Selector Debugger

1. Open a vitablo.de build guide in Firefox (e.g., https://vitablo.de/diablo-4-build-guides/)
2. Open the Browser Console (F12 → Console tab)
3. Copy and paste the contents of [debug_selectors.js](debug_selectors.js) into the console
4. Press Enter to run
5. **Share the console output** - it will tell us what selectors vitablo.de actually uses

### Step 2: Verify Extension is Running

In the browser console, check for:
```javascript
// Should see this message if extension loaded:
"D4 German Translator loaded - translating glyphs, items, aspects, and tempering recipes"
```

If you DON'T see this message, the extension isn't loading. Check:
- Extension is enabled in `about:addons`
- You're on a page matching `*://vitablo.de/*build-guide*`

### Step 3: Manual Test

In the browser console, test if the translation function works:

```javascript
// Get all translations
console.log('Total translations:', Object.keys(allTranslations).length);

// Test a specific item
console.log('Ring translation:', allTranslations['Ring der Sternenlosen Himmel']);
// Should output: "Ring of Starless Skies"

// Test if items are defined
console.log('Item translations:', Object.keys(itemTranslations).length);
// Should output: 848
```

---

## Possible Causes

### Cause 1: Wrong CSS Selector

**Current assumption**: Items are in `.d4-item` elements
**Reality**: vitablo.de might use different class names

**Evidence needed**: Output from debug_selectors.js

**Fix if confirmed**: Update content.js selectors to match actual class names

### Cause 2: Items Load After Observer Starts

**Symptom**: Glyphs work but items don't
**Cause**: Items might load dynamically via AJAX after page load

**Test**:
1. Open page, wait 5 seconds
2. Reload extension (about:debugging → Reload)
3. Check if items translate now

**Fix if confirmed**: Add a delayed retry or better MutationObserver configuration

### Cause 3: Item Names Don't Match Exactly

**Symptom**: Some items translate, others don't
**Cause**: Extra spaces, different formatting, or special characters

**Test in console**:
```javascript
// Find all text nodes
const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
let textNodes = [];
while (walker.nextNode()) {
  if (walker.currentNode.textContent.includes('Ring der Sternenlosen')) {
    textNodes.push(walker.currentNode);
  }
}
console.log('Found "Ring der Sternenlosen" in:', textNodes);
textNodes.forEach(node => {
  console.log('Exact text:', JSON.stringify(node.textContent));
  console.log('Parent:', node.parentElement.tagName, node.parentElement.className);
});
```

**Fix if confirmed**: Adjust regex pattern or add text normalization

### Cause 4: Items in Excluded Sections

**Current code**: Only processes `.d4para-row` and `.d4-item` elements
**Cause**: Items might be in different container

**Fix**: Expand selectors or process entire page

---

## Quick Fixes to Try

### Fix 1: Process Entire Page (Nuclear Option)

Replace the selector-based approach with a global text replacement:

```javascript
// In content.js, replace initialTranslation() with:
function initialTranslation() {
  // Translate everything on the page
  walkTextNodes(document.body);
}
```

**Pros**: Will definitely catch all items
**Cons**: Might translate things we don't want (navigation, etc.)

### Fix 2: Add More Selectors

Add common container patterns:

```javascript
function initialTranslation() {
  // Current selectors
  document.querySelectorAll('.d4para-row').forEach(row => walkTextNodes(row));
  document.querySelectorAll('.d4-item').forEach(item => walkTextNodes(item));

  // Additional selectors
  document.querySelectorAll('[class*="item"]').forEach(el => walkTextNodes(el));
  document.querySelectorAll('[class*="gear"]').forEach(el => walkTextNodes(el));
  document.querySelectorAll('[class*="equipment"]').forEach(el => walkTextNodes(el));

  // Or just translate the main content area
  const main = document.querySelector('main, article, .content, .build');
  if (main) walkTextNodes(main);
}
```

### Fix 3: Delayed Translation

Add a retry mechanism:

```javascript
// After initialTranslation(), add:
setTimeout(() => {
  console.log('D4 Translator: Retrying translation after delay');
  document.querySelectorAll('.d4-item, [class*="item"]').forEach(item => {
    walkTextNodes(item);
  });
}, 2000); // Wait 2 seconds for dynamic content
```

---

## Systematic Debugging Process

### Phase 1: Identify the Problem

1. ✅ Run debug_selectors.js
2. ✅ Check console for extension load message
3. ✅ Verify translations are loaded (`Object.keys(itemTranslations).length`)
4. ✅ Find where items appear in DOM (XPath search from debug script)

### Phase 2: Verify Selector

From debug_selectors.js output:
- If "Ring der Sternenlosen Himmel" is found in elements → Note the tag/class
- If `.d4-item` has 0 elements → Selector is wrong
- If `.d4-item` has elements but no item names → Items are elsewhere

### Phase 3: Test Fix

Based on Phase 2 findings:
- Update selectors in content.js
- Reload extension
- Test on build guide page

### Phase 4: Report Findings

Please share:
1. Output from debug_selectors.js
2. Console output (any errors?)
3. URL of a build guide you're testing on
4. Screenshot showing items not translated

---

## Expected Behavior

When working correctly:
- **Glyphs**: "Macht" → "Macht (Might)" in Paragon section
- **Items**: "Ring der Sternenlosen Himmel" → "Ring der Sternenlosen Himmel (Ring of Starless Skies)"
- **Aspects**: "Schneeverschleierter Aspekt" → "Schneeverschleierter Aspekt (Snowveiled Aspect)"

---

## Next Steps

**Option A**: Run debug_selectors.js and share output
**Option B**: Try Fix 1 (process entire page) as quick test
**Option C**: Check if glyphs are working (confirms extension loads)

---

## Files to Check

- [content.js](content.js:1545-1550) - Lines 1545-1550 contain the selector definitions
- [debug_selectors.js](debug_selectors.js) - Diagnostic script to run in browser console
- [manifest.json](manifest.json) - Verify URL pattern matches: `*://vitablo.de/*build-guide*`

---

**Status**: Awaiting diagnostic information
**Priority**: High - Items are the main translation target
