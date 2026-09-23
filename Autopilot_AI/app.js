/* ==============================
   AutoPilot AI – JavaScript Core
   ============================== */

// ─── State ───────────────────────────────────────────────
const STATE = {
  engine: false,
  locked: true,
  lights: false,
  climate: false,
  gpsActive: false,
  tripRunning: false,
  speed: 0,
  currentSpeed: 0,
  tripKm: 0,
  tripStartTime: null,
  tripMaxSpeed: 0,
  tripSpeeds: [],
  harshEvents: 0,
  harshBrakes: 0,
  lastAccel: { x: 0, y: 0, z: 0 },
  voice: null,
  ws: null,         // WebSocket to ESP32
  watchId: null,
  lastPos: null,
};

// ─── Settings ────────────────────────────────────────────
let SETTINGS = {
  brand: 'BMW', model: '320d', year: 2018,
  tankSize: 60,
  declaredCons: 6.0,
  realCons: 7.2,
  fuelLevel: 50,        // %
  fuelPrice: 7.25,
  voiceAlerts: true,
  speedAlerts: true,
  speedLimit: 130,
  espIP: '', espPort: 81,
};

// ─── Eco Tips ────────────────────────────────────────────
const ECO_TIPS = [
  '🔵 Diesel-urile BMW/Mercedes consumă optim la 1500-2000 RPM — evită supraregimul!',
  '🟢 Anticipează traficul și lasă mașina să decelereze singură — economiești 15-20% combustibil',
  '🟡 Pneuri umflate la presiunea corectă reduc consumul cu până la 3%',
  '🔵 Filtrul de particule diesel (DPF) funcționează optim la curse lungi de autostradă',
  '🟢 Climatizarea consumă 0.5-1.5L/100km — folosește ventilația când e posibil',
  '🟡 Oprire motor la semafoare lungi (>30s) economisește 0.1-0.3L/h',
  '🔵 Viteza optimă pentru diesel pe drum național: 80-90 km/h',
  '🟢 Pornire blândă la rece — nu accelera agresiv în primele 2-3 minute',
  '🟡 Schimbă uleiul la timp — motor curat consumă cu 5% mai puțin',
  '🔵 Aer condiționat pe autostradă vs geamuri deschise la viteză — AC e mai eficient peste 80 km/h',
];

// ─── Destinations for range check ────────────────────────
const DESTINATIONS = [
  { name: 'București', km: 220 },
  { name: 'Cluj', km: 450 },
  { name: 'Constanța', km: 280 },
  { name: 'Brașov', km: 166 },
];

// ═══════════════════════════════════════════════
// INIT
// ═══════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', () => {
  loadSettings();
  updateFuelDisplay();
  initParticles();
  updateDateTime();
  setInterval(updateDateTime, 1000);
  updateHUDTime();
  setInterval(updateHUDTime, 1000);
  renderTips();
  updateRangeCard();
  updateKPIs();
  renderMaintenance();
  updateLockScreen();
  updateGreeting();
  detectGPS();     // request permission early
  initAccelerometer();
  renderRemoteCar();
  setInterval(updateDateTime, 1000);
});

