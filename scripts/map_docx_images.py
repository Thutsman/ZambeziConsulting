"""Map inline images in docx to nearby paragraph text."""
from pathlib import Path
import zipfile
import re
from xml.etree import ElementTree as ET

docx_path = Path(r"d:\ZambeziConsulting\Zambezi Consulting Engineers Pvt Ltd (2) - Copy (1).docx")

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
}

with zipfile.ZipFile(docx_path) as z:
    rels_xml = z.read("word/_rels/document.xml.rels")
    doc_xml = z.read("word/document.xml")

rels_root = ET.fromstring(rels_xml)
rid_map = {}
for rel in rels_root:
    rid = rel.attrib.get("Id")
    target = rel.attrib.get("Target", "")
    if "media/" in target:
        rid_map[rid] = "word/" + target.replace("../", "")

root = ET.fromstring(doc_xml)
body = root.find("w:body", NS)

current_text = []
events = []

for child in body:
    tag = child.tag.split("}")[-1]
    if tag == "p":
        texts = []
        for t in child.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"):
            if t.text:
                texts.append(t.text)
            if t.tail:
                texts.append(t.tail)
        para = "".join(texts).strip()
        if para:
            events.append(("text", para))
        for blip in child.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}blip"):
            embed = blip.attrib.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed")
            if embed and embed in rid_map:
                events.append(("image", rid_map[embed]))
    elif tag == "tbl":
        events.append(("table", "..."))

# Print context around calundike
for i, (kind, val) in enumerate(events):
  if kind == "text" and "calundike" in val.lower():
    start = max(0, i - 3)
    end = min(len(events), i + 6)
    print(f"=== Context at index {i} ===")
    for j in range(start, end):
      print(f"  {events[j][0]}: {events[j][1][:120] if events[j][0]=='text' else events[j][1]}")
