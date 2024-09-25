const prevButton = document.querySelector('.prev-btn');
const nextButton = document.querySelector('.next-btn');
const submitButton = document.querySelector('.submit-btn');

function prevCompetition() {
  const selectedCompetition = document.querySelector('.field__competition.selected');
  const prevCompetition = selectedCompetition.previousElementSibling ?? null;
  if (!prevCompetition) return;
  selectedCompetition.classList.remove('selected');
  prevCompetition.classList.add('selected');
  nextButton.disabled = false;

  if (prevCompetition.classList.contains('first')) {
    prevButton.disabled = true;
  }
}

function nextCompetition() {
  const selectedCompetition = document.querySelector('.field__competition.selected');
  const nextCompetition = selectedCompetition.nextElementSibling ?? null;
  if (!nextCompetition) return;
  selectedCompetition.classList.remove('selected');
  nextCompetition.classList.add('selected');
  prevButton.disabled = false;

  if (nextCompetition.classList.contains('last')) {
    nextButton.disabled = true;
  }
}

const selectedCompetition = document.querySelector('.field__competition.selected');
if (selectedCompetition.classList.contains('last')) {
  nextButton.disabled = true;
}
if (selectedCompetition.classList.contains('first')) {
  prevButton.disabled = true;
}
