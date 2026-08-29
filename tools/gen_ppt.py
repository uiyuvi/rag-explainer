#!/usr/bin/env python3
"""
RAG Explainer — TCS France PPT Generator (pure stdlib, no python-pptx)
Generates slides/rag_explainer.pptx with 17 slides, TCS theme, mobile-ready narrative.
Stdlib only: zipfile + xml escaping. Based on images_to_pptx ZipFile pattern.
"""
from pathlib import Path
import html
from datetime import datetime, timezone
from zipfile import ZipFile, ZIP_DEFLATED

SLIDE_WIDTH_EMU = 12192000
SLIDE_HEIGHT_EMU = 6858000
OUT = Path(__file__).parent.parent / "slides" / "rag_explainer.pptx"

def xml_escape(s): return html.escape(s, quote=True)

# Reuse core XML helpers adapted from images_to_pptx.py (no image deps)
def content_types_xml(n):
    overrides = "\n".join(f'  <Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>' for i in range(1, n+1))
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Default Extension="png" ContentType="image/png"/>
  <Default Extension="jpg" ContentType="image/jpeg"/>
  <Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
  <Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/presProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presProps+xml"/>
  <Override PartName="/ppt/viewProps.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.viewProps+xml"/>
  <Override PartName="/ppt/tableStyles.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.tableStyles+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
{overrides}
</Types>
'''

def root_rels_xml():
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
  <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
  <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>
'''

def app_xml(n):
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
  <Application>rag_explainer</Application>
  <PresentationFormat>On-screen Show (16:9)</PresentationFormat>
  <Slides>{n}</Slides><Notes>0</Notes><HiddenSlides>0</HiddenSlides><MMClips>0</MMClips><ScaleCrop>false</ScaleCrop>
  <HeadingPairs><vt:vector size="2" baseType="variant"><vt:variant><vt:lpstr>Slides</vt:lpstr></vt:variant><vt:variant><vt:i4>{n}</vt:i4></vt:variant></vt:vector></HeadingPairs>
  <TitlesOfParts><vt:vector size="{n}" baseType="lpstr">{''.join(f'<vt:lpstr>Slide {i}</vt:lpstr>' for i in range(1,n+1))}</vt:vector></TitlesOfParts>
  <Company>TCS France</Company><LinksUpToDate>false</LinksUpToDate><SharedDoc>false</SharedDoc><HyperlinksChanged>false</HyperlinksChanged><AppVersion>16.0000</AppVersion>
</Properties>
'''

def core_xml(title):
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00","Z")
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <dc:title>{xml_escape(title)}</dc:title><dc:creator>TCS France – RAG Explainer</dc:creator><cp:lastModifiedBy>TCS France</cp:lastModifiedBy>
  <dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created><dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>
'''

def presentation_xml(n):
    ids = "\n".join(f'    <p:sldId id="{255+i}" r:id="rId{i+1}"/>' for i in range(1,n+1))
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst>
  <p:sldIdLst>
{ids}
  </p:sldIdLst>
  <p:sldSz cx="{SLIDE_WIDTH_EMU}" cy="{SLIDE_HEIGHT_EMU}" type="wide"/><p:notesSz cx="6858000" cy="9144000"/><p:defaultTextStyle/>
</p:presentation>
'''

def presentation_rels_xml(n):
    rels = "\n".join(f'  <Relationship Id="rId{i+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>' for i in range(1,n+1))
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>
{rels}
  <Relationship Id="rId{n+2}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/presProps" Target="presProps.xml"/>
  <Relationship Id="rId{n+3}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/viewProps" Target="viewProps.xml"/>
  <Relationship Id="rId{n+4}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/tableStyles" Target="tableStyles.xml"/>
</Relationships>
'''

def pres_props_xml(): return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:presentationPr xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"/>'''
def view_props_xml(): return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:viewPr xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"><p:normalViewPr><p:restoredLeft sz="15620"/><p:restoredTop sz="94660"/></p:normalViewPr><p:slideViewPr><p:cSldViewPr><p:cViewPr varScale="1"><p:scale><a:sx n="100" d="100"/><a:sy n="100" d="100"/></p:scale><p:origin x="0" y="0"/></p:cViewPr><p:guideLst/></p:cSldViewPr></p:slideViewPr><p:notesTextViewPr><p:cViewPr><p:scale><a:sx n="100" d="100"/><a:sy n="100" d="100"/></p:scale><p:origin x="0" y="0"/></p:cViewPr></p:notesTextViewPr><p:gridSpacing cx="72008" cy="72008"/></p:viewPr>'''
def table_styles_xml(): return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><a:tblStyleLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" def="{5C22544A-7EE6-4342-B048-85BDC9FD1C3A}"/>'''
def slide_master_rels_xml(): return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/><Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/></Relationships>'''
def slide_layout_rels_xml(): return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/></Relationships>'''

