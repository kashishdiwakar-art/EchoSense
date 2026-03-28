import streamlit as st

# ─────────────────────────────────────────────────────────────
# THEME TOKENS
# ─────────────────────────────────────────────────────────────
PALETTE = {
    "bg":           "#0d1f0e",   # deep forest black-green
    "surface":      "#122614",   # card surface
    "surface2":     "#1a3320",   # elevated surface
    "border":       "#2d5c35",   # subtle border
    "accent":       "#4ade80",   # neon leaf green
    "accent2":      "#86efac",   # soft mint
    "accent3":      "#fbbf24",   # warm amber
    "text":         "#e2f5e4",   # near-white green tint
    "text_muted":   "#6b9e74",   # muted paragraph text
    "danger":       "#f87171",   # warning red
    "bird":         "#38bdf8",   # sky blue
    "frog":         "#4ade80",   # leaf green
    "insect":       "#fbbf24",   # amber
    "mammal":       "#f472b6",   # rose pink
}

CATEGORY_META = {
    "birds":    {"emoji": "🐦", "color": PALETTE["bird"],    "label": "Bird"},
    "frogs":    {"emoji": "🐸", "color": PALETTE["frog"],    "label": "Amphibian"},
    "insects":  {"emoji": "🦗", "color": PALETTE["insect"],  "label": "Insect"},
    "mammals":  {"emoji": "🦊", "color": PALETTE["mammal"],  "label": "Mammal"},
    "unknown":  {"emoji": "❓", "color": PALETTE["text_muted"], "label": "Unknown"},
}

SPECIES_FACTS = {
    # Birds
    "Barn Owl":            "Silent hunters — their heart-shaped face acts as a natural sound dish.",
    "Common Cuckoo":       "Famous for laying eggs in other birds' nests — nature's ultimate con artist.",
    "Common Nightingale":  "Can sing over 200 distinct song types. Males sing through the night to attract mates.",
    "Blue Jay":            "Can mimic hawk calls to scare other birds away from food sources.",
    "Common Loon":         "Their haunting call echoes across lakes and can be heard from 10km away.",
    "Bald Eagle":          "Their iconic call is surprisingly high-pitched — almost a giggle.",
    # Frogs
    "American Bullfrog":   "The deepest frog call in North America. Their jug-o-rum can carry 1.5km.",
    "Spring Peeper":       "Tiny frog, massive chorus. A colony of 1000 peepers can exceed 90 decibels.",
    "Gray Tree Frog":      "Can survive being frozen solid during winter by producing natural antifreeze.",
    "Common Frog":         "First frog to call in spring — a single male can trigger an entire pond chorus.",
    # Insects
    "Honeybee":            "Bees communicate the location of flowers through complex waggle dances.",
    "Field Cricket":       "Only male crickets chirp — they rub their wings together, not their legs.",
    "Cicada":              "Some cicada species wait 17 years underground before emerging to sing.",
    "Mosquito":            "Female mosquitoes hum at 400Hz; males tune their wings to match when attracted.",
    # Mammals
    "Gray Wolf":           "Wolf howls can synchronize an entire pack over distances of 10km.",
    "Common Pipistrelle Bat": "Emits 200 ultrasonic pulses per second while hunting insects at night.",
    "African Lion":        "A lion's roar can be heard from 8km away and is used to mark territory.",
    "Chimpanzee":          "Their pant-hoots are unique signatures — each individual has a distinct voice.",
}


