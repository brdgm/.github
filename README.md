.github
======

Central configurations for all GitHub repositories.

* [release-drafter.yml](.github/release-drafter.yml): Shared Release Drafter configuration
* [copilot-instructions.md](.github/copilot-instructions.md): Copilot instructions for development of the brdgm.me solo helper apps (architecture, patterns, reference implementations, brdgm-commons usage, testing, code style)
* [instructions/](.github/instructions/): File-specific Copilot instructions, loaded automatically for matching files:
  * [vue-components.instructions.md](.github/instructions/vue-components.instructions.md): Vue component guidelines (`.vue`)
  * [typescript.instructions.md](.github/instructions/typescript.instructions.md): TypeScript guidelines for services, util and tests
  * [i18n.instructions.md](.github/instructions/i18n.instructions.md): i18n conventions
* [skills/create-solo-helper-app](.github/skills/create-solo-helper-app/SKILL.md): Copilot skill to create a new solo helper app for a new board game
