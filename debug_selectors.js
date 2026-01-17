// Diagnostic script to find what selectors vitablo.de uses for items
// Run this in the browser console on a vitablo.de build guide page

console.log('=== D4 Selector Debugger ===');

// Test 1: Check for d4-item elements
const d4Items = document.querySelectorAll('.d4-item');
console.log(`Found ${d4Items.length} elements with class .d4-item`);
if (d4Items.length > 0) {
  console.log('Sample .d4-item element:', d4Items[0]);
  console.log('Sample .d4-item text:', d4Items[0].textContent.substring(0, 100));
}

// Test 2: Check for d4para-row elements
const d4Para = document.querySelectorAll('.d4para-row');
console.log(`Found ${d4Para.length} elements with class .d4para-row`);
if (d4Para.length > 0) {
  console.log('Sample .d4para-row element:', d4Para[0]);
  console.log('Sample .d4para-row text:', d4Para[0].textContent.substring(0, 100));
}

// Test 3: Search for elements containing German item names
const germanItems = [
  'Ring der Sternenlosen Himmel',
  'Auge des Ozelots',
  'Wächter',
  'Schlächter'
];

console.log('\n=== Searching for German item names ===');
germanItems.forEach(itemName => {
  // Search all elements containing this text
  const xpath = `//*[contains(text(), '${itemName}')]`;
  const result = document.evaluate(xpath, document, null, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, null);

  console.log(`\n"${itemName}": found in ${result.snapshotLength} elements`);

  for (let i = 0; i < Math.min(3, result.snapshotLength); i++) {
    const element = result.snapshotItem(i);
    console.log(`  - Tag: ${element.tagName}, Classes: ${element.className}`);
    console.log(`    Parent: ${element.parentElement?.tagName}, Parent Classes: ${element.parentElement?.className}`);
    console.log(`    Text: "${element.textContent.substring(0, 50)}..."`);
  }
});

// Test 4: Look for common container patterns
console.log('\n=== Common container patterns ===');
const patterns = [
  'div[class*="item"]',
  'div[class*="gear"]',
  'div[class*="equipment"]',
  'div[class*="build"]',
  '[class*="unique"]',
  '[class*="mythic"]',
  '[class*="aspect"]'
];

patterns.forEach(pattern => {
  const elements = document.querySelectorAll(pattern);
  if (elements.length > 0) {
    console.log(`${pattern}: found ${elements.length} elements`);
    if (elements.length <= 5) {
      elements.forEach(el => console.log(`  - ${el.className}`));
    }
  }
});

// Test 5: Check if items are in a specific section
console.log('\n=== Looking for item sections ===');
const sections = document.querySelectorAll('section, article, div[class*="section"]');
sections.forEach(section => {
  const text = section.textContent;
  if (text.includes('Ring der Sternenlosen Himmel') ||
      text.includes('Auge des Ozelots') ||
      text.includes('Items') ||
      text.includes('Ausrüstung')) {
    console.log(`Found items section: ${section.tagName}.${section.className}`);
    console.log(`  First 100 chars: "${text.substring(0, 100)}..."`);

    // Check what children contain the actual item names
    const children = section.querySelectorAll('*');
    let itemContainers = [];
    children.forEach(child => {
      if (child.textContent.includes('Ring der Sternenlosen Himmel') ||
          child.textContent.includes('Auge des Ozelots')) {
        itemContainers.push(child);
      }
    });
    console.log(`  Item containers found: ${itemContainers.length}`);
    if (itemContainers.length > 0) {
      console.log(`  Example container: ${itemContainers[0].tagName}.${itemContainers[0].className}`);
    }
  }
});

console.log('\n=== Debugger complete ===');
console.log('Copy the output above and share it to identify the correct selectors.');
