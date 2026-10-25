# Analyze and Plan a New Solo Helper App

Detailed procedure for "Phase B: Analyze and Plan" of the `create-solo-helper-app` skill. It builds on the Markdown transcriptions of the rules, cards and solo components from Phase A ([game-components.md](./game-components.md)). **No implementation before the plan is confirmed by the user.**

## Goal of a Solo Helper App

A brdgm.me solo helper is **not a "card flipper"**. It replaces the solo deck(s) **and the other solo components** (solo board, solo mat, bot tiles, ...) **and** takes over as many bot decisions and as much bookkeeping as possible:

- The app tracks all bot state that does not depend on the board: resources, VP, tracks, markers, cards/tokens owned, counters, which rules/bonuses were already triggered, ...
- The app evaluates bot decisions (priorities, tie breakers, conditions, fallbacks) whenever they can be derived from tracked state.
- The player only gives input when the **board state must be inspected** (e.g. "is the target space free?", "which tile is closest?") or when the input comes from the player's actions (e.g. silver paid to the bot, player passed). Such inputs are asked as late and as simple as possible (one click, `NumberInput`, "Executed" / "Not Possible").
- The player still follows the full game flow; the app tells them exactly what to do for the bot on the board.
- Ideally the player needs **neither the solo cards nor the solo board**. Physical solo components are only kept where they are really needed (e.g. a place for things the bot collects).

## 1. Read the Sources

Work with the Markdown transcriptions in `brdgm-resources/apps/<appDeployName>-solo-helper/` (`<resources>`, see [game-components.md](./game-components.md)) - create them first if they do not exist yet:

- `rules/solo-rules-en.md` (mandatory), `solo-rules-de.md` (if available), base rules `rules-en.md`/`rules-de.md` for the game flow, terms and end game scoring.
- `cards/<deck>-cards.md` with **all solo cards (front and back)** of every solo deck. The rules usually only explain the icons and operations - the actual bot actions are defined **on the cards**. Without analyzing every card the bot behavior is not fully understood.
- `components/<component>.md` for the solo board and all other solo components.
- `glossary.md` for terms and icons.

Look at the PDFs/page images only for visual questions. If a source is missing or not readable, ask the user for it. Never guess card contents or rules.

## 2. Analyze the Game Flow

1. Full game flow from the player's perspective: setup, rounds/eras/seasons, phases, turn structure (alternating, until passing, fixed number of actions), end of round, end-game trigger, final scoring.
2. The bot's part in each phase. Bots often **use shortcuts or skip phases** (e.g. no income/upkeep, fixed VP instead of a mechanism, passes after a fixed number of cards, takes several actions per card, gets bonus turns). List per phase: player does / bot does / bot skips.
3. Turn order and passing rules (who starts, does the start player change, what happens when one side passed), round/game end conditions.
4. Map the flow to the closest reference app (see the game flow table in step 5b of the skill).

## 3. Analyze the Solo Cards

For each deck:

- Number of cards, how the deck is built (difficulty level, expansions, mode), draw/discard/reshuffle/removal rules, special cards (end of round, reshuffle, "draw another card").
- **Card identifier**: every card gets a unique `id`. Be flexible and follow the physical cards:
  - Use the identifier printed on the card - a number (`12`) or a combination of letters and numbers (`A1`, `B12`, `S3`), which is often used to distinguish card types, decks, difficulty levels or variants.
  - If there is none, define an own scheme in the same spirit (e.g. sequential numbers in the order of the card sheet in the rulebook, or a letter prefix per deck/type like `A1`…`A12`, `B1`…`B8`).
  - Type: `number` for purely numeric identifiers, `string` for anything else.
  - Document the scheme in `cards/<deck>-cards.md`, as a comment in `Cards.ts` and in the plan, and show the identifiers in `DebugInfo` so the user can cross-check against the physical cards.
