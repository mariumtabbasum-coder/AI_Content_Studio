const form = document.getElementById("generator-form");
const generateButton = document.getElementById("generate-btn");
const emptyState = document.getElementById("empty-state");
const loadingState = document.getElementById("loading-state");
const errorState = document.getElementById("error-state");
const resultState = document.getElementById("result-state");
const topicInput = document.getElementById("topic");
let lastPayload = null;

function showState(state) {
  [emptyState, loadingState, errorState, resultState].forEach(el => el.classList.add("hidden"));
  state.classList.remove("hidden");
}
function setLoading(isLoading) {
  generateButton.disabled = isLoading;
  generateButton.querySelector(".btn-text").textContent = isLoading ? "Creating your content..." : "Generate content ↗";
  generateButton.querySelector(".loader").style.display = isLoading ? "block" : "none";
}
function selectedContentType() {
  return document.querySelector('input[name="content_type"]:checked').value;
}
function getPayload() {
  return {
    topic: topicInput.value.trim(),
    content_type: selectedContentType(),
    tone: document.getElementById("tone").value,
    length: document.getElementById("length").value,
    audience: document.getElementById("audience").value.trim(),
    language: document.getElementById("language").value,
    keywords: document.getElementById("keywords").value.trim()
  };
}
function showError(message) {
  document.getElementById("error-message").textContent = message;
  showState(errorState);
}
function renderResult(data) {
  const result = data.result;
  document.getElementById("result-title").textContent = result.title || "Your generated content";
  document.getElementById("generated-content").textContent = result.content || "";
  document.getElementById("result-type").textContent = data.meta.content_type;
  const hashtags = document.getElementById("hashtags");
  hashtags.innerHTML = "";
  (result.hashtags || []).forEach(tag => {
    const chip = document.createElement("span");
    chip.className = "hashtag";
    chip.textContent = tag.startsWith("#") ? tag : `#${tag}`;
    hashtags.appendChild(chip);
  });
  if (!hashtags.children.length) {
    const empty = document.createElement("span");
    empty.className = "muted";
    empty.textContent = "No hashtags suggested for this format.";
    hashtags.appendChild(empty);
  }
  const tipsList = document.getElementById("tips-list");
  tipsList.innerHTML = "";
  (result.tips || []).forEach(tip => {
    const li = document.createElement("li");
    li.textContent = tip;
    tipsList.appendChild(li);
  });
  document.getElementById("meta-line").textContent = `Generated with ${data.meta.model} · ${data.meta.tone}`;
  showState(resultState);
}
async function generate(payload = getPayload()) {
  lastPayload = payload;
  setLoading(true);
  showState(loadingState);
  try {
    const controller = new AbortController();

const timeoutId = setTimeout(() => {
  controller.abort();
}, 70000);

let response;

try {
  response = await fetch("/api/generate", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(payload),
    signal: controller.signal
  });
} catch (error) {
  if (error.name === "AbortError") {
    throw new Error("Request timed out. Please check your Gemini API and try again.");
  }
  throw error;
} finally {
  clearTimeout(timeoutId);
}
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Request failed. Please try again.");
    renderResult(data);
  } catch (error) {
    showError(error.message || "Unable to connect. Please try again.");
  } finally {
    setLoading(false);
  }
}
form.addEventListener("submit", event => {
  event.preventDefault();
  generate();
});
document.querySelectorAll('input[name="content_type"]').forEach(input => {
  input.addEventListener("change", () => {
    document.querySelectorAll(".format-option").forEach(option => option.classList.remove("selected"));
    input.closest(".format-option").classList.add("selected");
  });
});
topicInput.addEventListener("input", () => {
  document.getElementById("char-count").textContent = `${topicInput.value.length} / 500`;
});
document.getElementById("try-again").addEventListener("click", () => generate(lastPayload || getPayload()));
document.getElementById("generate-again").addEventListener("click", () => generate(lastPayload || getPayload()));

function copyText(text, button, original) {
  navigator.clipboard.writeText(text).then(() => {
    button.textContent = "Copied!";
    setTimeout(() => button.textContent = original, 1400);
  }).catch(() => {
    button.textContent = "Copy unavailable";
    setTimeout(() => button.textContent = original, 1400);
  });
}
document.getElementById("copy-hashtags").addEventListener("click", event => {
  const tags = [...document.querySelectorAll("#hashtags .hashtag")].map(el => el.textContent).join(" ");
  copyText(tags, event.currentTarget, "Copy hashtags");
});
document.getElementById("copy-all").addEventListener("click", event => {
  const title = document.getElementById("result-title").textContent;
  const content = document.getElementById("generated-content").textContent;
  const tags = [...document.querySelectorAll("#hashtags .hashtag")].map(el => el.textContent).join(" ");
  copyText(`${title}\n\n${content}\n\n${tags}`, event.currentTarget, "Copy all content");
});
