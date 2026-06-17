const DATA = window.FOOTBALL_DATA;

const state = {
  methodFrame: 0,
  selectedTeam: "Spain",
  opponent: "Spain",
  teamA: "Morocco",
  teamB: "Portugal",
};

let methodTimer = null;

const teamColors = {
  Argentina: "#ffffff",
  France: "#080a08",
};

const starStyles = {
  Messi: { stroke: "#050705", fill: "#f0d45a", text: "#ffffff" },
  Mbappe: { stroke: "#ffffff", fill: "#111111", text: "#ffffff" },
  "Di Maria": { stroke: "#050705", fill: "#75c7f0", text: "#ffffff" },
};

function fmt(n, digits = 3) {
  return Number(n).toFixed(digits);
}

function fmtPct(n, digits = 0) {
  return `${(Number(n) * 100).toFixed(digits)}%`;
}

function esc(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function shortName(name) {
  const clean = String(name || "").trim();
  if (clean.length <= 20) return clean;
  const parts = clean.split(/\s+/);
  if (parts.length >= 2) return `${parts[0]} ${parts[parts.length - 1]}`;
  return `${clean.slice(0, 18)}...`;
}

function compact(n) {
  if (n >= 1000000) return `${(n / 1000000).toFixed(1)}M`;
  if (n >= 1000) return `${Math.round(n / 1000)}K`;
  return String(n);
}

const STYLE_SPLITS = {
  territory: 0.4785,
  pressure: 0.0755,
};

function styleArchetype(team) {
  const highTerritory = team.x >= STYLE_SPLITS.territory;
  const highPressure = team.pressureRate >= STYLE_SPLITS.pressure;
  if (highTerritory && highPressure) {
    return {
      name: "Front-foot hunters",
      read: "They play higher and keep biting. The match feels squeezed forward.",
    };
  }
  if (highTerritory) {
    return {
      name: "Territory controllers",
      read: "They camp higher upfield and let the game settle around possession.",
    };
  }
  if (highPressure) {
    return {
      name: "Counterpunch disruptors",
      read: "They live lower, then break the rhythm with pressure and duels.",
    };
  }
  return {
    name: "Deep absorbers",
    read: "They sit deeper and make the opponent carry the weight of the game.",
  };
}

function metricAverage(key) {
  const values = DATA.teams
    .map((name) => DATA.signatures2022[name]?.[key])
    .filter((value) => Number.isFinite(value));
  return values.reduce((sum, value) => sum + value, 0) / Math.max(1, values.length);
}

function svgEl(name, attrs = {}) {
  const el = document.createElementNS("http://www.w3.org/2000/svg", name);
  Object.entries(attrs).forEach(([key, value]) => el.setAttribute(key, String(value)));
  return el;
}

function clear(el) {
  while (el.firstChild) el.removeChild(el.firstChild);
}

function pitch(svg, width, height) {
  clear(svg);
  svg.appendChild(svgEl("rect", { x: 0, y: 0, width, height, fill: "#1f663b" }));
  svg.appendChild(svgEl("rect", {
    x: 4,
    y: 4,
    width: width - 8,
    height: height - 8,
    fill: "none",
    stroke: "rgba(255,255,255,0.72)",
    "stroke-width": 1.2,
  }));
  svg.appendChild(svgEl("line", {
    x1: width / 2,
    y1: 4,
    x2: width / 2,
    y2: height - 4,
    stroke: "rgba(255,255,255,0.72)",
    "stroke-width": 1.2,
  }));
  svg.appendChild(svgEl("circle", {
    cx: width / 2,
    cy: height / 2,
    r: Math.min(width, height) * 0.11,
    fill: "none",
    stroke: "rgba(255,255,255,0.72)",
    "stroke-width": 1.2,
  }));
  svg.appendChild(svgEl("rect", {
    x: 4,
    y: height * 0.27,
    width: width * 0.14,
    height: height * 0.46,
    fill: "none",
    stroke: "rgba(255,255,255,0.72)",
    "stroke-width": 1.2,
  }));
  svg.appendChild(svgEl("rect", {
    x: width - width * 0.14 - 4,
    y: height * 0.27,
    width: width * 0.14,
    height: height * 0.46,
    fill: "none",
    stroke: "rgba(255,255,255,0.72)",
    "stroke-width": 1.2,
  }));
}

function labelText(text, x, y, attrs = {}) {
  const node = svgEl("text", {
    x,
    y,
    fill: attrs.fill || "currentColor",
    "font-size": attrs.size || 12,
    "font-weight": attrs.weight || 700,
    "text-anchor": attrs.anchor || "start",
  });
  node.textContent = text;
  return node;
}

function textTag(text, x, y, attrs = {}) {
  const group = svgEl("g", {});
  const width = attrs.width || Math.max(48, text.length * 6.8 + 12);
  const height = attrs.height || 20;
  const anchor = attrs.anchor || "start";
  const rectX = anchor === "middle" ? x - width / 2 : x;
  group.appendChild(svgEl("rect", {
    x: rectX,
    y: y - height + 5,
    width,
    height,
    rx: 4,
    fill: attrs.bg || "rgba(5,7,5,0.78)",
    stroke: attrs.stroke || "rgba(255,255,255,0.35)",
    "stroke-width": 0.5,
  }));
  group.appendChild(labelText(text, anchor === "middle" ? x : x + 6, y - 8, {
    fill: attrs.fill || "#ffffff",
    size: attrs.size || 7.5,
    weight: attrs.weight || 800,
    anchor,
  }));
  return group;
}

function flagIcon(svg, code, country, x, y, options = {}) {
  const width = 34;
  const height = 22;
  const ox = options.anchor === "end" ? x - width : x;
  const oy = options.valign === "bottom" ? y - height : y;
  const group = svgEl("g", { class: "style-map-flag" });
  const addRect = (attrs) => group.appendChild(svgEl("rect", attrs));

  addRect({
    x: ox,
    y: oy,
    width,
    height,
    rx: 3,
    fill: "#ffffff",
    stroke: "rgba(13,15,13,0.38)",
    "stroke-width": 0.8,
  });

  if (code === "esp") {
    addRect({ x: ox + 1, y: oy + 1, width: width - 2, height: 5, fill: "#aa151b" });
    addRect({ x: ox + 1, y: oy + 6, width: width - 2, height: 10, fill: "#f1bf00" });
    addRect({ x: ox + 1, y: oy + 16, width: width - 2, height: 5, fill: "#aa151b" });
  } else if (code === "jpn") {
    group.appendChild(svgEl("circle", { cx: ox + width / 2, cy: oy + height / 2, r: 5.4, fill: "#bc002d" }));
  } else if (code === "mar") {
    addRect({ x: ox + 1, y: oy + 1, width: width - 2, height: height - 2, fill: "#c1272d" });
    group.appendChild(svgEl("polygon", {
      points: `${ox + 17},${oy + 6} ${ox + 19},${oy + 13} ${ox + 13},${oy + 9} ${ox + 21},${oy + 9} ${ox + 15},${oy + 13}`,
      fill: "none",
      stroke: "#006233",
      "stroke-width": 1.2,
    }));
  } else if (code === "crc") {
    addRect({ x: ox + 1, y: oy + 1, width: width - 2, height: 4, fill: "#002b7f" });
    addRect({ x: ox + 1, y: oy + 5, width: width - 2, height: 3, fill: "#ffffff" });
    addRect({ x: ox + 1, y: oy + 8, width: width - 2, height: 6, fill: "#ce1126" });
    addRect({ x: ox + 1, y: oy + 14, width: width - 2, height: 3, fill: "#ffffff" });
    addRect({ x: ox + 1, y: oy + 17, width: width - 2, height: 4, fill: "#002b7f" });
  } else if (code === "ksa") {
    addRect({ x: ox + 1, y: oy + 1, width: width - 2, height: height - 2, fill: "#006c35" });
    addRect({ x: ox + 8, y: oy + 10, width: width - 16, height: 1.8, fill: "#ffffff" });
  }

  const title = svgEl("title");
  title.textContent = country;
  group.appendChild(title);
  svg.appendChild(group);
}

function initMetrics() {
  const t = DATA.meta.tournaments;
  const matches = t["2018"].matches + t["2022"].matches;
  const events = t["2018"].eventsWithLocation + t["2022"].eventsWithLocation;
  document.getElementById("metric-matches").textContent = matches;
  document.getElementById("metric-events").textContent = compact(events);
  document.getElementById("metric-teams").textContent = DATA.teams.length;
  document.getElementById("metric-matchups").textContent = DATA.featuredMatchups.length;
}

function initMethod() {
  const tabs = document.getElementById("method-tabs");
  clear(tabs);
  const frames = DATA.finalMethod.frames || DATA.finalMethod.phases;
  const playButton = document.getElementById("method-play");
  const slider = document.getElementById("method-slider");
  slider.max = String(frames.length - 1);
  slider.value = String(state.methodFrame);
  slider.oninput = () => {
    stopMethodPlay();
    state.methodFrame = Number(slider.value);
    initMethod();
  };
  playButton.textContent = methodTimer ? "Pause" : "Play";
  playButton.onclick = () => toggleMethodPlay();

  frames.forEach((frame, index) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = frame.key.replace("-", "-");
    button.className = index === state.methodFrame ? "is-active" : "";
    if (frame.goals && frame.goals.length) {
      button.classList.add("has-goal");
      const ball = document.createElement("span");
      ball.className = "goal-ball";
      ball.setAttribute("aria-hidden", "true");
      button.appendChild(ball);
      button.setAttribute("title", frame.goals.map((goal) => `${goal.minute}' ${goal.player}`).join(", "));
    }
    button.addEventListener("click", () => {
      stopMethodPlay();
      state.methodFrame = index;
      initMethod();
    });
    tabs.appendChild(button);
  });

  const phase = frames[state.methodFrame] || frames[0];
  document.getElementById("method-phase").textContent = phase.label;
  document.getElementById("method-window").textContent = phase.label;

  const readouts = document.getElementById("method-readouts");
  clear(readouts);
  const maxEvents = Math.max(1, ...phase.teams.map((team) => team.nEvents));
  phase.teams.forEach((team) => {
    const card = document.createElement("article");
    card.className = "readout team-readout";
    const eventPct = Math.max(5, (team.nEvents / maxEvents) * 100);
    const pressurePct = Math.max(5, Math.min(100, (team.pressureRate / 0.24) * 100));
    const isFrance = team.team === "France";
    const attackX = isFrance ? 1 - team.meanX : team.meanX;
    const markerX = isFrance ? 1 - attackX : attackX;
    const markerPct = Math.max(4, Math.min(96, markerX * 100));
    const sideClass = isFrance ? "fra" : "arg";
    const axisClass = isFrance ? "attack-left" : "attack-right";
    card.innerHTML = `
      <div class="team-readout-head">
        <strong><i class="side-dot ${sideClass}"></i>${team.team}</strong>
        <span>${team.nEvents} events</span>
      </div>
      <div class="line-pack">
        <div class="attack-axis ${axisClass}" aria-label="Mean attacking position">
          <span class="axis-label own">own goal</span>
          <span class="axis-label attack">attack</span>
        </div>
        <div class="mini-field-line ${axisClass}" aria-label="Mean attacking position">
          <span class="goal-end left"></span>
          <span class="goal-end right"></span>
          <i style="left:${markerPct}%"></i>
        </div>
        <div class="line-metric">
          <span>event volume</span>
          <b><i style="width:${eventPct}%"></i></b>
        </div>
        <div class="line-metric pressure">
          <span>structural pressure</span>
          <b><i style="width:${pressurePct}%"></i></b>
        </div>
      </div>
      <span>attack depth=${fmt(attackX)}, pressure=${fmtPct(team.pressureRate)}</span>
    `;
    readouts.appendChild(card);
  });
  const goals = document.createElement("article");
  goals.className = "readout";
  goals.innerHTML = `
    <strong>Goals</strong>
    <span>${phase.goals.map((goal) => `<span class="goal-chip"><i></i>${goal.minute}' ${esc(goal.player)}</span>`).join(" ") || "No goals in this window"}</span>
  `;
  readouts.appendChild(goals);

  const legend = document.createElement("article");
  legend.className = "readout";
  const starLegend = phase.stars.map((star) => {
      const style = starStyles[star.name] || { fill: "#ffffff" };
      return `<span class="star-chip"><i style="background:${style.fill}"></i>${esc(star.name)} ${star.eventCount}</span>`;
    }).join(" ");
  const participants = (phase.topParticipants || [])
    .slice(0, 4)
    .map((player) => `<span class="participant ${player.isStar ? "is-star" : ""}">${esc(shortName(player.name))} <b>${player.count}</b></span>`)
    .join("");
  legend.innerHTML = `
    <strong>Legend + main participants</strong>
    <span>${starLegend || "No tracked star touches in this window"}</span>
    <div class="participant-list">${participants}</div>
  `;
  readouts.appendChild(legend);

  const svg = document.getElementById("method-pitch");
  pitch(svg, 120, 80);
  phase.events.forEach((event) => {
    const dot = svgEl("circle", {
      cx: event.x * 120,
      cy: event.y * 80,
      r: event.type === "Shot" ? 1.25 : 0.72,
      fill: teamColors[event.team] || "#d7c56a",
      stroke: event.team === "France" ? "rgba(255,255,255,0.45)" : "rgba(13,15,13,0.5)",
      "stroke-width": 0.18,
      opacity: event.type === "Pressure" ? 0.32 : 0.22,
    });
    dot.appendChild(svgEl("title"));
    dot.querySelector("title").textContent = `${event.team} ${event.minute}' ${event.type}`;
    svg.appendChild(dot);
  });

  phase.stars.forEach((star) => {
    const style = starStyles[star.name] || { stroke: "#ffffff", fill: "#ffffff", text: "#ffffff" };
    star.events.forEach((event, index) => {
      svg.appendChild(svgEl("circle", {
        cx: event.x * 120,
        cy: event.y * 80,
        r: event.type === "Shot" ? 2.4 : 1.85,
        fill: style.fill,
        stroke: style.stroke,
        "stroke-width": 0.45,
        opacity: 0.92,
      }));
      const title = svgEl("title");
      title.textContent = `${star.name} ${event.minute}' ${event.type}`;
      svg.lastChild.appendChild(title);
    });
  });

}

