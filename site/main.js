const DATA = window.GAME_CODEX_DATA;

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => [...document.querySelectorAll(selector)];

const state = {
  activeStage: DATA.stageVignettes?.stages?.[0]?.id || "opening",
  selectedCandidate: null,
  chroma: 52,
  activeGame: "lee",
  traceIndex: 0,
  traceTimer: null,
  driftIndex: 0,
  horizon: 3,
  regionalPhase: 1,
};

const fallbackStage = {
  id: "middle",
  label: "Middle game",
  chroma: 52,
  stones: [
    { x: 3, y: 3, color: "black" },
    { x: 15, y: 3, color: "white" },
    { x: 16, y: 15, color: "black" },
    { x: 3, y: 15, color: "white" },
    { x: 9, y: 9, color: "white" },
    { x: 10, y: 9, color: "black" },
    { x: 11, y: 10, color: "white" },
  ],
  candidates: [
    { id: "a", key: "A", name: "Contact pressure", x: 10, y: 10, color: "black", aiGap: 0, rhythm: "AI-like pressure" },
    { id: "b", key: "B", name: "Outer extension", x: 6, y: 12, color: "black", aiGap: 0.22, rhythm: "human-style extension" },
  ],
};

function formatPct(value) {
  return `${Math.round(value * 100)}%`;
}

function rankDisplay(row) {
  const rank = row.rawRank || row.rank;
  return {
    value: Math.min(rank, 20),
    label: rank > 20 ? "policy rank >20" : `policy rank ${rank}`,
    isCapped: rank > 20,
  };
}

function fmt(value, digits = 3) {
  return Number(value).toFixed(digits);
}

function referenceLabel(candidate) {
  if (candidate.reference) return candidate.reference;
  if (candidate.aiGap === 0) return "reference";
  return `+${fmt(candidate.aiGap, 2)}`;
}

function lifecycleLabel(value) {
  if (value < 24) return "Opening";
  if (value < 68) return "Middle game";
  return "Endgame";
}

function boardStages() {
  return DATA.stageVignettes?.stages?.length ? DATA.stageVignettes.stages : [fallbackStage];
}

function activeBoardStage() {
  return boardStages().find((stage) => stage.id === state.activeStage) || boardStages()[0];
}

function activeCandidate() {
  const stage = activeBoardStage();
  if (!state.selectedCandidate) {
    state.selectedCandidate = stage.candidates[0]?.id;
  }
  return stage.candidates.find((candidate) => candidate.id === state.selectedCandidate) || stage.candidates[0];
}

function resizeCanvas(canvas) {
  const rect = canvas.getBoundingClientRect();
  const dpr = window.devicePixelRatio || 1;
  canvas.width = Math.max(320, Math.round(rect.width * dpr));
  canvas.height = canvas.width;
  return { size: canvas.width, dpr };
}

function drawBoard() {
  const canvas = $("#go-board");
  if (!canvas) return;
  const stage = activeBoardStage();
  const selected = activeCandidate();
  const ctx = canvas.getContext("2d");
  const { size, dpr } = resizeCanvas(canvas);
  const margin = size * 0.07;
  const step = (size - margin * 2) / 18;
  ctx.clearRect(0, 0, size, size);
  ctx.fillStyle = "#f1ead8";
  ctx.fillRect(0, 0, size, size);
  ctx.strokeStyle = "#101010";
  ctx.lineWidth = Math.max(1, dpr);

  for (let i = 0; i < 19; i += 1) {
    const p = margin + i * step;
    ctx.beginPath();
    ctx.moveTo(margin, p);
    ctx.lineTo(size - margin, p);
    ctx.moveTo(p, margin);
    ctx.lineTo(p, size - margin);
    ctx.stroke();
  }

  [3, 9, 15].forEach((x) => {
    [3, 9, 15].forEach((y) => {
      ctx.beginPath();
      ctx.fillStyle = "#101010";
      ctx.arc(margin + x * step, margin + y * step, step * 0.08, 0, Math.PI * 2);
      ctx.fill();
    });
  });

  const drawStone = (stone, ghost = false, label = "") => {
    const px = margin + stone.x * step;
    const py = margin + stone.y * step;
    const r = step * 0.42;
    ctx.save();
    ctx.globalAlpha = ghost ? 0.5 : 1;
    ctx.beginPath();
    ctx.arc(px, py, r, 0, Math.PI * 2);
    ctx.fillStyle = stone.color === "black" ? "#101010" : "#fffdf8";
    ctx.fill();
    ctx.lineWidth = Math.max(1, dpr * 1.2);
    ctx.strokeStyle = "#101010";
    ctx.stroke();
    if (label) {
      ctx.fillStyle = stone.color === "black" ? "#fffdf8" : "#101010";
      ctx.font = `${Math.round(step * 0.42)}px sans-serif`;
      ctx.textAlign = "center";
      ctx.textBaseline = "middle";
      ctx.fillText(label, px, py + step * 0.02);
    }
    ctx.restore();
  };

  stage.stones.forEach((stone) => drawStone(stone));
  stage.candidates.forEach((candidate) => {
    drawStone(candidate, candidate.id !== selected.id, candidate.key);
    if (candidate.id === selected.id) {
      const px = margin + candidate.x * step;
      const py = margin + candidate.y * step;
      ctx.save();
      ctx.strokeStyle = "#a33c2f";
      ctx.lineWidth = Math.max(2, dpr * 2);
      ctx.beginPath();
      ctx.arc(px, py, step * 0.54, 0, Math.PI * 2);
      ctx.stroke();
      ctx.restore();
    }
  });

  canvas._boardGeometry = { margin, step, size };
  updateFeatures();
}

