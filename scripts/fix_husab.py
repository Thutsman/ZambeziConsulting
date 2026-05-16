import re
from pathlib import Path

p = Path(r"d:\ZambeziConsulting\index.html")
h = p.read_text(encoding="utf-8")

needle = "Functional Areas at Husab Mine"
i = h.find(needle)
card_start = h.rfind('<motion-div class="proj-card">', 0, i)
card_start = h.rfind('<div class="proj-card">', 0, i)
accent_close = h.find("</div>", h.find("proj-card-accent", card_start)) + 6
if "proj-card-img" not in h[card_start : i + 80]:
    img = '\n          <img class="proj-card-img" src="images/portfolio/construction-of-the-engineering-workshop-and-functional-area.png" alt="Husab Mine" loading="lazy">'
    h = h[:accent_close] + img + h[accent_close:]

h = re.sub(
    r"(Greater Maputo Water Supply[\s\S]{0,900}?<span class=\"proj-year\">)2023 – 2025(</span>)",
    r"\g<1>2023 – Present\g<2>",
    h,
    count=1,
)

p.write_text(h, encoding="utf-8")
print("images:", h.count("proj-card-img"))
