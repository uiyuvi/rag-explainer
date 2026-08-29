// Shared pipeline navigator — 8 steps (Encoder+Vector merged → Embeddings), clickable, highlight current
const PIPELINE = [
  {id:'ingest',    label:'Ingest',     demo:'01_keyword_vs_vector.html', desc:'Reads your PDF — text, tables, images — as the single source of truth.'},
  {id:'chunking',  label:'Chunking',   demo:'02_chunk_lab.html',         desc:'Cuts the 50-page policy into slices (chunks) so we can find the exact page.'},
  {id:'embeddings',label:'Embeddings', demo:'03_vector_map.html',        desc:'Turns slices into Meaning Fingerprints — similar meanings get similar numbers (Encoder + Vector).'},
  {id:'vectordb',  label:'Vector DB',  demo:'04b_vectordb.html',         desc:'Smart library — groups fingerprints so “Hospital” sits near “Medical Center”. No search here, just storage.'},
  {id:'query',     label:'Query',      demo:'04_similarity_rank.html',   desc:'Your question also becomes a fingerprint.'},
  {id:'search',    label:'Search',     demo:'04_similarity_rank.html',   desc:'Closest-match game — ranks every slice by meaning.'},
  {id:'context',   label:'Context',    demo:'05_context_window.html',    desc:'Lawyer’s desk — gives the AI only the 3 best slices (fits the token window).'},
  {id:'answer',    label:'Answer',     demo:'06_e2e_rag.html',           desc:'Grounded answer with citations — verify the page.'},
];

function renderPipeline(currentId, containerId='pipeline'){
  const el=document.getElementById(containerId);
  if(!el) return;
  const isDemos = location.pathname.includes('/demos/');
  const base = isDemos ? '' : 'demos/';
  const homeBase = isDemos ? '../' : '';
  const stepsHtml = PIPELINE.map(s=>{
    const active = s.id===currentId ? ' active' : '';
    const href = base + s.demo;
    return `<a class="pipe-step${active}" href="${href}" title="${s.desc}">${s.label}</a>`;
  }).join('<span class="pipe-arrow">→</span>');

  const cur = PIPELINE.find(s=>s.id===currentId);
  const desc = cur ? `<div class="pipe-desc"><strong>★ You are here: ${cur.label}</strong> — ${cur.desc}</div>` : `<div class="pipe-desc">Tap any step to visualise it — same 8 as the PPT.</div>`;

  el.innerHTML = `
    <div class="pipeline-wrap">
      <div class="pipeline">${stepsHtml}</div>
      ${desc}
      <div style="margin-top:6px;font-size:11px;color:#5A6C80">Tap a step to jump — 8 steps, no numbers. <a href="${homeBase}resources.html" style="font-weight:700">Resources</a> for links. • <a href="${base}06_e2e_rag.html" style="font-weight:700">End-to-end</a></div>
    </div>
  `;
}
window.renderPipeline = renderPipeline;
// For overview pages (index) that want to show pipeline without highlight
window.renderPipelineOverview = function(containerId='pipeline'){
  renderPipeline('', containerId);
}
