// Smoke test headless (Chromium sem janela): foco visível e rolagem horizontal.
// Uso: NODE_PATH=<pasta com node_modules do playwright> node smoke_acessibilidade.js
const { chromium } = require('playwright');
const path = require('path');
const base = 'file://' + path.resolve(__dirname) + '/';
const falhas = [];
const checar = (ok, msg) => { console.log((ok ? 'ok   ' : 'FALHA ') + msg); if (!ok) falhas.push(msg); };

(async () => {
  const browser = await chromium.launch({ headless: true });
  for (const pagina of ['index.html', 'about.html']) {
    for (const [w, fonte] of [[320, 16], [375, 16], [768, 16], [1280, 16], [640, 32]]) {
      const p = await browser.newPage({ viewport: { width: w, height: 700 } });
      await p.goto(base + pagina);
      await p.evaluate(f => { document.documentElement.style.fontSize = f + 'px'; }, fonte);
      const { sw, cw } = await p.evaluate(() => ({
        sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth }));
      checar(sw <= cw, `${pagina} @${w}px fonte ${fonte}px sem rolagem horizontal (${sw} <= ${cw})`);
      await p.close();
    }
  }
  const p = await browser.newPage({ viewport: { width: 1280, height: 700 } });
  await p.goto(base + 'index.html');
  for (let i = 0; i < 5; i++) {
    await p.keyboard.press('Tab');
    const r = await p.evaluate(() => {
      const e = document.activeElement, s = getComputedStyle(e);
      return { nome: e.textContent.trim().slice(0, 10), estilo: s.outlineStyle,
               largura: parseFloat(s.outlineWidth), cor: s.outlineColor };
    });
    checar(r.estilo !== 'none' && r.largura >= 2 && r.cor === 'rgb(34, 212, 253)',
           `foco por Tab em "${r.nome}": ${r.estilo} ${r.largura}px ${r.cor}`);
  }
  await browser.close();
  if (falhas.length) { console.log(`\n${falhas.length} falha(s)`); process.exit(1); }
  console.log('\ntudo ok');
})();