function nearestDistance(candidate, stones) {
  return Math.min(...stones.map((stone) => Math.hypot(stone.x - candidate.x, stone.y - candidate.y)));
}

function isOccupied(x, y, stones) {
  return stones.some((stone) => stone.x === x && stone.y === y);
}

function localCounts(candidate, stones) {
  let own = 0;
  let opp = 0;
  stones.forEach((stone) => {
    const distance = Math.hypot(stone.x - candidate.x, stone.y - candidate.y);
    if (distance <= Math.SQRT2 + 0.01) {
      if (stone.color === candidate.color) own += 1;
      else opp += 1;
    }
  });
  return { own, opp };
}

function openCorner(candidate, stones) {
  const corners = [
    { x: 3, y: 3 },
    { x: 15, y: 3 },
    { x: 3, y: 15 },
    { x: 15, y: 15 },
  ];
  const corner = corners.find((c) => Math.hypot(c.x - candidate.x, c.y - candidate.y) <= 3.8);
  if (!corner) return false;
  return stones.every((stone) => Math.hypot(stone.x - corner.x, stone.y - corner.y) > 4.2);
}

function rhythmLabel(candidate, counts, distance, cornerOpen) {
  if (cornerOpen && state.chroma < 32) return "new corner topic";
  if (counts.opp > counts.own && distance <= 2.2) return "contact pressure";
  if (counts.own > counts.opp && distance <= 2.2) return "local extension";
  if (distance > 6) return "tenuki / new area";
  return "positional bridge";
}

function updateFeatures() {
  const stage = activeBoardStage();
  const candidate = activeCandidate();
  state.chroma = stage.chroma;
  const distance = nearestDistance(candidate, stage.stones);
  const counts = localCounts(candidate, stage.stones);
  const corner = openCorner(candidate, stage.stones);
  $("#stage-label").textContent = stage.label;
  $("#candidate-label").textContent = candidate.name;
  const source = $("#stage-source");
  if (source) {
    const link = stage.sourceUrl
      ? `<a href="${stage.sourceUrl}" target="_blank" rel="noreferrer">SGF</a>`
      : "";
    source.innerHTML = `
      <strong>${stage.regionTag || lifecycleLabel(stage.chroma)}</strong>
      <span>${stage.source || ""}</span>
      ${link}
      <em>${stage.positionNote || ""}</em>
    `;
  }
  $("#feat-move").textContent = `${candidate.key}: ${candidate.name}${candidate.moveNumber ? ` (move ${candidate.moveNumber})` : ""}`;
  $("#feat-distance").textContent = `${fmt(distance, 1)} lines`;
  $("#feat-own").textContent = counts.own;
  $("#feat-opp").textContent = counts.opp;
  $("#feat-corner").textContent = corner ? "yes" : "no";
  $("#feat-ai-gap").textContent = referenceLabel(candidate);
  $("#feat-label").textContent = candidate.rhythm || rhythmLabel(candidate, counts, distance, corner);
}

function renderStageControls() {
  const container = $("#stage-tabs");
  container.innerHTML = "";
  boardStages().forEach((stage) => {
    const button = document.createElement("button");
    button.className = `seg-button ${stage.id === state.activeStage ? "active" : ""}`;
    button.type = "button";
    button.textContent = stage.label;
    button.setAttribute("role", "tab");
    button.addEventListener("click", () => {
      state.activeStage = stage.id;
      state.selectedCandidate = stage.candidates[0]?.id;
      renderStageControls();
      renderCandidateList();
      drawBoard();
    });
    container.appendChild(button);
  });
}

function renderCandidateList() {
  const stage = activeBoardStage();
  const container = $("#candidate-list");
  container.innerHTML = "";
  stage.candidates.forEach((candidate) => {
    const button = document.createElement("button");
    button.className = `candidate-button ${candidate.id === activeCandidate().id ? "active" : ""}`;
    button.type = "button";
    button.innerHTML = `
      <span class="candidate-key">${candidate.key}</span>
      <span class="candidate-name">${candidate.name}</span>
      <span class="candidate-gap">${referenceLabel(candidate)}</span>
    `;
    button.addEventListener("click", () => {
      state.selectedCandidate = candidate.id;
      renderCandidateList();
      drawBoard();
    });
    container.appendChild(button);
  });
}

