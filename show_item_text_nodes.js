// Show actual text content of items to see what needs translating
console.log('=== Showing Item Text Nodes ===\n');

const d4Items = document.querySelectorAll('.d4-item');
console.log(`Found ${d4Items.length} .d4-item elements\n`);

d4Items.forEach((item, index) => {
  console.log(`\n=== Item ${index + 1} ===`);
  console.log('Classes:', item.className);

  // Get ALL text nodes
  const walker = document.createTreeWalker(
    item,
    NodeFilter.SHOW_TEXT,
    {
      acceptNode: (node) => {
        const parent = node.parentElement;
        if (!parent) return NodeFilter.FILTER_REJECT;
        const tagName = parent.tagName.toLowerCase();
        // Include noscript to see if that's where items are
        if (tagName === 'script' || tagName === 'style') {
          return NodeFilter.FILTER_REJECT;
        }
        if (node.textContent.trim().length === 0) {
          return NodeFilter.FILTER_REJECT;
        }
        return NodeFilter.FILTER_ACCEPT;
      }
    }
  );

  const textNodes = [];
  while (walker.nextNode()) {
    textNodes.push(walker.currentNode);
  }

  console.log(`Text nodes found: ${textNodes.length}`);

  // Show all non-trivial text
  textNodes.forEach((node, i) => {
    const text = node.textContent.trim();
    if (text.length > 5) { // Only show meaningful text
      console.log(`  [${i}] Parent: ${node.parentElement.tagName}.${node.parentElement.className || '(no class)'}`);
      console.log(`      Text: "${text.substring(0, 100)}"`);

      // Check if this looks like an item name
      if (text.includes('Ring') || text.includes('Auge') ||
          text.includes('Unique') || text.includes('Mythic') ||
          text.match(/^[A-Z][a-zäöüß]+ (der|des|von)/)) {
        console.log(`      ⭐ MIGHT BE AN ITEM NAME`);
      }
    }
  });

  if (index >= 2) {
    console.log('\n... (showing first 3 items only)');
    return false; // Break forEach
  }
});

console.log('\n=== Complete ===');
console.log('Look for text that looks like item names above.');
console.log('Check what parent tag/class they have.');