// ═══════════════════════════════════════════════
// PARTICLES
// ═══════════════════════════════════════════════
function initParticles() {
  const canvas = document.getElementById('particleCanvas');
  const ctx = canvas.getContext('2d');
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;

  const particles = Array.from({ length: 60 }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    r: Math.random() * 1.5 + 0.5,
    dx: (Math.random() - 0.5) * 0.3,
    dy: (Math.random() - 0.5) * 0.3,
    opacity: Math.random() * 0.5 + 0.1,
  }));

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles.forEach(p => {
      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(0,212,255,${p.opacity})`;
      ctx.fill();
      p.x += p.dx; p.y += p.dy;
      if (p.x < 0 || p.x > canvas.width) p.dx *= -1;
      if (p.y < 0 || p.y > canvas.height) p.dy *= -1;
    });
    requestAnimationFrame(draw);
  }
  draw();

  window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  });
}

// ═══════════════════════════════════════════════
// LOCK SCREEN
// ═══════════════════════════════════════════════
function unlockApp() {
  document.getElementById('screenLock').classList.remove('active');
  document.getElementById('screenDash').classList.add('active');
  showTab('tabDash', document.getElementById('navDash'));
}

function updateLockScreen() {
  const s = SETTINGS;
  document.getElementById('carBrandBadge').textContent = s.brand.toUpperCase();
  document.getElementById('carModelText').textContent =
    s.model ? `${s.model} ${s.year}` : 'Configurează în Setări';
  const range = calcRange();
  document.getElementById('lockRangeStatus').innerHTML =
    `<span>⛽</span> ${range > 0 ? range + ' km' : '-- km'}`;
  document.getElementById('lockEngineStatus').innerHTML =
    STATE.engine ? '<span>⚡</span> Motor Pornit' : '<span>⚡</span> Motor Oprit';
  document.getElementById('lockEngineStatus').classList.toggle('active', STATE.engine);
}

// ═══════════════════════════════════════════════
// SETTINGS
// ═══════════════════════════════════════════════
function loadSettings() {
  const saved = localStorage.getItem('autopilot_settings');
  if (saved) {
    try { SETTINGS = { ...SETTINGS, ...JSON.parse(saved) }; } catch(e) {}
  }
  // Populate form
  document.getElementById('sBrand').value = SETTINGS.brand;
  document.getElementById('sModel').value = SETTINGS.model;
  document.getElementById('sYear').value = SETTINGS.year;
  document.getElementById('sTankSize').value = SETTINGS.tankSize;
  document.getElementById('sDeclaredCons').value = SETTINGS.declaredCons;
  document.getElementById('sRealCons').value = SETTINGS.realCons;
  document.getElementById('sFuelLevel').value = SETTINGS.fuelLevel;
  document.getElementById('sFuelPrice').value = SETTINGS.fuelPrice;
  document.getElementById('sVoiceAlerts').checked = SETTINGS.voiceAlerts;
  document.getElementById('sSpeedAlerts').checked = SETTINGS.speedAlerts;
  document.getElementById('sSpeedLimit').value = SETTINGS.speedLimit;
  document.getElementById('sEspIP').value = SETTINGS.espIP;
  document.getElementById('sEspPort').value = SETTINGS.espPort;
  document.getElementById('sFuelLevelDisplay').textContent = SETTINGS.fuelLevel + '%';
  updateCarBadge();
}

function saveSettings() {
  SETTINGS.brand = document.getElementById('sBrand').value;
  SETTINGS.model = document.getElementById('sModel').value;
  SETTINGS.year = parseInt(document.getElementById('sYear').value) || 2018;
  SETTINGS.tankSize = parseFloat(document.getElementById('sTankSize').value) || 60;
  SETTINGS.declaredCons = parseFloat(document.getElementById('sDeclaredCons').value) || 6.0;
  SETTINGS.realCons = parseFloat(document.getElementById('sRealCons').value) || 7.2;
  SETTINGS.fuelLevel = parseInt(document.getElementById('sFuelLevel').value) || 50;
  SETTINGS.fuelPrice = parseFloat(document.getElementById('sFuelPrice').value) || 7.25;
  SETTINGS.voiceAlerts = document.getElementById('sVoiceAlerts').checked;
  SETTINGS.speedAlerts = document.getElementById('sSpeedAlerts').checked;
  SETTINGS.speedLimit = parseInt(document.getElementById('sSpeedLimit').value) || 130;
  SETTINGS.espIP = document.getElementById('sEspIP').value;
  SETTINGS.espPort = parseInt(document.getElementById('sEspPort').value) || 81;
  SETTINGS.fuelLevel = parseInt(document.getElementById('sFuelLevel').value);
  document.getElementById('sFuelLevelDisplay').textContent = SETTINGS.fuelLevel + '%';

  localStorage.setItem('autopilot_settings', JSON.stringify(SETTINGS));
  updateCarBadge();
  updateRangeCard();
  updateKPIs();
  updateLockScreen();
  renderTips();
}

function updateFuelDisplay() {
  const lvl = parseInt(document.getElementById('sFuelLevel')?.value || SETTINGS.fuelLevel);
  const el = document.getElementById('sFuelLevelDisplay');
  if (el) el.textContent = lvl + '%';
}

function updateCarBadge() {
  const s = SETTINGS;
  document.getElementById('carBrandBadge').textContent = s.brand.toUpperCase();
  document.getElementById('carModelText').textContent =
    s.model ? `${s.model} ${s.year || ''}` : 'Configurează în Setări';
}

// ═══════════════════════════════════════════════
// TAB NAVIGATION
// ═══════════════════════════════════════════════
function showTab(tabId, navBtn) {
  document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  document.getElementById(tabId).classList.add('active');
  if (navBtn) navBtn.classList.add('active');

  if (tabId === 'tabHUD') startHUDMode();
  if (tabId === 'tabDash') updateRangeCard();
}

// ═══════════════════════════════════════════════
// RANGE / AUTONOMIE
// ═══════════════════════════════════════════════
function calcRange() {
  const fuelLiters = (SETTINGS.fuelLevel / 100) * SETTINGS.tankSize;
  const cons = SETTINGS.realCons || 7.2;
  return Math.round((fuelLiters / cons) * 100);
}

function updateRangeCard() {
  const range = calcRange();
  const fuelLiters = Math.round((SETTINGS.fuelLevel / 100) * SETTINGS.tankSize);
  const cost = Math.round(fuelLiters * SETTINGS.fuelPrice);
  const hoursToEmpty = SETTINGS.realCons > 0
    ? Math.round((fuelLiters / (SETTINGS.realCons * 90 / 100)) * 10) / 10
    : 0;  // at avg 90 km/h

  // Gauge
  const bar = document.getElementById('fuelLevelBar');
  if (bar) bar.style.height = SETTINGS.fuelLevel + '%';

  // Big range
  const bigVal = document.getElementById('rangeBigVal');
  if (bigVal) bigVal.textContent = range > 0 ? range + ' km' : '--- km';

  // Info items
  setText('tankDisplay', fuelLiters + ' L');
  setText('avgConsDisplay', SETTINGS.realCons + ' L/100');
  setText('costRemainingDisplay', cost + ' RON');
  setText('timeToEmptyDisplay', hoursToEmpty + ' ore');
  setText('kpiRangeVal', range > 0 ? range : '--');

  // Destinations
  const destPills = document.getElementById('destPills');
  if (destPills) {
    destPills.innerHTML = '';
    DESTINATIONS.forEach(d => {
      const can = range >= d.km;
      const pill = document.createElement('div');
      pill.className = `dest-pill ${can ? 'can' : 'cannot'}`;
      pill.innerHTML = `${can ? '✅' : '❌'} ${d.name} (${d.km}km)`;
      destPills.appendChild(pill);
    });
  }

  // Lock screen update
  const lockRange = document.getElementById('lockRangeStatus');
  if (lockRange) lockRange.innerHTML = `<span>⛽</span> ${range > 0 ? range + ' km' : '-- km'}`;
}

// ═══════════════════════════════════════════════
// KPIs
// ═══════════════════════════════════════════════
function updateKPIs() {
  const ecoScore = calcEcoScore();
  setText('kpiEcoVal', ecoScore);
  setText('kpiConsumptionVal', SETTINGS.realCons);
  setText('hudEcoVal', ecoScore);
  setText('hudRangeVal', calcRange());
}

function calcEcoScore() {
  const cons = SETTINGS.realCons;
  const declared = SETTINGS.declaredCons;
  if (!cons || !declared) return '--';
  const ratio = declared / cons;
  let score = Math.round(ratio * 70 + 30);
  score -= STATE.harshEvents * 5;
  score -= STATE.harshBrakes * 5;
  return Math.max(0, Math.min(100, score));
}

// ═══════════════════════════════════════════════
// ENGINE TOGGLE (Simulated)
// ═══════════════════════════════════════════════
function toggleEngine() {
  STATE.engine = !STATE.engine;
  updateEngineUI();

  if (STATE.ws && STATE.ws.readyState === WebSocket.OPEN) {
    STATE.ws.send(JSON.stringify({ cmd: STATE.engine ? 'engine_on' : 'engine_off' }));
    toast(`📡 Comandă trimisă la ESP32: motor ${STATE.engine ? 'PORNIT' : 'OPRIT'}`);
  } else {
    toast(STATE.engine ? '⚡ Motor pornit (simulat)' : '🔴 Motor oprit (simulat)');
  }
  updateLockScreen();
}

function updateEngineUI() {
  const on = STATE.engine;
  // Dashboard
  const status = document.getElementById('engineStatusText');
  const pulse = document.getElementById('enginePulse');
  const btn = document.getElementById('engineToggleBtn');
  const btnTxt = document.getElementById('engineBtnText');
  if (status) { status.textContent = on ? 'PORNIT' : 'OPRIT'; status.classList.toggle('running', on); }
  if (pulse) pulse.classList.toggle('running', on);
  if (btn) btn.classList.toggle('running', on);
  if (btnTxt) btnTxt.textContent = on ? 'OPREȘTE' : 'PORNEȘTE';

  // Remote tab
  const rsbIcon = document.getElementById('rsbIcon');
  const rsbText = document.getElementById('rsbText');
  const rsBtn = document.getElementById('remoteStartBtn');
  const carStatusText = document.getElementById('carStatusText');
  if (rsbIcon) rsbIcon.textContent = on ? '■' : '▶';
  if (rsbText) rsbText.innerHTML = on ? 'OPREȘTE<br>MOTORUL' : 'PORNEȘTE<br>MOTORUL';
  if (rsBtn) rsBtn.classList.toggle('engine-on', on);
  if (carStatusText) carStatusText.textContent = on ? '⚡ MOTOR PORNIT' : '⚡ MOTOR OPRIT';

  // Headlights glow on car svg
  const glow = document.getElementById('engineGlow');
  if (glow) glow.style.opacity = on ? '0.4' : '0';
  const hl = document.querySelectorAll('.headlight');
  hl.forEach(h => h.style.opacity = on ? '0.9' : '0.1');
  const tl = document.querySelectorAll('#taillightL, #taillightR');
  tl.forEach(t => t.style.opacity = on ? '0.8' : '0.3');
}

function remoteEngine() {
  toggleEngine();
  // Try ESP32 WebSocket
  if (SETTINGS.espIP) {
    connectESP32();
  }
}

// ─── Remote Controls ─────────────────────────────────────
function remoteLock() {
  STATE.locked = !STATE.locked;
  const icon = document.getElementById('lockIcon');
  const label = document.getElementById('lockLabel');
  if (icon) icon.textContent = STATE.locked ? '🔒' : '🔓';
  if (label) label.textContent = STATE.locked ? 'Blochează' : 'Deblochează';
  toast(STATE.locked ? '🔒 Mașina blocată' : '🔓 Mașina deblocată');
  sendESP32({ cmd: STATE.locked ? 'lock' : 'unlock' });
}

function remoteHonk() {
  toast('📢 Claxon activat!');
  sendESP32({ cmd: 'honk' });
  // Simulate honk animation
  const btn = event.currentTarget;
  btn.style.transform = 'scale(0.9)';
  setTimeout(() => btn.style.transform = '', 200);
}

function remoteClimate() {
  STATE.climate = !STATE.climate;
  const icon = document.getElementById('climateIcon');
  icon.textContent = STATE.climate ? '🔥' : '❄️';
  toast(STATE.climate ? '🔥 Climatizare încălzire pornită' : '❄️ Climatizare AC pornită');
  sendESP32({ cmd: 'climate', value: STATE.climate ? 'heat' : 'cool' });
}

function remoteLights() {
  STATE.lights = !STATE.lights;
  const icon = document.getElementById('lightsIcon');
  const label = document.getElementById('lightsLabel');
  icon.textContent = STATE.lights ? '🔆' : '💡';
  label.textContent = STATE.lights ? 'Faruri ON' : 'Faruri';
  toast(STATE.lights ? '💡 Faruri pornite' : '💡 Faruri oprite');
  sendESP32({ cmd: 'lights', value: STATE.lights });
  const hl = document.querySelectorAll('.headlight');
  hl.forEach(h => h.style.opacity = STATE.lights ? '1' : '0.1');
}

function renderRemoteCar() {
  updateEngineUI();
}

// ─── ESP32 WebSocket ──────────────────────────────────────
function connectESP32() {
  if (!SETTINGS.espIP) return;
  const url = `ws://${SETTINGS.espIP}:${SETTINGS.espPort || 81}`;
  try {
    STATE.ws = new WebSocket(url);
    STATE.ws.onopen = () => {
      document.getElementById('connDot').classList.add('connected');
      document.getElementById('connStatus').textContent = 'Conectat la ESP32';
      toast('🔌 Conectat la mașina ta!');
    };
    STATE.ws.onclose = () => {
      document.getElementById('connDot').classList.remove('connected');
      document.getElementById('connStatus').textContent = 'Deconectat';
    };
    STATE.ws.onerror = () => {
      toast('⚠️ Nu s-a putut conecta la ESP32. Verifică IP-ul în Setări.');
    };
    STATE.ws.onmessage = (e) => {
      try {
        const data = JSON.parse(e.data);
        if (data.engine !== undefined) {
          STATE.engine = data.engine;
          updateEngineUI();
        }
      } catch(err) {}
    };
  } catch(e) {
    toast('⚠️ Adresă ESP32 invalidă');
  }
}

function sendESP32(cmd) {
  if (STATE.ws && STATE.ws.readyState === WebSocket.OPEN) {
    STATE.ws.send(JSON.stringify(cmd));
  }
}

function testESPConnection() {
  SETTINGS.espIP = document.getElementById('sEspIP').value;
  SETTINGS.espPort = parseInt(document.getElementById('sEspPort').value) || 81;
  if (!SETTINGS.espIP) { toast('⚠️ Introdu IP-ul ESP32 mai întâi'); return; }
  toast('🔌 Încerc să mă conectez...');
  connectESP32();
}

// ═══════════════════════════════════════════════
// GPS & HUD
// ═══════════════════════════════════════════════
function startGPS() {
  if (!navigator.geolocation) { toast('❌ GPS indisponibil pe acest device'); return; }

  toast('📍 Activez GPS...');
  const btn = document.getElementById('hudGpsBtn');

  STATE.watchId = navigator.geolocation.watchPosition(
    pos => {
      const spd = pos.coords.speed;
      STATE.speed = spd != null ? Math.round(spd * 3.6) : STATE.speed; // m/s to km/h
      updateSpeedDisplay();

      if (STATE.tripRunning) {
        if (STATE.lastPos) {
          const dist = getDistance(STATE.lastPos, pos.coords);
          STATE.tripKm += dist;
          setText('tripKmVal', STATE.tripKm.toFixed(1));
          setText('hudTripVal', STATE.tripKm.toFixed(1));
          STATE.tripSpeeds.push(STATE.speed);
          if (STATE.speed > STATE.tripMaxSpeed) {
            STATE.tripMaxSpeed = STATE.speed;
            setText('tripMaxSpeedVal', STATE.tripMaxSpeed);
          }
          updateTripStats();
        }
        STATE.lastPos = pos.coords;
      }

      if (btn) { btn.textContent = '📍 GPS Activ'; btn.classList.add('active'); }
      STATE.gpsActive = true;
      document.getElementById('lockGpsStatus').classList.add('active');
    },
    err => { toast('❌ Nu am putut accesa GPS-ul'); },
    { enableHighAccuracy: true, maximumAge: 1000, timeout: 5000 }
  );
}

function detectGPS() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(() => {}, () => {});
  }
}

