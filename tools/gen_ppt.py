#!/usr/bin/env python3
"""
RAG Explainer deck generator — TEMPLATE-BASED (ground truth: tools/template.pptx).
Every infrastructure part is copied byte-for-byte from a file that opens in
PowerPoint (python-pptx fixture txt-text.pptx). Only slide XML is generated,
using that file's own <p:sp> textbox pattern. No hand-written theme/master.
"""
from pathlib import Path
import re, html
from zipfile import ZipFile, ZIP_DEFLATED

HERE = Path(__file__).parent
TEMPLATE = HERE / "template.pptx"
OUT = HERE.parent / "slides" / "rag_explainer.pptx"

def esc(s):
    return html.escape(s, quote=False).replace('"', "&quot;")

def para_xml(p, default_sz=1100):
    if isinstance(p, str):
        p = {"text": p}
    sz = p.get("size", default_sz)
    bold = p.get("bold", False)
    color = p.get("color", "152536")
    text = p.get("text", "")
    if text == "":
        return f'<a:p><a:endParaRPr lang="en-US" sz="{sz}"/></a:p>'
    if p.get("bullet") and not text.startswith("\u2022"):
        text = "\u2022  " + text
    b = ' b="1"' if bold else ""
    out = []
    # split explicit newlines into separate paragraphs
    for chunk in text.split("\n"):
        col = f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
        out.append(
            f'<a:p><a:pPr algn="l"/><a:r><a:rPr lang="en-US" sz="{sz}"{b} dirty="0">{col}</a:rPr>'
            f"<a:t>{esc(chunk)}</a:t></a:r></a:p>"
        )
    return "".join(out)

def box(id_, name, x, y, cx, cy, paragraphs, default_sz=1100):
    body = "".join(para_xml(p, default_sz) for p in paragraphs)
    return (
        f'<p:sp><p:nvSpPr><p:cNvPr id="{id_}" name="{esc(name)}"/>'
        f'<p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
        f'<p:txBody><a:bodyPr wrap="square" rtlCol="0"/><a:lstStyle/>{body}</p:txBody></p:sp>'
    )

GROUP = ('<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
         '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
         '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>')

FOOTER_TEXT = "RAG Explainer  |  Private data stays private  |  uiyuvi.github.io/rag-explainer"

def slide_shapes(d):
    shapes = []
    t = d.get("type")
    if t == "title":
        paras = [{"text": d["title"], "size": 3200, "bold": True, "color": "0A1931"}]
        if d.get("subtitle"):
            paras.append({"text": "", "size": 600})
            paras.append({"text": d["subtitle"], "size": 1300, "color": "5A6C80"})
        shapes.append(box(2, "Title", 500000, 1700000, 11192000, 2000000, paras))
        if d.get("kicker"):
            shapes.append(box(3, "Kicker", 500000, 900000, 11192000, 400000,
                              [{"text": d["kicker"], "size": 1000, "bold": True, "color": "12549E"}]))
    else:
        head = []
        if d.get("kicker"):
            head.append({"text": d["kicker"], "size": 1000, "bold": True, "color": "12549E"})
            head.append({"text": "", "size": 300})
        head.append({"text": d["title"], "size": 2200, "bold": True, "color": "0A1931"})
        shapes.append(box(2, "Header", 360000, 250000, 11472000, 1100000, head))
        if t == "split":
            shapes.append(box(3, "Body", 360000, 1550000, 5800000, 4650000, d["body"]))
            shapes.append(box(4, "Side", 6450000, 1550000, 5380000, 4650000, d["side"]))
        else:
            shapes.append(box(3, "Body", 360000, 1550000, 11472000, 4650000, d["body"]))
    shapes.append(box(9, "Footer", 360000, 6380000, 11472000, 330000,
                      [{"text": FOOTER_TEXT, "size": 800, "color": "5A6C80"}]))
    return "".join(shapes)

def slide_xml(d):
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
        f"<p:cSld><p:spTree>{GROUP}{slide_shapes(d)}</p:spTree></p:cSld>"
        "<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>"
    )

def slide_rels():
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/></Relationships>')

