#!/bin/bash
# Setup script for Wowhead scraping tools

set -e

echo "=========================================="
echo "Wowhead Scraper Setup"
echo "=========================================="
echo

# Check Python
echo "Checking Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "✅ $PYTHON_VERSION"
echo

# Check pip
echo "Checking pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip is not installed"
    exit 1
fi
PIP_VERSION=$(pip3 --version)
echo "✅ $PIP_VERSION"
echo

# Check Firefox (for Selenium scrapers)
echo "Checking Firefox..."
if command -v firefox &> /dev/null; then
    FIREFOX_VERSION=$(firefox --version)
    echo "✅ $FIREFOX_VERSION"
else
    echo "⚠️  Firefox not found (required for Selenium scrapers)"
    echo "   Install with: sudo pacman -S firefox (Arch/CachyOS)"
    echo "   Or: sudo apt install firefox (Ubuntu/Debian)"
fi
echo

# Check geckodriver (for Selenium scrapers)
echo "Checking geckodriver..."
if command -v geckodriver &> /dev/null; then
    GECKO_VERSION=$(geckodriver --version | head -n1)
    echo "✅ $GECKO_VERSION"
else
    echo "⚠️  geckodriver not found (required for Selenium scrapers)"
    echo "   Install with: sudo pacman -S geckodriver (Arch/CachyOS)"
    echo "   Or: sudo apt install firefox-geckodriver (Ubuntu/Debian)"
    echo "   Or download from: https://github.com/mozilla/geckodriver/releases"
fi
echo

# Install Python dependencies
echo "Installing Python dependencies..."
if pip3 install -r requirements.txt; then
    echo "✅ Dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo

# Summary
echo "=========================================="
echo "Setup Summary"
echo "=========================================="
echo
echo "Available scrapers:"
echo "  1. scrape_wowhead.py           - Basic (requests only)"
echo "  2. scrape_wowhead_selenium.py  - Enhanced (requires Firefox)"
echo "  3. scrape_wowhead_advanced.py  - Advanced (requires Firefox) ⭐"
echo
echo "Quick start:"
echo "  python3 scrape_wowhead.py              # Basic scraper"
echo "  python3 scrape_wowhead_advanced.py     # Recommended"
echo
echo "See SCRAPING.md for detailed documentation"