function setupBoard() {
  state.selectedCandidate = activeBoardStage().candidates[0]?.id;
  renderStageControls();
  renderCandidateList();

  const canvas = $("#go-board");
  canvas.addEventListener("click", (event) => {
    const geometry = canvas._boardGeometry;
    if (!geometry) return;
    const rect = canvas.getBoundingClientRect();
    const scale = geometry.size / rect.width;
    const px = (event.clientX - rect.left) * scale;
    const py = (event.clientY - rect.top) * scale;
    const x = Math.round((px - geometry.margin) / geometry.step);
    const y = Math.round((py - geometry.margin) / geometry.step);
    const stage = activeBoardStage();
    const candidate = stage.candidates.find((move) => Math.hypot(move.x - x, move.y - y) <= 1);
    if (!candidate) return;
    state.selectedCandidate = candidate.id;
    renderCandidateList();
    drawBoard();
  });

  $("#reset-board").addEventListener("click", () => {
    state.selectedCandidate = activeBoardStage().candidates[0]?.id;
    renderCandidateList();
    drawBoard();
  });

  window.addEventListener("resize", drawBoard);
  drawBoard();
}

function activeGame() {
  return DATA.pairedVignette.games.find((game) => game.id === state.activeGame);
}

function setupTrace() {
  const tabs = $("#game-tabs");
  DATA.pairedVignette.games.forEach((game) => {
    const button = document.createElement("button");
    button.className = `seg-button ${game.id === state.activeGame ? "active" : ""}`;
    button.type = "button";
    button.textContent = game.shortLabel;
    button.setAttribute("role", "tab");
    button.addEventListener("click", () => {
      state.activeGame = game.id;
      state.traceIndex = 0;
      stopTrace();
      renderTrace();
    });
    tabs.appendChild(button);
  });

  $("#trace-slider").addEventListener("input", (event) => {
    state.traceIndex = Number(event.target.value);
    renderTrace(false);
  });

  $("#play-trace").addEventListener("click", () => {
    if (state.traceTimer) {
      stopTrace();
      return;
    }
    $("#play-trace").textContent = "Pause";
    state.traceTimer = window.setInterval(() => {
      const game = activeGame();
      state.traceIndex = (state.traceIndex + 1) % game.rows.length;
      renderTrace(false);
    }, 260);
  });

  renderTrace();
}

function stopTrace() {
  if (state.traceTimer) {
    window.clearInterval(state.traceTimer);
    state.traceTimer = null;
  }
  $("#play-trace").textContent = "Play";
}

