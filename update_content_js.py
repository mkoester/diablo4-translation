#!/usr/bin/env python3
"""
Updates content.js with extracted translations while preserving the structure and logic.
Fixes:
- Unicode escape sequences (e.g., \\u00e4 -> ä)
- Preserves aspects from old content.js that weren't found in Wowhead
"""

import json
import re
import codecs
import subprocess

# Load extracted translations
with open('translations_by_string.json', 'r', encoding='utf-8') as f:
    extracted = json.load(f)

# Read current content.js to preserve tempering translations and translation logic
with open('content.js', 'r', encoding='utf-8') as f:
    current_content = f.read()

# Get the original content.js from git (before our updates) to preserve old aspects
try:
    result = subprocess.run(
        ['git', 'show', 'HEAD~1:content.js'],
        capture_output=True,
        text=True,
        check=True
    )
    original_content = result.stdout
    print("Retrieved original content.js from git history")
except subprocess.CalledProcessError:
    print("Warning: Could not retrieve original content.js from git, using current version")
    original_content = current_content

# Extract tempering translations from current file
tempering_match = re.search(
    r'const temperingTranslations = \{([^}]+)\};',
    current_content,
    re.DOTALL
)
tempering_translations = {}
if tempering_match:
    tempering_block = tempering_match.group(1)
    # Parse the tempering translations
    for line in tempering_block.split('\n'):
        line = line.strip()
        if line and line.startswith('"'):
            match = re.match(r'"([^"]+)":\s*"([^"]+)"', line)
            if match:
                tempering_translations[match.group(1)] = match.group(2)

print(f"Extracted {len(tempering_translations)} tempering translations from current file")

# Extract existing aspect translations from ORIGINAL file (before our updates)
existing_aspects = {}
aspect_match = re.search(
    r'const aspectTranslations = \{([^}]+)\};',
    original_content,
    re.DOTALL
)
if aspect_match:
    aspect_block = aspect_match.group(1)
    for line in aspect_block.split('\n'):
        line = line.strip()
        if line and line.startswith('"'):
            match = re.match(r'"([^"]+)":\s*"([^"]+)"', line)
            if match:
                existing_aspects[match.group(1)] = match.group(2)

print(f"Extracted {len(existing_aspects)} existing aspect translations from original file")

# Merge aspects: use Wowhead data first, then add missing ones from old content.js
merged_aspects = dict(extracted['aspects'])
new_from_old = 0
for german, english in existing_aspects.items():
    if german not in merged_aspects:
        merged_aspects[german] = english
        new_from_old += 1

if new_from_old > 0:
    print(f"Preserved {new_from_old} aspects from old content.js that weren't in Wowhead")

# Function to fix unicode escape sequences
def fix_unicode_escapes(text):
    """Convert unicode escape sequences like \\u00e4 to actual characters."""
    # This handles strings that have already been JSON-parsed but still contain escape sequences
    try:
        # Try to decode unicode escapes
        return text.encode('latin1').decode('unicode-escape')
    except:
        # If that fails, try direct decode
        try:
            return codecs.decode(text, 'unicode-escape')
        except:
            # If all fails, return original
            return text

# Apply unicode fixes to all translations
for category in ['glyphs', 'items']:
    fixed_dict = {}
    for german, english in extracted[category].items():
        fixed_german = fix_unicode_escapes(german)
        fixed_english = fix_unicode_escapes(english)
        fixed_dict[fixed_german] = fixed_english
    extracted[category] = fixed_dict

# Fix unicode in merged aspects
fixed_aspects = {}
for german, english in merged_aspects.items():
    fixed_german = fix_unicode_escapes(german)
    fixed_english = fix_unicode_escapes(english)
    fixed_aspects[fixed_german] = fixed_english
merged_aspects = fixed_aspects

# Generate new content.js
output = []
output.append("// D4 German Translator - Translates German D4 terms to English")
output.append("// Format: \"German (English)\"")
output.append("// Auto-updated with scrape_complete_id_based.py data")
output.append("")

# Write glyphs
output.append("// " + "="*76)
output.append("// PARAGON GLYPH TRANSLATIONS")
output.append("// " + "="*76)
output.append("const glyphTranslations = {")
for german, english in sorted(extracted['glyphs'].items()):
    german_escaped = german.replace('\\', '\\\\').replace('"', '\\"')
    english_escaped = english.replace('\\', '\\\\').replace('"', '\\"')
    output.append(f'  "{german_escaped}": "{english_escaped}",')
output.append("};")
output.append("")

# Write items
output.append("// " + "="*76)
output.append("// UNIQUE/MYTHIC ITEM TRANSLATIONS")
output.append("// " + "="*76)
output.append("const itemTranslations = {")
for german, english in sorted(extracted['items'].items()):
    german_escaped = german.replace('\\', '\\\\').replace('"', '\\"')
    english_escaped = english.replace('\\', '\\\\').replace('"', '\\"')
    output.append(f'  "{german_escaped}": "{english_escaped}",')
output.append("};")
output.append("")

# Write aspects (merged)
output.append("// " + "="*76)
output.append("// LEGENDARY ASPECT TRANSLATIONS")
output.append("// " + "="*76)
output.append("const aspectTranslations = {")
for german, english in sorted(merged_aspects.items()):
    german_escaped = german.replace('\\', '\\\\').replace('"', '\\"')
    english_escaped = english.replace('\\', '\\\\').replace('"', '\\"')
    output.append(f'  "{german_escaped}": "{english_escaped}",')
output.append("};")
output.append("")

# Write tempering (preserved from original)
output.append("// " + "="*76)
output.append("// TEMPERING RECIPE TRANSLATIONS")
output.append("// " + "="*76)
output.append("const temperingTranslations = {")
for german, english in sorted(tempering_translations.items()):
    german_escaped = german.replace('\\', '\\\\').replace('"', '\\"')
    english_escaped = english.replace('\\', '\\\\').replace('"', '\\"')
    output.append(f'  "{german_escaped}": "{english_escaped}",')
output.append("};")
output.append("")

# Extract and preserve the translation logic from original file
logic_start = current_content.find("// Combine all translations")
if logic_start != -1:
    logic_section = current_content[logic_start:]
    output.append(logic_section)
else:
    # Default logic if not found
    output.append("// Combine all translations for pattern matching")
    output.append("const allTranslations = {")
    output.append("  ...glyphTranslations,")
    output.append("  ...itemTranslations,")
    output.append("  ...aspectTranslations,")
    output.append("  ...temperingTranslations")
    output.append("};")
    output.append("")
    output.append("// Translation logic would go here...")

# Write updated content.js
with open('content.js', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print(f"\n✅ Updated content.js with:")
print(f"   - {len(extracted['glyphs'])} glyphs")
print(f"   - {len(extracted['items'])} items")
print(f"   - {len(merged_aspects)} aspects (including {new_from_old} preserved from old content.js)")
print(f"   - {len(tempering_translations)} tempering recipes")
print(f"   TOTAL: {len(extracted['glyphs']) + len(extracted['items']) + len(merged_aspects) + len(tempering_translations)} translations")