function stopMethodPlay() {
  if (methodTimer) {
    clearInterval(methodTimer);
    methodTimer = null;
  }
}

function toggleMethodPlay() {
  if (methodTimer) {
    stopMethodPlay();
    initMethod();
    return;
  }
  const frames = DATA.finalMethod.frames || DATA.finalMethod.phases;
  methodTimer = setInterval(() => {
    state.methodFrame = (state.methodFrame + 1) % frames.length;
    initMethod();
  }, 900);
  initMethod();
}

function initTeamMap() {
  const svg = document.getElementById("team-map");
  clear(svg);
  const teams = DATA.teams.map((team) => DATA.signatures2022[team]);
  const fieldAverage = metricAverage("x");
  const biteAverage = metricAverage("pressureRate");
  const fieldAverageEl = document.getElementById("field-height-avg");
  const biteAverageEl = document.getElementById("bite-avg");
  if (fieldAverageEl) fieldAverageEl.textContent = fmt(fieldAverage);
  if (biteAverageEl) biteAverageEl.textContent = fmtPct(biteAverage, 1);
  const minX = 0.38;
  const maxX = 0.54;
  const minP = 0.035;
  const maxP = 0.115;
  const margin = { left: 58, right: 28, top: 28, bottom: 54 };
  const width = 720;
  const height = 420;
  const plotW = width - margin.left - margin.right;
  const plotH = height - margin.top - margin.bottom;
  const sx = (x) => margin.left + ((x - minX) / (maxX - minX)) * plotW;
  const sy = (p) => margin.top + (1 - (p - minP) / (maxP - minP)) * plotH;
  const splitX = sx(STYLE_SPLITS.territory);
  const splitY = sy(STYLE_SPLITS.pressure);

  svg.appendChild(svgEl("rect", { x: 0, y: 0, width, height, fill: "#fffffa" }));
  [
    { x: margin.left, y: margin.top, w: splitX - margin.left, h: splitY - margin.top, fill: "#eef5e8" },
    { x: splitX, y: margin.top, w: margin.left + plotW - splitX, h: splitY - margin.top, fill: "#e7f1e1" },
    { x: margin.left, y: splitY, w: splitX - margin.left, h: margin.top + plotH - splitY, fill: "#f4f0df" },
    { x: splitX, y: splitY, w: margin.left + plotW - splitX, h: margin.top + plotH - splitY, fill: "#eef2e6" },
  ].forEach((zone) => {
    svg.appendChild(svgEl("rect", {
      x: zone.x,
      y: zone.y,
      width: zone.w,
      height: zone.h,
      fill: zone.fill,
    }));
  });
  svg.appendChild(svgEl("rect", {
    x: margin.left,
    y: margin.top,
    width: plotW,
    height: plotH,
    fill: "none",
    stroke: "rgba(13,15,13,0.18)",
  }));

  svg.appendChild(svgEl("line", {
    x1: splitX,
    y1: margin.top,
    x2: splitX,
    y2: margin.top + plotH,
    stroke: "rgba(13,15,13,0.22)",
    "stroke-dasharray": "5 6",
  }));
  svg.appendChild(svgEl("line", {
    x1: margin.left,
    y1: splitY,
    x2: margin.left + plotW,
    y2: splitY,
    stroke: "rgba(13,15,13,0.22)",
    "stroke-dasharray": "5 6",
  }));

  flagIcon(svg, "mar", "Morocco: counterpunch disruptor", margin.left + 10, margin.top + 10);
  flagIcon(svg, "ksa", "Saudi Arabia: front-foot hunter", margin.left + plotW - 10, margin.top + 10, { anchor: "end" });
  flagIcon(svg, "crc", "Costa Rica: deep absorber", margin.left + 10, margin.top + plotH - 10, { valign: "bottom" });
  flagIcon(svg, "esp", "Spain: territory controller", margin.left + plotW - 10, margin.top + plotH - 10, { anchor: "end", valign: "bottom" });

  teams.forEach((team) => {
    const active = team.team === state.selectedTeam;
    const dot = svgEl("circle", {
      class: "team-dot",
      cx: sx(team.x),
      cy: sy(team.pressureRate),
      r: active ? 8 : 5.5,
      fill: active ? "#0d0f0d" : "#ffffff",
      stroke: "#0d0f0d",
      "stroke-width": active ? 2.5 : 1.4,
    });
    dot.addEventListener("click", () => {
      state.selectedTeam = team.team;
      initTeamMap();
      renderTeamDetail();
    });
    dot.appendChild(svgEl("title"));
    dot.querySelector("title").textContent = `${team.team}: x=${fmt(team.x)}, press=${fmtPct(team.pressureRate)}`;
    svg.appendChild(dot);
  });

  ["Spain", "Germany", "Morocco", "Japan", "Brazil", "Saudi Arabia", "England"].forEach((name) => {
    const team = DATA.signatures2022[name];
    if (!team) return;
    const tx = sx(team.x);
    const ty = sy(team.pressureRate);
    const nearRight = tx > margin.left + plotW - 90;
    const nearTop = ty < margin.top + 34;
    svg.appendChild(labelText(name, tx + (nearRight ? -8 : 8), ty + (nearTop ? 18 : -8), {
      fill: "#0d0f0d",
      size: 12,
      anchor: nearRight ? "end" : "start",
    }));
  });
}

