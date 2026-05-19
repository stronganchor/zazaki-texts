(function () {
  "use strict";

  const STORAGE_KEY = "lerch-context-review:v1";
  const FIELDS = [
    ["turkishDisplayTitle", "Turkish display title", "input"],
    ["shortTurkishSummary", "Short Turkish summary/excerpt", "textarea"],
    ["contentWarnings", "Content warnings", "textarea"],
    ["peopleMentioned", "Historical people mentioned", "textarea"],
    ["placesMentioned", "Historical places mentioned", "textarea"],
    ["historicalContextNotes", "Historical/context notes", "textarea"],
    ["publicationReviewNotes", "Publication-status/review notes", "textarea"]
  ];

  const seed = window.LERCH_CONTEXT_SEED;
  const cardsEl = document.getElementById("cards");
  const template = document.getElementById("card-template");
  const saveState = document.getElementById("save-state");
  const exportButton = document.getElementById("export-json");
  const resetButton = document.getElementById("reset-seed");

  let reviewData = loadData();
  let saveTimer = null;

  function clone(value) {
    return JSON.parse(JSON.stringify(value));
  }

  function loadData() {
    const raw = window.localStorage.getItem(STORAGE_KEY);
    if (!raw) {
      return clone(seed);
    }

    try {
      const saved = JSON.parse(raw);
      return mergeWithSeed(saved);
    } catch (error) {
      console.warn("Could not parse saved Lerch context review data", error);
      return clone(seed);
    }
  }

  function mergeWithSeed(saved) {
    const next = clone(seed);
    const savedById = new Map((saved.texts || []).map((item) => [item.id, item]));
    next.texts = next.texts.map((text) => {
      const savedText = savedById.get(text.id);
      if (!savedText) {
        return text;
      }

      return {
        ...text,
        fields: {
          ...text.fields,
          ...(savedText.fields || {})
        }
      };
    });
    next.lastSavedAt = saved.lastSavedAt || null;
    return next;
  }

  function render() {
    cardsEl.innerHTML = "";
    reviewData.texts.forEach((text) => {
      const card = template.content.firstElementChild.cloneNode(true);
      card.dataset.id = text.id;
      card.querySelector(".source-title").textContent = `${text.folder} | ${text.sourceTitle}`;
      card.querySelector("h2").textContent = text.workingTitle;
      card.querySelector(".status-pill").textContent = text.status;

      const facts = card.querySelector(".facts");
      addFact(facts, "Lines", text.lineCount);
      addFact(facts, "Tokens", text.tokenCount);
      addFact(facts, "Source root", `${seed.sourceRoot}/${text.folder}`);

      const fields = card.querySelector(".fields");
      const hiddenFields = new Set(text.hiddenFields || []);
      FIELDS.forEach(([fieldName, labelText, elementType]) => {
        if (hiddenFields.has(fieldName)) {
          return;
        }
        const label = document.createElement("label");
        const control = document.createElement(elementType);
        label.textContent = labelText;
        control.value = text.fields[fieldName] || "";
        control.dataset.id = text.id;
        control.dataset.field = fieldName;
        control.addEventListener("input", handleInput);
        label.appendChild(control);
        fields.appendChild(label);
      });

      cardsEl.appendChild(card);
    });

    expandAllTextareas();
    window.requestAnimationFrame(expandAllTextareas);
    setSaveState(reviewData.lastSavedAt ? `Loaded autosave from ${reviewData.lastSavedAt}` : "Loaded seed data");
  }

  function addFact(parent, term, value) {
    const dt = document.createElement("dt");
    const dd = document.createElement("dd");
    dt.textContent = term;
    dd.textContent = String(value);
    parent.append(dt, dd);
  }

  function handleInput(event) {
    const id = event.target.dataset.id;
    const field = event.target.dataset.field;
    const text = reviewData.texts.find((item) => item.id === id);
    if (!text) {
      return;
    }

    text.fields[field] = event.target.value;
    if (event.target.tagName === "TEXTAREA") {
      autoExpand(event.target);
    }
    setSaveState("Saving...");
    window.clearTimeout(saveTimer);
    saveTimer = window.setTimeout(save, 250);
  }

  function autoExpand(textarea) {
    textarea.style.height = "auto";
    textarea.style.height = `${textarea.scrollHeight + 8}px`;
  }

  function expandAllTextareas() {
    cardsEl.querySelectorAll("textarea").forEach(autoExpand);
  }

  function save() {
    reviewData.lastSavedAt = new Date().toISOString();
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(reviewData));
    setSaveState(`Saved ${reviewData.lastSavedAt}`);
  }

  function setSaveState(message) {
    saveState.textContent = message;
  }

  function exportJson() {
    save();
    const payload = {
      ...reviewData,
      exportedAt: new Date().toISOString()
    };
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "lerch-context-review-export.json";
    document.body.appendChild(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(url);
  }

  function resetToSeed() {
    const confirmed = window.confirm("Reset all local edits for this review page back to the seeded values?");
    if (!confirmed) {
      return;
    }

    window.localStorage.removeItem(STORAGE_KEY);
    reviewData = clone(seed);
    render();
  }

  exportButton.addEventListener("click", exportJson);
  resetButton.addEventListener("click", resetToSeed);
  render();
})();
