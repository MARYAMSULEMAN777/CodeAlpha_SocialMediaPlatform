const commentForm = document.getElementById('comment-form');

if (commentForm) {
  commentForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const input = commentForm.querySelector('input[name="text"]');
    const text = input.value.trim();
    if (!text) return;

    try {
      const res = await fetch(commentForm.dataset.url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': CSRF_TOKEN,
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-Requested-With': 'XMLHttpRequest',
        },
        body: `text=${encodeURIComponent(text)}`,
      });
      const data = await res.json();

      if (data.success) {
        const noCommentsMsg = document.getElementById('no-comments-msg');
        if (noCommentsMsg) noCommentsMsg.remove();

        const list = document.getElementById('comment-list');
        const row = document.createElement('div');
        row.className = 'comment-item';
        row.innerHTML = `
          <div class="avatar avatar-sm">${data.username.charAt(0).toUpperCase()}</div>
          <div class="comment-bubble">
            <span class="comment-username">${data.username}</span>${data.text}
          </div>
        `;
        list.appendChild(row);
        input.value = '';

        const commentLinkSpan = document.querySelector('.comment-link span');
        if (commentLinkSpan) {
          commentLinkSpan.textContent = `${data.comment_count} comment${data.comment_count === 1 ? '' : 's'}`;
        }
      }
    } catch (err) {
      console.error('Could not post comment:', err);
    }
  });
}
