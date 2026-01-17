# .gitignore Configuration

**Date:** 2026-01-17

---

## What's Ignored

### Python Files
- `__pycache__/` - Python bytecode cache
- `*.pyc`, `*.pyo` - Compiled Python files
- `*.egg-info/` - Python package metadata
- Virtual environments (`venv/`, `env/`, `.venv`)

### Build Artifacts
- `*.xpi` - Firefox extension packages (in project directory)
- `web-ext-artifacts/` - Firefox extension build output
- Parent directory XPI files are NOT ignored (kept for distribution)

### Development Files
- `.vscode/`, `.idea/` - IDE configuration
- `*.swp`, `*.swo` - Editor swap files
- `*.log` - Log files (including `geckodriver.log`)

### Temporary Files
- `*.tmp`, `*.temp` - Temporary files
- `*.bak`, `*.backup` - Backup files
- `temp/`, `tmp/` - Temporary directories

### OS Files
- `.DS_Store` - macOS metadata
- `Thumbs.db` - Windows thumbnails
- `.Trashes` - macOS trash

---

## What's Tracked

All project files are tracked, including:
- `content.js` - Extension script
- `manifest.json` - Extension manifest
- `scrape_*.py` - Scraper scripts
- `update_content_js.py` - Integration script
- `translations_by_*.json` - Translation data
- `*.md` - Documentation
- `build.sh` - Build script

---

## XPI Files

- XPI files in **project directory** are ignored (temporary builds)
- XPI files in **parent directory** are NOT ignored (for distribution)
- Build script (`build.sh`) creates XPI in parent directory: `../diablo4-translation-VERSION.xpi`

---

## Verification

```bash
# Check that __pycache__ is ignored
$ git status --short
# Should NOT show __pycache__

# Check that .gitignore itself is untracked (until added)
$ git status --short
?? .gitignore

# Add .gitignore to repository
$ git add .gitignore
$ git commit -m "Add .gitignore for Python and Firefox extension development"
```

---

## Future Additions

If you add new temporary or build files in the future, update .gitignore accordingly. Common additions might include:
- Test output directories
- Coverage reports
- Node modules (if JavaScript tooling is added)
- Additional build artifacts

---

**Status:** ✅ .gitignore configured and working
