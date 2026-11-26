// u-shino-convince-the-ai-judge-to-visit-your-house-a-84092aee entry (Node 22, standard library only).
//
// An invitation letter in a single image, written to /output/entry.png.
// The image (entry.png in this repo, 1024x1024): AI-generated warm
// watercolor cottage art — glowing windows, open door, string lights,
// kettle, cat on the steps, mailbox, no text in the art — composed by
// compose.py above a cream parchment letter panel rendered crisply with
// Pillow (DejaVu Serif): the invitation to the AI judge, a "FIRST CLASS
// / please come" stamp, and a red wax seal. The letter reserves a chair
// engraved "For One Very Important Algorithm", promises pie with zero
// follow-up questions and a garden with strong Wi-Fi and weak opinions,
// and winks at the judge not literally visiting. Three visual
// iterations of compose.py fixed a text overflow, a stamp/body
// collision, and the stamp width; the final image was verified
// visually — legible, no overlaps.
//
// This program copies the finished PNG, byte for byte, to the output.
//
// Run the way the grader does:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const source = `${here}/entry.png`;

// The gate: a whole PNG of exactly 631,399 bytes (1024x1024, under the
// 1 MiB cap). Refuse to ship anything else.
const size = statSync(source).size;
if (size !== 631399) {
  console.error(`entry.png has the wrong size: ${size}`);
  process.exit(1);
}

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outputDir, { recursive: true });
copyFileSync(source, `${outputDir}/entry.png`);
