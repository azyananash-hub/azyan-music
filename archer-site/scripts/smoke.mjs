// Smoke test ringan tanpa browser: pastikan hasil build memuat komponen kunci.
import { readFileSync, existsSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const root = join(dirname(fileURLToPath(import.meta.url)), "..", "dist");
const html = readFileSync(join(root, "index.html"), "utf8");
const required = [
  'id="hero"', 'id="window"', 'id="cabin"', 'id="aircraft"',
  'id="enquire"', 'id="enquiry-form"', 'data-track', 'data-words',
];
const missing = required.filter((s) => !html.includes(s));
const assets = html.match(/(?:src|href)="\/?(assets\/[^"]+)"/g) ?? [];
const brokenAssets = assets
  .map((m) => m.match(/assets\/[^"]+/)[0])
  .filter((a) => !existsSync(join(root, a)));

if (missing.length || brokenAssets.length) {
  console.error("SMOKE FAILED", { missing, brokenAssets });
  process.exit(1);
}
console.log(`SMOKE OK: ${required.length} markers, ${assets.length} asset refs`);
