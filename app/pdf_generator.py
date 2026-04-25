"""
pdf_generator.py
Poster DIN A4 horizontal — Midnight Silver.
Distribución del sueldo, donuts, consideraciones clave, radar comparativo.
by a Cambeiro
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import base64
from pathlib import Path
from datetime import datetime
from app.styles import page_header

PROCESSED = Path(__file__).parent.parent / "data" / "processed"
ASSETS    = Path(__file__).parent.parent / "assets"

# ── Mapas auxiliares ──────────────────────────────────────────
CLIMATE_MAP = {
    "Norway": "frío", "Finland": "frío", "Sweden": "frío", "Denmark": "frío",
    "Canada": "frío", "Estonia": "frío", "Latvia": "frío", "Lithuania": "frío",
    "Germany": "templado", "Poland": "templado", "Czech Republic": "templado",
    "Austria": "templado", "Hungary": "templado", "Switzerland": "templado",
    "France": "templado", "Belgium": "templado", "Netherlands": "templado",
    "United Kingdom": "templado", "Ireland": "templado", "Romania": "templado",
    "Japan": "templado", "South Korea": "templado", "New Zealand": "templado",
    "Spain": "cálido", "Portugal": "cálido", "Italy": "cálido", "Greece": "cálido",
    "Mexico": "cálido", "Brazil": "cálido", "Colombia": "cálido",
    "Singapore": "cálido", "India": "cálido", "Turkey": "cálido",
    "United Arab Emirates": "cálido", "Israel": "cálido",
    "Australia": "cálido", "South Africa": "cálido",
    "United States": "variado", "China": "variado", "Argentina": "variado",
}

STABILITY_SCORES = {
    "Norway": 98, "Denmark": 97, "Finland": 97, "Sweden": 96,
    "Switzerland": 96, "New Zealand": 95, "Australia": 94,
    "Canada": 94, "Netherlands": 93, "Luxembourg": 93,
    "Germany": 92, "Austria": 91, "Ireland": 91,
    "United Kingdom": 89, "Japan": 89, "United States": 87,
    "Belgium": 87, "France": 85, "Singapore": 85,
    "South Korea": 84, "Portugal": 83, "Spain": 82,
    "Czech Republic": 81, "Slovenia": 80, "Estonia": 80,
    "Italy": 78, "Latvia": 77, "Lithuania": 76,
    "Poland": 76, "Slovakia": 75, "Hungary": 73,
    "Croatia": 72, "Greece": 70, "Israel": 68,
    "Romania": 65, "Bulgaria": 63, "South Africa": 58,
    "Turkey": 54, "India": 60, "China": 62,
    "Brazil": 55, "Mexico": 52, "Argentina": 48,
    "United Arab Emirates": 75,
}


# ── Distribución del sueldo ───────────────────────────────────
def compute_budget_distribution(city: dict, estimated_salary: float) -> dict:
    """
    Calcula la distribución % del sueldo neto en categorías.
    Vivienda: dato real del dataset.
    Alimentación, transporte, ocio: proxies escalados por cost_of_living_index.
    Ahorro: residual.
    """
    tax       = city.get("tax_rate", 30)
    net       = estimated_salary * (1 - tax / 100)
    rent      = city.get("average_rent", 1000)
    col_idx   = city.get("cost_of_living_index", 70) / 100

    vivienda      = min(rent * 12 / net * 100, 45) if net > 0 else 35
    alimentacion  = min(15 * col_idx * 1.2, 20)
    transporte    = min(5  * col_idx * 1.1, 10)
    ocio          = min(8  * col_idx * 1.0, 12)
    ahorro        = max(0, 100 - vivienda - alimentacion - transporte - ocio)

    return {
        "Vivienda":      round(vivienda,     1),
        "Alimentación":  round(alimentacion, 1),
        "Transporte":    round(transporte,   1),
        "Ocio":          round(ocio,         1),
        "Ahorro":        round(ahorro,       1),
    }


# ── Consideraciones clave ─────────────────────────────────────
def get_key_insights(city: dict, budget: dict) -> list[tuple[str, str]]:
    """
    Genera 3 consideraciones clave desde los datos.
    Devuelve lista de (emoji, texto).
    """
    insights = []
    country  = city.get("country", "")
    clima    = CLIMATE_MAP.get(country, "variado")
    stab     = STABILITY_SCORES.get(country, 60)
    tax      = city.get("tax_rate", 30)
    rent     = city.get("average_rent", 1000)
    qol      = city.get("quality_of_life_index", 100)
    job      = city.get("job_market_score", 50)
    ppi      = city.get("purchasing_power_index", 70)
    ahorro   = budget.get("Ahorro", 0)

    # Reglas ordenadas por impacto
    rules = [
        (stab >= 92,        "🛡️",  "País políticamente muy estable"),
        (stab >= 80,        "🛡️",  f"País estable ({stab}/100)"),
        (tax < 20,          "📋",  f"Carga fiscal muy baja ({tax:.0f}%)"),
        (tax < 30,          "📋",  f"Fiscalidad favorable ({tax:.0f}%)"),
        (tax > 48,          "⚠️",  f"Alta presión fiscal ({tax:.0f}%)"),
        (ahorro > 30,       "💰",  f"Alto potencial de ahorro ({ahorro:.0f}% del neto)"),
        (ahorro > 20,       "💰",  f"Buen margen de ahorro ({ahorro:.0f}% del neto)"),
        (ahorro < 5,        "📉",  "Margen de ahorro muy ajustado"),
        (rent < 700,        "🏠",  "Alquiler muy asequible"),
        (rent > 2500,       "🏠",  "Alquiler elevado"),
        (qol > 175,         "⭐",  "Calidad de vida excepcional"),
        (qol > 155,         "⭐",  "Alta calidad de vida"),
        (job > 80,          "💼",  "Ecosistema tech muy activo"),
        (job > 65,          "💼",  "Buen mercado tech local"),
        (ppi > 110,         "💎",  "Alto poder adquisitivo"),
        (ppi > 90,          "💎",  "Buen poder adquisitivo"),
        (clima == "cálido", "☀️",  "Clima cálido y soleado"),
        (clima == "frío",   "❄️",  "Clima frío — inviernos duros"),
        (clima == "templado","🌤️", "Clima templado y equilibrado"),
        (country in ["Singapore", "United Arab Emirates"], "🌏", "Hub internacional de negocios"),
        (country in ["United States", "Canada"],           "🗽", "Gran mercado anglófono"),
        (country in ["Spain", "Portugal", "Italy"],        "🍷", "Cultura mediterránea vibrante"),
        (country in ["Germany", "Netherlands", "Switzerland"], "🏗️", "Infraestructura de primer nivel"),
        (country in ["Sweden", "Denmark", "Finland", "Norway"], "🌿", "Modelo nórdico de bienestar"),
    ]

    seen_emojis = set()
    for condition, emoji, text in rules:
        if condition and emoji not in seen_emojis and len(insights) < 3:
            insights.append((emoji, text))
            seen_emojis.add(emoji)

    # Fallback si no hay suficientes
    fallbacks = [("🗺️", "Destino internacional"), ("🔍", "Ciudad con potencial"), ("📊", "Datos disponibles")]
    for fb in fallbacks:
        if len(insights) < 3:
            insights.append(fb)

    return insights[:3]


# ── Logo en base64 ────────────────────────────────────────────
def get_logo_b64() -> str:
    try:
        svg = (ASSETS / "logo.svg").read_text(encoding="utf-8")
        return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()
    except FileNotFoundError:
        return ""


# ── Donut chart en base64 ─────────────────────────────────────
def build_donut_b64(budget: dict, size: int = 200) -> str:
    """Genera un donut de distribución del sueldo en escala de grises."""
    labels = list(budget.keys())
    values = list(budget.values())
    colors = ["#f5f5f7", "#aeaeb2", "#8e8e93", "#636366", "#3a3a3c"]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.6,
        marker=dict(colors=colors, line=dict(color="#111111", width=2)),
        textinfo="none",
        hoverinfo="none",
        showlegend=False,
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=0, b=0, l=0, r=0),
        height=size, width=size,
        annotations=[dict(
            text=f"{budget.get('Ahorro', 0):.0f}%<br><span style='font-size:8px'>ahorro</span>",
            x=0.5, y=0.5, font_size=14,
            font_color="#f5f5f7",
            showarrow=False,
        )],
    )

    img_bytes = pio.to_image(fig, format="png", scale=2)
    return "data:image/png;base64," + base64.b64encode(img_bytes).decode()


# ── Radar comparativo en base64 ───────────────────────────────
def build_radar_b64(cities: list[dict]) -> str:
    metrics = [
        "purchasing_power_index",
        "quality_of_life_index",
        "job_market_score",
        "relocation_score",
    ]
    labels  = ["Poder adq.", "Calidad vida", "Mercado tech", "Rel. Score"]
    colors  = ["#f5f5f7", "#aeaeb2", "#6e6e73"]

    fig = go.Figure()
    for i, city in enumerate(cities[:3]):
        vals = [min(city.get(m, 0), 100) for m in metrics]
        fig.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=labels + [labels[0]],
            fill="toself",
            name=city.get("city_name", ""),
            line_color=colors[i % len(colors)],
            opacity=0.75,
            showlegend=True,
        ))

    fig.update_layout(
        polar=dict(
            bgcolor="#1c1c1e",
            radialaxis=dict(
                visible=True, range=[0, 100],
                gridcolor="#2c2c2e",
                tickfont=dict(color="#6e6e73", size=7),
                tickvals=[25, 50, 75, 100],
            ),
            angularaxis=dict(
                gridcolor="#2c2c2e",
                tickfont=dict(color="#aeaeb2", size=9),
            ),
        ),
        paper_bgcolor="#111111",
        showlegend=True,
        legend=dict(
            font=dict(color="#aeaeb2", size=9),
            bgcolor="rgba(0,0,0,0)",
            orientation="h",
            y=-0.2, x=0.5, xanchor="center",
        ),
        height=240, width=280,
        margin=dict(t=10, b=40, l=30, r=30),
    )

    img_bytes = pio.to_image(fig, format="png", scale=2)
    return "data:image/png;base64," + base64.b64encode(img_bytes).decode()


# ── HTML de card por ciudad ───────────────────────────────────
def city_card_html(
    city: dict,
    rank: int,
    estimated_salary: float,
    donut_b64: str,
    insights: list[tuple[str, str]],
) -> str:
    tax     = city.get("tax_rate", 30)
    net     = estimated_salary * (1 - tax / 100)
    rent    = city.get("average_rent", 1000)
    savings = max(0, net - rent * 12)
    score   = city.get("relocation_score", 0)

    rank_colors = {1: "#f5f5f7", 2: "#aeaeb2", 3: "#8e8e93"}
    rc = rank_colors.get(rank, "#6e6e73")

    insights_html = "".join(
        f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:7px;">'
        f'<span style="font-size:14px;flex-shrink:0;">{emoji}</span>'
        f'<span style="font-size:9px;color:#aeaeb2;line-height:1.3;">{text}</span>'
        f'</div>'
        for emoji, text in insights
    )

    budget_legend = "".join(
        f'<div style="display:flex;align-items:center;gap:4px;margin-bottom:3px;">'
        f'<div style="width:6px;height:6px;border-radius:50%;background:'
        f'{["#f5f5f7","#aeaeb2","#8e8e93","#636366","#3a3a3c"][i]};flex-shrink:0;"></div>'
        f'<span style="font-size:8px;color:#6e6e73;">{k} {v:.0f}%</span>'
        f'</div>'
        for i, (k, v) in enumerate(
            sorted(
                {k: v for k, v in
                 [("Vivienda", city.get("_v",0)),
                  ("Aliment.", city.get("_a",0)),
                  ("Transp.", city.get("_t",0)),
                  ("Ocio", city.get("_o",0)),
                  ("Ahorro", city.get("_s",0))]}.items(),
                key=lambda x: -x[1]
            )
        )
    )

    return f"""
    <div style="
        background: #1c1c1e;
        border: 1px solid #2c2c2e;
        border-radius: 10px;
        padding: 16px;
        flex: 1;
        min-width: 0;
        display: flex;
        flex-direction: column;
        gap: 10px;
    ">
        <!-- Ciudad header -->
        <div>
            <div style="display:flex;align-items:baseline;gap:8px;margin-bottom:3px;">
                <span style="font-size:11px;font-weight:700;color:{rc};">#{rank}</span>
                <span style="font-size:16px;font-weight:800;color:#f5f5f7;
                letter-spacing:-0.02em;line-height:1;">
                    {city.get('city_name','').upper()}
                </span>
            </div>
            <div style="font-size:9px;color:#6e6e73;">
                {city.get('country','')} — {city.get('region','')}
            </div>
        </div>

        <!-- Métricas clave -->
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;">
            {_metric_mini("SAL. NETO EST.", f"€{net:,.0f}/año")}
            {_metric_mini("ALQUILER", f"€{rent:,.0f}/mes")}
            {_metric_mini("AHORRO ANUAL", f"€{savings:,.0f}")}
            {_metric_mini("IMPUESTOS", f"{tax:.0f}%")}
        </div>

        <!-- Relocation Score badge -->
        <div style="
            background: #2c2c2e;
            border-radius: 6px;
            padding: 7px 10px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        ">
            <span style="font-size:8px;color:#6e6e73;text-transform:uppercase;
            letter-spacing:0.08em;">Relocation Score</span>
            <span style="font-size:18px;font-weight:800;color:#f5f5f7;
            letter-spacing:-0.02em;">{score:.1f}</span>
        </div>

        <!-- Separador -->
        <div style="height:1px;background:#2c2c2e;"></div>

        <!-- Distribución del sueldo -->
        <div>
            <div style="font-size:8px;color:#6e6e73;text-transform:uppercase;
            letter-spacing:0.08em;margin-bottom:8px;">Distribución del sueldo neto</div>
            <div style="display:flex;align-items:center;gap:10px;">
                <img src="{donut_b64}" width="80" height="80"
                     style="flex-shrink:0;" />
                <div style="flex:1;">
                    {budget_legend}
                </div>
            </div>
        </div>

        <!-- Separador -->
        <div style="height:1px;background:#2c2c2e;"></div>

        <!-- Consideraciones clave -->
        <div>
            <div style="font-size:8px;color:#6e6e73;text-transform:uppercase;
            letter-spacing:0.08em;margin-bottom:8px;">Consideraciones clave</div>
            {insights_html}
        </div>

    </div>
    """


def _metric_mini(label: str, value: str) -> str:
    return f"""
    <div style="background:#2c2c2e;border-radius:6px;padding:7px 8px;">
        <div style="font-size:7px;color:#6e6e73;text-transform:uppercase;
        letter-spacing:0.07em;margin-bottom:2px;">{label}</div>
        <div style="font-size:11px;font-weight:700;color:#f5f5f7;
        letter-spacing:-0.01em;">{value}</div>
    </div>
    """


# ── HTML completo del poster ──────────────────────────────────
def build_poster_html(
    cities: list[dict],
    profile: dict,
    donuts: list[str],
    insights_list: list[list],
    radar_b64: str,
    budgets: list[dict],
) -> str:
    logo_b64  = get_logo_b64()
    fecha     = datetime.now().strftime("%d %b %Y")
    position  = profile.get("position", "—")
    exp       = profile.get("years_experience", 0)
    edu       = profile.get("education_level", "—")
    origin    = profile.get("origin_country", "—")
    estimated = profile.get("estimated_salary", 0) or 0

    logo_img = (
        f'<img src="{logo_b64}" width="28" height="28" style="flex-shrink:0;" />'
        if logo_b64 else "🧭"
    )

    radar_img = (
        f'<img src="{radar_b64}" width="260" height="220" style="display:block;" />'
        if radar_b64 else ""
    )

    # Inyectar budget en cities para la leyenda
    enriched_cities = []
    for city, budget in zip(cities, budgets):
        c = dict(city)
        items = list(budget.items())
        keys  = ["_v", "_a", "_t", "_o", "_s"]
        for k, (_, v) in zip(keys, items):
            c[k] = v
        enriched_cities.append(c)

    cards_html = "".join(
        city_card_html(city, i + 1, estimated, donut, insights)
        for i, (city, donut, insights) in enumerate(
            zip(enriched_cities, donuts, insights_list)
        )
    )

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}

  @page {{ size: A4 landscape; margin: 0; }}

  body {{
    width: 297mm;
    height: 210mm;
    background: #111111;
    color: #f5f5f7;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI',
                 'Helvetica Neue', Arial, sans-serif;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    padding: 14px 18px 12px;
    gap: 10px;
  }}

  .header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 10px;
    border-bottom: 1px solid #2c2c2e;
    flex-shrink: 0;
  }}

  .brand {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  .brand-name {{
    font-size: 14px;
    font-weight: 700;
    color: #f5f5f7;
    letter-spacing: -0.02em;
  }}

  .brand-sub {{
    font-size: 9px;
    color: #6e6e73;
    letter-spacing: 0.04em;
    margin-top: 1px;
  }}

  .header-center {{
    text-align: center;
  }}

  .header-title {{
    font-size: 12px;
    font-weight: 700;
    color: #f5f5f7;
    letter-spacing: 0.06em;
    text-transform: uppercase;
  }}

  .header-sub {{
    font-size: 8px;
    color: #6e6e73;
    margin-top: 2px;
    letter-spacing: 0.04em;
  }}

  .header-meta {{
    font-size: 9px;
    color: #6e6e73;
    text-align: right;
    line-height: 1.5;
  }}

  .main {{
    display: flex;
    gap: 12px;
    flex: 1;
    min-height: 0;
  }}

  .left-panel {{
    width: 175px;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    gap: 10px;
  }}

  .profile-card {{
    background: #1c1c1e;
    border: 1px solid #2c2c2e;
    border-radius: 10px;
    padding: 12px;
    flex-shrink: 0;
  }}

  .profile-label {{
    font-size: 8px;
    color: #6e6e73;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 6px;
  }}

  .profile-position {{
    font-size: 13px;
    font-weight: 700;
    color: #f5f5f7;
    letter-spacing: -0.01em;
    margin-bottom: 4px;
    line-height: 1.2;
  }}

  .profile-detail {{
    font-size: 9px;
    color: #aeaeb2;
    margin-bottom: 2px;
    line-height: 1.3;
  }}

  .salary-badge {{
    background: #2c2c2e;
    border: 1px solid #3a3a3c;
    border-radius: 8px;
    padding: 8px 10px;
    margin-top: 10px;
  }}

  .salary-label {{
    font-size: 8px;
    color: #6e6e73;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 2px;
  }}

  .salary-value {{
    font-size: 18px;
    font-weight: 800;
    color: #f5f5f7;
    letter-spacing: -0.03em;
    line-height: 1;
  }}

  .salary-sub {{
    font-size: 8px;
    color: #6e6e73;
    margin-top: 2px;
  }}

  .radar-card {{
    background: #1c1c1e;
    border: 1px solid #2c2c2e;
    border-radius: 10px;
    padding: 10px;
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 0;
  }}

  .radar-label {{
    font-size: 8px;
    color: #6e6e73;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
    align-self: flex-start;
  }}

  .right-panel {{
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
    min-width: 0;
  }}

  .cities-label {{
    font-size: 8px;
    color: #6e6e73;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    flex-shrink: 0;
  }}

  .cities-grid {{
    display: flex;
    gap: 10px;
    flex: 1;
    min-height: 0;
  }}

  .footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 8px;
    border-top: 1px solid #1c1c1e;
    flex-shrink: 0;
  }}

  .footer-text {{
    font-size: 8px;
    color: #3a3a3c;
  }}

  @media print {{
    body {{
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
  }}
</style>
</head>
<body>

  <!-- HEADER -->
  <div class="header">
    <div class="brand">
      {logo_img}
      <div>
        <div class="brand-name">RelocationDevs</div>
        <div class="brand-sub">by a Cambeiro</div>
      </div>
    </div>
    <div class="header-center">
      <div class="header-title">Informe de Reubicación</div>
      <div class="header-sub">
        Análisis personalizado basado en tu perfil profesional
      </div>
    </div>
    <div class="header-meta">
      <div>{fecha}</div>
      <div>github.com/Udamian/RelocationDevs</div>
    </div>
  </div>

  <!-- MAIN -->
  <div class="main">

    <!-- PANEL IZQUIERDO -->
    <div class="left-panel">

      <div class="profile-card">
        <div class="profile-label">Tu perfil</div>
        <div class="profile-position">{position}</div>
        <div class="profile-detail">
          ESTADO: Desde {origin}
        </div>
        <div class="profile-detail">{exp} años · {edu}</div>
        <div class="salary-badge">
          <div class="salary-label">Salario estimado</div>
          <div class="salary-value">€{estimated:,.0f}</div>
          <div class="salary-sub">bruto anual</div>
        </div>
      </div>

      <div class="radar-card">
        <div class="radar-label">Comparativa</div>
        {radar_img}
      </div>

    </div>

    <!-- PANEL DERECHO -->
    <div class="right-panel">
      <div class="cities-label">
        Ciudades recomendadas para tu perfil
      </div>
      <div class="cities-grid">
        {cards_html}
      </div>
    </div>

  </div>

  <!-- FOOTER -->
  <div class="footer">
    <div class="footer-text">RelocationDevs · by a Cambeiro · 2025</div>
    <div class="footer-text">
      Datos: Stack Overflow Developer Survey 2023 ·
      Kaggle Cost of Living Index · OECD Tax Database
    </div>
    <div class="footer-text">github.com/Udamian/RelocationDevs</div>
  </div>

</body>
</html>"""


