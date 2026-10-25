---
name: create-solo-helper-app
description: 'Create a new brdgm.me solo helper app (Vue 3 + TypeScript PWA) for a new board game solo mode, step by step in the same style as the existing *-solo-helper apps. Use when: planning a new solo helper, transcribing rulebook PDFs and solo cards to markdown in brdgm-resources, writing or continuing the app plan, analyzing solo rules, solo cards and solo board, scaffolding a new brdgm app, implementing a new game automa/AI opponent app, creating app skeleton, assets/icons, card definitions, CardDeck, setup screens, player/bot turn views, sidebar, end game scoring or game statistics for a new game.'
argument-hint: 'Game name (and optionally BoardGameGeek link / solo rules)'
---

# Create a New Solo Helper App

Guides through creating a new `<appDeployName>-solo-helper` app in the same order the existing apps were built. Read `.github/copilot-instructions.md` first - all patterns and rules there apply - and the code guidelines in `.github/instructions/vue-components.instructions.md`, `typescript.instructions.md` and `i18n.instructions.md`.

## Golden Rules

- **Use the latest apps as templates** (`south-tigris-scholars`/`-inventors`/`-wayfarers`, `galactic-cruise`, `maracaibo`, `seti`, `grand-austria-hotel`), never the legacy ones (`blitzkrieg`, `monumental`, `ark-nova`, ... see "Reference Implementations" in `copilot-instructions.md`). `bloomworks` is still in development and is **not** a reference yet.
- The new app must look like the others: same skeleton, header/footer, home page, credits modal, footer buttons, button styles, shared i18n keys. Deviate only where the game's solo mode clearly needs a different UI or pattern.
- **Copy the look & feel and the patterns, not the code smells**: when copying components or views from a reference app, apply the code guidelines in `.github/instructions/vue-components.instructions.md` and `typescript.instructions.md` (Options API split between `setup()`/`data()`/`computed`, `v-model` via computed get/set, typed emits without `eslint-disable`, `useId()` instead of `nanoid`, no DOM access, accessible clickable elements, VP formulas in `util/` with tests) and fix the smells listed in their "Do Not Copy" tables.
- Reuse brdgm-commons components and utilities wherever possible.
- **Never invent solo rules** - everything comes from the official solo rulebook and the solo cards. Mark every rule uncertainty with `TODO (C<n>)` and collect it in `<resources>/clarifications.md`. **Proactively ask the user about each one** - at the end of Phase A, with the plan, and whenever new ones come up. The user either decides, or has it added to the list to be cleared up later (the app then uses a documented assumption). Never leave an uncertainty for the user to discover by chance, and never decide one silently.
- **Game resources outside the app repo**: rulebook PDFs, card scans, their transcriptions, the glossary and the app plan live in the private repo `brdgm-resources` in `apps/<appDeployName>-solo-helper/` (see "Game Resources" in `copilot-instructions.md`) - **never in the public app repo**. The app never references these files.
- **Transcribe first**: rulebook PDFs, solo cards and solo components are transcribed once to Markdown in the game resources folder; all later steps look things up there.
- **Not a card flipper**: the app takes over as many bot decisions and as much bot bookkeeping (resources, VP, tracks, ...) as possible. The player only gives input where the board must be inspected or the input results from the player's own actions.
- **Replace the solo components**: ideally the player needs neither the solo cards nor the solo board (solo mat, bot tiles, markers, ...). Only parts that are really needed (e.g. a place for items collected by the bot) remain physical, and the app says exactly which.
- **Preserve the hints of the physical solo mode** (e.g. the visible back of the next solo card, discard pile composition) - but do not reveal more than the physical game.
- **Use the rulebook wording**: terms and short rules fragments 1:1 from the official English (mandatory) and German (if available) rulebooks.
- **Plan first**: no implementation before the plan from Phase B is **explicitly confirmed** by the user. After writing the draft plan and resolving the open questions, **stop and end the turn** so the user can review `app-plan.md` - never continue to step 1 in the same turn.

## Working Mode

The app is built **incrementally**: first Phase A and B (sources and their transcription, analysis, plan), then the **implementation steps defined in the plan**, usually over several sessions.

`<resources>` below = `brdgm-resources/apps/<appDeployName>-solo-helper/`.

