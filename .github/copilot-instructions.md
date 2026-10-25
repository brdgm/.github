# brdgm.me Solo Helper Applications - Copilot Instructions

## Architecture Overview

This workspace contains **board game solo helper applications** built with Vue 3 + TypeScript. Each `*-solo-helper` project is a PWA that replaces the physical solo/automa components (card decks, AI boards, dice, ...) of a board game and guides the player through the solo rules against an AI opponent (the "bot"). They are published at `https://brdgm.me/<appDeployName>/`.

### Key Components

- **brdgm-commons**: Shared library with components and utilities used by all apps (see [brdgm-commons Integration](#brdgm-commons-integration))
- **Solo Helper Projects** (`*-solo-helper`): One Vue 3 PWA per board game
- **brdgm.github.io**: Deployment target and game index website (`games-index.json`, `resources/images/games/<appDeployName>.webp`)
- **.github**: Central Copilot instructions, skills and release-drafter config. CI/CD logic lives in shared GitHub Actions (`brdgm/github-action-build`, `-deploy`, `-release`, `-test-e2e`, `-release-drafter`) and `brdgm/renovate-config`

## Reference Implementations (Important)

The apps were created over several years (2022 → today). **Implementation quality, structure and solution approaches improved significantly over time. The old apps are NOT good references.**

When looking for a template for a new feature, a pattern, or the skeleton of a new app:

1. **Always look at the latest implementations first.**
2. Only fall back to older apps if no similar feature exists in the latest ones - and then adapt the solution to the current patterns instead of copying it as-is.
3. Never introduce patterns found only in legacy apps into newer apps.
4. The rules in this file take precedence over existing code - even the preferred references contain a few deviations (e.g. `Object.values(Expansion)` in `ExpansionsSetup.vue` instead of `getAllEnumValues`). Do not copy such deviations into new code.

| Category | Apps (newest first) |
|----------|---------------------|
| ✅ **Preferred references** (2025–2026) | `bloomworks`, `south-tigris-scholars`, `south-tigris-inventors`, `south-tigris-wayfarers`, `galactic-cruise`, `maracaibo`, `seti`, `grand-austria-hotel` |
| ⚠️ Acceptable fallback (2024 – early 2025) | `clans-of-caledonia`, `thiefdom`, `millennia`, `civolution`, `barrage`, `age-of-innovation`, `apiary`, `el-burro`, `gaia-project`, `welcome-to-the-moon`, `fractal` |
| ❌ **Legacy - do not use as template** (2022–2023) | `dinogenics`, `carnegie`, `roll-for-the-galaxy`, `ultimate-railroads`, `praga-caput-regni`, `autobahn`, `weather-machine`, `skymines`, `joan-of-arc-orleans`, `terra-mystica`, `stroganov`, `ark-nova`, `rurik`, `monumental`, `blitzkrieg` |

The creation date of an app can be checked with `git log --reverse --format=%ad --date=short` (first line) in the app repository. Apps created after this list was written are even better references.

Typical signs of a legacy implementation: store id `${name}.store`, no `tests/unit/helper/` mock helpers, game logic implemented inside views, no `NavigationState`/`RouteCalculator`, view names like `RoundPlayer`/`RoundBot`.

### Where to Find Good Examples

| Need | Look at |
|------|---------|
| Minimal, clean app skeleton | `south-tigris-scholars`, `bloomworks` |
| Card deck with draw/discard/reshuffle and persistence | `CardDeck.ts` in `bloomworks`, `south-tigris-scholars`, `seti` |
| Bot action with "Executed" / "Not Possible" steps (`.../bot/action/:action` routes) | `seti` (`RoundTurnBot.vue`), `south-tigris-scholars` (`TurnBot.vue`) |
| Complex turn order, passing, `RouteCalculator` | `seti` (`RouteCalculator.ts`, `getTurnOrder.ts`), `grand-austria-hotel` |
| Rounds + turns, season/round start screens | `bloomworks` (`RoundStart.vue`, `RoundTurnPlayer.vue`, `RoundTurnBot.vue`) |
| Several aggregated bot state objects | `bloomworks` (`BotPersistenceWrapper.ts`) |
| Multiple selectable bot variants in one app | `maracaibo` (`jacques/`, `jean/` subfolders) |
| Action display with rules help modal | `ActionBox.vue` + `components/*/action/Action*.vue` in `south-tigris-scholars`, `seti` |
| Difficulty level slider, expansion toggles | `components/setup/DifficultyLevel.vue`, `ExpansionsSetup.vue` in `seti` |
| Final scoring table, end-of-game amount entry, anonymous game stats | `bloomworks` (`EndOfGameAmounts.vue`, `FinalScoring.vue`), `thiefdom`, `millennia` |
| Rules / FAQ modals | `galactic-cruise` (`components/rules/`) |
| Bot status side bar, editable values via modal + `NumberInput` | `bloomworks` (`SideBar.vue`) |

## Consistency Across Apps

- New apps should **look and behave like the existing (latest) apps**: same skeleton, same screen flow (home → setup → turns → end of game), same header/footer, same button styles, same footer buttons, same credits modal, same i18n keys for shared texts.
- Reuse the same patterns where appropriate. If a different pattern or a new UI element fits the game's use case clearly better, it may be introduced - keep it consistent with the overall look & feel.
- **Reuse as much as possible from brdgm-commons**. If a generic utility/component is needed that does not exist yet, consider adding it to brdgm-commons instead of the app.
- To create a new app, use the `create-solo-helper-app` skill (`.github/skills/create-solo-helper-app/SKILL.md`).

## Project Structure

Structure of the latest apps (subfolder names of `components/` vary slightly: `round/` or `turn/`):

```
src/
├── App.vue                 # AppHeader, AppFooter, router-view, error/PWA-update/credits modals
├── main.ts                 # createApp + Pinia (persistedstate) + router + i18n + bootstrap
├── i18n.ts                 # vue-i18n (legacy: false), messages from @intlify/unplugin-vue-i18n
├── router/index.ts         # Routes + createRouterMatomoTracking from brdgm-commons
├── store/state.ts          # Pinia store + all persistence interfaces
├── services/               # Game logic (framework-free, unit tested)
│   ├── enum/               # Game constants as TypeScript enums (one enum per file, default export)
│   ├── Card.ts             # Card interface (+ CardAction)
│   ├── Cards.ts            # Static card list, get(id) / getAll()
│   ├── CardDeck.ts         # Card deck with new() / fromPersistence() / toPersistence()
│   ├── BotActions.ts       # Bot logic for current card/turn
│   └── RouteCalculator.ts  # Next/back routes (when turn order is non-trivial)
├── util/                   # NavigationState.ts + small single-function helpers (getXxx.ts)
├── views/                  # Route components
├── components/
│   ├── structure/          # AppIcon, FooterButtons wrapper, shared display components
│   ├── setup/              # DifficultyLevel, ExpansionsSetup, other setup options
│   ├── round/ or turn/     # SideBar, DebugInfo, BotAction, ActionBox, action/Action*.vue
│   └── scoring/            # FinalScoring, FinalAmounts
├── assets/                 # game-<name>.webp, kofi_button_dark.png, icons/<type>/<name>.webp
└── locales/                # en.json (master) + translations
tests/
├── unit/                   # Mirrors src/ (services/, util/), helper/ with mockXxx functions
└── e2e/smoke-test.spec.ts  # Playwright smoke test playing through a short game
```

Typical views: `AppHome`, `SetupApp`/`SetupGame` (options like difficulty, expansions), `SetupBot`/`SetupGameBoard` (setup instructions), `TurnPlayer`/`TurnBot` or `RoundTurnPlayer`/`RoundTurnBot`, optional `RoundStart`/`RoundEnd`, `EndOfGameAmounts` + `EndOfGame`/`GameEnd`, `NotFound`.

## Development Workflows

```bash
npm install
npm run dev                  # Vite dev server on port 8080
npm run build                # Production build (dist/)
npm run test:unit run        # Vitest unit tests (single run)
npm run test:coverage        # Unit tests with coverage
npm run test:e2e             # Playwright e2e tests
npm run lint                 # ESLint with --fix (also validates locale JSON files against en.json)
npm run generate-pwa-assets  # Generate PWA icons from public/img/icons/app-icon.png
```

### Key Dependencies
- **Vue 3** + **TypeScript** (strict) + **Vite**
- **Pinia** with `pinia-plugin-persistedstate`
- **Vue Router** (hash history) via brdgm-commons
- **Bootstrap 5** (+ `@popperjs/core`), **Vue I18n**, **Vite PWA**, **lodash** (e.g. `shuffle`, `cloneDeep`), **nanoid** (unique modal IDs)
- Vitest + chai + jsdom for unit tests, Playwright for e2e tests

### Branching, Build & Deployment
- Default branch `develop`; `master` holds released versions. Features are developed in branches and merged via PR.
- Each project has `appDeployName` in `package.json`; Vite base path is `/${appDeployName}/`.
- Workflows in `.github/workflows/` (`build.yml`, `test-e2e.yml`, `deploy.yml`, `release.yml`, `release-drafter.yml`) only delegate to the shared `brdgm/github-action-*` actions - copy them unchanged from the latest app.
- A `languages.json` is generated at build time from `src/locales/` for the brdgm.github.io game index.

## Critical Patterns

### State Management (`store/state.ts`)
- `export const useStateStore = defineStore(\`${name}.state\`, { ..., persist: true })` with `name` from `package.json` (legacy apps use `.store` - do not copy).
- State always contains `language`, `baseFontSize`, `setup` (game options, incl. `debugMode?`) and the game progression (`turns: Turn[]` or `rounds: Round[]` with nested turns).
- Actions: `resetGame()`, `storeTurn(turn)` / `storeRound(round)` / `storeRoundTurn(turn)`. Storing a turn **removes all later turns** (`filter(item => item.turn < turn.turn)`) so going back and changing a decision recalculates the future.
- All persistence interfaces (`BotPersistence`, `CardDeckPersistence`, ...) are defined and exported in `state.ts`. Persist only plain data and **IDs** (e.g. card IDs), never class instances.

### Navigation & Routing
- Router: `createRouterMatomoTracking(routes, \`${name}.route\`, appDeployName, version, 'AppHome')` - hash history, last route restored from localStorage, Matomo page tracking. Always include a catch-all `NotFound` route.
- Route params carry the game position, e.g. `/turn/:turn/player`, `/round/:round/turn/:turn/bot`, `/turn/:turn/bot/action/:action`.
- `App.vue` renders `<router-view :key="$route.fullPath"/>`, so each view is re-created on every navigation.
- **`util/NavigationState.ts`**: Constructed in each view's `setup()` via `new NavigationState(route, state)`. Reads route params with `getIntRouteParam`, restores bot state from the persisted previous turn (or initial setup), and executes the deterministic bot step (e.g. drawing the next card). Views never keep game progression in local state.
- On "Next": build the turn object (incl. `xxx.toPersistence()`), call `state.storeTurn(...)`, then `router.push(nextRoute)`. "Back" just navigates to the previous route - state is re-derived from the store.
- Use `services/RouteCalculator.ts` when next/back routes depend on turn order or passing.

### Game Services
- **Enums**: one enum per file in `services/enum/`, string values in kebab-case (`WINDOW_BOX = 'window-box'`) - they are reused as i18n keys, icon file names and component name suffixes. Numeric enums for levels (`DifficultyLevel.LEVEL_1 = 1`).
- **Cards**: `Card.ts` interface, `Cards.ts` with a static card array, a `Map` and `get(id)` using `findMandatory` + `getAll(...)`.
- **Stateful services** (`CardDeck`, other bot state): private constructor, internal Vue `ref()`s, getters returning `readonly` data, `static new(...)` (fresh/shuffled), `static fromPersistence(p)` and `toPersistence()`.
- **BotActions**: Derives the bot actions for the current turn deterministically from navigation state/card; no UI code.
- **Difficulty levels**: `util/getDifficultyLevelSettings.ts` maps each level to a settings object (`switch` + `throw` on invalid level).
- Small pure helpers go into `util/getXxx.ts` (one default-exported function per file, each with unit tests).
- Throw `TranslatableError` (brdgm-commons) for errors that should be shown translated to the user; `App.vue` shows captured errors in a modal.

### UI Patterns
- `components/structure/FooterButtons.vue`: app wrapper around commons `FooterButtons` with props `backButtonRouteTo` and `endGameButtonType` (`abortGame` during a game, `endGame` on the final screen); calls `state.resetGame()` and routes home.
- `components/structure/AppIcon.vue`: `<AppIcon type="action" :name="action.action"/>` → `src/assets/icons/<type>/<name>.webp`. Use `.webp` for images.
- `BotAction.vue` renders `<component :is="\`action-${action.action}\`">` dispatching to one `action/ActionXxx.vue` per action enum value; each wraps `ActionBox.vue`, which shows the action icons and opens a `ModalDialog` with the rules text (`#instruction` slot, modal ID via `nanoid`).
- `SideBar.vue` (floating right) shows round/turn and bot status; `DebugInfo.vue` dumps navigation state when `state.setup.debugMode` is enabled (checkbox in the credits modal).
- Primary flow buttons: `btn btn-primary btn-lg`; "Executed" `btn-success`, "Not Possible" `btn-danger`. Headings `h1` per view, `h3 class="mt-4 mb-3"` for setup sections.
- Prefer Bootstrap utility classes; scoped SCSS only for game-specific layout.

### Internationalization
- `src/locales/en.json` is master; German (`de.json`) in most apps, other languages are community-contributed.
- Detailed conventions: `.github/instructions/i18n.instructions.md`.

### Game Statistics (optional)
- Anonymous end-of-game statistics via `postGameStats(data, import.meta.env.VITE_STATS_FORM_URL, import.meta.env.VITE_STATS_FIELD_MAPPING)` in `FinalScoring.vue` `mounted()`, guarded by `state.gameStatsSend` (see `bloomworks`, `thiefdom`, `millennia`).

## brdgm-commons Integration

**Always use brdgm-commons** instead of duplicating functionality. Import directly from source: `@brdgm/brdgm-commons/src/...`. Use the latest released version of `@brdgm/brdgm-commons` (see `version` in `brdgm-commons/package.json`) for new apps.

### Components

| Import (`@brdgm/brdgm-commons/src/...`) | Purpose |
|-----------------------------------------|---------|
| `components/structure/AppHeader.vue` | Fixed header with brdgm.me logo, game title, language selector (emits `setLocale`) |
| `components/structure/AppFooter.vue` | Fixed footer with credits link, version, zoom buttons (emits `zoomFontSize`) |
| `components/structure/FooterButtons.vue` | Back button + end/abort game button with confirm modal (wrap it in the app's own `FooterButtons.vue`) |
| `components/structure/ModalDialog.vue` | Bootstrap modal |
| `components/form/NumberInput.vue` | Numeric input |

### Bootstrap Modals
Always use `ModalDialog` when a modal is needed - never write custom modal markup:

```vue
<ModalDialog id="myModal" :title="t('myModal.title')">
  <template #body>
    <p v-html="t('myModal.content')"/>
  </template>
</ModalDialog>
```

Props: `id` (required), `title`, `centered` (default `true`), `scrollable`, `sizeSm`/`sizeLg`/`sizeXl`, `fullscreen`/`fullscreenSmDown`/.../`fullscreenXxlDown`, `closeI18nKey` (default `action.close`). Slots: `header`, `body`, `footer`. Open via `data-bs-toggle="modal" data-bs-target="#myModal"` or programmatically with `showModal`.

### Number Inputs
Always use `NumberInput` - never a plain `<input type="number">`:

```vue
<NumberInput v-model="score" :min="0" :max="100"/>
```

Props: `min` (default `0`), `max` (default `9999`). Supports `v-model` (value may be `undefined` → use `toNumber`) and sum expressions (e.g. `1 + 2 - 3`).

### Utilities

| Import (`@brdgm/brdgm-commons/src/util/...`) | Purpose |
|----------------------------------------------|---------|
| `array/findMandatory` | `findMandatory(array, predicate)` - find item or throw |
| `map/findMandatory` | `findMandatory(map, key)` - get item or throw |
| `array/toggleArrayItem` | Add item if missing, otherwise remove it |
| `enum/getAllEnumValues` | All values of a string or number enum |
| `enum/getPrioritizedEnumValues` | All enum values, starting with the given value (keeps cyclic order) |
| `random/randomEnum`, `randomEnumDifferentValue`, `randomEnumMultiDifferentValue` | Random enum value(s), optionally excluding values / distinct |
| `random/rollDice`, `rollDiceDifferentValue`, `rollDiceMultiDifferentValue` | Roll die (1..sides), optionally excluding values / distinct |
| `form/toNumber` | Convert optional form value to number (`undefined` → `0`) |
| `modal/showModal` | `showModal(id)`, `showModalIfExist(id)`, `showModalPreselectTab(modalId, tabId)` |
| `tab/enableTabLinksInContent` | Make `<a href="#tab-id" data-custom-toggle="tab">` links switch Bootstrap tabs |
| `router/createRouterMatomoTracking` | Router with route persistence + Matomo tracking |
| `router/getIntRouteParam` | Read numeric route param (`0` if missing) |
| `error/TranslatableError`, `error/getErrorMessage` | Errors with i18n key + params, message resolution |
| `serviceWorker/onRegisteredSWCheckForUpdate` | Periodic PWA update check (used in `App.vue`) |
| `stats/postGameStats` | Post anonymous game stats to a Google Form |

Rules:
- Never use `Object.values()` or manual lists to enumerate enums - use `getAllEnumValues` / `getPrioritizedEnumValues`.
- Never use `Math.random()` directly for enum values or dice - use the random helpers. Use lodash `shuffle` for shuffling decks.
- Never use `array.find(...)!` or `map.get(...)!` for items that must exist - use `findMandatory`.

## Testing Strategy

- **Unit tests**: Vitest (globals enabled - `describe`/`it` without import) for everything in `services/` and `util/`, including `NavigationState`. Vue components are usually not unit tested.
- Tests mirror `src/` in `tests/unit/` (e.g. `tests/unit/services/CardDeck.spec.ts` with `describe('services/CardDeck', ...)`).
- **Assertions**: `chai` (`import { expect } from 'chai'`, e.g. `expect(result).to.eq(expected)`, `.to.eql(...)` for deep equality).
- **Mock helpers**: Reusable `mockXxx(params?)` functions in `tests/unit/helper/` (`mockState`, `mockTurn`/`mockRound`, `mockRouteLocation`, `mockCardDeck`, `mockBotPersistence`, ...), each with an optional `MockXxxParams` interface and sensible defaults. Always check this folder first and reuse/extend existing helpers instead of creating local helper functions in test files.
- Use fixed card IDs via `CardDeck.fromPersistence(...)` / mock helpers to make tests deterministic.
- **E2E**: `tests/e2e/smoke-test.spec.ts` plays through setup and at least one turn/round and aborts the game; keep it working when changing the flow.
- **Coverage**: Istanbul (lcov), analyzed by SonarCloud.

## Code Style

- **No semicolons** at line ends in TypeScript/JavaScript (ESLint rule `'semi': ['error', 'never']`).
- **Single quotes** for strings and imports in TypeScript/JavaScript (convention, not enforced by ESLint). Template literals for interpolation.
- **Vue 3 Options API** with `<script lang="ts">` and `defineComponent` (`name`, `components`, `props`, `emits`, `data`, `computed`, `methods`). `useI18n()`, `useStateStore()`, `useRoute()`/`useRouter()` are called in `setup()` and returned. Do **not** use `<script setup>`.
- Typed props: `type: Object as PropType<CardAction>`, class props like `type: NavigationState`.
- Explicit return types on computed properties and methods (`backButtonRouteTo() : string`).
- Imports via `@/` alias; one default export per file; JSDoc comments on services and non-trivial functions.
- TypeScript strict mode; prefer immutable/functional logic in services (`readonly` getters, `toSorted`, `map`/`filter`/`reduce`).
- 2-space indentation, UTF-8, final newline (`.editorconfig`).

## Common Tasks

- **New app**: Use the `create-solo-helper-app` skill.
- **New game feature**: Find the closest feature in the preferred reference apps → add enums/services/utils with unit tests → extend `state.ts` persistence → adapt `NavigationState` → add/extend views and components → add `en.json` (and `de.json` if present) keys.
- **Bot behavior**: Implement deterministically in `services/BotActions.ts` (or dedicated services), driven by `NavigationState`; cover with unit tests.
- **Translations**: New locale = new JSON file in `src/locales/` with identical keys to `en.json` (lint validates keys and placeholders).
- **PWA icons**: Replace `public/img/icons/app-icon.png`, run `npm run generate-pwa-assets`.
