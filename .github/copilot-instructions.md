# brdgm.me Solo Helper Applications - Copilot Instructions

## Architecture Overview

This workspace contains **board game solo helper applications** built with Vue 3 + TypeScript. Each `*-solo-helper` project is a PWA that assists players with AI opponents in solo board game modes.

### Key Components

- **brdgm-commons**: Shared library providing common utilities, components, and router functionality used across all projects
- **Solo Helper Projects**: Individual Vue 3 PWAs for specific board games (Ark Nova, Terra Mystica, etc.)
- **Centralized Configuration**: `.github/` contains shared CI/CD workflows and configurations

## Project Structure Patterns

Each solo helper follows this consistent architecture:

```
src/
├── services/          # Game-specific logic (cards, actions, bot behavior)
│   ├── enum/         # TypeScript enums for game constants
│   ├── Card.ts       # Card definitions and logic
│   └── BotActions.ts # AI opponent behavior
├── store/            # Pinia stores with persistence
│   └── state.ts      # Main application state with Pinia + persistedstate
├── views/            # Route components (SetupGame, RoundPlayer, RoundBot)
├── components/       # Vue components
│   ├── structure/    # Reusable structural/UI components (icons, footers, buttons)
│   ├── setup/        # Setup-phase components
│   └── round/        # Round/turn-phase components (game-specific subdirs may vary)
├── util/             # Utility functions (NavigationState, color mappings, etc.)
├── locales/          # I18n JSON files (en.json, de.json, etc.)
└── router/index.ts   # Vue Router with localStorage persistence
```

## Development Workflows

### Standard Commands
```bash
npm run dev            # Vite dev server with hot reload
npm run build          # Production build (outputs to dist/)
npm run test:unit run  # Vitest unit tests
npm run test:e2e       # Playwright e2e tests
npm run lint           # ESLint with --fix
```

### Key Dependencies
- **Vue 3** + **TypeScript** + **Vite** (build tool)
- **Pinia** with `pinia-plugin-persistedstate` for state management
- **Vue Router** with custom localStorage persistence from brdgm-commons
- **Bootstrap 5** for styling (no custom CSS framework)
- **Vue I18n** for internationalization
- **Vite PWA** plugin for Progressive Web App features

## Critical Patterns

### State Management
- Use Pinia stores with persistence: `pinia-plugin-persistedstate`
- Store names include package name: `defineStore(\`\${name}.store\`)`
- State includes `setup` (game configuration) and `rounds` (game progression)

### Routing & Navigation
- Use `createRouterMatomoTracking` from brdgm-commons
- Routes automatically save/restore from localStorage
- Hash-based routing for PWA compatibility

### Internationalization
- Vue I18n with JSON files in `src/locales/` per project (`en.json` is master, `de.json` in most projects)
- Detailed conventions are defined in `.github/instructions/i18n.instructions.md`

### Game Services Architecture
- **Enums**: Game constants (PlayerColor, DifficultyLevel, CardName)
- **Card/Actions classes**: Immutable game logic with static methods
- **Bot behavior**: Deterministic AI actions based on game state

### Build & Deployment
- Each project has `appDeployName` in package.json for deployment paths
- Vite base path: `/${appDeployName}/`
- PWA assets generated with `@vite-pwa/assets-generator`
- Uses shared GitHub Action: `brdgm/github-action-build@v1`

## brdgm-commons Integration

**Always import utilities from brdgm-commons** rather than duplicating:

```typescript
// Correct - use shared utilities
import toggleArrayItem from '@brdgm/brdgm-commons/src/util/array/toggleArrayItem'
import createRouterMatomoTracking from '@brdgm/brdgm-commons/src/util/router/createRouterMatomoTracking'

// Package.json dependency
"@brdgm/brdgm-commons": "^1.8.1"
```

### Bootstrap Modals
Always use the `ModalDialog` component from brdgm-commons when a Bootstrap modal is needed — never create custom modal markup:

```typescript
import ModalDialog from '@brdgm/brdgm-commons/src/components/structure/ModalDialog.vue'
```

