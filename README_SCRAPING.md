# Wowhead Scraping Documentation Index

Quick navigation for all scraping-related documentation.

## 🚀 Quick Start

**I just want to scrape Wowhead translations:**
→ Read [QUICKSTART_SCRAPING.md](QUICKSTART_SCRAPING.md)

**I want to understand why ID-based is better:**
→ Run `python3 compare_architectures.py` (interactive demo)

**I want comprehensive documentation:**
→ Read [SCRAPING.md](SCRAPING.md)

## 📚 Documentation Files

### For Users

| File | Purpose | When to Read |
|------|---------|--------------|
| [QUICKSTART_SCRAPING.md](QUICKSTART_SCRAPING.md) | Quick reference guide | Starting scraping |
| [SCRAPING.md](SCRAPING.md) | Complete scraping guide | Need full details |
| [ID_BASED_ARCHITECTURE.md](ID_BASED_ARCHITECTURE.md) | ID-based architecture explanation | Understanding design |
| [ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md) | Visual diagrams | Visual learner |
| [SUMMARY_ID_BASED.md](SUMMARY_ID_BASED.md) | Summary of ID improvements | Quick overview |

### For Developers

| File | Purpose | When to Read |
|------|---------|--------------|
| [compare_architectures.py](compare_architectures.py) | Interactive demo | See concrete examples |
| [scrape_wowhead_v2.py](scrape_wowhead_v2.py) | V2 scraper source | Understand implementation |
| [requirements.txt](requirements.txt) | Python dependencies | Setup environment |
| [setup_scraper.sh](setup_scraper.sh) | Setup script | Automated setup |

## 🛠️ Available Tools

### Scrapers

1. **`scrape_wowhead.py`** - Basic (requests only)
   - No browser needed
   - Fast but limited

2. **`scrape_wowhead_selenium.py`** - Enhanced (Selenium)
   - JavaScript support
   - More comprehensive

3. **`scrape_wowhead_advanced.py`** - Advanced
   - ID-based matching
   - Accurate translations

4. **`scrape_wowhead_v2.py`** - ⭐ **RECOMMENDED**
   - ID-based architecture
   - Future-proof design

### Utilities

- **`compare_architectures.py`** - Interactive demo
- **`setup_scraper.sh`** - Automated setup

## 📖 Reading Order

### Beginner Path
1. [QUICKSTART_SCRAPING.md](QUICKSTART_SCRAPING.md) - Get started
2. Run `python3 scrape_wowhead_v2.py` - Try it
3. [ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md) - See visuals

### Advanced Path
1. [SCRAPING.md](SCRAPING.md) - Full documentation
2. [ID_BASED_ARCHITECTURE.md](ID_BASED_ARCHITECTURE.md) - Architecture deep dive
3. Run `python3 compare_architectures.py` - See examples
4. Read [scrape_wowhead_v2.py](scrape_wowhead_v2.py) - Understand code

### Decision Maker Path
1. [SUMMARY_ID_BASED.md](SUMMARY_ID_BASED.md) - Quick benefits
2. Run `python3 compare_architectures.py` - See demos
3. [ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md) - Visual comparison

## 🎯 Common Tasks

### Task: "I want to extract translations"
```bash
# Quick method (basic)
python3 scrape_wowhead.py

# Recommended method (comprehensive + future-proof)
pip install -r requirements.txt
sudo pacman -S firefox geckodriver
python3 scrape_wowhead_v2.py
```

### Task: "I want to understand why ID-based is better"
```bash
# Interactive demo
python3 compare_architectures.py

# Or read
cat ID_BASED_ARCHITECTURE.md
```

### Task: "I want to see the architecture"
```bash
cat ARCHITECTURE_DIAGRAM.md
```

### Task: "I need help with setup"
```bash
./setup_scraper.sh
```

### Task: "I want to see code examples"
```bash
# Read the scraper source
cat scrape_wowhead_v2.py

# Or run the demo
python3 compare_architectures.py
```

## 🔍 Key Concepts

### What is ID-Based Architecture?

