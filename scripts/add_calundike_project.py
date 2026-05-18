"""Add Nyaradzo Calundike project card to index.html."""
from pathlib import Path

TAG = "§DIV§"

card = f"""
        <{TAG} class="proj-card">
          <{TAG} class="proj-card-accent" style="background:var(--gold)"></{TAG}>
          <img class="proj-card-img" src="images/portfolio/nyaradzo-calundike-retail-shop-and-offices.png" alt="Nyaradzo Calundike Retail Shop and Offices" loading="lazy">
          <{TAG} class="proj-card-body">
            <{TAG} class="proj-card-top">
              <{TAG} class="proj-name">Nyaradzo Calundike Retail Shop and Offices</{TAG}>
              <span class="tag active">Active</span>
            </{TAG}>
            <{TAG} class="proj-meta">
              <{TAG} class="proj-meta-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>Bulawayo, Zimbabwe</{TAG}>
              <{TAG} class="proj-meta-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>Electrical &amp; Mechanical Engineering — Design &amp; Supervision</{TAG}>
            </{TAG}>
            <{TAG} class="proj-footer"><span class="proj-year">2026 – Present</span></{TAG}>
          </{TAG}>
        </{TAG}>

""".replace(TAG, "div")

html_path = Path(r"d:\ZambeziConsulting\index.html")
html = html_path.read_text(encoding="utf-8")

if "Calundike" in html:
    print("Calundike already in index.html")
else:
    needle = 'alt="Maerua Mall Redevelopment"'
    idx = html.find(needle)
    if idx == -1:
        raise SystemExit("Maerua needle not found")
    card_start = html.rfind('<div class="proj-card">', 0, idx)
    html = html[:card_start] + card + html[card_start:]
    html_path.write_text(html, encoding="utf-8")
    print("Added Calundike project card")
