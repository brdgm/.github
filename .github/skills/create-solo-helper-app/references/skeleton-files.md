# Step 1: Skeleton Files

How to create the skeleton from a recent reference app (`bloomworks`, `south-tigris-scholars`, `seti`, ...). `<x>` = `appDeployName` (e.g. `bloomworks`), repo folder = `<x>-solo-helper`.

Get the file list of the reference app with `git -C <reference-app> ls-files`. The rulebooks, transcriptions and the plan are in `brdgm-resources/apps/<x>-solo-helper/` - never copy them into the app repo.

## A. Copy Unchanged

| File | Notes |
|------|-------|
| `.browserslistrc`, `.editorconfig`, `.gitattributes`, `.gitignore`, `LICENSE` | |
| `.vscode/settings.json` | i18n-ally locales path |
| `.github/renovate.json` | extends `github>brdgm/renovate-config` |
| `.github/workflows/build.yml`, `release-drafter.yml`, `test-e2e.yml` | delegate to shared `brdgm/github-action-*` |
| `.github/workflows/deploy.yml`, `release.yml` | Copy from a **non-Karma** app (e.g. `seti`) - without `stats-forms-url`/`stats-field-mapping` inputs. Those are only added in step 6 for Karma Games apps. |
| `babel.config.js`, `tsconfig.json`, `playwright.config.ts`, `pwa-assets.config.ts`, `vite.config.ts`, `vitest.config.ts` | `vite.config.ts` reads `description`/`appDeployName` from `package.json` and generates `languages.json` |
| `eslint.config.js` | Copy, then extend the `rules` block with `'@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }]` so typed emit validators need no `eslint-disable` comments |
| `tests/e2e/tsconfig.json` | |
| `src/main.ts`, `src/i18n.ts`, `src/shims-vue.d.ts` | |
| `src/views/NotFound.vue` | |
| `src/components/structure/FooterButtons.vue` | wrapper around commons `FooterButtons` |
| `src/components/structure/AppIcon.vue` | adjust `extension` default (`svg`/`webp`) in step 2 |
| `src/assets/kofi_button_dark.png` | |
| `tests/unit/helper/mockRouteLocation.ts` | |

## B. Copy and Adapt Identity

| File | What to change |
|------|----------------|
| `package.json` | `name: "@brdgm/<x>-solo-helper"`, `version` (`1.0.0` published game / `0.1.0` prototype), `description: "<Game> Solo Helper"`, `appDeployName: "<x>"`. Keep scripts and dependencies (without `nanoid` - use Vue's `useId()`), latest `@brdgm/brdgm-commons` version. Do not copy `package-lock.json` - run `npm install`. |
| `index.html` | `<title>` and `<meta name="description">` = `<Game> Solo Helper`. Matomo snippet unchanged. |
| `README.md` | Title, badge URLs (`brdgm/<x>-solo-helper`, `brdgm_<x>-solo-helper`), `https://brdgm.me/<x>/`, locales link |
| `sonar-project.properties` | `sonar.projectKey=brdgm_<x>-solo-helper` |
| `src/App.vue` | Only the credits modal: BGG link, Game design, Artist, Publisher (+ URL), GitHub release/source links with `<x>-solo-helper`. Everything else stays identical. |
| `src/views/AppHome.vue` | Game image `@/assets/game-<x>.webp` + BGG link, `home.play*` paragraphs, feedback paragraph (BGG thread + GitHub; commented out until the thread exists), disclaimer (with publisher permission: see `bloomworks`; unofficial: see `south-tigris-scholars`), prototype alert only for unpublished games, router link to the setup route. Remove styles not used. |
| `public/img/icons/app-icon.png` (+ `resources/app-icon.psd`), `public/favicon.ico`, `public/img/icons/favicon.svg` | New app icon, then `npm run generate-pwa-assets` |
| `src/assets/game-<x>.webp` | Game box image (~800 px) |

## C. Create Minimal Stubs

| File | Content in step 1 |
|------|-------------------|
| `src/router/index.ts` | `AppHome` (`/`), setup route (`/setup` → `SetupApp` or `/setupGame` → `SetupGame`), `NotFound` catch-all; `createRouterMatomoTracking(routes, LOCALSTORAGE_KEY, appDeployName, version, 'AppHome')` |
| `src/views/SetupApp.vue` / `SetupGame.vue` | `h1` with `setup.title`, placeholder content, primary button to the next setup step, `FooterButtons endGameButtonType="abortGame"` |
| `src/store/state.ts` | `defineStore(\`${name}.state\`)` with `language`, `baseFontSize`, `setup: { debugMode? }`, empty `turns`/`rounds`, `resetGame()`, `storeTurn()`/`storeRound()` (truncating later entries), `persist: true` |
| `src/util/NavigationState.ts` | Constructor `(route, state)` reading route params via `getIntRouteParam` |
| `src/components/round/` or `turn/` `SideBar.vue`, `DebugInfo.vue` | Empty frame with `navigationState` prop (`DebugInfo` only shown with `state.setup.debugMode`) |
| `src/services/enum/Player.ts` | `PLAYER = 'player'`, `BOT = 'bot'` |
| `src/locales/en.json`, `de.json` | Only keys of existing screens: `gameTitle`, `home.*`, `setup.title`, `setupBot.title` (next button), `action.*`, `footer.credits`, `serviceWorkerUpdatedRefresh.*`, `notfound.title` - identical keys in both files |
| `tests/unit/helper/mockState.ts`, `mockTurn.ts`/`mockRound.ts` | `mockXxx(params?: MockXxxParams)` with defaults matching `state.ts` |
| `tests/unit/util/NavigationState.spec.ts` | Simple test for route param parsing |
| `tests/e2e/smoke-test.spec.ts` | Home `h1` → "Play Game" → setup → "Abort Game" via `#endGameModal` → home `h1` |

## D. Do Not Copy

- Game-specific services, enums, components, views, icons, locale keys and test cases of the reference app.
- Leftovers in stubs (e.g. i18n keys or texts of the reference game in `SideBar.vue`, e2e steps of the reference flow).
- `resources/app-icon.psd` of another game.
