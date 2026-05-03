function initRevealCards() {
  const cards = document.querySelectorAll('.reveal');
  if (!cards.length) return;
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => entry.target.classList.toggle('active', entry.isIntersecting));
  }, { threshold: 0.15 });
  cards.forEach((el) => observer.observe(el));
}

function initQuestionsFlow() {
  const form = document.getElementById('proposalForm');
  if (!form) return;

  const steps = Array.from(document.querySelectorAll('.form-step'));
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const progressBar = document.getElementById('progressBar');
  const progressText = document.getElementById('progressText');
  const emojiBurst = document.getElementById('emojiBurst');
  const likeScore = document.getElementById('likeScore');
  const scoreValue = document.getElementById('scoreValue');
  const scoreEmoji = document.getElementById('scoreEmoji');
  const finalResponseInput = document.getElementById('finalResponse');
  const mumbaiMsg = document.getElementById('mumbaiMsg');
  let currentStep = 0;

  const map = { positive: ['❤️', '😊', '✨'], neutral: ['🙂', '🤔'], negative: ['😅', '😶'] };

  const showEmojis = (tone = 'neutral') => {
    const emojis = map[tone] || map.neutral;
    emojiBurst.innerHTML = '';
    for (let i = 0; i < 4; i += 1) {
      const span = document.createElement('span');
      span.textContent = emojis[i % emojis.length];
      span.style.left = `${20 + i * 18}%`;
      span.style.animationDelay = `${i * 0.08}s`;
      emojiBurst.appendChild(span);
    }
  };

  function getSliderEmoji(value) {
    if (value <= 25) return '😐';
    if (value <= 50) return '🙂';
    if (value <= 75) return '😊';
    return '❤️';
  }

  function updateSliderUI() {
    const value = Number(likeScore.value);
    scoreValue.textContent = `${value}%`;
    scoreEmoji.textContent = getSliderEmoji(value);
  }

  function validateCurrentStep() {
    if (currentStep === 0 || currentStep === 1) {
      const checked = steps[currentStep].querySelector('input[type="radio"]:checked');
      const error = steps[currentStep].querySelector('.error');
      if (!checked) { error.classList.add('show'); return false; }
      error.classList.remove('show');
    }
    if (currentStep === 3 && !finalResponseInput.value) return false;
    return true;
  }

  function renderStep() {
    steps.forEach((step, idx) => step.classList.toggle('active', idx === currentStep));
    prevBtn.disabled = currentStep === 0;
    const isLastStep = currentStep === steps.length - 1;
    nextBtn.classList.toggle('hidden', isLastStep);
    progressBar.style.width = `${((currentStep + 1) / steps.length) * 100}%`;
    progressText.textContent = `Step ${currentStep + 1} of ${steps.length}`;
  }

  likeScore?.addEventListener('input', updateSliderUI);
  updateSliderUI();

  form.querySelectorAll('input[type="radio"]').forEach((input) => {
    input.addEventListener('change', () => showEmojis(input.dataset.tone));
  });

  form.querySelectorAll('.final-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      finalResponseInput.value = btn.dataset.response;
      if (btn.dataset.response.includes('Mumbai')) mumbaiMsg.classList.remove('hidden');
      if (btn.dataset.response.includes('Yes')) showEmojis('positive');
      form.submit();
    });
  });

  nextBtn.addEventListener('click', () => { if (validateCurrentStep()) { currentStep += 1; renderStep(); } });
  prevBtn.addEventListener('click', () => { currentStep -= 1; renderStep(); });
  form.addEventListener('submit', (event) => { if (!validateCurrentStep()) event.preventDefault(); });
  renderStep();
}

function initLandingFX() {
  const layer = document.getElementById('heartsLayer');
  const toggle = document.getElementById('toggleHearts');
  if (!layer || !toggle) return;
  const renderHearts = () => {
    layer.innerHTML = '';
    for (let i = 0; i < 12; i += 1) {
      const heart = document.createElement('span');
      heart.className = 'heart';
      heart.textContent = '❤';
      heart.style.left = `${Math.random() * 100}%`;
      heart.style.animationDuration = `${5 + Math.random() * 4}s`;
      heart.style.animationDelay = `${Math.random() * 2}s`;
      heart.style.fontSize = `${12 + Math.random() * 10}px`;
      layer.appendChild(heart);
    }
  };
  let enabled = localStorage.getItem('hearts-enabled') !== 'off';
  const sync = () => { layer.style.display = enabled ? 'block' : 'none'; toggle.textContent = `Hearts: ${enabled ? 'On' : 'Off'}`; if (enabled) renderHearts(); };
  toggle.addEventListener('click', () => { enabled = !enabled; localStorage.setItem('hearts-enabled', enabled ? 'on' : 'off'); sync(); });
  sync();
}

initRevealCards();
initQuestionsFlow();
initLandingFX();


function initKnowYouFlip() {
  const cards = window.knowYouCards;
  if (!cards || !cards.length) return;

  const wrap = document.getElementById('flipCard');
  const inner = document.getElementById('flipInner');
  const img = document.getElementById('cardImage');
  const title = document.getElementById('cardTitle');
  const desc = document.getElementById('cardDescription');
  const backTitle = document.getElementById('cardBackTitle');
  const progress = document.getElementById('knowProgress');
  const prevBtn = document.getElementById('prevCardBtn');
  const nextBtn = document.getElementById('nextCardBtn');
  const proceedBtn = document.getElementById('proceedBtn');
  if (!wrap || !inner || !img || !title || !desc || !backTitle || !progress || !prevBtn || !nextBtn || !proceedBtn) return;

  let idx = 0;

  const render = () => {
    const card = cards[idx];
    inner.classList.remove('flipped');
    wrap.classList.add('card-transition');
    img.src = `/static/images/${card.image}`;
    title.textContent = card.title;
    desc.textContent = card.description;
    backTitle.textContent = card.title;
    progress.textContent = `Card ${idx + 1} of ${cards.length}`;
    prevBtn.disabled = idx === 0;
    const last = idx === cards.length - 1;
    nextBtn.classList.toggle('hidden', last);
    proceedBtn.classList.toggle('hidden', !last);
    setTimeout(() => wrap.classList.remove('card-transition'), 220);
  };

  wrap.addEventListener('click', () => inner.classList.toggle('flipped'));
  wrap.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      inner.classList.toggle('flipped');
    }
  });
  nextBtn.addEventListener('click', () => { if (idx < cards.length - 1) { idx += 1; render(); } });
  prevBtn.addEventListener('click', () => { if (idx > 0) { idx -= 1; render(); } });

  render();
}

initKnowYouFlip();
