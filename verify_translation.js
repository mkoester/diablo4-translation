// Verification script - run this after reloading the extension
console.log('=== Verifying Translation ===\n');

// 1. Check if extension loaded
if (typeof allTranslations !== 'undefined') {
  console.log('✅ Extension loaded (allTranslations defined)');
  console.log(`   Total translations: ${Object.keys(allTranslations).length}`);
} else {
  console.log('❌ Extension NOT loaded');
  console.log('   → Check about:debugging to see if extension is enabled');
  return;
}

// 2. Check noscript tags
const noscripts = document.querySelectorAll('.d4-item noscript');
console.log(`\n✅ Found ${noscripts.length} noscript tags in .d4-item elements`);

if (noscripts.length > 0) {
  console.log('\nChecking first 3 noscript tags:');
  for (let i = 0; i < Math.min(3, noscripts.length); i++) {
    const ns = noscripts[i];
    const html = ns.innerHTML;

    console.log(`\nNoscript ${i + 1}:`);

    // Extract alt text
    const altMatch = html.match(/alt="([^"]+)"/);
    if (altMatch) {
      const altText = altMatch[1];
      console.log(`  Alt text: "${altText}"`);

      // Check if translated
      if (altText.includes('(') && altText.includes(')')) {
        console.log('  ✅ TRANSLATED! Contains (English)');
      } else if (altText.includes('Ring') || altText.includes('Aspekt') ||
                 altText.includes('Unique') || altText.includes('Mythic')) {
        console.log('  ❌ NOT TRANSLATED (German item name without English)');
      } else {
        console.log('  ⚠️  Unknown content');
      }
    } else {
      console.log('  ⚠️  No alt attribute found');
    }
  }
}

// 3. Check regular text nodes (for glyphs)
console.log('\n=== Checking Paragon Glyphs ===');
const paraRows = document.querySelectorAll('.d4para-row');
console.log(`Found ${paraRows.length} .d4para-row elements`);

if (paraRows.length > 0) {
  const sampleText = paraRows[0].textContent.substring(0, 200);
  console.log(`Sample text: "${sampleText}"`);

  if (sampleText.includes('(') && sampleText.includes(')')) {
    console.log('✅ Glyphs appear to be translated!');
  } else {
    console.log('❌ Glyphs may not be translated');
  }
}

// 4. Summary
console.log('\n=== SUMMARY ===');
console.log('Extension loaded:', typeof allTranslations !== 'undefined' ? '✅' : '❌');
console.log('Noscript tags found:', noscripts.length > 0 ? '✅' : '❌');
console.log('Paragon rows found:', paraRows.length > 0 ? '✅' : '❌');

console.log('\n=== NEXT STEPS ===');
if (noscripts.length > 0) {
  console.log('1. Inspect a .d4-item element (right-click → Inspect)');
  console.log('2. Find the <noscript> tag inside it');
  console.log('3. Check the alt="..." attribute');
  console.log('4. It should contain "German (English)" format');
} else {
  console.log('⚠️  No noscript tags found - are you on a build guide page?');
}

console.log('\n=== COMPLETE ===');
