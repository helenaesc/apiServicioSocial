ADMIN_HTML = r"""
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Panel Administrativo</title>
  <script src="https://unpkg.com/html5-qrcode"></script>
  <style>
    :root {
      --bg: #F4F7FA;
      --panel: #FFFFFF;
      --panel-soft: #FAFBFD;
      --text: #111827;
      --text-soft: #6B7280;
      --muted: #94A3B8;
      --line: #E5E7EB;
      --line-strong: #D1D5DB;

      --blue: #3B82F6;
      --orange: #FF8C42;
      --green: #43AA8B;
      --purple: #7D5BA6;
      --pink: #F25C78;

      --blue-soft: #EFF6FF;
      --orange-soft: #FFF3EA;
      --green-soft: #ECFDF7;
      --purple-soft: #F5F0FB;
      --pink-soft: #FFF1F5;

      --shadow-sm: 0 2px 10px rgba(15, 23, 42, 0.04);
      --shadow-md: 0 10px 24px rgba(15, 23, 42, 0.06);

      --r-md: 12px;
      --r-lg: 16px;
      --r-xl: 22px;
      --r-pill: 999px;

      --module-accent: var(--blue);
      --module-accent-soft: var(--blue-soft);
    }

    * { box-sizing: border-box; }

    html, body {
      margin: 0;
      padding: 0;
      font-family: Inter, Montserrat, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--text);
      min-height: 100vh;
    }

    .hidden { display: none !important; }

    .app-shell {
      display: grid;
      grid-template-columns: 300px 1fr;
      min-height: 100vh;
    }

    .sidebar {
      background: #FFFFFF;
      border-right: 1px solid var(--line);
      padding: 18px 16px;
      position: sticky;
      top: 0;
      height: 100vh;
      overflow-y: auto;
    }

    .sidebar-shell {
      display: flex;
      flex-direction: column;
      gap: 18px;
    }

    .brand-box {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: var(--r-xl);
      padding: 16px;
      box-shadow: var(--shadow-sm);
    }

    .brand-title {
      font-size: 1.06rem;
      font-weight: 900;
      margin-bottom: 4px;
      color: var(--text);
    }

    .brand-subtitle {
      font-size: .88rem;
      color: var(--text-soft);
      line-height: 1.45;
    }

    .role-box {
      margin-top: 12px;
      border-radius: var(--r-md);
      background: var(--panel-soft);
      border: 1px solid var(--line);
      padding: 12px 14px;
      font-size: .9rem;
      color: var(--text-soft);
      font-weight: 700;
    }

    .nav-group {
      display: grid;
      gap: 10px;
    }

    .nav-group-header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      padding: 0 4px;
    }

    .nav-group-title {
      font-size: .76rem;
      text-transform: uppercase;
      letter-spacing: .08em;
      font-weight: 900;
      color: var(--muted);
    }

    .nav-group-pill {
      font-size: .72rem;
      font-weight: 900;
      padding: 6px 9px;
      border-radius: var(--r-pill);
      white-space: nowrap;
    }

    .pill-purple { background: var(--purple-soft); color: var(--purple); }
    .pill-orange { background: var(--orange-soft); color: var(--orange); }
    .pill-green  { background: var(--green-soft); color: var(--green); }
    .pill-pink   { background: var(--pink-soft); color: var(--pink); }
    .pill-blue   { background: var(--blue-soft); color: var(--blue); }

    .nav-list {
      display: grid;
      gap: 8px;
    }

    .nav-item {
      width: 100%;
      text-align: left;
      border: 1px solid transparent;
      background: transparent;
      color: var(--text);
      border-radius: var(--r-lg);
      padding: 12px 14px;
      font-size: .94rem;
      font-weight: 800;
      cursor: pointer;
      transition: background .18s ease, transform .16s ease, border-color .18s ease, box-shadow .18s ease;
    }

    .nav-item:hover {
      transform: translateY(-1px);
      background: #F9FAFB;
      border-color: var(--line);
      box-shadow: var(--shadow-sm);
    }

    .nav-item.active {
      background: var(--module-accent-soft);
      border-color: color-mix(in srgb, var(--module-accent) 35%, white);
      color: var(--module-accent);
      box-shadow: var(--shadow-sm);
    }

    .sidebar-actions {
      display: grid;
      gap: 10px;
      margin-top: 6px;
    }

    .sidebar-actions a,
    .sidebar-actions button {
      text-decoration: none;
      text-align: center;
      border: 1px solid var(--line);
      background: white;
      color: var(--text-soft);
      border-radius: var(--r-md);
      padding: 11px 12px;
      font-size: .9rem;
      font-weight: 800;
      cursor: pointer;
      transition: transform .16s ease, box-shadow .16s ease, border-color .16s ease;
    }

    .sidebar-actions a:hover,
    .sidebar-actions button:hover {
      transform: translateY(-1px);
      box-shadow: var(--shadow-sm);
      border-color: var(--line-strong);
    }

    .main {
      padding: 22px;
    }

    .topbar {
      margin-bottom: 18px;
    }

    .screen-header {
      background: linear-gradient(135deg, white 0%, var(--module-accent-soft) 100%);
      border: 1px solid color-mix(in srgb, var(--module-accent) 25%, white);
      border-radius: var(--r-xl);
      padding: 18px 20px;
      box-shadow: var(--shadow-md);
    }

    .screen-header__content {
      display: flex;
      justify-content: space-between;
      gap: 14px;
      flex-wrap: wrap;
      align-items: center;
    }

    .screen-kicker {
      font-size: .76rem;
      text-transform: uppercase;
      letter-spacing: .08em;
      color: var(--module-accent);
      font-weight: 900;
      margin-bottom: 5px;
    }

    .screen-title strong {
      display: block;
      font-size: 1.34rem;
      font-weight: 900;
      margin-bottom: 4px;
      color: var(--text);
    }

    .screen-title span {
      display: block;
      color: var(--text-soft);
      font-size: .95rem;
    }

    .screen-badges {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      align-items: center;
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

    .chip-accent {
      background: var(--module-accent-soft);
      color: var(--module-accent);
      border-color: color-mix(in srgb, var(--module-accent) 20%, white);
    }

    .chip-dark {
      background: white;
      color: var(--text-soft);
      border-color: var(--line);
    }

    .login-wrap {
      max-width: 820px;
      margin: 40px auto;
      padding: 0 18px;
    }

    .login-card,
    .card {
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: var(--r-lg);
      box-shadow: var(--shadow-sm);
      padding: 22px;
    }

    .msg {
      display: none;
      margin-bottom: 18px;
      padding: 14px 16px;
      border-radius: var(--r-md);
      font-size: .94rem;
      font-weight: 800;
      border: 1px solid transparent;
      box-shadow: var(--shadow-sm);
    }

    .msg.ok {
      display: block;
      background: var(--green-soft);
      color: var(--green);
      border-color: #CDEFE4;
    }

    .msg.err {
      display: block;
      background: var(--pink-soft);
      color: var(--pink);
      border-color: #FFD4DD;
    }

    .module { display: none; }
    .module.active { display: block; }

    .module-grid {
      display: grid;
      grid-template-columns: repeat(12, 1fr);
      gap: 18px;
    }

    .span-12 { grid-column: span 12; }
    .span-8 { grid-column: span 8; }
    .span-6 { grid-column: span 6; }
    .span-4 { grid-column: span 4; }

    .module-card-title {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: center;
      flex-wrap: wrap;
      margin-bottom: 12px;
    }

    h2, h3 {
      margin: 0;
      line-height: 1.2;
      color: var(--text);
    }

    h2 {
      font-size: 1.14rem;
      font-weight: 900;
    }

    h3 {
      font-size: 1rem;
      font-weight: 900;
    }

    .muted {
      color: var(--text-soft);
      font-size: .93rem;
      line-height: 1.55;
    }

    .small {
      font-size: .84rem;
      color: var(--text-soft);
    }

    .screen-chip {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 12px;
      border-radius: var(--r-pill);
      background: var(--module-accent-soft);
      color: var(--module-accent);
      font-size: .82rem;
      font-weight: 900;
      border: 1px solid color-mix(in srgb, var(--module-accent) 16%, white);
    }

    .form-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 12px;
      margin-top: 14px;
    }

    .field {
      display: flex;
      flex-direction: column;
      gap: 7px;
    }

    .field label {
      font-size: .78rem;
      font-weight: 900;
      color: var(--text-soft);
      text-transform: uppercase;
      letter-spacing: .04em;
    }

    input, select, textarea, button {
      width: 100%;
      min-height: 44px;
      border-radius: var(--r-md);
      border: 1px solid var(--line-strong);
      background: white;
      color: var(--text);
      font-size: .94rem;
      padding: 10px 12px;
      outline: none;
      transition: border-color .18s ease, box-shadow .18s ease, transform .16s ease;
    }

    textarea {
      min-height: 100px;
      resize: vertical;
    }

    input:focus, select:focus, textarea:focus {
      border-color: var(--module-accent);
      box-shadow: 0 0 0 3px color-mix(in srgb, var(--module-accent) 14%, white);
    }

    .actions {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-top: 16px;
    }

    .actions > button,
    .actions > a {
      width: auto;
      min-width: 150px;
    }

    .btn-primary,
    .btn-secondary,
    .btn-danger {
      min-height: 44px;
      border-radius: var(--r-md);
      padding: 10px 14px;
      font-size: .94rem;
      font-weight: 900;
      cursor: pointer;
      transition: transform .15s ease, box-shadow .15s ease, opacity .15s ease, border-color .15s ease;
    }

    .btn-primary:hover,
    .btn-secondary:hover,
    .btn-danger:hover {
      transform: translateY(-1px) scale(1.01);
    }

    .btn-primary {
      background: var(--blue);
      color: white;
      border: none;
      box-shadow: 0 8px 18px rgba(59,130,246,0.20);
    }

    .btn-secondary {
      background: #FFFFFF;
      color: #374151;
      border: 1px solid var(--line);
      box-shadow: var(--shadow-sm);
    }

    .btn-danger {
      background: var(--pink);
      color: white;
      border: none;
      box-shadow: 0 8px 18px rgba(242,92,120,0.18);
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 11px;
      border-radius: var(--r-pill);
      font-size: .76rem;
      font-weight: 900;
      white-space: nowrap;
    }

    .badge-success { background: var(--green-soft); color: var(--green); }
    .badge-warn { background: var(--orange-soft); color: var(--orange); }
    .badge-danger { background: var(--pink-soft); color: var(--pink); }
    .badge-purple { background: var(--purple-soft); color: var(--purple); }
    .badge-blue { background: var(--blue-soft); color: var(--blue); }
    .badge-neutral { background: #F3F4F6; color: #374151; }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 14px;
      margin-top: 16px;
    }

    .kpi-card {
      border-radius: var(--r-lg);
      padding: 18px;
      color: white;
      box-shadow: var(--shadow-sm);
    }

    .kpi-card--green { background: linear-gradient(135deg, #43AA8B 0%, #57C3A2 100%); }
    .kpi-card--orange { background: linear-gradient(135deg, #FF8C42 0%, #FFAA6E 100%); }
    .kpi-card--purple { background: linear-gradient(135deg, #7D5BA6 0%, #9B79C6 100%); }
    .kpi-card--pink { background: linear-gradient(135deg, #F25C78 0%, #FF7D96 100%); }
    .kpi-card--blue { background: linear-gradient(135deg, #3B82F6 0%, #60A5FA 100%); }

    .kpi-label {
      font-size: .78rem;
      text-transform: uppercase;
      letter-spacing: .05em;
      font-weight: 900;
      opacity: .95;
      margin-bottom: 8px;
    }

    .kpi-value {
      font-size: 2rem;
      font-weight: 900;
      line-height: 1;
      margin-bottom: 8px;
    }

    .kpi-sub {
      font-size: .84rem;
      opacity: .96;
    }

    .meta {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 10px;
      margin-top: 10px;
    }

    .meta-box {
      border: 1px solid var(--line);
      background: var(--panel-soft);
      border-radius: var(--r-md);
      padding: 10px 12px;
    }

    .meta-label {
      display: block;
      font-size: .72rem;
      text-transform: uppercase;
      color: var(--muted);
      font-weight: 900;
      margin-bottom: 4px;
      letter-spacing: .04em;
    }

    .meta-value {
      color: var(--text);
      font-weight: 800;
      font-size: .92rem;
      line-height: 1.4;
    }

    .record-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 14px;
      margin-top: 14px;
    }

    .record-card {
      background: #FFF;
      border: 1px solid var(--line);
      border-radius: var(--r-lg);
      padding: 16px;
      box-shadow: var(--shadow-sm);
    }

    .record-card__head {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: start;
      margin-bottom: 10px;
      flex-wrap: wrap;
    }

    .record-card__title {
      font-size: .98rem;
      font-weight: 900;
      color: var(--text);
      margin-bottom: 3px;
    }

    .record-card__sub {
      font-size: .84rem;
      color: var(--text-soft);
    }

    .record-stack {
      display: grid;
      gap: 8px;
      margin-top: 10px;
    }

    .stack-row {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: start;
      font-size: .88rem;
    }

    .stack-row strong {
      color: var(--text-soft);
      font-weight: 800;
      min-width: 120px;
    }

    .stack-row span {
      text-align: right;
      color: var(--text);
      font-weight: 700;
      word-break: break-word;
    }

    .mono {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: .9rem;
      background: #111827;
      color: #E5EEF8;
      border-radius: var(--r-md);
      padding: 9px 11px;
      word-break: break-all;
      display: inline-block;
    }

    .mono-soft {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: .88rem;
      color: #334155;
      background: #F3F4F6;
      border: 1px solid var(--line);
      padding: 5px 8px;
      border-radius: 10px;
      display: inline-block;
    }

    .table-wrap {
      overflow: auto;
      margin-top: 14px;
      border: 1px solid var(--line);
      border-radius: var(--r-lg);
      background: white;
      box-shadow: var(--shadow-sm);
    }

    table {
      width: 100%;
      border-collapse: collapse;
      min-width: 840px;
      background: white;
    }

    th, td {
      padding: 12px 14px;
      border-bottom: 1px solid var(--line);
      text-align: left;
      vertical-align: top;
      font-size: .9rem;
    }

    th {
      background: #F8FAFC;
      color: var(--text);
      font-weight: 900;
    }

    tr:last-child td {
      border-bottom: none;
    }

    .xp-wrapper {
      display: flex;
      flex-direction: column;
      gap: 6px;
      min-width: 180px;
    }

    .xp-text {
      font-size: .78rem;
      font-weight: 900;
      color: var(--text-soft);
      display: flex;
      justify-content: space-between;
      gap: 10px;
    }

    .xp-bar-bg {
      width: 100%;
      height: 12px;
      background: #E5E7EB;
      border-radius: 999px;
      overflow: hidden;
    }

    .xp-bar-fill {
      height: 100%;
      width: 0%;
      border-radius: 999px;
      background: linear-gradient(90deg, var(--blue) 0%, #60A5FA 100%);
      transition: width .35s ease;
    }

    .xp-bar-fill.level-up {
      background: linear-gradient(90deg, var(--green) 0%, #57C3A2 100%);
    }

    .scanner-shell {
      max-width: 620px;
      margin: 18px auto 0;
      display: grid;
      gap: 14px;
      justify-items: center;
    }

    #staffScanner {
      width: 100%;
      max-width: 420px;
      border-radius: var(--r-lg);
      overflow: hidden;
      border: 1px solid var(--line);
      background: white;
      box-shadow: var(--shadow-sm);
    }

    .center-note {
      text-align: center;
      color: var(--text-soft);
      font-size: .9rem;
      max-width: 620px;
      margin: 0 auto;
    }

    .evidence-box {
      display: grid;
      gap: 12px;
      margin-top: 14px;
    }

    .json-box {
      background: #0F172A;
      color: #E2E8F0;
      border-radius: var(--r-lg);
      padding: 14px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: .84rem;
      line-height: 1.5;
      white-space: pre-wrap;
      word-break: break-word;
      overflow: auto;
    }

    @media (max-width: 1280px) {
      .stats-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }

    @media (max-width: 1200px) {
      .app-shell {
        grid-template-columns: 1fr;
      }

      .sidebar {
        position: static;
        height: auto;
      }

      .span-8, .span-6, .span-4 {
        grid-column: span 12;
      }
    }

    @media (max-width: 700px) {
      .stats-grid {
        grid-template-columns: 1fr;
      }

      .main {
        padding: 18px;
      }

      .actions {
        flex-direction: column;
        align-items: stretch;
      }

      .actions > button,
      .actions > a {
        width: 100%;
      }
    }

    .dashboard-shell {
      display: grid;
      gap: 16px;
      margin-top: 16px;
    }

    .health-hero {
      border: 1px solid var(--line);
      background: linear-gradient(135deg, white 0%, var(--purple-soft) 100%);
      border-radius: var(--r-xl);
      padding: 18px;
      box-shadow: var(--shadow-sm);
    }

    .health-hero__head {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: start;
      flex-wrap: wrap;
      margin-bottom: 12px;
    }

    .health-hero__title {
      font-size: 1.06rem;
      font-weight: 900;
      color: var(--text);
    }

    .health-hero__sub {
      font-size: .92rem;
      color: var(--text-soft);
      margin-top: 4px;
    }

    .health-score {
      min-width: 120px;
      text-align: center;
      border-radius: 18px;
      padding: 14px 16px;
      background: white;
      border: 1px solid var(--line);
    }

    .health-score__value {
      font-size: 1.8rem;
      font-weight: 900;
      line-height: 1;
    }

    .health-score__label {
      margin-top: 6px;
      font-size: .78rem;
      font-weight: 900;
      color: var(--text-soft);
      text-transform: uppercase;
      letter-spacing: .05em;
    }

    .health-bars {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 12px;
    }

    .health-bar-card {
      border: 1px solid var(--line);
      border-radius: var(--r-lg);
      background: white;
      padding: 14px;
    }

    .health-bar-card__top {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      margin-bottom: 8px;
      align-items: center;
    }

    .health-bar-card__title {
      font-size: .84rem;
      font-weight: 900;
      color: var(--text-soft);
      text-transform: uppercase;
      letter-spacing: .04em;
    }

    .health-bar-card__value {
      font-size: .92rem;
      font-weight: 900;
      color: var(--text);
    }

    .project-priority {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 10px;
      border-radius: 999px;
      font-size: .74rem;
      font-weight: 900;
      white-space: nowrap;
    }

    .project-priority.high {
      background: var(--pink-soft);
      color: var(--pink);
    }

    .project-priority.medium {
      background: var(--orange-soft);
      color: var(--orange);
    }

    .project-priority.low {
      background: var(--green-soft);
      color: var(--green);
    }

    .action-tag {
      display: inline-flex;
      align-items: center;
      padding: 7px 10px;
      border-radius: 999px;
      font-size: .74rem;
      font-weight: 900;
      white-space: nowrap;
    }

    .action-tag.high {
      background: var(--pink-soft);
      color: var(--pink);
    }

    .action-tag.medium {
      background: var(--orange-soft);
      color: var(--orange);
    }

    .action-tag.low {
      background: var(--green-soft);
      color: var(--green);
    }

    .project-highlight-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 14px;
    }

    .project-highlight-card {
      border: 1px solid var(--line);
      background: white;
      border-radius: var(--r-xl);
      padding: 16px;
      box-shadow: var(--shadow-sm);
    }

    .project-highlight-card.primary {
      background: linear-gradient(135deg, white 0%, var(--pink-soft) 100%);
      border-color: #ffd5de;
    }

    .project-highlight-card.success {
      background: linear-gradient(135deg, white 0%, var(--green-soft) 100%);
      border-color: #d0eee3;
    }

    .project-highlight-card.info {
      background: linear-gradient(135deg, white 0%, var(--blue-soft) 100%);
      border-color: #dbeafe;
    }

    .project-highlight__kicker {
      font-size: .76rem;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: .05em;
      color: var(--text-soft);
      margin-bottom: 6px;
    }

    .project-highlight__title {
      font-size: 1rem;
      font-weight: 900;
      color: var(--text);
      margin-bottom: 4px;
    }

    .project-highlight__sub {
      font-size: .88rem;
      color: var(--text-soft);
      margin-bottom: 12px;
    }

    .project-highlight__value {
      font-size: 1.9rem;
      font-weight: 900;
      line-height: 1;
      color: var(--text);
    }

    .project-highlight__meta {
      margin-top: 10px;
      font-size: .86rem;
      color: var(--text-soft);
    }

    .record-card.clean-project {
      display: grid;
      gap: 12px;
    }

    .clean-project__top {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: start;
      flex-wrap: wrap;
    }

    .clean-project__title {
      font-size: 1rem;
      font-weight: 900;
      color: var(--text);
    }

    .clean-project__sub {
      font-size: .9rem;
      color: var(--text-soft);
      margin-top: 4px;
    }

    .clean-project__insight {
      border-radius: 14px;
      padding: 10px 12px;
      font-size: .88rem;
      font-weight: 700;
      border: 1px solid var(--line);
      background: #fafafa;
      color: var(--text);
    }

    .clean-project__metrics {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
      gap: 10px;
    }

    .metric-chip {
      border: 1px solid var(--line);
      border-radius: 14px;
      padding: 10px 12px;
      background: white;
    }

    .metric-chip__label {
      display: block;
      font-size: .74rem;
      font-weight: 900;
      color: var(--text-soft);
      text-transform: uppercase;
      letter-spacing: .04em;
      margin-bottom: 4px;
    }

    .metric-chip__value {
      font-size: .96rem;
      font-weight: 900;
      color: var(--text);
    }

    .cases-board {
      border: 1px solid var(--line);
      border-radius: var(--r-xl);
      background: white;
      box-shadow: var(--shadow-sm);
      overflow: hidden;
    }

    .cases-board__head {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: center;
      flex-wrap: wrap;
      padding: 16px 18px;
      border-bottom: 1px solid var(--line);
      background: linear-gradient(135deg, #ffffff 0%, var(--orange-soft) 100%);
    }

    .cases-board__title {
      font-size: 1rem;
      font-weight: 900;
      color: var(--text);
    }

    .cases-board__sub {
      font-size: .9rem;
      color: var(--text-soft);
      margin-top: 4px;
    }

    .cases-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 14px;
      padding: 16px;
    }

    .case-card {
      border: 1px solid var(--line);
      border-radius: var(--r-lg);
      background: white;
      padding: 16px;
      display: grid;
      gap: 12px;
    }

    .case-card.high {
      background: linear-gradient(135deg, white 0%, var(--pink-soft) 100%);
      border-color: #ffd4dc;
    }

    .case-card.medium {
      background: linear-gradient(135deg, white 0%, var(--orange-soft) 100%);
      border-color: #ffd9c0;
    }

    .case-card.low {
      background: linear-gradient(135deg, white 0%, var(--green-soft) 100%);
      border-color: #d5efe6;
    }

    .case-card__top {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      align-items: start;
      flex-wrap: wrap;
    }

    .case-card__title {
      font-size: .96rem;
      font-weight: 900;
      color: var(--text);
    }

    .case-card__value {
      font-size: 1.7rem;
      font-weight: 900;
      line-height: 1;
      color: var(--text);
    }

    .case-card__sub {
      font-size: .88rem;
      color: var(--text-soft);
      line-height: 1.45;
    }

    .case-card__actions {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .case-card__mini {
      display: grid;
      gap: 8px;
    }

    .case-mini-row {
      display: flex;
      justify-content: space-between;
      gap: 10px;
      font-size: .86rem;
      color: var(--text-soft);
    }

    .case-mini-row strong {
      color: var(--text);
    }

    .support-summary-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
      gap: 12px;
      margin-top: 14px;
      margin-bottom: 14px;
    }

    .support-mini-kpi {
      border: 1px solid var(--line);
      border-radius: var(--r-lg);
      background: white;
      box-shadow: var(--shadow-sm);
      padding: 14px;
    }

    .support-mini-kpi__label {
      font-size: .74rem;
      font-weight: 900;
      text-transform: uppercase;
      letter-spacing: .04em;
      color: var(--text-soft);
      margin-bottom: 8px;
    }

    .support-mini-kpi__value {
      font-size: 1.5rem;
      font-weight: 900;
      line-height: 1;
      color: var(--text);
    }

    .support-mini-kpi__sub {
      font-size: .82rem;
      color: var(--text-soft);
      margin-top: 8px;
    }

    .support-student-card {
      display: grid;
      gap: 12px;
    }

    .support-student__top {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      align-items: start;
      flex-wrap: wrap;
    }

    .support-student__name {
      font-size: 1rem;
      font-weight: 900;
      color: var(--text);
    }

    .support-student__sub {
      font-size: .87rem;
      color: var(--text-soft);
      margin-top: 4px;
    }

    .support-student__reason {
      border-radius: 14px;
      padding: 10px 12px;
      border: 1px solid var(--line);
      background: #fafafa;
      font-size: .88rem;
      font-weight: 700;
      color: var(--text);
    }

    .support-student__metrics {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(145px, 1fr));
      gap: 10px;
    }

    .support-metric {
      border: 1px solid var(--line);
      border-radius: 14px;
      background: white;
      padding: 10px 12px;
    }

    .support-metric__label {
      display: block;
      font-size: .73rem;
      font-weight: 900;
      color: var(--text-soft);
      text-transform: uppercase;
      letter-spacing: .04em;
      margin-bottom: 4px;
    }

    .support-metric__value {
      font-size: .94rem;
      font-weight: 900;
      color: var(--text);
    }

    .support-priority {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 10px;
      border-radius: 999px;
      font-size: .74rem;
      font-weight: 900;
      white-space: nowrap;
    }

    .support-priority.high {
      background: var(--pink-soft);
      color: var(--pink);
    }

    .support-priority.medium {
      background: var(--orange-soft);
      color: var(--orange);
    }

    .support-priority.low {
      background: var(--green-soft);
      color: var(--green);
    }

    .support-summary-wrap {
      display: grid;
      gap: 12px;
      margin-top: 14px;
      margin-bottom: 16px;
    }

    .support-summary-toolbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }

    .support-summary-title {
      font-size: .88rem;
      font-weight: 900;
      color: var(--text-soft);
      text-transform: uppercase;
      letter-spacing: .04em;
    }

    .support-summary-actions {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }

    .support-summary-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(155px, 1fr));
      gap: 12px;
      align-items: stretch;
    }

    .support-mini-kpi {
      border: 1px solid var(--line);
      border-radius: var(--r-lg);
      background: white;
      box-shadow: var(--shadow-sm);
      padding: 14px;
      transition: transform .16s ease, box-shadow .16s ease, border-color .16s ease;
    }

    .support-mini-kpi.clickable {
      cursor: pointer;
    }

    .support-mini-kpi.clickable:hover {
      transform: translateY(-1px);
      box-shadow: var(--shadow-md);
      border-color: var(--line-strong);
    }

    .support-mini-kpi.active {
      border-color: color-mix(in srgb, var(--green) 35%, white);
      background: linear-gradient(135deg, white 0%, var(--green-soft) 100%);
    }

    .support-filter-chip {
      width: auto;
      min-height: 36px;
      padding: 8px 12px;
      border-radius: 999px;
      border: 1px solid var(--line);
      background: white;
      color: var(--text-soft);
      font-size: .82rem;
      font-weight: 900;
      cursor: pointer;
    }

    .support-filter-chip.active {
      background: var(--green-soft);
      color: var(--green);
      border-color: #cfeee3;
    }

    .support-results-wrap {
      display: grid;
      gap: 14px;
    }
  </style>
</head>
<body>
  <div id="loginWrap" class="login-wrap">
    <div id="msgLogin" class="msg"></div>

    <div class="login-card">
      <h2>Acceso administrativo</h2>
      <div class="muted">
        Inicia sesión con tu cuenta ADMIN o STAFF. El panel usará sesión real del servidor.
      </div>

      <div class="form-grid" style="max-width:640px;">
        <div class="field">
          <label>Correo</label>
          <input id="loginEmail" type="email" placeholder="admin@evento.com">
        </div>
        <div class="field">
          <label>Contraseña</label>
          <input id="loginPassword" type="password" placeholder="Tu contraseña">
        </div>
      </div>

      <div class="actions">
        <button type="button" class="btn-primary" onclick="loginAdmin()">Entrar</button>
        <button type="button" class="btn-secondary" onclick="clearLoginFields()">Limpiar</button>
      </div>

      <div class="small" id="loginHint" style="margin-top:12px;">Sesión actual: no iniciada</div>
    </div>
  </div>

  <div id="appShell" class="app-shell hidden">
    <aside class="sidebar">
      <div class="sidebar-shell">
        <div class="brand-box">
          <div class="brand-title">Panel de Eventos Grandes</div>
          <div class="brand-subtitle">
            Operación clara, trazable y con evidencia legal verificable.
          </div>

          <div class="role-box" id="sidebarRoleBox">Rol actual: —</div>
        </div>

        <div id="adminNavWrap">
          <div class="nav-group">
            <div class="nav-group-header">
              <div class="nav-group-title">Estrategia</div>
              <span class="nav-group-pill pill-purple">Morado</span>
            </div>
             <div class="nav-list">
              <button class="nav-item active" data-module="summaryModule" onclick="showModule('summaryModule')">Dashboard</button>
              <button class="nav-item" data-module="eventsModule" onclick="showModule('eventsModule')">Temporadas</button>
              <button class="nav-item" data-module="masterProjectsModule" onclick="showModule('masterProjectsModule')">Proyectos Base</button>
              <button class="nav-item" data-module="studentSupportModule" onclick="showModule('studentSupportModule')">Solicitudes y Pases</button>
            </div>
          </div>

          <div class="nav-group">
            <div class="nav-group-header">
              <div class="nav-group-title">Operación</div>
              <div style="display:flex; gap:6px; flex-wrap:wrap;">
                <span class="nav-group-pill pill-orange">Naranja</span>
                <span class="nav-group-pill pill-green">Verde</span>
              </div>
            </div>
            <div class="nav-list">
              <button class="nav-item" data-module="eventProjectsModule" onclick="showModule('eventProjectsModule')">Proyectos Activos</button>
              <button class="nav-item" data-module="tokensModule" onclick="showModule('tokensModule')">Tokens</button>
              <button class="nav-item" data-module="registrationsModule" onclick="showModule('registrationsModule')">Inscritos</button>
              <button class="nav-item" data-module="checkinModule" onclick="showModule('checkinModule')">Check-in (QR)</button>
            </div>
          </div>

          <div class="nav-group">
            <div class="nav-group-header">
              <div class="nav-group-title">Control</div>
              <span class="nav-group-pill pill-pink">Rosa</span>
            </div>
            <div class="nav-list">
              <button class="nav-item" data-module="incidentsModule" onclick="showModule('incidentsModule')">Incidentes</button>
              <button class="nav-item" data-module="staffModule" onclick="showModule('staffModule')">Staff</button>
              <button class="nav-item" data-module="evidenceModule" onclick="showModule('evidenceModule')">Evidencia Legal</button>
              <button class="nav-item" data-module="importExportModule" onclick="showModule('importExportModule')">Importar / Exportar</button>
              <button class="nav-item" data-module="exportModule" onclick="showModule('exportModule')">Reporte por Temporada</button>
            </div>
          </div>
        </div>

        <div id="staffNavWrap" class="hidden">
          <div class="nav-group">
            <div class="nav-group-header">
              <div class="nav-group-title">Operación Staff</div>
              <span class="nav-group-pill pill-green">Verde</span>
            </div>
            <div class="nav-list">
              <button class="nav-item active" data-module="checkinModule" onclick="showModule('checkinModule')">Check-in (QR)</button>
              <button class="nav-item" data-module="incidentsModule" onclick="showModule('incidentsModule')">Incidentes</button>
            </div>
          </div>
        </div>

        <div class="sidebar-actions">
          <a href="/">Vista Alumno</a>
          <a href="/health">Health</a>
          <button type="button" onclick="logoutAdmin()">Cerrar sesión</button>
        </div>
      </div>
    </aside>

    <main class="main">
      <div id="msgApp" class="msg"></div>

      <div class="topbar">
        <div class="screen-header">
          <div class="screen-header__content">
            <div class="screen-title">
              <div class="screen-kicker" id="moduleKicker">Estrategia</div>
              <strong id="moduleTitle">Dashboard</strong>
              <span id="moduleSubtitle">Visión ejecutiva del evento.</span>
            </div>
            <div class="screen-badges">
              <span class="chip chip-accent" id="headerAccentBadge">Dashboard</span>
              <span class="chip chip-dark" id="headerRoleBadge">Panel</span>
            </div>
          </div>
        </div>
      </div>

      <div class="module active" id="summaryModule">
        <div class="module-grid">
          <div class="card span-12">
            <div class="module-card-title">
              <h2>Dashboard Ejecutivo</h2>
              <span class="screen-chip">Resumen general</span>
            </div>
            <div class="muted">
              KPI ejecutivos, proyectos, tokens, incidentes y estado real de la temporada.
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Temporada para dashboard</label>
                <select id="dashboardEventSelector"></select>
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-primary" onclick="loadDashboard()">Cargar dashboard</button>
              <button type="button" class="btn-secondary" onclick="loadEvents()">Recargar temporadas</button>
            </div>

            <div class="dashboard-shell">
              <div id="dashboardSummary" class="stats-grid"></div>
              <div id="dashboardHealthHero"></div>
              <div id="dashboardCasesBoard"></div>
              <div id="dashboardProjectsHighlights"></div>
              <div id="dashboardProjectsBody" class="record-grid"></div>
            </div>
          </div>
        </div>
      </div>

      <div class="module" id="studentSupportModule">
        <div class="module-grid">
          <div class="card span-12">
            <div class="module-card-title">
              <h2>Solicitudes y Pases</h2>
              <span class="screen-chip">Mesa de corrección</span>
            </div>

            <div class="muted">
              Busca alumnos por matrícula, folio, nombre o correo. Corrige datos, revisa solicitud, revoca pase, genera nuevo pase o habilita acceso manualmente.
            </div>

            <div class="form-grid" style="margin-top:14px;">
              <div class="field">
                <label>Temporada</label>
                <select id="studentSupportEventSelector"></select>
              </div>
              <div class="field">
                <label>Buscar</label>
                <input id="studentSupportSearch" placeholder="Matrícula, folio, nombre o correo">
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-primary" onclick="searchStudentSupport()">Buscar</button>
              <button type="button" class="btn-secondary" onclick="clearStudentSupportSearch()">Limpiar</button>
            </div>
          </div>

          <div class="card span-7">
            <div class="module-card-title">
              <h2>Resultados</h2>
              <span class="screen-chip">Consulta</span>
            </div>
            <div id="studentSupportSummary"></div>
            <div id="studentSupportResultsWrap" class="support-results-wrap">
              <div id="studentSupportResults" class="record-grid"></div>
            </div>
          </div>

          <div class="card span-5">
            <div class="module-card-title">
              <h2>Editar alumno</h2>
              <span class="screen-chip">Corrección</span>
            </div>

            <div class="small" id="studentSupportSelectedHint" style="margin-bottom:12px;">
              Selecciona un alumno desde los resultados.
            </div>

            <div class="form-grid">
              <div class="field">
                <label>User ID</label>
                <input id="ss_user_id" readonly>
              </div>
              <div class="field">
                <label>Request ID</label>
                <input id="ss_request_id" readonly>
              </div>

              <div class="field">
                <label>Nombre</label>
                <input id="ss_first_name" placeholder="Nombre">
              </div>
              <div class="field">
                <label>Segundo nombre</label>
                <input id="ss_second_name" placeholder="Segundo nombre">
              </div>

              <div class="field">
                <label>Apellido paterno</label>
                <input id="ss_p_last_name" placeholder="Apellido paterno">
              </div>
              <div class="field">
                <label>Apellido materno</label>
                <input id="ss_m_last_name" placeholder="Apellido materno">
              </div>

              <div class="field">
                <label>Correo principal</label>
                <input id="ss_email" type="email" placeholder="correo@ejemplo.com">
              </div>
              <div class="field">
                <label>Segundo correo</label>
                <input id="ss_secondary_email" type="email" placeholder="Opcional">
              </div>

              <div class="field">
                <label>Teléfono</label>
                <input id="ss_phone_number" placeholder="Teléfono">
              </div>
              <div class="field">
                <label>Matrícula</label>
                <input id="ss_enrolment_number" placeholder="Ej: a01234567">
              </div>

              <div class="field">
                <label>Carrera</label>
                <input id="ss_degree" placeholder="Ej: LAF">
              </div>
              <div class="field">
                <label>Semestre</label>
                <input id="ss_semester" type="number" min="1" max="20" placeholder="Ej: 5">
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-primary" onclick="saveStudentSupportUser()">Guardar cambios</button>
              <button type="button" class="btn-secondary" onclick="reloadSelectedStudentSupport()">Recargar detalle</button>
            </div>

            <hr style="margin:18px 0; border:none; border-top:1px solid var(--line);">

            <div class="module-card-title" style="margin-bottom:8px;">
              <h3>Operación de solicitud / pase</h3>
            </div>

            <div class="actions">
              <button type="button" class="btn-secondary" onclick="reissueSelectedStudentPass()">Generar nuevo pase</button>
              <button type="button" class="btn-danger" onclick="revokeSelectedStudentPass()">Revocar pase activo</button>
              <button type="button" class="btn-secondary" onclick="enableSelectedStudentAccess()">Habilitar acceso manualmente</button>
            </div>

            <div id="studentSupportDetail" class="record-grid" style="margin-top:14px;"></div>
          </div>
        </div>
      </div>

      <div class="module" id="eventsModule">
        <div class="module-grid">
          <div class="card span-6">
            <div class="module-card-title">
              <h2>Crear temporada</h2>
              <span class="screen-chip">Configuración</span>
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Año</label>
                <input id="eventYear" type="number" min="2020" max="2100" placeholder="Ej: 2026">
              </div>
              <div class="field">
                <label>Temporada</label>
                <select id="eventSeason">
                  <option value="PRIMAVERA">Primavera</option>
                  <option value="INVIERNO">Invierno</option>
                </select>
              </div>
              <div class="field">
                <label>Estado</label>
                <select id="eventStatus">
                  <option value="VISIBLE">VISIBLE</option>
                  <option value="DRAFT">DRAFT</option>
                  <option value="ONSITE">ONSITE</option>
                  <option value="CLOSED">CLOSED</option>
                  <option value="ARCHIVED">ARCHIVED</option>
                </select>
              </div>
              <div class="field">
                <label>Visible para alumnos</label>
                <select id="eventVisible">
                  <option value="true">Sí</option>
                  <option value="false">No</option>
                </select>
              </div>
              <div class="field">
                <label>Abre catálogo</label>
                <input id="eventCatalogOpenAt" type="datetime-local">
              </div>
              <div class="field">
                <label>Inicio presencial</label>
                <input id="eventOnsiteStartAt" type="datetime-local">
              </div>
              <div class="field">
                <label>Fin presencial</label>
                <input id="eventOnsiteEndAt" type="datetime-local">
              </div>
              <div class="field">
                <label>Cierre registro</label>
                <input id="eventRegistrationCloseAt" type="datetime-local">
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-primary" onclick="createAdminEvent()">Crear temporada</button>
            </div>
          </div>

          <div class="card span-6">
            <div class="module-card-title">
              <h2>Operar temporada</h2>
              <span class="screen-chip">Edición</span>
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Temporada seleccionada</label>
                <select id="eventSelector"></select>
              </div>
              <div class="field">
                <label>Nuevo estado</label>
                <select id="eventStatusUpdate">
                  <option value="">Sin cambio</option>
                  <option value="DRAFT">DRAFT</option>
                  <option value="VISIBLE">VISIBLE</option>
                  <option value="ONSITE">ONSITE</option>
                  <option value="CLOSED">CLOSED</option>
                  <option value="ARCHIVED">ARCHIVED</option>
                </select>
              </div>
              <div class="field">
                <label>Visible para alumnos</label>
                <select id="eventVisibleUpdate">
                  <option value="">Sin cambio</option>
                  <option value="true">Sí</option>
                  <option value="false">No</option>
                </select>
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-primary" onclick="updateSelectedEvent()">Guardar cambios</button>
              <button type="button" class="btn-secondary" onclick="setSelectedEventVisible()">Marcar visible</button>
            </div>

            <div id="selectedEventInfo" class="record-grid"></div>
          </div>

          <div class="card span-12">
            <div class="module-card-title">
              <h2>Temporadas existentes</h2>
              <span class="screen-chip">Historial</span>
            </div>
            <div id="eventsList" class="record-grid"></div>
          </div>
        </div>
      </div>

      <div class="module" id="masterProjectsModule">
        <div class="module-grid">
          <div class="card span-12">
            <div class="module-card-title">
              <h2>Crear proyecto base</h2>
              <span class="screen-chip">Catálogo maestro</span>
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Nombre general / organización</label>
                <input id="mp_general_name" placeholder="Ej: Adidas, Tigres, Nike">
              </div>
              <div class="field">
                <label>Nombre del proyecto</label>
                <input id="mp_name" placeholder="Ej: Análisis del equipo">
              </div>
              <div class="field">
                <label>Carrera preferida</label>
                <select id="mp_partner"></select>
              </div>
              <div class="field">
                <label>Modalidad</label>
                <select id="mp_modality"></select>
              </div>
              <div class="field">
                <label>Días</label>
                <select id="mp_week_days"></select>
              </div>
              <div class="field">
                <label>Horario</label>
                <select id="mp_schedule"></select>
              </div>
              <div class="field">
                <label>Cupo base</label>
                <input id="mp_slots" type="number" min="0" placeholder="Ej: 2">
              </div>
              <div class="field">
                <label>Detalle de horario</label>
                <input id="mp_schedule_description" placeholder="Ej: 10:00 a 18:00">
              </div>
              <div class="field">
                <label>Responsables</label>
                <input id="mp_team_owners" placeholder="Ej: Equipo de análisis">
              </div>
              <div class="field">
                <label>Duración</label>
                <input id="mp_duration" placeholder="Ej: 5 semanas">
              </div>
              <div class="field">
                <label>Población</label>
                <input id="mp_audience" placeholder="Ej: Jóvenes">
              </div>
              <div class="field">
                <label>Horas máximas</label>
                <input id="mp_max_hours" type="number" min="0" placeholder="Ej: 100">
              </div>
              <div class="field">
                <label>Lugar de trabajo</label>
                <input id="mp_location" placeholder="Dirección o lugar">
              </div>
              <div class="field">
                <label>Clave externa</label>
                <input id="mp_clave" placeholder="Clave usada fuera del evento">
              </div>
              <div class="field">
                <label>Competencias</label>
                <input id="mp_competencies" placeholder="Ej: creatividad, análisis">
              </div>
            </div>

            <div class="field" style="margin-top:12px;">
              <label>Objetivos</label>
              <textarea id="mp_objectives"></textarea>
            </div>

            <div class="field" style="margin-top:12px;">
              <label>Actividades</label>
              <textarea id="mp_activities"></textarea>
            </div>

            <div class="field" style="margin-top:12px;">
              <label>Comentarios</label>
              <textarea id="mp_comments"></textarea>
            </div>

            <div class="actions">
              <button type="button" class="btn-primary" onclick="createMasterProject()">Crear proyecto base</button>
              <button type="button" class="btn-secondary" onclick="loadMasterProjects()">Recargar lista</button>
            </div>
          </div>

          <div class="card span-12">
            <div class="module-card-title">
              <h2>Catálogo de proyectos base</h2>
              <span class="screen-chip">Consulta</span>
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Buscar proyecto base</label>
                <input id="masterProjectsSearch" placeholder="Buscar..." oninput="loadMasterProjects()">
              </div>
            </div>

            <div id="masterProjectsList" class="record-grid"></div>
          </div>
        </div>
      </div>

      <div class="module" id="eventProjectsModule">
        <div class="module-grid">
          <div class="card span-12">
            <div class="module-card-title">
              <h2>Activar proyecto en temporada</h2>
              <span class="screen-chip">Operación</span>
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Temporada</label>
                <select id="eventProjectEventSelector"></select>
              </div>
              <div class="field">
                <label>Proyecto base</label>
                <select id="projectSelector"></select>
              </div>
              <div class="field">
                <label>Cupo inicial para esta temporada</label>
                <input id="slotsInput" type="number" min="0" placeholder="Ej: 10">
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-primary" onclick="addProjectToEvent()">Agregar a temporada</button>
              <button type="button" class="btn-secondary" onclick="loadEventProjects()">Actualizar lista</button>
            </div>

            <div class="module-card-title" style="margin-top:18px;">
              <h2>Administrar proyectos activos</h2>
              <span class="screen-chip">Edición y operación</span>
            </div>

            <div class="muted" style="margin-bottom:8px;">
              Aquí puedes cambiar el cupo de cada proyecto activo, revisar sus tokens y actualizar su estado.
            </div>

            <div id="eventProjectsList" class="record-grid"></div>
          </div>
        </div>
      </div>

      <div class="module" id="tokensModule">
        <div class="module-grid">
          <div class="card span-6">
            <div class="module-card-title">
              <h2>Generar tokens</h2>
              <span class="screen-chip">Acceso</span>
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Proyecto en temporada</label>
                <select id="tokensEventProjectSelector"></select>
              </div>
              <div class="field">
                <label>Cantidad</label>
                <input id="tokensCount" type="number" min="1" max="200" value="5">
              </div>
              <div class="field">
                <label>Longitud</label>
                <input id="tokensLength" type="number" min="6" max="20" value="8">
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-primary" onclick="generateProjectTokens()">Generar tokens</button>
            </div>

            <div id="tokensGenerationResult" class="record-grid"></div>
          </div>

          <div class="card span-6">
            <div class="module-card-title">
              <h2>Revocar token</h2>
              <span class="screen-chip">Acción crítica</span>
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Token</label>
                <input id="revokeTokenValue" placeholder="Ej: A7K9P3Q2">
              </div>
              <div class="field">
                <label>Motivo</label>
                <input id="revokeTokenReason" placeholder="Ej: Error del líder">
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-danger" onclick="revokeProjectToken()">Revocar token</button>
            </div>
          </div>

          <div class="card span-12">
            <div class="module-card-title">
              <h2>Tokens del proyecto</h2>
              <span class="screen-chip">Seguimiento</span>
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Estado</label>
                <select id="tokensStatusFilter" onchange="loadProjectTokens()">
                  <option value="ALL">Todos</option>
                  <option value="AVAILABLE">AVAILABLE</option>
                  <option value="RESERVED">RESERVED</option>
                  <option value="USED">USED</option>
                  <option value="REVOKED">REVOKED</option>
                  <option value="EXPIRED">EXPIRED</option>
                </select>
              </div>
            </div>

            <div id="tokensSummary" class="stats-grid"></div>
            <div id="tokensCards" class="record-grid"></div>
          </div>
        </div>
      </div>

      <div class="module" id="registrationsModule">
        <div class="module-grid">
          <div class="card span-12">
            <div class="module-card-title">
              <h2>Inscritos</h2>
              <span class="screen-chip">Cierre final</span>
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Temporada</label>
                <select id="registrationsEventSelector"></select>
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-primary" onclick="loadRegistrations()">Cargar inscripciones</button>
            </div>

            <div id="registrationsCards" class="record-grid"></div>
          </div>
        </div>
      </div>

      <div class="module" id="checkinModule">
        <div class="module-grid">
          <div class="card span-12">
            <div class="module-card-title">
              <h2>Check-in (QR)</h2>
              <span class="screen-chip">Acceso presencial</span>
            </div>
            <div class="center-note">
              Escanea el QR, valida matrícula y habilita acceso.
            </div>

            <div class="form-grid" style="margin-top:18px;">
              <div class="field">
                <label>QR escaneado</label>
                <input id="staffScannedToken" placeholder="Aquí aparece el token escaneado o puedes pegarlo">
              </div>
              <div class="field">
                <label>Matrícula física presentada</label>
                <input id="staffPhysicalEnrolment" placeholder="Ej: A01234567">
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-primary" onclick="startQrScanner()">Abrir cámara</button>
              <button type="button" class="btn-secondary" onclick="stopQrScanner()">Detener cámara</button>
              <button type="button" class="btn-secondary" onclick="scanStaffQr()">Verificar QR</button>
              <button type="button" class="btn-primary" onclick="grantStaffAccess()">Dar acceso</button>
            </div>

            <div class="scanner-shell">
              <div id="staffScanner"></div>
            </div>

            <div id="staffCheckinInfo" class="record-grid"></div>
          </div>
        </div>
      </div>

      <div class="module" id="incidentsModule">
        <div class="module-grid">
          <div class="card span-6">
            <div class="module-card-title">
              <h2>Crear incidente</h2>
              <span class="screen-chip">Control crítico</span>
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Event ID</label>
                <input id="incidentEventId" placeholder="Se llena con la temporada seleccionada">
              </div>
              <div class="field">
                <label>Request ID (opcional)</label>
                <input id="incidentRequestId" placeholder="ID de solicitud">
              </div>
              <div class="field">
                <label>User ID (opcional)</label>
                <input id="incidentUserId" placeholder="ID de usuario">
              </div>
              <div class="field">
                <label>Tipo</label>
                <select id="incidentType">
                  <option value="ID_NO_COINCIDE">ID_NO_COINCIDE</option>
                  <option value="FOLIO_NO_ENCONTRADO">FOLIO_NO_ENCONTRADO</option>
                  <option value="QR_INVALIDO">QR_INVALIDO</option>
                  <option value="QR_EXPIRADO">QR_EXPIRADO</option>
                  <option value="DATOS_INCORRECTOS">DATOS_INCORRECTOS</option>
                  <option value="ALUMNO_YA_VALIDADO">ALUMNO_YA_VALIDADO</option>
                  <option value="ALUMNO_YA_REGISTRADO">ALUMNO_YA_REGISTRADO</option>
                  <option value="TOKEN_INVALIDO">TOKEN_INVALIDO</option>
                  <option value="TOKEN_YA_USADO">TOKEN_YA_USADO</option>
                  <option value="TOKEN_REVOCADO">TOKEN_REVOCADO</option>
                  <option value="TOKEN_EXPIRADO">TOKEN_EXPIRADO</option>
                  <option value="PROYECTO_INCORRECTO">PROYECTO_INCORRECTO</option>
                  <option value="PROBLEMA_TECNICO">PROBLEMA_TECNICO</option>
                  <option value="OTRO">OTRO</option>
                </select>
              </div>
              <div class="field">
                <label>Severidad</label>
                <select id="incidentSeverity">
                  <option value="LOW">LOW</option>
                  <option value="MEDIUM" selected>MEDIUM</option>
                  <option value="HIGH">HIGH</option>
                </select>
              </div>
            </div>

            <div class="field" style="margin-top:12px;">
              <label>Descripción</label>
              <textarea id="incidentDescription" placeholder="Describe el caso con claridad"></textarea>
            </div>

            <div class="actions">
              <button type="button" class="btn-primary" onclick="createIncident()">Reportar caso</button>
            </div>
          </div>

          <div class="card span-6">
            <div class="module-card-title">
              <h2>Listado de incidentes</h2>
              <span class="screen-chip">Seguimiento</span>
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Filtrar status</label>
                <select id="incidentFilterStatus" onchange="loadIncidents()">
                  <option value="">Todos</option>
                  <option value="OPEN">OPEN</option>
                  <option value="IN_PROGRESS">IN_PROGRESS</option>
                  <option value="RESOLVED">RESOLVED</option>
                  <option value="DISMISSED">DISMISSED</option>
                </select>
              </div>
              <div class="field">
                <label>Filtrar severidad</label>
                <select id="incidentFilterSeverity" onchange="loadIncidents()">
                  <option value="">Todas</option>
                  <option value="LOW">LOW</option>
                  <option value="MEDIUM">MEDIUM</option>
                  <option value="HIGH">HIGH</option>
                </select>
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-secondary" onclick="loadIncidents()">Recargar incidentes</button>
            </div>

            <div id="incidentsList" class="record-grid"></div>
          </div>
        </div>
      </div>

      <div class="module" id="staffModule">
        <div class="module-grid">
          <div class="card span-6">
            <div class="module-card-title">
              <h2>Crear staff</h2>
              <span class="screen-chip">Gestión de cuentas</span>
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Nombre completo</label>
                <input id="staffFullName" placeholder="Ej: Laura Torres">
              </div>
              <div class="field">
                <label>Correo</label>
                <input id="staffEmail" type="email" placeholder="laura@evento.com">
              </div>
              <div class="field">
                <label>Contraseña</label>
                <input id="staffPassword" type="password" placeholder="Mínimo 8 caracteres">
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-primary" onclick="createStaff()">Crear staff</button>
            </div>
          </div>

          <div class="card span-6">
            <div class="module-card-title">
              <h2>Listado de staff</h2>
              <span class="screen-chip">Seguimiento</span>
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Filtrar status</label>
                <select id="staffStatusFilter" onchange="loadStaff()">
                  <option value="">Todos</option>
                  <option value="ACTIVE">ACTIVE</option>
                  <option value="DISABLED">DISABLED</option>
                </select>
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-secondary" onclick="loadStaff()">Recargar staff</button>
            </div>

            <div id="staffList" class="record-grid"></div>
          </div>
        </div>
      </div>

      <div class="module" id="evidenceModule">
        <div class="module-grid">
          <div class="card span-4">
            <div class="module-card-title">
              <h2>Evidencia legal</h2>
              <span class="screen-chip">Verificación</span>
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Matrícula</label>
                <input id="evidenceEnrolmentNumber" placeholder="Ej: A01234567">
              </div>
              <div class="field">
                <label>Temporada</label>
                <select id="evidenceEventSelector"></select>
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-primary" onclick="loadEvidenceByEnrolment()">Ver evidencia</button>
            </div>
          </div>

          <div class="card span-8">
            <div class="module-card-title">
              <h2>Detalle técnico / legal</h2>
              <span class="screen-chip">Integridad</span>
            </div>

            <div id="evidenceResult" class="evidence-box">
              <div class="record-card">
                <div class="record-card__title">Sin consulta</div>
                <div class="record-card__sub">
                  Ingresa matrícula y temporada para ver fingerprint, hash, firma y snapshot.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div> 

      <div class="module" id="importExportModule">
        <div class="module-grid">
          <div class="card span-12">
            <div class="module-card-title">
              <h2>Carga Masiva (Import / Export)</h2>
              <span class="screen-chip">Control de catálogo</span>
            </div>
            <div class="muted">
              Importa proyectos base desde Excel o exporta el catálogo actual.
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Archivo Excel (.xlsx)</label>
                <input id="importProjectsFile" type="file" accept=".xlsx">
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-primary" onclick="importProjects()">Importar proyectos</button>
              <button type="button" class="btn-secondary" onclick="exportProjects()">Exportar proyectos</button>
            </div>

            <div id="importProjectsResult" class="record-grid"></div>
          </div>
        </div>
      </div>

      <div class="module" id="exportModule">
        <div class="module-grid">
          <div class="card span-12">
            <div class="module-card-title">
              <h2>Exportación por temporada</h2>
              <span class="screen-chip">Reporte completo</span>
            </div>
            <div class="muted">
              Descarga el reporte completo de la temporada seleccionada: resumen, proyectos, inscritos, tokens, incidentes y evidencia legal.
            </div>

            <div class="form-grid">
              <div class="field">
                <label>Temporada</label>
                <select id="exportEventSelector"></select>
              </div>
            </div>

            <div class="actions">
              <button type="button" class="btn-primary" onclick="exportEventReport()">Exportar reporte completo</button>
            </div>
            <div id="exportHint" class="record-grid"></div>
          </div>
        </div>
      </div>
    </main>
  </div>

  <script>
  let staffQrScanner = null;
  let lastScannedPassSession = null;
  let currentUser = null;
  let allEvents = [];
  let masterProjectsCache = [];
  let eventProjectsCache = [];
  let studentSupportCache = [];
  let selectedStudentSupport = null;
  let studentSupportSearchTimer = null;
  let studentSupportActiveFilter = 'ALL';

  function clearStudentSupportSearch() {
    const q = document.getElementById('studentSupportSearch');
    if (q) q.value = '';

    studentSupportCache = [];
    selectedStudentSupport = null;
    studentSupportActiveFilter = 'ALL';
    clearStudentSupportForm();
    renderStudentSupportDetail(null);

    const results = document.getElementById('studentSupportResults');
    const detail = document.getElementById('studentSupportDetail');
    const summary = document.getElementById('studentSupportSummary');
    const hint = document.getElementById('studentSupportSelectedHint');

    if (results) {
      results.innerHTML = renderEmptyCard(
        'Sin búsqueda',
        'Escribe matrícula, folio, nombre o correo.'
      );
    }

    if (summary) {
      summary.innerHTML = "";
    }

    if (detail) {
      detail.innerHTML = renderEmptyCard(
        'Sin selección',
        'Selecciona un alumno para ver detalle y operar.'
      );
    }

    if (hint) {
      hint.textContent = 'Selecciona un alumno desde los resultados.';
    }

    clearStudentSupportForm();
  }

  function clearStudentSupportForm() {
    [
      'ss_user_id',
      'ss_request_id',
      'ss_first_name',
      'ss_second_name',
      'ss_p_last_name',
      'ss_m_last_name',
      'ss_email',
      'ss_secondary_email',
      'ss_phone_number',
      'ss_enrolment_number',
      'ss_degree',
      'ss_semester'
    ].forEach(id => {
      const el = document.getElementById(id);
      if (el) el.value = '';
    });
  }

  function getStudentSupportPriority(item) {
    const requestStatus = String(item?.request_status || '').toUpperCase();
    const passStatus = String(item?.active_pass_status || '').toUpperCase();

    if (requestStatus === 'ACCESS_ENABLED') {
      return { cls: 'high', label: 'Cierre pendiente' };
    }

    if (requestStatus === 'VALIDATED') {
      return { cls: 'medium', label: 'Listo para habilitar' };
    }

    if (requestStatus === 'REQUESTED' && !item?.active_pass_session_id) {
      return { cls: 'medium', label: 'Sin pase' };
    }

    if (requestStatus === 'CANCELLED') {
      return { cls: 'medium', label: 'Baja aplicada' };
    }

    if (passStatus === 'REVOKED' || passStatus === 'EXPIRED') {
      return { cls: 'medium', label: 'Pase no vigente' };
    }

    return { cls: 'low', label: 'Estable' };
  }

  function getStudentSupportReason(item) {
    const requestStatus = String(item?.request_status || '').toUpperCase();
    const passStatus = String(item?.active_pass_status || '').toUpperCase();

    if (requestStatus === 'ACCESS_ENABLED') {
      return 'Ya tiene acceso habilitado, pero todavía no concluye la inscripción.';
    }

    if (requestStatus === 'VALIDATED') {
      return 'Ya fue validado presencialmente y conviene revisar la habilitación final.';
    }

    if (requestStatus === 'REQUESTED' && !item?.active_pass_session_id) {
      return 'La solicitud existe, pero aún no tiene pase activo generado.';
    }

    if (requestStatus === 'REQUESTED' && passStatus === 'ACTIVE') {
      return 'Ya tiene pase vigente. El siguiente paso es el check-in presencial.';
    }

    if (requestStatus === 'CANCELLED') {
      return 'La solicitud quedó dada de baja. Solo requiere acción si se reabre el flujo.';
    }

    if (passStatus === 'REVOKED') {
      return 'El pase fue revocado. Puede requerir regeneración o revisión de soporte.';
    }

    if (passStatus === 'EXPIRED') {
      return 'El pase expiró. Probablemente necesite un nuevo flujo presencial.';
    }

    if (requestStatus === 'REGISTERED') {
      return 'El alumno ya cerró correctamente su inscripción.';
    }

    return 'Caso visible para seguimiento general.';
  }

  function sortStudentSupportItems(items) {
    const order = { high: 0, medium: 1, low: 2 };
    return [...(items || [])].sort((a, b) => {
      const pa = getStudentSupportPriority(a);
      const pb = getStudentSupportPriority(b);

      if (order[pa.cls] !== order[pb.cls]) {
        return order[pa.cls] - order[pb.cls];
      }

      const aTime = new Date(
        a?.access_enabled_at || a?.validated_at || a?.requested_at || 0
      ).getTime();

      const bTime = new Date(
        b?.access_enabled_at || b?.validated_at || b?.requested_at || 0
      ).getTime();

      return bTime - aTime;
    });
  }

  function renderStudentSupportSummary(items) {
    const box = document.getElementById('studentSupportSummary');
    if (!box) return;

    const list = items || [];

    const countByRequest = (status) =>
      list.filter(x => String(x?.request_status || '').toUpperCase() === status).length;

    const countByPass = (status) =>
      list.filter(x => String(x?.active_pass_status || '').toUpperCase() === status).length;

    const requested = countByRequest('REQUESTED');
    const validated = countByRequest('VALIDATED');
    const accessEnabled = countByRequest('ACCESS_ENABLED');
    const registered = countByRequest('REGISTERED');
    const cancelled = countByRequest('CANCELLED');
    const activePass = countByPass('ACTIVE');
    const noPass = list.filter(x => !x?.active_pass_session_id).length;

    const active = String(studentSupportActiveFilter || 'ALL').toUpperCase();

    box.innerHTML = list.length ? `
      <div class="support-summary-wrap">
        <div class="support-summary-toolbar">
          <div class="support-summary-title">Resumen operativo rápido</div>
          <div class="support-summary-actions">
            <button
              type="button"
              class="support-filter-chip ${active === 'ALL' ? 'active' : ''}"
              onclick="setStudentSupportFilter('ALL')"
            >
              Ver todos
            </button>
          </div>
        </div>

        <div class="support-summary-grid">
          <div
            class="support-mini-kpi clickable ${active === 'REQUESTED' ? 'active' : ''}"
            onclick="setStudentSupportFilter('REQUESTED')"
          >
            <div class="support-mini-kpi__label">Requested</div>
            <div class="support-mini-kpi__value">${requested}</div>
            <div class="support-mini-kpi__sub">Solicitud creada</div>
          </div>

          <div
            class="support-mini-kpi clickable ${active === 'VALIDATED' ? 'active' : ''}"
            onclick="setStudentSupportFilter('VALIDATED')"
          >
            <div class="support-mini-kpi__label">Validated</div>
            <div class="support-mini-kpi__value">${validated}</div>
            <div class="support-mini-kpi__sub">Listos para habilitar</div>
          </div>

          <div
            class="support-mini-kpi clickable ${active === 'ACCESS_ENABLED' ? 'active' : ''}"
            onclick="setStudentSupportFilter('ACCESS_ENABLED')"
          >
            <div class="support-mini-kpi__label">Access enabled</div>
            <div class="support-mini-kpi__value">${accessEnabled}</div>
            <div class="support-mini-kpi__sub">Pendientes de cierre</div>
          </div>

          <div
            class="support-mini-kpi clickable ${active === 'REGISTERED' ? 'active' : ''}"
            onclick="setStudentSupportFilter('REGISTERED')"
          >
            <div class="support-mini-kpi__label">Registered</div>
            <div class="support-mini-kpi__value">${registered}</div>
            <div class="support-mini-kpi__sub">Ya cerrados</div>
          </div>

          <div
            class="support-mini-kpi clickable ${active === 'CANCELLED' ? 'active' : ''}"
            onclick="setStudentSupportFilter('CANCELLED')"
          >
            <div class="support-mini-kpi__label">Cancelled</div>
            <div class="support-mini-kpi__value">${cancelled}</div>
            <div class="support-mini-kpi__sub">Bajas aplicadas</div>
          </div>

          <div
            class="support-mini-kpi clickable ${active === 'PASS_ACTIVE' ? 'active' : ''}"
            onclick="setStudentSupportFilter('PASS_ACTIVE')"
          >
            <div class="support-mini-kpi__label">Pase activo</div>
            <div class="support-mini-kpi__value">${activePass}</div>
            <div class="support-mini-kpi__sub">Sesión vigente</div>
          </div>

          <div
            class="support-mini-kpi clickable ${active === 'NO_PASS' ? 'active' : ''}"
            onclick="setStudentSupportFilter('NO_PASS')"
          >
            <div class="support-mini-kpi__label">Sin pase</div>
            <div class="support-mini-kpi__value">${noPass}</div>
            <div class="support-mini-kpi__sub">Requieren soporte</div>
          </div>

          <div class="support-mini-kpi">
            <div class="support-mini-kpi__label">Resultados</div>
            <div class="support-mini-kpi__value">${list.length}</div>
            <div class="support-mini-kpi__sub">Total visibles en búsqueda</div>
          </div>
        </div>
      </div>
    ` : '';
  }

  function renderStudentSupportResultCard(item) {
    const priority = getStudentSupportPriority(item);
    const reason = getStudentSupportReason(item);

    return `
      <div class="record-card support-student-card">
        <div class="support-student__top">
          <div>
            <div class="support-student__name">${escapeHTML(item.full_name || 'Alumno')}</div>
            <div class="support-student__sub">
              ${escapeHTML(item.enrolment_number || '—')} · ${escapeHTML(item.email || '—')}
            </div>
          </div>
          <div style="display:flex; gap:8px; flex-wrap:wrap; align-items:center;">
            <span class="support-priority ${priority.cls}">${priority.label}</span>
            ${statusBadge(item.request_status || '—')}
            ${item.active_pass_status ? statusBadge(item.active_pass_status) : '<span class="badge badge-neutral">SIN PASE</span>'}
          </div>
        </div>

        <div class="support-student__reason">${escapeHTML(reason)}</div>

        <div class="support-student__metrics">
          <div class="support-metric">
            <span class="support-metric__label">Folio</span>
            <div class="support-metric__value">${escapeHTML(item.folio || '—')}</div>
          </div>
          <div class="support-metric">
            <span class="support-metric__label">Temporada</span>
            <div class="support-metric__value">${escapeHTML(item.display_name || '—')}</div>
          </div>
          <div class="support-metric">
            <span class="support-metric__label">Carrera</span>
            <div class="support-metric__value">${escapeHTML(item.degree || '—')}</div>
          </div>
          <div class="support-metric">
            <span class="support-metric__label">Pase actual</span>
            <div class="support-metric__value">${escapeHTML(item.active_pass_expires_at || 'Sin sesión')}</div>
          </div>
        </div>

        <div class="actions">
          <button type="button" class="btn-primary" onclick="selectStudentSupport(${Number(item.request_id)})">
            Seleccionar
          </button>
        </div>
      </div>
    `;
  }

  function getFilteredStudentSupportItems(items, filter) {
    const list = items || [];
    const current = String(filter || 'ALL').toUpperCase();

    if (current === 'ALL') return list;

    if (current === 'NO_PASS') {
      return list.filter(x => !x?.active_pass_session_id);
    }

    if (current === 'PASS_ACTIVE') {
      return list.filter(x => String(x?.active_pass_status || '').toUpperCase() === 'ACTIVE');
    }

    return list.filter(x => String(x?.request_status || '').toUpperCase() === current);
  }

  function setStudentSupportFilter(filter) {
    studentSupportActiveFilter = String(filter || 'ALL').toUpperCase();
    rerenderStudentSupportResults();
  }

  function rerenderStudentSupportResults() {
    const results = document.getElementById('studentSupportResults');
    const summary = document.getElementById('studentSupportSummary');

    if (!results) return;

    const base = studentSupportCache || [];
    const filtered = getFilteredStudentSupportItems(base, studentSupportActiveFilter);

    renderStudentSupportSummary(base);

    if (!filtered.length) {
      results.innerHTML = renderEmptyCard(
        'Sin resultados para este filtro',
        'Prueba otro filtro o vuelve a “Ver todos”.'
      );
      return;
    }

    results.innerHTML = filtered.map(item => renderStudentSupportResultCard(item)).join('');
  }

  function fillStudentSupportForm(item) {
    if (!item) {
      clearStudentSupportForm();
      return;
    }

    document.getElementById('ss_user_id').value = item.user_id || '';
    document.getElementById('ss_request_id').value = item.request_id || '';
    document.getElementById('ss_first_name').value = item.first_name || '';
    document.getElementById('ss_second_name').value = item.second_name || '';
    document.getElementById('ss_p_last_name').value = item.p_last_name || '';
    document.getElementById('ss_m_last_name').value = item.m_last_name || '';
    document.getElementById('ss_email').value = item.email || '';
    document.getElementById('ss_secondary_email').value = item.secondary_email || '';
    document.getElementById('ss_phone_number').value = item.phone_number || '';
    document.getElementById('ss_enrolment_number').value = item.enrolment_number || '';
    document.getElementById('ss_degree').value = item.degree || '';
    document.getElementById('ss_semester').value = item.semester || '';
  }

  function renderStudentSupportDetail(item, passSessions = null) {
    const detail = document.getElementById('studentSupportDetail');
    const hint = document.getElementById('studentSupportSelectedHint');
    if (!detail) return;

    if (!item) {
      detail.innerHTML = renderEmptyCard(
        'Sin selección',
        'Selecciona un alumno para ver detalle y operar.'
      );
      if (hint) hint.textContent = 'Selecciona un alumno desde los resultados.';
      return;
    }

    if (hint) {
      hint.textContent = `Seleccionado: ${item.full_name || 'Alumno'} · ${item.enrolment_number || '—'}`;
    }

    const passesHtml = Array.isArray(passSessions) && passSessions.length
      ? passSessions.map(ps => `
          <div class="record-card">
            <div class="record-card__head">
              <div>
                <div class="record-card__title">Pass Session #${ps.id}</div>
                <div class="record-card__sub">Refresh count: ${ps.refresh_count ?? 0}</div>
              </div>
              <div>${statusBadge(ps.status)}</div>
            </div>
            <div class="record-stack">
              <div class="stack-row"><strong>Issued:</strong><span>${escapeHTML(ps.issued_at || '—')}</span></div>
              <div class="stack-row"><strong>Expires:</strong><span>${escapeHTML(ps.expires_at || '—')}</span></div>
              <div class="stack-row"><strong>Used:</strong><span>${escapeHTML(ps.used_at || '—')}</span></div>
              <div class="stack-row"><strong>Revoked:</strong><span>${escapeHTML(ps.revoked_at || '—')}</span></div>
            </div>
          </div>
        `).join('')
      : (
          item.active_pass_session_id
            ? `
              <div class="record-card">
                <div class="record-card__head">
                  <div>
                    <div class="record-card__title">Pase actual</div>
                    <div class="record-card__sub">Pass Session #${item.active_pass_session_id}</div>
                  </div>
                  <div>${statusBadge(item.active_pass_status || '—')}</div>
                </div>
                <div class="record-stack">
                  <div class="stack-row"><strong>Issued:</strong><span>${escapeHTML(item.active_pass_issued_at || '—')}</span></div>
                  <div class="stack-row"><strong>Expires:</strong><span>${escapeHTML(item.active_pass_expires_at || '—')}</span></div>
                  <div class="stack-row"><strong>Used:</strong><span>${escapeHTML(item.active_pass_used_at || '—')}</span></div>
                  <div class="stack-row"><strong>Revoked:</strong><span>${escapeHTML(item.active_pass_revoked_at || '—')}</span></div>
                  <div class="stack-row"><strong>Refresh count:</strong><span>${escapeHTML(item.active_pass_refresh_count || 0)}</span></div>
                </div>
              </div>
            `
            : renderEmptyCard(
                'Sin pase registrado',
                'Este alumno no tiene sesiones de pase todavía.'
              )
        );

    detail.innerHTML = `
      <div class="record-card">
        <div class="record-card__head">
          <div>
            <div class="record-card__title">${escapeHTML(item.full_name || 'Alumno')}</div>
            <div class="record-card__sub">${escapeHTML(item.email || '—')}</div>
          </div>
          <div style="display:flex; gap:8px; flex-wrap:wrap;">
            ${statusBadge(item.request_status || '—')}
            ${statusBadge(item.event_status || '—')}
          </div>
        </div>
        <div class="record-stack">
          <div class="stack-row"><strong>User ID:</strong><span>${escapeHTML(item.user_id || '—')}</span></div>
          <div class="stack-row"><strong>Request ID:</strong><span>${escapeHTML(item.request_id || '—')}</span></div>
          <div class="stack-row"><strong>Folio:</strong><span>${escapeHTML(item.folio || '—')}</span></div>
          <div class="stack-row"><strong>Matrícula:</strong><span>${escapeHTML(item.enrolment_number || '—')}</span></div>
          <div class="stack-row"><strong>Teléfono:</strong><span>${escapeHTML(item.phone_number || '—')}</span></div>
          <div class="stack-row"><strong>Carrera:</strong><span>${escapeHTML(item.degree || '—')}</span></div>
          <div class="stack-row"><strong>Semestre:</strong><span>${escapeHTML(item.semester || '—')}</span></div>
          <div class="stack-row"><strong>Temporada:</strong><span>${escapeHTML(item.display_name || '—')}</span></div>
          <div class="stack-row"><strong>Requested:</strong><span>${escapeHTML(item.requested_at || '—')}</span></div>
          <div class="stack-row"><strong>Validated:</strong><span>${escapeHTML(item.validated_at || '—')}</span></div>
          <div class="stack-row"><strong>Access enabled:</strong><span>${escapeHTML(item.access_enabled_at || '—')}</span></div>
          <div class="stack-row"><strong>Registered:</strong><span>${escapeHTML(item.registered_at || '—')}</span></div>
          <div class="stack-row"><strong>Cancelled:</strong><span>${escapeHTML(item.cancelled_at || '—')}</span></div>
          <div class="stack-row"><strong>Closed:</strong><span>${escapeHTML(item.closed_at || '—')}</span></div>
          <div class="stack-row"><strong>Notas:</strong><span>${escapeHTML(item.notes || '—')}</span></div>
        </div>
      </div>
      ${passesHtml}
    `;
  }

  function scheduleStudentSupportSearch() {
    clearTimeout(studentSupportSearchTimer);
    studentSupportSearchTimer = setTimeout(() => {
      searchStudentSupport();
    }, 250);
  }

  async function searchStudentSupport() {
    const q = (document.getElementById('studentSupportSearch')?.value || '').trim();
    const eventId = document.getElementById('studentSupportEventSelector')?.value;
    const results = document.getElementById('studentSupportResults');
    const summary = document.getElementById('studentSupportSummary');
    if (!results) return;

    if (!q && !eventId) {
      return showMsg('Escribe algo para buscar o selecciona una temporada', false);
    }

    try {
      results.innerHTML = renderEmptyCard('Buscando...', 'Consultando alumnos y solicitudes...');

      const params = new URLSearchParams();
      if (q) params.set('q', q);
      if (eventId) params.set('event_id', eventId);

      const data = await apiGet(`/api/admin/student-support/search?${params.toString()}`);
      const items = sortStudentSupportItems(data.items || []);
      studentSupportCache = items;
      selectedStudentSupport = null;
      studentSupportActiveFilter = 'ALL';
      clearStudentSupportForm();
      renderStudentSupportDetail(null);

      if (!items.length) {
        if (summary) summary.innerHTML = '';
        results.innerHTML = renderEmptyCard(
          'Sin resultados',
          'No encontramos alumnos o solicitudes con esa búsqueda.'
        );
        return showMsg('No se encontraron resultados', false);
      }

      renderStudentSupportSummary(items);
      rerenderStudentSupportResults();

      showMsg('Resultados cargados correctamente');
    } catch (e) {
      results.innerHTML = renderEmptyCard('No se pudo buscar', e.message || 'Error inesperado');
      showMsg(e.message, false);
    }
  }

  async function selectStudentSupport(requestId) {
    try {
      const data = await apiGet(`/api/admin/student-support/request/${requestId}`);
      const requestRow = data.request || null;
      const passSessions = data.pass_sessions || [];

      if (!requestRow) {
        return showMsg('No se pudo cargar el detalle de la solicitud', false);
      }

      selectedStudentSupport = {
        ...requestRow,
        active_pass_session_id: passSessions[0]?.id || null,
        active_pass_status: passSessions[0]?.status || null,
        active_pass_issued_at: passSessions[0]?.issued_at || null,
        active_pass_expires_at: passSessions[0]?.expires_at || null,
        active_pass_used_at: passSessions[0]?.used_at || null,
        active_pass_revoked_at: passSessions[0]?.revoked_at || null,
        active_pass_refresh_count: passSessions[0]?.refresh_count || null
      };

      fillStudentSupportForm(selectedStudentSupport);
      renderStudentSupportDetail(selectedStudentSupport, passSessions);
      showMsg('Detalle cargado correctamente');
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  async function reloadSelectedStudentSupport() {
    const requestId = document.getElementById('ss_request_id')?.value;
    if (!requestId) return showMsg('No hay solicitud seleccionada', false);
    await selectStudentSupport(Number(requestId));
  }

  async function saveStudentSupportUser() {
    try {
      const userId = Number(document.getElementById('ss_user_id')?.value || 0);
      if (!userId) return showMsg('No hay alumno seleccionado', false);

      const payload = {
        first_name: document.getElementById('ss_first_name')?.value.trim(),
        second_name: document.getElementById('ss_second_name')?.value.trim(),
        p_last_name: document.getElementById('ss_p_last_name')?.value.trim(),
        m_last_name: document.getElementById('ss_m_last_name')?.value.trim(),
        email: document.getElementById('ss_email')?.value.trim().toLowerCase(),
        secondary_email: document.getElementById('ss_secondary_email')?.value.trim().toLowerCase(),
        phone_number: document.getElementById('ss_phone_number')?.value.trim(),
        enrolment_number: document.getElementById('ss_enrolment_number')?.value.trim().toLowerCase(),
        degree: document.getElementById('ss_degree')?.value.trim(),
        semester: document.getElementById('ss_semester')?.value.trim()
      };

      const data = await apiPatch(`/api/admin/student-support/users/${userId}`, payload);
      showMsg(data.message || 'Alumno actualizado correctamente');

      const requestId = Number(document.getElementById('ss_request_id')?.value || 0);
      if (requestId) await selectStudentSupport(requestId);

      const q = (document.getElementById('studentSupportSearch')?.value || '').trim();
      const eventId = document.getElementById('studentSupportEventSelector')?.value;
      if (q || eventId) await searchStudentSupport();
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  async function reissueSelectedStudentPass() {
    try {
      const requestId = Number(document.getElementById('ss_request_id')?.value || 0);
      if (!requestId) return showMsg('No hay solicitud seleccionada', false);

      const data = await apiPost(`/api/admin/student-support/request/${requestId}/reissue-pass`, {});
      showMsg(data.message || 'Nuevo pase generado');

      const detail = document.getElementById('studentSupportDetail');
      if (detail && data.pass_session?.plain_token) {
        detail.insertAdjacentHTML('afterbegin', `
          <div class="record-card">
            <div class="record-card__title">Nuevo pase generado</div>
            <div class="record-card__sub">Comparte este token QR con el alumno solo si lo necesitas para soporte inmediato.</div>
            <div style="margin-top:10px;"><span class="mono">${escapeHTML(data.pass_session.plain_token)}</span></div>
            <div class="small" style="margin-top:8px;">Expira: ${escapeHTML(data.pass_session.expires_at || '—')}</div>
          </div>
        `);
      }

      await selectStudentSupport(requestId);
      await searchStudentSupport();
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  async function revokeSelectedStudentPass() {
    try {
      const passSessionId = Number(selectedStudentSupport?.active_pass_session_id || 0);
      const requestId = Number(document.getElementById('ss_request_id')?.value || 0);

      if (!passSessionId) return showMsg('No hay pase activo para revocar', false);
      if (!requestId) return showMsg('No hay solicitud seleccionada', false);

      const data = await apiPost(`/api/admin/student-support/pass/${passSessionId}/revoke`, {});
      showMsg(data.message || 'Pase revocado correctamente');

      await selectStudentSupport(requestId);
      await searchStudentSupport();
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  async function enableSelectedStudentAccess() {
    try {
      const requestId = Number(document.getElementById('ss_request_id')?.value || 0);
      if (!requestId) return showMsg('No hay solicitud seleccionada', false);

      const data = await apiPost(`/api/admin/student-support/request/${requestId}/enable-access`, {});
      showMsg(data.message || 'Acceso habilitado manualmente');

      await selectStudentSupport(requestId);
      await searchStudentSupport();
      await loadDashboard();
    } catch (e) {
      showMsg(e.message, false);
    }
  }



  const MODULE_META = {
    summaryModule: { title: 'Dashboard', subtitle: 'Visión ejecutiva del evento.', kicker: 'Estrategia', accent: '#7D5BA6', accentSoft: '#F5F0FB' },
    eventsModule: { title: 'Temporadas', subtitle: 'Configuración de ciclos y ventanas operativas.', kicker: 'Estrategia', accent: '#7D5BA6', accentSoft: '#F5F0FB' },
    masterProjectsModule: { title: 'Proyectos Base', subtitle: 'Catálogo maestro de proyectos.', kicker: 'Estrategia', accent: '#7D5BA6', accentSoft: '#F5F0FB' },
    eventProjectsModule: { title: 'Proyectos Activos', subtitle: 'Activación de proyectos por temporada.', kicker: 'Operación', accent: '#FF8C42', accentSoft: '#FFF3EA' },
    tokensModule: { title: 'Tokens', subtitle: 'Generación, consulta y revocación.', kicker: 'Operación', accent: '#FF8C42', accentSoft: '#FFF3EA' },
    registrationsModule: { title: 'Inscritos', subtitle: 'Consulta de cierres de inscripción.', kicker: 'Operación', accent: '#43AA8B', accentSoft: '#ECFDF7' },
    checkinModule: { title: 'Check-in (QR)', subtitle: 'Escaneo y habilitación de acceso.', kicker: 'Operación', accent: '#43AA8B', accentSoft: '#ECFDF7' },
    incidentsModule: { title: 'Incidentes', subtitle: 'Seguimiento de problemas y casos especiales.', kicker: 'Control', accent: '#F25C78', accentSoft: '#FFF1F5' },
    staffModule: { title: 'Staff', subtitle: 'Gestión de cuentas operativas.', kicker: 'Control', accent: '#3B82F6', accentSoft: '#EFF6FF' },
    evidenceModule: { title: 'Evidencia Legal', subtitle: 'Hash, firma y snapshot del registro.', kicker: 'Control', accent: '#3B82F6', accentSoft: '#EFF6FF' },
    importExportModule: { title: 'Carga Masiva', subtitle: 'Importación y exportación del catálogo.', kicker: 'Control', accent: '#F25C78', accentSoft: '#FFF1F5' },
    exportModule: { title: 'Exportación', subtitle: 'Reporte completo por temporada.', kicker: 'Control', accent: '#3B82F6', accentSoft: '#EFF6FF' },
    studentSupportModule: { title: 'Solicitudes y Pases', subtitle: 'Corrección de alumnos, revisión de solicitudes y operación de pases.', kicker: 'Operación', accent: '#43AA8B', accentSoft: '#ECFDF7'}
  };

  function escapeHTML(value) {
    return String(value ?? '')
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  function prettyJSON(value) {
    try {
      if (typeof value === 'string') return JSON.stringify(JSON.parse(value), null, 2);
      return JSON.stringify(value ?? {}, null, 2);
    } catch {
      return String(value ?? '');
    }
  }

  function showMsg(text, ok = true, login = false) {
    const target = login ? document.getElementById('msgLogin') : document.getElementById('msgApp');
    if (!target) return;
    target.textContent = text || '';
    target.className = 'msg ' + (ok ? 'ok' : 'err');
  }

  function clearLoginFields() {
    const email = document.getElementById('loginEmail');
    const password = document.getElementById('loginPassword');
    if (email) email.value = '';
    if (password) password.value = '';
  }

  function setModuleAccent(accent, accentSoft) {
    document.documentElement.style.setProperty('--module-accent', accent);
    document.documentElement.style.setProperty('--module-accent-soft', accentSoft);
  }

  function showModule(moduleId) {
    document.querySelectorAll('.module').forEach(m => m.classList.remove('active'));
    document.getElementById(moduleId)?.classList.add('active');

    document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
    document.querySelectorAll(`.nav-item[data-module="${moduleId}"]`).forEach(x => x.classList.add('active'));

    const meta = MODULE_META[moduleId] || MODULE_META.summaryModule;
    document.getElementById('moduleTitle').textContent = meta.title;
    document.getElementById('moduleSubtitle').textContent = meta.subtitle;
    document.getElementById('moduleKicker').textContent = meta.kicker;
    document.getElementById('headerAccentBadge').textContent = meta.title;

    setModuleAccent(meta.accent, meta.accentSoft);
  }

  function applyRoleUI(user) {
    currentUser = user || null;
    const role = user?.role || '';

    const loginHint = document.getElementById('loginHint');
    const sidebarRoleBox = document.getElementById('sidebarRoleBox');
    const headerRoleBadge = document.getElementById('headerRoleBadge');

    if (loginHint) loginHint.textContent = role ? `Sesión activa como: ${role}` : 'Sesión actual: no iniciada';
    if (sidebarRoleBox) sidebarRoleBox.textContent = role ? `Rol actual: ${role} · ${user.full_name || user.email || ''}` : 'Rol actual: —';
    if (headerRoleBadge) headerRoleBadge.textContent = role || 'Panel';

    document.getElementById('loginWrap')?.classList.toggle('hidden', !!role);
    document.getElementById('appShell')?.classList.toggle('hidden', !role);

    const adminNavWrap = document.getElementById('adminNavWrap');
    const staffNavWrap = document.getElementById('staffNavWrap');

    if (role === 'ADMIN') {
      adminNavWrap?.classList.remove('hidden');
      staffNavWrap?.classList.add('hidden');
      showModule('summaryModule');
    } else if (role === 'STAFF') {
      adminNavWrap?.classList.add('hidden');
      staffNavWrap?.classList.remove('hidden');
      showModule('checkinModule');
    }
  }

  function boolFromString(v) {
    return String(v).toLowerCase() === 'true';
  }

  function toSqlDateTime(value) {
    if (!value) return null;
    return value.replace('T', ' ') + ':00';
  }

  async function apiGet(url) {
    const r = await fetch(url, { credentials: 'include' });
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(data.error || ('Error ' + r.status));
    return data;
  }

  async function apiPost(url, body) {
    const r = await fetch(url, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body || {})
    });
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(data.error || ('Error ' + r.status));
    return data;
  }

  async function apiPatch(url, body) {
    const r = await fetch(url, {
      method: 'PATCH',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body || {})
    });
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(data.error || ('Error ' + r.status));
    return data;
  }

  async function apiPut(url, body) {
    const r = await fetch(url, {
      method: 'PUT',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body || {})
    });
    const data = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(data.error || ('Error ' + r.status));
    return data;
  }

  async function loginAdmin() {
    try {
      const email = document.getElementById('loginEmail').value.trim().toLowerCase();
      const password = document.getElementById('loginPassword').value;

      if (!email) return showMsg('Escribe tu correo', false, true);
      if (!password) return showMsg('Escribe tu contraseña', false, true);

      const data = await apiPost('/api/admin-auth/login', { email, password });
      showMsg(data.message || 'Login correcto', true, true);
      await bootstrapAdmin();
    } catch (e) {
      showMsg(e.message, false, true);
    }
  }

  async function logoutAdmin() {
    try { await apiPost('/api/admin-auth/logout', {}); } catch (e) {}
    currentUser = null;
    applyRoleUI(null);
    clearLoginFields();
    showMsg('Sesión cerrada', true, true);
  }

  async function fetchSessionUser() {
    try {
      const data = await apiGet('/api/admin-auth/me');
      return data.user || null;
    } catch {
      return null;
    }
  }

  function statusBadge(status) {
    const value = String(status || '').toUpperCase();
    const map = {
      DRAFT: ['badge badge-purple', 'DRAFT'],
      VISIBLE: ['badge badge-purple', 'VISIBLE'],
      ONSITE: ['badge badge-success', 'ONSITE'],
      CLOSED: ['badge badge-warn', 'CLOSED'],
      ARCHIVED: ['badge badge-danger', 'ARCHIVED'],
      ACTIVE: ['badge badge-success', 'ACTIVE'],
      CANCELLED: ['badge badge-danger', 'CANCELLED'],
      HIDDEN: ['badge badge-warn', 'HIDDEN'],
      OPEN: ['badge badge-danger', 'OPEN'],
      IN_PROGRESS: ['badge badge-warn', 'IN_PROGRESS'],
      RESOLVED: ['badge badge-success', 'RESOLVED'],
      DISMISSED: ['badge badge-neutral', 'DISMISSED'],
      AVAILABLE: ['badge badge-success', 'AVAILABLE'],
      RESERVED: ['badge badge-warn', 'RESERVED'],
      USED: ['badge badge-neutral', 'USED'],
      REVOKED: ['badge badge-danger', 'REVOKED'],
      EXPIRED: ['badge badge-danger', 'EXPIRED'],
      DISABLED: ['badge badge-danger', 'DISABLED'],
      ACCESS_ENABLED: ['badge badge-success', 'ACCESS_ENABLED'],
      REGISTERED: ['badge badge-blue', 'REGISTERED'],
      REQUESTED: ['badge badge-warn', 'REQUESTED'],
      VALIDATED: ['badge badge-purple', 'VALIDATED']
    };
    const cfg = map[value] || ['badge badge-neutral', value || '—'];
    return `<span class="${cfg[0]}">${cfg[1]}</span>`;
  }

  function fillSelect(id, items, placeholderText = 'Selecciona', labelFn = null) {
    const el = document.getElementById(id);
    if (!el) return;
    el.innerHTML = `<option value="">${placeholderText}</option>`;
    for (const item of items || []) {
      const opt = document.createElement('option');
      opt.value = item.id;
      opt.textContent = labelFn ? labelFn(item) : (item.name || item.description || item.display_name || item.id);
      el.appendChild(opt);
    }
  }

  function fillSelectNoBlank(id, items, labelFn = null) {
    const el = document.getElementById(id);
    if (!el) return;
    el.innerHTML = '';
    for (const item of items || []) {
      const opt = document.createElement('option');
      opt.value = item.id;
      opt.textContent = labelFn ? labelFn(item) : (item.name || item.description || item.display_name || item.id);
      el.appendChild(opt);
    }
  }

  function ensureSelectsDefault(ids) {
    ids.forEach(id => {
      const el = document.getElementById(id);
      if (el && !el.value && el.options.length > 0) {
        el.selectedIndex = 0;
      }
    });
  }

  function renderXPBar(registrados, slotsTotales) {
    const usados = Number(registrados || 0);
    const total = Number(slotsTotales || 0);
    const porcentaje = total > 0 ? Math.round((usados / total) * 100) : 0;
    const porcentajeSeguro = Math.min(porcentaje, 100);
    const levelUpClass = porcentaje >= 100 ? 'level-up' : '';

    return `
      <div class="xp-wrapper">
        <div class="xp-text">
          <span>Ocupación</span>
          <span>${porcentaje}%</span>
        </div>
        <div class="xp-bar-bg">
          <div class="xp-bar-fill ${levelUpClass}" style="width:${porcentajeSeguro}%"></div>
        </div>
      </div>
    `;
  }
  
  function clampPercent(value) {
    const n = Number(value || 0);
    if (Number.isNaN(n)) return 0;
    return Math.max(0, Math.min(100, Math.round(n)));
  }

  function getDashboardHealthScore(summary, projects) {
    const requests = summary?.requests || {};
    const incidents = summary?.incidents || {};
    const items = Array.isArray(projects) ? projects : [];

    const registered = Number(requests.registered || 0);
    const accessEnabled = Number(requests.access_enabled || 0);
    const openIncidents = Number(incidents.open || 0);

    const totalSlots = items.reduce((acc, p) => acc + Number(p.slots_total || 0), 0);
    const totalRegistered = items.reduce((acc, p) => acc + Number(p.registered_count || 0), 0);
    const occupancy = totalSlots > 0 ? (totalRegistered / totalSlots) * 100 : 0;

    let score = 100;
    score -= Math.min(openIncidents * 8, 32);
    score -= Math.min(accessEnabled * 2, 20);

    if (occupancy < 25) score -= 18;
    else if (occupancy < 50) score -= 10;
    else if (occupancy >= 85) score += 4;

    if (registered === 0 && totalSlots > 0) score -= 15;

    return Math.max(0, Math.min(100, Math.round(score)));
  }

  function getHealthTone(score) {
    if (score >= 80) return { label: 'Salud alta', tone: 'ok' };
    if (score >= 55) return { label: 'Salud media', tone: 'warn' };
    return { label: 'Salud crítica', tone: 'danger' };
  }

  function getProjectPriority(project) {
    const slots = Number(project?.slots_total || 0);
    const registered = Number(project?.registered_count || 0);
    const openSeats = Math.max(0, slots - registered);
    const occupancy = slots > 0 ? (registered / slots) * 100 : 0;
    const status = String(project?.event_project_status || '').toUpperCase();

    if (status !== 'ACTIVE') {
      return { label: 'No activo', cls: 'medium' };
    }
    if (openSeats <= 1 || occupancy >= 90) {
      return { label: 'Alta atención', cls: 'high' };
    }
    if (occupancy >= 60) {
      return { label: 'Seguimiento', cls: 'medium' };
    }
    return { label: 'Estable', cls: 'low' };
  }

  function renderDashboardHealthHero(summary, projects) {
    const requests = summary?.requests || {};
    const incidents = summary?.incidents || {};
    const items = Array.isArray(projects) ? projects : [];

    const score = getDashboardHealthScore(summary, items);
    const tone = getHealthTone(score);

    const totalSlots = items.reduce((acc, p) => acc + Number(p.slots_total || 0), 0);
    const totalRegistered = items.reduce((acc, p) => acc + Number(p.registered_count || 0), 0);
    const occupancy = totalSlots > 0 ? Math.round((totalRegistered / totalSlots) * 100) : 0;

    return `
      <div class="health-hero">
        <div class="health-hero__head">
          <div>
            <div class="health-hero__title">Salud operativa de la temporada</div>
            <div class="health-hero__sub">
              Lectura rápida del evento para saber si todo está fluyendo o si ya requiere intervención.
            </div>
          </div>
          <div class="health-score">
            <div class="health-score__value">${score}</div>
            <div class="health-score__label">${tone.label}</div>
          </div>
        </div>

        <div class="health-bars">
          <div class="health-bar-card">
            <div class="health-bar-card__top">
              <span class="health-bar-card__title">Ocupación total</span>
              <span class="health-bar-card__value">${occupancy}%</span>
            </div>
            <div class="xp-bar-bg">
              <div class="xp-bar-fill ${occupancy >= 100 ? 'level-up' : ''}" style="width:${clampPercent(occupancy)}%"></div>
            </div>
          </div>

          <div class="health-bar-card">
            <div class="health-bar-card__top">
              <span class="health-bar-card__title">Access enabled</span>
              <span class="health-bar-card__value">${requests.access_enabled || 0}</span>
            </div>
            <div class="small">Alumnos ya validados pero que aún no cierran inscripción.</div>
          </div>

          <div class="health-bar-card">
            <div class="health-bar-card__top">
              <span class="health-bar-card__title">Incidentes abiertos</span>
              <span class="health-bar-card__value">${incidents.open || 0}</span>
            </div>
            <div class="small">Casos que siguen activos y pueden frenar la operación.</div>
          </div>

          <div class="health-bar-card">
            <div class="health-bar-card__top">
              <span class="health-bar-card__title">Proyectos activos</span>
              <span class="health-bar-card__value">${items.length}</span>
            </div>
            <div class="small">Proyectos vivos dentro de la temporada seleccionada.</div>
          </div>
        </div>
      </div>
    `;
  }

  function getProjectOccupancy(project) {
    const slots = Number(project?.slots_total || 0);
    const registered = Number(project?.registered_count || 0);
    return slots > 0 ? (registered / slots) * 100 : 0;
  }

  function getProjectInsight(project) {
    const slots = Number(project?.slots_total || 0);
    const registered = Number(project?.registered_count || 0);
    const available = Math.max(0, slots - registered);
    const occupancy = getProjectOccupancy(project);
    const status = String(project?.event_project_status || '').toUpperCase();

    if (status !== 'ACTIVE') return 'Proyecto no activo en este momento.';
    if (slots === 0) return 'Sin cupos configurados.';
    if (occupancy >= 95) return 'Prácticamente lleno. Requiere vigilancia inmediata.';
    if (occupancy >= 80) return 'Muy alta demanda. Conviene monitorear cierres.';
    if (occupancy >= 55) return 'Flujo sano y avance constante.';
    if (registered === 0) return 'Sin registros todavía. Revisar visibilidad o demanda.';
    if (available >= slots * 0.7) return 'Todavía tiene mucho espacio disponible.';
    return 'Avance estable.';
  }

  function sortProjectsForDashboard(projects) {
    const items = Array.isArray(projects) ? [...projects] : [];

    return items.sort((a, b) => {
      const pa = getProjectPriority(a);
      const pb = getProjectPriority(b);

      const order = { high: 0, medium: 1, low: 2 };
      if (order[pa.cls] !== order[pb.cls]) {
        return order[pa.cls] - order[pb.cls];
      }

      const occA = getProjectOccupancy(a);
      const occB = getProjectOccupancy(b);
      if (occA !== occB) return occB - occA;

      const regA = Number(a?.registered_count || 0);
      const regB = Number(b?.registered_count || 0);
      return regB - regA;
    });
  }

  function renderDashboardProjectHighlights(projects) {
    const items = sortProjectsForDashboard(projects);
    if (!items.length) {
      return renderEmptyCard('Sin proyectos', 'No hay proyectos para resumir en esta temporada.');
    }

    const mostSaturated = [...items].sort((a, b) => getProjectOccupancy(b) - getProjectOccupancy(a))[0];
    const mostRegistered = [...items].sort((a, b) => Number(b.registered_count || 0) - Number(a.registered_count || 0))[0];
    const mostOpen = [...items].sort((a, b) => Number(b.cupos_disponibles || 0) - Number(a.cupos_disponibles || 0))[0];

    return `
      <div class="project-highlight-grid">
        <div class="project-highlight-card primary">
          <div class="project-highlight__kicker">Mayor presión</div>
          <div class="project-highlight__title">${escapeHTML(mostSaturated?.project_name || '—')}</div>
          <div class="project-highlight__sub">${escapeHTML(mostSaturated?.partner_name || 'Sin carrera preferida')}</div>
          <div class="project-highlight__value">${Math.round(getProjectOccupancy(mostSaturated))}%</div>
          <div class="project-highlight__meta">Proyecto con mayor ocupación relativa.</div>
        </div>

        <div class="project-highlight-card success">
          <div class="project-highlight__kicker">Más cierres / registros</div>
          <div class="project-highlight__title">${escapeHTML(mostRegistered?.project_name || '—')}</div>
          <div class="project-highlight__sub">${escapeHTML(mostRegistered?.partner_name || 'Sin carrera preferida')}</div>
          <div class="project-highlight__value">${escapeHTML(mostRegistered?.registered_count || 0)}</div>
          <div class="project-highlight__meta">Proyecto que más alumnos ha absorbido.</div>
        </div>

        <div class="project-highlight-card info">
          <div class="project-highlight__kicker">Mayor oportunidad</div>
          <div class="project-highlight__title">${escapeHTML(mostOpen?.project_name || '—')}</div>
          <div class="project-highlight__sub">${escapeHTML(mostOpen?.partner_name || 'Sin carrera preferida')}</div>
          <div class="project-highlight__value">${escapeHTML(mostOpen?.cupos_disponibles || 0)}</div>
          <div class="project-highlight__meta">Proyecto con más espacio disponible.</div>
        </div>
      </div>
    `;
  }

  function renderDashboardProjectCard(project) {
    const priority = getProjectPriority(project);
    const occupancy = Math.round(getProjectOccupancy(project));
    const insight = getProjectInsight(project);

    return `
      <div class="record-card clean-project">
        <div class="clean-project__top">
          <div>
            <div class="clean-project__title">${escapeHTML(project.project_name || '—')}</div>
            <div class="clean-project__sub">${escapeHTML(project.partner_name || 'Sin carrera preferida')}</div>
          </div>
          <div style="display:flex; gap:8px; flex-wrap:wrap; align-items:center;">
            <span class="project-priority ${priority.cls}">${priority.label}</span>
            ${statusBadge(project.event_project_status)}
          </div>
        </div>

        <div class="clean-project__insight">${escapeHTML(insight)}</div>

        <div class="clean-project__metrics">
          <div class="metric-chip">
            <span class="metric-chip__label">Ocupación</span>
            <div class="metric-chip__value">${occupancy}%</div>
          </div>
          <div class="metric-chip">
            <span class="metric-chip__label">Registrados</span>
            <div class="metric-chip__value">${escapeHTML(project.registered_count || 0)}</div>
          </div>
          <div class="metric-chip">
            <span class="metric-chip__label">Disponibles</span>
            <div class="metric-chip__value">${escapeHTML(project.cupos_disponibles || 0)}</div>
          </div>
          <div class="metric-chip">
            <span class="metric-chip__label">Tokens usados</span>
            <div class="metric-chip__value">${escapeHTML(project.tokens_used || 0)}</div>
          </div>
        </div>

        <div style="margin-top:4px;">
          ${renderXPBar(project.registered_count || 0, project.slots_total || 0)}
        </div>
      </div>
    `;
  }

  function openDashboardModule(moduleId) {
    showModule(moduleId);
  }

  function getDashboardCases(summary, projects) {
    const requests = summary?.requests || {};
    const incidents = summary?.incidents || {};
    const items = Array.isArray(projects) ? projects : [];

    const accessEnabled = Number(requests.access_enabled || 0);
    const validated = Number(requests.validated || 0);
    const registered = Number(requests.registered || 0);
    const openIncidents = Number(incidents.open || 0);

    const nearlyFullProjects = items
      .map(p => ({
        ...p,
        occupancy: getProjectOccupancy(p)
      }))
      .filter(p => p.occupancy >= 90)
      .sort((a, b) => b.occupancy - a.occupancy)
      .slice(0, 3);

    const lowTractionProjects = items
      .map(p => ({
        ...p,
        occupancy: getProjectOccupancy(p)
      }))
      .filter(p => Number(p.event_project_status || '') === 0 || true)
      .filter(p => p.occupancy <= 25)
      .sort((a, b) => a.occupancy - b.occupancy)
      .slice(0, 3);

    return [
      {
        priority: openIncidents > 0 ? 'high' : 'low',
        title: 'Incidentes que requieren atención',
        value: openIncidents,
        subtitle: openIncidents > 0
          ? 'Hay casos activos que conviene resolver antes de que contaminen la operación.'
          : 'No hay incidentes abiertos en este momento.',
        ctaLabel: 'Ir a Incidentes',
        ctaAction: "openDashboardModule('incidentsModule')",
        rows: [
          ['Estado', openIncidents > 0 ? 'Atención inmediata' : 'Controlado'],
          ['Módulo', 'Incidentes']
        ]
      },
      {
        priority: accessEnabled > 0 ? 'high' : 'low',
        title: 'Alumnos con acceso habilitado sin cierre',
        value: accessEnabled,
        subtitle: accessEnabled > 0
          ? 'Ya pueden cerrar inscripción, pero siguen sin convertir.'
          : 'No hay alumnos pendientes entre acceso y cierre.',
        ctaLabel: 'Ir a Solicitudes y Pases',
        ctaAction: "openDashboardModule('studentSupportModule')",
        rows: [
          ['Estado', accessEnabled > 0 ? 'Fuga de conversión' : 'Sano'],
          ['Módulo', 'Solicitudes y Pases']
        ]
      },
      {
        priority: validated > 0 ? 'medium' : 'low',
        title: 'Validados pendientes de habilitar',
        value: validated,
        subtitle: validated > 0
          ? 'Ya pasaron validación presencial, pero todavía no avanzan al cierre.'
          : 'No hay alumnos atascados en validación.',
        ctaLabel: 'Ir a Check-in',
        ctaAction: "openDashboardModule('checkinModule')",
        rows: [
          ['Siguiente paso', validated > 0 ? 'ACCESS_ENABLED' : '—'],
          ['Módulo', 'Check-in']
        ]
      },
      {
        priority: nearlyFullProjects.length > 0 ? 'medium' : 'low',
        title: 'Proyectos casi saturados',
        value: nearlyFullProjects.length,
        subtitle: nearlyFullProjects.length > 0
          ? 'Conviene vigilar estos proyectos antes de que revienten cupo.'
          : 'No hay proyectos en saturación crítica.',
        ctaLabel: 'Ver Proyectos',
        ctaAction: "openDashboardModule('eventProjectsModule')",
        rows: nearlyFullProjects.length
          ? nearlyFullProjects.map(p => [p.project_name, `${Math.round(p.occupancy)}%`])
          : [['Estado', 'Sin riesgo inmediato']]
      },
      {
        priority: registered === 0 ? 'medium' : 'low',
        title: 'Conversión global',
        value: registered,
        subtitle: registered === 0
          ? 'Todavía no hay cierres reales. Conviene revisar el embudo completo.'
          : 'La temporada ya está convirtiendo en registros finales.',
        ctaLabel: 'Ver Inscritos',
        ctaAction: "openDashboardModule('registrationsModule')",
        rows: [
          ['Registrados', registered],
          ['Lectura', registered === 0 ? 'Sin cierres' : 'Convirtiendo']
        ]
      },
      {
        priority: lowTractionProjects.length > 0 ? 'medium' : 'low',
        title: 'Proyectos con baja tracción',
        value: lowTractionProjects.length,
        subtitle: lowTractionProjects.length > 0
          ? 'Tienen baja ocupación relativa y podrían requerir empuje o revisión.'
          : 'No hay proyectos con alerta temprana de baja tracción.',
        ctaLabel: 'Ver Dashboard',
        ctaAction: "openDashboardModule('summaryModule')",
        rows: lowTractionProjects.length
          ? lowTractionProjects.map(p => [p.project_name, `${Math.round(p.occupancy)}%`])
          : [['Estado', 'Sin alertas']]
      }
    ];
  }

  function renderDashboardCasesBoard(summary, projects) {
    const cases = getDashboardCases(summary, projects);

    return `
      <div class="cases-board">
        <div class="cases-board__head">
          <div>
            <div class="cases-board__title">Casos que requieren intervención</div>
            <div class="cases-board__sub">
              Lectura operativa rápida para decidir dónde actuar primero.
            </div>
          </div>
        </div>

        <div class="cases-grid">
          ${cases.map(item => `
            <div class="case-card ${item.priority}">
              <div class="case-card__top">
                <div>
                  <div class="case-card__title">${escapeHTML(item.title)}</div>
                </div>
                <div class="case-card__value">${escapeHTML(item.value)}</div>
              </div>

              <div class="case-card__sub">${escapeHTML(item.subtitle)}</div>

              <div class="case-card__mini">
                ${(item.rows || []).map(([label, value]) => `
                  <div class="case-mini-row">
                    <strong>${escapeHTML(label)}</strong>
                    <span>${escapeHTML(value)}</span>
                  </div>
                `).join('')}
              </div>

              <div class="case-card__actions">
                <button type="button" class="btn-secondary" onclick="${item.ctaAction}">
                  ${escapeHTML(item.ctaLabel)}
                </button>
              </div>
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  function renderEmptyCard(title, subtitle = '') {
    return `
      <div class="record-card">
        <div class="record-card__title">${escapeHTML(title)}</div>
        <div class="record-card__sub">${escapeHTML(subtitle)}</div>
      </div>
    `;
  }

  function syncBaseProjectSlotsToEventSlots() {
    const projectId = Number(document.getElementById('projectSelector')?.value || 0);
    const slotsInput = document.getElementById('slotsInput');
    if (!projectId || !slotsInput) return;

    const project = (masterProjectsCache || []).find(p => Number(p.id) === projectId);
    if (!project) return;

    slotsInput.value = Number(project.slots || 0);
  }

  async function bootstrapAdmin() {
    const user = await fetchSessionUser();
    applyRoleUI(user);
    if (!user) return;

    const tasks = [loadEvents(), loadAdminCatalogs(), loadMasterProjects()];
    if (user.role === 'ADMIN') tasks.push(loadStaff());
    await Promise.allSettled(tasks);
  }

  async function createAdminEvent() {
    try {
      const year = Number(document.getElementById('eventYear').value);
      const season = document.getElementById('eventSeason').value;
      const status = document.getElementById('eventStatus').value;
      const isVisible = boolFromString(document.getElementById('eventVisible').value);

      if (!year || year < 2020 || year > 2100) {
        return showMsg('Año inválido', false);
      }

      const payload = {
        year,
        season,
        status,
        is_visible_to_students: isVisible,
        catalog_open_at: toSqlDateTime(document.getElementById('eventCatalogOpenAt').value),
        onsite_start_at: toSqlDateTime(document.getElementById('eventOnsiteStartAt').value),
        onsite_end_at: toSqlDateTime(document.getElementById('eventOnsiteEndAt').value),
        registration_close_at: toSqlDateTime(document.getElementById('eventRegistrationCloseAt').value)
      };

      const data = await apiPost('/api/admin/events', payload);
      showMsg(data.message || 'Temporada creada');
      await loadEvents();
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  async function loadEvents() {
    try {
      const data = await apiGet('/api/admin/events');
      allEvents = data || [];

      fillSelectNoBlank('eventSelector', allEvents, e => `${e.display_name} · ${e.status}`);
      fillSelectNoBlank('dashboardEventSelector', allEvents, e => `${e.display_name} · ${e.status}`);
      fillSelectNoBlank('eventProjectEventSelector', allEvents, e => `${e.display_name} · ${e.status}`);
      fillSelectNoBlank('registrationsEventSelector', allEvents, e => `${e.display_name} · ${e.status}`);
      fillSelectNoBlank('exportEventSelector', allEvents, e => `${e.display_name} · ${e.status}`);
      fillSelectNoBlank('evidenceEventSelector', allEvents, e => `${e.display_name} · ${e.status}`);
      fillSelectNoBlank('studentSupportEventSelector', allEvents, e => `${e.display_name} · ${e.status}`);

      ensureSelectsDefault([
        'eventSelector',
        'dashboardEventSelector',
        'eventProjectEventSelector',
        'registrationsEventSelector',
        'exportEventSelector',
        'evidenceEventSelector',
        'studentSupportEventSelector'
      ]);

      const eventsList = document.getElementById('eventsList');

      if (!allEvents.length) {
        if (eventsList) eventsList.innerHTML = renderEmptyCard('No hay temporadas creadas', 'Crea la primera temporada para comenzar.');
        document.getElementById('selectedEventInfo').innerHTML = '';
        document.getElementById('dashboardSummary').innerHTML = '';
        document.getElementById('dashboardProjectsBody').innerHTML = renderEmptyCard('Sin temporadas', 'No hay nada que mostrar todavía.');
        return;
      }

      if (eventsList) {
        eventsList.innerHTML = allEvents.map(e => `
          <div class="record-card">
            <div class="record-card__head">
              <div>
                <div class="record-card__title">${escapeHTML(e.display_name)}</div>
                <div class="record-card__sub">Año ${e.year} · ${e.season}</div>
              </div>
              <div style="display:flex; gap:8px; flex-wrap:wrap;">
                ${statusBadge(e.status)}
                ${e.is_visible_to_students ? '<span class="badge badge-success">VISIBLE ALUMNO</span>' : '<span class="badge badge-neutral">NO VISIBLE</span>'}
              </div>
            </div>
            <div class="meta">
              <div class="meta-box"><span class="meta-label">Catálogo abre</span><div class="meta-value">${escapeHTML(e.catalog_open_at || '—')}</div></div>
              <div class="meta-box"><span class="meta-label">Inicio presencial</span><div class="meta-value">${escapeHTML(e.onsite_start_at || '—')}</div></div>
              <div class="meta-box"><span class="meta-label">Fin presencial</span><div class="meta-value">${escapeHTML(e.onsite_end_at || '—')}</div></div>
              <div class="meta-box"><span class="meta-label">Cierre registro</span><div class="meta-value">${escapeHTML(e.registration_close_at || '—')}</div></div>
            </div>
          </div>
        `).join('');
      }

      await loadSelectedEventInfo();
      await loadEventProjects();
      await loadDashboard();
      await loadIncidents();
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  async function loadSelectedEventInfo() {
    const eventId = document.getElementById('eventSelector')?.value;
    const box = document.getElementById('selectedEventInfo');
    if (!eventId) {
      if (box) box.innerHTML = '';
      return;
    }

    try {
      const e = await apiGet(`/api/admin/events/${eventId}`);
      box.innerHTML = `
        <div class="record-card">
          <div class="record-card__head">
            <div>
              <div class="record-card__title">${escapeHTML(e.display_name)}</div>
              <div class="record-card__sub">${e.season} ${e.year}</div>
            </div>
            <div style="display:flex; gap:8px; flex-wrap:wrap;">
              ${statusBadge(e.status)}
              ${e.is_visible_to_students ? '<span class="badge badge-success">VISIBLE ALUMNO</span>' : '<span class="badge badge-neutral">NO VISIBLE</span>'}
            </div>
          </div>
          <div class="stack-row"><strong>ID:</strong><span>${e.id}</span></div>
        </div>
      `;
      document.getElementById('incidentEventId').value = e.id;
    } catch (e) {
      box.innerHTML = renderEmptyCard(e.message || 'No se pudo cargar la temporada');
    }
  }

  async function updateSelectedEvent() {
    const eventId = document.getElementById('eventSelector')?.value;
    if (!eventId) return showMsg('Selecciona una temporada', false);

    const body = {};
    const statusVal = document.getElementById('eventStatusUpdate')?.value;
    const visibleVal = document.getElementById('eventVisibleUpdate')?.value;

    if (statusVal) body.status = statusVal;
    if (visibleVal !== '') body.is_visible_to_students = boolFromString(visibleVal);

    if (!Object.keys(body).length) return showMsg('No hay cambios para aplicar', false);

    try {
      const data = await apiPatch(`/api/admin/events/${eventId}`, body);
      showMsg(data.message || 'Temporada actualizada');
      await loadEvents();
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  async function setSelectedEventVisible() {
    const eventId = document.getElementById('eventSelector')?.value;
    if (!eventId) return showMsg('Selecciona una temporada', false);

    try {
      const data = await apiPut(`/api/admin/events/${eventId}/visible`, {});
      showMsg(data.message || 'Temporada visible actualizada');
      await loadEvents();
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  async function loadAdminCatalogs() {
    try {
      const data = await apiGet('/api/admin/catalogs');
      fillSelect('mp_partner', data.socio || [], 'Selecciona', item => item.name);
      fillSelect('mp_modality', data.modalidad || [], 'Selecciona', item => item.description);
      fillSelect('mp_week_days', data.dias || [], 'Selecciona', item => item.description);
      fillSelect('mp_schedule', data.horario || [], 'Selecciona', item => item.description);
    } catch (e) {
      showMsg('Error cargando catálogos admin: ' + e.message, false);
    }
  }

  async function createMasterProject() {
    try {
      const payload = {
        general_name: document.getElementById('mp_general_name')?.value.trim(),
        name: document.getElementById('mp_name')?.value.trim(),
        id_partner: Number(document.getElementById('mp_partner')?.value),
        id_modality: Number(document.getElementById('mp_modality')?.value),
        id_week_days: Number(document.getElementById('mp_week_days')?.value),
        id_schedule: Number(document.getElementById('mp_schedule')?.value),
        slots: Number(document.getElementById('mp_slots')?.value || 0),
        schedule_description: document.getElementById('mp_schedule_description')?.value.trim(),
        team_owners: document.getElementById('mp_team_owners')?.value.trim(),
        objectives: document.getElementById('mp_objectives')?.value.trim(),
        activities: document.getElementById('mp_activities')?.value.trim(),
        clave: document.getElementById('mp_clave')?.value.trim(),
        competencies: document.getElementById('mp_competencies')?.value.trim(),
        location: document.getElementById('mp_location')?.value.trim(),
        duration: document.getElementById('mp_duration')?.value.trim(),
        audience: document.getElementById('mp_audience')?.value.trim(),
        max_hours: document.getElementById('mp_max_hours')?.value.trim(),
        comments: document.getElementById('mp_comments')?.value.trim()
      };

      const data = await apiPost('/api/admin/projects', payload);
      showMsg(data.message || 'Proyecto base creado');
      await loadMasterProjects();
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  async function loadMasterProjects() {
    try {
      const q = document.getElementById('masterProjectsSearch')?.value?.trim() || '';
      const query = q ? `?q=${encodeURIComponent(q)}` : '';
      const data = await apiGet('/api/admin/projects' + query);

      masterProjectsCache = data || [];
      fillSelect('projectSelector', masterProjectsCache, 'Selecciona proyecto base', p => `${p.general_name || 'Sin nombre general'} | ${p.name}`);
      syncBaseProjectSlotsToEventSlots();

      const list = document.getElementById('masterProjectsList');
      if (!list) return;

      if (!masterProjectsCache.length) {
        list.innerHTML = renderEmptyCard('No hay proyectos base', 'Crea el primero para empezar.');
        return;
      }

      list.innerHTML = masterProjectsCache.map(p => `
        <div class="record-card">
          <div class="record-card__head">
            <div>
              <div class="record-card__title">${escapeHTML(p.general_name || 'Sin nombre general')} | ${escapeHTML(p.name)}</div>
              <div class="record-card__sub">Project ID: ${p.id}</div>
            </div>
            <div style="display:flex; gap:8px; flex-wrap:wrap;">
              <span class="badge badge-purple">${escapeHTML(p.modality_name || '—')}</span>
              <span class="badge badge-neutral">${escapeHTML(p.week_days_name || '—')}</span>
              <span class="badge badge-neutral">${escapeHTML(p.schedule_name || '—')}</span>
            </div>
          </div>
          <div class="record-stack">
            <div class="stack-row"><strong>Carrera:</strong><span>${escapeHTML(p.partner_name || '—')}</span></div>
            <div class="stack-row"><strong>Horario:</strong><span>${escapeHTML(p.schedule_description || '—')}</span></div>
            <div class="stack-row"><strong>Duración:</strong><span>${escapeHTML(p.duration || '—')}</span></div>
            <div class="stack-row"><strong>Cupo base:</strong><span>${escapeHTML(p.slots ?? '—')}</span></div>
            <div class="stack-row"><strong>Clave:</strong><span>${escapeHTML(p.clave || '—')}</span></div>
          </div>
        </div>
      `).join('');
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  async function addProjectToEvent() {
    const eventId = document.getElementById('eventProjectEventSelector')?.value;
    const projectId = document.getElementById('projectSelector')?.value;
    const rawSlots = document.getElementById('slotsInput')?.value;
    const slots = Number(rawSlots);

    if (!eventId) return showMsg('Selecciona una temporada', false);
    if (!projectId) return showMsg('Selecciona un proyecto base', false);
    if (rawSlots === '' || Number.isNaN(slots)) return showMsg('Debes capturar el cupo para esta temporada', false);
    if (slots <= 0) return showMsg('El cupo para esta temporada debe ser mayor a 0', false);

    try {
      const data = await apiPost(`/api/admin/events/${eventId}/projects`, {
        project_id: Number(projectId),
        slots_total: slots
      });
      showMsg(data.message || 'Proyecto activado en temporada');
      await loadEventProjects();
      await loadDashboard();
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  async function loadEventProjects() {
    const eventId = document.getElementById('eventProjectEventSelector')?.value;
    const container = document.getElementById('eventProjectsList');

    if (!container) return;

    if (!eventId) {
      container.innerHTML = renderEmptyCard('Selecciona una temporada', 'Después podrás ver y operar los proyectos activos.');
      return;
    }

    try {
      const data = await apiGet(`/api/admin/events/${eventId}/projects`);
      eventProjectsCache = data || [];

      fillSelect(
        'tokensEventProjectSelector',
        eventProjectsCache,
        'Selecciona proyecto en temporada',
        p => `${p.name} · ${p.partner || '—'} · EventProject ${p.id}`
      );

      if (!eventProjectsCache.length) {
        container.innerHTML = renderEmptyCard('No hay proyectos activos', 'Activa un proyecto para esta temporada.');
        return;
      }

      container.innerHTML = eventProjectsCache.map(p => `
        <div class="record-card">
          <div class="record-card__head">
            <div>
              <div class="record-card__title">${escapeHTML(p.name)}</div>
              <div class="record-card__sub">Carrera preferida: ${escapeHTML(p.partner || '—')}</div>
            </div>
            <div>${statusBadge(p.status)}</div>
          </div>

          <div class="record-stack">
            <div class="stack-row"><strong>Project ID:</strong><span>${p.project_id}</span></div>
            <div class="stack-row"><strong>EventProject ID:</strong><span>${p.id}</span></div>
            <div class="stack-row"><strong>Cupo actual:</strong><span>${p.slots_total}</span></div>
          </div>

          <div class="form-grid" style="margin-top:12px;">
            <div class="field">
              <label>Nuevo cupo para esta temporada</label>
              <input id="slots_edit_${p.id}" type="number" min="1" value="${p.slots_total}">
            </div>
          </div>

          <div class="actions">
            <button type="button" class="btn-primary" onclick="saveEventProjectSlots(${p.id})">Guardar cupo</button>
            <button type="button" class="btn-secondary" onclick="goToTokensModule(${p.id})">Ver tokens</button>
            <button
              type="button"
              class="btn-secondary"
              onclick="quickUpdateEventProject(${p.id}, Number(document.getElementById('slots_edit_${p.id}').value || ${p.slots_total}), 'ACTIVE')"
            >
              Activar
            </button>
            <button
              type="button"
              class="btn-secondary"
              onclick="quickUpdateEventProject(${p.id}, Number(document.getElementById('slots_edit_${p.id}').value || ${p.slots_total}), 'HIDDEN')"
            >
              Ocultar
            </button>
            <button
              type="button"
              class="btn-secondary"
              onclick="quickUpdateEventProject(${p.id}, Number(document.getElementById('slots_edit_${p.id}').value || ${p.slots_total}), 'CLOSED')"
            >
              Cerrar
            </button>
          </div>
        </div>
      `).join('');
    } catch (e) {
      container.innerHTML = renderEmptyCard(e.message || 'No se pudo cargar proyectos activos');
    }
  }

  async function quickUpdateEventProject(eventProjectId, currentSlots, status) {
    try {
      const data = await apiPatch(`/api/admin/event-projects/${eventProjectId}`, {
        slots_total: currentSlots,
        status
      });
      showMsg(data.message || 'Proyecto de temporada actualizado');
      await loadEventProjects();
      await loadDashboard();
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  async function saveEventProjectSlots(eventProjectId) {
    try {
      const input = document.getElementById(`slots_edit_${eventProjectId}`);
      if (!input) return showMsg('No se encontró el input de cupo', false);

      const rawValue = input.value;
      const slots = Number(rawValue);

      if (rawValue === '' || Number.isNaN(slots)) {
        return showMsg('Captura un cupo válido', false);
      }

      if (slots <= 0) {
        return showMsg('El cupo debe ser mayor a 0', false);
      }

      const data = await apiPatch(`/api/admin/event-projects/${eventProjectId}`, {
        slots_total: slots
      });

      showMsg(data.message || 'Cupo actualizado');
      await loadEventProjects();
      await loadDashboard();
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  function goToTokensModule(eventProjectId) {
    showModule('tokensModule');

    const selector = document.getElementById('tokensEventProjectSelector');
    if (selector) {
      selector.value = String(eventProjectId);
    }

    loadProjectTokens();
  }

  async function generateProjectTokens() {
    try {
      const eventProjectId = document.getElementById('tokensEventProjectSelector')?.value;
      const count = Number(document.getElementById('tokensCount')?.value || 0);
      const length = Number(document.getElementById('tokensLength')?.value || 0);

      if (!eventProjectId) return showMsg('Selecciona un proyecto en temporada', false);

      const data = await apiPost(`/api/admin/event-projects/${eventProjectId}/tokens`, { count, length });

      const result = document.getElementById('tokensGenerationResult');
      if (result) {
        result.innerHTML = `
          <div class="record-card">
            <div class="record-card__title">${escapeHTML(data.message || 'Tokens generados')}</div>
            <div class="record-card__sub">Creados: ${data.created || 0} · TTL: ${data.ttl_hours || '—'} horas</div>
            <div style="margin-top:12px;" class="mono">${(data.tokens || []).join(', ')}</div>
          </div>
        `;
      }

      showMsg(data.message || 'Tokens generados');
      await loadProjectTokens();
      await loadDashboard();
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  async function revokeProjectToken() {
    try {
      const token = document.getElementById('revokeTokenValue')?.value.trim().toUpperCase();
      const reason = document.getElementById('revokeTokenReason')?.value.trim();

      if (!token) return showMsg('Escribe un token', false);

      const data = await apiPost('/api/admin/project-tokens/revoke', { token, reason });
      showMsg(data.message || 'Token revocado');
      await loadProjectTokens();
      await loadDashboard();
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  async function loadProjectTokens() {
    const eventProjectId = document.getElementById('tokensEventProjectSelector')?.value;
    const status = document.getElementById('tokensStatusFilter')?.value || 'ALL';
    const cards = document.getElementById('tokensCards');
    const summary = document.getElementById('tokensSummary');

    if (!cards || !summary) return;

    if (!eventProjectId) {
      cards.innerHTML = renderEmptyCard('Selecciona un proyecto', 'Después podrás ver el estado de sus tokens.');
      summary.innerHTML = '';
      return;
    }

    try {
      const data = await apiGet(`/api/admin/event-projects/${eventProjectId}/tokens?status=${encodeURIComponent(status)}`);
      const s = data.summary || {};

      summary.innerHTML = `
        <div class="kpi-card kpi-card--orange">
          <div class="kpi-label">Available</div>
          <div class="kpi-value">${s.available || 0}</div>
          <div class="kpi-sub">Tokens libres</div>
        </div>
        <div class="kpi-card kpi-card--orange">
          <div class="kpi-label">Reserved</div>
          <div class="kpi-value">${s.reserved || 0}</div>
          <div class="kpi-sub">En espera</div>
        </div>
        <div class="kpi-card kpi-card--green">
          <div class="kpi-label">Used</div>
          <div class="kpi-value">${s.used || 0}</div>
          <div class="kpi-sub">Ya utilizados</div>
        </div>
        <div class="kpi-card kpi-card--pink">
          <div class="kpi-label">Revocados + Expirados</div>
          <div class="kpi-value">${(s.revoked || 0) + (s.expired || 0)}</div>
          <div class="kpi-sub">Fuera de circulación</div>
        </div>
      `;

      const items = data.items || [];
      cards.innerHTML = items.length
        ? items.map(t => `
            <div class="record-card">
              <div class="record-card__head">
                <div>
                  <div class="record-card__title">Token</div>
                  <div class="record-card__sub"><span class="mono">${escapeHTML(t.token_value || '—')}</span></div>
                </div>
                <div>${statusBadge(t.status || '—')}</div>
              </div>

              <div class="record-stack">
                <div class="stack-row"><strong>Reservado por:</strong><span>${escapeHTML(t.reserved_by_request_id || '—')}</span></div>
                <div class="stack-row"><strong>Reserved until:</strong><span>${escapeHTML(t.reserved_until || '—')}</span></div>
                <div class="stack-row"><strong>Usado por:</strong><span>${escapeHTML(t.used_by_request_id || '—')}</span></div>
                <div class="stack-row"><strong>Usado:</strong><span>${escapeHTML(t.used_at || '—')}</span></div>
                <div class="stack-row"><strong>Revocado:</strong><span>${escapeHTML(t.revoked_at || '—')}</span></div>
                <div class="stack-row"><strong>Revocado por admin:</strong><span>${escapeHTML(t.revoked_by_admin_user_id || '—')}</span></div>
                <div class="stack-row"><strong>Expira:</strong><span>${escapeHTML(t.expires_at || '—')}</span></div>
              </div>
            </div>
          `).join('')
        : renderEmptyCard('No hay tokens con ese filtro', 'Prueba otro estado o genera nuevos tokens.');
    } catch (e) {
      summary.innerHTML = '';
      cards.innerHTML = renderEmptyCard(e.message || 'No se pudo cargar tokens');
    }
  }

  async function loadDashboard() {
    const selector = document.getElementById('dashboardEventSelector');
    const summaryBox = document.getElementById('dashboardSummary');
    const healthHero = document.getElementById('dashboardHealthHero');
    const casesBoard = document.getElementById('dashboardCasesBoard');
    const highlights = document.getElementById('dashboardProjectsHighlights');
    const body = document.getElementById('dashboardProjectsBody');

    if (!selector || !summaryBox || !healthHero || !casesBoard || !highlights || !body) return;

    const eventId = selector.value;

    if (!eventId) {
      summaryBox.innerHTML = '';
      healthHero.innerHTML = '';
      casesBoard.innerHTML = '';
      highlights.innerHTML = '';
      body.innerHTML = renderEmptyCard('Selecciona una temporada', 'Luego podrás ver el dashboard.');
      return;
    }

    try {
      const summary = await apiGet(`/api/admin/dashboard/summary?event_id=${eventId}`);
      const projects = await apiGet(`/api/admin/dashboard/projects?event_id=${eventId}`);

      const requests = summary.requests || {};
      const incidents = summary.incidents || {};
      const items = Array.isArray(projects) ? projects : [];

      summaryBox.innerHTML = `
        <div class="kpi-card kpi-card--green">
          <div class="kpi-label">Total inscritos</div>
          <div class="kpi-value">${requests.registered || 0}</div>
          <div class="kpi-sub">Alumnos con cierre final</div>
        </div>

        <div class="kpi-card kpi-card--orange">
          <div class="kpi-label">Access enabled</div>
          <div class="kpi-value">${requests.access_enabled || 0}</div>
          <div class="kpi-sub">Listos para registrar</div>
        </div>

        <div class="kpi-card kpi-card--purple">
          <div class="kpi-label">Proyectos</div>
          <div class="kpi-value">${items.length}</div>
          <div class="kpi-sub">Activos en temporada</div>
        </div>

        <div class="kpi-card kpi-card--pink">
          <div class="kpi-label">Incidentes abiertos</div>
          <div class="kpi-value">${incidents.open || 0}</div>
          <div class="kpi-sub">Pendientes de resolver</div>
        </div>

        <div class="kpi-card kpi-card--blue">
          <div class="kpi-label">Validated</div>
          <div class="kpi-value">${requests.validated || 0}</div>
          <div class="kpi-sub">Ya validados por staff</div>
        </div>
      `;

      const sortedItems = sortProjectsForDashboard(items);

      healthHero.innerHTML = renderDashboardHealthHero(summary, sortedItems);
      casesBoard.innerHTML = renderDashboardCasesBoard(summary, sortedItems);
      highlights.innerHTML = renderDashboardProjectHighlights(sortedItems);

      body.innerHTML = sortedItems.length
        ? sortedItems.map(p => renderDashboardProjectCard(p)).join('')
        : renderEmptyCard('No hay proyectos cargados en esta temporada', 'Activa proyectos para empezar a operar.');
    } catch (e) {
      summaryBox.innerHTML = '';
      healthHero.innerHTML = '';
      casesBoard.innerHTML = '';
      highlights.innerHTML = '';
      body.innerHTML = renderEmptyCard('No se pudo cargar dashboard', e.message || 'Error inesperado');
      showMsg(e.message, false);
    }
  }

  async function loadRegistrations() {
    const eventId = document.getElementById('registrationsEventSelector')?.value;
    const cards = document.getElementById('registrationsCards');

    if (!cards) return;

    if (!eventId) {
      cards.innerHTML = renderEmptyCard('Selecciona una temporada', 'Luego podrás consultar inscripciones cerradas.');
      return;
    }

    try {
      const rows = await apiGet(`/api/admin/registrations?event_id=${encodeURIComponent(eventId)}`);

      if (!rows.length) {
        cards.innerHTML = renderEmptyCard('No hay inscripciones', 'Todavía no hay registros para esta temporada.');
        return;
      }

      cards.innerHTML = rows.map(r => `
        <div class="record-card">
          <div class="record-card__head">
            <div>
              <div class="record-card__title">${escapeHTML(r.student_name || r.student_full_name || '—')}</div>
              <div class="record-card__sub"><span class="mono-soft">${escapeHTML(r.enrolment_number || '—')}</span></div>
            </div>
            <div>${statusBadge(r.registration_status || r.status || '—')}</div>
          </div>

          <div class="record-stack">
            <div class="stack-row"><strong>Registration ID:</strong><span>${escapeHTML(r.registration_id || r.id || '—')}</span></div>
            <div class="stack-row"><strong>Proyecto:</strong><span>${escapeHTML(r.project_name || '—')}</span></div>
            <div class="stack-row"><strong>Organización:</strong><span>${escapeHTML(r.general_name || '—')}</span></div>
            <div class="stack-row"><strong>Carrera preferida:</strong><span>${escapeHTML(r.partner_name || '—')}</span></div>
            <div class="stack-row"><strong>Folio:</strong><span>${escapeHTML(r.folio || '—')}</span></div>
            <div class="stack-row"><strong>Token:</strong><span class="mono">${escapeHTML(r.token_value || '—')}</span></div>
            <div class="stack-row"><strong>Nombre aceptado:</strong><span>${escapeHTML(r.accepted_full_name || '—')}</span></div>
            <div class="stack-row"><strong>Versión legal:</strong><span>${escapeHTML(r.legal_text_version || '—')}</span></div>
            <div class="stack-row"><strong>Fecha cierre:</strong><span>${escapeHTML(r.accepted_at || '—')}</span></div>

            ${
              (r.registration_status || r.status) === 'CANCELLED'
                ? `
                  <div class="stack-row"><strong>Fecha baja:</strong><span>${escapeHTML(r.cancelled_at || '—')}</span></div>
                  <div class="stack-row"><strong>Motivo baja:</strong><span>${escapeHTML(r.cancel_reason || '—')}</span></div>
                  <div class="stack-row"><strong>Cancelado por admin:</strong><span>${escapeHTML(r.cancelled_by_admin_user_id || '—')}</span></div>
                `
                : ''
            }
          </div>

          <div class="actions">
            <button
              type="button"
              class="btn-secondary"
              data-enrolment="${escapeHTML(r.enrolment_number || '')}"
              data-event-id="${Number(r.event_id || eventId || 0)}"
              onclick="openEvidenceFromButton(this)"
            >
              Ver evidencia
            </button>

            ${
              (r.registration_status || r.status) === 'ACTIVE'
                ? `
                  <button
                    type="button"
                    class="btn-danger"
                    onclick="cancelRegistration(${Number(r.registration_id || r.id || 0)})"
                  >
                    Dar de baja
                  </button>
                `
                : ''
            }
          </div>
        </div>
      `).join('');

      showMsg('Inscripciones cargadas correctamente');
    } catch (e) {
      cards.innerHTML = renderEmptyCard(e.message || 'No se pudo cargar inscripciones');
      showMsg(e.message, false);
    }
  }

  function openEvidenceFromButton(btn) {
    const enrolmentNumber = btn?.dataset?.enrolment || '';
    const eventId = Number(btn?.dataset?.eventId || 0);
    setEvidenceFromRegistration(enrolmentNumber, eventId);
  }

  function setEvidenceFromRegistration(enrolmentNumber, eventId) {
    const enrolmentInput = document.getElementById('evidenceEnrolmentNumber');
    const eventSelect = document.getElementById('evidenceEventSelector');
    if (enrolmentInput) enrolmentInput.value = enrolmentNumber || '';
    if (eventId && eventSelect) eventSelect.value = String(eventId);
    showModule('evidenceModule');
    loadEvidenceByEnrolment();
  }

  async function loadEvidenceByEnrolment() {
    const enrolment = (document.getElementById('evidenceEnrolmentNumber')?.value || '').trim();
    const eventId = document.getElementById('evidenceEventSelector')?.value;
    const box = document.getElementById('evidenceResult');

    if (!box) return;
    if (!enrolment) return showMsg('Ingresa una matrícula válida', false);

    try {
      const params = new URLSearchParams();
      params.set('enrolment_number', enrolment);
      if (eventId) params.set('event_id', eventId);

      const data = await apiGet(`/api/admin/registrations/evidence?${params.toString()}`);

      const v = data.verification || {};
      const legal = data.legal_confirmation || {};
      const reg = data.registration || {};
      const student = data.student || {};
      const project = data.project || {};
      const request = data.request || {};
      const event = data.event || {};
      const evidence = data.evidence || {};

      box.innerHTML = `
        <div class="record-card">
          <div class="record-card__head">
            <div>
              <div class="record-card__title">${escapeHTML(student.full_name || 'Alumno')}</div>
              <div class="record-card__sub">
                Matrícula: ${escapeHTML(student.enrolment_number || '—')} ·
                Folio: ${escapeHTML(request.folio || '—')}
              </div>
            </div>

            <div style="display:flex; gap:8px; flex-wrap:wrap;">
              ${v.verified ? '<span class="badge badge-success">VERIFICADO</span>' : '<span class="badge badge-danger">NO VERIFICADO</span>'}
              ${v.hash_matches ? '<span class="badge badge-success">HASH OK</span>' : '<span class="badge badge-danger">HASH FAIL</span>'}
              ${v.signature_matches ? '<span class="badge badge-success">SIGNATURE OK</span>' : '<span class="badge badge-danger">SIGNATURE FAIL</span>'}
              ${statusBadge(reg.status || '—')}
            </div>
          </div>

          <div class="record-stack">
            <div class="stack-row"><strong>Temporada:</strong><span>${escapeHTML(event.display_name || '—')}</span></div>
            <div class="stack-row"><strong>Proyecto:</strong><span>${escapeHTML(project.project_name || '—')}</span></div>
            <div class="stack-row"><strong>Organización:</strong><span>${escapeHTML(project.general_name || '—')}</span></div>
            <div class="stack-row"><strong>Nombre aceptado:</strong><span>${escapeHTML(legal.accepted_full_name || '—')}</span></div>
            <div class="stack-row"><strong>Versión legal:</strong><span>${escapeHTML(legal.legal_text_version || '—')}</span></div>
            <div class="stack-row"><strong>Fecha aceptación:</strong><span>${escapeHTML(legal.accepted_at || '—')}</span></div>
            <div class="stack-row"><strong>IP:</strong><span>${escapeHTML(legal.accepted_ip || '—')}</span></div>
            <div class="stack-row"><strong>User agent:</strong><span>${escapeHTML(legal.accepted_user_agent || '—')}</span></div>
            <div class="stack-row"><strong>Fingerprint:</strong><span class="mono">${escapeHTML(student.student_fingerprint || '—')}</span></div>
          </div>
        </div>

        <div class="record-card">
          <div class="record-card__title">Hash guardado</div>
          <div class="record-card__sub" style="margin-top:8px;"><span class="mono">${escapeHTML(evidence.stored_hash || '—')}</span></div>
        </div>

        <div class="record-card">
          <div class="record-card__title">Hash recalculado</div>
          <div class="record-card__sub" style="margin-top:8px;"><span class="mono">${escapeHTML(evidence.recalculated_hash || '—')}</span></div>
        </div>

        <div class="record-card">
          <div class="record-card__title">Firma guardada</div>
          <div class="record-card__sub" style="margin-top:8px;"><span class="mono">${escapeHTML(evidence.stored_signature || '—')}</span></div>
        </div>

        <div class="record-card">
          <div class="record-card__title">Firma recalculada</div>
          <div class="record-card__sub" style="margin-top:8px;"><span class="mono">${escapeHTML(evidence.recalculated_signature || '—')}</span></div>
        </div>

        <div class="record-card">
          <div class="record-card__title">Snapshot parseado</div>
          <div class="json-box">${escapeHTML(prettyJSON(evidence.snapshot_data || {}))}</div>
        </div>

        <div class="record-card">
          <div class="record-card__title">Snapshot JSON original</div>
          <div class="json-box">${escapeHTML(prettyJSON(evidence.snapshot_json || ''))}</div>
        </div>
      `;

      showMsg('Evidencia legal cargada correctamente');
    } catch (e) {
      box.innerHTML = renderEmptyCard(e.message || 'No se pudo cargar evidencia');
      showMsg(e.message, false);
    }
  }

  async function cancelRegistration(registrationId) {
    try {
      if (!registrationId) return showMsg('registrationId inválido', false);

      const reason = window.prompt('Escribe el motivo de baja:');
      if (reason === null) return;

      const cleanReason = reason.trim();
      if (!cleanReason) return showMsg('El motivo es obligatorio', false);

      const data = await apiPatch(`/api/admin/registrations/${registrationId}/cancel`, {
        reason: cleanReason
      });

      showMsg(data.message || 'Inscripción cancelada');
      await loadRegistrations();
      await loadDashboard();
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  async function startQrScanner() {
    try {
      if (staffQrScanner) await stopQrScanner();

      staffQrScanner = new Html5Qrcode('staffScanner');

      await staffQrScanner.start(
        { facingMode: 'environment' },
        { fps: 10, qrbox: { width: 220, height: 220 } },
        async (decodedText) => {
          const input = document.getElementById('staffScannedToken');
          if (input) input.value = decodedText;
          await scanStaffQr();
        },
        () => {}
      );

      showMsg('Cámara activa para escaneo QR');
    } catch (e) {
      showMsg('No se pudo abrir la cámara: ' + e.message, false);
    }
  }

  async function stopQrScanner() {
    try {
      if (staffQrScanner) {
        await staffQrScanner.stop();
        await staffQrScanner.clear();
        staffQrScanner = null;
        showMsg('Cámara detenida');
      }
    } catch (e) {
      showMsg('Error al detener cámara: ' + e.message, false);
    }
  }

  async function scanStaffQr() {
    try {
      const token = document.getElementById('staffScannedToken')?.value.trim();
      if (!token) return showMsg('Escanea o pega primero un QR/token', false);

      const data = await apiPost('/api/staff/checkin/scan', { token });
      lastScannedPassSession = data.pass_session?.id || null;

      document.getElementById('staffCheckinInfo').innerHTML = `
        <div class="record-card">
          <div class="record-card__head">
            <div>
              <div class="record-card__title">${escapeHTML(data.student?.full_name || 'Alumno')}</div>
              <div class="record-card__sub">Matrícula registrada: ${escapeHTML(data.student?.enrolment_number || '—')}</div>
            </div>
            <div>${statusBadge(data.request?.status || 'REQUESTED')}</div>
          </div>

          <div class="record-stack">
            <div class="stack-row"><strong>Folio:</strong><span>${escapeHTML(data.request?.folio || '—')}</span></div>
            <div class="stack-row"><strong>Temporada:</strong><span>${escapeHTML(data.event?.display_name || '—')}</span></div>
            <div class="stack-row"><strong>QR expira:</strong><span>${escapeHTML(data.pass_session?.expires_at || '—')}</span></div>
            <div class="stack-row"><strong>Carrera:</strong><span>${escapeHTML(data.student?.degree || '—')}</span></div>
          </div>
        </div>
      `;

      showMsg('QR válido. Verifica ahora la matrícula física.');
    } catch (e) {
      lastScannedPassSession = null;
      document.getElementById('staffCheckinInfo').innerHTML = renderEmptyCard('QR inválido o no disponible', e.message || '');
      showMsg(e.message, false);
    }
  }

  async function grantStaffAccess() {
    try {
      const passSessionId = lastScannedPassSession;
      const enrolment = document.getElementById('staffPhysicalEnrolment')?.value.trim();

      if (!passSessionId) return showMsg('Primero debes verificar el QR', false);
      if (!enrolment) return showMsg('Falta capturar la matrícula física', false);

      const data = await apiPost('/api/staff/checkin/grant-access', {
        pass_session_id: passSessionId,
        enrolment_number: enrolment
      });

      lastScannedPassSession = null;
      document.getElementById('staffScannedToken').value = '';
      document.getElementById('staffPhysicalEnrolment').value = '';

      showMsg(data.message || 'Acceso habilitado');
      document.getElementById('staffCheckinInfo').innerHTML += `
        <div class="record-card">
          <div class="record-card__title">Acceso habilitado correctamente</div>
          <div class="record-card__sub">El alumno ya puede entrar al catálogo y cerrar inscripción.</div>
        </div>
      `;
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  async function createIncident() {
    try {
      const payload = {
        event_id: Number(document.getElementById('incidentEventId')?.value),
        request_id: document.getElementById('incidentRequestId')?.value || null,
        id_user: document.getElementById('incidentUserId')?.value || null,
        type: document.getElementById('incidentType')?.value,
        severity: document.getElementById('incidentSeverity')?.value,
        description: document.getElementById('incidentDescription')?.value.trim()
      };

      const data = await apiPost('/api/incidents', payload);
      showMsg(data.message || 'Caso reportado');
      document.getElementById('incidentDescription').value = '';
      document.getElementById('incidentRequestId').value = '';
      document.getElementById('incidentUserId').value = '';
      await loadIncidents();
      await loadDashboard();
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  async function loadIncidents() {
    const eventId =
      document.getElementById('eventSelector')?.value ||
      document.getElementById('dashboardEventSelector')?.value ||
      document.getElementById('eventProjectEventSelector')?.value ||
      document.getElementById('registrationsEventSelector')?.value;

    const list = document.getElementById('incidentsList');
    if (!list) return;

    if (!eventId) {
      list.innerHTML = renderEmptyCard('Selecciona una temporada', 'Luego podrás consultar incidentes.');
      return;
    }

    const params = new URLSearchParams();
    params.set('event_id', eventId);

    const status = document.getElementById('incidentFilterStatus')?.value;
    const severity = document.getElementById('incidentFilterSeverity')?.value;
    if (status) params.set('status', status);
    if (severity) params.set('severity', severity);

    try {
      const response = await apiGet(`/api/incidents?${params.toString()}`);
      const data = Array.isArray(response) ? response : (response.items || []);

      if (!data.length) {
        list.innerHTML = renderEmptyCard('No hay incidentes con esos filtros', 'Prueba otro estado o severidad.');
        return;
      }

      list.innerHTML = data.map(i => `
        <div class="record-card">
          <div class="record-card__head">
            <div>
              <div class="record-card__title">${escapeHTML(i.type)}</div>
              <div class="record-card__sub">Incident ID: ${i.id} · Request ID: ${i.request_id ?? '—'} · User ID: ${i.id_user ?? '—'}</div>
            </div>
            <div style="display:flex; gap:8px; flex-wrap:wrap;">
              ${statusBadge(i.status)}
              <span class="${i.severity === 'HIGH' ? 'badge badge-danger' : i.severity === 'MEDIUM' ? 'badge badge-warn' : 'badge badge-success'}">${i.severity}</span>
            </div>
          </div>

          <div class="record-stack">
            <div class="stack-row"><strong>Descripción:</strong><span>${escapeHTML(i.description || 'Sin descripción')}</span></div>
            <div class="stack-row"><strong>Creado:</strong><span>${escapeHTML(i.created_at || '—')}</span></div>
            <div class="stack-row"><strong>Resuelto:</strong><span>${escapeHTML(i.resolved_at || '—')}</span></div>
            <div class="stack-row"><strong>Actor admin:</strong><span>${escapeHTML(i.performed_by_admin_user_id || '—')}</span></div>
          </div>

          <div class="actions">
            <button type="button" class="btn-secondary" onclick="updateIncidentStatus(${i.id}, 'IN_PROGRESS')">Marcar en proceso</button>
            <button type="button" class="btn-secondary" onclick="updateIncidentStatus(${i.id}, 'RESOLVED')">Resolver</button>
            <button type="button" class="btn-secondary" onclick="updateIncidentStatus(${i.id}, 'DISMISSED')">Descartar</button>
          </div>
        </div>
      `).join('');
    } catch (e) {
      list.innerHTML = renderEmptyCard(e.message || 'No se pudo cargar incidentes');
    }
  }

  async function updateIncidentStatus(incidentId, status) {
    try {
      const data = await apiPatch(`/api/incidents/${incidentId}`, { status });
      showMsg(data.message || 'Caso actualizado');
      await loadIncidents();
      await loadDashboard();
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  async function loadStaff() {
    const list = document.getElementById('staffList');
    if (!list) return;

    try {
      const status = document.getElementById('staffStatusFilter')?.value || '';
      const query = status ? `?status=${encodeURIComponent(status)}` : '';
      const response = await apiGet('/api/admin/staff' + query);
      const items = response.items || response || [];

      if (!items.length) {
        list.innerHTML = renderEmptyCard('No hay cuentas staff', 'Crea la primera cuenta operativa.');
        return;
      }

      list.innerHTML = items.map(s => `
        <div class="record-card">
          <div class="record-card__head">
            <div>
              <div class="record-card__title">${escapeHTML(s.full_name || '—')}</div>
              <div class="record-card__sub">${escapeHTML(s.email || '—')}</div>
            </div>
            <div>${statusBadge(s.status)}</div>
          </div>

          <div class="record-stack">
            <div class="stack-row"><strong>ID:</strong><span>${escapeHTML(s.id || '—')}</span></div>
            <div class="stack-row"><strong>Último login:</strong><span>${escapeHTML(s.last_login_at || '—')}</span></div>
            <div class="stack-row"><strong>Creado:</strong><span>${escapeHTML(s.created_at || '—')}</span></div>
          </div>

          <div class="actions">
            <button type="button" class="btn-secondary" onclick="updateStaffStatus(${s.id}, 'ACTIVE')">Activar</button>
            <button type="button" class="btn-danger" onclick="updateStaffStatus(${s.id}, 'DISABLED')">Desactivar</button>
          </div>
        </div>
      `).join('');
    } catch (e) {
      list.innerHTML = renderEmptyCard(e.message || 'No se pudo cargar staff');
    }
  }

  async function createStaff() {
    try {
      const full_name = document.getElementById('staffFullName')?.value.trim();
      const email = document.getElementById('staffEmail')?.value.trim().toLowerCase();
      const password = document.getElementById('staffPassword')?.value;

      if (!full_name) return showMsg('Falta nombre completo', false);
      if (!email) return showMsg('Falta correo', false);
      if (!password) return showMsg('Falta contraseña', false);

      const data = await apiPost('/api/admin/staff', { full_name, email, password });
      showMsg(data.message || 'Staff creado');

      document.getElementById('staffFullName').value = '';
      document.getElementById('staffEmail').value = '';
      document.getElementById('staffPassword').value = '';

      await loadStaff();
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  async function updateStaffStatus(userId, status) {
    try {
      const data = await apiPatch(`/api/admin/staff/${userId}/status`, { status });
      showMsg(data.message || 'Estado de staff actualizado');
      await loadStaff();
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  async function importProjects() {
    try {
      const fileInput = document.getElementById('importProjectsFile');
      const file = fileInput?.files?.[0];
      if (!file) return showMsg('Selecciona un archivo Excel', false);

      const formData = new FormData();
      formData.append('file', file);

      const r = await fetch('/api/admin/projects/import', {
        method: 'POST',
        credentials: 'include',
        body: formData
      });

      const data = await r.json().catch(() => ({}));
      if (!r.ok) throw new Error(data.error || ('Error ' + r.status));

      const result = document.getElementById('importProjectsResult');
      if (result) {
        result.innerHTML = `
          <div class="record-card">
            <div class="record-card__title">${escapeHTML(data.message || 'Importación completada')}</div>
            <div class="record-card__sub">Insertados: ${data.inserted || 0} · Fallidos: ${data.failed || 0}</div>
          </div>
          ${(data.errors && data.errors.length)
            ? data.errors.map(e => `
              <div class="record-card">
                <div class="record-card__title">Fila ${e.row}</div>
                <div class="record-card__sub">${escapeHTML(e.error)}</div>
              </div>
            `).join('')
            : ''}
        `;
      }

      showMsg(data.message || 'Importación completada');
      await loadMasterProjects();
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  async function exportProjects() {
    try {
      const r = await fetch('/api/admin/projects/export', {
        credentials: 'include'
      });

      if (!r.ok) {
        const data = await r.json().catch(() => ({}));
        throw new Error(data.error || ('Error ' + r.status));
      }

      const blob = await r.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'projects_export.xlsx';
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);

      showMsg('Exportación iniciada correctamente');
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  async function exportEventReport() {
    const eventId = document.getElementById('exportEventSelector')?.value;
    if (!eventId) return showMsg('Selecciona una temporada para exportar', false);

    try {
      const r = await fetch(`/api/admin/events/${eventId}/export`, {
        credentials: 'include'
      });

      if (!r.ok) {
        const data = await r.json().catch(() => ({}));
        throw new Error(data.error || ('Error ' + r.status));
      }

      const blob = await r.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `reporte_temporada_${eventId}.xlsx`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);

      const hint = document.getElementById('exportHint');
      if (hint) {
        hint.innerHTML = `
          <div class="record-card">
            <div class="record-card__title">Exportación iniciada</div>
            <div class="record-card__sub">El reporte completo de la temporada se descargó correctamente.</div>
          </div>
        `;
      }

      showMsg('Exportación iniciada correctamente');
    } catch (e) {
      showMsg(e.message, false);
    }
  }

  document.addEventListener('DOMContentLoaded', async () => {
    await bootstrapAdmin();

    clearStudentSupportSearch();
    clearTimeout(studentSupportSearchTimer);

    document.getElementById('loginPassword')?.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') loginAdmin();
    });

    document.getElementById('eventSelector')?.addEventListener('change', async () => {
      await loadSelectedEventInfo();
      document.getElementById('incidentEventId').value = document.getElementById('eventSelector').value || '';
    });

    document.getElementById('dashboardEventSelector')?.addEventListener('change', async () => {
      await loadDashboard();
    });

    document.getElementById('eventProjectEventSelector')?.addEventListener('change', async () => {
      await loadEventProjects();
    });

    document.getElementById('tokensEventProjectSelector')?.addEventListener('change', async () => {
      await loadProjectTokens();
    });

    document.getElementById('registrationsEventSelector')?.addEventListener('change', async () => {
      await loadRegistrations();
    });

    document.getElementById('studentSupportSearch')?.addEventListener('input', scheduleStudentSupportSearch);

    document.getElementById('studentSupportSearch')?.addEventListener('keypress', async (e) => {
      if (e.key === 'Enter') {
        await searchStudentSupport();
      }
    });
    
    document.getElementById('studentSupportEventSelector')?.addEventListener('change', async () => {
      const q = (document.getElementById('studentSupportSearch')?.value || '').trim();
      const eventId = document.getElementById('studentSupportEventSelector')?.value;
      if (q || eventId) {
        await searchStudentSupport();
      }
    });

    document.getElementById('projectSelector')?.addEventListener('change', syncBaseProjectSlotsToEventSlots);
  });
</script>
</body>
</html>
"""

