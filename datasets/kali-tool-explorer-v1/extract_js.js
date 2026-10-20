#!/usr/bin/env node
/*
 * Extract data-only JavaScript objects from the Kali Tool Explorer HTML.
 *
 * The app keeps its data in top-level const declarations. This helper finds
 * each declaration, walks the matching braces while respecting string
 * literals, and evaluates the resulting object literal. It refuses blocks
 * that contain functions or arrow functions, so only static data is parsed.
 *
 * Usage: node extract_js.js /path/to/forensik-explorer.html > data.json
 */
'use strict';

const fs = require('fs');

const NAMES = [
  'toolExamples',
  'toolFlags',
  'playbooks',
  'learningPaths',
  'wizardFlows',
  'promptTemplates'
];

function extractBlock(html, name) {
  const re = new RegExp('(?:const|let|var)\\s+' + name + '\\s*=\\s*([\\{\\[])');
  const match = re.exec(html);
  if (!match) return null;

  const open = match[1];
  const close = open === '{' ? '}' : ']';
  const start = match.index + match[0].length - 1;
  let depth = 0;
  let quote = null;
  let escaped = false;

  for (let i = start; i < html.length; i += 1) {
    const ch = html[i];
    if (quote) {
      if (escaped) escaped = false;
      else if (ch === '\\') escaped = true;
      else if (ch === quote) quote = null;
      continue;
    }
    if (ch === "'" || ch === '"' || ch === '`') {
      quote = ch;
    } else if (ch === open) {
      depth += 1;
    } else if (ch === close) {
      depth -= 1;
      if (depth === 0) return html.slice(start, i + 1);
    }
  }
  throw new Error('Unterminated block for ' + name);
}

const html = fs.readFileSync(process.argv[2], 'utf8');
const result = {};

for (const name of NAMES) {
  const block = extractBlock(html, name);
  if (block === null) {
    result[name] = null;
    continue;
  }
  if (/\bfunction\b|=>/.test(block)) {
    throw new Error('Refusing to evaluate non-data block: ' + name);
  }
  result[name] = eval('(' + block + ')');
}

process.stdout.write(JSON.stringify(result));