function meter(label, value, max, display, note, average) {
  const pct = Math.max(0, Math.min(100, (value / max) * 100));
  const avgPct = Math.max(0, Math.min(100, (average / max) * 100));
  const averageDisplay = label === "Bite" || label === "Settling play" || label === "Finishing attempts"
    ? fmtPct(average, label === "Finishing attempts" ? 1 : 0)
    : fmt(average);
  return `
    <div class="meter">
      <div class="meter-top"><span>${label}</span><strong>${display}</strong></div>
      <div class="meter-track">
        <div class="meter-fill" style="width:${pct}%"></div>
        <i class="meter-avg" style="left:${avgPct}%"></i>
      </div>
      <div class="meter-note">
        <span>${note}</span>
        <b>avg ${averageDisplay}</b>
      </div>
    </div>
  `;
}

function renderTeamDetail() {
  const detail = document.getElementById("team-detail");
  const team = DATA.signatures2022[state.selectedTeam];
  const archetype = styleArchetype(team);
  const options = DATA.teams
    .map((name) => `<option value="${esc(name)}"${name === state.selectedTeam ? " selected" : ""}>${esc(name)}</option>`)
    .join("");
  detail.innerHTML = `
    <div class="detail-title">
      <div>
        <p class="eyebrow">Selected team</p>
        <h3>${team.team}</h3>
      </div>
      <span class="badge">${archetype.name}</span>
    </div>
    <label class="team-picker">
      <span>Choose team</span>
      <select id="team-select">${options}</select>
    </label>
    <p class="style-read">${archetype.read}</p>
    <div class="meter-list">
      ${meter("Field height", team.x, 0.55, fmt(team.x), "How far up the pitch this team usually lives.", metricAverage("x"))}
      ${meter("Settling play", team.passRate, 0.34, fmtPct(team.passRate), "How much the match runs through passes.", metricAverage("passRate"))}
      ${meter("Bite", team.pressureRate, 0.12, fmtPct(team.pressureRate), "How often events become pressure moments.", metricAverage("pressureRate"))}
      ${meter("Finishing attempts", team.shotRate, 0.012, fmtPct(team.shotRate, 1), "How often located events turn into shots.", metricAverage("shotRate"))}
      ${meter("Fingerprint strength", team.distinctiveness, 0.18, fmt(team.distinctiveness), "How far this team sits from the tournament's average shape.", metricAverage("distinctiveness"))}
    </div>
    <span class="detail-foot">${team.nEvents.toLocaleString()} located events</span>
  `;
  const select = detail.querySelector("#team-select");
  select.addEventListener("change", () => {
    state.selectedTeam = select.value;
    initTeamMap();
    renderTeamDetail();
  });
}