1. **Make sure `brdgm-resources` is in the workspace** first. If it is missing, ask the user (ask-questions tool) to add it to the workspace (it is usually checked out next to the app repos) and wait - do not create the files elsewhere (e.g. in the app repo or the session folder) and do not continue on guessed rules.
2. **Find the current phase/step**: are the transcriptions in `<resources>` complete? Is there a confirmed plan (`<resources>/app-plan.md` with its implementation steps and status)? Inspect the target app folder (does it exist? `src/services/Cards.ts`? `CardDeck.ts`? which views and routes?) and ask the user which step to continue with if it's unclear.
3. **Implementation steps**: the plan splits the implementation into **3-10 reviewable steps**, tailored to the game. Each step has:
   - a goal;
   - its scope (files/features);
   - its validation;
   - what the user can review afterwards (e.g. screens to try in `npm run dev`).

   The generic steps 1-6 below are the building blocks: small ones can be merged (e.g. assets + card definitions), and large ones split (e.g. 5b game flow → player/bot turn skeleton, bot actions, round end/milestones). Each step leaves a runnable app.
4. **One step per turn, then stop.** Implement exactly one implementation step of the plan. Never implement several steps or the whole app in one go. At the end of the step:
   1. Run the validation listed for it.
   2. Update the implementation status in `<resources>/app-plan.md`.
   3. Summarize what was done and what is still open (missing assets, unclear rules - new ones go to `clarifications.md` and are asked - and `TODO`s), and what to review.
   4. Suggest commit messages (app repo and, if changed, `brdgm-resources`).
   5. **End the turn.**

   Continue with the next step only after the user has explicitly confirmed the reviewed step (e.g. "step 2 confirmed, continue"). If the implementation reveals that the plan needs to change, propose the change, ask first and update `app-plan.md` (incl. the step list).
5. Keep the app **runnable after every step**: `npm run lint`, `npm run test:unit run`, `npm run build` and `npm run test:e2e` must pass after **every** step - not only in step 1. The e2e smoke test is extended in each step that changes the flow, so it always covers the complete flow implemented so far (home → setup → ... → abort/end game).
   - Run the e2e test like the CI does, against the production build: `npm run build`, then `CI=1 npx playwright test` (PowerShell: `$env:CI='1'; npx playwright test`). Without `CI`, Playwright reuses any dev server already running on port 8080 - possibly another app or a stale build.
   - The `image` version in `.github/workflows/test-e2e.yml` (`mcr.microsoft.com/playwright:v<version>-noble`) must equal the installed `@playwright/test` version (`package-lock.json`), otherwise the CI e2e test fails ("Playwright version mismatch"). Check this after every `npm install` - a fresh `npm install` often resolves a newer Playwright version than the reference app's workflow uses.

## Phase A: Gather and Transcribe Sources

Ask the user for anything not provided yet:

| Item | Used for |
|------|----------|
| Game title, BoardGameGeek URL | `gameTitle`, home page, credits |
| `appDeployName` (kebab-case, e.g. `south-tigris-scholars`) → repo `<appDeployName>-solo-helper` | `package.json`, URLs, Sonar key |
| Game design, artist, publisher (+ URLs) | Credits modal |
| Official app with publisher permission, or unofficial | Home page disclaimer |
| Published game or prototype | Prototype alert, version `0.x.0` vs `1.0.0` |
| Publisher is **Karma Games**? | Game statistics (step 6) |
| **Solo rulebook EN (mandatory) and DE (if available)**, base rulebook EN/DE | Game flow, bot logic, terms and texts in `en.json`/`de.json` |
| **All solo cards (front and back)** of all solo decks (part of the rulebook PDF, print-and-play files or scans/photos) | Actual bot actions, card definitions, icons |
| **Solo board and other solo components** (solo mat, bot tiles, markers, overview cards - usually depicted in the solo rulebook) | Bot state the app takes over, parts still needed physically |
| AI opponent name | Texts |

The user stores the source files (PDFs, card scans/photos, print-and-play files, solo board images) in `<resources>/rules/`, `cards/` and `components/` - or provides them and you copy them there. Create the folder `<resources>` if it does not exist yet.

Then **transcribe the sources to Markdown** next to the source files in `<resources>` following [game-components.md](./references/game-components.md):

- `rules/`: all rules text of the solo and base rulebooks (and relevant expansions) verbatim, EN (mandatory) and DE (if available) in separate files with identical structure and page markers. Examples without additional rules content, imprint, credits, image attributions and similar are omitted.
- `cards/`: one card table per solo deck (every card, front and back, with identifiers).
- `components/`: solo board and other solo components with all areas and their purpose.
- `glossary.md`: EN/DE terms and icon names (`{icon-name}`, future enum values/icon file names).

