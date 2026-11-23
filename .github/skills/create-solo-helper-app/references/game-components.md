# Transcribe the Game Components to Markdown

Procedure for the transcription part of "Phase A: Gather and Transcribe Sources" of the `create-solo-helper-app` skill. Rulebook PDFs, card sheets and solo boards are transcribed **once** into Markdown files. All later phases (analysis, plan, card definitions, i18n texts, setup instructions) look things up in these files instead of the PDFs.

## Folder Structure

All source files and transcriptions are stored in the **private** repo `brdgm-resources` below `apps/<appDeployName>-solo-helper/` (`<resources>`) - **never in the public app repo**. If `brdgm-resources` is not in the workspace, ask the user to add it first. Create the app folder if it does not exist yet. The source files are kept next to their transcriptions:

```
brdgm-resources/apps/<appDeployName>-solo-helper/
├── rules/
│   ├── <original file names>.pdf          # rulebook PDFs as provided (solo, base, expansions; EN/DE)
│   ├── solo-rules-en.md       # solo rulebook EN (mandatory)
│   ├── solo-rules-de.md       # solo rulebook DE (if available)
│   ├── rules-en.md            # base rulebook EN
│   ├── rules-de.md            # base rulebook DE (if available)
│   └── <expansion>-rules-en.md / -de.md   # expansion rules relevant for the solo mode
├── cards/
│   ├── <original file names>.jpg|pdf      # card scans/photos, print-and-play files
│   └── <deck>-cards.md        # one file per solo deck (e.g. bot-cards.md, objective-cards.md)
├── components/
│   ├── <original file names>.jpg|pdf      # solo board etc. (if not only depicted in the rulebook)
│   └── <component>.md         # solo board, solo mats, bot tiles, markers, reference cards, ...
├── images/                    # optional: page renders/crops needed for later lookup (WebP)
├── glossary.md                # EN/DE terms and icons
├── clarifications.md          # rule uncertainties: decided ones and those to be cleared up later
└── app-plan.md                # confirmed plan from Phase B (see app-plan.md)
```

- If the solo rules are a chapter of the base rulebook, still create a separate `solo-rules-*.md` with that chapter.
- Keep the original file names of the sources as provided by the user.
- The app (code, tests, build, i18n) must **never reference** anything in `brdgm-resources`. Do not copy longer rules passages into code comments.
- The app repo's own `resources/` folder only holds source files of app assets, like `app-icon.psd`.

## File Header

Every file starts with:

```markdown
# <Game> - Solo Rules (EN)

- Source: `<pdf file name>`, pages <from>-<to>
- Edition/version: <as printed in the rulebook, e.g. "v1.2, 2025"> (omit if not printed)
- Transcribed for analysis and lookup while building the solo helper app. Not used by the app.
```

## What to Include

- **All rules text, complete and verbatim** - no summaries, no paraphrasing, no "translation" between languages. Wording must be usable for 1:1 fragments in `en.json`/`de.json`. Fix only extraction artifacts (hyphenation, broken lines, ligatures, column mix-ups). Keep umlauts and special characters exactly (UTF-8 without BOM, see "File Encoding (UTF-8)" in `copilot-instructions.md`) - PDF extraction output read or written through PowerShell easily turns `ü` into `?` or `Ã¼`.
- **EN mandatory, DE if available** - one file per language, with the **same heading structure, order and page markers**, so passages can be matched between languages.
- Setup, game flow, all rules sections, scoring, icon glossaries, FAQ/clarifications, rule boxes and sidebars, variants, difficulty levels, expansion rules relevant for the solo mode.
- **Examples only if they contain additional rule-specific instructions** (e.g. a clarification of an edge case). Then keep the example text as a blockquote: `> **Example:** ...`.
- **Rules information shown only in images** (setup diagrams, card anatomy, solo board illustrations, icon legends): describe the relevant information in text as `_Figure: ..._`. Optionally keep a render/crop in `images/` and link it.

## What to Omit

- Examples without additional rules content.
- Imprint, credits, image attributions, copyright notices, thanks, publisher contact/addresses, marketing text.
- Table of contents, page headers/footers, page numbers in the text, decorative captions.
- Pure flavor/story text without rules content.

## Conventions

