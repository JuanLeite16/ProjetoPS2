## @file styles.py
#  @package styles
#  @brief Módulo responsável pelas definições de estilo visual (CSS).
#  @details Contém a string CSS que personaliza a aparência do dashboard Shiny,
#  inclui cores, fontes, cartões e tabelas.

## @var CSS
#  @brief String que contém todo o código CSS da aplicação.
CSS = """
:root{
  --bg:#F5F7FB;
  --card:#FFFFFF;
  --text:#0F172A;
  --muted:#64748B;
  --blue:#1677FF;
  --line:#E5E7EB;
  --shadow: 0 10px 30px rgba(2, 6, 23, .08);
  --radius: 16px;
}
body{
  background: var(--bg);
  color: var(--text);
  font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial;
}
.header{ display:flex; align-items:flex-end; justify-content:space-between; gap:16px; margin: 6px 0 18px; }
.title{ font-size: 42px; font-weight: 900; letter-spacing: -0.03em; margin: 0; }
.subtitle{ margin: 4px 0 0; color: var(--muted); font-weight: 600; }

.card{
  background: var(--card) !important;
  border-radius: var(--radius) !important;
  box-shadow: var(--shadow) !important;
  border: 1px solid rgba(229,231,235,.9) !important;
  padding: 18px !important;
}
.card-title{ display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom: 10px; }
.card-title h3{ margin: 0; font-size: 16px; font-weight: 900; color: var(--text); }
.badge{
  display:inline-flex; align-items:center;
  padding: 6px 10px; border-radius: 999px;
  background: rgba(22,119,255,.10);
  color: var(--blue); font-weight: 800; font-size: 12px;
}
.muted{ color: var(--muted); font-weight: 700; }

.kpi{ display:flex; flex-direction:column; gap:6px; }
.kpi .label{ color: var(--muted); font-weight: 800; font-size: 12px; text-transform: uppercase; letter-spacing: .08em; }
.kpi .value{ font-size: 30px; font-weight: 1000; letter-spacing: -0.02em; }
.kpi .hint{ color: var(--muted); font-weight: 600; font-size: 12px; }

.info-grid{ display:flex; flex-direction:column; gap:10px; }
.info-row{ display:flex; justify-content:space-between; gap:12px; border-bottom: 1px dashed rgba(229,231,235,.9); padding-bottom: 8px; }
.info-row:last-child{ border-bottom: none; padding-bottom: 0; }
.info-row .k{ color: var(--muted); font-weight: 800; }
.info-row .v{ color: var(--text); font-weight: 800; }

.table-wrap{ max-height: 520px; overflow: auto; border-radius: 12px; border: 1px solid var(--line); }
table{ width: 100%; border-collapse: collapse; background:#fff; font-size: 13px; }
thead th{
  position: sticky; top: 0;
  background: #F1F5FF; color: #0B2A5B;
  font-weight: 900; border-bottom: 1px solid var(--line);
  padding: 10px; text-align: center;
}
tbody td{ border-bottom: 1px solid rgba(229,231,235,.8); padding: 10px; text-align: center; }
tbody tr:hover{ background: #F8FAFF; }

.table-wrap{ width: 100% !important; }
.table-wrap > div{ width: 100% !important; }
.table-wrap table{ width: 100% !important; min-width: 100% !important; table-layout: auto; }
"""