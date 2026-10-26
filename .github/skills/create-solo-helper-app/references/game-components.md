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

1. Extract the text with available tools (e.g. Python `pypdf`/`pdfplumber`, `pymupdf` for page renders); install them into a temporary virtual environment in the session folder, not in the app repo. Long rulebooks can be transcribed file by file (e.g. one subagent per PDF/language) to keep the context small.
2. Render the pages to images and **compare** them with the extracted text - extraction often mixes columns, drops icons, breaks umlauts/ligatures and loses tables. Fix the Markdown accordingly. Look at the page images for card sheets, icon glossaries, setup diagrams and solo boards.
3. Write the files following the conventions above; resolve every inline icon to a `{icon-name}` in the glossary.
4. **Verify completeness**: every page of the source has its page marker, no rules section is missing, EN and DE files have the same structure, every card of every deck is in the card table. **Verify the encoding**: no replaced umlauts or special characters (`?`, `Ã`, `Â`, `â€`, `\uFFFD`), no BOM.
5. Collect **all** uncertainties (illegible text, unclear icons, differences between EN and DE, assumptions from images, invented icon names, and every uncertainty reported by subagents) in `clarifications.md`, mark them with `TODO (C<n>)`, and **ask the user about each one** (see "Clarifications"). Ask the user to spot check the transcription. When delegating transcription to subagents, instruct them to mark uncertainties with `TODO` and to report them; then add the reported ones to `clarifications.md`.

Later phases use these files as the primary source. Go back to the PDFs/page images only for visual questions. If an error in a transcription is found later, fix the Markdown file. Suggest a commit message for `brdgm-resources` after the transcription.
