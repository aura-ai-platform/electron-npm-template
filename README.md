# Electron NPM Template 

 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/aura-ai-platform/electron-npm-template/actions/workflows/release.yml/badge.svg)](https://github.com/aura-ai-platform/electron-npm-template/actions)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://makeapullrequest.com)
[![Code Style: Prettier](https://img.shields.io/badge/code_style-prettier-ff69b4.svg)](https://prettier.io/)
[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)


## Introduction

The Electron NPM Template is a template for building modern monorepo Electron applications using pnpm for package management, Turborepo for building, and Vite for code integration. It is designed to be a solid starting point for Electron projects, including support for the CLI (`@aura/cli`) and the core libraries (`@aura/core`).


## Project Structure CLI Commands

```bash

pnpm cli dev            # Run CLI locally
pnpm cli build          # Build CLI package
pnpm cli lint           # Lint CLI code

```

```

.eslintrc.js        // Configuration file for ESLint, a code linting utility.
.prettierrc         // Configuration file for Prettier, a code formatting tool.
LICENSE             // File containing the project's license information.
README.md           // Project's main documentation file, usually displayed on platforms like GitHub.
package.json        // Describes the project, its dependencies, and scripts.
pnpm-workspace.yaml // Configuration file for pnpm workspace, managing multiple packages.
turbo.json          // Configuration file for Turborepo, a build system for monorepos.
vite.config.ts      // Configuration file for Vite, the build tool.

scripts/            // Directory containing scripts.
  build.js          // A build script.
  generate.py       // A Python script for generating something.

packages/           // Directory containing packages.
  core/             // A core package.
    package.json    // Package configuration.
    tsconfig.json   // TypeScript compiler configuration.
    src/            // Source code directory.
      index.ts      // Entry point for the core package.
  cli/              // A command-line interface (CLI) package.
    package.json    // Package configuration.
    tsconfig.json   // TypeScript compiler configuration.
    src/            // Source code directory.
      index.ts      // Entry point for the CLI package.

apps/               // Directory containing application code.
  electron-app/     // An Electron application.
    main.ts         // Main process entry point for the Electron app.
    package.json    // Package configuration for the Electron app. Contains dependencies, and build scripts
    preload.ts      // Preload script for the Electron app, used for security and bridging between the main and renderer processes.
    tsconfig.json   // TypeScript compiler configuration.
    vite.config.ts  // Vite configuration for the Electron app.
    renderer/       // Directory containing the renderer process code (UI).
      index.html    // HTML file for the renderer process.
      src/          // Source code directory for the renderer process.
        App.tsx     // Main React component.
        main.tsx    // Entry point for the React app, which renders the App component.
.github/            // Directory containing GitHub workflow configurations.
  workflows/        // Directory containing workflow files.
    release.yml     // GitHub Actions workflow for releases.


```


License MIT © [AURA](/LICENSE)