- Card front: every icon/field and its meaning (from the rules' icon glossary), the order of actions, parameters, conditions, priorities, fallbacks ("if not possible, ...").
- **Card back**: information visible to the player before the card is drawn (color, symbols, next action type, direction indicator).
- Result: the **card table** in `cards/<deck>-cards.md` (id, deck/type, back, actions with parameters) covering all cards. Mark every icon or combination that is unclear and ask the user.

## 4. Solo Board and Other Solo Components

Besides the solo cards, solo modes often come with a **solo board** (or solo mat, bot player board, bot tiles, dials, markers, overview cards). They are usually depicted and described in the solo rulebook. Analyze every component and every area/track/space/slot on it (documented in `components/<component>.md`):

- What it holds or tracks (bot resources, VP, track positions, action/priority displays, round/card counters, cards/tiles/tokens the bot collected, ...), when it changes, which rules use it.
- Whether the player interacts with it (e.g. takes items from it, compares own progress with it) or other game components refer to it.

The goal is that the app makes the solo board **and** the solo cards **superfluous**. Decide per area (and record it in the "App handling" of the component file):

| Area type | Typical handling |
|-----------|------------------|
| Counters, tracks, resources, VP, markers, displays, reference tables | Replaced by the app: tracked state shown in the sidebar/turn views, rules evaluated by the app |
| Storage for physical items the bot collects (cards, tiles, tokens from the shared supply) that are still needed on the table | Still needed physically - or replaced by "place next to the board" if the area is only a storage place; the app tracks counts/values where they matter for bot decisions or scoring |
| Areas the player interacts with during the game | Still needed physically if replacing them would make the game harder to play; otherwise the app shows the information and asks for minimal input |

Sometimes parts of the solo board are still required. Then the app states **exactly which parts are needed and for what** (bot setup instructions, action texts), and marks everything else as "managed by the app". Do not let the player maintain the same state twice (on the board and in the app).

## 5. Decide What the App Takes Over

For every element of the bot (resources, VP, tracks, markers, cards, tokens, solo board areas, decisions) decide:

| Category | Handling |
|----------|----------|
| Derivable from tracked state | Managed by the app (persisted in `BotPersistence`), shown to the player where useful ("managed by the app" hints in setup/rules texts) |
| Needs board inspection | App shows the rule plus visual aids (priority lists, focus icons, as in `GuildPriority.vue`/`LanguagePriority.vue` of `south-tigris-scholars`) and asks for minimal input |
| Physical action on the board | App shows exactly what to place/move/take |
| Player-driven input | Asked in the player turn view (e.g. resources paid to the bot, pass) |

Prefer tracking more in the app; only leave state on the physical board when tracking it would require too much input.

## 6. Preserve Hints of the Physical Solo Mode

When playing with physical components, the player sees certain information that helps planning (e.g. the back of the next solo card, the composition of the discard pile, the number of remaining cards until reshuffle/end of round, the direction indicator of the current card, the bot's track positions and collected items on the solo board). The app must preserve these hints - typically in the sidebar or the turn view. Examples: `seti` shows the decision direction of the current card and the drawn/total card count in the sidebar; `south-tigris-scholars` shows the number of blue/red cards in the discard pile (relevant for the color majority); `bloomworks` shows the remaining card stack. Do not show more than the physical game reveals.

## 7. Sidebar

Identify the information the player needs at a glance during the game, typically:

- round/turn/phase/season
- bot resources, VP and track positions managed by the app (usually what the solo board showed)
- deck information and preserved hints (see 6)
- quick access to rules or occasional bot actions (e.g. "Caliph Card" button in `south-tigris-scholars`)

Keep it compact (it floats right, ~145 px wide); editable values only where the player must correct the tracked state (modal + `NumberInput`, as in `bloomworks`).

## 8. Terminology and Rules Texts

- Complete the **glossary EN/DE** in `glossary.md` with all terms (components, actions, resources, phases) as used in the official rulebooks; enum values (kebab-case) are derived from the English terms (and match the `{icon-name}` names). The German translation uses the terms of the German rulebook.
- Rules texts shown in the app (setup instructions, action help modals, rule changes): **take short fragments 1:1 from the rulebook** (EN from `*-en.md`, DE from the matching passage in `*-de.md`). Write own wording, aligned with the original terms and style, only if the original is too long or does not fit because the app handles the solo components differently (e.g. "shuffle the deck" or "move the marker on the solo board" → managed by the app).

## 9. Setup and End of Game

- General setup options: difficulty levels (and what they change), expansions, modes/variants, start player, player color, ...
- Bot setup instructions: differences to a 2-player setup, which solo components (cards, solo board or parts of it, markers) the player does not need because the app manages them and which are still needed, opportunities for a randomizer.
- End game scoring of the bot (and player): which values are already tracked by the app (pre-filled, no input) and which must be entered. Game statistics only for Karma Games apps.

## Plan Template

Present the plan to the user in this structure (concise, tables preferred):

1. **Summary**: game, solo mode, bot name, difficulty levels, supported expansions/modes, chosen reference app.
2. **Game flow**: rounds/phases/turns for player and bot, incl. bot shortcuts/skipped phases, passing, end conditions.
3. **Routes and views**: route | view | when | player part | bot part | next/back.
4. **App vs. player responsibility**: element/decision | managed by app | player input / board action.
5. **Solo board and other solo components**: component/area | purpose in the rules | replaced by the app / still needed physically (and why). Summary which physical solo components the player still needs.
6. **Bot state** to persist (draft of `BotPersistence` and other state in `state.ts`).
7. **Solo decks**: build rules, card identifier scheme, reference to the card tables in `cards/<deck>-cards.md`, card back information.
8. **Bot actions**: list of `Action` values with the automated logic and the remaining player input; "if not possible" handling.
9. **Sidebar** contents and **preserved physical hints**.
10. **Setup screens** (general setup, bot setup instructions incl. needed/not needed solo components, randomizer).
11. **End game scoring** (tracked vs. entered values; statistics if Karma Games).
12. **Services/util/enums** draft (names and responsibilities).
13. **Icons** needed (by type, planned file names = `{icon-name}`s from `glossary.md`) - input for step 2.
14. **Glossary EN/DE** (reference to `glossary.md`) and which rules passages are taken 1:1.
15. **Open questions and alternatives** with a recommendation for each.

Then ask for confirmation and guidance with the ask-questions tool: confirm or correct the plan, decide the open questions/alternatives (e.g. how much board state to track, which solo board parts remain physical, view granularity, how to handle rare cases). Record the confirmed "App handling" decisions in the `components/<component>.md` files.

## Save the Plan

Save the confirmed plan as **`<resources>/app-plan.md`** in `brdgm-resources` - never in the app repo. It is the reference for all later sessions:

- Header: game, `appDeployName`, date of confirmation, links to the source/transcription files in the same folder.
- The 15 sections of the plan template with the confirmed decisions (open questions replaced by the decisions taken).
- **Implementation status**: checklist of steps 1-6 (and sub-steps 5a-5c), updated at the end of each step, plus a short list of open points/`TODO`s.
- **Change log**: when decisions change during implementation, update the affected sections and add a dated entry (what changed and why).
