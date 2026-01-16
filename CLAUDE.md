# D4 Glyph Translator

Firefox extension that translates German Diablo 4 paragon glyph names to English on vitablo.de.

## Structure

- `manifest.json` - Manifest V3, targets `*://vitablo.de/*build-guide*`
- `content.js` - MutationObserver-based translator, contains all translation logic
- `translations.json` - Reference file (translations are embedded in content.js)

## How It Works

1. Content script runs on matching pages
2. Only translates text within `.d4para-row` elements (paragon board rows)
3. Replaces German glyph names with "German (English)" format
4. MutationObserver watches for dynamically loaded content within paragon boards

## Adding New Translations

Edit the `translations` object in `content.js`:
```javascript
const translations = {
  "GermanName": "EnglishName",
  // ...
};
```

## Testing

1. `about:debugging` → This Firefox → Load Temporary Add-on → select `manifest.json`
2. Visit: https://vitablo.de/diablo-4-build-guides/

## Translation Sources

- https://www.wowhead.com/diablo-4/paragon-glyphs (English)
- https://www.wowhead.com/diablo-4/de/paragon-glyphs (German)

## Git Flow Convention

This project follows the git flow branching model:

### Branch Structure

- `main` - Production-ready code, tagged releases
- `develop` - Integration branch for features, default development branch
- `feature/*` - New features (branch from `develop`, merge back to `develop`)
- `bugfix/*` - Bug fixes for develop (branch from `develop`, merge back to `develop`)
- `hotfix/*` - Urgent production fixes (branch from `main`, merge to both `main` and `develop`)
- `release/*` - Release preparation (branch from `develop`, merge to both `main` and `develop`)

### Workflow

1. **New features**: Create `feature/feature-name` from `develop`
2. **Bug fixes**: Create `bugfix/bug-description` from `develop`
3. **Releases**: Create `release/x.y.z` from `develop`, merge to `main` and `develop`
4. **Hotfixes**: Create `hotfix/x.y.z` from `main`, merge to `main` and `develop`
5. **Pull requests**: Target `develop` for features/bugfixes, `main` for releases/hotfixes

### Commands

```bash
# Start a new feature
git checkout develop
git checkout -b feature/feature-name

# Finish a feature (via PR to develop)
git push -u origin feature/feature-name

# Start a release
git checkout develop
git checkout -b release/1.0.0

# Finish a release (via PR to main and develop)
git push -u origin release/1.0.0
```