function renderTrace(updateTabs = true) {
  const game = activeGame();
  const rows = game.rows;
  const slider = $("#trace-slider");
  slider.max = rows.length - 1;
  slider.value = state.traceIndex;
  const current = rows[state.traceIndex];

  if (updateTabs) {
    $$("#game-tabs .seg-button").forEach((button, idx) => {
      button.classList.toggle("active", DATA.pairedVignette.games[idx].id === state.activeGame);
    });
  }

  $("#trace-move").textContent = `Move ${current.move}`;
  const currentRank = rankDisplay(current);
  $("#trace-rank").textContent = currentRank.label;
  $("#trace-winrate").textContent = `human win-rate ${formatPct(current.winrate)}`;
  $("#trace-note").textContent = game.note;

  const w = 860;
  const h = 190;
  const pad = { top: 32, right: 52, bottom: 24, left: 52 };
  const minMove = Math.min(...rows.map((r) => r.move));
  const maxMove = Math.max(...rows.map((r) => r.move));
  const x = (move) => pad.left + ((move - minMove) / (maxMove - minMove)) * (w - pad.left - pad.right);
  const markerPercent = (move) => ((move - minMove) / (maxMove - minMove)) * 100;
  const rankY = (rank) => pad.top + ((rank - 1) / 19) * (h - pad.top - pad.bottom);
  const rankPath = rows.map((r, idx) => {
    const display = rankDisplay(r);
    return `${idx === 0 ? "M" : "L"}${x(r.move).toFixed(1)},${rankY(display.value).toFixed(1)}`;
  }).join(" ");
  const cx = x(current.move);
  const cy = rankY(currentRank.value);
  const markers = game.markers || (game.pivotMove ? [{ move: game.pivotMove, label: `move ${game.pivotMove}` }] : []);

  $("#trace-slider-markers").innerHTML = markers.map((marker) => {
    const label = marker.label || `move ${marker.move}`;
    return `<span class="trace-marker" style="left:${markerPercent(marker.move)}%" title="${label}"></span>`;
  }).join("");

  const quote = $("#trace-quote");
  if (game.quote) {
    quote.hidden = false;
    const quoteText = game.quote.isParaphrase ? game.quote.text : `"${game.quote.text}"`;
    quote.innerHTML = `<strong>${game.quote.lead}</strong> ${quoteText} <a href="${game.quote.url}" target="_blank" rel="noreferrer">${game.quote.sourceLabel}</a>`;
  } else {
    quote.hidden = true;
    quote.textContent = "";
  }

  $("#trace-chart").innerHTML = `
    <svg viewBox="0 0 ${w} ${h}" aria-hidden="true">
      <rect width="${w}" height="${h}" fill="#fbfaf7"></rect>
      <rect x="${pad.left}" y="${rankY(1)}" width="${w - pad.left - pad.right}" height="${rankY(5) - rankY(1)}" fill="#eeece4"></rect>
      <line x1="${pad.left}" y1="${pad.top}" x2="${pad.left}" y2="${h - pad.bottom}" stroke="#d9d6ca"/>
      <line x1="${pad.left}" y1="${h - pad.bottom}" x2="${w - pad.right}" y2="${h - pad.bottom}" stroke="#d9d6ca"/>
      <text x="${pad.left}" y="20" font-size="12">policy rank: 1 = KataGo first choice; 20+ = outside top 20</text>
      <text x="${w - 180}" y="20" font-size="12" fill="#68645c">top-5 AI band</text>
      ${[1, 5, 10, 15, 20].map((tick) => `
        <line x1="${pad.left}" x2="${w - pad.right}" y1="${rankY(tick)}" y2="${rankY(tick)}" stroke="#eeece4"/>
        <text x="${tick === 20 ? 9 : 16}" y="${rankY(tick) + 4}" font-size="11">${tick === 20 ? "20+" : tick}</text>
      `).join("")}
      <path d="${rankPath}" fill="none" stroke="#101010" stroke-width="3"/>
      <circle cx="${cx}" cy="${cy}" r="7" fill="${currentRank.isCapped ? "#a33c2f" : "#101010"}"></circle>
      <text x="${pad.left}" y="${h - 13}" font-size="12">${minMove}</text>
      <text x="${w - pad.right - 24}" y="${h - 13}" font-size="12">${maxMove}</text>
    </svg>
  `;

  const wh = 154;
  const wpad = { top: 18, right: 52, bottom: 26, left: 52 };
  const winY = (value) => wpad.top + (1 - value) * (wh - wpad.top - wpad.bottom);
  const winPath = rows.map((r, idx) => `${idx === 0 ? "M" : "L"}${x(r.move).toFixed(1)},${winY(r.winrate).toFixed(1)}`).join(" ");
  $("#winrate-chart").innerHTML = `
    <svg viewBox="0 0 ${w} ${wh}" aria-hidden="true">
      <rect width="${w}" height="${wh}" fill="#fbfaf7"></rect>
      <line x1="${wpad.left}" y1="${wh - wpad.bottom}" x2="${w - wpad.right}" y2="${wh - wpad.bottom}" stroke="#d9d6ca"/>
      <line x1="${wpad.left}" y1="${wpad.top}" x2="${wpad.left}" y2="${wh - wpad.bottom}" stroke="#d9d6ca"/>
      ${[0.25, 0.5, 0.75].map((tick) => `
        <line x1="${wpad.left}" x2="${w - wpad.right}" y1="${winY(tick)}" y2="${winY(tick)}" stroke="#eeece4"/>
        <text x="15" y="${winY(tick) + 4}" font-size="11">${formatPct(tick)}</text>
      `).join("")}
      <text x="${wpad.left}" y="17" font-size="12" fill="#23645b">human win-rate, separate from policy rank</text>
      <path d="${winPath}" fill="none" stroke="#23645b" stroke-width="3"/>
      <circle cx="${cx}" cy="${winY(current.winrate)}" r="6" fill="#23645b"></circle>
      <text x="${Math.min(cx + 10, w - 160)}" y="${Math.max(winY(current.winrate) - 8, 32)}" font-size="12">${formatPct(current.winrate)}</text>
    </svg>
  `;
}

