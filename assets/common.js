// RAG Explainer — shared helpers
function mockHash(s){
  let h=2166136261 >>>0;
  for(let i=0;i<s.length;i++){ h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
  return h >>>0;
}

// Angle-based mock embeddings: each concept cluster owns an orthogonal 8-D axis
// pair; a word sits at angle θ on its cluster plane, so
//   cosine(a,b) = cos(θa − θb)   (same cluster)
//   cosine(a,b) = cosθa·cosθb    (different clusters, B-axes orthogonal)
// → controllable, distinct scores (no 1.00 walls).
const CLUSTER_AXIS = { med:0, ins:2, fruit:4, tra:6 };
// Medical cluster: ≥9° between any pair (hospital 0°, medical center 9°, clinic 18°,
// physician 27°, doctor 36°, medical care center 45°). Plurals alias their singular.
const WORD_ANGLE = {
  // medical
  "hospital":            ["med",  0],
  "medical center":      ["med",  9],
  "medical care center": ["med", 45],
  "clinic":              ["med", 18],
  "doctor":              ["med", 35],
  "physician":           ["med", 27],
  // insurance / policy
  "insurance":           ["ins", 60],
  "policy":              ["ins", 72],
  // fruit
  "apple":               ["fruit", 76],
  "pear":                ["fruit", 88],
  "fruit":               ["fruit", 82],
  // transport
  "car":                 ["tra", 78],
  "vehicle":             ["tra", 88],
};
const PLURAL_ALIAS = { "hospitals": "hospital", "physicians": "physician" };
function axisVector(cluster, deg){
  const r = deg*Math.PI/180;
  const v = new Array(8).fill(0);
  v[CLUSTER_AXIS[cluster]]   = Math.cos(r);
  v[CLUSTER_AXIS[cluster]+1] = Math.sin(r);
  return v;
}
const SYN_VECTORS = {};
for (const w in WORD_ANGLE){
  const [c, d] = WORD_ANGLE[w];
  SYN_VECTORS[w] = axisVector(c, d);
}
for (const p in PLURAL_ALIAS){
  SYN_VECTORS[p] = SYN_VECTORS[PLURAL_ALIAS[p]].slice();
}

function mockEmbed(text){
  const key = text.trim().toLowerCase();
  if(SYN_VECTORS[key]) return SYN_VECTORS[key].slice();
  // fallback: deterministic hash -> sin wave, L2 normalized
  const h = mockHash(key) % 10000;
  const v=[];
  for(let i=0;i<8;i++) v.push(Math.sin((h+1)*(i+1)*0.37) + Math.cos((h+2)*(i+1)*0.61));
  const n=Math.sqrt(v.reduce((a,b)=>a+b*b,0))||1;
  return v.map(x=>x/n);
}
function cosine(a,b){
  let d=0;
  for(let i=0;i<a.length;i++){ d+=a[i]*b[i]; }
  return Math.max(-1,Math.min(1,d));
}
function topK(query, candidates, k=5){
  const q=mockEmbed(query);
  return candidates.filter(c=>c.trim().toLowerCase()!==query.trim().toLowerCase())
    .map(c=>({text:c, score:cosine(q, mockEmbed(c))}))
    .sort((a,b)=>b.score-a.score).slice(0,k);
}
function chunkText(text, size=500, overlap=50){
  const chunks=[];
  let i=0;
  while(i<text.length){
    chunks.push(text.slice(i, i+size));
    if(i+size>=text.length) break;
    i += Math.max(1,(size-overlap));
  }
  return chunks;
}
