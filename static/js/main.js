function initQuestionsFlow() {
  const form = document.getElementById('proposalForm');
  if (!form) return;

  const steps = Array.from(document.querySelectorAll('.form-step'));
  const prevBtn = document.getElementById('prevBtn');
  const nextBtn = document.getElementById('nextBtn');
  const submitBtn = document.getElementById('submitBtn');
  const progressBar = document.getElementById('progressBar');
  const progressText = document.getElementById('progressText');
  const emojiBurst = document.getElementById('emojiBurst');
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

  function renderStep() {
    steps.forEach((step, idx) => step.classList.toggle('active', idx === currentStep));
    prevBtn.disabled = currentStep === 0;
    const isLastStep = currentStep === steps.length - 1;
    nextBtn.classList.toggle('hidden', isLastStep);
    submitBtn.classList.toggle('hidden', !isLastStep);
    progressBar.style.width = `${((currentStep + 1) / steps.length) * 100}%`;
    progressText.textContent = `Question ${currentStep + 1} of ${steps.length}`;
  }

  function validateCurrentStep() {
    const checked = steps[currentStep].querySelector('input[type="radio"]:checked');
    const error = steps[currentStep].querySelector('.error');
    if (!checked) {
      error.classList.add('show');
      return false;
    }
    error.classList.remove('show');
    return true;
  }

  form.querySelectorAll('input[type="radio"]').forEach((input) => {
    input.addEventListener('change', () => showEmojis(input.dataset.tone));
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
  const sync = () => {
    layer.style.display = enabled ? 'block' : 'none';
    toggle.textContent = `Hearts: ${enabled ? 'On' : 'Off'}`;
    if (enabled) renderHearts();
  };

  toggle.addEventListener('click', () => {
    enabled = !enabled;
    localStorage.setItem('hearts-enabled', enabled ? 'on' : 'off');
    sync();
  });

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => entry.target.classList.toggle('show', entry.isIntersecting));
  }, { threshold: 0.18 });
  document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

  sync();
}

initQuestionsFlow();
initLandingFX();