def group_xml(): return '''      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'''

def slide_master_xml(): return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:bg><p:bgRef idx="1001"><a:schemeClr val="bg1"/></p:bgRef></p:bg><p:spTree>{group_xml()}</p:spTree></p:cSld>
  <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles>
</p:sldMaster>'''

def slide_layout_xml(): return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1">
  <p:cSld name="Blank"><p:spTree>{group_xml()}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>'''

def theme_xml():
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="TCS France">
  <a:themeElements>
    <a:clrScheme name="TCS">
      <a:dk1><a:srgbClr val="0A1931"/></a:dk1>
      <a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>
      <a:dk2><a:srgbClr val="1F2A44"/></a:dk2>
      <a:lt2><a:srgbClr val="F4F7FA"/></a:lt2>
      <a:accent1><a:srgbClr val="12549E"/></a:accent1>
      <a:accent2><a:srgbClr val="EF413D"/></a:accent2>
      <a:accent3><a:srgbClr val="5B9BD5"/></a:accent3>
      <a:accent4><a:srgbClr val="70AD47"/></a:accent4>
      <a:accent5><a:srgbClr val="ED7D31"/></a:accent5>
      <a:accent6><a:srgbClr val="A5A5A5"/></a:accent6>
      <a:hlink><a:srgbClr val="12549E"/></a:hlink>
      <a:folHlink><a:srgbClr val="0A1931"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="TCS"><a:majorFont><a:latin typeface="Calibri"/></a:majorFont><a:minorFont><a:latin typeface="Calibri"/></a:minorFont></a:fontScheme>
    <a:fmtScheme name="TCS"><a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst><a:lnStyleLst><a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln></a:lnStyleLst><a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst><a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst></a:fmtScheme>
  </a:themeElements><a:objectDefaults/><a:extraClrSchemeLst/>
