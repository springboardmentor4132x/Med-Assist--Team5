// Change this to wherever Member 5 hosts the FastAPI backend.
const API_BASE_URL = "http://localhost:8000";
const ENDPOINT = `${API_BASE_URL}/api/risk/categorization`;

const $ = (id) => document.getElementById(id);
const splitList = (s) => s.split(",").map((x) => x.trim()).filter(Boolean);

function showError(msg) {
  $("error").textContent = msg;
  $("error").hidden = false;
  $("result").hidden = true;
}

// FastAPI 422 returns {detail: [{loc:[...], msg:"..."}]}
function formatApiError(body) {
  if (body && Array.isArray(body.detail)) {
    return body.detail.map((d) => `${(d.loc || []).slice(1).join(".") || "input"}: ${d.msg}`).join("; ");
  }
  return (body && body.detail) || "The request could not be processed.";
}

function render(r) {
  $("error").hidden = true;
  $("out-score").textContent = `${r.risk_score}/100`;
  const badge = $("out-category");
  badge.textContent = r.category_label.toUpperCase();
  badge.className = `badge ${r.category_color}`; // label text + colour (not colour alone)
  $("out-severity").textContent = r.severity_level || "Not provided / not recognized";
  $("out-emergency").textContent = r.emergency_flag ? "TRIGGERED" : "Not Triggered";

  const banner = $("emergency-banner");
  banner.hidden = !r.emergency_alert;
  banner.textContent = r.emergency_alert || "";

  $("out-explanation").textContent = r.explanation;
  $("out-guidance").textContent = r.urgency_guidance;
  const ul = $("out-factors");
  ul.replaceChildren(...r.contributing_factors.map((f) => {
    const li = document.createElement("li");
    li.textContent = f; // textContent, never innerHTML
    return li;
  }));
  $("out-disclaimer").textContent = r.disclaimer;
  $("result").hidden = false;
}

$("risk-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const raw = $("risk_score").value.trim();
  if (raw === "" || Number.isNaN(Number(raw))) return showError("Enter a risk score between 0 and 100.");

  const payload = {
    risk_score: Number(raw),
    severity_level: $("severity_level").value || null,
    emergency_flag: $("emergency_flag").checked, // real boolean
    symptoms: splitList($("symptoms").value),
    risk_factors: splitList($("risk_factors").value),
  };

  const btn = e.target.querySelector("button");
  btn.disabled = true;
  try {
    const res = await fetch(ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const body = await res.json().catch(() => null);
    if (!res.ok) return showError(formatApiError(body));
    render(body);
  } catch {
    showError(`Cannot reach the backend at ${API_BASE_URL}. Is it running?`);
  } finally {
    btn.disabled = false;
  }
});