function initAnchors() {
  const turnover = DATA.drift.groups.find((group) => group.status === "turnover") || { status: "turnover", n: 0, meanDrift: 0 };
  const rowByTeam = Object.fromEntries(DATA.drift.teams.map((row) => [row.team, row]));
  const matchByTeam = Object.fromEntries(DATA.opponent.opponents.map((row) => [row.team, row.nMatches]));
  const nTeams = DATA.drift.teams.length;
  const matchCounts = DATA.drift.teams
    .map((row) => matchByTeam[row.team])
    .filter((value) => Number.isFinite(value));
  const minMatches = Math.min(...matchCounts);
  const maxMatches = Math.max(...matchCounts);
  const fmtThree = (value) => fmt(value, 3);

  document.getElementById("anchor-bars").innerHTML = `
    <article>
      <strong>${nTeams}</strong>
      <span>teams seen in both Cups</span>
    </article>
    <article>
      <strong>${minMatches}-${maxMatches}</strong>
      <span>matches per team in 2022</span>
    </article>
    <article>
      <strong>${turnover.n}</strong>
      <span>core-turnover teams</span>
    </article>
  `;

  const croatia = rowByTeam.Croatia;
  const belgium = rowByTeam.Belgium;
  const costaRica = rowByTeam["Costa Rica"];
  document.getElementById("anchor-examples").innerHTML = `Example read: Croatia barely moved (${fmtThree(croatia.drift)}), Belgium moved a lot (${fmtThree(belgium.drift)}), Costa Rica moved most (${fmtThree(costaRica.drift)}). That is a scene-setting cue, not a causal claim.`;
}
function initOpponentMirror() {
  const select = document.getElementById("opponent-select");
  if (!select.options.length) {
    DATA.opponent.opponents
      .slice()
      .sort((a, b) => a.team.localeCompare(b.team))
      .forEach((row) => {
        const option = document.createElement("option");
        option.value = row.team;
        option.textContent = row.team;
        select.appendChild(option);
      });
    select.addEventListener("change", () => {
      state.opponent = select.value;
      renderOpponentMirror();
    });
  }
  select.value = state.opponent;
  renderOpponentMirror();
}