function updateSpeedDisplay() {
  const spd = STATE.speed;
  setText('kpiSpeedVal', spd);
  setText('hudSpeedVal', spd);

  // Speed arc (max display 200 km/h)
  const arc = document.getElementById('hudSpeedArc');
  if (arc) {
    const pct = Math.min(spd / 200, 1);
    const total = 553;
    arc.style.strokeDashoffset = total - (total * pct);
  }

  // Speed alert
  if (SETTINGS.speedAlerts && spd > SETTINGS.speedLimit) {
    showHUDAlert(`⚠️ VITEZĂ: ${spd} km/h — Limita: ${SETTINGS.speedLimit} km/h`);
    if (SETTINGS.voiceAlerts) speak(`Atenție! Viteza ta este ${spd} kilometri pe oră`);
  } else {
    hideHUDAlert();
  }
}

function getDistance(c1, c2) {
  const R = 6371;
  const dLat = (c2.latitude - c1.latitude) * Math.PI / 180;
  const dLon = (c2.longitude - c1.longitude) * Math.PI / 180;
  const a = Math.sin(dLat/2)**2 + Math.cos(c1.latitude*Math.PI/180) * Math.cos(c2.latitude*Math.PI/180) * Math.sin(dLon/2)**2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}

// ─── HUD Mode ─────────────────────────────────────────────
function startHUDMode() {
  updateHUDTime();
  updateKPIs();
}