# ─────────────────────────────────────────────────────────────
# MAIN CSS INJECTION
# ─────────────────────────────────────────────────────────────
GLOBAL_CSS = f"""
<style>
/* ── Google Fonts ─────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

/* ── CSS Variables ────────────────────────────── */
:root {{
    --bg:         {PALETTE['bg']};
    --surface:    {PALETTE['surface']};
    --surface2:   {PALETTE['surface2']};
    --border:     {PALETTE['border']};
    --accent:     {PALETTE['accent']};
    --accent2:    {PALETTE['accent2']};
    --accent3:    {PALETTE['accent3']};
    --text:       {PALETTE['text']};
    --muted:      {PALETTE['text_muted']};
    --danger:     {PALETTE['danger']};
    --bird:       {PALETTE['bird']};
    --frog:       {PALETTE['frog']};
    --insect:     {PALETTE['insect']};
    --mammal:     {PALETTE['mammal']};
    --radius:     14px;
    --radius-lg:  22px;
    --shadow:     0 8px 32px rgba(0,0,0,0.45);
    --glow:       0 0 24px rgba(74,222,128,0.18);
}}

/* ── Global Reset & Body ──────────────────────── */
html, body, [class*="css"] {{
    font-family: 'Outfit', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}}

/* ── Hide Streamlit Chrome ────────────────────── */
#MainMenu, footer, header {{ visibility: hidden; }}
.stDeployButton {{ display: none; }}

/* ── App Container ────────────────────────────── */
.main .block-container {{
    padding: 1.5rem 2rem 3rem 2rem;
    max-width: 1100px;
}}

/* ── Scrollbar ────────────────────────────────── */
::-webkit-scrollbar {{ width: 6px; }}
::-webkit-scrollbar-track {{ background: var(--surface); }}
::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 3px; }}

/* ── Hero Header ──────────────────────────────── */
.echo-hero {{
    background: linear-gradient(135deg, #0f2e12 0%, #153a1a 50%, #0d1f0e 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 2.8rem 2.4rem 2.2rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow), var(--glow);
}}
.echo-hero::before {{
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(ellipse at 20% 50%, rgba(74,222,128,0.06) 0%, transparent 65%),
                radial-gradient(ellipse at 80% 20%, rgba(56,189,248,0.05) 0%, transparent 55%);
    pointer-events: none;
}}
.echo-hero-title {{
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 60%, var(--accent3) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.3rem 0;
    line-height: 1.1;
}}
.echo-hero-sub {{
    font-size: 1.05rem;
    color: var(--muted);
    font-weight: 400;
    margin: 0;
    letter-spacing: 0.01em;
}}
.echo-hero-badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(74,222,128,0.12);
    border: 1px solid rgba(74,222,128,0.3);
    color: var(--accent);
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    padding: 4px 10px;
    border-radius: 20px;
    margin-bottom: 1rem;
    letter-spacing: 0.08em;
}}
.echo-pulse {{
    width: 7px; height: 7px;
    background: var(--accent);
    border-radius: 50%;
    animation: pulse-dot 1.8s ease-in-out infinite;
    display: inline-block;
}}
@keyframes pulse-dot {{
    0%, 100% {{ opacity: 1; transform: scale(1); }}
    50%       {{ opacity: 0.4; transform: scale(0.7); }}
}}

/* ── Upload Zone ──────────────────────────────── */
.upload-zone {{
    background: var(--surface);
    border: 2px dashed var(--border);
    border-radius: var(--radius-lg);
    padding: 2.5rem 2rem;
    text-align: center;
    transition: border-color 0.25s, background 0.25s;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}}
.upload-zone:hover {{
    border-color: var(--accent);
    background: var(--surface2);
}}
.upload-icon {{
    font-size: 3.2rem;
    display: block;
    margin-bottom: 0.6rem;
    animation: float 3s ease-in-out infinite;
}}
@keyframes float {{
    0%, 100% {{ transform: translateY(0px); }}
    50%       {{ transform: translateY(-6px); }}
}}
.upload-label {{
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text);
    margin: 0 0 0.2rem;
}}
.upload-hint {{
    font-size: 0.82rem;
    color: var(--muted);
    font-family: 'Space Mono', monospace;
}}

/* ── Streamlit file uploader override ─────────── */
[data-testid="stFileUploader"] {{
    background: transparent !important;
    border: none !important;
}}
[data-testid="stFileUploader"] > div {{
    background: var(--surface) !important;
    border: 2px dashed var(--border) !important;
    border-radius: var(--radius-lg) !important;
    transition: border-color 0.25s;
}}
[data-testid="stFileUploader"] > div:hover {{
    border-color: var(--accent) !important;
}}
[data-testid="stFileUploaderDropzoneInstructions"] {{
    color: var(--muted) !important;
}}

/* ── Result Card ──────────────────────────────── */
.result-card {{
    background: linear-gradient(135deg, var(--surface) 0%, var(--surface2) 100%);
    border: 1px solid var(--border);
    border-radius: var(--radius-lg);
    padding: 2rem;
    margin: 1.2rem 0;
    box-shadow: var(--shadow);
    animation: slide-up 0.4s cubic-bezier(0.16,1,0.3,1) both;
    position: relative;
    overflow: hidden;
}}
.result-card::after {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2), var(--accent3));
    border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}}
@keyframes slide-up {{
    from {{ opacity: 0; transform: translateY(20px); }}
    to   {{ opacity: 1; transform: translateY(0); }}
}}
.result-species {{
    font-size: 2.2rem;
    font-weight: 800;
    color: var(--accent);
    margin: 0.3rem 0 0.2rem;
    letter-spacing: -0.5px;
}}
.result-category {{
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 1.2rem;
}}
.result-emoji {{
    font-size: 4rem;
    line-height: 1;
    display: block;
    margin-bottom: 0.5rem;
    filter: drop-shadow(0 0 12px rgba(74,222,128,0.3));
}}

/* ── Confidence Bar ───────────────────────────── */
.conf-wrap {{
    margin: 1rem 0;
}}
.conf-label {{
    display: flex;
    justify-content: space-between;
    font-size: 0.82rem;
    color: var(--muted);
    font-family: 'Space Mono', monospace;
    margin-bottom: 6px;
}}
.conf-track {{
    background: rgba(255,255,255,0.06);
    border-radius: 99px;
    height: 10px;
    overflow: hidden;
}}
.conf-fill {{
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, var(--accent), var(--accent3));
    box-shadow: 0 0 10px rgba(74,222,128,0.4);
    transition: width 1s cubic-bezier(0.16,1,0.3,1);
    animation: fill-anim 1s cubic-bezier(0.16,1,0.3,1) both;
}}
@keyframes fill-anim {{
    from {{ width: 0; }}
}}

/* ── Top-3 Bars ───────────────────────────────── */
.top3-row {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 8px;
}}
.top3-name {{
    font-size: 0.82rem;
    color: var(--text);
    min-width: 160px;
    font-weight: 500;
}}
.top3-track {{
    flex: 1;
    background: rgba(255,255,255,0.06);
    border-radius: 99px;
    height: 7px;
    overflow: hidden;
}}
.top3-fill {{
    height: 100%;
    border-radius: 99px;
    opacity: 0.8;
    animation: fill-anim 0.8s cubic-bezier(0.16,1,0.3,1) both;
}}
.top3-pct {{
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: var(--muted);
    min-width: 45px;
    text-align: right;
}}

/* ── Fact Card ────────────────────────────────── */
.fact-card {{
    background: rgba(74,222,128,0.06);
    border-left: 3px solid var(--accent);
    border-radius: 0 var(--radius) var(--radius) 0;
    padding: 1rem 1.2rem;
    margin: 1rem 0;
    font-size: 0.9rem;
    color: var(--text);
    font-style: italic;
    line-height: 1.6;
}}
.fact-card::before {{
    content: '💡 ';
}}

/* ── Info Chip ────────────────────────────────── */
.chip {{
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 12px;
    border-radius: 99px;
    font-size: 0.78rem;
    font-weight: 600;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.04em;
    margin-right: 6px;
    margin-bottom: 6px;
}}
.chip-green  {{ background: rgba(74,222,128,0.12); color: var(--accent);  border: 1px solid rgba(74,222,128,0.25); }}
.chip-blue   {{ background: rgba(56,189,248,0.12); color: var(--bird);    border: 1px solid rgba(56,189,248,0.25); }}
.chip-amber  {{ background: rgba(251,191,36,0.12); color: var(--accent3); border: 1px solid rgba(251,191,36,0.25); }}
.chip-red    {{ background: rgba(248,113,113,0.12); color: var(--danger); border: 1px solid rgba(248,113,113,0.25); }}

/* ── Section Divider ──────────────────────────── */
.section-head {{
    font-size: 0.72rem;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 1.6rem 0 0.7rem;
    display: flex;
    align-items: center;
    gap: 10px;
}}
.section-head::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}}

/* ── Waveform Container ───────────────────────── */
.wave-container {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.8rem;
    overflow: hidden;
}}

/* ── Stat Pill ────────────────────────────────── */
.stat-grid {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin: 1rem 0;
}}
.stat-pill {{
    background: var(--surface2);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 0.85rem 1rem;
    text-align: center;
}}
.stat-val {{
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--accent);
    font-family: 'Space Mono', monospace;
    display: block;
}}
.stat-key {{
    font-size: 0.68rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 2px;
    display: block;
}}

/* ── Sidebar ──────────────────────────────────── */
[data-testid="stSidebar"] {{
    background: var(--surface) !important;
    border-right: 1px solid var(--border) !important;
}}
[data-testid="stSidebar"] .stMarkdown p {{
    color: var(--muted);
    font-size: 0.85rem;
}}

/* ── Buttons ──────────────────────────────────── */
.stButton > button {{
    background: linear-gradient(135deg, #1f5c28, #2e7d32) !important;
    color: var(--accent2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.2s !important;
    letter-spacing: 0.01em !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important;
}}
.stButton > button:hover {{
    background: linear-gradient(135deg, #2e7d32, #388e3c) !important;
    box-shadow: 0 4px 16px rgba(74,222,128,0.2) !important;
    transform: translateY(-1px) !important;
}}

/* ── Audio Player ─────────────────────────────── */
audio {{
    width: 100%;
    filter: invert(0.85) hue-rotate(100deg);
    border-radius: 8px;
    margin: 0.5rem 0;
}}

/* ── Spinner override ─────────────────────────── */
.stSpinner > div {{
    border-color: var(--accent) transparent transparent transparent !important;
}}

/* ── Tabs ─────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {{
    background: var(--surface) !important;
    border-radius: var(--radius) var(--radius) 0 0;
    gap: 4px;
    padding: 4px;
    border-bottom: 1px solid var(--border);
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent !important;
    color: var(--muted) !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500 !important;
    border-radius: 8px !important;
    padding: 0.4rem 1rem !important;
    transition: all 0.2s !important;
}}
.stTabs [aria-selected="true"] {{
    background: var(--surface2) !important;
    color: var(--accent) !important;
    font-weight: 600 !important;
}}

/* ── Error / Warning Box ──────────────────────── */
.echo-error {{
    background: rgba(248,113,113,0.08);
    border: 1px solid rgba(248,113,113,0.25);
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    color: var(--danger);
    font-size: 0.88rem;
    margin: 0.8rem 0;
}}
.echo-warning {{
    background: rgba(251,191,36,0.08);
    border: 1px solid rgba(251,191,36,0.25);
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    color: var(--accent3);
    font-size: 0.88rem;
    margin: 0.8rem 0;
}}

/* ── Footer ───────────────────────────────────── */
.echo-footer {{
    text-align: center;
    padding: 2rem 0 1rem;
    color: var(--muted);
    font-size: 0.78rem;
    font-family: 'Space Mono', monospace;
    border-top: 1px solid var(--border);
    margin-top: 3rem;
}}
</style>
"""