- Preserve the **heading hierarchy and order** of the rulebook (`#` = document title, `##` = top-level sections, ...).
- **Page markers** before the content of each page: `<!-- p. 5 -->` (printed page number), for cross-checks against the PDF.
- Lists and tables as Markdown lists/tables; rule boxes and sidebars as blockquotes with their title in bold.
- **Inline icons** as `{icon-name}`: kebab-case English name, identical in EN and DE files, defined in the icons table of `glossary.md`. These names become the future enum values and icon file names (`src/assets/icons/<type>/<name>.<ext>`), so choose them carefully.
- Bold/italic only where the rulebook emphasizes terms.
- **Uncertainties** (unclear or contradictory rules, EN/DE differences, illegible text, unclear icons, assumptions read from images, invented icon names): mark them in place with `TODO (C<n>): <short question>` and add each one to `clarifications.md` (see "Clarifications" below). Never leave an uncertainty only as a `TODO` in a file, or only in a subagent report - the user must not discover it by chance.

## Clarifications (`clarifications.md`)

Central list of all rule uncertainties, one entry per item:

| id | question | sources (file/section, page) | options | status | decision / assumption used |
|----|----------|------------------------------|---------|--------|----------------------------|
| C1 | ... | `components/solo-board.md` "Rondel", p. 19 | A: ..., B: ... | decided / open (clear up later) | ... |

- **Ask the user about every entry** with the ask-questions tool at the end of Phase A, and again for new entries during/after Phase B (plan) and whenever new ones come up during implementation. Use one field per entry. Offer the concrete options with a recommended default, plus the option **"Add to clarification list (clear up later)"**.
- **Decided**: set the status to `decided`, record the decision (and its source, e.g. "user", "designer on BGG <link>"), and replace the `TODO (C<n>)` in the transcription with a note `(C<n>: <decision>)`.
- **Clear up later**: set the status to `open`, and record the assumption the app uses until then (the recommended option, unless the user says otherwise). Keep the `TODO (C<n>)` marker. Open entries are listed in the implementation status of `app-plan.md`, and are asked again at "Finalize and Publish".
- Before ending a phase or step, search `<resources>` for `TODO` and check that every marker has an entry in `clarifications.md` that was asked.

## Card Files (`cards/<deck>-cards.md`)

Derived from the card sheets (rulebook pages, print-and-play files or scans/photos) - **every card, front and back**:

- Short intro: deck name, number of cards, source pages, reference to the rules section about deck building/drawing/reshuffling (`solo-rules-en.md` section name).
- **Identifier scheme** (printed identifier or own scheme, see `app-plan.md`).
- **Card table**, one row per card: `id` | deck/type/difficulty | back (color, symbols, indicators) | front: actions in printed order with `{icon}` names and parameters | notes (conditions, fallbacks, unclear icons marked with `TODO (C<n>)`).
- Text printed on the cards: verbatim, with an EN and a DE column if the cards are language-dependent and both are available.
- **Rulebook text first**: if the rulebook explains every icon/action of the cards (usually with the same content as the card text plus extra information), the app shows that **full rulebook text** (EN and DE from `rules/*-en.md`/`*-de.md`) in the action help modal. Card texts are then only for cross-checking. Add a "Rules Texts per Action" table to the card file (icon → rulebook paragraph EN/DE, page). Do not derive translations for card texts the rulebook already covers.
- If only one language of the cards is available, take the other language from example card images in the rulebook where they exist. Derive texts from the other language (using the rulebook terms) only where nothing else exists, and mark them as `derived` for review.

## Component Files (`components/<component>.md`)

One file per solo component besides the solo cards (solo board, solo mat, bot tiles, dials, markers, reference/overview cards, ...):

- What the component is, source pages, image description (`_Figure: ..._`, optional render in `images/`).
- **Every area/track/space/slot**: what it holds or tracks, how it is used according to the rules (with the section name in the rules file), when it changes, whether the player interacts with it.
- **App handling** per area: filled in during Phase B (`replaced by the app` / `still needed physically` + reason / `partly`), see "Solo Board and Other Solo Components" in `app-plan.md`.

## Glossary (`glossary.md`)