Verify completeness against the PDFs. Collect all uncertainties in `clarifications.md` and ask the user about each of them (decide, or add to the list to clear up later - see "Clarifications" in [game-components.md](./references/game-components.md)), and ask the user to spot check. Nothing of this goes into the app repo.

## Phase B: Analyze and Plan

Analyze the transcribed rules, **every solo card** and **every solo component**, then create a detailed plan for the app, following [app-plan.md](./references/app-plan.md):

- full game flow for the player, and the bot's part per phase (bots often have shortcuts or are not active in all phases)
- solo decks: build/draw/reshuffle rules, card table with a **unique identifier per card** (printed number or letter/number code like `A1`, or an own documented scheme), card fronts and backs
- solo board and other solo components: what each area is for, and whether the app replaces it or it is still needed physically (e.g. storage for items collected by the bot)
- clear split **managed by the app vs. done/entered by the player**, bot state to persist
- routes and views, sidebar contents, preserved hints of the physical solo mode
- setup screens, end game scoring, services/enums, needed icons, EN/DE glossary
- open questions and alternative approaches with a recommendation

Write the plan as a draft to `<resources>/app-plan.md`, ask the open questions (ask-questions tool, one field per concrete question with a recommended default), incorporate the answers, then **end the turn** and let the user review the file (see "Review Loop" in [app-plan.md](./references/app-plan.md)). Start step 1 only after the user has explicitly confirmed the plan; then remove the draft marker. `app-plan.md` (incl. the implementation steps and their status) is the reference for all later sessions.

## Step 1: App Skeleton

Goal: a running app with home screen, an empty setup screen, credits and proper naming - no game logic yet.

Copy the framework files from the recent reference app chosen in the plan and adapt them as described in [skeleton-files.md](./references/skeleton-files.md). The skeleton contains:

- All infrastructure files (build, lint, test, PWA, workflows, `.vscode`, `.editorconfig`, ...), `main.ts`, `i18n.ts`, `App.vue`.
- **Proper naming**: visible name (`description` in `package.json`, `<title>` in `index.html`, `gameTitle`/`home.title` in `en.json`) and internal name (`name`, `appDeployName`, README, Sonar key).
- **Credits modal** in `App.vue` with BGG link, game design, artist, publisher and the app's GitHub links.
- **Home screen** `AppHome.vue` with game image, `home.play1`/`play2` texts, disclaimer, feedback links (commented out until a BGG thread exists), prototype alert if unpublished.
- **Empty setup screen** (`SetupApp.vue` or `SetupGame.vue`) with title, placeholder content, button to the next (not yet existing) setup step, `FooterButtons endGameButtonType="abortGame"`.
- Router with `AppHome`, the setup route and `NotFound`.
- Minimal stubs: `store/state.ts` (`language`, `baseFontSize`, `setup: { debugMode? }`, empty `turns`/`rounds`, `resetGame()`), `util/NavigationState.ts` (route params only), `components/round|turn/SideBar.vue` and `DebugInfo.vue`, `components/structure/FooterButtons.vue` and `AppIcon.vue`, `services/enum/Player.ts`.
- Test stubs: `tests/unit/helper/mockState.ts`, `mockRouteLocation.ts`, `mockTurn.ts`/`mockRound.ts`, `tests/unit/util/NavigationState.spec.ts`; `tests/e2e/smoke-test.spec.ts` covering home → setup → abort game.
- **Locale files `en.json` and `de.json`** containing only the keys used on the existing screens (shared keys `gameTitle`, `home`, `setup.title`, `action`, `footer`, `serviceWorkerUpdatedRefresh`, `notfound`). `de.json` must have identical keys (lint checks this). Game title and terms as in the EN/DE rulebooks.
- App icon: `public/img/icons/app-icon.png` (+ `resources/app-icon.psd` source if available) → `npm run generate-pwa-assets` (generates the PWA icons and `public/img/icons/favicon.ico`); `src/assets/game-<appDeployName>.webp` (game box image, max 800 px on the longer side so it fits into an 800×800 box, aspect ratio of the box cover - a placeholder uses the same limit, e.g. 600×800); `src/assets/kofi_button_dark.png`. Ask the user for the images; use clearly marked placeholders until provided. `public/favicon.ico` and `public/img/icons/favicon.svg` are the generic brdgm.me icon, identical in all apps: copy them unchanged from the reference app, never replace them or create placeholders for them.

