---
name: create-solo-helper-app
description: 'Create a new brdgm.me solo helper app (Vue 3 + TypeScript PWA) for a new board game solo mode, in the same style as the existing *-solo-helper apps. Use when: scaffolding a new solo helper, starting a new brdgm app, implementing a new game automa/AI opponent app, setting up skeleton, routes, state, card deck, bot actions, setup and scoring screens for a new game.'
argument-hint: 'Game name (and optionally BoardGameGeek link / solo rules)'
---

# Create a New Solo Helper App

Creates a new `<game>-solo-helper` app that looks and behaves like the latest brdgm.me apps and reuses brdgm-commons as much as possible. Read `.github/copilot-instructions.md` first - all patterns and rules there apply.

## Golden Rules

- **Use the latest apps as template** - never the legacy ones (`blitzkrieg`, `monumental`, `ark-nova`, `rurik`, ... see "Reference Implementations" in `copilot-instructions.md`). Check creation dates with `git log --reverse --format=%ad --date=short` if unsure.
- The new app must look like the others: same skeleton, header/footer, home page, credits modal, footer buttons, screen flow, button styles and shared i18n keys.
- Deviate only where the game's solo mode clearly needs a different UI or pattern.
- Use brdgm-commons components/utilities instead of writing own code. If something generic is missing, propose adding it to brdgm-commons.

## Procedure

### 1. Gather Information

Ask the user (use the ask-questions tool) for everything that is not provided:

| Item | Used for |
|------|----------|
| Game title, BoardGameGeek URL | `gameTitle`, home page, credits |
| `appDeployName` (kebab-case, e.g. `south-tigris-scholars`) → repo `brdgm/<appDeployName>-solo-helper` | package.json, URLs, Sonar key |
| Game design, artist, publisher (+ URL) | Credits modal in `App.vue` |
| Permission status: official with publisher permission, or unofficial | Disclaimer on home page |
| Published game or prototype | Prototype alert on home page, version `0.x` vs `1.0.0` |
| **Solo mode rules** (PDF/text) | Everything - never invent rules |
| Name of the AI opponent (e.g. "AI" or automa name), difficulty levels, expansions | Setup screens, i18n |
| Languages besides `en` (e.g. `de`) | Locale files |
| Game box image, icons for actions/resources | Assets |

### 2. Choose the Reference App

Pick the **newest** app whose structure is closest to the new game (see the "Where to Find Good Examples" table in `copilot-instructions.md`):

- Simple alternating player/bot turns without rounds → `south-tigris-scholars` (`/turn/:turn/player|bot`)
- Rounds with several turns per round, round start screens → `bloomworks`, `seti`
- Non-trivial turn order / passing → `seti` (`RouteCalculator`, `getTurnOrder`)
- Multiple AI variants → `maracaibo`

Open the reference app and read its `state.ts`, `router/index.ts`, `NavigationState.ts`, the turn views and `services/` before writing code.

### 3. Model the Solo Mode

Before scaffolding, derive from the solo rules:

1. **Enums** (`services/enum/`): actions, card types, colors, difficulty level, expansions, player (`PLAYER = 'player'`, `BOT = 'bot'`), ... - kebab-case string values.
2. **Cards**: `Card` interface with `id` and `actions: CardAction[]`; full card list in `Cards.ts`.
3. **Bot state** that must survive navigation (card deck, resources, tracks, ...) → `BotPersistence` interfaces in `state.ts` (IDs/plain data only) and service classes with `new()` / `fromPersistence()` / `toPersistence()`.
4. **Turn structure** → routes and `Turn`/`Round` interfaces; what `NavigationState` has to compute per route.
5. **Difficulty settings** → `util/getDifficultyLevelSettings.ts`.
6. **Setup instructions** for the bot (`SetupBot` view) and rule changes.
7. **Final scoring** of the bot (and player) → `EndOfGameAmounts`/`FinalScoring` or `GameEnd`.

Present this model briefly to the user if the rules are ambiguous.

### 4. Scaffold the Project

Follow [skeleton-files.md](./references/skeleton-files.md): copy the unchanged infrastructure files from the reference app, adapt the identity files, and create the game-specific structure following the reference patterns. Remove all game-specific leftovers of the reference app.

