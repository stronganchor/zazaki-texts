#!/usr/bin/env python3
"""Build a static review UI for Lerch glossary headwords and glosses."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import fitz


REPO_ROOT = Path(__file__).resolve().parents[1]
LERCH_DIR = Path(r"C:\Users\messy\OneDrive\Documents\Language\Z\Dictionaries\Lerch")
PDF_PATH = LERCH_DIR / "lerch glossary german.pdf"
CORRECTED_TSV = REPO_ROOT / "reports" / "lerch-glossary-corrected-layer.tsv"
REVIEW_DIR = REPO_ROOT / "reviews" / "lerch-glossary-headword-review"
ASSET_DIR = REVIEW_DIR / "assets"
DATA_JS = REVIEW_DIR / "glossary-data.js"
INDEX_HTML = REVIEW_DIR / "index.html"


def read_tsv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def render_page_assets(rows: list[dict[str, str]]) -> dict[str, str]:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    pages = sorted({int(row["source_page"]) for row in rows if row.get("source_page", "").isdigit()})
    page_assets: dict[str, str] = {}
    with fitz.open(PDF_PATH) as doc:
        for page_no in pages:
            out = ASSET_DIR / f"german_glossary_p{page_no}.webp"
            if not out.exists():
                page = doc[page_no - 1]
                pix = page.get_pixmap(matrix=fitz.Matrix(2.0, 2.0), alpha=False)
                try:
                    pix.pil_save(str(out), format="WEBP", optimize=True, quality=82)
                except Exception:
                    out = ASSET_DIR / f"german_glossary_p{page_no}.png"
                    if not out.exists():
                        pix.save(str(out))
            page_assets[str(page_no)] = f"assets/{out.name}"
    return page_assets


def write_data(rows: list[dict[str, str]], page_assets: dict[str, str]) -> None:
    payload = {
        "source_pdf": str(PDF_PATH),
        "rows": rows,
        "page_assets": page_assets,
    }
    DATA_JS.write_text(
        "window.LERCH_GLOSSARY_REVIEW_DATA = "
        + json.dumps(payload, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )


def write_html() -> None:
    INDEX_HTML.write_text(
        r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Lerch Glossary Headword Review</title>
  <script src="glossary-data.js"></script>
  <style>
    :root {
      color-scheme: light;
      --bg: #f7f2ea;
      --panel: #fffaf2;
      --ink: #16120e;
      --muted: #6e6255;
      --line: #dacbbb;
      --accent: #0f766e;
      --warn: #8a4b0f;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--ink);
      padding-bottom: 92px;
    }
    header {
      position: sticky;
      top: 0;
      z-index: 20;
      background: rgba(247, 242, 234, .96);
      border-bottom: 1px solid var(--line);
      padding: 14px 18px;
      backdrop-filter: blur(10px);
    }
    h1 {
      margin: 0 0 10px;
      font-size: 22px;
      line-height: 1.2;
    }
    .controls {
      display: grid;
      grid-template-columns: minmax(220px, 1fr) 140px 170px 140px 130px;
      gap: 10px;
      align-items: end;
    }
    label {
      display: grid;
      gap: 4px;
      font-size: 12px;
      color: var(--muted);
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: .03em;
    }
    input, textarea, select, button {
      font: inherit;
      border: 1px solid var(--line);
      background: #fffdf8;
      color: var(--ink);
      border-radius: 7px;
    }
    input, select {
      min-height: 38px;
      padding: 8px 10px;
    }
    textarea {
      width: 100%;
      min-height: 58px;
      resize: vertical;
      padding: 8px 10px;
      line-height: 1.35;
    }
    button {
      min-height: 38px;
      padding: 8px 12px;
      cursor: pointer;
      font-weight: 700;
    }
    button.primary {
      background: var(--accent);
      border-color: var(--accent);
      color: white;
    }
    .layout {
      display: grid;
      grid-template-columns: minmax(360px, 43vw) 1fr;
      gap: 16px;
      padding: 16px;
    }
    .page-pane {
      position: sticky;
      top: 104px;
      align-self: start;
      max-height: calc(100vh - 198px);
      overflow: auto;
      border: 1px solid var(--line);
      background: #efe5d4;
      border-radius: 8px;
      padding: 10px;
    }
    .page-meta {
      display: flex;
      justify-content: space-between;
      gap: 12px;
      color: var(--muted);
      font-size: 13px;
      margin-bottom: 8px;
    }
    #pageImage {
      display: block;
      width: 100%;
      min-width: 700px;
      height: auto;
      background: #e5dbc9;
      border: 1px solid #cdbba6;
    }
    .rows {
      display: grid;
      gap: 12px;
    }
    .row-card {
      border: 1px solid var(--line);
      background: var(--panel);
      border-radius: 8px;
      overflow: hidden;
    }
    .row-card.is-active {
      border-color: var(--accent);
      box-shadow: 0 0 0 2px rgba(15, 118, 110, .18);
    }
    .row-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      padding: 10px 12px;
      border-bottom: 1px solid var(--line);
      background: #fff7e9;
    }
    .row-title {
      font-weight: 800;
    }
    .row-meta {
      color: var(--muted);
      font-size: 13px;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      border: 1px solid #b8a891;
      border-radius: 999px;
      padding: 3px 8px;
      font-size: 12px;
      color: #513f2f;
      background: #f8ead6;
      white-space: nowrap;
    }
    .body-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
      padding: 12px;
    }
    .full { grid-column: 1 / -1; }
    .readonly {
      min-height: 38px;
      padding: 8px 10px;
      border: 1px dashed var(--line);
      border-radius: 7px;
      background: #f6efe3;
      line-height: 1.35;
      white-space: pre-wrap;
    }
    .source-text {
      font-family: "Times New Roman", serif;
      font-size: 18px;
    }
    .muted {
      color: var(--muted);
      font-size: 13px;
      line-height: 1.35;
    }
    .keyboard {
      position: fixed;
      left: 0;
      right: 0;
      bottom: 0;
      z-index: 30;
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      padding: 10px 14px;
      background: rgba(33, 28, 24, .96);
      border-top: 1px solid #5f5147;
    }
    .keyboard button {
      min-height: 34px;
      min-width: 36px;
      padding: 4px 8px;
      border-color: #736258;
      background: #fffaf2;
      border-radius: 5px;
    }
    .keyboard .mark {
      background: #e3f3f1;
    }
    .status-line {
      color: var(--muted);
      font-size: 13px;
      margin-top: 8px;
    }
    @media (max-width: 1000px) {
      .controls { grid-template-columns: 1fr 1fr; }
      .layout { grid-template-columns: 1fr; }
      .page-pane { position: relative; top: auto; max-height: 55vh; }
      .body-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <header>
    <h1>Lerch Glossary Headword Review</h1>
    <div class="controls">
      <label>Search <input id="search" type="search" placeholder="headword, gloss, page, notes"></label>
      <label>Page <select id="pageFilter"></select></label>
      <label>Status <select id="statusFilter"></select></label>
      <label>Confidence <select id="confidenceFilter"></select></label>
      <button class="primary" id="exportBtn" type="button">Export JSON</button>
    </div>
    <div class="status-line" id="statusLine"></div>
  </header>

  <main class="layout">
    <aside class="page-pane">
      <div class="page-meta">
        <strong id="pageTitle">German source page</strong>
        <span id="sourcePdf"></span>
      </div>
      <img id="pageImage" alt="German glossary source page">
    </aside>
    <section class="rows" id="rows"></section>
  </main>

  <div class="keyboard" id="keyboard" aria-label="Lerch special-character keyboard"></div>

  <script>
    const data = window.LERCH_GLOSSARY_REVIEW_DATA;
    const storageKey = "lerch-glossary-headword-review:v1";
    const rowsEl = document.getElementById("rows");
    const pageImage = document.getElementById("pageImage");
    const pageTitle = document.getElementById("pageTitle");
    const statusLine = document.getElementById("statusLine");
    const sourcePdf = document.getElementById("sourcePdf");
    const filters = {
      search: document.getElementById("search"),
      page: document.getElementById("pageFilter"),
      status: document.getElementById("statusFilter"),
      confidence: document.getElementById("confidenceFilter"),
    };
    let activeInput = null;
    let activePage = "";
    let saved = {};

    try {
      saved = JSON.parse(localStorage.getItem(storageKey) || "{}");
    } catch (_error) {
      saved = {};
    }

    sourcePdf.textContent = data.source_pdf;

    function unique(values) {
      return Array.from(new Set(values.filter(Boolean))).sort((a, b) => String(a).localeCompare(String(b), undefined, {numeric: true}));
    }

    function optionList(select, label, values) {
      select.innerHTML = "";
      select.append(new Option(label, ""));
      values.forEach(value => select.append(new Option(value, value)));
    }

    optionList(filters.page, "All pages", unique(data.rows.map(row => row.source_page)));
    optionList(filters.status, "All statuses", unique(data.rows.map(row => row.entry_review_status || "(blank)")));
    optionList(filters.confidence, "All", unique(data.rows.map(row => row.correction_confidence)));

    function rowValue(row, field) {
      return saved[row.row_id]?.[field] ?? row[field] ?? "";
    }

    function setRowValue(rowId, field, value) {
      if (!saved[rowId]) saved[rowId] = {};
      saved[rowId][field] = value;
      localStorage.setItem(storageKey, JSON.stringify(saved));
      statusLine.textContent = `Saved locally ${new Date().toLocaleTimeString()}`;
    }

    function setPage(page) {
      if (!page || page === activePage) return;
      activePage = page;
      pageTitle.textContent = `German glossary source page ${page}`;
      pageImage.src = data.page_assets[page] || "";
      pageImage.alt = `German glossary source page ${page}`;
    }

    function field(label, content, className = "") {
      const wrap = document.createElement("label");
      if (className) wrap.className = className;
      wrap.append(label);
      wrap.append(content);
      return wrap;
    }

    function inputField(row, key, labelText) {
      const input = document.createElement("input");
      input.value = rowValue(row, key);
      input.spellcheck = false;
      input.dataset.row = row.row_id;
      input.dataset.field = key;
      input.addEventListener("focus", () => {
        activeInput = input;
        setPage(row.source_page);
      });
      input.addEventListener("input", () => setRowValue(row.row_id, key, input.value));
      return field(labelText, input);
    }

    function textareaField(row, key, labelText, full = false) {
      const textarea = document.createElement("textarea");
      textarea.value = rowValue(row, key);
      textarea.spellcheck = false;
      textarea.dataset.row = row.row_id;
      textarea.dataset.field = key;
      textarea.addEventListener("focus", () => {
        activeInput = textarea;
        setPage(row.source_page);
      });
      textarea.addEventListener("input", () => {
        textarea.style.height = "auto";
        textarea.style.height = `${textarea.scrollHeight + 2}px`;
        setRowValue(row.row_id, key, textarea.value);
      });
      setTimeout(() => {
        textarea.style.height = "auto";
        textarea.style.height = `${textarea.scrollHeight + 2}px`;
      }, 0);
      return field(labelText, textarea, full ? "full" : "");
    }

    function readonly(labelText, value, extraClass = "") {
      const div = document.createElement("div");
      div.className = `readonly ${extraClass}`;
      div.textContent = value || "";
      return field(labelText, div);
    }

    function selectField(row) {
      const select = document.createElement("select");
      ["needs_review", "headword_checked", "gloss_checked", "ready", "skip_name_place", "uncertain"].forEach(value => {
        select.append(new Option(value, value));
      });
      select.value = rowValue(row, "review_status") || "needs_review";
      select.addEventListener("focus", () => setPage(row.source_page));
      select.addEventListener("change", () => setRowValue(row.row_id, "review_status", select.value));
      return field("Review status", select);
    }

    function renderRow(row) {
      const card = document.createElement("article");
      card.className = "row-card";
      card.dataset.page = row.source_page;
      card.tabIndex = 0;
      card.addEventListener("focusin", () => {
        document.querySelectorAll(".row-card.is-active").forEach(item => item.classList.remove("is-active"));
        card.classList.add("is-active");
        setPage(row.source_page);
      });

      const head = document.createElement("div");
      head.className = "row-head";
      const title = document.createElement("div");
      title.innerHTML = `<div class="row-title">Row ${row.row_id}: ${escapeHtml(row.raw_lerch_headword || "")}</div><div class="row-meta">page ${row.source_page}; ${row.corrected_headword_source}; ${row.entry_review_status || "no status"}</div>`;
      const badge = document.createElement("span");
      badge.className = "badge";
      badge.textContent = row.correction_confidence;
      head.append(title, badge);

      const body = document.createElement("div");
      body.className = "body-grid";
      body.append(
        readonly("Raw OCR headword", row.raw_lerch_headword, "source-text"),
        inputField(row, "corrected_lerch_headword", "Corrected Lerch headword"),
        inputField(row, "modern_zazaki_guess", "Modern Zazaki guess"),
        inputField(row, "proposed_group_headword", "Group under headword"),
        textareaField(row, "german_gloss_clean", "German gloss", true),
        textareaField(row, "english_gloss", "English gloss"),
        textareaField(row, "turkish_gloss", "Turkish gloss"),
        selectField(row),
        textareaField(row, "reviewer_notes", "Reviewer notes", true),
        readonly("Raw German extraction", row.german_gloss_raw, "full"),
        readonly("Generated notes", row.notes || "", "full muted")
      );

      card.append(head, body);
      return card;
    }

    function escapeHtml(value) {
      return String(value).replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        "\"": "&quot;",
        "'": "&#039;"
      }[char]));
    }

    function matches(row) {
      const term = filters.search.value.trim().toLocaleLowerCase();
      if (filters.page.value && row.source_page !== filters.page.value) return false;
      if (filters.status.value) {
        const status = row.entry_review_status || "(blank)";
        if (status !== filters.status.value) return false;
      }
      if (filters.confidence.value && row.correction_confidence !== filters.confidence.value) return false;
      if (!term) return true;
      const blob = [
        row.row_id,
        row.source_page,
        row.raw_lerch_headword,
        row.corrected_lerch_headword,
        row.modern_zazaki_guess,
        row.proposed_group_headword,
        row.german_gloss_clean,
        row.english_gloss,
        row.turkish_gloss,
        row.notes,
      ].join(" ").toLocaleLowerCase();
      return blob.includes(term);
    }

    function renderRows() {
      rowsEl.innerHTML = "";
      const visible = data.rows.filter(matches);
      visible.forEach(row => rowsEl.append(renderRow(row)));
      statusLine.textContent = `${visible.length} of ${data.rows.length} rows shown. Edits save in this browser automatically. Use Export JSON for a durable handoff.`;
      if (visible[0]) setPage(visible[0].source_page);
    }

    Object.values(filters).forEach(filter => filter.addEventListener("input", renderRows));
    Object.values(filters).forEach(filter => filter.addEventListener("change", renderRows));

    document.getElementById("exportBtn").addEventListener("click", () => {
      const merged = data.rows.map(row => ({...row, ...(saved[row.row_id] || {})}));
      const blob = new Blob([JSON.stringify({exported_at: new Date().toISOString(), rows: merged}, null, 2)], {type: "application/json"});
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "lerch-glossary-headword-review-autosave.json";
      link.click();
      URL.revokeObjectURL(link.href);
    });

    const keys = [
      "ā","ē","ī","ō","ū","ă","ĕ","ĭ","ŏ","ŭ","e̱","ẹ","i̥","ṳ","o̤","ọ","ḱ","ǵ","ń","ṅ","š","ž","t̮","d̮","h̔","ʿ","ʼ","γ","Γ","χ","Χ",
      {label:"acute", value:"\u0301", mark:true},
      {label:"macron", value:"\u0304", mark:true},
      {label:"line below", value:"\u0331", mark:true},
      {label:"dot below", value:"\u0323", mark:true},
      {label:"ring below", value:"\u0325", mark:true},
      {label:"diaeresis below", value:"\u0324", mark:true},
      {label:"crescent below", value:"\u032E", mark:true},
      {label:"h mark", value:"\u0314", mark:true}
    ];
    const keyboard = document.getElementById("keyboard");
    keys.forEach(item => {
      const spec = typeof item === "string" ? {label: item, value: item} : item;
      const btn = document.createElement("button");
      btn.type = "button";
      btn.textContent = spec.label;
      if (spec.mark) btn.className = "mark";
      btn.addEventListener("click", () => {
        if (!activeInput) return;
        const start = activeInput.selectionStart ?? activeInput.value.length;
        const end = activeInput.selectionEnd ?? activeInput.value.length;
        activeInput.value = activeInput.value.slice(0, start) + spec.value + activeInput.value.slice(end);
        const pos = start + spec.value.length;
        activeInput.setSelectionRange(pos, pos);
        activeInput.dispatchEvent(new Event("input", {bubbles: true}));
        activeInput.focus();
      });
      keyboard.append(btn);
    });

    renderRows();
  </script>
</body>
</html>
''',
        encoding="utf-8",
    )


def main() -> None:
    rows = read_tsv(CORRECTED_TSV)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    page_assets = render_page_assets(rows)
    write_data(rows, page_assets)
    write_html()
    print(f"Wrote {INDEX_HTML}")
    print(f"Wrote {DATA_JS}")
    print(f"Rendered {len(page_assets)} source page images")


if __name__ == "__main__":
    main()
