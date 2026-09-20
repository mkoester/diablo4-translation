# diablo4-translation

A browser userscript/extension translating Diablo 4 UI terms into German. Plain JS; the dictionary
lives in `content.js`.

Cross-project conventions come from the OKF vault — including git-flow branch naming and the
release procedure, which are **not** restated here. Structure, the translation-architecture
walkthrough and the translation sources are in `docs/design-notes.md`.

## Working on it

- **The dictionary is the artifact.** Adding a translation means adding an entry, not adding code —
  read the existing shape in `content.js` rather than inventing a new one.
- **Translation sources are recorded per category** (paragon glyphs, affixes, …) in
  `docs/design-notes.md`. Use the recorded source for a category rather than a general one, so
  terms stay consistent with how the German client actually names them.
- `scripts/test` covers the pure lookup helpers; keep matching logic out of the DOM walk so it
  stays testable.
