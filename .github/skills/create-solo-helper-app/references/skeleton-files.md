# Skeleton Files of a Solo Helper App

Inventory of the files of a new app, based on the latest apps (`bloomworks`, `south-tigris-scholars`, `seti`). `<x>` = `appDeployName` (e.g. `bloomworks`), repo = `<x>-solo-helper`.

Get the file list of the reference app with `git -C <reference-app> ls-files`.

## A. Copy Unchanged (from the reference app)

| File | Notes |
|------|-------|
| `.browserslistrc`, `.editorconfig`, `.gitattributes`, `.gitignore`, `LICENSE` | |
| `.vscode/settings.json` | i18n-ally locales path |
| `.github/renovate.json` | extends `github>brdgm/renovate-config` |
| `.github/workflows/build.yml`, `deploy.yml`, `release.yml`, `release-drafter.yml`, `test-e2e.yml` | delegate to shared `brdgm/github-action-*`; keep the `stats-*` inputs |
| `babel.config.js`, `eslint.config.js`, `tsconfig.json`, `playwright.config.ts`, `pwa-assets.config.ts`, `vite.config.ts`, `vitest.config.ts` | `vite.config.ts` reads `description`/`appDeployName` from package.json and generates `languages.json` |
| `tests/e2e/tsconfig.json` | |
| `src/main.ts`, `src/i18n.ts`, `src/shims-vue.d.ts` | |
| `src/views/NotFound.vue` | |
| `src/components/structure/AppIcon.vue` | |
| `src/components/structure/FooterButtons.vue` | wrapper around commons `FooterButtons` |
| `src/assets/kofi_button_dark.png`, `src/assets/icons/help-semi-transparent.webp` | |
| `tests/unit/helper/mockRouteLocation.ts` | |

## B. Copy and Adapt Identity

| File | What to change |
|------|----------------|
| `package.json` | `name: "@brdgm/<x>-solo-helper"`, `version` (`1.0.0` published game / `0.x.0` prototype), `description: "<Game> Solo Helper"`, `appDeployName: "<x>"`. Keep scripts and dependencies (use latest `@brdgm/brdgm-commons` version; drop deps that are not used, e.g. `nanoid` if no `ActionBox` modal). Delete copied `package-lock.json` and run `npm install`. |
| `index.html` | `<title>` and `<meta name="description">` = `<Game> Solo Helper`. Keep Matomo snippet unchanged. |
| `README.md` | Title, badge URLs (`brdgm/<x>-solo-helper`, `brdgm_<x>-solo-helper`), `https://brdgm.me/<x>/`, locales link |
| `sonar-project.properties` | `sonar.projectKey=brdgm_<x>-solo-helper` |
| `src/App.vue` | Only the credits modal: BGG link, Game design, Artist, Publisher, GitHub release/source links. Everything else stays identical. |
| `src/views/AppHome.vue` | Game image `@/assets/game-<x>.webp` + BGG link, `home.play*` paragraphs, feedback links (BGG thread + GitHub; comment out until thread exists), disclaimer (with permission: see `bloomworks`; unofficial: see `south-tigris-scholars`), prototype alert only for unpublished games. Router link to first setup route. |
| `src/locales/en.json` | Keep shared keys, replace game-specific ones (see i18n instructions) |
| `tests/e2e/smoke-test.spec.ts` | Home `h1` text and the game flow |
| `public/img/icons/app-icon.png` (+ generated icons), `public/favicon.ico`, `public/img/icons/favicon.svg` | New app icon; run `npm run generate-pwa-assets` |

## C. Create Game-Specific Code (follow reference patterns)

| File | Pattern source |
|------|----------------|
| `src/router/index.ts` | Same structure; routes for the game flow + `NotFound` catch-all; `createRouterMatomoTracking(routes, LOCALSTORAGE_KEY, appDeployName, version, 'AppHome')` |
| `src/store/state.ts` | `defineStore(\`${name}.state\`)`, `language`, `baseFontSize`, `setup` (incl. `difficultyLevel`, `expansions`, `debugMode?`), `turns`/`rounds`, `resetGame()`, `storeTurn()`/`storeRound()` truncating later entries, `persist: true`, persistence interfaces |
| `src/util/NavigationState.ts` | Route params via `getIntRouteParam`, restore bot persistence from last stored turn or initial setup, draw/compute bot step |
| `src/util/getDifficultyLevelSettings.ts` | `switch` per level, `throw` on invalid |
| `src/services/enum/*.ts` | One enum per file, default export, JSDoc comment |
| `src/services/Card.ts`, `Cards.ts`, `CardDeck.ts` | `Cards.get(id)` with `findMandatory`; `CardDeck` with private constructor, `ref`s, `new()`, `fromPersistence()`, `toPersistence()`, lodash `shuffle` |
| `src/services/BotActions.ts` | Deterministic bot logic per turn |
| `src/services/RouteCalculator.ts` | Only if next/back routes are non-trivial (`seti`) |
| `src/views/SetupApp.vue` / `SetupGame.vue` | Setup option components, button to next setup step, `FooterButtons endGameButtonType="abortGame"` |
| `src/views/SetupBot.vue` | Setup instructions list (`setupBot.instructions.*`), rule changes box (`alert alert-info`), "Start Game" initializes bot persistence and stores first turn/round |
| `src/views/TurnPlayer.vue`, `TurnBot.vue` (or `RoundTurnPlayer`/`RoundTurnBot`) | `NavigationState` in `setup()`, store turn + `router.push` on next, `backButtonRouteTo`, `DebugInfo`, `FooterButtons` |
| `src/views/EndOfGameAmounts.vue`, `EndOfGame.vue` / `GameEnd.vue` | Score entry with `NumberInput`, `FinalScoring` table, optional `postGameStats` |
| `src/components/setup/DifficultyLevel.vue`, `ExpansionsSetup.vue` | From `seti` / `south-tigris-scholars` (use `getAllEnumValues`) |
| `src/components/turn/` (or `round/`): `SideBar.vue`, `DebugInfo.vue`, `BotAction.vue`, `ActionBox.vue`, `action/Action*.vue` | From `south-tigris-scholars` / `bloomworks` / `seti` |
| `src/components/scoring/FinalScoring.vue` (+ `FinalAmounts.vue`) | From `bloomworks` / `grand-austria-hotel` |
| `tests/unit/helper/mockState.ts`, `mockTurn.ts`/`mockRound.ts`, `mockCardDeck.ts`, `mockBotPersistence.ts` | Same `mockXxx(params?: MockXxxParams)` style |
| `tests/unit/services/*.spec.ts`, `tests/unit/util/*.spec.ts` | One spec per service/util, incl. `NavigationState.spec.ts` and `Cards.spec.ts` (`get(id)` and expected card counts of `getAll()`) |

## D. Do Not Copy

- Game-specific services, enums, components, icons, locale texts and test cases of the reference app.
- `resources/app-icon.psd` of another game (create an own icon source if needed).
- Any `TODO`/prototype markers that do not apply to the new game.
