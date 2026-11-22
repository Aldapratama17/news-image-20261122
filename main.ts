#!/usr/bin/env node
/**
 * Entrypoint: copies entry.png to the output directory.
 * Uses only Node.js standard library. Deterministic.
 */

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from 'fs';
import { dirname, join, resolve } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

function main(): void {
  const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
  const srcPath = resolve(__dirname, 'entry.png');
  const destPath = resolve(outputDir, 'entry.png');

  // Verify source exists and is a valid PNG
  if (!existsSync(srcPath)) {
    console.error(`Source not found: ${srcPath}`);
    process.exit(1);
  }

  const srcStat = statSync(srcPath);
  if (srcStat.size === 0) {
    console.error('Source file is empty');
    process.exit(1);
  }

  // Verify PNG magic bytes
  const magic = readFileSync(srcPath, { encoding: null });
  if (magic.length < 8 ||
      magic[0] !== 0x89 || magic[1] !== 0x50 || magic[2] !== 0x4e || magic[3] !== 0x47 ||
      magic[4] !== 0x0d || magic[5] !== 0x0a || magic[6] !== 0x1a || magic[7] !== 0x0a) {
    console.error('Source is not a valid PNG (bad magic)');
    process.exit(1);
  }

  // Ensure output directory exists
  mkdirSync(outputDir, { recursive: true });

  // Copy file
  copyFileSync(srcPath, destPath);

  // Verify copy
  const destStat = statSync(destPath);
  if (destStat.size !== srcStat.size) {
    console.error(`Size mismatch: src=${srcStat.size} dest=${destStat.size}`);
    process.exit(1);
  }

  console.log(`Copied ${srcStat.size} bytes to ${destPath}`);
}

main();
