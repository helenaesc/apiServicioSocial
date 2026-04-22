INDEX_HTML = r"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Registro de Proyectos</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
  <style>
    :root {
      --bg: #f4f7fa;
      --bg-soft: #fbfcfe;
      --panel: #ffffff;
      --panel-soft: #f8fbff;
      --text: #111827;
      --text-soft: #6b7280;
      --muted: #98a2b3;
      --line: #e5e7eb;
      --line-strong: #d1d5db;

      --blue: #3B82F6;
      --orange: #FF8C42;
      --green: #43AA8B;
      --pink: #F25C78;
      --purple: #7D5BA6;

      --blue-soft: #EFF6FF;
      --orange-soft: #FFF3EA;
      --green-soft: #ECFDF7;
      --pink-soft: #FFF1F5;
      --purple-soft: #F5F0FB;

      --shadow-sm: 0 4px 16px rgba(16, 24, 40, 0.05);
      --shadow-md: 0 12px 28px rgba(16, 24, 40, 0.08);
      --shadow-lg: 0 20px 40px rgba(16, 24, 40, 0.10);

      --r-sm: 12px;
      --r-md: 16px;
      --r-lg: 22px;
      --r-xl: 28px;
      --r-pill: 999px;
    }

    * { box-sizing: border-box; }

    html, body {
      margin: 0;
      padding: 0;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: radial-gradient(circle at top left, #ffffff 0%, #f7f9fd 28%, #f4f7fa 100%);
      color: var(--text);
      min-height: 100vh;
    }

    .hidden { display: none !important; }

    .page-shell {
      max-width: 1460px;
      margin: 0 auto;
      padding: 20px;
    }

    .topbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 14px;
      flex-wrap: wrap;
      margin-bottom: 18px;
    }

    .brand {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .brand strong {
      font-size: 1.2rem;
      font-weight: 900;
      letter-spacing: -.02em;
    }

    .brand span {
      font-size: .92rem;
      color: var(--text-soft);
    }

    .top-actions {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
    }

    .link-btn {
      text-decoration: none;
      border: 1px solid var(--line);
      background: white;
      color: var(--text-soft);
      border-radius: var(--r-md);
      padding: 10px 14px;
      font-size: .9rem;
      font-weight: 800;
      box-shadow: var(--shadow-sm);
      transition: transform .15s ease, box-shadow .15s ease, border-color .15s ease;
    }

    .link-btn:hover {
      transform: translateY(-1px);
      border-color: var(--line-strong);
      box-shadow: var(--shadow-md);
    }

    .msg {
      display: none;
      margin-bottom: 18px;
      padding: 14px 16px;
      border-radius: 14px;
      font-size: .94rem;
      font-weight: 800;
      border: 1px solid transparent;
      box-shadow: var(--shadow-sm);
    }

    .msg.ok {
      display: block;
      background: var(--green-soft);
      color: var(--green);
      border-color: #cdeee4;
    }

    .msg.err {
      display: block;
      background: var(--pink-soft);
      color: var(--pink);
      border-color: #ffd7df;
    }

    .hero {
      position: relative;
      overflow: hidden;
      border: 1px solid var(--line);
      border-radius: var(--r-xl);
      background:
        radial-gradient(circle at top right, rgba(125,91,166,0.15) 0%, rgba(125,91,166,0) 30%),
        radial-gradient(circle at bottom left, rgba(59,130,246,0.10) 0%, rgba(59,130,246,0) 24%),
        linear-gradient(135deg, #ffffff 0%, #f8fbff 100%);
      box-shadow: var(--shadow-lg);
      padding: 24px;
      margin-bottom: 18px;
    }

    .hero-grid {
      display: grid;
      grid-template-columns: 1.2fr .8fr;
      gap: 18px;
      align-items: center;
    }

    .hero-kicker {
      font-size: .76rem;
      text-transform: uppercase;
      letter-spacing: .1em;
      color: var(--purple);
      font-weight: 900;
      margin-bottom: 8px;
    }

    .hero h1 {
      margin: 0 0 10px;
      font-size: clamp(1.8rem, 3vw, 2.7rem);
      line-height: 1.05;
      letter-spacing: -.04em;
    }

    .hero p {
      margin: 0;
      color: var(--text-soft);
      font-size: 1rem;
      line-height: 1.6;
      max-width: 760px;
    }

    .hero-badges {
      margin-top: 16px;
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .hero-side {
      display: grid;
      gap: 12px;
    }

    .hero-panel {
      border: 1px solid var(--line);
      background: rgba(255,255,255,0.84);
      backdrop-filter: blur(8px);
      border-radius: var(--r-lg);
      padding: 16px;
      box-shadow: var(--shadow-sm);
    }

    .hero-panel-label {
      font-size: .74rem;
      text-transform: uppercase;
      letter-spacing: .08em;
      color: var(--muted);
      font-weight: 900;
      margin-bottom: 6px;
    }

    .hero-panel-value {
      font-size: 1rem;
      font-weight: 900;
      line-height: 1.35;
    }

    .hero-panel-sub {
      margin-top: 5px;
      color: var(--text-soft);
      font-size: .88rem;
      line-height: 1.45;
    }

    .chip {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 12px;
      border-radius: var(--r-pill);
      font-size: .8rem;
      font-weight: 900;
      white-space: nowrap;
      border: 1px solid transparent;
    }

    .chip-primary { background: var(--purple-soft); color: var(--purple); border-color: #e6dbf3; }
    .chip-green { background: var(--green-soft); color: var(--green); border-color: #cdeee4; }
    .chip-orange { background: var(--orange-soft); color: var(--orange); border-color: #ffe1cf; }
    .chip-pink { background: var(--pink-soft); color: var(--pink); border-color: #ffd7df; }
    .chip-blue { background: var(--blue-soft); color: var(--blue); border-color: #d6e4ff; }
    .chip-neutral { background: #f2f4f7; color: #475467; border-color: #eaecf0; }

    .nav-strip {
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 12px;
      margin-bottom: 18px;
    }

    .nav-card {
      border: 1px solid var(--line);
      background: white;
      border-radius: var(--r-lg);
      padding: 16px;
      box-shadow: var(--shadow-sm);
      cursor: pointer;
      transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
    }

    .nav-card:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
    }

    .nav-card.active {
      border-color: #d6e4ff;
      background: linear-gradient(135deg, var(--blue-soft) 0%, white 100%);
      box-shadow: var(--shadow-md);
    }

    .nav-card.done {
      border-color: #bee7da;
      background: linear-gradient(135deg, var(--green-soft) 0%, white 100%);
    }

    .nav-card.locked {
      opacity: .55;
      filter: grayscale(.08);
    }

    .nav-card.unlocked {
      border-color: #cdeee4;
      background: linear-gradient(135deg, #f0fdf7 0%, #ffffff 100%);
    }

    .nav-index {
      font-size: .72rem;
      text-transform: uppercase;
      letter-spacing: .08em;
      color: var(--muted);
      font-weight: 900;
      margin-bottom: 6px;
    }

    .nav-title {
      font-size: .98rem;
      font-weight: 900;
      margin-bottom: 4px;
    }

    .nav-desc {
      color: var(--text-soft);
      font-size: .84rem;
      line-height: 1.45;
    }

    .layout {
      display: grid;
      grid-template-columns: 1fr 360px;
      gap: 18px;
      align-items: start;
    }

    .main-column {
      display: grid;
      gap: 18px;
    }

    .side-column {
      position: sticky;
      top: 20px;
      display: grid;
      gap: 18px;
    }

    .section {
      display: none;
    }

    .section.active {
      display: block;
    }

    .card {
      border: 1px solid var(--line);
      background: linear-gradient(180deg, #ffffff 0%, #fcfdff 100%);
      border-radius: var(--r-lg);
      padding: 22px;
      box-shadow: var(--shadow-md);
    }

    .card-title-row {
      display: flex;
      justify-content: space-between;
      align-items: start;
      gap: 12px;
      flex-wrap: wrap;
      margin-bottom: 12px;
    }

    .card h2 {
      margin: 0;
      font-size: 1.12rem;
      line-height: 1.2;
      font-weight: 900;
    }

    .card-subtitle {
      color: var(--text-soft);
      font-size: .93rem;
      line-height: 1.55;
      margin-bottom: 14px;
    }

    .form-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }

    .field {
      display: flex;
      flex-direction: column;
      gap: 7px;
    }

    .field.span-2 {
      grid-column: span 2;
    }

    .field label {
      font-size: .76rem;
      text-transform: uppercase;
      letter-spacing: .06em;
      color: var(--muted);
      font-weight: 900;
    }

    input, select, textarea, button {
      font: inherit;
    }

    input, select, textarea {
      width: 100%;
      min-height: 46px;
      border: 1px solid var(--line-strong);
      background: white;
      border-radius: 14px;
      padding: 11px 13px;
      color: var(--text);
      transition: border-color .16s ease, box-shadow .16s ease;
    }

    textarea {
      min-height: 110px;
      resize: vertical;
    }

    input:focus, select:focus, textarea:focus {
      outline: none;
      border-color: var(--blue);
      box-shadow: 0 0 0 4px rgba(59,130,246,0.10);
    }

    .actions {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 16px;
    }

    button {
      border: none;
      min-height: 46px;
      border-radius: 14px;
      padding: 10px 15px;
      font-size: .94rem;
      font-weight: 900;
      cursor: pointer;
      transition: transform .15s ease, box-shadow .15s ease, opacity .15s ease;
    }

    button:hover {
      transform: translateY(-1px);
    }

    .btn-primary {
      background: linear-gradient(135deg, var(--purple) 0%, #9b79c6 100%);
      color: white;
      box-shadow: 0 10px 20px rgba(125,91,166,0.20);
    }

    .btn-green {
      background: linear-gradient(135deg, var(--green) 0%, #57c3a2 100%);
      color: white;
      box-shadow: 0 10px 20px rgba(67,170,139,0.18);
    }

    .btn-orange {
      background: linear-gradient(135deg, var(--orange) 0%, #ffad76 100%);
      color: white;
      box-shadow: 0 10px 20px rgba(255,140,66,0.18);
    }

    .btn-blue {
      background: linear-gradient(135deg, var(--blue) 0%, #60A5FA 100%);
      color: white;
      box-shadow: 0 10px 20px rgba(59,130,246,0.18);
    }

    .btn-secondary {
      background: white;
      color: var(--text-soft);
      border: 1px solid var(--line);
      box-shadow: var(--shadow-sm);
    }

    .catalog-toolbar {
      display: grid;
      grid-template-columns: repeat(6, minmax(0, 1fr));
      gap: 12px;
      margin-bottom: 14px;
    }

    .catalog-stats {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
      flex-wrap: wrap;
      margin-bottom: 14px;
      padding: 14px 16px;
      background: linear-gradient(135deg, #fafbff 0%, #f6f9ff 100%);
      border: 1px solid var(--line);
      border-radius: 16px;
    }

    .catalog-count {
      font-weight: 900;
      font-size: .96rem;
    }

    .catalog-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 16px;
    }

    .project-card {
      position: relative;
      overflow: hidden;
      border: 1px solid var(--line);
      border-radius: 24px;
      background:
        radial-gradient(circle at top right, rgba(59,130,246,0.10) 0%, rgba(59,130,246,0.00) 30%),
        radial-gradient(circle at bottom left, rgba(125,91,166,0.10) 0%, rgba(125,91,166,0.00) 28%),
        linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
      box-shadow: var(--shadow-md);
      padding: 16px;
      transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
    }

    .project-card:hover {
      transform: translateY(-3px);
      box-shadow: var(--shadow-lg);
      border-color: #d6e4ff;
    }

    .project-card.selected {
      border-color: #e2c6ef;
      box-shadow: 0 0 0 4px rgba(125,91,166,0.08), var(--shadow-lg);
    }

    .project-head {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: start;
      margin-bottom: 12px;
    }

    .project-org {
      font-size: .72rem;
      text-transform: uppercase;
      letter-spacing: .08em;
      color: var(--muted);
      font-weight: 900;
      margin-bottom: 4px;
    }

    .project-title {
      font-size: 1.02rem;
      line-height: 1.25;
      font-weight: 900;
      margin-bottom: 3px;
    }

    .project-subtitle {
      color: var(--text-soft);
      font-size: .86rem;
      line-height: 1.4;
    }

    .project-rank {
      min-width: 56px;
      text-align: center;
      border-radius: 16px;
      padding: 10px 8px;
      border: 1px solid #dae7ff;
      background: linear-gradient(180deg, #eff5ff 0%, #ffffff 100%);
      color: var(--blue);
      font-size: .72rem;
      font-weight: 900;
    }

    .project-hero {
      border: 1px solid #e6ecf5;
      border-radius: 18px;
      background: linear-gradient(135deg, #f8fbff 0%, #eef4ff 45%, #faf5ff 100%);
      padding: 14px;
      min-height: 116px;
      display: flex;
      align-items: flex-end;
      margin-bottom: 12px;
    }

    .project-hero-text {
      font-size: .9rem;
      font-weight: 700;
      line-height: 1.5;
      color: #344054;
    }

    .project-stats {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
      margin-bottom: 12px;
    }

    .project-stat {
      border: 1px solid #edf1f7;
      background: #f9fafb;
      border-radius: 14px;
      padding: 10px 12px;
    }

    .project-stat-label {
      display: block;
      font-size: .7rem;
      text-transform: uppercase;
      letter-spacing: .04em;
      color: var(--muted);
      font-weight: 900;
      margin-bottom: 4px;
    }

    .project-stat-value {
      font-size: .88rem;
      font-weight: 800;
      color: var(--text);
      line-height: 1.35;
    }

    .project-extra {
      display: grid;
      gap: 8px;
      margin-bottom: 12px;
    }

    .project-extra-row {
      color: var(--text-soft);
      font-size: .86rem;
      line-height: 1.45;
    }

    .project-extra-row strong {
      color: var(--text);
    }

    .selected-banner {
      border: 1px dashed #e2c6ef;
      background: linear-gradient(135deg, #fcf8ff 0%, #ffffff 100%);
      border-radius: 16px;
      padding: 14px 16px;
      margin-bottom: 14px;
    }

    .selected-banner-title {
      font-size: .88rem;
      color: var(--purple);
      font-weight: 900;
      margin-bottom: 4px;
    }

    .selected-banner-text {
      font-size: .9rem;
      color: var(--text-soft);
      line-height: 1.45;
    }

    .info-stack {
      display: grid;
      gap: 12px;
    }

    .info-card {
      border: 1px solid var(--line);
      background: white;
      border-radius: 18px;
      padding: 16px;
      box-shadow: var(--shadow-sm);
    }

    .info-head {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: start;
      flex-wrap: wrap;
      margin-bottom: 10px;
    }

    .info-title {
      font-size: .98rem;
      font-weight: 900;
    }

    .info-sub {
      color: var(--text-soft);
      font-size: .84rem;
    }

    .meta-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }

    .meta-box {
      border: 1px solid #edf1f7;
      background: #f9fafb;
      border-radius: 14px;
      padding: 10px 12px;
    }

    .meta-label {
      display: block;
      font-size: .7rem;
      text-transform: uppercase;
      letter-spacing: .04em;
      color: var(--muted);
      font-weight: 900;
      margin-bottom: 4px;
    }

    .meta-value {
      font-size: .88rem;
      font-weight: 800;
      line-height: 1.4;
      color: var(--text);
    }

    .mono {
      display: inline-block;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      background: #111827;
      color: #f8fafc;
      border-radius: 12px;
      padding: 9px 11px;
      font-size: .88rem;
      word-break: break-all;
    }

    .mono-soft {
      display: inline-block;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      background: #f2f4f7;
      color: #344054;
      border: 1px solid #eaecf0;
      border-radius: 10px;
      padding: 6px 9px;
      font-size: .82rem;
      word-break: break-all;
    }

    .qr-shell {
      border: 1px solid var(--line);
      background: linear-gradient(180deg, #ffffff 0%, #f9fbff 100%);
      border-radius: 22px;
      padding: 18px;
      display: grid;
      gap: 14px;
      box-shadow: var(--shadow-sm);
    }

    .qr-head {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      flex-wrap: wrap;
      align-items: center;
    }

    .qr-canvas-wrap {
      min-height: 240px;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 1px dashed #d8e4ff;
      background: #fcfdff;
      border-radius: 18px;
    }

    .qr-plain {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      background: #111827;
      color: #f8fafc;
      border-radius: 14px;
      padding: 12px;
      font-size: .9rem;
      text-align: center;
      word-break: break-all;
    }

    .legal-box {
      border: 1px solid #dbeafe;
      background: #f8fbff;
      border-radius: 16px;
      padding: 16px;
      margin-top: 12px;
    }

    .preview-box {
      display: grid;
      gap: 12px;
      margin-top: 14px;
    }

    .success-card {
      border: 1px solid #cceee3;
      background: linear-gradient(135deg, #ecfdf7 0%, #ffffff 100%);
      border-radius: 18px;
      padding: 16px;
      box-shadow: var(--shadow-sm);
    }

    .success-title {
      font-size: 1rem;
      font-weight: 900;
      color: var(--green);
      margin-bottom: 8px;
    }

    .empty-state {
      border: 1px dashed var(--line-strong);
      background: linear-gradient(180deg, #fcfcfd 0%, #f9fafb 100%);
      border-radius: 18px;
      padding: 20px;
      text-align: center;
      color: var(--text-soft);
      box-shadow: var(--shadow-sm);
    }

    .empty-title {
      font-size: .96rem;
      font-weight: 900;
      color: var(--text);
      margin-bottom: 6px;
    }

    @media (max-width: 1280px) {
      .nav-strip {
        grid-template-columns: repeat(3, 1fr);
      }

      .layout {
        grid-template-columns: 1fr;
      }

      .side-column {
        position: static;
      }

      .hero-grid {
        grid-template-columns: 1fr;
      }

      .catalog-toolbar {
        grid-template-columns: repeat(3, minmax(0, 1fr));
      }
    }

    @media (max-width: 820px) {
      .nav-strip {
        grid-template-columns: repeat(2, 1fr);
      }

      .form-grid,
      .meta-grid {
        grid-template-columns: 1fr;
      }

      .field.span-2 {
        grid-column: span 1;
      }

      .catalog-toolbar {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }

      .project-stats {
        grid-template-columns: 1fr;
      }
    }

    @media (max-width: 560px) {
      .page-shell {
        padding: 14px;
      }

      .nav-strip {
        grid-template-columns: 1fr;
      }

      .catalog-toolbar {
        grid-template-columns: 1fr;
      }

      .actions {
        flex-direction: column;
      }

      button {
        width: 100%;
      }
    }

    .journey-card {
      border: 1px solid var(--line);
      background:
        radial-gradient(circle at top right, rgba(125,91,166,0.10) 0%, rgba(125,91,166,0) 26%),
        radial-gradient(circle at bottom left, rgba(79,124,255,0.08) 0%, rgba(79,124,255,0) 24%),
        linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
      border-radius: 26px;
      padding: 20px;
      box-shadow: var(--shadow-md);
      margin-bottom: 18px;
    }

    .journey-top {
      display: flex;
      justify-content: space-between;
      align-items: start;
      gap: 12px;
      flex-wrap: wrap;
      margin-bottom: 18px;
    }

    .journey-kicker {
      font-size: .74rem;
      text-transform: uppercase;
      letter-spacing: .08em;
      font-weight: 900;
      color: var(--muted);
      margin-bottom: 6px;
    }

    .journey-title {
      font-size: 1.18rem;
      font-weight: 900;
      color: var(--text);
      line-height: 1.2;
    }

    .journey-subtitle {
      margin-top: 6px;
      color: var(--text-soft);
      font-size: .92rem;
      line-height: 1.45;
      max-width: 760px;
    }

    .journey-badge {
      padding: 10px 14px;
      border-radius: 999px;
      font-size: .82rem;
      font-weight: 900;
      border: 1px solid var(--line);
      background: #f8fafc;
      color: var(--text-soft);
      box-shadow: var(--shadow-sm);
    }

    .journey-track {
      position: relative;
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 16px;
    }

    .journey-line {
      position: absolute;
      top: 22px;
      left: 9%;
      right: 9%;
      height: 6px;
      border-radius: 999px;
      background: #e5e7eb;
      z-index: 0;
    }

    .journey-progress {
      position: absolute;
      top: 22px;
      left: 9%;
      width: 0%;
      height: 6px;
      border-radius: 999px;
      background: linear-gradient(90deg, var(--primary) 0%, var(--green) 100%);
      z-index: 1;
      transition: width .35s ease;
    }

    .journey-step {
      position: relative;
      z-index: 2;
      text-align: center;
    }

    .journey-dot {
      width: 46px;
      height: 46px;
      border-radius: 50%;
      margin: 0 auto 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 900;
      font-size: .95rem;
      background: white;
      border: 2px solid #d0d5dd;
      color: var(--text-soft);
      transition: all .25s ease;
    }

    .journey-label {
      font-size: .9rem;
      font-weight: 900;
      color: var(--text);
    }

    .journey-meta {
      margin-top: 4px;
      font-size: .78rem;
      color: var(--text-soft);
      line-height: 1.35;
    }

    .journey-step.done .journey-dot {
      background: var(--green);
      border-color: var(--green);
      color: white;
      box-shadow: 0 10px 20px rgba(67,170,139,0.18);
    }

    .journey-step.active .journey-dot {
      background: var(--primary);
      border-color: var(--primary);
      color: white;
      box-shadow: 0 10px 22px rgba(125,91,166,0.24);
      transform: scale(1.08);
      animation: journeyPulse 1.5s infinite;
    }

    .journey-step.locked .journey-dot {
      background: #f8fafc;
      border-color: #d0d5dd;
      color: #98a2b3;
    }

    .journey-step.locked .journey-label,
    .journey-step.locked .journey-meta {
      color: #98a2b3;
    }

    .journey-step.error .journey-dot {
      background: var(--pink);
      border-color: var(--pink);
      color: white;
      box-shadow: 0 10px 20px rgba(242,92,120,0.18);
    }


    @keyframes journeyPulse {
      0% { box-shadow: 0 0 0 0 rgba(125,91,166,0.26); }
      70% { box-shadow: 0 0 0 14px rgba(125,91,166,0); }
      100% { box-shadow: 0 0 0 0 rgba(125,91,166,0); }
    }

    .journey-bottom {
      display: grid;
      grid-template-columns: 1fr 220px;
      gap: 12px;
      align-items: stretch;
    }

    .journey-alert {
      border: 1px solid var(--line);
      background: #f8fafc;
      border-radius: 16px;
      padding: 13px 15px;
      color: var(--text-soft);
      font-size: .9rem;
      line-height: 1.45;
    }

    .journey-alert.ok {
      background: var(--green-soft);
      border-color: #cdeee4;
      color: var(--green);
    }

    .journey-alert.warn {
      background: #fff7ed;
      border-color: #fed7aa;
      color: #c2410c;
    }

    .journey-alert.err {
      background: var(--pink-soft);
      border-color: #ffd7df;
      color: var(--pink);
    }

    .journey-timer {
      border: 1px solid #dbeafe;
      background: linear-gradient(180deg, #f8fbff 0%, #ffffff 100%);
      border-radius: 18px;
      padding: 14px;
      box-shadow: var(--shadow-sm);
    }

    .journey-timer-label {
      font-size: .72rem;
      text-transform: uppercase;
      letter-spacing: .08em;
      color: var(--muted);
      font-weight: 900;
      margin-bottom: 6px;
    }

    .journey-timer-value {
      font-size: 1.55rem;
      font-weight: 900;
      color: var(--blue);
      line-height: 1;
      margin-bottom: 6px;
      font-variant-numeric: tabular-nums;
    }

    .journey-timer-sub {
      font-size: .82rem;
      color: var(--text-soft);
      line-height: 1.4;
    }

    @media (max-width: 900px) {
      .journey-bottom {
        grid-template-columns: 1fr;
      }
    }

    @media (max-width: 760px) {
      .journey-track {
        grid-template-columns: 1fr 1fr;
        row-gap: 22px;
      }

      .journey-line,
      .journey-progress {
        display: none;
      }
    }
    
    .qr-timer-box {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 14px;
      border-radius: 999px;
      font-weight: 800;
      font-size: .92rem;
      transition: all .25s ease;
      background: rgba(59,130,246,.12);
      color: #2563eb;
      border: 1px solid rgba(59,130,246,.18);
    }

    .qr-timer-box.warn {
      background: rgba(245,158,11,.12);
      color: #d97706;
      border-color: rgba(245,158,11,.22);
    }

    .qr-timer-box.danger {
      background: rgba(239,68,68,.12);
      color: #dc2626;
      border-color: rgba(239,68,68,.22);
    }

    .qr-timer-box.expired {
      background: rgba(107,114,128,.14);
      color: #4b5563;
      border-color: rgba(107,114,128,.22);
    }  

    .smart-toast {
      position: fixed;
      right: 18px;
      bottom: 18px;
      z-index: 9999;
      min-width: 280px;
      max-width: 360px;
      background: #111827;
      color: white;
      border-radius: 16px;
      padding: 14px 16px;
      box-shadow: 0 16px 40px rgba(0,0,0,.22);
      transform: translateY(20px);
      opacity: 0;
      pointer-events: none;
      transition: all .28s ease;
    }

    .smart-toast.show {
      transform: translateY(0);
      opacity: 1;
    }

    .smart-toast__title {
      font-weight: 900;
      margin-bottom: 4px;
    }

    .smart-toast__text {
      font-size: .92rem;
      color: rgba(255,255,255,.84);
    }

    .catalog-card.selected {
      outline: 2px solid rgba(59,130,246,.42);
      box-shadow: 0 16px 36px rgba(37,99,235,.14);
      transform: translateY(-2px);
    }

    .catalog-card .selected-pill {
      display: none;
    }

    .catalog-card.selected .selected-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 10px;
      border-radius: 999px;
      background: rgba(59,130,246,.12);
      color: #2563eb;
      font-size: .8rem;
      font-weight: 800;
    }

    .success-shell {
      background: linear-gradient(135deg, rgba(16,185,129,.10), rgba(59,130,246,.08));
      border: 1px solid rgba(16,185,129,.16);
      border-radius: 22px;
      padding: 22px;
      text-align: center;
    }

    .success-icon {
      width: 72px;
      height: 72px;
      margin: 0 auto 14px;
      border-radius: 50%;
      display: grid;
      place-items: center;
      font-size: 2rem;
      font-weight: 900;
      background: rgba(16,185,129,.14);
      color: #059669;
    }

    .success-title {
      font-size: 1.25rem;
      font-weight: 900;
      margin-bottom: 6px;
    }

    .success-sub {
      color: var(--text-soft);
      max-width: 640px;
      margin: 0 auto;
    }

    .step4-shell {
      display: grid;
      gap: 14px;
    }

    .step4-statebar {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }

    .step4-pill {
      padding: 8px 12px;
      border-radius: 999px;
      font-size: .84rem;
      font-weight: 800;
      border: 1px solid transparent;
      background: #f3f4f6;
      color: #374151;
    }

    .step4-pill.ok {
      background: rgba(16,185,129,.12);
      color: #047857;
      border-color: rgba(16,185,129,.2);
    }

    .step4-pill.warn {
      background: rgba(245,158,11,.12);
      color: #b45309;
      border-color: rgba(245,158,11,.2);
    }

    .step4-pill.err {
      background: rgba(239,68,68,.12);
      color: #b91c1c;
      border-color: rgba(239,68,68,.2);
    }

    .step4-preview-card {
      border: 1px solid rgba(59,130,246,.14);
      background: linear-gradient(135deg, rgba(59,130,246,.05), rgba(255,255,255,1));
      border-radius: 18px;
      padding: 16px;
    }

    .step4-preview-title {
      font-weight: 900;
      margin-bottom: 6px;
    }

    .step4-preview-sub {
      color: var(--text-soft);
      font-size: .92rem;
      margin-bottom: 12px;
    }

    .step4-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 10px;
    }

    .step4-confirm-box {
      border: 1px dashed rgba(16,185,129,.28);
      background: rgba(16,185,129,.05);
      border-radius: 18px;
      padding: 16px;
    }

    .step4-confirm-ready {
      font-weight: 900;
      color: #047857;
      margin-bottom: 4px;
    }

    .input-ok {
      border-color: rgba(16,185,129,.4) !important;
      box-shadow: 0 0 0 3px rgba(16,185,129,.08);
    }

    .input-err {
      border-color: rgba(239,68,68,.45) !important;
      box-shadow: 0 0 0 3px rgba(239,68,68,.08);
    }

    .pass-card {
      background: linear-gradient(135deg, #111827, #1f2937);
      border-radius: 18px;
      padding: 20px;
      color: white;
      box-shadow: 0 10px 30px rgba(0,0,0,0.4);
    }

    .pass-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .pass-title {
      font-weight: 600;
      font-size: 16px;
    }

    .pass-status {
      font-size: 12px;
      padding: 4px 10px;
      border-radius: 20px;
      background: #374151;
    }

    .pass-body {
      margin-top: 15px;
      text-align: center;
    }

    .pass-name {
      font-size: 18px;
      font-weight: 600;
    }

    .pass-matricula {
      font-size: 13px;
      opacity: 0.7;
    }

    .qr-container {
      margin: 15px 0;
    }

    .qr-expire {
      font-size: 12px;
      opacity: 0.7;
      margin-top: 5px;
    }

    .pass-info {
      font-size: 13px;
      margin-top: 10px;
    }

    .pass-actions {
      margin-top: 15px;
      text-align: center;
    }

    .project-card {
      background: #fff;
      border: 1px solid rgba(15, 23, 42, 0.08);
      border-radius: 18px;
      padding: 16px;
      box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
      transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
    }

    .project-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 12px 30px rgba(15, 23, 42, 0.10);
    }

    .project-card.selected {
      border-color: rgba(37, 99, 235, 0.40);
      box-shadow: 0 14px 34px rgba(37, 99, 235, 0.12);
    }

    .project-card-top {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: flex-start;
    }

    .project-card-title {
      font-size: 15px;
      font-weight: 700;
      color: #0f172a;
    }

    .project-card-subtitle {
      margin-top: 4px;
      font-size: 13px;
      color: #475569;
    }

    .project-card-meta {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 12px;
    }

    .project-card-body {
      margin-top: 14px;
    }
  </style>
</head>
<body>
  <div class="page-shell">
    <div id="msg" class="msg"></div>

    <div class="topbar">
      <div class="brand">
        <strong>Registro de Proyectos</strong>
        <span>Explora, solicita, valida y cierra tu inscripción con una ruta guiada.</span>
      </div>
      <div class="top-actions">
        <a href="/admin" class="link-btn">Admin</a>
        <a href="/health" class="link-btn">Health</a>
      </div>
    </div>

    <section class="hero">
      <div class="hero-grid">
        <div>
          <div class="hero-kicker">Ruta del alumno</div>
          <h1>Explora primero. Decide bien. Regístrate solo cuando ya tengas acceso.</h1>
          <p>
            Puedes revisar el catálogo antes de solicitar tu pase. Cuando el staff te habilite acceso, podrás cerrar tu inscripción con el token del proyecto.
          </p>
          <div class="hero-badges">
            <span class="chip chip-primary">Catálogo visible</span>
            <span class="chip chip-green">Flujo guiado</span>
            <span class="chip chip-blue">Credencial viva</span>
          </div>
        </div>

        <div class="hero-side">
          <div class="hero-panel">
            <div class="hero-panel-label">Estado de ruta</div>
            <div class="hero-panel-value" id="heroRouteStatus">Explorando catálogo</div>
            <div class="hero-panel-sub">Tu progreso se actualiza conforme completas cada paso.</div>
          </div>
          <div class="hero-panel">
            <div class="hero-panel-label">Proyecto actual</div>
            <div class="hero-panel-value" id="heroProjectStatus">Sin proyecto seleccionado</div>
            <div class="hero-panel-sub">Selecciona uno desde el catálogo para preparar tu cierre.</div>
          </div>
        </div>
      </div>
    </section>

    <section class="journey-card" id="studentJourneyCard">
      <div class="journey-top">
        <div>
          <div class="journey-kicker">Ruta inteligente del alumno</div>
          <div class="journey-title" id="journeyTitle">Esperando solicitud</div>
          <div class="journey-subtitle" id="journeySubtitle">
            Completa tu solicitud para comenzar el flujo.
          </div>
        </div>
        <div class="journey-badge" id="journeyBadge">INACTIVO</div>
      </div>

      <div class="journey-track">
        <div class="journey-line"></div>
        <div class="journey-progress" id="journeyProgress"></div>

        <div class="journey-step locked" id="journeyStep1">
          <div class="journey-dot">1</div>
          <div class="journey-label">Solicitud</div>
          <div class="journey-meta" id="journeyMeta1">Pendiente</div>
        </div>

        <div class="journey-step locked" id="journeyStep2">
          <div class="journey-dot">2</div>
          <div class="journey-label">QR activo</div>
          <div class="journey-meta" id="journeyMeta2">Sin pase</div>
        </div>

        <div class="journey-step locked" id="journeyStep3">
          <div class="journey-dot">3</div>
          <div class="journey-label">Validación</div>
          <div class="journey-meta" id="journeyMeta3">Pendiente</div>
        </div>

        <div class="journey-step locked" id="journeyStep4">
          <div class="journey-dot">4</div>
          <div class="journey-label">Inscripción</div>
          <div class="journey-meta" id="journeyMeta4">Bloqueada</div>
        </div>
      </div>

      <div class="journey-bottom">
        <div class="journey-alert" id="journeyAlert">
          Aún no has iniciado tu proceso.
        </div>

        <div class="journey-timer hidden" id="journeyTimerBox">
          <div class="journey-timer-label">Vida del QR</div>
          <div class="journey-timer-value" id="journeyTimerValue">--:--</div>
          <div class="journey-timer-sub" id="journeyTimerSub">
            Tu código cambia cuando se refresca.
          </div>
        </div>
      </div>
    </section>

    <section class="nav-strip" id="stepsBar">
      <div class="nav-card active" data-step="1" onclick="showStudentSection('catalogSection')">
        <div class="nav-index">Paso 1</div>
        <div class="nav-title">Explorar catálogo</div>
        <div class="nav-desc">Busca, compara y elige un proyecto con intención.</div>
      </div>
      <div class="nav-card" data-step="2" onclick="showStudentSection('requestSection')">
        <div class="nav-index">Paso 2</div>
        <div class="nav-title">Solicitar pase</div>
        <div class="nav-desc">Genera tu folio con tus datos completos.</div>
      </div>
      <div class="nav-card" data-step="3" onclick="showStudentSection('passSection')">
        <div class="nav-index">Paso 3</div>
        <div class="nav-title">Mostrar QR</div>
        <div class="nav-desc">Presenta tu credencial viva al staff.</div>
      </div>
      <div class="nav-card" data-step="4" onclick="validateAccessAndShowRegistration()">
        <div class="nav-index">Paso 4</div>
        <div class="nav-title">Cerrar inscripción</div>
        <div class="nav-desc">Haz preview y confirma legalmente.</div>
      </div>
      <div class="nav-card" data-step="5" onclick="showStudentSection('statusSection')">
        <div class="nav-index">Mi estado</div>
        <div class="nav-title">Seguimiento</div>
        <div class="nav-desc">Consulta folio, pase y progreso actual.</div>
      </div>
    </section>

    <div class="layout">
      <main class="main-column">
        <section id="catalogSection" class="section active">
          <div class="card">
            <div class="card-title-row">
              <div>
                <h2>Catálogo de proyectos</h2>
              </div>
              <span class="chip chip-primary">Explorar</span>
            </div>

            <div class="card-subtitle">
              Explora, compara y elige el proyecto que mejor se ajuste a ti. Cuando encuentres uno que te convenza, selecciónalo y continúa con tu solicitud.
            </div>

            <div class="catalog-toolbar">
              <div class="field">
                <label>Temporada</label>
                <select id="seasonSelector">
                  <option value="PRIMAVERA">Primavera</option>
                  <option value="INVIERNO">Invierno</option>
                </select>
              </div>
              <div class="field">
                <label>Buscar</label>
                <input id="catalogSearch" placeholder="Nombre, responsables, comentarios">
              </div>
              <div class="field">
                <label>Carrera preferida</label>
                <select id="filterPartner">
                  <option value="">Todas</option>
                </select>
              </div>
              <div class="field">
                <label>Modalidad</label>
                <select id="filterModality">
                  <option value="">Todas</option>
                </select>
              </div>
              <div class="field">
                <label>Días</label>
                <select id="filterWeekDays">
                  <option value="">Todos</option>
                </select>
              </div>
              <div class="field">
                <label>Horario</label>
                <select id="filterSchedule">
                  <option value="">Todos</option>
                </select>
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-primary" onclick="loadCatalog()">Cargar catálogo</button>
              <button type="button" class="btn-secondary" onclick="resetCatalogFilters()">Limpiar filtros</button>
              <button type="button" class="btn-blue" onclick="goToSectionAndStep('requestSection', 2)">Ya elegí proyecto</button>
            </div>

            <div class="catalog-stats">
              <div class="catalog-count" id="catalogCountLabel">Sin catálogo cargado</div>
              <div style="display:flex; gap:8px; flex-wrap:wrap;">
                <span class="chip chip-blue" id="catalogSeasonChip">Temporada</span>
                <span class="chip chip-neutral" id="catalogProjectsChip">0 proyectos</span>
              </div>
            </div>

            <div id="selectedProjectBanner" class="selected-banner hidden">
              <div class="selected-banner-title">Proyecto seleccionado</div>
              <div id="selectedProjectBannerText" class="selected-banner-text">Aún no seleccionas proyecto.</div>
            </div>

            <div id="catalogList" class="catalog-grid"></div>
          </div>
        </section>

        <section id="requestSection" class="section">
          <div class="card">
            <div class="card-title-row">
              <div>
                <h2>Solicitar pase</h2>
              </div>
              <span class="chip chip-orange">Paso 2</span>
            </div>

            <div class="card-subtitle">
              Esto no te registra todavía. Solo crea tu solicitud y tu folio para que el staff pueda validarte presencialmente.
            </div>

            <div id="resumeFlowBanner" class="selected-banner" style="margin-bottom:14px;">
              <div class="selected-banner-title">¿Ya habías iniciado tu proceso?</div>
              <div id="resumeFlowText" class="selected-banner-text" style="margin-bottom:10px;">
                Escribe tu matrícula y recupera tu avance sin volver a capturar todo.
              </div>

              <div class="actions" style="margin-top:0; margin-bottom:10px;">
                <button type="button" class="btn-blue" onclick="recoverStudentProcess()">
                  Continuar donde me quedé
                </button>
              </div>

              <div class="form-grid" style="margin-bottom:0;">
                <div class="field">
                  <label>Matrícula para recuperar</label>
                  <input
                    id="recoverEnrolmentInput"
                    type="text"
                    inputmode="text"
                    maxlength="9"
                    autocomplete="off"
                    placeholder="Ej. a01234564"
                  />
                  <small class="muted">Úsala si ya habías creado tu solicitud, generado tu QR o estabas por cerrar tu inscripción.</small>
                </div>
              </div>
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Nombre completo</label>
                <input id="fullNameInput"
                  type="text"
                  maxlength="100"
                  autocomplete="name"
                  placeholder="Escribe tu nombre completo"
                />
                <small class="muted">Escríbelo como quieres que quede registrado en tu solicitud.</small>
              </div>
              <div class="field">
                <label>Matrícula</label>
                <input
                  id="enrolmentInput"
                  type="text"
                  inputmode="text"
                  maxlength="9"
                  autocomplete="off"
                  placeholder="Ej. a01234564"
                />
                <small class="muted">Debe tener exactamente 9 caracteres y será la base de tu correo institucional.</small>
              </div>
              <div class="field">
                <label>Correo principal</label>
                <div class="meta-box">
                  <span class="meta-label">Correo institucional</span>
                  <div id="generatedInstitutionalEmail" class="meta-value">Se generará con tu matrícula</div>
                </div>
              </div>
              <div class="field">
                <div>
                  <label for="secondaryEmailInput">Correo alternativo (opcional)</label>
                  <input
                    id="secondaryEmailInput"
                    type="email"
                    maxlength="120"
                    autocomplete="email"
                    placeholder="ejemplo@gmail.com"
                  />
                  <small class="muted">Solo se usará como respaldo en caso necesario.</small>
                </div>
              </div>
              <div class="field">
                <label>Teléfono</label>
                <input
                  id="phoneInput"
                  type="text"
                  inputmode="numeric"
                  maxlength="10"
                  autocomplete="tel"
                  placeholder="10 dígitos"
                />
                <small class="muted">Solo números. Se usará únicamente si hace falta contactarte.</small>
              </div>
              <div class="field">
                <label>Carrera</label>
                <select id="degreeInput">
                  <option value="">Selecciona tu carrera</option>
                </select>
                <small class="muted">Elige la carrera con la que quieres identificar tu solicitud.</small>
              </div>
              <div class="field">
                <label>Semestre</label>
                <input
                  id="semesterInput"
                  type="text"
                  inputmode="numeric"
                  maxlength="2"
                  placeholder="Ej: 5"
                />
                <small class="muted">Captura un valor entre 1 y 20.</small>
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-orange" onclick="createStudentRequest()">Crear solicitud y generar folio</button>
              <button type="button" class="btn-secondary" onclick="loadStudentRequest()">Recuperar mis datos</button>
              <button type="button" class="btn-blue" onclick="goToSectionAndStep('passSection', 3)">Ir a mi QR</button>
            </div>
          </div>
        </section>

        <section id="passSection" class="section">
          <div class="card">
            <div class="card-title-row">
              <div>
                <h2>Credencial viva</h2>
              </div>
              <span class="chip chip-blue">Paso 3</span>
            </div>

            <div class="card-subtitle">
              Refresca tu QR cuando el staff te lo pida. El QR cambia y el anterior deja de servir.
            </div>

            <div class="actions">
              <button type="button" class="btn-blue" onclick="refreshStudentPass()">Refrescar credencial</button>
              <button type="button" class="btn-secondary" onclick="loadStudentPass()">Consultar pase</button>
              <button type="button" class="btn-green" onclick="validateAccessAndGoStep4()">Ya tengo acceso</button>
            </div>

            <div id="passInfo" class="info-stack" style="margin-top:14px;"></div>

            <div class="qr-shell" style="margin-top:14px;">
              <div class="qr-head">
                <div>
                  <div style="font-weight:900; margin-bottom:3px;">QR vigente del pase</div>
                  <div style="font-size:.86rem; color:var(--text-soft);">
                    Este código cambia al refrescarse y deja de servir al expirar o cuando el staff lo usa.
                  </div>
                </div>
                <div id="qrStatusBadge" class="chip chip-neutral">Sin sesión</div>
              </div>
              <div class="qr-canvas-wrap">
                <div id="qrCanvas"></div>
              </div>
              <div id="qrPlainToken" class="qr-plain">Genera tu código</div>
            </div>
          </div>
        </section>

        <section id="registrationSection" class="section">
          <div class="card">
            <div class="card-title-row">
              <div>
                <h2>Cierre de inscripción</h2>
              </div>
              <span class="chip chip-green">Paso 4</span>
            </div>

            <div class="card-subtitle">
              Solo cuando el staff ya te haya habilitado acceso y tengas el token del proyecto, primero haz preview y luego confirma.
            </div>

            <div id="step4GateBox" class="selected-banner" style="margin-bottom:14px;">
              <div class="selected-banner-title">Estado del paso 4</div>
              <div id="step4GateText" class="selected-banner-text">
                Todavía no disponible. Primero solicita tu pase y completa la validación presencial.
              </div>
            </div>

            <div class="step4-shell">
              <div id="step4StateBar" class="step4-statebar"></div>
              <div id="step4PreviewBox"></div>
              <div id="step4ConfirmBox"></div>
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Proyecto seleccionado</label>
                <input id="selectedProjectName" placeholder="Elige un proyecto del catálogo" readonly>
              </div>
              <div class="field">
                <label>ID del proyecto</label>
                <input id="selectedProjectId" placeholder="Se llena al elegir un proyecto" readonly>
              </div>
              <div class="field">
                <label>Token del proyecto</label>
                <input
                  id="projectTokenInput"
                  maxlength="12"
                  placeholder="Token que te entrega el proyecto"
                />
              </div>
              <div class="field">
                <label>Nombre completo para aceptación</label>
                <input id="acceptanceFullNameInput" placeholder="Debe coincidir con tu nombre">
              </div>
              <div class="field">
                <label>Versión legal</label>
                <input id="legalVersionInput" value="v1">
              </div>
            </div>

            <div class="legal-box">
              <div style="font-size:.84rem; font-weight:900; margin-bottom:8px; color:var(--text);">
                Confirmación legal
              </div>
              <label style="display:flex; gap:10px; align-items:flex-start; font-size:.92rem; line-height:1.55; color:var(--text);">
                <input id="acceptanceCheckbox" type="checkbox" style="width:auto; min-height:auto; margin-top:3px;">
                <span>
                  Confirmo que realicé esta inscripción de manera personal, que acepto el proyecto seleccionado y que entiendo que el cierre queda auditado con token y registro digital.
                </span>
              </label>
            </div>

            <div class="actions">
              <button type="button" class="btn-secondary" id="previewRegistrationBtn" onclick="previewRegistration()">Ver preview</button>
              <button type="button" class="btn-green" id="confirmRegistrationBtn" onclick="confirmRegistration()">Confirmar inscripción</button>
              <button type="button" class="btn-blue" onclick="goToSectionAndStep('statusSection', 5)">Ver mi estado</button>
            </div>

            <div id="registrationPreview" class="preview-box"></div>
            <div id="registrationSuccessBox" class="preview-box hidden"></div>
          </div>
        </section>

        <section id="statusSection" class="section">
          <div class="card">
            <div class="card-title-row">
              <div>
                <h2>Mi estado actual</h2>
              </div>
              <span class="chip chip-primary">Seguimiento</span>
            </div>

            <div class="card-subtitle">
              Aquí puedes revisar tu folio, el estado de tu solicitud y tu progreso general dentro del flujo.
            </div>

            <div id="requestInfo" class="info-stack"></div>
          </div>
        </section>
      </main>

      <aside class="side-column">
        <section class="card" id="step4card">
          <div class="card-title-row">
            <div>
              <h2>Resumen de avance</h2>
            </div>
            <span class="chip chip-neutral">Ruta</span>
          </div>

          <div class="info-stack">
            <div class="info-card">
              <div class="info-head">
                <div>
                  <div class="info-title">Estado actual</div>
                  <div class="info-sub">Lectura rápida de tu progreso</div>
                </div>
              </div>
              <div class="meta-grid">
                <div class="meta-box">
                  <span class="meta-label">Ruta</span>
                  <div class="meta-value" id="sideRouteStatus">Explorando catálogo</div>
                </div>
                <div class="meta-box">
                  <span class="meta-label">Proyecto</span>
                  <div class="meta-value" id="sideProjectStatus">Sin selección</div>
                </div>
              </div>
            </div>

            <div class="info-card">
              <div class="info-head">
                <div>
                  <div class="info-title">Atajos</div>
                  <div class="info-sub">Muévete rápido según tu estado</div>
                </div>
              </div>
              <div class="actions" style="margin-top:0;">
                <button type="button" class="btn-secondary" onclick="showStudentSection('catalogSection')">Catálogo</button>
                <button type="button" class="btn-secondary" onclick="showStudentSection('requestSection')">Pase</button>
                <button type="button" class="btn-secondary" onclick="showStudentSection('passSection')">QR</button>
                <button type="button" class="btn-secondary" onclick="validateAccessAndShowRegistration()">Registro</button>
              </div>
            </div>
          </div>
        </section>
      </aside>
    </div>
  </div>

  <script>
    let currentCatalog = [];
    let currentRequest = null;
    let currentPass = null;
    let currentPreview = null;
    let currentSelectedProject = null;
    let currentRegistration = null;
    let catalogSearchTimer = null;
    let canStudentRegister = false;
    let currentRequestStatus = null;
    let journeyTimerInterval = null;
    let currentAccessUnlocked = false;
    let studentAutoSyncInterval = null;
    let lastKnownStudentStatus = null;
    let currentPlainQrToken = '';
    
    function humanizeErrorMessage(err) {
      const raw =
        (typeof err === 'string' ? err : '') ||
        err?.error ||
        err?.message ||
        '';

      const msg = raw.toLowerCase();

      // --- TOKENS ---
      if (msg.includes('token no existe')) {
        return 'Ese token no existe. Verifica que esté bien escrito.';
      }

      if (msg.includes('token expir')) {
        return 'Ese token ya expiró. Solicita uno nuevo al socio del proyecto.';
      }

      if (msg.includes('token ya fue utilizado')) {
        return 'Ese token ya fue utilizado y no puede volver a usarse.';
      }

      if (msg.includes('token fue revocado')) {
        return 'Ese token fue revocado. Solicita uno nuevo al responsable del proyecto.';
      }

      if (msg.includes('token no corresponde')) {
        return 'Ese token no pertenece al proyecto seleccionado.';
      }

      if (msg.includes('token está reservado')) {
        return 'Ese token está reservado por otro alumno.';
      }

      // --- SOLICITUD ---
      if (msg.includes('no existe solicitud')) {
        return 'No tienes una solicitud para esta temporada. Primero solicita tu pase.';
      }

      if (msg.includes('no está habilitada para registro')) {
        return 'Aún no estás habilitado por staff. Muestra tu QR para validación.';
      }

      if (msg.includes('ya tiene un registro activo')) {
        return 'Ya estás inscrito en esta temporada.';
      }

      if (msg.includes('solicitud ya no permite acceso')) {
        return 'Esta solicitud ya fue cerrada o cancelada.';
      }

      // --- QR / PASE ---
      if (msg.includes('qr no reconocido')) {
        return 'El QR no es válido. Genera uno nuevo.';
      }

      if (msg.includes('qr expirado')) {
        return 'El QR expiró. Pide al alumno que lo refresque.';
      }

      if (msg.includes('qr no disponible')) {
        return 'Este QR ya no está disponible (puede haber sido usado o expirado).';
      }

      if (msg.includes('la sesión ya no está activa')) {
        return 'La sesión del QR ya no está activa.';
      }

      // --- MATRÍCULA ---
      if (msg.includes('matrícula no coincide')) {
        return 'La matrícula no coincide con la del pase.';
      }

      // --- PROYECTOS ---
      if (msg.includes('proyecto no pertenece')) {
        return 'El proyecto no corresponde a la temporada seleccionada.';
      }

      if (msg.includes('proyecto no está disponible')) {
        return 'Este proyecto ya no está disponible para inscripción.';
      }

      // --- CAMPOS ---
      if (msg.includes('es obligatorio')) {
        return 'Faltan campos obligatorios. Revisa la información.';
      }

      // --- TEMPORADA ---
      if (msg.includes('temporada inválida')) {
        return 'La temporada seleccionada no es válida.';
      }

      if (msg.includes('no hay temporada visible')) {
        return 'No hay temporada activa disponible en este momento.';
      }

      // --- FALLBACK ---
      if (raw) {
        return raw; // muestra mensaje backend si no lo reconocemos
      }

      return 'Ocurrió un error inesperado. Intenta nuevamente.';
    }

    function getStudentStatus() {
      return (
        currentRequest?.request?.status ||
        currentRequest?.status ||
        currentPass?.request?.status ||
        currentRequestStatus ||
        null
      );
    }

    function hasJourneyQrEvidence() {
      const status = getStudentStatus();
      return ['VALIDATED', 'ACCESS_ENABLED', 'REGISTERED'].includes(String(status || '').toUpperCase());
    }

    function syncRegistrationLock() {
      const step4Card = document.querySelector('.nav-card[data-step="4"]');
      const previewBtn = document.getElementById('previewRegistrationBtn');
      const confirmBtn = document.getElementById('confirmRegistrationBtn');
      const tokenInput = document.getElementById('projectTokenInput');
      const nameInput = document.getElementById('acceptanceFullNameInput');
      const legalInput = document.getElementById('legalVersionInput');
      const checkbox = document.getElementById('acceptanceCheckbox');

      const status = getStudentStatus();

      canStudentRegister =
        !!currentRegistration ||
        status === 'ACCESS_ENABLED' ||
        status === 'REGISTERED';

      if (step4Card) {
        step4Card.style.pointerEvents = canStudentRegister ? 'auto' : 'none';
        step4Card.title = canStudentRegister
          ? ''
          : 'Bloqueado: primero debes mostrar tu QR al staff para habilitar acceso';

        step4Card.classList.remove('locked', 'unlocked');
        step4Card.classList.add(canStudentRegister ? 'unlocked' : 'locked');
      }

      if (previewBtn) previewBtn.disabled = !canStudentRegister;
      if (confirmBtn) confirmBtn.disabled = !canStudentRegister;
      if (tokenInput) tokenInput.disabled = !canStudentRegister;
      if (nameInput) nameInput.disabled = !canStudentRegister;
      if (legalInput) legalInput.disabled = !canStudentRegister;
      if (checkbox) checkbox.disabled = !canStudentRegister;
    }

    function syncStep4GateText() {
      const gateText = document.getElementById('step4GateText');
      if (!gateText) return;

      const status = getStudentStatus();

      if (!status) {
        gateText.textContent = 'Todavía no disponible. Primero solicita tu pase y completa la validación presencial.';
        return;
      }

      if (status === 'REQUESTED') {
        gateText.textContent = 'Tu solicitud ya existe. Ahora debes generar y mostrar tu QR al staff.';
        return;
      }

      if (status === 'VALIDATED') {
        gateText.textContent = 'Ya fuiste validado, pero staff todavía no habilita tu acceso al cierre.';
        return;
      }

      if (status === 'ACCESS_ENABLED') {
        gateText.textContent = 'Paso 4 desbloqueado. Ya puedes capturar el token del proyecto y confirmar tu inscripción.';
        return;
      }

      if (status === 'REGISTERED') {
        gateText.textContent = 'Tu inscripción ya fue completada correctamente.';
        return;
      }

      if (status === 'CANCELLED' || status === 'CLOSED') {
        gateText.textContent = 'Tu solicitud está cerrada. Necesitas apoyo de administración para continuar.';
        return;
      }

      gateText.textContent = `Estado actual: ${status}`;
    }

    function renderStep4PremiumState() {
      const stateBar = document.getElementById('step4StateBar');
      const previewBox = document.getElementById('step4PreviewBox');
      const confirmBox = document.getElementById('step4ConfirmBox');

      if (!stateBar || !previewBox || !confirmBox) return;

      const status = getStudentStatus();
      const tokenValue = document.getElementById('projectTokenInput')?.value.trim() || '';
      const acceptedFullName = document.getElementById('acceptanceFullNameInput')?.value.trim() || '';
      const legalVersion = document.getElementById('legalVersionInput')?.value.trim() || 'v1';
      const acceptedCheckbox = !!document.getElementById('acceptanceCheckbox')?.checked;

      const tokenReady = tokenValue.length > 0;
      const nameReady = acceptedFullName.length > 0;
      const legalReady = legalVersion.length > 0;
      const checkboxReady = acceptedCheckbox;
      const previewReady = !!currentPreview;
      const canAccess = status === 'ACCESS_ENABLED' || status === 'REGISTERED' || !!currentRegistration;
      const canConfirm = canAccess && tokenReady && nameReady && legalReady && checkboxReady && previewReady;

      stateBar.innerHTML = `
        <div class="step4-pill ${canAccess ? 'ok' : 'warn'}">
          ${canAccess ? 'Acceso habilitado' : 'Paso bloqueado'}
        </div>
        <div class="step4-pill ${tokenReady ? 'ok' : 'warn'}">
          ${tokenReady ? 'Token capturado' : 'Falta token'}
        </div>
        <div class="step4-pill ${nameReady ? 'ok' : 'warn'}">
          ${nameReady ? 'Nombre listo' : 'Falta nombre'}
        </div>
        <div class="step4-pill ${checkboxReady ? 'ok' : 'warn'}">
          ${checkboxReady ? 'Aceptación legal lista' : 'Falta aceptación'}
        </div>
        <div class="step4-pill ${previewReady ? 'ok' : 'warn'}">
          ${previewReady ? 'Preview válido' : 'Preview pendiente'}
        </div>
      `;

      if (currentPreview) {
        const p = currentPreview.project || {};
        const e = currentPreview.event || {};
        const t = currentPreview.token || {};

        previewBox.innerHTML = `
          <div class="step4-preview-card">
            <div class="step4-preview-title">Tu inscripción está lista para confirmarse</div>
            <div class="step4-preview-sub">
              Verifica estos datos antes de cerrar el proceso.
            </div>
            <div class="step4-grid">
              <div class="meta-box">
                <span class="meta-label">Proyecto</span>
                <div class="meta-value">${escapeHTML(p.project_name || '—')}</div>
              </div>
              <div class="meta-box">
                <span class="meta-label">Organización</span>
                <div class="meta-value">${escapeHTML(p.general_name || '—')}</div>
              </div>
              <div class="meta-box">
                <span class="meta-label">Temporada</span>
                <div class="meta-value">${escapeHTML(e.display_name || '—')}</div>
              </div>
              <div class="meta-box">
                <span class="meta-label">Token</span>
                <div class="meta-value">${escapeHTML(t.token_value || tokenValue || '—')}</div>
              </div>
            </div>
          </div>
        `;
      } else {
        previewBox.innerHTML = `
          <div class="step4-preview-card">
            <div class="step4-preview-title">Preview pendiente</div>
            <div class="step4-preview-sub">
              Captura tu token, completa el nombre y genera el preview antes de confirmar.
            </div>
          </div>
        `;
      }

      const tokenInputEl = document.getElementById('projectTokenInput');
      const nameInputEl = document.getElementById('acceptanceFullNameInput');
      const legalInputEl = document.getElementById('legalVersionInput');

      if (tokenInputEl) tokenInputEl.disabled = !!currentPreview;
      if (nameInputEl) nameInputEl.disabled = !!currentPreview;
      if (legalInputEl) legalInputEl.disabled = !!currentPreview;

      if (canConfirm) {
        confirmBox.innerHTML = `
          <div class="step4-confirm-box">
            <div class="step4-confirm-ready">Datos congelados para confirmación</div>
            <div class="step4-preview-sub">
              Revisa el resumen. Si todo está bien, confirma tu inscripción. Si no, usa “Modificar datos”.
            </div>
            <div class="actions" style="margin-top:10px;">
              <button type="button" class="btn-secondary" onclick="clearRegistrationPreview()">
                Modificar aquí
              </button>
              <button type="button" class="btn-blue" onclick="goBackToCatalogFromStep4()">
                Volver al catálogo y cambiar proyecto
              </button>
            </div>
          </div>
        `;
      } else {
        confirmBox.innerHTML = `
          <div class="step4-confirm-box">
            <div class="step4-confirm-ready" style="color:#92400e;">Aún no listo para confirmar</div>
            <div class="step4-preview-sub">
              Completa los elementos pendientes y genera el preview válido.
            </div>
          </div>
        `;
      }

      const confirmBtn = document.getElementById('confirmRegistrationBtn');
      if (confirmBtn) {
        confirmBtn.disabled = !canConfirm;
        confirmBtn.textContent = canConfirm ? 'Confirmar inscripción' : 'Completa el preview primero';
      }
    }

    function renderRegistrationSuccess(data) {
      const box = document.getElementById('requestInfo');
      if (!box) return;

      box.innerHTML = `
        <div class="success-shell">
          <div class="success-icon">✓</div>
          <div class="success-title">Inscripción completada</div>
          <div class="success-sub">
            Tu lugar quedó registrado correctamente. Guarda esta información como comprobante de cierre.
          </div>

          <div class="info-card" style="margin-top:18px; text-align:left;">
            <div class="info-head">
              <div>
                <div class="info-title">Comprobante oficial del alumno</div>
                <div class="info-sub">Resumen final de tu inscripción cerrada</div>
              </div>
              <div><span class="chip chip-green">CONFIRMADO</span></div>
            </div>

            <div class="meta-grid">
              <div class="meta-box">
                <span class="meta-label">Proyecto</span>
                <div class="meta-value">${escapeHTML(data?.project_name || '—')}</div>
              </div>

              <div class="meta-box">
                <span class="meta-label">Organización</span>
                <div class="meta-value">${escapeHTML(data?.general_name || '—')}</div>
              </div>

              <div class="meta-box">
                <span class="meta-label">Token usado</span>
                <div class="meta-value">${escapeHTML(data?.token_value || '—')}</div>
              </div>

              <div class="meta-box">
                <span class="meta-label">Temporada</span>
                <div class="meta-value">${escapeHTML(data?.season || getSeason() || '—')}</div>
              </div>

              <div class="meta-box">
                <span class="meta-label">Confirmado</span>
                <div class="meta-value">${escapeHTML(data?.accepted_at || '—')}</div>
              </div>

              <div class="meta-box">
                <span class="meta-label">Estado</span>
                <div class="meta-value">Inscripción cerrada correctamente</div>
              </div>
            </div>
          </div>
        </div>
      `;
    }

    function syncStep4InputsVisualState() {
      const tokenInput = document.getElementById('projectTokenInput');
      const nameInput = document.getElementById('acceptanceFullNameInput');
      const legalInput = document.getElementById('legalVersionInput');
      const checkbox = document.getElementById('acceptanceCheckbox');

      if (tokenInput) {
        tokenInput.classList.remove('input-ok', 'input-err');
        if (tokenInput.value.trim()) tokenInput.classList.add('input-ok');
      }

      if (nameInput) {
        nameInput.classList.remove('input-ok', 'input-err');
        if (nameInput.value.trim()) nameInput.classList.add('input-ok');
      }

      if (legalInput) {
        legalInput.classList.remove('input-ok', 'input-err');
        if (legalInput.value.trim()) legalInput.classList.add('input-ok');
      }

      const checkboxWrap = checkbox?.closest('label');
      if (checkboxWrap) {
        checkboxWrap.style.opacity = checkbox?.checked ? '1' : '.8';
      }
    }

    function escapeHTML(value) {
      return String(value ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    function setJourneyStepState(stepNumber, state, metaText) {
      const step = document.getElementById(`journeyStep${stepNumber}`);
      const meta = document.getElementById(`journeyMeta${stepNumber}`);
      if (!step || !meta) return;

      step.classList.remove('done', 'active', 'locked', 'error');
      if (state) step.classList.add(state);
      meta.textContent = metaText || '';
    }

    function setJourneyProgress(percent) {
      const bar = document.getElementById('journeyProgress');
      if (bar) bar.style.width = `${percent}%`;
    }

    function setJourneyBadge(text, variant = 'neutral') {
      const badge = document.getElementById('journeyBadge');
      if (!badge) return;

      badge.textContent = text || '—';
      badge.style.background = '';
      badge.style.color = '';
      badge.style.borderColor = '';

      if (variant === 'ok') {
        badge.style.background = 'var(--green-soft)';
        badge.style.color = 'var(--green)';
        badge.style.borderColor = '#cdeee4';
      } else if (variant === 'warn') {
        badge.style.background = '#fff7ed';
        badge.style.color = '#c2410c';
        badge.style.borderColor = '#fed7aa';
      } else if (variant === 'err') {
        badge.style.background = 'var(--pink-soft)';
        badge.style.color = 'var(--pink)';
        badge.style.borderColor = '#ffd7df';
      } else if (variant === 'brand') {
        badge.style.background = 'var(--primary-soft)';
        badge.style.color = 'var(--primary)';
        badge.style.borderColor = '#e6dbf3';
      }
    }

    function lockStep4UI(locked = true) {
      const section = document.getElementById('registrationSection');
      const tokenInput = document.getElementById('projectTokenInput');
      const nameInput = document.getElementById('acceptanceFullNameInput');
      const legalInput = document.getElementById('legalVersionInput');
      const checkbox = document.getElementById('acceptanceCheckbox');
      const previewBtn = document.getElementById('previewRegistrationBtn');
      const confirmBtn = document.getElementById('confirmRegistrationBtn');

      if (section) {
        section.style.opacity = locked ? '0.65' : '1';
        section.style.pointerEvents = locked ? 'none' : 'auto';
      }

      if (tokenInput) tokenInput.disabled = locked;
      if (nameInput) nameInput.disabled = locked;
      if (legalInput) legalInput.disabled = locked;
      if (checkbox) checkbox.disabled = locked;
      if (previewBtn) previewBtn.disabled = locked;
      if (confirmBtn) confirmBtn.disabled = locked;

      currentAccessUnlocked = !locked;
    }

    function formatCountdown(totalSeconds) {
      const safe = Math.max(0, totalSeconds);
      const minutes = Math.floor(safe / 60);
      const seconds = safe % 60;
      return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }

    function parseServerDateTime(value) {
      if (!value) return null;
      const dt = new Date(value);
      return Number.isNaN(dt.getTime()) ? null : dt;
    }


    function startJourneyTimer(expiresAt) {
      stopJourneyTimer();

      const box = document.getElementById('journeyTimerBox');
      const val = document.getElementById('journeyTimerValue');
      const sub = document.getElementById('journeyTimerSub');

      if (!box || !val || !expiresAt) return;

      const targetDate = parseServerDateTime(expiresAt);
      if (!targetDate) return;

      box.classList.remove('hidden', 'warn', 'danger', 'expired');

      function tick() {
        const passSession = currentPass?.pass_session || currentPass?.active_session || null;

        if (!passSession) {
          stopJourneyTimer();
          box.classList.add('hidden');
          return;
        }

        const diff = Math.floor((targetDate.getTime() - Date.now()) / 1000);

        if (diff <= 0) {
          val.textContent = 'Expirado';
          if (sub) sub.textContent = 'Tu QR expiró. Debes refrescar tu credencial.';
          box.classList.remove('warn', 'danger');
          box.classList.add('expired');
          stopJourneyTimer();
          return;
        }

        val.textContent = formatCountdown(diff);

        if (sub) {
          sub.textContent = 'Tu QR sigue vigente para mostrarlo al staff.';
        }

        box.classList.remove('warn', 'danger', 'expired');

        if (diff <= 60) {
          box.classList.add('danger');
        } else if (diff <= 180) {
          box.classList.add('warn');
        }
      }

      tick();
      journeyTimerInterval = setInterval(tick, 1000);
    }

    function stopJourneyTimer() {
      if (journeyTimerInterval) {
        clearInterval(journeyTimerInterval);
        journeyTimerInterval = null;
      }
    }

    function computeStudentJourneyState() {
      const requestStatus = currentRequest?.request?.status || currentRequest?.status || null;
      const passSession = currentPass?.pass_session || currentPass?.active_session || null;
      const hasPass = !!passSession;
      const hasPreview = !!currentPreview;
      const isRegistered = !!currentRegistration || requestStatus === 'REGISTERED';

      return {
        requestStatus,
        passSession,
        hasPass,
        hasPreview,
        isRegistered
      };
    }

    function renderJourneyState() {
      const title = document.getElementById('journeyTitle');
      const subtitle = document.getElementById('journeySubtitle');
      const alert = document.getElementById('journeyAlert');
      const timerBox = document.getElementById('journeyTimerBox');

      if (!title || !subtitle || !alert) return;

      const requestStatus = getStudentStatus();
      const passSession = currentPass?.pass_session || currentPass?.active_session || null;
      const hasPass = !!passSession;
      const hasPreview = !!currentPreview;
      const isRegistered = !!currentRegistration || requestStatus === 'REGISTERED';
      const qrFlowCompleted = hasPass || hasJourneyQrEvidence();

      setJourneyStepState(1, 'locked', 'Pendiente');
      setJourneyStepState(2, 'locked', 'Sin pase');
      setJourneyStepState(3, 'locked', 'Pendiente');
      setJourneyStepState(4, 'locked', 'Bloqueada');
      setJourneyProgress(0);
      lockStep4UI(true);

      stopJourneyTimer();
      if (timerBox) timerBox.classList.add('hidden');

      if (passSession?.expires_at) {
        startJourneyTimer(passSession.expires_at);
      }

      if (!requestStatus) {
        title.textContent = 'Esperando solicitud';
        subtitle.textContent = 'Completa tu solicitud para generar folio y comenzar el flujo.';
        setJourneyBadge('INACTIVO', 'neutral');
        alert.className = 'journey-alert';
        alert.textContent = 'Primero crea tu solicitud. Después podrás generar tu QR y continuar.';
        return;
      }

      setJourneyStepState(1, 'done', 'Solicitud creada');

      if (requestStatus === 'REQUESTED') {
        title.textContent = 'Solicitud creada';
        subtitle.textContent = 'Tu folio ya existe. Ahora debes generar tu QR y mostrarlo al staff.';
        setJourneyBadge('REQUESTED', 'warn');
        setJourneyStepState(2, hasPass ? 'active' : 'locked', hasPass ? 'QR vigente' : 'Genera tu pase');
        setJourneyStepState(3, 'locked', 'Esperando staff');
        setJourneyStepState(4, 'locked', 'Bloqueada');
        setJourneyProgress(hasPass ? 38 : 25);
        alert.className = 'journey-alert warn';
        alert.textContent = hasPass
          ? 'Ya tienes un QR activo. Muéstralo al staff para seguir.'
          : 'Genera tu QR. Sin ese paso no puedes avanzar.';
        return;
      }

      if (requestStatus === 'VALIDATED') {
        title.textContent = 'Validado por staff';
        subtitle.textContent = 'Tu identidad fue validada, pero todavía no tienes acceso habilitado para cerrar inscripción.';
        setJourneyBadge('VALIDATED', 'brand');
        setJourneyStepState(2, qrFlowCompleted ? 'done' : 'locked', qrFlowCompleted ? 'QR completado' : 'Sin pase');
        setJourneyStepState(3, 'active', 'Validado');
        setJourneyStepState(4, 'locked', 'Aún sin acceso');
        setJourneyProgress(60);
        alert.className = 'journey-alert warn';
        alert.textContent = 'Aún no puedes usar el paso 4. Necesitas que el flujo quede en ACCESS_ENABLED.';
        return;
      }

      if (requestStatus === 'ACCESS_ENABLED') {
        title.textContent = 'Acceso habilitado';
        subtitle.textContent = 'El staff ya cerró la validación. Ahora solo falta capturar tu token, revisar el preview y confirmar.';
        setJourneyBadge('ACCESS ENABLED', 'ok');
        setJourneyStepState(2, qrFlowCompleted ? 'done' : 'locked', qrFlowCompleted ? 'QR completado' : 'Sin pase');
        setJourneyStepState(3, 'done', 'Validación terminada');
        setJourneyStepState(4, 'active', hasPreview ? 'Preview listo' : 'Listo para cierre');
        setJourneyProgress(hasPreview ? 92 : 82);
        lockStep4UI(false);
        alert.className = 'journey-alert ok';
        alert.textContent = hasPreview
          ? 'Tu preview es válido. Ya puedes confirmar tu inscripción.'
          : 'Tu camino ya está abierto. Captura el token del proyecto y genera el preview.';
        return;
      }

      if (requestStatus === 'REGISTERED' || isRegistered) {
        title.textContent = 'Inscripción completada';
        subtitle.textContent = 'Tu lugar quedó registrado correctamente.';
        setJourneyBadge('REGISTERED', 'ok');
        setJourneyStepState(2, 'done', 'QR completado');
        setJourneyStepState(3, 'done', 'Validación correcta');
        setJourneyStepState(4, 'done', 'Inscripción cerrada');
        setJourneyProgress(100);
        lockStep4UI(true);
        alert.className = 'journey-alert ok';
        alert.textContent = 'Proceso finalizado. Ya estás inscrito.';
        return;
      }

      if (requestStatus === 'CANCELLED' || requestStatus === 'CLOSED') {
        title.textContent = 'Proceso detenido';
        subtitle.textContent = 'Tu solicitud necesita revisión con staff o administración.';
        setJourneyBadge(requestStatus, 'err');
        setJourneyStepState(2, 'error', 'Revisión requerida');
        setJourneyStepState(3, 'error', 'Proceso detenido');
        setJourneyStepState(4, 'locked', 'No disponible');
        setJourneyProgress(25);
        alert.className = 'journey-alert err';
        alert.textContent = 'Tu solicitud fue cerrada o cancelada. Debes acudir con administración.';
        return;
      }

      title.textContent = `Estado actual: ${requestStatus}`;
      subtitle.textContent = 'Tu proceso tiene un estado no contemplado explícitamente.';
      setJourneyBadge(requestStatus, 'neutral');
      alert.className = 'journey-alert';
      alert.textContent = 'Revisa tu situación con staff si el proceso no avanza.';
    }

    function getSeason() {
      const el = document.getElementById('seasonSelector');
      return el ? el.value : 'PRIMAVERA';
    }

    function showMsg(text, ok = true) {
      const el = document.getElementById('msg');
      if (!el) return;

      el.textContent = text || '';
      el.className = 'msg ' + (ok ? 'ok' : 'err');
    }

    function getEnrolment() {
      return normalizeEnrolmentInput();
    }

    function getEffectiveEnrolment() {
      const inputValue = (getEnrolment() || '').trim().toLowerCase();
      if (inputValue) return inputValue;

      const requestEnrolment =
        (currentRequest?.student?.enrolment_number || '').trim().toLowerCase() ||
        (currentRequest?.user?.enrolment_number || '').trim().toLowerCase();

      if (requestEnrolment) return requestEnrolment;

      try {
        const saved = (localStorage.getItem('student_enrolment') || '').trim().toLowerCase();
        if (saved) return saved;
      } catch {}

      return '';
    }

    function saveStudentEnrolment(enrolment) {
      try {
        const clean = String(enrolment || '').trim().toLowerCase();
        if (!clean) {
          localStorage.removeItem('student_enrolment');
          return;
        }
        localStorage.setItem('student_enrolment', clean);
      } catch {}
    }

    function saveSelectedProject(project) {
      try {
        if (!project) {
          localStorage.removeItem('selected_project');
          return;
        }
        localStorage.setItem('selected_project', JSON.stringify(project));
      } catch {}
    }

    function loadSavedSelectedProject() {
      try {
        const raw = localStorage.getItem('selected_project');
        return raw ? JSON.parse(raw) : null;
      } catch {
        return null;
      }
    }

    function clearSavedSelectedProject() {
      try {
        localStorage.removeItem('selected_project');
      } catch {}
    }

    function loadSavedStudentEnrolment() {
      try {
        return localStorage.getItem('student_enrolment') || '';
      } catch {
        return '';
      }
    }

    function setCurrentPlainQrToken(token) {
      currentPlainQrToken = token || '';
      try {
        if (token) {
          sessionStorage.setItem('student_plain_qr_token', token);
        } else {
          sessionStorage.removeItem('student_plain_qr_token');
        }
      } catch {}
    }

    function getCurrentPlainQrToken() {
      if (currentPlainQrToken) return currentPlainQrToken;
      try {
        return sessionStorage.getItem('student_plain_qr_token') || '';
      } catch {
        return '';
      }
    }

    function clearCurrentPlainQrToken() {
      currentPlainQrToken = '';
      try {
        sessionStorage.removeItem('student_plain_qr_token');
      } catch {}
    }

    function normalizeEnrolmentInput() {
      const input = document.getElementById('enrolmentInput');
      if (!input) return '';

      const cleaned = String(input.value || '')
        .replace(/\s+/g, '')
        .toUpperCase()
        .slice(0, 9);

      input.value = cleaned;
      return cleaned.toLowerCase();
    }

    function normalizeStudentNameInput() {
      const input = document.getElementById('fullNameInput');
      if (!input) return;
      input.value = input.value.replace(/\s+/g, ' ').slice(0, 100);
    }

    function normalizePhoneInput() {
      const input = document.getElementById('phoneInput');
      if (!input) return;
      input.value = input.value.replace(/\D/g, '').slice(0, 10);
    }

    function normalizeSemesterInput() {
      const input = document.getElementById('semesterInput');
      if (!input) return;

      input.value = input.value.replace(/\D/g, '').slice(0, 2);

      const n = Number(input.value);
      if (input.value && n > 20) {
        input.value = '20';
      }
    }

    function normalizeProjectTokenInput() {
      const input = document.getElementById('projectTokenInput');
      if (!input) return;
      input.value = input.value.replace(/\s+/g, '').toUpperCase().slice(0, 12);
    }

    function normalizeSecondaryEmailInput() {
      const input = document.getElementById('secondaryEmailInput');
      if (!input) return;
      input.value = input.value.trim().toLowerCase().slice(0, 120);
    }

    function getInstitutionalEmailFromEnrolment(enrolment) {
      const clean = String(enrolment || '').trim().toLowerCase();
      return clean ? `${clean}@tec.mx` : '';
    }

    function renderGeneratedInstitutionalEmail() {
      const box = document.getElementById('generatedInstitutionalEmail');
      if (!box) return;

      const enrolment = getEnrolment();
      const email = getInstitutionalEmailFromEnrolment(enrolment);
      box.textContent = email || 'Se generará con tu matrícula';
    }

    function isValidPhone(phone) {
      return /^\d{10}$/.test(String(phone || '').trim());
    }

    function isValidSecondaryEmail(email) {
      if (!email) return true;
      return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(email).trim().toLowerCase());
    }

    function validateEnrolmentStrict(showError = true) {
      const enrolment = normalizeEnrolmentInput();

      if (enrolment.length !== 9) {
        if (showError) {
          showMsg('La matrícula debe tener exactamente 9 caracteres.', false);
        }
        return null;
      }

      return enrolment;
    }

    function getRecoverEnrolment() {
      const input = document.getElementById('recoverEnrolmentInput');
      if (!input) return '';

      const cleaned = String(input.value || '')
        .replace(/\s+/g, '')
        .toUpperCase()
        .slice(0, 9);

      input.value = cleaned;
      return cleaned.toLowerCase();
    }

    function showStudentSection(sectionId) {
      document.querySelectorAll('.section').forEach(el => el.classList.remove('active'));
      document.getElementById(sectionId)?.classList.add('active');
    }

    function setCurrentStep(step) {
      const status = getStudentStatus();
      const step4Unlocked = status === 'ACCESS_ENABLED' || status === 'REGISTERED' || !!currentRegistration;

      document.querySelectorAll('.nav-card').forEach(el => {
        const n = Number(el.getAttribute('data-step'));

        el.classList.remove('active', 'done', 'locked', 'unlocked');

        if (n < step) {
          el.classList.add('done');
        } else if (n === step) {
          el.classList.add('active');
        }

        if (n === 4) {
          if (step4Unlocked) {
            el.classList.add('unlocked');
          } else {
            el.classList.add('locked');
          }
        }
      });
    }

    function goToSectionAndStep(sectionId, step) {
      showStudentSection(sectionId);
      setCurrentStep(step);
    }

    async function validateAccessAndGoStep4() {
      try {
        const enrolment = getEffectiveEnrolment();

        if (!enrolment) {
          showMsg('Primero recupera tu proceso o escribe tu matrícula.', false);
          return;
        }

        if (!/^[a-zA-Z0-9]{9}$/.test(enrolment)) {
          showMsg('La matrícula debe tener exactamente 9 caracteres.', false);
          return;
        }

        await loadStudentRequest().catch(() => {});
        await loadStudentPass().catch(() => {});

        const status =
          currentRequest?.request?.status ||
          currentRequest?.status ||
          currentRequestStatus ||
          null;

        if (status !== 'ACCESS_ENABLED' && !currentRegistration) {
          showMsg('Aún no tienes acceso habilitado. Primero muestra tu QR al staff.', false);
          return;
        }

        showStudentSection('registrationSection');
        setCurrentStep(4);
        showMsg('Ya puedes pasar al cierre de inscripción.');
      } catch (e) {
        console.error(e);
        showMsg(humanizeErrorMessage(e), false);
      }
    }

    async function validateAccessAndShowRegistration() {
      try {
        const enrolment = getEffectiveEnrolment();

        if (!enrolment) {
          showMsg('Primero recupera tu proceso o escribe tu matrícula.', false);
          return;
        }

        if (!/^[a-zA-Z0-9]{9}$/.test(enrolment)) {
          showMsg('La matrícula debe tener exactamente 9 caracteres.', false);
          return;
        }

        await loadStudentRequest().catch(() => {});
        await loadStudentPass().catch(() => {});

        const status =
          currentRequest?.request?.status ||
          currentRequest?.status ||
          currentRequestStatus ||
          null;

        if (status !== 'ACCESS_ENABLED' && !currentRegistration) {
          showMsg('El paso 4 sigue bloqueado. Primero muestra tu QR al staff.', false);
          return;
        }

        showStudentSection('registrationSection');
        setCurrentStep(4);
        showMsg('Ya puedes continuar con tu inscripción.');
      } catch (e) {
        console.error(e);
        showMsg(humanizeErrorMessage(e), false);
      }
    }
    
    function stopStudentAutoSync() {
      if (studentAutoSyncInterval) {
        clearInterval(studentAutoSyncInterval);
        studentAutoSyncInterval = null;
      }
    }

    function startStudentAutoSync() {
      stopStudentAutoSync();

      studentAutoSyncInterval = setInterval(async () => {
        try {
          const status =
            currentRequest?.request?.status ||
            currentRequest?.status ||
            currentRequestStatus ||
            null;

          if (!status) return;

          if (status === 'ACCESS_ENABLED' || status === 'REGISTERED' || status === 'CANCELLED' || status === 'CLOSED') {
            stopStudentAutoSync();
            return;
          }

          await loadStudentRequest().catch(() => {});

          const statusAfterRequest = getStudentStatus();
          if (statusAfterRequest === 'REQUESTED' || statusAfterRequest === 'VALIDATED') {
            await loadStudentPass().catch(() => {});
          }
        } catch (e) {
          console.error('AutoSync error:', e);
        }
      }, 8000);
    }

    function showSmartToast(title, text) {
      const toast = document.getElementById('smartToast');
      if (!toast) return;

      const titleEl = toast.querySelector('.smart-toast__title');
      const textEl = toast.querySelector('.smart-toast__text');

      if (titleEl) titleEl.textContent = title || 'Aviso';
      if (textEl) textEl.textContent = text || '';

      toast.classList.remove('hidden');
      requestAnimationFrame(() => toast.classList.add('show'));

      setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.classList.add('hidden'), 280);
      }, 3000);
    }

    async function getJSON(url) {
      const r = await fetch(url);
      const data = await r.json().catch(() => ({}));

      if (!r.ok) {
        throw {
          error: data.error || data.message || ('Error ' + r.status),
          status: r.status
        };
      }

      return data;
    }

    async function postJSON(url, body) {
      const r = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });

      const data = await r.json().catch(() => ({}));

      if (!r.ok) {
        throw {
          error: data.error || data.message || ('Error ' + r.status),
          status: r.status
        };
      }

      return data;
    }

    async function tryGet(urls) {
      let lastError = null;

      for (const url of urls) {
        try {
          return await getJSON(url);
        } catch (e) {
          console.error('Falló GET:', url, e);
          lastError = e;
        }
      }

      throw lastError || new Error('No se pudo completar la consulta');
    }

    async function tryPost(candidates) {
      let lastError = null;

      for (const item of candidates) {
        try {
          return await postJSON(item.url, item.body);
        } catch (e) {
          console.error('Falló POST:', item.url, e);
          lastError = e;
        }
      }

      throw lastError || new Error('No se pudo completar la operación');
    }

    function updateHeroState() {
      const routeStatus = document.getElementById('heroRouteStatus');
      const projectStatus = document.getElementById('heroProjectStatus');
      const sideRouteStatus = document.getElementById('sideRouteStatus');
      const sideProjectStatus = document.getElementById('sideProjectStatus');

      const heroKicker = document.querySelector('.hero-kicker');
      const heroTitle = document.querySelector('.hero h1');
      const heroText = document.querySelector('.hero p');

      const status =
        currentRequest?.request?.status ||
        currentRequest?.status ||
        currentRequestStatus ||
        null;

      const selectedProjectText = currentSelectedProject
        ? `${currentSelectedProject.general_name || 'Proyecto'} | ${currentSelectedProject.name || currentSelectedProject.project_name || 'Sin nombre'}`
        : 'Sin proyecto seleccionado';

      let routeText = 'Explorando catálogo';
      let kicker = 'Ruta del alumno';
      let title = 'Explora primero. Decide bien. Regístrate solo cuando ya tengas acceso.';
      let text = 'Puedes revisar el catálogo antes de solicitar tu pase. Cuando el staff te habilite acceso, podrás cerrar tu inscripción con el token del proyecto.';

      if (status === 'REQUESTED') {
        routeText = 'Solicitud creada';
        kicker = 'Solicitud lista';
        title = 'Tu folio ya existe. Ahora toca generar y mostrar tu QR.';
        text = 'Ya diste el primer paso. El siguiente movimiento es usar tu credencial viva para que staff valide tu proceso presencialmente.';
      } else if (status === 'VALIDATED') {
        routeText = 'Validado por staff';
        kicker = 'Validación completada';
        title = 'Tu identidad ya fue validada. Falta habilitar el acceso final.';
        text = 'Ya pasaste la validación presencial. Solo falta que el flujo quede habilitado para cerrar tu inscripción.';
      } else if (status === 'ACCESS_ENABLED') {
        routeText = 'Acceso habilitado';
        kicker = 'Cierre disponible';
        title = 'Ya puedes cerrar tu inscripción.';
        text = 'Captura el token del proyecto, revisa el preview y confirma. Estás a un paso del cierre oficial.';
      } else if (status === 'REGISTERED') {
        routeText = 'Inscripción completada';
        kicker = 'Proceso finalizado';
        title = 'Tu inscripción ya fue completada correctamente.';
        text = 'Tu lugar quedó registrado. Ya no necesitas generar otro QR ni volver a capturar tu solicitud para esta temporada.';
      } else if (status === 'CANCELLED' || status === 'CLOSED') {
        routeText = 'Proceso detenido';
        kicker = 'Revisión necesaria';
        title = 'Tu proceso necesita atención de staff o administración.';
        text = 'Tu solicitud está cerrada o detenida. Si necesitas continuar, acércate con el equipo de apoyo.';
      }

      if (routeStatus) routeStatus.textContent = routeText;
      if (projectStatus) projectStatus.textContent = selectedProjectText;
      if (sideRouteStatus) sideRouteStatus.textContent = routeText;
      if (sideProjectStatus) sideProjectStatus.textContent = selectedProjectText;

      if (heroKicker) heroKicker.textContent = kicker;
      if (heroTitle) heroTitle.textContent = title;
      if (heroText) heroText.textContent = text;
    }

    function renderEmptyState(title, subtitle) {
      return `
        <div class="empty-state">
          <div class="empty-title">${escapeHTML(title)}</div>
          <div>${escapeHTML(subtitle || '')}</div>
        </div>
      `;
    }

    function resetCatalogFilters() {
      const search = document.getElementById('catalogSearch');
      const partner = document.getElementById('filterPartner');
      const modality = document.getElementById('filterModality');
      const weekDays = document.getElementById('filterWeekDays');
      const schedule = document.getElementById('filterSchedule');

      if (search) search.value = '';
      if (partner) partner.value = '';
      if (modality) modality.value = '';
      if (weekDays) weekDays.value = '';
      if (schedule) schedule.value = '';

      loadCatalog();
      showMsg('Filtros limpiados. Ya puedes explorar el catálogo completo.');
    }

    function renderSelectedProjectBanner() {
      const box = document.getElementById('selectedProjectBanner');
      if (!box) return;

      if (!currentSelectedProject) {
        box.innerHTML = `
          <div class="selected-banner-title">Aún no has elegido proyecto</div>
          <div class="selected-banner-text">
            Explora las opciones del catálogo, compara y selecciona un proyecto para continuar con tu solicitud.
          </div>
        `;
        return;
      }

      const p = currentSelectedProject;
      const generalName = p.general_name || p.organization || 'Sin nombre general';
      const projectName = p.name || p.project_name || 'Sin nombre';
      const partner = p.partner_name || p.socio || 'Sin organización';
      const modality = p.modalidad || p.modality_name || '—';
      const schedule = p.horario || p.schedule_name || '—';
      const day = p.dia || p.week_days_name || '—';
      const available = p.cupos_disponibles ?? '—';

      box.innerHTML = `
        <div class="selected-banner-title">Proyecto listo para continuar</div>
        <div class="selected-banner-text" style="margin-bottom:10px;">
          Ya elegiste un proyecto. Si todo se ve bien, continúa con tu solicitud o cambia de opción cuando quieras.
        </div>

        <div class="meta-grid">
          <div class="meta-box">
            <span class="meta-label">Proyecto</span>
            <div class="meta-value">${escapeHTML(generalName)} | ${escapeHTML(projectName)}</div>
          </div>

          <div class="meta-box">
            <span class="meta-label">Organización</span>
            <div class="meta-value">${escapeHTML(partner)}</div>
          </div>

          <div class="meta-box">
            <span class="meta-label">Modalidad</span>
            <div class="meta-value">${escapeHTML(modality)}</div>
          </div>

          <div class="meta-box">
            <span class="meta-label">Día</span>
            <div class="meta-value">${escapeHTML(day)}</div>
          </div>

          <div class="meta-box">
            <span class="meta-label">Horario</span>
            <div class="meta-value">${escapeHTML(schedule)}</div>
          </div>

          <div class="meta-box">
            <span class="meta-label">Cupos disponibles</span>
            <div class="meta-value">${escapeHTML(String(available))}</div>
          </div>
        </div>

        <div class="actions" style="margin-top:12px;">
          <button type="button" class="btn-blue" onclick="goToSectionAndStep('requestSection', 2)">
            Continuar con este proyecto
          </button>
          <button type="button" class="btn-secondary" onclick="showStudentSection('catalogSection')">
            Seguir explorando
          </button>
        </div>
      `;
    }

    function renderCatalogHeader(projects, eventInfo = null) {
      const season = eventInfo?.season || getSeason();
      const displayName = eventInfo?.display_name || season;
      const countLabel = document.getElementById('catalogCountLabel');
      const seasonChip = document.getElementById('catalogSeasonChip');
      const projectsChip = document.getElementById('catalogProjectsChip');

      if (countLabel) countLabel.textContent = `Catálogo de ${displayName}`;
      if (seasonChip) seasonChip.textContent = season;
      if (projectsChip) projectsChip.textContent = `${projects.length} proyectos`;
    }

    function renderCatalog(projects) {
      const grid = document.getElementById('catalogList');
      if (!grid) return;

      if (!projects || !projects.length) {
        grid.innerHTML = renderEmptyState(
          'No encontramos proyectos con esos filtros',
          'Prueba limpiando filtros o cambiando tu búsqueda.'
        );
        return;
      }

      const selectedId = Number(currentSelectedProject?.id ?? currentSelectedProject?.project_id ?? 0);

      grid.innerHTML = projects.map((p) => {
        const projectId = Number(p.id ?? p.project_id ?? 0);
        const eventProjectId = p.event_project_id ?? '—';
        const generalName = p.general_name || 'Sin nombre general';
        const projectName = p.name || p.project_name || 'Sin nombre';
        const partner = p.partner_name || p.socio || 'Sin organización';
        const modality = p.modalidad || p.modality_name || '—';
        const day = p.dia || p.week_days_name || '—';
        const schedule = p.horario || p.schedule_name || '—';
        const location = p.location || 'Sin ubicación';
        const available = p.cupos_disponibles ?? '—';
        const selected = selectedId === projectId;

        return `
          <article class="project-card ${selected ? 'selected' : ''}">
            <div class="project-card-top">
              <div>
                <div class="project-card-title">${escapeHTML(generalName)}</div>
                <div class="project-card-subtitle">${escapeHTML(projectName)}</div>
              </div>
              <div>
                <span class="chip ${selected ? 'chip-blue' : 'chip-neutral'}">
                  ${selected ? 'SELECCIONADO' : 'DISPONIBLE'}
                </span>
              </div>
            </div>

            <div class="project-card-meta">
              <span class="chip chip-neutral">${escapeHTML(partner)}</span>
              <span class="chip chip-neutral">${escapeHTML(modality)}</span>
              <span class="chip chip-neutral">${escapeHTML(day)}</span>
              <span class="chip chip-neutral">${escapeHTML(schedule)}</span>
            </div>

            <div class="project-card-body">
              <div class="meta-grid">
                <div class="meta-box">
                  <span class="meta-label">Ubicación</span>
                  <div class="meta-value">${escapeHTML(location)}</div>
                </div>
                <div class="meta-box">
                  <span class="meta-label">Cupos disponibles</span>
                  <div class="meta-value">${escapeHTML(String(available))}</div>
                </div>
                <div class="meta-box">
                  <span class="meta-label">ID de proyecto</span>
                  <div class="meta-value">${escapeHTML(String(projectId))}</div>
                </div>
                <div class="meta-box">
                  <span class="meta-label">ID en temporada</span>
                  <div class="meta-value">${escapeHTML(String(eventProjectId))}</div>
                </div>
              </div>
            </div>

            <div class="actions" style="margin-top:12px;">
              <button type="button" class="btn-secondary" onclick="selectProject(${projectId})">
                ${selected ? 'Proyecto elegido' : 'Elegir proyecto'}
              </button>
              <button type="button" class="btn-blue" onclick="selectProjectAndContinue(${projectId})">
                Elegir y continuar
              </button>
            </div>
          </article>
        `;
      }).join('');
    }

    function selectProject(projectId) {
      const project = currentCatalog.find(p => Number(p.id ?? p.project_id) === Number(projectId));
      if (!project) return;

      currentSelectedProject = project;
      saveSelectedProject(project);

      const selectedProjectId = document.getElementById('selectedProjectId');
      const selectedProjectName = document.getElementById('selectedProjectName');
      const acceptanceFullNameInput = document.getElementById('acceptanceFullNameInput');

      if (selectedProjectId) {
        selectedProjectId.value = String(project.id ?? project.project_id ?? '');
      }

      if (selectedProjectName) {
        selectedProjectName.value =
          `${project.general_name ?? project.organization ?? 'Sin nombre general'} | ${project.name ?? project.project_name ?? 'Sin nombre'}`;
      }

      if (acceptanceFullNameInput && !acceptanceFullNameInput.value.trim()) {
        const fullName = currentRequest?.student?.full_name || currentRequest?.user?.full_name || '';
        if (fullName) acceptanceFullNameInput.value = fullName;
      }

      renderCatalog(currentCatalog);
      renderSelectedProjectBanner();
      syncStep4InputsVisualState();
      renderStep4PremiumState();
      updateHeroState();

      showMsg('Proyecto seleccionado para el cierre de inscripción');
    }

    function selectProjectAndContinue(projectId) {
      selectProject(projectId);
      goToSectionAndStep('requestSection', 2);
      showMsg('Proyecto elegido. Ahora continúa con tu solicitud.');
    }

    function fillSelect(id, items, placeholderText = 'Selecciona', labelFn = null, valueFn = null) {
      const el = document.getElementById(id);
      if (!el) return;

      el.innerHTML = `<option value="">${placeholderText}</option>`;

      for (const item of items || []) {
        const opt = document.createElement('option');
        opt.value = valueFn
          ? valueFn(item)
          : (item.id ?? item.value ?? item.name ?? item.description ?? '');

        opt.textContent = labelFn
          ? labelFn(item)
          : (item.name || item.description || item.display_name || item.id || 'Opción');

        el.appendChild(opt);
      }
    }

    async function loadCatalogsForSeason() {
      try {
        const season = getSeason();
        const data = await getJSON(`/api/catalogs?season=${encodeURIComponent(season)}`);

        fillSelect('filterPartner', data.socio || [], 'Todas las carreras', item => item.name, item => item.id);
        fillSelect('degreeInput', data.careers || [], 'Selecciona tu carrera', item => item.name, item => item.name);
        fillSelect('filterModality', data.modalidad || [], 'Todas las modalidades', item => item.description || item.name, item => item.id);
        fillSelect('filterWeekDays', data.dias || [], 'Todos los días', item => item.description || item.name, item => item.id);
        fillSelect('filterSchedule', data.horario || [], 'Todos los horarios', item => item.description || item.name, item => item.id);
      } catch (e) {
        console.error('loadCatalogsForSeason error:', e);
        showMsg(humanizeErrorMessage(e), false);
      }
    }

    async function loadCatalog() {
      try {
        const season = getSeason();

        const partner = document.getElementById('filterPartner')?.value || '';
        const modality = document.getElementById('filterModality')?.value || '';
        const day = document.getElementById('filterWeekDays')?.value || '';
        const schedule = document.getElementById('filterSchedule')?.value || '';
        const q = document.getElementById('catalogSearch')?.value?.trim() || '';

        const params = new URLSearchParams();
        params.set('season', season);

        if (q) params.set('q', q);
        if (partner) params.set('socio', partner);
        if (modality) params.set('modalidad', modality);
        if (day) params.set('dia', day);
        if (schedule) params.set('horario', schedule);

        const data = await getJSON(`/api/projects?${params.toString()}`);

        currentCatalog = data.items || [];
        currentCatalogEvent = data.event || null;

        renderCatalogHeader(currentCatalog, currentCatalogEvent);
        renderCatalog(currentCatalog);
      } catch (e) {
        console.error('loadCatalog error:', e);
        showMsg(humanizeErrorMessage(e), false);

        const savedProject = loadSavedSelectedProject();

        if (savedProject && Array.isArray(currentCatalog) && currentCatalog.length) {
          const match = currentCatalog.find(
            p => Number(p.id ?? p.project_id) === Number(savedProject.id ?? savedProject.project_id)
          );

          if (match) {
            currentSelectedProject = match;

            document.getElementById('selectedProjectId').value =
              String(match.id ?? match.project_id ?? '');

            document.getElementById('selectedProjectName').value =
              `${match.general_name ?? match.organization ?? 'Sin nombre general'} | ${match.name ?? match.project_name ?? 'Sin nombre'}`;

            renderSelectedProjectBanner();
            renderCatalog(currentCatalog);
            updateHeroState();
          }
        }

        const list = document.getElementById('catalogList');
        if (list) {
          list.innerHTML = renderEmptyState(
            'No se pudo cargar el catálogo',
            'Revisa la temporada, filtros o conexión.'
          );
        }
      }
    }

    function scheduleCatalogSearch() {
      clearTimeout(catalogSearchTimer);
      catalogSearchTimer = setTimeout(() => {
        loadCatalog();
      }, 280);
    }

    function renderRequestStatus(status) {
      const value = String(status || '').toUpperCase();
      const map = {
        REQUESTED: ['chip chip-blue', 'REQUESTED'],
        VALIDATED: ['chip chip-primary', 'VALIDATED'],
        ACCESS_ENABLED: ['chip chip-green', 'ACCESS_ENABLED'],
        REGISTERED: ['chip chip-green', 'REGISTERED'],
        CANCELLED: ['chip chip-pink', 'CANCELLED'],
        CLOSED: ['chip chip-orange', 'CLOSED']
      };
      const cfg = map[value] || ['chip chip-neutral', value || '—'];
      return `<span class="${cfg[0]}">${cfg[1]}</span>`;
    }

    function renderRequestInfo(data) {
      const box = document.getElementById('requestInfo');
      if (!box) return;

      if (!data) {
        box.innerHTML = renderEmptyState(
          'Todavía no hay información de solicitud',
          'Primero captura tus datos y genera tu folio.'
        );
        updateHeroState();
        return;
      }

      const request = data.request || data;
      const event = data.event || {};
      const user = data.user || {
        email: data.email,
        secondary_email: data.secondary_email,
        phone_number: data.phone_number,
        enrolment_number: data.enrolment_number,
        degree: data.degree,
        semester: data.semester
      };

      box.innerHTML = `
        <div class="info-card">
          <div class="info-head">
            <div>
              <div class="info-title">Folio ${escapeHTML(request.folio || '—')}</div>
              <div class="info-sub">Estado actual de tu solicitud</div>
            </div>
            <div>${renderRequestStatus(request.status)}</div>
          </div>

          <div class="meta-grid">
            <div class="meta-box">
              <span class="meta-label">Temporada</span>
              <div class="meta-value">${escapeHTML(event.display_name || getSeason())}</div>
            </div>
            <div class="meta-box">
              <span class="meta-label">Correo principal</span>
              <div class="meta-value">${escapeHTML(user.email || '—')}</div>
            </div>
            <div class="meta-box">
              <span class="meta-label">Segundo correo</span>
              <div class="meta-value">${escapeHTML(user.second_email || user.secondary_email || '—')}</div>
            </div>
            <div class="meta-box">
              <span class="meta-label">Matrícula</span>
              <div class="meta-value">${escapeHTML(user.enrolment_number || getEnrolment() || '—')}</div>
            </div>
            <div class="meta-box">
              <span class="meta-label">Carrera</span>
              <div class="meta-value">${escapeHTML(user.degree || '—')}</div>
            </div>
            <div class="meta-box">
              <span class="meta-label">Semestre</span>
              <div class="meta-value">${escapeHTML(user.semester || '—')}</div>
            </div>
          </div>
        </div>
      `;
      updateHeroState();
      syncRegistrationLock();
      updateResumeFlowBanner();
    }

    function hydrateStudentFormFromRequest(data) {
      if (!data) return;

      const user = data.user || data || {};

      const fullNameInput = document.getElementById('fullNameInput');
      const phoneInput = document.getElementById('phoneInput');
      const secondaryEmailInput = document.getElementById('secondaryEmailInput');
      const degreeInput = document.getElementById('degreeInput');
      const semesterInput = document.getElementById('semesterInput');


      if (fullNameInput && user.full_name) {
        fullNameInput.value = String(user.full_name).trim().slice(0, 100);
      }

      if (phoneInput && user.phone_number) {
        phoneInput.value = String(user.phone_number).replace(/\D/g, '').slice(0, 10);
      }

      if (secondaryEmailInput) {
        secondaryEmailInput.value = String(
          user.secondary_email || user.second_email || ''
        ).trim().toLowerCase().slice(0, 120);
      }

      if (degreeInput && user.degree) {
        degreeInput.value = String(user.degree).trim();
      }

      if (semesterInput && user.semester != null) {
        semesterInput.value = String(user.semester).trim();
      }

      normalizeStudentNameInput();
      normalizePhoneInput();
      normalizeSecondaryEmailInput();
      normalizeSemesterInput();
      renderGeneratedInstitutionalEmail();
    }

    function updateResumeFlowBanner() {
      const banner = document.getElementById('resumeFlowBanner');
      const text = document.getElementById('resumeFlowText');
      const recoverInput = document.getElementById('recoverEnrolmentInput');

      if (!banner || !text) return;

      const savedEnrolment = getEffectiveEnrolment();
      const status = getStudentStatus();

      if (recoverInput && savedEnrolment && !recoverInput.value.trim()) {
        recoverInput.value = savedEnrolment.toUpperCase();
      }

      if (!savedEnrolment) {
        text.textContent = 'Escribe tu matrícula y recupera tu avance sin volver a capturar todo.';
        return;
      }

      if (status === 'REGISTERED') {
        text.textContent = 'Ya detectamos una matrícula con inscripción completada. Puedes recuperar el comprobante final.';
        return;
      }

      if (status === 'ACCESS_ENABLED') {
        text.textContent = 'Ya detectamos una matrícula con acceso habilitado. Puedes continuar directo al cierre de inscripción.';
        return;
      }

      if (status === 'VALIDATED' || status === 'REQUESTED') {
        text.textContent = 'Ya detectamos una matrícula con solicitud activa. Puedes continuar mostrando tu QR al staff.';
        return;
      }

      if (status) {
        text.textContent = 'Ya detectamos una matrícula con avance guardado. Puedes continuar donde te quedaste.';
        return;
      }

      text.textContent = 'Escribe tu matrícula y recupera tu avance sin volver a capturar todo.';
    }

    async function recoverStudentProcess() {
      try {
        const enrolment = getRecoverEnrolment();
        if (!/^[a-zA-Z0-9]{9}$/.test(enrolment)) {
          return showMsg('La matrícula para recuperar debe tener exactamente 9 caracteres.', false);
        }

        const mainInput = document.getElementById('enrolmentInput');
        if (mainInput) {
          mainInput.value = enrolment.toUpperCase();
        }

        renderGeneratedInstitutionalEmail();
        updateResumeFlowBanner();

        await loadStudentRequest();
        const status = getStudentStatus();

        if (status === 'REQUESTED' || status === 'VALIDATED') {
          await loadStudentPass().catch(() => {});
        }

        if (status === 'REGISTERED') {
          showStudentSection('statusSection');
          setCurrentStep(5);
          showMsg('Proceso recuperado. Ya cuentas con una inscripción completada.');
          return;
        }

        if (status === 'ACCESS_ENABLED') {
          showStudentSection('registrationSection');
          setCurrentStep(4);
          showMsg('Proceso recuperado. Ya puedes continuar con tu inscripción.');
          return;
        }

        if (status === 'VALIDATED' || status === 'REQUESTED') {
          showStudentSection('passSection');
          setCurrentStep(3);
          showMsg('Proceso recuperado. Continúa mostrando tu QR al staff.');
          return;
        }

        showStudentSection('requestSection');
        setCurrentStep(2);
        showMsg('Proceso recuperado correctamente. Revisa tus datos y continúa.');
      } catch (e) {
        console.error(e);
        showMsg(humanizeErrorMessage(e), false);
      }
    }

    function continueStudentFlowFromStatus() {
      const status = getStudentStatus();

      if (status === 'REGISTERED') {
        showStudentSection('statusSection');
        setCurrentStep(5);
        showMsg('Tu inscripción ya fue completada. Aquí puedes consultar tu comprobante y estado final.');
        return;
      }

      if (status === 'ACCESS_ENABLED') {
        showStudentSection('registrationSection');
        setCurrentStep(4);
        showMsg('Tu acceso ya fue habilitado. Solo falta revisar el preview y confirmar.');
        return;
      }

      if (status === 'VALIDATED' || status === 'REQUESTED') {
        showStudentSection('passSection');
        setCurrentStep(3);
        showMsg('Tu siguiente paso es mostrar tu QR al staff para continuar.');
        return;
      }

      if (status) {
        showStudentSection('requestSection');
        setCurrentStep(2);
        showMsg('Tu solicitud ya existe. Revisa tu información y continúa con el siguiente paso.');
        return;
      }

      showStudentSection('catalogSection');
      setCurrentStep(1);
      showMsg('Empieza explorando el catálogo y elige un proyecto con intención.');
    }

    async function createStudentRequest() {
      try {
        const enrolment = getEnrolment();
        const fullName = (document.getElementById('fullNameInput')?.value || '').trim();
        const phone = (document.getElementById('phoneInput')?.value || '').trim();
        const secondaryEmail = (document.getElementById('secondaryEmailInput')?.value || '').trim().toLowerCase();
        const institutionalEmail = getInstitutionalEmailFromEnrolment(enrolment);
        const degree = (document.getElementById('degreeInput')?.value || '').trim();
        const semesterRaw = (document.getElementById('semesterInput')?.value || '').trim();

        if (!/^[a-zA-Z0-9]{9}$/.test(enrolment)) {
          return showMsg('La matrícula debe tener exactamente 9 caracteres.', false);
        }

        if (!fullName) {
          return showMsg('Debes escribir tu nombre completo.', false);
        }

        if (fullName.length > 100) {
          return showMsg('El nombre completo no puede superar 100 caracteres.', false);
        }

        if (!isValidPhone(phone)) {
          return showMsg('El teléfono debe tener exactamente 10 dígitos.', false);
        }

        if (!isValidSecondaryEmail(secondaryEmail)) {
          return showMsg('El correo alternativo no tiene un formato válido.', false);
        }

        if (!degree) {
          return showMsg('Debes capturar tu carrera.', false);
        }

        const semester = Number(semesterRaw);
        if (!semesterRaw || !Number.isInteger(semester) || semester < 1 || semester > 20) {
          return showMsg('El semestre debe estar entre 1 y 20.', false);
        }

        const payload = {
          enrolment_number: enrolment,
          full_name: fullName,
          email: institutionalEmail,
          secondary_email: secondaryEmail || null,
          phone_number: phone,
          degree,
          semester,
          season: getSeason(),
          temporada: getSeason()
        };

        const data = await tryPost([
          { url: '/api/student/requests', body: payload }
        ]);

        currentRequest = data;
        currentRequestStatus = data.request?.status || data.status || 'REQUESTED';
        lastKnownStudentStatus = currentRequestStatus;

        renderRequestInfo(data);
        hydrateStudentFormFromRequest(data);
        updateResumeFlowBanner();
        updateHeroState();
        renderJourneyState();
        syncRegistrationLock();
        syncStep4GateText();
        syncStep4InputsVisualState();
        renderStep4PremiumState();
        startStudentAutoSync();

        goToSectionAndStep('passSection', 3);
        showMsg(data.message || 'Solicitud creada. Tu siguiente paso es mostrar tu QR al staff.');
      } catch (e) {
        console.error(e);
        showMsg(humanizeErrorMessage(e), false);
      }
    }

    async function loadStudentRequest() {
      try {
        const enrolment = validateEnrolmentStrict();
        if (!enrolment) return;

        const season = getSeason();

        const data = await getJSON(
          `/api/student/requests?enrolment_number=${encodeURIComponent(enrolment)}&season=${encodeURIComponent(season)}`
        );

        const newStatus = data.request?.status || data.status || null;
        const oldStatus = lastKnownStudentStatus;

        currentRequest = data;
        currentRequestStatus = newStatus;
        lastKnownStudentStatus = newStatus;

        renderRequestInfo(data);
        hydrateStudentFormFromRequest(data);
        updateHeroState();
        renderJourneyState();
        syncRegistrationLock();
        syncStep4GateText();
        syncStep4InputsVisualState();
        renderStep4PremiumState();

        if (oldStatus && oldStatus !== newStatus && newStatus === 'ACCESS_ENABLED') {
          showSmartToast('Acceso habilitado', 'Ya puedes continuar al paso de inscripción.');
        }

        showMsg('Solicitud cargada correctamente');
      } catch (e) {
        console.error(e);
        showMsg(humanizeErrorMessage(e), false);
      }
    }

    function renderStudentQR(plainToken) {
      const qrCanvas = document.getElementById('qrCanvas');
      const qrPlainToken = document.getElementById('qrPlainToken');
      if (!qrCanvas || !qrPlainToken) return;

      qrCanvas.innerHTML = '';
      qrPlainToken.textContent = plainToken || 'Genera tu código';

      if (!plainToken) return;

      new QRCode(qrCanvas, {
        text: plainToken,
        width: 190,
        height: 190,
        correctLevel: QRCode.CorrectLevel.M
      });
    }

    async function loadStudentPass() {
      try {
        const enrolment = validateEnrolmentStrict();
        if (!enrolment) return;

        const season = getSeason();

        const data = await tryGet([
          `/api/student/pass?enrolment_number=${encodeURIComponent(enrolment)}&season=${encodeURIComponent(season)}`,
          `/api/student/pass?enrolment_number=${encodeURIComponent(enrolment)}&temporada=${encodeURIComponent(season)}`
        ]);

        currentPass = data;
        currentRequestStatus = data.request?.status || currentRequestStatus || null;

        renderPassInfo(data);
        updateHeroState();
        goToSectionAndStep('passSection', 3);
        showMsg('Estado del pase cargado correctamente');
      } catch (e) {
        console.error(e);
        showMsg(humanizeErrorMessage(e), false);
      }
    }

    async function refreshStudentPass() {
      try {
        const enrolment = validateEnrolmentStrict();
        if (!enrolment) return;

        const season = getSeason();

        const payload = {
          enrolment_number: enrolment,
          season,
          temporada: season
        };

        const data = await tryPost([
          { url: `/api/student/pass/refresh`, body: payload }
        ]);

        currentPass = data;
        currentRequestStatus = data.request?.status || currentRequestStatus || null;

        renderPassInfo(data);
        await loadStudentRequest().catch(() => {});
        updateHeroState();
        setCurrentStep(3);

        showMsg(data.message || 'Credencial actualizada');
      } catch (e) {
        console.error(e);
        showMsg(humanizeErrorMessage(e), false);
      }
    }

    function renderPreview(data) {
      const box = document.getElementById('registrationPreview');
      if (!box) return;

      if (!data) {
        box.innerHTML = renderEmptyState(
          'Todavía no hay preview',
          'Escribe el token del proyecto y usa “Ver preview” para revisar antes de confirmar.'
        );
        return;
      }

      const student = data.student || {};
      const event = data.event || {};
      const project = data.project || {};
      const token = data.token || {};

      box.innerHTML = `
        <div class="info-card">
          <div class="info-head">
            <div>
              <div class="info-title">Preview válido</div>
              <div class="info-sub">Revisa cuidadosamente antes de confirmar</div>
            </div>
            <div><span class="chip chip-green">PREVIEW OK</span></div>
          </div>

          <div class="meta-grid">
            <div class="meta-box">
              <span class="meta-label">Alumno</span>
              <div class="meta-value">${escapeHTML(student.full_name || '—')}</div>
            </div>

            <div class="meta-box">
              <span class="meta-label">Temporada</span>
              <div class="meta-value">${escapeHTML(event.display_name || '—')}</div>
            </div>

            <div class="meta-box">
              <span class="meta-label">Proyecto</span>
              <div class="meta-value">${escapeHTML(project.general_name || '—')} | ${escapeHTML(project.project_name || '—')}</div>
            </div>

            <div class="meta-box">
              <span class="meta-label">Organización</span>
              <div class="meta-value">${escapeHTML(project.partner_name || '—')}</div>
            </div>

            <div class="meta-box">
              <span class="meta-label">Token</span>
              <div class="meta-value">${escapeHTML(token.token_value || '—')}</div>
            </div>

            <div class="meta-box">
              <span class="meta-label">Token expira</span>
              <div class="meta-value">${escapeHTML(token.expires_at || '—')}</div>
            </div>
          </div>

          <div class="actions" style="margin-top:14px;">
            <button type="button" class="btn-secondary" onclick="clearRegistrationPreview()">
              Modificar aquí
            </button>
            <button type="button" class="btn-blue" onclick="goBackToCatalogFromStep4()">
              Volver al catálogo y cambiar proyecto
            </button>
          </div>
        </div>
      `;
    }

    function clearStep4TransientState() {
      currentPreview = null;

      const previewBox = document.getElementById('registrationPreview');
      if (previewBox) {
        previewBox.innerHTML = renderEmptyState(
          'Todavía no hay preview',
          'Escribe el token del proyecto y usa “Ver preview” para revisar antes de confirmar.'
        );
      }

      const successBox = document.getElementById('registrationSuccessBox');
      if (successBox) {
        successBox.classList.add('hidden');
        successBox.innerHTML = '';
      }

      const tokenInput = document.getElementById('projectTokenInput');
      const checkbox = document.getElementById('acceptanceCheckbox');

      if (tokenInput) tokenInput.value = '';
      if (checkbox) checkbox.checked = false;

      syncStep4GateText();
      syncStep4InputsVisualState();
      renderStep4PremiumState();
    }


    function clearRegistrationPreview() {
      currentPreview = null;

      const previewBox = document.getElementById('registrationPreview');
      if (previewBox) {
        previewBox.innerHTML = renderEmptyState(
          'Todavía no hay preview',
          'Escribe el token del proyecto y usa “Ver preview” para revisar antes de confirmar.'
        );
      }

      const tokenInput = document.getElementById('projectTokenInput');
      const nameInput = document.getElementById('acceptanceFullNameInput');
      const legalInput = document.getElementById('legalVersionInput');

      if (tokenInput) tokenInput.disabled = false;
      if (nameInput) nameInput.disabled = false;
      if (legalInput) legalInput.disabled = false;

      syncStep4GateText();
      syncStep4InputsVisualState();
      renderStep4PremiumState();

      showMsg('Preview liberado. Ya puedes modificar la información.');
    }

    function goBackToCatalogFromStep4() {
      clearStep4TransientState();

      showStudentSection('catalogSection');
      setCurrentStep(1);

      renderSelectedProjectBanner();
      renderCatalog(currentCatalog);
      updateHeroState();

      showMsg('Volviste al catálogo. Tu proceso sigue guardado; solo vas a cambiar tu selección o revisar antes de continuar.');
    }

    function renderPassInfo(data) {
      const box = document.getElementById('passInfo');
      const statusBadge = document.getElementById('qrStatusBadge');
      const qrPlainToken = document.getElementById('qrPlainToken');

      if (!box || !statusBadge) return;

      if (!data) {
        box.innerHTML = renderEmptyState(
          'Todavía no hay información del pase',
          'Cuando tu solicitud exista, podrás consultar o refrescar tu credencial viva.'
        );
        statusBadge.className = 'chip chip-neutral';
        statusBadge.textContent = 'Sin sesión';
        clearCurrentPlainQrToken();
        renderStudentQR('');
        renderJourneyState();
        updateHeroState();
        syncRegistrationLock();
        syncStep4GateText();
        return;
      }

      const request = data.request || {};
      const event = data.event || {};
      const student = data.student || {};
      const session = data.pass_session || data.active_session || null;

      const requestStatus = getStudentStatus();
      const shouldShowQrSession = ['REQUESTED', 'VALIDATED'].includes(
        String(requestStatus || '').toUpperCase()
      );

      const freshToken =
        data.pass_session?.plain_token ||
        data.active_session?.plain_token ||
        '';

      if (freshToken) {
        setCurrentPlainQrToken(freshToken);
      }

      const tokenToRender = (session && shouldShowQrSession)
        ? getCurrentPlainQrToken()
        : '';

      let statusText = 'Sin sesión';
      let helperText = 'Genera o consulta tu credencial viva.';
      let timerText = 'Sin vigencia';
      let badgeClass = 'chip chip-neutral';

      if (session && shouldShowQrSession) {
        statusText = 'QR activo';
        helperText = 'Muéstralo al staff para continuar.';
        timerText = session.expires_at || '—';
        badgeClass = 'chip chip-green';
      } else if (request.status === 'ACCESS_ENABLED') {
        statusText = 'Acceso habilitado';
        helperText = 'Ya no necesitas mostrar otro QR. Continúa al paso 4.';
        timerText = 'Completado';
        badgeClass = 'chip chip-blue';
        clearCurrentPlainQrToken();
      } else if (request.status === 'REGISTERED') {
        statusText = 'Proceso cerrado';
        helperText = 'Tu inscripción ya fue completada.';
        timerText = 'Finalizado';
        badgeClass = 'chip chip-green';
        clearCurrentPlainQrToken();
      } else {
        clearCurrentPlainQrToken();
      }

      statusBadge.className = badgeClass;
      statusBadge.textContent = statusText;

      box.innerHTML = `
        <div class="pass-card">
          <div class="pass-header">
            <div class="pass-title">Credencial viva</div>
            <div class="pass-status">${escapeHTML(statusText)}</div>
          </div>

          <div class="pass-body">
            <div class="pass-user">
              <div class="pass-name">${escapeHTML(student.full_name || 'Alumno')}</div>
              <div class="pass-matricula">${escapeHTML(student.enrolment_number || '—')}</div>
            </div>

            <div class="meta-grid" style="margin-top:14px; margin-bottom:14px;">
              <div class="meta-box">
                <span class="meta-label">Folio</span>
                <div class="meta-value">${escapeHTML(request.folio || '—')}</div>
              </div>
              <div class="meta-box">
                <span class="meta-label">Temporada</span>
                <div class="meta-value">${escapeHTML(event.display_name || '—')}</div>
              </div>
              <div class="meta-box">
                <span class="meta-label">Refresh count</span>
                <div class="meta-value">${session ? escapeHTML(session.refresh_count || 0) : 0}</div>
              </div>
              <div class="meta-box">
                <span class="meta-label">Vigencia</span>
                <div class="meta-value">${escapeHTML(timerText)}</div>
              </div>
            </div>

            <div class="pass-info">
              <div>${escapeHTML(helperText)}</div>
              <div class="muted">No compartas capturas. Si el staff te lo pide, actualiza el QR.</div>
            </div>
          </div>
        </div>
      `;

      if (!shouldShowQrSession) {
        renderStudentQR('');
        if (qrPlainToken) qrPlainToken.textContent = 'No necesitas QR en este momento';
      } else {
        renderStudentQR(tokenToRender);
        if (qrPlainToken) {
          qrPlainToken.textContent = tokenToRender || 'Genera tu código';
        }
      }

      renderJourneyState();
      updateHeroState();
      syncRegistrationLock();
      syncStep4GateText();
    }

    async function previewRegistration() {
      try {
        const enrolment = getEffectiveEnrolment();
        const projectId = document.getElementById('selectedProjectId').value.trim();
        const tokenValue = document.getElementById('projectTokenInput').value.trim();

        if (!canStudentRegister) {
          return showMsg('Aún no tienes acceso habilitado. Primero muestra tu QR al staff.', false);
        }

        if (!enrolment) return showMsg('Primero recupera tu proceso o escribe tu matrícula', false);
        if (!projectId) return showMsg('Primero elige un proyecto', false);
        if (!tokenValue) return showMsg('Falta el token del proyecto', false);
        const payload = {
          enrolment_number: enrolment,
          season: getSeason(),
          temporada: getSeason(),
          project_id: Number(projectId),
          token_value: tokenValue
        };

        const data = await tryPost([
          { url: '/api/student/registration/preview', body: payload }
        ]);

        currentPreview = data;

        renderPreview(data);
        renderStep4PremiumState();
        syncStep4InputsVisualState();

        showMsg(data.message || 'Preview válido');
      } catch (e) {
        console.error(e);
        showMsg(humanizeErrorMessage(e), false);
      }
    }

    async function confirmRegistration() {
      try {
        const enrolment = getEffectiveEnrolment();
        const projectId = document.getElementById('selectedProjectId').value.trim();
        const tokenValue = document.getElementById('projectTokenInput').value.trim();
        const acceptedFullName = document.getElementById('acceptanceFullNameInput').value.trim();
        const acceptedCheckbox = document.getElementById('acceptanceCheckbox').checked;
        const legalVersion = document.getElementById('legalVersionInput').value.trim() || 'v1';

        if (!canStudentRegister) {
          return showMsg('Aún no tienes acceso habilitado. Primero muestra tu QR al staff.', false);
        }

        if (!enrolment) return showMsg('Primero recupera tu proceso o escribe tu matrícula.', false);
        if (!projectId) return showMsg('Primero elige un proyecto.', false);
        if (!tokenValue) return showMsg('Falta el token del proyecto.', false);
        if (!acceptedFullName) return showMsg('Debes escribir tu nombre completo.', false);
        if (!acceptedCheckbox) return showMsg('Debes aceptar la confirmación legal.', false);

        const payload = {
          enrolment_number: enrolment,
          season: getSeason(),
          temporada: getSeason(),
          project_id: Number(projectId),
          token_value: tokenValue,
          accepted_checkbox: acceptedCheckbox,
          accepted_full_name: acceptedFullName,
          legal_text_version: legalVersion
        };

        const data = await tryPost([
          { url: '/api/student/registration/confirm', body: payload }
        ]);

        currentRegistration = {
          project_name: data?.registration?.project_name || data?.project?.project_name || currentSelectedProject?.name || '—',
          general_name: data?.registration?.general_name || data?.project?.general_name || currentSelectedProject?.general_name || '—',
          token_value: data?.registration?.token_value || data?.token?.token_value || tokenValue,
          accepted_at: data?.legal_confirmation?.accepted_at || new Date().toLocaleString(),
          season: data?.event?.season || getSeason() || '—'
        };

        clearCurrentPlainQrToken();
        clearSavedSelectedProject();

        await loadStudentRequest().catch(() => {});
        await loadStudentPass().catch(() => {});

        stopStudentAutoSync();
        setCurrentStep(5);
        updateHeroState();
        renderRegistrationSuccess(currentRegistration);
        showStudentSection('statusSection');
        showMsg(data.message || 'Registro completado.');
      } catch (e) {
        console.error(e);
        showMsg(humanizeErrorMessage(e), false);
      }
    }

    function bindStudentNav() {
      document.querySelectorAll('[data-student-section]').forEach(btn => {
        btn.addEventListener('click', () => {
          const sectionId = btn.getAttribute('data-student-section');
          if (!sectionId) return;
          showStudentSection(sectionId);
        });
      });
    }

    function bindCatalogFilters() {
      const partner = document.getElementById('filterPartner');
      const modality = document.getElementById('filterModality');
      const day = document.getElementById('filterWeekDays');
      const schedule = document.getElementById('filterSchedule');
      const search = document.getElementById('catalogSearch');
      const season = document.getElementById('seasonSelector');

      if (season) {
        season.addEventListener('change', async () => {
          await loadCatalogsForSeason();
          await loadCatalog();
        });
      }

      [partner, modality, day, schedule].forEach(el => {
        if (el) {
          el.addEventListener('change', () => {
            loadCatalog().catch(e => {
              console.error('loadCatalog from filter error:', e);
              showMsg(humanizeErrorMessage(e), false);
            });
          });
        }
      });

      if (search) {
        search.addEventListener('input', scheduleCatalogSearch);
      }
    }

    function bindRegistrationActions() {
      // Los botones ya usan onclick inline en el HTML actual.
    }

    document.addEventListener('DOMContentLoaded', async () => {
      try {
        bindStudentNav();
        bindCatalogFilters();
        bindRegistrationActions();

        const enrolmentInput = document.getElementById('enrolmentInput');
        if (enrolmentInput) {
          enrolmentInput.addEventListener('input', () => {
            const enrolment = normalizeEnrolmentInput();
            saveStudentEnrolment(enrolment);
            renderGeneratedInstitutionalEmail();
          });
        }

        const fullNameInput = document.getElementById('fullNameInput');
        if (fullNameInput) {
          fullNameInput.addEventListener('input', () => {
            normalizeStudentNameInput();
          });
        }

        const phoneInput = document.getElementById('phoneInput');
        if (phoneInput) {
          phoneInput.addEventListener('input', () => {
            normalizePhoneInput();
          });
        }

        const semesterInput = document.getElementById('semesterInput');
        if (semesterInput) {
          semesterInput.addEventListener('input', () => {
            normalizeSemesterInput();
          });
        }

        const savedEnrolment = loadSavedStudentEnrolment();
        if (savedEnrolment) {
          const mainInput = document.getElementById('enrolmentInput');
          const recoverInput = document.getElementById('recoverEnrolmentInput');

          if (mainInput) mainInput.value = savedEnrolment.toUpperCase();
          if (recoverInput) recoverInput.value = savedEnrolment.toUpperCase();
        }

        const projectTokenInput = document.getElementById('projectTokenInput');
        if (projectTokenInput) {
          projectTokenInput.addEventListener('input', () => {
            normalizeProjectTokenInput();
            syncStep4InputsVisualState();
            renderStep4PremiumState();
          });
        }

        const acceptanceFullNameInput = document.getElementById('acceptanceFullNameInput');
        if (acceptanceFullNameInput) {
          acceptanceFullNameInput.addEventListener('input', () => {
            syncStep4InputsVisualState();
            renderStep4PremiumState();
          });
        }

        const legalVersionInput = document.getElementById('legalVersionInput');
        if (legalVersionInput) {
          legalVersionInput.addEventListener('input', () => {
            syncStep4InputsVisualState();
            renderStep4PremiumState();
          });
        }

        const acceptanceCheckbox = document.getElementById('acceptanceCheckbox');
        if (acceptanceCheckbox) {
          acceptanceCheckbox.addEventListener('change', () => {
            syncStep4InputsVisualState();
            renderStep4PremiumState();
          });
        }

        renderGeneratedInstitutionalEmail();

        await loadCatalogsForSeason().catch((e) => console.error(e));
        await loadCatalog().catch((e) => console.error(e));

        const enrolment = getEnrolment();
        if (enrolment) {
          await loadStudentRequest().catch((e) => console.error(e));

          const status = getStudentStatus();
          if (status === 'REQUESTED' || status === 'VALIDATED') {
            await loadStudentPass().catch((e) => console.error(e));
          }

          startStudentAutoSync();
        }
        if (enrolment) {
          continueStudentFlowFromStatus();
        } else {
          updateResumeFlowBanner();
          showStudentSection('catalogSection');
          setCurrentStep(1);
        }
      } catch (e) {
        console.error(e);
        showMsg('Error al inicializar la página', false);
      }
    });
  </script>
  <div id="smartToast" class="smart-toast hidden">
    <div class="smart-toast__title">Acceso habilitado</div>
    <div class="smart-toast__text">Ya puedes pasar al cierre de inscripción.</div>
  </div>
</body>
</html>
"""