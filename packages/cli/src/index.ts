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