Then:

```bash
npm install
```

### 5. Implement Game Logic (with Unit Tests)

- `services/` and `util/` first, each with unit tests in `tests/unit/` (mirroring `src/`), using chai and `tests/unit/helper/mockXxx.ts` helpers (`mockState`, `mockTurn`/`mockRound`, `mockRouteLocation`, `mockCardDeck`, `mockBotPersistence`).
- `util/NavigationState.ts` + `tests/unit/util/NavigationState.spec.ts` (simulate several turns via `mockState({turns:[...]})`).
- Use `findMandatory`, `getAllEnumValues`, `randomEnum`, `rollDice`, lodash `shuffle` - no `Math.random()`, no `Object.values()` on enums, no non-null assertions for mandatory lookups.

### 6. Implement Views and Components

Standard flow (adapt names/steps to the game):

```
AppHome → SetupApp/SetupGame → SetupBot (instructions) → TurnPlayer ⇄ TurnBot (… RoundStart/RoundEnd) → EndOfGameAmounts → EndOfGame
```

- Each view: `SideBar` (if useful), `h1`, content, primary button(s), `DebugInfo`, `FooterButtons` (`backButtonRouteTo`, `endGameButtonType="abortGame"`; `endGame` on the final screen).
- Bot actions: `BotAction.vue` → `action/Action<Name>.vue` per action enum value → `ActionBox.vue` with rules help in `ModalDialog`.
- Setup options: `components/setup/DifficultyLevel.vue`, `ExpansionsSetup.vue` (with `getAllEnumValues`).
- Use `ModalDialog`, `NumberInput`, `AppIcon`; Bootstrap classes; Options API with `<script lang="ts">`.

### 7. Translations

- Start `en.json` from the reference app: keep shared keys (`gameTitle`, `home`, `action`, `footer`, `serviceWorkerUpdatedRefresh`, `notfound`, `difficultyLevel`, ...), replace game-specific ones.
- Follow `.github/instructions/i18n.instructions.md`. Rules texts go into `rules.*` and should be close to the official solo rules wording.
- Add `de.json` (or other languages requested) with identical keys.

### 8. Assets

- `src/assets/game-<appDeployName>.webp` (box image, linked to BGG on the home page).
- Icons as `.webp` in `src/assets/icons/<type>/<name>.webp`, where `<name>` matches the enum value.
- Copy `src/assets/kofi_button_dark.png` and `src/assets/icons/help-semi-transparent.webp` from the reference app.
- App icon `public/img/icons/app-icon.png` (square, 512px+), then `npm run generate-pwa-assets`. Also provide `public/favicon.ico` and `public/img/icons/favicon.svg` (referenced by `index.html`).
- If image assets are not available yet, ask the user; use clearly marked placeholders only temporarily.

### 9. E2E Smoke Test

Adapt `tests/e2e/smoke-test.spec.ts`: check the home `h1`, go through setup, play at least one player and bot turn, abort the game via `#endGameModal`, verify return to home.

### 10. Validate

Run and fix until all pass:

```bash
npm run lint
npm run test:unit run
npm run build
npm run test:e2e
```

Start `npm run dev` and check the app in the browser (setup → several turns → back button → end of game, zoom, language switch, debug mode).

### 11. Publishing Checklist (manual steps - list them for the user)

- GitHub repo `brdgm/<appDeployName>-solo-helper`: initial commit (LICENSE Apache-2.0, README, `.gitignore`, `.gitattributes`) on default branch `develop`, app code via PR "Solo Helper App"; `master` branch for releases.
- Repo secrets/vars as in other brdgm repos (`SONARCLOUD_TOKEN`, `GH_SITE_DEPLOY_*`, optional `VITE_STATS_FORM_URL`/`VITE_STATS_FIELD_MAPPING` for game stats) and `Production` environment.
- SonarCloud project `brdgm_<appDeployName>-solo-helper`.
- Release via the "Release and Deploy" workflow (`1.0.0` for published games).
- `brdgm.github.io`: add entry to `games-index.json` (`name`, `title`, `languages`, `addedAt`) and image `resources/images/games/<appDeployName>.webp`.
- After publishing: create BGG thread and add the link to the home page `feedback` paragraph.
