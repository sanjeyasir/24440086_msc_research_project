import re
import json
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
timeline_file = os.path.join(script_dir, "MSc_Research_Detailed_Timeline.txt")
output_html = os.path.join(script_dir, "index.html")

with open(timeline_file, 'r', encoding='utf-8') as f:
    raw_content = f.read()

phases_info = [
    {
        "id": 1,
        "name": "Research foundation and literature review",
        "weeks": [1, 9],
        "dates": "01 Apr 2026 – 02 Jun 2026",
        "total_weeks": 9,
        "hours": 9 * 33,
        "status": "completed",
        "progress": 100,
        "description": "Define research problem, objectives and research questions; review CMOS switching transients, near-field EM radiation, side-channel analysis, and inductive measurement techniques; establish literature matrix.",
        "icon": "📚"
    },
    {
        "id": 2,
        "name": "Mathematical electromagnetic modelling",
        "weeks": [10, 13],
        "dates": "03 Jun 2026 – 30 Jun 2026",
        "total_weeks": 4,
        "hours": 4 * 33,
        "status": "completed",
        "progress": 100,
        "description": "Develop simplified forward/return-current representation; formulate two-conductor Biot-Savart flux density B(t); implement Faraday's Law numerical differentiation (dB/dt) and Fourier derivative weighting (+20 dB/dec).",
        "icon": "📐"
    },
    {
        "id": 3,
        "name": "LTspice circuit simulation",
        "weeks": [14, 22],
        "dates": "01 Jul 2026 – 01 Sep 2026",
        "total_weeks": 9,
        "hours": 9 * 33,
        "status": "completed",
        "progress": 100,
        "description": "Build four-inverter CMOS bank; simulate Hamming-distance state sequences across four MOSFET models: Level 1 (Shichman-Hodges), Level 2 (Grove-Frohman), BSIM3v3.3, and BSIM4 with 5 pF capacitive loads.",
        "icon": "⚡"
    },
    {
        "id": 4,
        "name": "Python integration and simulated signal analysis",
        "weeks": [23, 26],
        "dates": "02 Sep 2026 – 29 Sep 2026",
        "total_weeks": 4,
        "hours": 4 * 33,
        "status": "completed",
        "progress": 100,
        "description": "Import transient waveforms; interpolate onto uniform time grid; compute Biot-Savart magnetic flux and time derivative; perform RFFT spectral normalisation; extract resonant peaks (15–68 MHz).",
        "icon": "🐍"
    },
    {
        "id": 5,
        "name": "Experimental setup and HackRF acquisition",
        "weeks": [27, 31],
        "dates": "30 Sep 2026 – 03 Nov 2026",
        "total_weeks": 5,
        "hours": 5 * 33,
        "status": "completed",
        "progress": 100,
        "description": "Assemble SN74HC04N hex inverter circuit; apply Arduino Nano 4-bit Hamming stimulus; configure HackRF One SDR (fc = 40 MHz, fs = 20 MS/s, 20 dB gain); acquire and organise 5 raw IQ recordings.",
        "icon": "📡"
    },
    {
        "id": 6,
        "name": "IQ processing and spectral analysis",
        "weeks": [32, 35],
        "dates": "04 Nov 2026 – 01 Dec 2026",
        "total_weeks": 4,
        "hours": 4 * 33,
        "status": "active",
        "progress": 37.5,
        "description": "Load raw interleaved int8 IQ; compute 50 µs block energy; apply adaptive threshold (µ + 3σ); cluster packet bursts (ΔT ≈ 87–91 ms); estimate packet-gated Welch PSD, SNR curves, and STFT waterfall spectrograms.",
        "icon": "🔬"
    },
    {
        "id": 7,
        "name": "Evaluation and comparison",
        "weeks": [36, 40],
        "dates": "02 Dec 2026 – 05 Jan 2027",
        "total_weeks": 5,
        "hours": 5 * 33,
        "status": "upcoming",
        "progress": 0,
        "description": "Compare simulated vs physical SDR spectra within 30–50 MHz; evaluate repeatability across 5 captures; reconcile 40–50 MHz ringing with parasitic LC loop tank and driver output resistance.",
        "icon": "⚖️"
    },
    {
        "id": 8,
        "name": "Dissertation writing",
        "weeks": [41, 44],
        "dates": "06 Jan 2027 – 02 Feb 2027",
        "total_weeks": 4,
        "hours": 4 * 33,
        "status": "upcoming",
        "progress": 0,
        "description": "Author complete dissertation: introduction, literature review, mathematical Biot-Savart modeling, SPICE simulations, HackRF experimental setup, DSP results, hardware reconciliation, and conclusions.",
        "icon": "✍️"
    },
    {
        "id": 9,
        "name": "Final review and submission preparation",
        "weeks": [45, 46],
        "dates": "03 Feb 2027 – 15 Feb 2027",
        "total_weeks": 2,
        "hours": 33 + 29,
        "status": "upcoming",
        "progress": 0,
        "description": "Technical review of equations, citations, figures; incorporate supervisor feedback; format final dissertation package; verify university submission requirements.",
        "icon": "🎓"
    }
]