function updateHUDTime() {
  const el = document.getElementById('hudTime');
  if (el) el.textContent = new Date().toLocaleTimeString('ro-RO', { hour: '2-digit', minute: '2-digit' });
}

function showHUDAlert(msg) {
  const el = document.getElementById('hudAlert');
  const txt = document.getElementById('hudAlertText');
  if (el && txt) { txt.textContent = msg; el.style.display = 'block'; }
}
function hideHUDAlert() {
  const el = document.getElementById('hudAlert');
  if (el) el.style.display = 'none';
}

function toggleHUDFullscreen() {
  if (!document.fullscreenElement) {
    document.getElementById('hudContainer').requestFullscreen?.();
  } else {
    document.exitFullscreen?.();
  }
}

// ═══════════════════════════════════════════════
// ACCELEROMETER (Detect harsh events)
// ═══════════════════════════════════════════════
function initAccelerometer() {
  if (!window.DeviceMotionEvent) return;

  if (typeof DeviceMotionEvent.requestPermission === 'function') {
    // iOS 13+ – permission needed
  } else {
    window.addEventListener('devicemotion', handleMotion);
  }
}

function handleMotion(e) {
  const a = e.acceleration;
  if (!a) return;

  const HARSH_ACCEL = 3.0;   // m/s²
  const HARSH_BRAKE = -4.0;

  const now = Date.now();
  const last = STATE._lastMotionTime || 0;
  if (now - last < 500) return;   // debounce
  STATE._lastMotionTime = now;

  const ax = a.x || 0, ay = a.y || 0;

  if (ay > HARSH_ACCEL) {
    STATE.harshEvents++;
    logTripEvent('⚡', 'Accelerare bruscă detectată', 'warn');
    if (SETTINGS.voiceAlerts) speak('Accelerează mai lin pentru a economisi motorină');
    updateBehaviorBars();
  } else if (ay < HARSH_BRAKE) {
    STATE.harshBrakes++;
    logTripEvent('🛑', 'Frânare bruscă detectată', 'warn');
    if (SETTINGS.voiceAlerts) speak('Frânează mai blând');
    updateBehaviorBars();
  }

  const accText = document.getElementById('hudAccStatus');
  if (accText) accText.textContent = `📳 ${ax.toFixed(1)}, ${ay.toFixed(1)} m/s²`;
}

