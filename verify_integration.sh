#!/bin/bash
# Verification script for Firefox extension integration

echo "=========================================="
echo "Firefox Extension Integration Verification"
echo "=========================================="
echo ""

# Check files exist
echo "Checking files..."
files=(
    "content.js"
    "manifest.json"
    "../diablo4-translation-1.0.1-c0777da-SNAPSHOT.xpi"
    "translations_by_id.json"
    "translations_by_string.json"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        size=$(du -h "$file" | cut -f1)
        echo "  ✅ $file ($size)"
    else
        echo "  ❌ $file (missing)"
    fi
done

echo ""
echo "Checking translation counts..."

# Count translations in content.js
glyphs=$(grep -c '":' content.js | head -1 || echo "0")
echo "  content.js size: $(du -h content.js | cut -f1)"
echo "  Lines: $(wc -l < content.js)"

# Count from JSON
if [ -f "translations_by_string.json" ]; then
    echo ""
    echo "Translation counts from JSON:"
    python3 << 'PYTHON'
import json
with open('translations_by_string.json', 'r') as f:
    data = json.load(f)
print(f"  Glyphs: {len(data['glyphs'])}")
print(f"  Items: {len(data['items'])}")
print(f"  Aspects: {len(data['aspects'])}")
print(f"  Total: {len(data['glyphs']) + len(data['items']) + len(data['aspects'])}")
PYTHON
fi

echo ""
echo "Extension package:"
if [ -f "../diablo4-translation-1.0.1-c0777da-SNAPSHOT.xpi" ]; then
    ls -lh ../diablo4-translation-1.0.1-c0777da-SNAPSHOT.xpi | awk '{print "  " $9 ": " $5}'
    echo "  ✅ Ready to load in Firefox!"
fi

echo ""
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Load extension in Firefox:"
echo "   about:debugging#/runtime/this-firefox"
echo "   → Load Temporary Add-on"
echo "   → Select: manifest.json"
echo ""
echo "2. Test on vitablo.de:"
echo "   https://vitablo.de/diablo-4-build-guides/"
echo ""
echo "3. Verify translations appear as:"
echo "   German (English)"
echo ""