Instead of:
```javascript
{ "Macht": "Might" }  // String key (collision risk)
```

Use:
```javascript
{ 12345: { de: "Macht", en: "Might" } }  // ID key (unique)
```

**Benefits:**
- ✅ No collisions
- ✅ Metadata support
- ✅ Easy updates
- ✅ Multi-language ready

### Why Multiple Scrapers?

Each serves a purpose:
- **Basic** - No dependencies, quick test
- **Selenium** - Learning example
- **Advanced** - Production ready (string-based)
- **V2** - Production ready (ID-based) ⭐

### What's the Recommended Approach?

**Use `scrape_wowhead_v2.py`** because:
1. ID-based architecture (future-proof)
2. No collisions
3. Metadata support
4. Backward compatible
5. Easy to maintain

## 📊 Comparison Table

| Feature | Basic | Selenium | Advanced | V2 ⭐ |
|---------|-------|----------|----------|-------|
| Dependencies | requests | selenium | selenium | selenium |
| JavaScript | ❌ | ✅ | ✅ | ✅ |
| Pagination | ❌ | ✅ | ✅ | ✅ |
| ID Matching | ❌ | ❌ | ✅ | ✅ |
| ID Storage | ❌ | ❌ | ❌ | ✅ |
| Metadata | ❌ | ❌ | ❌ | ✅ |
| Multi-lang Ready | ❌ | ❌ | ❌ | ✅ |
| Coverage | ~100 | ~200+ | ~400+ | ~400+ |

## 🎓 Learning Resources

### Visual Learners
→ [ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md)

### Hands-On Learners
→ Run `python3 compare_architectures.py`

### Documentation Readers
→ [ID_BASED_ARCHITECTURE.md](ID_BASED_ARCHITECTURE.md)

### Code Readers
→ Read [scrape_wowhead_v2.py](scrape_wowhead_v2.py)

## ❓ FAQ

**Q: Which scraper should I use?**
A: `scrape_wowhead_v2.py` - It's the most future-proof.

**Q: Do I need Firefox?**
A: Yes for V2, Selenium, and Advanced scrapers. No for Basic.

**Q: Is ID-based more complex?**
A: Slightly more data, but much easier to maintain long-term.

**Q: Can I use the old string-based format?**
A: Yes! V2 exports both formats for backward compatibility.

**Q: What's the file size overhead?**
A: ~100 KB extra (negligible for modern browsers).

**Q: Where do I start?**
A: [QUICKSTART_SCRAPING.md](QUICKSTART_SCRAPING.md)

## 🔗 Related Files

- [CLAUDE.md](CLAUDE.md) - Main project documentation
- [content.js](content.js) - Current translation implementation
- [manifest.json](manifest.json) - Extension manifest

## 💡 Tips

1. **Start Simple**: Try `scrape_wowhead.py` first to understand the concept
2. **Go Deep**: Use `scrape_wowhead_v2.py` for production
3. **Learn Why**: Run `compare_architectures.py` to see benefits
4. **Read Code**: [scrape_wowhead_v2.py](scrape_wowhead_v2.py) is well-commented

## 🚦 Status

- ✅ Basic scraper - Working
- ✅ Selenium scraper - Working
- ✅ Advanced scraper - Working
- ✅ V2 scraper - **Recommended** ⭐
- ✅ Documentation - Complete
- ✅ Setup automation - Available

## 📝 Quick Command Reference

```bash
# Setup
./setup_scraper.sh

# Run scrapers
python3 scrape_wowhead.py              # Basic
python3 scrape_wowhead_selenium.py     # Selenium
python3 scrape_wowhead_advanced.py     # Advanced
python3 scrape_wowhead_v2.py          # V2 (recommended)

# Demo
python3 compare_architectures.py

# Read docs
cat QUICKSTART_SCRAPING.md
cat SCRAPING.md
cat ID_BASED_ARCHITECTURE.md
cat ARCHITECTURE_DIAGRAM.md
```

---

**Need help?** Start with [QUICKSTART_SCRAPING.md](QUICKSTART_SCRAPING.md)!
