"""Extract Calundike project images from ZCE Word profile."""
from pathlib import Path
import zipfile
import shutil
from xml.etree import ElementTree as ET

DOCX = Path(r"D:\ZambeziConsulting\Zambezi Consulting Engineers Pvt Ltd (2) - Copy.docx")
OUT_DIR = Path(r"D:\ZambeziConsulting\images\portfolio")
R_EMBED = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed"


def resolve_media_path(target: str) -> str:
    target = target.lstrip("/")
    if target.startswith("media/"):
        return target
    if target.startswith("word/"):
        return target
    return "word/" + target.replace("../", "")


def map_events(docx_path: Path) -> list[tuple[str, str]]:
    with zipfile.ZipFile(docx_path) as z:
        names = set(z.namelist())
        rels_root = ET.fromstring(z.read("word/_rels/document.xml.rels"))
        rid_map = {}
        for rel in rels_root:
            rid = rel.attrib.get("Id")
            target = rel.attrib.get("Target", "")
            if "media" in target.lower():
                path = resolve_media_path(target)
                # some targets are /media/x — try both locations
                candidates = [path, path.replace("word/", ""), "media/" + Path(path).name]
                for c in candidates:
                    if c in names:
                        rid_map[rid] = c
                        break
                else:
                    rid_map[rid] = path

        doc = ET.fromstring(z.read("word/document.xml"))
        body = doc.find("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}body")
        events: list[tuple[str, str]] = []

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
                    embed = blip.attrib.get(R_EMBED)
                    if embed and embed in rid_map:
                        events.append(("image", rid_map[embed]))
            elif tag == "tbl":
                events.append(("table", "table"))

        return events, z, names, rid_map


def main():
    events, z, names, rid_map = map_events(DOCX)

    # Print context around calundike
    calundike_idxs = [i for i, (k, v) in enumerate(events) if k == "text" and "calundike" in v.lower()]
    print(f"Calundike text occurrences: {len(calundike_idxs)}")
    calundike_images: list[str] = []

    for idx in calundike_idxs:
        print(f"\n=== Context at event {idx} ===")
        start = max(0, idx - 4)
        end = min(len(events), idx + 8)
        for j in range(start, end):
            kind, val = events[j]
            marker = ">>>" if j == idx else "   "
            preview = val[:100] + "..." if kind == "text" and len(val) > 100 else val
            print(f"{marker} [{j}] {kind}: {preview}")

    # Collect images in Calundike section: from 2 events before title through next project
    if calundike_idxs:
        i0 = calundike_idxs[0]
        next_proj = len(events)
        for j in range(i0 + 1, len(events)):
            if events[j][0] == "text" and events[j][1].strip().lower().startswith("name of assignment"):
                if "calundike" not in events[j][1].lower():
                    next_proj = j
                    break
        for j in range(max(0, i0 - 2), next_proj):
            if events[j][0] == "image":
                calundike_images.append(events[j][1])

    # dedupe preserve order
    seen = set()
    unique_images = []
    for img in calundike_images:
        if img not in seen:
            seen.add(img)
            unique_images.append(img)

    print(f"\n=== Calundike-linked images ({len(unique_images)}) ===")
    for img in unique_images:
        print(f"  {img} (in zip: {img in names})")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    if not unique_images:
        print("No images found for Calundike")
        return

    # Prefer image before the title (Word often places the render above the heading).
    # The image after the title may belong to the next project (e.g. Glenara).
    before: list[str] = []
    after: list[str] = []
    if calundike_idxs:
        i0 = calundike_idxs[0]
        next_proj = len(events)
        for j in range(i0 + 1, len(events)):
            if events[j][0] == "text" and events[j][1].strip().lower().startswith("name of assignment"):
                if "calundike" not in events[j][1].lower():
                    next_proj = j
                    break
        before = [events[j][1] for j in range(max(0, i0 - 2), i0) if events[j][0] == "image"]
        after = [events[j][1] for j in range(i0 + 1, next_proj) if events[j][0] == "image"]
    primary = before[-1] if before else (unique_images[0] if unique_images else "")
    if len(unique_images) > 1 and after and before:
        print(f"Note: using pre-title image {primary!r}; post-title {after!r} may be next project.")
    ext = Path(primary).suffix or ".png"
    out_primary = OUT_DIR / f"nyaradzo-calundike-retail-shop-and-offices{ext}"

    with zipfile.ZipFile(DOCX) as zf:
        data = zf.read(primary)
        out_primary.write_bytes(data)
        print(f"\nWrote primary: {out_primary} ({len(data)} bytes)")

        # Only export additional images that are not the next project's render
        extras = [img for img in unique_images if img != primary and img not in after]
        for n, img_path in enumerate(extras, start=2):
            ext_n = Path(img_path).suffix or ".png"
            out_n = OUT_DIR / f"nyaradzo-calundike-retail-shop-and-offices-{n}{ext_n}"
            out_n.write_bytes(zf.read(img_path))
            print(f"Wrote extra: {out_n}")

    # List all media for debugging
    print("\n=== All media in docx ===")
    for n in sorted(names):
        if "media" in n.lower():
            print(f"  {n}")


if __name__ == "__main__":
    main()