# ─────────────────────────────────────────────────────────────
# HTML COMPONENT BUILDERS
# ─────────────────────────────────────────────────────────────
def inject_css():
    """Call once at app start to inject all styles."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def hero_header():
    """Render the EchoSense hero banner."""
    st.markdown("""
    <div class="echo-hero">
        <div class="echo-hero-badge">
            <span class="echo-pulse"></span>
            BIOACOUSTIC AI · IoT READY
        </div>
        <h1 class="echo-hero-title">🎙️ EchoSense</h1>
        <p class="echo-hero-sub">
            Upload any wildlife audio and instantly identify the species —
            birds, frogs, insects &amp; mammals.
        </p>
    </div>
    """, unsafe_allow_html=True)


def section_divider(label):
    st.markdown(f'<div class="section-head">{label}</div>',
                unsafe_allow_html=True)


def confidence_bar(value, label="Confidence"):
    """Render animated confidence progress bar."""
    pct = int(value * 100)
    color = "#4ade80" if pct >= 70 else ("#fbbf24" if pct >= 45 else "#f87171")
    st.markdown(f"""
    <div class="conf-wrap">
        <div class="conf-label">
            <span>{label}</span>
            <span style="color:{color}; font-weight:700">{pct}%</span>
        </div>
        <div class="conf-track">
            <div class="conf-fill" style="width:{pct}%; background:linear-gradient(90deg,{color},{color}aa);"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def top3_bars(top3_list):
    """Render top-3 species probability bars."""
    colors = ["#4ade80", "#86efac", "#bbf7d0"]
    html   = ""
    for i, item in enumerate(top3_list):
        pct   = int(item["confidence"] * 100)
        color = colors[i] if i < len(colors) else "#6b9e74"
        html += f"""
        <div class="top3-row">
            <span class="top3-name">{'🥇' if i==0 else '🥈' if i==1 else '🥉'} {item['species']}</span>
            <div class="top3-track">
                <div class="top3-fill" style="width:{pct}%; background:{color};"></div>
            </div>
            <span class="top3-pct">{pct}%</span>
        </div>"""
    st.markdown(html, unsafe_allow_html=True)


