(() => {
  const cards = [...document.querySelectorAll('.pattern-card')];
  const search = document.getElementById('pattern-search');
  const area = document.getElementById('pattern-area');
  const collection = document.getElementById('pattern-collection');
  const type = document.getElementById('pattern-type');
  const review = document.getElementById('pattern-review');
  const count = document.getElementById('pattern-count');
  const empty = document.getElementById('pattern-empty');
  const clear = document.getElementById('pattern-clear');
  if (!cards.length || !search || !area || !collection || !type || !review || !count || !empty || !clear) return;

  function update() {
    const words = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    let shown = 0;
    for (const card of cards) {
      const text = card.textContent.toLocaleLowerCase();
      const matches = (!area.value || card.dataset.area === area.value) &&
        (!collection.value || card.dataset.collection === collection.value) &&
        (!type.value || card.dataset.types.split(' ').includes(type.value)) &&
        (!review.value || card.dataset.review === review.value) &&
        words.every(word => text.includes(word));
      card.hidden = !matches;
      if (matches) shown += 1;
    }
    count.textContent = `${shown} of ${cards.length} patterns shown`;
    empty.hidden = shown !== 0;
  }

  for (const control of [search, type, review]) {
    control.addEventListener(control === search ? 'input' : 'change', update);
  }
  area.addEventListener('change', () => {
    if (collection.value) {
      const selected = cards.find(card => card.dataset.collection === collection.value);
      if (selected && area.value && selected.dataset.area !== area.value) collection.value = '';
    }
    update();
  });
  collection.addEventListener('change', () => {
    if (collection.value) {
      const selected = cards.find(card => card.dataset.collection === collection.value);
      if (selected) area.value = selected.dataset.area;
    }
    update();
  });
  clear.addEventListener('click', () => {
    search.value = '';
    area.value = '';
    collection.value = '';
    type.value = '';
    review.value = '';
    update();
    search.focus();
  });
})();