**Remove all leftovers of the reference app** (game-specific components, enums, i18n keys, icons, texts in stubs, e2e steps).

Validate: `npm install`, align the Playwright image in `test-e2e.yml` with the installed `@playwright/test` version, `npm run lint`, `npm run test:unit run`, `npm run build`, e2e test in CI mode (see "Working Mode" 5); start `npm run dev` and check home, setup, credits, language switch.

## Step 2: Assets and Icons

The user usually extracts the icons from the rulebook PDF (card symbols, action icons, resources, ...). Support this step by:

- Starting from the **icon list of the plan**: a checklist of all needed icons, grouped by type, with the planned file names (the `{icon-name}`s from `<resources>/glossary.md`). File names must match the **future enum values** (kebab-case), because they are loaded via `<AppIcon type="<type>" :name="enumValue"/>` → `src/assets/icons/<type>/<name>.<ext>`.
- Format: **SVG** if the rulebook provides vector graphics (default in `south-tigris-*`), otherwise **WebP** (default in `seti`, `maracaibo`, `galactic-cruise`). Set the `extension` default in `AppIcon.vue` to the predominant format. Raster icons are typically ~50-200 px high (larger only for card-like images); the game box image fits into an 800×800 box (max 800 px on the longer side).
- Common icons in `src/assets/icons/`: `help-semi-transparent.webp` (copy from a reference app, used by `ActionBox`), plus game-specific ones.
- If the user asks for it, help extracting images from the PDFs in `<resources>/rules/` with available tools; otherwise just provide the checklist and verify that the files the user added match the expected names.

Validate: check the list of missing/unexpected files against the checklist; lint, unit tests, build and e2e test still pass.

## Step 3: Card Definitions

- `services/Card.ts`: `Card` interface (`id` + card properties incl. information on the card back, if relevant) and `CardAction` interface (`action: Action` + optional parameters) as defined in the plan's card table. `id` is a `number` for purely numeric identifiers, otherwise a `string` (e.g. `'A1'`).
- `services/Cards.ts`: static array with **all cards** exactly as printed (source: `<resources>/cards/<deck>-cards.md`), each with its **unique identifier** as `id` (printed number/code, or the own scheme from the plan - documented in a comment), a `Map` for lookup, `get(id)` via `findMandatory`, `getAll(...)` (optionally filtered by card type/deck).
- Enums needed by the cards in `services/enum/` (`Action`, `CardType`, colors, ...), string values kebab-case matching icon names.
- **Multiple decks**: either one `Card`/`Cards` with a `CardType`/`DeckType` enum (`grand-austria-hotel`, `south-tigris-inventors`) or separate card classes per deck/bot (`maracaibo`: `jacques/JacquesCards.ts`, `jean/JeanCards.ts`; `seti`: `Cards.ts` + `Objectives.ts`).
- Unit test `tests/unit/services/Cards.spec.ts`: `get(id)` and expected card counts per deck.

Validate: lint, unit tests, build, e2e test. Ask the user to double check card data against the physical cards/rulebook (summarize counts per type).

## Step 4: Core Services

- `services/CardDeck.ts` (one per deck if needed): private constructor, Vue `ref`s for `pile`/`discard` (and other piles the rules need), getters returning `readonly` data, `currentCard`, `draw()`, reshuffle logic as in the solo rules, `static new(...)` (lodash `shuffle`, difficulty/expansion dependent cards), `static fromPersistence(p)`, `toPersistence()` with card IDs only.
- `CardDeckPersistence` (and later `BotPersistence`) interfaces in `store/state.ts`; `tests/unit/helper/mockCardDeck.ts` (+ `mockBotPersistence.ts`).
- Other bot state services from the plan (resources, tracks, markers, ...) using the same `new`/`fromPersistence`/`toPersistence` pattern; `util/getDifficultyLevelSettings.ts` if difficulty levels exist.
- Thorough unit tests (`CardDeck.spec.ts`: new deck counts, draw order, reshuffle, persistence round trip) using fixed card IDs.

Validate: lint, unit tests with good coverage of the services, build, e2e test.

## Step 5: Screens - Setup, Game Flow, End of Game

Implement step by step, each sub-step runnable and committed separately.

### 5a. Setup Screens