# Parse weeks from text
week_blocks = re.split(r'(?m)^WEEK ', raw_content)
weeks_data = []

for block in week_blocks[1:]:
    lines = block.strip().split('\n')
    header_line = lines[0]
    m = re.match(r'(\d+):\s*([\d\w\s–]+)', header_line)
    if not m:
        continue
    w_num = int(m.group(1))
    w_dates = m.group(2).strip()
    full_body = ' '.join([l.strip() for l in lines[1:]])
    
    milestone = ''
    if 'Milestone:' in full_body:
        m_parts = full_body.split('Milestone:')
        body = m_parts[0].strip()
        milestone = m_parts[1].strip()
        if 'PHASE SUMMARY' in milestone:
            milestone = milestone.split('PHASE SUMMARY')[0].strip()
    else:
        body = full_body.strip()
        
    if "Phase:" in body:
        body = body.split("Phase:")[1].strip()
        
    phase_id = 1
    phase_name = ""
    for p in phases_info:
        if p["weeks"][0] <= w_num <= p["weeks"][1]:
            phase_id = p["id"]
            phase_name = p["name"]
            break
            
    if w_num < 33:
        status = "completed"
    elif w_num == 33:
        status = "current"
    else:
        status = "upcoming"
        
    hours = 33 if w_num < 46 else 29
        
    weeks_data.append({
        "week": w_num,
        "dates": w_dates,
        "phase_id": phase_id,
        "phase_name": phase_name,
        "body": body,
        "milestone": milestone,
        "status": status,
        "hours": hours
    })