- **Terms**: EN | DE | kebab-case id (future enum value) | type (component, action, resource, phase, track, ...) | rules reference/page. EN/DE terms exactly as used in the rulebooks.
- **Icons**: `{icon-name}` | meaning (EN, as in the rulebook's icon glossary) | where used (cards, solo board, rules) | page.

## Procedure

Transcription is the most token-intensive part of the whole skill. **Images are the cost driver**: every page image or crop an agent views stays in its context and is re-sent with every following step - so the cost of an agent grows with (images viewed) × (steps after them). Text from a PDF text layer is cheap. Work lean:

1. **Inventory first** (cheap, no images): run [scripts/prepare-sources.py](../scripts/prepare-sources.py) `inventory <resources>` (`python -X utf8`, needs `pymupdf`; install into a temporary venv in the session folder if missing). It lists every PDF with page count, text layer or scan, garbled spans and an effort estimate.
2. **Ask the user how to proceed** (ask-questions tool) - present the inventory table with the effort per source, a recommended scope and the options, e.g.:
   - text-layer PDFs (low effort): transcribe fully;
   - scans (high effort, one image per page plus crops): fully / only the solo-relevant parts (solo rules, solo cards, solo board) / only terms for the glossary / later;
   - expansions, fan-made/unofficial material: fully / only solo-relevant rules and deviations from the official rules / skip for now;
   - DE versions: fully (needed for 1:1 wording in `de.json`) / only solo rules + terms.

   Never start a high-effort source without this decision.
3. **Prepare once, centrally**: `prepare-sources.py extract <resources> <session-folder>/sources` writes the text of all text-layer PDFs (garbled `WKH`-style spans already decoded) and page renders at moderate resolution. Write a shared `{icon-name}` vocabulary (from the rulebook's icon legend) and one short common instruction file for subagents to the session folder. Subagents reuse these - nobody extracts or renders again.
4. **Transcribe**:
   - Text-layer PDFs: transcribe from the extracted text. Look at a page image only for pages with figures, icon-only rules or tables - not for every page.
   - Scans: view each page image **once** at normal resolution. Crops only for specific values that are not legible (card values, track spaces), at most ~2-3 per page, ~250 dpi, combining several details in one crop. If still unreadable: `TODO (C<n>)` instead of zooming further - the user can check the physical component.
   - Card sheets and solo boards: one overview image per sheet, then targeted crops of the card headers/value areas only. Write the card table right away, card by card.
5. **Delegating to subagents** (learnings):
   - **Small, bounded tasks with a fresh context**: one document (≤ ~6 scan pages) per agent; split long scans (e.g. 16 pages → 3-4 agents by page range). The coordinator's long context is more expensive than a fresh subagent.
   - The prompt lists the **exact input files** (text file, page images, icon vocabulary, format template) and says "read nothing else": no other apps' resources, no full rulebook "for context" unless the task needs it. Use the first finished file of **this** app as format template.
   - Give an **image budget** ("view each page image once, at most N crops") and the TODO fallback.
   - **Write incrementally** (create the file after the first page, then append per page with the edit tool), so an interruption (cancel, IDE crash) loses no work. On restart, tell the agent to continue from the existing file, not from scratch.
   - **Short final report**: files written, TODOs, new icon names and terms - no data dumps.
   - **No duplicate work**: the coordinator does not view the page images of delegated sources itself, and does not delegate what it already did. Check output files (page markers) instead of re-reading sources.
   - Run independent agents in parallel, but check after a few minutes that they produce output (file size grows); stop an agent that has not written anything instead of letting it run.
6. **Ask back on the way** if a source turns out more expensive than estimated (e.g. many unreadable details, a scan of poor quality): report the status and offer to continue / reduce the scope / mark the rest as TODO.
7. Write the files following the conventions above; resolve every inline icon to a `{icon-name}` in the glossary.
8. **Verify completeness**: every page of the source has its page marker, no rules section is missing, EN and DE files have the same structure, every card of every deck is in the card table. Check page markers with a script, not by re-reading. **Verify the encoding**: no replaced umlauts or special characters (`?`, `Ã`, `Â`, `â€`, `\uFFFD`), no BOM.
9. Collect **all** uncertainties (illegible text, unclear icons, differences between EN and DE, assumptions from images, invented icon names, and every uncertainty reported by subagents) in `clarifications.md`, mark them with `TODO (C<n>)`, and **ask the user about each one** (see "Clarifications"). Ask the user to spot check the transcription. Subagents use their own TODO prefix (e.g. `TODO (C-D1)`) to avoid collisions; the coordinator renumbers them when creating `clarifications.md` and merges duplicates (e.g. the same question in the EN and DE file).
10. Delete temporary crops; keep the extracted text and page renders in the session folder for later lookups.

Later phases use these files as the primary source. Go back to the PDFs/page images only for visual questions. If an error in a transcription is found later, fix the Markdown file. Suggest a commit message for `brdgm-resources` after the transcription.