1. **General game setup** (`SetupApp.vue`/`SetupGame.vue`): options stored in `state.setup` - e.g. `components/setup/DifficultyLevel.vue` (range slider), `ExpansionsSetup.vue` (switches, `getAllEnumValues`), start player, bot mode, player color. Copy setup components from `seti` / `south-tigris-scholars`.
2. **Bot setup instructions** (`SetupBot.vue`, sometimes `SetupGameBoard.vue`): numbered `setupBot.instructions.*` list as in the solo rulebook (texts depending on difficulty/expansions, wording from the EN/DE rulebooks, components managed by the app marked as such - in particular the solo cards and the solo board or the parts of it that are not needed anymore; the parts still needed physically are named explicitly), "rule changes" summary in `alert alert-info`, "Start Game" button that initializes the bot persistence (`CardDeck.new(...)`, ...) and stores the first turn/round, then routes to the first game screen.
3. **Optional randomizer** to help setting up the board (random tiles/goals/setup cards) using `randomEnum`/`rollDice`/lodash `shuffle`, generated when leaving the general setup and stored in `state.setup` so it survives reloads: see `seti` (`getRandomGoldScoreTileSetup` in `SetupApp.vue`, displayed by `GoldScoringTiles.vue` in `SetupGameBoard.vue`), `galactic-cruise` (`getActionSetup`, `getDevelopmentSetup`, `components/setup/GameSetup.vue`).

Update the smoke test to go through all setup screens up to the first game screen.

### 5b. Game Flow

Implement the routes and views of the confirmed plan. The game flow references (also used for choosing the reference app in the plan):

| Game flow | Reference |
|-----------|-----------|
| Alternating player/bot turns, no rounds (`/turn/:turn/player\|bot`) | `south-tigris-scholars`, `-wayfarers`, `-inventors` |
| Rounds with turns until passing, round start screen | `grand-austria-hotel` (`RoundStart`, `TurnPlayer`, `TurnBot`), `south-tigris-inventors` (`RoundStart`) |
| Rounds with complex turn order/passing, `RouteCalculator` | `seti` (`getTurnOrder`, `RouteCalculator`), `grand-austria-hotel` |
| Additional pre/post steps per round | `grand-austria-hotel` (`RoundStart`, `RoundEnd`), `galactic-cruise` (`TurnPlayerAdvanceShips`, `TurnBotAdvanceShips`, `EndOfRound`), `clans-of-caledonia` (`RoundPreparation`, `RoundProduction`, `RoundScoring`) |
| Fixed phases per round | `millennia` (`PhaseADrafting` … `PhaseGUpkeep`) |
| Multiple selectable AI opponents | `maracaibo` (`views/jacques/`, `views/jean/`) |

Then implement in this order, always supporting **both player turns and bot turns**:

1. **State and navigation**: `Turn`/`Round` + `BotPersistence` interfaces and `storeTurn`/`storeRound`/`storeRoundTurn` in `state.ts`; routes; `NavigationState` restoring bot persistence from the previous turn (or the initial setup) and executing the deterministic bot step (e.g. drawing a card); `RouteCalculator` if next/back is non-trivial. Unit tests for `NavigationState` simulating several turns with `mockState`/`mockTurn`.
2. **Player turn view** (`TurnPlayer`/`RoundTurnPlayer`): only the inputs the plan assigns to the player (passing, resources paid to the bot, ...), "Next"/"Pass" buttons storing the turn and routing on.
3. **Bot turn view** (`TurnBot`/`RoundTurnBot`): `services/BotActions.ts` (deterministic, unit tested) resolves everything the plan assigns to the app (decisions, resource/VP changes) and updates the tracked bot state → `BotAction.vue` dispatching to `action/Action<Name>.vue` per action → `ActionBox.vue` with icons, the already resolved result, and rules help in `ModalDialog` (`rules.action.<action>.*` i18n keys). Ask only for the board-dependent input defined in the plan. For "if not possible, do the next action" rules use `.../bot/action/:action` routes with "Executed"/"Not Possible" buttons (`seti`, `south-tigris-scholars`). Respect the bot's shortcuts and skipped phases.
4. **`SideBar`** with the contents from the plan (round/turn/phase, tracked bot state that replaces the solo board, deck information and the preserved hints of the physical solo mode).
5. **Back navigation** for every view (`backButtonRouteTo`), round/phase transitions, pre/post round steps, game end detection.
6. **`DebugInfo`** showing the relevant navigation state/bot persistence, incl. the card identifiers of current card and deck.
7. Implement **action by action** and rule by rule; add i18n keys (en + de) as screens are added - rules texts 1:1 from the matching passages in `<resources>/rules/*-en.md`/`*-de.md` where short, otherwise own wording aligned with the rulebook terms; extend the smoke test to play at least one round/several turns.

