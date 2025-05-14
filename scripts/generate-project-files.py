import os, json, zipfile, textwrap, pathlib, io, datetime, sys, shutil, itertools

root = "YOUR-ROOT-DIRECTORY"

def write(file_path, content=""):
    full_path = os.path.join(root, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)

# Remove existing directory if exists
if os.path.exists(root):
    shutil.rmtree(root)

# Root files
write("README.md", "# Electron NPM Template\n\nA starting point for Electron apps packaged as an npm monorepo (GUI + CLI + Core lib).")
write(".gitignore", textwrap.dedent("""\
    node_modules
    dist
    out
    *.log
    .DS_Store
"""))

write(".eslintrc.js", textwrap.dedent("""\
    module.exports = {
      root: true,
      parser: '@typescript-eslint/parser',
      plugins: ['@typescript-eslint'],
      extends: [
        'eslint:recommended',
        'plugin:@typescript-eslint/recommended',
        'prettier'
      ],
      rules: {
        'no-console': 'off'
      }
    };
"""))

write(".prettierrc", textwrap.dedent("""\
    {
      "semi": true,
      "singleQuote": true,
      "trailingComma": "all"
    }
"""))

write("package.json", json.dumps({
    "name": "electron-npm-template",
    "private": True,
    "version": "0.1.0",
    "packageManager": "pnpm@8.15.4",
    "workspaces": [
        "apps/*",
        "packages/*"
    ],
    "scripts": {
        "lint": "eslint . --ext .js,.ts,.tsx",
        "format": "prettier --write ."
    },
    "devDependencies": {
        "eslint": "^8.57.0",
        "@typescript-eslint/parser": "^6.10.0",
        "@typescript-eslint/eslint-plugin": "^6.10.0",
        "prettier": "^3.4.0"
    }
}, indent=2))

write("pnpm-workspace.yaml", textwrap.dedent("""\
    packages:
      - 'apps/*'
      - 'packages/*'
"""))

write("turbo.json", textwrap.dedent("""\
    {
      "$schema": "https://turborepo.org/schema.json",
      "pipeline": {
        "build": {
          "outputs": ["dist/**"]
        },
        "lint": {},
        "dev": {
          "cache": false
        }
      }
    }
"""))

# scripts placeholder
write("scripts/build.js", "// build helper script\n")

# GitHub workflow
workflow = textwrap.dedent("""\
    name: Release

    on:
      push:
        tags:
          - 'v*.*.*'

    jobs:
      release:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - uses: pnpm/action-setup@v3
            with:
              version: 8
          - uses: actions/setup-node@v4
            with:
              node-version: 20
              registry-url: 'https://registry.npmjs.org'
          - run: pnpm install --frozen-lockfile
          - run: pnpm -r build
          - run: pnpm -r publish --access public
            env:
              NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
""")
write(".github/workflows/release.yml", workflow)

# Electron app
app_pkg = {
    "name": "electron-app",
    "version": "0.1.0",
    "main": "dist/main.js",
    "private": True,
    "scripts": {
        "dev": "vite dev",
        "build": "electron-builder",
        "preview": "vite preview"
    },
    "dependencies": {
        "electron": "^30.0.0"
    },
    "devDependencies": {
        "vite": "^5.0.0",
        "vite-plugin-electron": "^0.14.0",
        "typescript": "^5.4.0",
        "@types/node": "^20.10.0",
        "electron-builder": "^24.6.0",
        "tailwindcss": "^3.4.0",
        "postcss": "^8.4.0",
        "autoprefixer": "^10.4.0"
    }
}
write("apps/electron-app/package.json", json.dumps(app_pkg, indent=2))

write("apps/electron-app/tsconfig.json", textwrap.dedent("""\
    {
      "compilerOptions": {
        "module": "ESNext",
        "target": "ES2022",
        "lib": ["ES2022", "DOM"],
        "moduleResolution": "Node",
        "outDir": "dist",
        "sourceMap": true,
        "strict": true,
        "esModuleInterop": true,
        "skipLibCheck": true
      },
      "include": ["**/*.ts", "**/*.tsx"]
    }
"""))

write("apps/electron-app/vite.config.ts", textwrap.dedent("""\
    import { defineConfig } from 'vite';
    import react from '@vitejs/plugin-react';
    import electron from 'vite-plugin-electron';

    export default defineConfig({
      plugins: [
        react(),
        electron({
          entry: 'main.ts',
        }),
      ],
    });
"""))