def build():
    tz = ZipFile(TEMPLATE)
    parts = {n: tz.read(n) for n in tz.namelist()}
    n = len(SLIDES)

    # presentation.xml — patch slide list + 16:9 size
    pres = parts["ppt/presentation.xml"].decode()
    ids = "".join(f'<p:sldId id="{255+i}" r:id="rId{i+1}"/>' for i in range(1, n + 1))
    pres = re.sub(r"<p:sldIdLst>.*?</p:sldIdLst>", f"<p:sldIdLst>{ids}</p:sldIdLst>", pres, flags=re.S)
    pres = re.sub(r'(<p:sldSz cx=")\d+(")', r"\g<1>12192000\g<2>", pres)
    parts["ppt/presentation.xml"] = pres.encode()

    # presentation rels — replace slide relationships, keep master/props/theme/tableStyles
    rels = parts["ppt/_rels/presentation.xml.rels"].decode()
    rels = re.sub(r'<Relationship Id="rId\d+" Type="[^"]*/slide" Target="slides/slide\d+\.xml"/>', "", rels)
    slide_rels_xml = "".join(
        f'<Relationship Id="rId{i+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
        for i in range(1, n + 1)
    )
    rels = rels.replace("</Relationships>", slide_rels_xml + "</Relationships>")
    parts["ppt/_rels/presentation.xml.rels"] = rels.encode()

    # content types — replace slide overrides with n of them
    ct = parts["[Content_Types].xml"].decode()
    ct = re.sub(r'<Override PartName="/ppt/slides/slide\d+\.xml"[^>]*/>', "", ct)
    overrides = "".join(
        f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        for i in range(1, n + 1)
    )
    ct = ct.replace("</Types>", overrides + "</Types>")
    parts["[Content_Types].xml"] = ct.encode()

    # core metadata — title/creator only (text nodes)
    core = parts["docProps/core.xml"].decode()
    core = re.sub(r"<dc:title>.*?</dc:title>", "<dc:title>RAG Explainer - Build Your Personal Document Assistant</dc:title>", core, flags=re.S)
    core = re.sub(r"<dc:creator>.*?</dc:creator>", "<dc:creator>RAG Explainer</dc:creator>", core, flags=re.S)
    core = re.sub(r"<cp:lastModifiedBy>.*?</cp:lastModifiedBy>", "<cp:lastModifiedBy>RAG Explainer</cp:lastModifiedBy>", core, flags=re.S)
    parts["docProps/core.xml"] = core.encode()

    # generate slides + rels
    for i, d in enumerate(SLIDES, start=1):
        parts[f"ppt/slides/slide{i}.xml"] = slide_xml(d).encode()
        parts[f"ppt/slides/_rels/slide{i}.xml.rels"] = slide_rels().encode()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    order = ["[Content_Types].xml"] + [k for k in parts if k != "[Content_Types].xml"]
    with ZipFile(OUT, "w", ZIP_DEFLATED) as z:
        for name in order:
            z.writestr(name, parts[name])
    print(f"Generated {OUT} ({n} slides, template-based)")