function renderDrift() {
  const pairs = DATA.drift.pairs;
  if (state.driftIndex === 0) {
    state.driftIndex = pairs.findIndex((p) => p.is_ai_era);
  }
  const w = 900;
  const h = 258;
  const pad = { top: 26, right: 24, bottom: 48, left: 46 };
  const max = Math.max(...pairs.map((p) => p.value)) * 1.08;
  const barW = (w - pad.left - pad.right) / pairs.length;
  const y = (value) => h - pad.bottom - (value / max) * (h - pad.top - pad.bottom);
  const bars = pairs.map((p, idx) => {
    const x = pad.left + idx * barW + 1;
    const height = h - pad.bottom - y(p.value);
    const fill = p.is_largest ? "#101010" : p.is_ai_era ? "#a33c2f" : "#b8b3a8";
    const stroke = idx === state.driftIndex ? "#101010" : "none";
    return `
      <rect class="bar" data-index="${idx}" x="${x}" y="${y(p.value)}" width="${Math.max(3, barW - 2)}" height="${height}" fill="${fill}" stroke="${stroke}" stroke-width="2">
        <title>${p.from} to ${p.to}: ${p.value}</title>
      </rect>`;
  }).join("");
  const selected = pairs[state.driftIndex];

  $("#drift-chart").innerHTML = `
    <svg viewBox="0 0 ${w} ${h}" aria-hidden="true">
      <rect width="${w}" height="${h}" fill="#fbfaf7"></rect>
      <line x1="${pad.left}" x2="${w - pad.right}" y1="${h - pad.bottom}" y2="${h - pad.bottom}" stroke="#d9d6ca"/>
      <line x1="${pad.left}" x2="${pad.left}" y1="${pad.top}" y2="${h - pad.bottom}" stroke="#d9d6ca"/>
      ${[0.01, 0.02, 0.03].map((tick) => `
        <line x1="${pad.left}" x2="${w - pad.right}" y1="${y(tick)}" y2="${y(tick)}" stroke="#eeece4"/>
        <text x="8" y="${y(tick) + 4}" font-size="11">${tick.toFixed(2)}</text>
      `).join("")}
      ${bars}
      <line x1="${pad.left}" x2="${w - pad.right}" y1="${y(DATA.drift.summary.pre2016Mean)}" y2="${y(DATA.drift.summary.pre2016Mean)}" stroke="#23645b" stroke-width="2" stroke-dasharray="6 5"/>
      <text x="${w - 205}" y="${y(DATA.drift.summary.pre2016Mean) - 8}" font-size="12" fill="#23645b">pre-2016 mean</text>
      <text x="${pad.left}" y="${h - 19}" font-size="12">1600s</text>
      <text x="${w - 96}" y="${h - 19}" font-size="12">2020s</text>
      <text x="${pad.left + 90}" y="${h - 19}" font-size="12" fill="#68645c">Red: AI decade. Black: largest comparator. Green: pre-2016 mean.</text>
    </svg>
  `;

  $("#drift-detail").innerHTML = `
    <div class="detail-head">
      <span><strong>${selected.from} to ${selected.to}</strong></span>
      <span>drift ${fmt(selected.value, 4)}</span>
    </div>
    <div class="detail-event">
      <strong>${selected.event}</strong>
      <p>${selected.read}</p>
    </div>
  `;
}

function setupDrift() {
  renderDrift();
  $("#drift-chart").addEventListener("click", (event) => {
    const bar = event.target.closest(".bar");
    if (!bar) return;
    state.driftIndex = Number(bar.dataset.index);
    renderDrift();
  });
}

function setupAdoption() {
  renderAdoption();
}

function parsePattern(pattern) {
  const sgfCols = "abcdefghijklmnopqrs";
  return pattern.split(",").map((entry, idx) => {
    const color = entry[0] === "B" ? "black" : "white";
    const coord = entry.slice(1, 3);
    return {
      index: idx + 1,
      color,
      x: sgfCols.indexOf(coord[0]),
      y: sgfCols.indexOf(coord[1]),
    };
  }).filter((move) => move.x >= 0 && move.y >= 0);
}

function patternBoard(pattern) {
  const moves = parsePattern(pattern);
  const size = 210;
  const pad = 17;
  const step = (size - pad * 2) / 18;
  const stars = [3, 9, 15].flatMap((x) => [3, 9, 15].map((y) => ({ x, y })));
  return `
    <svg class="pattern-board" viewBox="0 0 ${size} ${size}" aria-hidden="true">
      <rect width="${size}" height="${size}" fill="#f1ead8"></rect>
      ${Array.from({ length: 19 }, (_, idx) => {
        const p = pad + idx * step;
        return `<path d="M${pad},${p}H${size - pad}M${p},${pad}V${size - pad}" stroke="#101010" stroke-width="0.8"/>`;
      }).join("")}
      ${stars.map((star) => `
        <circle cx="${pad + star.x * step}" cy="${pad + star.y * step}" r="1.6" fill="#101010"/>
      `).join("")}
      ${moves.map((move) => {
        const cx = pad + move.x * step;
        const cy = pad + move.y * step;
        const fill = move.color === "black" ? "#101010" : "#fffdf8";
        const text = move.color === "black" ? "#fffdf8" : "#101010";
        return `
          <g>
            <circle cx="${cx}" cy="${cy}" r="4.8" fill="${fill}" stroke="#101010" stroke-width="0.8"/>
            <text x="${cx}" y="${cy + 1.8}" text-anchor="middle" font-size="5.2" fill="${text}">${move.index}</text>
          </g>
        `;
      }).join("")}
    </svg>
  `;
}

