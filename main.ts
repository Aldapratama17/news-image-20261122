#!/usr/bin/env node
/**
 * Entrypoint for news-image-20261122
 * Copies entry.png to the output directory specified by MAKEFUN_OUTPUT_DIR env var
 * or defaults to /output
 */

import { copyFileSync, existsSync, mkdirSync, readFileSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

function main(): void {
  // Get the directory of this script
  const __filename = fileURLToPath(import.meta.url);
  const __dirname = dirname(__filename);
  
  // Source file
  const srcPath = join(__dirname, "entry.png");
  
  // Destination directory from env or default
  const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  const destPath = join(outputDir, "entry.png");
  
  // Verify source exists
  if (!existsSync(srcPath)) {
    console.error(`Source file not found: ${srcPath}`);
    process.exit(1);
  }
  
  // Create output directory if needed
  if (!existsSync(outputDir)) {
    mkdirSync(outputDir, { recursive: true });
  }
  
  // Copy file
  copyFileSync(srcPath, destPath);
  
  // Verify copy
  const srcStat = readFileSync(srcPath);
  const destStat = readFileSync(destPath);
  
  if (srcStat.length !== destStat.length) {
    console.error("Copy verification failed: size mismatch");
    process.exit(1);
  }
  
  // Verify PNG magic
  const magic = destStat.slice(0, 8);
  const expectedMagic = Buffer.from([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]);
  if (!magic.equals(expectedMagic)) {
    console.error("Copy verification failed: not a valid PNG");
    process.exit(1);
  }
  
  console.log(`Copied ${srcPath} -> ${destPath} (${srcStat.length} bytes)`);
}

main();
