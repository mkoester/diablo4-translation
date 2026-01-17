// Test version of content.js with broader selector matching
// This version tries to translate items in more places to help diagnose the issue

// Copy the entire content.js first, then modify the initialTranslation function:

// Replace the initialTranslation() function with this expanded version:
function initialTranslation() {
  console.log('D4 Translator: Starting initial translation with expanded selectors');

  // Original selectors
  const d4ParaRows = document.querySelectorAll('.d4para-row');
  console.log(`Found ${d4ParaRows.length} .d4para-row elements`);
  d4ParaRows.forEach(row => walkTextNodes(row));

  const d4Items = document.querySelectorAll('.d4-item');
  console.log(`Found ${d4Items.length} .d4-item elements`);
  d4Items.forEach(item => walkTextNodes(item));

  // Try alternative selectors
  const itemContainers = document.querySelectorAll('[class*="item"], [class*="gear"], [class*="equipment"]');
  console.log(`Found ${itemContainers.length} elements with item/gear/equipment in class`);
  itemContainers.forEach(el => walkTextNodes(el));

  // Try translating main content areas
  const mainContent = document.querySelector('main, article, .content, .build-content, #content');
  if (mainContent) {
    console.log('Found main content area, translating...');
    walkTextNodes(mainContent);
  } else {
    console.log('No main content area found, translating entire body');
    walkTextNodes(document.body);
  }

  // Report what we found
  console.log('D4 Translator: Initial translation complete');
  console.log(`Processed ${processedNodes.size} text nodes`);
}

// You can also add debugging to the translateTextNode function:
// At the start of translateTextNode, add:
/*
const originalTranslateTextNode = translateTextNode;
function translateTextNode(textNode) {
  const originalText = textNode.textContent;
  const result = originalTranslateTextNode(textNode);
  if (textNode.textContent !== originalText) {
    console.log('Translated:', originalText.substring(0, 50), '→', textNode.textContent.substring(0, 50));
  }
  return result;
}
*/
