// RAG Explainer — shared helpers
function mockHash(s){
  let h=2166136261 >>>0;
  for(let i=0;i<s.length;i++){ h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>>0;
}
// Deterministic mock embedding — 8 dims, L2 normalized
// Synonym map makes demo clusters intuitive (Hospital ≈ Medical Center)
const SYNONYM_MAP = {
  "hospital": [0.90,0.12,0.05,0.10,0.30,0.10,0.20,0.15],
  "hospitals": [0.90,0.12,0.05,0.10,0.30,0.10,0.20,0.15],
  "medical center": [0.88,0.13,0.06,0.11,0.31,0.09,0.21,0.14],
  "medical centre": [0.88,0.13,0.06,0.11,0.31,0.09,0.21,0.14],
  "clinic": [0.86,0.15,0.07,0.09,0.28,0.11,0.19,0.16],
  "doctor": [0.84,0.18,0.04,0.08,0.26,0.13,0.17,0.12],
  "physician": [0.83,0.19,0.04,0.07,0.27,0.12,0.18,0.13],
  "physicians": [0.83,0.19,0.04,0.07,0.27,0.12,0.18,0.13],
  "apple": [0.10,0.90,0.12,0.80,0.05,0.02,0.10,0.05],
  "pear": [0.12,0.88,0.13,0.79,0.06,0.03,0.09,0.06],
  "fruit": [0.11,0.91,0.10,0.82,0.04,0.02,0.11,0.04],
  "car": [0.05,0.10,0.92,0.05,0.85,0.90,0.06,0.04],
  "vehicle": [0.06,0.09,0.90,0.06,0.84,0.88,0.07,0.05],
  "insurance": [0.70,0.20,0.10,0.15,0.60,0.20,0.40,0.30],
  "policy": [0.68,0.22,0.09,0.14,0.58,0.21,0.38,0.31],
};

function mockEmbed(text){
  const key = text.trim().toLowerCase();
  if(SYNONYM_MAP[key]){
    const v=SYNONYM_MAP[key].slice();
    const n=Math.sqrt(v.reduce((a,b)=>a+b*b,0));
    return v.map(x=>x/n);
  }
  // fallback: hash -> sin wave
  let h = mockHash(key) % 10000;
  const v=[];
  for(let i=0;i<8;i++) v.push(Math.sin((h+1)*(i+1)*0.37) + Math.cos((h+2)*(i+1)*0.61));
  const n=Math.sqrt(v.reduce((a,b)=>a+b*b,0))||1;
  return v.map(x=>x/n);
}
function cosine(a,b){
  let d=0, na=0, nb=0;
  for(let i=0;i<a.length;i++){ d+=a[i]*b[i]; }
  // vectors already normalized -> dot
  return Math.max(-1,Math.min(1,d));
}
function topK(query, candidates, k=5){
  const q=mockEmbed(query);
  return candidates.map(c=>({text:c, score:cosine(q, mockEmbed(c))})).sort((a,b)=>b.score-a.score).slice(0,k);
}
function chunkText(text, size=500, overlap=50){
  const chunks=[];
  let i=0;
  while(i<text.length){
    chunks.push(text.slice(i, i+size));
    if(i+size>=text.length) break;
    i += (size-overlap);
  }
  return chunks;
}
function confettiBurst(){ /* lightweight */ 
  const c=document.createElement('div');
  c.textContent='✨';
  c.style.position='fixed';c.style.left='50%';c.style.top='40%';c.style.fontSize='32px';c.style.pointerEvents='none';c.style.transform='translate(-50%,-50%)';
  document.body.appendChild(c); setTimeout(()=>c.remove(),900);
}