function updateBehaviorBars() {
  const totalEvents = STATE.tripSpeeds.length || 1;
  const smoothPct = Math.max(0, 100 - (STATE.harshEvents / totalEvents) * 100 * 5);
  const brakePct = Math.max(0, 100 - (STATE.harshBrakes / totalEvents) * 100 * 5);
  const speedPct = STATE.tripSpeeds.length > 0
    ? STATE.tripSpeeds.filter(s => s >= 70 && s <= 110).length / STATE.tripSpeeds.length * 100
    : 100;

  setWidth('behSmooth', smoothPct);
  setWidth('behBraking', brakePct);
  setWidth('behSpeed', speedPct);
  setText('behSmoothPct', Math.round(smoothPct) + '%');
  setText('behBrakingPct', Math.round(brakePct) + '%');
  setText('behSpeedPct', Math.round(speedPct) + '%');

  const score = calcEcoScore();
  setText('tripEcoVal', score);
  setText('hudEcoVal', score);
  setText('kpiEcoVal', score);
}

// ═══════════════════════════════════════════════
// TRIP
// ═══════════════════════════════════════════════
function toggleTrip() {
  STATE.tripRunning = !STATE.tripRunning;
  const btn = document.getElementById('tripStartBtn');
  const icon = document.getElementById('tripBtnIcon');
  const text = document.getElementById('tripBtnText');

  if (STATE.tripRunning) {
    STATE.tripStartTime = Date.now();
    STATE.lastPos = null;
    STATE.tripSpeeds = [];
    STATE.harshEvents = 0;
    STATE.harshBrakes = 0;
    if (icon) icon.textContent = '⏹️';
    if (text) text.textContent = 'Stop Trip';
    logTripEvent('🚀', 'Trip pornit', 'info');
    if (!STATE.gpsActive) startGPS();
    startTripTimer();
  } else {
    if (icon) icon.textContent = '▶️';
    if (text) text.textContent = 'Start Trip';
    logTripEvent('🏁', `Trip finalizat — ${STATE.tripKm.toFixed(1)} km`, 'info');
    toast(`🏁 Trip salvat: ${STATE.tripKm.toFixed(1)} km`);
  }
}

