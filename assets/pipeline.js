// Shared pipeline navigator — 8 steps (Encoder+Vector merged → Embeddings), clickable, highlight current
const PIPELINE = [
  {id:'ingest',    label:'Ingest',     demo:'00_ingest.html',            anchor:'',        desc:'Reads your PDF — text, tables, images. Model: OCR (only for scanned pages).'},
  {id:'chunking',  label:'Chunking',   demo:'02_chunk_lab.html',         anchor:'',        desc:'Cuts the 50-page policy into slices so we can find the exact page. No model — plain code.'},
  {id:'embeddings',label:'Embeddings', demo:'03_vector_map.html',        anchor:'',        desc:'Turns slices into Meaning Fingerprints — similar meanings get similar numbers. Model: embedding model.'},
  {id:'vectordb',  label:'Vector DB',  demo:'04b_vectordb.html',         anchor:'',        desc:'Smart library — groups fingerprints so “Hospital” sits near “Medical Center”. No model — storage only.'},
  {id:'query',     label:'Query',      demo:'04a_query.html',            anchor:'',        desc:'Your question also becomes a fingerprint. Model: same embedding model as the slices.'},
  {id:'search',    label:'Search',     demo:'04_similarity_rank.html',   anchor:'',        desc:'Ranks every slice by meaning. No model — cosine math.'},
  {id:'context',   label:'Context',    demo:'05_context_window.html',    anchor:'',        desc:'Lawyer’s desk — assembles the winning slices into the LLM’s reading window. No model — assembly.'},
  {id:'answer',    label:'Answer',     demo:'06_e2e_rag.html',           anchor:'',        desc:'Model: LLM — reads the slices, writes the answer with citations. The only step where the LLM works.'},
];

function renderPipeline(currentId, containerId='pipeline'){
  const el=document.getElementById(containerId);
  if(!el) return;
  const isDemos = location.pathname.includes('/demos/');
  const base = isDemos ? '' : 'demos/';
  const homeBase = isDemos ? '../' : '';
  const stepsHtml = PIPELINE.map(s=>{
    const active = s.id===currentId ? ' active' : '';
    const href = base + s.demo + s.anchor;
    return `<a class="pipe-step${active}" href="${href}" title="${s.desc}">${s.label}</a>`;
  }).join('<span class="pipe-arrow">→</span>');

  const cur = PIPELINE.find(s=>s.id===currentId);
  const desc = cur ? `<div class="pipe-desc"><strong>You are here: ${cur.label}</strong> — ${cur.desc}</div>` : `<div class="pipe-desc">Tap any step to visualise it.</div>`;

  el.innerHTML = `
    <div class="pipeline-wrap">
      <div class="pipeline">${stepsHtml}</div>
      ${desc}
      <div style="margin-top:6px;font-size:11px;color:#9C4B47">Tap a step to jump — no numbers to memorise. <a href="${homeBase}resources.html" style="font-weight:700">Resources</a> for links. • <a href="${base}06_e2e_rag.html" style="font-weight:700">End-to-end</a></div>
    </div>
  `;
}
window.renderPipeline = renderPipeline;
// For overview pages (index) that want to show pipeline without highlight
window.renderPipelineOverview = function(containerId='pipeline'){
  renderPipeline('', containerId);
}