function patternFlow(example) {
  const steps = [
    ["first seen", example.firstSeen],
    ["3+ players", example.adoptedYear ?? "-"],
    [`peak ${example.peakUsage} uses`, example.peakYear],
    ["last seen", example.lastSeen],
  ];
  return steps.map(([label, value]) => `
    <div class="flow-step">
      <span>${label}</span>
      <strong>${value}</strong>
    </div>
  `).join("");
}

function renderAdoption() {
  const eras = DATA.adoption.eras;
  const first = eras[0];
  const last = eras[eras.length - 1];
  const examples = DATA.adoption.examples || [];
  const definition = DATA.adoption.definition || {};
  const comparison = [first, last];
  const maxLag = Math.max(...comparison.map((era) => era.meanLag));
  $("#adoption-chart").innerHTML = `
    <div class="adoption-speed">
      <div class="pattern-definition">
        <strong>Pattern = ${definition.unit || "opening fingerprint"}</strong>
        <span>${definition.qualifier || ""}</span>
        <em>${definition.interpretation || ""}</em>
      </div>
      <div class="pattern-cards" aria-label="Concrete opening pattern circulation examples">
        ${examples.map((example) => `
          <article class="pattern-card">
            <div class="pattern-card-head">
              <span>${example.label}</span>
              <strong>${example.adoptionLag === 0 ? "same-year adoption" : `${example.adoptionLag}y adoption lag`}</strong>
            </div>
            <div class="pattern-card-body">
              ${patternBoard(example.pattern)}
              <div class="pattern-copy">
                <p>${example.summary}</p>
                <div class="pattern-flow">${patternFlow(example)}</div>
                <div class="pattern-stats">
                  <span>${example.totalUses} uses</span>
                  <span>${example.nRegions} stream${example.nRegions === 1 ? "" : "s"}</span>
                  <span>${formatPct(example.reuseRate)} reuse density</span>
                </div>
              </div>
            </div>
          </article>
        `).join("")}
      </div>
      <div class="speed-claim">
        <span>Aggregate check against the pre-1980 baseline</span>
        <strong>${fmt(first.meanLag, 1)} years -> ${fmt(last.meanLag, 1)} years</strong>
        <em>${fmt(DATA.adoption.lagRatio, 1)}x faster after public AI oracles</em>
      </div>
      <div class="lag-lanes" aria-label="Mean observed adoption lag">
        ${comparison.map((era) => `
          <div class="lag-row ${era.era === "2016+" ? "hot" : ""}">
            <span>${era.era}</span>
            <div class="lag-track">
              <i style="width:${(era.meanLag / maxLag) * 100}%"></i>
            </div>
            <strong>${fmt(era.meanLag, 1)}y</strong>
          </div>
        `).join("")}
      </div>
    </div>
  `;
}