let tripTimerInt = null;
function startTripTimer() {
  clearInterval(tripTimerInt);
  tripTimerInt = setInterval(() => {
    if (!STATE.tripRunning) { clearInterval(tripTimerInt); return; }
    const elapsed = Math.floor((Date.now() - STATE.tripStartTime) / 1000);
    const m = Math.floor(elapsed / 60).toString().padStart(2, '0');
    const s = (elapsed % 60).toString().padStart(2, '0');
    setText('tripTimeVal', `${m}:${s}`);
  }, 1000);
}

function updateTripStats() {
  const speeds = STATE.tripSpeeds;
  if (speeds.length > 0) {
    const avg = Math.round(speeds.reduce((a, b) => a + b, 0) / speeds.length);
    setText('tripAvgSpeedVal', avg);
  }
  updateBehaviorBars();
}

function clearTrip() {
  STATE.tripRunning = false;
  STATE.tripKm = 0;
  STATE.tripStartTime = null;
  STATE.tripMaxSpeed = 0;
  STATE.tripSpeeds = [];
  STATE.harshEvents = 0;
  STATE.harshBrakes = 0;
  setText('tripKmVal', '0.0');
  setText('tripTimeVal', '00:00');
  setText('tripAvgSpeedVal', '0');
  setText('tripMaxSpeedVal', '0');
  setText('tripEcoVal', '--');
  document.getElementById('eventsList').innerHTML =
    '<div class="event-empty">Pornește un trip pentru a înregistra evenimente</div>';
  document.getElementById('tripBtnIcon').textContent = '▶️';
  document.getElementById('tripBtnText').textContent = 'Start Trip';
  updateBehaviorBars();
  toast('🗑️ Trip resetat');
}

