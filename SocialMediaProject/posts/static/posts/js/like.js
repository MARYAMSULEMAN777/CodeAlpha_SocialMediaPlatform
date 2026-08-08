document.querySelectorAll('.like-btn').forEach((btn) => {
  btn.addEventListener('click', async () => {
    const url = btn.dataset.url;
    try {
      const res = await fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': CSRF_TOKEN,
          'X-Requested-With': 'XMLHttpRequest',
        },
      });
      if (res.status === 403) {
        window.location.href = '/users/login/';
        return;
      }
      const data = await res.json();
      const countEl = btn.querySelector('.like-count');
      countEl.textContent = data.like_count;
      btn.classList.toggle('liked', data.liked);
      if (data.liked) {
        btn.classList.add('just-liked');
        setTimeout(() => btn.classList.remove('just-liked'), 200);
      }
    } catch (err) {
      console.error('Could not update like:', err);
    }
  });
});