def result_card(result):
    """Render the main prediction result card."""
    meta = CATEGORY_META.get(result.get("category","").lower(),
                              CATEGORY_META["unknown"])
    species  = result.get("species", "Unknown")
    category = meta["label"]
    emoji    = meta["emoji"]
    color    = meta["color"]
    conf_pct = int(result.get("confidence", 0) * 100)

    st.markdown(f"""
    <div class="result-card">
        <span class="result-emoji">{emoji}</span>
        <div class="result-species" style="color:{color}">{species}</div>
        <div class="result-category">{category.upper()} · {conf_pct}% CONFIDENCE</div>
    </div>
    """, unsafe_allow_html=True)


def fact_box(species_name):
    """Render a fun fact about the species if available."""
    fact = SPECIES_FACTS.get(species_name)
    if fact:
        st.markdown(f'<div class="fact-card">{fact}</div>',
                    unsafe_allow_html=True)


def stat_grid(duration, sample_rate, file_size_kb):
    """Render audio stats strip."""
    st.markdown(f"""
    <div class="stat-grid">
        <div class="stat-pill">
            <span class="stat-val">{duration:.1f}s</span>
            <span class="stat-key">Duration</span>
        </div>
        <div class="stat-pill">
            <span class="stat-val">{sample_rate//1000}kHz</span>
            <span class="stat-key">Sample Rate</span>
        </div>
        <div class="stat-pill">
            <span class="stat-val">{file_size_kb:.0f}KB</span>
            <span class="stat-key">File Size</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def echo_footer():
    st.markdown("""
    <div class="echo-footer">
        EchoSense v1.0 · Biodiversity Audio Intelligence ·
        Built for hackathon demo — no AI tools used
    </div>
    """, unsafe_allow_html=True)