### 5c. End Game Scoring

Default (all apps except Karma Games) - a **simple final scoring screen**:
- `GameEnd.vue`/`EndOfGame.vue` with `components/scoring/FinalScoring.vue`: table with **one column for the player and one for the bot** and **one row per scoring category** of the base game's end game scoring (plus end-game VP from other sources, e.g. special tiles) - the player's VP are always entered per category via `NumberInput` (never just a total), the bot's values tracked by the app are pre-filled/calculated, only the rest is entered - VP computed per the solo rules, totals for both, plus difficulty level display; `FooterButtons endGameButtonType="endGame"`. See `seti`, `south-tigris-scholars` for the UI - but put non-trivial VP formulas into `util/getXxxVP.ts` with unit tests (as in `south-tigris-wayfarers` `getCardVP.ts`) instead of inline in the component.
- Optionally a separate `EndOfGameAmounts.vue` + `FinalAmounts.vue` step if many values must be entered first (`grand-austria-hotel`).

## Step 6: Game Statistics (Karma Games only)

Only for games published by **Karma Games** (`clans-of-caledonia`, `millennia`, `thiefdom`). Skip for all other publishers.

- Two-step end: `EndOfGameAmounts.vue` (enter amounts, stored in `state.finalScoringAmount`) → `EndOfGame.vue` with `FinalScoring.vue`.
- In `FinalScoring.vue` `mounted()`: if `!state.gameStatsSend`, build a flat stats object (`version`, difficulty/mode, player and bot VP per category, per-round/turn statistics) and call `postGameStats(stats, import.meta.env.VITE_STATS_FORM_URL, import.meta.env.VITE_STATS_FIELD_MAPPING)`, then set `state.gameStatsSend = true`. `resetGame()` resets `gameStatsSend`.
- Per-turn stats recorded while playing (optional fields on the turn, small helpers in `util/`) with unit tests.
- Workflows `deploy.yml` and `release.yml` need the `stats-forms-url`/`stats-field-mapping` inputs (copy from `clans-of-caledonia`); the Google Form and repo variables `VITE_STATS_FORM_URL`/`VITE_STATS_FIELD_MAPPING` are set up manually by the user - list the stats field names for the form.

## Finalize and Publish

1. Full validation: `npm run lint`, `npm run test:unit run`, `npm run build`, `npm run test:e2e`; play a complete game in `npm run dev` (back button, reload in the middle of a game, end of game, zoom, language switch, debug mode).
2. Check `en.json`/`de.json` completeness and wording against the EN/DE rulebooks (`<resources>/rules/`, `glossary.md`), remove `TODO`s and unused keys/icons/dependencies (e.g. `nanoid` if copied from a reference app).
3. Check against the confirmed plan (`<resources>/app-plan.md`): everything the plan assigns to the app is automated, all preserved hints and sidebar contents are present, every solo card is defined with its identifier, the solo cards and the solo board are superfluous except the parts documented as still needed (and named in the bot setup instructions). Update the implementation status and record deviations in the plan. Ask the user again about all `open` entries in `clarifications.md`.
4. Make sure the app repo contains no rulebook PDFs, scans or transcriptions, and nothing in the app (code, tests, build) references `brdgm-resources`.
5. Review the code against `vue-components.instructions.md` and `typescript.instructions.md` (no `eslint-disable` for emits, no `any`/`!`, no DOM access, `v-model` via computed, scoring formulas tested). Optionally run a type check with `npx -p typescript@5.9 -p vue-tsc vue-tsc --noEmit` (current `vue-tsc` cannot load TypeScript 6 yet).
6. List the manual steps for the user:
   - Repo `brdgm/<appDeployName>-solo-helper` (default branch `develop`, `master` for releases), initial PR "Solo Helper App", secrets (`SONARCLOUD_TOKEN`, `GH_SITE_DEPLOY_*`), `Production` environment, SonarCloud project `brdgm_<appDeployName>-solo-helper`.
   - Release via "Release and Deploy" workflow (`1.0.0` for published games, `0.x.0` for prototypes).
   - `brdgm.github.io`: entry in `games-index.json` (`name`, `title`, `languages`, `addedAt`) and image `resources/images/games/<appDeployName>.webp`.
   - BGG thread → enable the feedback links on the home page.
