"""Insert portfolio project cards from Word doc into index.html."""
from pathlib import Path

D = "motion.div"  # placeholder replaced below

kazozu_card = f"""
        <{D} class="proj-card">
          <{D} class="proj-card-accent" style="background:var(--navy)"></{D}>
          <img class="proj-card-img" src="https://images.unsplash.com/photo-1581092160562-40aa08e78837?w=800&amp;q=80" alt="Kazozu Mine electrical power system" loading="lazy">
          <{D} class="proj-card-body">
            <{D} class="proj-card-top">
              <{D} class="proj-name">Kazozu Mine — Phase 1 Electrical Power System (Metalex Africa Mining)</{D}>
              <span class="tag active">Active</span>
            </{D}>
            <{D} class="proj-meta">
              <{D} class="proj-meta-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>Kalumbila, North-West Province, Zambia</{D}>
              <{D} class="proj-meta-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>Electrical Engineering Services (Sub-Consultant)</{D}>
              <{D} class="proj-meta-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>MV/LV reticulation, MCC design, lightning protection &amp; earthing</{D}>
            </{D}>
            <{D} class="proj-footer"><span class="proj-year">2024 – 2025</span></{D}>
          </{D}>
        </{D}>

""".replace("motion.div", "div")

lab_card = f"""
        <{D} class="proj-card">
          <{D} class="proj-card-accent" style="background:var(--gold)"></{D}>
          <img class="proj-card-img" src="https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?w=800&amp;q=80" alt="Lab Partners Head Office and Health Centre" loading="lazy">
          <{D} class="proj-card-body">
            <{D} class="proj-card-top">
              <{D} class="proj-name">Lab Partners Head Office and Health Centre</{D}>
              <span class="tag active">Active</span>
            </{D}>
            <{D} class="proj-meta">
              <{D} class="proj-meta-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>Belgravia, Harare, Zimbabwe</{D}>
              <{D} class="proj-meta-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>Electrical &amp; Mechanical Engineering Services</{D}>
              <{D} class="proj-meta-row"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>Two-storey private healthcare — MRI, radiology, theatre &amp; dialysis</{D}>
            </{D}>
            <{D} class="proj-footer"><span class="proj-year">2024 – Present</span></{D}>
          </{D}>
        </{D}>

""".replace("motion.div", "div")

html_path = Path(r"d:\ZambeziConsulting\index.html")
html = html_path.read_text(encoding="utf-8")

if "Kazozu Mine" not in html:
    needle = 'alt="Husab Mine" loading="lazy">'
    idx = html.find(needle)
    if idx == -1:
        raise SystemExit("Husab needle not found")
    card_start = html.rfind('<div class="proj-card">', 0, idx)
    html = html[:card_start] + kazozu_card + html[card_start:]

if "Lab Partners" not in html:
    needle2 = 'alt="Maerua Mall Redevelopment"'
    idx2 = html.find(needle2)
    if idx2 == -1:
        raise SystemExit("Maerua needle not found")
    card_start2 = html.rfind('<div class="proj-card">', 0, idx2)
    html = html[:card_start2] + lab_card + html[card_start2:]

html_path.write_text(html, encoding="utf-8")
print("Updated index.html")