# ── Módulo Streamlit ──────────────────────────────────────────
def render():
    page_header(
        "Informe de reubicación",
        "Genera tu poster personalizado — DIN A4 horizontal · Fondo negro"
    )

    df_path = PROCESSED / "cities_processed.csv"
    if not df_path.exists():
        st.warning("Sin datos procesados. Ejecuta primero el notebook 02_indicators.ipynb.")
        return

    df      = pd.read_csv(df_path)
    profile = st.session_state.get("profile", {})
    estimated = profile.get("estimated_salary", 0) or 0

    # ── Selección de ciudades ──────────────────────────────────
    st.markdown("""
    <p style="font-size:11px;font-weight:600;color:#6e6e73;
    letter-spacing:0.1em;text-transform:uppercase;margin-bottom:16px;">
        Ciudades del informe
    </p>
    """, unsafe_allow_html=True)

    finder_cities = []
    if st.session_state.get("finder_step", 0) == 3:
        try:
            from app.city_finder import compute_compatibility
            prefs    = st.session_state.get("finder", {})
            df_res   = compute_compatibility(df, prefs, profile)
            finder_cities = df_res.head(3)["city_name"].tolist()
        except Exception:
            pass

    all_cities = sorted(df["city_name"].unique().tolist())
    default    = [c for c in finder_cities if c in all_cities][:3]

    selected = st.multiselect(
        "Selecciona hasta 3 ciudades",
        all_cities,
        default=default,
        max_selections=3,
        help="Por defecto se usan las ciudades del Buscador si has realizado una búsqueda"
    )

    if not selected:
        st.markdown("""
        <div style="background:#1c1c1e;border:1px solid #2c2c2e;
        border-radius:12px;padding:32px;text-align:center;margin-top:16px;">
            <p style="font-size:14px;color:#6e6e73;">
                Selecciona al menos una ciudad para generar el informe.
            </p>
        </div>
        """, unsafe_allow_html=True)
        return

    cities_data = []
    for name in selected:
        row = df[df["city_name"] == name]
        if not row.empty:
            cities_data.append(row.iloc[0].to_dict())

    # ── Preview rápido ─────────────────────────────────────────
    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
    cols = st.columns(len(cities_data))
    rank_icons = ["🥇", "🥈", "🥉"]

    for i, (col, city) in enumerate(zip(cols, cities_data)):
        tax     = city.get("tax_rate", 30)
        net     = estimated * (1 - tax / 100)
        rent    = city.get("average_rent", 1000)
        savings = max(0, net - rent * 12)
        score   = city.get("relocation_score", 0)
        budget  = compute_budget_distribution(city, estimated)

        with col:
            st.markdown(f"""
            <div style="background:#1c1c1e;border:1px solid #2c2c2e;
            border-radius:12px;padding:18px;text-align:center;">
                <div style="font-size:12px;margin-bottom:4px;">{rank_icons[i]}</div>
                <div style="font-size:16px;font-weight:700;color:#f5f5f7;
                letter-spacing:-0.02em;margin-bottom:6px;">
                    {city.get('city_name','')}
                </div>
                <div style="font-size:11px;color:#aeaeb2;margin-bottom:2px;">
                    Neto €{net:,.0f}/año
                </div>
                <div style="font-size:11px;color:#aeaeb2;margin-bottom:2px;">
                    Alquiler €{rent:,.0f}/mes
                </div>
                <div style="font-size:11px;color:#aeaeb2;margin-bottom:8px;">
                    Ahorro €{savings:,.0f}/año · {budget['Ahorro']:.0f}% del neto
                </div>
                <div style="font-size:22px;font-weight:700;color:#f5f5f7;">
                    {score:.1f}
                </div>
                <div style="font-size:9px;color:#6e6e73;text-transform:uppercase;
                letter-spacing:0.06em;">relocation score</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Botón generar ──────────────────────────────────────────
    st.markdown("<div style='height:24px;'></div>", unsafe_allow_html=True)
    _, col_btn, _ = st.columns([1, 2, 1])

    with col_btn:
        if st.button("Generar poster PDF →", type="primary", use_container_width=True):
            with st.spinner("Generando imágenes y componiendo el poster..."):
                try:
                    budgets       = [compute_budget_distribution(c, estimated) for c in cities_data]
                    insights_list = [get_key_insights(c, b) for c, b in zip(cities_data, budgets)]
                    donuts        = [build_donut_b64(b, size=160) for b in budgets]
                    radar_b64     = build_radar_b64(cities_data)

                    poster_html = build_poster_html(
                        cities_data, profile, donuts,
                        insights_list, radar_b64, budgets
                    )

                    st.download_button(
                        label="⬇ Descargar HTML → Ctrl+P en navegador → Guardar PDF (horizontal, sin márgenes)",
                        data=poster_html.encode("utf-8"),
                        file_name=f"RelocationDevs_{datetime.now().strftime('%Y%m%d')}.html",
                        mime="text/html",
                        use_container_width=True,
                    )

                    st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
                    st.markdown("""
                    <p style="font-size:11px;font-weight:600;color:#6e6e73;
                    letter-spacing:0.1em;text-transform:uppercase;margin-bottom:12px;">
                        Preview
                    </p>
                    """, unsafe_allow_html=True)
                    st.components.v1.html(poster_html, height=520, scrolling=False)

                except Exception as e:
                    st.error(f"Error al generar el poster: {e}")
                    st.caption("Asegúrate de tener kaleido instalado: pip install kaleido")