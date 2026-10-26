---
description: "Use when writing, reviewing or refactoring Vue components and views (.vue) in the brdgm solo helper apps. Covers Options API best practices (setup/data/computed/methods split, why not Composition API or script setup), props, typed emits, v-model components, templates, DOM access, Bootstrap modals, useId, accessibility, v-for keys, component size and known code smells not to copy from existing apps."
applyTo: "**/*.vue"
---

# Vue Component Guidelines

The look & feel and usage patterns of the apps stay the same, but new code follows these best practices (based on an audit of the apps since 2024). They take precedence over patterns found in existing apps - see [Do Not Copy](#do-not-copy-known-smells-in-existing-apps).

## Options API

**Why the Options API is kept:** It is not deprecated and Vue recommends it as "a solid choice for low-to-medium-complexity scenarios" - which fits these apps (one view per route, logic in services). It gives every component the same readable structure, keeps all 30+ apps consistent and lets components be copied between apps. Logic reuse - the main benefit of the Composition API - happens through services/util classes and brdgm-commons instead of composables. Type checking with `vue-tsc` works for computed, methods, props and emits. Do not convert components to `<script setup>` or plain Composition API.

Component structure: `<script lang="ts">` with `defineComponent` (`name`, `components`, `props`, `emits`, `setup`, `data`, `computed`, `methods`). Explicit return types on computed properties and methods (`backButtonRouteTo() : string`) - required for correct `this` typing.

Rules for the split between `setup()` and the options:

- **`setup()`** only for:
  - composables: `useI18n()`, `useStateStore()`, `useRoute()`/`useRouter()`, `useId()`
  - objects created once per view from route + store: `NavigationState`, `RouteCalculator`, `BotActions`, and destructured readonly values (`const { round, turn } = navigationState`)
  - local reactive state whose **initial value depends on these setup values** (`ref(...)`), because `this.<setupValue>` is not correctly typed inside `data()`
  - return only what the template/options use.
- **`data()`** for all other local UI state (form inputs, selections, toggles), with typed initial values (`botSilver: undefined as number|undefined`). Do not create the same kind of state in both `setup()` and `data()`.
- **`computed`** for everything derived (from props, store, navigation state) - no side effects, no store/route mutations, no `draw()` calls. Prefer `computed` over `watch`.
- **`methods`** for event handlers and actions (store turn → navigate).
- Views are re-created on each route change (`<router-view :key="$route.fullPath"/>`), so values computed once in `setup()` are fine; never rely on mutating plain (non-`ref`) fields of class instances to update the UI.

## Props, Emits and `v-model`

- Typed props: `type: Object as PropType<CardAction>`, class props like `type: NavigationState`.
- Never mutate props (also not nested objects/arrays passed as props); emit an event instead.
- Declare all emits with typed payload validators: `emits: { ready: (_techType?: TechType) => true }`. Prefix unused parameters with `_` and configure ESLint (`'@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }]` in `eslint.config.js`) instead of adding `// eslint-disable-line` comments (121 such comments exist in the apps since 2024).
- **`v-model` components**: `modelValue` prop + `update:modelValue` emit, bound through a computed getter/setter:

  ```ts
  computed: {
    value: {
      get() : number|undefined { return this.modelValue },
      set(value: number|undefined) { this.$emit('update:modelValue', value) }
    }
  }
  ```

  Do **not** copy `modelValue` into `data()` and emit from a `watch` - the copy goes stale when the parent changes the value. For objects/arrays emit a new (cloned) value instead of mutating.

## Templates, DOM and Bootstrap

- No direct DOM access (`document.querySelector`, `getElementById`, `classList`) in components - use bindings, template refs (`ref="x"` + `this.$refs.x`) or brdgm-commons helpers (`showModal(id)`).
- Modals: always `ModalDialog`; open via `data-bs-toggle="modal" data-bs-target="#id"` or `showModal(id)`. Unique IDs for modals in reusable components via `` `modal-${useId()}` `` (instead of `nanoid`).
- Use `<button type="button">` for actions - also for clickable tiles and cards (e.g. the `ActionBox` that opens rules help): a real `<button>` with reset styles (`font: inherit`, own border/background, `text-align`) and only phrasing content inside (`<span>`s with `display: block/flex` instead of `<div>`s). Do not use `role="button"` + `tabindex` + `@keydown.enter` on a `<div>` (Sonar S6819 "Use <button> instead of the button role"). Likewise use native elements instead of ARIA roles: `<output>` (with `d-block`) for status notices instead of `role="status"`, `<img>`/`<svg>` with `<title>` instead of `role="img"`. Do not nest clickable elements with the same handler. `<a href="#">` only together with `data-bs-toggle` (Bootstrap prevents the navigation) or `@click.prevent`.
- `v-for` always with `:key`; use a stable domain key (card ID, enum value) where available. Index keys only for static lists that never change while the view is shown. Never `v-if` on the same element as `v-for`.
- Keep templates simple - move complex expressions into computed properties.
- Images: `alt=""` for decorative icons; meaningful `alt` if the image carries information not available as text. Inline `<svg>` icons need `aria-hidden="true"` (decorative) or an `aria-label` (Sonar ImgWithoutAltCheck).
- Every `<input>`/`<select>` has an associated label: `id` on the input and `<label for="...">`, or the input nested inside the `<label>`; every `<label>` has text and belongs to a control (Sonar InputWithoutLabelCheck, S6853).
- All user-visible texts via i18n (see `i18n.instructions.md`) - except the credits modal, the home page disclaimer and the debug mode label, which are intentionally English-only in all apps.
- Scoped SCSS for component-specific styles; no inline `style` attributes except bound dynamic values; global styles only in `App.vue`.

## Component Size and Logic Placement

- Views orchestrate: create `NavigationState`, show components, store the turn, navigate. Game rules, bot decisions and VP calculations belong in `services/`/`util/` with unit tests (see `typescript.instructions.md`).
- Split components that grow beyond ~250 lines (excluding large inline SVG) or that contain several unrelated sections; one `Action<Name>.vue` per action instead of `v-if` chains in one component.
- Large inline SVGs (e.g. for highlighting parts of a board) are fine, but must not use global IDs that clash when rendered twice.
- In `.vue` files the TypeScript rules of `typescript.instructions.md` apply as well (no `any`, no `!` for lookups, `as` casts only for `data()` initial values and `PropType`).

## Do Not Copy (known smells in existing apps)

| Smell | Found in | Instead |
|-------|----------|---------|
| `modelValue` copied into `data()` + `watch` to emit | `seti` `BotResources.vue`, `south-tigris-*` `BotSilver.vue`, `el-burro` `StartPlayer.vue` | computed get/set |
| `:key="xxxUpdateCount"` counter to force remounting a child | `seti` `RoundTurnBot.vue` (workaround for the stale `data()` copy in `BotResources.vue`) | computed get/set `v-model` - then no remount is needed |
| `// eslint-disable-line @typescript-eslint/no-unused-vars` on emits | most apps since 2024 | `argsIgnorePattern: '^_'` in ESLint config |
| `Object.values(Enum)` | `ExpansionsSetup.vue` in many apps | `getAllEnumValues` |
| `document.querySelector(...)` in components | `bloomworks` `PlayerMakeDelivery.vue`, `clans-of-caledonia` `RoundTurnBot.vue` | bindings, template refs, `showModal` |
| Clickable `<div>` without keyboard support | `ActionBox.vue` in most apps | `<button type="button">` with reset styles (not `role="button"` on a `<div>`, Sonar S6819) |
| VP formulas inline in `FinalScoring.vue`, untested | `seti`, `south-tigris-scholars` | `util/getXxxVP.ts` with tests |
| `nanoid` for element IDs | recent apps | Vue `useId()` |
