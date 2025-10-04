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
- JSON files in `src/locales/` (en.json is master)
- Use descriptive keys: `"setup.players.playerCount"`
- English is always the master language
- For additional language, German is supported in most cases as well
- Other languages are optional and provided by the community in later stages

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

## Testing Strategy

- **Unit tests**: Vitest for service classes and utilities
- **E2E tests**: Playwright for full user workflows
- **Coverage**: Istanbul coverage reporting
- Tests mirror `src/` structure in `tests/unit/` and `tests/e2e/`

## Code Style

- **No semicolons**: ESLint rule `'semi': ['error', 'never']`
- **TypeScript strict mode** with Vue 3 composition API
- **Bootstrap classes** for styling (avoid custom CSS)
- **Functional programming** patterns in game logic services

## Common Tasks

- **Adding new game features**: Create services in `src/services/`, add to state store, create views
- **New translations**: Add JSON file to `src/locales/`, follow existing key patterns
- **Bot behavior**: Extend `BotActions.ts` with deterministic logic methods
- **PWA updates**: Use `pwa-assets-generator` for icons, configure in `vite.config.ts`

Focus on maintaining consistency across all solo helper projects while leveraging shared functionality from brdgm-commons.