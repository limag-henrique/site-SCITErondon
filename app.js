/* ============================================
   Painel territorial anonimizado — lógica da aplicação
   ============================================ */

const D = window.TERRITORIAL_DATA;
const q = (s) => document.querySelector(s);
const qa = (s) => [...document.querySelectorAll(s)];

// ============ TABS ============
function tab(id) {
  qa('.panel').forEach((p) => (p.hidden = p.id !== id));
  qa('.tabs button').forEach((b) =>
    b.classList.toggle('active', b.dataset.tab === id)
  );
  location.hash = id;
}
qa('.tabs button').forEach((b) => (b.onclick = () => tab(b.dataset.tab)));

// ============ ESCAPE HTML ============
function esc(s) {
  return String(s).replace(/[&<>"']/g, (c) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])
  );
}

// ============ CADASTRO ============
function loadCad() {
  return JSON.parse(localStorage.getItem('territorial_cad') || 'null') || D.cadastros;
}
function saveCad(x) {
  localStorage.setItem('territorial_cad', JSON.stringify(x));
}
function renderCad() {
  const rows = loadCad();
  q('#cadastro-body').innerHTML = rows
    .map(
      (r, i) =>
        `<tr><td>${esc(r.localidade)}</td><td>${esc(r.tipo)}</td><td>${esc(r.servico)}</td><td>${esc(r.regularidade)}</td><td>${esc(r.fonte)}</td><td><button data-del="${i}">Excluir</button></td></tr>`
    )
    .join('');
  qa('[data-del]').forEach(
    (b) =>
      (b.onclick = () => {
        const x = loadCad();
        x.splice(+b.dataset.del, 1);
        saveCad(x);
        renderCad();
      })
  );
  q('#kpi-localidades').textContent = new Set(rows.map((r) => r.localidade)).size;
}
q('#novo-registro').onclick = () => (q('#cadastro-form').hidden = false);
q('#cancelar-registro').onclick = () => (q('#cadastro-form').hidden = true);
q('#cadastro-form').onsubmit = (e) => {
  e.preventDefault();
  const f = new FormData(e.target),
    x = loadCad();
  x.push({
    localidade: f.get('localidade'),
    tipo: f.get('tipo'),
    servico: f.get('servico'),
    regularidade: f.get('regularidade'),
    fonte: 'Cadastro local',
  });
  saveCad(x);
  e.target.reset();
  e.target.hidden = true;
  renderCad();
};

// ============ BARS (Comparação) ============
function renderBars() {
  q('#bars').innerHTML =
    `<div class="legend"><span><i class="le"></i>Eventos/espaços públicos</span><span><i class="ld"></i>Porta a porta/distritos</span></div>` +
    D.comparacao
      .map(
        (r) =>
          `<div class="bar-row"><div class="bar-label"><strong>${r.nome}</strong><small>${r.n}</small></div><div class="bar-track"><div class="bar-event" style="width:${r.evento}%" title="Eventos: ${r.evento}%"></div><div class="bar-door" style="width:${r.porta}%" title="Porta a porta: ${r.porta}%"></div></div><div><strong>${r.evento}%</strong><br><strong>${r.porta}%</strong></div></div>`
      )
      .join('');
}

// ============ FICHAS METODOLÓGICAS ============
function renderMethods() {
  q('#method-cards').innerHTML = D.metodologias
    .map(
      (m) =>
        `<article><h3>${m.nome}</h3><dl><dt>Definição</dt><dd>${m.def}</dd><dt>Numerador</dt><dd>${m.num}</dd><dt>Denominador</dt><dd>${m.den}</dd><dt>Fonte</dt><dd>${m.fonte}</dd><dt>Atualização</dt><dd>${m.freq}</dd><dt>Limitação</dt><dd>${m.lim}</dd><dt>Uso proibido</dt><dd>${m.proib}</dd></dl></article>`
    )
    .join('');
}

// ============ CONTESTAÇÃO ============
function loadMan() {
  return JSON.parse(localStorage.getItem('territorial_man') || '[]');
}
function renderMan() {
  const x = loadMan();
  q('#manifestacoes').className = x.length ? '' : 'empty';
  q('#manifestacoes').innerHTML = x.length
    ? x
        .map(
          (r) =>
            `<div class="manifestacao"><strong>${esc(r.tipo)} - ${esc(r.localidade)}</strong><br>${esc(r.item)}: ${esc(r.relato)}<br><small>Estado: recebida para revisão</small></div>`
        )
        .join('')
    : 'Nenhuma manifestação registrada neste navegador.';
}
q('#contestacao-form').onsubmit = (e) => {
  e.preventDefault();
  const f = new FormData(e.target),
    x = loadMan();
  x.unshift(Object.fromEntries(f));
  localStorage.setItem('territorial_man', JSON.stringify(x));
  e.target.reset();
  renderMan();
};

// ============ EXPORTAR ============
q('#exportar').onclick = () => {
  const txt = `Painel territorial anonimizado - ficha da visão territorial\nData: ${new Date().toLocaleDateString('pt-BR')}\nAmostra principal: 557 questionários de conveniência\nSegunda onda: 83 questionários\nEstratos públicos agregados: ${q('#kpi-localidades').textContent}\nProteção territorial: ${q('#kpi-cobertura').textContent}\nAlerta: categoria "outro" = 40,2% (>20%).\n\n--- Saneamento (amostra principal) ---\nFossa: 48,6%\nRede pública de esgoto: 47,5%\nColeta municipal de resíduos: 92,6%\nLixo queimado: 8,8%`;
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([txt], { type: 'text/plain' }));
  a.download = 'ficha-territorial-anonimizada.txt';
  a.click();
  URL.revokeObjectURL(a.href);
};

