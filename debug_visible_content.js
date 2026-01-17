// Check what content is actually visible in .d4-item elements
console.log('=== Checking visible content in .d4-item ===');

const d4Items = document.querySelectorAll('.d4-item');
console.log(`Found ${d4Items.length} .d4-item elements\n`);

d4Items.forEach((item, index) => {
  console.log(`\n--- Item ${index + 1} ---`);
  console.log('Classes:', item.className);

  // Get all visible text
  const allText = item.innerText || item.textContent;
  console.log('Visible text (innerText):', allText.substring(0, 200));

  // Look for img tags with alt text
  const imgs = item.querySelectorAll('img');
  console.log(`Images: ${imgs.length}`);
  imgs.forEach((img, imgIndex) => {
    const alt = img.getAttribute('alt');
    if (alt && alt.length > 5) {
      console.log(`  Img ${imgIndex + 1} alt: "${alt}"`);
      if (alt.includes('Ring') || alt.includes('Aspekt') || alt.includes('Unique')) {
        console.log('    ✅ This looks like an item name!');
      }
    }
  });

  // Look for title attributes
  const elementsWithTitle = item.querySelectorAll('[title]');
  console.log(`Elements with title: ${elementsWithTitle.length}`);
  elementsWithTitle.forEach(el => {
    console.log(`  Title: "${el.getAttribute('title')}"`);
  });

  // Look for data attributes
  const elementsWithData = item.querySelectorAll('[data-item], [data-name], [data-title]');
  console.log(`Elements with data attributes: ${elementsWithData.length}`);
  elementsWithData.forEach(el => {
    console.log(`  Data attrs:`, el.dataset);
  });

  if (index >= 2) {
    console.log('\n... (showing first 3 items only)');
    return;
  }
});

console.log('\n=== Checking if tooltips or hover content exists ===');
// Maybe items show on hover?
const tooltips = document.querySelectorAll('[class*="tooltip"], [class*="hover"], [role="tooltip"]');
console.log(`Tooltip elements: ${tooltips.length}`);

console.log('\n=== Complete ===');