```vue
<ModalDialog id="myModal" :title="t('myModal.title')">
  <template #body>
    <p v-html="t('myModal.content')"/>
  </template>
</ModalDialog>
```

Key props: `id` (required), `title`, `sizeLg`/`sizeXl`, `scrollable`, `centered` (default `true`). Slots: `header`, `body`, `footer`.

### Number Inputs
Always use the `NumberInput` component from brdgm-commons when a numeric input field is needed — never use a plain `<input type="number">`:

```typescript
import NumberInput from '@brdgm/brdgm-commons/src/components/form/NumberInput.vue'
```

```vue
<NumberInput v-model="score" :min="0" :max="100"/>
```

Key props: `min` (default `0`), `max` (default `9999`). Supports v-model and arithmetic expressions (e.g. `1 + 2 - 3`).

### Enum Utilities
Always use enum helpers from brdgm-commons — never use `Object.values()` or manual enum lists:

```typescript
import getAllEnumValues from '@brdgm/brdgm-commons/src/util/enum/getAllEnumValues'
import getPrioritizedEnumValues from '@brdgm/brdgm-commons/src/util/enum/getPrioritizedEnumValues'
```

- `getAllEnumValues(MyEnum)` — returns all values of a string or number enum
- `getPrioritizedEnumValues(MyEnum, preferredValues)` — returns enum values with preferred values first

### Random Utilities
Always use random helpers from brdgm-commons — never use `Math.random()` directly for picking enum values or rolling dice:

```typescript
import randomEnum from '@brdgm/brdgm-commons/src/util/random/randomEnum'
import randomEnumDifferentValue from '@brdgm/brdgm-commons/src/util/random/randomEnumDifferentValue'
import rollDice from '@brdgm/brdgm-commons/src/util/random/rollDice'
```

- `randomEnum(MyEnum)` — picks a random enum value
- `randomEnumDifferentValue(MyEnum, currentValue)` — picks a random enum value excluding the given value(s)
- `randomEnumMultiDifferentValue(MyEnum, count)` — picks multiple distinct random enum values
- `rollDice(sides)` — rolls a die (1 to sides)
- `rollDiceDifferentValue(sides, currentValue)` — rolls a die excluding the given value(s)
- `rollDiceMultiDifferentValue(sides, count)` — rolls multiple distinct dice values

## Testing Strategy

- **Unit tests**: Vitest for service classes and utilities
- **E2E tests**: Playwright for full user workflows
- **Coverage**: Istanbul coverage reporting
- Tests mirror `src/` structure in `tests/unit/` (e.g. `tests/unit/services/`, `tests/unit/util/`)
- **Assertions**: Use `chai` (`import { expect } from 'chai'`, e.g. `expect(result).to.eq(expected)`)
- **Mock helpers**: Each project has reusable `mockXxx` helper functions in `tests/unit/helper/` (e.g. `mockState.ts`, `mockRound.ts`, `mockCardDeck.ts`). When writing new unit tests, always check this folder first and reuse existing helpers instead of creating local helper functions within individual test files.

## Code Style

- **No semicolons**: Never use semicolons at the end of lines in TypeScript/JavaScript files. ESLint rule: `'semi': ['error', 'never']`
- **Single quotes**: Always use `'` instead of `"` for strings, imports, and object keys in TypeScript/JavaScript. ESLint rule: `'quotes': ['error', 'single']`
- **TypeScript strict mode** with Vue 3 **Options API** (`defineComponent` with `props`, `computed`, `methods`; composition utilities like `useI18n()` are called inside `setup()`)
- **Bootstrap classes** for styling (avoid custom CSS)
- **Functional programming** patterns in game logic services

## Common Tasks

- **Adding new game features**: Create services in `src/services/`, add to state store, create views
- **New translations**: Add JSON file to `src/locales/`, follow existing key patterns
- **Bot behavior**: Extend `BotActions.ts` with deterministic logic methods
- **PWA updates**: Use `pwa-assets-generator` for icons, configure in `vite.config.ts`

Focus on maintaining consistency across all solo helper projects while leveraging shared functionality from brdgm-commons.