function renderOpponentMirror() {
  const row = DATA.opponent.opponents.find((item) => item.team === state.opponent);
  const byOpponent = (team) => DATA.opponent.opponents.find((item) => item.team === team);
  const byStability = (team) => DATA.opponent.stability.find((item) => item.team === team);
  const costaRica = byOpponent("Costa Rica");
  const spain = byOpponent("Spain");
  const brazil = byOpponent("Brazil");
  const uruguay = byStability("Uruguay");
  const germany = byStability("Germany");
  const axis = document.getElementById("mirror-axis");
  const min = -0.055;
  const max = 0.06;
  const pos = ((row.deltaX - min) / (max - min)) * 100;
  axis.innerHTML = `
    <div style="position:absolute;left:50%;top:18px;bottom:18px;border-left:1px solid rgba(13,15,13,0.32)"></div>
    <div style="position:absolute;left:12px;bottom:14px;color:#5d665e;font-size:0.82rem">pins you back</div>
    <div style="position:absolute;right:12px;bottom:14px;color:#5d665e;font-size:0.82rem">lets you step up</div>
    <div style="position:absolute;left:${pos}%;top:38px;transform:translateX(-50%);width:22px;height:22px;border-radius:50%;background:#0d0f0d;border:3px solid #fff"></div>
    <div style="position:absolute;left:${pos}%;top:68px;transform:translateX(-50%);font-weight:800">${fmt(row.deltaX, 3)}</div>
  `;

  const card = document.getElementById("mirror-card");
  const sentence = row.deltaX < -0.015
    ? `${row.team} tends to push opponents into lower field position.`
    : row.deltaX > 0.015
      ? `${row.team} tends to allow opponents to play higher upfield.`
      : `${row.team} sits near the neutral zone in this read.`;
  card.innerHTML = `
    <div class="mirror-selected">
      <h3>${row.team}: ${row.label}</h3>
      <p>${sentence} Read from ${row.nMatches} matches in the 2022 World Cup.</p>
    </div>
    <div class="mirror-story-grid">
      <article>
        <strong>Costa Rica</strong>
        <span>+${fmt(costaRica.deltaX, 3)}</span>
        <p>Everyone steps onto them. A deep block makes the opponent look braver.</p>
      </article>
      <article>
        <strong>Spain / Brazil</strong>
        <span>${fmt(spain.deltaX, 3)} / ${fmt(brazil.deltaX, 3)}</span>
        <p>Possession pressure moves the other team backward.</p>
      </article>
      <article>
        <strong>Uruguay</strong>
        <span>SD=${fmt(uruguay.sdX, 4)}</span>
        <p>Almost no opponent dependence. One field position, whoever the opponent is.</p>
      </article>
      <article>
        <strong>Germany</strong>
        <span>SD=${fmt(germany.sdX, 3)}</span>
        <p>The most matchup-sensitive read here: different opponent, different field shape.</p>
      </article>
    </div>
  `;
}

