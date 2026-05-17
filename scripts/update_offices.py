"""Remove Windhoek office block from contact section."""
from pathlib import Path

INDEX = Path(r"d:\ZambeziConsulting\index.html")
html = INDEX.read_text(encoding="utf-8")

marker = "Head Office — Namibia"
idx = html.find(marker)
if idx != -1:
    start = html.rfind('<motion.div class="office">', 0, idx)
    start = html.rfind('<div class="office">', 0, idx)
    end = html.find("</div>\n          </div>", idx) + len("</div>\n          </div>")
    html = html[:start] + html[end:]

INDEX.write_text(html, encoding="utf-8")
print("Removed:", "Head Office — Namibia" not in html)