SLIDES = [
  # 1 Title
  {"type":"title", "title":"Build Your Personal\nDocument Assistant", "subtitle":"How AI answers from data it was never trained on — the RAG technique behind private PDFs", "notes":"Welcome. Today we demystify how AI reads your private documents. One example, full pipeline, zero magic."},
  # 2 Agenda
  {"type":"header_body_side", "kicker":"AGENDA  •  25 MINUTES", "title":"Our Journey Today", "body":[
    {"text":"The Problem  —  5 min", "size":1300, "bold":True, "color":"12549E"},
    {"text":"Why searching with exact words fails. See it live.", "size":1000, "color":"5A6C80"},
    {"text":"", "size":600},
    {"text":"The Flow  —  15 min", "size":1300, "bold":True, "color":"12549E"},
    {"text":"How Vector Search works, step-by-step.\nOne insurance PDF, end-to-end.", "size":1000, "color":"5A6C80"},
    {"text":"", "size":600},
    {"text":"The Value  —  5 min", "size":1300, "bold":True, "color":"12549E"},
    {"text":"Benefits, limits, where to use it,\nand live demos on your phone.", "size":1000,"color":"5A6C80"},
  ], "side":[
    {"text":"You will scan, not just listen.", "size":1100, "bold":True, "color":"0A1931"},
    {"text":"", "size":400},
    {"text":"Ask a question → see which chunk\nis closest in meaning → see the answer with citations.", "size":950,"color":"5A6C80"},
    {"text":"", "size":400},
    {"text":"QR at the end → all demos + further reading.", "size":900,"color":"12549E","bold":True},
  ]},
  # 3 Why keyword fails
  {"type":"header_body_side", "kicker":"THE PROBLEM", "title":"Why Normal Search Is Not Enough", "body":[
    {"text":"The “Keyword” Problem", "size":1400,"bold":True,"color":"12549E"},
    {"text":"", "size":400},
    {"text":"✘  Search looks for exact words only.", "size":1050},
    {"text":"✘  You ask for “Hospitals” → it misses “Medical Centers.”", "size":1050},
    {"text":"✘  It does not understand meaning.", "size":1050},
    {"text":"", "size":400},
    {"text":"Demo in your hand: try it now →", "size":1000,"bold":True,"color":"12549E"},
    {"text":"01_keyword_vs_vector.html", "size":900,"color":"5A6C80"},
  ], "side":[
    {"text":"Analogy — The Receptionist", "size":1100,"bold":True,"color":"0A1931"},
    {"text":"", "size":300},
    {"text":"You ask: “Is there a doctor available?”", "size":950,"color":"5A6C80"},
    {"text":"Reply: “No, only Physicians on duty.”", "size":950,"color":"5A6C80"},
    {"text":"", "size":300},
    {"text":"Keywords are literal.\nHumans are semantic.", "size":1000,"bold":True,"color":"0A1931"},
    {"text":"We need meaning, not letters.", "size":950,"color":"12549E"},
  ]},
  # 4 Example
  {"type":"header_body_side", "kicker":"RUNNING EXAMPLE", "title":"Our Example: The 50-Page Insurance PDF", "body":[
    {"text":"Imagine you have a 50-page policy.\nYou need one answer, fast.", "size":1050,"color":"5A6C80"},
    {"text":"", "size":400},
    {"text":"User asks:", "size":1000,"bold":True,"color":"0A1931"},
    {"text":"“Which hospitals are covered\nin this policy?”", "size":1300,"bold":True,"color":"12549E"},
    {"text":"", "size":400},
    {"text":"We will follow this ONE question through every step.", "size":950,"color":"5A6C80"},
  ], "side":[
    {"text":"HEALTH INSURANCE POLICY", "size":900,"bold":True,"color":"0A1931"},
    {"text":"Schedule of Network Providers & User Query", "size":800,"color":"5A6C80"},
    {"text":"", "size":300},
    {"text":"• 50 pages, tables, scanned images\n• Legal language\n• Stays in your system — private", "size":900,"color":"5A6C80"},
    {"text":"", "size":300},
    {"text":"This question card stays visible on every next slide.", "size":900,"color":"12549E"},
  ]},
  # 5 Big Picture
  {"type":"full", "kicker":"BIG PICTURE", "title":"The Architecture — One Flow", "body":[
    {"text":"PDF Policy  →  Chunking  →  Encoder  →  Vector DB  →  LLM Answer", "size":1150,"bold":True,"color":"0A1931"},
    {"text":"", "size":300},
    {"text":"We turn text into Meaning Fingerprints (Vectors), store them, find the closest match to your question, and let the AI write the answer.", "size":1000,"color":"5A6C80"},
    {"text":"", "size":400},
    {"text":"Next 9 slides = each box, with the same insurance question.", "size":950,"color":"12549E","bold":True},
  ]},
  # 6 Step1
  {"type":"header_body_side", "kicker":"STEP 1  •  DOCUMENT INPUT", "title":"Reading Your Source Files", "body":[
    {"text":"The system reads source files as the single source of truth.", "size":1050,"color":"5A6C80"},
    {"text":"", "size":300},
    {"text":"•  Reads text, tables and images (OCR if scanned)", "size":1000, "bullet":True},
    {"text":"•  Keeps data in your system — secure, private", "size":1000, "bullet":True},
    {"text":"•  Extracts every word to prepare for the next step", "size":1000, "bullet":True},
  ], "side":[
    {"text":"What it does NOT do: “look” like you do.", "size":1000,"bold":True,"color":"0A1931"},
    {"text":"It extracts, not views. Errors here (blurry PDF) → wrong answers later.", "size":950,"color":"5A6C80"},
    {"text":"", "size":400},
    {"text":"For Builders: OCR + layout parsing.", "size":900,"color":"EF413D","bold":True},
  ]},
  # 7 Step2 Chunking
  {"type":"header_body_side", "kicker":"STEP 2  •  CHUNKING", "title":"Cutting the Baguette", "body":[
    {"text":"50 pages is too big to digest at once.", "size":1050,"color":"5A6C80"},
    {"text":"We cut it into small “chunks” (paragraphs).", "size":1050,"color":"0A1931","bold":True},
    {"text":"", "size":300},
    {"text":"•  Ensures we find the exact page you need", "size":1000,"bullet":True},
    {"text":"•  Example: 500 characters + 50 overlap", "size":1000,"bullet":True},
    {"text":"•  Too small → loses context. Too big → misses precision.", "size":1000,"bullet":True},
  ], "side":[
    {"text":"Analogy — French Baguette", "size":1100,"bold":True,"color":"0A1931"},
    {"text":"Cut a long baguette into slices to find the slice with the most garlic.", "size":950,"color":"5A6C80"},
    {"text":"", "size":300},
    {"text":"Try: demos/02_chunk_lab.html → move the slider.", "size":900,"color":"12549E","bold":True},
  ]},
  # 8 Step3+4 Embeddings
  {"type":"header_body_side", "kicker":"STEP 3+4  •  EMBEDDINGS & VECTORS", "title":"Meaning Fingerprints", "body":[
    {"text":"The Encoder turns each chunk into a list of numbers — a Vector.", "size":1050,"color":"0A1931","bold":True},
    {"text":"These numbers represent concept, not letters.", "size":1000,"color":"5A6C80"},
    {"text":"", "size":300},
    {"text":"Similar meanings → similar numbers.", "size":1000,"bold":True,"color":"12549E"},
    {"text":"“St. Jude’s Hospital” ≈ “Medical Care Center” (0.92)\n“St. Jude’s Hospital” ≠ “Car” (0.03)", "size":950,"color":"5A6C80"},
    {"text":"", "size":300},
    {"text":"Think: coordinates on a map of all human knowledge.", "size":900,"color":"5A6C80"},
  ], "side":[
    {"text":"2-D Map (demo)", "size":1000,"bold":True,"color":"0A1931"},
    {"text":"Hospital • near • Medical Center\nFar from • Car, Apple", "size":950,"color":"5A6C80"},
    {"text":"", "size":300},
    {"text":"Scan → demos/03_vector_map.html\nType a word → see closest match.", "size":900,"color":"12549E","bold":True},
    {"text":"For Builders: 768-D, cosine similarity.", "size":900,"color":"EF413D"},
  ]},
  # 9 Step5 Vector DB
  {"type":"header_body_side", "kicker":"STEP 5  •  VECTOR DATABASE", "title":"The Smart Library", "body":[
    {"text":"A storage system for all fingerprints.", "size":1050,"color":"0A1931"},
    {"text":"", "size":200},
    {"text":"•  Groups related topics together", "size":1000,"bullet":True},
    {"text":"•  Finds matches in milliseconds, even for 10,000 pages", "size":1000,"bullet":True},
    {"text":"•  When you ask, it ranks every chunk by meaning", "size":1000,"bullet":True},
  ], "side":[
    {"text":"Analogy — Hyper-Organized Library", "size":1100,"bold":True,"color":"0A1931"},
    {"text":"All books about “Fruit” on the same shelf,\neven if one says “Apple” and one “Pear”.", "size":950,"color":"5A6C80"},
    {"text":"", "size":300},
    {"text":"No training needed — just file the fingerprints.", "size":950,"color":"12549E","bold":True},
  ]},
  # 10 Step6+7 Query + Search
  {"type":"header_body_side", "kicker":"STEP 6+7  •  QUERY & SEARCH", "title":"The “Closest Match” Game", "body":[
    {"text":"You ask: “Which hospitals are covered?”", "size":1100,"bold":True,"color":"12549E"},
    {"text":"System makes a fingerprint for the question too.", "size":1000,"color":"5A6C80"},
    {"text":"", "size":300},
    {"text":"Then compares → pulls Top-K (best 3-4 chunks).", "size":1000,"color":"0A1931","bold":True},
    {"text":"Ignores 40 pages of legal fluff.", "size":1000,"color":"5A6C80"},
    {"text":"", "size":300},
    {"text":"Try: demos/04_similarity_rank.html → Top-K slider.", "size":900,"color":"12549E"},
  ], "side":[
    {"text":"Scores (cosine)", "size":1000,"bold":True,"color":"0A1931"},
    {"text":"• Chunk 12: City General ...  0.93", "size":950,"color":"5A6C80"},
    {"text":"• Chunk 08: St. Jude’s ... 0.91", "size":950,"color":"5A6C80"},
    {"text":"• Chunk 31: Westside ... 0.84", "size":950,"color":"5A6C80"},
    {"text":"• Chunk 02: Legal disclaimer  0.12", "size":950,"color":"5A6C80"},
    {"text":"", "size":300},
    {"text":"For Builders: cosine = dot / |a||b|.", "size":900,"color":"EF413D"},
  ]},
  # 11 Step8 Context
  {"type":"header_body_side", "kicker":"STEP 8  •  FEEDING THE EXPERT", "title":"The Lawyer’s Desk", "body":[
    {"text":"We give the LLM (AI brain) ONLY the relevant chunks.", "size":1050,"color":"0A1931","bold":True},
    {"text":"", "size":300},
    {"text":"•  Not the whole 50 pages — just 3 pages", "size":1000,"bullet":True},
    {"text":"•  Fits in the token window (e.g., 4,096 tokens)", "size":1000,"bullet":True},
    {"text":"•  LLM reads → writes a clear answer", "size":1000,"bullet":True},
  ], "side":[
    {"text":"Analogy — Lawyer", "size":1100,"bold":True,"color":"0A1931"},
    {"text":"Give a lawyer only the 3 pages they need,\nnot the whole box of files.", "size":950,"color":"5A6C80"},
    {"text":"", "size":300},
    {"text":"Try: demos/05_context_window.html\nDrag chunks until the window fills.", "size":900,"color":"12549E","bold":True},
  ]},
  # 12 Step9 Answer
  {"type":"full", "kicker":"STEP 9  •  ANSWER", "title":"A Natural Response — With Citations", "body":[
    {"text":"AI says:", "size":1100,"bold":True,"color":"0A1931"},
    {"text":"“According to your policy (p.12, p.8, p.31), you are covered at City General, St. Jude’s Medical Center, and Westside Health.”", "size":1100,"color":"12549E"},
    {"text":"", "size":400},
    {"text":"Grounded: answer + sources. You can verify.      Try end-to-end: demos/06_e2e_rag.html", "size":1000,"color":"5A6C80"},
  ]},
  # 13 Failure modes
  {"type":"full", "kicker":"TRUST  •  FAILURE MODES", "title":"When It Goes Wrong", "body":[
    {"text":"If retrieval misses → LLM may hallucinate. We mitigate:", "size":1050,"color":"0A1931","bold":True},
    {"text":"", "size":300},
    {"text":"•  Blurry PDF → OCR errors → wrong vectors → check scans          •  Mitigate: OCR + human review", "size":950,"bullet":True},
    {"text":"•  Chunks too small → big picture lost                             •  Mitigate: 50 overlap", "size":950,"bullet":True},
    {"text":"•  No relevant chunk in Top-K → model guesses                      •  Mitigate: show “No answer found” + citations", "size":950,"bullet":True},
    {"text":"", "size":300},
    {"text":"Try: demos/07_limits.html — make it fail, then fix it.", "size":950,"color":"12549E","bold":True},
  ]},
  # 14 Benefits vs Limits
  {"type":"header_body_side", "kicker":"THE VALUE", "title":"Benefits & Limitations", "body":[
    {"text":"Benefits", "size":1200,"bold":True,"color":"12549E"},
    {"text":"✓  Semantic: “Physician” = “Doctor”", "size":1000,"bullet":True},
    {"text":"✓  Speed: right page in milliseconds", "size":1000,"bullet":True},
    {"text":"✓  No training: add a PDF, ready", "size":1000,"bullet":True},
    {"text":"✓  Private & grounded with page refs", "size":1000,"bullet":True},
  ], "side":[
    {"text":"Limitations", "size":1200,"bold":True,"color":"EF413D"},
    {"text":"•  Data quality in → quality out", "size":1000,"bullet":True},
    {"text":"•  Cost: embedding = compute", "size":1000,"bullet":True},
    {"text":"•  Small chunks → lost context", "size":1000,"bullet":True},
    {"text":"•  Update → re-chunk & re-embed that file", "size":1000,"bullet":True},
  ]},
  # 14b Use Cases
  {"type":"full", "kicker":"INDUSTRY — HIGH LEVEL", "title":"Where RAG Is Used Today (Generic)", "body":[
    {"text":"Customer Support — manuals + tickets → cited answer  •  Healthcare — records → private assistant", "size":950},
    {"text":"Finance / Insurance — policies, claims → “what is covered?”  •  Legal — contracts → “find risky clause + page”", "size":950},
    {"text":"Education — textbooks → Q&A with sources  •  Enterprise — handbooks → “leave policy?”", "size":950},
    {"text":"", "size":300},
    {"text":"Same pattern: private docs + question → grounded answer with citations. All need re-processing on update.", "size":950,"color":"12549E","bold":True},
  ]},
  # 14c Beyond Basic RAG
  {"type":"full", "kicker":"BEYOND BASIC RAG  •  2 LINES EACH", "title":"When to Level Up", "body":[
    {"text":"Basic RAG (today)  —  Split → embed → Top-K → answer.  On update: re-chunk + re-embed only that file. Cheapest, fastest.", "size":950,"color":"0A1931","bold":True},
    {"text":"", "size":200},
    {"text":"GraphRAG  —  Builds entity graph (Hospital ↔ covers ↔ City). On update: rebuild graph. Good for “how are X and Y connected?” but heavy.", "size":950},
    {"text":"", "size":200},
    {"text":"Agentic RAG  —  Agent loops: search → check → search again → answer. No extra storage, but slower + higher token cost. For multi-hop questions.", "size":950},
    {"text":"", "size":200},
    {"text":"All 3 require re-processing on change — Basic cheapest per file.", "size":900,"color":"EF413D","bold":True},
  ]},
  # 15 Key Takeaway
  {"type":"full", "kicker":"KEY TAKEAWAY", "title":"Finding Answers Is Now Like Asking a Friend", "body":[
    {"text":"Vector search lets computers understand the human meaning of your documents.", "size":1150,"color":"0A1931","bold":True},
    {"text":"", "size":300},
    {"text":"Not letters — meaning. With citations you can trust.", "size":1100,"color":"5A6C80"},
    {"text":"", "size":400},
    {"text":"Scan now → try the closest-match map on your phone.", "size":1000,"color":"12549E","bold":True},
  ]},
  # 16 Go Further + Thank You
  {"type":"full", "kicker":"GO FURTHER  •  SCAN AFTER SESSION", "title":"Explore Later — One QR", "body":[
    {"text":"resources.html — separate file, one QR, all links:", "size":1000,"bold":True,"color":"0A1931"},
    {"text":"•  Visualize real embeddings — TensorFlow Projector (your enwiki skipgram link)", "size":900,"bullet":True},
    {"text":"•  Modern alternative — Embedding Atlas (Apple, lighter)", "size":900,"bullet":True},
    {"text":"•  Why it works — Sentence-Transformers / all-MiniLM docs", "size":900,"bullet":True},
    {"text":"•  Store at scale — Vector DB intro (Pinecone / Chroma)", "size":900,"bullet":True},
    {"text":"•  Pattern — RAG from scratch + GraphRAG / Agentic RAG", "size":900,"bullet":True},
    {"text":"", "size":300},
    {"text":"QR → https://uiyuvi.github.io/rag-explainer/resources.html   •   THANK YOU — Q&A", "size":1000,"color":"12549E","bold":True},
  ]},
]

if __name__ == "__main__":
    build()
