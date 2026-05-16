"""Inject portfolio images and missing projects into index.html."""
import re
from pathlib import Path

INDEX = Path(r"d:\ZambeziConsulting\index.html")

IMG_BY_NAME = [
    ("Greater Maputo Water Supply Project", "images/portfolio/preparation-of-phase-ii-of-the-greater-maputo.jpeg"),
    ("Oshakati Water Purification Plant", "images/portfolio/oshakati-water-purification-plant-extension.jpeg"),
    ("Husab Mine", "images/portfolio/construction-of-the-engineering-workshop-and-functional-area.png"),
    ("126kWp Grid-Tied Solar PV", "images/portfolio/126kwp-grid-tied-solar-photovoltaic-system-at-mashare-agricu.png"),
    ("Maerua Mall Redevelopment", "images/portfolio/maerua-mall-redevelopment-upgrade-phase-1.jpeg"),
    ("Katutura Medical &amp; Wellness Centre", "images/portfolio/katutura-medical-wellness-centre.png"),
    ("Upgrade of Ondangwa Private Hospital", "images/portfolio/upgrade-of-ondangwa-private-hospital.png"),
    ("Academia Medical Centre", "images/portfolio/academia-medical-centre.png"),
    ("Nored Katima Regional Office", "images/portfolio/nored-katima-regional-office.png"),
    ("Modern Grootfontein Open Market", "images/portfolio/modern-grootfontein-open-market-facility-for-grootfontein-mu.png"),
    ("Seed Processing Plants Design", "images/portfolio/the-design-and-construction-supervision-for-the.png"),
]

NEW_CARDS = """
        <div class="proj-card">
          <motion-div class="proj-card-accent" style="background:var(--gold)"></div>
          <img class="proj-card-img" src="images/portfolio/tate-village-student-accommodation.png" alt="Tate Village Student Accommodation" loading="lazy">
          <div class="proj-card-body">
            <div class="proj-card-top">
              <div class="proj-name">Tate Village Student Accommodation</div>
              <span class="tag complete">Complete</span>
            </div>
            <div class="proj-meta">
              <motion-div class="proj-meta-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>Windhoek West, Windhoek, Namibia</div>
              <div class="proj-meta-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>Electrical &amp; Mechanical Engineering</div>
            </div>
            <div class="proj-footer"><span class="proj-year">2017 – 2018</span></div>
          </div>
        </div>

        <div class="proj-card">
          <div class="proj-card-accent" style="background:var(--gold)"></div>
          <img class="proj-card-img" src="images/portfolio/nored-main-store.png" alt="Nored Main Store" loading="lazy">
          <div class="proj-card-body">
            <div class="proj-card-top">
              <div class="proj-name">Nored Main Store</div>
              <span class="tag complete">Complete</span>
            </div>
            <div class="proj-meta">
              <div class="proj-meta-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>Ondangwa, Namibia</div>
              <div class="proj-meta-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>Electrical &amp; Mechanical Engineering</div>
            </div>
            <div class="proj-footer"><span class="proj-year">2017 – 2021</span></div>
          </div>
        </div>

        <div class="proj-card">
          <div class="proj-card-accent" style="background:var(--gold)"></div>
          <img class="proj-card-img" src="images/portfolio/nored-head-office-expansion.png" alt="Nored Head Office Expansion" loading="lazy">
          <div class="proj-card-body">
            <div class="proj-card-top">
              <div class="proj-name">Nored Head Office Expansion</div>
              <span class="tag complete">Complete</span>
            </div>
            <div class="proj-meta">
              <div class="proj-meta-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>Ondangwa, Namibia</div>
              <div class="proj-meta-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>Electrical &amp; Mechanical Engineering</div>
            </div>
            <div class="proj-footer"><span class="proj-year">2019 – 2022</span></div>
          </div>
        </motion-div>
""".replace("motion-div", "div")


def main():
    html = INDEX.read_text(encoding="utf-8")

    for name, src in IMG_BY_NAME:
        if "proj-card-img" in html and f'alt="{name}' in html:
            continue
        pattern = (
            rf'(<div class="proj-name">{re.escape(name)}</motion-div>[\s\S]*?</motion-div>\s*</motion-div>\s*)'
        )
        pattern = (
            rf'(<motion-div class="proj-card">[\s\S]*?<div class="proj-name">{re.escape(name)}</div>[\s\S]*?</div>\s*</div>\s*)'
        )
        # Find card by name and inject image after accent if missing
        idx = html.find(f'<div class="proj-name">{name}')
        if idx == -1:
            print("skip (not found):", name[:40])
            continue
        card_start = html.rfind('<div class="proj-card">', 0, idx)
        accent_close = html.find("</div>", html.find("proj-card-accent", card_start)) + 6
        segment = html[card_start:accent_close + 50]
        if "proj-card-img" in html[card_start : idx + 100]:
            continue
        alt = name.replace("&amp;", "&")
        img = f'\n          <img class="proj-card-img" src="{src}" alt="{alt}" loading="lazy">'
        html = html[:accent_close] + img + html[accent_close:]

    if "Tate Village" not in html:
        needle = '<motion-div class="proj-name">Nored Katima Regional Office</div>'
        needle = '<div class="proj-name">Nored Katima Regional Office</div>'
        pos = html.find(needle)
        if pos != -1:
            card_start = html.rfind('<div class="proj-card">', 0, pos)
            html = html[:card_start] + NEW_CARDS + html[card_start:]

    html = re.sub(
        r'(<div class="proj-name">Greater Maputo Water Supply[\s\S]*?<span class="proj-year">)2023 – 2025(</span>)',
        r"\g<1>2023 – Present\g<2>",
        html,
        count=1,
    )

    INDEX.write_text(html, encoding="utf-8")
    print("proj-card-img count:", html.count("proj-card-img"))


if __name__ == "__main__":
    main()