function coreVector(team) {
  const sig = DATA.signatures2022[team];
  return [sig.x, sig.y, sig.distGoal, sig.passRate, sig.shotRate, sig.pressureRate];
}

function vecDistance(a, b) {
  return Math.sqrt(a.reduce((sum, value, i) => sum + (value - b[i]) ** 2, 0));
}

function driftByTeam() {
  return Object.fromEntries(DATA.drift.teams.map((row) => [row.team, row]));
}

function stabilityByTeam() {
  return Object.fromEntries(DATA.opponent.stability.map((row) => [row.team, row]));
}

function confidenceFor(teamA, teamB) {
  const drifts = driftByTeam();
  const stabilities = stabilityByTeam();
  let score = 0;
  const reasons = [];
  [teamA, teamB].forEach((team) => {
    const sig = DATA.signatures2022[team];
    if (sig.nEvents >= 6000) score += 1;
    if (drifts[team]) {
      score += 1;
      if (drifts[team].drift <= 0.06) {
        score += 1;
        reasons.push(`${team} has low 2018-2022 drift`);
      } else if (drifts[team].drift > 0.09) {
        reasons.push(`${team} is volatile across 2018-2022`);
      }
    } else {
      reasons.push(`${team} lacks a 2018 comparison`);
    }
    if (stabilities[team] && stabilities[team].sdX <= 0.035) {
      score += 1;
      reasons.push(`${team} is less opponent-dependent`);
    }
  });
  if (score >= 7) return { label: "High", score, reasons: reasons.slice(0, 3) };
  if (score >= 4) return { label: "Medium", score, reasons: reasons.slice(0, 3) };
  return { label: "Low", score, reasons: reasons.slice(0, 3) };
}

