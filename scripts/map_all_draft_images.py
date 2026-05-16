"""Map all images in draft website doc with surrounding text context."""
import re
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(r"d:\ZambeziConsulting")
DRAFT_DOC = ROOT / "Draft Website Information (1).docx"
OUT = ROOT / "images" / "draft"
OUT.mkdir(parents=True, exist_ok=True)

NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def load_rels(z):
    rels = {}
    root = ET.fromstring(z.read("word/_rels/document.xml.rels"))
    for rel in root:
        rid = rel.attrib.get("Id")
        target = rel.attrib.get("Target", "")
        if rid and "media/" in target:
            rels[rid] = target.split("/")[-1]
    return rels


def main():
    lines = []
    context = []
    idx = 0
    with zipfile.ZipFile(DRAFT_DOC, "r") as z:
        rels = load_rels(z)
        root = ET.fromstring(z.read("word/document.xml"))
        body = root.find("w:body", NS)
        for child in body:
            tag = child.tag.split("}")[-1]
            elems = [child] if tag == "p" else child.findall(".//w:p", NS)
            for p in elems:
                texts = []
                for t in p.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"):
                    if t.text:
                        texts.append(t.text)
                txt = "".join(texts).strip()
                if txt:
                    context.append(txt)
                    if len(context) > 8:
                        context = context[-8:]
                for blip in p.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}blip"):
                    embed = blip.attrib.get(
                        "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"
                    )
                    if embed and embed in rels:
                        idx += 1
                        media = rels[embed]
                        data = z.read(f"word/media/{media}")
                        ext = Path(media).suffix
                        out = OUT / f"image{idx:02d}{ext}"
                        out.write_bytes(data)
                        ctx = " | ".join(context[-4:])
                        lines.append(f"image{idx:02d}{ext} <- {ctx[:200]}")
    (ROOT / "scripts" / "draft_image_context.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"Extracted {idx} images to {OUT}")
    print("\n".join(lines[:30]))


if __name__ == "__main__":
    main()
