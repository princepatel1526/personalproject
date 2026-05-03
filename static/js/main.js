const steps = Array.from(document.querySelectorAll('.form-step'));
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const submitBtn = document.getElementById('submitBtn');
const progressBar = document.getElementById('progressBar');
const progressText = document.getElementById('progressText');

let currentStep = 0;

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

nextBtn.addEventListener('click', () => {
  if (!validateCurrentStep()) return;
  currentStep += 1;
  renderStep();
});

prevBtn.addEventListener('click', () => {
  currentStep -= 1;
  renderStep();
});

document.querySelectorAll('.option-card').forEach((card) => {
  card.addEventListener('click', () => {
    const error = card.closest('.form-step').querySelector('.error');
    error.classList.remove('show');
  });
});

document.getElementById('proposalForm').addEventListener('submit', (event) => {
  if (!validateCurrentStep()) {
    event.preventDefault();
  }
});

renderStep();