function matchupRead(teamA, teamB) {
  const a = DATA.signatures2022[teamA];
  const b = DATA.signatures2022[teamB];
  const d = vecDistance(coreVector(teamA), coreVector(teamB));
  const xDiff = a.x - b.x;
  const pressDiff = a.pressureRate - b.pressureRate;
  const passDiff = a.passRate - b.passRate;
  const style = d >= 0.10 ? "style clash" : d <= 0.04 ? "style mirror" : "moderate contrast";
  return { a, b, d, xDiff, pressDiff, passDiff, style, confidence: confidenceFor(teamA, teamB) };
}

function edgeSentence(diff, teamA, teamB, metric, strong, unit = "") {
  if (Math.abs(diff) < strong / 3) return `${metric}: close to even`;
  const leader = diff > 0 ? teamA : teamB;
  const level = Math.abs(diff) >= strong ? "clear" : "slight";
  const value = unit === "pt" ? `${Math.abs(diff * 100).toFixed(1)} pts` : fmt(Math.abs(diff), 3);
  return `${metric}: ${leader} has a ${level} edge (${value})`;
}

function initMatchups() {
  const selectA = document.getElementById("team-a");
  const selectB = document.getElementById("team-b");
  [selectA, selectB].forEach((select) => {
    if (select.options.length) return;
    DATA.teams.forEach((team) => {
      const option = document.createElement("option");
      option.value = team;
      option.textContent = team;
      select.appendChild(option);
    });
    select.addEventListener("change", () => {
      state.teamA = selectA.value;
      state.teamB = selectB.value;
      renderMatchup();
    });
  });
  selectA.value = state.teamA;
  selectB.value = state.teamB;

  const featured = document.getElementById("featured-matchups");
  clear(featured);
  DATA.featuredMatchups.forEach((match) => {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = `${match.teamA} vs ${match.teamB}`;
    button.className = match.teamA === state.teamA && match.teamB === state.teamB ? "is-active" : "";
    button.addEventListener("click", () => {
      state.teamA = match.teamA;
      state.teamB = match.teamB;
      selectA.value = state.teamA;
      selectB.value = state.teamB;
      initMatchups();
    });
    featured.appendChild(button);
  });
  renderMatchup();
}

