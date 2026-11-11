import re
import html
import streamlit as st

from compiler import Compiler


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MiniTAC Compiler",
    page_icon=None,
    layout="wide",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>

@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #c9e7eb;
    --surface: #f7f5ee;
    --surface-2: #eef5f3;
    --border: #b7d1d4;
    --border-soft: #d7e5e5;
    --text: #18343b;
    --text-dim: #5e747a;
    --text-faint: #7b9196;
    --accent: #5f9fa8;
    --accent-soft: rgba(95, 159, 168, 0.14);
    --accent-text: #ffffff;
    --danger: #b85b5b;
    --danger-soft: rgba(184, 91, 91, 0.10);
    --radius: 14px;
    --radius-sm: 9px;
    --font-body: "Inter", "Space Grotesk", sans-serif;
    --font-mono: "JetBrains Mono", monospace;
    --code-bg: #eef5f3;
    --code-text: #18343b;
    --code-border: #b7d1d4;
}

html, body, [class*="css"] {
    font-family: var(--font-body);
}

.stApp {
    background: var(--bg);
    color: var(--text);
}

.block-container {
    max-width: 1200px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}


/* ============================================================
   EDITOR + CODE AREAS
   ============================================================ */

textarea {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    font-family: var(--font-mono) !important;
    font-size: 14px !important;
}

textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent-soft) !important;
}

div[data-testid="stCodeBlock"] {
    border: 1px solid var(--code-border) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
    background: var(--code-bg) !important;
}

div[data-testid="stCodeBlock"] pre,
div[data-testid="stCodeBlock"] code {
    background: var(--code-bg) !important;
    color: var(--code-text) !important;
}

/* Streamlit table/dataframe containers */
div[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 14px !important;
    overflow: hidden !important;
}

/* Tabs */
div[data-testid="stTabs"] {
    margin-top: 10px;
}

div[data-testid="stTabs"] [data-baseweb="tab-list"],
div[data-testid="stTabs"] div[role="tablist"] {
    gap: 14px !important;
    border-bottom: none !important;
    flex-wrap: nowrap !important;
    row-gap: 0 !important;
    overflow-x: auto !important;
    overflow-y: hidden !important;
    padding: 6px 2px 12px !important;
    scrollbar-width: thin !important;
}

/* ============================================================
   LARGE EDITORIAL TABS
   ============================================================ */

div[data-testid="stTabs"] [data-baseweb="tab-list"],
div[data-testid="stTabs"] div[role="tablist"] {

    display: flex !important;

    gap: 28px !important;

    border-bottom: none !important;

    flex-wrap: nowrap !important;

    row-gap: 0 !important;

    overflow-x: auto !important;

    overflow-y: hidden !important;

    padding: 6px 2px 12px !important;

    scrollbar-width: thin !important;
}


div[data-testid="stTabs"] button[data-baseweb="tab"],
div[data-testid="stTabs"] button[role="tab"] {

    color: var(--text-dim) !important;

    background: transparent !important;

    border: none !important;

    border-radius: 0 !important;

    padding: 10px 0 16px !important;

    min-height: 58px !important;

    min-width: max-content !important;

    font-size: 25px !important;

    font-weight: 800 !important;

    line-height: 1.2 !important;

    white-space: nowrap !important;

    box-shadow: none !important;

    transition: color 0.15s ease !important;
}


/* TAB TEXT */

div[data-testid="stTabs"] button[data-baseweb="tab"] p,
div[data-testid="stTabs"] button[role="tab"] p {

    color: inherit !important;

    font-size: 25px !important;

    font-weight: 800 !important;

    line-height: 1.2 !important;

    white-space: nowrap !important;

    margin: 0 !important;

    padding: 0 !important;
}


/* HOVER */

div[data-testid="stTabs"] button[data-baseweb="tab"]:hover,
div[data-testid="stTabs"] button[role="tab"]:hover {

    color: var(--accent) !important;

}


/* ACTIVE TAB */

div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"],
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {

    color: var(--accent) !important;

    font-weight: 800 !important;

}


/* ACTIVE UNDERLINE */

div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"]::after,
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"]::after {

    content: "";

    display: block;

    height: 3px;

    margin-top: 10px;

    border-radius: 3px;

    background: var(--accent);

}

div[data-testid="stTabs"] button[data-baseweb="tab"] p,
div[data-testid="stTabs"] button[role="tab"] p {
    font-weight: inherit !important;
    font-size: inherit !important;
    color: inherit !important;
    white-space: nowrap !important;
    margin: 0 !important;
}

/* Native controls */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: var(--surface) !important;
    border-color: var(--border) !important;
    color: var(--text) !important;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    text-align: center;
    padding: 30px 20px 20px;
}

.hero-small {
    display: inline-block;
    color: var(--accent);
    background: var(--accent-soft);
    font-size: 13px;
    font-weight: 600;
    padding: 5px 14px;
    border-radius: 999px;
}

.hero-title {
    font-size: 42px;
    font-weight: 800;
    margin-top: 16px;
    color: var(--text);
    letter-spacing: -0.5px;
}

.hero-subtitle {
    color: var(--text-dim);
    font-size: 15px;
    margin-top: 10px;
    max-width: 560px;
    margin-left: auto;
    margin-right: auto;
    line-height: 1.5;
}


/* ============================================================
   PIPELINE
   ============================================================ */

.pipeline {
    display: flex;
    justify-content: center;
    align-items: center;
    flex-wrap: nowrap;
    gap: 12px;
    margin: 26px 0 36px;
    padding: 8px 4px 12px;
    overflow-x: auto;
    scrollbar-width: thin;
}
.pipeline-item {
    border: 1px solid var(--border);
    background: var(--surface);
    color: var(--text);
    padding: 12px 20px;
    min-height: 44px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 999px;
    font-size: 14px;
    font-weight: 650;
    white-space: nowrap;
    box-sizing: border-box;
    box-shadow: 0 4px 12px rgba(24, 52, 59, 0.05);
    transition: all 0.2s ease;
}

.pipeline-item:hover {
    border-color: var(--accent);
    transform: translateY(-1px);
}

.pipeline-item.active {
    color: var(--surface);
    background: var(--accent);
    border-color: var(--accent);
    font-weight: 700;
    box-shadow: 0 5px 14px rgba(95, 159, 168, 0.20);
}

.pipeline-arrow {
    color: var(--accent);
    font-size: 15px;
    font-weight: 600;
    flex-shrink: 0;
}


/* ============================================================
   CARDS
   ============================================================ */

.card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px 22px;
    margin-bottom: 18px;
}

.card-title {
    color: var(--text);
    font-size: 19px;
    font-weight: 700;
}

.card-subtitle {
    color: var(--text-dim);
    font-size: 14px;
    margin-top: 6px;
    line-height: 1.5;
}


/* ============================================================
   METRICS
   ============================================================ */

.metric {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 16px 10px;
    text-align: center;
}

.metric-value {
    color: var(--accent);
    font-size: 26px;
    font-weight: 800;
}

.metric-label {
    color: var(--text-dim);
    font-size: 11px;
    font-weight: 500;
    margin-top: 4px;
}



/* ============================================================
   AST - VERTICAL TREE
   ============================================================ */

.ast-area {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 40px 25px 50px;
    overflow-x: auto;
    overflow-y: hidden;
}

.ast-wrapper {
    width: 100%;
    display: flex;
    justify-content: center;
}

.ast-tree {
    width: max-content;
    min-width: 850px;
    margin: 0 auto;
}

/* Every AST node - a table-like layout keeps parents centered
   over the true midpoint of their children instead of the
   midpoint of the flex box (which breaks once children wrap
   or have unequal widths). */
.ast-item {
    display: table;
    margin: 0 auto;
    position: relative;
}

.ast-item-inner {
    display: table-row;
}

.ast-node-cell {
    display: table-cell;
    text-align: center;
    vertical-align: bottom;
    padding-bottom: 0;
}

/* Node box */
.ast-node {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    min-width: 150px;
    max-width: 220px;
    padding: 12px 18px;
    border-radius: 12px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    text-align: center;
    box-sizing: border-box;
    position: relative;
    z-index: 1;
}

/* Program */
.ast-node.program {
    min-width: 190px;
    border-color: var(--accent);
}

/* Node title */
.ast-node-type {
    color: var(--accent);
    font-family: var(--font-mono);
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.6px;
    white-space: nowrap;
}

/* Node value */
.ast-node-value {
    color: var(--text-dim);
    font-family: var(--font-mono);
    font-size: 11px;
    margin-top: 7px;
    line-height: 1.4;
}

/* Relationship label */
.ast-relation {
    color: var(--text-faint);
    font-size: 11px;
    font-weight: 600;
    margin-bottom: 6px;
    white-space: nowrap;
}

/* ============================================================
   PROGRAM STATEMENTS
   Table layout, one statement per row, each row centered
   independently under the PROGRAM node above it.
   ============================================================ */

.ast-program-children {
    display: table;
    margin: 30px auto 0;
    border-collapse: collapse;
    position: relative;
}

.ast-program-children::before {
    content: "";
    position: absolute;
    top: -30px;
    left: 50%;
    width: 1px;
    height: 30px;
    background: var(--border);
}

.ast-statement {
    display: table-row;
}

.ast-statement-cell {
    display: table-cell;
    text-align: center;
    padding-top: 26px;
    position: relative;
}

/* Connector line above every statement after the first */
.ast-statement:not(:first-child) .ast-statement-cell::before {
    content: "";
    position: absolute;
    top: 0;
    left: 50%;
    width: 1px;
    height: 26px;
    background: var(--border);
}

/* ============================================================
   NORMAL CHILDREN
   Table layout: each child sits in its own table-cell so the
   row's total width is the sum of real child widths, and the
   horizontal connector spans exactly between the first and
   last child's centers rather than a fixed 25%/25% guess.
   ============================================================ */

.ast-children {
    display: table;
    margin: 28px auto 0;
    border-collapse: collapse;
    position: relative;
}

.ast-children-row {
    display: table-row;
}

/* Vertical connector from parent down to the row */
.ast-children::before {
    content: "";
    position: absolute;
    top: -28px;
    left: 50%;
    width: 1px;
    height: 28px;
    background: var(--border);
    z-index: 2;
}

.ast-child-cell {
    display: table-cell;
    text-align: center;
    vertical-align: top;
    padding: 0 35px;
    position: relative;
}

/* Horizontal bus line running through every cell at connector height */
.ast-child-cell::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: var(--border);
}

/* First and last cells: cut the bus line off outside the
   actual child positions so it only spans between real children */
.ast-child-cell:first-child::before {
    left: 50%;
}

.ast-child-cell:last-child::before {
    right: 50%;
}

/* If there is only one child, no bus line is needed */
.ast-child-cell:first-child:last-child::before {
    display: none;
}

/* Vertical drop from the bus line into each child node */
.ast-child-cell::after {
    content: "";
    position: absolute;
    top: 0;
    left: 50%;
    width: 1px;
    height: 28px;
    background: var(--border);
}

.ast-child-inner {
    margin-top: 28px;
}

/* Leaves */
.ast-leaf .ast-node {
    border-color: var(--border-soft);
}

/* Mobile */
@media (max-width: 900px) {

    .ast-area {
        padding: 30px 15px 40px;
    }

    .ast-tree {
        min-width: 700px;
    }

    .ast-child-cell {
        padding: 0 20px;
    }

    .ast-node {
        min-width: 130px;
        padding: 10px 14px;
    }
}


/* ============================================================
   CFG
   ============================================================ */

.cfg-area {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 30px 20px;
}

.cfg-block {
    width: min(650px, 100%);
    margin: auto;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 13px;
    overflow: hidden;
}

.cfg-header {
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    color: var(--accent);
    padding: 12px 16px;
    font-family: var(--font-mono);
    font-size: 13px;
    font-weight: 700;
}

