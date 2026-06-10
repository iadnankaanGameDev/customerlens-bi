import streamlit as st


def apply_custom_css():
    st.markdown(
        """
<style>
/* ============================================================
   CustomerLens BI - Premium Dark Theme
   Cleaned + stronger Streamlit/BaseWeb overrides
   ============================================================ */

:root {
  --bg-main: #07111f;
  --bg-deep: #020617;
  --surface: rgba(15, 23, 42, 0.86);
  --surface-soft: rgba(30, 41, 59, 0.72);
  --surface-hover: rgba(51, 65, 85, 0.54);
  --panel: rgba(8, 13, 27, 0.88);
  --border: rgba(148, 163, 184, 0.18);
  --border-soft: rgba(148, 163, 184, 0.10);
  --border-accent: rgba(56, 189, 248, 0.34);
  --text: #f8fafc;
  --text-soft: #dbe4ef;
  --muted: #b6c4d6;
  --muted-2: #8da0b8;
  --accent: #38bdf8;
  --accent-2: #14b8a6;
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #fb7185;
  --shadow: 0 28px 80px rgba(0, 0, 0, 0.38);
  --radius: 18px;
}

/* ============================================================
   Main canvas
   ============================================================ */

.stApp {
  background:
    radial-gradient(circle at 10% 0%, rgba(56, 189, 248, 0.12), transparent 32rem),
    radial-gradient(circle at 90% 12%, rgba(20, 184, 166, 0.10), transparent 28rem),
    linear-gradient(180deg, #07111f 0%, #0b1220 52%, #020617 100%);
  color: var(--text);
}

.block-container {
  max-width: 1180px;
  padding-top: 3rem;
  padding-bottom: 4rem;
}

/* Typography */
h1, h2, h3, h4, h5, h6, p, label, span, div {
  color: var(--text);
}

h1 {
  letter-spacing: -0.06em;
  font-weight: 900;
}

h2, h3 {
  letter-spacing: -0.035em;
}

p, li {
  color: var(--text-soft);
}

/* ============================================================
   Sidebar
   ============================================================ */

[data-testid="stSidebar"] {
  background:
    radial-gradient(circle at top, rgba(56, 189, 248, 0.11), transparent 18rem),
    linear-gradient(180deg, rgba(2, 6, 23, 0.98), rgba(15, 23, 42, 0.96));
  border-right: 1px solid var(--border-soft);
}

[data-testid="stSidebar"] .block-container {
  padding-top: 2rem;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
  color: #f8fafc;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
  color: var(--text-soft);
}

/* ============================================================
   Hero
   ============================================================ */

.hero-card {
  position: relative;
  padding: 2.05rem 2.1rem 1.85rem 2.1rem;
  border-radius: 26px;
  background:
    linear-gradient(135deg, rgba(15, 23, 42, 0.92), rgba(19, 38, 55, 0.76)),
    radial-gradient(circle at 12% 0%, rgba(56, 189, 248, 0.16), transparent 22rem);
  border: 1px solid rgba(148, 163, 184, 0.18);
  box-shadow: var(--shadow);
  overflow: hidden;
  margin-bottom: 1.35rem;
}

.hero-card::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 96% 8%, rgba(20, 184, 166, 0.15), transparent 22rem),
    linear-gradient(90deg, rgba(56, 189, 248, 0.10), transparent 42%);
  pointer-events: none;
}

.hero-eyebrow {
  position: relative;
  display: inline-flex;
  align-items: center;
  padding: 0.38rem 0.78rem;
  border-radius: 999px;
  border: 1px solid rgba(56, 189, 248, 0.30);
  background: rgba(8, 47, 73, 0.32);
  color: #bae6fd;
  font-size: 0.76rem;
  font-weight: 750;
  margin-bottom: 0.9rem;
}

.hero-title {
  position: relative;
  font-size: clamp(2.25rem, 5vw, 4.1rem);
  line-height: 0.95;
  font-weight: 950;
  letter-spacing: -0.078em;
  margin: 0;
  color: #f8fafc;
}

.hero-subtitle {
  position: relative;
  max-width: 780px;
  color: var(--muted);
  font-size: 1rem;
  line-height: 1.75;
  margin-top: 1rem;
  margin-bottom: 1.3rem;
}

.hero-grid {
  position: relative;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 0.85rem;
  margin-top: 1rem;
}

.hero-mini-card {
  padding: 0.95rem 1rem;
  border-radius: 17px;
  background: rgba(2, 6, 23, 0.38);
  border: 1px solid rgba(148, 163, 184, 0.14);
}

.hero-mini-label {
  color: var(--muted-2);
  font-size: 0.70rem;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  margin-bottom: 0.3rem;
}

.hero-mini-value {
  color: #f1f5f9;
  font-size: 0.9rem;
  font-weight: 760;
}

/* ============================================================
   Workflow / sections / KPI
   ============================================================ */

.step-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.8rem;
  margin: 1rem 0 1.35rem 0;
}

.step-card {
  padding: 1rem;
  border-radius: 18px;
  background: linear-gradient(180deg, rgba(15, 23, 42, 0.72), rgba(2, 6, 23, 0.48));
  border: 1px solid rgba(148, 163, 184, 0.13);
  box-shadow: 0 18px 45px rgba(0, 0, 0, 0.18);
}

.step-number {
  color: var(--accent);
  font-weight: 850;
  font-size: 0.72rem;
  letter-spacing: 0.08em;
  margin-bottom: 0.35rem;
}

.step-title {
  color: #f8fafc;
  font-weight: 800;
  font-size: 0.94rem;
  margin-bottom: 0.28rem;
}

.step-copy {
  color: var(--muted) !important;
  font-size: 0.78rem;
  line-height: 1.45;
}

.section-card {
  padding: 1.25rem 1.3rem;
  border-radius: 20px;
  background:
    linear-gradient(180deg, rgba(15, 23, 42, 0.78), rgba(2, 6, 23, 0.50));
  border: 1px solid rgba(148, 163, 184, 0.13);
  box-shadow: 0 18px 55px rgba(0, 0, 0, 0.18);
  margin: 1.1rem 0;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  font-size: 1.28rem;
  font-weight: 850;
  letter-spacing: -0.04em;
  margin-bottom: 0.38rem;
  color: #f8fafc;
}

.section-caption {
  color: var(--muted) !important;
  font-size: 0.91rem;
  line-height: 1.65;
}

.kpi-card {
  padding: 1.05rem 1.1rem;
  background:
    linear-gradient(180deg, rgba(30, 41, 59, 0.84), rgba(15, 23, 42, 0.88));
  border: 1px solid rgba(148, 163, 184, 0.15);
  border-radius: 18px;
  box-shadow: 0 18px 55px rgba(0, 0, 0, 0.24);
}

.kpi-label {
  color: var(--muted);
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: 0.42rem;
}

.kpi-value {
  color: #f8fafc;
  font-size: 1.55rem;
  font-weight: 850;
  letter-spacing: -0.04em;
}

/* ============================================================
   Cluster naming
   ============================================================ */

.cluster-name-card {
  padding: 1rem;
  border-radius: 16px;
  background: rgba(15, 23, 42, 0.66);
  border: 1px solid rgba(148, 163, 184, 0.14);
  margin-bottom: 0.55rem;
}

.cluster-name-title {
  font-weight: 820;
  color: #f8fafc;
  margin-bottom: 0.25rem;
}

.cluster-name-meta {
  color: var(--muted) !important;
  font-size: 0.83rem;
  line-height: 1.55;
}

/* ============================================================
   Custom dark tables
   ============================================================ */

.dark-table-wrap {
  width: 100%;
  max-height: 520px;
  overflow: auto;
  border-radius: 16px;
  border: 1px solid rgba(148, 163, 184, 0.16);
  background: rgba(2, 6, 23, 0.34);
  box-shadow: 0 18px 45px rgba(0, 0, 0, 0.18);
}

.dark-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.82rem;
  color: #f1f5f9 !important;
}

.dark-table thead th {
  position: sticky;
  top: 0;
  z-index: 2;
  background: #132238 !important;
  color: #f8fafc !important;
  text-align: left;
  padding: 0.72rem 0.85rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.20);
  white-space: nowrap;
  font-weight: 800 !important;
}

.dark-table tbody td {
  padding: 0.64rem 0.85rem;
  border-bottom: 1px solid rgba(148, 163, 184, 0.09);
  color: #e2e8f0 !important;
  white-space: nowrap;
}

.dark-table tbody tr:nth-child(even) {
  background: rgba(30, 41, 59, 0.42) !important;
}

.dark-table tbody tr:nth-child(odd) {
  background: rgba(15, 23, 42, 0.46) !important;
}

.dark-table tbody tr:hover {
  background: rgba(56, 189, 248, 0.08);
}

.column-pill-wrap {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  padding: 0.9rem;
  border-radius: 16px;
  background: rgba(2, 6, 23, 0.34);
  border: 1px solid rgba(148, 163, 184, 0.14);
}

.column-pill {
  display: inline-flex;
  padding: 0.32rem 0.58rem;
  border-radius: 999px;
  background: rgba(8, 47, 73, 0.38);
  border: 1px solid rgba(56, 189, 248, 0.22);
  color: #bae6fd;
  font-size: 0.76rem;
  font-weight: 650;
}

/* ============================================================
   Streamlit containers
   ============================================================ */

[data-testid="stMetric"],
[data-testid="stExpander"],
.stPlotlyChart {
  background: rgba(15, 23, 42, 0.58);
  border: 1px solid rgba(148, 163, 184, 0.13);
  border-radius: 18px;
}

[data-testid="stExpander"] {
  overflow: hidden;
}

[data-testid="stExpander"] summary {
  color: #e5e7eb;
  font-weight: 760;
  background: rgba(15, 23, 42, 0.54);
}

[data-testid="stAlert"] {
  border-radius: 16px;
  border: 1px solid rgba(148, 163, 184, 0.14);
}

[data-testid="stDataFrame"] {
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(148, 163, 184, 0.13);
  background: rgba(15, 23, 42, 0.58);
}

/* ============================================================
   Buttons
   ============================================================ */

.stButton > button,
.stDownloadButton > button {
  background: linear-gradient(135deg, #0284c7, #10b981) !important;
  color: #f8fafc !important;
  border: 0 !important;
  border-radius: 13px !important;
  font-weight: 780 !important;
  min-height: 2.7rem;
  box-shadow: 0 14px 35px rgba(14, 165, 233, 0.15);
}

.stButton > button:hover,
.stDownloadButton > button:hover {
  color: #ffffff !important;
  filter: brightness(1.08);
  transform: translateY(-1px);
}

/* ============================================================
   File uploader
   ============================================================ */

[data-testid="stFileUploader"] {
  background:
    linear-gradient(180deg, rgba(15, 23, 42, 0.88), rgba(2, 6, 23, 0.58)) !important;
  border: 1px dashed rgba(56, 189, 248, 0.32) !important;
  border-radius: 20px !important;
  padding: 1rem !important;
  color: #e5e7eb !important;
}

[data-testid="stFileUploaderDropzone"] {
  background: rgba(2, 6, 23, 0.42) !important;
  border: 1px solid rgba(148, 163, 184, 0.14) !important;
  border-radius: 16px !important;
  color: #e5e7eb !important;
}

[data-testid="stFileUploaderDropzone"] section {
  background: rgba(2, 6, 23, 0.28) !important;
  border: 1px solid rgba(148, 163, 184, 0.12) !important;
  border-radius: 14px !important;
}

[data-testid="stFileUploaderDropzone"] button,
[data-testid="stFileUploaderDropzone"] button[kind="secondary"] {
  background: #0f172a !important;
  color: #f8fafc !important;
  border: 1px solid rgba(148, 163, 184, 0.26) !important;
  border-radius: 12px !important;
  box-shadow: none !important;
}

[data-testid="stFileUploaderDropzone"] button:hover,
[data-testid="stFileUploaderDropzone"] button[kind="secondary"]:hover {
  background: linear-gradient(135deg, #0369a1, #0f766e) !important;
  color: #ffffff !important;
  border-color: rgba(56, 189, 248, 0.58) !important;
}

[data-testid="stFileUploaderDropzone"] button p,
[data-testid="stFileUploaderDropzone"] button span,
[data-testid="stFileUploaderDropzone"] small,
[data-testid="stFileUploader"] small {
  color: #dbe4ef !important;
}

[data-testid="stFileUploaderDropzone"] svg {
  color: #cbd5e1 !important;
  fill: #cbd5e1 !important;
}

[data-testid="stFileUploaderFile"],
[data-testid="stFileUploaderFile"] * {
  background-color: #0f172a !important;
  color: #e5e7eb !important;
  border-color: rgba(148, 163, 184, 0.22) !important;
}

/* ============================================================
   Radio buttons - remove red accent
   ============================================================ */

input[type="radio"],
[data-testid="stRadio"] *,
[data-testid="stRadio"] input[type="radio"],
[data-testid="stRadio"] input[type="radio"]:checked {
  accent-color: #38bdf8 !important;
}

[data-testid="stRadio"] div[role="radiogroup"] {
  gap: 0.45rem;
}

[data-testid="stRadio"] div[role="radiogroup"] label {
  background: rgba(15, 23, 42, 0.72) !important;
  border: 1px solid rgba(148, 163, 184, 0.18) !important;
  border-radius: 999px !important;
  padding: 0.45rem 0.78rem !important;
  margin-bottom: 0.35rem !important;
  transition: 0.18s ease;
}

[data-testid="stRadio"] div[role="radiogroup"] label:hover {
  background: rgba(30, 41, 59, 0.82) !important;
  border-color: rgba(56, 189, 248, 0.38) !important;
}

[data-testid="stRadio"] div[role="radiogroup"] label p {
  color: #e5e7eb !important;
  font-weight: 650;
}

[data-testid="stRadio"] [aria-checked="true"],
[data-testid="stRadio"] label:has(input:checked) {
  background: linear-gradient(135deg, rgba(8, 47, 73, 0.86), rgba(15, 118, 110, 0.42)) !important;
  border-color: rgba(56, 189, 248, 0.58) !important;
  box-shadow:
    0 0 0 1px rgba(20, 184, 166, 0.18),
    0 0 24px rgba(56, 189, 248, 0.12) !important;
}

[data-testid="stRadio"] svg,
[data-testid="stRadio"] svg *,
[data-testid="stRadio"] [aria-checked="true"] svg,
[data-testid="stRadio"] [aria-checked="true"] svg * {
  color: #38bdf8 !important;
  fill: #38bdf8 !important;
  stroke: #38bdf8 !important;
}

/* ============================================================
   Slider / progress - cyan teal glow
   ============================================================ */

input[type="range"],
[data-testid="stSlider"] *,
.stSlider * {
  accent-color: #38bdf8 !important;
}

.stSlider [data-baseweb="slider"],
.stSlider [data-baseweb="slider"] > div {
  color: #38bdf8 !important;
}

.stSlider [data-baseweb="slider"] [role="presentation"] {
  background: linear-gradient(90deg, #38bdf8, #14b8a6) !important;
}

.stSlider [data-baseweb="slider"] div[style*="background"] {
  background: linear-gradient(90deg, #38bdf8, #14b8a6) !important;
}

.stSlider [role="slider"] {
  background: radial-gradient(circle, #e0f2fe 0%, #38bdf8 45%, #14b8a6 100%) !important;
  border: 2px solid rgba(224, 242, 254, 0.95) !important;
  box-shadow:
    0 0 0 5px rgba(56, 189, 248, 0.16),
    0 0 24px rgba(20, 184, 166, 0.42) !important;
}

[data-testid="stProgress"] {
  background: rgba(15, 23, 42, 0.74) !important;
  border: 1px solid rgba(148, 163, 184, 0.18) !important;
  border-radius: 999px !important;
  overflow: hidden !important;
}

[data-testid="stProgress"] > div,
[data-testid="stProgress"] div[role="progressbar"],
[data-testid="stProgress"] div[style*="background"] {
  background: linear-gradient(90deg, #38bdf8, #14b8a6) !important;
  box-shadow: 0 0 18px rgba(56, 189, 248, 0.28) !important;
}

/* ============================================================
   Selectbox / dropdown - dark BaseWeb override
   ============================================================ */

[data-baseweb="select"] > div {
  background: #0f172a !important;
  border: 1px solid rgba(148, 163, 184, 0.22) !important;
  border-radius: 14px !important;
  color: #f8fafc !important;
  box-shadow: none !important;
}

[data-baseweb="select"] > div:hover,
[data-baseweb="select"] > div:focus-within {
  border-color: rgba(56, 189, 248, 0.54) !important;
  box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.11) !important;
}

[data-baseweb="select"] input,
[data-baseweb="select"] span,
[data-baseweb="select"] div {
  color: #e5e7eb !important;
}

/* Dropdown portal/popover */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
div[data-baseweb="menu"],
[data-baseweb="popover"],
[data-baseweb="menu"],
ul[role="listbox"],
div[role="listbox"],
[role="listbox"] {
  background: #0f172a !important;
  color: #f8fafc !important;
  border: 1px solid rgba(148, 163, 184, 0.24) !important;
  border-radius: 14px !important;
  box-shadow: 0 24px 70px rgba(0, 0, 0, 0.42) !important;
}

div[data-baseweb="popover"] *,
div[data-baseweb="menu"] *,
[role="listbox"] * {
  color: #f8fafc !important;
}

li[role="option"],
div[role="option"],
[role="option"] {
  background: #0f172a !important;
  color: #e5e7eb !important;
}

li[role="option"]:hover,
div[role="option"]:hover,
[role="option"]:hover,
li[aria-selected="true"],
div[aria-selected="true"],
[aria-selected="true"] {
  background: rgba(56, 189, 248, 0.18) !important;
  color: #ffffff !important;
}

li[role="option"]:hover *,
div[role="option"]:hover *,
[role="option"]:hover *,
li[aria-selected="true"] *,
div[aria-selected="true"] *,
[aria-selected="true"] * {
  color: #ffffff !important;
}

/* Try to neutralize stubborn white menu item inner backgrounds */
div[data-baseweb="menu"] div,
div[data-baseweb="popover"] div,
[role="listbox"] div {
  background-color: transparent !important;
}

/* Dropdown scrollbar */
[data-baseweb="popover"] ::-webkit-scrollbar,
[data-baseweb="menu"] ::-webkit-scrollbar,
[role="listbox"]::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

[data-baseweb="popover"] ::-webkit-scrollbar-track,
[data-baseweb="menu"] ::-webkit-scrollbar-track,
[role="listbox"]::-webkit-scrollbar-track {
  background: #020617;
}

[data-baseweb="popover"] ::-webkit-scrollbar-thumb,
[data-baseweb="menu"] ::-webkit-scrollbar-thumb,
[role="listbox"]::-webkit-scrollbar-thumb {
  background: linear-gradient(180deg, #38bdf8, #14b8a6);
  border-radius: 999px;
  border: 2px solid #020617;
}

/* ============================================================
   Inputs
   ============================================================ */

[data-baseweb="input"] > div {
  background: rgba(15, 23, 42, 0.92) !important;
  border: 1px solid rgba(148, 163, 184, 0.28) !important;
  border-radius: 14px !important;
}

[data-baseweb="input"] input {
  color: #f8fafc !important;
  caret-color: #38bdf8 !important;
}

[data-baseweb="input"] > div:focus-within {
  border-color: rgba(56, 189, 248, 0.70) !important;
  box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.12) !important;
}

/* ============================================================
   Misc
   ============================================================ */

hr {
  border-color: rgba(148, 163, 184, 0.13);
  margin: 1.35rem 0;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

@media (max-width: 900px) {
  .hero-grid,
  .step-grid {
    grid-template-columns: 1fr;
  }

  .block-container {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}
/* ============================================================
   Extra hard overrides for Streamlit dropdown / multiselect
   ============================================================ */

/* Selectbox dropdown portal */
[data-testid="stSelectbox"] div,
[data-testid="stMultiSelect"] div {
  color: #f8fafc !important;
}

/* Open dropdown menu */
[data-testid="stSelectboxVirtualDropdown"],
[data-testid="stMultiSelectVirtualDropdown"],
div[data-baseweb="popover"],
div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] li,
ul[role="listbox"],
div[role="listbox"] {
  background: #0f172a !important;
  color: #f8fafc !important;
  border-color: rgba(148, 163, 184, 0.24) !important;
}

/* Dropdown option rows */
[data-testid="stSelectboxVirtualDropdown"] div,
[data-testid="stMultiSelectVirtualDropdown"] div,
li[role="option"],
div[role="option"] {
  background-color: #0f172a !important;
  color: #e5e7eb !important;
}

/* Hover / selected option */
[data-testid="stSelectboxVirtualDropdown"] div:hover,
[data-testid="stMultiSelectVirtualDropdown"] div:hover,
li[role="option"]:hover,
div[role="option"]:hover,
[aria-selected="true"] {
  background-color: rgba(56, 189, 248, 0.18) !important;
  color: #ffffff !important;
}

/* Multiselect selected tags - remove red chips */
[data-baseweb="tag"] {
  background: linear-gradient(135deg, rgba(14, 165, 233, 0.92), rgba(20, 184, 166, 0.88)) !important;
  color: #ffffff !important;
  border: 1px solid rgba(186, 230, 253, 0.24) !important;
  border-radius: 999px !important;
}

[data-baseweb="tag"] span,
[data-baseweb="tag"] svg,
[data-baseweb="tag"] path {
  color: #ffffff !important;
  fill: #ffffff !important;
}

/* Multiselect input area */
[data-testid="stMultiSelect"] [data-baseweb="select"] > div {
  background: #0f172a !important;
  border: 1px solid rgba(148, 163, 184, 0.22) !important;
  color: #f8fafc !important;
}
/* Dropdown selected/hover row refinement */
li[aria-selected="true"],
div[aria-selected="true"],
[aria-selected="true"],
li[role="option"]:hover,
div[role="option"]:hover,
[role="option"]:hover {
  background: linear-gradient(
    90deg,
    rgba(56, 189, 248, 0.22),
    rgba(20, 184, 166, 0.16)
  ) !important;
  color: #f8fafc !important;
}

li[aria-selected="true"] *,
div[aria-selected="true"] *,
[aria-selected="true"] *,
li[role="option"]:hover *,
div[role="option"]:hover *,
[role="option"]:hover * {
  color: #f8fafc !important;
  background-color: transparent !important;
}

/* Remove pale blue/white selected option background */
[data-baseweb="menu"] [aria-selected="true"] {
  background-color: rgba(56, 189, 248, 0.20) !important;
}

[data-baseweb="menu"] [aria-selected="true"] div {
  background-color: transparent !important;
}
/* ============================================================
   Dropdown selected / hover row refinement
   ============================================================ */

li[aria-selected="true"],
div[aria-selected="true"],
[aria-selected="true"],
li[role="option"]:hover,
div[role="option"]:hover,
[role="option"]:hover {
  background: linear-gradient(
    90deg,
    rgba(56, 189, 248, 0.22),
    rgba(20, 184, 166, 0.16)
  ) !important;
  color: #f8fafc !important;
}

li[aria-selected="true"] *,
div[aria-selected="true"] *,
[aria-selected="true"] *,
li[role="option"]:hover *,
div[role="option"]:hover *,
[role="option"]:hover * {
  color: #f8fafc !important;
  background-color: transparent !important;
}

/* Remove pale selected option background */
[data-baseweb="menu"] [aria-selected="true"] {
  background-color: rgba(56, 189, 248, 0.20) !important;
}

[data-baseweb="menu"] [aria-selected="true"] div {
  background-color: transparent !important;
}
/* ============================================================
   Dropdown selected / hover row final refinement
   ============================================================ */

[data-baseweb="menu"] [aria-selected="true"],
[data-baseweb="menu"] [aria-selected="true"] div,
[data-baseweb="menu"] [aria-selected="true"] span,
[role="listbox"] [aria-selected="true"],
[role="listbox"] [aria-selected="true"] div,
[role="listbox"] [aria-selected="true"] span {
  background: linear-gradient(
    90deg,
    rgba(8, 47, 73, 0.95),
    rgba(15, 118, 110, 0.65)
  ) !important;
  color: #f8fafc !important;
}

[data-baseweb="menu"] [aria-selected="true"] *,
[role="listbox"] [aria-selected="true"] * {
  background-color: transparent !important;
  color: #f8fafc !important;
}

/* Hover option */
[data-baseweb="menu"] [role="option"]:hover,
[role="listbox"] [role="option"]:hover {
  background: linear-gradient(
    90deg,
    rgba(56, 189, 248, 0.18),
    rgba(20, 184, 166, 0.14)
  ) !important;
  color: #f8fafc !important;
}

[data-baseweb="menu"] [role="option"]:hover *,
[role="listbox"] [role="option"]:hover * {
  background-color: transparent !important;
  color: #f8fafc !important;
}

.segment-insight-card {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.96), rgba(8, 13, 28, 0.96));
    border: 1px solid rgba(56, 189, 248, 0.16);
    border-radius: 16px;
    padding: 18px 20px;
    margin: 14px 0;
    box-shadow: 0 16px 34px rgba(0, 0, 0, 0.22);
}

.segment-insight-header {
    margin-bottom: 14px;
}

.segment-insight-kicker {
    color: #38bdf8;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 4px;
}

.segment-insight-title {
    color: #e5e7eb;
    font-size: 1.02rem;
    font-weight: 800;
}

.segment-insight-label {
    color: #94a3b8;
    font-size: 0.78rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 8px;
}

.segment-insight-list {
    list-style: none;
    padding-left: 0;
    margin: 0;
}

.segment-insight-list li {
    display: flex;
    gap: 10px;
    align-items: flex-start;
    color: #cbd5e1;
    font-size: 0.88rem;
    line-height: 1.55;
    padding: 5px 0;
}

.insight-driver-symbol {
    color: #22c55e;
    font-weight: 900;
    min-width: 18px;
}

.insight-note {
    margin-top: 12px;
    padding: 10px 12px;
    border-radius: 12px;
    background: rgba(245, 158, 11, 0.10);
    border: 1px solid rgba(245, 158, 11, 0.22);
    color: #fcd34d;
    font-size: 0.82rem;
    line-height: 1.45;
}
.insight-action-box {
    margin-top: 14px;
    padding: 12px 14px;
    border-radius: 14px;
    background: linear-gradient(135deg, rgba(34, 197, 94, 0.10), rgba(14, 165, 233, 0.08));
    border: 1px solid rgba(34, 197, 94, 0.22);
}

.insight-action-label {
    color: #86efac;
    font-size: 0.74rem;
    font-weight: 800;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.insight-action-text {
    color: #d1fae5;
    font-size: 0.86rem;
    line-height: 1.55;
}

</style>
""",
        unsafe_allow_html=True,
    )