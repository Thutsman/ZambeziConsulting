"""Map portfolio images from Draft Website Information docx to named project files."""
import re
import shutil
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(r"d:\ZambeziConsulting")
DRAFT_DOC = ROOT / "Draft Website Information (1).docx"
CAP_DOC = ROOT / "Zambezi Consulting Engineers Capability Statement 2025.docx"
OUT_PORTFOLIO = ROOT / "images" / "portfolio"
OUT_PORTFOLIO.mkdir(parents=True, exist_ok=True)

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
}


def slugify(text: str, max_len: int = 60) -> str:
    text = re.sub(r"Name of Assignment:\s*", "", text, flags=re.I)
    text = re.sub(r"Consultancy Services for\s*", "", text, flags=re.I)
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", "-", text.strip().lower())
    return text[:max_len].strip("-")


def load_rels(z: zipfile.ZipFile) -> dict[str, str]:
    rels = {}
    data = z.read("word/_rels/document.xml.rels")
    root = ET.fromstring(data)
    for rel in root:
        rid = rel.attrib.get("Id")
        target = rel.attrib.get("Target", "")
        if rid and "media/" in target:
            rels[rid] = target.replace("media/", "")
    return rels


def iter_body_elements(docx_path: Path):
    with zipfile.ZipFile(docx_path, "r") as z:
        rels = load_rels(z)
        root = ET.fromstring(z.read("word/document.xml"))
        body = root.find("w:body", NS)
        if body is None:
            return
        for child in body:
            tag = child.tag.split("}")[-1]
            if tag == "p":
                texts = []
                for t in child.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"):
                    if t.text:
                        texts.append(t.text)
                yield ("text", "".join(texts).strip())
                for blip in child.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}blip"):
                    embed = blip.attrib.get(
                        "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"
                    )
                    if embed and embed in rels:
                        yield ("image", rels[embed])
            elif tag == "tbl":
                for p in child.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"):
                    texts = []
                    for t in p.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"):
                        if t.text:
                            texts.append(t.text)
                    txt = "".join(texts).strip()
                    if txt:
                        yield ("text", txt)
                    for blip in p.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}blip"):
                        embed = blip.attrib.get(
                            "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"
                        )
                        if embed and embed in rels:
                            yield ("image", rels[embed])


def extract_portfolio_from_draft():
    mappings = []
    current_assignment = None
    in_portfolio = False

    with zipfile.ZipFile(DRAFT_DOC, "r") as z:
        media_cache = {}

        for kind, value in iter_body_elements(DRAFT_DOC):
            if kind == "text":
                upper = value.upper()
                if "EXPERIENCE PORTFOLIO" in upper:
                    in_portfolio = True
                    continue
                if not in_portfolio:
                    continue
                if "NAME OF ASSIGNMENT" in upper or value.startswith("Name of Assignment"):
                    current_assignment = value
                elif value.startswith("WATER SUPPLY") or value.startswith("SUSTAINABLE URBAN"):
                    pass  # category headers
            elif kind == "image" and in_portfolio and current_assignment:
                img_name = value
                src = f"word/media/{img_name}"
                if src not in media_cache:
                    media_cache[src] = z.read(src)
                slug = slugify(current_assignment)
                ext = Path(img_name).suffix.lower()
                out = OUT_PORTFOLIO / f"{slug}{ext}"
                out.write_bytes(media_cache[src])
                mappings.append(
                    {
                        "assignment": current_assignment,
                        "file": str(out.relative_to(ROOT)).replace("\\", "/"),
                        "slug": slug,
                    }
                )
                current_assignment = None  # one image per project typically

    return mappings


def extract_capability_portfolio():
    """Extract images from capability statement after SELECTED PROJECTS."""
    mappings = []
    current_assignment = None
    in_projects = False

    with zipfile.ZipFile(CAP_DOC, "r") as z:
        media_cache = {}

        for kind, value in iter_body_elements(CAP_DOC):
            if kind == "text":
                upper = value.upper()
                if "SELECTED PROJECTS" in upper:
                    in_projects = True
                    continue
                if "CONTACTS" in upper and in_projects:
                    break
                if not in_projects:
                    continue
                if "Name of Assignment" in value or "NAME OF ASSIGNMENT" in upper:
                    current_assignment = value
            elif kind == "image" and in_projects and current_assignment:
                img_name = value
                src = f"word/media/{img_name}"
                if src not in media_cache:
                    media_cache[src] = z.read(src)
                slug = slugify(current_assignment)
                ext = Path(img_name).suffix.lower()
                out = OUT_PORTFOLIO / f"cap_{slug}{ext}"
                if not out.exists():
                    out.write_bytes(media_cache[src])
                    mappings.append(
                        {
                            "assignment": current_assignment,
                            "file": str(out.relative_to(ROOT)).replace("\\", "/"),
                            "slug": slug,
                        }
                    )
                current_assignment = None

    return mappings


def main():
    draft_maps = extract_portfolio_from_draft()
    cap_maps = extract_capability_portfolio()

    report = ROOT / "scripts" / "portfolio_image_map.txt"
    lines = ["=== Draft Website Information ===", ""]
    for m in draft_maps:
        lines.append(f"{m['slug']}\n  -> {m['file']}\n  {m['assignment'][:120]}...\n")
    lines += ["", "=== Capability Statement (additional) ===", ""]
    for m in cap_maps:
        lines.append(f"{m['slug']}\n  -> {m['file']}\n  {m['assignment'][:120]}...\n")

    report.write_text("\n".join(lines), encoding="utf-8")
    print(f"Draft portfolio images: {len(draft_maps)}")
    print(f"Capability portfolio images: {len(cap_maps)}")
    print(f"Saved to: {OUT_PORTFOLIO}")
    print(f"Report: {report}")


if __name__ == "__main__":
    main()
