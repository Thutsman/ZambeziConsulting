"""Replace services section in index.html from website Word doc content."""
from pathlib import Path

ROOT = Path(r"d:\ZambeziConsulting")
INDEX = ROOT / "index.html"

NEW_SECTION = """<section id="services" class="alt">
  <div class="container">
    <div class="section-head center reveal">
      <p class="eyebrow green">What We Do</p>
      <h2>Our <em>Services</em></h2>
      <div class="section-rule center"></div>
      <p>Leading MEP&amp;F and renewable energy consulting — delivering world-class, multidisciplinary engineering solutions that drive sustainable development across Southern Africa.</p>
    </div>

    <div class="services-grid">

      <article id="service-electrical" class="service-card reveal" style="--service-accent:var(--gold)">
        <header class="service-card-head">
          <div class="service-card-icon" aria-hidden="true">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/></svg>
          </div>
          <h3>Electrical Services</h3>
        </header>
        <ul class="service-card-items">
          <li>High and Low Voltage Electrical Infrastructure</li>
          <li>Electrical Distribution Networks up to 132kV</li>
          <li>Instrumentation, Process Control and Automation</li>
          <li>Emergency Power Installations</li>
          <li>Street and Area Lighting Systems</li>
          <li>Load Studies and Fault Current Determinations</li>
        </ul>
      </article>

      <article id="service-mechanical" class="service-card reveal" style="--service-accent:var(--navy2)">
        <header class="service-card-head">
          <div class="service-card-icon" aria-hidden="true">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83M1 12h4M19 12h4M4.22 19.78l2.83-2.83M16.95 7.05l2.83-2.83"/></svg>
          </div>
          <h3>Mechanical Services</h3>
        </header>
        <ul class="service-card-items">
          <li>Air Conditioning &amp; Ventilation Systems</li>
          <li>Chilled Water Plants &amp; Thermal Energy Storage</li>
          <li>Variable Refrigerant Flow (VRF) Systems</li>
          <li>Vertical Transportation (Lifts, Escalators)</li>
          <li>Wet Services (Plumbing &amp; Drainage)</li>
          <li>Water Treatment Plants &amp; Pumping Systems</li>
        </ul>
      </article>

      <article id="service-fire" class="service-card reveal" style="--service-accent:#C44A2A">
        <header class="service-card-head">
          <div class="service-card-icon" aria-hidden="true">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M8.5 14.5A2.5 2.5 0 0011 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 11-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 003.5 0z"/></svg>
          </div>
          <h3>Fire Protection Engineering</h3>
        </header>
        <ul class="service-card-items">
          <li>Fire Rational Designs</li>
          <li>Automatic Sprinkler Protection Systems</li>
          <li>Smoke Extract and Pressurisation Systems</li>
          <li>Gaseous Suppression Systems</li>
          <li>Automatic Smoke Detection Systems</li>
          <li>Voice Evacuation Systems</li>
        </ul>
      </article>

      <article id="service-electronic" class="service-card reveal" style="--service-accent:var(--water)">
        <header class="service-card-head">
          <div class="service-card-icon" aria-hidden="true">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8M12 17v4"/></svg>
          </div>
          <h3>Electronic &amp; ICT Services</h3>
        </header>
        <ul class="service-card-items">
          <li>Fire Life &amp; Safety Systems</li>
          <li>Security Systems &amp; Access Control</li>
          <li>CCTV &amp; Surveillance Systems</li>
          <li>IP Networks &amp; VoIP Systems</li>
          <li>Audio Visual Systems</li>
          <li>Building Management &amp; Automation</li>
          <li>Data Centre Control Systems</li>
        </ul>
      </article>

      <article id="service-renewable" class="service-card reveal" style="--service-accent:var(--green)">
        <header class="service-card-head">
          <div class="service-card-icon" aria-hidden="true">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
          </div>
          <h3>Renewable Energy Services</h3>
        </header>
        <ul class="service-card-items">
          <li>Solar Power System Design</li>
          <li>Wind Energy Solutions</li>
          <li>Energy Storage Systems</li>
          <li>Grid Integration Studies</li>
          <li>Energy Efficiency Assessments</li>
          <li>Sustainable Energy Consulting</li>
        </ul>
      </article>

      <article id="service-water" class="service-card reveal" style="--service-accent:#1A7A9E">
        <header class="service-card-head">
          <div class="service-card-icon" aria-hidden="true">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2.69l5.66 5.66a8 8 0 11-11.31 0z"/></svg>
          </div>
          <h3>Water &amp; Sanitation Services</h3>
        </header>
        <ul class="service-card-items">
          <li>Water Treatment Plant Design</li>
          <li>Sewage Treatment Systems</li>
          <li>Water Distribution Networks</li>
          <li>Stormwater Management</li>
          <li>Groundwater Development</li>
          <li>Sanitation Infrastructure</li>
        </ul>
      </article>

    </div>
  </div>
</section>"""

def main():
    html = INDEX.read_text(encoding="utf-8")
    marker = '<section id="services"'
    start = html.index(marker)
    end = html.index("</section>", start) + len("</section>")
    INDEX.write_text(html[:start] + NEW_SECTION + html[end:], encoding="utf-8")
    print("Updated services section in", INDEX)


if __name__ == "__main__":
    main()
