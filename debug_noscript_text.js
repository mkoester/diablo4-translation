// Debug script to check what text is actually in noscript tags
console.log('=== Checking noscript content ===');

// Find all noscript tags
const noscripts = document.querySelectorAll('noscript');
console.log(`Found ${noscripts.length} noscript tags`);

// Check first few noscript tags
for (let i = 0; i < Math.min(5, noscripts.length); i++) {
  const ns = noscripts[i];
  console.log(`\nNoscript ${i + 1}:`);
  console.log('  innerHTML:', ns.innerHTML.substring(0, 100));
  console.log('  textContent:', ns.textContent.substring(0, 100));
  console.log('  Parent:', ns.parentElement?.tagName, ns.parentElement?.className);

  // Try to find German text
  if (ns.textContent.includes('Ring') || ns.textContent.includes('Ozelot') ||
      ns.textContent.includes('Aspekt') || ns.textContent.includes('Wächter')) {
    console.log('  ✅ Contains German item text!');
    console.log('  Full text:', ns.textContent);
  }
}

// Check .d4-item elements more carefully
console.log('\n=== Checking .d4-item elements ===');
const d4Items = document.querySelectorAll('.d4-item');
console.log(`Found ${d4Items.length} .d4-item elements`);

for (let i = 0; i < Math.min(3, d4Items.length); i++) {
  const item = d4Items[i];
  console.log(`\nItem ${i + 1}:`);
  console.log('  Classes:', item.className);
  console.log('  Full text content:', item.textContent.substring(0, 150));

  // Check if it has noscript children
  const noscriptChildren = item.querySelectorAll('noscript');
  console.log(`  Noscript children: ${noscriptChildren.length}`);

  // Check all text nodes
  const walker = document.createTreeWalker(item, NodeFilter.SHOW_TEXT);
  let textNodes = [];
  while (walker.nextNode()) {
    const node = walker.currentNode;
    if (node.textContent.trim().length > 0) {
      textNodes.push({
        text: node.textContent.trim().substring(0, 50),
        parent: node.parentElement?.tagName,
        parentClass: node.parentElement?.className
      });
    }
  }
  console.log('  Text nodes:', textNodes);

  // Look for German items specifically
  const germanPattern = /Ring der|Auge des|Aspekt|Wächter|Schlächter/;
  if (germanPattern.test(item.textContent)) {
    console.log('  ✅ HAS German item text');
    console.log('  Full item HTML:', item.innerHTML.substring(0, 300));
  } else {
    console.log('  ❌ NO German item text found');
  }
}

// Test if allTranslations is accessible
console.log('\n=== Testing translation data ===');
if (typeof allTranslations !== 'undefined') {
  console.log('✅ allTranslations is defined');
  console.log('Total translations:', Object.keys(allTranslations).length);
  console.log('Test translation:', allTranslations['Ring der Sternenlosen Himmel']);
} else {
  console.log('❌ allTranslations is NOT defined - extension may not have loaded');
}

console.log('\n=== Debug complete ===');