function logTripEvent(icon, text, type) {
  const list = document.getElementById('eventsList');
  const empty = list.querySelector('.event-empty');
  if (empty) empty.remove();

  const now = new Date().toLocaleTimeString('ro-RO', { hour: '2-digit', minute: '2-digit' });
  const item = document.createElement('div');
  item.className = 'event-item';
  item.innerHTML = `
    <span class="event-icon">${icon}</span>
    <span class="event-text">${text}</span>
    <span class="event-time">${now}</span>`;
  list.insertBefore(item, list.firstChild);

  // Max 20 events
  while (list.children.length > 20) list.removeChild(list.lastChild);
}

// ═══════════════════════════════════════════════
// VOICE ASSISTANT
// ═══════════════════════════════════════════════
function startVoice() {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SR) { toast('❌ Vocea AI nu e disponibilă în acest browser. Încearcă Chrome.'); return; }

  document.getElementById('voiceOverlay').style.display = 'flex';

  STATE.voice = new SR();
  STATE.voice.lang = 'ro-RO';
  STATE.voice.interimResults = false;

  STATE.voice.onresult = (e) => {
    const result = e.results[0][0].transcript.toLowerCase();
    document.getElementById('voiceResult').textContent = `"${result}"`;
    processVoiceCommand(result);
    setTimeout(stopVoice, 1500);
  };
  STATE.voice.onerror = () => { stopVoice(); toast('❌ Nu am putut înțelege'); };
  STATE.voice.start();
}

function stopVoice() {
  if (STATE.voice) { try { STATE.voice.stop(); } catch(e) {} STATE.voice = null; }
  document.getElementById('voiceOverlay').style.display = 'none';
}

function processVoiceCommand(cmd) {
  setText('voiceText', 'Procesez...');
  if (cmd.includes('pornit') || cmd.includes('start') || cmd.includes('pornești')) {
    STATE.engine = true; updateEngineUI(); speak('Motor pornit');
  } else if (cmd.includes('oprit') || cmd.includes('stop') || cmd.includes('oprești')) {
    STATE.engine = false; updateEngineUI(); speak('Motor oprit');
  } else if (cmd.includes('autonomie') || cmd.includes('cât am')) {
    const r = calcRange();
    speak(`Ai aproximativ ${r} kilometri autonomie`);
  } else if (cmd.includes('blocat') || cmd.includes('blochează')) {
    STATE.locked = true; speak('Mașina blocată');
  } else if (cmd.includes('deblocat') || cmd.includes('deblochează')) {
    STATE.locked = false; speak('Mașina deblocată');
  } else if (cmd.includes('faruri')) {
    remoteLights(); speak(STATE.lights ? 'Faruri pornite' : 'Faruri oprite');
  } else if (cmd.includes('consum')) {
    speak(`Consumul tău mediu este ${SETTINGS.realCons} litri la suta de kilometri`);
  } else {
    speak('Nu am înțeles comanda. Încearcă: pornit, oprit, autonomie, blocat');
  }
}

function speak(text) {
  if (!window.speechSynthesis) return;
  window.speechSynthesis.cancel();
  const u = new SpeechSynthesisUtterance(text);
  u.lang = 'ro-RO'; u.rate = 1; u.pitch = 1;
  window.speechSynthesis.speak(u);
}

// ═══════════════════════════════════════════════
// TIPS TICKER
// ═══════════════════════════════════════════════
let tipIndex = 0;
function renderTips() {
  const tip = ECO_TIPS[tipIndex % ECO_TIPS.length];
  const el = document.getElementById('tipsTicker');
  if (el) el.textContent = tip;
  tipIndex++;
  setTimeout(renderTips, 12000);
}

// ═══════════════════════════════════════════════
// MAINTENANCE REMINDERS
// ═══════════════════════════════════════════════
function renderMaintenance() {
  const brand = SETTINGS.brand;
  const items = [
    { icon: '🔧', name: 'Ulei motor', info: 'Diesel necesită ulei la 15.000-20.000 km', status: 'ok', detail: 'Verificat recent' },
    { icon: '🔵', name: 'Filtru particule (DPF)', info: 'Specific diesel — curăță la curse lungi', status: 'warn', detail: 'Fă o cursă de autostradă' },
    { icon: '💨', name: 'Filtru aer', info: 'Filtru înfundat = +5-10% consum', status: 'ok', detail: 'OK' },
    { icon: '⚙️', name: 'Filtru combustibil', info: `La ${brand}: schimb la 30.000 km`, status: 'ok', detail: 'OK' },
    { icon: '🌡️', name: 'Termostat', info: 'Termostat defect = motor rece = consum +15%', status: 'ok', detail: 'Verificat' },
    { icon: '🔋', name: 'Baterie 12V', info: 'Baterie slabă afectează sistemele start/stop', status: 'ok', detail: 'OK' },
  ];

  // This used to go in a separate section, now just show in toast or skip
  // since we simplified the HTML
}