.cfg-line {
    padding: 9px 16px;
    border-bottom: 1px solid var(--border-soft);
    color: var(--text);
    font-family: var(--font-mono);
    font-size: 12px;
}

.cfg-line:last-child {
    border-bottom: none;
}

.cfg-arrow {
    text-align: center;
    color: var(--accent);
    font-size: 22px;
    padding: 8px;
}


/* ============================================================
   LIVENESS
   ============================================================ */

.live-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 13px;
    padding: 18px;
    margin-bottom: 12px;
}

.live-title {
    color: var(--accent);
    font-weight: 700;
    font-size: 14px;
    margin-bottom: 14px;
}

.live-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 14px;
    align-items: start;
}

.live-cell {
    display: flex;
    flex-direction: column;
    min-width: 0;
}

.live-label {
    color: var(--text-faint);
    font-size: 11px;
    font-weight: 600;
    line-height: 1.2;
}

.live-value {
    color: var(--text);
    font-family: var(--font-mono);
    font-size: 12px;
    margin-top: 5px;
    line-height: 1.5;
    overflow-wrap: anywhere;
    word-break: break-word;
}

@media (max-width: 600px) {

    .live-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
        row-gap: 18px;
    }
}


/* ============================================================
   DCE / FLOW DIAGRAM
   ============================================================ */

.flow {
    display: flex;
    justify-content: center;
    align-items: stretch;
    flex-wrap: wrap;
    gap: 10px;
    margin: 22px 0 28px;
}

.flow-box {
    flex: 1 1 175px;
    max-width: 200px;
    min-width: 140px;
    min-height: 84px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 10px 14px;
    box-sizing: border-box;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 13px;
}

.flow-arrow {
    display: flex;
    align-items: center;
    color: var(--accent);
    font-size: 20px;
}

.flow-title {
    color: var(--text);
    font-weight: 700;
    font-size: 14px;
}

.flow-description {
    color: var(--text-dim);
    font-size: 11px;
    margin-top: 6px;
}

.keep {
    background: var(--accent-soft);
    border-left: 3px solid var(--accent);
    border-radius: 6px;
    padding: 10px 13px;
    margin: 5px 0;
    color: var(--text);
    font-family: var(--font-mono);
    font-size: 12px;
}

.removed {
    background: var(--danger-soft);
    border-left: 3px solid var(--danger);
    border-radius: 6px;
    padding: 10px 13px;
    margin: 5px 0;
    color: var(--text);
    font-family: var(--font-mono);
    font-size: 12px;
}


/* ============================================================
   INFO
   ============================================================ */

.info {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 13px 16px;
    margin: 6px 0;
    color: var(--text-dim);
    font-size: 13px;
    line-height: 1.5;
}

.info strong {
    color: var(--text);
}


/* ============================================================
   EXPLAINER (plain-language helper boxes)
   ============================================================ */

.explainer {
    background: var(--surface);
    border: 1px solid var(--border-soft);
    border-left: 3px solid var(--accent);
    border-radius: var(--radius-sm);
    padding: 14px 18px;
    margin: 4px 0 18px;
    color: var(--text-dim);
    font-size: 13.5px;
    line-height: 1.6;
}

.explainer strong {
    color: var(--text);
}


/* ============================================================
   FOOTER
   ============================================================ */

.footer {
    text-align: center;
    color: var(--text-faint);
    font-size: 12px;
    padding: 40px 0 10px;
    line-height: 1.6;
}

.green {
    color: var(--accent);
}


@media (max-width: 800px) {

    .hero-title {
        font-size: 32px;
    }

    .live-grid {
        grid-template-columns: repeat(2, 1fr);
    }

}

/* ============================================================
   COMPILE PROGRAM BUTTON
   ============================================================ */

button[kind="primary"] {
    background: var(--accent) !important;
    color: var(--accent-text) !important;
    border: 1px solid var(--accent) !important;
    border-radius: 10px !important;
    font-family: var(--font-body) !important;
    font-size: 16px !important;
    font-weight: 700 !important;
    transition: all 0.15s ease !important;
}

button[kind="primary"]:hover {
    filter: brightness(1.08);
    transform: translateY(-1px);
}

/* =====================================================
   COMPILER ERROR PANEL
   ===================================================== */

.compiler-error-card {
    margin-top: 20px;
    padding: 18px 22px;
    border: 1px solid var(--danger);
    border-left: 5px solid var(--danger);
    border-radius: var(--radius);
    background: var(--danger-soft);
}

.compiler-error-title {
    color: var(--danger);
    font-family: var(--font-body);
    font-size: 19px;
    font-weight: 800;
}

.compiler-error-type {
    margin-top: 4px;
    color: var(--text-dim);
    font-size: 13px;
    font-weight: 600;
}

.compiler-error-location {
    margin-top: 12px;
    padding: 9px 14px;
    border-radius: var(--radius-sm);
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text);
    font-family: var(--font-mono);
    font-size: 13px;
}

.compiler-error-message {
    margin-top: 12px;
    padding: 15px 16px;
    border-radius: var(--radius-sm);
    background: var(--surface);
    border: 1px solid var(--border);
}

.error-label {
    color: var(--text-faint);
    font-size: 11px;
    font-weight: 700;
    margin-bottom: 6px;
}

.error-text {
    color: var(--text);
    font-family: var(--font-mono);
    font-size: 13.5px;
    line-height: 1.6;
}

.error-source-title {
    margin-top: 16px;
    margin-bottom: 8px;
    color: var(--text-faint);
    font-size: 11px;
    font-weight: 700;
}

.error-source-box {
    padding: 12px 0;
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    background: var(--bg);
    overflow-x: auto;
    font-family: var(--font-mono);
}

.error-source-line {
    display: flex;
    min-height: 26px;
    align-items: center;
    padding: 2px 18px;
}

.error-source-line.active {
    background: var(--danger-soft);
    border-left: 3px solid var(--danger);
}

.line-number {
    width: 38px;
    flex-shrink: 0;
    color: var(--text-faint);
    text-align: right;
    margin-right: 16px;
    user-select: none;
    font-size: 12px;
}

.error-source-line.active .line-number {
    color: var(--danger);
    font-weight: 700;
}

.line-code {
    color: var(--text);
    white-space: pre;
    font-size: 13px;
}

.error-caret-row {
    display: flex;
    min-height: 18px;
    padding: 0 18px;
}

.error-caret {
    color: var(--danger);
    font-family: var(--font-mono);
    font-weight: 900;
    white-space: pre;
}

/* ============================================================
   MODE SWITCHER
   ============================================================ */

.mode-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 16px 20px;
    margin: 12px 0 22px;
}

.mode-title {
    color: var(--text);
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.3px;
    margin-bottom: 4px;
}

.mode-subtitle {
    color: var(--text-dim);
    font-size: 12px;
}

/* ============================================================
   LEARN MODE - EDUCATIONAL UI
   ============================================================ */

.learn-hero {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 30px 34px;
    margin-bottom: 22px;
}

.learn-hero-title {
    color: var(--text);
    font-size: 28px;
    font-weight: 800;
    letter-spacing: -0.4px;
}

.learn-hero-text {
    color: var(--text-dim);
    font-size: 14px;
    line-height: 1.7;
    margin-top: 8px;
    max-width: 820px;
}

.learn-section {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 26px 28px;
    margin: 18px 0;
}

.learn-phase-header {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 18px;
}

.learn-number {
    color: var(--accent);
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
}

.learn-title {
    color: var(--text);
    font-size: 22px;
    font-weight: 800;
}

.learn-text {
    color: var(--text-dim);
    font-size: 14px;
    line-height: 1.7;
    margin: 8px 0 20px;
}

.learn-label {
    color: var(--text-faint);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 9px;
}

/* Visual flow */

.learn-flow {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
    margin: 18px 0 24px;
}

.learn-flow-box {
    min-width: 135px;
    padding: 16px 18px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 13px;
    text-align: center;
}

.learn-flow-box strong {
    display: block;
    color: var(--text);
    font-size: 14px;
}

.learn-flow-box span {
    display: block;
    color: var(--text-dim);
    font-family: var(--font-mono);
    font-size: 10px;
    margin-top: 6px;
}

.learn-flow-arrow {
    color: var(--accent);
    font-family: var(--font-mono);
    font-size: 20px;
    font-weight: 700;
}

/* Code transformation */

.learn-code {
    background: var(--code-bg);
    border: 1px solid var(--code-border);
    border-radius: 13px;
    padding: 18px 20px;
    font-family: var(--font-mono);
    font-size: 13px;
    line-height: 1.8;
    color: var(--code-text);
    white-space: pre-wrap;
    overflow-x: auto;
}

.learn-transform {
    display: grid;
    grid-template-columns: 1fr 70px 1fr;
    gap: 14px;
    align-items: center;
    margin-top: 12px;
}

.learn-transform-arrow {
    text-align: center;
    color: var(--accent);
    font-family: var(--font-mono);
    font-size: 24px;
    font-weight: 700;
}

.learn-transform-box {
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 13px;
    padding: 16px;
}

.learn-transform-title {
    color: var(--accent);
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.8px;
    margin-bottom: 8px;
}

/* Token table */

.learn-token-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 12px;
    font-size: 13px;
}

.learn-token-table th {
    text-align: left;
    color: var(--text-faint);
    font-size: 11px;
    letter-spacing: 0.7px;
    text-transform: uppercase;
    padding: 10px 12px;
    border-bottom: 1px solid var(--border);
}

.learn-token-table td {
    color: var(--text);
    font-family: var(--font-mono);
    padding: 10px 12px;
    border-bottom: 1px solid var(--border-soft);
}

.learn-token-table tr:last-child td {
    border-bottom: none;
}

/* Explanation cards */

.learn-two-column {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
    margin-top: 18px;
}

.learn-info-box {
    background: var(--surface-2);
    border: 1px solid var(--border-soft);
    border-radius: 13px;
    padding: 17px 18px;
}

.learn-info-title {
    color: var(--text);
    font-size: 14px;
    font-weight: 750;
    margin-bottom: 7px;
}

.learn-info-text {
    color: var(--text-dim);
    font-size: 12.5px;
    line-height: 1.65;
}

/* AST visual */

.learn-ast {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
    padding: 22px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 15px;
}

.learn-ast-node {
    background: var(--surface);
    border: 1px solid var(--accent);
    border-radius: 10px;
    padding: 9px 18px;
    color: var(--text);
    font-family: var(--font-mono);
    font-size: 12px;
    font-weight: 700;
}

.learn-ast-children {
    display: flex;
    gap: 18px;
    justify-content: center;
}

.learn-ast-child {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 9px;
    padding: 8px 14px;
    color: var(--text-dim);
    font-family: var(--font-mono);
    font-size: 11px;
}

/* CFG */

.learn-cfg {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 7px;
    padding: 22px;
    background: var(--surface-2);
    border: 1px solid var(--border);
    border-radius: 15px;
}

.learn-cfg-block {
    min-width: 190px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 18px;
    text-align: center;
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--text);
}

.learn-cfg-decision {
    border-color: var(--accent);
}

.learn-cfg-arrow {
    color: var(--accent);
    font-family: var(--font-mono);
    font-size: 18px;
}

/* DCE */

.learn-dce-row {
    display: grid;
    grid-template-columns: 1fr 50px 1fr;
    gap: 12px;
    align-items: center;
}

.learn-keep {
    padding: 11px 14px;
    margin: 6px 0;
    background: var(--accent-soft);
    border-left: 3px solid var(--accent);
    border-radius: 7px;
    color: var(--text);
    font-family: var(--font-mono);
    font-size: 12px;
}

.learn-remove {
    padding: 11px 14px;
    margin: 6px 0;
    background: var(--danger-soft);
    border-left: 3px solid var(--danger);
    border-radius: 7px;
    color: var(--text);
    font-family: var(--font-mono);
    font-size: 12px;
}