weeks_json = json.dumps(weeks_data)
phases_json = json.dumps(phases_info)

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MSc Research Project Timeline | CMOS EM Side-Channel Analysis</title>
  <meta name="description" content="Detailed 46-Week Research Project Timeline for MSc Research: Electromagnetic Side-Channel Analysis of CMOS Switching Activity (University of Colombo)">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <style>
    :root {
      --bg-primary: #0a0e17;
      --bg-secondary: #111827;
      --bg-card: rgba(17, 24, 39, 0.75);
      --bg-card-hover: rgba(31, 41, 55, 0.85);
      --border-subtle: rgba(255, 255, 255, 0.08);
      --border-focus: rgba(56, 189, 248, 0.4);
      --text-main: #f3f4f6;
      --text-muted: #9ca3af;
      --text-dim: #6b7280;
      
      --accent-cyan: #06b6d4;
      --accent-cyan-glow: rgba(6, 182, 212, 0.35);
      --accent-blue: #3b82f6;
      --accent-emerald: #10b981;
      --accent-emerald-glow: rgba(16, 185, 129, 0.3);
      --accent-amber: #f59e0b;
      --accent-amber-glow: rgba(245, 158, 11, 0.3);
      --accent-purple: #8b5cf6;
      
      --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', Consolas, monospace;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background-color: var(--bg-primary);
      color: var(--text-main);
      font-family: var(--font-sans);
      line-height: 1.6;
      min-height: 100vh;
      overflow-x: hidden;
      background-image: 
        radial-gradient(circle at 15% 10%, rgba(56, 189, 248, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 85% 30%, rgba(139, 92, 246, 0.08) 0%, transparent 40%),
        radial-gradient(circle at 50% 80%, rgba(16, 185, 129, 0.05) 0%, transparent 50%);
      background-attachment: fixed;
    }

    a {
      color: var(--accent-cyan);
      text-decoration: none;
      transition: color 0.2s;
    }
    a:hover {
      color: #38bdf8;
      text-decoration: underline;
    }

    .container {
      max-width: 1280px;
      margin: 0 auto;
      padding: 0 24px;
    }

    /* Top Live Announcement Banner */
    .announcement-bar {
      background: linear-gradient(90deg, rgba(6, 182, 212, 0.15), rgba(139, 92, 246, 0.15));
      border-bottom: 1px solid rgba(56, 189, 248, 0.25);
      padding: 10px 0;
      font-size: 0.88rem;
      backdrop-filter: blur(8px);
      position: sticky;
      top: 0;
      z-index: 100;
    }
    .announcement-inner {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }
    .live-status {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-weight: 600;
      color: #38bdf8;
    }
    .pulse-dot {
      width: 10px;
      height: 10px;
      background-color: #06b6d4;
      border-radius: 50%;
      position: relative;
    }
    .pulse-dot::after {
      content: '';
      position: absolute;
      top: -3px;
      left: -3px;
      right: -3px;
      bottom: -3px;
      border-radius: 50%;
      border: 2px solid #06b6d4;
      animation: pulse 1.6s infinite ease-out;
    }
    @keyframes pulse {
      0% { transform: scale(0.9); opacity: 1; }
      100% { transform: scale(2.2); opacity: 0; }
    }

    .jump-btn {
      background: linear-gradient(135deg, #0284c7, #0369a1);
      color: #ffffff;
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 0.8rem;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      box-shadow: 0 2px 10px rgba(2, 132, 199, 0.35);
      transition: all 0.2s;
      border: 1px solid rgba(255, 255, 255, 0.15);
      cursor: pointer;
    }
    .jump-btn:hover {
      transform: translateY(-1px);
      box-shadow: 0 4px 14px rgba(2, 132, 199, 0.5);
      text-decoration: none;
      background: linear-gradient(135deg, #0369a1, #0284c7);
    }

    /* Header Section */
    .hero {
      padding: 48px 0 32px 0;
      border-bottom: 1px solid var(--border-subtle);
    }
    .badge-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-subtle);
      padding: 4px 12px;
      border-radius: 9999px;
      font-size: 0.78rem;
      font-weight: 500;
      color: var(--accent-cyan);
      margin-bottom: 14px;
    }
    .hero h1 {
      font-size: 2.5rem;
      font-weight: 800;
      line-height: 1.2;
      letter-spacing: -0.02em;
      background: linear-gradient(135deg, #ffffff 30%, #94a3b8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      margin-bottom: 12px;
    }
    .hero p.lead {
      font-size: 1.1rem;
      color: var(--text-muted);
      max-width: 900px;
      margin-bottom: 24px;
    }
    .meta-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
    }
    .meta-tag {
      background: rgba(30, 41, 59, 0.6);
      border: 1px solid var(--border-subtle);
      padding: 6px 14px;
      border-radius: 8px;
      font-size: 0.85rem;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      color: #cbd5e1;
    }

    /* KPI Cockpit Cards */
    .cockpit-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 20px;
      margin: 36px 0;
    }
    .kpi-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 22px;
      backdrop-filter: blur(12px);
      transition: transform 0.2s, border-color 0.2s;
      position: relative;
      overflow: hidden;
    }
    .kpi-card:hover {
      transform: translateY(-2px);
      border-color: rgba(255, 255, 255, 0.15);
    }
    .kpi-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 4px;
      background: var(--card-accent, var(--accent-blue));
    }
    .kpi-label {
      font-size: 0.82rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-dim);
      font-weight: 600;
      margin-bottom: 8px;
    }
    .kpi-value {
      font-size: 2.2rem;
      font-weight: 800;
      font-family: var(--font-mono);
      color: #ffffff;
      line-height: 1.1;
      margin-bottom: 6px;
    }
    .kpi-subtext {
      font-size: 0.85rem;
      color: var(--text-muted);
    }

    /* Global Progress Bar */
    .progress-track {
      width: 100%;
      height: 10px;
      background: rgba(255, 255, 255, 0.06);
      border-radius: 9999px;
      overflow: hidden;
      margin: 12px 0 6px 0;
      position: relative;
    }
    .progress-fill {
      height: 100%;
      background: linear-gradient(90deg, var(--accent-emerald) 0%, var(--accent-cyan) 80%, #38bdf8 100%);
      border-radius: 9999px;
      box-shadow: 0 0 12px var(--accent-cyan-glow);
      transition: width 1.2s ease-in-out;
    }

    /* Stepper Bar (Phases Breadcrumbs) */
    .stepper-section {
      margin: 40px 0 24px 0;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 24px;
    }
    .stepper-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 18px;
    }
    .stepper-header h3 {
      font-size: 1.1rem;
      font-weight: 700;
      color: #f1f5f9;
    }
    .stepper-grid {
      display: grid;
      grid-template-columns: repeat(9, 1fr);
      gap: 8px;
      overflow-x: auto;
      padding-bottom: 8px;
    }
    @media (max-width: 1024px) {
      .stepper-grid {
        grid-template-columns: repeat(9, minmax(130px, 1fr));
      }
    }
    .step-node {
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--border-subtle);
      border-radius: 10px;
      padding: 12px 8px;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s;
      position: relative;
    }
    .step-node:hover {
      background: rgba(255, 255, 255, 0.07);
      transform: translateY(-2px);
    }
    .step-node.completed {
      border-color: rgba(16, 185, 129, 0.4);
      background: rgba(16, 185, 129, 0.08);
    }
    .step-node.active {
      border-color: #06b6d4;
      background: rgba(6, 182, 212, 0.12);
      box-shadow: 0 0 16px var(--accent-cyan-glow);
    }
    .step-node.upcoming {
      opacity: 0.65;
    }
    .step-num {
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      margin-bottom: 4px;
      color: var(--text-dim);
    }
    .step-node.completed .step-num { color: var(--accent-emerald); }
    .step-node.active .step-num { color: var(--accent-cyan); }
    .step-name {
      font-size: 0.75rem;
      font-weight: 600;
      line-height: 1.25;
      color: #e2e8f0;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
      min-height: 28px;
    }
    .step-badge {
      font-size: 0.65rem;
      font-weight: 700;
      padding: 2px 6px;
      border-radius: 4px;
      margin-top: 6px;
      display: inline-block;
    }
    .step-node.completed .step-badge {
      background: rgba(16, 185, 129, 0.2);
      color: #34d399;
    }
    .step-node.active .step-badge {
      background: rgba(6, 182, 212, 0.25);
      color: #38bdf8;
    }
    .step-node.upcoming .step-badge {
      background: rgba(255, 255, 255, 0.08);
      color: #94a3b8;
    }

    /* Filter & Controls Toolbar */
    .controls-toolbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
      margin: 32px 0 24px 0;
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 14px 20px;
    }
    .filter-group {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .filter-btn {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      padding: 6px 14px;
      border-radius: 8px;
      font-size: 0.84rem;
      font-weight: 500;
      cursor: pointer;
      transition: all 0.2s;
    }
    .filter-btn:hover {
      background: rgba(255, 255, 255, 0.09);
      color: #ffffff;
    }
    .filter-btn.active {
      background: var(--accent-blue);
      color: #ffffff;
      border-color: var(--accent-blue);
      box-shadow: 0 2px 8px rgba(59, 130, 246, 0.35);
    }
    .search-box {
      position: relative;
      min-width: 260px;
    }
    .search-input {
      width: 100%;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid var(--border-subtle);
      color: #ffffff;
      padding: 8px 14px 8px 36px;
      border-radius: 8px;
      font-size: 0.86rem;
      outline: none;
      transition: border-color 0.2s;
    }
    .search-input:focus {
      border-color: var(--accent-cyan);
    }
    .search-icon {
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-dim);
      font-size: 0.9rem;
    }

    /* Main Timeline Container */
    .timeline-container {
      position: relative;
      margin: 32px 0 64px 0;
      padding-left: 36px;
    }
    .timeline-container::before {
      content: '';
      position: absolute;
      top: 0;
      bottom: 0;
      left: 11px;
      width: 2px;
      background: linear-gradient(180deg, var(--accent-emerald) 0%, var(--accent-cyan) 65%, rgba(255,255,255,0.1) 100%);
    }

    /* Phase Header Banner */
    .phase-divider {
      margin: 48px 0 24px -36px;
      padding: 20px 24px;
      background: linear-gradient(90deg, rgba(30, 41, 59, 0.85), rgba(15, 23, 42, 0.5));
      border: 1px solid var(--border-subtle);
      border-left: 4px solid var(--phase-color, var(--accent-blue));
      border-radius: 12px;
      backdrop-filter: blur(8px);
    }
    .phase-divider-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
      margin-bottom: 6px;
    }
    .phase-title-grp {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .phase-icon {
      font-size: 1.4rem;
    }
    .phase-title {
      font-size: 1.25rem;
      font-weight: 700;
      color: #f8fafc;
    }
    .phase-badge {
      font-size: 0.75rem;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 9999px;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .badge-comp {
      background: rgba(16, 185, 129, 0.15);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: #34d399;
    }
    .badge-curr {
      background: rgba(6, 182, 212, 0.2);
      border: 1px solid rgba(6, 182, 212, 0.4);
      color: #38bdf8;
    }
    .badge-upc {
      background: rgba(148, 163, 184, 0.1);
      border: 1px solid rgba(148, 163, 184, 0.2);
      color: #94a3b8;
    }
    .phase-meta {
      font-size: 0.86rem;
      color: var(--text-muted);
    }

    /* Week Card */
    .week-item {
      position: relative;
      margin-bottom: 20px;
      transition: all 0.2s;
    }
    .week-item.hidden {
      display: none;
    }
    .week-bullet {
      position: absolute;
      left: -32px;
      top: 22px;
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: var(--bg-primary);
      border: 2px solid var(--bullet-color, #475569);
      z-index: 2;
      transition: all 0.2s;
    }
    .week-item.completed .week-bullet {
      border-color: var(--accent-emerald);
      background: var(--accent-emerald);
      box-shadow: 0 0 8px var(--accent-emerald-glow);
    }
    .week-item.current .week-bullet {
      border-color: #06b6d4;
      background: #06b6d4;
      box-shadow: 0 0 12px var(--accent-cyan-glow);
      transform: scale(1.3);
    }

    .week-card {
      background: var(--bg-card);
      border: 1px solid var(--border-subtle);
      border-radius: 14px;
      padding: 20px;
      backdrop-filter: blur(10px);
      transition: all 0.2s;
    }
    .week-card:hover {
      background: var(--bg-card-hover);
      border-color: rgba(255, 255, 255, 0.18);
      transform: translateX(4px);
    }

    /* CURRENT WEEK 33 SPECIAL HIGHLIGHT */
    .week-item.current .week-card {
      background: linear-gradient(135deg, rgba(14, 116, 144, 0.25) 0%, rgba(17, 24, 39, 0.9) 100%);
      border: 2px solid #06b6d4;
      box-shadow: 0 0 28px rgba(6, 182, 212, 0.25), inset 0 0 16px rgba(6, 182, 212, 0.1);
      position: relative;
    }
    .current-week-flag {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: linear-gradient(90deg, #0284c7, #06b6d4);
      color: #ffffff;
      padding: 4px 12px;
      border-radius: 6px;
      font-size: 0.76rem;
      font-weight: 700;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      margin-bottom: 12px;
    }

    .week-card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 10px;
    }
    .week-title-wrap {
      display: flex;
      align-items: baseline;
      gap: 10px;
    }
    .week-num {
      font-size: 1.15rem;
      font-weight: 700;
      font-family: var(--font-mono);
      color: #f8fafc;
    }
    .week-dates {
      font-size: 0.86rem;
      color: var(--text-muted);
      font-weight: 500;
    }
    .week-badges {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .hours-tag {
      font-size: 0.75rem;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-subtle);
      padding: 2px 8px;
      border-radius: 4px;
      color: #94a3b8;
      font-family: var(--font-mono);
    }
    .status-tag {
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      padding: 2px 8px;
      border-radius: 4px;
    }
    .status-completed {
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
    }
    .status-current {
      background: rgba(6, 182, 212, 0.25);
      color: #38bdf8;
      border: 1px solid #06b6d4;
    }
    .status-upcoming {
      background: rgba(148, 163, 184, 0.1);
      color: #94a3b8;
    }

    .week-body {
      font-size: 0.93rem;
      color: #d1d5db;
      line-height: 1.55;
    }

    /* Milestone Callout Box */
    .milestone-callout {
      margin-top: 14px;
      background: linear-gradient(90deg, rgba(245, 158, 11, 0.12), rgba(245, 158, 11, 0.04));
      border: 1px solid rgba(245, 158, 11, 0.35);
      border-left: 4px solid var(--accent-amber);
      border-radius: 8px;
      padding: 10px 14px;
      display: flex;
      align-items: flex-start;
      gap: 10px;
    }
    .milestone-icon {
      color: var(--accent-amber);
      font-size: 1.1rem;
      line-height: 1.2;
    }
    .milestone-text {
      font-size: 0.86rem;
      color: #fef3c7;
      font-weight: 500;
    }
    .milestone-label {
      font-weight: 700;
      color: var(--accent-amber);
      text-transform: uppercase;
      font-size: 0.75rem;
      letter-spacing: 0.05em;
      margin-bottom: 2px;
    }

    /* Scope & Evaluation Notes */
    .notes-card {
      background: rgba(15, 23, 42, 0.7);
      border: 1px solid var(--border-subtle);
      border-radius: 16px;
      padding: 28px;
      margin: 48px 0;
    }
    .notes-card h3 {
      font-size: 1.15rem;
      font-weight: 700;
      color: #f8fafc;
      margin-bottom: 16px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .notes-list {
      list-style-type: none;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 14px;
    }
    .notes-list li {
      background: rgba(255, 255, 255, 0.02);
      border: 1px solid var(--border-subtle);
      border-radius: 8px;
      padding: 12px 14px;
      font-size: 0.88rem;
      color: #cbd5e1;
      line-height: 1.5;
    }
    .notes-list strong {
      color: #38bdf8;
    }

    /* Footer */
    footer {
      border-top: 1px solid var(--border-subtle);
      padding: 36px 0;
      text-align: center;
      font-size: 0.86rem;
      color: var(--text-dim);
    }
    footer p {
      margin-bottom: 8px;
    }

    /* Floating Scroll-to-Top / Jump to Current */
    .floating-nav {
      position: fixed;
      bottom: 24px;
      right: 24px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      z-index: 99;
    }
    .fab-btn {
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      padding: 10px 16px;
      border-radius: 30px;
      font-size: 0.82rem;
      font-weight: 600;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      backdrop-filter: blur(8px);
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
      cursor: pointer;
      transition: all 0.2s;
    }
    .fab-btn:hover {
      background: #0284c7;
      border-color: #38bdf8;
      color: #ffffff;
      transform: translateY(-2px);
    }

    /* Pulse animation for current week highlight trigger */
    .highlight-flash {
      animation: flashGlow 2s ease-in-out;
    }
    @keyframes flashGlow {
      0% { box-shadow: 0 0 0px #06b6d4; }
      50% { box-shadow: 0 0 40px #06b6d4, 0 0 20px #38bdf8; }
      100% { box-shadow: 0 0 28px rgba(6, 182, 212, 0.25); }
    }

    @media print {
      body { background: #ffffff; color: #000000; }
      .announcement-bar, .controls-toolbar, .floating-nav, .stepper-section { display: none; }
      .week-card { border: 1px solid #cccccc; background: #ffffff; color: #000000; margin-bottom: 12px; page-break-inside: avoid; }
      .timeline-container::before { background: #cccccc; }
      .phase-divider { background: #f1f5f9; color: #000000; border-left: 4px solid #003366; }
    }
  </style>
</head>
<body>

  <!-- Top Announcement Bar with Live Status -->
  <div class="announcement-bar">
    <div class="container announcement-inner">
      <div class="live-status">
        <span class="pulse-dot"></span>
        <span>CURRENT RESEARCH SPRINT: Week 33 of 46 (11 Nov – 17 Nov 2026)</span>
        <span style="color: var(--text-dim);">|</span>
        <span style="color: #cbd5e1;">Today: 13 Nov 2026 (Sprint Day 3/7)</span>
      </div>
      <div>
        <button class="jump-btn" onclick="scrollToCurrentWeek()">
          <span>🎯 Jump to Current Week (Week 33)</span>
        </button>
      </div>
    </div>
  </div>

  <div class="container">
    
    <!-- Hero Header -->
    <header class="hero">
      <div class="badge-pill">
        <span>🎓 MSc Research Project</span>
        <span>•</span>
        <span>University of Colombo (UoC 24440086)</span>
      </div>
      <h1>MSc Research Project Timeline</h1>
      <p class="lead">
        Comprehensive 46-Week Execution Plan: Electromagnetic Side-Channel Analysis of CMOS Switching Activity, Biot-Savart Modeling, and HackRF One SDR Hardware Reconciliation.
      </p>
      
      <div class="meta-tags">
        <div class="meta-tag">
          <span>📅</span>
          <span><strong>Period:</strong> 01 Apr 2026 – 15 Feb 2027</span>
        </div>
        <div class="meta-tag">
          <span>⏱️</span>
          <span><strong>Working Pattern:</strong> 33 hrs/week (Mon–Fri: 4h, Sat–Sun: 6.5h)</span>
        </div>
        <div class="meta-tag">
          <span>🎯</span>
          <span><strong>Total Planned Hours:</strong> 1,514 Hours</span>
        </div>
        <div class="meta-tag">
          <span>🔬</span>
          <span><strong>Target IC:</strong> SN74HC04N CMOS Inverter</span>
        </div>
      </div>
    </header>

    <!-- KPI Cockpit Cards -->
    <section class="cockpit-grid">
      
      <!-- Overall Progress -->
      <div class="kpi-card" style="--card-accent: #06b6d4;">
        <div class="kpi-label">Project Completion Status</div>
        <div class="kpi-value" style="color: #38bdf8;">70.5%</div>
        <div class="progress-track">
          <div class="progress-fill" style="width: 70.5%;"></div>
        </div>
        <div class="kpi-subtext"><strong>32.4 of 46 Weeks</strong> completed (13.6 weeks remaining)</div>
      </div>

      <!-- Current Week -->
      <div class="kpi-card" style="--card-accent: #3b82f6;">
        <div class="kpi-label">Active Research Sprint</div>
        <div class="kpi-value">Week 33</div>
        <div class="kpi-subtext" style="color: #93c5fd;"><strong>11 Nov 2026 – 17 Nov 2026</strong></div>
        <div class="kpi-subtext" style="margin-top: 4px;">Phase 6: IQ Processing & Spectral Analysis</div>
      </div>

      <!-- Research Hours -->
      <div class="kpi-card" style="--card-accent: #10b981;">
        <div class="kpi-label">Planned Hours Logged</div>
        <div class="kpi-value" style="color: #34d399;">1,068 hrs</div>
        <div class="kpi-subtext">Out of <strong>1,514 planned hours</strong> (446 hrs remaining)</div>
        <div class="kpi-subtext" style="margin-top: 4px;">Pace: 4h/weekday, 6.5h/weekend</div>
      </div>

      <!-- Key Milestones -->
      <div class="kpi-card" style="--card-accent: #f59e0b;">
        <div class="kpi-label">Major Milestone Progress</div>
        <div class="kpi-value" style="color: #fbbf24;">5 / 9</div>
        <div class="kpi-subtext"><strong>5 major milestones completed</strong></div>
        <div class="kpi-subtext" style="margin-top: 4px;">Next Milestone: Week 35 (IQ Processing Complete)</div>
      </div>

    </section>

    <!-- Interactive Stepper (All 9 Phases) -->
    <section class="stepper-section">
      <div class="stepper-header">
        <h3>Research Phases Overview (Click to Navigate)</h3>
        <span style="font-size: 0.82rem; color: var(--text-muted);">Phases 1–5 Done • Phase 6 Active • Phases 7–9 Upcoming</span>
      </div>
      <div class="stepper-grid" id="stepperGrid">
        <!-- Rendered by JS -->
      </div>
    </section>

    <!-- Controls Toolbar (Search & Filter) -->
    <div class="controls-toolbar">
      <div class="filter-group">
        <button class="filter-btn active" data-filter="all" onclick="applyFilter('all')">All Weeks (46)</button>
        <button class="filter-btn" data-filter="completed" onclick="applyFilter('completed')">Completed (1–32)</button>
        <button class="filter-btn" data-filter="current" onclick="applyFilter('current')">Active (Week 33)</button>
        <button class="filter-btn" data-filter="upcoming" onclick="applyFilter('upcoming')">Upcoming (34–46)</button>
        <button class="filter-btn" data-filter="milestone" onclick="applyFilter('milestone')">⭐ Milestones Only (9)</button>
      </div>
      <div class="search-box">
        <span class="search-icon">🔍</span>
        <input type="text" id="searchInput" class="search-input" placeholder="Search tasks, SPICE, HackRF, Welch..." oninput="handleSearch()">
      </div>
    </div>

    <!-- Timeline Render -->
    <main class="timeline-container" id="timelineList">
      <!-- Injected by JS -->
    </main>

    <!-- Scope and Assumptions Notes -->
    <section class="notes-card">
      <h3>📌 Scope & Methodological Assumptions (Reference Notes)</h3>
      <ul class="notes-list">
        <li>
          <strong>Circuit Realisation:</strong> The LTspice four-inverter bank and the physical SN74HC04N experiment are related test arrangements designed to evaluate transition dynamics; they are not exact physical replicas.
        </li>
        <li>
          <strong>Hamming Metric:</strong> Hamming distance is treated as a switching-activity indicator, not as a direct linear measurement of supply current or electromagnetic radiation.
        </li>
        <li>
          <strong>Electromagnetic Modeling:</strong> The simplified two-conductor model uses stated geometric assumptions (r1 = 100 um, r2 = 120 um); it is an analytical formulation rather than a full 3D FEM solver.
        </li>
        <li>
          <strong>Derivative Principle:</strong> The calculated derivative dB/dt represents the time rate of change of magnetic flux density and is not directly an electric-field measurement.
        </li>
        <li>
          <strong>Relative Calibration:</strong> HackRF One IQ amplitudes are not calibrated to absolute magnetic flux density (Tesla). The comparison focuses on frequency-domain characteristics and relative spectral prominence.
        </li>
        <li>
          <strong>Observation Bandwidth:</strong> For recordings made at fc = 40.0 MHz and fs = 20.0 MS/s, the observable RF band is 30.0–50.0 MHz. Comparisons are strictly restricted to this observable range.
        </li>
      </ul>
    </section>

    <!-- Footer -->
    <footer>
      <p><strong>MSc Research Project Timeline</strong> • Department of Computer Science, University of Colombo (UoC)</p>
      <p>Student ID: 24440086 • Researcher: Sanjey Asirvatham</p>
      <p style="margin-top: 12px;">
        <a href="https://github.com/sanjeyasir/msc_research_project_uoc_24440086" target="_blank">View GitHub Repository</a> • 
        <a href="README.md">README Overview</a> • 
        <a href="MSc_Research_Detailed_Timeline.txt" target="_blank">Raw Timeline Text</a>
      </p>
    </footer>

  </div>

  <!-- Floating Nav Buttons -->
  <div class="floating-nav">
    <button class="fab-btn" onclick="scrollToCurrentWeek()">
      <span>🎯 Week 33 (Current)</span>
    </button>
    <button class="fab-btn" onclick="window.scrollTo({ top: 0, behavior: 'smooth' })">
      <span>⬆️ Top</span>
    </button>
  </div>

  <!-- Data and Interactive Script -->
  <script>
    const phasesData = __PHASES_JSON__;
    const weeksData = __WEEKS_JSON__;

    let currentFilter = 'all';
    let searchQuery = '';

    // Render Stepper Nodes
    function renderStepper() {
      const grid = document.getElementById('stepperGrid');
      grid.innerHTML = phasesData.map(p => {
        const statusClass = p.status === 'completed' ? 'completed' : (p.status === 'active' ? 'active' : 'upcoming');
        const badgeText = p.status === 'completed' ? 'Done' : (p.status === 'active' ? 'ACTIVE' : 'Upcoming');
        return `
          <div class="step-node ${statusClass}" onclick="scrollToPhase(${p.id})">
            <div class="step-num">Phase ${p.id}</div>
            <div class="step-name">${p.name}</div>
            <span class="step-badge">${badgeText}</span>
          </div>
        `;
      }).join('');
    }

    // Render Timeline
    function renderTimeline() {
      const container = document.getElementById('timelineList');
      let html = '';

      phasesData.forEach(phase => {
        const phaseWeeks = weeksData.filter(w => w.phase_id === phase.id);
        
        const phaseStatusBadge = phase.status === 'completed' 
          ? '<span class="phase-badge badge-comp">Completed</span>'
          : (phase.status === 'active' 
              ? '<span class="phase-badge badge-curr">ACTIVE NOW • WEEK 33</span>' 
              : '<span class="phase-badge badge-upc">Upcoming</span>');
              
        const phaseColor = phase.status === 'completed' ? '#10b981' : (phase.status === 'active' ? '#06b6d4' : '#64748b');

        html += `
          <div class="phase-divider" id="phase-${phase.id}" style="--phase-color: ${phaseColor};">
            <div class="phase-divider-top">
              <div class="phase-title-grp">
                <span class="phase-icon">${phase.icon}</span>
                <span class="phase-title">Phase ${phase.id}: ${phase.name}</span>
              </div>
              <div>${phaseStatusBadge}</div>
            </div>
            <div class="phase-meta">
              <span>📅 ${phase.dates}</span> • 
              <span>⏱️ ${phase.total_weeks} Weeks (${phase.hours} planned hours)</span> • 
              <span style="color: #cbd5e1;">${phase.description}</span>
            </div>
          </div>
        `;

        phaseWeeks.forEach(w => {
          const isMilestone = w.milestone && w.milestone.length > 0;
          const statusClass = w.status === 'completed' ? 'completed' : (w.status === 'current' ? 'current' : 'upcoming');
          const bulletColor = w.status === 'completed' ? '#10b981' : (w.status === 'current' ? '#06b6d4' : '#475569');
          const statusTag = w.status === 'completed'
            ? '<span class="status-tag status-completed">Completed</span>'
            : (w.status === 'current' 
                ? '<span class="status-tag status-current">CURRENT SPRINT</span>' 
                : '<span class="status-tag status-upcoming">Upcoming</span>');

          html += `
            <div class="week-item ${statusClass}" id="week-${w.week}" data-status="${w.status}" data-milestone="${isMilestone ? 'true' : 'false'}" data-text="${w.body.toLowerCase()} ${w.milestone.toLowerCase()}">
              <div class="week-bullet" style="--bullet-color: ${bulletColor};"></div>
              <div class="week-card">
                ${w.status === 'current' ? `
                  <div class="current-week-flag">
                    <span class="pulse-dot"></span>
                    <span>WHERE YOU CURRENTLY ARE AT • 13 NOVEMBER 2026 (DAY 3/7)</span>
                  </div>
                ` : ''}
                <div class="week-card-header">
                  <div class="week-title-wrap">
                    <span class="week-num">WEEK ${w.week}</span>
                    <span class="week-dates">${w.dates}</span>
                  </div>
                  <div class="week-badges">
                    <span class="hours-tag">${w.hours} hrs</span>
                    ${statusTag}
                  </div>
                </div>
                <div class="week-body">
                  ${w.body}
                </div>
                ${isMilestone ? `
                  <div class="milestone-callout">
                    <span class="milestone-icon">⭐</span>
                    <div>
                      <div class="milestone-label">Key Phase Milestone</div>
                      <div class="milestone-text">${w.milestone}</div>
                    </div>
                  </div>
                ` : ''}
              </div>
            </div>
          `;
        });
      });

      container.innerHTML = html;
      applyFilterAndSearch();
    }

    function applyFilter(filter) {
      currentFilter = filter;
      document.querySelectorAll('.filter-btn').forEach(btn => {
        if (btn.getAttribute('data-filter') === filter) {
          btn.classList.add('active');
        } else {
          btn.classList.remove('active');
        }
      });
      applyFilterAndSearch();
    }

    function handleSearch() {
      searchQuery = document.getElementById('searchInput').value.toLowerCase().trim();
      applyFilterAndSearch();
    }

    function applyFilterAndSearch() {
      const items = document.querySelectorAll('.week-item');
      items.forEach(item => {
        const status = item.getAttribute('data-status');
        const isMilestone = item.getAttribute('data-milestone') === 'true';
        const text = item.getAttribute('data-text');

        let matchesFilter = true;
        if (currentFilter === 'completed') matchesFilter = (status === 'completed');
        else if (currentFilter === 'current') matchesFilter = (status === 'current');
        else if (currentFilter === 'upcoming') matchesFilter = (status === 'upcoming');
        else if (currentFilter === 'milestone') matchesFilter = isMilestone;

        let matchesSearch = true;
        if (searchQuery.length > 0) {
          matchesSearch = text.includes(searchQuery);
        }

        if (matchesFilter && matchesSearch) {
          item.classList.remove('hidden');
        } else {
          item.classList.add('hidden');
        }
      });
    }

    function scrollToPhase(phaseId) {
      const el = document.getElementById(`phase-${phaseId}`);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }

    function scrollToCurrentWeek() {
      if (currentFilter !== 'all' && currentFilter !== 'current') {
        applyFilter('all');
      }
      const el = document.getElementById('week-33');
      if (el) {
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        const card = el.querySelector('.week-card');
        card.classList.add('highlight-flash');
        setTimeout(() => {
          card.classList.remove('highlight-flash');
        }, 2200);
      }
    }

    document.addEventListener('DOMContentLoaded', () => {
      renderStepper();
      renderTimeline();
    });
  </script>
</body>
</html>
"""

html_final = html_content.replace("__PHASES_JSON__", phases_json).replace("__WEEKS_JSON__", weeks_json)

with open(output_html, 'w', encoding='utf-8') as f:
    f.write(html_final)
print(f"Generated: {output_html}")