function renderRegional() {
  const phases = DATA.regional.phases;
  const streams = DATA.regional.streams || [
    { id: "jpn", label: "Japan", short: "anchor", color: "#101010" },
    { id: "kor", label: "Korea", short: "fighting", color: "#a33c2f" },
    { id: "chn", label: "China", short: "mobility", color: "#23645b" },
  ];
  const activeIndex = Math.min(state.regionalPhase, phases.length - 1);
  const activePhase = phases[activeIndex];
  const rhythm = activePhase.rhythm || {};
  const vectors = rhythm.vectors || [];
  const pairs = rhythm.pairs || [];
  const streamByRegion = Object.fromEntries(streams.map((stream) => [stream.id.toUpperCase(), stream]));
  const rhythmBounds = DATA.regional.rhythmBounds || {
    contact: { min: 0.02, max: 0.05 },
    mobility: { min: 0.15, max: 0.175 },
  };
  const maxDistance = Math.max(...phases.map((phase) => phase.distance));
  const maxPairDistance = Math.max(...phases.flatMap((phase) => (phase.rhythm?.pairs || []).map((pair) => pair.distance)), 0.001);
  const scalePoint = (vector) => {
    const contactSpan = rhythmBounds.contact.max - rhythmBounds.contact.min || 1;
    const mobilitySpan = rhythmBounds.mobility.max - rhythmBounds.mobility.min || 1;
    return {
      x: 54 + ((vector.contactIndex - rhythmBounds.contact.min) / contactSpan) * 252,
      y: 226 - ((vector.mobilityIndex - rhythmBounds.mobility.min) / mobilitySpan) * 170,
    };
  };
  const centerVector = vectors.length ? {
    contactIndex: vectors.reduce((sum, vector) => sum + vector.contactIndex, 0) / vectors.length,
    mobilityIndex: vectors.reduce((sum, vector) => sum + vector.mobilityIndex, 0) / vectors.length,
  } : { contactIndex: 0, mobilityIndex: 0 };
  const centerPoint = scalePoint(centerVector);
  const deltaLabel = (pct, suffix = "") => {
    if (pct === null || pct === undefined) return "baseline";
    const direction = pct < 0 ? "closer" : "wider";
    return `${fmt(Math.abs(pct), 1)}% ${direction}${suffix}`;
  };
  const phaseDeltaText = deltaLabel(rhythm.deltaFromPreviousPct, " vs previous");
  const points = {
    jpn: [[70, 86], [335, 152], [585, 104], [830, 154]],
    kor: [[70, 180], [335, 172], [585, 236], [830, 176]],
    chn: [[70, 274], [335, 192], [585, 168], [830, 198]],
  };
  const pathFor = (series) => series.map(([x, y], idx) => {
    if (idx === 0) return `M${x},${y}`;
    const [px, py] = series[idx - 1];
    const dx = x - px;
    return `C${px + dx * 0.48},${py} ${x - dx * 0.48},${y} ${x},${y}`;
  }).join(" ");
  const phaseXs = [70, 335, 585, 830];

  $("#regional-chart").innerHTML = `
    <div class="regional-braid">
      <div class="braid-legend" aria-label="Regional stream legend">
        ${streams.map((stream) => `
          <span><i style="background:${stream.color}"></i><strong>${stream.label}</strong>${stream.short}</span>
        `).join("")}
      </div>
      <svg class="braid-svg" viewBox="0 0 900 370" role="img" aria-label="Regional style streams converge and diverge across the AI decade">
        <rect width="900" height="370" fill="#fbfaf7"></rect>
        ${phases.map((phase, idx) => `
          <g class="regional-phase-target ${idx === activeIndex ? "active" : ""}" data-index="${idx}">
            <rect x="${phaseXs[idx] - 80}" y="0" width="160" height="370" fill="${idx === activeIndex ? "#eeece4" : "transparent"}" opacity="${idx === activeIndex ? "0.62" : "1"}"></rect>
            <line x1="${phaseXs[idx]}" x2="${phaseXs[idx]}" y1="42" y2="310" stroke="#d9d6ca" stroke-dasharray="5 6"></line>
            <text x="${phaseXs[idx]}" y="22" text-anchor="middle" font-size="13" font-weight="800">${phase.plain || phase.phase}</text>
            <text x="${phaseXs[idx]}" y="39" text-anchor="middle" font-size="11" fill="#68645c">${phase.years}</text>
          </g>
        `).join("")}
        <path d="M305,176 C318,132 350,132 365,176 C350,220 318,220 305,176" fill="none" stroke="#a33c2f" stroke-width="1.5" opacity="0.55"></path>
        <path d="M800,176 C814,142 846,142 860,176 C846,210 814,210 800,176" fill="none" stroke="#a33c2f" stroke-width="1.5" opacity="0.45"></path>
        ${streams.map((stream) => `
          <path d="${pathFor(points[stream.id])}" fill="none" stroke="${stream.color}" stroke-width="5" stroke-linecap="round" opacity="0.94"></path>
          ${points[stream.id].map(([x, y]) => `
            <circle cx="${x}" cy="${y}" r="6" fill="#fbfaf7" stroke="${stream.color}" stroke-width="3"></circle>
          `).join("")}
          <text x="18" y="${points[stream.id][0][1] + 4}" font-size="12" font-weight="800" fill="${stream.color}">${stream.label}</text>
        `).join("")}
        ${phases.map((phase, idx) => `
          <g transform="translate(${phaseXs[idx] - 54},324)">
            <line x1="0" x2="108" y1="0" y2="0" stroke="#d9d6ca" stroke-width="4" stroke-linecap="round"></line>
            <line x1="0" x2="${(phase.distance / maxDistance) * 108}" y1="0" y2="0" stroke="${idx === 1 || idx === 3 ? "#a33c2f" : "#101010"}" stroke-width="4" stroke-linecap="round"></line>
            <text x="54" y="22" text-anchor="middle" font-size="12" font-weight="800">${fmt(phase.distance, 4)}</text>
          </g>
        `).join("")}
      </svg>
      <div class="braid-phase-grid">
        ${phases.map((phase, idx) => `
          <article class="${idx === activeIndex ? "active" : ""} ${idx === 1 || idx === 3 ? "tight" : ""}" data-index="${idx}">
            <span>${phase.phase}</span>
            <strong>${phase.plain || phase.phase}</strong>
            <p>${idx === activeIndex ? phase.note : phase.years}</p>
          </article>
        `).join("")}
      </div>
      <div class="regional-detail rhythm-detail">
        <section class="rhythm-panel">
          <div class="regional-detail-head">
            <span>${activePhase.phase}</span>
            <strong>Country rhythm vectors</strong>
            <em>${activePhase.years}; mean SHP rhythm for moves 16-50</em>
          </div>
          <div class="fingerprint-phase-read rhythm-phase-read">
            <span>${activePhase.plain}: ${activePhase.note}</span>
            <strong>gap ${fmt(rhythm.meanDistance || activePhase.distance, 4)} - ${phaseDeltaText}</strong>
          </div>
          <div class="rhythm-phase-strip">
            ${phases.map((phase, idx) => `
              <button class="${idx === activeIndex ? "active" : ""}" data-index="${idx}" type="button">
                <span>${phase.plain || phase.phase}</span>
                <strong>${fmt(phase.rhythm?.meanDistance || phase.distance, 4)}</strong>
                <em>${phase.rhythm?.deltaFromPreviousPct === null || phase.rhythm?.deltaFromPreviousPct === undefined
                  ? "baseline"
                  : deltaLabel(phase.rhythm.deltaFromPreviousPct)}</em>
              </button>
            `).join("")}
          </div>
          <div class="rhythm-map-grid">
            <div class="rhythm-map-card">
              <svg viewBox="0 0 360 260" role="img" aria-label="Country rhythm vectors in contact and mobility space">
                <rect x="0" y="0" width="360" height="260" rx="8" fill="#fbfaf7"></rect>
                <line x1="44" x2="320" y1="226" y2="226" stroke="#d9d6ca"></line>
                <line x1="44" x2="44" y1="42" y2="230" stroke="#d9d6ca"></line>
                <text x="182" y="248" text-anchor="middle" font-size="11" fill="#68645c">contact pressure</text>
                <text x="17" y="136" text-anchor="middle" font-size="11" fill="#68645c" transform="rotate(-90 17 136)">opening mobility</text>
                <circle cx="248" cy="50" r="5" fill="#fbfaf7" stroke="#101010" stroke-width="1.6"></circle>
                <text x="259" y="54" font-size="11" font-weight="800" fill="#101010">shared center</text>
                <circle cx="${centerPoint.x}" cy="${centerPoint.y}" r="8" fill="#fbfaf7" stroke="#101010" stroke-width="2"></circle>
                ${vectors.map((vector) => {
                  const point = scalePoint(vector);
                  const stream = streamByRegion[vector.region] || { color: "#101010", label: vector.label };
                  return `
                    <line x1="${centerPoint.x}" x2="${point.x}" y1="${centerPoint.y}" y2="${point.y}" stroke="${stream.color}" stroke-width="1.5" stroke-dasharray="4 4" opacity="0.65"></line>
                    <circle cx="${point.x}" cy="${point.y}" r="9" fill="${stream.color}"></circle>
                    <text x="${point.x + 13}" y="${point.y + 4}" font-size="12" font-weight="800" fill="${stream.color}">${vector.label}</text>
                  `;
                }).join("")}
              </svg>
            </div>
            <div class="pair-gap-card">
              <span>Pairwise rhythm gaps</span>
              <strong>${fmt(rhythm.meanDistance || activePhase.distance, 4)}</strong>
              <p>Lower gap means the country-coded event streams are choosing moves from a more similar SHP rhythm position.</p>
              <div class="pair-gap-bars">
                ${pairs.map((pair) => `
                  <div>
                    <span>${pair.pair}</span>
                    <b>${fmt(pair.distance, 4)}</b>
                    <i style="width:${(pair.distance / maxPairDistance) * 100}%"></i>
                  </div>
                `).join("")}
              </div>
            </div>
          </div>
          <div class="country-vector-grid">
            ${vectors.map((vector) => {
              const stream = streamByRegion[vector.region] || { color: "#101010", label: vector.label };
              return `
                <article style="--stream-color:${stream.color}">
                  <div class="country-vector-head">
                    <span>${vector.label}</span>
                    <strong>${fmt(vector.gapToCenter, 4)}</strong>
                  </div>
                  <p>gap to shared center - ${Math.round(vector.nMoves / 1000)}k moves</p>
                  <div class="vector-feature-list">
                    <div><span>contact</span><b>${fmt(vector.contactIndex, 4)}</b></div>
                    <div><span>open corner</span><b>${formatPct(vector.features.is_corner_open)}</b></div>
                    <div><span>step length</span><b>${fmt(vector.features.dist_last, 3)}</b></div>
                  </div>
                </article>
              `;
            }).join("")}
          </div>
        </section>
      </div>
    </div>
  `;

  $("#signature-chart").innerHTML = `
    <div class="regional-footnote">
      Measured with five SHP rhythm features. The braid uses phase-aggregated country vectors;
      the technical note reports separate bootstrap checks.
    </div>
  `;

  $$("#regional-chart [data-index]").forEach((target) => {
    target.addEventListener("click", () => {
      state.regionalPhase = Number(target.dataset.index);
      renderRegional();
    });
  });
}

function init() {
  setupBoard();
  setupTrace();
  setupDrift();
  setupAdoption();
  renderRegional();
}

init();
