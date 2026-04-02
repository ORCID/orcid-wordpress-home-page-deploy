import fs from "node:fs/promises";
import postcss from "postcss";

const CSS_PATH = "dist/wordpress-homepage.css";

function shouldSkipRule(rule) {
  // Skip keyframes inner rules like "0% { ... }"
  const parent = rule.parent;
  return (
    parent &&
    parent.type === "atrule" &&
    typeof parent.name === "string" &&
    parent.name.toLowerCase().endsWith("keyframes")
  );
}

function transformSingleSelector(sel) {
  const trimmed = sel.trim();
  if (!trimmed) return trimmed;

  if (trimmed === ":root") return ":root .homepage";
  if (trimmed === "body") return "#main.homepage";

  if (trimmed.startsWith(".homepage")) {
    const rest = trimmed.slice(".homepage".length).trimStart();
    return rest ? `#main.homepage ${rest}` : "#main.homepage";
  }

  return `.homepage ${trimmed}`;
}

const css = await fs.readFile(CSS_PATH, "utf8");

const result = await postcss([
  (root) => {
    root.walkRules((rule) => {
      if (shouldSkipRule(rule)) return;
      if (!rule.selector) return;
      // PostCSS exposes `rule.selectors` split on commas at the selector-list level.
      // This is safe for modern selectors like :where() and avoids brittle parsing.
      rule.selectors = rule.selectors.map(transformSingleSelector);
    });
  },
]).process(css, { from: CSS_PATH, to: CSS_PATH });

await fs.writeFile(CSS_PATH, result.css);

