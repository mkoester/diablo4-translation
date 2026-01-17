#!/usr/bin/env python3
"""
Scrapes Wowhead Diablo 4 German database for glyphs, items, and aspects.
Extracts German terms from the embedded JavaScript data structures.
"""

import requests
import re
import json
from typing import List, Set

def extract_glyphs(url: str) -> List[str]:
    """Extract all German glyph names from Wowhead paragon glyphs page."""
    print(f"Fetching glyphs from {url}...")
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    content = response.text

    # Look for the JavaScript data structure containing glyph data
    # Wowhead typically embeds data in listview patterns
    pattern = r'new Listview\(\{.*?data:\s*(\[.*?\])\s*\}\);'
    matches = re.findall(pattern, content, re.DOTALL)

    glyphs = set()
    for match in matches:
        try:
            # Parse the JSON data array
            data = json.loads(match)
            for item in data:
                if 'name_de' in item:
                    glyphs.add(item['name_de'])
                elif 'name' in item:
                    glyphs.add(item['name'])
        except json.JSONDecodeError:
            pass

    # Alternative: extract from table rows if JSON parsing fails
    if not glyphs:
        name_pattern = r'<td class="listview-cell-name">.*?<a.*?>(.*?)</a>'
        names = re.findall(name_pattern, content, re.DOTALL)
        glyphs = set(n.strip() for n in names if n.strip())

    return sorted(glyphs)

def extract_items(url: str) -> List[str]:
    """Extract all German unique/mythic item names from Wowhead items page."""
    print(f"Fetching items from {url}...")
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    content = response.text

    # Look for the JavaScript data structure containing item data
    pattern = r'new Listview\(\{.*?data:\s*(\[.*?\])\s*\}\);'
    matches = re.findall(pattern, content, re.DOTALL)

    items = set()
    for match in matches:
        try:
            # Parse the JSON data array
            data = json.loads(match)
            for item in data:
                # Filter for quality 5 (unique) and 6 (mythic) only
                if item.get('quality') in [5, 6]:
                    if 'name_de' in item:
                        items.add(item['name_de'])
                    elif 'name' in item:
                        items.add(item['name'])
        except json.JSONDecodeError:
            pass

    # Alternative: look for direct JSON data embedded in script tags
    if not items:
        script_pattern = r'<script[^>]*>(.*?)</script>'
        scripts = re.findall(script_pattern, content, re.DOTALL)
        for script in scripts:
            # Look for item data arrays
            item_pattern = r'"name":"([^"]+)".*?"quality":([56])'
            matches = re.findall(item_pattern, script)
            items.update(name for name, quality in matches)

    return sorted(items)

def extract_aspects(url: str) -> List[str]:
    """Extract all German aspect names from Wowhead aspects page."""
    print(f"Fetching aspects from {url}...")
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    content = response.text

    # Look for the JavaScript data structure containing aspect data
    pattern = r'new Listview\(\{.*?data:\s*(\[.*?\])\s*\}\);'
    matches = re.findall(pattern, content, re.DOTALL)

    aspects = set()
    for match in matches:
        try:
            # Parse the JSON data array
            data = json.loads(match)
            for item in data:
                if 'name_de' in item:
                    name = item['name_de']
                    # Convert from "Aspekt: Name" to "Name Aspekt" format
                    if name.startswith('Aspekt:'):
                        # "Aspekt: Keilender" -> "Keilender Aspekt"
                        name = name.replace('Aspekt:', '').strip() + ' Aspekt'
                    aspects.add(name)
                elif 'name' in item:
                    name = item['name']
                    # Convert from "Aspekt: Name" to "Name Aspekt" format
                    if name.startswith('Aspekt:'):
                        name = name.replace('Aspekt:', '').strip() + ' Aspekt'
                    aspects.add(name)
        except json.JSONDecodeError:
            pass

    # Alternative: extract from table rows if JSON parsing fails
    if not aspects:
        name_pattern = r'<a href="/diablo-4/de/aspects/[^"]*">([^<]+)</a>'
        names = re.findall(name_pattern, content)
        for name in names:
            name = name.strip()
            # Convert from "Aspekt: Name" to "Name Aspekt" format
            if name.startswith('Aspekt:'):
                name = name.replace('Aspekt:', '').strip() + ' Aspekt'
            aspects.add(name)

    return sorted(aspects)

def main():
    print("=" * 80)
    print("Wowhead Diablo 4 German Term Extractor")
    print("=" * 80)
    print()

    # Extract glyphs
    glyphs = extract_glyphs('https://www.wowhead.com/diablo-4/de/paragon-glyphs')
    print(f"Found {len(glyphs)} glyphs\n")

    # Extract items
    items = extract_items('https://www.wowhead.com/diablo-4/de/items/quality:5,6')
    print(f"Found {len(items)} unique/mythic items\n")

    # Extract aspects
    aspects = extract_aspects('https://www.wowhead.com/diablo-4/de/aspects')
    print(f"Found {len(aspects)} aspects\n")

    print("=" * 80)
    print("RESULTS")
    print("=" * 80)
    print()

    print("GLYPHS:")
    for glyph in glyphs:
        print(f"- {glyph}")

    print()
    print("ITEMS:")
    for item in items:
        print(f"- {item}")

    print()
    print("ASPECTS:")
    for aspect in aspects:
        print(f"- {aspect}")

if __name__ == '__main__':
    main()
