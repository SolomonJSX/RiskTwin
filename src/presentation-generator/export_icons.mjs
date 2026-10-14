import fs from 'node:fs';
import path from 'node:path';

const iconMap = {
  'shield': 'shield',
  'shield-check': 'shield-check',
  'award': 'award',
  'trophy': 'trophy',
  'alert-triangle': 'triangle-alert',
  'alert-circle': 'circle-alert',
  'landmark': 'landmark',
  'scale': 'scale',
  'trending-down': 'trending-down',
  'trending-up': 'trending-up',
  'bar-chart': 'chart-column',
  'eye-off': 'eye-off',
  'cpu': 'cpu',
  'brain': 'brain',
  'layers': 'layers',
  'zap': 'zap',
  'calculator': 'calculator',
  'sliders': 'sliders-horizontal',
  'file-check': 'file-check',
  'file-text': 'file-text',
  'user': 'user',
  'user-check': 'user-check',
  'smartphone': 'smartphone',
  'bell': 'bell',
  'key': 'key',
  'check-circle': 'circle-check',
  'coins': 'coins',
  'percent': 'percent',
  'heart-handshake': 'handshake',
  'code': 'code',
  'server': 'server',
  'database': 'database',
  'rocket': 'rocket',
  'target': 'target',
  'calendar': 'calendar',
  'clock': 'clock',
  'lock': 'lock',
  'sparkles': 'sparkles'
};

const outDir = path.join(import.meta.dirname, 'assets', 'svg');
if (!fs.existsSync(outDir)) {
  fs.mkdirSync(outDir, { recursive: true });
}

async function run() {
  for (const [alias, actual] of Object.entries(iconMap)) {
    try {
      const mod = await import('../web/node_modules/lucide-react/dist/esm/icons/' + actual + '.mjs');
      const data = mod.__iconData;
      let inner = '';
      for (const [tag, attrs] of data.node) {
        let attrStr = Object.entries(attrs)
          .filter(([k]) => k !== 'key')
          .map(([k, v]) => `${k}="${v}"`)
          .join(' ');
        inner += `  <${tag} ${attrStr} />\n`;
      }
      fs.writeFileSync(path.join(outDir, `${alias}.svg`), inner.trim(), 'utf8');
      console.log(`Saved: ${alias} (from ${actual})`);
    } catch (e) {
      console.error(`Failed: ${alias} (${actual})`, e.message);
    }
  }
}

run();