// ============ DIAGNÓSTICO SOCIAL — GRÁFICOS ============

function hbar(items, container, colorClass, wideLabel) {
  const maxVal = Math.max(...items.map((i) => i.pct || i.qtd));
  q(container).innerHTML = items
    .map((item) => {
      const pct = item.pct !== undefined ? item.pct : item.qtd;
      const barW = (pct / Math.max(maxVal, 1)) * 100;
      const label = item.faixa || item.tipo || item.espaco || item.avaliacao || item.destino || item.label || item.nome;
      return `<div class="hbar-row${wideLabel ? ' wide-label' : ''}">
        <div class="hbar-label" title="${esc(label)}">${esc(label)}</div>
        <div class="hbar-track"><div class="hbar-fill ${colorClass}" style="width:0%" data-target="${barW}"></div></div>
        <div class="hbar-pct">${typeof item.pct === 'number' ? item.pct.toFixed(1) + '%' : item.qtd}</div>
      </div>`;
    })
    .join('');
}

function renderDiagnostico() {
  // Renda
  hbar(D.renda, '#chart-renda', 'accent', true);

  // Esgoto
  hbar(D.saneamento.esgoto, '#chart-esgoto', 'teal');

  // Lixo
  hbar(D.saneamento.lixo, '#chart-lixo', 'warn');

  // Moradia
  hbar(D.moradia, '#chart-moradia', 'success');

  // Gestão
  hbar(D.gestaoPrefeitura, '#chart-gestao', 'accent');

  // Composição familiar
  hbar(D.composicaoFamiliar.pessoasPorDomicilio, '#chart-familia', 'teal');

  // Lazer
  hbar(D.lazer, '#chart-lazer', 'success');

  // Melhorias
  hbar(D.pedidosMelhorias, '#chart-melhorias', 'accent');

  // Vulnerabilidade
  const vulnItems = Object.values(D.vulnerabilidade).map((v) => ({
    label: v.label,
    pct: v.pct,
  }));
  hbar(vulnItems, '#chart-vulnerabilidade', 'danger', true);

  // Serviços — stacked bars
  const svcContainer = q('#chart-servicos');
  svcContainer.innerHTML =
    `<div class="stacked-legend">
      <span><i style="background:#2a9d8f"></i> Bom</span>
      <span><i style="background:#e0b94f"></i> Neutro</span>
      <span><i style="background:#c94040"></i> Ruim</span>
      <span><i style="background:#b0bec5"></i> Não sabe</span>
    </div>` +
    D.servicosAvaliacao
      .map((s) => {
        const bomP = ((s.bom / s.n) * 100).toFixed(1);
        const neutroP = ((s.neutro / s.n) * 100).toFixed(1);
        const ruimP = ((s.ruim / s.n) * 100).toFixed(1);
        const nsP = ((s.naoSabe / s.n) * 100).toFixed(1);
        return `<div class="stacked-row">
        <div class="stacked-label">${esc(s.servico)}</div>
        <div class="stacked-track">
          <div class="stacked-seg bom" style="width:0%" data-target="${bomP}" title="Bom: ${bomP}%">${+bomP > 8 ? bomP + '%' : ''}</div>
          <div class="stacked-seg neutro" style="width:0%" data-target="${neutroP}" title="Neutro: ${neutroP}%">${+neutroP > 8 ? neutroP + '%' : ''}</div>
          <div class="stacked-seg ruim" style="width:0%" data-target="${ruimP}" title="Ruim: ${ruimP}%">${+ruimP > 8 ? ruimP + '%' : ''}</div>
          <div class="stacked-seg naosabe" style="width:0%" data-target="${nsP}" title="Não sabe: ${nsP}%">${+nsP > 8 ? nsP + '%' : ''}</div>
        </div>
      </div>`;
      })
      .join('');

  // Animate bars
  requestAnimationFrame(() => {
    setTimeout(animateBars, 50);
  });
}

function animateBars() {
  qa('[data-target]').forEach((el) => {
    el.style.width = el.dataset.target + '%';
  });
}

// ============ INIT ============
renderCad();
renderBars();
renderMethods();
renderMan();
renderDiagnostico();

// Handle tab from hash
const initialTab = (location.hash || '#territorio').slice(1);
tab(initialTab);

// Re-animate bars when switching tabs (for visible bars)
const observer = new MutationObserver(() => {
  setTimeout(animateBars, 100);
});
qa('.panel').forEach((p) =>
  observer.observe(p, { attributes: true, attributeFilter: ['hidden'] })
);

// Service Worker
if ('serviceWorker' in navigator && location.protocol.startsWith('http')) {
  navigator.serviceWorker.register('sw.js');
}
