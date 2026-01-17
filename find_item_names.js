// Find exactly where item names appear in the DOM
console.log('=== Finding Item Names ===\n');

// Look for a specific item we know should be there
const searchTerms = [
  'Ring der Sternenlosen Himmel',
  'Auge des Ozelots',
  'Wächter',
  'Andariel'
];

searchTerms.forEach(term => {
  console.log(`\nSearching for: "${term}"`);

  // Method 1: XPath search
  const xpath = `//*[contains(text(), '${term}')]`;
  const result = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);

  if (result.snapshotLength > 0) {
    console.log(`✅ Found in ${result.snapshotLength} elements`);

    for (let i = 0; i < Math.min(2, result.snapshotLength); i++) {
      const element = result.snapshotItem(i);
      console.log(`  Element ${i + 1}:`);
      console.log(`    Tag: ${element.tagName}`);
      console.log(`    Class: ${element.className}`);
      console.log(`    Parent: ${element.parentElement?.tagName}.${element.parentElement?.className}`);
      console.log(`    Text: "${element.textContent.substring(0, 80)}"`);

      // Check if it's inside .d4-item
      const d4Item = element.closest('.d4-item');
      if (d4Item) {
        console.log(`    ✅ Inside .d4-item`);
      } else {
        console.log(`    ❌ NOT inside .d4-item`);
      }

      // Check if it's inside .d4para-row
      const d4Para = element.closest('.d4para-row');
      if (d4Para) {
        console.log(`    ✅ Inside .d4para-row`);
      }
    }
  } else {
    console.log(`  ❌ Not found in DOM`);
  }
});

// Check if items exist but in a different format
console.log('\n\n=== Checking for partial matches ===');
const partialTerms = ['Ring der', 'Auge des', 'Sternenlosen'];

partialTerms.forEach(term => {
  const xpath = `//*[contains(text(), '${term}')]`;
  const result = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);

  if (result.snapshotLength > 0) {
    console.log(`\n"${term}": found in ${result.snapshotLength} elements`);
    const element = result.snapshotItem(0);
    console.log(`  Example: "${element.textContent.substring(0, 100)}"`);
  }
});

console.log('\n=== Complete ===');