@media (max-width: 700px) {

    .learn-two-column {
        grid-template-columns: 1fr;
    }

    .learn-transform {
        grid-template-columns: 1fr;
    }

    .learn-transform-arrow {
        transform: rotate(90deg);
    }

    .learn-dce-row {
        grid-template-columns: 1fr;
    }
}
/* ============================================================
   INSIGHTS / COMPLEXITY
   ============================================================ */

.insight-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px;
    margin-bottom: 14px;
}

.insight-heading {
    color: var(--text);
    font-size: 16px;
    font-weight: 800;
}

.insight-muted {
    color: var(--text-dim);
    font-size: 12.5px;
    line-height: 1.5;
    margin-top: 5px;
}

.complexity-score {
    color: var(--accent);
    font-family: var(--font-mono);
    font-size: 34px;
    font-weight: 800;
}

.complexity-label {
    color: var(--text-dim);
    font-size: 12px;
    margin-top: 2px;
}

.savings-row {
    margin: 14px 0;
}

.savings-label {
    display: flex;
    justify-content: space-between;
    color: var(--text-dim);
    font-family: var(--font-mono);
    font-size: 11px;
    margin-bottom: 6px;
}

.savings-track {
    height: 12px;
    background: var(--bg);
    border: 1px solid var(--border-soft);
    border-radius: 999px;
    overflow: hidden;
}

.savings-fill-before {
    height: 100%;
    width: 100%;
    background: var(--text-dim);
    border-radius: 999px;
}

.savings-fill-after {
    height: 100%;
    background: var(--accent);
    border-radius: 999px;
}

.savings-callout {
    margin-top: 16px;
    padding: 14px 16px;
    background: var(--accent-soft);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    color: var(--text);
    font-size: 13px;
    line-height: 1.5;
}
/* ============================================================
   SOURCE INPUT
   ============================================================ */

.source-label {
    color: var(--text);
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1.2px;
    margin: 18px 0 10px;
}


/* ============================================================
   CODE EXPLANATION
   ============================================================ */

.code-explanation {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 28px 30px;
    margin: 28px 0 34px;
    box-shadow: 0 10px 28px rgba(24, 52, 59, 0.06);
}

.code-explanation-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 22px;
}

.code-explanation-title {
    color: var(--text);
    font-size: 22px;
    font-weight: 800;
}

.code-explanation-subtitle {
    color: var(--text-dim);
    font-size: 14px;
    margin-top: 6px;
}

.code-explanation-label {
    color: var(--accent);
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    white-space: nowrap;
}

.explanation-table {
    width: 100%;
    overflow: hidden;
    border: 1px solid var(--border-soft);
    border-radius: 16px;
}

.explanation-header-row,
.explanation-row {
    display: grid;
    grid-template-columns:
        70px
        minmax(220px, 1fr)
        minmax(300px, 1.4fr);
}

.explanation-header-row {
    background: var(--surface-2);
    color: var(--text-dim);
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}

.explanation-header-row > div {
    padding: 13px 16px;
}

.explanation-row {
    border-top: 1px solid var(--border-soft);
    background: var(--surface);
}

.explanation-row > div {
    padding: 16px;
}

.explanation-line-number {
    color: var(--accent);
    font-family: var(--font-mono);
    font-size: 13px;
    font-weight: 700;
    text-align: center;
    border-right: 1px solid var(--border-soft);
}

.explanation-code {
    color: var(--text);
    font-family: var(--font-mono);
    font-size: 14px;
    font-weight: 600;
    border-right: 1px solid var(--border-soft);
    white-space: pre-wrap;
    word-break: break-word;
}

.explanation-text {
    color: var(--text-dim);
    font-size: 14px;
    line-height: 1.55;
}

.explanation-row:hover {
    background: var(--surface-2);
}

@media (max-width: 900px) {

    .explanation-header-row,
    .explanation-row {
        grid-template-columns: 50px 1fr;
    }

    .explanation-header-row > div:nth-child(3) {
        display: none;
    }

    .explanation-text {
        grid-column: 2;
        border-top: 1px solid var(--border-soft);
        border-right: none;
    }

    .explanation-code {
        border-right: none;
    }
}


/* ============================================================
   PROGRAM OUTPUT
   ============================================================ */

.program-output {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 24px 28px;
    margin: 24px 0 30px;
    box-shadow: 0 8px 24px rgba(24, 52, 59, 0.06);
}

.program-output-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 16px;
}

.program-output-title {
    color: var(--text);
    font-size: 18px;
    font-weight: 800;
    letter-spacing: 0.2px;
}

.program-output-label {
    color: var(--accent);
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.program-output-box {
    background: var(--surface-2);
    border: 1px solid var(--border-soft);
    border-radius: 13px;
    padding: 24px 28px;
    min-height: 110px;
    box-sizing: border-box;
    width: 100%;
    overflow: hidden;
}

.program-output-value {
    display: block !important;
    width: 100% !important;
    box-sizing: border-box !important;

    color: var(--text) !important;
    font-family: var(--font-mono) !important;
    font-size: 20px !important;
    font-weight: 600 !important;

    line-height: 1.8 !important;
    text-align: left !important;

    margin: 0 !important;
    padding: 0 !important;

    white-space: normal !important;
    word-break: break-word !important;
}

.program-output-empty {
    color: var(--text-faint);
    font-family: var(--font-body);
    font-size: 13px;
}
/* ============================================================
   CODE EXPLANATION
   ============================================================ */

.code-explanation {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 28px 30px;
    margin: 26px 0 30px;
    box-shadow: 0 10px 28px rgba(24, 52, 59, 0.06);
}

.code-explanation-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 20px;
    margin-bottom: 22px;
}

.code-explanation-title {
    color: var(--text);
    font-size: 22px;
    font-weight: 800;
}

.code-explanation-subtitle {
    color: var(--text-dim);
    font-size: 14px;
    margin-top: 6px;
}

.code-explanation-label {
    color: var(--accent);
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    white-space: nowrap;
}

.explanation-table {
    width: 100%;
    overflow: hidden;
    border: 1px solid var(--border-soft);
    border-radius: 16px;
}

.explanation-header-row,
.explanation-row {
    display: grid;
    grid-template-columns:
        70px
        minmax(220px, 1fr)
        minmax(300px, 1.4fr);
}

.explanation-header-row {
    background: var(--surface-2);
    color: var(--text-dim);
    font-family: var(--font-mono);
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1px;
}

.explanation-header-row > div {
    padding: 13px 16px;
}

.explanation-row {
    border-top: 1px solid var(--border-soft);
    background: var(--surface);
}

.explanation-row > div {
    padding: 16px;
}

.explanation-line-number {
    color: var(--accent);
    font-family: var(--font-mono);
    font-size: 13px;
    font-weight: 700;
    text-align: center;
    border-right: 1px solid var(--border-soft);
}

.explanation-code {
    color: var(--text);
    font-family: var(--font-mono);
    font-size: 14px;
    font-weight: 600;
    border-right: 1px solid var(--border-soft);
    white-space: pre-wrap;
    word-break: break-word;
}

.explanation-text {
    color: var(--text-dim);
    font-size: 14px;
    line-height: 1.55;
}

.explanation-row:hover {
    background: var(--surface-2);
}

</style>

