// Check if we need to parse noscript innerHTML to get item names
console.log('=== Checking noscript innerHTML parsing ===');

const noscripts = document.querySelectorAll('.d4-item noscript');
console.log(`Found ${noscripts.length} noscript tags in .d4-item elements\n`);

for (let i = 0; i < Math.min(5, noscripts.length); i++) {
  const ns = noscripts[i];
  console.log(`Noscript ${i + 1}:`);

  // Get the raw HTML
  const html = ns.innerHTML;
  console.log('  innerHTML:', html.substring(0, 150));

  // Try to extract alt text using regex
  const altMatch = html.match(/alt="([^"]+)"/);
  if (altMatch) {
    console.log('  ✅ Found alt text:', altMatch[1]);

    // Check if this matches a German item
    if (altMatch[1].includes('Ring') || altMatch[1].includes('Aspekt') ||
        altMatch[1].includes('Unique') || altMatch[1].includes('Mythic')) {
      console.log('  ✅✅ THIS IS AN ITEM NAME!');
    }
  } else {
    console.log('  ❌ No alt attribute found');
  }

  // Also check textContent (might work differently)
  console.log('  textContent:', ns.textContent.substring(0, 100));
}

console.log('\n=== Suggestion ===');
console.log('We need to:');
console.log('1. Find all noscript tags in .d4-item elements');
console.log('2. Parse their innerHTML to extract alt="..." text');
console.log('3. Translate the alt text');
console.log('4. Update the innerHTML with translated alt text');
