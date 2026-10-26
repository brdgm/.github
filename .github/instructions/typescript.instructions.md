---
description: "Use when writing, reviewing or refactoring TypeScript services, utils, NavigationState, card decks, bot logic, scoring calculations or unit tests in the brdgm solo helper apps. Covers layering (services/util independent of components, store, router, i18n), reactivity in stateful services, scoring formulas in util, strict typing (no any, no non-null assertions, casts), ESLint config and known code smells not to copy."
applyTo: "**/src/**/*.ts, **/tests/**/*.ts"
---

# TypeScript Guidelines (Services, Util, Tests)

Best practices for new code, based on an audit of the apps since 2024. They take precedence over patterns found in existing apps.

## Layering

- `services/` and `util/` contain the game logic and are independent of the UI: they never import components/views, never call `useStateStore()`, `useRoute()`/`useRouter()` or `useI18n()`. Views pass the needed data (e.g. `state`, route params, settings) in as parameters.
- The only Vue imports allowed in services are `ref`/`readonly` for **stateful services** (`CardDeck`, bot state): state lives in internal `ref()`s so the UI updates when a view calls e.g. `draw()`. Persist via `toPersistence()` (plain data and IDs only), restore via `static fromPersistence()`.
- Game rules, bot decisions and non-trivial **VP/scoring formulas** go into `services/` or `util/getXxx.ts` with unit tests (e.g. `getCardVP.ts` in `south-tigris-wayfarers`, `calculateTieredScores.ts` in `clans-of-caledonia`) - components only bind inputs and sum up.
- Throw `TranslatableError` (brdgm-commons) for errors that should be shown translated to the user.

## Typing

- TypeScript strict mode. No `any`, no `@ts-ignore`/`@ts-expect-error`.
- No non-null assertions (`!`) for lookups - use `findMandatory` (brdgm-commons) or explicit checks.
- `as` casts only where unavoidable (typed initial values in `data()`, `PropType`). `as unknown as` belongs only into test mock helpers.
- No unused imports or variables. Unused parameters (e.g. in emit validators) are prefixed with `_`; new apps configure ESLint with `'@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }]` instead of using `eslint-disable` comments.
- Prefer immutable/functional logic: `readonly` getters, `toSorted`, `map`/`filter`/`reduce`. Use lodash `cloneDeep` (works with Vue proxies, unlike `structuredClone`) instead of `JSON.parse(JSON.stringify(...))`.
- No type checker runs in the build (`vite build` only strips types, ESLint is not type-aware) - keep the code free of TypeScript errors in the editor. Optional manual check: `npx -p typescript@5.9 -p vue-tsc vue-tsc --noEmit` (current `vue-tsc` cannot load TypeScript 6 yet).

## Unit Tests

- Test every service/util, including `NavigationState` and scoring formulas, with deterministic data (fixed card IDs via `fromPersistence`/mock helpers).
- Reuse/extend the `mockXxx(params?)` helpers in `tests/unit/helper/` instead of local helper functions.
- Use the most specific chai assertion (Sonar S5906, the most frequent issue in all apps): `expect(list).to.have.lengthOf(3)` instead of `expect(list.length).to.eq(3)`, `.to.be.true`/`.to.be.undefined` instead of `.to.eq(true)`/`.to.eq(undefined)`.
- Always assert the expected error message (Sonar S5958): `expect(() => deck.draw()).to.throw('Pile is empty.')`, not a bare `.to.throw()`. `findMandatory` throws `No item with key: <key>`.
- Unique test titles within a `describe` (Sonar S8754). Repeated tests that only differ in their input data go into one test with a loop over a data table (Sonar S5976).

## Sonar Rules for Code

SonarCloud analyzes every PR. Avoid these issues found repeatedly in the apps:

- Existence checks with `.some(...)` instead of `.find(...)` or `.filter(...).length > 0` (S7754).
- Default-exported functions are named: `export default function getStarLimit(...)`, never an anonymous `export default (...) => ...` (S7726).
- Constant lookup lists and collections only used for existence checks are a `Set` with `.has()`, not an array with `.includes()` (S7776).
- No nested template literals, e.g. ``t(`rules.${t(`...`)}`)`` - build the inner key in a separate variable/computed (S4624).

## Do Not Copy (known smells in existing apps)

| Smell | Found in | Instead |
|-------|----------|---------|
| Service importing a component (`BotActions.ts` → `BotAction.vue`) | `bloomworks` | services never import components |
| `useStateStore()` inside util/service classes | `gaia-project` `NavigationState.ts`, `el-burro` `storePhase.ts` | pass `state` as parameter |
| `any` in helper methods (e.g. `getCardInfo(card: any)`) | `millennia` `DebugInfo.vue` | proper (union) types |
| `// eslint-disable-line @typescript-eslint/no-unused-vars` | most apps since 2024 | `argsIgnorePattern: '^_'` in ESLint config |
| VP formulas inline in components, untested | `seti`, `south-tigris-scholars` `FinalScoring.vue` | `util/getXxxVP.ts` with tests |
| `expect(list.length).to.eq(n)` (Sonar S5906) | test specs in all apps | `expect(list).to.have.lengthOf(n)` |
| `expect(fn).to.throw()` without message (Sonar S5958) | test specs in most apps | `.to.throw('expected message')` |