</a:theme>'''

# Helper to create text shape XML
def tx_shape(id_, name, x, y, cx, cy, paragraphs, font_size=1200, bold=False, color=None, align=None):
    # paragraphs: list of dict {text, bold, size, color, bullet}
    # color: hex RRGGBB
    # size in hundredths pt (1200 = 12pt)
    p_xml=""
    for para in paragraphs:
        # para may be single run or multiple runs
        if isinstance(para, str):
            para = {"text": para}
        txt = xml_escape(para.get("text",""))
        sz = para.get("size", font_size)
        b = " b=\"1\"" if para.get("bold", bold) else ""
        c = para.get("color", color)
        col_xml = f'<a:solidFill><a:srgbClr val="{c}"/></a:solidFill>' if c else '<a:solidFill><a:schemeClr val="tx1"/></a:solidFill>'
        # bullet?
        # align
        aln = f' algn="{align}"' if align else ""
        # handle empty?
        if txt=="":
            p_xml += f'<a:p{aln}><a:pPr/><a:endParaRPr sz="{sz}"{b}/></a:p>'
        else:
            # split bullet handling: if bullet true, add buChar
            bu = '<a:buChar char="•"/>' if para.get("bullet") else '<a:buNone/>'
            p_xml += f'<a:p{aln}><a:pPr {bu[3:-2] if "buChar" not in bu else "><a:buChar char=\"•\"/"}></a:pPr>' if False else f'<a:p{aln}><a:pPr>{bu}</a:pPr><a:r><a:rPr sz="{sz}"{b}>{col_xml}</a:rPr><a:t>{txt}</a:t></a:r></a:p>'
            # Actually need proper bu handling; simplify:
            # We'll redo to avoid complexity: use buNone vs buChar
    # Better construct correctly without escaping confusion:
    # Rebuild properly
    # Instead of above broken, reconstruct clean
    return "" # placeholder to be replaced

# Improved tx builder
def build_paragraphs_xml(paragraphs, default_size=1000, default_color=None, default_bold=False, align=None):
    out=""
    for para in paragraphs:
        if isinstance(para, str):
            para={"text": para}
        text = xml_escape(para.get("text",""))
        size = para.get("size", default_size)
        bold = para.get("bold", default_bold)
        color = para.get("color", default_color)
        bullet = para.get("bullet", False)
        is_bullet = bool(bullet)
        aln = f' algn="{align}"' if align else ""
        b_attr = ' b="1"' if bold else ""
        col = f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>' if color else '<a:solidFill><a:schemeClr val="tx1"/></a:solidFill>'
        if text=="":
            out+= f'<a:p{aln}><a:pPr>{("<a:buChar char=\"•\"/>" if is_bullet else "<a:buNone/>")}</a:pPr><a:endParaRPr sz="{size}"{b_attr}>{col}</a:endParaRPr></a:p>'
        else:
            bu = '<a:buChar char="•"/>' if is_bullet else '<a:buNone/>'
            out+= f'<a:p{aln}><a:pPr>{bu}</a:pPr><a:r><a:rPr sz="{size}"{b_attr}>{col}</a:rPr><a:t>{text}</a:t></a:r></a:p>'
    return out

def shape_tx(id_, name, x,y,cx,cy, paragraphs, fill=None, line=None):
    # paragraphs already as list of dicts
    # Use build_paragraphs_xml
    # Determine font defaults?
    # caller passes paragraphs with size/color
    body = build_paragraphs_xml(paragraphs, default_size=1100)
    fill_xml = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else '<a:noFill/>'
    ln_xml = '<a:ln><a:noFill/></a:ln>' if not line else f'<a:ln w="12700"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>'
    return f'''
      <p:sp>
        <p:nvSpPr><p:cNvPr id="{id_}" name="{xml_escape(name)}"/><p:cNvPr/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:solidFill>{fill_xml}</a:solidFill>{ln_xml}</p:spPr>
        <p:txBody><a:bodyPr wrap="square" lIns="72000" rIns="72000" tIns="36000" bIns="36000"/><a:lstStyle/>{body}</p:txBody>
      </p:sp>'''

# Specialized shape helpers for TCS deck
def title_shape(text, subtitle=None):
    paras=[{"text": text, "size":2400, "bold": True, "color":"0A1931"}]
    if subtitle:
        paras.append({"text":"", "size":800})
        paras.append({"text": subtitle, "size":1100, "color":"5A6C80"})
    return shape_tx(2,"Title", 360000, 300000, 11472000, 1400000, paras)

def header_shape(text, kicker=None):
    paras=[]
    if kicker:
        paras.append({"text": kicker, "size":800, "bold":True, "color":"12549E"})
        paras.append({"text":"", "size":400})
    paras.append({"text": text, "size":1800, "bold":True, "color":"0A1931"})
    return shape_tx(2,"Header", 360000, 200000, 11472000, 1100000, paras)

def body_shape(paras):
    return shape_tx(3,"Body", 360000, 1500000, 5820000, 4600000, paras)

def side_shape(paras):
    return shape_tx(4,"Side", 6500000, 1500000, 5000000, 4600000, paras)

def footer_shape():
    return shape_tx(5,"Footer", 360000, 6400000, 11472000, 300000, [{"text":"TCS France  •  RAG Explainer  •  Private data stays private  •  rag-explainer.github.io","size":700,"color":"5A6C80"}])

def full_shape(paras, y=1500000, h=4600000):
    return shape_tx(3,"Full", 360000, y, 11472000, h, paras)

# Slide definitions — 17 slides, TCS professional English
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

def slide_xml_for(idx, data):
    # idx 1-based
    t = data.get("type")
    shapes=[]
    if t=="title":
        shapes.append(title_shape(data["title"], data.get("subtitle")))
        shapes.append(footer_shape())
        inner="\n".join(shapes)
    elif t=="full":
        shapes.append(header_shape(data["title"], data.get("kicker")))
        shapes.append(full_shape(data["body"]))
        shapes.append(footer_shape())
        inner="\n".join(shapes)
    elif t=="header_body_side":
        shapes.append(header_shape(data["title"], data.get("kicker")))
        shapes.append(body_shape(data["body"]))
        shapes.append(side_shape(data["side"]))
        shapes.append(footer_shape())
        inner="\n".join(shapes)
    else:
        inner=full_shape(data.get("body",[]))
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld><p:spTree>{group_xml()}
{inner}
  </p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>
'''

def slide_rels_xml_text():
    return '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/></Relationships>'''

def build():
    n=len(SLIDES)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUT,"w",ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types_xml(n))
        z.writestr("_rels/.rels", root_rels_xml())
        z.writestr("docProps/app.xml", app_xml(n))
        z.writestr("docProps/core.xml", core_xml("RAG Explainer — Build Your Personal Document Assistant"))
        z.writestr("ppt/presentation.xml", presentation_xml(n))
        z.writestr("ppt/_rels/presentation.xml.rels", presentation_rels_xml(n))
        z.writestr("ppt/presProps.xml", pres_props_xml())
        z.writestr("ppt/viewProps.xml", view_props_xml())
        z.writestr("ppt/tableStyles.xml", table_styles_xml())
        z.writestr("ppt/slideMasters/slideMaster1.xml", slide_master_xml())
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", slide_master_rels_xml())
        z.writestr("ppt/slideLayouts/slideLayout1.xml", slide_layout_xml())
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", slide_layout_rels_xml())
        z.writestr("ppt/theme/theme1.xml", theme_xml())
        for i, s in enumerate(SLIDES, start=1):
            z.writestr(f"ppt/slides/slide{i}.xml", slide_xml_for(i, s))
            z.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", slide_rels_xml_text())
    print(f"Generated {OUT} ({n} slides)")

if __name__=="__main__":
    build()