// ═══════════════════════════════════════════════
// FUEL MODAL
// ═══════════════════════════════════════════════
function openFuelModal() {
  document.getElementById('mFuelLevel').value = SETTINGS.fuelLevel;
  document.getElementById('mFuelDisplay').textContent = SETTINGS.fuelLevel + '%';
  document.getElementById('mFuelPrice').value = SETTINGS.fuelPrice;
  document.getElementById('fuelModal').style.display = 'flex';
}
function closeFuelModal() {
  document.getElementById('fuelModal').style.display = 'none';
}
function saveFuel() {
  SETTINGS.fuelLevel = parseInt(document.getElementById('mFuelLevel').value);
  SETTINGS.fuelPrice = parseFloat(document.getElementById('mFuelPrice').value) || 7.25;
  localStorage.setItem('autopilot_settings', JSON.stringify(SETTINGS));
  // Sync settings tab
  document.getElementById('sFuelLevel').value = SETTINGS.fuelLevel;
  document.getElementById('sFuelLevelDisplay').textContent = SETTINGS.fuelLevel + '%';
  document.getElementById('sFuelPrice').value = SETTINGS.fuelPrice;
  closeFuelModal();
  updateRangeCard();
  updateLockScreen();
  toast('⛽ Nivel combustibil actualizat!');
}

// ═══════════════════════════════════════════════
// ESP32 GUIDE MODAL
// ═══════════════════════════════════════════════
function showESP32Guide() {
  document.getElementById('espModal').style.display = 'flex';
}
function closeESPModal() {
  document.getElementById('espModal').style.display = 'none';
}

// ═══════════════════════════════════════════════
// PARKING
// ═══════════════════════════════════════════════
function saveParking() {
  if (!navigator.geolocation) { toast('❌ GPS indisponibil'); return; }
  navigator.geolocation.getCurrentPosition(pos => {
    const lat = pos.coords.latitude.toFixed(5);
    const lon = pos.coords.longitude.toFixed(5);
    localStorage.setItem('parking', JSON.stringify({ lat, lon, time: new Date().toLocaleTimeString('ro-RO') }));
    toast(`🅿️ Parcare salvată: ${lat}, ${lon}`);
  }, () => toast('❌ Nu am putut accesa GPS-ul'));
}

// ═══════════════════════════════════════════════
// DATE / TIME
// ═══════════════════════════════════════════════
function updateDateTime() {
  const now = new Date();
  const el = document.getElementById('dateDisplay');
  if (el) el.textContent = now.toLocaleDateString('ro-RO', { weekday: 'long', day: 'numeric', month: 'long' });
}

function updateGreeting() {
  const h = new Date().getHours();
  const el = document.getElementById('greetingText');
  if (!el) return;
  if (h < 12) el.textContent = '☀️ Bună dimineața!';
  else if (h < 18) el.textContent = '🌤️ Bună ziua!';
  else el.textContent = '🌙 Bună seara!';
}

// ═══════════════════════════════════════════════
// TOAST
// ═══════════════════════════════════════════════
let toastTimeout;
function toast(msg) {
  const el = document.getElementById('toast');
  el.textContent = msg; el.classList.add('show');
  clearTimeout(toastTimeout);
  toastTimeout = setTimeout(() => el.classList.remove('show'), 3000);
}

// ═══════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════
function setText(id, val) {
  const el = document.getElementById(id);
  if (el) el.textContent = val;
}
function setWidth(id, pct) {
  const el = document.getElementById(id);
  if (el) el.style.width = Math.round(pct) + '%';
}

// ─── SVG Gradient defs ────────────────────────────────────
// Injected inline since we need them for canvas
document.addEventListener('DOMContentLoaded', () => {
  const svgDefs = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svgDefs.style.cssText = 'position:absolute;width:0;height:0;overflow:hidden';
  svgDefs.innerHTML = `
    <defs>
      <linearGradient id="lockGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#00d4ff"/>
        <stop offset="100%" style="stop-color:#7b2ff7"/>
      </linearGradient>
      <linearGradient id="hudGrad" x1="0%" y1="0%" x2="100%" y2="100%">
        <stop offset="0%" style="stop-color:#00d4ff"/>
        <stop offset="100%" style="stop-color:#7b2ff7"/>
      </linearGradient>
    </defs>`;
  document.body.prepend(svgDefs);
});