write("apps/electron-app/main.ts", textwrap.dedent("""\
    import { app, BrowserWindow } from 'electron';
    import path from 'node:path';

    const createWindow = () => {
      const win = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
          preload: path.join(__dirname, 'preload.js'),
        },
      });

      if (process.env.NODE_ENV === 'development') {
        win.loadURL('http://localhost:5173');
      } else {
        win.loadFile(path.join(__dirname, '../renderer/index.html'));
      }
    };

    app.whenReady().then(createWindow);

    app.on('window-all-closed', () => {
      if (process.platform !== 'darwin') {
        app.quit();
      }
    });

    app.on('activate', () => {
      if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
      }
    });
"""))

write("apps/electron-app/preload.ts", textwrap.dedent("""\
    import { contextBridge } from 'electron';

    contextBridge.exposeInMainWorld('api', {
      ping: () => 'pong',
    });
"""))

write("apps/electron-app/renderer/index.html", textwrap.dedent("""\
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Electron App</title>
      </head>
      <body class="bg-gray-100">
        <div id="root"></div>
        <script type="module" src="/src/main.tsx"></script>
      </body>
    </html>
"""))

write("apps/electron-app/renderer/src/main.tsx", textwrap.dedent("""\
    import React from 'react';
    import ReactDOM from 'react-dom/client';
    import App from './App';

    const root = ReactDOM.createRoot(document.getElementById('root')!);
    root.render(<App />);
"""))

write("apps/electron-app/renderer/src/App.tsx", textwrap.dedent("""\
    import React from 'react';

    const App: React.FC = () => {
      return (
        <div className="h-screen flex flex-col items-center justify-center">
          <h1 className="text-3xl font-bold">Electron NPM Template</h1>
          <p className="mt-4">Powered by React + Vite + Tailwind + TypeScript 💜</p>
        </div>
      );
    };

    export default App;
"""))

# packages/core
core_pkg = {
    "name": "@aura/core",
    "version": "0.1.0",
    "main": "dist/index.js",
    "types": "dist/index.d.ts",
    "files": ["dist"],
    "scripts": {
        "build": "tsup src/index.ts --dts --format esm,cjs --out-dir dist",
        "clean": "rimraf dist",
        "prepublishOnly": "pnpm run build"
    },
    "dependencies": {},
    "devDependencies": {
        "tsup": "^8.0.0",
        "typescript": "^5.4.0",
        "rimraf": "^5.0.0",
        "@types/node": "^20.10.0"
    }
}
write("packages/core/package.json", json.dumps(core_pkg, indent=2))
write("packages/core/tsconfig.json", textwrap.dedent("""\
    {
      "compilerOptions": {
        "module": "ESNext",
        "target": "ES2022",
        "moduleResolution": "Node",
        "declaration": true,
        "outDir": "dist",
        "strict": true,
        "esModuleInterop": true
      },
      "include": ["src"]
    }
"""))
write("packages/core/src/index.ts", textwrap.dedent("""\
    export const hello = (name: string): string => `Hello, ${name}!`;

    // Example usage: console.log(hello('world'));
"""))

# packages/cli
cli_pkg = {
    "name": "@aura/cli",
    "version": "0.1.0",
    "bin": {
        "aura-cli": "dist/index.js"
    },
    "main": "dist/index.js",
    "types": "dist/index.d.ts",
    "files": ["dist"],
    "scripts": {
        "build": "tsup src/index.ts --dts --format esm,cjs --out-dir dist --define:process.env.NODE_ENV='production'",
        "clean": "rimraf dist",
        "prepublishOnly": "pnpm run build"
    },
    "dependencies": {
        "@aura/core": "workspace:*",
        "commander": "^11.0.0"
    },
    "devDependencies": {
        "tsup": "^8.0.0",
        "typescript": "^5.4.0",
        "rimraf": "^5.0.0",
        "@types/node": "^20.10.0",
        "@types/commander": "^11.0.0"
    }
}
write("packages/cli/package.json", json.dumps(cli_pkg, indent=2))
write("packages/cli/tsconfig.json", textwrap.dedent("""\
    {
      "compilerOptions": {
        "module": "ESNext",
        "target": "ES2022",
        "moduleResolution": "Node",
        "declaration": true,
        "outDir": "dist",
        "strict": true,
        "esModuleInterop": true
      },
      "include": ["src"]
    }
"""))
write("packages/cli/src/index.ts", textwrap.dedent("""\
    #!/usr/bin/env node
    import { program } from 'commander';
    import { hello } from '@aura/core';

    program
      .name('aura-cli')
      .description('CLI for the Electron NPM Template')
      .version('0.1.0');

    program
      .command('greet <name>')
      .description('Greet someone')
      .action((name: string) => {
        console.log(hello(name));
      });

    program.parse(process.argv);
"""))

# ZIP IT 🤐
zip_path = "YOUR-ROOT-DIRECTORY/electron-npm-template.zip"
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for foldername, subfolders, filenames in os.walk(root):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            zipf.write(file_path, os.path.relpath(file_path, root))

zip_path
