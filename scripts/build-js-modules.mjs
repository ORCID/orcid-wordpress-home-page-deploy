import { build } from "esbuild";
import fs from "node:fs/promises";
import path from "node:path";

const distDir = path.resolve("dist");
const entry = path.join(distDir, "blablablocks-tabs-view.js");
const outFile = path.join(distDir, "wordpress-homepage-modules.js");

async function fileExists(p) {
  try {
    await fs.access(p);
    return true;
  } catch {
    return false;
  }
}

// If the module entry wasn't downloaded in this run, still output a stub so
// HTML can safely reference it (and gulp can fingerprint it).
if (!(await fileExists(entry))) {
  await fs.mkdir(distDir, { recursive: true });
  await fs.writeFile(
    outFile,
    "/* wordpress-homepage-modules.js: no module entries for this build */\n"
  );
  process.exit(0);
}

await build({
  entryPoints: [entry],
  bundle: true,
  // @wordpress/interactivity uses top-level await, so we must output ESM.
  format: "esm",
  platform: "browser",
  target: ["es2022"],
  outfile: outFile,
  sourcemap: false,
  logLevel: "info",
  define: {
    "process.env.NODE_ENV": JSON.stringify(process.env.NODE_ENV ?? "production"),
  },
});

import { build } from "esbuild";
import fs from "node:fs/promises";
import path from "node:path";

const distDir = path.resolve("dist");
const entry = path.join(distDir, "blablablocks-tabs-view.js");
const outFile = path.join(distDir, "wordpress-homepage-modules.js");

async function fileExists(p) {
  try {
    await fs.access(p);
    return true;
  } catch {
    return false;
  }
}

if (!(await fileExists(entry))) {
  // Nothing to build (plugin not included in this run).
  // Still write a stub so HTML can always reference it.
  await fs.mkdir(distDir, { recursive: true });
  await fs.writeFile(
    outFile,
    "/* wordpress-homepage-modules.js: no module entries for this build */\n"
  );
  process.exit(0);
}

await build({
  entryPoints: [entry],
  bundle: true,
  // Use ESM output because @wordpress/interactivity uses top-level await.
  format: "esm",
  platform: "browser",
  // TLA requires modern targets.
  target: ["es2022"],
  outfile: outFile,
  sourcemap: false,
  logLevel: "info",
  // Some WordPress packages assume NODE_ENV exists.
  define: {
    "process.env.NODE_ENV": JSON.stringify(process.env.NODE_ENV ?? "production"),
  },
});