""",
    unsafe_allow_html=True,
)


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def esc(value):
    return html.escape(str(value))


# ============================================================
# CODE EXPLANATION
# ============================================================

def explain_code_line(line):

    line = line.strip()

    if not line:
        return ""

    # PRINT
    if line.startswith("print("):
        value = line[6:].rstrip(";").rstrip(")")
        return (
            f"Displays the value of {value} "
            f"as program output."
        )

    # WHILE
    if line.startswith("while"):
        return (
            "Checks the condition and repeatedly executes "
            "the statements inside the loop while the "
            "condition is true."
        )

    # IF
    if line.startswith("if"):
        return (
            "Checks the condition and executes the "
            "statements inside the block when it is true."
        )

    # ELSE
    if line.startswith("else"):
        return (
            "Executes the statements in this block when "
            "the previous if condition is false."
        )

    # Opening brace
    if line == "{":
        return "Begins a block of statements."

    # Closing brace
    if line == "}":
        return "Ends the current block of statements."

    # Assignment
    if "=" in line:

        variable, expression = line.split("=", 1)

        variable = variable.strip()
        expression = expression.strip().rstrip(";")

        # Number assignment
        if re.fullmatch(r"-?\d+", expression):
            return (
                f"Assigns the value {expression} "
                f"to variable {variable}."
            )

        # Addition
        if "+" in expression:
            left, right = expression.split("+", 1)
            return (
                f"Adds {left.strip()} and {right.strip()}, "
                f"then stores the result in {variable}."
            )

        # Subtraction
        if "-" in expression:
            left, right = expression.split("-", 1)
            return (
                f"Subtracts {right.strip()} from "
                f"{left.strip()}, then stores the result "
                f"in {variable}."
            )

        # Multiplication
        if "*" in expression:
            left, right = expression.split("*", 1)
            return (
                f"Multiplies {left.strip()} by "
                f"{right.strip()}, then stores the result "
                f"in {variable}."
            )

        # Division
        if "/" in expression:
            left, right = expression.split("/", 1)
            return (
                f"Divides {left.strip()} by "
                f"{right.strip()}, then stores the result "
                f"in {variable}."
            )

        # Variable copy
        return (
            f"Copies the value of {expression} "
            f"into variable {variable}."
        )

    return "Executes this statement."

def block_id(block):
    return getattr(block, "block_id", "?")


def successor_id(value):
    if hasattr(value, "block_id"):
        return getattr(value, "block_id")

    return value


def normalize_set(value):
    """
    Convert whatever liveness returns into a normal Python set.

    This function deliberately does NOT use get_set().
    """

    if value is None:
        return set()

    if isinstance(
        value,
        (set, frozenset, list, tuple)
    ):
        return set(value)

    return {value}


def get_analysis_value(obj, names, bid):
    """
    Safely retrieve a block analysis value.

    Supports dictionaries using either integer or string
    block IDs and supports several common attribute names.
    """

    if obj is None:
        return set()


    # --------------------------------------------------------
    # Object attributes
    # --------------------------------------------------------

    for name in names:

        data = getattr(
            obj,
            name,
            None
        )

        if data is None:
            continue


        if isinstance(
            data,
            dict
        ):

            value = data.get(bid)

            if value is None:
                value = data.get(
                    str(bid)
                )

            if value is not None:
                return normalize_set(
                    value
                )


        else:

            return normalize_set(
                data
            )


    # --------------------------------------------------------
    # Dictionary itself
    # --------------------------------------------------------

    if isinstance(
        obj,
        dict
    ):

        for name in names:

            data = obj.get(name)

            if not isinstance(
                data,
                dict
            ):
                continue

            value = data.get(bid)

            if value is None:
                value = data.get(
                    str(bid)
                )

            if value is not None:
                return normalize_set(
                    value
                )


    return set()



# ============================================================
# LEARNING / COMPLEXITY HELPERS
# ============================================================

def count_ast_metrics(node):
    """
    Count useful structural properties from the existing AST.
    Returns: total nodes, branches, loops.
    """
    total = 0
    branches = 0
    loops = 0

    def walk(value):
        nonlocal total, branches, loops

        if value is None:
            return

        node_type = str(_node_type(value)).lower()

        if isinstance(value, (dict, list, tuple)) or hasattr(value, "__dict__"):
            total += 1

            if node_type == "if":
                branches += 1

            if node_type == "while":
                loops += 1

            children = _children_from_generic(value)

            # Use explicit AST fields where available.
            if node_type == "program":
                statements = _field(
                    value,
                    "statements",
                    "body",
                    "program",
                    "items"
                )
                if statements is not None:
                    walk(statements)
                return

            if node_type == "assignment":
                walk(_field(value, "variable", "target", "name"))
                walk(_field(value, "expression", "value", "right", "rhs"))
                return

            if node_type == "binary":
                walk(_field(value, "left"))
                walk(_field(value, "right"))
                return

            if node_type in {"if", "while"}:
                walk(_field(value, "condition", "test"))

                if node_type == "if":
                    walk(
                        _field(
                            value,
                            "then_branch",
                            "then_body",
                            "then"
                        )
                    )
                    walk(
                        _field(
                            value,
                            "else_branch",
                            "else_body",
                            "else_"
                        )
                    )
                else:
                    walk(_field(value, "body"))
                return

            if isinstance(value, (list, tuple)):
                for item in value:
                    walk(item)
                return

            for _, child in children:
                walk(child)

    walk(node)

    # Lists are structural containers, not actual AST nodes.
    # Keep the metric useful by ensuring it is at least 1 for a valid AST.
    return max(total, 1), branches, loops


def complexity_level(score):
    if score <= 3:
        return "Low"
    if score <= 7:
        return "Medium"
    return "High"


def learn_mode_content():

    st.html(
        """
        <div class="learn-hero">

            <div class="learn-hero-title">
                How a Compiler Thinks
            </div>

            <div class="learn-hero-text">
                Learn how MiniTAC transforms a simple source program
                step by step. Each section explains one compiler phase,
                shows what happens internally, and demonstrates the
                transformation with a small example.
            </div>

        </div>
        """
    )

    # ========================================================
    # COMPLETE COMPILER FLOW
    # ========================================================

    st.html(
        """
        <div class="learn-section">

            <div class="learn-label">
                Complete Compiler Journey
            </div>

            <div class="learn-flow">

                <div class="learn-flow-box">
                    <strong>Source</strong>
                    <span>a = 10 + 20;</span>
                </div>

                <div class="learn-flow-arrow">-&gt;</div>

                <div class="learn-flow-box">
                    <strong>Lexer</strong>
                    <span>Tokens</span>
                </div>

                <div class="learn-flow-arrow">-&gt;</div>

                <div class="learn-flow-box">
                    <strong>Parser</strong>
                    <span>Structure</span>
                </div>

                <div class="learn-flow-arrow">-&gt;</div>

                <div class="learn-flow-box">
                    <strong>AST</strong>
                    <span>Tree</span>
                </div>

                <div class="learn-flow-arrow">-&gt;</div>

                <div class="learn-flow-box">
                    <strong>TAC</strong>
                    <span>Instructions</span>
                </div>

                <div class="learn-flow-arrow">-&gt;</div>

                <div class="learn-flow-box">
                    <strong>Optimizer</strong>
                    <span>Improve</span>
                </div>

                <div class="learn-flow-arrow">-&gt;</div>

                <div class="learn-flow-box">
                    <strong>CFG</strong>
                    <span>Control Flow</span>
                </div>

                <div class="learn-flow-arrow">-&gt;</div>

                <div class="learn-flow-box">
                    <strong>Liveness</strong>
                    <span>Variable Usage</span>
                </div>

                <div class="learn-flow-arrow">-&gt;</div>

                <div class="learn-flow-box">
                    <strong>DCE</strong>
                    <span>Remove Dead Code</span>
                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # 01 LEXER
    # ========================================================

    st.html(
        """
        <div class="learn-section">

            <div class="learn-phase-header">
                <div class="learn-number">PHASE 01</div>
                <div class="learn-title">Lexer</div>
            </div>

            <div class="learn-text">
                The lexer is the first compiler phase. It reads the
                source code character by character and groups those
                characters into meaningful units called tokens.
            </div>

            <div class="learn-label">
                What the lexer does
            </div>

            <div class="learn-flow">

                <div class="learn-flow-box">
                    <strong>Source Code</strong>
                    <span>a = 10 + 20;</span>
                </div>

                <div class="learn-flow-arrow">-&gt;</div>

                <div class="learn-flow-box">
                    <strong>Lexer</strong>
                    <span>Scan + classify</span>
                </div>

                <div class="learn-flow-arrow">-&gt;</div>

                <div class="learn-flow-box">
                    <strong>Token Stream</strong>
                    <span>IDENTIFIER, NUMBER...</span>
                </div>

            </div>

            <div class="learn-label">
                Example
            </div>

            <table class="learn-token-table">

                <tr>
                    <th>Source</th>
                    <th>Token Type</th>
                    <th>Meaning</th>
                </tr>

                <tr>
                    <td>a</td>
                    <td>IDENTIFIER</td>
                    <td>Variable name</td>
                </tr>

                <tr>
                    <td>=</td>
                    <td>ASSIGN</td>
                    <td>Assignment operator</td>
                </tr>

                <tr>
                    <td>10</td>
                    <td>NUMBER</td>
                    <td>Numeric literal</td>
                </tr>

                <tr>
                    <td>+</td>
                    <td>PLUS</td>
                    <td>Addition operator</td>
                </tr>

                <tr>
                    <td>20</td>
                    <td>NUMBER</td>
                    <td>Numeric literal</td>
                </tr>

                <tr>
                    <td>;</td>
                    <td>SEMICOLON</td>
                    <td>Statement terminator</td>
                </tr>

            </table>

            <div class="learn-two-column">

                <div class="learn-info-box">

                    <div class="learn-info-title">
                        Why is it needed?
                    </div>

                    <div class="learn-info-text">
                        The parser should not have to understand individual
                        characters. The lexer converts raw text into a
                        structured token stream that the parser can consume.
                    </div>

                </div>

                <div class="learn-info-box">

                    <div class="learn-info-title">
                        Common errors
                    </div>

                    <div class="learn-info-text">
                        Invalid or unknown characters, malformed numbers,
                        and unsupported symbols can be detected during
                        lexical analysis.
                    </div>

                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # 02 PARSER
    # ========================================================

    st.html(
        """
        <div class="learn-section">

            <div class="learn-phase-header">
                <div class="learn-number">PHASE 02</div>
                <div class="learn-title">Parser</div>
            </div>

            <div class="learn-text">
                The parser receives the token stream from the lexer and
                checks whether the tokens follow the grammar of the
                language. It then builds a structured representation
                of the program.
            </div>

            <div class="learn-label">
                Transformation
            </div>

            <div class="learn-transform">

                <div class="learn-transform-box">

                    <div class="learn-transform-title">
                        TOKEN STREAM
                    </div>

                    <div class="learn-code">IDENTIFIER
ASSIGN
NUMBER
PLUS
NUMBER
SEMICOLON</div>

                </div>

                <div class="learn-transform-arrow">
                    -&gt;
                </div>

                <div class="learn-transform-box">

                    <div class="learn-transform-title">
                        PARSED STRUCTURE
                    </div>

                    <div class="learn-code">Assignment
    |
    +-- variable: a
    |
    +-- expression
          |
          +-- 10 + 20</div>

                </div>

            </div>

            <div class="learn-two-column">

                <div class="learn-info-box">

                    <div class="learn-info-title">
                        Syntax checking
                    </div>

                    <div class="learn-info-text">
                        The parser verifies that operators, operands,
                        parentheses and statement terminators appear
                        in valid positions.
                    </div>

                </div>

                <div class="learn-info-box">

                    <div class="learn-info-title">
                        MiniTAC example
                    </div>

                    <div class="learn-info-text">
                        The statement a = 10 + 20; is recognized as a
                        valid assignment containing a binary expression.
                    </div>

                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # 03 AST
    # ========================================================

    st.html(
        """
        <div class="learn-section">

            <div class="learn-phase-header">
                <div class="learn-number">PHASE 03</div>
                <div class="learn-title">Abstract Syntax Tree</div>
            </div>

            <div class="learn-text">
                The AST represents the meaning and structure of the
                program as a tree. Parent nodes describe larger
                operations while child nodes describe their components.
            </div>

            <div class="learn-label">
                Example: a = 10 + 20;
            </div>

            <div class="learn-ast">

                <div class="learn-ast-node">
                    ASSIGNMENT
                </div>

                <div class="learn-flow-arrow">
                    |
                </div>

                <div class="learn-ast-children">

                    <div class="learn-ast-child">
                        Variable: a
                    </div>

                    <div class="learn-ast-child">
                        BINARY: +
                    </div>

                </div>

                <div class="learn-flow-arrow">
                    |
                </div>

                <div class="learn-ast-children">

                    <div class="learn-ast-child">
                        NUMBER: 10
                    </div>

                    <div class="learn-ast-child">
                        NUMBER: 20
                    </div>

                </div>

            </div>

            <div class="learn-two-column">

                <div class="learn-info-box">

                    <div class="learn-info-title">
                        What does the tree tell us?
                    </div>

                    <div class="learn-info-text">
                        The assignment is the main operation. Its expression
                        is an addition, and the addition has two operands:
                        10 and 20.
                    </div>

                </div>

                <div class="learn-info-box">

                    <div class="learn-info-title">
                        Why use a tree?
                    </div>

                    <div class="learn-info-text">
                        A tree makes relationships between operations
                        explicit, which makes later compiler phases easier
                        to implement.
                    </div>

                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # 04 TAC
    # ========================================================

    st.html(
        """
        <div class="learn-section">

            <div class="learn-phase-header">
                <div class="learn-number">PHASE 04</div>
                <div class="learn-title">Three Address Code</div>
            </div>

            <div class="learn-text">
                TAC converts complex expressions into simple instructions.
                Temporary variables such as t1 allow the compiler to break
                a large expression into smaller operations.
            </div>

            <div class="learn-label">
                AST to TAC
            </div>

            <div class="learn-transform">

                <div class="learn-transform-box">

                    <div class="learn-transform-title">
                        AST
                    </div>

                    <div class="learn-code">ASSIGNMENT
     |
     +-- a
     |
     +-- 10 + 20</div>

                </div>

                <div class="learn-transform-arrow">
                    -&gt;
                </div>

                <div class="learn-transform-box">

                    <div class="learn-transform-title">
                        TAC
                    </div>

                    <div class="learn-code">t1 = 10 + 20
a = t1</div>

                </div>

            </div>

            <div class="learn-info-box">

                <div class="learn-info-title">
                    Why Three Address Code?
                </div>

                <div class="learn-info-text">
                    TAC provides a simple intermediate representation
                    between the source language and lower-level execution.
                    It also gives optimization passes a convenient form
                    to analyze.
                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # 05 OPTIMIZER
    # ========================================================

    st.html(
        """
        <div class="learn-section">

            <div class="learn-phase-header">
                <div class="learn-number">PHASE 05</div>
                <div class="learn-title">Optimizer</div>
            </div>

            <div class="learn-text">
                The optimizer attempts to produce an equivalent program
                that is simpler or more efficient. MiniTAC demonstrates
                several optimization techniques.
            </div>

            <div class="learn-label">
                Example
            </div>

            <div class="learn-transform">

                <div class="learn-transform-box">

                    <div class="learn-transform-title">
                        BEFORE
                    </div>

                    <div class="learn-code">t1 = 10 + 20
b = t1
c = b + 0</div>

                </div>

                <div class="learn-transform-arrow">
                    -&gt;
                </div>

                <div class="learn-transform-box">

                    <div class="learn-transform-title">
                        AFTER
                    </div>

                    <div class="learn-code">t1 = 30
b = 30
c = 30</div>

                </div>

            </div>

            <div class="learn-two-column">

                <div class="learn-info-box">

                    <div class="learn-info-title">
                        Constant Folding
                    </div>

                    <div class="learn-info-text">
                        Calculates expressions whose operands are already
                        known constants.
                    </div>

                </div>

                <div class="learn-info-box">

                    <div class="learn-info-title">
                        Algebraic Simplification
                    </div>

                    <div class="learn-info-text">
                        Rewrites identities such as x + 0 into x and
                        x * 1 into x.
                    </div>

                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # 06 CFG
    # ========================================================

    st.html(
        """
        <div class="learn-section">

            <div class="learn-phase-header">
                <div class="learn-number">PHASE 06</div>
                <div class="learn-title">Control Flow Graph</div>
            </div>

            <div class="learn-text">
                A CFG divides the program into basic blocks and connects
                those blocks according to the possible execution paths.
            </div>

            <div class="learn-label">
                Example with a branch
            </div>

            <div class="learn-cfg">

                <div class="learn-cfg-block">
                    B0<br>
                    a = 10
                </div>

                <div class="learn-cfg-arrow">
                    |
                </div>

                <div class="learn-cfg-block learn-cfg-decision">
                    B1<br>
                    a &gt; 5 ?
                </div>

                <div class="learn-cfg-arrow">
                    / \
                </div>

                <div class="learn-ast-children">

                    <div class="learn-cfg-block">
                        B2<br>
                        b = 20
                    </div>

                    <div class="learn-cfg-block">
                        B3<br>
                        b = 30
                    </div>

                </div>

                <div class="learn-cfg-arrow">
                    \ /
                </div>

                <div class="learn-cfg-block">
                    B4<br>
                    c = b
                </div>

            </div>

            <div class="learn-info-box">

                <div class="learn-info-title">
                    Why CFG matters
                </div>

                <div class="learn-info-text">
                    Control-flow information is important for analyses
                    such as liveness and optimizations such as dead-code
                    elimination.
                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # 07 LIVENESS
    # ========================================================

    st.html(
        """
        <div class="learn-section">

            <div class="learn-phase-header">
                <div class="learn-number">PHASE 07</div>
                <div class="learn-title">Liveness Analysis</div>
            </div>

            <div class="learn-text">
                Liveness analysis determines whether a variable will be
                needed later. A variable is live when its current value
                may be used in the future.
            </div>

            <div class="learn-label">
                Backward data-flow analysis
            </div>

            <div class="learn-flow">

                <div class="learn-flow-box">
                    <strong>LIVE IN</strong>
                    <span>Variables needed before block</span>
                </div>

                <div class="learn-flow-arrow">
                    &lt;-
                </div>

                <div class="learn-flow-box">
                    <strong>Basic Block</strong>
                    <span>USE / DEF</span>
                </div>

                <div class="learn-flow-arrow">
                    &lt;-
                </div>

                <div class="learn-flow-box">
                    <strong>LIVE OUT</strong>
                    <span>Variables needed after block</span>
                </div>

            </div>

            <div class="learn-two-column">

                <div class="learn-info-box">

                    <div class="learn-info-title">
                        USE
                    </div>

                    <div class="learn-info-text">
                        Variables whose current values are read by
                        instructions in a block.
                    </div>

                </div>

                <div class="learn-info-box">

                    <div class="learn-info-title">
                        DEF
                    </div>

                    <div class="learn-info-text">
                        Variables whose values are assigned or defined
                        by instructions in a block.
                    </div>

                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # 08 DCE
    # ========================================================

    st.html(
        """
        <div class="learn-section">

            <div class="learn-phase-header">
                <div class="learn-number">PHASE 08</div>
                <div class="learn-title">Dead Code Elimination</div>
            </div>

            <div class="learn-text">
                DCE removes calculations whose results are not needed.
                MiniTAC uses liveness information to determine whether
                temporary assignments can safely be removed.
            </div>

            <div class="learn-label">
                Example
            </div>

            <div class="learn-dce-row">

                <div class="learn-transform-box">

                    <div class="learn-transform-title">
                        BEFORE DCE
                    </div>

                    <div class="learn-code">t1 = 10 + 20
t2 = t1 * 5
t3 = 100
PRINT t2</div>

                </div>

                <div class="learn-transform-arrow">
                    -&gt;
                </div>

                <div class="learn-transform-box">

                    <div class="learn-transform-title">
                        ANALYSIS
                    </div>

                    <div class="learn-keep">
                        t1 is used
                    </div>

                    <div class="learn-keep">
                        t2 is used
                    </div>

                    <div class="learn-remove">
                        t3 is never used
                    </div>

                </div>

            </div>

            <div class="learn-transform-box" style="margin-top:16px;">

                <div class="learn-transform-title">
                    AFTER DCE
                </div>

                <div class="learn-code">t1 = 10 + 20
t2 = t1 * 5
PRINT t2</div>

            </div>

            <div class="learn-info-box" style="margin-top:16px;">

                <div class="learn-info-title">
                    Key idea
                </div>

                <div class="learn-info-text">
                    Removing an unused temporary does not change the
                    observable result of the program, so the unnecessary
                    computation can be eliminated.
                </div>

            </div>

        </div>
        """
    )


    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    st.html(
        """
        <div class="learn-hero">

            <div class="learn-hero-title">
                The Big Picture
            </div>

            <div class="learn-hero-text">
                The important idea is that no single compiler phase does
                everything. Each phase transforms the program into a form
                that makes the next phase easier to perform.
            </div>

            <div class="learn-flow">

                <div class="learn-flow-box">
                    <strong>Understand</strong>
                    <span>Lexer + Parser</span>
                </div>

                <div class="learn-flow-arrow">-&gt;</div>

                <div class="learn-flow-box">
                    <strong>Represent</strong>
                    <span>AST + TAC</span>
                </div>

                <div class="learn-flow-arrow">-&gt;</div>

                <div class="learn-flow-box">
                    <strong>Improve</strong>
                    <span>Optimizer</span>
                </div>

                <div class="learn-flow-arrow">-&gt;</div>

                <div class="learn-flow-box">
                    <strong>Analyze</strong>
                    <span>CFG + Liveness</span>
                </div>

                <div class="learn-flow-arrow">-&gt;</div>

                <div class="learn-flow-box">
                    <strong>Clean</strong>
                    <span>DCE</span>
                </div>

            </div>

        </div>
        """
    )

    st.html(
        """
        <div class="card">
            <div class="card-title">Learn Mode</div>
            <div class="card-subtitle">
                Explore what each compiler phase does without needing to
                understand the implementation first.
            </div>
        </div>
        """
    )

    

   
# ============================================================
# AST VISUALIZATION
# ============================================================

def ast_escape(value):
    return html.escape(str(value))


def _node_type(node):
    """Return the AST node type for dicts or normal Python objects."""

    if isinstance(node, dict):
        return (
            node.get("type")
            or node.get("node_type")
            or node.get("kind")
            or node.get("tag")
            or "Node"
        )

    return node.__class__.__name__


def _field(node, *names):
    """Read the first available field from a dict or object."""

    if isinstance(node, dict):
        for name in names:
            if name in node:
                return node[name]
        return None

    for name in names:
        if hasattr(node, name):
            return getattr(node, name)

    return None


def _children_from_generic(node):
    """Build children for an unknown AST node without exposing Python internals."""

    children = []

    if isinstance(node, dict):
        items = node.items()
    elif hasattr(node, "__dict__"):
        items = vars(node).items()
    else:
        return children

    for key, value in items:
        if key in {"type", "node_type", "kind", "tag"}:
            continue

        if value is None:
            continue

        if isinstance(value, (dict, list, tuple)) or hasattr(value, "__dict__"):
            children.append((str(key), value))

    return children


def ast_node_info(node):
    """
    Convert the MiniTAC AST into a clean visual tree.

    Important:
    Assignment and Binary nodes are handled explicitly so the UI
    shows real compiler relationships instead of generic 'dict' nodes.
    """

    if node is None:
        return "NULL", "", []


    # --------------------------------------------------------
    # PROGRAM / LIST OF STATEMENTS
    # --------------------------------------------------------

    if isinstance(node, (list, tuple)):

        children = [
            (f"Statement {index + 1}", item)
            for index, item in enumerate(node)
        ]

        return "PROGRAM", "", children


    node_type = str(_node_type(node))


    # --------------------------------------------------------
    # PROGRAM NODE
    # --------------------------------------------------------

    if node_type.lower() == "program":

        statements = _field(
            node,
            "statements",
            "body",
            "program",
            "items"
        )

        if statements is not None:

            if not isinstance(
                statements,
                (list, tuple)
            ):
                statements = [statements]

            children = [
                (f"Statement {index + 1}", item)
                for index, item in enumerate(statements)
            ]

            return "PROGRAM", "", children


    # --------------------------------------------------------
    # ASSIGNMENT
    # --------------------------------------------------------

    if node_type.lower() == "assignment":

        variable = _field(
            node,
            "variable",
            "target",
            "name"
        )

        expression = _field(
            node,
            "expression",
            "value",
            "right",
            "rhs"
        )

        children = []

        if variable is not None:

            # A plain variable name is displayed as Identifier.
            if isinstance(variable, str):
                variable_node = {
                    "type": "Identifier",
                    "name": variable
                }
            else:
                variable_node = variable

            children.append(
                ("Variable", variable_node)
            )

        if expression is not None:
            children.append(
                ("Expression", expression)
            )

        return (
            "ASSIGNMENT",
            "",
            children
        )


    # --------------------------------------------------------
    # BINARY EXPRESSION
    # --------------------------------------------------------

    if node_type.lower() == "binary":

        operator = _field(
            node,
            "operator",
            "op"
        )

        left = _field(
            node,
            "left"
        )

        right = _field(
            node,
            "right"
        )

        children = []

        if left is not None:
            children.append(
                ("Left", left)
            )

        if right is not None:
            children.append(
                ("Right", right)
            )

        return (
            "BINARY",
            f"operator: {operator}" if operator is not None else "",
            children
        )


    # --------------------------------------------------------
    # IDENTIFIER
    # --------------------------------------------------------

    if node_type.lower() in {
        "identifier",
        "id",
        "variable"
    }:

        name = _field(
            node,
            "name",
            "value"
        )

        return (
            "IDENTIFIER",
            f"name: {name}" if name is not None else "",
            []
        )


    # --------------------------------------------------------
    # NUMBER
    # --------------------------------------------------------

    if node_type.lower() in {
        "number",
        "literal",
        "constant"
    }:

        value = _field(
            node,
            "value",
            "number"
        )

        return (
            "NUMBER",
            f"value: {value}" if value is not None else "",
            []
        )


    # --------------------------------------------------------
    # IF
    # --------------------------------------------------------

    if node_type.lower() == "if":

        condition = _field(
            node,
            "condition",
            "test"
        )

        then_branch = _field(
            node,
            "then_branch",
            "then_body",
            "then"
        )

        else_branch = _field(
            node,
            "else_branch",
            "else_body",
            "else_"
        )

        children = []

        if condition is not None:
            children.append(
                ("Condition", condition)
            )

        if then_branch is not None:
            children.append(
                ("Then", then_branch)
            )

        if else_branch is not None:
            children.append(
                ("Else", else_branch)
            )

        return (
            "IF",
            "",
            children
        )


    # --------------------------------------------------------
    # WHILE
    # --------------------------------------------------------

    if node_type.lower() == "while":

        condition = _field(
            node,
            "condition",
            "test"
        )

        body = _field(
            node,
            "body"
        )

        children = []

        if condition is not None:
            children.append(
                ("Condition", condition)
            )

        if body is not None:
            children.append(
                ("Body", body)
            )

        return (
            "WHILE",
            "",
            children
        )


    # --------------------------------------------------------
    # GENERIC OBJECT / DICT
    # --------------------------------------------------------

    children = _children_from_generic(node)

    value_parts = []

    if isinstance(node, dict):
        items = node.items()
    elif hasattr(node, "__dict__"):
        items = vars(node).items()
    else:
        items = []

    for key, value in items:

        if key in {
            "type",
            "node_type",
            "kind",
            "tag"
        }:
            continue

        if value is None:
            continue

        if not (
            isinstance(value, (dict, list, tuple))
            or hasattr(value, "__dict__")
        ):
            value_parts.append(
                f"{key}: {value}"
            )

    return (
        node_type.upper(),
        " | ".join(value_parts),
        children
    )


def render_ast_node(node, relation="", depth=0):

    if depth > 20:
        return """
        <div class="ast-item ast-leaf">
            <div class="ast-node">
                <div class="ast-node-type">...</div>
            </div>
        </div>
        """

    node_type, node_value, children = ast_node_info(node)

    is_leaf = not children

    program_class = (
        " program"
        if node_type == "PROGRAM"
        else ""
    )

    leaf_class = (
        " ast-leaf"
        if is_leaf
        else ""
    )

    value_html = ""

    if node_value:
        value_html = f"""
        <div class="ast-node-value">
            {ast_escape(node_value)}
        </div>
        """

    relation_html = ""

    if relation:
        relation_html = f"""
        <div class="ast-relation">
            {ast_escape(relation)}
        </div>
        """

    # ========================================================
    # PROGRAM NODE
    # ========================================================

    if node_type == "PROGRAM":

        statement_parts = []

        for index, child in enumerate(children):

            child_html = render_ast_node(
                child[1],
                "",
                depth + 1
            )

            statement_parts.append(
                f"""
                <div class="ast-statement">
                    <div class="ast-statement-cell">

                        <div class="ast-relation">
                            STATEMENT {index + 1}
                        </div>

                        {child_html}

                    </div>
                </div>
                """
            )

        return f"""
        <div class="ast-item">
            <div class="ast-item-inner">
                <div class="ast-node-cell">

                    <div class="ast-node program">

                        <div class="ast-node-type">
                            PROGRAM
                        </div>

                    </div>

                </div>
            </div>

            <div class="ast-program-children">

                {"".join(statement_parts)}

            </div>

        </div>
        """

    # ========================================================
    # NORMAL NODE
    # ========================================================

    children_html = ""

    if children:

        child_parts = []

        for child_relation, child in children:

            child_html = render_ast_node(
                child,
                child_relation,
                depth + 1
            )

            child_parts.append(
                f"""
                <div class="ast-child-cell">
                    <div class="ast-child-inner">
                        {child_html}
                    </div>
                </div>
                """
            )

        children_html = f"""
        <div class="ast-children">
            <div class="ast-children-row">
                {"".join(child_parts)}
            </div>
        </div>
        """

    return f"""
    <div class="ast-item{leaf_class}">
        <div class="ast-item-inner">
            <div class="ast-node-cell">

                {relation_html}

                <div class="ast-node{program_class}">

                    <div class="ast-node-type">
                        {ast_escape(node_type)}
                    </div>

                    {value_html}

                </div>

            </div>
        </div>

        {children_html}

    </div>
    """


def render_ast_tree(ast):

    return f"""
    <div class="ast-wrapper">

        <div class="ast-tree">

            {render_ast_node(ast)}

        </div>

    </div>
    """


# ============================================================
# HEADER
# ============================================================

st.html(
    """
    <div class="hero">

        <div class="hero-small">
            How a compiler thinks
        </div>

        <div class="hero-title">
            MiniTAC Compiler
        </div>

        <div class="hero-subtitle">
            Type in a small program below and watch each step a
            compiler takes to turn it into something a computer
            can run - explained in plain language, no compiler
            course required.
        </div>

    </div>
    """
)


# ============================================================
# PIPELINE
# ============================================================

st.html(
    """
    <div class="pipeline">

        <div class="pipeline-item active">
            Lexer
        </div>

        <div class="pipeline-arrow">-></div>

        <div class="pipeline-item active">
            Parser
        </div>

        <div class="pipeline-arrow">-></div>

        <div class="pipeline-item active">
            AST
        </div>

        <div class="pipeline-arrow">-></div>

        <div class="pipeline-item active">
            TAC
        </div>

        <div class="pipeline-arrow">-></div>

        <div class="pipeline-item active">
            Optimizer
        </div>

        <div class="pipeline-arrow">-></div>

        <div class="pipeline-item active">
            CFG
        </div>

        <div class="pipeline-arrow">-></div>

        <div class="pipeline-item active">
            Liveness
        </div>

        <div class="pipeline-arrow">-></div>

        <div class="pipeline-item active">
            DCE
        </div>

    </div>

    <div style="text-align:center; color: var(--text-faint); font-size: 12.5px; margin: 4px 0 30px;">
        Each stage below is a step your code passes through, in order, left to right.
    </div>
    """
)

# ============================================================
# COMPILER MODE / LEARN MODE
# ============================================================

st.html(
    """
    <div class="mode-card">
        <div class="mode-title">Choose your experience</div>
        <div class="mode-subtitle">
            Compile a program or learn what happens inside each compiler phase.
        </div>
    </div>
    """
)

mode = st.radio(
    "View",
    ["Compiler Mode", " Learn Mode"],
    horizontal=True,
    label_visibility="collapsed",
)

if mode == " Learn Mode":
    learn_mode_content()
    st.stop()


# ============================================================
# SOURCE
# ============================================================

st.html(
    """
    <div class="card">

        <div class="card-title">
            1. Write your program
        </div>

        <div class="card-subtitle">
            Type a short program using simple statements like
            <code>a = 10;</code> and <code>c = a + b;</code>.
            Then press Compile to see every step the compiler
            takes to process it.
        </div>

    </div>
    """
)


default_source = ""

# ============================================================
# TYPE YOUR CODE
# ============================================================

st.html(
    """
    <div class="source-label">
        TYPE YOUR CODE HERE
    </div>
    """
)

source = st.text_area(
    "source",
    value=default_source,
    height=260,
    placeholder="Type your MiniTAC program here...",
    label_visibility="collapsed",
)


# ============================================================
# COMPILE BUTTON
# ============================================================

compile_button = st.button(
    "Compile Program",
    type="primary",
    use_container_width=True,
)


# ============================================================
# CODE EXPLANATION
# ============================================================

if source.strip():

    explanation_rows = ""

    source_lines = source.splitlines()

    for line_number, line in enumerate(
        source_lines,
        start=1
    ):

        stripped_line = line.strip()

        if not stripped_line:
            continue

        explanation = explain_code_line(
            stripped_line
        )

        explanation_rows += f"""
        <div class="explanation-row">

            <div class="explanation-line-number">
                {line_number}
            </div>

            <div class="explanation-code">
                {html.escape(stripped_line)}
            </div>

            <div class="explanation-text">
                {html.escape(explanation)}
            </div>

        </div>
        """

    st.html(
        f"""
        <div class="code-explanation">

            <div class="code-explanation-header">

                <div>

                    <div class="code-explanation-title">
                        Code Explanation
                    </div>

                    <div class="code-explanation-subtitle">
                        Understand what each line of your program does.
                    </div>

                </div>

                <div class="code-explanation-label">
                    LINE BY LINE
                </div>

            </div>

            <div class="explanation-table">

                <div class="explanation-header-row">

                    <div>LINE</div>
                    <div>CODE</div>
                    <div>EXPLANATION</div>

                </div>

                {explanation_rows}

            </div>

        </div>
        """
    )


# =====================================================
# PROFESSIONAL COMPILATION ERROR DISPLAY
# =====================================================

if st.session_state.get("compile_error") is not None:

    error = st.session_state["compile_error"]

    # -------------------------------------------------
    # Get error information
    # -------------------------------------------------

    error_message = getattr(
        error,
        "message",
        str(error)
    )

    error_line = getattr(
        error,
        "line",
        None
    )

    error_column = getattr(
        error,
        "column",
        None
    )

    # -------------------------------------------------
    # Determine error type
    # -------------------------------------------------

    error_text = str(error)

    if "Lexer Error" in error_text:

        error_type = "Problem reading your characters (lexical error)"

    elif "Parser Error" in error_text:

        error_type = "Problem with the structure of your code (syntax error)"

    else:

        error_type = "Compilation error"

    # -------------------------------------------------
    # ERROR HEADER
    # -------------------------------------------------

    st.html(
        f"""
        <div class="compiler-error-card">

            <div class="compiler-error-title">
                Your program couldn't be compiled
            </div>

            <div class="compiler-error-type">
                {html.escape(error_type)}
            </div>

        </div>
        """
    )

    # -------------------------------------------------
    # ERROR LOCATION
    # -------------------------------------------------

    if error_line is not None:

        location_text = f"Line {error_line}"

        if error_column is not None:

            location_text += (
                f" - Column {error_column}"
            )

        st.html(
            f"""
            <div class="compiler-error-location">
                {html.escape(location_text)}
            </div>
            """
        )

    # -------------------------------------------------
    # ERROR MESSAGE
    # -------------------------------------------------

    st.html(
        f"""
        <div class="compiler-error-message">

            <div class="error-label">
                What went wrong
            </div>

            <div class="error-text">
                {html.escape(error_message)}
            </div>

        </div>
        """
    )

    # -------------------------------------------------
    # SOURCE LOCATION
    # -------------------------------------------------

    if error_line is not None:

        source_lines = source.splitlines()

        if 1 <= error_line <= len(source_lines):

            st.html(
                """
                <div class="error-source-title">
                    Where it happened
                </div>
                """
            )

            start_line = max(
                1,
                error_line - 2
            )

            end_line = min(
                len(source_lines),
                error_line + 2
            )

            source_html = ""

            for number in range(
                start_line,
                end_line + 1
            ):

                line_text = source_lines[
                    number - 1
                ]

                escaped_line = html.escape(
                    line_text
                )

                # -------------------------------------
                # Error line
                # -------------------------------------

                if number == error_line:

                    source_html += f"""
                    <div class="error-source-line active">

                        <span class="line-number">
                            {number}
                        </span>

                        <span class="line-code">
                            {escaped_line}
                        </span>

                    </div>
                    """

                    # ---------------------------------
                    # Caret
                    # ---------------------------------

                    if error_column is not None:

                        caret_position = max(
                            0,
                            error_column - 1
                        )

                        caret_position = min(
                            caret_position,
                            len(line_text)
                        )

                        source_html += f"""
                        <div class="error-caret-row">

                            <span class="line-number">
                            </span>

                            <span class="error-caret">{" " * caret_position}^</span>

                        </div>
                        """

                # -------------------------------------
                # Normal line
                # -------------------------------------

                else:

                    source_html += f"""
                    <div class="error-source-line">

                        <span class="line-number">
                            {number}
                        </span>

                        <span class="line-code">
                            {escaped_line}
                        </span>

                    </div>
                    """

            # -----------------------------------------
            # Render complete source box
            # -----------------------------------------

            st.html(
                f"""
                <div class="error-source-box">
                    {source_html}
                </div>
                """
            )


# ============================================================
# COMPILE
# ============================================================

if compile_button:

    try:

        compiler = Compiler(source)

        compiler.compile()

        st.session_state["compiler_results"] = (
            compiler.get_results()
        )

        st.session_state["compiled"] = True
        st.session_state["compile_error"] = None

    except Exception as error:

        st.session_state["compiled"] = False
        st.session_state["compile_error"] = error

# ============================================================
# RESULTS
# ============================================================

if st.session_state.get(
    "compiled",
    False
):

    results = st.session_state[
        "compiler_results"
    ]


    tokens = results.get(
        "tokens",
        []
    )

    ast = results.get(
        "ast"
    )

    tac = results.get(
        "tac",
        []
    )

    optimized_tac = results.get(
        "optimized_tac",
        []
    )

    cfg = results.get(
        "cfg"
    )

    liveness = results.get(
        "liveness"
    )

    optimizer_stats = results.get(
        "optimizer_statistics",
        {}
    )

    dce_removed = results.get(
        "dce_removed",
        0
    )
    program_output = results.get(
    "program_output",
    []
    )

    ast_nodes, branch_count, loop_count = count_ast_metrics(ast)
    cyclomatic = 1 + branch_count
    complexity = complexity_level(cyclomatic)


    # ========================================================
    # SUCCESS
    # ========================================================

    st.html(
        """
        <div class="info">

            <strong>OK Your program compiled successfully.</strong>

            It passed through every stage below - explore each tab
            to see what happened at each step.

        </div>
        """
    )


    # ========================================================
    # METRICS
    # ========================================================

    st.markdown(
        "### Quick summary"
    )


    c1, c2, c3, c4, c5 = st.columns(5)


    with c1:

        st.html(
            f"""
            <div class="metric">

                <div class="metric-value">
                    {len(tokens)}
                </div>

                <div class="metric-label">
                    Words found
                </div>

            </div>
            """
        )


    with c2:

        st.html(
            f"""
            <div class="metric">

                <div class="metric-value">
                    {len(tac)}
                </div>

                <div class="metric-label">
                    Steps before cleanup
                </div>

            </div>
            """
        )


    with c3:

        st.html(
            f"""
            <div class="metric">

                <div class="metric-value">
                    {len(optimized_tac)}
                </div>

                <div class="metric-label">
                    Steps after cleanup
                </div>

            </div>
            """
        )


    with c4:

        block_count = (
            len(cfg.blocks)
            if cfg is not None
            else 0
        )

        st.html(
            f"""
            <div class="metric">

                <div class="metric-value">
                    {block_count}
                </div>

                <div class="metric-label">
                    Code sections
                </div>

            </div>
            """
        )


    with c5:

        st.html(
            f"""
            <div class="metric">

                <div class="metric-value">
                    {dce_removed}
                </div>

                <div class="metric-label">
                    Unneeded steps removed
                </div>

            </div>
            """
        )
            # ========================================================
    # PROGRAM OUTPUT
    # ========================================================

    output_text = "\n".join(
        str(value)
        for value in program_output
    )

    if output_text:

        st.html(
            f"""
            <div class="program-output">

                <div class="program-output-header">

                    <div class="program-output-title">
                        Program Output
                    </div>

                    <div class="program-output-label">
                        Execution Result
                    </div>

                </div>

                <div class="program-output-box">

                    <div class="program-output-value">
                        {esc(output_text)}
                    </div>

                </div>

            </div>
            """
        )

    else:

        st.html(
            """
            <div class="program-output">

                <div class="program-output-header">

                    <div class="program-output-title">
                        Program Output
                    </div>

                    <div class="program-output-label">
                        No Printed Values
                    </div>

                </div>

                <div class="program-output-box">

                    <div class="program-output-empty">
                        Add a print(expression); statement to see
                        the program result here.
                    </div>

                </div>

            </div>
            """
        )


    # ========================================================
    # TABS
    # ========================================================

    tabs = st.tabs(
        [
            "1. Words (Tokens)",
            "2. Structure (AST)",
            "3. Instructions (TAC)",
            "4. Cleanup (Optimization)",
            "5. Sections (CFG)",
            "6. Usage (Liveness)",
            "7. Trim (DCE)",
            "8. Insights",
        ]
    )


    # ========================================================
    # TOKENS
    # ========================================================

    with tabs[0]:

        st.html(
            """
            <div class="card">

                <div class="card-title">
                    Step 1  |  Breaking your text into words
                </div>

                <div class="card-subtitle">
                    Before the computer can understand your program, it
                    splits the raw text into small meaningful pieces -
                    called tokens - like numbers, names, and symbols.
                    This is exactly like reading a sentence one word at
                    a time.
                </div>

            </div>
            """
        )


        rows = []


        for index, token in enumerate(
            tokens
        ):

            rows.append(
                {
                    "#": index + 1,
                    "Type": getattr(
                        token,
                        "type",
                        ""
                    ),
                    "Value": getattr(
                        token,
                        "value",
                        ""
                    ),
                }
            )


        if rows:

            st.dataframe(
                rows,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "No words were found - try typing a program above."
            )


    # ========================================================
    # AST
    # ========================================================

    with tabs[1]:

        st.html(
            """
            <div class="card">

                <div class="card-title">
                    Step 2  |  Understanding the sentence structure
                </div>

                <div class="card-subtitle">
                    The tokens are arranged into a tree that shows how
                    each part of your program relates to the others -
                    similar to diagramming the grammar of a sentence.
                    This tree is called the Abstract Syntax Tree, or
                    AST for short.
                </div>

            </div>
            """
        )


        try:

            ast_visual = render_ast_tree(
                ast
            )

            st.html(
                f"""
                <div class="ast-area">

                    {ast_visual}

                </div>
                """
            )

        except Exception as error:

            st.error(
                f"We couldn't draw the tree for this program: {error}"
            )


        with st.expander(
            "See the raw tree data (technical)"
        ):

            st.write(ast)


    # ========================================================
    # TAC
    # ========================================================

    with tabs[2]:

        st.html(
            """
            <div class="card">

                <div class="card-title">
                    Step 3  |  Rewriting as simple instructions
                </div>

                <div class="card-subtitle">
                    The tree is turned into a straight list of very
                    simple instructions, each doing at most one
                    calculation - like <code>t1 = a + b</code>. This
                    format is called Three Address Code, or TAC, and
                    it's much closer to what a real processor
                    understands.
                </div>

            </div>
            """
        )


        st.code(
            "\n".join(
                str(x)
                for x in tac
            ),
            language="text",
        )


        st.markdown(
            "### After cleanup (optimized)"
        )


        st.code(
            "\n".join(
                str(x)
                for x in optimized_tac
            ),
            language="text",
        )


    # ========================================================
    # OPTIMIZATION
    # ========================================================

    with tabs[3]:

        st.html(
            """
            <div class="card">

                <div class="card-title">
                    Step 4  |  Tidying up the instructions
                </div>

                <div class="card-subtitle">
                    The compiler now looks over the instruction list
                    for anything wasteful - repeated calculations,
                    unnecessary steps - and rewrites it to do the same
                    job with less work. The table below shows what
                    kind of tidying was done, and how many times.
                </div>

            </div>
            """
        )


        if optimizer_stats:

            optimization_rows = []

            for name, count in (
                optimizer_stats.items()
            ):

                optimization_rows.append(
                    {
                        "Cleanup applied":
                            name,
                        "Times used":
                            count,
                    }
                )


            st.dataframe(
                optimization_rows,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "No cleanup was needed for this program."
            )


        st.markdown(
            "### Before tidying up"
        )

        st.code(
            "\n".join(
                str(x)
                for x in tac
            ),
            language="text",
        )


        st.markdown(
            "### After tidying up"
        )

        st.code(
            "\n".join(
                str(x)
                for x in optimized_tac
            ),
            language="text",
        )


    # ========================================================
    # CFG
    # ========================================================

    with tabs[4]:

        st.html(
            """
            <div class="card">

                <div class="card-title">
                    Step 5  |  Mapping out the order things run in
                </div>

                <div class="card-subtitle">
                    The instructions are grouped into sections - each
                    one runs straight through, top to bottom, with no
                    jumps in the middle. The arrows below show which
                    section can run after which. This map is called
                    the Control Flow Graph, or CFG.
                </div>

            </div>
            """
        )


        if cfg is None:

            st.warning(
                "This program is too simple, or something went wrong, "
                "so no code sections could be mapped."
            )

        elif not getattr(
            cfg,
            "blocks",
            []
        ):

            st.warning(
                "No code sections were found for this program."
            )

        else:

            blocks = cfg.blocks


            st.html(
                """
                <div class="explainer">
                    <strong>How to read the map below:</strong>
                    each box is a <strong>section</strong> of
                    instructions that runs straight through with no
                    jumps. The arrow underneath a section shows which
                    section runs right after it - follow the arrows
                    top to bottom to see every path your program can
                    take.
                </div>
                """
            )


            cfg_html = '<div class="cfg-area">'


            for index, block in enumerate(
                blocks
            ):

                bid = block_id(
                    block
                )


                instruction_html = ""


                for instruction in (
                    getattr(
                        block,
                        "instructions",
                        []
                    )
                ):

                    instruction_html += (
                        f"""
                        <div class="cfg-line">
                            {esc(instruction)}
                        </div>
                        """
                    )


                cfg_html += (
                    f"""
                    <div class="cfg-block">

                        <div class="cfg-header">
                            Section B{esc(bid)}
                        </div>

                        {instruction_html}

                    </div>
                    """
                )


                successors = getattr(
                    block,
                    "successors",
                    []
                )


                for successor in (
                    successors
                ):

                    sid = successor_id(
                        successor
                    )


                    cfg_html += (
                        f"""
                        <div class="cfg-arrow">
                            v
                        </div>

                        <div style="
                            text-align:center;
                            color: var(--text-faint);
                            font-size:11.5px;
                            margin-bottom:12px;
                        ">
                            then runs Section B{esc(sid)}
                        </div>
                        """
                    )


            cfg_html += "</div>"


            st.html(
                cfg_html
            )


            # ------------------------------------------------
            # BLOCK INSPECTOR
            # ------------------------------------------------

            st.markdown(
                "### Look at one section closely"
            )


            names = [
                f"B{block_id(block)}"
                for block in blocks
            ]


            selected = st.selectbox(
                "Choose a section",
                names,
            )


            selected_number = (
                selected[1:]
            )


            selected_block = None


            for block in blocks:

                if str(
                    block_id(block)
                ) == selected_number:

                    selected_block = block
                    break


            if selected_block is not None:

                left, right = st.columns(2)


                with left:

                    st.markdown(
                        "#### Comes from"
                    )


                    predecessors = getattr(
                        selected_block,
                        "predecessors",
                        []
                    )


                    if predecessors:

                        for item in (
                            predecessors
                        ):

                            st.html(
                                f"""
                                <div class="info">
                                    Section B{esc(
                                        block_id(item)
                                    )}
                                </div>
                                """
                            )

                    else:

                        st.caption(
                            "Nothing - this is where the program starts."
                        )


                with right:

                    st.markdown(
                        "#### Goes to"
                    )


                    successors = getattr(
                        selected_block,
                        "successors",
                        []
                    )


                    if successors:

                        for item in (
                            successors
                        ):

                            st.html(
                                f"""
                                <div class="info">
                                    Section B{esc(
                                        successor_id(item)
                                    )}
                                </div>
                                """
                            )

                    else:

                        st.caption(
                            "Nothing - this is where the program ends."
                        )


    # ========================================================
    # LIVENESS
    # ========================================================

    with tabs[5]:

        st.html(
            """
            <div class="card">

                <div class="card-title">
                    Step 6  |  Checking which values are still needed
                </div>

                <div class="card-subtitle">
                    For each section, the compiler checks which
                    variables are read from, which are written to,
                    and - most importantly - which ones will still
                    be needed later. A variable that's written but
                    never used again is a candidate for removal.
                </div>

            </div>
            """
        )


        if liveness is None:

            st.warning(
                "This check couldn't run for this program."
            )

        elif cfg is None:

            st.warning(
                "This program has no code sections to check."
            )

        else:

            # ------------------------------------------------
            # FLOW
            # ------------------------------------------------

            st.html(
                """
                <div class="explainer">
                    <strong>How to read the table below:</strong>
                    for each section, <strong>USE</strong> is what it
                    reads, <strong>DEF</strong> is what it writes,
                    <strong>LIVE IN</strong> is what's needed the
                    moment the section starts, and
                    <strong>LIVE OUT</strong> is what's still needed
                    once it finishes.
                </div>

                <div class="flow">

                    <div class="flow-box">

                        <div class="flow-title">
                            Sections
                        </div>

                        <div class="flow-description">
                            From the map above
                        </div>

                    </div>

                    <div class="flow-arrow">
                        ->
                    </div>

                    <div class="flow-box">

                        <div class="flow-title">
                            Read &amp; write
                        </div>

                        <div class="flow-description">
                            USE / DEF
                        </div>

                    </div>

                    <div class="flow-arrow">
                        ->
                    </div>

                    <div class="flow-box">

                        <div class="flow-title">
                            Needed at start
                        </div>

                        <div class="flow-description">
                            LIVE IN
                        </div>

                    </div>

                    <div class="flow-arrow">
                        ->
                    </div>

                    <div class="flow-box">

                        <div class="flow-title">
                            Needed at end
                        </div>

                        <div class="flow-description">
                            LIVE OUT
                        </div>

                    </div>

                </div>
                """
            )


            for block in cfg.blocks:

                bid = block_id(
                    block
                )


                use_values = (
                    get_analysis_value(
                        liveness,
                        [
                            "use",
                            "USE",
                            "uses"
                        ],
                        bid
                    )
                )


                def_values = (
    get_analysis_value(
        liveness,
        [
            "definitions",
            "def",
            "DEF",
            "defs",
            "def_sets"
        ],
        bid
    )
)


                live_in_values = (
                    get_analysis_value(
                        liveness,
                        [
                            "live_in",
                            "LIVE_IN",
                            "livein"
                        ],
                        bid
                    )
                )


                live_out_values = (
                    get_analysis_value(
                        liveness,
                        [
                            "live_out",
                            "LIVE_OUT",
                            "liveout"
                        ],
                        bid
                    )
                )


                def display(values):

                    if not values:
                        return "empty"

                    return ", ".join(
                        sorted(
                            str(x)
                            for x in values
                        )
                    )


                st.html(
                    f"""
                    <div class="live-card">

                        <div class="live-title">
                            Section B{esc(bid)}
                        </div>

                        <div class="live-grid">

                            <div class="live-cell">

                                <div class="live-label">
                                    USE
                                </div>

                                <div class="live-value">
                                    {esc(
                                        display(
                                            use_values
                                        )
                                    )}
                                </div>

                            </div>


                            <div class="live-cell">

                                <div class="live-label">
                                    DEF
                                </div>

                                <div class="live-value">
                                    {esc(
                                        display(
                                            def_values
                                        )
                                    )}
                                </div>

                            </div>


                            <div class="live-cell">

                                <div class="live-label">
                                    LIVE IN
                                </div>

                                <div class="live-value">
                                    {esc(
                                        display(
                                            live_in_values
                                        )
                                    )}
                                </div>

                            </div>


                            <div class="live-cell">

                                <div class="live-label">
                                    LIVE OUT
                                </div>

                                <div class="live-value">
                                    {esc(
                                        display(
                                            live_out_values
                                        )
                                    )}
                                </div>

                            </div>

                        </div>

                    </div>
                    """
                )


    # ========================================================
    # DCE
    # ========================================================

    with tabs[6]:

        st.html(
            """
            <div class="card">

                <div class="card-title">
                    Step 7  |  Deleting what's never used
                </div>

                <div class="card-subtitle">
                    Using what it learned in the last step, the
                    compiler deletes any instruction whose result is
                    never needed - a calculation nobody reads is just
                    wasted work. This last cleanup pass is called
                    Dead Code Elimination, or DCE.
                </div>

            </div>
            """
        )


        # ----------------------------------------------------
        # DCE FLOW
        # ----------------------------------------------------

        st.html(
            """
            <div class="flow">

                <div class="flow-box">

                    <div class="flow-title">
                        Sections
                    </div>

                    <div class="flow-description">
                        The code map
                    </div>

                </div>

                <div class="flow-arrow">
                    ->
                </div>

                <div class="flow-box">

                    <div class="flow-title">
                        Usage check
                    </div>

                    <div class="flow-description">
                        What's still needed
                    </div>

                </div>

                <div class="flow-arrow">
                    ->
                </div>

                <div class="flow-box">

                    <div class="flow-title">
                        Delete unused
                    </div>

                    <div class="flow-description">
                        Drop dead instructions
                    </div>

                </div>

                <div class="flow-arrow">
                    ->
                </div>

                <div class="flow-box">

                    <div class="flow-title">
                        Final program
                    </div>

                    <div class="flow-description">
                        Clean and ready
                    </div>

                </div>

            </div>
            """
        )


        original = len(
            tac
        )

        final = len(
            optimized_tac
        )


        reduction = (
            (
                original - final
            )
            / original
            * 100
        ) if original else 0


        d1, d2, d3 = st.columns(3)


        with d1:

            st.html(
                f"""
                <div class="metric">

                    <div class="metric-value">
                        {original}
                    </div>

                    <div class="metric-label">
                        Steps before cleanup
                    </div>

                </div>
                """
            )


        with d2:

            st.html(
                f"""
                <div class="metric">

                    <div class="metric-value">
                        {dce_removed}
                    </div>

                    <div class="metric-label">
                        Steps removed
                    </div>

                </div>
                """
            )


        with d3:

            st.html(
                f"""
                <div class="metric">

                    <div class="metric-value">
                        {reduction:.1f}%
                    </div>

                    <div class="metric-label">
                        Smaller by
                    </div>

                </div>
                """
            )


        # ----------------------------------------------------
        # BEFORE
        # ----------------------------------------------------

        st.markdown(
            "### Before this step"
        )


        st.code(
            "\n".join(
                str(x)
                for x in tac
            ),
            language="text",
        )


        # ----------------------------------------------------
        # RESULT
        # ----------------------------------------------------

        if dce_removed == 0:

            st.html(
                """
                <div class="keep">

                    OK Nothing to remove - every instruction was
                    already needed.

                </div>
                """
            )

        else:

            st.html(
                f"""
                <div class="removed">

                    Removed
                    <strong>
                        {dce_removed}
                    </strong>
                    instruction(s) whose result was never used.

                </div>
                """
            )


        # ----------------------------------------------------
        # FINAL
        # ----------------------------------------------------

        st.markdown(
            "### The final program"
        )


        for instruction in (
            optimized_tac
        ):

            st.html(
                f"""
                <div class="keep">

                    OK {esc(instruction)}

                </div>
                """
            )


        # ----------------------------------------------------
        # EXPLANATION
        # ----------------------------------------------------

        st.markdown(
            "### How this step works"
        )


        st.html(
            """
            <div class="info">

                <strong>1. Map the sections</strong><br>
                The program is divided into sections that each run
                straight through with no jumps.

            </div>

            <div class="info">

                <strong>2. Check what's needed</strong><br>
                The compiler figures out which variables are actually
                read later on.

            </div>

            <div class="info">

                <strong>3. Remove the unused</strong><br>
                Any instruction whose result is never read gets
                deleted - it was wasted work.

            </div>

            <div class="info">

                <strong>4. Done</strong><br>
                What's left is a smaller, equivalent program that
                does exactly the same thing, faster.

            </div>
            """
        )


    # ========================================================
    # INSIGHTS
    # ========================================================

    with tabs[7]:

        st.html(
            """
            <div class="card">
                <div class="card-title">
                     Code Insights
                </div>
                <div class="card-subtitle">
                    A compact view of your program's structural complexity
                    and the amount of work removed by optimization.
                </div>
            </div>
            """
        )

        # ----------------------------------------------------
        # COMPLEXITY ANALYZER
        # ----------------------------------------------------

        st.markdown("### Code Complexity Analyzer")

        q1, q2, q3, q4 = st.columns(4)

        with q1:
            st.html(
                f"""
                <div class="metric">
                    <div class="metric-value">{ast_nodes}</div>
                    <div class="metric-label">AST nodes</div>
                </div>
                """
            )

        with q2:
            st.html(
                f"""
                <div class="metric">
                    <div class="metric-value">{branch_count}</div>
                    <div class="metric-label">Branches</div>
                </div>
                """
            )

        with q3:
            st.html(
                f"""
                <div class="metric">
                    <div class="metric-value">{loop_count}</div>
                    <div class="metric-label">Loops</div>
                </div>
                """
            )

        with q4:
            st.html(
                f"""
                <div class="metric">
                    <div class="complexity-score">{cyclomatic}</div>
                    <div class="complexity-label">
                        Cyclomatic complexity  |  {esc(complexity)}
                    </div>
                </div>
                """
            )

        st.html(
            f"""
            <div class="insight-card">
                <div class="insight-heading">
                    What does this score mean?
                </div>
                <div class="insight-muted">
                    Cyclomatic complexity starts at 1 and increases for each
                    decision point such as an <strong>if</strong> or
                    <strong>while</strong>. Your program has
                    <strong>{branch_count}</strong> decision point(s), giving
                    a score of <strong>{cyclomatic}</strong>.
                    This project classifies that as
                    <strong>{esc(complexity)}</strong> complexity.
                </div>
            </div>
            """
        )

        # ----------------------------------------------------
        # OPTIMIZATION SAVINGS
        # ----------------------------------------------------

        st.markdown("### Optimization Savings")

        before = len(tac)
        after = len(optimized_tac)
        removed = max(before - after, 0)
        savings = (removed / before * 100) if before else 0
        after_width = (after / before * 100) if before else 0

        st.html(
            f"""
            <div class="insight-card">

                <div class="insight-heading">
                    Instruction count
                </div>

                <div class="insight-muted">
                    Visual comparison of the TAC before and after the
                    compiler's cleanup passes.
                </div>

                <div class="savings-row">
                    <div class="savings-label">
                        <span>BEFORE OPTIMIZATION</span>
                        <strong>{before}</strong>
                    </div>
                    <div class="savings-track">
                        <div class="savings-fill-before"></div>
                    </div>
                </div>

                <div class="savings-row">
                    <div class="savings-label">
                        <span>AFTER OPTIMIZATION</span>
                        <strong>{after}</strong>
                    </div>
                    <div class="savings-track">
                        <div class="savings-fill-after"
                             style="width:{after_width:.1f}%;">
                        </div>
                    </div>
                </div>

                <div class="savings-callout">
                    <strong>{removed}</strong> instruction(s) removed -
                    <strong>{savings:.1f}%</strong> reduction in the
                    instruction count.
                </div>

            </div>
            """
        )

        # ----------------------------------------------------
        # QUICK HEALTH SUMMARY
        # ----------------------------------------------------

        st.markdown("### Program Snapshot")

        s1, s2 = st.columns(2)

        with s1:
            st.html(
                f"""
                <div class="info">
                    <strong>Source lines:</strong>
                    {len(source.splitlines())}
                    &nbsp;  |  &nbsp;
                    <strong>Tokens:</strong>
                    {len(tokens)}
                </div>

                <div class="info">
                    <strong>TAC instructions:</strong>
                    {before}
                    &nbsp; -> &nbsp;
                    <strong>Final:</strong>
                    {after}
                </div>
                """
            )

        with s2:
            st.html(
                f"""
                <div class="info">
                    <strong>CFG blocks:</strong>
                    {len(getattr(cfg, "blocks", [])) if cfg is not None else 0}
                    &nbsp;  |  &nbsp;
                    <strong>Branches:</strong>
                    {branch_count}
                </div>

                <div class="info">
                    <strong>Loops:</strong>
                    {loop_count}
                    &nbsp;  |  &nbsp;
                    <strong>DCE removals:</strong>
                    {dce_removed}
                </div>
                """
            )


# ============================================================
# READY STATE
# ============================================================

else:

    st.html(
        """
        <div class="card"
             style="text-align:center;padding:55px 20px;">

            <div style="
                color: var(--accent);
                font-size:32px;
            ">
                
            </div>

            <div class="card-title"
                 style="margin-top:10px;">

                Ready when you are

            </div>

            <div class="card-subtitle">

                Type a program above and press Compile Program to see
                every step, explained in plain language.

            </div>

        </div>
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div class="footer">

        MiniTAC Compiler  |  A compiler design project  | 

        <span class="green">
            Words -> Structure -> Instructions -> Cleanup ->
            Sections -> Usage -> Trim
        </span>

    </div>
    """
)