function renderMatchup() {
  if (state.teamA === state.teamB) {
    state.teamB = DATA.teams.find((team) => team !== state.teamA) || state.teamB;
    document.getElementById("team-b").value = state.teamB;
  }
  const read = matchupRead(state.teamA, state.teamB);
  document.getElementById("matchup-title").textContent = `${state.teamA} vs ${state.teamB}`;
  const badge = document.getElementById("matchup-confidence");
  badge.textContent = `${read.confidence.label} read`;
  badge.className = `badge ${read.confidence.label.toLowerCase()}`;

  document.getElementById("matchup-score").innerHTML = `
    <div class="score-pill"><strong>${fmt(read.d, 3)}</strong><span>style distance</span></div>
    <div class="score-pill"><strong>${read.style}</strong><span>overall relation</span></div>
    <div class="score-pill"><strong>${read.confidence.score}/8</strong><span>read strength</span></div>
  `;

  const reasons = read.confidence.reasons.length
    ? read.confidence.reasons.join("; ")
    : "Both teams have adequate 2022 event samples.";
  document.getElementById("matchup-grid").innerHTML = `
    <article class="match-card">
      <strong>${edgeSentence(read.xDiff, state.teamA, state.teamB, "Territory", 0.04)}</strong>
      <span>Higher x-position means events occur farther upfield.</span>
    </article>
    <article class="match-card">
      <strong>${edgeSentence(read.pressDiff, state.teamA, state.teamB, "Press", 0.03, "pt")}</strong>
      <span>Pressure share is pressure events divided by located events.</span>
    </article>
    <article class="match-card">
      <strong>${edgeSentence(read.passDiff, state.teamA, state.teamB, "Pass/control", 0.03, "pt")}</strong>
      <span>Pass share is not possession, but it tracks event texture.</span>
    </article>
    <article class="match-card">
      <strong>Read notes</strong>
      <span>${reasons}</span>
    </article>
  `;
  renderDuelSvg(read);
}

function renderDuelSvg(read) {
  const svg = document.getElementById("duel-svg");
  pitch(svg, 720, 180);
  const mapX = (x) => 24 + x * (720 - 48);
  const yA = 66;
  const yB = 112;
  const xa = mapX(read.a.x);
  const xb = mapX(read.b.x);
  svg.appendChild(svgEl("line", { x1: xa, y1: yA, x2: xb, y2: yB, stroke: "#ffffff", "stroke-width": 1.2, opacity: 0.7 }));
  [
    { team: read.a.team, x: xa, y: yA, fill: "#ffffff", stroke: "#0d0f0d", sig: read.a },
    { team: read.b.team, x: xb, y: yB, fill: "#0d0f0d", stroke: "#ffffff", sig: read.b },
  ].forEach((item) => {
    svg.appendChild(svgEl("circle", {
      cx: item.x,
      cy: item.y,
      r: 12,
      fill: item.fill,
      stroke: item.stroke,
      "stroke-width": 2,
    }));
    svg.appendChild(labelText(item.team, item.x, item.y - 20, { fill: "#ffffff", anchor: "middle", size: 13 }));
    svg.appendChild(labelText(`press ${fmtPct(item.sig.pressureRate)}`, item.x, item.y + 32, { fill: "#ffffff", anchor: "middle", size: 11 }));
  });
  svg.appendChild(labelText("lower field position", 22, 166, { fill: "#ffffff", size: 11 }));
  svg.appendChild(labelText("higher field position", 578, 166, { fill: "#ffffff", size: 11 }));
}

function boot() {
  if (!DATA) {
    document.body.innerHTML = "<main class='section'><h1>Football data failed to load.</h1></main>";
    return;
  }
  initMetrics();
  initMethod();
  initTeamMap();
  renderTeamDetail();
  initAnchors();
  initOpponentMirror();
  initMatchups();
}

boot();

