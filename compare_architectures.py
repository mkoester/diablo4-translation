#!/usr/bin/env python3
"""
Comparison tool demonstrating benefits of ID-based vs string-based architecture.
"""

import json


# Simulated data examples
STRING_BASED = {
    "glyphs": {
        "Macht": "Might",
        "Zorn": "Wrath",
        "Kontrolle": "Control"  # What if there are two "Kontrolle" glyphs?
    }
}

ID_BASED = {
    "glyphs": {
        "12345": {"de": "Macht", "en": "Might"},
        "12346": {"de": "Zorn", "en": "Wrath"},
        "12347": {"de": "Kontrolle", "en": "Control"},
        "12348": {"de": "Kontrolle", "en": "Control"}  # Different ID, same name!
    }
}


def demonstrate_collision_problem():
    """Show how string-based approach handles collisions."""
    print("=" * 80)
    print("PROBLEM 1: String Collisions")
    print("=" * 80)
    print()

    print("Scenario: Two different glyphs with the same German name 'Kontrolle'")
    print()

    print("String-based approach:")
    print("  const glyphTranslations = {")
    print('    "Kontrolle": "Control",  // Which Kontrolle?')
    print('    "Kontrolle": "Domination",  // This overwrites the first!')
    print("  };")
    print()
    print("  Result: ❌ Only one translation survives, data loss!")
    print()

    print("ID-based approach:")
    print("  const glyphsById = {")
    print('    12347: { de: "Kontrolle", en: "Control" },')
    print('    12348: { de: "Kontrolle", en: "Domination" },')
    print("  };")
    print()
    print("  Result: ✅ Both translations preserved, no collision!")
    print()


def demonstrate_update_detection():
    """Show how ID-based approach handles updates."""
    print("=" * 80)
    print("PROBLEM 2: Detecting Changes")
    print("=" * 80)
    print()

    print("Scenario: Wowhead updates 'Ring der Sternenlosen Himmel' → 'Ring der Sternlosen Himmel'")
    print()

    print("String-based approach:")
    print("  // Old data")
    print('  "Ring der Sternenlosen Himmel": "Ring of Starless Skies"')
    print()
    print("  // New scrape")
    print('  "Ring der Sternlosen Himmel": "Ring of Starless Skies"')
    print()
    print("  Problem:")
    print("  - ❌ Old translation no longer matches German text on site")
    print("  - ❌ No automatic way to detect what changed")
    print("  - ❌ Must manually search and update")
    print()

    print("ID-based approach:")
    print("  // Old data")
    print('  67890: { de: "Ring der Sternenlosen Himmel", en: "Ring of Starless Skies" }')
    print()
    print("  // New scrape")
    print('  67890: { de: "Ring der Sternlosen Himmel", en: "Ring of Starless Skies" }')
    print()
    print("  Detection code:")
    print("    if (old[67890].de !== new[67890].de) {")
    print('      console.log(`Item 67890 renamed!`);')
    print('      console.log(`  Old: ${old[67890].de}`);')
    print('      console.log(`  New: ${new[67890].de}`);')
    print("    }")
    print()
    print("  Result: ✅ Automatic change detection!")
    print()


def demonstrate_metadata():
    """Show how ID-based approach stores metadata."""
    print("=" * 80)
    print("PROBLEM 3: No Metadata")
    print("=" * 80)
    print()

    print("String-based approach:")
    print('  "Ring der Sternenlosen Himmel": "Ring of Starless Skies"')
    print()
    print("  Questions we CAN'T answer:")
    print("  - ❌ Is this unique or mythic?")
    print("  - ❌ Which class can use it?")
    print("  - ❌ Which season was it added?")
    print("  - ❌ What's the Wowhead URL?")
    print()

    print("ID-based approach:")
    print("  67890: {")
    print('    de: "Ring der Sternenlosen Himmel",')
    print('    en: "Ring of Starless Skies",')
    print('    quality: 5,  // Unique')
    print('    slot: "ring",')
    print('    classes: ["sorcerer", "spiritborn"],')
    print('    season: 7,')
    print('    url: "https://www.wowhead.com/diablo-4/item/67890"')
    print("  }")
    print()
    print("  Now we can:")
    print("  - ✅ Filter by quality: mythicItems = items.filter(i => i.quality === 6)")
    print("  - ✅ Filter by class: sorcItems = items.filter(i => i.classes.includes('sorcerer'))")
    print("  - ✅ Show new season items: newItems = items.filter(i => i.season === 7)")
    print("  - ✅ Link to Wowhead: <a href={item.url}>View on Wowhead</a>")
    print()


