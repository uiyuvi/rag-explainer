// Shared pipeline navigator — 9 steps, clickable, highlight current
const PIPELINE = [
  {id:'ingest',  label:'Ingest',    demo:'01_keyword_vs_vector.html', desc:'Reads your PDF — text, tables, images — as the single source of truth.'},
  {id:'chunking',label:'Chunking',  demo:'02_chunk_lab.html',         desc:'Cuts the 50-page policy into slices (chunks) so we can find the exact page.'},
  {id:'encoder', label:'Encoder',   demo:'03_vector_map.html',        desc:'Magic translator — turns each slice into numbers.'},
  {id:'vector',  label:'Vector',    demo:'03_vector_map.html',        desc:'Meaning Fingerprint — similar meanings get similar numbers.'},
  {id:'vectordb',label:'Vector DB', demo:'04_similarity_rank.html',   desc:'Smart library — groups related fingerprints so “Hospital” sits near “Medical Center”.'},
  {id:'query',   label:'Query',     demo:'04_similarity_rank.html',   desc:'Your question also becomes a fingerprint.'},
  {id:'search',  label:'Search',    demo:'04_similarity_rank.html',   desc:'Closest-match game — ranks every slice by meaning.'},
  {id:'context', label:'Context',   demo:'05_context_window.html',    desc:'Lawyer’s desk — gives the AI only the 3 best slices (fits the token window).'},
  {id:'answer',  label:'Answer',    demo:'06_e2e_rag.html',           desc:'Grounded answer with citations — verify the page.'},
];

function renderPipeline(currentId, containerId='pipeline'){
  const el=document.getElementById(containerId);
  if(!el) return;
  const isDemos = location.pathname.includes('/demos/');
  const base = isDemos ? '' : 'demos/';
  const homeBase = isDemos ? '../' : '';
  const stepsHtml = PIPELINE.map(s=>{
    const active = s.id===currentId ? ' active' : '';
    // group encoder+vector as one visual when current is either
    const isEncoderGroup = (currentId==='encoder' || currentId==='vector') && (s.id==='encoder' || s.id==='vector');
    const cls = isEncoderGroup ? ' active' : active;
    const href = base + s.demo;
    // for current, keep clickable but style as active
    return `<a class="pipe-step${cls}" href="${href}" title="${s.desc}">${s.label}</a>`;
  }).join('<span class="pipe-arrow">→</span>');

  const cur = PIPELINE.find(s=>s.id===currentId);
  const desc = cur ? `<div class="pipe-desc"><strong>★ You are here: ${cur.label}</strong> — ${cur.desc}</div>` : `<div class="pipe-desc">Tap any step to visualise it — you don’t need the PPT.</div>`;
  // add overview link for e2e
  const endLinks = currentId==='answer' || currentId==='search' ? '' : `<a class="pipe-step" href="${base}06_e2e_rag.html" style="background:#EFF6FF;border-color:#12549E">End-to-end</a>`;

  el.innerHTML = `
    <div class="pipeline-wrap">
      <div class="pipeline">${stepsHtml}</div>
      ${desc}
      <div style="margin-top:6px;font-size:11px;color:#5A6C80">Tap a step to jump — same 9 as the PPT, no numbers to memorise. <a href="${homeBase}resources.html" style="font-weight:700">Resources</a> for links.</div>
    </div>
  `;
}
// expose
window.renderPipeline = renderPipeline;