def demonstrate_multilang():
    """Show how ID-based approach enables multi-language."""
    print("=" * 80)
    print("PROBLEM 4: Multi-Language Support")
    print("=" * 80)
    print()

    print("String-based approach:")
    print("  // German → English")
    print('  const deToEn = { "Macht": "Might" };')
    print()
    print("  // Want to add French?")
    print('  const deToFr = { "Macht": "Puissance" };')
    print('  const enToFr = { "Might": "Puissance" };')
    print('  const frToEn = { "Puissance": "Might" };')
    print()
    print("  Result: ❌ Need N² dictionaries for N languages!")
    print()

    print("ID-based approach:")
    print("  12345: {")
    print('    de: "Macht",')
    print('    en: "Might",')
    print('    fr: "Puissance",')
    print('    es: "Poder",')
    print('    ja: "力"')
    print("  }")
    print()
    print("  Usage:")
    print("    const userLang = navigator.language.slice(0, 2);")
    print("    const translation = glyphsById[12345][userLang];")
    print()
    print("  Result: ✅ Single source of truth for all languages!")
    print()


def demonstrate_incremental_updates():
    """Show how ID-based approach enables incremental updates."""
    print("=" * 80)
    print("PROBLEM 5: Incremental Updates")
    print("=" * 80)
    print()

    print("Scenario: Diablo 4 Season 8 adds 20 new unique items")
    print()

    print("String-based approach:")
    print("  1. Scrape all 1000+ items again")
    print("  2. Compare new list vs. old list by string matching")
    print("  3. Hope no items were renamed (breaks comparison)")
    print("  4. Manually identify which are truly new")
    print()
    print("  Result: ❌ Tedious, error-prone")
    print()

    print("ID-based approach:")
    print("  // Load existing IDs")
    print("  const existingIds = new Set(Object.keys(itemsById));")
    print()
    print("  // Scrape new data")
    print("  const newItems = scrapedData.filter(item => !existingIds.has(item.id));")
    print()
    print("  console.log(`Found ${newItems.length} new items:`);")
    print("  newItems.forEach(item => {")
    print("    console.log(`  - [${item.id}] ${item.de} → ${item.en}`);")
    print("  });")
    print()
    print("  Result: ✅ Automatic new item detection!")
    print()


def show_memory_comparison():
    """Show memory usage is similar."""
    print("=" * 80)
    print("BONUS: Memory Usage Comparison")
    print("=" * 80)
    print()

    string_based = {
        "Macht": "Might",
        "Zorn": "Wrath"
    }

    id_based = {
        12345: {"de": "Macht", "en": "Might"},
        12346: {"de": "Zorn", "en": "Wrath"}
    }

    # Also need string lookup for regex performance
    string_lookup = {
        "Macht": "Might",
        "Zorn": "Wrath"
    }

    print("String-based only:")
    print(f"  {json.dumps(string_based, ensure_ascii=False)}")
    print(f"  Size: ~{len(json.dumps(string_based))} bytes")
    print()

    print("ID-based + string lookup (for regex):")
    print(f"  ID: {json.dumps(id_based, ensure_ascii=False)}")
    print(f"  String: {json.dumps(string_lookup, ensure_ascii=False)}")
    print(f"  Total size: ~{len(json.dumps(id_based)) + len(json.dumps(string_lookup))} bytes")
    print()

    print("Overhead:")
    overhead = len(json.dumps(id_based)) + len(json.dumps(string_lookup)) - len(json.dumps(string_based))
    print(f"  ~{overhead} bytes per entry (negligible for modern browsers)")
    print()
    print("Trade-off: ✅ Tiny memory cost for huge maintainability gain!")
    print()


def main():
    """Run all demonstrations."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "ID-BASED vs STRING-BASED ARCHITECTURE" + " " * 21 + "║")
    print("╚" + "=" * 78 + "╝")
    print()

    demonstrate_collision_problem()
    input("Press Enter to continue...")
    print("\n")

    demonstrate_update_detection()
    input("Press Enter to continue...")
    print("\n")

    demonstrate_metadata()
    input("Press Enter to continue...")
    print("\n")

    demonstrate_multilang()
    input("Press Enter to continue...")
    print("\n")

    demonstrate_incremental_updates()
    input("Press Enter to continue...")
    print("\n")

    show_memory_comparison()

    print("=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print()
    print("ID-based architecture provides:")
    print("  ✅ No collision issues")
    print("  ✅ Automatic change detection")
    print("  ✅ Rich metadata support")
    print("  ✅ Easy multi-language")
    print("  ✅ Incremental updates")
    print("  ✅ Negligible overhead")
    print()
    print("Recommendation: Use scrape_wowhead_v2.py for ID-based extraction!")
    print()


if __name__ == '__main__':
    main()
